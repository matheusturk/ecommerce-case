SELECT 
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    SUM(i.price) AS order_value,
    SUM(i.freight_value) AS freight_value,
    SUM(i.price + i.freight_value) AS order_total_value,
    COUNT(i.order_item_id) AS item_count
FROM {{ ref('olist_orders_dataset') }} o
LEFT JOIN {{ ref('olist_order_items_dataset') }} i
ON o.order_id = i.order_id
GROUP BY 
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date