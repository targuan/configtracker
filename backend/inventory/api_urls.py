from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import DeviceViewSet, ConfigurationViewSet, DeviceConfigurationViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'configurations', ConfigurationViewSet)
router.register(r'device-configurations', DeviceConfigurationViewSet)

urlpatterns = router.urls
