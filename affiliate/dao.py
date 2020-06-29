import datetime
from django.db import connection


def _daily_report_sql(
        user_id: int, start_date: datetime, end_date: datetime,
        offer_id: int = None) -> str:

    offer_filter_clause = ""

    if offer_id:
        offer_filter_clause = f"AND offer_id = {offer_id}"

    sql = f"""
        (SELECT
            cl.day,
            cl.clicks,
            cv.total_qty,
            cv.approved_qty,
            cv.hold_qty,
            cv.rejected_qty,
            case cl.clicks
                when 0 then 0  -- avoid divizion by zero
                else (100 * cv.total_qty / cl.clicks)
            end AS cr,
            cv.total_payout,
            cv.approved_payout,
            cv.hold_payout,
            cv.rejected_payout
        FROM
            (
                SELECT
                    created_at::date AS day,
                    count(*) AS clicks
                FROM tracker_click
                WHERE
                    affiliate_id = {user_id}
                    AND created_at between '{start_date}' AND '{end_date}'
                    {offer_filter_clause}
                GROUP BY day
            ) AS cl
        FULL OUTER JOIN
            (
                SELECT
                    created_at::date AS day,
                    count(*)                                       AS total_qty,
                    count(*)    FILTER (WHERE status = 'approved') AS approved_qty,
                    count(*)    FILTER (WHERE status = 'hold')     AS hold_qty,
                    count(*)    FILTER (WHERE status = 'rejected') AS rejected_qty,
                    sum(payout)                                    AS total_payout,
                    sum(CASE WHEN status = 'approved' THEN payout ELSE 0 END) AS approved_payout,
                    sum(CASE WHEN status = 'hold'     THEN payout ELSE 0 END) AS hold_payout,
                    sum(CASE WHEN status = 'rejected' THEN payout ELSE 0 END) AS rejected_payout
                FROM tracker_conversion
                WHERE
                    affiliate_id = {user_id}
                    AND created_at between '{start_date}' AND '{end_date}'
                    {offer_filter_clause}
                GROUP BY day
            ) AS cv
        ON cl.day = cv.day
        ORDER BY cl.day ASC)
    ;
    """

    return sql


def daily_report(
        user_id: int, start_date: datetime, end_date: datetime,
        offer_id: int = None) -> list:

    sql = _daily_report_sql(user_id, start_date, end_date, offer_id)

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


def _offer_report_sql(
        user_id: int, start_date: datetime, end_date: datetime) -> str:

    sql = f"""
    SELECT
        report.offer_id,
        o.title,
        report.clicks,
        report.total_qty,
        report.approved_qty,
        report.hold_qty,
        report.rejected_qty,
        report.cr,
        report.total_payout,
        report.approved_payout,
        report.hold_payout,
        report.rejected_payout
    FROM
        (
            SELECT
                cl.offer_id,
                cl.clicks,
                cv.total_qty,
                cv.approved_qty,
                cv.hold_qty,
                cv.rejected_qty,
                case cl.clicks
                    when 0 then 0  -- avoid divizion by zero
                    else (100 * cv.total_qty / cl.clicks)
                end AS cr,
                cv.total_payout,
                cv.approved_payout,
                cv.hold_payout,
                cv.rejected_payout
            FROM
                (
                    SELECT
                        offer_id,
                        count(*) as clicks
                    FROM tracker_click
                    WHERE
                        affiliate_id = {user_id}
                        AND created_at between '{start_date}' AND '{end_date}'
                    GROUP BY offer_id
                ) AS cl
            FULL OUTER JOIN
                (
                    SELECT
                        offer_id,
                        count(*)                                       AS total_qty,
                        count(*)    FILTER (WHERE status = 'approved') AS approved_qty,
                        count(*)    FILTER (WHERE status = 'hold')     AS hold_qty,
                        count(*)    FILTER (WHERE status = 'rejected') AS rejected_qty,
                        sum(payout)                                    AS total_payout,
                        sum(CASE WHEN status = 'approved' THEN payout ELSE 0 END) AS approved_payout,
                        sum(CASE WHEN status = 'hold'     THEN payout ELSE 0 END) AS hold_payout,
                        sum(CASE WHEN status = 'rejected' THEN payout ELSE 0 END) AS rejected_payout
                    FROM tracker_conversion
                    WHERE
                        affiliate_id = {user_id}
                        AND created_at between '{start_date}' AND '{end_date}'
                    GROUP BY offer_id
                ) AS cv
            ON cl.offer_id = cv.offer_id
        ) AS report
    LEFT JOIN offer_offer AS o
    ON report.offer_id = o.id
    ;
    """

    return sql


def offer_report(
        user_id: int, start_date: datetime, end_date: datetime) -> list:

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

    sql = _offer_report_sql(user_id, start_date, end_date)

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data
