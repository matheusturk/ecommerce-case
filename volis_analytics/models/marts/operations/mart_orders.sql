{{ config(
    materialized='table'
) }}

SELECT 
    DATE(order_purchase_timestamp) AS purchase_date,
    COUNT(order_id) AS total_orders,
    AVG(
        CASE WHEN order_approved_at IS NOT NULL THEN DATE_DIFF('day', order_purchase_timestamp, order_approved_at) END) AS days_to_approval,
    AVG(
        CASE WHEN order_approved_at IS NOT NULL 
        AND order_delivered_carrier_date IS NOT NULL 
        THEN DATE_DIFF('day', order_approved_at, order_delivered_carrier_date) END) AS days_to_post,
    AVG(
        CASE WHEN LOWER(order_status) = 'delivered' 
        AND order_delivered_customer_date IS NOT NULL
        THEN DATE_DIFF('day', order_delivered_carrier_date, order_delivered_customer_date) END) AS days_to_customer,
    AVG(
        CASE WHEN LOWER(order_status) = 'delivered' 
        AND order_delivered_customer_date IS NOT NULL
        THEN DATE_DIFF('day', order_purchase_timestamp, order_delivered_customer_date) END) AS total_delivery_time,
    
    SUM(CASE WHEN LOWER(order_status) = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN LOWER(order_status) IN ('canceled', 'unavailable') THEN 1 ELSE 0 END) AS failed_orders,
    SUM(CASE 
        WHEN LOWER(order_status) NOT IN ('delivered', 'canceled', 'unavailable') 
        THEN 1 ELSE 0 
    END) AS in_progress_orders,

    SUM(CASE WHEN LOWER(order_status) = 'delivered' THEN 1 ELSE 0 END) * 1.0 / COUNT(order_id) AS delivered_rate,
    SUM(CASE WHEN LOWER(order_status) IN ('canceled', 'unavailable') THEN 1 ELSE 0 END) * 1.0 / COUNT(order_id) AS failure_rate,
    SUM(CASE 
        WHEN LOWER(order_status) NOT IN ('delivered', 'canceled', 'unavailable') 
        THEN 1 ELSE 0 
    END) * 1.0 / COUNT(order_id) AS in_progress_rate
FROM {{ ref('int_orders') }}  
GROUP BY 1
ORDER BY purchase_date