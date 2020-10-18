import uuid
from typing import Dict, Any
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest
from tracker.tasks.click import click as click_task
from tracker.tasks.conversion import conversion
from tracker.dao import TrackerCache
from .models import conversion_statuses


# class ClickData(NamedTuple):
#     click_id: str
#     offer_id: int
#     pid: int
#     ip: str
#     ua: str
#     sub1: str
#     sub2: str
#     sub3: str
#     sub4: str
#     sub5: str
#     fb_id: str


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def replace_macro(url: str, context: Dict[str, Any]) -> str:
    url = url.replace('{click_id}', context['click_id'])
    url = url.replace('{clickid}', context['click_id'])
    url = url.replace('{pid}', context['pid'])
    url = url.replace('{fb_id}', context['fb_id'])
    return url


def click(request):
    offer_id = request.GET.get('offer_id')
    pid = request.GET.get('pid')
    if not offer_id or not pid:
        return HttpResponse("Missing parameters", status=400)

    offer_data = TrackerCache.get_offer(offer_id)
    if not offer_data:
        return HttpResponse(status=404)

    click_id = uuid.uuid4().hex

    data = {
        'click_id': click_id,
        'offer_id': offer_id,
        'pid': pid,
        'ip': get_client_ip(request),
        'ua': request.META['HTTP_USER_AGENT'],
        'sub1': request.GET.get('sub1', ""),
        'sub2': request.GET.get('sub2', ""),
        'sub3': request.GET.get('sub3', ""),
        'sub4': request.GET.get('sub4', ""),
        'sub5': request.GET.get('sub5', ""),
    }

    click_task.delay(data)

    context = {
        'click_id': click_id,
        'pid': pid,
        'fb_id': request.GET.get('fb_id', ""),
    }
    url = replace_macro(offer_data['tracking_link'], context)

    return redirect(url)


def postback(request):
    click_id = request.GET.get('click_id')
    goal = request.GET.get('goal', '1')
    status = request.GET.get('status')

    try:
        sum_ = float(request.GET.get('sum', ''))
    except ValueError:
        sum_ = 0.0

    if not click_id:
        resp = HttpResponse("Missing click_id")
        resp.status_code = 400
        return resp

    data = {
        'click_id': click_id,
        'goal': goal,
        'sum': sum_,
    }

    available_status_codes = list(map(lambda t: t[0], conversion_statuses))
    if status in available_status_codes:
        data.update({'status': status})

    conversion.delay(data)

    return HttpResponse("Conversion logged")
