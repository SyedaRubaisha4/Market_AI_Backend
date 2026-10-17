
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Find the Market project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Load the .env file from the project root
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Check your .env file."
    )

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Write a product description for a black leather handbag."
        }
    ],
)

print(response.choices[0].message.content)
