SELECT
    i.order_id,
    i.order_item_id,
    i.product_id,
    p.product_category_name,
    i.seller_id,
    i.shipping_limit_date,
    i.price,
    i.freight_value
FROM {{ ref('olist_order_items_dataset') }} i LEFT JOIN {{ ref('olist_products_dataset') }} p ON i.product_id = p.product_id