from django.contrib.auth import get_user_model
from project._celery import _celery
from tracker.models import Click
from ext.ipapi import API, Err as IpstackErr


# def detect_country(ip: str) -> str:
#     reader = geolite2.reader()
#     ip_info = reader.get(ip) or {}
#     country = ip_info.get("country", {}).get("iso_code", "")
#     return country


def detect_country_service(ip: str) -> str:
    api = API()
    try:
        resp = api.query(ip)
    except IpstackErr:
        return ''
    return resp.country_code


@_celery.task
def click(data):
    country = detect_country_service(data["ip"])

    try:
        user = get_user_model().objects.get(pk=data['pid'])
    except get_user_model().DoesNotExist:
        msg = f"affiliate {data['pid']} not found"
        print(msg)
        return msg

    click = Click()
    click.id = data['click_id']
    click.offer_id = data['offer_id']
    click.affiliate_id = data['pid']
    click.affiliate_manager = user.profile.manager
    click.sub1 = data['sub1']
    click.sub2 = data['sub2']
    click.sub3 = data['sub3']
    click.sub4 = data['sub4']
    click.sub5 = data['sub5']
    click.revenue = 0
    click.payout = 0
    click.ip = data['ip']
    click.country = country
    click.ua = data['ua']
    click.save()

    return f"Click created: {click.id}"
