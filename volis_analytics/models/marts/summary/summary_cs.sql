{{ config(materialized='table') }}

WITH overall AS (
    SELECT
        AVG(avg_review_score) AS avg_score,
        SUM(total_reviews) AS total_reviews
    FROM {{ ref('mart_reviews_summary') }}
),

by_delivery AS (
    SELECT
        delivery_status,
        AVG(avg_review_score) AS avg_score
    FROM {{ ref('mart_reviews_vs_delivery') }}
    GROUP BY delivery_status
)

SELECT
    o.avg_score AS avg_review_score,
    o.total_reviews AS total_reviews,
    MAX(CASE WHEN b.delivery_status = 'on_time' THEN b.avg_score END) AS avg_score_on_time,
    MAX(CASE WHEN b.delivery_status = 'late' THEN b.avg_score END) AS avg_score_late
FROM overall o
CROSS JOIN by_delivery b
GROUP BY o.avg_score, o.total_reviews