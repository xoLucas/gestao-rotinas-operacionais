from django.contrib import admin

from .models import OperationalArea, OperationalRoute, Asset


@admin.register(OperationalArea)
class OperationalAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "station", "radius_meters", "requires_authorization", "is_active")
    search_fields = ("name", "station__code")
    list_filter = ("station", "requires_authorization", "is_active")


@admin.register(OperationalRoute)
class OperationalRouteAdmin(admin.ModelAdmin):
    list_display = ("name", "station", "is_active")
    search_fields = ("name", "station__code")
    list_filter = ("station", "is_active")
    filter_horizontal = ("areas",)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("tag", "name", "asset_type", "area", "is_active")
    search_fields = ("tag", "name")
    list_filter = ("asset_type", "area", "is_active")