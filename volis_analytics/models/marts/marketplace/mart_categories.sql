{{ config(
    materialized='table'
) }}

SELECT
    COALESCE(product_category_name, 'unknown') AS product_category,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(order_item_id) AS total_order_items,
    SUM(price) AS total_revenue
FROM {{ ref('int_order_items') }}
GROUP BY product_category_name
ORDER BY total_revenue DESC