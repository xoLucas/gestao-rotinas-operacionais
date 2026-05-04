from django.db import models

# Create your models here.

class OperationalArea(models.Model):
    station = models.ForeignKey(
        "organizations.Station",
        on_delete=models.CASCADE,
        related_name="areas",
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    radius_meters = models.PositiveIntegerField(default=50)

    requires_authorization = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Área operacional"
        verbose_name_plural = "Áreas operacionais"

    def __str__(self):
        return f"{self.station.code} - {self.name}"


class OperationalRoute(models.Model):
    station = models.ForeignKey(
        "organizations.Station",
        on_delete=models.CASCADE,
        related_name="routes",
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    areas = models.ManyToManyField(
        OperationalArea,
        related_name="routes",
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Rota operacional"
        verbose_name_plural = "Rotas operacionais"

    def __str__(self):
        return f"{self.station.code} - {self.name}"


class Asset(models.Model):
    class AssetType(models.TextChoices):
        TANK = "tank", "Tanque"
        PUMP = "pump", "Bomba"
        VESSEL = "vessel", "Vaso de pressão"
        COMPRESSOR = "compressor", "Compressor"
        FLARE = "flare", "Flare"
        API_BOX = "api_box", "Caixa API"
        VALVE = "valve", "Válvula"
        PIPELINE = "pipeline", "Duto/Tubulação"
        OTHER = "other", "Outro"

    area = models.ForeignKey(
        OperationalArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assets",
    )
    tag = models.CharField(max_length=80, blank=True)
    name = models.CharField(max_length=150)
    asset_type = models.CharField(max_length=30, choices=AssetType.choices)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ativo/Equipamento"
        verbose_name_plural = "Ativos/Equipamentos"

    def __str__(self):
        return self.tag or self.name