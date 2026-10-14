from django.db import models

from .BaseModel import BaseModel


class GeneratedContent(BaseModel):
    product = models.ForeignKey('domain.Product', db_column='product_id', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=100)
    platform = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=100, blank=True)
    version = models.PositiveIntegerField(default=1)
    content_data = models.JSONField()
    status = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'generated_contents'
