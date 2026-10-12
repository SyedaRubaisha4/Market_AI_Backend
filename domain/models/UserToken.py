from mongoengine import fields

from .BaseModel import BaseModel


class UserToken(BaseModel):
    user_id = fields.ReferenceField('User', required=True)
    token_hash = fields.StringField(required=True)
    token_type = fields.StringField(required=True, max_length=100)
    expires_at = fields.DateTimeField(required=True)
    revoked_at = fields.DateTimeField()
    # created_at = fields.DateTimeField()

    meta = {'collection': 'user_tokens'}
