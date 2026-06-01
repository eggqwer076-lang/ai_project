from pathlib import Path
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    base_dir = Path(__file__).resolve().parent.parent

    csv_path = base_dir / "seoul.csv"

    df = pd.read_csv(csv_path, encoding="cp949")

    df.columns = [
        "date",
        "station",
        "avg_temp",
        "min_temp",
        "max_temp"
    ]

    df["date"] = pd.to_datetime(df["date"])

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    return df
