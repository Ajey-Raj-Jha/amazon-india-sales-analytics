# combine_and_clean.py
import os, re
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
OUT_PARQUET = DATA_DIR / "combined.parquet"
OUT_CSV = DATA_DIR / "combined.csv"

def try_read_csv(path):
    encs = ["utf-8", "latin1", "cp1252"]
    last_err = None
    for e in encs:
        try:
            return pd.read_csv(path, encoding=e, low_memory=False), e
        except Exception as err:
            last_err = err
    try:
        return pd.read_csv(path, engine="python"), "python-fallback"
    except Exception as err:
        raise IOError(f"Failed to read {path}: {last_err} / fallback: {err}")

def detect_date_cols(df, sample_n=500):
    candidates=[]
    for c in df.columns:
        s = df[c].dropna().astype(str).head(sample_n)
        if s.empty: continue
        parsed = pd.to_datetime(s, errors="coerce", dayfirst=False)
        rate = parsed.notna().sum()/max(1,len(s))
        if rate > 0.3:
            candidates.append((c, rate))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [c for c,_ in candidates]

def detect_price_cols(df, sample_n=300):
    price_cols=[]
    for c in df.columns:
        ser = df[c].dropna().astype(str).head(sample_n)
        if ser.empty: continue
        digits = ser.str.contains(r"\d").sum()
        rupee = ser.str.contains(r"[\u20b9₹]|Rs\b|INR", case=False, regex=True).sum()
        if pd.api.types.is_numeric_dtype(df[c]) or digits > max(3, 0.6*len(ser)) or rupee>0:
            price_cols.append(c)
    return price_cols

def clean_price_series(s):
    def _c(x):
        try:
            if pd.isna(x): return pd.NA
            sx = str(x).replace("\u20b9","").replace("₹","")
            sx = re.sub(r"[^\d\.\-]", "", sx)
            if sx=="" or sx.lower() in ("nan","none"): return pd.NA
            return float(sx)
        except:
            return pd.NA
    return s.apply(_c)

def find_id_column(df):
    candidates = ["order_id","orderid","transaction_id","transactionid","id","invoice_id","order_no","order_number"]
    for col in df.columns:
        if col.lower() in candidates:
            return col
    return None

def main():
    csvs = sorted([p for p in DATA_DIR.iterdir() if p.suffix.lower()==".csv"])
    if not csvs:
        print("No CSV files in data/.")
        return

    parts=[]; summary=[]
    for p in csvs:
        try:
            dfp, enc = try_read_csv(p)
            dfp["source_file"] = p.name
            parts.append(dfp)
            summary.append((p.name, len(dfp), len(dfp.columns), enc))
            print(f"Loaded {p.name} ({len(dfp):,} rows) encoding={enc}")
        except Exception as e:
            print(f"ERROR reading {p.name}: {e}")

    if not parts:
        print("No files readable. Stop.")
        return

    combined = pd.concat(parts, ignore_index=True, sort=False)
    print(f"\nCombined shape: {combined.shape[0]:,} rows × {combined.shape[1]} cols")

    date_cands = detect_date_cols(combined)
    if date_cands:
        parsed_col = date_cands[0]
        combined[parsed_col + "_parsed"] = pd.to_datetime(combined[parsed_col], errors="coerce", dayfirst=False)
        print(f"Parsed `{parsed_col}` -> `{parsed_col}_parsed` (non-null: {combined[parsed_col + '_parsed'].notna().sum():,})")
    else:
        print("No clear date-like column detected.")

    price_cands = detect_price_cols(combined)
    if price_cands:
        for c in price_cands[:3]:
            nc = c + "_clean"
            combined[nc] = clean_price_series(combined[c])
            print(f"Cleaned `{c}` -> `{nc}` (non-null: {combined[nc].notna().sum():,})")
    else:
        print("No obvious price-like columns found.")

    id_col = find_id_column(combined)
    if id_col:
        before=len(combined)
        combined = combined.drop_duplicates(subset=[id_col])
        after=len(combined)
        print(f"Deduped by `{id_col}`: {before-after:,} removed ({after:,} remain)")
    else:
        before=len(combined)
        combined = combined.drop_duplicates()
        after=len(combined)
        print(f"Dropped exact duplicates: {before-after:,} removed ({after:,} remain)")

    try:
        combined.to_parquet(OUT_PARQUET, index=False)
        print(f"Saved parquet: {OUT_PARQUET}")
    except Exception as e:
        print(f"Could not save parquet: {e}")

    try:
        combined.to_csv(OUT_CSV, index=False)
        print(f"Saved csv: {OUT_CSV}")
    except Exception as e:
        print(f"Could not save csv: {e}")

    print("\nDone.")

if __name__ == '__main__':
    main()
