from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Workflow, WorkflowRun, WorkflowSchedule
from .serializers import WorkflowSerializer, WorkflowRunSerializer, WorkflowScheduleSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        workflow_type = self.request.query_params.get('workflow_type')
        status_filter = self.request.query_params.get('status')
        
        if workflow_type:
            queryset = queryset.filter(workflow_type=workflow_type)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created')

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        workflow = self.get_object()
        
        try:
            run = WorkflowRun.objects.create(
                workflow=workflow,
                run_id=f"{workflow.workflow_id}-{workflow.runs.count() + 1}",
                status='pending',
                parameters=request.data.get('parameters', {})
            )
            
            serializer = WorkflowRunSerializer(run)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        workflow = self.get_object()
        
        if workflow.status not in ['pending', 'running']:
            return Response(
                {'error': 'Cannot cancel a workflow that is not pending or running'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        workflow.status = 'cancelled'
        workflow.save()
        
        serializer = self.get_serializer(workflow)
        return Response(serializer.data)


class WorkflowRunViewSet(viewsets.ModelViewSet):
    queryset = WorkflowRun.objects.all()
    serializer_class = WorkflowRunSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        workflow_id = self.request.query_params.get('workflow_id')
        status_filter = self.request.query_params.get('status')
        
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created')

    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        run = self.get_object()
        
        new_run = WorkflowRun.objects.create(
            workflow=run.workflow,
            run_id=f"{run.run_id}-retry-{run.workflow.runs.count() + 1}",
            status='pending',
            parameters=run.parameters
        )
        
        serializer = self.get_serializer(new_run)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WorkflowScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkflowSchedule.objects.all()
    serializer_class = WorkflowScheduleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        workflow_id = self.request.query_params.get('workflow_id')
        is_active = self.request.query_params.get('is_active')
        
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset.order_by('-created')

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        schedule = self.get_object()
        schedule.is_active = True
        schedule.save()
        
        serializer = self.get_serializer(schedule)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        schedule = self.get_object()
        schedule.is_active = False
        schedule.save()
        
        serializer = self.get_serializer(schedule)
        return Response(serializer.data)
