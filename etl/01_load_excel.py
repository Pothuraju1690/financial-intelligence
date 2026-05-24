import pandas as pd
import os

# Path to raw data
DATA_PATH = "../data/raw/"

files = {
    "companies": "companies.xlsx",
    "profit_loss": "profitandloss.xlsx",
    "balance_sheet": "balancesheet.xlsx",
    "cash_flow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "pros_cons": "prosandcons.xlsx",
    "documents": "documents.xlsx"
}

dataframes = {}

print("📂 Loading Excel files...\n")

for name, file in files.items():
    try:
        file_path = os.path.join(DATA_PATH, file)
        df = pd.read_excel(file_path)
        dataframes[name] = df

        print(f"✅ Loaded: {name}")
        print(df.head())
        print("\n----------------------\n")

    except Exception as e:
        print(f"❌ Error loading {file}: {e}")

print("🎯 All files loaded successfully!")