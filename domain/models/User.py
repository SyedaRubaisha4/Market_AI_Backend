from mongoengine import fields

from .BaseModel import BaseModel


class User(BaseModel):
    name = fields.StringField(required=True, max_length=255)
    email = fields.EmailField(required=True, unique=True)
    password_hash = fields.StringField(required=True)
    status = fields.StringField(
        choices=('Active', 'Suspended'),
        default='Active',
        required=True,
    )

    meta = {'collection': 'users'}
