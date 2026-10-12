from mongoengine import fields

from .BaseModel import BaseModel


class SocialConnect(BaseModel):
    user_id = fields.ReferenceField('User', required=True)
    brand_id = fields.ReferenceField('Brand')
    platform = fields.StringField(required=True, max_length=100)
    platform_account_id = fields.StringField(required=True, max_length=255)
    access_token_encrypted = fields.StringField(required=True)
    refresh_token_encrypted = fields.StringField()
    token_expires_at = fields.DateTimeField()
    granted_scopes = fields.ListField(fields.StringField())
    connection_status = fields.StringField(
        choices=('Connected', 'Expired', 'Revoked', 'Disconnected'),
        default='Connected',
    )
    connected_at = fields.DateTimeField()
    last_validated_at = fields.DateTimeField()
    # created_at = fields.DateTimeField()
    # updated_at = fields.DateTimeField()

    meta = {'collection': 'social_connects'}
