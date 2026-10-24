from django.db import models
from django.utils import timezone


class WorkflowStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    RUNNING = 'running', 'Running'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'


class WorkflowType(models.TextChoices):
    DEPLOY = 'deploy', 'Deploy'
    ROLLBACK = 'rollback', 'Rollback'
    VALIDATE = 'validate', 'Validate'
    SYNC = 'sync', 'Sync'


class Workflow(models.Model):
    name = models.CharField(max_length=255)
    workflow_id = models.CharField(max_length=255, unique=True, help_text="Prefect workflow ID")
    workflow_type = models.CharField(
        max_length=20,
        choices=WorkflowType.choices,
        default=WorkflowType.DEPLOY
    )
    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.PENDING
    )
    parameters = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} ({self.workflow_id})"


class WorkflowRun(models.Model):
    workflow = models.ForeignKey(
        Workflow, 
        on_delete=models.CASCADE, 
        related_name='runs'
    )
    run_id = models.CharField(max_length=255, unique=True, help_text="Prefect run ID")
    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.PENDING
    )
    parameters = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Workflow Run'
        verbose_name_plural = 'Workflow Runs'

    def __str__(self):
        return f"{self.workflow.name} - Run {self.run_id}"


class WorkflowSchedule(models.Model):
    workflow = models.ForeignKey(
        Workflow, 
        on_delete=models.CASCADE, 
        related_name='schedules'
    )
    cron_expression = models.CharField(max_length=100, help_text="Cron expression for scheduling")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    next_run_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Workflow Schedule'
        verbose_name_plural = 'Workflow Schedules'

    def __str__(self):
        return f"{self.workflow.name} - {self.cron_expression}"
