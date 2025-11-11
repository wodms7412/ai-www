import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="국가별 MBTI 시각화", layout="centered")

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    # 숫자형 변환
    mbti_cols = [c for c in df.columns if c.lower() != "country"]
    df[mbti_cols] = df[mbti_cols].apply(pd.to_numeric, errors="coerce")
    return df, mbti_cols

df, mbti_cols = load_data()

st.title("🌍 국가별 MBTI 비율 시각화")
st.markdown("**국가를 선택하면 해당 국가의 MBTI 비율을 확인할 수 있습니다.**")

# --- 국가 선택 ---
selected_country = st.selectbox("국가를 선택하세요:", sorted(df["Country"].unique()))

# --- 선택한 국가 데이터 ---
country_data = df[df["Country"] == selected_country][mbti_cols].T.reset_index()
country_data.columns = ["MBTI", "비율"]
country_data["비율"] = country_data["비율"].astype(float)

# 1등 타입 찾기
top_mbti = country_data.loc[country_data["비율"].idxmax(), "MBTI"]

# 색상 설정: 1등 빨강, 나머지는 파랑 그라데이션
colors = [
    "red" if mbti == top_mbti else f"rgba(0,0,255,{0.3 + 0.7 * (val / country_data['비율'].max())})"
    for mbti, val in zip(country_data["MBTI"], country_data["비율"])
]

# --- 그래프 ---
fig = go.Figure(
    data=[
        go.Bar(
            x=country_data["MBTI"],
            y=country_data["비율"],
            marker_color=colors,
            hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>",
        )
    ]
)

fig.update_layout(
    title=f"🇨🇦 {selected_country}의 MBTI 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)

# --- 추가 설명 ---
st.markdown(
    """
    **🧠 해석 도움말**  
    - 빨간색 막대는 해당 국가에서 가장 높은 MBTI 유형입니다.  
    - 파란색 막대는 비율에 따라 진해집니다 (높을수록 진한 파랑).  
    - 데이터 출처: `countriesMBTI_16types.csv`
    """
)
