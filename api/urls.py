from django.urls import include, path
from .views import HelloView

urlpatterns = [
    # path('hello/', HelloView.as_view(), name='hello'),
    path('product/', include('api.controllers.Product.urls')),
    # path('schedule/', include('api.controllers.Schedule.urls')),
    path('lookup/', include('api.controllers.Lookup.urls')),
    path('auth/', include('api.controllers.Auth.urls')),
    path('profile/' , include('api.controllers.Profile.urls')),
    path('brands/', include('api.controllers.Brands.urls')),
    path('social/facebook/', include('api.controllers.Social.Facebook.urls')),

]