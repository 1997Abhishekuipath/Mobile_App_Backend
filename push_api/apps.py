from django.apps import AppConfig


class PushApiConfig(AppConfig):
    print('push-api-in')
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'push_api'

    def ready(self):
            print('push-api-in')
            from scheduler import scheduler
            scheduler.start()
            print("web connection app ready")