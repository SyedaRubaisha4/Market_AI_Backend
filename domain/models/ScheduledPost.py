from mongoengine import fields

from .BaseModel import BaseModel


class ScheduledPost(BaseModel):
    brand_id = fields.ReferenceField('Brand', required=True)
    product_id = fields.ReferenceField('Product')
    generated_content_id = fields.ReferenceField('GeneratedContent')
    scheduled_at = fields.DateTimeField(required=True)
    time_zone = fields.StringField(required=True, max_length=100)
    status = fields.StringField(max_length=50)
    created_by_user_id = fields.ReferenceField('User', required=True)
    # created_at = fields.DateTimeField()
    # updated_at = fields.DateTimeField()

    meta = {'collection': 'scheduled_posts'}
