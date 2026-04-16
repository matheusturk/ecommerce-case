{{ config(
    materialized='table'
) }}

SELECT 
    seller_id,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT order_item_id) AS total_order_items,
    SUM(price) AS total_revenue,
    SUM(price) / NULLIF(COUNT(DISTINCT order_id), 0) AS avg_order_value,
    AVG(price) AS avg_item_price,
    AVG(freight_value) AS avg_freight_value
FROM {{ ref('int_order_items') }}
GROUP BY seller_id
ORDER BY total_revenue DESC