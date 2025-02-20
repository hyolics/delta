DROP TABLE IF EXISTS overview_by_months;

CREATE TABLE overview_by_months AS
SELECT 
    CAST(DATE_TRUNC('MONTH', invoice_date) AS DATE) AS mon,
    COUNT(DISTINCT CASE WHEN customer_id != 'NaN' THEN customer_id END) AS unique_customers,
    COUNT(DISTINCT invoice_no) AS unique_transactions,
    ROUND(SUM(unit_price * quantity)::numeric, 2) AS revenue
FROM invoices
WHERE invoice_date > '2010-12-31'
GROUP BY DATE_TRUNC('MONTH', invoice_date);





