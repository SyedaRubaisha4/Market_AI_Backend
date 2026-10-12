import uuid
from mongoengine import Document, fields


class Lookup(Document):
    id = fields.UUIDField(primary_key=True, binary=False, default=uuid.uuid4)

    parent = fields.ReferenceField('self', null=True, default=None)

    name = fields.StringField(max_length=255)
    value = fields.StringField(max_length=255)

    created_on = fields.DateTimeField()
    updated_on = fields.DateTimeField()
    action_type = fields.IntField(default=1)

    meta = {
        'collection': 'lookup',
        'indexes': [
            {'fields': ['value'], 'unique': True}
        ]
    }