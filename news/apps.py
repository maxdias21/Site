from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # Chamar os signals
    def ready(self, *args, **kwargs):
        from news import signals
        return super().ready(*args, **kwargs)

