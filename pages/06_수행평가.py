import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# ----------------------------------
# 페이지 설정
# ----------------------------------
st.set_page_config(
    page_title="프로미스나인 인기곡 TOP10",
    page_icon="🎵",
    layout="wide"
)

# ----------------------------------
# 배경 이미지 함수
# ----------------------------------
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_base64("fromis9_group.jpg")

# ----------------------------------
# CSS
# ----------------------------------
page_bg = f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

.block-container {{
    background: rgba(255,255,255,0.88);
    padding: 2rem;
    border-radius: 25px;
}}

h1 {{
    text-align:center;
    color:#ff1493;
}}

.rank-box {{
    background: rgba(255,240,245,0.95);
    padding:12px;
    margin-bottom:8px;
    border-radius:12px;
    font-size:18px;
}}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ----------------------------------
# 제목
# ----------------------------------
st.title("🎵 프로미스나인 인기곡 TOP10")

st.markdown(
    "<h4 style='text-align:center;'>프로미스나인 대표 인기곡 순위</h4>",
    unsafe_allow_html=True
)

st.markdown("---")

# ----------------------------------
# 데이터
# ----------------------------------
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

# ----------------------------------
# 세로 막대그래프
# ----------------------------------
fig = px.bar(
    df,
    x="노래",
    y="인기도",
    text="인기도",
    color_discrete_sequence=["#FF00FF"]  # 마젠타
)

fig.update_traces(
    textposition="outside",
    marker_line_width=2
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
    font=dict(size=16)
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# TOP10 순위
# ----------------------------------
st.subheader("🏆 인기곡 순위")

for i, song in enumerate(songs, start=1):
    st.markdown(
        f"""
        <div class="rank-box">
        <b>{i}위</b> - {song}
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------
# 데이터 테이블
# ----------------------------------
with st.expander("📊 데이터 보기"):
    st.dataframe(df, use_container_width=True)

# ----------------------------------
# 푸터
# ----------------------------------
st.markdown("---")
st.caption("fromis_9 인기곡 TOP10 시각화")
