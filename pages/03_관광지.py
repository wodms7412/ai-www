import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.features import DivIcon

st.set_page_config(page_title="서울 관광지도", page_icon="🗺️", layout="wide")

st.title("🗺️ 외국인들이 좋아하는 서울의 주요 관광지 TOP 10")

st.markdown("""
서울에는 전통과 현대가 공존하는 아름다운 명소들이 많습니다.  
아래 지도는 외국인들이 특히 많이 찾는 **서울의 대표 관광지 10곳**을 보여줍니다.  
마커를 클릭하면 각 명소의 설명을 확인할 수 있습니다. 🌸
""")

# 관광지 데이터 (한글 + 영어 설명)
locations = [
    {
        "name": "경복궁 (Gyeongbokgung Palace)",
        "lat": 37.579617, "lon": 126.977041,
        "desc": ("조선의 법궁으로 웅장한 규모와 아름다운 경관을 자랑합니다.<br>"
                 "It is the main royal palace of the Joseon dynasty and a symbol of Korean history.")
    },
    {
        "name": "명동 (Myeongdong)",
        "lat": 37.563757, "lon": 126.982690,
        "desc": ("서울의 대표적인 쇼핑 거리로 외국인 관광객이 가장 많이 방문합니다.<br>"
                 "The most famous shopping district in Seoul, popular with tourists.")
    },
    {
        "name": "남산서울타워 (Namsan Seoul Tower)",
        "lat": 37.551169, "lon": 126.988227,
        "desc": ("서울의 중심에서 전망을 감상할 수 있는 명소입니다.<br>"
                 "A landmark tower offering panoramic views of Seoul.")
    },
    {
        "name": "인사동 (Insadong)",
        "lat": 37.574024, "lon": 126.984911,
        "desc": ("전통 문화와 예술이 공존하는 거리입니다.<br>"
                 "A vibrant street showcasing Korean traditional culture and art.")
    },
    {
        "name": "홍대 (Hongdae)",
        "lat": 37.556332, "lon": 126.922651,
        "desc": ("젊은 예술가와 음악, 자유로운 분위기의 거리입니다.<br>"
                 "Trendy district known for youth culture, art, and nightlife.")
    },
    {
        "name": "북촌한옥마을 (Bukchon Hanok Village)",
        "lat": 37.582604, "lon": 126.983998,
        "desc": ("전통 한옥이 잘 보존된 마을로 사진 명소로 유명합니다.<br>"
                 "A picturesque village of traditional Korean houses (hanok).")
    },
    {
        "name": "동대문디자인플라자 (DDP)",
        "lat": 37.566295, "lon": 127.009301,
        "desc": ("현대적인 건축물과 패션 중심지로 유명합니다.<br>"
                 "A futuristic landmark for design, fashion, and exhibitions.")
    },
    {
        "name": "롯데월드 (Lotte World)",
        "lat": 37.511000, "lon": 127.098000,
        "desc": ("실내외 테마파크로 가족 여행객에게 인기입니다.<br>"
                 "One of the world's largest indoor theme parks.")
    },
    {
        "name": "청계천 (Cheonggyecheon Stream)",
        "lat": 37.569002, "lon": 126.978388,
        "desc": ("도심 속 휴식 공간으로 산책과 야경 명소입니다.<br>"
                 "A peaceful urban stream with walking paths and night lights.")
    },
    {
        "name": "한강공원 (Hangang Park)",
        "lat": 37.520930, "lon": 126.939230,
        "desc": ("서울의 여가 명소로 피크닉과 자전거를 즐길 수 있습니다.<br>"
                 "A riverside park perfect for cycling, picnics, and relaxation.")
    },
]

# 지도 생성 (더 깔끔한 배경)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles="CartoDB positron")

# 마커 추가 (더 잘 보이도록 Circle + Marker + 텍스트 라벨)
for loc in locations:
    popup_html = f"<div style='min-width:200px'><b>{loc['name']}</b><br>{loc['desc']}</div>"
    # 원형 마커로 시인성 향상
    folium.CircleMarker(
        location=[loc["lat"], loc["lon"]],
        radius=9,
        color="#D43030",
        fill=True,
        fill_color="#D43030",
        fill_opacity=0.9,
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(m)

    # 아이콘 마커(클릭/툴팁용)
    folium.Marker(
        location=[loc["lat"], loc]()
