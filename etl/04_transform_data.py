import pandas as pd
import os

CLEAN_PATH = "../data/clean"

# Load datasets
companies = pd.read_csv(os.path.join(CLEAN_PATH, "companies.csv"))
profit = pd.read_csv(os.path.join(CLEAN_PATH, "profit_loss.csv"))
balance = pd.read_csv(os.path.join(CLEAN_PATH, "balance_sheet.csv"))
cash = pd.read_csv(os.path.join(CLEAN_PATH, "cash_flow.csv"))

print("📂 Data Loaded")

# -----------------------------
# STEP 1: Convert numeric columns
# -----------------------------

def convert_numeric(df):
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            continue
    return df

profit = convert_numeric(profit)
balance = convert_numeric(balance)
cash = convert_numeric(cash)

print("✅ Numeric conversion done")

# -----------------------------
# STEP 2: Create computed columns
# -----------------------------

# Profit margin
profit["profit_margin"] = (profit["net_profit"] / profit["sales"]) * 100

# Debt to equity
balance["debt_to_equity"] = balance["borrowings"] / (
    balance["equity_capital"] + balance["reserves"]
)

# Free cash flow
cash["free_cash_flow"] = (
    cash["operating_activity"] + cash["investing_activity"]
)

print("✅ Computed columns created")

# -----------------------------
# STEP 3: Save transformed data
# -----------------------------

TRANSFORM_PATH = "../data/clean"

profit.to_csv(os.path.join(TRANSFORM_PATH, "profit_loss_transformed.csv"), index=False)
balance.to_csv(os.path.join(TRANSFORM_PATH, "balance_sheet_transformed.csv"), index=False)
cash.to_csv(os.path.join(TRANSFORM_PATH, "cash_flow_transformed.csv"), index=False)

print("\n🎯 Transformation complete and saved!")