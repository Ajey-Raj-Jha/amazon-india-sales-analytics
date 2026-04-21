# fix_order_date.py
import pandas as pd
from pathlib import Path

p = Path("data/combined.parquet")
df = pd.read_parquet(p)

df["order_datetime"] = pd.to_datetime(df["order_date"], errors="coerce")

print("order_datetime non-null:", df["order_datetime"].notna().sum(), "/", len(df))
print("Range:", df["order_datetime"].min(), "→", df["order_datetime"].max())

# save back
df.to_parquet("data/combined_fixed.parquet", index=False)
print("Saved fixed dataset as data/combined_fixed.parquet")
