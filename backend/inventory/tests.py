from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Device, Configuration, DeviceConfiguration


class DeviceCRUDTestCase(TestCase):
    """Test cases for Device CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/inventory/devices/'

    def test_create_device(self):
        """Test creating a new device"""
        data = {'name': 'New Device'}
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], 'New Device')
        self.assertIn('created', response.data)
        self.assertIn('modified', response.data)
        self.assertTrue(Device.objects.filter(id=response.data['id']).exists())

    def test_create_device_invalid_data(self):
        """Test creating a device with invalid data"""
        data = {'name': ''}  # Empty name
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_devices_empty(self):
        """Test listing devices when none exist"""
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_devices_with_data(self):
        """Test listing devices with existing data"""
        device1 = Device.objects.create(name='Device 1')
        device2 = Device.objects.create(name='Device 2')
        
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        names = [d['name'] for d in response.data]
        self.assertIn('Device 1', names)
        self.assertIn('Device 2', names)

    def test_retrieve_device(self):
        """Test retrieving a specific device"""
        device = Device.objects.create(name='Retrieve Test Device')
        url = f'{self.base_url}{device.id}/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], device.id)
        self.assertEqual(response.data['name'], 'Retrieve Test Device')

    def test_retrieve_nonexistent_device(self):
        """Test retrieving a non-existent device"""
        url = f'{self.base_url}999999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_device(self):
        """Test updating a device"""
        device = Device.objects.create(name='Original Name')
        url = f'{self.base_url}{device.id}/'
        update_data = {'name': 'Updated Name'}
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        
        # Verify in database
        device.refresh_from_db()
        self.assertEqual(device.name, 'Updated Name')

    def test_partial_update_device(self):
        """Test partial update of a device"""
        device = Device.objects.create(name='Original Name')
        url = f'{self.base_url}{device.id}/'
        update_data = {'name': 'Partially Updated Name'}
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Partially Updated Name')

    def test_delete_device(self):
        """Test deleting a device"""
        device = Device.objects.create(name='Device to Delete')
        url = f'{self.base_url}{device.id}/'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(id=device.id).exists())

    def test_delete_nonexistent_device(self):
        """Test deleting a non-existent device"""
        url = f'{self.base_url}999999/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
        
        url = f'{self.base_url}{device.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(id=device.id).exists())
        self.assertEqual(DeviceConfiguration.objects.filter(device_id=device.id).count(), 0)
        # Configurations should still exist (only DeviceConfiguration is cascaded)
        self.assertTrue(Configuration.objects.filter(id=config1.id).exists())
        self.assertTrue(Configuration.objects.filter(id=config2.id).exists())


class ConfigurationCRUDTestCase(TestCase):
    """Test cases for Configuration CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/inventory/configurations/'

    def test_create_configuration(self):
        """Test creating a new configuration"""
        data = {'configuration': '{\"interface\": \"eth0\"}'}
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['configuration'], '{\"interface\": \"eth0\"}')
        self.assertIn('created', response.data)
        self.assertIn('modified', response.data)
        self.assertTrue(Configuration.objects.filter(id=response.data['id']).exists())

    def test_create_configuration_invalid_data(self):
        """Test creating a configuration with invalid data"""
        data = {'configuration': ''}  # Empty configuration
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_configurations_empty(self):
        """Test listing configurations when none exist"""
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_configurations_with_data(self):
        """Test listing configurations with existing data"""
        config1 = Configuration.objects.create(configuration='Config 1')
        config2 = Configuration.objects.create(configuration='Config 2')
        
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_configuration(self):
        """Test retrieving a specific configuration"""
        config = Configuration.objects.create(configuration='Retrieve Test Config')
        url = f'{self.base_url}{config.id}/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], config.id)
        self.assertEqual(response.data['configuration'], 'Retrieve Test Config')

    def test_retrieve_nonexistent_configuration(self):
        """Test retrieving a non-existent configuration"""
        url = f'{self.base_url}999999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_configuration(self):
        """Test updating a configuration"""
        config = Configuration.objects.create(configuration='Original Config')
        url = f'{self.base_url}{config.id}/'
        update_data = {'configuration': 'Updated Config'}
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['configuration'], 'Updated Config')
        
        # Verify in database
        config.refresh_from_db()
        self.assertEqual(config.configuration, 'Updated Config')

    def test_partial_update_configuration(self):
        """Test partial update of a configuration"""
        config = Configuration.objects.create(configuration='Original Config')
        url = f'{self.base_url}{config.id}/'
        update_data = {'configuration': 'Partially Updated Config'}
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['configuration'], 'Partially Updated Config')

    def test_delete_configuration(self):
        """Test deleting a configuration"""
        config = Configuration.objects.create(configuration='Config to Delete')
        url = f'{self.base_url}{config.id}/'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Configuration.objects.filter(id=config.id).exists())

    def test_delete_nonexistent_configuration(self):
        """Test deleting a non-existent configuration"""
        url = f'{self.base_url}999999/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_configuration_with_device_configurations_cascade(self):
        """Test deleting a configuration with associated device configurations (cascade delete)"""
        config = Configuration.objects.create(configuration='Config with Devices')
        device1 = Device.objects.create(name='Device 1')
        device2 = Device.objects.create(name='Device 2')
        dc1 = DeviceConfiguration.objects.create(
            device=device1, 
            configuration=config, 
            state='running'
        )
        dc2 = DeviceConfiguration.objects.create(
            device=device2, 
            configuration=config, 
            state='intent'
        )
        
        url = f'{self.base_url}{config.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Configuration.objects.filter(id=config.id).exists())
        self.assertEqual(DeviceConfiguration.objects.filter(configuration_id=config.id).count(), 0)
        # Devices should still exist (only DeviceConfiguration is cascaded)
        self.assertTrue(Device.objects.filter(id=device1.id).exists())
        self.assertTrue(Device.objects.filter(id=device2.id).exists())


class DeviceConfigurationCRUDTestCase(TestCase):
    """Test cases for DeviceConfiguration CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/inventory/device-configurations/'
        self.device = Device.objects.create(name='Test Device')
        self.config = Configuration.objects.create(configuration='Test Config')

    def test_create_device_configuration(self):
        """Test creating a new device configuration"""
        data = {
            'device': self.device.id,
            'configuration': self.config.id,
            'state': 'running'
        }
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['device'], self.device.id)
        self.assertEqual(response.data['configuration'], self.config.id)
        self.assertEqual(response.data['state'], 'running')
        self.assertTrue(DeviceConfiguration.objects.filter(id=response.data['id']).exists())

    def test_create_device_configuration_invalid_state(self):
        """Test creating a device configuration with invalid state"""
        data = {
            'device': self.device.id,
            'configuration': self.config.id,
            'state': 'invalid_state'
        }
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_device_configuration_missing_fields(self):
        """Test creating a device configuration with missing required fields"""
        data = {
            'device': self.device.id,
            # Missing configuration and state
        }
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_device_configurations_empty(self):
        """Test listing device configurations when none exist"""
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_device_configurations_with_data(self):
        """Test listing device configurations with existing data"""
        dc1 = DeviceConfiguration.objects.create(
            device=self.device, 
            configuration=self.config, 
            state='running'
        )
        dc2 = DeviceConfiguration.objects.create(
            device=self.device, 
            configuration=self.config, 
            state='intent'
        )
        
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_device_configuration(self):
        """Test retrieving a specific device configuration"""
        dc = DeviceConfiguration.objects.create(
            device=self.device, 
            configuration=self.config, 
            state='running'
        )
        url = f'{self.base_url}{dc.id}/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], dc.id)
        self.assertEqual(response.data['device'], self.device.id)
        self.assertEqual(response.data['configuration'], self.config.id)
        self.assertEqual(response.data['state'], 'running')

    def test_retrieve_nonexistent_device_configuration(self):
        """Test retrieving a non-existent device configuration"""
        url = f'{self.base_url}999999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_device_configuration(self):
        """Test updating a device configuration"""
        config2 = Configuration.objects.create(configuration='Config 2')
        dc = DeviceConfiguration.objects.create(
            device=self.device, 
            configuration=self.config, 
            state='running'
        )
        url = f'{self.base_url}{dc.id}/'
        update_data = {
            'device': self.device.id,
            'configuration': config2.id,
            'state': 'intent'
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['configuration'], config2.id)
        self.assertEqual(response.data['state'], 'intent')
        
        # Verify in database
        dc.refresh_from_db()
        self.assertEqual(dc.configuration.id, config2.id)
        self.assertEqual(dc.state, 'intent')

    def test_partial_update_device_configuration(self):
        """Test partial update of a device configuration"""
        dc = DeviceConfiguration.objects.create(
            device=self.device, 
            configuration=self.config, 
            state='running'
        )
        url = f'{self.base_url}{dc.id}/'
        update_data = {'state': 'design'}
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 'design')

    def test_delete_device_configuration(self):
        """Test deleting a device configuration"""
        dc = DeviceConfiguration.objects.create(
            device=self.device, 
            configuration=self.config, 
            state='running'
        )
        url = f'{self.base_url}{dc.id}/'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DeviceConfiguration.objects.filter(id=dc.id).exists())
        # Device and Configuration should still exist
        self.assertTrue(Device.objects.filter(id=self.device.id).exists())
        self.assertTrue(Configuration.objects.filter(id=self.config.id).exists())

    def test_delete_nonexistent_device_configuration(self):
        """Test deleting a non-existent device configuration"""
        url = f'{self.base_url}999999/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unique_constraint_device_configuration(self):
        """Test that unique_together constraint is enforced"""
        dc1 = DeviceConfiguration.objects.create(
            device=self.device, 
            configuration=self.config, 
            state='running'
        )
        # Try to create another with same device, configuration, and state
        data = {
            'device': self.device.id,
            'configuration': self.config.id,
            'state': 'running'
        }
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
