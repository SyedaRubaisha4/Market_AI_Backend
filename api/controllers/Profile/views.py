from .service import get_profile, update_profile, delete_profile, get_user_by_id
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_summary="Get Current User Profile",
    security=[{'Bearer': []}],
    tags=['Profile']
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])        
def view_get_profile(request):
    profile_data = get_profile(request.user)
    return Response({"success": True, "user": profile_data}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='patch',
    operation_summary="Update User Profile",
    security=[{'Bearer': []}],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="Naya Username"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="Naya Email"),
            'full_name': openapi.Schema(type=openapi.TYPE_STRING, description="Naya Full Name"),
        },
    ),
    tags=['Profile']
)
@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])       
def view_update_profile(request):
    try:
        updated_user = update_profile(request.user, request.data)
        return Response({
            "success": True, 
            "message": "Profile updated successfully.",
            "user": get_profile(updated_user)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    operation_summary="Deactivate User Account",
    operation_description="Yeh account ko delete nahi karta, balke deactivate (inactive) kar deta hai.",
    security=[{'Bearer': []}],
    tags=['Profile']
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])       
def view_delete_profile(request):
    try:
        delete_profile(request.user)
        return Response({"success": True, "message": "Account deactivated successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(
    method='get',
    operation_summary="Get User by ID",
    manual_parameters=[
        openapi.Parameter('user_id', openapi.IN_PATH, description="ID of the user", type=openapi.TYPE_INTEGER)
    ],
    tags=['Profile']
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])      
def view_get_user_by_id(request, user_id):
    try:
        user = get_user_by_id(user_id)
        return Response({"success": True, "user": get_profile(user)}, status=200)
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=404)