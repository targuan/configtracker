from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Device, Configuration, DeviceConfiguration


class DeviceDeletionTestCase(TestCase):
    """Test cases for device deletion functionality"""

    def setUp(self):
        self.client = APIClient()

    def test_delete_device_without_configurations(self):
        """Test deleting a device that has no associated configurations"""
        device = Device.objects.create(name='Test Device')
        url = f'/api/inventory/devices/{device.id}/'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(id=device.id).exists())

    def test_delete_device_with_configurations_cascade(self):
        """Test deleting a device with associated configurations (cascade delete)"""
        device = Device.objects.create(name='Device with Configs')
        config1 = Configuration.objects.create(configuration='Config 1')
        config2 = Configuration.objects.create(configuration='Config 2')
        dc1 = DeviceConfiguration.objects.create(
            device=device, 
            configuration=config1, 
            state='running'
        )
        dc2 = DeviceConfiguration.objects.create(
            device=device, 
            configuration=config2, 
            state='intent'
        )
        
        url = f'/api/inventory/devices/{device.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(id=device.id).exists())
        self.assertEqual(DeviceConfiguration.objects.filter(device_id=device.id).count(), 0)
        # Configurations should still exist (only DeviceConfiguration is cascaded)
        self.assertTrue(Configuration.objects.filter(id=config1.id).exists())
        self.assertTrue(Configuration.objects.filter(id=config2.id).exists())

    def test_delete_nonexistent_device(self):
        """Test deleting a device that does not exist"""
        url = '/api/inventory/devices/999999/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_devices_empty(self):
        """Test listing devices when none exist"""
        url = '/api/inventory/devices/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_and_delete_device(self):
        """Test creating and then deleting a device"""
        # Create
        create_data = {'name': 'New Device'}
        create_response = self.client.post('/api/inventory/devices/', create_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        device_id = create_response.data['id']
        
        # Verify creation
        self.assertTrue(Device.objects.filter(id=device_id).exists())
        
        # Delete
        delete_url = f'/api/inventory/devices/{device_id}/'
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion
        self.assertFalse(Device.objects.filter(id=device_id).exists())
