# inspect_prices.py
import pandas as pd
from pathlib import Path

p = Path("data/combined_fixed.parquet")
df = pd.read_parquet(p)

cands = [c for c in df.columns if any(tok in c.lower() for tok in ["price","amount","revenue","total"])]
print("Candidate price/revenue columns:")
for c in cands:
    nonnull = df[c].notna().sum()
    uniq = df[c].nunique(dropna=True)
    print(f"{c:25}  non-null: {nonnull:,}   unique: {uniq:,}")
    sample = df[c].dropna().astype(str).unique()[:6].tolist()
    print("  sample ->", sample)
    print()
