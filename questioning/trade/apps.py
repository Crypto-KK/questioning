from django.apps import AppConfig


class TradeConfig(AppConfig):
    name = 'questioning.trade'
    verbose_name = '交易明细'

    def ready(self):
        import questioning.trade.signals
