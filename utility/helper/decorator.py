from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .jwthelper import verify_jwt_token, generate_jwt_token
# from domain.models.auth import Auth

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Skip JWT check for OPTIONS requests (CORS preflight)
        # Browsers send OPTIONS requests without Authorization header
        if request.method == 'OPTIONS':
            result = view_func(request, *args, **kwargs)
            # If view returned a Response, add CORS headers and return it
            if isinstance(result, Response):
                _add_cors_headers_to_response(result, request)
                return result
            # Create a new Response for OPTIONS
            response = Response(status=status.HTTP_200_OK)
            _add_cors_headers_to_response(response, request)
            return response
        
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            # Create Response with explicit CORS headers
            response = Response(
                {"success": False, "message": "Missing or invalid token"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            _add_cors_headers_to_response(response, request)
            return response

        token = auth_header.split(" ")[1]

        try:
            payload = verify_jwt_token(token)
            request.user_id = payload["user_id"]
            request.user_email = payload["email"]

            # Optional: generate new token (auto refresh)
            new_token = generate_jwt_token(payload["user_id"], payload["email"])
            request.new_token = new_token

        except Exception as e:
            # Create Response with explicit CORS headers
            response = Response(
                {"success": False, "message": str(e)}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            _add_cors_headers_to_response(response, request)
            return response

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def _add_cors_headers_to_response(response, request):
    """
    Explicitly add CORS headers to response to ensure they're always present.
    This is critical for early returns from decorators.
    """
    origin = request.META.get('HTTP_ORIGIN')
    
    # Add Access-Control-Allow-Origin
    if getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False):
        if origin:
            response['Access-Control-Allow-Origin'] = origin
        else:
            response['Access-Control-Allow-Origin'] = '*'
    elif hasattr(settings, 'CORS_ALLOWED_ORIGINS') and settings.CORS_ALLOWED_ORIGINS:
        if origin and origin in settings.CORS_ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin
    
    # Add Access-Control-Allow-Methods
    if hasattr(settings, 'CORS_ALLOW_METHODS'):
        response['Access-Control-Allow-Methods'] = ', '.join(settings.CORS_ALLOW_METHODS)
    
    # Add Access-Control-Allow-Headers
    if hasattr(settings, 'CORS_ALLOW_HEADERS'):
        response['Access-Control-Allow-Headers'] = ', '.join(settings.CORS_ALLOW_HEADERS)
    
    # Add Access-Control-Allow-Credentials
    if getattr(settings, 'CORS_ALLOW_CREDENTIALS', False):
        response['Access-Control-Allow-Credentials'] = 'true'
    
    # Add Access-Control-Expose-Headers
    if hasattr(settings, 'CORS_EXPOSE_HEADERS'):
        response['Access-Control-Expose-Headers'] = ', '.join(settings.CORS_EXPOSE_HEADERS)
    
    # Add Access-Control-Max-Age for preflight caching
    if hasattr(settings, 'CORS_PREFLIGHT_MAX_AGE'):
        response['Access-Control-Max-Age'] = str(settings.CORS_PREFLIGHT_MAX_AGE)
