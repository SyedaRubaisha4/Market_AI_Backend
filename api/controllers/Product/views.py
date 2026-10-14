from rest_framework.decorators import api_view
from .service import (create_or_update_product, get_products, delete_product)


@api_view(['POST', 'PUT', 'PATCH'])
def view_add_or_update_product(request):
    return create_or_update_product(
        request.data,
        request.FILES.getlist('product_images'),
        request=request
    )
@api_view(['GET'])
def view_get_products(request):
    return get_products(request.query_params)

@api_view (['DELETE'])
def view_delete_product(request, product_id):
    return delete_product( product_id)