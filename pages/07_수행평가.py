import streamlit as st
import pandas as pd
import altair as alt

# 1. 📋 음식 재료 목록 정의
# 사용자가 선택할 10가지 음식 재료
AVAILABLE_INGREDIENTS = [
    "쌀", "밀가루", "감자", "토마토", "양파",
    "마늘", "소고기", "돼지고기", "닭고기", "콩"
]

# 2. 🌍 가상 데이터 생성 (실제 데이터 대신 임의의 사용 빈도 데이터)
# 재료별로 어떤 나라에서 많이 사용되는지 가정한 데이터
def generate_mock_data(selected_ingredient):
    # 가상의 국가 목록
    countries = [
        "중국", "인도", "미국", "러시아", "브라질",
        "멕시코", "이탈리아", "프랑스", "한국", "일본",
        "독일", "태국", "베트남", "나이지리아", "영국"
    ]
    
    # 선택된 재료에 따라 특정 국가의 사용 빈도를 높게 설정
    if selected_ingredient == "쌀":
        high_usage_countries = ["중국", "인도", "일본", "한국", "태국", "베트남"]
    elif selected_ingredient == "밀가루":
        high_usage_countries = ["러시아", "미국", "이탈리아", "프랑스", "독일"]
    elif selected_ingredient == "소고기":
        high_usage_countries = ["브라질", "미국", "아르헨티나", "호주", "인도(종교적 이유 제외)"] # 예시
    elif selected_ingredient == "토마토":
        high_usage_countries = ["이탈리아", "멕시코", "스페인", "미국"]
    else: # 나머지 재료는 임의로 설정
        high_usage_countries = countries[:5]
    
    # 국가별 사용 빈도 (가상의 숫자) 생성
    data = []
    import random
    random.seed(42) # 일관된 결과를 위해 시드 설정
    
    for country in countries:
        # 주요 사용 국가에는 높은 빈도수를 부여
        usage = random.randint(10, 50)
        if country in high_usage_countries:
            usage += random.randint(50, 100)
            
        data.append({
            "국가": country,
            "사용_빈도": usage,
            "음식_재료": selected_ingredient
        })
        
    df = pd.DataFrame(data)
    
    # 사용 빈도가 높은 상위 10개 국가만 선택
    top_10_df = df.nlargest(10, '사용_빈도')
    return top_10_df

# 3. 🖼️ Streamlit 애플리케이션 정의
def main():
    st.set_page_config(
        page_title="음식 재료 사용 국가 Top 10 시각화",
        layout="wide"
    )

    st.title("🍚 음식 재료별 주요 사용 국가 Top 10 분석")
    st.markdown("---")

    # 4. 🖱️ 사이드바에서 사용자 입력 받기
    st.sidebar.header("재료 선택")
    
    # selectbox를 사용하여 사용자가 재료 10가지 중 하나를 선택하도록 함
    selected_ingredient = st.sidebar.selectbox(
        "분석할 음식 재료를 선택하세요:",
        AVAILABLE_INGREDIENTS
    )

    # 5. 📊 데이터 생성 및 시각화
    if selected_ingredient:
        st.subheader(f"선택된 재료: **{selected_ingredient}**")
        st.write(f"**{selected_ingredient}**을(를) 가장 많이 사용하는 상위 10개 국가입니다. (가상 데이터 기반)")
        
        # 가상 데이터 가져오기
        data_df = generate_mock_data(selected_ingredient)
        
        # Altair를 사용한 막대 그래프 생성
        chart = alt.Chart(data_df).mark_bar().encode(
            # X축: 국가 (정렬 기준: 사용 빈도 내림차순)
            x=alt.X('국가', sort='-y', axis=alt.Axis(labelAngle=0)),
            # Y축: 사용 빈도 (재료별 가중치)
            y=alt.Y('사용_빈도', title=f'{selected_ingredient} 사용 빈도 (가상)'),
            # 색상: 국가
            color=alt.Color('국가', legend=None),
            # 툴팁: 마우스를 올렸을 때 국가와 빈도 표시
            tooltip=['국가', '사용_빈도']
        ).properties(
            title=f'{selected_ingredient}의 상위 10개 사용 국가'
        ).interactive() # 줌/패닝 가능하도록 설정
        
        # Streamlit에 그래프 표시
        st.altair_chart(chart, use_container_width=True)
        
        st.markdown("---")
        st.caption("참고: 이 데이터는 **예시를 위해 임의로 생성된 가상의 데이터**이며, 실제 국가별 사용량과는 다를 수 있습니다.")


if __name__ == "__main__":
    main()
