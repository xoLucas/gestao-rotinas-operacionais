from django.db import models
from django.conf import settings

# Create your models here.

class ShiftReport(models.Model):
    work_session = models.OneToOneField(
        "execution.WorkSession",
        on_delete=models.CASCADE,
        related_name="shift_report",
    )
    summary = models.TextField()
    abnormalities_summary = models.TextField(blank=True)
    service_requests_summary = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_shift_reports",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Relatório de passagem de serviço"
        verbose_name_plural = "Relatórios de passagem de serviço"

    def __str__(self):
        return f"Passagem de serviço - {self.work_session}"


class PunctualityScore(models.Model):
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="punctuality_scores",
    )
    reference_date = models.DateField()
    total_routines = models.PositiveIntegerField(default=0)
    completed_on_time = models.PositiveIntegerField(default=0)
    completed_late = models.PositiveIntegerField(default=0)
    not_done = models.PositiveIntegerField(default=0)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Score de pontualidade"
        verbose_name_plural = "Scores de pontualidade"
        unique_together = ("operator", "reference_date")

    def __str__(self):
        return f"{self.operator} - {self.reference_date} - {self.score}"