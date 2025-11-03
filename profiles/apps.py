from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        # Import signal handlers to ensure profile creation on user signup
        from . import signals  # noqa: F401
