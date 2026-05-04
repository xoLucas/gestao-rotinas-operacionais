from django.db import models
from django.conf import settings

# Create your models here.

class OperatorProfile(models.Model):
    class Role(models.TextChoices):
        OPERATION_MANAGER = "operation_manager", "Gerente de operação"
        COORDINATOR = "coordinator", "Coordenador/Líder"
        SUPERVISOR = "supervisor", "Supervisor de operação"
        CONTROL_ROOM_OPERATOR = "control_room_operator", "Operador de sala de controle"
        FIELD_OPERATOR = "field_operator", "Operador de estação"
        OPERATIONS_ASSISTANT = "operations_assistant", "Assistente de operações"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="operator_profile",
    )
    team = models.ForeignKey(
        "organizations.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )
    role = models.CharField(max_length=40, choices=Role.choices)
    registration_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Perfil operacional"
        verbose_name_plural = "Perfis operacionais"

    def __str__(self):
        return self.user.get_full_name() or self.user.username