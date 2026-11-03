# api/controllers/Social/Instagram/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("connect/",  views.connect_instagram,     name="ig-connect"),
    path("callback/", views.callback_instagram,    name="ig-callback"),
    path("choose/",   views.choose_page_instagram, name="ig-choose"),
    path("success/",  views.connect_success,       name="ig-success"),
]