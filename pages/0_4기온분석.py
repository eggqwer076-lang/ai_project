from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")

# ----------------------------
# 데이터 로드
# ----------------------------
@st.cache_data
def load_data():

    # 프로젝트 루트 찾기
    root_dir = Path(__file__).resolve().parent.parent

    csv_path = root_dir / "seoul.csv"

    if not csv_path.exists():
        st.error(f"CSV 파일을 찾을 수 없습니다.\n\n경로: {csv_path}")
        st.stop()

    df = pd.read_csv(csv_path, encoding="cp949")

    # 컬럼명 변경
    df.columns = [
        "date",
        "station",
        "avg_temp",
        "min_temp",
        "max_temp"
    ]

    # 날짜형 변환
    df["date"] = pd.to_datetime(df["date"])

    # 연월일 생성
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    return df


df = load_data()

# ----------------------------
# 월 선택
# ----------------------------
st.sidebar.header("날짜 선택")

month = st.sidebar.selectbox(
    "월 선택",
    sorted(df["month"].unique())
)

available_days = sorted(
    df[df["month"] == month]["day"].unique()
)

day = st.sidebar.selectbox(
    "일 선택",
    available_days
)

# ----------------------------
# 데이터 필터링
# ----------------------------
filtered = df[
    (df["month"] == month) &
    (df["day"] == day)
].copy()

filtered = filtered.sort_values("year")

# ----------------------------
# 제목
# ----------------------------
st.subheader(
    f"📅 {month}월 {day}일의 연도별 최고기온 · 최저기온"
)

# ----------------------------
# 무지개색 생성
# ----------------------------
rainbow_colors = px.colors.sample_colorscale(
    "Rainbow",
    [
        i / (len(filtered) - 1)
        if len(filtered) > 1 else 0
        for i in range(len(filtered))
    ]
)

# ----------------------------
# 그래프
# ----------------------------
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered["year"],
        y=filtered["max_temp"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            width=4,
            color="red"
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
            width=3,
            color="lightblue"
        ),
        marker=dict(
            size=7,
            color="lightblue"
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

fig.update_xaxes(
    showgrid=True,
    tickmode="linear",
    dtick=10
)

fig.update_yaxes(
    showgrid=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------
# 통계
# ----------------------------
st.subheader("📊 요약 통계")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "최고기온 평균",
        f"{filtered['max_temp'].mean():.1f}℃"
    )

with col2:
    st.metric(
        "최저기온 평균",
        f"{filtered['min_temp'].mean():.1f}℃"
    )

with col3:
    st.metric(
        "최고기온 최고값",
        f"{filtered['max_temp'].max():.1f}℃"
    )

with col4:
    st.metric(
        "최저기온 최저값",
        f"{filtered['min_temp'].min():.1f}℃"
    )

# ----------------------------
# 데이터 표
# ----------------------------
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
