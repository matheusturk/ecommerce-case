{{ config(
    materialized='table'
) }}

SELECT 
    DATE(order_approved_at),
    COUNT(order_id) AS total_orders,
    COALESCE(SUM(order_value), 0) AS gross_revenue,
    AVG(order_value) AS average_order_value,
    SUM(CASE 
        WHEN LOWER(order_status) IN ('unavailable', 'canceled') THEN order_value 
        ELSE 0
    END) AS refunded_revenue
FROM {{ ref('int_orders') }}
WHERE order_approved_at IS NOT NULL
GROUP BY 1
ORDER BY 1