{{ config(
    materialized='table'
) }}

SELECT
    r.review_id,
    r.order_id,
    DATE(r.review_creation_date) AS review_date,
    DATE(o.order_purchase_timestamp) AS purchase_date,
    o.order_status,
    r.review_score,
    CASE 
        WHEN LOWER(o.order_status) = 'delivered' THEN 1 ELSE 0 
    END AS is_delivered,
    CASE
        WHEN LOWER(o.order_status) = 'delivered'
        AND o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1
        ELSE 0
    END AS is_late_delivery,
    CASE 
        WHEN LOWER(o.order_status) = 'delivered'
        THEN DATE_DIFF('day', o.order_purchase_timestamp, o.order_delivered_customer_date)
    END AS delivery_time_days
FROM {{ ref('int_reviews') }} r LEFT JOIN {{ ref('int_orders') }} o ON r.order_id = o.order_id
WHERE r.review_score IS NOT NULL