from django.db import transaction
from django.core.paginator import Paginator
from django.core.files import File
from django.utils.text import slugify

from domain.models.Product import Product
from domain.models.ProductImage import ProductImage
from domain.models.GeneratedContent import GeneratedContent
import uuid
from uuid import UUID
from domain.serializers.serializers import (
    GeneratedContentSerializer,
    ProductImageSerializer,
    ProductSerializer,
)
from market_ai.text_generation.text_generation import (
    generate_product_images,
    generate_product_text,
)
from utility.common.createresponse import CreateResponse
from utility.helper import errormessages
from utility.helper.constant import ErrorCodes
import traceback
import os
from django.core.files.storage import default_storage

from utility.helper.helperfuncitons import HelperFunctions
def create_or_update_product(data, image_files=None, request=None):
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

        generated_text = None
        generated_images = []
        if product is None:
            product = Product(**values)
            generated_text = generate_product_text(
                name=product.name,
                category=product.category_id,
                price=product.price,
                details=product.basic_details,
            )
            generated_images = generate_product_images(
                name=product.name,
                category=product.category_id,
                details=product.basic_details,
            )
        else:
            for key, value in values.items():
                setattr(product, key, value)

        saved_images = []

        with transaction.atomic():
            product.save()

            if generated_text is not None:
                GeneratedContent.objects.create(
                    product=product,
                    content_type="product_marketing",
                    content_data={"generated_text": generated_text},
                    status="Generated",
                )

            for index, image_file in enumerate(image_files or []):
                file_extension = os.path.splitext(image_file.name)[1]
                file_name = f"{slugify(product.name) or 'product'}-{uuid.uuid4().hex}"
                file_path = f"products/{product.id}"

                saved_path = HelperFunctions.save_file(
                    image_file,
                    file_name,
                    file_path,
                )

                image_url = request.build_absolute_uri(
                    "/" + saved_path.replace("\\", "/").lstrip("/")
                )

                image = ProductImage.objects.create(
                    product=product,
                    storage_key=(
                        f"{file_path}/{file_name}"
                        f"{file_extension}"
                    ),
                    image_url=image_url,
                    image_type=getattr(image_file, "content_type", "") or "",
                    alt_text=os.path.splitext(image_file.name)[0],
                    is_primary=(index == 0),
                )
                saved_images.append(image)

            for image_path in generated_images:
                image_path = os.fspath(image_path)
                file_extension = os.path.splitext(image_path)[1]
                file_name = f"{slugify(product.name) or 'product'}-{uuid.uuid4().hex}"
                file_path = f"products/{product.id}"

                with open(image_path, "rb") as generated_image:
                    image_file = File(
                        generated_image,
                        name=os.path.basename(image_path),
                    )
                    saved_path = HelperFunctions.save_file(
                        image_file,
                        file_name,
                        file_path,
                    )

                image_url = request.build_absolute_uri(
                    "/" + saved_path.replace("\\", "/").lstrip("/")
                )

                image = ProductImage.objects.create(
                    product=product,
                    storage_key=f"{file_path}/{file_name}{file_extension}",
                    image_url=image_url,
                    image_type="image/png",
                    alt_text=os.path.splitext(os.path.basename(image_path))[0],
                    is_primary=(not saved_images),
                )
                saved_images.append(image)

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

        query = Product.objects.exclude(action_type=3)

        search_query = request.get('search')
        if search_query:
            query = query.filter(name__icontains=search_query)

        paginator = Paginator(query.order_by('-created_on'), page_size)
        products = paginator.get_page(page_number)

        product_list = ProductSerializer(
            products.object_list, many=True
        ).data

        product_images = ProductImage.objects.filter(
            product_id__in=[p.id for p in products.object_list],
            action_type=1,
        )

        images_by_product = {}

        for image in product_images:
            product_id = str(image.product_id)

            if product_id not in images_by_product:
                images_by_product[product_id] = []

            images_by_product[product_id].append(
                ProductImageSerializer(image).data
            )

        generated_contents = GeneratedContent.objects.filter(
            product_id__in=[product.id for product in products.object_list],
            action_type=1,
        )
        generated_contents_by_product = {}

        for generated_content in generated_contents:
            product_id = str(generated_content.product_id)
            generated_contents_by_product.setdefault(product_id, []).append(
                GeneratedContentSerializer(generated_content).data
            )

        for product in product_list:
            product_id = str(product['id'])
            product['images'] = images_by_product.get(product_id, [])
            product['generated_contents'] = generated_contents_by_product.get(
                product_id, []
            )

        return CreateResponse.paginated(
            product_list,
            message=errormessages.DATA_FOUND,
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
        
        product_data = ProductSerializer(product).data
        product_data['images'] = ProductImageSerializer(
            ProductImage.objects.filter(product=product, action_type=1),
            many=True
        ).data
        product_data['generated_contents'] = GeneratedContentSerializer(
            GeneratedContent.objects.filter(product=product, action_type=1),
            many=True,
        ).data

        return CreateResponse.success(product_data, errormessages.PRODUCT_FETCHED_SUCCESSFULLY)
    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED))

def delete_product(product_id):
    try:
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            return CreateResponse.error(errormessages.NO_RECORD, int(ErrorCodes.NOT_FOUND))
        
        with transaction.atomic():
            product.action_type = 3
            product.save()
            ProductImage.objects.filter(product=product).update(action_type=3)
            GeneratedContent.objects.filter(product=product).update(action_type=3)

        return CreateResponse.success(None, errormessages.SUCCESS)
    except Exception as e:
        print(traceback.format_exc())
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED))
               