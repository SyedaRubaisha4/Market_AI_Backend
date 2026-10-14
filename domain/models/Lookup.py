from django.db import models

from .BaseModel import BaseModel


class Lookup(BaseModel):
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
    )
    name = models.CharField(max_length=255, blank=True)
    value = models.CharField(max_length=255, unique=True, blank=True)

    class Meta:
        db_table = 'lookup'