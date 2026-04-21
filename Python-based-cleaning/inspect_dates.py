# inspect_dates.py
from pathlib import Path
import pandas as pd

p = Path("data/combined.parquet")
if not p.exists():
    p = Path("data/combined.csv")
    if not p.exists():
        raise SystemExit("No combined file found at data/combined.parquet or data/combined.csv")

# load combined (parquet preferred)
if p.suffix == ".parquet":
    df = pd.read_parquet(p)
else:
    df = pd.read_csv(p, low_memory=False)

print("ROWS:", len(df), "COLS:", df.shape[1])
print("Columns with 'date'/'year' in name and their non-null counts:\n")

cands = [c for c in df.columns if any(tok in c.lower() for tok in ["date","day","month","year"])]
for c in sorted(cands):
    nonnull = df[c].notna().sum()
    uniq = df[c].nunique(dropna=True)
    print(f"{c:30}  non-null: {nonnull:,}   unique: {uniq:,}")
    sample = df[c].dropna().astype(str).unique()[:6].tolist()
    print("  sample ->", sample)
    print()

# show head of parsed/clean columns if present
for suffix in ["_parsed","_clean"]:
    matches = [c for c in df.columns if c.endswith(suffix)]
    for c in matches:
        print(f"Head of {c}:")
        print(df[c].head(10).tolist())
        print()
