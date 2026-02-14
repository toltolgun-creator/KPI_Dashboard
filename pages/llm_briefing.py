"""
규칙 기반 KPI 분석 모듈
- 실제 데이터를 기반으로 자동 분석 텍스트 생성
- 추후 Anthropic API로 교체 가능
"""

import pandas as pd


def _parse_rate(rate_str: str) -> float:
    """'110.72%' → 110.72 숫자로 변환"""
    try:
        return float(str(rate_str).replace("%", "").strip())
    except (ValueError, TypeError):
        return 0.0


def analyze_org_kpis(kpi_data: pd.DataFrame) -> dict:
    """
    조직의 KPI 데이터를 분석하여 해석 결과 반환

    Returns:
        {
            "summary": "종합평가 문장",
            "avg_rate": 평균달성률,
            "achieved_count": 목표달성 KPI 수,
            "total_count": 전체 KPI 수,
            "strong": [{"name", "rate", "grade"}, ...],  # 상위 2개
            "risk": [{"name", "rate", "grade"}, ...],    # 하위 2개
            "actions": ["제안1", "제안2", ...]
        }
    """
    if kpi_data.empty:
        return {
            "summary": "데이터가 없습니다.",
            "avg_rate": 0, "achieved_count": 0, "total_count": 0,
            "strong": [], "risk": [], "actions": [],
        }

    df = kpi_data.copy()
    df["달성률_num"] = df["YTD달성률"].apply(_parse_rate)

    total = len(df)
    avg_rate = df["달성률_num"].mean()
    achieved = df[df["달성률_num"] >= 100]
    achieved_count = len(achieved)

    # 달성률 기준 정렬
    sorted_df = df.sort_values("달성률_num", ascending=False)

    # 강점 KPI (상위 2개)
    top = sorted_df.head(2)
    strong = [
        {"name": r["KPI명"], "rate": r["달성률_num"], "grade": r["YTD평가결과"]}
        for _, r in top.iterrows()
    ]

    # 리스크 KPI (하위 2개)
    bottom = sorted_df.tail(2)
    risk = [
        {"name": r["KPI명"], "rate": r["달성률_num"], "grade": r["YTD평가결과"]}
        for _, r in bottom.iterrows()
    ]

    # 종합평가 문장
    pct = (achieved_count / total * 100) if total > 0 else 0
    if pct >= 80:
        tone = "우수한 성과를 보이고 있습니다."
    elif pct >= 50:
        tone = "보통 수준이며 일부 개선이 필요합니다."
    else:
        tone = "목표 달성이 부진하여 집중 관리가 필요합니다."
    summary = f"{total}개 KPI 중 {achieved_count}개 목표 달성 ({pct:.0f}%). {tone}"

    # 활동 제안
    actions = []
    for _, r in bottom.iterrows():
        rate = r["달성률_num"]
        name = r["KPI명"]
        if rate < 80:
            actions.append(f"'{name}' ({rate:.1f}%) 긴급 원인 분석 및 대응 필요")
        elif rate < 90:
            actions.append(f"'{name}' ({rate:.1f}%) 목표 재점검 및 실행력 강화 필요")
        elif rate < 100:
            actions.append(f"'{name}' ({rate:.1f}%) 목표 달성까지 집중 관리 필요")

    # 강점 기반 제안
    if strong and strong[0]["rate"] >= 110:
        actions.append(f"'{strong[0]['name']}' 우수 사례를 타 KPI에 벤치마킹 권장")

    if not actions:
        actions.append("전반적으로 양호하나 지속적인 모니터링 필요")

    return {
        "summary": summary,
        "avg_rate": round(avg_rate, 1),
        "achieved_count": achieved_count,
        "total_count": total,
        "strong": strong,
        "risk": risk,
        "actions": actions,
    }
