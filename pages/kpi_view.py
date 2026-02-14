"""
Phase 3: KPI 추진현황 탭
- 드롭다운 없이 전체 조직을 계층별로 나열
- 각 조직마다: 조직명 헤더 + KPI 카드 + AI 해석
- Level 1 → Level 2 → Level 3 순서
"""

import streamlit as st
import pandas as pd
from pages.llm_briefing import analyze_org_kpis


# 평가등급별 색상
GRADE_COLORS = {
    "S": {"bg": "#059669", "text": "#FFFFFF"},
    "A": {"bg": "#10B981", "text": "#FFFFFF"},
    "B": {"bg": "#3B82F6", "text": "#FFFFFF"},
    "C": {"bg": "#F59E0B", "text": "#FFFFFF"},
    "D": {"bg": "#EF4444", "text": "#FFFFFF"},
}


def _get_latest_month(monthly_df: pd.DataFrame) -> int:
    """데이터에서 가장 최근 월 반환"""
    return int(monthly_df["월"].max())


def _render_kpi_card(row: pd.Series):
    """KPI 카드 1개를 HTML로 렌더링"""
    kpi_name = row["KPI명"]
    grade = str(row["YTD평가결과"]).strip()
    ytd_rate = str(row["YTD달성률"]).strip()
    target = row["월목표"]
    actual = row["월실적"]
    kpi_type = row["KPI유형"]

    color = GRADE_COLORS.get(grade, {"bg": "#9CA3AF", "text": "#FFFFFF"})

    card_html = f"""<div style="background:#FFFFFF; border-radius:14px; box-shadow:0 2px 12px rgba(30,58,138,0.10); overflow:hidden; border:1px solid #E0E8F9; height:100%;">
<div style="background:{color['bg']}; padding:14px 18px; display:flex; justify-content:space-between; align-items:center;">
<span style="color:{color['text']}; font-weight:900; font-size:15px; font-family:'Noto Sans KR',sans-serif;">{kpi_name}</span>
<span style="background:rgba(255,255,255,0.25); color:{color['text']}; font-weight:900; font-size:14px; padding:3px 12px; border-radius:20px;">{grade}등급</span>
</div>
<div style="padding:18px;">
<div style="text-align:center; margin-bottom:16px;">
<div style="font-size:13px; color:#6B7280; font-weight:700; margin-bottom:4px;">YTD 달성률</div>
<div style="font-size:36px; font-weight:900; color:{color['bg']}; line-height:1.1;">{ytd_rate}</div>
</div>
<hr style="border:none; height:1px; background:#E5E7EB; margin:0 0 14px 0;">
<div style="display:flex; justify-content:space-between; margin-bottom:8px;">
<div style="text-align:center; flex:1;">
<div style="font-size:11px; color:#9CA3AF; font-weight:700;">이번 달 목표</div>
<div style="font-size:20px; font-weight:900; color:#1E3A8A;">{target}</div>
</div>
<div style="width:1px; background:#E5E7EB; margin:0 12px;"></div>
<div style="text-align:center; flex:1;">
<div style="font-size:11px; color:#9CA3AF; font-weight:700;">이번 달 실적</div>
<div style="font-size:20px; font-weight:900; color:{color['bg']};">{actual}</div>
</div>
</div>
<div style="text-align:center; margin-top:12px; font-size:11px; color:#9CA3AF; background:#F8FAFC; padding:4px 8px; border-radius:6px;">{kpi_type}</div>
</div>
</div>"""
    st.markdown(card_html, unsafe_allow_html=True)


def _render_ai_box(analysis: dict):
    """AI 해석 박스 렌더링"""
    summary = analysis["summary"]
    avg_rate = analysis["avg_rate"]
    strong = analysis["strong"]
    risk = analysis["risk"]
    actions = analysis["actions"]

    # 강점 KPI 텍스트
    strong_text = ""
    for s in strong:
        strong_text += f'<span style="display:inline-block; background:#059669; color:white; padding:2px 10px; border-radius:12px; font-size:13px; font-weight:700; margin:2px 4px;">▲ {s["name"]} {s["rate"]:.1f}%</span>'

    # 리스크 KPI 텍스트
    risk_text = ""
    for r in risk:
        risk_text += f'<span style="display:inline-block; background:#EF4444; color:white; padding:2px 10px; border-radius:12px; font-size:13px; font-weight:700; margin:2px 4px;">▼ {r["name"]} {r["rate"]:.1f}%</span>'

    # 활동 제안 텍스트
    actions_html = ""
    for a in actions:
        actions_html += f'<div style="padding:4px 0; font-size:13px; color:#374151;">→ {a}</div>'

    box_html = f"""<div style="background:linear-gradient(135deg,#EEF2FF,#F0F4FF); border:1px solid #C7D2F0; border-radius:14px; padding:20px; margin:12px 0 24px 0;">
<div style="display:flex; align-items:center; margin-bottom:14px;">
<span style="font-size:22px; margin-right:8px;">💡</span>
<span style="font-weight:900; font-size:16px; color:#1E3A8A; font-family:'Noto Sans KR',sans-serif;">AI 성과 해석</span>
<span style="margin-left:auto; background:#0047AB; color:white; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700;">평균 {avg_rate}%</span>
</div>
<div style="font-size:14px; color:#1E3A8A; font-weight:700; margin-bottom:14px; padding:10px 14px; background:white; border-radius:10px; border-left:4px solid #0047AB;">{summary}</div>
<div style="display:flex; gap:16px; margin-bottom:14px; flex-wrap:wrap;">
<div style="flex:1; min-width:200px;">
<div style="font-size:12px; color:#059669; font-weight:900; margin-bottom:6px;">✅ 강점 KPI</div>
{strong_text}
</div>
<div style="flex:1; min-width:200px;">
<div style="font-size:12px; color:#EF4444; font-weight:900; margin-bottom:6px;">⚠️ 리스크 KPI</div>
{risk_text}
</div>
</div>
<div>
<div style="font-size:12px; color:#0047AB; font-weight:900; margin-bottom:6px;">📋 다음 활동 제안</div>
{actions_html}
</div>
<div style="text-align:right; margin-top:12px; font-size:10px; color:#999999; font-style:italic;">* 규칙 기반 자동 생성 (LLM API 미사용)</div>
</div>"""
    st.markdown(box_html, unsafe_allow_html=True)


def _render_org_section(org_name: str, org_id: int, level: int,
                        monthly_df: pd.DataFrame, latest_month: int):
    """하나의 조직 섹션 렌더링 (헤더 + KPI 카드 + AI 해석)"""
    # 해당 조직의 최신 월 KPI 데이터
    kpi_data = monthly_df[
        (monthly_df["조직ID"] == org_id) & (monthly_df["월"] == latest_month)
    ].copy()

    if kpi_data.empty:
        return

    # 레벨별 헤더 스타일 (margin-left 통일: 0)
    if level == 1:
        bg = "linear-gradient(90deg,#0047AB,#1E3A8A)"
        font_size = "18px"
        icon = "🏢"
    elif level == 2:
        bg = "linear-gradient(90deg,#1E3A8A,#3B82F6)"
        font_size = "16px"
        icon = "🏛️"
    else:
        bg = "linear-gradient(90deg,#3B82F6,#60A5FA)"
        font_size = "15px"
        icon = "👥"

    # 조직 헤더
    header_html = f"""<div style="margin-top:28px; margin-bottom:12px; padding:12px 20px; background:{bg}; border-radius:10px; color:white; font-weight:900; font-size:{font_size}; display:flex; justify-content:space-between; align-items:center; font-family:'Noto Sans KR',sans-serif;">
<span>{icon} {org_name}</span>
<span style="font-size:13px; opacity:0.8; font-weight:700;">{latest_month}월 기준 | KPI {len(kpi_data)}개</span>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)

    # KPI 카드 (3열 배치)
    kpi_list = kpi_data.reset_index(drop=True)
    for i in range(0, len(kpi_list), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(kpi_list):
                with col:
                    _render_kpi_card(kpi_list.iloc[i + j])
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # AI 해석 박스
    analysis = analyze_org_kpis(kpi_data)
    _render_ai_box(analysis)


def render(data: dict[str, pd.DataFrame]):
    """KPI 추진현황 탭 전체 렌더링"""
    org_df = data["org"]
    monthly_df = data["monthly"]
    latest_month = _get_latest_month(monthly_df)

    # 1) Level 1: 전사 (조직ID 순)
    level1 = org_df[org_df["Level"] == 1].sort_values("조직ID")
    for _, org in level1.iterrows():
        org_id = int(org["조직ID"])
        _render_org_section(org["조직명"], org_id, 1, monthly_df, latest_month)

    # Level 2 분류: "본부" 포함 vs "팀" 포함 (CEO 직보)
    level2_all = org_df[org_df["Level"] == 2].sort_values("조직ID")
    bonbu = level2_all[level2_all["조직명"].str.contains("본부")]
    jikbo = level2_all[level2_all["조직명"].str.contains("팀")]

    # 2) 본부들만 먼저 전부 표시 (소속 팀 없이)
    for _, l2 in bonbu.iterrows():
        _render_org_section(l2["조직명"], int(l2["조직ID"]), 2, monthly_df, latest_month)

    # 3) 구분선
    st.markdown(
        '<hr style="border:none; height:2px; background:linear-gradient'
        '(90deg,#3B82F6,#60A5FA); margin:32px 0 8px 0;">',
        unsafe_allow_html=True,
    )

    # 4) 각 본부별 소속 팀 그룹
    for _, l2 in bonbu.iterrows():
        l2_id = int(l2["조직ID"])
        level3 = org_df[org_df["ParentID"] == l2_id].sort_values("조직ID")
        if level3.empty:
            continue
        st.markdown(
            f'<div style="margin-top:28px; margin-bottom:4px; padding:8px 16px;'
            f' background:#E0E8F9; border-radius:8px; font-size:14px;'
            f' font-weight:900; color:#1E3A8A; font-family:\'Noto Sans KR\',sans-serif;">'
            f'📂 {l2["조직명"]} 소속 팀</div>',
            unsafe_allow_html=True,
        )
        for _, l3 in level3.iterrows():
            _render_org_section(l3["조직명"], int(l3["조직ID"]), 3, monthly_df, latest_month)

    # 5) CEO 직보 팀 (Level 2 중 "팀" 포함, 조직ID 순)
    if not jikbo.empty:
        st.markdown(
            '<hr style="border:none; height:2px; background:linear-gradient'
            '(90deg,#3B82F6,#60A5FA); margin:32px 0 8px 0;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="margin-bottom:4px; padding:8px 16px;'
            ' background:#E0E8F9; border-radius:8px; font-size:14px;'
            ' font-weight:900; color:#1E3A8A; font-family:\'Noto Sans KR\',sans-serif;">'
            '⭐ CEO 직보</div>',
            unsafe_allow_html=True,
        )
        for _, l2 in jikbo.iterrows():
            _render_org_section(l2["조직명"], int(l2["조직ID"]), 2, monthly_df, latest_month)
