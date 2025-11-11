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

st.title("🌍 국가별 MBTI 데이터 시각화")

tab1, tab2 = st.tabs(["📊 국가별 MBTI 비율", "🏆 MBTI 유형별 상위 국가"])

# ------------------------------- #
# 탭 1: 국가 선택 -> MBTI 비율 보기
# ------------------------------- #
with tab1:
    st.subheader("국가별 MBTI 비율 보기")
    selected_country = st.selectbox("국가를 선택하세요:", sorted(df["Country"].unique()))

    country_data = df[df["Country"] == selected_country][mbti_cols].T.reset_index()
    country_data.columns = ["MBTI", "비율"]
    country_data["비율"] = country_data["비율"].astype(float)

    # 1등 타입
    top_mbti = country_data.loc[country_data["비율"].idxmax(), "MBTI"]

    # 색상 설정: 1등 빨강, 나머지 파랑 그라데이션
    colors = [
        "red" if mbti == top_mbti else f"rgba(0,0,255,{0.3 + 0.7 * (val / country_data['비율'].max())})"
        for mbti, val in zip(country_data["MBTI"], country_data["비율"])
    ]

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
        title=f"{selected_country}의 MBTI 분포",
        xaxis_title="MBTI 유형",
        yaxis_title="비율",
        template="plotly_white",
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------- #
# 탭 2: MBTI 선택 -> 상위 국가 보기
# ------------------------------- #
with tab2:
    st.subheader("MBTI 유형별 상위 국가 보기")
    selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_cols)

    sorted_df = df[["Country", selected_mbti]].sort_values(by=selected_mbti, ascending=False)
    top_country = sorted_df.iloc[0]["Country"]

    # 색상 설정: 1등 노랑, 한국 파랑, 나머지 회색
    colors = []
    for c in sorted_df["Country"]:
        if "korea" in c.lower():
            colors.append("blue")
        elif c == top_country:
            colors.append("yellow")
        else:
            colors.append("lightgray")

    fig2 = go.Figure(
        data=[
            go.Bar(
                x=sorted_df["Country"],
                y=sorted_df[selected_mbti],
                marker_color=colors,
                hovertemplate="<b>%{x}</b><br>비율: %{y:.2%}<extra></extra>",
            )
        ]
    )

    fig2.update_layout(
        title=f"{selected_mbti} 유형 비율이 높은 국가 순위",
        xaxis_title="국가",
        yaxis_title="비율",
        template="plotly_white",
        showlegend=False,
    )

    st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
    ---
    **🎨 색상 규칙**
    - 🟥 [탭1] 국가별 MBTI 보기 → 1등: 빨강 / 나머지: 파랑 그라데이션  
    - 🟨 [탭2] MBTI별 국가 순위 → 1등 국가: 노랑 / 한국: 파랑 / 나머지: 회색  
    """
)
