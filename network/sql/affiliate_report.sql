SELECT
    report.affiliate_id,
    u.email,
    COALESCE(report.clicks, 0),

    COALESCE(report.approved_qty, 0),
    COALESCE(report.approved_revenue, 0),
    COALESCE(report.hold_qty, 0),
    COALESCE(report.hold_revenue, 0),
    COALESCE(report.rejected_qty, 0),
    COALESCE(report.rejected_revenue, 0),

    COALESCE(report.cr, 0),

    COALESCE(report.total_qty, 0),
    COALESCE(report.total_revenue, 0),
    COALESCE(report.total_payout, 0),
    COALESCE(report.total_profit, 0)
FROM
    (
        SELECT
            COALESCE(cl.affiliate_id, cv.affiliate_id) as affiliate_id,
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
            (cv.total_revenue - cv.total_payout) as total_profit
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
                    count(*)     FILTER (WHERE status = 'approved') AS approved_qty,
                    sum(revenue) FILTER (WHERE status = 'approved') AS approved_revenue,
                    count(*)     FILTER (WHERE status = 'hold') AS hold_qty,
                    sum(revenue) FILTER (WHERE status = 'hold') AS hold_revenue,
                    count(*)     FILTER (WHERE status = 'rejected') AS rejected_qty,
                    sum(revenue) FILTER (WHERE status = 'rejected') AS rejected_revenue
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