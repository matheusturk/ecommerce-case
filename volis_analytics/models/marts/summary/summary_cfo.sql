{{ config(materialized='table') }}

SELECT
    SUM(gross_revenue) AS total_revenue,
    SUM(total_orders) AS total_orders,
    SUM(gross_revenue) / NULLIF(SUM(total_orders), 0) AS avg_ticket,
    SUM(refunded_revenue) AS total_refunded,
    SUM(refunded_revenue) / NULLIF(SUM(gross_revenue), 0) AS refund_rate
FROM {{ ref('mart_financials') }}
