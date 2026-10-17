from django.urls import path

from api.controllers.Product.views import view_add_or_update_product, view_delete_product, view_get_product_by_id
from api.controllers.Schedule.views import (
    view_add_or_update_schedule,
    view_delete_schedule,
    view_get_schedules,
    view_get_schedule_by_id)

urlpatterns = [
    path('add/', view_add_or_update_schedule, name='add-or-update-schedule'),
    path ('get/',view_get_schedules,name='get-schedules'),
    path('get/<uuid:schedule_id>/', view_get_schedule_by_id, name='get-schedule-by-id'),
    path ('delete/<uuid:schedule_id>/',view_delete_schedule,name='delete-schedule')
    
]