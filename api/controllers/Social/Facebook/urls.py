# api/controllers/Social/Facebook/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("connect/",  views.connect_facebook,     name="fb-connect"),
    path("callback/", views.callback_facebook,    name="fb-callback"),
    path("choose/",   views.choose_page_facebook, name="fb-choose"),
    path("success/",  views.connect_success,      name="social-connect-success"),
]