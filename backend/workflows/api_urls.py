from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import WorkflowViewSet, WorkflowRunViewSet, WorkflowScheduleViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'workflows', WorkflowViewSet, basename="api-workflows")
router.register(r'workflow-runs', WorkflowRunViewSet, basename="api-workflow-runs")
router.register(r'workflow-schedules', WorkflowScheduleViewSet, basename="api-workflow-schedules")

urlpatterns = router.urls
