from django.db import models

from .BaseModel import BaseModel


class UserToken(BaseModel):
    user = models.ForeignKey('domain.User', db_column='user_id', on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=255)
    token_type = models.CharField(max_length=100)
    expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_tokens'
