from rest_framework.decorators import api_view
from .service import ProductService


@api_view(['POST'])
def view_add_or_update_product(request, product_id):
    """
    Add a new product or update an existing one.
    """
    return ProductService.add_or_update_product(request, product_id)