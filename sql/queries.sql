-- CUSTOMER INTELLIGENCE SUPPORT COPILOT
-- PART A: SQL ANALYSIS QUERIES

-- 1. Display all customers
SELECT *
FROM customers;

-- 2. Display all products
SELECT *
FROM products;

-- 3. Display all completed orders
SELECT *
FROM orders
WHERE status = 'completed';

-- 4. Total orders for each customer
SELECT
    customer_id,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC;

-- 5. Total spending by each customer
SELECT
    customer_id,
    ROUND(SUM(order_amount), 2) AS total_spending
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
ORDER BY total_spending DESC;

-- 6. Average product price by category
SELECT
    category,
    ROUND(AVG(price_inr), 2) AS average_price
FROM products
GROUP BY category;

-- 7. Order status summary
SELECT
    status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY status;

-- 8. Average delivery time
SELECT
    ROUND(AVG(delivery_minutes), 2) AS average_delivery_time
FROM orders
WHERE status = 'completed';