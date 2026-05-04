from django.db import models

# Create your models here.

class Shift(models.Model):
    station = models.ForeignKey(
        "organizations.Station",
        on_delete=models.CASCADE,
        related_name="shifts",
    )
    name = models.CharField(max_length=80)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    def __str__(self):
        return f"{self.station.code} - {self.name}"


class ScheduleRule(models.Model):
    class FrequencyType(models.TextChoices):
        ONCE_PER_SHIFT = "once_per_shift", "Uma vez por turno"
        SHIFT_START = "shift_start", "Início do turno"
        SHIFT_END = "shift_end", "Fim do turno"
        EVERY_X_HOURS = "every_x_hours", "A cada X horas"
        DAILY = "daily", "Diária"
        WEEKLY = "weekly", "Semanal"
        SPECIFIC_WEEKDAYS = "specific_weekdays", "Dias específicos da semana"
        FIXED_TIME = "fixed_time", "Horário fixo"
        ON_DEMAND = "on_demand", "Sob demanda"
        CAMPAIGN = "campaign", "Campanha/Cronograma"

    routine = models.ForeignKey(
        "routines.Routine",
        on_delete=models.CASCADE,
        related_name="schedule_rules",
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="schedule_rules",
    )

    frequency_type = models.CharField(max_length=40, choices=FrequencyType.choices)

    interval_hours = models.PositiveSmallIntegerField(null=True, blank=True)
    fixed_time = models.TimeField(null=True, blank=True)

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    window_before_minutes = models.PositiveIntegerField(default=0)
    window_after_minutes = models.PositiveIntegerField(default=60)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Regra de agendamento"
        verbose_name_plural = "Regras de agendamento"

    def __str__(self):
        return f"{self.routine} - {self.get_frequency_type_display()}"