from domain.models.Product import Product
from domain.models.ProductImage import ProductImage
from domain.models.GeneratedContent import GeneratedContent
import uuid
from domain.serializers.serializers import ProductSerializer, ProductImageSerializer, GeneratedContentSerializer    
from utility.common.createresponse import CreateResponse
from utility.helper import errormessages
from utility.helper.constant import ErrorCodes
import traceback
def create_or_update_product(data):
    try:
        product_id = data.get('id')
        if product_id:
            product = Product.objects(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id {product_id} does not exist.")
            serializer = ProductSerializer(product, data=data, partial=True)
        else:
            serializer = ProductSerializer(data=data)
            brand_id = data.get('brand_id')
            product_name = data.get('product_name')
            product_images = data.get('product_images', [])
            product_categpry = data.get('product_category')
            product_price =data.get('product_price')
            product_currency = data.get('product_currency')
            product_basic_details = data.get('product_basic_details', {})   
            if not brand_id:
                raise ValueError("brand_id is required for creating a new product.")
            if not product_name:
                raise ValueError("product_name is required for creating a new product.")
            if not product_images:
                raise ValueError("At least one product image is required for creating a new product.")
            if not product_categpry:
                raise ValueError("product_category is required for creating a new product.")
            if not product_price:
                raise ValueError("product_price is required for creating a new product.")
       
            product = serializer.save()
            return CreateResponse.success(serializer.data, errormessages.SUCCESS)
        
    except Exception as e:
         
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED))# if serializer.is_valid():
        