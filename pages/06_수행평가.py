import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="프로미스나인 인기곡 TOP10",
    page_icon="🎵",
    layout="wide"
)

# 배경 이미지
page_bg = """
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1511379938547-c1f69419868d");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container{
    background-color: rgba(255,255,255,0.88);
    padding: 2rem;
    border-radius: 20px;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

st.title("🎵 프로미스나인 인기곡 TOP10")
st.markdown("### 프로미스나인 대표 인기곡 순위")

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

scores = [100, 96, 93, 90, 88, 85, 82, 78, 75, 72]

df = pd.DataFrame({
    "노래": songs,
    "인기도": scores
})

fig = px.bar(
    df,
    x="인기도",
    y="노래",
    orientation="h",
    text="인기도",
    title="프로미스나인 인기곡 TOP10"
)

fig.update_layout(
    height=650,
    yaxis=dict(categoryorder="total ascending"),
    title_x=0.5,
    font=dict(size=16)
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 TOP 10 순위")

for i, song in enumerate(songs, start=1):
    st.write(f"{i}. {song}")
