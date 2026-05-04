from django.db import models
from django.conf import settings

# Create your models here.

class Evidence(models.Model):
    class EvidenceType(models.TextChoices):
        PHOTO = "photo", "Foto"
        LOCATION = "location", "Localização"
        DOCUMENT = "document", "Documento"
        SIGNATURE = "signature", "Assinatura"

    execution = models.ForeignKey(
        "execution.RoutineExecution",
        on_delete=models.CASCADE,
        related_name="evidences",
    )
    evidence_type = models.CharField(max_length=30, choices=EvidenceType.choices)

    file = models.FileField(upload_to="evidences/", null=True, blank=True)
    external_url = models.URLField(blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    accuracy_meters = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    is_inside_geofence = models.BooleanField(null=True, blank=True)

    collected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="collected_evidences",
    )
    collected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Evidência"
        verbose_name_plural = "Evidências"

    def __str__(self):
        return f"{self.get_evidence_type_display()} - {self.execution}"