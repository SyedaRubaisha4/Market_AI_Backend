from django.db import models

from .BaseModel import BaseModel


class Product(BaseModel):
    brand = models.ForeignKey('domain.Brand', db_column='brand_id', on_delete=models.CASCADE)
    category_id = models.UUIDField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3)
    basic_details = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=50, blank=True)
    brand = models.ForeignKey('domain.Brand', db_column='brand_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'