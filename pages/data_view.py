"""
KPI 데이터 탭
- Google Sheets에서 읽어온 KPI 월별 데이터를 피벗 테이블로 표시
- 조직별 KPI의 월별 목표/실적/달성률을 한 행에 나열
"""

import streamlit as st
import pandas as pd
from utils.data_loader import filter_active_orgs, get_active_org_ids, get_active_kpi_ids


def _build_html_table(df: pd.DataFrame) -> str:
    """DataFrame을 스타일링된 HTML 테이블로 변환"""

    css = """
<style>
.kpi-data-wrap {
    overflow-x: auto;
    overflow-y: auto;
    max-height: 660px;
    margin-top: 8px;
}
.kpi-data-table {
    border-collapse: collapse;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 11px;
    white-space: nowrap;
}
.kpi-data-table th {
    padding: 7px 10px;
    text-align: center;
    font-weight: 700;
    font-size: 10px;
    border: 1px solid rgba(255,255,255,0.3);
    position: sticky;
    top: 0;
    z-index: 10;
}
.kpi-data-table td {
    padding: 5px 10px;
    border: 1px solid #E2E8F0;
    text-align: center;
    min-width: 62px;
}
.kpi-data-table td:nth-child(1) { text-align: left; font-weight: 600; min-width: 90px; }
.kpi-data-table td:nth-child(2) { text-align: center; font-weight: 600; min-width: 60px; }
.kpi-data-table td:nth-child(3) { text-align: left; font-weight: 600; min-width: 140px; }
.th-info { background: #1E293B; color: #FFFFFF; }
.th-m-odd { background: #0047AB; color: #FFFFFF; }
.th-m-even { background: #2563EB; color: #FFFFFF; }
.th-y-odd { background: #0F766E; color: #FFFFFF; }
.th-y-even { background: #0D9488; color: #FFFFFF; }
.th-grade { background: #1E293B; color: #FFFFFF; }
.kpi-data-table tbody tr:hover { background: #DBEAFE; }
</style>
"""

    parts = [css, '<div class="kpi-data-wrap"><table class="kpi-data-table">']

    # ── 헤더 ──
    parts.append("<thead><tr>")
    for col in ["단위조직명", "단위조직ID", "KPI명"]:
        parts.append(f'<th class="th-info">{col}</th>')
    for m in range(1, 13):
        cls = "th-m-odd" if m % 2 == 1 else "th-m-even"
        for s in ["목표", "실적", "달성률"]:
            parts.append(f'<th class="{cls}">{m}월{s}</th>')
    for m in range(1, 13):
        cls = "th-y-odd" if m % 2 == 1 else "th-y-even"
        for s in ["YTD목표", "YTD실적", "YTD달성률"]:
            parts.append(f'<th class="{cls}">{m}월{s}</th>')
    parts.append('<th class="th-grade">YTD평가결과</th>')
    parts.append("</tr></thead>")

    # ── 조직별 배경색 ──
    org_colors = [
        "#F0F4FF", "#FFF8EE", "#F0FFF4", "#FFF0F6",
        "#F5F0FF", "#FEFCE8", "#F0FDFA", "#FFF1F2",
        "#EFF6FF", "#FDF4FF", "#ECFDF5",
    ]
    org_ids = list(dict.fromkeys(df["단위조직ID"]))  # 순서 유지 중복 제거
    org_color_map = {oid: org_colors[i % len(org_colors)] for i, oid in enumerate(org_ids)}

    # ── 본문 ──
    parts.append("<tbody>")
    for _, row in df.iterrows():
        bg = org_color_map.get(row["단위조직ID"], "#FFFFFF")
        parts.append(f'<tr style="background:{bg};">')
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                parts.append("<td>-</td>")
            else:
                parts.append(f"<td>{val}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table></div>")

    return "\n".join(parts)


def render(data: dict[str, pd.DataFrame]):
    """KPI 데이터 탭 렌더링"""
    org_df = filter_active_orgs(data["org"])
    active_ids = get_active_org_ids(data["org"])
    active_kpis = get_active_kpi_ids(data["kpi"])
    monthly_df = data["monthly"][
        data["monthly"]["조직ID"].isin(active_ids)
        & data["monthly"]["KPI_ID"].isin(active_kpis)
    ].copy()

    latest_month = int(monthly_df["월"].max())

    # 조직·KPI별로 12개월 데이터를 한 행으로 피벗
    rows = []
    for (org_name, org_id, kpi_name), grp in monthly_df.groupby(
        ["조직명", "조직ID", "KPI명"], sort=False,
    ):
        row: dict = {
            "단위조직명": org_name,
            "단위조직ID": int(org_id),
            "KPI명": kpi_name,
        }

        for _, r in grp.iterrows():
            m = int(r["월"])
            row[f"{m}월목표"] = r["월목표"]
            row[f"{m}월실적"] = r["월실적"]
            row[f"{m}월달성률"] = r["월 달성률"]
            row[f"{m}월YTD목표"] = r["YTD목표"]
            row[f"{m}월YTD실적"] = r["YTD실적"]
            row[f"{m}월YTD달성률"] = r["YTD달성률"]

            if m == latest_month:
                row["YTD평가결과"] = r["YTD평가결과"]

        rows.append(row)

    # 컬럼 순서 지정
    cols = ["단위조직명", "단위조직ID", "KPI명"]
    for m in range(1, 13):
        cols.extend([f"{m}월목표", f"{m}월실적", f"{m}월달성률"])
    for m in range(1, 13):
        cols.extend([f"{m}월YTD목표", f"{m}월YTD실적", f"{m}월YTD달성률"])
    cols.append("YTD평가결과")

    result_df = pd.DataFrame(rows, columns=cols)
    result_df.sort_values(["단위조직ID", "KPI명"], inplace=True)
    result_df.reset_index(drop=True, inplace=True)

    # 정보 표시
    kpi_count = len(result_df)
    org_count = result_df["단위조직ID"].nunique()
    st.markdown(
        f'<div style="font-size:14px; color:#1E3A8A; font-weight:700; '
        f'margin-bottom:12px; font-family:\'Noto Sans KR\',sans-serif;">'
        f'총 {org_count}개 조직 · {kpi_count}개 KPI · {latest_month}월 기준</div>',
        unsafe_allow_html=True,
    )

    # HTML 테이블 렌더링 (st.markdown으로 메인 페이지에 삽입해야 sticky 헤더 동작)
    st.markdown(_build_html_table(result_df), unsafe_allow_html=True)
