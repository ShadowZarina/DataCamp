'''
Find out how much Wholesale net revenue each product_line generated per month per warehouse in the dataset.

The query should be saved as revenue_by_product_line using the SQL cell provided, and contain the following:
product_line,
month: displayed as 'June', 'July', and 'August',
warehouse, and
net_revenue: the sum of total minus the sum of payment_fee.
The results should be sorted by product_line and month, followed by net_revenue in descending order.
'''

SELECT product_line,
    CASE WHEN EXTRACT('month' from date) = 6 THEN 'June'
        WHEN EXTRACT('month' from date) = 7 THEN 'July'
        WHEN EXTRACT('month' from date) = 8 THEN 'August'
    END as month,
    warehouse,
	SUM(total) - SUM(payment_fee) AS net_revenue
FROM sales
WHERE client_type = 'Wholesale'
GROUP BY product_line, warehouse, month
ORDER BY product_line, month, net_revenue DESC
