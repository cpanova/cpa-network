from geolite2 import geolite2
from project._celery import _celery
from tracker.models import Click


def detect_country(ip: str) -> str:
    reader = geolite2.reader()
    ip_info = reader.get(ip) or {}
    country = ip_info.get("country", {}).get("iso_code", "")
    return country


@_celery.task
def click(data):
    country = detect_country(data["ip"])

    click = Click()
    click.id = data['click_id']
    click.offer_id = data['offer_id']
    click.affiliate_id = data['pid']
    click.sub1 = data['sub1']
    click.sub2 = data['sub2']
    click.sub3 = data['sub3']
    click.sub4 = data['sub4']
    click.sub5 = data['sub5']
    # TODO revenue, payout
    click.revenue = 0
    click.payout = 0
    click.ip = data['ip']
    click.country = country
    click.ua = data['ua']
    click.save()

    return f"Click created: {click.id}"
