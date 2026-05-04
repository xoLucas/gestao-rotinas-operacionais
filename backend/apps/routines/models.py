from django.db import models

# Create your models here.

class ProcedureDocument(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    revision = models.CharField(max_length=20)
    issue_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Procedimento"
        verbose_name_plural = "Procedimentos"
        unique_together = ("code", "revision")

    def __str__(self):
        return f"{self.code} Rev. {self.revision}"


class Routine(models.Model):
    class Category(models.TextChoices):
        OPERATIONAL_ROUTINE = "operational_routine", "Rotina da operação"
        CRITICAL_TASK = "critical_task", "Tarefa crítica"
        EQUIPMENT_RELEASE = "equipment_release", "Liberação de equipamento"
        OPERATIONAL_RETURN = "operational_return", "Retorno operacional"
        SHIFT_HANDOVER = "shift_handover", "Passagem de serviço"
        SAFETY_DIALOGUE = "safety_dialogue", "Diálogo de segurança"

    class Criticality(models.TextChoices):
        LOW = "low", "Baixa"
        MEDIUM = "medium", "Média"
        HIGH = "high", "Alta"
        CRITICAL = "critical", "Crítica"

    procedure = models.ForeignKey(
        ProcedureDocument,
        on_delete=models.PROTECT,
        related_name="routines",
        null=True,
        blank=True,
    )
    procedure_item = models.CharField(max_length=30, blank=True)

    name = models.CharField(max_length=150)
    instruction = models.TextField()

    category = models.CharField(
        max_length=40,
        choices=Category.choices,
        default=Category.OPERATIONAL_ROUTINE,
    )
    criticality = models.CharField(
        max_length=20,
        choices=Criticality.choices,
        default=Criticality.MEDIUM,
    )

    station = models.ForeignKey(
        "organizations.Station",
        on_delete=models.CASCADE,
        related_name="routines",
    )
    area = models.ForeignKey(
        "operations.OperationalArea",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="routines",
    )
    route = models.ForeignKey(
        "operations.OperationalRoute",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="routines",
    )
    asset = models.ForeignKey(
        "operations.Asset",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="routines",
    )

    requires_photo = models.BooleanField(default=False)
    requires_geolocation = models.BooleanField(default=False)
    requires_observation = models.BooleanField(default=False)
    can_generate_service_request = models.BooleanField(default=True)

    priority = models.PositiveSmallIntegerField(default=3)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Rotina"
        verbose_name_plural = "Rotinas"
        ordering = ["priority", "name"]

    def __str__(self):
        if self.procedure_item:
            return f"{self.procedure_item} - {self.name}"
        return self.name


class RoutineStep(models.Model):
    routine = models.ForeignKey(
        Routine,
        on_delete=models.CASCADE,
        related_name="steps",
    )
    order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_required = models.BooleanField(default=True)
    requires_photo = models.BooleanField(default=False)
    requires_value_input = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Etapa da rotina"
        verbose_name_plural = "Etapas da rotina"
        ordering = ["order"]

    def __str__(self):
        return f"{self.routine} - {self.order}. {self.title}"