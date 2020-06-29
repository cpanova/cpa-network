import redis
from django.conf import settings

# redis_conn = Redis.from_url(settings.REDIS_URL)
pool = redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=8)
