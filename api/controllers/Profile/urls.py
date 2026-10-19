from django.urls import path
from api.controllers.Profile.views import (
    view_get_profile,
    view_update_profile,
    view_delete_profile,
    view_get_user_by_id
)

urlpatterns = [
    path('get/', view_get_profile, name='get_profile'),
    path('update/', view_update_profile, name='update_profile'),
    path('delete/', view_delete_profile, name='delete_profile'),
    path('<int:user_id>/', view_get_user_by_id, name='get_user_by_id'),

]