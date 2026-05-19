import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 인기 관광지 TOP10",
    layout="wide"
)

st.title("🇰🇷 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("폴리움(Folium) 지도로 서울 주요 관광지를 표시합니다.")

# 관광지 데이터
places = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "desc": "조선 왕조의 대표 궁궐"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "desc": "전통 한옥 거리"
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "desc": "쇼핑과 길거리 음식 명소"
    },
    {
        "name": "남산서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "desc": "서울 야경 명소"
    },
    {
        "name": "홍대거리",
        "lat": 37.556350,
        "lon": 126.922672,
        "desc": "젊은 문화와 공연의 중심지"
    },
    {
        "name": "인사동",
        "lat": 37.574187,
        "lon": 126.985417,
        "desc": "전통 문화와 기념품 거리"
    },
    {
        "name": "롯데월드타워",
        "lat": 37.512500,
        "lon": 127.102778,
        "desc": "서울 랜드마크 초고층 빌딩"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.566526,
        "lon": 127.009224,
        "desc": "현대적 건축과 패션 중심지"
    },
    {
        "name": "광장시장",
        "lat": 37.570435,
        "lon": 126.999603,
        "desc": "한국 전통 먹거리 시장"
    },
    {
        "name": "한강공원",
        "lat": 37.520694,
        "lon": 126.939186,
        "desc": "서울 시민과 관광객의 휴식 공간"
    }
]

# 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="OpenStreetMap"
)

# 마커 추가
for idx, place in enumerate(places, start=1):
    popup_html = f"""
    <b>TOP {idx}. {place['name']}</b><br>
    {place['desc']}
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=popup_html,
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

# 지도 출력
st_folium(m, width=1200, height=700)

# 관광지 리스트 출력
st.subheader("📍 관광지 리스트")

for idx, place in enumerate(places, start=1):
    st.write(f"{idx}. {place['name']} - {place['desc']}")
