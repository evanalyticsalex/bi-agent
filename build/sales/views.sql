

CREATE OR REPLACE VIEW kpi_revenue_day AS
SELECT
    DATE_TRUNC('day', order_date) AS day,
    SUM(orders.amount) AS value
FROM orders
WHERE channel IN ('web','app')
GROUP BY 1;

CREATE OR REPLACE VIEW kpi_orders_day AS
SELECT
    DATE_TRUNC('day', order_date) AS day,
    COUNT(*) AS value
FROM orders

GROUP BY 1;

CREATE OR REPLACE VIEW kpi_aov_day AS
SELECT
    DATE_TRUNC('day', order_date) AS day,
    SUM(orders.amount) / NULLIF(COUNT(*),0) AS value
FROM orders

GROUP BY 1;
