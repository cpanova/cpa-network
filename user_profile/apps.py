from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    name = 'user_profile'

    def ready(self):
        super(UserProfileConfig, self).ready()
        import user_profile.signals  # noqa: F401
