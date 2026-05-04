from django.contrib import admin

from .models import Evidence


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ("evidence_type", "execution", "is_inside_geofence", "collected_by", "collected_at")
    search_fields = ("execution__routine__name", "collected_by__username")
    list_filter = ("evidence_type", "is_inside_geofence", "collected_at")