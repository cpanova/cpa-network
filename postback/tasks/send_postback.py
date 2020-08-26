import requests
from project._celery import _celery
from ..models import Postback, Log


def find_postbacks(affiliate_id, offer_id=None):
    return Postback.objects.filter(affiliate_id=affiliate_id, offer_id=offer_id)


@_celery.task
def send_postback(conversion):
    assert(bool(conversion['offer_id']))
    assert(bool(conversion['affiliate_id']))

    offer_id = conversion['offer_id']
    affiliate_id = conversion['affiliate_id']

    postbacks = find_postbacks(offer_id=offer_id, affiliate_id=affiliate_id)
    if not postbacks:
        postbacks = find_postbacks(affiliate_id=affiliate_id)

    for postback in postbacks:
        if postback.goal:
            if conversion['goal_value'] != postback.goal:
                continue

        url = replace_macro(postback.url, conversion)

        try:
            resp = requests.get(url)

            persist_log(url, resp.status_code, resp.text)
        except requests.exceptions.Timeout:
            persist_log(url, None, 'Timeout')
        except Exception as e:
            persist_log(url, None, str(e))


def persist_log(url, status, text):
    log = Log()
    log.url = url
    log.response_status = status
    log.response_text = text
    log.save()


def replace_macro(url: str, data: dict) -> str:
    # macros:

    # - sub1..5
    # - offer_id
    # - sum
    # - currency
    # - goal_value
    url = url.replace('{sub1}', data.get('sub1', ''))
    url = url.replace('{sub2}', data.get('sub2', ''))
    url = url.replace('{sub3}', data.get('sub3', ''))
    url = url.replace('{sub4}', data.get('sub4', ''))
    url = url.replace('{sub5}', data.get('sub5', ''))
    url = url.replace('{offer}', str(data.get('offer_id', '')))
    url = url.replace('{sum}', str(data.get('payout', '')))
    url = url.replace('{currency}', data.get('currency', ''))
    url = url.replace('{goal}', data.get('goal_value', ''))

    return url
