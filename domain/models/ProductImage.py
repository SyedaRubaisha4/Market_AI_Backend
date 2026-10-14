from django.db import models

from .BaseModel import BaseModel


class ProductImage(BaseModel):
    product = models.ForeignKey('domain.Product', db_column='product_id', on_delete=models.CASCADE)
    storage_key = models.CharField(max_length=1024)
    image_url = models.URLField(max_length=2048)
    image_type = models.CharField(max_length=100, blank=True)
    alt_text = models.CharField(max_length=500, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'product_images'
