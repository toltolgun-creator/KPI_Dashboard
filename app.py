"""
KPI Dashboard - 메인 앱
신발원단섬유 (150명) KPI 성과 대시보드
"""

import streamlit as st
from utils.data_loader import load_all_data
from pages import kpi_view, org_view, trend_view

# 페이지 설정
st.set_page_config(
    page_title="KPI Dashboard",
    page_icon="📈",
    layout="wide",
)

# ──────────────────────────────────────────
# 커스텀 CSS (짙은 파란색 테마)
# ──────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');

    /* 전체 배경 & 폰트 */
    .stApp {
        background-color: #F0F4FF;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 사이드바 배경 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E0E8F9 0%, #F0F4FF 100%);
    }

    /* ── 탭 스타일 ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #E0E8F9;
        padding: 8px 12px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 10px;
        font-family: 'Noto Sans KR', sans-serif;
        font-weight: 700;
        font-size: 15px;
        color: #1E3A8A;
        background-color: transparent;
        border: none;
        padding: 0 20px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 71, 171, 0.12);
        color: #0047AB;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0047AB !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(0, 71, 171, 0.4);
    }
    /* 탭 하단 인디케이터 숨기기 */
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* ── 카드 스타일 (info 박스) ── */
    .stAlert {
        background-color: #FFFFFF;
        border: 1px solid #C7D2F0;
        border-left: 5px solid #0047AB;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.1);
        font-family: 'Noto Sans KR', sans-serif;
        transition: all 0.3s ease;
    }
    .stAlert:hover {
        box-shadow: 0 4px 16px rgba(30, 58, 138, 0.22);
        transform: translateY(-2px);
    }

    /* ── 스피너 색상 ── */
    .stSpinner > div {
        border-top-color: #0047AB !important;
    }

    /* ── 헤더 영역 ── */
    header[data-testid="stHeader"] {
        background-color: #F0F4FF;
    }

    /* ── 버튼 스타일 ── */
    .stButton > button {
        background-color: #0047AB;
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Noto Sans KR', sans-serif;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0066CC;
        box-shadow: 0 4px 14px rgba(0, 71, 171, 0.4);
        transform: translateY(-1px);
    }

    /* ── 메트릭 카드 ── */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E8F9;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.08);
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 4px 16px rgba(30, 58, 138, 0.18);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Noto Sans KR', sans-serif;
        font-weight: 700;
        color: #1E3A8A;
    }
    [data-testid="stMetricValue"] {
        color: #0047AB;
        font-weight: 900;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────
# 커스텀 헤더
# ──────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 30px 0 10px 0;
">
    <div style="font-size: 60px; margin-bottom: 8px;">📈</div>
    <h1 style="
        font-family: 'Noto Sans KR', sans-serif;
        font-weight: 900;
        font-size: 42px;
        color: #0047AB;
        margin: 0;
        letter-spacing: -1px;
    ">KPI Dashboard</h1>
    <p style="
        font-family: 'Noto Sans KR', sans-serif;
        font-weight: 700;
        font-size: 18px;
        color: #1E3A8A;
        margin: 12px 0 0 0;
        letter-spacing: 1px;
    ">열정적인 성과추진으로 비전 달성!</p>
</div>
<hr style="border: none; height: 3px; background: linear-gradient(90deg, #3B82F6, #0047AB, #1E3A8A); border-radius: 2px; margin: 10px 0 25px 0;">
""", unsafe_allow_html=True)

# ──────────────────────────────────────────
# 데이터 로드 (캐싱)
# ──────────────────────────────────────────
@st.cache_data(ttl=300)
def get_data():
    return load_all_data()

with st.spinner("데이터 로딩 중..."):
    data = get_data()

# ──────────────────────────────────────────
# 3개 탭
# ──────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📋 KPI 추진현황", "📈 월별 KPI 추이", "🏢 조직도"])

with tab1:
    kpi_view.render(data)

with tab2:
    trend_view.render(data)

with tab3:
    org_view.render(data)
