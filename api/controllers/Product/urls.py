from django.urls import path

from api.controllers.Product.views import view_add_or_update_product,view_delete_product,view_get_products

    
urlpatterns = [
    path('add/', view_add_or_update_product, name='add-or-update-product'),
    path ('get/',view_get_products,name='get-products'),
    path ('delete/<uuid:product_id>/',view_delete_product,name='delete-product')
    
]               