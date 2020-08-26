from django.apps import AppConfig


class TrackerConfig(AppConfig):
    name = 'tracker'

    def ready(self):
        super(TrackerConfig, self).ready()
        import tracker.signals  # noqa: F401
