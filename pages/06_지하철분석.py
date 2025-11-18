# Streamlit Subway Analysis App (pages/subway_analysis.py)

이 문서는 `pages/subway_analysis.py`에 그대로 복사해서 사용할 수 있는 **완전한 파이썬 코드 파일 내용**을 담고 있습니다. **(중요)** 파일에 마크다운 코드펜스 ```python
import streamlit as st
import pandas as pd
import plotly.express as px
import os

def load_data():
data_path = os.path.join(os.path.dirname(**file**), "..", "subway.csv")
try:
return pd.read_csv(data_path, encoding="cp949")
except:
return pd.read_csv(data_path, encoding="utf-8")

df = load_data()

df['사용일자'] = df['사용일자'].astype(str)

df_oct = df[df['사용일자'].str.startswith("202510")]

st.title("🚇 2025년 10월 지하철 승하차 데이터 분석")

dates = sorted(df_oct['사용일자'].unique())
selected_date = st.selectbox("날짜 선택", dates)

lines = sorted(df_oct['노선명'].unique())
selected_line = st.selectbox("호선 선택", lines)

filtered = df_oct[(df_oct['사용일자'] == selected_date) & (df_oct['노선명'] == selected_line)]

required_cols = {"승차총승객수", "하차총승객수", "역명"}
if not required_cols.issubset(filtered.columns):
st.error("CSV 파일의 컬럼명이 예상과 다릅니다.")
else:
filtered['총승하차'] = filtered['승차총승객수'] + filtered['하차총승객수']
filtered = filtered.sort_values("총승하차", ascending=False)

```
st.subheader(f"{selected_date} · {selected_line} 승하차 수 TOP 역")

fig = px.bar(
    filtered,
    x="역명",
    y="총승하차",
    color="총승하차",
    color_continuous_scale="Viridis",
    title=f"{selected_date} {selected_line} 승하차 많은 역 순위",
)

fig.update_layout(xaxis_title="역명", yaxis_title="승하차총합")

st.plotly_chart(fig, use_container_width=True)
```

```를 절대 포함하지 마세요).
# - CSV는 repo 루트 또는 pages/의 상위 폴더에 'subway.csv'로 넣어두세요.
# - requirements.txt에 streamlit, pandas, plotly를 추가하고 배포하세요.

# requirements.txt 내용
# streamlit
# pandas
# plotly

```

