from django.contrib import admin

from .models import OperatorProfile


@admin.register(OperatorProfile)
class OperatorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "team", "registration_number", "is_active")
    search_fields = ("user__username", "user__first_name", "user__last_name", "registration_number")
    list_filter = ("role", "team", "is_active")