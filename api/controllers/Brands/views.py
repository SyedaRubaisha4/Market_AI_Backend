from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .service import create_brand, get_user_brands, get_brand_by_id, update_brand, delete_brand
from domain.serializers.serializers import BrandSerializer

# --- 1. CREATE BRAND ---
@swagger_auto_schema(
    method='post',
    security=[{'Bearer': []}],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['business_name'],
        properties={
            'business_name': openapi.Schema(type=openapi.TYPE_STRING),
            'business_type': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'tone_of_voice': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            'target_customer_class': openapi.Schema(type=openapi.TYPE_STRING),
            'customer_type': openapi.Schema(type=openapi.TYPE_STRING),
            'language': openapi.Schema(type=openapi.TYPE_STRING),
            'words_to_avoid': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            'brand_keywords': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
        },
    ),
    tags=['Brand']
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])           
def view_create_brand(request):
    if not request.user.is_authenticated:
        return Response({"success": False, "errors": "Auth required."}, status=401)
    try:
        brand = create_brand(request.user, request.data)
        return Response(
            {
                "success": True,
                "id": brand.id,
                "data": BrandSerializer(brand).data,
                "message": "Brand created.",
            },
            status=201,
        )
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=400)

# --- 2. LIST BRANDS ---
@swagger_auto_schema(method='get', security=[{'Bearer': []}], tags=['Brand'])
@api_view(['GET'])
def view_list_brands(request):
    if not request.user.is_authenticated:
        return Response({"success": False, "errors": "Auth required."}, status=401)
    
    brands = get_user_brands(request.user)
    data = [{"id": b.id, "business_name": b.business_name, "status": b.status} for b in brands]
    return Response({"success": True, "brands": data}, status=200)

# --- 3. GET BRAND BY ID ---
@swagger_auto_schema(
    method='get', security=[{'Bearer': []}], tags=['Brand'],
    manual_parameters=[
        openapi.Parameter(
            'brand_id',
            openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            format='uuid',
        )
    ]
)
@api_view(['GET'])
def view_get_brand(request, brand_id):
    if not request.user.is_authenticated:
        return Response({"success": False, "errors": "Auth required."}, status=401)
    try:
        brand = get_brand_by_id(request.user, brand_id)
        return Response({"success": True, "data": {
            "id": brand.id, "business_name": brand.business_name, "description": brand.description,
            "tone_of_voice": brand.tone_of_voice, "brand_keywords": brand.brand_keywords
        }}, status=200)
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=404)

# --- 4. UPDATE BRAND ---
@swagger_auto_schema(
    method='patch', security=[{'Bearer': []}], tags=['Brand'],
    manual_parameters=[
        openapi.Parameter(
            'brand_id',
            openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            format='uuid',
        )
    ],
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'business_name': openapi.Schema(type=openapi.TYPE_STRING),
        'description': openapi.Schema(type=openapi.TYPE_STRING),
        'status': openapi.Schema(type=openapi.TYPE_STRING),
    })
)
@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_update_brand(request, brand_id):
    if not request.user.is_authenticated:
        return Response({"success": False, "errors": "Auth required."}, status=401)
    try:
        brand = update_brand(request.user, brand_id, request.data)
        return Response({"success": True, "message": "Brand updated."}, status=200)
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=400)

# --- 5. DELETE BRAND ---
@swagger_auto_schema(
    method='delete', security=[{'Bearer': []}], tags=['Brand'],
    manual_parameters=[
        openapi.Parameter(
            'brand_id',
            openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            format='uuid',
        )
    ]
)
@api_view(['DELETE'])
def view_delete_brand(request, brand_id):
    if not request.user.is_authenticated:
        return Response({"success": False, "errors": "Auth required."}, status=401)
    try:
        delete_brand(request.user, brand_id)
        return Response({"success": True, "message": "Brand deactivated."}, status=200)
    except Exception as e:
        return Response({"success": False, "errors": str(e)}, status=400)