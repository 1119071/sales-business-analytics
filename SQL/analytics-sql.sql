USE sales_analytics;

# Customers
SELECT COUNT(DISTINCT customer_unique_id) as customer_count
FROM customers;

SELECT COUNT(customer_unique_id) as customer_count, customer_city
FROM customers
GROUP BY customer_city;

SELECT COUNT(customer_unique_id) as customer_count, customer_state, customer_city
FROM customers
GROUP BY customer_city, customer_state
ORDER BY customer_count DESC
Limit 20;

# Geolocation
SELECT COUNT(geolocation_zip_code_prefix) as geolocation_zip_code_count, geolocation_city, geolocation_state
FROM geolocation
GROUP BY geolocation_city, geolocation_state
ORDER BY geolocation_zip_code_count ASC
Limit 10;

SELECT COUNT(geolocation_zip_code_prefix) as geolocation_zip_code_count, geolocation_city, geolocation_state
FROM geolocation
GROUP BY geolocation_city, geolocation_state
ORDER BY geolocation_zip_code_count DESC
Limit 10;

# Order Items
SELECT COUNT(DISTINCT product_id) AS product_count, seller_id
FROM order_items
GROUP BY seller_id
ORDER BY product_count DESC;

SELECT AVG(price) as average_price
FROM order_items;

SELECT seller_id, SUM(price) as total_revenue
FROM order_items
GROUP BY seller_id
ORDER BY total_revenue DESC
LIMIT 10;

SELECT product_id, SUM(price) as total_revenue
FROM order_items
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;

SELECT seller_id, SUM(price) as total_revenue
FROM order_items
GROUP BY seller_id
ORDER BY total_revenue DESC
LIMIT 10;

# Payments
SELECT AVG(payment_value) as average_payment
FROM payments;

SELECT COUNT(payment_type) as payment_type_count, payment_type
FROM payments
GROUP BY payment_type
ORDER BY payment_type_count DESC;

SELECT AVG(payment_value) as average_payment_value, payment_type
FROM payments
GROUP BY payment_type
ORDER BY average_payment_value DESC;

# Reviews
SELECT AVG(review_score)
FROM reviews;

SELECT COUNT(review_comment_title) as count_review_comment_title, COUNT(review_comment_message) as count_review_comment_message
FROM reviews;

# Orders
SELECT COUNT(order_status) as count_order_status, order_status
FROM orders
GROUP BY order_status
ORDER BY count_order_status DESC;

SELECT AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)) as average_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

SELECT YEAR(order_purchase_timestamp) as year, MONTH(order_purchase_timestamp) as month, COUNT(*) as order_count
FROM orders
GROUP BY YEAR(order_purchase_timestamp), MONTH(order_purchase_timestamp)
ORDER BY year, month;

# Products
SELECT AVG(product_weight_g) as average_weight
FROM products;

SELECT MAX(product_length_cm) as max_product_length
FROM products;

SELECT COUNT(product_id) as count_product, product_category_name
FROM products
GROUP BY product_category_name
ORDER BY count_product DESC
Limit 10;

# Sellers
SELECT COUNT(seller_id) as count_seller, seller_city, seller_state
FROM sellers
GROUP BY seller_city, seller_state
ORDER BY count_seller DESC;

SELECT COUNT(seller_id) as count_seller, seller_zip_code_prefix
FROM sellers
GROUP BY seller_zip_code_prefix
ORDER BY count_seller DESC;

# Translation
SELECT COUNT(DISTINCT(product_category_name))
FROM translation;

# JOIN's
SELECT YEAR(o.order_purchase_timestamp) as year, MONTH(o.order_purchase_timestamp) as month, SUM(oi.price) as total_revenue
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY YEAR(o.order_purchase_timestamp), MONTH(o.order_purchase_timestamp)
ORDER BY year, month;

SELECT c.customer_state, SUM(oi.price) as total_revenue
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN order_items oi
ON o.order_id = oi.order_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC;

SELECT t.product_category_name_english, COUNT(*) as items_sold
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
JOIN translation t
ON p.product_category_name = t.product_category_name
GROUP BY t.product_category_name_english
ORDER BY items_sold DESC
LIMIT 10;

SELECT t.product_category_name_english, SUM(oi.price) as total_revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
JOIN translation t
ON p.product_category_name = t.product_category_name
GROUP BY t.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;