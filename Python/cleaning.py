import pandas as pd
import os

raw_folder = os.path.join(os.path.dirname(__file__), "..", "Data", "Raw")
cleaned_folder = os.path.join(os.path.dirname(__file__), "..", "Data", "Cleaned")


customers = pd.read_csv(os.path.join(raw_folder, "olist_customers_dataset.csv"))
customers = customers.drop_duplicates()
customers["customer_city"] = customers["customer_city"].str.strip().str.lower()
customers["customer_state"] = customers["customer_state"].str.strip().str.lower()
customers.to_csv(os.path.join(cleaned_folder, "olist_customers_dataset_clean.csv"), index=False)


sellers = pd.read_csv(os.path.join(raw_folder, "olist_sellers_dataset.csv"))
sellers = sellers.drop_duplicates()
sellers["seller_city"] = sellers["seller_city"].str.strip().str.lower()
sellers["seller_state"] = sellers["seller_state"].str.strip().str.lower()
sellers.to_csv(os.path.join(cleaned_folder, "olist_sellers_dataset_clean.csv"), index=False)


geolocation = pd.read_csv(os.path.join(raw_folder, "olist_geolocation_dataset.csv"))
geolocation = geolocation.drop_duplicates()
geolocation["geolocation_city"] = geolocation["geolocation_city"].str.strip().str.lower()
geolocation["geolocation_state"] = geolocation["geolocation_state"].str.strip().str.lower()
geolocation.to_csv(os.path.join(cleaned_folder, "olist_geolocation_dataset_clean.csv"), index=False)


translation = pd.read_csv(os.path.join(raw_folder, "product_category_name_translation.csv"))
translation = translation.drop_duplicates()
translation.to_csv(os.path.join(cleaned_folder, "product_category_name_translation_clean.csv"), index=False)


products = pd.read_csv(os.path.join(raw_folder, "olist_products_dataset.csv"))
products = products.drop_duplicates()
products["product_category_name"] = products["product_category_name"].fillna("unknown")

products = products.merge(
    translation,
    how="left",
    on="product_category_name"
)

products["product_category_name_english"] = products["product_category_name_english"].fillna("unknown")

products.to_csv(os.path.join(cleaned_folder, "olist_products_dataset_clean.csv"), index=False)


orders = pd.read_csv(os.path.join(raw_folder, "olist_orders_dataset.csv"))
orders = orders.drop_duplicates()
orders["order_status"] = orders["order_status"].str.strip().str.lower()
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"], errors="coerce")
orders["order_approved_at"] = pd.to_datetime(orders["order_approved_at"], errors="coerce")
orders["order_delivered_carrier_date"] = pd.to_datetime(orders["order_delivered_carrier_date"], errors="coerce")
orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"], errors="coerce")
orders["order_estimated_delivery_date"] = pd.to_datetime(orders["order_estimated_delivery_date"], errors="coerce")
orders.to_csv(os.path.join(cleaned_folder, "olist_orders_dataset_clean.csv"), index=False)


order_items = pd.read_csv(os.path.join(raw_folder, "olist_order_items_dataset.csv"))
order_items = order_items.drop_duplicates()
order_items["shipping_limit_date"] = pd.to_datetime(order_items["shipping_limit_date"], errors="coerce")
order_items.to_csv(os.path.join(cleaned_folder, "olist_order_items_dataset_clean.csv"), index=False)


payments = pd.read_csv(os.path.join(raw_folder, "olist_order_payments_dataset.csv"))
payments = payments.drop_duplicates()
payments["payment_type"] = payments["payment_type"].str.strip().str.lower()
payments.to_csv(os.path.join(cleaned_folder, "olist_order_payments_dataset_clean.csv"), index=False)


reviews = pd.read_csv(os.path.join(raw_folder, "olist_order_reviews_dataset.csv"))
reviews = reviews.drop_duplicates()
reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"], errors="coerce")
reviews["review_answer_timestamp"] = pd.to_datetime(reviews["review_answer_timestamp"], errors="coerce")
reviews["review_comment_title"] = reviews["review_comment_title"].fillna("")
reviews["review_comment_message"] = reviews["review_comment_message"].fillna("")
reviews.to_csv(os.path.join(cleaned_folder, "olist_order_reviews_dataset_clean.csv"), index=False)