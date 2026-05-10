from django.db import models
from django.urls import reverse
from django.conf import settings


class Contact(models.Model):

    # Fields
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    telephone = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontakte"

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("gauge_checker_Contact_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Contact_update", args=(self.pk,))



class Customer(models.Model):

    # Relationships
    Sites = models.ForeignKey("gauge_checker.Site", on_delete=models.CASCADE, related_name="customers_by_site", null=True, blank=True)
    Name = models.ForeignKey("gauge_checker.Contact", on_delete=models.CASCADE, related_name="customers_by_name", null=True, blank=True)
    PropertyManagement = models.ForeignKey("gauge_checker.Contact", on_delete=models.CASCADE, related_name="customers_by_property_management", null=True, blank=True)

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Mitglied"
        verbose_name_plural = "Mitglieder"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Customer_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Customer_update", args=(self.pk,))



class Gauge(models.Model):

    # Relationships
    Contact = models.ForeignKey("gauge_checker.Contact", on_delete=models.CASCADE, related_name="gauges", null=True, blank=True)
    Measurements = models.ForeignKey("gauge_checker.Measurement", on_delete=models.CASCADE, related_name="gauges", null=True, blank=True)

    # Fields
    date_calibrated = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    date_installed = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    serial = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    last_consumed = models.IntegerField(null=True, blank=True)
    date_expire = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Wasserzähler"
        verbose_name_plural = "Wasserzähler"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Gauge_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Gauge_update", args=(self.pk,))



class Group(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Gebiet"
        verbose_name_plural = "Gebiete"

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("gauge_checker_Group_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Group_update", args=(self.pk,))



class Images(models.Model):

    # Relationships
    Location = models.ForeignKey("gauge_checker.Location", on_delete=models.CASCADE, related_name="images", null=True, blank=True)

    # Fields
    image = models.ImageField(upload_to="upload/images/", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Bild"
        verbose_name_plural = "Bilder"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Images_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Images_update", args=(self.pk,))



class Location(models.Model):

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    longitude = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    latitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Standort"
        verbose_name_plural = "Standorte"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Location_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Location_update", args=(self.pk,))



class Measurement(models.Model):

    # Relationships
    Images = models.ForeignKey("gauge_checker.Images", on_delete=models.CASCADE, related_name="measurements", null=True, blank=True)

    # Fields
    date_measured = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    comments = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    consumed = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Messung"
        verbose_name_plural = "Messungen"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Measurement_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Measurement_update", args=(self.pk,))



class Site(models.Model):

    # Relationships
    Location = models.ForeignKey("gauge_checker.Location", on_delete=models.CASCADE, related_name="sites", null=True, blank=True)
    Gauges = models.ForeignKey("gauge_checker.Gauge", on_delete=models.CASCADE, related_name="sites", null=True, blank=True)
    Group = models.ForeignKey("auth.Group", on_delete=models.CASCADE, related_name="sites", null=True, blank=True)

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Installation"
        verbose_name_plural = "Installationen"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Site_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Site_update", args=(self.pk,))



class Technican(models.Model):

    # Relationships
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='technican_profile',
        null=True,
        blank=True
    )
    Name = models.ForeignKey("gauge_checker.Contact", on_delete=models.CASCADE, related_name="technicans", null=True, blank=True)

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Techniker"
        verbose_name_plural = "Techniker"

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Technican_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Technican_update", args=(self.pk,))
