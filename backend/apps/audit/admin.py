from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "model_name", "object_id", "user", "created_at")
    search_fields = ("model_name", "object_id", "user__username")
    list_filter = ("action", "model_name", "created_at")
    readonly_fields = ("created_at",)