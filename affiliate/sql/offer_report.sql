SELECT
    report.offer_id,
    o.title,
    COALESCE(report.clicks, 0),
    COALESCE(report.total_qty, 0),
    COALESCE(report.approved_qty, 0),
    COALESCE(report.hold_qty, 0),
    COALESCE(report.rejected_qty, 0),
    COALESCE(report.cr, 0),
    COALESCE(report.total_payout, 0),
    COALESCE(report.approved_payout, 0),
    COALESCE(report.hold_payout, 0),
    COALESCE(report.rejected_payout, 0)
FROM
    (
        SELECT
            COALESCE(cl.offer_id, cv.offer_id) as offer_id,
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
                    sum(payout) FILTER (WHERE status = 'approved') AS approved_payout,
                    sum(payout) FILTER (WHERE status = 'hold')     AS hold_payout,
                    sum(payout) FILTER (WHERE status = 'rejected') AS rejected_payout
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