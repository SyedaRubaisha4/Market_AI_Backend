from mongoengine import fields

from .BaseModel import BaseModel


class Notification(BaseModel):
    body = fields.StringField(required=True)
    platforms_count = fields.IntField(default=0, min_value=0)
    project_id = fields.UUIDField(binary=False)

    meta = {'collection': 'notifications'}
