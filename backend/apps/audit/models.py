from django.db import models
from django.conf import settings

# Create your models here.

class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "create", "Criação"
        UPDATE = "update", "Alteração"
        DELETE = "delete", "Exclusão"
        LOGIN = "login", "Login"
        SYNC = "sync", "Sincronização"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=20, choices=Action.choices)
    model_name = models.CharField(max_length=120)
    object_id = models.CharField(max_length=80, blank=True)
    previous_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log de auditoria"
        verbose_name_plural = "Logs de auditoria"

    def __str__(self):
        return f"{self.get_action_display()} - {self.model_name} - {self.created_at}"