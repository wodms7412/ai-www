import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="국가별 MBTI 시각화", layout="centered")

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    mbti_cols = [c for c in df.columns if c.lower() != "country"]
    df[mbti_cols] = df[mbti_cols].apply(pd.to_numeric, errors="coerce")
    return df, mbti_cols

df, mbti_cols = load_data()

st.title("🌍 MBTI 유형별 상위 국가 시각화")

# --- MBTI 선택 ---
selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_cols)

# --- 선택된 MBTI에 대한 국가별 데이터 ---
sorted_df = df[["Country", selected_mbti]].sort_values(by=selected_mbti, ascending=False).reset_index(drop=True)

# 상위 10개국 추출
top10 = sorted_df.head(10).copy()

# "South Korea" 또는 "Korea" 포함된 행 찾기
korea_row = sorted_df[sorted_df["Country"].str.lower().str.contains("korea", na=False)]

# 만약 Korea가 top10 안에 없으면 추가
if not korea_row.empty:
    if korea_row["Country"].iloc[0] not in top10["Country"].values:
        top10 = pd.concat([top10, korea_row.iloc[[0]]], ignore_index=True)
else:
    # South Korea가 데이터에 없을 경우 예외 처리
    st.warning("⚠️ 데이터에 'South Korea'가 존재하지 않습니다. CSV 파일을 확인해주세요.")

# 색상 설정
colors = []
top_country = top10.iloc[0]["Country"]

for c in top10["Country"]:
    if "korea" in c.lower():
        colors.append("blue")        # 한국: 파란색
    elif c == top_country:
        colors.append("yellow")      # 1등: 노랑색
    else:
        colors.append("lightgray")   # 나머지: 회색

# --- 그래프 ---
fig = go.Figure(
    data=[
        go.Bar(
            x=top10["Country"],
            y=top10[selected_mbti],
            marker_color=colors,
            hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>",
        )
    ]
)

fig.update_layout(
    title=f"🏆 {selected_mbti} 유형 비율이 높은 국가 Top 10",
    xaxis_title="국가",
    yaxis_title="비율",
    template="plotly_white",
    showlegend=False,
)

st.plotly_chart(fig, use_container_width=True)

# --- 설명 ---
st.markdown(
    """
    ---
    **🎨 색상 규칙**
    - 🟨 1등 국가 → 노랑  
    - 🔵 South Korea → 파랑 (Top10에 없을 시 자동 추가)  
    - ⚪ 나머지 국가 → 회색  
    """
)
