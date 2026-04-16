{{ config(
    materialized='table'
) }}

SELECT 
    DATE(o.order_approved_at) AS order_date,
    p.payment_type,
    COUNT(DISTINCT p.order_id) AS total_orders,
    SUM(p.payment_value) AS total_payment_value,
    AVG(p.payment_value) AS avg_payment_value
FROM {{ ref('int_payments') }} p LEFT JOIN {{ ref('int_orders') }} o ON p.order_id = o.order_id
WHERE o.order_approved_at IS NOT NULL
GROUP BY 1, 2
ORDER BY 1, 2