# api/controllers/Social/Facebook/service.py
from asgiref.sync import async_to_sync
from socialchimp.platform import SendToNetwork, ChooseAccount, Finished
from domain.social_client import get_social_client


CALLBACK_URL = "http://localhost:8000/api/social/facebook/callback/"
def start_facebook_login(user_id: int):
    required_scopes = [
        "pages_show_list",
        "pages_read_engagement",
        "pages_manage_posts"
    ]
    
    step = async_to_sync(get_social_client().start_login)(
        "facebook",
        redirect_uri=CALLBACK_URL,
        state=f"user-{user_id}",
        scopes=required_scopes
    )
    
    if not isinstance(step, SendToNetwork):
        raise ValueError(f"Unexpected step: {step!r}")
        
    return step

def process_facebook_callback(callback_data: dict, state: str, remember: str):
    return async_to_sync(get_social_client().finish_login)(
        "facebook",
        callback=callback_data,
        redirect_uri=CALLBACK_URL,
        state=state,
        remember=remember
    )

def choose_facebook_page(account_id: str, resume_token: str, state: str, remember: str):
    return async_to_sync(get_social_client().choose)(
        "facebook",
        account_id=account_id,
        resume_token=resume_token,
        redirect_uri=CALLBACK_URL,
        state=state,
        remember=remember
    )
