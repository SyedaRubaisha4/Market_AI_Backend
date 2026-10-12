import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt_token(user_id, email):
    """Generate a new JWT token (valid for 1 hour)."""
    payload = {
        "user_id": str(user_id),
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def verify_jwt_token(token):
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def get_user_id_from_token(token):
    """Verify the JWT token and return the user_id from the payload. Raises on invalid or expired token."""
    payload = verify_jwt_token(token)
    return payload.get("user_id")
