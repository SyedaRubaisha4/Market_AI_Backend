from django.db import models

from .BaseModel import BaseModel


class Brand(BaseModel):
    user = models.ForeignKey('domain.User', db_column='user_id', on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    tone_of_voice = models.JSONField(default=list, blank=True)
    target_customer_class = models.CharField(
        max_length=20,
        choices=(('middle', 'middle'), ('elite', 'elite'), ('lower', 'lower')),
        null=True,
        blank=True,
    )
    customer_type = models.CharField(
        max_length=20,
        choices=(('child', 'child'), ('men', 'men'), ('women', 'women')),
        null=True,
        blank=True,
    )
    language = models.CharField(max_length=100, blank=True)
    words_to_avoid = models.JSONField(default=list, blank=True)
    brand_keywords = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'brands'
