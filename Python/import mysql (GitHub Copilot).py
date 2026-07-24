import os
import re
import numpy as np
import pandas as pd
import mysql.connector

# =========================
# CONFIG
# =========================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "sales_analytics",
    "port": 3306,
    "charset": "utf8mb4",
    "use_unicode": True,
    "autocommit": False
}

DATA_DIR = r"D:\Projects\Sales-Business-Analytics\Data\Raw"

FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "translation": "product_category_name_translation.csv",
    "products": "olist_products_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
}

BATCH_SIZE = 5000


# =========================
# HELPERS
# =========================
def py_val(x):
    if x is None or pd.isna(x):
        return None
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.floating):
        return float(x)
    if isinstance(x, pd.Timestamp):
        return x.to_pydatetime()
    return x

def chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def run_insert(cursor, sql, rows, batch_size=BATCH_SIZE):
    for batch in chunked(rows, batch_size):
        cursor.executemany(sql, batch)

def read_csv(path):
    return pd.read_csv(path, encoding="utf-8", keep_default_na=True, encoding_errors="replace")

def table_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]

def strip_4byte_chars(text):
    """Remove chars outside BMP (e.g., many emojis) for utf8 (3-byte) DB compatibility."""
    if text is None or pd.isna(text):
        return None
    s = str(text)
    return re.sub(r"[\U00010000-\U0010FFFF]", "", s)


# =========================
# LOADERS
# =========================
def load_customers(cursor, path):
    df = read_csv(path)[[
        "customer_id", "customer_unique_id", "customer_zip_code_prefix",
        "customer_city", "customer_state"
    ]]
    df["customer_zip_code_prefix"] = pd.to_numeric(df["customer_zip_code_prefix"], errors="coerce")

    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
    sql = """
    INSERT INTO customers (
      customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state
    ) VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      customer_unique_id=VALUES(customer_unique_id),
      customer_zip_code_prefix=VALUES(customer_zip_code_prefix),
      customer_city=VALUES(customer_city),
      customer_state=VALUES(customer_state)
    """
    run_insert(cursor, sql, rows)

def load_geolocation(cursor, path):
    df = read_csv(path)[[
        "geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng",
        "geolocation_city", "geolocation_state"
    ]]
    df["geolocation_zip_code_prefix"] = pd.to_numeric(df["geolocation_zip_code_prefix"], errors="coerce")
    df["geolocation_lat"] = pd.to_numeric(df["geolocation_lat"], errors="coerce")
    df["geolocation_lng"] = pd.to_numeric(df["geolocation_lng"], errors="coerce")

    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
    sql = """
    INSERT INTO geolocation (
      geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state
    ) VALUES (%s, %s, %s, %s, %s)
    """
    run_insert(cursor, sql, rows)

def load_sellers(cursor, path):
    df = read_csv(path)[["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"]]
    df["seller_zip_code_prefix"] = pd.to_numeric(df["seller_zip_code_prefix"], errors="coerce")

    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
    sql = """
    INSERT INTO sellers (
      seller_id, seller_zip_code_prefix, seller_city, seller_state
    ) VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      seller_zip_code_prefix=VALUES(seller_zip_code_prefix),
      seller_city=VALUES(seller_city),
      seller_state=VALUES(seller_state)
    """
    run_insert(cursor, sql, rows)

def load_translation(cursor, path):
    df = read_csv(path)[["product_category_name", "product_category_name_english"]]
    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]

    sql = """
    INSERT INTO translation (
      product_category_name, product_category_name_english
    ) VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE
      product_category_name_english=VALUES(product_category_name_english)
    """
    run_insert(cursor, sql, rows)

def load_products(cursor, path):
    df = read_csv(path)[[
        "product_id", "product_category_name", "product_name_lenght",
        "product_description_lenght", "product_photos_qty", "product_weight_g",
        "product_length_cm", "product_height_cm", "product_width_cm"
    ]]

    for c in [
        "product_name_lenght", "product_description_lenght", "product_photos_qty",
        "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"
    ]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    cursor.execute("SELECT product_category_name FROM translation")
    valid_categories = {r[0] for r in cursor.fetchall() if r[0] is not None}

    def normalize_category(x):
        if x is None or pd.isna(x):
            return None
        s = str(x).strip()
        if s == "" or s not in valid_categories:
            return None
        return s

    df["product_category_name"] = df["product_category_name"].apply(normalize_category)

    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
    sql = """
    INSERT INTO products (
      product_id, product_category_name, product_name_lenght, product_description_lenght,
      product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      product_category_name=VALUES(product_category_name),
      product_name_lenght=VALUES(product_name_lenght),
      product_description_lenght=VALUES(product_description_lenght),
      product_photos_qty=VALUES(product_photos_qty),
      product_weight_g=VALUES(product_weight_g),
      product_length_cm=VALUES(product_length_cm),
      product_height_cm=VALUES(product_height_cm),
      product_width_cm=VALUES(product_width_cm)
    """
    run_insert(cursor, sql, rows)

def load_orders(cursor, path):
    df = read_csv(path)[[
        "order_id", "customer_id", "order_status", "order_purchase_timestamp",
        "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date"
    ]]

    for c in [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]:
        df[c] = pd.to_datetime(df[c], errors="coerce")

    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
    sql = """
    INSERT INTO orders (
      order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at,
      order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      customer_id=VALUES(customer_id),
      order_status=VALUES(order_status),
      order_purchase_timestamp=VALUES(order_purchase_timestamp),
      order_approved_at=VALUES(order_approved_at),
      order_delivered_carrier_date=VALUES(order_delivered_carrier_date),
      order_delivered_customer_date=VALUES(order_delivered_customer_date),
      order_estimated_delivery_date=VALUES(order_estimated_delivery_date)
    """
    run_insert(cursor, sql, rows)

def load_order_items(cursor, path):
    df = read_csv(path)[[
        "order_id", "order_item_id", "product_id", "seller_id",
        "shipping_limit_date", "price", "freight_value"
    ]]

    df["order_item_id"] = pd.to_numeric(df["order_item_id"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["freight_value"] = pd.to_numeric(df["freight_value"], errors="coerce")
    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")

    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
    sql = """
    INSERT INTO order_items (
      order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      product_id=VALUES(product_id),
      seller_id=VALUES(seller_id),
      shipping_limit_date=VALUES(shipping_limit_date),
      price=VALUES(price),
      freight_value=VALUES(freight_value)
    """
    run_insert(cursor, sql, rows)

def load_payments(cursor, path):
    df = read_csv(path)[[
        "order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"
    ]]

    df["payment_sequential"] = pd.to_numeric(df["payment_sequential"], errors="coerce")
    df["payment_installments"] = pd.to_numeric(df["payment_installments"], errors="coerce")
    df["payment_value"] = pd.to_numeric(df["payment_value"], errors="coerce")

    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
    sql = """
    INSERT INTO payments (
      order_id, payment_sequential, payment_type, payment_installments, payment_value
    ) VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      payment_type=VALUES(payment_type),
      payment_installments=VALUES(payment_installments),
      payment_value=VALUES(payment_value)
    """
    run_insert(cursor, sql, rows)

def load_reviews(cursor, path):
    df = read_csv(path)[[
        "review_id", "order_id", "review_score", "review_comment_title",
        "review_comment_message", "review_creation_date", "review_answer_timestamp"
    ]]

    df["review_score"] = pd.to_numeric(df["review_score"], errors="coerce")
    df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], errors="coerce")
    df["review_answer_timestamp"] = pd.to_datetime(df["review_answer_timestamp"], errors="coerce")

    rows = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
    sql = """
    INSERT INTO reviews (
      review_id, order_id, review_score, review_comment_title, review_comment_message,
      review_creation_date, review_answer_timestamp
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
      order_id=VALUES(order_id),
      review_score=VALUES(review_score),
      review_comment_title=VALUES(review_comment_title),
      review_comment_message=VALUES(review_comment_message),
      review_creation_date=VALUES(review_creation_date),
      review_answer_timestamp=VALUES(review_answer_timestamp)
    """

    try:
        run_insert(cursor, sql, rows)
    except mysql.connector.Error as e:
        # Fallback for utf8 (3-byte) columns that reject emoji
        if e.errno == 1366:
            print("⚠️ review text has unsupported chars for current DB charset; sanitizing and retrying reviews...")
            df["review_comment_title"] = df["review_comment_title"].apply(strip_4byte_chars)
            df["review_comment_message"] = df["review_comment_message"].apply(strip_4byte_chars)
            rows2 = [tuple(py_val(v) for v in r) for r in df.itertuples(index=False, name=None)]
            run_insert(cursor, sql, rows2)
        else:
            raise


# =========================
# MAIN
# =========================
def main():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Connected.")

        # UTF-8 session
        cursor.execute("SET NAMES utf8mb4")
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET collation_connection = 'utf8mb4_unicode_ci'")

        loaders = [
            ("customers", load_customers),
            ("geolocation", load_geolocation),
            ("sellers", load_sellers),
            ("translation", load_translation),
            ("products", load_products),
            ("orders", load_orders),
            ("order_items", load_order_items),
            ("payments", load_payments),
            ("reviews", load_reviews),
        ]

        for table, fn in loaders:
            fpath = os.path.join(DATA_DIR, FILES[table])
            print(f"Loading {table} from {fpath} ...")
            fn(cursor, fpath)
            conn.commit()
            print(f"✅ {table} loaded | rows now: {table_count(cursor, table)}")

        print("\n🎉 All imports completed successfully.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Import failed: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()