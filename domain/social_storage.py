# domain/social_storage.py

from django.utils import timezone
from django.conf import settings
from socialchimp import AppCredentials, Connection, Token
from domain.models.SocialConnect import SocialConnect
from domain.encryption import encrypt, decrypt
import os

class DjangoStorage:
    """Maps SocialChimp connections to the SocialConnect model."""

    def get_connection(self, connection_id: str) -> Connection | None:
        row = SocialConnect.objects.filter(
            socialchimp_connection_id=connection_id
        ).first()
        if row is None:
            return None

        if row.token_expires_at and row.token_expires_at < timezone.now():
            row.connection_status = 'Expired'
            row.save(update_fields=['connection_status'])

        return Connection(
            id=row.socialchimp_connection_id,
            platform=row.platform,
            host=None,
            account_id=row.platform_account_id,
            account_name='',
            token=Token(
                access_token=decrypt(row.access_token_encrypted),
                refresh_token=(
                    decrypt(row.refresh_token_encrypted)
                    if row.refresh_token_encrypted else None
                ),
                expires_at=row.token_expires_at,
            ),
            scopes=tuple(row.granted_scopes or []),
            extra={},
        )

    def save_connection(self, connection: Connection) -> None:
        SocialConnect.objects.update_or_create(
            socialchimp_connection_id=connection.id,
            defaults={
                'platform': connection.platform,
                'platform_account_id': connection.account_id or '',
                'access_token_encrypted': encrypt(connection.token.access_token or ''),
                'refresh_token_encrypted': (
                    encrypt(connection.token.refresh_token)
                    if connection.token.refresh_token else ''
                ),
                'token_expires_at': connection.token.expires_at,
                'granted_scopes': list(connection.scopes or []),
                'connection_status': 'Connected',
                'connected_at': timezone.now(),
                'last_validated_at': timezone.now(),
            },
        )

    def delete_connection(self, connection_id: str) -> None:
        SocialConnect.objects.filter(
            socialchimp_connection_id=connection_id
        ).update(connection_status='Disconnected')

    def get_app(self, platform: str, host: str | None = None) -> AppCredentials | None:
        if platform in ['facebook', 'instagram']:
            client_id = os.environ.get('FACEBOOK_APP_ID')
            client_secret = os.environ.get('FACEBOOK_APP_SECRET')

            if not client_id or not client_secret:
                print(f"❌ DEBUG: .env mein {platform.upper()}_APP_ID not found SECRET keys")
                return None

            return AppCredentials(
                platform=platform,
                host=host,
                client_id=client_id,
                client_secret=client_secret,
            )
        return None

    def save_app(self, app: AppCredentials) -> None:
        pass