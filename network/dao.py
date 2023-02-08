import os
from typing import List, Dict
from datetime import datetime
from django.db import connection


def daily_report(
        user_id: int, start_date: datetime, end_date: datetime,
        offer_id: int = 0) -> List[Dict]:

    if offer_id:
        offer_filter_clause = f"AND offer_id = {offer_id}"
    else:
        offer_filter_clause = ''

    filepath = os.path.join(
        os.path.dirname(__file__), 'sql', 'daily_report.sql'
    )
    with open(filepath, 'r') as f:
        sql = f.read().format(**locals())

    colnames = [
        'day',

        'clicks',

        'approved_qty',
        'approved_revenue',
        'hold_qty',
        'hold_revenue',
        'rejected_qty',
        'rejected_revenue',

        'cr',

        'total_qty',
        'total_revenue',
        'total_payout',
        'total_profit',
    ]

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data


def offer_report(
        user_id: int, start_date: datetime, end_date: datetime) -> List[Dict]:

    colnames = [
        'offer_id',
        'offer_title',

        'clicks',

        'approved_qty',
        'approved_revenue',
        'hold_qty',
        'hold_revenue',
        'rejected_qty',
        'rejected_revenue',

        'cr',

        'total_qty',
        'total_revenue',
        'total_payout',
        'total_profit',
    ]

    filepath = os.path.join(
        os.path.dirname(__file__), 'sql', 'offer_report.sql'
    )
    with open(filepath, 'r') as f:
        sql = f.read().format(**locals())

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data


def affiliate_report(
        user_id: int, start_date: datetime, end_date: datetime) -> List[Dict]:

    colnames = [
        'affiliate_id',
        'affiliate_name',

        'clicks',

        'approved_qty',
        'approved_revenue',
        'hold_qty',
        'hold_revenue',
        'rejected_qty',
        'rejected_revenue',

        'cr',

        'total_qty',
        'total_revenue',
        'total_payout',
        'total_profit',
    ]

    filepath = os.path.join(
        os.path.dirname(__file__), 'sql', 'affiliate_report.sql'
    )
    with open(filepath, 'r') as f:
        sql = f.read().format(**locals())

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data
