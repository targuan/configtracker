from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Workflow, WorkflowRun, WorkflowSchedule
from inventory.models import Device, Configuration, DeviceConfiguration


class WorkflowModelTestCase(TestCase):
    """Test cases for Workflow model"""

    def test_workflow_creation(self):
        """Test creating a workflow"""
        workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-workflow-123',
            workflow_type='deploy',
            status='pending'
        )
        
        self.assertEqual(workflow.name, 'Test Workflow')
        self.assertEqual(workflow.workflow_id, 'test-workflow-123')
        self.assertEqual(workflow.workflow_type, 'deploy')
        self.assertEqual(workflow.status, 'pending')
        self.assertIsNotNone(workflow.created)
        self.assertIsNotNone(workflow.modified)

    def test_workflow_str(self):
        """Test workflow string representation"""
        workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-workflow-123'
        )
        
        self.assertEqual(str(workflow), 'Test Workflow (test-workflow-123)')

    def test_workflow_unique_workflow_id(self):
        """Test that workflow_id must be unique"""
        Workflow.objects.create(
            name='Workflow 1',
            workflow_id='unique-id'
        )
        
        with self.assertRaises(Exception):
            Workflow.objects.create(
                name='Workflow 2',
                workflow_id='unique-id'
            )


class WorkflowRunModelTestCase(TestCase):
    """Test cases for WorkflowRun model"""

    def setUp(self):
        self.workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-workflow-123'
        )

    def test_workflow_run_creation(self):
        """Test creating a workflow run"""
        run = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='test-run-456',
            status='pending'
        )
        
        self.assertEqual(run.workflow, self.workflow)
        self.assertEqual(run.run_id, 'test-run-456')
        self.assertEqual(run.status, 'pending')
        self.assertIsNotNone(run.created)

    def test_workflow_run_str(self):
        """Test workflow run string representation"""
        run = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='test-run-456'
        )
        
        self.assertEqual(str(run), 'Test Workflow - Run test-run-456')


class WorkflowScheduleModelTestCase(TestCase):
    """Test cases for WorkflowSchedule model"""

    def setUp(self):
        self.workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-workflow-123'
        )

    def test_workflow_schedule_creation(self):
        """Test creating a workflow schedule"""
        schedule = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='0 * * * *',
            is_active=True
        )
        
        self.assertEqual(schedule.workflow, self.workflow)
        self.assertEqual(schedule.cron_expression, '0 * * * *')
        self.assertTrue(schedule.is_active)

    def test_workflow_schedule_str(self):
        """Test workflow schedule string representation"""
        schedule = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='0 * * * *'
        )
        
        self.assertEqual(str(schedule), 'Test Workflow - 0 * * * *')


class WorkflowCRUDTestCase(TestCase):
    """Test cases for Workflow CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/workflows/workflows'

    def test_create_workflow(self):
        """Test creating a new workflow"""
        data = {
            'name': 'Deploy Workflow',
            'workflow_id': 'deploy-123',
            'workflow_type': 'deploy',
            'status': 'pending'
        }
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], 'Deploy Workflow')
        self.assertEqual(response.data['workflow_id'], 'deploy-123')
        self.assertEqual(response.data['workflow_type'], 'deploy')
        self.assertTrue(Workflow.objects.filter(id=response.data['id']).exists())

    def test_list_workflows_empty(self):
        """Test listing workflows when none exist"""
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_workflows_with_data(self):
        """Test listing workflows with existing data"""
        workflow1 = Workflow.objects.create(
            name='Workflow 1',
            workflow_id='workflow-1',
            workflow_type='deploy'
        )
        workflow2 = Workflow.objects.create(
            name='Workflow 2',
            workflow_id='workflow-2',
            workflow_type='validate'
        )
        
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_workflow(self):
        """Test retrieving a specific workflow"""
        workflow = Workflow.objects.create(
            name='Retrieve Test',
            workflow_id='retrieve-123'
        )
        url = f'{self.base_url}/{workflow.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], workflow.id)
        self.assertEqual(response.data['name'], 'Retrieve Test')

    def test_update_workflow(self):
        """Test updating a workflow"""
        workflow = Workflow.objects.create(
            name='Original Name',
            workflow_id='original-123'
        )
        url = f'{self.base_url}/{workflow.id}'
        update_data = {
            'name': 'Updated Name',
            'workflow_id': 'original-123',
            'status': 'running'
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        self.assertEqual(response.data['status'], 'running')

    def test_partial_update_workflow(self):
        """Test partial update of a workflow"""
        workflow = Workflow.objects.create(
            name='Original Name',
            workflow_id='original-123'
        )
        url = f'{self.base_url}/{workflow.id}'
        update_data = {'status': 'completed'}
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_delete_workflow(self):
        """Test deleting a workflow"""
        workflow = Workflow.objects.create(
            name='Delete Test',
            workflow_id='delete-123'
        )
        url = f'{self.base_url}/{workflow.id}'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Workflow.objects.filter(id=workflow.id).exists())

    def test_filter_workflows_by_type(self):
        """Test filtering workflows by type"""
        Workflow.objects.create(
            name='Deploy Workflow',
            workflow_id='deploy-1',
            workflow_type='deploy'
        )
        Workflow.objects.create(
            name='Validate Workflow',
            workflow_id='validate-1',
            workflow_type='validate'
        )
        
        url = f'{self.base_url}?workflow_type=deploy'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['workflow_type'], 'deploy')

    def test_filter_workflows_by_status(self):
        """Test filtering workflows by status"""
        Workflow.objects.create(
            name='Workflow 1',
            workflow_id='workflow-1',
            status='pending'
        )
        Workflow.objects.create(
            name='Workflow 2',
            workflow_id='workflow-2',
            status='running'
        )
        
        url = f'{self.base_url}?status=running'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'running')


class WorkflowRunCRUDTestCase(TestCase):
    """Test cases for WorkflowRun CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/workflows/workflow-runs'
        self.workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-123'
        )

    def test_create_workflow_run(self):
        """Test creating a new workflow run"""
        data = {
            'workflow': self.workflow.id,
            'run_id': 'run-456',
            'status': 'pending'
        }
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['workflow'], self.workflow.id)
        self.assertEqual(response.data['run_id'], 'run-456')
        self.assertTrue(WorkflowRun.objects.filter(id=response.data['id']).exists())

    def test_list_workflow_runs_empty(self):
        """Test listing workflow runs when none exist"""
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_workflow_runs_with_data(self):
        """Test listing workflow runs with existing data"""
        run1 = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='run-1'
        )
        run2 = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='run-2'
        )
        
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_workflow_run(self):
        """Test retrieving a specific workflow run"""
        run = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='retrieve-run'
        )
        url = f'{self.base_url}/{run.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], run.id)
        self.assertEqual(response.data['run_id'], 'retrieve-run')

    def test_update_workflow_run(self):
        """Test updating a workflow run"""
        run = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='update-run',
            status='pending'
        )
        url = f'{self.base_url}/{run.id}'
        update_data = {
            'workflow': self.workflow.id,
            'run_id': 'update-run',
            'status': 'running'
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'running')

    def test_delete_workflow_run(self):
        """Test deleting a workflow run"""
        run = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='delete-run'
        )
        url = f'{self.base_url}/{run.id}'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkflowRun.objects.filter(id=run.id).exists())

    def test_filter_workflow_runs_by_workflow(self):
        """Test filtering workflow runs by workflow"""
        workflow2 = Workflow.objects.create(
            name='Workflow 2',
            workflow_id='workflow-2'
        )
        run1 = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='run-1'
        )
        WorkflowRun.objects.create(
            workflow=workflow2,
            run_id='run-2'
        )
        
        url = f'{self.base_url}?workflow_id={self.workflow.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['workflow'], self.workflow.id)

    def test_filter_workflow_runs_by_status(self):
        """Test filtering workflow runs by status"""
        WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='run-1',
            status='pending'
        )
        WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='run-2',
            status='running'
        )
        
        url = f'{self.base_url}?status=running'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'running')


class WorkflowScheduleCRUDTestCase(TestCase):
    """Test cases for WorkflowSchedule CRUD operations"""

    def setUp(self):
        self.client = APIClient()
        self.base_url = '/api/workflows/workflow-schedules'
        self.workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-123'
        )

    def test_create_workflow_schedule(self):
        """Test creating a new workflow schedule"""
        data = {
            'workflow': self.workflow.id,
            'cron_expression': '0 * * * *',
            'is_active': True
        }
        response = self.client.post(self.base_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['workflow'], self.workflow.id)
        self.assertEqual(response.data['cron_expression'], '0 * * * *')
        self.assertTrue(response.data['is_active'])
        self.assertTrue(WorkflowSchedule.objects.filter(id=response.data['id']).exists())

    def test_list_workflow_schedules_empty(self):
        """Test listing workflow schedules when none exist"""
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_workflow_schedules_with_data(self):
        """Test listing workflow schedules with existing data"""
        schedule1 = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='0 * * * *'
        )
        schedule2 = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='0 0 * * *'
        )
        
        response = self.client.get(self.base_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_workflow_schedule(self):
        """Test retrieving a specific workflow schedule"""
        schedule = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='retrieve-cron'
        )
        url = f'{self.base_url}/{schedule.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], schedule.id)
        self.assertEqual(response.data['cron_expression'], 'retrieve-cron')

    def test_update_workflow_schedule(self):
        """Test updating a workflow schedule"""
        schedule = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='original-cron',
            is_active=True
        )
        url = f'{self.base_url}/{schedule.id}'
        update_data = {
            'workflow': self.workflow.id,
            'cron_expression': 'updated-cron',
            'is_active': False
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cron_expression'], 'updated-cron')
        self.assertFalse(response.data['is_active'])

    def test_delete_workflow_schedule(self):
        """Test deleting a workflow schedule"""
        schedule = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='delete-cron'
        )
        url = f'{self.base_url}/{schedule.id}'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkflowSchedule.objects.filter(id=schedule.id).exists())

    def test_filter_workflow_schedules_by_workflow(self):
        """Test filtering workflow schedules by workflow"""
        workflow2 = Workflow.objects.create(
            name='Workflow 2',
            workflow_id='workflow-2'
        )
        schedule1 = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='cron-1'
        )
        WorkflowSchedule.objects.create(
            workflow=workflow2,
            cron_expression='cron-2'
        )
        
        url = f'{self.base_url}?workflow_id={self.workflow.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['workflow'], self.workflow.id)

    def test_filter_workflow_schedules_by_active(self):
        """Test filtering workflow schedules by active status"""
        WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='cron-1',
            is_active=True
        )
        WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='cron-2',
            is_active=False
        )
        
        url = f'{self.base_url}?is_active=true'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]['is_active'])


class WorkflowActionTestCase(TestCase):
    """Test cases for Workflow custom actions"""

    def setUp(self):
        self.client = APIClient()
        self.workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-123',
            status='pending'
        )
        self.base_url = '/api/workflows/workflows'

    def test_workflow_run_action(self):
        """Test the run action on a workflow"""
        url = f'{self.base_url}/{self.workflow.id}/run'
        data = {'parameters': {'device_id': 1}}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['workflow'], self.workflow.id)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(response.data['parameters'], {'device_id': 1})
        self.assertTrue(WorkflowRun.objects.filter(id=response.data['id']).exists())

    def test_workflow_cancel_action(self):
        """Test the cancel action on a workflow"""
        url = f'{self.base_url}/{self.workflow.id}/cancel'
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'cancelled')
        
        self.workflow.refresh_from_db()
        self.assertEqual(self.workflow.status, 'cancelled')

    def test_workflow_cancel_invalid_state(self):
        """Test cancelling a workflow with invalid state"""
        self.workflow.status = 'completed'
        self.workflow.save()
        
        url = f'{self.base_url}/{self.workflow.id}/cancel'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class WorkflowRunActionTestCase(TestCase):
    """Test cases for WorkflowRun custom actions"""

    def setUp(self):
        self.client = APIClient()
        self.workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-123'
        )
        self.run = WorkflowRun.objects.create(
            workflow=self.workflow,
            run_id='run-456',
            status='completed'
        )
        self.base_url = '/api/workflows/workflow-runs'

    def test_workflow_run_retry_action(self):
        """Test the retry action on a workflow run"""
        url = f'{self.base_url}/{self.run.id}/retry'
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['workflow'], self.workflow.id)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(response.data['parameters'], self.run.parameters)
        self.assertTrue(WorkflowRun.objects.filter(id=response.data['id']).exists())


class WorkflowScheduleActionTestCase(TestCase):
    """Test cases for WorkflowSchedule custom actions"""

    def setUp(self):
        self.client = APIClient()
        self.workflow = Workflow.objects.create(
            name='Test Workflow',
            workflow_id='test-123'
        )
        self.schedule = WorkflowSchedule.objects.create(
            workflow=self.workflow,
            cron_expression='0 * * * *',
            is_active=False
        )
        self.base_url = '/api/workflows/workflow-schedules'

    def test_workflow_schedule_activate_action(self):
        """Test the activate action on a workflow schedule"""
        url = f'{self.base_url}/{self.schedule.id}/activate'
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_active'])
        
        self.schedule.refresh_from_db()
        self.assertTrue(self.schedule.is_active)

    def test_workflow_schedule_deactivate_action(self):
        """Test the deactivate action on a workflow schedule"""
        self.schedule.is_active = True
        self.schedule.save()
        
        url = f'{self.base_url}/{self.schedule.id}/deactivate'
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_active'])
        
        self.schedule.refresh_from_db()
        self.assertFalse(self.schedule.is_active)
