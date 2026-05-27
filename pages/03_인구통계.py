import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
import platform

# -----------------------------
# 한글 폰트 설정
# -----------------------------
if platform.system() == "Windows":
    rcParams["font.family"] = "Malgun Gothic"
elif platform.system() == "Darwin":
    rcParams["font.family"] = "AppleGothic"
else:
    # Streamlit Cloud(Linux)
    rcParams["font.family"] = "NanumGothic"

rcParams["axes.unicode_minus"] = False

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="서울시 연령별 인구 분석",
    layout="wide"
)

st.title("서울시 연령별 인구 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
uploaded_file = st.file_uploader(
    "population.csv 파일을 업로드하세요",
    type=["csv"]
)

if uploaded_file is not None:

    # 인코딩 자동 처리
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
    except:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file, encoding="cp949")

    st.success("데이터 로드 완료")

    # 첫 번째 열: 행정구
    region_col = df.columns[0]

    # 두 번째 열: 총인구
    total_col = df.columns[1]

    # 나이 컬럼 추출
    age_cols = df.columns[2:]

    # 서울시 전체 제외
    region_df = df[df[region_col] != "서울특별시"]

    region_list = sorted(region_df[region_col].unique())

    selected_region = st.selectbox(
        "행정구 선택",
        region_list
    )

    selected_row = region_df[
        region_df[region_col] == selected_region
    ].iloc[0]

    ages = []
    populations = []

    for col in age_cols:

        age_text = str(col)

        # 숫자만 추출
        digits = "".join(
            ch for ch in age_text if ch.isdigit()
        )

        if digits:
            ages.append(int(digits))
            populations.append(selected_row[col])

    chart_df = pd.DataFrame({
        "나이": ages,
        "인구수": populations
    }).sort_values("나이")

    # -----------------------------
    # 그래프
    # -----------------------------
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(
        chart_df["나이"],
        chart_df["인구수"],
        color="hotpink",
        linewidth=3
    )

    ax.set_title(
        f"{selected_region} 연령별 인구 분포",
        fontsize=16
    )

    ax.set_xlabel("나이")
    ax.set_ylabel("인구수")

    # 10세 단위 구분선
    max_age = chart_df["나이"].max()

    ax.set_xticks(
        range(0, int(max_age) + 10, 10)
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.5
    )

    ax.grid(
        axis="y",
        alpha=0.3
    )

    st.pyplot(fig)

    # 데이터 보기
    with st.expander("연령별 데이터 보기"):
        st.dataframe(
            chart_df,
            use_container_width=True
        )
