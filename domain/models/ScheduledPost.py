from django.db import models

from .BaseModel import BaseModel


class ScheduledPost(BaseModel):
    brand = models.ForeignKey('domain.Brand', db_column='brand_id', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'domain.Product',
        db_column='product_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    generated_content = models.ForeignKey(
        'domain.GeneratedContent',
        db_column='generated_content_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    scheduled_at = models.DateTimeField()
    time_zone = models.CharField(max_length=100)
    status = models.CharField(max_length=50, blank=True)
    created_by_user = models.ForeignKey(
        'domain.User',
        db_column='created_by_user_id',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'scheduled_posts'
