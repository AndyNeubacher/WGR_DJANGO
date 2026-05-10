"""
WGR URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from gauge_checker.views import TechnicanLoginView


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('technician/', TechnicanLoginView.as_view(), name='technician_login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('gauge_checker/', include('gauge_checker.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
