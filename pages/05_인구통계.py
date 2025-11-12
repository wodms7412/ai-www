import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="서울시 연령별 인구 그래프", layout="wide")

st.title("📊 서울시 행정구별 연령별 인구 시각화")
st.write("CSV 파일(`population.csv`)을 업로드하거나 기본 데이터를 사용하세요.")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

# 데이터 불러오기
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    st.warning("⚠️ CSV 파일을 업로드해주세요. (예: population.csv)")
    st.stop()

# 기본 전처리
df.columns = df.columns.str.strip()

# 행정구 이름 정리 (코드 제거)
df["행정구역명"] = df["행정구역"].str.replace(r"\s*\(.*\)", "", regex=True)

# 연령 관련 열만 추출 (0세~100세 이상)
age_cols = [c for c in df.columns if "거주자_" in c and "남" not in c and "여" not in c]
age_cols = [c for c in age_cols if "총인구수" not in c and "연령구간인구수" not in c]

# 연령 추출 함수
def extract_age(col):
    import re
    match = re.search(r"거주자_(\d+)", col)
    if match:
        return int(match.group(1))
    elif "100세 이상" in col:
        return 100
    else:
        return None

age_map = {col: extract_age(col) for col in age_cols if extract_age(col) is not None}

# 숫자형 변환
for col in age_cols:
    df[col] = df[col].astype(str).str.replace(",", "").astype(float)

# 행정구 선택
region = st.selectbox("행정구 선택", df["행정구역명"].unique())

# 선택된 구 데이터
region_data = df[df["행정구역명"] == region].iloc[0]
ages = list(age_map.values())
population = [region_data[col] for col in age_map.keys()]

# 그래프 설정
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#f0f0f0")  # 회색 배경
ax.plot(ages, population, marker="o", color="black", linewidth=2)

ax.set_facecolor("#eaeaea")
ax.set_title(f"{region} 연령별 인구 분포", fontsize=16)
ax.set_xlabel("나이", fontsize=12)
ax.set_ylabel("인구수", fontsize=12)

ax.grid(True, which="both", linestyle="--", alpha=0.5)
ax.set_xticks(range(0, 101, 10))  # 10세 단위
ax.set_yticks(range(0, int(max(population)) + 100, 100))  # 100명 단위

st.pyplot(fig)

st.caption("📈 데이터 출처: 서울특별시 인구통계 (예시용)")
