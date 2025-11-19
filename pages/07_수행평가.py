import streamlit as st
import pandas as pd

# 1. 📋 음식 재료 및 가상 데이터 설정
INGREDIENTS = [
    "마늘 (Garlic)", "토마토 (Tomato)", "쌀 (Rice)", "고추 (Chili)",
    "파스타 (Pasta)", "감자 (Potato)", "코코넛 (Coconut)", "콩 (Bean)",
    "카레 (Curry Powder)", "양파 (Onion)"
]

# 가상의 사용량 데이터 (실제 통계가 아닌 데모용 데이터)
data = {
    'Ingredient': ['마늘', '토마토', '쌀', '고추', '파스타', '감자', '코코넛', '콩', '카레', '양파'],
    'Country_1': ['한국', '이탈리아', '중국', '멕시코', '이탈리아', '페루', '태국', '브라질', '인도', '프랑스'],
    'Usage_1': [80, 75, 90, 85, 95, 70, 88, 77, 92, 65],
    'Country_2': ['스페인', '그리스', '인도', '태국', '미국', '러시아', '인도네시아', '멕시코', '영국', '독일'],
    'Usage_2': [60, 50, 70, 65, 55, 60, 68, 55, 50, 40],
}
df_base = pd.DataFrame(data)

# 국가별 추천 음식 데이터
FOOD_RECOMMENDATIONS = {
    '한국': ['김치찌개', '비빔밥', '불고기'],
    '이탈리아': ['피자 마르게리타', '라자냐', '티라미수'],
    '중국': ['마파두부', '베이징 덕', '딤섬'],
    '멕시코': ['타코', '엔칠라다', '퀘사디아'],
    '페루': ['세비체', '로모 살타도', '아히 데 가이나'],
    '태국': ['팟타이', '똠얌꿍', '그린 커리'],
    '인도': ['탄두리 치킨', '난 (Naan)', '사모사'],
    '스페인': ['파에야', '타파스', '가스파초'],
    '브라질': ['페이조아다', '슈하스코', '파스텔'],
    '프랑스': ['크루아상', '라타투이', '에스카르고'],
}


# --- Streamlit 앱 메인 함수 ---
def main():
    st.set_page_config(page_title="음식 재료 분석기", layout="wide")
    st.title("🍜 음식 재료별 국가 사용량 분석기")
    st.markdown("---")

    # 2. 🎈 재료 선택 (사이드바)
    st.sidebar.header("재료를 선택하세요")
    selected_ingredient = st.sidebar.selectbox(
        '어떤 재료에 대해 알아보고 싶으신가요?',
        INGREDIENTS
    )

    # 재료 이름만 추출
    ingredient_name = selected_ingredient.split(' ')[0]

    st.header(f"선택된 재료: **{selected_ingredient}**")
    st.markdown("---")

    # 3. 📈 그래프 및 음식 추천 로직
    try:
        selected_row = df_base[df_base['Ingredient'] == ingredient_name].iloc[0]

        # --- 재료 사용량 그래프 생성 ---
        chart_data = pd.DataFrame({
            'Country': [selected_row['Country_1'], selected_row['Country_2']],
            'Usage': [selected_row['Usage_1'], selected_row['Usage_2']],
        }).set_index('Country')

        st.subheader(f"📊 {selected_ingredient}을(를) 많이 쓰는 국가 Top 2 (가상 데이터)")
        # Streamlit 내장 차트 사용
        st.bar_chart(chart_data)

        st.markdown("---")

        # --- 추천 음식 표시 ---
        # 가장 사용량이 높은 국가 (Country_1)
        selected_country = selected_row['Country_1']

        st.subheader(f"🍽️ 재료를 가장 많이 쓰는 국가, **{selected_country}**의 추천 음식 3가지")
        
        if selected_country in FOOD_RECOMMENDATIONS:
            foods = FOOD_RECOMMENDATIONS[selected_country]
            
            # 컬럼을 사용하여 정리된 형태로 표시
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"🥇 1. **{foods[0]}**")
            with col2:
                st.info(f"🥈 2. **{foods[1]}**")
            with col3:
                st.info(f"🥉 3. **{foods[2]}**")
                
        else:
            st.warning(f"죄송합니다, {selected_country}에 대한 추천 음식 정보가 부족합니다.")

    except IndexError:
        st.error(f"데이터베이스에 **{ingredient_name}** 재료 정보가 없습니다. 관리자에게 문의하세요.")
        
    st.markdown("---")
    st.caption("🚨 이 앱의 데이터(사용량, 추천 음식)는 **데모를 위한 가상의 정보**입니다.")

if __name__ == "__main__":
    main()
