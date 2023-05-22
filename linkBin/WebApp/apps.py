from django.apps import AppConfig


class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WebApp'

class UsersConfig(AppConfig):
    name = 'Users'
    def ready(self):
        import signals
