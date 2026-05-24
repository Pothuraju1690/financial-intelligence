import pandas as pd
import os

RAW_PATH = "../data/raw"
CLEAN_PATH = "../data/clean"

os.makedirs(CLEAN_PATH, exist_ok=True)

files = {
    "companies": "companies.xlsx",
    "profit_loss": "profitandloss.xlsx",
    "balance_sheet": "balancesheet.xlsx",
    "cash_flow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "pros_cons": "prosandcons.xlsx",
    "documents": "documents.xlsx"
}

for table_name, file_name in files.items():
    print(f"\nCleaning {table_name}...")

    file_path = os.path.join(RAW_PATH, file_name)

    # IMPORTANT: header=1 means second row contains real column names
    df = pd.read_excel(file_path, header=1)

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "percentage")
        .str.replace("-", "_")
    )

    # Remove fully empty rows/columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Save clean CSV
    output_path = os.path.join(CLEAN_PATH, f"{table_name}.csv")
    df.to_csv(output_path, index=False)

    print(f"✅ Saved: {output_path}")
    print(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
    print("Columns:", list(df.columns))

print("\n🎯 All Excel files cleaned and saved as CSV!")