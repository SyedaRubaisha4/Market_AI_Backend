from mongoengine import fields

from .BaseModel import BaseModel


class ScheduledPostTarget(BaseModel):
    scheduled_post_id = fields.ReferenceField('ScheduledPost', required=True)
    social_connection_id = fields.ReferenceField('SocialConnect', required=True)
    platform_content_id = fields.StringField(max_length=255)
    status = fields.StringField(max_length=50)
    attempt_count = fields.IntField(default=0, min_value=0)
    published_at = fields.DateTimeField()
    last_attempt_at = fields.DateTimeField()
    last_error = fields.StringField()

    meta = {'collection': 'scheduled_post_targets'}
