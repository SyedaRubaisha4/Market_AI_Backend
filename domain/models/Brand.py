from mongoengine import fields

from .BaseModel import BaseModel


class Brand(BaseModel):
    user_id = fields.ReferenceField('User', required=True)
    business_name = fields.StringField(required=True, max_length=255)
    business_type = fields.StringField(max_length=100)
    description = fields.StringField()
    tone_of_voice = fields.ListField(fields.StringField())
    target_customer_class = fields.StringField(
        choices=('middle', 'elite', 'lower'),
    )
    customer_type = fields.StringField(
        choices=('child', 'men', 'women'),
    )
    language = fields.StringField(max_length=100)
    words_to_avoid = fields.ListField(fields.StringField())
    brand_keywords = fields.ListField(fields.StringField())
    status = fields.StringField(max_length=50)

    meta = {'collection': 'brands'}
