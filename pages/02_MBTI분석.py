import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Countries MBTI Explorer",
    page_icon="🌏",
    layout="wide"
)

st.title("🌏 Countries MBTI Explorer")

@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

country_col = df.columns[0]
mbti_cols = [col for col in df.columns if col != country_col]

tab1, tab2 = st.tabs(
    [
        "🌍 국가별 MBTI",
        "🏆 MBTI 국가 랭킹"
    ]
)

# ----------------------------------
# TAB 1 : 국가 선택
# ----------------------------------

with tab1:

    st.header("국가별 MBTI 분포")

    countries = sorted(df[country_col].unique())

    selected_country = st.selectbox(
        "국가 선택",
        countries,
        key="country_select"
    )

    country_row = df[
        df[country_col] == selected_country
    ].iloc[0]

    mbti_df = pd.DataFrame({
        "MBTI": mbti_cols,
        "Percentage": [
            country_row[col]
            for col in mbti_cols
        ]
    })

    # 높은 순 정렬
    mbti_df = mbti_df.sort_values(
        "Percentage",
        ascending=False
    ).reset_index(drop=True)

    # 색상 생성
    colors = []

    for i in range(len(mbti_df)):

        if i == 0:
            colors.append("#008000")
        else:
            alpha = max(
                0.2,
                1 - (i / len(mbti_df))
            )

            colors.append(
                f"rgba(0,128,0,{alpha})"
            )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=mbti_df["MBTI"],
            y=mbti_df["Percentage"],
            marker_color=colors,
            text=mbti_df["Percentage"].round(2),
            textposition="outside"
        )
    )

    fig.update_layout(
        title=f"{selected_country} MBTI Ranking",
        xaxis_title="MBTI",
        yaxis_title="Percentage (%)",
        template="plotly_white",
        height=650
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("🏆 TOP 3")

    top3 = mbti_df.head(3)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "🥇 1위",
            top3.iloc[0]["MBTI"],
            f"{top3.iloc[0]['Percentage']:.2f}%"
        )

    with c2:
        st.metric(
            "🥈 2위",
            top3.iloc[1]["MBTI"],
            f"{top3.iloc[1]['Percentage']:.2f}%"
        )

    with c3:
        st.metric(
            "🥉 3위",
            top3.iloc[2]["MBTI"],
            f"{top3.iloc[2]['Percentage']:.2f}%"
        )

    st.dataframe(
        mbti_df,
        use_container_width=True,
        hide_index=True
    )

# ----------------------------------
# TAB 2 : MBTI 선택
# ----------------------------------

with tab2:

    st.header("MBTI 유형별 국가 랭킹")

    selected_mbti = st.selectbox(
        "MBTI 선택",
        mbti_cols,
        key="mbti_select"
    )

    ranking_df = df[
        [country_col, selected_mbti]
    ].copy()

    ranking_df.columns = [
        "Country",
        "Percentage"
    ]

    ranking_df = ranking_df.sort_values(
        "Percentage",
        ascending=False
    ).head(10)

    ranking_df = ranking_df.reset_index(
        drop=True
    )

    colors = []

    for i in range(len(ranking_df)):

        if i == 0:
            colors.append("#008000")
        else:
            alpha = max(
                0.2,
                1 - (i / len(ranking_df))
            )

            colors.append(
                f"rgba(0,128,0,{alpha})"
            )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=ranking_df["Country"],
            y=ranking_df["Percentage"],
            marker_color=colors,
            text=ranking_df["Percentage"].round(2),
            textposition="outside"
        )
    )

    fig.update_layout(
        title=f"Top 10 Countries for {selected_mbti}",
        xaxis_title="Country",
        yaxis_title="Percentage (%)",
        template="plotly_white",
        height=650
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        f"🏆 {selected_mbti} TOP 10 국가"
    )

    ranking_show = ranking_df.copy()

    ranking_show.insert(
        0,
        "Rank",
        range(1, len(ranking_show)+1)
    )

    st.dataframe(
        ranking_show,
        use_container_width=True,
        hide_index=True
    )
