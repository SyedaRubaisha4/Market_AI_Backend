from django.urls import path
from api.controllers.Schedule.views import (
    view_add_or_update_schedule,
    view_get_all_schedules,  
    view_get_schedule_by_id, 
    view_delete_schedule
)

urlpatterns = [
    path('', view_get_all_schedules, name='get_all_schedules'), 
    path('create/', view_add_or_update_schedule, name='create_schedule'),
    path('get/', view_get_all_schedules, name='get_schedules'),
    path('get/<uuid:schedule_id>/', view_get_schedule_by_id, name='get_schedule_by_id'),
    path('delete/<uuid:schedule_id>/', view_delete_schedule, name='delete_schedule'),
]