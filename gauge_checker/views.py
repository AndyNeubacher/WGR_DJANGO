from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class ContactListView(generic.ListView):
    model = models.Contact
    form_class = forms.ContactForm


class ContactCreateView(generic.CreateView):
    model = models.Contact
    form_class = forms.ContactForm


class ContactDetailView(generic.DetailView):
    model = models.Contact
    form_class = forms.ContactForm


class ContactUpdateView(generic.UpdateView):
    model = models.Contact
    form_class = forms.ContactForm
    pk_url_kwarg = "pk"


class ContactDeleteView(generic.DeleteView):
    model = models.Contact
    success_url = reverse_lazy("gauge_checker_Contact_list")


class CustomerListView(generic.ListView):
    model = models.Customer
    form_class = forms.CustomerForm


class CustomerCreateView(generic.CreateView):
    model = models.Customer
    form_class = forms.CustomerForm


class CustomerDetailView(generic.DetailView):
    model = models.Customer
    form_class = forms.CustomerForm


class CustomerUpdateView(generic.UpdateView):
    model = models.Customer
    form_class = forms.CustomerForm
    pk_url_kwarg = "pk"


class CustomerDeleteView(generic.DeleteView):
    model = models.Customer
    success_url = reverse_lazy("gauge_checker_Customer_list")


class GaugeListView(generic.ListView):
    model = models.Gauge
    form_class = forms.GaugeForm


class GaugeCreateView(generic.CreateView):
    model = models.Gauge
    form_class = forms.GaugeForm


class GaugeDetailView(generic.DetailView):
    model = models.Gauge
    form_class = forms.GaugeForm


class GaugeUpdateView(generic.UpdateView):
    model = models.Gauge
    form_class = forms.GaugeForm
    pk_url_kwarg = "pk"


class GaugeDeleteView(generic.DeleteView):
    model = models.Gauge
    success_url = reverse_lazy("gauge_checker_Gauge_list")


class GroupListView(generic.ListView):
    model = models.Group
    form_class = forms.GroupForm


class GroupCreateView(generic.CreateView):
    model = models.Group
    form_class = forms.GroupForm


class GroupDetailView(generic.DetailView):
    model = models.Group
    form_class = forms.GroupForm


class GroupUpdateView(generic.UpdateView):
    model = models.Group
    form_class = forms.GroupForm
    pk_url_kwarg = "pk"


class GroupDeleteView(generic.DeleteView):
    model = models.Group
    success_url = reverse_lazy("gauge_checker_Group_list")


class ImagesListView(generic.ListView):
    model = models.Images
    form_class = forms.ImagesForm


class ImagesCreateView(generic.CreateView):
    model = models.Images
    form_class = forms.ImagesForm


class ImagesDetailView(generic.DetailView):
    model = models.Images
    form_class = forms.ImagesForm


class ImagesUpdateView(generic.UpdateView):
    model = models.Images
    form_class = forms.ImagesForm
    pk_url_kwarg = "pk"


class ImagesDeleteView(generic.DeleteView):
    model = models.Images
    success_url = reverse_lazy("gauge_checker_Images_list")


class LocationListView(generic.ListView):
    model = models.Location
    form_class = forms.LocationForm


class LocationCreateView(generic.CreateView):
    model = models.Location
    form_class = forms.LocationForm


class LocationDetailView(generic.DetailView):
    model = models.Location
    form_class = forms.LocationForm


class LocationUpdateView(generic.UpdateView):
    model = models.Location
    form_class = forms.LocationForm
    pk_url_kwarg = "pk"


class LocationDeleteView(generic.DeleteView):
    model = models.Location
    success_url = reverse_lazy("gauge_checker_Location_list")


class MeasurementListView(generic.ListView):
    model = models.Measurement
    form_class = forms.MeasurementForm


class MeasurementCreateView(generic.CreateView):
    model = models.Measurement
    form_class = forms.MeasurementForm


class MeasurementDetailView(generic.DetailView):
    model = models.Measurement
    form_class = forms.MeasurementForm


class MeasurementUpdateView(generic.UpdateView):
    model = models.Measurement
    form_class = forms.MeasurementForm
    pk_url_kwarg = "pk"


class MeasurementDeleteView(generic.DeleteView):
    model = models.Measurement
    success_url = reverse_lazy("gauge_checker_Measurement_list")


class SiteListView(generic.ListView):
    model = models.Site
    form_class = forms.SiteForm


class SiteCreateView(generic.CreateView):
    model = models.Site
    form_class = forms.SiteForm


class SiteDetailView(generic.DetailView):
    model = models.Site
    form_class = forms.SiteForm


class SiteUpdateView(generic.UpdateView):
    model = models.Site
    form_class = forms.SiteForm
    pk_url_kwarg = "pk"


class SiteDeleteView(generic.DeleteView):
    model = models.Site
    success_url = reverse_lazy("gauge_checker_Site_list")


class TechnicanListView(generic.ListView):
    model = models.Technican
    form_class = forms.TechnicanForm


class TechnicanCreateView(generic.CreateView):
    model = models.Technican
    form_class = forms.TechnicanForm


class TechnicanDetailView(generic.DetailView):
    model = models.Technican
    form_class = forms.TechnicanForm


class TechnicanUpdateView(generic.UpdateView):
    model = models.Technican
    form_class = forms.TechnicanForm
    pk_url_kwarg = "pk"


class TechnicanDeleteView(generic.DeleteView):
    model = models.Technican
    success_url = reverse_lazy("gauge_checker_Technican_list")
