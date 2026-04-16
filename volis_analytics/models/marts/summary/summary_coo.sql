{{ config(materialized='table') }}

SELECT
    SUM(total_orders) AS total_orders,
    SUM(delivered_orders) AS total_delivered,
    SUM(failed_orders) AS total_failed,
    SUM(in_progress_orders) AS total_in_progress,
    SUM(delivered_orders) * 1.0 / NULLIF(SUM(total_orders), 0) AS delivered_rate,
    SUM(failed_orders) * 1.0 / NULLIF(SUM(total_orders), 0) AS failure_rate,
    AVG(days_to_approval) AS avg_days_to_approval,
    AVG(days_to_post) AS avg_days_to_post,
    AVG(days_to_customer) AS avg_days_to_customer,
    AVG(total_delivery_time) AS avg_total_delivery_time
FROM {{ ref('mart_orders') }}