import json
import redis
from offer.models import Payout
from project.redis_conn import pool


def any(predicate, collection):
    return bool(len(list(filter(predicate, collection))))


def first(collection):
    try:
        return collection[0]
    except IndexError:
        return None


def find_payout(offer_id: int, country: str, goal: str) -> Payout:
    return (
        Payout.objects
        .filter(
            offer_id=offer_id,
            goal_value=goal,
            countries__in=[country]
        )
        .first()
    )
    # payouts = Payout.objects.filter(offer_id=offer_id, goal_value=goal)
    # return (
    #     first(
    #         list(
    #             filter(
    #                 lambda p:
    #                     any(
    #                         lambda c:
    #                             c.code == country, p.countries),
    #                 payouts))))


class TrackerCache(object):

    @staticmethod
    def get_offer(id: int) -> dict:
        redis_conn = redis.Redis(connection_pool=pool)
        resp = redis_conn.get(f"offers:{id}")
        if resp:
            return json.loads(resp)
        return None

    # @staticmethod
    # def get_user(id: int) -> dict:
    #     redis_conn = redis.Redis(connection_pool=pool)
    #     resp = redis_conn.get(f"users:{id}")
    #     if resp:
    #         return json.loads(resp)
    #     return None
