import pandas as pd
import matplotlib.pyplot as plt
import os

BASE = "C:/Users/prianka/OneDrive/Desktop/supply-chain-delay-analysis/"
os.makedirs(BASE + "charts", exist_ok=True)

df = pd.read_csv(BASE + "data/processed/master_table_features.csv")

## Which states have the highest delivery delay rate, and how do they compare to the national average?
state_delay = df.groupby("customer_state")["is_delayed"].mean().sort_values(ascending=False).head(10) * 100

plt.figure(figsize=(8, 5))
plt.bar(state_delay.index, state_delay.values, color="steelblue")
plt.axhline(y=df["is_delayed"].mean() * 100, color="red", linestyle="--", label="National average")
plt.title("Top 10 States by Delay Rate")
plt.xlabel("Customer State")
plt.ylabel("Delay Rate (%)")
plt.legend()
plt.tight_layout()
plt.savefig("charts/delay_rate_by_state.png")
plt.show()


# ---------- Chart 2: Monthly delay trend ----------
exclude_months = ["2018-09", "2018-10", "2016-09", "2016-10", "2016-12"]
monthly = df[~df["purchase_month"].isin(exclude_months)]
monthly_rate = monthly.groupby("purchase_month")["is_delayed"].mean() * 100

plt.figure(figsize=(10, 5))
plt.plot(monthly_rate.index, monthly_rate.values, marker="o", color="darkorange")
plt.xticks(rotation=45)
plt.title("Monthly Delay Rate Trend")
plt.xlabel("Month")
plt.ylabel("Delay Rate (%)")
plt.tight_layout()
plt.savefig(BASE + "charts/monthly_delay_trend.png")
plt.show()

# ---------- Chart 3: Review score by delay bucket ----------
order = ["on_time", "1-3_days_late", "4-7_days_late", "8plus_days_late"]
review_by_bucket = df.dropna(subset=["review_score"]).groupby("delay_bucket")["review_score"].mean().reindex(order)

plt.figure(figsize=(7, 5))
plt.bar(review_by_bucket.index, review_by_bucket.values, color="seagreen")
plt.title("Average Review Score by Delay Severity")
plt.xlabel("Delay Bucket")
plt.ylabel("Avg Review Score")
plt.tight_layout()
plt.savefig(BASE + "charts/review_score_by_delay.png")
plt.show()

# ---------- Chart 4: Financial exposure by state ----------
exposure = df.groupby("customer_state")["penalty_cost"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(8, 5))
plt.bar(exposure.index, exposure.values, color="indianred")
plt.title("Top 10 States by Total Penalty Exposure")
plt.xlabel("Customer State")
plt.ylabel("Total Penalty Cost (R$)")
plt.tight_layout()
plt.savefig(BASE + "charts/penalty_exposure_by_state.png")
plt.show()


# ---------- Chart 5: Seller state vs Customer state delay rate ----------
seller_counts = df["seller_state"].value_counts()
valid_seller_states = seller_counts[seller_counts >= 20].index

seller_delay = df[df["seller_state"].isin(valid_seller_states)].groupby("seller_state")["is_delayed"].mean().sort_values(ascending=False).head(5) * 100
customer_delay = df.groupby("customer_state")["is_delayed"].mean().sort_values(ascending=False).head(5) * 100

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

axes[0].bar(seller_delay.index, seller_delay.values, color="darkslateblue")
axes[0].set_title("Top 5 Seller States by Delay Rate")
axes[0].set_ylabel("Delay Rate (%)")

axes[1].bar(customer_delay.index, customer_delay.values, color="steelblue")
axes[1].set_title("Top 5 Customer States by Delay Rate")
axes[1].set_ylabel("Delay Rate (%)")

plt.tight_layout()
plt.savefig(BASE + "charts/seller_vs_customer_delay.png")
plt.show()