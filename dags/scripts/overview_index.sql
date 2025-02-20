DROP TABLE IF EXISTS overview_index;

CREATE TABLE overview_index  as
select
	COUNT(DISTINCT CASE WHEN customer_id != 'NaN' THEN customer_id END) as unique_customers,
	COUNT(DISTINCT invoice_no) AS unique_transactions,
	COUNT(DISTINCT CASE WHEN invoice_no NOT LIKE 'C%' THEN invoice_no END) AS success_transactions,
    COUNT(DISTINCT CASE WHEN invoice_no LIKE 'C%' THEN invoice_no END) AS cancel_transactions,
    ROUND(SUM(unit_price * quantity)::numeric, 2) AS revenue,
    ROUND(SUM(unit_price * quantity)/count(DISTINCT CASE WHEN customer_id != 'NaN' THEN customer_id END)) as avg_by_customer,
    ROUND(SUM(unit_price * quantity)/COUNT(DISTINCT CASE WHEN invoice_no NOT LIKE 'C%' THEN invoice_no END)) as avg_by_transaction
FROM invoices;
