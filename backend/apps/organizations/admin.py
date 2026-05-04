from django.contrib import admin

from .models import Company, Station, Sector, Team


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "company", "is_active")
    search_fields = ("code", "name")
    list_filter = ("company", "is_active")


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("name", "station", "is_active")
    search_fields = ("name", "station__code", "station__name")
    list_filter = ("station", "is_active")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "sector", "is_active")
    search_fields = ("name", "sector__name")
    list_filter = ("sector", "is_active")