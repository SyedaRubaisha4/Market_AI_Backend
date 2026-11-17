"""
URL configuration for config project.
"""
from django.conf.urls import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse

# Swagger schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Market AI API",
        default_version='v1',
        description="API documentation for Market AI Backend",
        contact=openapi.Contact(email="admin@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def health_check(request):
    return JsonResponse({
        "status": "success",
        "message": "Market AI Backend is running"
    })
urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  

    # Swagger UI
    path('swagger/',    schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('health/', health_check, name='health-check'),
    path('api/', include('api.urls')),    


]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )