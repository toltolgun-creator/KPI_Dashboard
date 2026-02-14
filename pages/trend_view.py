"""
월별 KPI 추이 탭
- 조직별 YTD 달성률 꺾은선 그래프 + AI 추이 분석
- 조직 표시 순서: kpi_view.py와 동일 (전사→본부→본부별 팀→CEO 직보)
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# KPI별 색상 팔레트
_PALETTE = [
    "#0047AB", "#10B981", "#EF4444", "#F59E0B", "#8B5CF6",
    "#EC4899", "#06B6D4", "#84CC16", "#F97316", "#6366F1",
]


def _parse_rate(val) -> float | None:
    """'110.72%' 같은 문자열을 float(110.72)로 변환"""
    try:
        return float(str(val).replace("%", "").strip())
    except (ValueError, TypeError):
        return None


# ──────────────────────────────────────────
# 추이 분석 (규칙 기반)
# ──────────────────────────────────────────

def _analyze_trend(org_data: pd.DataFrame) -> dict:
    """조직의 월별 KPI 추이를 분석하여 결과 반환"""
    kpi_names = org_data["KPI명"].unique()
    latest_month = int(org_data["월"].max())

    improving = []   # 개선 추세 KPI
    worsening = []   # 악화 추세 KPI
    alerts = []      # 주의 KPI

    for kpi in kpi_names:
        kd = org_data[org_data["KPI명"] == kpi].sort_values("월")
        rates = kd["달성률"].tolist()
        if len(rates) < 2:
            continue

        latest = rates[-1]
        prev = rates[-2]
        diff = latest - prev
        first = rates[0]
        overall_diff = latest - first

        if diff > 0 and overall_diff > 0:
            improving.append({"name": kpi, "latest": latest, "diff": diff})
        elif diff < 0 and overall_diff < 0:
            worsening.append({"name": kpi, "latest": latest, "diff": diff})

        if latest < 90:
            alerts.append({"name": kpi, "latest": latest})

    # 정렬
    improving.sort(key=lambda x: x["diff"], reverse=True)
    worsening.sort(key=lambda x: x["diff"])

    # 종합 요약
    avg_latest = org_data[org_data["월"] == latest_month]["달성률"].mean()
    if len(org_data["월"].unique()) >= 2:
        prev_month = sorted(org_data["월"].unique())[-2]
        avg_prev = org_data[org_data["월"] == prev_month]["달성률"].mean()
        avg_diff = avg_latest - avg_prev
        if avg_diff > 0:
            trend_text = f"전월 대비 평균 +{avg_diff:.1f}%p 개선 추세입니다."
        else:
            trend_text = f"전월 대비 평균 {avg_diff:.1f}%p 하락 추세입니다."
    else:
        trend_text = "추이 비교를 위한 데이터가 부족합니다."

    # 활동 제안
    actions = []
    for w in worsening[:2]:
        actions.append(
            f"'{w['name']}' 연속 하락 중 ({w['diff']:+.1f}%p) — 원인 분석 필요"
        )
    for a in alerts[:2]:
        if not any(a["name"] in act for act in actions):
            actions.append(
                f"'{a['name']}' {a['latest']:.1f}% — 목표 대비 크게 미달"
            )
    if improving and not actions:
        actions.append("전반적으로 개선 추세이나 지속 모니터링 필요")
    if not actions:
        actions.append("안정적 추세 유지 중 — 현행 유지 권장")

    return {
        "summary": trend_text,
        "avg_rate": round(avg_latest, 1),
        "improving": improving[:3],
        "worsening": worsening[:3],
        "alerts": alerts[:3],
        "actions": actions,
    }


def _render_trend_ai_box(analysis: dict):
    """추이 분석 AI 박스 렌더링 (kpi_view 스타일 동일)"""
    summary = analysis["summary"]
    avg_rate = analysis["avg_rate"]
    improving = analysis["improving"]
    worsening = analysis["worsening"]
    actions = analysis["actions"]

    # 개선 KPI 텍스트
    imp_text = ""
    for s in improving:
        imp_text += (
            f'<span style="display:inline-block; background:#059669; color:white;'
            f' padding:2px 10px; border-radius:12px; font-size:12px;'
            f' font-weight:700; margin:2px 0;">▲ {s["name"]}'
            f' +{s["diff"]:.1f}%p</span>'
        )
    if not imp_text:
        imp_text = '<span style="font-size:12px; color:#9CA3AF;">—</span>'

    # 악화 KPI 텍스트
    wrs_text = ""
    for w in worsening:
        wrs_text += (
            f'<span style="display:inline-block; background:#EF4444; color:white;'
            f' padding:2px 10px; border-radius:12px; font-size:12px;'
            f' font-weight:700; margin:2px 0;">▼ {w["name"]}'
            f' {w["diff"]:.1f}%p</span>'
        )
    if not wrs_text:
        wrs_text = '<span style="font-size:12px; color:#9CA3AF;">—</span>'

    # 활동 제안
    actions_html = ""
    for a in actions:
        actions_html += (
            f'<div style="padding:3px 0; font-size:12px; color:#374151;">'
            f'→ {a}</div>'
        )

    box_html = f"""<div style="background:linear-gradient(135deg,#EEF2FF,#F0F4FF);
        border:1px solid #C7D2F0; border-radius:14px; padding:20px;
        margin:12px 0 24px 0;">
<div style="display:flex; align-items:center; margin-bottom:10px;">
<span style="font-size:22px; margin-right:8px;">💡</span>
<span style="font-weight:900; font-size:16px; color:#1E3A8A;
    font-family:'Noto Sans KR',sans-serif;">AI 성과해석</span>
<span style="margin-left:auto; background:#0047AB; color:white;
    padding:2px 10px; border-radius:20px; font-size:11px;
    font-weight:700;">평균 {avg_rate}%</span>
</div>
<div style="font-size:13px; color:#1E3A8A; font-weight:700;
    margin-bottom:12px; padding:8px 10px; background:white;
    border-radius:8px; border-left:4px solid #0047AB;">{summary}</div>
<div style="margin-bottom:10px;">
<div style="font-size:11px; color:#059669; font-weight:900;
    margin-bottom:4px;">✅ 개선 추세</div>
{imp_text}
</div>
<div style="margin-bottom:10px;">
<div style="font-size:11px; color:#EF4444; font-weight:900;
    margin-bottom:4px;">⚠️ 악화 추세</div>
{wrs_text}
</div>
<div>
<div style="font-size:11px; color:#0047AB; font-weight:900;
    margin-bottom:4px;">📋 제안</div>
{actions_html}
</div>
<div style="margin-top:12px; font-size:10px; color:#999999; font-style:italic;">* 규칙 기반 자동 생성 (LLM API 미사용)</div>
</div>"""
    st.markdown(box_html, unsafe_allow_html=True)


# ──────────────────────────────────────────
# 조직별 섹션 렌더링
# ──────────────────────────────────────────

def _make_kpi_fig(kpi_name: str, kpi_data: pd.DataFrame, color: str,
                  y_min: float, y_max: float):
    """KPI 1개의 소형 꺾은선 그래프 생성 (Y축 범위 통일, 영역 색상)"""
    fig = go.Figure()

    # 배경 영역: 100% 이상 → 연한 초록
    fig.add_hrect(
        y0=100, y1=y_max,
        fillcolor="rgba(16,185,129,0.08)", line_width=0,
    )
    # 배경 영역: 90% 미만 → 연한 빨강
    fig.add_hrect(
        y0=y_min, y1=90,
        fillcolor="rgba(239,68,68,0.08)", line_width=0,
    )

    line_color = "#0047AB"
    fig.add_trace(go.Scatter(
        x=kpi_data["월"],
        y=kpi_data["달성률"],
        mode="lines+markers+text",
        line=dict(color=line_color, width=2.5),
        marker=dict(size=6, color=line_color),
        text=[f"{v:.1f}" for v in kpi_data["달성률"]],
        textposition="top center",
        textfont=dict(size=9, color=line_color),
        hovertemplate="%{x}월: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(
        y=100, line_dash="dot", line_color="#D1D5DB", line_width=1,
    )
    fig.update_layout(
        height=180,
        margin=dict(l=10, r=10, t=28, b=24),
        plot_bgcolor="#FAFBFF",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        title=dict(
            text=kpi_name,
            font=dict(size=13, color="#1E3A8A", family="Noto Sans KR, sans-serif"),
            x=0, xanchor="left", y=0.98,
        ),
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=[f"{m}" for m in range(1, 13)],
            gridcolor="#E0E8F9",
            range=[0.5, 12.5],
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            gridcolor="#E0E8F9", tickfont=dict(size=10),
            range=[y_min, y_max],
        ),
        font=dict(family="Noto Sans KR, sans-serif"),
    )
    return fig


def _render_org_chart(org_name: str, org_id: int, level: int,
                      monthly_df: pd.DataFrame, y_min: float, y_max: float):
    """한 조직의 KPI별 개별 차트 + AI 분석"""
    org_data = monthly_df[monthly_df["조직ID"] == org_id].copy()
    if org_data.empty:
        return

    org_data["달성률"] = org_data["YTD달성률"].apply(_parse_rate)
    org_data = org_data.dropna(subset=["달성률"])
    if org_data.empty:
        return

    kpi_list = org_data["KPI명"].unique()

    # 레벨별 헤더 스타일
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

    # 헤더
    st.markdown(
        f'<div style="margin-top:28px; margin-bottom:12px; padding:12px 20px;'
        f' background:{bg}; border-radius:10px; color:white; font-weight:900;'
        f' font-size:{font_size}; display:flex; align-items:baseline;'
        f' font-family:\'Noto Sans KR\',sans-serif;">'
        f'{icon} {org_name}'
        f'<span style="font-size:12px; font-weight:600; opacity:0.75;'
        f' margin-left:10px;">(YTD 달성률 %)</span></div>',
        unsafe_allow_html=True,
    )

    # 그래프 3열 그리드
    for i in range(0, len(kpi_list), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(kpi_list):
                kpi_name = kpi_list[idx]
                kpi_data = org_data[org_data["KPI명"] == kpi_name].sort_values("월")
                color = _PALETTE[idx % len(_PALETTE)]
                with col:
                    st.plotly_chart(
                        _make_kpi_fig(kpi_name, kpi_data, color, y_min, y_max),
                        width="stretch",
                    )

    # AI 성과해석 박스 (그래프 아래)
    analysis = _analyze_trend(org_data)
    _render_trend_ai_box(analysis)


# ──────────────────────────────────────────
# 조직 순서
# ──────────────────────────────────────────

def _ordered_orgs(org_df: pd.DataFrame) -> list[tuple[str, int, int]]:
    """kpi_view.py와 동일한 순서로 (조직명, 조직ID, level) 리스트 반환"""
    result: list[tuple[str, int, int]] = []

    # Level 1
    for _, r in org_df[org_df["Level"] == 1].sort_values("조직ID").iterrows():
        result.append((r["조직명"], int(r["조직ID"]), 1))

    # Level 2 분류
    l2 = org_df[org_df["Level"] == 2].sort_values("조직ID")
    bonbu = l2[l2["조직명"].str.contains("본부")]
    jikbo = l2[l2["조직명"].str.contains("팀")]

    # 본부들
    for _, r in bonbu.iterrows():
        result.append((r["조직명"], int(r["조직ID"]), 2))

    # 본부별 소속 팀
    for _, r in bonbu.iterrows():
        l3 = org_df[org_df["ParentID"] == int(r["조직ID"])].sort_values("조직ID")
        for _, t in l3.iterrows():
            result.append((t["조직명"], int(t["조직ID"]), 3))

    # CEO 직보
    for _, r in jikbo.iterrows():
        result.append((r["조직명"], int(r["조직ID"]), 2))

    return result


def render(data: dict[str, pd.DataFrame]):
    """월별 KPI 추이 탭 렌더링"""
    org_df = data["org"]
    monthly_df = data["monthly"]

    # 전체 데이터에서 Y축 범위 계산 (모든 차트 통일)
    all_rates = monthly_df["YTD달성률"].apply(_parse_rate).dropna()
    rate_min = all_rates.min()
    rate_max = all_rates.max()
    margin = (rate_max - rate_min) * 0.08
    y_min = rate_min - margin
    y_max = rate_max + margin

    for org_name, org_id, level in _ordered_orgs(org_df):
        _render_org_chart(org_name, org_id, level, monthly_df, y_min, y_max)
