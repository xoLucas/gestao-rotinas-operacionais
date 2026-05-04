from django.contrib import admin

from .models import ShiftReport, PunctualityScore


@admin.register(ShiftReport)
class ShiftReportAdmin(admin.ModelAdmin):
    list_display = ("work_session", "created_by", "created_at")
    search_fields = ("summary", "created_by__username")


@admin.register(PunctualityScore)
class PunctualityScoreAdmin(admin.ModelAdmin):
    list_display = ("operator", "reference_date", "total_routines", "completed_on_time", "completed_late", "not_done", "score")
    search_fields = ("operator__username",)
    list_filter = ("reference_date",)