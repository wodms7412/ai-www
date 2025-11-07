import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지 지도", page_icon="🗺️", layout="wide")

st.title("🗺️ 외국인들이 좋아하는 서울의 주요 관광지 TOP 10")

# 관광지 데이터
locations = [
    {"name": "경복궁", "lat": 37.579617, "lon": 126.977041, "desc": "조선의 대표 궁궐"},
    {"name": "명동", "lat": 37.563757, "lon": 126.982690, "desc": "서울의 대표 쇼핑거리"},
    {"name": "남산서울타워", "lat": 37.551169, "lon": 126.988227, "desc": "서울의 전망 명소"},
    {"name": "인사동", "lat": 37.574024, "lon": 126.984911, "desc": "전통 문화 거리"},
    {"name": "홍대", "lat": 37.556332, "lon": 126.922651, "desc": "젊음과 예술의 거리"},
    {"name": "북촌한옥마을", "lat": 37.582604, "lon": 126.983998, "desc": "전통 한옥마을"},
    {"name": "동대문디자인플라자(DDP)", "lat": 37.566295, "lon": 127.009301, "desc": "현대적 건축물과 패션 중심지"},
    {"name": "롯데월드", "lat": 37.511000, "lon": 127.098000, "desc": "서울의 대표 놀이공원"},
    {"name": "청계천", "lat": 37.569002, "lon": 126.978388, "desc": "도심 속 산책길"},
    {"name": "한강공원", "lat": 37.520930, "lon": 126.939230, "desc": "서울의 여가 명소"}
]

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가
for loc in locations:
    folium.Marker(
        [loc["lat"], loc["lon"]],
        popup=f"<b>{loc['name']}</b><br>{loc['desc']}",
        tooltip=loc["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 출력
st_folium(m, width=800, height=600)
