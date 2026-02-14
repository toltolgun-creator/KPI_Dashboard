"""
Google Sheets 데이터 로더
- Google Sheets CSV Export 방식 (인증 불필요)
- 시트가 '링크가 있는 모든 사용자에게 공개'로 설정되어 있어야 함
"""

from datetime import date

import pandas as pd
import urllib.parse


# Google Sheets ID (URL에서 추출)
SHEET_ID = "1gL-Y0LHpJqlDaqJx0TS87LGOISSX1oER"

# 4개 시트 이름
SHEET_NAMES = {
    "monthly": "KPI_Monthly_Data",
    "org": "Org_Master",
    "kpi": "KPI_Master",
    "type_guide": "KPI_Type_Guide",
}

# gviz API가 헤더를 자동 감지할 때 데이터를 헤더에 합치는 시트 목록
# 이 시트들은 headers=1 파라미터로 헤더 행을 명시해야 함
_SHEETS_NEED_EXPLICIT_HEADER = {"Org_Master", "KPI_Master"}


def _build_csv_url(sheet_name: str) -> str:
    """시트 이름으로 CSV export URL 생성"""
    encoded_name = urllib.parse.quote(sheet_name)
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={encoded_name}"
    )
    if sheet_name in _SHEETS_NEED_EXPLICIT_HEADER:
        url += "&headers=1"
    return url


def load_sheet(sheet_name: str) -> pd.DataFrame:
    """개별 시트를 DataFrame으로 로드"""
    url = _build_csv_url(sheet_name)
    try:
        df = pd.read_csv(url)
        print(f"  [OK] {sheet_name}: {df.shape[0]}행 x {df.shape[1]}열")
        return df
    except Exception as e:
        print(f"  [ERROR] {sheet_name} 로드 실패: {e}")
        raise


def load_all_data() -> dict[str, pd.DataFrame]:
    """4개 시트를 한 번에 로드하여 딕셔너리로 반환"""
    print("Google Sheets 데이터 로딩 시작...")
    data = {}
    for key, sheet_name in SHEET_NAMES.items():
        data[key] = load_sheet(sheet_name)
    print("데이터 로딩 완료!")
    return data


def get_active_org_ids(org_df: pd.DataFrame) -> set[int]:
    """폐지되지 않은 조직 ID 집합을 반환.

    해지일이 비어있거나(NaN) 해지일이 오늘 이후이면 활성 조직.
    해지일이 있고 오늘보다 과거이면 폐지된 조직으로 판단하여 제외.
    """
    today = date.today()
    active_ids: set[int] = set()
    for _, row in org_df.iterrows():
        end_date = row.get("해지일")
        # NaN / None / 빈 문자열 → 활성
        if pd.isna(end_date) or str(end_date).strip() == "":
            active_ids.add(int(row["조직ID"]))
            continue
        # 날짜 파싱 후 비교
        try:
            parsed = pd.to_datetime(str(end_date)).date()
            if parsed >= today:
                active_ids.add(int(row["조직ID"]))
        except (ValueError, TypeError):
            # 파싱 실패 시 안전하게 활성 처리
            active_ids.add(int(row["조직ID"]))
    return active_ids


def filter_active_orgs(org_df: pd.DataFrame) -> pd.DataFrame:
    """폐지된 조직을 제외한 Org_Master DataFrame 반환"""
    active_ids = get_active_org_ids(org_df)
    return org_df[org_df["조직ID"].astype(int).isin(active_ids)].copy()


def get_active_kpi_ids(kpi_df: pd.DataFrame) -> set[str]:
    """폐지되지 않은 KPI_ID 집합을 반환.

    해지일이 비어있거나(NaN) 해지일이 오늘 이후이면 활성 KPI.
    해지일이 있고 오늘보다 과거이면 폐지된 KPI로 판단하여 제외.
    """
    today = date.today()
    active_ids: set[str] = set()
    for _, row in kpi_df.iterrows():
        end_date = row.get("해지일")
        if pd.isna(end_date) or str(end_date).strip() == "":
            active_ids.add(str(row["KPI_ID"]))
            continue
        try:
            parsed = pd.to_datetime(str(end_date)).date()
            if parsed >= today:
                active_ids.add(str(row["KPI_ID"]))
        except (ValueError, TypeError):
            active_ids.add(str(row["KPI_ID"]))
    return active_ids
