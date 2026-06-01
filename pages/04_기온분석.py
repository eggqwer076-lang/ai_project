from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")

# --------------------------------------------------
# 데이터 로드
# --------------------------------------------------

@st.cache_data
def load_data():

    root_dir = Path(__file__).resolve().parent.parent
    csv_path = root_dir / "seoul.csv"

    try:
        df = pd.read_csv(csv_path, encoding="utf-8")
    except:
        try:
            df = pd.read_csv(csv_path, encoding="utf-8-sig")
        except:
            df = pd.read_csv(csv_path, encoding="cp949")

    df = df.iloc[:, :5]

    df.columns = [
        "date",
        "station",
        "avg_temp",
        "min_temp",
        "max_temp"
    ]

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df = df.dropna(subset=["date"])

    for col in ["avg_temp", "min_temp", "max_temp"]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.dropna(
        subset=["min_temp", "max_temp"]
    )

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    return df


df = load_data()

# --------------------------------------------------
# 사이드바
# --------------------------------------------------

st.sidebar.header("날짜 선택")

month = st.sidebar.selectbox(
    "월",
    sorted(df["month"].unique())
)

available_days = sorted(
    df[df["month"] == month]["day"].unique()
)

day = st.sidebar.selectbox(
    "일",
    available_days
)

future_year = st.sidebar.selectbox(
    "예측 연도",
    list(range(2025, 2101))
)

# --------------------------------------------------
# 필터링
# --------------------------------------------------

filtered = df[
    (df["month"] == month) &
    (df["day"] == day)
].copy()

filtered = filtered.sort_values("year")

st.subheader(
    f"📅 {month}월 {day}일 연도별 최고·최저기온"
)

# --------------------------------------------------
# 예측 모델
# --------------------------------------------------

X = filtered[["year"]]

max_model = LinearRegression()
max_model.fit(X, filtered["max_temp"])

min_model = LinearRegression()
min_model.fit(X, filtered["min_temp"])

pred_max = max_model.predict([[future_year]])[0]
pred_min = min_model.predict([[future_year]])[0]

# --------------------------------------------------
# 무지개색
# --------------------------------------------------

if len(filtered) > 1:
    rainbow_colors = px.colors.sample_colorscale(
        "Rainbow",
        [i/(len(filtered)-1) for i in range(len(filtered))]
    )
else:
    rainbow_colors = ["red"]

# --------------------------------------------------
# 그래프
# --------------------------------------------------

fig = go.Figure()

# 최고기온

fig.add_trace(
    go.Scatter(
        x=filtered["year"],
        y=filtered["max_temp"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="red",
            width=4
        ),
        marker=dict(
            size=8,
            color=rainbow_colors
        )
    )
)

# 최저기온

fig.add_trace(
    go.Scatter(
        x=filtered["year"],
        y=filtered["min_temp"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="lightblue",
            width=3
        ),
        marker=dict(
            size=7,
            color="lightblue"
        )
    )
)

# 최고기온 예측점

fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_max],
        mode="markers+text",
        name="최고기온 예측",
        text=[f"{pred_max:.1f}℃"],
        textposition="top center",
        marker=dict(
            size=16,
            symbol="star"
        )
    )
)

# 최저기온 예측점

fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_min],
        mode="markers+text",
        name="최저기온 예측",
        text=[f"{pred_min:.1f}℃"],
        textposition="bottom center",
        marker=dict(
            size=16,
            symbol="diamond"
        )
    )
)

fig.update_layout(
    height=700,
    hovermode="x unified",
    legend_title="범례",
    xaxis_title="연도",
    yaxis_title="기온(℃)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# 예측 결과
# --------------------------------------------------

st.subheader("🔮 미래 기온 예측")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        f"{future_year}년 예상 최고기온",
        f"{pred_max:.1f}℃"
    )

with c2:
    st.metric(
        f"{future_year}년 예상 최저기온",
        f"{pred_min:.1f}℃"
    )

# --------------------------------------------------
# 원본 데이터
# --------------------------------------------------

st.subheader("📋 데이터")

st.dataframe(
    filtered[
        [
            "year",
            "max_temp",
            "min_temp"
        ]
    ],
    use_container_width=True
)
