import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정

st.set_page_config(
page_title="프로미스나인 인기곡 TOP10",
page_icon="🎵",
layout="wide"
)

# 배경 스타일

st.markdown("""

<style>
.stApp{
    background: linear-gradient(
        135deg,
        #ff69b4 0%,
        #ffb6e1 50%,
        #ffffff 100%
    );
}

.block-container{
    background-color: rgba(255,255,255,0.9);
    padding: 2rem;
    border-radius: 20px;
}

h1{
    text-align:center;
    color:#ff1493;
}
</style>

""", unsafe_allow_html=True)

# 제목

st.title("🎵 프로미스나인 인기곡 TOP10")

# 데이터

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

# 세로 막대그래프

fig = px.bar(
df,
x="노래",
y="인기도",
text="인기도",
color_discrete_sequence=["#FF00FF"]
)

fig.update_traces(textposition="outside")

fig.update_layout(
title="프로미스나인 인기곡 TOP10",
title_x=0.5,
height=700,
showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# 순위 표시

st.subheader("🏆 TOP10 순위")

for i, song in enumerate(songs, start=1):
st.write(f"{i}위 - {song}")

# 데이터 보기

with st.expander("데이터 보기"):
st.dataframe(df, use_container_width=True)
