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

# EMAIL HELPERS

def send_welcome_email(user):
    """Send welcome email to user."""
    try:
        send_mail(
            subject='Welcome to Market AI!',
            message=f'Hi {user.username},\n\nWelcome to Market AI! Your account has been created successfully.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email sending failed: {e}")


def send_password_reset_email(user):
    """Email Password Reset Link."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
    send_mail(
        subject='Password Reset Request',
        message=f'Click this link to reset your password:\n\n{reset_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


# JWT TOKEN HELPER

def generate_tokens(user):
    """JWT access +Generate refresh tokens."""
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# AUTH SERVICE FUNCTIONS

def register_user(data):
    """Validations and User Creation"""
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # 1. Required fields
    if not username or not email or not password:
        raise ValidationError("Username, email, and password are required.")
    
    # 2. Email format validation
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError("Invalid email format. Please enter a valid email address.")
        

    # 4. Password strength
    try:
        validate_password(password)
    except ValidationError as e:
        raise ValidationError(f"Password error: {', '.join(e.messages)}")
    # 4. Password strength ( Rules)
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one UPPERCASE letter (A-Z).")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter (a-z).")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one number (0-9).")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character (!@#$%^&*).")
    # 5. Username check
    if User.objects.filter(username__iexact=username).exists():
        raise ValidationError("Username already taken.")

    # 6. Email exists check
    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError("Email already registered.")

    
    # 7. Create User
    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            email=email.lower(),
            password=password,
        )
        send_welcome_email(user)
        return user


def login_user(data):
    """Authenticate User + Return JWT tokens"""
    email = data.get("email")
    password = data.get("password")
    
    # Validations
    if not email or not password:
        raise ValidationError("Email and password are required.")
        
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError("Invalid email format. Please enter a valid email address.")

    # Pehle email se user dhoondo
    try:
        user_obj = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        raise ValidationError("Invalid email or password.")

    # Ab authenticate karo
    user = authenticate(username=user_obj.username, password=password)

    if not user:
        raise ValidationError("Invalid email or password.")

    if not user.is_active:
        raise ValidationError("User account is disabled.")

    tokens = generate_tokens(user)

    return {
        'user': user,
        'tokens': tokens,
    }


def logout_user(refresh_token):
    """Blacklists Refresh Token"""
    from rest_framework_simplejwt.tokens import RefreshToken, TokenError
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return True
    except TokenError:
        return False


def change_password(user, old_password, new_password):
    """Change User's password"""
    if not user.check_password(old_password):
        raise ValidationError("Old password is incorrect.")
    user.set_password(new_password)
    user.save()
    return True


def request_password_reset(email):
    """Send Password reset email"""
    try:
        user = User.objects.get(email__iexact=email)
        send_password_reset_email(user)
        return True
    except User.DoesNotExist:
        return True