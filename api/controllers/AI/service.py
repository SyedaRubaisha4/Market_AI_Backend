import os
import json
from groq import Groq
from django.conf import settings

def generate_ai_content(product_name, price, description, brand_name):
    api_key = os.getenv("GROQ_API_KEY") or getattr(settings, "GROQ_API_KEY", None)
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Make sure it is in your .env file and settings.py loads it.")

    client = Groq(api_key=api_key)

    prompt = f"""
    You are an expert social media manager.
    Generate marketing content for this product:
    Product Name: {product_name}
    Price: {price}
    Description: {description}
    Brand: {brand_name}

    Return the response strictly in this JSON format:
    {{
        "caption": "A catchy social media caption with hashtags",
        "short_description": "A 1-sentence short description",
        "long_description": "A detailed 3-sentence description"
    }}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"} 
    )

    return response.choices[0].message.content