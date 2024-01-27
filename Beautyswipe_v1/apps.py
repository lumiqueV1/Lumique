# Beautyswipe/Beautyswipe_v1/apps.py

from django.apps import AppConfig

class BeautyswipeV1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Beautyswipe_v1'

    def ready(self):
        import Beautyswipe_v1.signals  # This line is needed to connect signals when the app is ready
