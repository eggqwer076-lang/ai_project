import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="프로미스나인 인기곡 TOP10",
    page_icon="🎵",
    layout="wide"
)

# ---------------------------
# 프로미스나인 배경
# fromis9.jpg 파일을 앱 폴더에 업로드
# ---------------------------
page_bg = """
<style>
.stApp {
    background-image: url("fromis9.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    background: rgba(255,255,255,0.92);
    padding: 2rem;
    border-radius: 20px;
}

h1 {
    text-align: center;
    color: hotpink;
}

.rank-box {
    background-color: #fff0f8;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------------------------
# 제목
# ---------------------------
st.title("🎵 프로미스나인 인기곡 TOP10")
st.markdown("---")

# ---------------------------
# 데이터
# ---------------------------
songs = [
    "DM",
    "Supersonic",
    "WE GO",
    "Stay This Way",
    "Love Bomb",
    "Feel Good",
    "Talk & Talk",
    "FUN!",
    "#menow",
    "To Heart"
]

popularity = [100, 96, 93, 90, 88, 85, 82, 78, 75, 72]

df = pd.DataFrame({
    "노래": songs,
    "인기도": popularity
})

# ---------------------------
# 세로 막대그래프 (마젠타색)
# ---------------------------
fig = px.bar(
    df,
    x="노래",
    y="인기도",
    text="인기도",
    color_discrete_sequence=["#FF00FF"]  # 마젠타
)

fig.update_traces(
    textposition="outside",
    marker_line_width=1.5
)

fig.update_layout(
    title={
        "text": "프로미스나인 인기곡 TOP10",
        "x": 0.5
    },
    height=700,
    showlegend=False,
    plot_bgcolor="rgba(255,255,255,0.7)",
    paper_bgcolor="rgba(255,255,255,0)",
    xaxis_title="노래",
    yaxis_title="인기도",
    font=dict(size=16),
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# TOP10 순위 출력
# ---------------------------
st.subheader("🏆 인기곡 순위")

for i, row in enumerate(df.values, start=1):
    st.markdown(
        f"""
        <div class="rank-box">
            <b>{i}위</b> - {row[0]}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# 데이터 보기
# ---------------------------
with st.expander("📊 데이터 보기"):
    st.dataframe(df, use_container_width=True)
