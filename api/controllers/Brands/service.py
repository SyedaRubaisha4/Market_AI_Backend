from django.core.exceptions import ValidationError
from domain.models.Brand import Brand

def create_brand(user, data):
    if not data.get('business_name'):
        raise ValidationError("Business name is required.")
    
    brand = Brand.objects.create(
        user=user,
        business_name=data.get('business_name'),
        business_type=data.get('business_type', ''),
        description=data.get('description', ''),
        tone_of_voice=data.get('tone_of_voice', []),
        target_customer_class=data.get('target_customer_class', ''),
        customer_type=data.get('customer_type', ''),
        language=data.get('language', ''),
        words_to_avoid=data.get('words_to_avoid', []),
        brand_keywords=data.get('brand_keywords', []),
    )
    return brand

def get_user_brands(user):
    return Brand.objects.filter(user=user, is_active=True).order_by('-created_on')

def get_brand_by_id(user, brand_id):
    try:
        return Brand.objects.get(id=brand_id, user=user, is_active=True)
    except Brand.DoesNotExist:
        raise ValidationError("Brand not found or you don't have permission.")

def update_brand(user, brand_id, data):
    brand = get_brand_by_id(user, brand_id)
    
    # Update allowed fields
    allowed_fields = [
        'business_name', 'business_type', 'description', 'tone_of_voice',
        'target_customer_class', 'customer_type', 'language', 
        'words_to_avoid', 'brand_keywords', 'status'
    ]
    
    for field in allowed_fields:
        if field in data:
            setattr(brand, field, data[field])
            
    brand.save()
    return brand

def delete_brand(user, brand_id):
    brand = get_brand_by_id(user, brand_id)
    brand.is_active = False # Soft delete
    brand.save()
    return True