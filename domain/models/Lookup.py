from mongoengine import fields

from .BaseModel import BaseModel


class Lookup(BaseModel):
    parent = fields.ReferenceField('self', null=True, default=None)

    name = fields.StringField(max_length=255)
    value = fields.StringField(max_length=255)

    meta = {
        'collection': 'lookup',
        'indexes': [
            {'fields': ['value'], 'unique': True}
        ]
    }