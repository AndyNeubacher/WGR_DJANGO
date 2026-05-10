from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("Contact", api.ContactViewSet)
router.register("Customer", api.CustomerViewSet)
router.register("Gauge", api.GaugeViewSet)
router.register("Group", api.GroupViewSet)
router.register("Images", api.ImagesViewSet)
router.register("Location", api.LocationViewSet)
router.register("Measurement", api.MeasurementViewSet)
router.register("Site", api.SiteViewSet)
router.register("Technican", api.TechnicanViewSet)

urlpatterns = (
    path("technician/login/", views.TechnicanLoginView.as_view(), name="technician_login"),
    path("technician/dashboard/", views.TechnicanDashboardView.as_view(), name="technician_dashboard"),
    path("technician/sites/", views.TechnicanSitesListView.as_view(), name="technician_sites_list"),
    path("technician/site/<int:pk>/", views.TechnicanSiteDetailView.as_view(), name="technician_site_detail"),
    path("technician/gauge/<int:pk>/", views.TechnicanGaugesView.as_view(), name="technician_gauge_detail"),
    path("technician/gauge/<int:gauge_pk>/add-measurement/", views.TechnicanMeasurementAddView.as_view(), name="technician_add_measurement"),
    path("technician/ocr/", views.TechnicanOCRView.as_view(), name="technician_ocr"),
    path("api/v1/", include(router.urls)),
    path("gauge_checker/Contact/", views.ContactListView.as_view(), name="gauge_checker_Contact_list"),
    path("gauge_checker/Contact/create/", views.ContactCreateView.as_view(), name="gauge_checker_Contact_create"),
    path("gauge_checker/Contact/detail/<int:pk>/", views.ContactDetailView.as_view(), name="gauge_checker_Contact_detail"),
    path("gauge_checker/Contact/update/<int:pk>/", views.ContactUpdateView.as_view(), name="gauge_checker_Contact_update"),
    path("gauge_checker/Contact/delete/<int:pk>/", views.ContactDeleteView.as_view(), name="gauge_checker_Contact_delete"),
    path("gauge_checker/Customer/", views.CustomerListView.as_view(), name="gauge_checker_Customer_list"),
    path("gauge_checker/Customer/create/", views.CustomerCreateView.as_view(), name="gauge_checker_Customer_create"),
    path("gauge_checker/Customer/detail/<int:pk>/", views.CustomerDetailView.as_view(), name="gauge_checker_Customer_detail"),
    path("gauge_checker/Customer/update/<int:pk>/", views.CustomerUpdateView.as_view(), name="gauge_checker_Customer_update"),
    path("gauge_checker/Customer/delete/<int:pk>/", views.CustomerDeleteView.as_view(), name="gauge_checker_Customer_delete"),
    path("gauge_checker/Gauge/", views.GaugeListView.as_view(), name="gauge_checker_Gauge_list"),
    path("gauge_checker/Gauge/create/", views.GaugeCreateView.as_view(), name="gauge_checker_Gauge_create"),
    path("gauge_checker/Gauge/detail/<int:pk>/", views.GaugeDetailView.as_view(), name="gauge_checker_Gauge_detail"),
    path("gauge_checker/Gauge/update/<int:pk>/", views.GaugeUpdateView.as_view(), name="gauge_checker_Gauge_update"),
    path("gauge_checker/Gauge/delete/<int:pk>/", views.GaugeDeleteView.as_view(), name="gauge_checker_Gauge_delete"),
    path("gauge_checker/Group/", views.GroupListView.as_view(), name="gauge_checker_Group_list"),
    path("gauge_checker/Group/create/", views.GroupCreateView.as_view(), name="gauge_checker_Group_create"),
    path("gauge_checker/Group/detail/<int:pk>/", views.GroupDetailView.as_view(), name="gauge_checker_Group_detail"),
    path("gauge_checker/Group/update/<int:pk>/", views.GroupUpdateView.as_view(), name="gauge_checker_Group_update"),
    path("gauge_checker/Group/delete/<int:pk>/", views.GroupDeleteView.as_view(), name="gauge_checker_Group_delete"),
    path("gauge_checker/Images/", views.ImagesListView.as_view(), name="gauge_checker_Images_list"),
    path("gauge_checker/Images/create/", views.ImagesCreateView.as_view(), name="gauge_checker_Images_create"),
    path("gauge_checker/Images/detail/<int:pk>/", views.ImagesDetailView.as_view(), name="gauge_checker_Images_detail"),
    path("gauge_checker/Images/update/<int:pk>/", views.ImagesUpdateView.as_view(), name="gauge_checker_Images_update"),
    path("gauge_checker/Images/delete/<int:pk>/", views.ImagesDeleteView.as_view(), name="gauge_checker_Images_delete"),
    path("gauge_checker/Location/", views.LocationListView.as_view(), name="gauge_checker_Location_list"),
    path("gauge_checker/Location/create/", views.LocationCreateView.as_view(), name="gauge_checker_Location_create"),
    path("gauge_checker/Location/detail/<int:pk>/", views.LocationDetailView.as_view(), name="gauge_checker_Location_detail"),
    path("gauge_checker/Location/update/<int:pk>/", views.LocationUpdateView.as_view(), name="gauge_checker_Location_update"),
    path("gauge_checker/Location/delete/<int:pk>/", views.LocationDeleteView.as_view(), name="gauge_checker_Location_delete"),
    path("gauge_checker/Measurement/", views.MeasurementListView.as_view(), name="gauge_checker_Measurement_list"),
    path("gauge_checker/Measurement/create/", views.MeasurementCreateView.as_view(), name="gauge_checker_Measurement_create"),
    path("gauge_checker/Measurement/detail/<int:pk>/", views.MeasurementDetailView.as_view(), name="gauge_checker_Measurement_detail"),
    path("gauge_checker/Measurement/update/<int:pk>/", views.MeasurementUpdateView.as_view(), name="gauge_checker_Measurement_update"),
    path("gauge_checker/Measurement/delete/<int:pk>/", views.MeasurementDeleteView.as_view(), name="gauge_checker_Measurement_delete"),
    path("gauge_checker/Site/", views.SiteListView.as_view(), name="gauge_checker_Site_list"),
    path("gauge_checker/Site/create/", views.SiteCreateView.as_view(), name="gauge_checker_Site_create"),
    path("gauge_checker/Site/detail/<int:pk>/", views.SiteDetailView.as_view(), name="gauge_checker_Site_detail"),
    path("gauge_checker/Site/update/<int:pk>/", views.SiteUpdateView.as_view(), name="gauge_checker_Site_update"),
    path("gauge_checker/Site/delete/<int:pk>/", views.SiteDeleteView.as_view(), name="gauge_checker_Site_delete"),
    path("gauge_checker/Technican/", views.TechnicanListView.as_view(), name="gauge_checker_Technican_list"),
    path("gauge_checker/Technican/create/", views.TechnicanCreateView.as_view(), name="gauge_checker_Technican_create"),
    path("gauge_checker/Technican/detail/<int:pk>/", views.TechnicanDetailView.as_view(), name="gauge_checker_Technican_detail"),
    path("gauge_checker/Technican/update/<int:pk>/", views.TechnicanUpdateView.as_view(), name="gauge_checker_Technican_update"),
    path("gauge_checker/Technican/delete/<int:pk>/", views.TechnicanDeleteView.as_view(), name="gauge_checker_Technican_delete"),
    path("api/v1/auth/login/", api.TechnicanLoginView.as_view(), name="api_technican_login"),
    path("api/v1/auth/me/", api.TechnicanMeView.as_view(), name="api_technican_me"),

)
