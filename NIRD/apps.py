from django.apps import AppConfig



class NirdConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "NIRD"

    def ready(self):
        import NIRD.signals 