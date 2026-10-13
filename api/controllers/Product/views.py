from rest_framework.decorators import api_view
from .service import (create_or_update_product, get_products, delete_product)


@api_view(['POST'])
def view_add_or_update_product(request):
    """
    Add a new product or update an existing one.
    """
    return create_or_update_product(request.data)
@api_view(['GET'])
def view_get_products(request):
    return get_products(request.query_params)

@api_view (['DELETE'])
def view_delete_product(request, product_id):
    return delete_product( product_id)