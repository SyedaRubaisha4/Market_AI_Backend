from mongoengine import fields

from .BaseModel import BaseModel


class ProductImage(BaseModel):
    product_id = fields.ReferenceField('Product', required=True)
    storage_key = fields.StringField(required=True, max_length=1024)
    image_url = fields.URLField(required=True, max_length=2048)
    image_type = fields.StringField(max_length=100)
    alt_text = fields.StringField(max_length=500)
    is_primary = fields.BooleanField(default=False)
    # created_at = fields.DateTimeField()

    meta = {'collection': 'product_images'}
