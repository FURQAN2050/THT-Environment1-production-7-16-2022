from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
 
    def ready(self):
        # import signal handlers
        import accounts.signals