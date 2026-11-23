"""
Market AI - Cloudflare Workers AI
Text generation: Gemma 4
Text-to-image: FLUX.2 Klein 9B

Install:
    pip install requests pillow python-dotenv

Create a .env file beside this script:
    CLOUDFLARE_ACCOUNT_ID=your_account_id
    CLOUDFLARE_API_TOKEN=your_api_token

Run:
    python text_generation.py

Notes:
- FLUX.2 Klein 9B requires multipart/form-data, even for prompt-only generation.
- Do not manually set the multipart Content-Type header. requests creates the
  required boundary when the `files=` argument is used.
- FLUX.2 Klein 9B has a fixed 4-step process. Do not send `steps` or
  `num_steps`.
"""

import base64
import binascii
import io
import json
import os
import sys
from pathlib import Path

import requests
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv


# ----------------------------- Configuration -----------------------------

load_dotenv()

ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "").strip()

BASE_URL = (
    "https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run"
)

TEXT_MODEL = "@cf/google/gemma-4-26b-a4b-it"
IMAGE_MODEL = "@cf/black-forest-labs/flux-2-klein-9b"

OUTPUT_DIR = Path(__file__).resolve().parent / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REQUEST_TIMEOUT = 240
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024


def validate_credentials():
    if not ACCOUNT_ID or not API_TOKEN:
        raise ValueError(
            "Cloudflare credentials are missing. Add these values to the .env "
            "file beside this script:\n"
            "CLOUDFLARE_ACCOUNT_ID=your_account_id\n"
            "CLOUDFLARE_API_TOKEN=your_api_token"
        )


def model_url(model):
    validate_credentials()
    return f"{BASE_URL}/{model}"


def cloudflare_json_post(model, payload):
    """Send a JSON request (used by the text model)."""
    try:
        response = requests.post(
            model_url(model),
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not reach Cloudflare: {exc}") from exc

    if not response.ok:
        raise RuntimeError(
            f"Cloudflare returned HTTP {response.status_code} for {model}:\n"
            f"{response.text[:3000]}"
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"{model} returned a non-JSON response: {response.text[:1500]}"
        ) from exc

    if not data.get("success", False):
        raise RuntimeError(f"Cloudflare model error for {model}: {data}")

    return data


def cloudflare_flux_post(prompt, width=1024, height=1024, guidance=4.0):
    """
    Send FLUX.2 Klein 9B as multipart/form-data.

    Passing fields through `files=` makes requests generate a valid multipart
    boundary. Do not add Content-Type manually.
    """
    multipart_fields = {
        "prompt": (None, prompt),
        "width": (None, str(width)),
        "height": (None, str(height)),
        "guidance": (None, str(guidance)),
    }

    try:
        response = requests.post(
            model_url(IMAGE_MODEL),
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            files=multipart_fields,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not reach Cloudflare image model: {exc}") from exc

    if not response.ok:
        raise RuntimeError(
            f"Cloudflare returned HTTP {response.status_code} for {IMAGE_MODEL}:\n"
            f"{response.text[:3000]}"
        )

    return response


# --------------------------- Marketing Text AI ---------------------------

def extract_text_response(data):
    """Support Cloudflare's text-generation response shapes."""
    result = data.get("result") or {}

    text = result.get("response")
    if isinstance(text, str) and text.strip():
        return text.strip(), None

    choices = result.get("choices") or []
    if choices:
        choice = choices[0]
        text = choice.get("text")

        if not text:
            message = choice.get("message") or {}
            text = message.get("content")

        if isinstance(text, str) and text.strip():
            return text.strip(), choice.get("finish_reason")

    return None, None


def generate_product_text(name, category, price, details):
    prompt = f"""
Create concise, useful e-commerce marketing copy using only the product facts
provided below.

Product name: {name}
Product category: {category}
Price: {price}
Verified product details supplied by the user: {details or "No additional details supplied."}

Return these seven sections:
1. Improved Product Name
2. Short Description (2 sentences)
3. Full Product Description (one short paragraph)
4. SEO Title
5. SEO Meta Description
6. Instagram Caption with relevant hashtags
7. Facebook Marketing Post

Accuracy rules:
- Do not invent ingredients, SPF rating, skin benefits, certifications,
  protection claims, materials, sizes, warranties, or other features.
- If a detail is unclear or misspelled, do not guess what it means.
- Do not repeat sentences.
- Do not write instructions to yourself.
- Keep each section concise and complete.
"""

    data = cloudflare_json_post(
        TEXT_MODEL,
        {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a careful e-commerce copywriter. Produce "
                        "original, concise copy. Never invent product facts."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 2200,
            "temperature": 0.2,
            "repetition_penalty": 1.1,
        },
    )

    text, finish_reason = extract_text_response(data)

    if not text:
        raise RuntimeError(
            "Cloudflare reported success but returned no extractable text. "
            f"Response: {data}"
        )

    if finish_reason == "length":
        print(
            "Warning: The text model reached its output-token limit. "
            "The saved text may be incomplete."
        )

    return text


# ----------------------------- Image Generation ---------------------------
PHOTOGRAPHY_STYLES = {
    "studio": (
        "Professional studio product photography, single product package, "
        "clean neutral background, soft lighting and natural shadows."
    ),

    "lifestyle": (
        "A single product package displayed on a clean bathroom vanity, "
        "bright natural daylight, elegant minimal surroundings."
    ),

    "detail": (
        "Professional packaging-focused product photograph. "
        "Show the complete product package from a three-quarter angle, "
        "with clear visibility of its shape, cap and outer packaging. "
        "Use a plain background and soft studio lighting."
    ),

    "campaign": (
        "Premium commercial product advertising photography, "
        "elegant background, balanced composition, "
        "professional lighting and realistic shadows."
    ),
}
def build_image_prompt(name, category, details, style_description):
    # Do not ask the image model to print packaging text or logos: generated
    # lettering is often inaccurate. The real product label can be added later.
    if isinstance(details, str):
        verified_details = details.strip() or "No additional details supplied."
    elif details is None:
        verified_details = "No additional details supplied."
    else:
        verified_details = json.dumps(details, ensure_ascii=False)

    return f"""
Create one photorealistic commercial product photograph for an online store.

Product: {name}
Category: {category}
User-provided product details: {verified_details}

Photography direction:
{style_description}

Visual requirements:
- Show one plausible product package as the main subject.
- Make the image look like professional real-world product photography.
- Use physically plausible lighting, realistic shadows and a clear composition.
- Use a square composition.
- Do not add people, extra products, promotional banners, watermarks,
  readable text, fake brand names, fake logos, or unsupported claims.
- Keep the packaging clean and visually believable.
"""


def save_flux_image(response, output_path):
    """
    FLUX.2 Klein 9B returns a JSON result containing a Base64 `image` field.
    Also accept raw image bytes in case the endpoint returns an image directly.
    """
    content_type = response.headers.get("Content-Type", "").lower()
    image_bytes = None

    if "json" in content_type or response.content[:1] == b"{":
        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                f"Image endpoint returned invalid JSON: {response.text[:1500]}"
            ) from exc

        if not data.get("success", False):
            raise RuntimeError(f"Image generation failed: {data}")

        result = data.get("result") or {}
        encoded_image = result.get("image")

        if not encoded_image:
            raise RuntimeError(
                "Cloudflare returned success but no result.image field. "
                f"Response: {data}"
            )

        try:
            image_bytes = base64.b64decode(encoded_image, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise RuntimeError("Cloudflare returned invalid Base64 image data.") from exc
    else:
        image_bytes = response.content

    if not image_bytes:
        raise RuntimeError("Cloudflare returned an empty image.")

    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            image.load()
            image.convert("RGB").save(output_path, format="PNG")
    except (UnidentifiedImageError, OSError) as exc:
        raise RuntimeError(
            "Cloudflare response was not a valid image. "
            f"Content-Type: {content_type or 'unknown'}"
        ) from exc


def generate_one_product_image(name, category, details, style_name, style_description):
    prompt = build_image_prompt(
        name=name,
        category=category,
        details=details,
        style_description=style_description,
    )

    response = cloudflare_flux_post(
        prompt=prompt,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        guidance=4.0,
    )

    output_path = OUTPUT_DIR / f"product_{style_name}.png"
    save_flux_image(response, output_path)
    return output_path.resolve()


def generate_product_images(name, category, details):
    generated = []
    failures = []

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
            failures.append((style_name, str(exc)))
            print(f"{style_name.capitalize()} image failed: {exc}")

    return generated, failures


# ----------------------------------- Main ----------------------------------

def main():
    print("=" * 68)
    print("Market AI - Cloudflare Workers AI text-to-image test")
    print("=" * 68)

    validate_credentials()

    name = input("Product name: ").strip()
    category = input("Product category: ").strip()
    price = input("Price and currency: ").strip()
    details = input("Product details (optional; enter only verified facts): ").strip()

    if not name or not category:
        raise ValueError("Product name and category are required.")

    # Text generation is independent: an image request can still run if text
    # generation fails.
    print("\nGenerating marketing text...")

    try:
        marketing_text = generate_product_text(
            name=name,
            category=category,
            price=price,
            details=details,
        )
        text_path = OUTPUT_DIR / "product_marketing.txt"
        text_path.write_text(marketing_text, encoding="utf-8")

        print("\n--- GENERATED MARKETING CONTENT ---")
        print(marketing_text)
        print(f"\nMarketing content saved to: {text_path.resolve()}")

    except Exception as exc:
        print(f"\nMarketing text generation failed: {exc}")
        print("Continuing with image generation...")

    print("\nStarting FLUX.2 Klein 9B text-to-image generation...")

    images, failures = generate_product_images(
        name=name,
        category=category,
        details=details,
    )

    print("\n" + "=" * 68)
    print(f"Successfully generated {len(images)} image(s):")

    for image_path in images:
        print(f" - {image_path}")

    if failures:
        print(f"\nFailed image styles: {len(failures)}")
        for style, error in failures:
            print(f" - {style}: {error}")

    print(f"\nOutput folder: {OUTPUT_DIR.resolve()}")
    print("=" * 68)

    if not images:
        raise RuntimeError(
            "No images were generated. Review the Cloudflare errors above."
        )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as exc:
        print(f"\nERROR: {exc}")
        sys.exit(1)
