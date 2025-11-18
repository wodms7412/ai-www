# Streamlit Subway Analysis App (pages/subway_analysis.py)

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# -----------------------------
# 1) 데이터 로드
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

# Streamlit Cloud에서도 안전하게 동작하는 경로
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "subway.csv"))

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"데이터 파일을 로드하지 못했습니다: {e}")
    st.stop()

# -----------------------------
# 2) 날짜 처리
# -----------------------------
if df['사용일자'].dtype != 'datetime64[ns]':
```
