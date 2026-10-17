from django.urls import include, path
from .views import HelloView

urlpatterns = [
    # path('hello/', HelloView.as_view(), name='hello'),
    path('product/', include('api.controllers.Product.urls')),
    path('schedule/', include('api.controllers.Schedule.urls')),
    path('lookup/', include('api.controllers.Lookup.urls'))
]