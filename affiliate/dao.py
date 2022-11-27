import os
from datetime import datetime
from typing import List, Dict, Any
from django.db import connection


def daily_report(
        user_id: int, start_date: datetime, end_date: datetime,
        offer_id: int = 0) -> list:

    offer_filter_clause = ""

    if offer_id:
        offer_filter_clause = f"AND offer_id = {offer_id}"

    filepath = os.path.join(
        os.path.dirname(__file__), 'sql', 'daily_report.sql'
    )
    with open(filepath, 'r') as f:
        sql = f.read().format(**locals())

    colnames = [
        'date',

        'clicks',

        'total_qty',
        'approved_qty',
        'hold_qty',
        'rejected_qty',

        'cr',

        'total_payout',
        'approved_payout',
        'hold_payout',
        'rejected_payout'
    ]

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data


def offer_report(
        user_id: int, start_date: datetime,
        end_date: datetime) -> List[Dict[str, Any]]:

    colnames = [
        'offer_id',
        'offer_title',

        'clicks',

        'total_qty',
        'approved_qty',
        'hold_qty',
        'rejected_qty',

        'cr',

        'total_payout',
        'approved_payout',
        'hold_payout',
        'rejected_payout'
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


def goal_report(
        user_id: int, start_date: datetime, end_date: datetime) -> list:

    colnames = [
        'goal_id',
        'goal_name',

        'total_qty',
        'approved_qty',
        'hold_qty',
        'rejected_qty',

        'total_payout',
        'approved_payout',
        'hold_payout',
        'rejected_payout'
    ]

    filepath = os.path.join(
        os.path.dirname(__file__), 'sql', 'goal_report.sql'
    )
    with open(filepath, 'r') as f:
        sql = f.read().format(**locals())

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data


def report_bysub(
        sub_index: int, offer_id: int, user_id: int,
        start_date: datetime, end_date: datetime) -> list:

    colnames = [
        'sub',

        'clicks',

        'total_qty',
        'approved_qty',
        'hold_qty',
        'rejected_qty',

        'cr',

        'total_payout',
        'approved_payout',
        'hold_payout',
        'rejected_payout'
    ]

    offer_filter_clause = f" AND offer_id = {offer_id} "

    filepath = os.path.join(
        os.path.dirname(__file__), 'sql', 'sub_report.sql'
    )
    with open(filepath, 'r') as f:
        sql = f.read().format(**locals())

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data
