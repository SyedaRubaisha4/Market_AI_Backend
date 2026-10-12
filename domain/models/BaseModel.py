import uuid

from mongoengine import Document, fields


class BaseModel(Document):
    id = fields.UUIDField(primary_key=True, binary=False, default=uuid.uuid4)
    created_on = fields.DateTimeField()
    updated_on = fields.DateTimeField()
    action_type = fields.IntField(default=1)

    meta = {'abstract': True}
