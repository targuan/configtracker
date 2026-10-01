from django.db import models
from django.utils import timezone


class ConfigurationState(models.TextChoices):
    INTENT = 'intent', 'Intent'
    DESIGN = 'design', 'Design'
    RUNNING = 'running', 'Running'
    STARTUP = 'startup', 'Startup'


class Device(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Configuration(models.Model):
    configuration = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuration {self.id}"


class DeviceConfiguration(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_configurations')
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE, related_name='device_configurations')
    state = models.CharField(
        max_length=20,
        choices=ConfigurationState.choices,
        default=ConfigurationState.RUNNING
    )

    class Meta:
        unique_together = ('device', 'configuration', 'state')

    def __str__(self):
        return f"{self.device.name} - {self.configuration.id} ({self.state})"
