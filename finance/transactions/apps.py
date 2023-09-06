from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance.transactions'

    def ready(self):
        import finance.transactions.signals
