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

# 관광지 데이터
locations = [
    {
        "name": "경복궁 (Gyeongbokgung Palace)",
        "lat": 37.579617, "lon": 126.977041,
        "desc": "조선의 법궁으로 웅장한 규모와 아름다운 경관을 자랑합니다.<br>"
                "It is the main royal palace of the Jo
