프로젝트: Streamlit KPI Dashboard (신발원단섬유, 150명)
원칙: Google Sheets가 계산, Python은 시각화만

Google Sheets: https://docs.google.com/spreadsheets/d/1gL-Y0LHpJqlDaqJx0TS87LGOISSX1oER/edit?usp=sharing
- 4개 시트 (KPI_Monthly_Data, Org_Master, KPI_Master, KPI_Type_Guide)
- 11개 조직, 55개 KPI, 12개월 데이터

완료:
- Python 3.13, Streamlit 설치
- VS Code, GitHub 연결
- Google Sheets 구축

화면 3개:
1. KPI 추진현황 (카드 + LLM 해석)
2. 월별 추이 (그래프)
3. 조직도 (트리)

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

현재 상태: Phase 5 완료 (Phase 6 부분 포함)

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
