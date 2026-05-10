from django.apps import AppConfig


class GaugeCheckerConfig(AppConfig):
    name = 'gauge_checker'
    verbose_name = 'Gauge Checker'

    def ready(self):
        from .ocr_service.ocr_utils import preload_models
        preload_models()
