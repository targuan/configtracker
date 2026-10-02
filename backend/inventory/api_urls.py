from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import DeviceViewSet, ConfigurationViewSet, DeviceConfigurationViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename="api-")
router.register(r'configurations', ConfigurationViewSet, basename="api-")
router.register(r'device-configurations', DeviceConfigurationViewSet, basename="api-")

urlpatterns = router.urls
