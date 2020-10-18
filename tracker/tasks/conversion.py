from project._celery import _celery
from tracker.models import (
    Click,
    Conversion,
    HOLD_STATUS,
    REJECTED_STATUS,
)
from offer.models import Payout


@_celery.task
def conversion(data):
    try:
        click = Click.objects.get(pk=data['click_id'])
    except Click.DoesNotExist:
        return f"Click not found. click_id: {data['click_id']}"

    existing_conversion = (
        Conversion.objects
        .filter(click_id=click.id, goal_value=data['goal'])
        .first()
    )
    if existing_conversion and data.get('status'):
        if existing_conversion.status == HOLD_STATUS:
            existing_conversion.status = data.get('status')
            existing_conversion.save()
            return f"Processed conversion for click_id: {data['click_id']}"

    duplicate = bool(existing_conversion)

    conversion = Conversion()

    payout = (
        Payout.objects
        .filter(
            offer_id=click.offer_id,
            goal_value=data['goal'],
            countries__in=[click.country]
        )
        .first()
    )

    if payout:
        conversion.revenue = payout.revenue
        conversion.payout = payout.payout
        conversion.goal = payout.goal
        conversion.currency = payout.currency

        if data.get('status'):
            conversion.status = data.get('status')
        else:
            conversion.status = HOLD_STATUS

        if duplicate:
            conversion.status = REJECTED_STATUS
            conversion.comment = 'Duplicate Click ID'
    else:
        conversion.revenue = 0
        conversion.payout = 0
        conversion.status = REJECTED_STATUS
        conversion.comment = 'Payout not found'

    conversion.click_id = click.id
    conversion.click_date = click.created_at

    conversion.offer_id = click.offer.id
    conversion.affiliate_id = click.affiliate.id
    conversion.affiliate_manager = click.affiliate.profile.manager
    conversion.sub1 = click.sub1
    conversion.sub2 = click.sub2
    conversion.sub3 = click.sub3
    conversion.sub4 = click.sub4
    conversion.sub5 = click.sub5
    conversion.ip = click.ip
    conversion.ua = click.ua
    conversion.country = click.country

    conversion.goal_value = data['goal']
    conversion.sum = data['sum']

    conversion.save()

    return f"Processed conversion for click_id: {data['click_id']}"
