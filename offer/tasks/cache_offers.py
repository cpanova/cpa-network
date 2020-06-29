import json
import redis
from project._celery import _celery
from project.redis_conn import pool
from ..models import Offer


@_celery.task
def cache_offers():
    redis_conn = redis.Redis(connection_pool=pool)
    for offer in Offer.objects.all():
        record = {
            'tracking_link': offer.tracking_link
        }
        redis_conn.set(f'offers:{offer.id}', json.dumps(record))
