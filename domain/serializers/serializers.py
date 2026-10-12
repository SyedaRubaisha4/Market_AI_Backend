from uuid import UUID

from rest_framework import serializers

from models import (
    Brand,
    GeneratedContent,
    Lookup,
    Notification,
    Product,
    ProductImage,
    ScheduledPost,
    ScheduledPostTarget,
    SocialConnect,
    User,
    UserToken,
)


class DocumentReferenceField(serializers.Field):
    def __init__(self, document_class, **kwargs):
        self.document_class = document_class
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            document_id = UUID(str(data))
        except (TypeError, ValueError, AttributeError) as exc:
            raise serializers.ValidationError('A valid UUID is required.') from exc

        return self.document_class(id=document_id)

    def to_representation(self, value):
        if value is None:
            return None
        return str(value.id)


class BaseDocumentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)
    action_type = serializers.IntegerField(required=False, default=1)


class UserSerializer(BaseDocumentSerializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password_hash = serializers.CharField(write_only=True)
    status = serializers.ChoiceField(choices=('Active', 'Suspended'), required=False, default='Active')


class UserTokenSerializer(BaseDocumentSerializer):
    user_id = DocumentReferenceField(User)
    token_hash = serializers.CharField()
    token_type = serializers.CharField(max_length=100)
    expires_at = serializers.DateTimeField()
    revoked_at = serializers.DateTimeField(required=False, allow_null=True)


class BrandSerializer(BaseDocumentSerializer):
    user_id = DocumentReferenceField(User)
    business_name = serializers.CharField(max_length=255)
    business_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    tone_of_voice = serializers.ListField(child=serializers.CharField(), required=False)
    target_customer_class = serializers.ChoiceField(
        choices=('middle', 'elite', 'lower'),
        required=False,
        allow_null=True,
    )
    customer_type = serializers.ChoiceField(
        choices=('child', 'men', 'women'),
        required=False,
        allow_null=True,
    )
    language = serializers.CharField(max_length=100, required=False, allow_blank=True)
    words_to_avoid = serializers.ListField(child=serializers.CharField(), required=False)
    brand_keywords = serializers.ListField(child=serializers.CharField(), required=False)
    status = serializers.CharField(max_length=50, required=False, allow_blank=True)


class ProductSerializer(BaseDocumentSerializer):
    brand_id = DocumentReferenceField(Brand)
    category_id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=18, decimal_places=2, min_value=0)
    currency = serializers.CharField(max_length=3)
    basic_details = serializers.JSONField(required=False)
    status = serializers.CharField(max_length=50, required=False, allow_blank=True)


class ProductImageSerializer(BaseDocumentSerializer):
    product_id = DocumentReferenceField(Product)
    storage_key = serializers.CharField(max_length=1024)
    image_url = serializers.URLField(max_length=2048)
    image_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    alt_text = serializers.CharField(max_length=500, required=False, allow_blank=True)
    is_primary = serializers.BooleanField(required=False, default=False)


class GeneratedContentSerializer(BaseDocumentSerializer):
    product_id = DocumentReferenceField(Product)
    content_type = serializers.CharField(max_length=100)
    platform = serializers.CharField(max_length=100, required=False, allow_blank=True)
    language = serializers.CharField(max_length=100, required=False, allow_blank=True)
    version = serializers.IntegerField(required=False, default=1, min_value=1)
    content_data = serializers.JSONField()
    status = serializers.CharField(max_length=50, required=False, allow_blank=True)


class SocialConnectSerializer(BaseDocumentSerializer):
    user_id = DocumentReferenceField(User)
    brand_id = DocumentReferenceField(Brand, required=False, allow_null=True)
    platform = serializers.CharField(max_length=100)
    platform_account_id = serializers.CharField(max_length=255)
    access_token_encrypted = serializers.CharField(write_only=True)
    refresh_token_encrypted = serializers.CharField(required=False, allow_blank=True, write_only=True)
    token_expires_at = serializers.DateTimeField(required=False, allow_null=True)
    granted_scopes = serializers.ListField(child=serializers.CharField(), required=False)
    connection_status = serializers.ChoiceField(
        choices=('Connected', 'Expired', 'Revoked', 'Disconnected'),
        required=False,
        default='Connected',
    )
    connected_at = serializers.DateTimeField(required=False, allow_null=True)
    last_validated_at = serializers.DateTimeField(required=False, allow_null=True)


class ScheduledPostSerializer(BaseDocumentSerializer):
    brand_id = DocumentReferenceField(Brand)
    product_id = DocumentReferenceField(Product, required=False, allow_null=True)
    generated_content_id = DocumentReferenceField(
        GeneratedContent,
        required=False,
        allow_null=True,
    )
    scheduled_at = serializers.DateTimeField()
    time_zone = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=50, required=False, allow_blank=True)
    created_by_user_id = DocumentReferenceField(User)


class ScheduledPostTargetSerializer(BaseDocumentSerializer):
    scheduled_post_id = DocumentReferenceField(ScheduledPost)
    social_connection_id = DocumentReferenceField(SocialConnect)
    platform_content_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    status = serializers.CharField(max_length=50, required=False, allow_blank=True)
    attempt_count = serializers.IntegerField(required=False, default=0, min_value=0)
    published_at = serializers.DateTimeField(required=False, allow_null=True)
    last_attempt_at = serializers.DateTimeField(required=False, allow_null=True)
    last_error = serializers.CharField(required=False, allow_blank=True)


class NotificationSerializer(BaseDocumentSerializer):
    body = serializers.CharField()
    platforms_count = serializers.IntegerField(required=False, default=0, min_value=0)
    project_id = serializers.UUIDField(required=False, allow_null=True)


class LookupSerializer(BaseDocumentSerializer):
    parent = DocumentReferenceField(Lookup, required=False, allow_null=True)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    value = serializers.CharField(max_length=255, required=False, allow_blank=True)


__all__ = [
    'BaseDocumentSerializer',
    'BrandSerializer',
    'GeneratedContentSerializer',
    'LookupSerializer',
    'NotificationSerializer',
    'ProductImageSerializer',
    'ProductSerializer',
    'ScheduledPostSerializer',
    'ScheduledPostTargetSerializer',
    'SocialConnectSerializer',
    'UserSerializer',
    'UserTokenSerializer',
]
