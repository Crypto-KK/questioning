from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'questioning.articles'
    verbose_name = '文章'

    def ready(self):
        from questioning.trade import signals
