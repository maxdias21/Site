from django.apps import AppConfig


class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    # Chamar os signals
    def ready(self, *args, **kwargs):
        from blog import signals
        return super().ready(*args, **kwargs)
