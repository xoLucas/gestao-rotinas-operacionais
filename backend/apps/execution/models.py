from django.db import models
from django.conf import settings

# Create your models here.

class WorkSession(models.Model):
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="work_sessions",
    )
    shift = models.ForeignKey(
        "scheduling.Shift",
        on_delete=models.PROTECT,
        related_name="work_sessions",
    )
    device_id = models.CharField(max_length=120, blank=True)

    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name = "Sessão de trabalho"
        verbose_name_plural = "Sessões de trabalho"

    def __str__(self):
        return f"{self.operator} - {self.shift} - {self.started_at}"


class RoutineExecution(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        CLAIMED = "claimed", "Assumida"
        IN_PROGRESS = "in_progress", "Em execução"
        COMPLETED = "completed", "Concluída"
        LATE = "late", "Atrasada"
        NOT_DONE = "not_done", "Não realizada"
        BLOCKED = "blocked", "Bloqueada"
        SYNC_PENDING = "sync_pending", "Sincronização pendente"

    work_session = models.ForeignKey(
        WorkSession,
        on_delete=models.CASCADE,
        related_name="executions",
    )
    routine = models.ForeignKey(
        "routines.Routine",
        on_delete=models.PROTECT,
        related_name="executions",
    )

    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="claimed_executions",
    )

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)

    planned_start_at = models.DateTimeField(null=True, blank=True)
    planned_end_at = models.DateTimeField(null=True, blank=True)

    claimed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    observation = models.TextField(blank=True)
    outside_geofence_justification = models.TextField(blank=True)

    has_abnormality = models.BooleanField(default=False)
    service_request_required = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Execução de rotina"
        verbose_name_plural = "Execuções de rotinas"

    def __str__(self):
        return f"{self.routine} - {self.get_status_display()}"


class ExecutionStepResult(models.Model):
    execution = models.ForeignKey(
        RoutineExecution,
        on_delete=models.CASCADE,
        related_name="step_results",
    )
    step = models.ForeignKey(
        "routines.RoutineStep",
        on_delete=models.PROTECT,
        related_name="execution_results",
    )
    is_completed = models.BooleanField(default=False)
    observation = models.TextField(blank=True)
    value = models.CharField(max_length=120, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Resultado da etapa"
        verbose_name_plural = "Resultados das etapas"

    def __str__(self):
        return f"{self.execution} - {self.step}"


class Abnormality(models.Model):
    execution = models.ForeignKey(
        RoutineExecution,
        on_delete=models.CASCADE,
        related_name="abnormalities",
    )
    description = models.TextField()
    risk_to_people = models.BooleanField(default=False)
    environmental_risk = models.BooleanField(default=False)
    equipment_integrity_risk = models.BooleanField(default=False)
    communicated_to_supervisor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Anormalidade"
        verbose_name_plural = "Anormalidades"

    def __str__(self):
        return f"Anormalidade - {self.execution}"


class ServiceRequestRecord(models.Model):
    abnormality = models.OneToOneField(
        Abnormality,
        on_delete=models.CASCADE,
        related_name="service_request",
    )
    external_system = models.CharField(max_length=80, default="Sistema de manutenção")
    external_code = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de SS"
        verbose_name_plural = "Registros de SS"

    def __str__(self):
        return self.external_code or f"SS - {self.abnormality}"