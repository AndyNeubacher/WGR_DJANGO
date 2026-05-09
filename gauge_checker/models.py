from django.db import models
from django.urls import reverse


class Contact(models.Model):

    # Fields
    email = models.EmailField()
    name = models.CharField(max_length=100)
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    telephone = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    address = models.CharField(max_length=255)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("gauge_checker_Contact_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Contact_update", args=(self.pk,))



class Customer(models.Model):

    # Relationships
    Sites = models.ForeignKey("gauge_checker.Site", on_delete=models.CASCADE, related_name="customers_by_site")
    Name = models.ForeignKey("gauge_checker.Contact", on_delete=models.CASCADE, related_name="customers_by_name")
    PropertyManagement = models.ForeignKey("gauge_checker.Contact", on_delete=models.CASCADE, related_name="customers_by_property_management")

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Customer_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Customer_update", args=(self.pk,))



class Gauge(models.Model):

    # Relationships
    Contact = models.ForeignKey("gauge_checker.Contact", on_delete=models.CASCADE, related_name="gauges")
    Measurements = models.ForeignKey("gauge_checker.Measurement", on_delete=models.CASCADE, related_name="gauges", null=True, blank=True)

    # Fields
    date_calibrated = models.DateField()
    type = models.CharField(max_length=100)
    date_installed = models.DateField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    serial = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    last_consumed = models.IntegerField()
    date_expire = models.DateField()
    state = models.CharField(max_length=100)
    comments = models.TextField(blank=True)

    class Meta:
        pass

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
    name = models.CharField(max_length=100)
    comments = models.TextField(blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("gauge_checker_Group_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Group_update", args=(self.pk,))



class Images(models.Model):

    # Relationships
    Location = models.ForeignKey("gauge_checker.Location", on_delete=models.CASCADE, related_name="images")

    # Fields
    image = models.ImageField(upload_to="upload/images/")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Images_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Images_update", args=(self.pk,))



class Location(models.Model):

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    longitude = models.FloatField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    latitude = models.FloatField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Location_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Location_update", args=(self.pk,))



class Measurement(models.Model):

    # Relationships
    Images = models.ForeignKey("gauge_checker.Images", on_delete=models.CASCADE, related_name="measurements")

    # Fields
    date_measured = models.DateField()
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    consumed = models.IntegerField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Measurement_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Measurement_update", args=(self.pk,))



class Site(models.Model):

    # Relationships
    Location = models.ForeignKey("gauge_checker.Location", on_delete=models.CASCADE, related_name="sites")
    Gauges = models.ForeignKey("gauge_checker.Gauge", on_delete=models.CASCADE, related_name="sites")
    Group = models.OneToOneField("auth.Group", on_delete=models.CASCADE, related_name="site")

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    address = models.CharField(max_length=255)
    comments = models.TextField(blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Site_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Site_update", args=(self.pk,))



class Technican(models.Model):

    # Relationships
    Name = models.ForeignKey("gauge_checker.Contact", on_delete=models.CASCADE, related_name="technicans")

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("gauge_checker_Technican_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("gauge_checker_Technican_update", args=(self.pk,))
