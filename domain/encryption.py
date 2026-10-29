# domain/utility/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings

# Ensure FERNET_KEY is loaded as bytes
key = settings.FERNET_KEY.encode() if isinstance(settings.FERNET_KEY, str) else settings.FERNET_KEY
cipher = Fernet(key)

def encrypt(text: str) -> str:
    if not text:
        return ''
    return cipher.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    if not token:
        return ''
    return cipher.decrypt(token.encode()).decode()