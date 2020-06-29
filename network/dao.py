import datetime
from django.db import connection


def _daily_report_sql(
        user_id: int, start_date: datetime, end_date: datetime,
        offer_id: int = None) -> str:

    offer_filter_clause = ""

    if offer_id:
        offer_filter_clause = f"AND offer_id = {offer_id}"

    sql = f"""
    SELECT
        cl.day,
        cl.clicks,
        cv.approved_qty,
        cv.approved_revenue,
        cv.hold_qty,
        cv.hold_revenue,
        cv.rejected_qty,
        cv.rejected_revenue,
        case cl.clicks
            when 0 then 0  -- avoid divizion by zero
            else (100 * cv.total_qty / cl.clicks)
        end AS cr,
        cv.total_qty,
        cv.total_revenue,
        cv.total_payout,
        cv.total_revenue - cv.total_payout as total_profit
    FROM
        (
            SELECT
                created_at::date AS day,
                count(*) AS clicks
            FROM tracker_click
            WHERE
                -- affiliate_id = {user_id}
                TRUE
                AND created_at between '{start_date}' AND '{end_date}'
                {offer_filter_clause}
            GROUP BY day
        ) AS cl
    FULL OUTER JOIN
        (
            SELECT
                created_at::date AS day,
                count(*)         AS total_qty,
                sum(payout)      AS total_payout,
                sum(revenue)     AS total_revenue,
                count(*)     FILTER (WHERE status = 'Approved') AS approved_qty,
                sum(revenue) FILTER (WHERE status = 'Approved') AS approved_revenue,
                count(*)     FILTER (WHERE status = 'Hold') AS hold_qty,
                sum(revenue) FILTER (WHERE status = 'Hold') AS hold_revenue,
                count(*)     FILTER (WHERE status = 'Rejected') AS rejected_qty,
                sum(revenue) FILTER (WHERE status = 'Rejected') AS rejected_revenue
            FROM tracker_conversion
            WHERE
                -- affiliate_id = {user_id}
                TRUE
                AND created_at between '{start_date}' AND '{end_date}'
                {offer_filter_clause}
            GROUP BY day
        ) AS cv
    ON cl.day = cv.day
    ORDER BY cl.day ASC
    ;
    """

    return sql


def daily_report(
        user_id: int, start_date: datetime, end_date: datetime,
        offer_id: int = None) -> list:

    sql = _daily_report_sql(user_id, start_date, end_date, offer_id)

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


# def _ext_daily_report_sql(
#         user_id: int, start_date: datetime, end_date: datetime) -> str:

#     sql = f"""
#     SELECT
#         cl.day,
#         cl.clicks,
#         cv.registrations,
#         cv.deposits,
#         cv.deposits_sum,
#         cv.baselines,
#         case cl.clicks
#             when 0 then 0  -- avoid divizion by zero
#             else (100 * cv.conversions / cl.clicks)
#         end AS cr,
#         cv.payout
#     FROM
#         (
#             SELECT
#                 created_at::date AS day,
#                 count(*) AS clicks
#             FROM tracker_click
#             WHERE
#                 affiliate_id = {user_id}
#                 AND created_at between '{start_date}' AND '{end_date}'
#             GROUP BY day
#         ) AS cl
#     FULL OUTER JOIN
#         (
#             SELECT
#                 created_at::date AS day,
#                 count(*) FILTER (WHERE goal='1') AS registrations,
#                 count(*) FILTER (WHERE goal='2') AS deposits,
#                 sum(tracker_conversion.sum) FILTER (WHERE goal='2') AS deposits_sum,
#                 count(*) FILTER (WHERE goal='3') AS baselines,
#                 count(*) AS conversions,
#                 sum(payout) AS payout
#             FROM tracker_conversion
#             WHERE
#                 affiliate_id = {user_id}
#                 AND created_at between '{start_date}' AND '{end_date}'
#             GROUP BY day
#         ) AS cv
#     ON cl.day = cv.day
#     ORDER BY cl.day ASC
#     ;
#     """

#     return sql


# def ext_daily_report(
#         user_id: int, start_date: datetime, end_date: datetime) -> list:

#     sql = _ext_daily_report_sql(user_id, start_date, end_date)

#     colnames = [
#         'day', 'clicks', 'registrations', 'deposits', 'deposits_sum',
#         'baselines', 'cr', 'payout']

#     with connection.cursor() as cursor:
#         cursor.execute(sql)
#         data = cursor.fetchall()
#         data = [dict(zip(colnames, row)) for row in data]

#     return data


def _offer_report_sql(
        user_id: int, start_date: datetime, end_date: datetime) -> str:

    sql = f"""
    SELECT
        report.offer_id,
        o.title,
        report.clicks,

        report.approved_qty,
        report.approved_revenue,
        report.hold_qty,
        report.hold_revenue,
        report.rejected_qty,
        report.rejected_revenue,

        report.cr,

        report.total_qty,
        report.total_revenue,
        report.total_payout,
        report.total_profit

    FROM
        (
            SELECT
                cl.offer_id,
                cl.clicks,
                cv.approved_qty,
                cv.approved_revenue,
                cv.hold_qty,
                cv.hold_revenue,
                cv.rejected_qty,
                cv.rejected_revenue,
                case cl.clicks
                    when 0 then 0  -- avoid divizion by zero
                    else (100 * cv.total_qty / cl.clicks)
                end AS cr,
                cv.total_qty,
                cv.total_revenue,
                cv.total_payout,
                cv.total_revenue - cv.total_payout as total_profit
            FROM
                (
                    SELECT
                        offer_id,
                        count(*) as clicks
                    FROM tracker_click
                    WHERE
                        -- affiliate_id = {user_id}
                        TRUE
                        AND created_at between '{start_date}' AND '{end_date}'
                    GROUP BY offer_id
                ) AS cl
            FULL OUTER JOIN
                (
                    SELECT
                        offer_id,
                        count(*)         AS total_qty,
                        sum(payout)      AS total_payout,
                        sum(revenue)     AS total_revenue,
                        count(*)     FILTER (WHERE status = 'Approved') AS approved_qty,
                        sum(revenue) FILTER (WHERE status = 'Approved') AS approved_revenue,
                        count(*)     FILTER (WHERE status = 'Hold') AS hold_qty,
                        sum(revenue) FILTER (WHERE status = 'Hold') AS hold_revenue,
                        count(*)     FILTER (WHERE status = 'Rejected') AS rejected_qty,
                        sum(revenue) FILTER (WHERE status = 'Rejected') AS rejected_revenue
                    FROM tracker_conversion
                    WHERE
                        -- affiliate_id = {user_id}
                        TRUE
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
        'offer_name',

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

    sql = _offer_report_sql(user_id, start_date, end_date)

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data


def _affiliate_report_sql(
        user_id: int, start_date: datetime, end_date: datetime) -> str:

    sql = f"""
    SELECT
        report.affiliate_id,
        u.email,
        report.clicks,

        report.approved_qty,
        report.approved_revenue,
        report.hold_qty,
        report.hold_revenue,
        report.rejected_qty,
        report.rejected_revenue,

        report.cr,

        report.total_qty,
        report.total_revenue,
        report.total_payout,
        report.total_profit
    FROM
        (
            SELECT
                cl.affiliate_id,
                cl.clicks,
                cv.approved_qty,
                cv.approved_revenue,
                cv.hold_qty,
                cv.hold_revenue,
                cv.rejected_qty,
                cv.rejected_revenue,
                case cl.clicks
                    when 0 then 0  -- avoid divizion by zero
                    else (100 * cv.total_qty / cl.clicks)
                end AS cr,
                cv.total_qty,
                cv.total_revenue,
                cv.total_payout,
                cv.total_revenue - cv.total_payout as total_profit
            FROM
                (
                    SELECT
                        affiliate_id,
                        count(*) as clicks
                    FROM tracker_click
                    WHERE
                        affiliate_manager_id = {user_id}
                        AND created_at between '{start_date}' AND '{end_date}'
                    GROUP BY affiliate_id
                ) AS cl
            FULL OUTER JOIN
                (
                    SELECT
                        affiliate_id,
                        count(*)         AS total_qty,
                        sum(payout)      AS total_payout,
                        sum(revenue)     AS total_revenue,
                        count(*)     FILTER (WHERE status = 'Approved') AS approved_qty,
                        sum(revenue) FILTER (WHERE status = 'Approved') AS approved_revenue,
                        count(*)     FILTER (WHERE status = 'Hold') AS hold_qty,
                        sum(revenue) FILTER (WHERE status = 'Hold') AS hold_revenue,
                        count(*)     FILTER (WHERE status = 'Rejected') AS rejected_qty,
                        sum(revenue) FILTER (WHERE status = 'Rejected') AS rejected_revenue
                    FROM tracker_conversion
                    WHERE
                        affiliate_manager_id = {user_id}
                        AND created_at between '{start_date}' AND '{end_date}'
                    GROUP BY affiliate_id
                ) AS cv
            ON cl.affiliate_id = cv.affiliate_id
        ) AS report
    LEFT JOIN auth_user AS u
    ON report.affiliate_id = u.id
    ;
    """

    return sql


def affiliate_report(
        user_id: int, start_date: datetime, end_date: datetime) -> list:

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

    sql = _affiliate_report_sql(user_id, start_date, end_date)

    with connection.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [dict(zip(colnames, row)) for row in data]

    return data
