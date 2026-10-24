from rest_framework import serializers
from .models import Workflow, WorkflowRun, WorkflowSchedule


class WorkflowScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowSchedule
        fields = ['id', 'workflow', 'cron_expression', 'is_active', 'created', 'modified', 'next_run_at']
        read_only_fields = ['id', 'created', 'modified']


class WorkflowRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowRun
        fields = [
            'id', 'workflow', 'run_id', 'status', 'parameters', 
            'result', 'error_message', 'created', 'modified', 
            'started_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created', 'modified', 'started_at', 'completed_at']


class WorkflowSerializer(serializers.ModelSerializer):
    runs = WorkflowRunSerializer(many=True, read_only=True)
    schedules = WorkflowScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = [
            'id', 'name', 'workflow_id', 'workflow_type', 'status', 
            'parameters', 'result', 'error_message', 'created', 'modified',
            'started_at', 'completed_at', 'runs', 'schedules'
        ]
        read_only_fields = ['id', 'created', 'modified', 'started_at', 'completed_at']
