from django.conf import settings
from django.db import models


class SiteGroup(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Standortgruppe"
        verbose_name_plural = "Standortgruppen"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True)
    contact_person = models.CharField(max_length=200, blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    member_since = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kunde"
        verbose_name_plural = "Kunden"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Site(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="sites"
    )
    group = models.ForeignKey(
        SiteGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sites",
    )
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    class Meta:
        verbose_name = "Standort"
        verbose_name_plural = "Standorte"
        ordering = ["customer__name", "name"]

    def __str__(self):
        return f"{self.customer.name} - {self.name}"


class Gauge(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="gauges")
    serial_number = models.CharField(max_length=100, unique=True)
    installed_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    additional_data = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Wasserzaehler"
        verbose_name_plural = "Wasserzaehler"
        ordering = ["serial_number"]

    def __str__(self):
        return self.serial_number


class TechnicianProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="technician_profile",
    )
    employee_id = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    assigned_sites = models.ManyToManyField(
        Site, blank=True, related_name="technicians"
    )
    assigned_gauges = models.ManyToManyField(
        Gauge, blank=True, related_name="technicians"
    )

    class Meta:
        verbose_name = "Techniker"
        verbose_name_plural = "Techniker"

    def __str__(self):
        return self.user.get_username()


class ManagerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="manager_profile",
    )
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Manager"

    def __str__(self):
        return self.user.get_username()


class AdminProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_profile",
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Administrator"
        verbose_name_plural = "Administratoren"

    def __str__(self):
        return self.user.get_username()


class Photo(models.Model):
    gauge = models.ForeignKey(Gauge, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="gauges/%Y/%m/")
    taken_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_photos",
    )
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = "Foto"
        verbose_name_plural = "Fotos"
        ordering = ["-taken_at"]

    def __str__(self):
        return f"Foto #{self.pk} - {self.gauge.serial_number}"


class Reading(models.Model):
    gauge = models.ForeignKey(Gauge, on_delete=models.CASCADE, related_name="readings")
    photo = models.OneToOneField(
        Photo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reading",
    )
    serial_number_ocr = models.CharField(max_length=100, blank=True)
    serial_number_verified = models.CharField(max_length=100, blank=True)
    consumed_volume_ocr = models.DecimalField(
        max_digits=12, decimal_places=3, null=True, blank=True
    )
    consumed_volume_verified = models.DecimalField(
        max_digits=12, decimal_places=3, null=True, blank=True
    )
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_readings",
    )
    manager_note = models.TextField(blank=True)

    class Meta:
        verbose_name = "Zaehlerstand"
        verbose_name_plural = "Zaehlerstaende"
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"Stand {self.consumed_volume_verified or self.consumed_volume_ocr} - {self.gauge.serial_number}"
