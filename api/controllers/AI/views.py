import json
import traceback
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from domain.models import Product
from .service import generate_ai_content

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def view_generate_content(request, product_id):
    try:
        # 1. Find product
        product = Product.objects.get(id=product_id, brand__user=request.user)
        brand_name = product.brand.business_name if product.brand else "Our Store"

        # 2. Extract product details
        details_list = []
        
        # Check if details present or not
        if hasattr(product, 'basic_details') and product.basic_details:
            for item in product.basic_details:
                if isinstance(item, dict) and 'key' in item and 'value' in item:
                    details_list.append(f"{item['key']}: {item['value']}")
        
        # If basic details are empty then send default text
        description_str = ", ".join(details_list) if details_list else "No description provided"

        # 3. Call Groq Api
        ai_response_str = generate_ai_content(
            product_name=product.name,
            price=product.price,
            description=description_str,
            brand_name=brand_name
        )

        # 4.Convert json to dictionary
        ai_data = json.loads(ai_response_str)

        return Response({
            "success": True,
            "content": ai_data
        }, status=200)

    except Product.DoesNotExist:
        return Response({"success": False, "errors": "Product not found."}, status=404)
    
    except Exception as e:
        traceback.print_exc()
        return Response({"success": False, "errors": str(e)}, status=500)