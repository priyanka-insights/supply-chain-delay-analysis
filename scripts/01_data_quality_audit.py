import pandas as pd

BASE = "C:/Users/prianka/OneDrive/Desktop/supply-chain-delay-analysis/data/raw/"

orders = pd.read_csv(BASE + "olist_orders_dataset.csv")
items = pd.read_csv(BASE + "olist_order_items_dataset.csv")
reviews = pd.read_csv(BASE + "olist_order_reviews_dataset.csv")

# Check 1: is order_id one-to-many between orders and order_items?
orders_count = orders["order_id"].nunique()
items_orders_count = items["order_id"].nunique()
items_per_order = items.groupby("order_id").size()

print("Check 1: order_items cardinality")
print(f"  Unique orders in orders table: {orders_count}")
print(f"  Unique orders in items table: {items_orders_count}")
print(f"  Avg items per order: {items_per_order.mean():.2f}")
print(f"  Orders with more than 1 item: {(items_per_order > 1).sum()} ({(items_per_order > 1).mean()*100:.1f}%)")

# Check 2: duplicate order_id in reviews table
duplicate_order_reviews = reviews["order_id"].duplicated().sum()

print("\nCheck 2: duplicate reviews")
print(f"  Total review rows: {len(reviews)}")
print(f"  Duplicate order_id count: {duplicate_order_reviews}")

# Check 3: monthly order volume — Olist data has a known Sep-Oct 2018 cutoff
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
monthly_orders = orders.groupby(orders["order_purchase_timestamp"].dt.to_period("M")).size()

print("\nCheck 3: monthly order count (last 6 months)")
print(monthly_orders.tail(6).to_string())

# Check 4: 'delivered' status orders missing delivery date
delivered_orders = orders[orders["order_status"] == "delivered"]
missing_date_count = delivered_orders["order_delivered_customer_date"].isnull().sum()

print("\nCheck 4: delivered orders missing delivery date")
print(f"  Total delivered orders: {len(delivered_orders)}")
print(f"  Missing delivery date: {missing_date_count}")