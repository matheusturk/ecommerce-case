{{ config(materialized='table') }}

WITH sellers AS (
    SELECT
        COUNT(DISTINCT seller_id) AS total_sellers,
        SUM(total_revenue) AS total_revenue,
        AVG(avg_order_value) AS avg_ticket,
        AVG(avg_freight_value) AS avg_freight
    FROM {{ ref('mart_sellers') }}
),

top_category AS (
    SELECT product_category
    FROM {{ ref('mart_categories') }}
    ORDER BY total_revenue DESC
    LIMIT 1
)

SELECT
    s.total_sellers,
    s.total_revenue,
    s.avg_ticket,
    s.avg_freight,
    t.product_category AS top_category
FROM sellers s
CROSS JOIN top_category t