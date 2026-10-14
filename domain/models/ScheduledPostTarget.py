from django.db import models

from .BaseModel import BaseModel


class ScheduledPostTarget(BaseModel):
    scheduled_post = models.ForeignKey(
        'domain.ScheduledPost',
        db_column='scheduled_post_id',
        on_delete=models.CASCADE,
    )
    social_connection = models.ForeignKey(
        'domain.SocialConnect',
        db_column='social_connection_id',
        on_delete=models.CASCADE,
    )
    platform_content_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, blank=True)
    attempt_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)

    class Meta:
        db_table = 'scheduled_post_targets'
