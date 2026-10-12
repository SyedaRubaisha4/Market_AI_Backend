from mongoengine import fields

from .BaseModel import BaseModel


class GeneratedContent(BaseModel):
    product_id = fields.ReferenceField('Product', required=True)
    content_type = fields.StringField(required=True, max_length=100)
    platform = fields.StringField(max_length=100)
    language = fields.StringField(max_length=100)
    version = fields.IntField(default=1, min_value=1)
    content_data = fields.DictField(required=True)
    status = fields.StringField(max_length=50)
    # created_at = fields.DateTimeField()

    meta = {'collection': 'generated_contents'}
