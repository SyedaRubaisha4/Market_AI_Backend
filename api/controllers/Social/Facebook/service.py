# api/controllers/Social/service.py
from asgiref.sync import async_to_sync
from django.utils import timezone
from socialchimp.platform import ChooseAccount, Finished, SendToNetwork
from domain.social_client import get_social_client
from domain.models.SocialConnect import SocialConnect

CALLBACK_URL = "http://localhost:8000/api/social/facebook/callback/"


def start_facebook_login(user_id: int):
    """Initiates the Facebook login flow and returns the redirect step."""
    step = async_to_sync(get_social_client().start_login)(
        "facebook",
        redirect_uri=CALLBACK_URL,
        state=f"user-{user_id}",
    )
    if not isinstance(step, SendToNetwork):
        raise ValueError(f"Unexpected step: {step!r}")
    return step

def process_facebook_callback(callback_data: dict, state: str, remember: str):
    """Exchanges the code for an access token and fetches Facebook Pages."""
    step = async_to_sync(get_social_client().finish_login)(
        "facebook",
        callback=callback_data,
        redirect_uri=CALLBACK_URL,
        state=state,
        remember=remember,
    )
    return step

def complete_facebook_connection(account_id: str, resume_token: str, state: str, remember: str, user, brand_id: int = None):
    """Finalizes the connection and attaches User & Brand to the SocialConnect row."""
    step = async_to_sync(get_social_client().choose)(
        "facebook",
        account_id=account_id,
        resume_token=resume_token,
        redirect_uri=CALLBACK_URL,
        state=state,
        remember=remember,
    )

    if isinstance(step, Finished):
        # SocialChimp created the row, now attach user and brand
        conn = SocialConnect.objects.filter(platform="facebook", user__isnull=True).order_by("-id").first()
        if conn:
            conn.user = user
            if brand_id:
                conn.brand_id = brand_id
            conn.connected_at = timezone.now()
            conn.save()
    
    return step