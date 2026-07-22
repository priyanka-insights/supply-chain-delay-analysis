import pandas as pd

BASE = "C:/Users/prianka/OneDrive/Desktop/supply-chain-delay-analysis/"

orders = pd.read_csv(BASE + "data/raw/olist_orders_dataset.csv")
items = pd.read_csv(BASE + "data/raw/olist_order_items_dataset.csv")
reviews = pd.read_csv(BASE + "data/raw/olist_order_reviews_dataset.csv")
customers = pd.read_csv(BASE + "data/raw/olist_customers_dataset.csv")
sellers = pd.read_csv(BASE + "data/raw/olist_sellers_dataset.csv")

# Step 1: keep only delivered orders that have a delivery date
delivered = orders[orders["order_status"] == "delivered"].copy()
delivered = delivered.dropna(subset=["order_delivered_customer_date"])

print(f"Step 1: {len(orders)} total orders -> {len(delivered)} usable delivered orders")

# Step 2: aggregate order_items to order-level (order_id is one-to-many)
items_agg = items.groupby("order_id").agg(
    total_price=("price", "sum"),
    total_freight=("freight_value", "sum"),
    item_count=("order_item_id", "count"),
    seller_id=("seller_id", "first")
).reset_index()

print(f"Step 2: items aggregated to {len(items_agg)} order-level rows")

# Step 3: remove duplicate reviews, keep latest review per order
reviews_clean = reviews.sort_values("review_answer_timestamp").drop_duplicates(
    subset="order_id", keep="last"
)

print(f"Step 3: reviews deduplicated to {len(reviews_clean)} rows")

# Step 4: merge everything into one master table
master = delivered.merge(customers, on="customer_id", how="left")
master = master.merge(items_agg, on="order_id", how="inner")
master = master.merge(sellers, on="seller_id", how="left")
master = master.merge(reviews_clean[["order_id", "review_score"]], on="order_id", how="left")

date_cols = ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
for col in date_cols:
    master[col] = pd.to_datetime(master[col])

print(f"Step 4: master table shape = {master.shape}")
print(f"  Missing review_score: {master['review_score'].isnull().sum()}")

master.to_csv(BASE + "data/processed/master_table.csv", index=False)
print("\nSaved: data/processed/master_table.csv")