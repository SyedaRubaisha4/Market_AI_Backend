from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .service import (
    create_or_update_product,
    get_products,
    get_product_by_id,
    delete_product,
)
from domain.models.Product import Product
from domain.models.ProductImage import ProductImage
from rest_framework.response import Response
@api_view(['POST', 'PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_add_or_update_product(request, product_id=None): 
    image_files = []
    if request.content_type and request.content_type.startswith('multipart'):
        image_files = request.FILES.getlist('product_images')

    return create_or_update_product(
        request.data,
        image_files,
        request=request,
        product_id=product_id 
    )

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_get_products(request):
    return get_products(request)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_get_product_by_id(request, product_id):
    return get_product_by_id(product_id, request)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_delete_product(request, product_id):
    return delete_product(product_id, request)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_enhance_image(request, product_id):
    try:
        product = Product.objects.get(id=product_id, brand__user=request.user)
        image = ProductImage.objects.filter(product=product, action_type=1).first()
        
        if not image:
            return Response({"success": False, "errors": "No image found for this product."}, status=404)
            
        return Response({
            "success": True, 
            "image_url": image.image_url
        }, status=200)
    except Product.DoesNotExist:
        return Response({"success": False, "errors": "Product not found."}, status=404)