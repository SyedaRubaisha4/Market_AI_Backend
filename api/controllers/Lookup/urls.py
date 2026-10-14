from django.urls import path

from api.controllers.Lookup.views import (
    view_add_lookup,
    view_get_lookups,
    view_get_lookup_by_id,
    view_update_lookup,
    view_delete_lookup,
)

urlpatterns = [
    path('add/', view_add_lookup, name='add-lookup'),
    path('get/', view_get_lookups, name='get-lookups'),
    path('get/<uuid:lookup_id>/', view_get_lookup_by_id, name='get-lookup-by-id'),
    path('update/<uuid:lookup_id>/', view_update_lookup, name='update-lookup'),
    path('delete/<uuid:lookup_id>/', view_delete_lookup, name='delete-lookup'),
]