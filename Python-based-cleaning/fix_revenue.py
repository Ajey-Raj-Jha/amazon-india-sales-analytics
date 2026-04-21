# fix_revenue.py
import pandas as pd
from pathlib import Path
import numpy as np

p = Path("data/combined_fixed.parquet")
df = pd.read_parquet(p)

# Clean final_amount_inr
def clean_price(x):
    try:
        if pd.isna(x): return np.nan
        s = str(x).replace(",", "").replace("₹", "").strip()
        return float(s)
    except:
        return np.nan

df["revenue"] = df["final_amount_inr"].apply(clean_price)

print("revenue non-null:", df["revenue"].notna().sum(), "/", len(df))
print("Range:", df["revenue"].min(), "→", df["revenue"].max())

# Save back
df.to_parquet("data/combined_ready.parquet", index=False)
print("Saved dataset with clean revenue → data/combined_ready.parquet")
