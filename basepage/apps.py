from django.apps import AppConfig


class BasepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'basepage'
    verbose_name = 'Panel zasobów'  # Ta nazwa pojawi się w menu bocznym
