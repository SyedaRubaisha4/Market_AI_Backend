# api/controllers/Social/Instagram/service.py
from asgiref.sync import async_to_sync
from socialchimp.platform import SendToNetwork
from domain.social_client import get_social_client

CALLBACK_URL = "http://localhost:8000/api/social/instagram/callback/"

def start_instagram_login(user_id: int):
    # Facebook Login ke zariye Instagram scopes maang rahe hain
    required_scopes = [
        "instagram_basic",
        "instagram_content_publish",
        "pages_show_list",
        "pages_read_engagement"
    ]
    
    step = async_to_sync(get_social_client().start_login)(
        "facebook",  # 👈 Yahan "instagram" ki jagah "facebook" kar dein
        redirect_uri=CALLBACK_URL,
        state=f"user-{user_id}",
        scopes=required_scopes
    )
    
    if not isinstance(step, SendToNetwork):
        raise ValueError(f"Unexpected step: {step!r}")
        
    return step

def process_instagram_callback(callback_data: dict, state: str, remember: str):
    return async_to_sync(get_social_client().finish_login)(
        "facebook",  # 👈 Yahan bhi "facebook" kar dein
        callback=callback_data,
        redirect_uri=CALLBACK_URL,
        state=state,
        remember=remember
    )

def choose_instagram_account(account_id: str, resume_token: str, state: str, remember: str):
    return async_to_sync(get_social_client().choose)(
        "facebook",  # 👈 Yahan bhi "facebook" kar dein
        account_id=account_id,
        resume_token=resume_token,
        redirect_uri=CALLBACK_URL,
        state=state,
        remember=remember
    )