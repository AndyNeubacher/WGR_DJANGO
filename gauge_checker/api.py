from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

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


class TechnicanLoginView(APIView):
    """API endpoint for technician login - returns authentication token"""
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})


class TechnicanMeView(APIView):
    """API endpoint to get current authenticated technician's profile"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.technican_profile
        except models.Technican.DoesNotExist:
            return Response({'error': 'No technician profile for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.TechnicanMeSerializer(profile)
        return Response(serializer.data)
