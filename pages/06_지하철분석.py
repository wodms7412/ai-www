# Streamlit Subway Analysis App (pages/subway_analysis.py)

이 문서는 `pages/subway_analysis.py`에 그대로 복사해서 사용할 수 있는 **완전한 파이썬 코드 파일 내용**을 담고 있습니다. **(중요)** 파일에 마크다운 코드펜스 ``` 같은 문법이 들어가면 Streamlit이 파일을 파싱할 때 `SyntaxError`가 발생하므로 **절대 포함하지 마세요**. 아래 텍스트를 그대로 파일에 붙여넣으시면 됩니다.

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# -----------------------------

# 데이터 로드 함수

# -----------------------------

@st.cache_data
def load_data(path):
# 여러 인코딩 자동 시도
for enc in ("cp949", "euc-kr", "utf-8", "utf-8-sig"):
try:
return pd.read_csv(path, encoding=enc)
except Exception:
pass
raise ValueError("CSV 파일 인코딩을 읽을 수 없습니다.")

# -----------------------------

# 경로 설정 (pages/에서 상위의 subway.csv를 찾음)

# -----------------------------

# 기본 경로: pages/의 상위 폴더에 subway.csv가 있어야 함

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(**file**), "..", "subway.csv"))

# Cloud 환경에서 상대경로 문제가 생기면 repo 루트의 subway.csv를 우선 시도

if not os.path.exists(DATA_PATH):
alt = os.path.abspath(os.path.join(os.getcwd(), "subway.csv"))
if os.path.exists(alt):
DATA_PATH = alt

try:
df = load_data(DATA_PATH)
except Exception as e:
st.error(f"데이터 파일을 로드하지 못했습니다: {e}")
st.stop()

# -----------------------------

# 날짜 처리

# -----------------------------

if '사용일자' not in df.columns:
st.error("CSV에 '사용일자' 컬럼이 존재하지 않습니다.")
st.stop()

if df['사용일자'].dtype != 'datetime64[ns]':
df['사용일자'] = df['사용일자'].astype(str)
try:
df['사용일자'] = pd.to_datetime(df['사용일자'], format="%Y%m%d")
except Exception:
df['사용일자'] = pd.to_datetime(df['사용일자'], errors='coerce')

# 2025년 10월 필터링

df_oct = df[(df['사용일자'].dt.year == 2025) & (df['사용일자'].dt.month == 10)].copy()

st.title("🚇 2025년 10월 지하철 승하차 데이터 분석")

if df_oct.empty:
st.error("⚠ CSV에 2025년 10월 데이터가 없습니다!")
st.stop()

# -----------------------------

# UI: 날짜 / 호선 선택

# -----------------------------

dates = sorted(df_oct['사용일자'].dt.date.unique())
selected_date = st.selectbox("날짜 선택", [d.isoformat() for d in dates])
d_selected = pd.to_datetime(selected_date).date()

if '노선명' not in df.columns:
st.error("CSV에 '노선명' 컬럼이 존재하지 않습니다.")
st.stop()

lines = sorted(df_oct['노선명'].dropna().unique())
selected_line = st.selectbox("호선 선택", lines)

# -----------------------------

# 선택 조건으로 필터링

# -----------------------------

filtered = df_oct[(df_oct['사용일자'].dt.date == d_selected) & (df_oct['노선명'] == selected_line)].copy()

if filtered.empty:
st.warning("이 날짜/호선 조합의 데이터가 없습니다.")
st.stop()

# 승하차 합계 계산 및 정렬

filtered['승차총승객수'] = filtered.get('승차총승객수', 0).fillna(0).astype(int)
filtered['하차총승객수'] = filtered.get('하차총승객수', 0).fillna(0).astype(int)
filtered['총승하차'] = filtered['승차총승객수'] + filtered['하차총승객수']
filtered = filtered.sort_values('총승하차', ascending=False).reset_index(drop=True)
filtered['rank'] = filtered.index + 1

st.subheader(f"{selected_date} · {selected_line} 승하차 수 TOP 역")

# -----------------------------

# 막대그래프: 각 막대에 서로 다른 그라데이션 색 적용

# -----------------------------

colorscale = px.colors.sequential.Viridis
if filtered['rank'].max() == filtered['rank'].min():
norm = [0.5 for _ in filtered['rank']]
else:
norm = (filtered['rank'] - filtered['rank'].min()) / (filtered['rank'].max() - filtered['rank'].min())
mapped_colors = [px.colors.sample_colorscale(colorscale, float(v))[0] for v in norm]

fig = go.Figure()
fig.add_trace(go.Bar(
x=filtered['역명'],
y=filtered['총승하차'],
marker=dict(color=mapped_colors),
hovertemplate='<b>%{x}</b><br>총승하차: %{y}<extra></extra>'
))

fig.update_layout(
title=f"{selected_date} {selected_line} 승하차 많은 역 순위",
xaxis_title="역명",
yaxis_title="승하차총합",
template="plotly_white",
margin=dict(l=40, r=20, t=60, b=120),
)
fig.update_xaxes(tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------

# 실행 팁

# -----------------------------

# - pages/subway_analysis.py로 파일을 저장하세요 (파일에 코드펜스 ``` 를 절대 포함하지 마세요).

# - CSV는 repo 루트 또는 pages/의 상위 폴더에 'subway.csv'로 넣어두세요.

# - requirements.txt에 streamlit, pandas, plotly를 추가하고 배포하세요.

# requirements.txt 내용

# streamlit

# pandas

# plotly
