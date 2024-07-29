from django.apps import AppConfig


class IdentitymanagementservConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'identitymanagementserv'

    def ready(self):
        import identitymanagementserv.signals
