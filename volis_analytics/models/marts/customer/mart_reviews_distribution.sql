{{ config(
    materialized='table'
) }}

SELECT 
    purchase_date,
    review_score,
    COUNT(review_id) AS review_count,
    COUNT(review_id) * 1.0 / SUM(COUNT(review_id)) OVER (PARTITION BY purchase_date) AS review_score_share
FROM {{ ref('mart_reviews') }}
GROUP BY purchase_date, review_score
ORDER BY purchase_date, review_score