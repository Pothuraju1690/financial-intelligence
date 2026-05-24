import pandas as pd
import os

PATH = "../data/clean"

# Load transformed data
profit = pd.read_csv(os.path.join(PATH, "profit_loss_transformed.csv"))
balance = pd.read_csv(os.path.join(PATH, "balance_sheet_transformed.csv"))
cash = pd.read_csv(os.path.join(PATH, "cash_flow_transformed.csv"))

print("📂 Data Loaded")

# -----------------------------
# STEP 1: Aggregate data per company
# -----------------------------

# Take average values per company
profit_avg = profit.groupby("company_id").mean(numeric_only=True).reset_index()
balance_avg = balance.groupby("company_id").mean(numeric_only=True).reset_index()
cash_avg = cash.groupby("company_id").mean(numeric_only=True).reset_index()

# Merge all
df = profit_avg.merge(balance_avg, on="company_id")
df = df.merge(cash_avg, on="company_id")

print("✅ Aggregation done")

# -----------------------------
# STEP 2: Create scoring metrics
# -----------------------------

# Normalize helper
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# Create scores
df["profit_score"] = normalize(df["profit_margin"])
df["leverage_score"] = 1 - normalize(df["debt_to_equity"])  # lower debt = better
df["cash_score"] = normalize(df["free_cash_flow"])

# Final score
df["health_score"] = (
    df["profit_score"] * 0.4 +
    df["leverage_score"] * 0.3 +
    df["cash_score"] * 0.3
) * 100

print("✅ Health score calculated")

# -----------------------------
# STEP 3: Label companies
# -----------------------------

def label(score):
    if score >= 75:
        return "EXCELLENT"
    elif score >= 60:
        return "GOOD"
    elif score >= 40:
        return "AVERAGE"
    else:
        return "POOR"

df["health_label"] = df["health_score"].apply(label)

# -----------------------------
# STEP 4: Save
# -----------------------------

df.to_csv(os.path.join(PATH, "company_health_scores.csv"), index=False)

print("\n🎯 Health Score Model completed!")