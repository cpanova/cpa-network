SELECT
    report.goal_id,
    goal.name,
    COALESCE(report.total_qty, 0),
    COALESCE(report.approved_qty, 0),
    COALESCE(report.hold_qty, 0),
    COALESCE(report.rejected_qty, 0),
    COALESCE(report.total_payout, 0),
    COALESCE(report.approved_payout, 0),
    COALESCE(report.hold_payout, 0),
    COALESCE(report.rejected_payout, 0)
FROM (
    SELECT
        goal_id,
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
    GROUP BY goal_id
    ) AS report
LEFT JOIN offer_goal AS goal
ON report.goal_id = goal.id
;