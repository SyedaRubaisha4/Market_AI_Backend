from django.urls import path

from api.controllers.Product.views import view_add_or_update_product

    
urlpatterns = [
    path('add-or-update/<str:product_id>/', view_add_or_update_product, name='add-or-update-product'),
]               