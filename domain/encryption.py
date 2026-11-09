# domain/utility/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

configured_key = settings.FERNET_KEY
if not configured_key:
    raise ImproperlyConfigured(
        "FERNET_KEY is not set. Add a Fernet key to your environment or .env file. "
        "Generate one with: python -c \"from cryptography.fernet import Fernet; "
        "print(Fernet.generate_key().decode())\""
    )

key = configured_key.encode("ascii") if isinstance(configured_key, str) else configured_key
try:
    cipher = Fernet(key)
except (TypeError, ValueError) as exc:
    raise ImproperlyConfigured(
        "FERNET_KEY must be a valid Fernet key (32 url-safe base64-encoded bytes)."
    ) from exc

def encrypt(text: str) -> str:
    if not text:
        return ''
    return cipher.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    if not token:
        return ''
    return cipher.decrypt(token.encode()).decode()