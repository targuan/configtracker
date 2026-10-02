from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import DeviceViewSet, ConfigurationViewSet, DeviceConfigurationViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename="api-devices")
router.register(r'configurations', ConfigurationViewSet, basename="api-configurations")
router.register(r'device-configurations', DeviceConfigurationViewSet, basename="api-device-configurations")

urlpatterns = router.urls
