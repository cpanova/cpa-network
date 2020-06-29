from project._celery import _celery
from tracker.models import Click, Conversion, APPROVED_STATUS, REJECTED_STATUS
from offer.models import Payout


@_celery.task
def conversion(data):
    try:
        click = Click.objects.get(pk=data['click_id'])
    except Click.DoesNotExist:
        return f"Click not found. click_id: {data['click_id']}"

    # TODO detect duplicates of conversion.click_id + goal_value

    conversion = Conversion()

    # offer_payout = find_payout(click.offer_id, click.country, data['goal'])
    offer_payout = (
        Payout.objects
        .filter(
            offer_id=click.offer_id,
            goal_value=data['goal'],
            countries__in=[click.country]
        )
        .first()
    )

    if offer_payout:
        revenue = offer_payout.revenue
        payout = offer_payout.payout
        conversion.status = APPROVED_STATUS
    else:
        revenue = 0
        payout = 0
        conversion.status = REJECTED_STATUS

    # conversion.id = click.id
    conversion.click_id = click.id
    conversion.click_date = click.created_at

    conversion.offer_id = click.offer.id
    conversion.affiliate_id = click.affiliate.id
    conversion.sub1 = click.sub1
    conversion.sub2 = click.sub2
    conversion.sub3 = click.sub3
    conversion.sub4 = click.sub4
    conversion.sub5 = click.sub5
    conversion.revenue = revenue
    conversion.payout = payout
    conversion.ip = click.ip
    conversion.ua = click.ua
    conversion.country = click.country

    conversion.goal = data['goal']
    conversion.sum = data['sum']

    conversion.save()

    return f"Processed conversion for click_id: {data['click_id']}"
