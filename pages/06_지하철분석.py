# Streamlit Subway Analysis App (pages/subway_analysis.py)

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load data (CSV is in parent folder)
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "subway.csv")
df = pd.read_csv(DATA_PATH, encoding="cp949")

# Filter for October 2025
# 사용일자 형식이 YYYYMMDD 정수라고 가정
# 날짜 컬럼을 문자열로 변환 후 필터링
df['사용일자'] = df['사용일자'].astype(str)
df_oct = df[df['사용일자'].str.startswith("202510")]

# UI
st.title("🚇 2025년 10월 지하철 승하차 데이터 분석")

# 날짜 선택
dates = sorted(df_oct['사용일자'].unique())
selected_date = st.selectbox("날짜 선택", dates)

# 호선 선택
lines = sorted(df_oct['노선명'].unique())
selected_line = st.selectbox("호선 선택", lines)

# Filtered df
filtered = df_oct[(df_oct['사용일자'] == selected_date) & (df_oct['노선명'] == selected_line)]

# 승하차 총합 계산
filtered['총승하차'] = filtered['승차총승객수'] + filtered['하차총승객수']
filtered = filtered.sort_values("총승하차", ascending=False)

st.subheader(f"{selected_date} · {selected_line} 승하차 수 TOP 역")

# Gradient coloring
# 색상이 모두 다른 그라데이션: 역 순위에 따라 컬러 스케일 적용
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

---

# requirements.txt

```
streamlit
pandas
plotly
```
