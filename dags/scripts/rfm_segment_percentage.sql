DROP TABLE IF EXISTS rfm_segment_percentage;

CREATE TABLE rfm_segment_percentage as 
WITH rfm_filtered AS (
  SELECT *
  FROM rfm
  WHERE monetary > 0
)
SELECT 
  customer_segment,
  COUNT(*) AS segment_count,
  COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rfm_filtered) AS segment_percentage
FROM rfm_filtered
GROUP BY customer_segment
ORDER BY segment_percentage DESC;