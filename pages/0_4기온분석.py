import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")

# 상위 폴더의 CSV 읽기
@st.cache_data
def load_data():
    df = pd.read_csv("../seoul.csv", encoding="cp949")

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


try:
    df = load_data()

except Exception as e:
    st.error(f"CSV 파일을 읽을 수 없습니다.\n\n{e}")
    st.stop()

# -------------------
# 사이드바
# -------------------

st.sidebar.header("날짜 선택")

month = st.sidebar.selectbox(
    "월 선택",
    sorted(df["month"].unique())
)

day_list = sorted(
    df[df["month"] == month]["day"].unique()
)

day = st.sidebar.selectbox(
    "일 선택",
    day_list
)

# -------------------
# 필터링
# -------------------

filtered = df[
    (df["month"] == month) &
    (df["day"] == day)
].copy()

filtered = filtered.sort_values("year")

st.subheader(
    f"📅 {month}월 {day}일의 연도별 최고·최저기온"
)

# -------------------
# 무지개 색상 생성
# -------------------

rainbow_colors = px.colors.sample_colorscale(
    "Rainbow",
    [
        i / (len(filtered) - 1)
        if len(filtered) > 1 else 0
        for i in range(len(filtered))
    ]
)

# -------------------
# 그래프
# -------------------

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
            width=3
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

fig.update_layout(
    height=700,
    hovermode="x unified",
    xaxis_title="연도",
    yaxis_title="기온(℃)",
    legend_title="기온 종류"
)

fig.update_xaxes(
    showgrid=True
)

fig.update_yaxes(
    showgrid=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------
# 통계
# -------------------

col1, col2 = st.columns(2)

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

# -------------------
# 데이터 테이블
# -------------------

st.subheader("원본 데이터")

st.dataframe(
    filtered[
        ["year", "max_temp", "min_temp"]
    ],
    use_container_width=True
)
