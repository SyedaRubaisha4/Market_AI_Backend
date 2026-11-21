from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError 
from django.core.validators import validate_email    
from django.contrib.auth.password_validation import validate_password 
import re

User = get_user_model()
def get_profile(user):
    from domain.models.Brand import Brand 

    brand = (
        Brand.objects.filter(user=user, action_type=1)
        .order_by("-created_on")
        .first()
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": getattr(user, 'full_name', ''),
        "is_active": user.is_active,
        "date_joined": user.date_joined,
        "is_onboarded": brand is not None,
        "brand_id": brand.id if brand is not None else None,
    }

def update_profile(user, data):
    username = data.get('username')
    email = data.get('email')
    full_name = data.get('full_name')

    if username and username.lower() != user.username.lower():
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Username already taken.")
        user.username = username

    if email and email.lower() != user.email.lower():
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Invalid email format.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Email already registered.")
        user.email = email.lower()

    if full_name is not None:
        user.full_name = full_name

    user.save()
    return user

def delete_profile(user):
    user.is_active = False
    user.save()
    return True
    
def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValidationError("User with this ID does not exist.")