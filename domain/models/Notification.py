from django.db import models

from .BaseModel import BaseModel


class Notification(BaseModel):
    body = models.TextField()
    platforms_count = models.PositiveIntegerField(default=0)
    project_id = models.UUIDField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
