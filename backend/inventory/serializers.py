from rest_framework import serializers
from .models import Device, Configuration, DeviceConfiguration


class DeviceConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceConfiguration
        fields = ['id', 'device', 'configuration', 'state']


class ConfigurationSerializer(serializers.ModelSerializer):
    device_configurations = DeviceConfigurationSerializer(many=True, read_only=True)

    class Meta:
        model = Configuration
        fields = ['id', 'configuration', 'created', 'modified', 'device_configurations']


class DeviceSerializer(serializers.ModelSerializer):
    device_configurations = DeviceConfigurationSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'name', 'created', 'modified', 'device_configurations']
