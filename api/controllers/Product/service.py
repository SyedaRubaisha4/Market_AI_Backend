from django.db import transaction
from django.core.paginator import Paginator

from domain.models.Product import Product
from domain.models.ProductImage import ProductImage
from uuid import UUID
from domain.serializers.serializers import ProductSerializer, ProductImageSerializer
from utility.common.createresponse import CreateResponse
from utility.helper import errormessages
from utility.helper.constant import ErrorCodes
import traceback
import os
from django.core.files.storage import default_storage

def create_or_update_product(data, image_files=None):
    try:
        product_id = data.get("id")
        product = None

        if product_id:
            try:
                product_id = UUID(str(product_id))
            except (ValueError, TypeError, AttributeError):
                return CreateResponse.error("Invalid product ID.")

            product = Product.objects.filter(pk=product_id).first()

            if not product:
                return CreateResponse.error("Product not found.")

        payload = data.copy()
        payload.pop("product_images", None)

        serializer = ProductSerializer(
            instance=product,
            data=payload,
            partial=product is not None
        )

        if not serializer.is_valid():
            return CreateResponse.error(serializer.errors)

        values = dict(serializer.validated_data)
        values.pop("action_type", None)

        if product is None:
            product = Product(**values)
        else:
            for key, value in values.items():
                setattr(product, key, value)

        saved_images = []

        with transaction.atomic():
            product.save()

            for image_file in image_files or []:
                storage_key = default_storage.save(
                    f"products/{product.id}/{os.path.basename(image_file.name)}",
                    image_file
                )

                image_data = {
                    "product_id": str(product.id),
                    "storage_key": storage_key,
                    "image_url": default_storage.url(storage_key),
                    "image_type": "",
                    "alt_text": os.path.splitext(image_file.name)[0],
                    "is_primary": len(saved_images) == 0,
                }

                image_serializer = ProductImageSerializer(data=image_data)
                image_serializer.is_valid(raise_exception=True)
                image_values = dict(image_serializer.validated_data)
                image_values.pop("action_type", None)
                saved_images.append(ProductImage.objects.create(**image_values))

        return CreateResponse.success(
            {
                "product": ProductSerializer(product).data,
                "images": ProductImageSerializer(
                    saved_images, many=True
                ).data,
            },
            errormessages.SUCCESS
        )

    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(
            str(e), int(ErrorCodes.FAILED)
        )

def get_products(request):
    try:
        page_size = int(request.get('page_size', 10))
        page_number = int(request.get('page', 1))
        if page_number < 1 or page_size < 1:
            raise ValueError("page and page_size must be positive integers.")

        query = Product.objects.all()
        search_query = request.get('search')
        if search_query:
            query = query.filter(name__icontains=search_query)
        action_type = request.get('action_type')
        if action_type:
            query = query.filter(action_type=action_type)
        paginator = Paginator(query.order_by('-created_on'), page_size)
        products = paginator.get_page(page_number)
        return CreateResponse.paginated(
            ProductSerializer(products.object_list, many=True).data,
            message=errormessages.PRODUCT_LIST_FETCHED_SUCCESSFULLY,
            page=products.number,
            page_size=page_size,
            total_records=paginator.count,
            error_code=int(ErrorCodes.SUCCESS),
        )
    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED)) 

def get_product_by_id(product_id):
    try:
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            return CreateResponse.error(errormessages.PRODUCT_NOT_FOUND, int(ErrorCodes.NOT_FOUND))
        
        return CreateResponse.success(ProductSerializer(product).data, errormessages.PRODUCT_FETCHED_SUCCESSFULLY)
    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED))

def delete_product(product_id):
    try:
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            return CreateResponse.error(errormessages.PRODUCT_NOT_FOUND, int(ErrorCodes.NOT_FOUND))
        
        product.delete()
        return CreateResponse.success(None, errormessages.PRODUCT_DELETED_SUCCESSFULLY)
    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED))
               