"""
Market AI: Cloudflare Workers AI product marketing + image-to-image test.

Install:
    pip install requests pillow python-dotenv

Create a .env file in the same directory:
    CLOUDFLARE_ACCOUNT_ID=your_account_id
    CLOUDFLARE_API_TOKEN=your_api_token

Run:
    python market_ai_cloudflare_test.py

This script:
1. Generates marketing text with Llama.
2. Asks for a local product-image path.
3. Sends that image to SDXL-Lightning using image_b64.
4. Saves up to four image variations in ./generated.

Note: AI image generation may alter product labels/logos. Test with a copy of
your product image first. Confirm current model access and account limits in
Cloudflare's dashboard.
"""

import base64
import io
import os
import sys
from pathlib import Path

import requests
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv


# ----------------------------- Configuration -----------------------------

load_dotenv()

# API_TOKEN = "cfut_m59aszZWmlth5XgCFPN8Sm1BYsBjN8z3WB9Umpgp2d81869f"
# ACCOUNT_ID="91aa2b775e1a8ef9be878425e2f3be59"
ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

BASE_URL = (
    "https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run"
)

TEXT_MODEL = "@cf/meta/llama-3.1-8b-instruct"
IMAGE_MODEL = "@cf/bytedance/stable-diffusion-xl-lightning"

OUTPUT_DIR = Path("generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REQUEST_TIMEOUT = 180
IMAGE_SIZE = 1024


# ------------------------------- Utilities -------------------------------

def validate_credentials():
    if not ACCOUNT_ID or not API_TOKEN:
        raise ValueError(
            "Cloudflare credentials are missing.\n"
            "Create a .env file beside this script containing:\n"
            "CLOUDFLARE_ACCOUNT_ID=your_account_id\n"
            "CLOUDFLARE_API_TOKEN=your_api_token"
        )


def cloudflare_post(model, payload):
    """Post JSON to a Cloudflare Workers AI model endpoint."""
    validate_credentials()

    url = f"{BASE_URL}/{model}"
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {API_TOKEN}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not reach Cloudflare: {exc}") from exc

    if not response.ok:
        raise RuntimeError(
            f"Cloudflare returned HTTP {response.status_code} for {model}:\n"
            f"{response.text[:2000]}"
        )

    return response


def save_response_image(response, output_path):
    """Validate the returned image bytes and save as a PNG."""
    content_type = response.headers.get("Content-Type", "").lower()
    raw_bytes = response.content

    if "json" in content_type or not raw_bytes:
        try:
            details = response.json()
        except ValueError:
            details = response.text[:1500]
        raise RuntimeError(
            "Expected image bytes, but Cloudflare returned "
            f"{content_type or 'an unknown content type'}: {details}"
        )

    try:
        with Image.open(io.BytesIO(raw_bytes)) as image:
            image.load()
            image.convert("RGB").save(output_path, format="PNG")
    except (UnidentifiedImageError, OSError) as exc:
        raise RuntimeError(
            "Cloudflare responded, but the response was not a readable image. "
            f"Content-Type: {content_type or 'unknown'}"
        ) from exc


# --------------------------- Marketing Text AI ---------------------------

def generate_product_text(name, category, price, details):
    prompt = f"""
You are an e-commerce marketing writer.

Create marketing content using only the verified product information below.
Do not invent materials, ingredients, certifications, warranties, features,
or product claims.

Product name: {name}
Category: {category}
Price: {price}
Verified details: {details}

Return these clearly labeled sections:
1. Improved Product Name
2. Short Description
3. Full Product Description
4. SEO Title
5. SEO Meta Description
6. Instagram Caption with relevant hashtags
7. Facebook Marketing Post

Use clear, natural, attractive language.
"""

    response = cloudflare_post(
        TEXT_MODEL,
        {
            "prompt": prompt,
            "max_tokens": 1200,
        },
    )

    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"Text model returned non-JSON data: {response.text[:1000]}"
        ) from exc

    if not result.get("success", False):
        raise RuntimeError(f"Text generation failed: {result}")

    text = result.get("result", {}).get("response")
    if not text:
        raise RuntimeError(f"No text was returned by the text model: {result}")

    return text


# ---------------------------- Text-to-Image ------------------------------

PHOTOGRAPHY_STYLES = {
    "studio": (
        "Premium commercial studio product photography, softbox lighting, "
        "clean light neutral background, realistic contact shadows, crisp focus."
    ),
    "lifestyle": (
        "Elegant lifestyle product photography in a believable setting suitable "
        "for the product category, natural window light, tasteful props, "
        "realistic surfaces and shadows."
    ),
    "detail": (
        "Close-up commercial product photography showing realistic surface "
        "texture and packaging details, sharp focus, controlled reflections "
        "and professional studio lighting."
    ),
    "campaign": (
        "Premium e-commerce advertising photography, refined composition, "
        "sophisticated background, balanced negative space, realistic lighting."
    ),
}


def generate_one_product_image(name, category, details, style_name, style_description):
    """
    Generate an image from a text prompt only.
    No uploaded/reference image is sent to Cloudflare.
    """
    prompt = f"""
Create a professional commercial product photograph for an online store.

PRODUCT INFORMATION
Product name: {name}
Category: {category}
Verified product details: {details}

PHOTOGRAPHY STYLE
{style_description}

VISUAL REQUIREMENTS
Create one realistic product as the main subject. Make the product look
plausible for its category. Use professional composition, natural contact
shadows, physically plausible lighting, clear focus, and a polished
e-commerce photography style.

Do not add unsupported product claims, extra products, promotional banners,
watermarks, or unnecessary text. Avoid gibberish labels and fake logos.
The result should be a single square product photograph.
"""

    payload = {
        "prompt": prompt,
        "negative_prompt": (
            "blurry, low quality, distorted object, malformed packaging, "
            "duplicate products, gibberish text, fake logo, watermark, "
            "unrealistic reflections, floating object, collage, banner"
        ),
        "width": IMAGE_SIZE,
        "height": IMAGE_SIZE,
        "num_steps": 8,
        "guidance": 7.5,
    }

    response = cloudflare_post(IMAGE_MODEL, payload)
    output_path = OUTPUT_DIR / f"product_{style_name}.png"
    save_response_image(response, output_path)
    return output_path.resolve()


def generate_product_images(name, category, details):
    """Generate four text-to-image style variations."""
    generated = []

    for style_name, style_description in PHOTOGRAPHY_STYLES.items():
        print(f"\nGenerating {style_name} image...")
        try:
            output_path = generate_one_product_image(
                name=name,
                category=category,
                details=details,
                style_name=style_name,
                style_description=style_description,
            )
            generated.append(str(output_path))
            print(f"Saved image: {output_path}")
        except Exception as exc:
            print(f"{style_name.capitalize()} image failed: {exc}")

    if not generated:
        raise RuntimeError(
            "No images were generated. Check the Cloudflare API error above."
        )

    return generated


# --------------------------------- Main ----------------------------------

def main():
    print("=" * 68)
    print("Market AI - Cloudflare Workers AI text-to-image test")
    print("=" * 68)

    validate_credentials()

    name = input("Product name: ").strip()
    category = input("Product category: ").strip()
    price = input("Price and currency: ").strip()
    details = input("Product details: ").strip()

    if not name or not category:
        print("Product name and category are required.")
        sys.exit(1)

    product = {
        "name": name,
        "category": category,
        "price": price,
        "details": details,
    }

    # Marketing text is separate from image generation. If text generation
    # fails, image generation can still proceed.
    try:
        print("\nGenerating marketing text...")
        marketing_text = generate_product_text(**product)
        text_path = OUTPUT_DIR / "product_marketing.txt"
        text_path.write_text(marketing_text, encoding="utf-8")
        print("\n--- GENERATED MARKETING CONTENT ---")
        print(marketing_text)
        print(f"\nMarketing content saved to: {text_path.resolve()}")
    except Exception as exc:
        print(f"\nMarketing text generation failed: {exc}")
        print("Continuing with image generation...")

    print("\nStarting text-to-image generation...")
    images = generate_product_images(
        name=name,
        category=category,
        details=details,
    )

    print("\n" + "=" * 68)
    print(f"Successfully generated {len(images)} image(s):")
    for image_path in images:
        print(f" - {image_path}")
    print(f"\nOutput folder: {OUTPUT_DIR.resolve()}")
    print("=" * 68)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"\nERROR: {exc}")
        sys.exit(1)
