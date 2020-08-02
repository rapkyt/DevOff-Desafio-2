from django.apps import AppConfig


class Config(AppConfig):
    name = "app.devoff"
    label = "app_devoff"
    verbose_name = "Dev Off"

    def ready(self):
        pass
