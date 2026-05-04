from django.contrib import admin

from .models import (
    WorkSession,
    RoutineExecution,
    ExecutionStepResult,
    Abnormality,
    ServiceRequestRecord,
)


class ExecutionStepResultInline(admin.TabularInline):
    model = ExecutionStepResult
    extra = 0


class AbnormalityInline(admin.TabularInline):
    model = Abnormality
    extra = 0


@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    list_display = ("operator", "shift", "started_at", "ended_at", "device_id")
    search_fields = ("operator__username", "device_id")
    list_filter = ("shift", "started_at")


@admin.register(RoutineExecution)
class RoutineExecutionAdmin(admin.ModelAdmin):
    list_display = ("routine", "work_session", "status", "planned_start_at", "completed_at", "has_abnormality")
    search_fields = ("routine__name", "work_session__operator__username")
    list_filter = ("status", "has_abnormality", "service_request_required")
    inlines = [ExecutionStepResultInline, AbnormalityInline]


@admin.register(ExecutionStepResult)
class ExecutionStepResultAdmin(admin.ModelAdmin):
    list_display = ("execution", "step", "is_completed", "completed_at")
    search_fields = ("step__title", "execution__routine__name")
    list_filter = ("is_completed",)


@admin.register(Abnormality)
class AbnormalityAdmin(admin.ModelAdmin):
    list_display = (
        "execution",
        "risk_to_people",
        "environmental_risk",
        "equipment_integrity_risk",
        "communicated_to_supervisor",
        "created_at",
    )
    search_fields = ("description", "execution__routine__name")
    list_filter = (
        "risk_to_people",
        "environmental_risk",
        "equipment_integrity_risk",
        "communicated_to_supervisor",
    )


@admin.register(ServiceRequestRecord)
class ServiceRequestRecordAdmin(admin.ModelAdmin):
    list_display = ("external_code", "external_system", "abnormality", "created_at")
    search_fields = ("external_code", "description")