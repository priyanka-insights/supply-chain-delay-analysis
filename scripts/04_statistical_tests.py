import pandas as pd
from pathlib import Path
from scipy import stats

BASE = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE / "data/processed/master_table_features.csv")

# H1: does delay rate genuinely vary by customer state? (chi-square)
table_h1 = pd.crosstab(df["customer_state"], df["is_delayed"])
chi2, p_h1, dof, expected = stats.chi2_contingency(table_h1)

print("H1: State vs Delay rate")
print(f"  p-value = {p_h1:.6f}")

# H2: is festive season (Nov-Dec) delay rate higher? (chi-square)
table_h2 = pd.crosstab(df["is_festive_season"], df["is_delayed"])
chi2, p_h2, dof, expected = stats.chi2_contingency(table_h2)
festive_rate = df[df["is_festive_season"] == 1]["is_delayed"].mean() * 100
normal_rate = df[df["is_festive_season"] == 0]["is_delayed"].mean() * 100

print("\nH2: Festive season vs Delay rate")
print(f"  Festive: {festive_rate:.2f}%  |  Normal: {normal_rate:.2f}%")
print(f"  p-value = {p_h2:.6f}")

# H3: does delay length correlate with review score? (Spearman — review score is ordinal)
df_with_review = df.dropna(subset=["review_score"])
corr, p_h3 = stats.spearmanr(df_with_review["delay_days"], df_with_review["review_score"])

print("\nH3: Delay days vs Review score")
print(f"  Spearman correlation = {corr:.3f}, p-value = {p_h3:.6f}")

# H4: seller state delay ranking vs customer state delay ranking
seller_delay_rate = df.groupby("seller_state")["is_delayed"].mean().sort_values(ascending=False) * 100
customer_delay_rate = df.groupby("customer_state")["is_delayed"].mean().sort_values(ascending=False) * 100

print("\nH4: Top 5 seller states by delay rate")
print(seller_delay_rate.head(5).round(2).to_string())
print("\nTop 5 customer states by delay rate")
print(customer_delay_rate.head(5).round(2).to_string())
