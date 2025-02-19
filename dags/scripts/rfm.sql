DROP TABLE IF EXISTS rfm;

CREATE TABLE rfm AS
WITH sub_data as(
SELECT
    customer_id,
    SUM(unit_price * quantity) AS monetary
  FROM invoices
  where customer_id!='NaN'
  GROUP BY customer_id
),
rfm_data AS (
  SELECT
    customer_id,
    EXTRACT(days FROM('2011-12-11'::DATE - MAX(invoice_date))) AS recency,
    COUNT(DISTINCT invoice_no) AS frequency
  FROM invoices
  where customer_id!='NaN' and invoice_no NOT LIKE 'C%'
  GROUP BY customer_id 
),
rfm_scores AS (
  SELECT 
    a.*,
    b.monetary,
    -- 計算 RFM 個別分數
    CASE WHEN NTILE(5) OVER (ORDER BY a.recency) = 1 THEN 5
        WHEN NTILE(5) OVER (ORDER BY a.recency) = 2 THEN 4
        WHEN NTILE(5) OVER (ORDER BY a.recency) = 3 THEN 3
        WHEN NTILE(5) OVER (ORDER BY a.recency) = 4 THEN 2
        WHEN NTILE(5) OVER (ORDER BY a.recency) = 5 THEN 1
 		END AS recency_score,
    CASE WHEN NTILE(5) OVER (ORDER BY a.frequency) = 1 THEN 1
        WHEN NTILE(5) OVER (ORDER BY a.frequency) = 2 THEN 2
        WHEN NTILE(5) OVER (ORDER BY a.frequency) = 3 THEN 3
        WHEN NTILE(5) OVER (ORDER BY a.frequency) = 4 THEN 4
        WHEN NTILE(5) OVER (ORDER BY a.frequency) = 5 THEN 5
        END AS frequency_score,
    CASE WHEN NTILE(5) OVER (ORDER BY b.monetary) = 1 THEN 1
        WHEN NTILE(5) OVER (ORDER BY b.monetary) = 2 THEN 2
        WHEN NTILE(5) OVER (ORDER BY b.monetary) = 3 THEN 3
        WHEN NTILE(5) OVER (ORDER BY b.monetary) = 4 THEN 4
        WHEN NTILE(5) OVER (ORDER BY b.monetary) = 5 THEN 5
        END AS monetary_score
  FROM rfm_data a, sub_data b
  where a.customer_id=b.customer_id and b.monetary>0
)
SELECT *,
  CONCAT(recency_score, frequency_score) AS rfm_score,
  -- 分類客戶
  CASE 
    WHEN CONCAT(recency_score, frequency_score) ~ '^[1-2][1-2]$' THEN 'hibernating'
    WHEN CONCAT(recency_score, frequency_score) ~ '^[1-2][3-4]$' THEN 'at_Risk'
    WHEN CONCAT(recency_score, frequency_score) ~ '^[1-2]5$' THEN 'cant_loose'
    WHEN CONCAT(recency_score, frequency_score) ~ '^3[1-2]$' THEN 'about_to_sleep'
    WHEN CONCAT(recency_score, frequency_score) = '33' THEN 'need_attention'
    WHEN CONCAT(recency_score, frequency_score) ~ '^[3-4][4-5]$' THEN 'loyal_customers'
    WHEN CONCAT(recency_score, frequency_score) = '41' THEN 'promising'
    WHEN CONCAT(recency_score, frequency_score) = '51' THEN 'new_customers'
    WHEN CONCAT(recency_score, frequency_score) ~ '^[4-5][2-3]$' THEN 'potential_loyalists'
    WHEN CONCAT(recency_score, frequency_score) ~ '^5[4-5]$' THEN 'champions'
    ELSE 'Other'
  END AS customer_segment
FROM rfm_scores;


CREATE TABLE rfm_segment_percentage as 
WITH rfm_filtered AS (
  SELECT *
  FROM rfm
)
SELECT 
  customer_segment,
  COUNT(*) AS segment_count,
  COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rfm_filtered) AS segment_percentage
FROM rfm_filtered
GROUP BY customer_segment
ORDER BY segment_percentage DESC;
