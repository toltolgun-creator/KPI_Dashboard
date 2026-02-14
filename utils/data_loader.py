"""
Google Sheets 데이터 로더
- Google Sheets CSV Export 방식 (인증 불필요)
- 시트가 '링크가 있는 모든 사용자에게 공개'로 설정되어 있어야 함
"""

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
