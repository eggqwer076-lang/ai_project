import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Countries MBTI Explorer",
    page_icon="🌏",
    layout="wide"
)

st.title("🌏 Countries MBTI Distribution")
st.markdown("국가를 선택하면 MBTI 비율을 확인할 수 있습니다.")

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 국가 컬럼 찾기
country_col = df.columns[0]

countries = sorted(df[country_col].unique())

selected_country = st.selectbox(
    "국가 선택",
    countries
)

country_data = df[df[country_col] == selected_country].iloc[0]

mbti_cols = [col for col in df.columns if col != country_col]

mbti_df = pd.DataFrame({
    "MBTI": mbti_cols,
    "Percentage": [country_data[col] for col in mbti_cols]
})

# 내림차순 정렬
mbti_df = mbti_df.sort_values(
    "Percentage",
    ascending=False
).reset_index(drop=True)

# 색상 생성
max_idx = 0

n = len(mbti_df)

colors = []

for i in range(n):
    if i == max_idx:
        colors.append("#FFD700")  # 1등 노란색
    else:
        alpha = max(0.25, 1 - (i / n))

        colors.append(
            f"rgba(135,206,250,{alpha})"
        )

# 그래프
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
    title=f"{selected_country} MBTI Distribution",
    xaxis_title="MBTI Type",
    yaxis_title="Percentage (%)",
    height=650,
    showlegend=False,
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Top 3 표시
st.subheader("🏆 Top 3 MBTI")

top3 = mbti_df.head(3)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🥇 1위",
        top3.iloc[0]["MBTI"],
        f"{top3.iloc[0]['Percentage']:.2f}%"
    )

with col2:
    st.metric(
        "🥈 2위",
        top3.iloc[1]["MBTI"],
        f"{top3.iloc[1]['Percentage']:.2f}%"
    )

with col3:
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
