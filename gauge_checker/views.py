from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from . import models
from . import forms


class TechnicanLoginView(LoginView):
    template_name = 'technician/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('technician_dashboard')


class TechnicanDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'technician/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sites'] = models.Site.objects.all()
        context['groups'] = models.Site.objects.values_list('Group', flat=True).distinct()
        return context


class TechnicanSitesListView(LoginRequiredMixin, generic.ListView):
    model = models.Site
    template_name = 'technician/sites_list.html'
    context_object_name = 'sites'
    paginate_by = 20

    def get_queryset(self):
        from django.contrib.auth.models import Group
        queryset = models.Site.objects.all()
        group_id = self.request.GET.get('group')
        if group_id:
            queryset = queryset.filter(Group_id=group_id)
        return queryset

    def get_context_data(self, **kwargs):
        from django.contrib.auth.models import Group
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.filter(sites__isnull=False).distinct()
        context['selected_group'] = self.request.GET.get('group', '')
        return context


class TechnicanSiteDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Site
    template_name = 'technician/site_detail.html'
    context_object_name = 'site'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = self.get_object()
        context['gauges'] = models.Gauge.objects.filter(pk=site.Gauges_id) if site.Gauges else []
        return context


class TechnicanGaugesView(LoginRequiredMixin, generic.DetailView):
    model = models.Gauge
    template_name = 'technician/gauges_detail.html'
    context_object_name = 'gauge'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gauge = self.get_object()
        context['measurements'] = models.Measurement.objects.filter(Images__isnull=False).order_by('-date_measured')
        return context


class TechnicanOCRView(LoginRequiredMixin, generic.View):
    def post(self, request):
        import tempfile
        import os
        import json
        from django.http import JsonResponse
        from .ocr_service import run_ocr

        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)

        image_file = request.FILES['image']

        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            for chunk in image_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            ocr_result = run_ocr(tmp_path)
            return JsonResponse(ocr_result)
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass


class TechnicanMeasurementAddView(LoginRequiredMixin, generic.FormView):
    form_class = forms.MeasurementUploadForm
    template_name = 'technician/add_measurement.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gauge_pk = self.kwargs.get('gauge_pk')
        context['gauge'] = models.Gauge.objects.get(pk=gauge_pk)
        return context

    def form_valid(self, form):
        import tempfile
        import os
        from .ocr_service import run_ocr

        gauge_pk = self.kwargs.get('gauge_pk')
        gauge = models.Gauge.objects.get(pk=gauge_pk)
        consumed = form.cleaned_data.get('consumed')

        if not consumed or consumed == 0:
            image_file = form.cleaned_data['image']

            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                for chunk in image_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            try:
                ocr_result = run_ocr(tmp_path)

                initial_data = {
                    'date_measured': form.cleaned_data.get('date_measured'),
                    'image': form.cleaned_data.get('image'),
                    'comments': form.cleaned_data.get('comments'),
                }

                if ocr_result.get('consumed_volume'):
                    try:
                        initial_data['consumed'] = float(ocr_result['consumed_volume'])
                    except (ValueError, TypeError):
                        pass

                if ocr_result.get('serial_number'):
                    initial_data['serial_number'] = ocr_result['serial_number']

                self.request.session['ocr_results'] = ocr_result
                self.request.session.modified = True

                new_form = forms.MeasurementUploadForm(initial=initial_data)

                context = self.get_context_data()
                context['form'] = new_form
                context['ocr_results'] = ocr_result
                context['show_ocr_review'] = True

                return self.render_to_response(context)
            finally:
                try:
                    os.unlink(tmp_path)
                except:
                    pass

        site = models.Site.objects.filter(Gauges_id=gauge_pk).first()
        location = site.Location if site else None

        image_obj = models.Images.objects.create(
            image=form.cleaned_data['image'],
            Location=location
        )

        measurement = models.Measurement.objects.create(
            Images=image_obj,
            date_measured=form.cleaned_data['date_measured'],
            consumed=form.cleaned_data['consumed'],
            comments=form.cleaned_data['comments']
        )

        gauge.last_consumed = form.cleaned_data['consumed']
        gauge.save()

        self.request.session.pop('ocr_results', None)

        return super().form_valid(form)

    def get_success_url(self):
        gauge_pk = self.kwargs.get('gauge_pk')
        return reverse_lazy('technician_gauge_detail', kwargs={'pk': gauge_pk})


class ContactListView(LoginRequiredMixin, generic.ListView):
    model = models.Contact
    form_class = forms.ContactForm


class ContactCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Contact
    form_class = forms.ContactForm


class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Contact
    form_class = forms.ContactForm


class ContactUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Contact
    form_class = forms.ContactForm
    pk_url_kwarg = "pk"


class ContactDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Contact
    success_url = reverse_lazy("gauge_checker_Contact_list")


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = models.Customer
    form_class = forms.CustomerForm


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Customer
    form_class = forms.CustomerForm


class CustomerDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Customer
    form_class = forms.CustomerForm


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Customer
    form_class = forms.CustomerForm
    pk_url_kwarg = "pk"


class CustomerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Customer
    success_url = reverse_lazy("gauge_checker_Customer_list")


class GaugeListView(LoginRequiredMixin, generic.ListView):
    model = models.Gauge
    form_class = forms.GaugeForm


class GaugeCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Gauge
    form_class = forms.GaugeForm


class GaugeDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Gauge
    form_class = forms.GaugeForm


class GaugeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Gauge
    form_class = forms.GaugeForm
    pk_url_kwarg = "pk"


class GaugeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Gauge
    success_url = reverse_lazy("gauge_checker_Gauge_list")


class GroupListView(LoginRequiredMixin, generic.ListView):
    model = models.Group
    form_class = forms.GroupForm


class GroupCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Group
    form_class = forms.GroupForm


class GroupDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Group
    form_class = forms.GroupForm


class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Group
    form_class = forms.GroupForm
    pk_url_kwarg = "pk"


class GroupDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Group
    success_url = reverse_lazy("gauge_checker_Group_list")


class ImagesListView(LoginRequiredMixin, generic.ListView):
    model = models.Images
    form_class = forms.ImagesForm


class ImagesCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Images
    form_class = forms.ImagesForm


class ImagesDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Images
    form_class = forms.ImagesForm


class ImagesUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Images
    form_class = forms.ImagesForm
    pk_url_kwarg = "pk"


class ImagesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Images
    success_url = reverse_lazy("gauge_checker_Images_list")


class LocationListView(LoginRequiredMixin, generic.ListView):
    model = models.Location
    form_class = forms.LocationForm


class LocationCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Location
    form_class = forms.LocationForm


class LocationDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Location
    form_class = forms.LocationForm


class LocationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Location
    form_class = forms.LocationForm
    pk_url_kwarg = "pk"


class LocationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Location
    success_url = reverse_lazy("gauge_checker_Location_list")


class MeasurementListView(LoginRequiredMixin, generic.ListView):
    model = models.Measurement
    form_class = forms.MeasurementForm


class MeasurementCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Measurement
    form_class = forms.MeasurementForm


class MeasurementDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Measurement
    form_class = forms.MeasurementForm


class MeasurementUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Measurement
    form_class = forms.MeasurementForm
    pk_url_kwarg = "pk"


class MeasurementDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Measurement
    success_url = reverse_lazy("gauge_checker_Measurement_list")


class SiteListView(LoginRequiredMixin, generic.ListView):
    model = models.Site
    form_class = forms.SiteForm


class SiteCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Site
    form_class = forms.SiteForm


class SiteDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Site
    form_class = forms.SiteForm


class SiteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Site
    form_class = forms.SiteForm
    pk_url_kwarg = "pk"


class SiteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Site
    success_url = reverse_lazy("gauge_checker_Site_list")


class TechnicanListView(LoginRequiredMixin, generic.ListView):
    model = models.Technican
    form_class = forms.TechnicanForm


class TechnicanCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Technican
    form_class = forms.TechnicanForm


class TechnicanDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Technican
    form_class = forms.TechnicanForm


class TechnicanUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Technican
    form_class = forms.TechnicanForm
    pk_url_kwarg = "pk"


class TechnicanDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Technican
    success_url = reverse_lazy("gauge_checker_Technican_list")
