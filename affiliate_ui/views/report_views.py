import iso8601
from datetime import datetime, time, timedelta, date
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render

from offer.models import Offer
from tracker.models import Conversion
from affiliate.dao import daily_report, offer_report, goal_report


@login_required
def daily_report_view(request):
    start_date_arg = request.GET.get('start_date')
    end_date_arg = request.GET.get('end_date')
    offer_id = request.GET.get('offer_id')

    if start_date_arg:
        start_date = iso8601.parse_date(start_date_arg).date()
    else:
        start_date = date.today() - timedelta(days=6)

    if end_date_arg:
        end_date = iso8601.parse_date(end_date_arg).date()
    else:
        end_date = date.today()

    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(end_date, time.max)

    if start_datetime <= end_datetime:
        data = daily_report(
            request.user.id, start_datetime, end_datetime, int(offer_id) if offer_id else 0)
    else:
        data = []

    offers = Offer.objects.filter(
        conversions__affiliate=request.user
    ).distinct()

    context = {
        'data': data,
        'offers': offers,
        'selected_offer_id': int(offer_id) if offer_id else None,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
    }
    return render(request, 'affiliate_ui/daily_report.html', context)


@login_required
def offer_report_view(request):
    start_date_arg = request.GET.get('start_date')
    end_date_arg = request.GET.get('end_date')

    if start_date_arg:
        start_date = iso8601.parse_date(start_date_arg).date()
    else:
        start_date = date.today() - timedelta(days=6)

    if end_date_arg:
        end_date = iso8601.parse_date(end_date_arg).date()
    else:
        end_date = date.today()

    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(end_date, time.max)

    if start_datetime <= end_datetime:
        data = offer_report(request.user.id, start_datetime, end_datetime)
    else:
        data = []

    context = {
        'data': data,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
    }
    return render(request, 'affiliate_ui/offer_report.html', context)


@login_required
def goal_report_view(request):
    start_date_arg = request.GET.get('start_date')
    end_date_arg = request.GET.get('end_date')

    if start_date_arg:
        start_date = iso8601.parse_date(start_date_arg).date()
    else:
        start_date = date.today() - timedelta(days=6)

    if end_date_arg:
        end_date = iso8601.parse_date(end_date_arg).date()
    else:
        end_date = date.today()

    start_datetime = datetime.combine(start_date, time.min)
    end_datetime = datetime.combine(end_date, time.max)

    data = goal_report(request.user.id, start_datetime, end_datetime)

    context = {
        'data': data,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
    }
    return render(request, 'affiliate_ui/goal_report.html', context)
