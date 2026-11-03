# domain/social_client.py
from socialchimp import SocialChimp
from socialchimp.contrib.django import orm_storage
from domain.social_storage import DjangoStorage

def get_social_client():
    return SocialChimp(storage=orm_storage(DjangoStorage()))