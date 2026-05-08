from django.contrib import admin

from .models import (
    AdminProfile,
    Customer,
    Gauge,
    ManagerProfile,
    Photo,
    Reading,
    Site,
    SiteGroup,
    TechnicianProfile,
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "contact_email", "member_since")
    search_fields = ("name", "contact_person", "contact_email")


@admin.register(SiteGroup)
class SiteGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "customer", "group", "address")
    list_filter = ("group", "customer")
    search_fields = ("name", "address", "customer__name")


@admin.register(Gauge)
class GaugeAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "site", "installed_on")
    search_fields = ("serial_number",)
    list_filter = ("site__customer",)


@admin.register(TechnicianProfile)
class TechnicianProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "employee_id", "phone")
    search_fields = ("user__username", "employee_id")
    filter_horizontal = ("assigned_sites", "assigned_gauges")


@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "phone")
    search_fields = ("user__username", "department")


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "gauge", "taken_at", "uploaded_by")
    list_filter = ("gauge__site__customer",)
    readonly_fields = ("taken_at",)


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gauge",
        "serial_number_verified",
        "consumed_volume_verified",
        "recorded_at",
        "recorded_by",
    )
    search_fields = ("gauge__serial_number", "serial_number_verified")
    list_filter = ("recorded_at",)
    readonly_fields = ("recorded_at",)
