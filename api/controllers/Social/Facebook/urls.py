from django.urls import path
from . import views

urlpatterns = [
    path("connect/",  views.connect_facebook,     name="social-connect-facebook"),
    path("callback/", views.callback_facebook,    name="social-callback-facebook"),
    path("choose/",   views.choose_facebook_page, name="social-choose-facebook"),
    path("success/",  views.connect_success,      name="social-connect-success"),
]