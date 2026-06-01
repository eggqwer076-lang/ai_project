import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석")

uploaded_file = st.file_uploader(
    "CSV 파일 업로드",
    type=["csv"]
)

if uploaded_file is not None:

    # 데이터 불러오기
    df = pd.read_csv(uploaded_file, encoding="cp949")

    # 날짜 변환
    date_col = df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])

    # 컬럼명 통일
    df.columns = [
        "date",
        "station",
        "avg_temp",
        "min_temp",
        "max_temp"
    ]

    # 연월일 생성
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day

    st.sidebar.header("조건 선택")

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

    filtered = df[
        (df["month"] == month) &
        (df["day"] == day)
    ].copy()

    filtered = filtered.sort_values("year")

    st.subheader(
        f"📅 {month}월 {day}일의 연도별 최고·최저기온"
    )

    # 무지개색 생성
    rainbow_colors = px.colors.sample_colorscale(
        "Rainbow",
        [i/(len(filtered)-1) if len(filtered) > 1 else 0
         for i in range(len(filtered))]
    )

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
                color="lightblue",
                size=7
            )
        )
    )

    fig.update_layout(
        height=650,
        xaxis_title="연도",
        yaxis_title="기온(℃)",
        hovermode="x unified",
        legend_title="구분"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        filtered[
            ["year", "max_temp", "min_temp"]
        ],
        use_container_width=True
    )

else:
    st.info("CSV 파일을 업로드해주세요.")
