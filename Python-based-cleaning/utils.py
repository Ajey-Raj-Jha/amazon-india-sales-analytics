# utils.py
import os
import re
from pathlib import Path

import pandas as pd
import numpy as np
from dateutil import parser
from sqlalchemy import create_engine

# ---------- Basic single-file loader ----------
def load_data_cached(path):
    """Simple CSV loader for a single file path."""
    return pd.read_csv(path, low_memory=False)

# ---------- Cleaning functions ----------
def parse_dates(series, col_name="order_date"):
    def safe_parse(x):
        try:
            if pd.isna(x):
                return pd.NaT
            s = str(x).strip()
            if s.lower() in ["", "nan", "na", "none"]:
                return pd.NaT
            dt = parser.parse(s, dayfirst=True, fuzzy=True)
            return dt.date()
        except Exception:
            return pd.NaT
    return series.apply(safe_parse)

def clean_price(series):
    def to_float(x):
        try:
            if pd.isna(x):
                return np.nan
            s = str(x)
            s = re.sub(r"[^\d\.\-]", "", s)  # keep digits, dot, minus
            if s == "":
                return np.nan
            return float(s)
        except Exception:
            return np.nan
    return series.apply(to_float)

def clean_boolean(series):
    true_set = {"true", "1", "yes", "y", "t", "prime"}
    false_set = {"false", "0", "no", "n", "f", "na", "none"}
    def conv(x):
        if pd.isna(x):
            return np.nan
        s = str(x).strip().lower()
        if s in true_set:
            return True
        if s in false_set:
            return False
        try:
            v = float(s)
            return bool(v)
        except:
            return np.nan
    return series.apply(conv)

def standardize_city(series, mapping=None):
    if mapping is None:
        mapping = {}
    def std(x):
        if pd.isna(x):
            return np.nan
        s = str(x).lower().strip()
        for k, v in mapping.items():
            if k in s:
                return v
        return s.title()
    return series.apply(std)

def clean_delivery_days(series):
    def conv(x):
        if pd.isna(x):
            return np.nan
        s = str(x).lower().strip()
        if any(token in s for token in ["same", "same day"]):
            return 0.0
        m = re.findall(r"(\d+)", s)
        if m:
            nums = list(map(int, m))
            return float(np.mean(nums))
        try:
            return float(s)
        except:
            return np.nan
    out = series.apply(conv)
    out = out.mask(out > 30, np.nan)
    return out

def handle_duplicates(df, subset_cols):
    df["_is_duplicate"] = df.duplicated(subset=subset_cols, keep=False)
    return df

def fix_price_outliers(df, price_col="original_price_inr", z_thresh=4):
    s = df[price_col]
    mean = s.mean()
    std = s.std()
    z = (s - mean) / std
    df.loc[z.abs() > z_thresh, price_col] = np.nan
    return df

# ---------- SQL ----------
def get_sqlite_engine(sqlite_path="sqlite:///amazon_analytics.db"):
    engine = create_engine(sqlite_path, future=True)
    return engine

def df_to_sql(df, table_name, engine, if_exists="replace", index=False):
    df.to_sql(table_name, engine, if_exists=if_exists, index=index)

# ---------- Multi-file loader (robust) ----------
def _try_read_csv(path):
    """Try reading a CSV with multiple encodings and return (df, encoding) or raise."""
    encodings = ["utf-8", "latin1", "cp1252"]
    last_err = None
    for enc in encodings:
        try:
            df = pd.read_csv(path, low_memory=False, encoding=enc)
            return df, enc
        except Exception as e:
            last_err = e
    # last fallback: try engine='python' without low_memory
    try:
        df = pd.read_csv(path, engine="python")
        return df, "python-fallback"
    except Exception as e:
        raise IOError(f"All read attempts failed for {path}. Last error: {last_err} / fallback error: {e}")

def load_all_data(data_folder="data"):
    """
    Combine all CSV files in `data_folder` into a single DataFrame.
    Returns the combined DataFrame. If no readable files found, raises FileNotFoundError.
    """
    data_path = Path(data_folder)
    if not data_path.exists():
        raise FileNotFoundError(f"Data folder not found: {data_folder}")

    # case-insensitive CSV search
    csv_files = sorted([p for p in data_path.iterdir() if p.suffix.lower() == ".csv"])
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_folder}")

    dfs = []
    failed = []
    for p in csv_files:
        try:
            df_part, enc = _try_read_csv(p)
            df_part["source_file"] = p.name
            dfs.append(df_part)
            print(f"Loaded {p.name} ({len(df_part):,} rows) using encoding: {enc}")
        except Exception as e:
            failed.append((p.name, str(e)))
            print(f"⚠️ Could not read {p.name}: {e}")

    if not dfs:
        # nothing readable
        raise FileNotFoundError(f"No CSV files could be read successfully in {data_folder}. Failures: {failed}")

    combined = pd.concat(dfs, ignore_index=True, sort=False)
    print(f"Combined dataframe shape: {combined.shape}")
    return combined
