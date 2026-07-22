import pandas as pd

BASE = "C:/Users/prianka/OneDrive/Desktop/supply-chain-delay-analysis/"

master = pd.read_csv(BASE + "data/processed/master_table.csv", parse_dates=[
    "order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"
])

# delay_days: actual delivery date minus promised date. Positive = late.
master["delay_days"] = (master["order_delivered_customer_date"] - master["order_estimated_delivery_date"]).dt.days

# is_delayed: binary flag used for rate calculations and hypothesis tests
master["is_delayed"] = (master["delay_days"] > 0).astype(int)

# delay_bucket: groups delay_days into readable ranges
def bucket_delay(days):
    if days <= 0:
        return "on_time"
    elif days <= 3:
        return "1-3_days_late"
    elif days <= 7:
        return "4-7_days_late"
    else:
        return "8plus_days_late"

master["delay_bucket"] = master["delay_days"].apply(bucket_delay)

# purchase_month: used for trend chart, excludes the Sep-Oct 2018 data cutoff
master["purchase_month"] = master["order_purchase_timestamp"].dt.to_period("M").astype(str)

# is_festive_season: Nov-Dec flag, based on purchase date
master["is_festive_season"] = master["order_purchase_timestamp"].dt.month.isin([11, 12]).astype(int)

# delivery_duration_days: absolute purchase-to-delivery time (different from delay_days)
master["delivery_duration_days"] = (master["order_delivered_customer_date"] - master["order_purchase_timestamp"]).dt.days

# order_value_total: base value used for penalty_cost
master["order_value_total"] = master["total_price"] + master["total_freight"]

# penalty_cost: modeling assumption (10% of order value) — no real SLA penalty data exists
master["penalty_cost"] = master["order_value_total"] * 0.10 * master["is_delayed"]

print(f"Overall delay rate: {master['is_delayed'].mean()*100:.2f}%")
print(f"\nDelay bucket counts:")
print(master["delay_bucket"].value_counts().to_string())
print(f"\nTotal estimated penalty exposure: R$ {master['penalty_cost'].sum():,.2f}")

master.to_csv(BASE + "data/processed/master_table_features.csv", index=False)
print("\nSaved: data/processed/master_table_features.csv")