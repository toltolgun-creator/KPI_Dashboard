"""
조직도 탭 - 트리 구조 시각화
- Org_Master 데이터를 기반으로 전사→본부→팀 트리 표시
- Level별 색상 구분
"""

import pandas as pd
import streamlit as st

# Level별 색상 정의
LEVEL_COLORS = {
    1: {"bg": "#0047AB", "text": "#FFFFFF", "border": "#003380"},  # 진한 파란색
    2: {"bg": "#3B82F6", "text": "#FFFFFF", "border": "#2563EB"},  # 중간 파란색
    3: {"bg": "#93C5FD", "text": "#1E3A8A", "border": "#60A5FA"},  # 연한 파란색
}

# Level 2 표시 순서 (조직ID 기준)
LEVEL2_ORDER = [2002, 2003, 3101, 2004, 2005]


def _build_tree(org_df: pd.DataFrame) -> dict:
    """Org_Master DataFrame을 트리 딕셔너리로 변환"""
    root = org_df[org_df["Level"] == 1].iloc[0]
    root_id = int(root["조직ID"])

    # Level 2 자식 조직 (지정 순서대로)
    level2 = org_df[org_df["ParentID"] == root_id]
    level2_ordered = []
    for oid in LEVEL2_ORDER:
        match = level2[level2["조직ID"] == oid]
        if not match.empty:
            level2_ordered.append(match.iloc[0])

    children = []
    for l2 in level2_ordered:
        l2_id = int(l2["조직ID"])
        # Level 3 자식 조직
        level3 = org_df[org_df["ParentID"] == l2_id]
        grandchildren = [
            {"name": row["조직명"], "level": 3}
            for _, row in level3.iterrows()
        ]
        children.append({
            "name": l2["조직명"],
            "level": 2,
            "children": grandchildren,
        })

    return {"name": root["조직명"], "level": 1, "children": children}


def _render_tree_html(tree: dict) -> str:
    """트리 딕셔너리를 HTML로 변환 (ul/li 기반 표준 트리 패턴)"""
    root = tree
    c1 = LEVEL_COLORS[1]
    c2 = LEVEL_COLORS[2]
    c3 = LEVEL_COLORS[3]
    line_color = "#3B82F6"
    line_w = "2px"
    gap_h = "28px"  # 수직 연결선 높이

    # Level 2 → Level 3 서브트리 생성
    level2_items = []
    for child in root["children"]:
        l3_html = ""
        if child["children"]:
            l3_nodes = "".join(
                f'<li><div class="card l3" style="background:{c3["bg"]};'
                f'color:{c3["text"]};border-color:{c3["border"]};">'
                f'{gc["name"]}</div></li>'
                for gc in child["children"]
            )
            l3_html = f"<ul>{l3_nodes}</ul>"

        level2_items.append(
            f'<li><div class="card l2" style="background:{c2["bg"]};'
            f'color:{c2["text"]};border-color:{c2["border"]};">'
            f'{child["name"]}</div>{l3_html}</li>'
        )

    level2_html = "".join(level2_items)

    html = f"""
    <style>
        .otree *  {{ margin:0; padding:0; box-sizing:border-box; }}
        .otree    {{ padding:36px 10px 20px; overflow-x:auto;
                     font-family:'Noto Sans KR',sans-serif; }}

        /* ── 카드 공통 ── */
        .otree .card {{
            display:inline-block; border-radius:10px; border:2px solid;
            font-weight:700; text-align:center; white-space:nowrap;
            box-shadow:0 2px 10px rgba(0,71,171,.15);
            transition:transform .2s, box-shadow .2s;
            cursor:default; position:relative; z-index:1;
        }}
        .otree .card:hover {{
            transform:translateY(-3px);
            box-shadow:0 6px 18px rgba(0,71,171,.28);
        }}
        .otree .card.l1 {{ padding:16px 44px; font-size:20px; font-weight:900;
                           letter-spacing:2px; }}
        .otree .card.l2 {{ padding:11px 22px; font-size:15px; }}
        .otree .card.l3 {{ padding:9px 18px;  font-size:13px; font-weight:600; }}

        /* ── 트리 구조 (ul/li) ── */
        .otree ul {{
            display:flex; justify-content:center;
            padding-top:{gap_h}; position:relative;
            list-style:none;
        }}

        /* 부모 → 수평선 구간으로 내려오는 세로선 */
        .otree ul::before {{
            content:''; position:absolute;
            top:0; left:50%;
            width:{line_w}; height:{gap_h};
            background:{line_color};
        }}

        .otree li {{
            display:flex; flex-direction:column; align-items:center;
            position:relative; padding:{gap_h} 14px 0;
        }}

        /* 각 li 상단: 수평 가지선 + 세로 내려오는 선 */
        .otree li::before,
        .otree li::after {{
            content:''; position:absolute; top:0;
        }}

        /* 세로선 (수평선 → 카드) */
        .otree li::before {{
            left:50%; width:{line_w}; height:{gap_h};
            background:{line_color};
        }}

        /* 수평선 (형제 간 연결) */
        .otree li::after {{
            left:0; right:0; height:{line_w};
            background:{line_color};
        }}

        /* 첫 번째 자식: 왼쪽 절반만 */
        .otree li:first-child::after {{ left:50%; }}
        /* 마지막 자식: 오른쪽 절반만 */
        .otree li:last-child::after  {{ right:50%; }}
        /* 외동: 수평선 없음 */
        .otree li:only-child::after  {{ display:none; }}

        /* ── 루트 노드 (ul 밖) ── */
        .otree > .card {{ display:block; width:fit-content; margin:0 auto; }}
    </style>

    <div class="otree">
        <div class="card l1" style="background:{c1['bg']};color:{c1['text']};
             border-color:{c1['border']};">🏢 {root['name']}</div>
        <ul>{level2_html}</ul>
    </div>
    """
    return html


def render(data: dict[str, pd.DataFrame]):
    """조직도 탭 렌더링"""
    org_df = data["org"]
    tree = _build_tree(org_df)
    html = _render_tree_html(tree)

    # 범례를 트리 HTML에 합쳐서 st.html()로 한 번에 렌더링
    legend = """
    <div style="display:flex; justify-content:center; gap:24px; margin-top:8px; padding:12px 0;">
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:16px; height:16px; background:#0047AB; border-radius:4px;"></div>
            <span style="font-size:13px; color:#1E3A8A; font-weight:700; font-family:'Noto Sans KR',sans-serif;">전사 (Level 1)</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:16px; height:16px; background:#3B82F6; border-radius:4px;"></div>
            <span style="font-size:13px; color:#1E3A8A; font-weight:700; font-family:'Noto Sans KR',sans-serif;">본부/직보 (Level 2)</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:16px; height:16px; background:#93C5FD; border-radius:4px;"></div>
            <span style="font-size:13px; color:#1E3A8A; font-weight:700; font-family:'Noto Sans KR',sans-serif;">팀 (Level 3)</span>
        </div>
    </div>
    """
    st.html(html + legend)
