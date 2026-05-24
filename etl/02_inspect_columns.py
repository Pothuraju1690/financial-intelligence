import pandas as pd
import os

DATA_PATH = "../data/raw/"

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "prosandcons.xlsx",
    "documents.xlsx"
]

for file in files:
    print("\n" + "="*80)
    print(f"FILE: {file}")
    print("="*80)

    df = pd.read_excel(os.path.join(DATA_PATH, file))

    print("\nCOLUMNS:")
    for col in df.columns:
        print(col)

    print("\nFIRST 10 ROWS:")
    print(df.head(10))