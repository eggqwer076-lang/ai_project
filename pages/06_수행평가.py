import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

st.set_page_config(
page_title="프로미스나인 인기곡 TOP10",
page_icon="🎵",
layout="wide"
)

def get_base64(file_path):
with open(file_path, "rb") as f:
return base64.b64encode(f.read()).decode()

# 배경 설정

if os.path.exists("fromis9_group.jpg"):
img = get_base64("fromis9_group.jpg")

```
page_bg = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    background: rgba(255,255,255,0.88);
    padding: 2rem;
    border-radius: 20px;
}}
</style>
"""
```

else:
page_bg = """ <style>
.stApp{
background: linear-gradient(
135deg,
#ff69b4 0%,
#ffb6e1 50%,
#ffffff 100%
);
}

```
.block-container{
    background: rgba(255,255,255,0.9);
    padding: 2rem;
    border-radius: 20px;
}
</style>
"""
```

st.markdown(page_bg, unsafe_allow_html=True)

st.title("🎵 프로미스나인 인기곡 TOP10")

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

fig = px.bar(
df,
x="노래",
y="인기도",
text="인기도",
color_discrete_sequence=["#FF00FF"]
)

fig.update_traces(
textposition="outside"
)

fig.update_layout(
height=700,
showlegend=False,
title={
"text":"프로미스나인 인기곡 TOP10",
"x":0.5
},
xaxis_title="노래",
yaxis_title="인기도"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 TOP10")

for i, song in enumerate(songs, start=1):
st.write(f"{i}위 - {song}")

with st.expander("데이터 보기"):
st.dataframe(df, use_container_width=True)
