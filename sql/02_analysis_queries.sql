-- Q1: Which customer states have the highest delay rate? (ranking for outreach priority)
SELECT
    customer_state,
    COUNT(*) AS total_orders,
    SUM(is_delayed) AS delayed_orders,
    ROUND(SUM(is_delayed) * 100.0 / COUNT(*), 2) AS delay_rate_pct
FROM orders_master
GROUP BY customer_state
ORDER BY delay_rate_pct DESC
LIMIT 10;


-- Q2: Is delay a growing or shrinking problem over time? (excludes Sep-Oct 2018 data cutoff months)
SELECT
    purchase_month,
    COUNT(*) AS total_orders,
    ROUND(SUM(is_delayed) * 100.0 / COUNT(*), 2) AS delay_rate_pct
FROM orders_master
WHERE purchase_month NOT IN ('2018-09', '2018-10')
GROUP BY purchase_month
ORDER BY purchase_month;


-- Q3: Which sellers have the highest delay rate AND enough volume to matter (min 20 orders)?
SELECT
    seller_id,
    seller_state,
    COUNT(*) AS total_orders,
    ROUND(SUM(is_delayed) * 100.0 / COUNT(*), 2) AS delay_rate_pct
FROM orders_master
GROUP BY seller_id, seller_state
HAVING COUNT(*) >= 20
ORDER BY delay_rate_pct DESC
LIMIT 10;


-- Q4: How does average review score drop as delay severity increases?
SELECT
    delay_bucket,
    COUNT(*) AS total_orders,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM orders_master
WHERE review_score IS NOT NULL
GROUP BY delay_bucket
ORDER BY
    CASE delay_bucket
        WHEN 'on_time' THEN 1
        WHEN '1-3_days_late' THEN 2
        WHEN '4-7_days_late' THEN 3
        WHEN '8plus_days_late' THEN 4
    END;


-- Q5: Which state-pairs (seller_state -> customer_state) have the worst delay rate? (cross-state shipping risk)
SELECT
    seller_state,
    customer_state,
    COUNT(*) AS total_orders,
    ROUND(SUM(is_delayed) * 100.0 / COUNT(*), 2) AS delay_rate_pct
FROM orders_master
GROUP BY seller_state, customer_state
HAVING COUNT(*) >= 30
ORDER BY delay_rate_pct DESC
LIMIT 10;


-- Q6: What is the total financial exposure (penalty_cost) by customer state? (where to prioritize carrier renegotiation)
SELECT
    customer_state,
    SUM(is_delayed) AS delayed_orders,
    ROUND(SUM(penalty_cost), 2) AS total_penalty_exposure
FROM orders_master
GROUP BY customer_state
ORDER BY total_penalty_exposure DESC
LIMIT 10;


-- Q7: Prioritized outreach list — top 20 delayed orders by penalty_cost (highest-value at-risk customers)
SELECT
    order_id,
    customer_state,
    order_value_total,
    delay_days,
    review_score,
    penalty_cost
FROM orders_master
WHERE is_delayed = 1
ORDER BY penalty_cost DESC
LIMIT 20;
