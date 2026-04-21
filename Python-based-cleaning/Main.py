# main.py
import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Amazon India Analytics", layout="wide", page_icon="🛒")

# ---------- sidebar header / logo ----------
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
logo_path = os.path.join(ASSETS_PATH, "logo.png")

if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.title("Amazon India — Dashboard")

st.sidebar.markdown("---")

# ---------- load cleaned dataset ----------
@st.cache_data(show_spinner=False)
def load_ready(path="data/combined_ready.parquet"):
    return pd.read_parquet(path)

if "df" not in st.session_state:
    try:
        st.session_state.df = load_ready()
    except FileNotFoundError:
        st.error("Cleaned dataset not found. Please run `combine_and_clean.py` and `fix_order_date.py` & `fix_revenue.py` first.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()

st.title("Amazon India — Analytics")
st.write("Using cleaned dataset (`combined_ready.parquet`).")
st.write(f"Rows: **{len(st.session_state.df):,}** | Columns: **{st.session_state.df.shape[1]}**")
