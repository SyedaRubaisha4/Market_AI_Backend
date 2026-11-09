from django.db import models
from .BaseModel import BaseModel

class SocialConnect(BaseModel):
    user = models.ForeignKey('domain.User', db_column='user_id', on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(
        'domain.Brand',
        db_column='brand_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    platform = models.CharField(max_length=100)
    platform_account_id = models.CharField(max_length=255)
    
    socialchimp_connection_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True,
        help_text="SocialChimp ka internal connection ID"
    )
    access_token_encrypted = models.TextField(null=True, blank=True)
    refresh_token_encrypted = models.TextField(null=True, blank=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    granted_scopes = models.JSONField(default=list, blank=True)
    connection_status = models.CharField(
        max_length=20,
        choices=(
            ('Connected', 'Connected'),
            ('Expired', 'Expired'),
            ('Revoked', 'Revoked'),
            ('Disconnected', 'Disconnected'),
        ),
        default='Connected',
    )
    connected_at = models.DateTimeField(null=True, blank=True)
    last_validated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'social_connects'