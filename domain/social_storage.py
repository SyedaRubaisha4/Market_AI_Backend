# domain/social_storage.py

from datetime import datetime
from django.utils import timezone
from socialchimp.models import Connection, Token
from socialchimp.storage import Storage
from domain.models.SocialConnect import SocialConnect
from domain.encryption import encrypt, decrypt

class DjangoStorage(Storage):
    """SocialConnect model ko SocialChimp ke Connection object se map karta hai."""

    def get_connection(self, connection_id: str):
        try:
            row = SocialConnect.objects.get(socialchimp_connection_id=connection_id)
        except SocialConnect.DoesNotExist:
            return None

        if row.token_expires_at and row.token_expires_at < timezone.now():
            row.connection_status = 'Expired'
            row.save(update_fields=['connection_status'])

        return Connection(
            id=row.socialchimp_connection_id,
            platform=row.platform,
            access_token=decrypt(row.access_token_encrypted),
            refresh_token=decrypt(row.refresh_token_encrypted) if row.refresh_token_encrypted else None,
            expires_at=row.token_expires_at,
            scopes=row.granted_scopes or [],
            account_id=row.platform_account_id,
        )

    def save_connection(self, connection: Connection):
        # Platform account ID se existing row dhoondein ya naya banayein
        row, created = SocialConnect.objects.update_or_create(
            socialchimp_connection_id=connection.id,
            defaults={
                'platform': connection.platform,
                'platform_account_id': connection.account_id or '',
                'access_token_encrypted': encrypt(connection.access_token or ''),
                'refresh_token_encrypted': encrypt(connection.refresh_token) if connection.refresh_token else '',
                'token_expires_at': connection.expires_at,
                'granted_scopes': connection.scopes or [],
                'connection_status': 'Connected',
                'connected_at': timezone.now() if created else None,
                'last_validated_at': timezone.now(),
            },
        )
        return row

    def delete_connection(self, connection_id: str):
        SocialConnect.objects.filter(
            socialchimp_connection_id=connection_id
        ).update(connection_status='Disconnected')

    def get_app(self, platform: str, host: str = None):
        """Platform ke app credentials return karein — settings se."""
        from django.conf import settings
        apps = getattr(settings, 'SOCIALCHIMP_APPS', {})
        cfg = apps.get(platform)
        if not cfg:
            return None
        from socialchimp import AppCredentials
        return AppCredentials(
            client_id=cfg['client_id'],
            client_secret=cfg['client_secret'],
        )

    def save_app(self, platform: str, host, app):
        pass