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
from utility.helper.helperfuncitons import HelperFunctions
from PIL import Image, ImageEnhance
from io import BytesIO
from django.core.files.base import ContentFile


def enhance_product_image(image_file, product_id):
    """Uploaded image ko enhance karein (brightness, contrast, sharpness)."""
    try:
        # 1. Open Image 
        img = Image.open(image_file)
        
        # 2. Enhancements apply 
        # Brightness (1.0 = original, 1.15 = 15% brighter)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.15)
        
        # Contrast (1.0 = original, 1.2 = 20% more contrast)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Sharpness (1.0 = original, 1.3 = 30% sharper)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)
        
        # 3. Enhanced image saved in bytes 
        output = BytesIO()
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        # 4. Make File name
        file_name = f"enhanced_{product_id}.jpg"
        
        return ContentFile(output.read(), name=file_name)
    except Exception as e:
        print(f"Enhancement error: {e}")
        return image_file  


def create_or_update_product(data, image_files, request=None, product_id=None):
    try:
        product_id = data.get("id") or product_id
        if not product_id and request:
            product_id = request.parser_context.get('kwargs', {}).get('product_id')

        product = None

        if product_id:
            try:
                product_id = UUID(str(product_id))
            except (ValueError, TypeError, AttributeError):
                return CreateResponse.error("Invalid product ID.")

            product = Product.objects.filter(
                pk=product_id,
                brand__user=request.user,
                action_type=1,
            ).first()

            if not product:
                return CreateResponse.error("Product not found.")

        payload = data.copy()
        payload.pop("product_images", None)

        serializer = ProductSerializer(
            instance=product,
            data=payload,
            partial=product is not None,
        )

        if not serializer.is_valid():
            return CreateResponse.error(serializer.errors)

        values = dict(serializer.validated_data)
        values.pop("action_type", None)
        if product is not None:
            values.pop("brand", None)

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
                enhanced_file = enhance_product_image(image_file, product.id)
                file_name = uuid.uuid4().hex
                file_path = f"products/{product.id}"
                saved_path = HelperFunctions.save_file(enhanced_file, file_name, file_path)
                image_url = request.build_absolute_uri("/" + saved_path.replace("\\", "/").lstrip("/"))
                image_extension = os.path.splitext(enhanced_file.name)[1]

                image = ProductImage.objects.create(
                    product=product,
                    storage_key=f"{file_path}/{file_name}{image_extension}",
                    image_url=image_url,
                    image_type="image/jpeg",
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

        if product_id:
            saved_images = ProductImage.objects.filter(
                product=product,
                action_type=1,
            )

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
        return CreateResponse.error(str(e), int(ErrorCodes.FAILED))


def get_products(request):
    try:
        page_size = int(request.query_params.get('page_size', 10))
        page_number = int(request.query_params.get('page', 1))

        if page_number < 1 or page_size < 1:
            raise ValueError("page and page_size must be positive integers.")

        query = Product.objects.filter(brand__user=request.user).exclude(action_type=3)

        search_query = request.query_params.get('search')
        if search_query:
            query = query.filter(name__icontains=search_query)

        paginator = Paginator(query.order_by('-created_on'), page_size)
        products = paginator.get_page(page_number)

        product_list = ProductSerializer(products.object_list, many=True).data

        product_images = ProductImage.objects.filter(
            product_id__in=[p.id for p in products.object_list],
            action_type=1,
        )

        images_by_product = {}

        for image in product_images:
            product_id = str(image.product_id)
            if product_id not in images_by_product:
                images_by_product[product_id] = []
            images_by_product[product_id].append(ProductImageSerializer(image).data)

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


def get_product_by_id(product_id, request):
    try:
        product = Product.objects.filter(
            pk=product_id,
            brand__user=request.user,
            action_type=1,
        ).first()
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


def delete_product(product_id, request):
    try:
        product = Product.objects.filter(
            pk=product_id,
            brand__user=request.user,
            action_type=1,
        ).first()
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