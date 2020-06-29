import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from django.conf import settings  # noqa


_celery = Celery(
    'leon-pp',
    broker=settings.REDIS_URL
)

_celery.config_from_object('django.conf:settings', namespace='CELERY')

_celery.autodiscover_tasks()

# task_routes = {
#     'campaigns.tasks.stats.push_sent': {'queue': 'stats:pushes'},
#     'tracker.tasks.stats.*': {'queue': 'stats'},
# }

_celery.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    timezone='Europe/Moscow',
    # task_routes=task_routes,
)

_celery.conf.beat_schedule = {
    'cache-offers': {
        'task': 'offer.tasks.cache_offers.cache_offers',
        'schedule': 60
    },
}
