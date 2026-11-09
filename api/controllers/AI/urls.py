from django.urls import path
from .views import view_generate_content

urlpatterns = [
    path('<uuid:product_id>/', view_generate_content, name='generate_content'),
]