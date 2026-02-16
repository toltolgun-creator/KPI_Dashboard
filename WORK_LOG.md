프로젝트: Streamlit KPI Dashboard (신발원단섬유, 150명)
원칙: Google Sheets가 계산, Python은 시각화만

Google Sheets: https://docs.google.com/spreadsheets/d/1gL-Y0LHpJqlDaqJx0TS87LGOISSX1oER/edit?usp=sharing
- 4개 시트 (KPI_Monthly_Data, Org_Master, KPI_Master, KPI_Type_Guide)
- 11개 조직, 55개 KPI, 12개월 데이터

완료:
- Python 3.13, Streamlit 설치
- VS Code, GitHub 연결
- Google Sheets 구축

화면 4개:
1. KPI 추진현황 (카드 + AI 해석)
2. 월별 추이 (그래프)
3. KPI 데이터 (전체 테이블)
4. 조직도 (트리)

---

## 개발 Phase 계획 (총 7단계)

### Phase 1: Google Sheets 데이터 연결 (기초)
- utils/data_loader.py 생성
- Google Sheets 4개 시트 읽기 함수
- 데이터 로드 테스트

### Phase 2: 기본 Streamlit 앱 구조
- app.py 생성 (메인 앱)
- 3개 탭 구조 (KPI 추진현황 / 월별 추이 / 조직도)

### Phase 3: Tab 1 - KPI 추진현황
- pages/kpi_view.py
- 조직 선택, KPI 카드, 평가등급 색상, 달성률 표시

### Phase 4: Tab 2 - 월별 KPI 추이
- pages/trend_view.py
- KPI 선택, 시계열 그래프, 월별 데이터 표

### Phase 5: Tab 3 - 조직도
- pages/org_view.py
- 전사→본부→팀 트리 구조

### Phase 6: LLM 해석 기능
- pages/llm_briefing.py
- 종합 평가, 강점/리스크, 활동 제안

### Phase 7: UI/UX 개선 및 마무리
- 디자인 정리, 로딩/에러 처리, 최종 테스트

---

현재 상태: 전체 Phase 완료 (프로젝트 완성)

---

## 2025-02-14 작업 내역

### 완료 사항

**데이터 구조:**
- Google Sheets에 본부 KPI 20개 추가 (조직ID 2002~2005, 각 5개)
- 총 KPI: 75개 (전사 5 + 본부 20 + 팀 50)

**utils/data_loader.py:**
- gviz API 헤더 파싱 문제 수정 (Org_Master, KPI_Master에 `headers=1` 적용)

**pages/kpi_view.py:**
- 조직 표시 순서 동적 정렬 구현
- Level, ParentID, 조직명 패턴("본부"/"팀") 기반
- 순서: Level 1 → Level 2 본부들 → 각 본부별 소속 팀들 → Level 2 팀들 (CEO 직보)
- 헤더/카드/AI박스 좌측 정렬 통일 (margin-left 제거)

**pages/trend_view.py (신규):**
- 조직별 KPI 월별 추이 그래프
- 3열 그리드 레이아웃 (KPI별 개별 차트)
- Plotly 사용, 꺾은선 색상 파란색(#0047AB) 통일
- Y축 범위 전체 차트 동일 적용
- 배경 색상: 100% 이상 연한 초록, 90% 미만 연한 빨강
- 꺾은선 위 달성률 수치 표시 (소수점 1자리)
- AI 성과해석 박스 (추이 분석, 개선/악화 KPI, 제안)

**pages/org_view.py (신규):**
- 조직도 트리 시각화 (ul/li 기반 표준 트리 패턴)
- Level별 색상 구분 (진한/중간/연한 파란색)
- st.html() 사용으로 HTML 렌더링 문제 해결

### 다음 작업
- 배포 준비 (Streamlit Cloud)

---

## 2026-02-14 작업 내역

### 완료 사항

**pages/trend_view.py (월별 추이 그래프 개선):**
- 꺾은선 2개로 확장: YTD 달성률(진한 파랑 #0047AB) + 월 달성률(주황색 #F5A623)
- 범례 추가 (차트 상단 수평 배치)
- 조직명 헤더에서 "(YTD 달성률 %)" 텍스트 삭제
- 차트 배경색 변경: 100% 이상 아쿠아블루, 100% 미만 연한 붉은색
- Y축 범위 계산에 월 달성률 포함

**utils/data_loader.py (폐지 조직/KPI 제외 로직):**
- `get_active_org_ids()`: Org_Master 해지일 기준 활성 조직 ID 반환
- `filter_active_orgs()`: 폐지 조직 제외한 DataFrame 반환
- `get_active_kpi_ids()`: KPI_Master 해지일 기준 활성 KPI ID 반환
- 로직: 해지일 NaN/빈값/파싱실패 → 활성, 미래 → 활성, 과거 → 폐지

**pages/kpi_view.py (폐지 제외 적용):**
- render()에서 org_df, monthly_df에 활성 조직 + 활성 KPI 이중 필터 적용

**pages/trend_view.py (폐지 제외 적용):**
- render()에서 org_df, monthly_df에 활성 조직 + 활성 KPI 이중 필터 적용

**pages/org_view.py (폐지 제외 적용):**
- render()에서 org_df에 활성 조직 필터 적용

**Google Sheets 변경:**
- KPI_Monthly_Data에 '월 달성률' 컬럼 추가 (14열)

### 커밋
- `9403da1` 폐지된 조직/KPI 제외 로직 추가, 월별 추이 그래프 개선

### 다음 작업
- 배포 준비 (Streamlit Cloud)

---

## 2026-02-16 작업 내역

### 완료 사항

**프로젝트 정리:**
- `pages/trend_view.py.bak`, `nul` 파일 삭제
- `.gitignore` 생성 (`__pycache__/`, `*.pyc`, `*.bak`, `nul`, `pyproject.toml`)
- `README.md` 작성 (프로젝트 소개, 기능, 구조, 설치/실행 가이드)

**pages/trend_view.py (차트 높이 조정):**
- 꺾은선 그래프 높이 200px → 280px로 변경

**pages/data_view.py (신규 — KPI 데이터 탭):**
- 조직도 앞에 "📊 KPI 데이터" 탭 추가 (3번째 탭, 총 4탭 구조)
- KPI_Monthly_Data를 피벗하여 조직·KPI별 한 행에 12개월 데이터 표시
- 컬럼: 단위조직명, 단위조직ID, KPI명, 1~12월(목표/실적/달성률), 1~12월(YTD목표/YTD실적/YTD달성률), YTD평가결과
- YTD평가결과는 가장 최근 월의 값만 표시
- HTML 테이블 직접 렌더링 (조직별 배경색 구분, 헤더 고정, 세로 스크롤)
- 헤더 색상: 월별(파랑 교차), YTD(초록 교차)
- 폐지 조직/KPI 필터링 적용

**app.py:**
- `data_view` import 및 탭 추가 (총 4탭 구조)

**전체 코드 점검:**
- 7개 핵심 파일 전수 검토, 에러 없음 확인

### 프로젝트 완성
- 전체 Phase 1~7 완료
- Streamlit Cloud 배포

---

## 향후 작업: LLM API 연동 (AI 성과해석 고도화)

### 현재 상태
- KPI 추진현황, 월별 추이 탭의 "AI 성과해석" 박스는 **룰 기반 자동 생성** (LLM 미사용)
- `pages/llm_briefing.py`의 `analyze_org_kpis()` — KPI 추진현황용 분석
- `pages/trend_view.py`의 `_analyze_trend()` — 월별 추이용 분석
- 달성률 구간별 고정 멘트를 출력하는 방식 (분석 깊이 제한적)

### 목표
- 실제 LLM API(Claude API 등)를 연동하여 데이터 기반 심층 분석 제공
- 고객 배포 시 전문적인 KPI 성과 해석이 가능하도록 개선

### 수정 범위 (작업량: 소)
현재 코드 구조가 **분석 함수 ↔ 렌더링 함수**로 분리되어 있어 수정이 간단함

| 수정 대상 | 내용 |
|---|---|
| `llm_briefing.py` → `analyze_org_kpis()` | 내부 로직을 LLM API 호출로 교체 |
| `trend_view.py` → `_analyze_trend()` | 내부 로직을 LLM API 호출로 교체 |
| Streamlit Secrets | API 키 설정 추가 |
| `requirements.txt` | LLM SDK 추가 (예: `anthropic`) |

**변경 불필요**: 렌더링 코드(`_render_ai_box`, `_render_trend_ai_box`), app.py, data_view.py, org_view.py

### 주의사항: 비용과 속도

| 항목 | 설명 |
|---|---|
| API 호출 횟수 | 현재 11개 조직 × 2개 탭 = 페이지 로드당 약 22회 호출 |
| 비용 | 호출당 과금 발생 (LLM 요금제에 따라 다름) |
| 속도 | LLM 호출 1건당 2~5초 → 전체 로딩 느려질 수 있음 |

### 비용/속도 최적화 대안

1. **캐싱 강화**: 데이터가 바뀔 때만 LLM 호출 (매 로드마다 호출하지 않음)
2. **배치 처리**: 전체 조직 데이터를 한 번에 보내서 1회 호출로 처리
3. **수동 트리거**: "AI 분석 실행" 버튼을 누를 때만 LLM 호출
4. **하이브리드**: 기본은 룰 기반, 사용자가 원할 때만 LLM 분석 실행
