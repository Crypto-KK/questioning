from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'questioning.home'

    def ready(self):
        import questioning.home.signals
