{{ config(
    materialized='table'
) }}

SELECT 
    purchase_date,
    COUNT(review_id) AS total_reviews,
    AVG(review_score) AS avg_review_score
FROM {{ ref('mart_reviews') }}
GROUP BY purchase_date
ORDER BY purchase_date