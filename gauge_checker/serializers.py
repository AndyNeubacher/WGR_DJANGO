from rest_framework import serializers

from . import models


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Contact
        fields = [
            "email",
            "name",
            "comments",
            "created",
            "telephone",
            "last_updated",
            "address",
        ]

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = [
            "last_updated",
            "comments",
            "created",
            "Sites",
            "Name",
            "PropertyManagement",
        ]

class GaugeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Gauge
        fields = [
            "date_calibrated",
            "type",
            "date_installed",
            "created",
            "serial",
            "last_updated",
            "last_consumed",
            "date_expire",
            "state",
            "comments",
            "Contact",
            "Measurements",
        ]

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Group
        fields = [
            "created",
            "last_updated",
            "name",
            "comments",
        ]

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Images
        fields = [
            "image",
            "created",
            "last_updated",
            "Location",
        ]

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = [
            "last_updated",
            "longitude",
            "created",
            "latitude",
        ]

class MeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Measurement
        fields = [
            "date_measured",
            "last_updated",
            "comments",
            "created",
            "consumed",
            "Images",
        ]

class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Site
        fields = [
            "created",
            "last_updated",
            "address",
            "comments",
            "Location",
            "Gauges",
            "Group",
        ]

class TechnicanSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Technican
        fields = [
            "created",
            "last_updated",
            "Name",
        ]
