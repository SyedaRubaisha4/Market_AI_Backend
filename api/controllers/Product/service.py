from pyexpat.errors import messages

from domain.models.Product import Product
from domain.models.ProductImage import ProductImage
from domain.models.GeneratedContent import GeneratedContent
from uuid import UUID
from domain.serializers.serializers import ProductSerializer, ProductImageSerializer, GeneratedContentSerializer    
from utility.common.createresponse import CreateResponse
from utility.helper import errormessages
from utility.helper.constant import ErrorCodes
import traceback
def create_or_update_product(data):
    try:
        product_id = data.get('id')
        product=None
        if product_id:
            try:
                product_id = UUID(str(product_id))
            except (TypeError, ValueError):
                return CreateResponse.error("id must be a valid UUID")
            product = Product.objects(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id {product_id} does not exist.")
            serializer = ProductSerializer(product, data=data, partial=product is not None)
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

def get_products(request):
    try:
        page=request.GET.get('page', 1)
        page_size=request.GET.get('page_size', 10)
        start_index = (int(page) - 1) * int(page_size)
        end_index = start_index + int(page_size)
        query=Product.objects
        search_query = request.GET.get('search', None)
        if search_query:
            query = query.filter(product_name__icontains=search_query)
        action_type = request.GET.get('action_type', None)
        if action_type:
            query = query.filter(action_type=action_type)
        total_count = query.count()
        products = query.order_by('-created_at')[start_index:end_index]
        if not products:
            return CreateResponse.error(errormessages.PRODUCT_NOT_FOUND, int(ErrorCodes.NOT_FOUND))
        
        return CreateResponse.paginated_success(ProductSerializer(products, many=True).data,message=messages.PRODUCT_LIST_FETCHED_SUCCESSFULLY,
                                                 page=page, page_size=page_size, total_count=total_count,error_code=int(ErrorCodes.SUCCESS))
    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED)) 

def get_product_by_id(product_id):
    try:
        product = Product.objects(id=product_id).first()
        if not product:
            return CreateResponse.error(errormessages.PRODUCT_NOT_FOUND, int(ErrorCodes.NOT_FOUND))
        
        return CreateResponse.success(ProductSerializer(product).data, errormessages.PRODUCT_FETCHED_SUCCESSFULLY)
    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED))

def delete_product(product_id):
    try:
        product = Product.objects(id=product_id).first()
        if not product:
            return CreateResponse.error(errormessages.PRODUCT_NOT_FOUND, int(ErrorCodes.NOT_FOUND))
        
        product.delete()
        return CreateResponse.success(None, errormessages.PRODUCT_DELETED_SUCCESSFULLY)
    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED))
               