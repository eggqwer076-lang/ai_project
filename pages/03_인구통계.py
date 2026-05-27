import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import platform
import re

# ---------------------------
# 한글 폰트 설정
# ---------------------------
if platform.system() == "Windows":
    rcParams["font.family"] = "Malgun Gothic"
elif platform.system() == "Darwin":
    rcParams["font.family"] = "AppleGothic"
else:
    rcParams["font.family"] = "NanumGothic"

rcParams["axes.unicode_minus"] = False

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    layout="wide"
)

st.title("서울시 연령별 인구 분석")

# ---------------------------
# 데이터 읽기
# ---------------------------
df = pd.read_csv(
    "population.csv",
    encoding="cp949"
)

# 쉼표 제거 후 숫자 변환
for col in df.columns[1:]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 서울특별시 전체 제외
df = df[df["행정구역"] != "서울특별시  (1100000000)"]

# ---------------------------
# 행정구 선택
# ---------------------------
region_names = (
    df["행정구역"]
    .str.replace(r"\s+\(\d+\)", "", regex=True)
    .tolist()
)

selected_region = st.selectbox(
    "행정구 선택",
    region_names
)

row = df[
    df["행정구역"]
    .str.replace(r"\s+\(\d+\)", "", regex=True)
    == selected_region
].iloc[0]

# ---------------------------
# 나이별 데이터 추출
# ---------------------------
ages = []
population = []

for col in df.columns:

    if "총인구수" in col:
        continue

    if "연령구간인구수" in col:
        continue

    m = re.search(r"_(\d+)세$", col)

    if m:
        age = int(m.group(1))

        ages.append(age)
        population.append(row[col])

# 100세 이상 제외
plot_df = pd.DataFrame({
    "나이": ages,
    "인구수": population
}).sort_values("나이")

# ---------------------------
# 그래프
# ---------------------------
fig, ax = plt.subplots(figsize=(15, 7))

ax.plot(
    plot_df["나이"],
    plot_df["인구수"],
    color="hotpink",
    linewidth=3
)

ax.set_title(
    f"{selected_region} 연령별 인구 분포",
    fontsize=18
)

ax.set_xlabel("나이", fontsize=13)
ax.set_ylabel("인구수", fontsize=13)

# 10세 단위 눈금
ax.set_xticks(range(0, 101, 10))

# 세로 구분선
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.6
)

ax.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

st.pyplot(fig)

# 데이터 표시
with st.expander("연령별 데이터 보기"):
    st.dataframe(
        plot_df,
        use_container_width=True
    )
