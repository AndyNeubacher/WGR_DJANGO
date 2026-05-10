from django.contrib import admin
from django import forms

from . import models


class ContactAdminForm(forms.ModelForm):

    class Meta:
        model = models.Contact
        fields = "__all__"


class ContactAdmin(admin.ModelAdmin):
    form = ContactAdminForm
    list_display = [
        "name",
        "address",
        "telephone",
        "email",
        "comments",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class CustomerAdminForm(forms.ModelForm):

    class Meta:
        model = models.Customer
        fields = "__all__"


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm
    list_display = [
        "last_updated",
        "comments",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class GaugeAdminForm(forms.ModelForm):

    class Meta:
        model = models.Gauge
        fields = "__all__"


class GaugeAdmin(admin.ModelAdmin):
    form = GaugeAdminForm
    list_display = [
        "serial",
        "type",
        "state",
        "date_calibrated",
        "date_installed",
        "date_expire",
        "created",
        "last_updated",
        "last_consumed",
        "comments",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class GroupAdminForm(forms.ModelForm):

    class Meta:
        model = models.Group
        fields = "__all__"


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = [
        "name",
        "created",
        "last_updated",
        "comments",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class ImagesAdminForm(forms.ModelForm):

    class Meta:
        model = models.Images
        fields = "__all__"


class ImagesAdmin(admin.ModelAdmin):
    form = ImagesAdminForm
    list_display = [
        "image",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class LocationAdminForm(forms.ModelForm):

    class Meta:
        model = models.Location
        fields = "__all__"


class LocationAdmin(admin.ModelAdmin):
    form = LocationAdminForm
    list_display = [
        "address",
        "longitude",
        "latitude",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class MeasurementAdminForm(forms.ModelForm):

    class Meta:
        model = models.Measurement
        fields = "__all__"


class MeasurementAdmin(admin.ModelAdmin):
    form = MeasurementAdminForm
    list_display = [
        "date_measured",
        "consumed",
        "comments",
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class SiteAdminForm(forms.ModelForm):

    class Meta:
        model = models.Site
        fields = "__all__"


class SiteAdmin(admin.ModelAdmin):
    form = SiteAdminForm
    list_display = [
        "address",
        "comments",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


class TechnicanAdminForm(forms.ModelForm):

    class Meta:
        model = models.Technican
        fields = "__all__"


class TechnicanAdmin(admin.ModelAdmin):
    form = TechnicanAdminForm
    list_display = [
        "Name",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Gauge, GaugeAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Images, ImagesAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Measurement, MeasurementAdmin)
admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Technican, TechnicanAdmin)
