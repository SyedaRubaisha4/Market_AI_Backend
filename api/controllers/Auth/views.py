from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError
from .service import register_user, login_user, logout_user,change_password,request_password_reset

@swagger_auto_schema(
    method='post',
    operation_summary = 'Register a new user',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password', ],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Email user name"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="Enter email"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="Enter Password"),
        },
    ),
    tags=['Auth']
)
@api_view(['POST'])
def view_register_user(request):
    try:
        user = register_user(request.data)
        
    except Exception as e:
        errors = "; ".join(e.messages) if isinstance(e, ValidationError) else str(e)
        return Response(
            {"success": False, "errors": errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "success": True,
            "message": "User registered successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@swagger_auto_schema(
    method='post',
    operation_summary = 'Login a user',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[ 'email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="Enter email"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="Enter Password"),
        },
    ),
    tags=['Auth']
)
@api_view(['POST'])
def view_login_user(request):
    try:
        result = login_user(request.data)
        
    except Exception as e:
        return Response(
            {"success": False, "errors": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not result:
        return Response(
            {"success": False, "errors": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response(
        {
            "success": True,
            "message": "Login successful.",
            "user": {
                "id": result['user'].id,
                "username": result['user'].username,
                "email": result['user'].email,
            },
            "tokens": result['tokens'],
        },
        status=status.HTTP_200_OK,
    )

@swagger_auto_schema(
    method='post',
    operation_summary = 'Logout a  user',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh'],
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    tags=['Auth']
)
@api_view(['POST'])
def view_logout_user(request):
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response(
            {"success": False, "errors": "refresh token required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    success = logout_user(refresh_token)

    if not success:
        return Response(
            {"success": False, "errors": "Invalid token."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"success": True, "message": "Logged out successfully."},
        status=status.HTTP_200_OK,
    )
    
@swagger_auto_schema(
    method='post',
    operation_summary = 'Change password of logged in  user',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['old_password', 'new_password'],
        properties={
            'old_password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
        },
    ),
    tags=['User']
)
@api_view(['POST'])
def view_change_password(request):
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({"success": False, "errors": "Old and new password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if not request.user.is_authenticated:
           return Response({"success": False, "errors": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
            
        change_password(request.user, old_password, new_password)
        return Response({"success": True, "message": "Password changed"})
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary = 'Reset password of logged out  user',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    tags=['User']
)
@api_view(['POST'])
def view_request_password_reset(request):
    email = request.data.get('email')
    if not email:
        return Response({"success": False, "errors": "Email required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        request_password_reset(email)
        return Response({"success": True, "message": "Reset link sent if email exists"})
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    