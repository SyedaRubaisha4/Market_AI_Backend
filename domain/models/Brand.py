from django.db import models
from django.conf import settings
from .BaseModel import BaseModel

class Brand(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='brands')
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tone_of_voice = models.JSONField(default=list, blank=True) # e.g. ["Friendly", "Professional"]
    target_customer_class = models.CharField(max_length=50, blank=True, null=True)
    customer_type = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    words_to_avoid = models.JSONField(default=list, blank=True)
    brand_keywords = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=50, default='Active')

    class Meta:
        db_table = 'brands'

    def __str__(self):
        return self.business_name