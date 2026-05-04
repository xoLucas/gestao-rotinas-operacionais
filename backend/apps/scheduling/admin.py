from django.contrib import admin

from .models import Shift, ScheduleRule


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("name", "station", "start_time", "end_time", "is_active")
    search_fields = ("name", "station__code")
    list_filter = ("station", "is_active")


@admin.register(ScheduleRule)
class ScheduleRuleAdmin(admin.ModelAdmin):
    list_display = ("routine", "shift", "frequency_type", "interval_hours", "fixed_time", "is_active")
    search_fields = ("routine__name",)
    list_filter = ("frequency_type", "shift", "is_active")