from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "questioning.users"
    verbose_name = '用户'

    def ready(self):
        try:
            import questioning.users.signals  # noqa F401
        except ImportError:
            pass
