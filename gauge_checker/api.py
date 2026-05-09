from rest_framework import viewsets, permissions

from . import serializers
from . import models


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet for the Contact class"""

    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for the Customer class"""

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class GaugeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Gauge class"""

    queryset = models.Gauge.objects.all()
    serializer_class = serializers.GaugeSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the Group class"""

    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ImagesViewSet(viewsets.ModelViewSet):
    """ViewSet for the Images class"""

    queryset = models.Images.objects.all()
    serializer_class = serializers.ImagesSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Location class"""

    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasurementViewSet(viewsets.ModelViewSet):
    """ViewSet for the Measurement class"""

    queryset = models.Measurement.objects.all()
    serializer_class = serializers.MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]


class SiteViewSet(viewsets.ModelViewSet):
    """ViewSet for the Site class"""

    queryset = models.Site.objects.all()
    serializer_class = serializers.SiteSerializer
    permission_classes = [permissions.IsAuthenticated]


class TechnicanViewSet(viewsets.ModelViewSet):
    """ViewSet for the Technican class"""

    queryset = models.Technican.objects.all()
    serializer_class = serializers.TechnicanSerializer
    permission_classes = [permissions.IsAuthenticated]
