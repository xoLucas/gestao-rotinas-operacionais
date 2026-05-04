from django.contrib import admin

from .models import ProcedureDocument, Routine, RoutineStep


class RoutineStepInline(admin.TabularInline):
    model = RoutineStep
    extra = 1


@admin.register(ProcedureDocument)
class ProcedureDocumentAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "revision", "issue_date", "is_active")
    search_fields = ("code", "title", "revision")
    list_filter = ("is_active",)


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "procedure_item",
        "category",
        "criticality",
        "station",
        "area",
        "requires_photo",
        "requires_geolocation",
        "is_active",
    )
    search_fields = ("name", "instruction", "procedure_item")
    list_filter = (
        "category",
        "criticality",
        "station",
        "requires_photo",
        "requires_geolocation",
        "is_active",
    )
    inlines = [RoutineStepInline]


@admin.register(RoutineStep)
class RoutineStepAdmin(admin.ModelAdmin):
    list_display = ("routine", "order", "title", "is_required", "requires_photo", "requires_value_input")
    search_fields = ("title", "description", "routine__name")
    list_filter = ("is_required", "requires_photo", "requires_value_input")