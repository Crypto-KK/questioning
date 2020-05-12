from django.apps import AppConfig


class QaConfig(AppConfig):
    name = 'questioning.qa'
    verbose_name = '问答'

    def ready(self):
        import questioning.qa.signals
