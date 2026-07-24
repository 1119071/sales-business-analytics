import pandas as pd
import matplotlib.pyplot as plt

customers = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/olist_customers_dataset_clean.csv")
geolocation = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/olist_geolocation_dataset_clean.csv")
order_items = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/olist_order_items_dataset_clean.csv")
payments = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/olist_order_payments_dataset_clean.csv")
reviews = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/olist_order_reviews_dataset_clean.csv")
orders = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/olist_orders_dataset_clean.csv")
products = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/olist_products_dataset_clean.csv")
sellers = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/olist_sellers_dataset_clean.csv")
translation = pd.read_csv("D:/Projects/Sales-Business-Analytics/Data/Cleaned/product_category_name_translation_clean.csv")


most_expensive_product = order_items["price"].max()
print("Most Expensive Item:", most_expensive_product)

cheapest_product = order_items["price"].min()
print("Cheapest Product:", cheapest_product)

average_product_price = order_items["price"].mean()
print("Average Product Price:", average_product_price)

customer_count = customers["customer_unique_id"].nunique()
print("Customer Count:", customer_count)

top_products = order_items.groupby("product_id")["price"].sum().sort_values(ascending=False).head(10)
print("Top Products:", top_products)

top_sellers = order_items.groupby("seller_id")["price"].sum().sort_values(ascending=False).head(10)
print("Top Sellers:", top_sellers)

payment_methods = payments["payment_type"].value_counts()
print("Payment Methods:", payment_methods)

average_payment = payments["payment_value"].mean()
print("Average Payment:", average_payment)

average_review_score = reviews["review_score"].mean()
print("Average Review Score:", average_review_score)

sales = orders.merge(order_items, on="order_id")
print(sales.head())

revenue = round((order_items["price"] + order_items["freight_value"]).sum(),2)
print("Revenue Including Shipping:", revenue)

orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
delivery_days = orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
average_delivery_days = delivery_days.dt.days.mean()
print(average_delivery_days)

sales["order_purchase_timestamp"] = pd.to_datetime(sales["order_purchase_timestamp"])
sales["month"] = sales["order_purchase_timestamp"].dt.to_period("M")
monthly_revenue = sales.groupby("month")["price"].sum()
print(monthly_revenue)

sales = orders.merge(customers,on="customer_id")
sales = sales.merge(order_items, on="order_id")
revenue_by_state = sales.groupby("customer_state")["price"].sum().sort_values(ascending=False)
print(revenue_by_state)

category_sales = order_items.merge(products, on="product_id")
top_categories = (category_sales.groupby("product_category_name_english")["price"].sum().sort_values(ascending=False).head(10))
print(top_categories)


top_products.plot(kind="bar")
plt.title("Top 10 Products By Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

top_sellers.plot(kind="bar")
plt.title("Top 10 Sellers By Revenue")
plt.xlabel("Seller")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

revenue_by_state.head(10).plot(kind="bar")
plt.title("Top 10 States By Revenue")
plt.xlabel("State")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

monthly_revenue.plot(kind="line")
plt.title("Revenue Over Time")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()