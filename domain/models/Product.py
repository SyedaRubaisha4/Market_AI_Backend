from mongoengine import fields

from .BaseModel import BaseModel


class Product(BaseModel):
    brand_id = fields.ReferenceField('Brand', required=True)
    category_id = fields.UUIDField(binary=False, required=True)
    name = fields.StringField(required=True, max_length=255)
    price = fields.DecimalField(required=True, precision=2, min_value=0)
    currency = fields.StringField(required=True, max_length=3)
    basic_details = fields.DictField()
    status = fields.StringField(max_length=50)
    # created_at = fields.DateTimeField()
    # updated_at = fields.DateTimeField()

    meta = {'collection': 'products'}