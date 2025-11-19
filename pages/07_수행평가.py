import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("서울 25개 자치구 음식점／식품위생업소 수 비교")

# 데이터 파일 경로 (다운로드 받은 CSV 파일명으로 변경하세요)
csv_file = "Seoul_FoodHygiene_Upsos_2023.csv"  # 예시 파일명

# CSV 읽기 (실제 파일에 맞게 encoding/sep/columns 조정)
df = pd.read_csv(csv_file, encoding='utf-8')

# 컬럼명 예시: '자치구명', '업소수'
# 실제 컬럼명이 다르면 아래 부분을 수정하세요
df = df[['자치구명', '업소수']].dropna()

df = df.rename(columns={'자치구명':'지역', '업소수':'업소수'})

st.subheader("📊 표: 자치구별 업소수")
st.dataframe(df)

st.subheader("📈 막대그래프: 자치구별 업소수")
plt.figure(figsize=(12,8))
plt.bar(df['지역'], df['업소수'], color='skyblue')
plt.xticks(rotation=90)
plt.ylabel("업소수 (건)")
plt.title("서울 25개 자치구의 식품위생업소 수 비교")
st.pyplot(plt)

st.write("※ 데이터 출처: 서울열린데이터광장 ‘서울시 식품위생업 현황(구별)’ 통계. 단, ‘음식점(식품접객업)’만을 분리한 수치가 아닐 수 있으므로 참조용으로 활용하세요.")

