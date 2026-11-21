from django.urls import path
from api.controllers.Brands.views import (
    view_create_brand, view_list_brands, view_get_brand, 
    view_update_brand, view_delete_brand
)

urlpatterns = [
    path('', view_list_brands, name='list_brands'),
    path('create/', view_create_brand, name='create_brand'),
    path('<uuid:brand_id>/', view_get_brand, name='get_brand'),
    path('<uuid:brand_id>/update/', view_update_brand, name='update_brand'),
    path('<uuid:brand_id>/delete/', view_delete_brand, name='delete_brand'),
]