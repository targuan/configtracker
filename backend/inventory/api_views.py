from rest_framework import viewsets
from .models import Device, Configuration, DeviceConfiguration
from .serializers import DeviceSerializer, ConfigurationSerializer, DeviceConfigurationSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer


class DeviceConfigurationViewSet(viewsets.ModelViewSet):
    queryset = DeviceConfiguration.objects.all()
    serializer_class = DeviceConfigurationSerializer
