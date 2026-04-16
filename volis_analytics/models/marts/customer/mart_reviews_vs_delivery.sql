{{ config(
    materialized='table'
) }}

SELECT 
    purchase_date,
    CASE 
        WHEN is_late_delivery = 1 THEN 'late'
        ELSE 'on_time'
    END AS delivery_status,
    COUNT(review_id) AS total_reviews,
    AVG(review_score) AS avg_review_score
FROM {{ ref('mart_reviews') }}
WHERE is_delivered = 1
GROUP BY 1, 2
ORDER BY 1, 2