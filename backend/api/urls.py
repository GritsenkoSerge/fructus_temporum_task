from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api.views import UserViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('schema/', SpectacularAPIView.as_view(), name='openapi-schema'),
    path(
        'schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='api:openapi-schema'),
        name='swagger-ui',
    ),
    path(
        'schema/redoc/',
        SpectacularRedocView.as_view(url_name='api:openapi-schema'),
        name='redoc',
    ),
]
