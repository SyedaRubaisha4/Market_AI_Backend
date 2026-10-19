from django.urls import path
from api.controllers.Auth.views import view_register_user,view_login_user,view_logout_user,view_change_password,view_request_password_reset

urlpatterns = [
    path('register/', view_register_user, name='view_register_user'),
    path ('login/',view_login_user,name='view_login_user'),
    path ('logout/',view_logout_user,name='view_logout_user'),
    path ('change-password/',view_change_password,name='change_password'),
    path ('request-password/',view_request_password_reset,name='request_password_reset'),

]               