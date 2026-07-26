# Sales Business Analytics — Olist Brazilian E-Commerce

A data analytics project that takes the Olist Brazilian E-commerce dataset from raw CSV files through cleaning, a MySQL relational database, Python-based analysis, and a Power BI dashboard.

Built by **Level Up Systems**.

Python | Pandas | MySQL | SQL | Power BI | Data Analytics

---

## Overview

This project explores an e-commerce dataset covering customers, orders, order items, payments, reviews, products, and sellers. The pipeline is:

1. **Raw CSVs** → cleaned and standardized with `cleaning.py`
2. **Cleaned CSVs** → imported into a MySQL database (`sales_analytics`) with a custom import script
3. **MySQL database** → queried directly (`analytics-sql.sql`) and analyzed with Python/pandas (`analytics.py`)
4. **Insights** → visualized in an interactive **Power BI** dashboard (`Power_BI_Analysis.pbix`)

The dataset is the public [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle.

---

## Project Structure

```
Sales-Business-Analytics/
│
├── Data/
│   ├── Raw/                                   # Original Olist CSV files
│   └── Cleaned/                                # Cleaned CSVs, output of cleaning.py
│       ├── olist_customers_dataset_clean.csv
│       ├── olist_geolocation_dataset_clean.csv
│       ├── olist_order_items_dataset_clean.csv
│       ├── olist_order_payments_dataset_clean.csv
│       ├── olist_order_reviews_dataset_clean.csv
│       ├── olist_orders_dataset_clean.csv
│       ├── olist_products_dataset_clean.csv
│       ├── olist_sellers_dataset_clean.csv
│       └── product_category_name_translation_clean.csv
│
├── cleaning.py                                 # Cleans raw CSVs and exports cleaned versions
├── data_information.py                         # Inspects raw data (shape, dtypes, nulls)
├── analytics.py                                # Pandas analysis + matplotlib charts
├── import_mysql (GitHub Copilot).py            # Loads cleaned CSVs into MySQL
├── create-database.sql                         # Creates the sales_analytics database
├── create-tables.sql                           # Creates all tables and relationships
├── analytics-sql.sql                            # SQL queries used for analysis
├── Power_BI_Analysis.pbix                       # Power BI dashboard
├── requirements.txt
└── README.md
```

### Python

| File | Purpose |
|---|---|
| `cleaning.py` | Reads the raw CSVs, drops duplicates, standardizes text fields, parses dates, fills missing categories/comments, and exports cleaned CSVs |
| `data_information.py` | Inspects the raw datasets — shape, columns, dtypes, and null counts per table |
| `import_mysql (GitHub Copilot).py` | Connects to MySQL and loads the cleaned CSVs into the `sales_analytics` database, with batched inserts and error handling |
| `analytics.py` | Loads the cleaned CSVs with pandas, computes key metrics (top products/sellers, revenue by state, monthly revenue, delivery times, etc.) and generates matplotlib charts |

### SQL

| File | Purpose |
|---|---|
| `create-database.sql` | Creates the `sales_analytics` database |
| `create-tables.sql` | Creates the 9 tables and their foreign key relationships |
| `analytics-sql.sql` | Standalone SQL queries covering customers, orders, products, sellers, payments, reviews, and joined revenue/category analysis |

### Data

| File | Purpose |
|---|---|
| `Data/Raw/` | Original, unmodified Olist CSV files |
| `Data/Cleaned/` | Cleaned CSVs (output of `cleaning.py`), used by both `analytics.py` and the MySQL import script |

> **Note:** the CSV data files are not included in this repository — several exceed GitHub's per-file size limits and, more generally, raw datasets don't belong in a code repo. To run this project yourself:
> 1. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
> 2. Place the raw CSVs in `Data/Raw/`
> 3. Run `cleaning.py` to generate the cleaned CSVs in `Data/Cleaned/`

### Power BI

| File | Purpose |
|---|---|
| `Power_BI_Analysis.pbix` | Interactive dashboard built on top of the `sales_analytics` MySQL database |

### Docs

| File | Purpose |
|---|---|
| `README.md` | Project documentation (this file) |
| `requirements.txt` | Python dependencies |

---

## Database Schema

The MySQL database `sales_analytics` consists of 9 tables:

| Table | Description |
|---|---|
| `customers` | Customer ID, location (city/state), zip code |
| `sellers` | Seller ID, location, zip code |
| `geolocation` | Zip code to lat/lng mapping |
| `translation` | Portuguese → English product category names |
| `products` | Product dimensions, weight, category |
| `orders` | Order status and all timestamps (purchase, approval, delivery) |
| `order_items` | Line items per order: product, seller, price, freight |
| `payments` | Payment type, installments, value |
| `reviews` | Review score, comments, timestamps |

Relationships are enforced with foreign keys (see `create-tables.sql`), linking `orders` → `customers`, `order_items` → `orders`/`products`/`sellers`, `payments`/`reviews` → `orders`, and `products` → `translation`.

---

## Analysis Highlights

Using `analytics.py` and `analytics-sql.sql`, the project answers questions such as:

- What are the top-selling products and top-performing sellers by revenue?
- How is revenue distributed across Brazilian states?
- What are the most common payment types, and how does average payment value differ between them?
- What is the average customer review score?
- How does revenue trend over time (monthly)?
- What is the average delivery time (order purchase → delivery)?
- Which product categories generate the most revenue and the most items sold?

These same insights are presented interactively in the **Power BI dashboard**.

---

## Setup

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Set up the database

Run in MySQL (e.g. MySQL Workbench or CLI):

```bash
mysql -u root -p < create-database.sql
mysql -u root -p < create-tables.sql
```

### 3. Clean the raw data

Update the `raw_folder` / `cleaned_folder` paths in `cleaning.py` if needed, then run:

```bash
python cleaning.py
```

### 4. Import into MySQL

Update `DB_CONFIG` and `DATA_DIR` in `import_mysql.py` to match your local setup, then run:

```bash
python "import_mysql.py"
```

### 5. Run the analysis

```bash
python analytics.py
```

### 6. Open the dashboard

Open `Power_BI_Analysis.pbix` in Power BI Desktop. If prompted, reconnect the data source to your local MySQL database.


---

## Data Source & Attribution

Dataset: [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), provided by Olist on Kaggle, used here for educational/portfolio purposes.

---

## Notes on AI Usage

This project was built and coded by me. In some parts, AI was used to help clarify and refine the code without drastically changing the logic or approach.

The MySQL import script (`import_mysql (GitHub Copilot).py`) was written with AI assistance specifically, since MySQL Workbench's built-in Import Wizard failed on this dataset (authentication issues, dropped connections on large inserts, duplicate key conflicts, and character encoding errors with emoji/4-byte UTF-8 characters in review text). The AI-assisted script resolves these issues directly with batched inserts, `ON DUPLICATE KEY UPDATE` handling, and a fallback that sanitizes unsupported characters.

---

## License

This project is shared for portfolio purposes. The underlying dataset is licensed by Olist via Kaggle under its own terms — see the Kaggle page for details.
