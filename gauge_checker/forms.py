from django import forms
from gauge_checker.models import Site
from gauge_checker.models import Contact
from gauge_checker.models import Contact
from gauge_checker.models import Contact
from gauge_checker.models import Measurement
from gauge_checker.models import Location
from gauge_checker.models import Images
from gauge_checker.models import Location
from gauge_checker.models import Gauge
from django.contrib.auth.models import Group
from gauge_checker.models import Contact
from . import models


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = [
            "email",
            "name",
            "comments",
            "telephone",
            "address",
        ]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = [
            "comments",
            "Sites",
            "Name",
            "PropertyManagement",
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields["Sites"].queryset = Site.objects.all()
        self.fields["Name"].queryset = Contact.objects.all()
        self.fields["PropertyManagement"].queryset = Contact.objects.all()



class GaugeForm(forms.ModelForm):
    class Meta:
        model = models.Gauge
        fields = [
            "serial",
            "type",
            "state",
            "date_calibrated",
            "date_installed",
            "date_expire",
            "last_consumed",
            "comments",
            "Contact",
            "Measurements",
        ]

    def __init__(self, *args, **kwargs):
        super(GaugeForm, self).__init__(*args, **kwargs)
        self.fields["Contact"].queryset = Contact.objects.all()
        self.fields["Measurements"].queryset = Measurement.objects.all()



class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = [
            "name",
            "comments",
        ]


class ImagesForm(forms.ModelForm):
    class Meta:
        model = models.Images
        fields = [
            "image",
            "Location",
        ]

    def __init__(self, *args, **kwargs):
        super(ImagesForm, self).__init__(*args, **kwargs)
        self.fields["Location"].queryset = Location.objects.all()



class LocationForm(forms.ModelForm):
    class Meta:
        model = models.Location
        fields = [
            "longitude",
            "latitude",
        ]


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = models.Measurement
        fields = [
            "date_measured",
            "comments",
            "consumed",
            "Images",
        ]
        widgets = {
            'date_measured': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MeasurementForm, self).__init__(*args, **kwargs)
        self.fields["Images"].queryset = Images.objects.all()



class SiteForm(forms.ModelForm):
    class Meta:
        model = models.Site
        fields = [
            "address",
            "comments",
            "Location",
            "Gauges",
            "Group",
        ]

    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        self.fields["Location"].queryset = Location.objects.all()
        self.fields["Gauges"].queryset = Gauge.objects.all()
        self.fields["Group"].queryset = Group.objects.all()



class TechnicanForm(forms.ModelForm):
    class Meta:
        model = models.Technican
        fields = [
            "Name",
        ]

    def __init__(self, *args, **kwargs):
        super(TechnicanForm, self).__init__(*args, **kwargs)
        self.fields["Name"].queryset = Contact.objects.all()


class MeasurementUploadForm(forms.Form):
    image = forms.ImageField(
        label='Bild des Wasserzählers',
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'capture': 'environment'
        })
    )
    serial_number = forms.CharField(
        label='Seriennummer (OCR-Ergebnis - überprüfen)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Wird durch OCR gefüllt'
        })
    )
    date_measured = forms.DateTimeField(
        label='Messdatum',
        required=True,
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        )
    )
    consumed = forms.DecimalField(
        label='Zählerstand (m³) (OCR-Ergebnis - überprüfen)',
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'step': '0.01',
            'placeholder': 'Wird durch OCR gefüllt'
        })
    )
    comments = forms.CharField(
        label='Kommentare',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        })
    )

