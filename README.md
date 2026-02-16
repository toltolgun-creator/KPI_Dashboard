# KPI Dashboard

신발원단섬유(150명) 전사 KPI 성과를 한눈에 확인할 수 있는 Streamlit 대시보드입니다.
Google Sheets에서 데이터를 실시간으로 불러와 시각화합니다.

## 주요 기능

| 탭 | 설명 |
|---|---|
| **KPI 추진현황** | 조직별 KPI 카드 그리드, 평가등급(S/A/B/C/D) 색상 표시, AI 성과 해석 |
| **월별 KPI 추이** | KPI별 YTD/월 달성률 이중 꺾은선 차트, 추이 분석 |
| **KPI 데이터** | 전체 KPI 월별 목표/실적/달성률 피벗 테이블, 조직별 색상 구분 |
| **조직도** | 전사 → 본부 → 팀 계층 트리 시각화 |

## 데이터 구조

Google Sheets 4개 시트를 사용합니다.

| 시트명 | 용도 |
|---|---|
| `KPI_Monthly_Data` | 월별 KPI 실적 (목표, 실적, 달성률) |
| `Org_Master` | 조직 마스터 (조직ID, 조직명, Level, ParentID) |
| `KPI_Master` | KPI 마스터 (KPI_ID, KPI명, 목표값) |
| `KPI_Type_Guide` | KPI 유형 참조 |

> **원칙**: Google Sheets가 계산을 담당하고, Python(Streamlit)은 시각화만 수행합니다.

## 프로젝트 구조

```
KPI_Dashboard/
├── app.py                  # 메인 앱 (탭 구성, 테마, 데이터 캐싱)
├── requirements.txt        # 의존성 목록
├── pages/
│   ├── kpi_view.py         # Tab 1: KPI 추진현황
│   ├── trend_view.py       # Tab 2: 월별 KPI 추이
│   ├── data_view.py        # Tab 3: KPI 데이터 테이블
│   ├── org_view.py         # Tab 4: 조직도
│   └── llm_briefing.py     # 룰 기반 KPI 성과 분석 엔진
└── utils/
    └── data_loader.py      # Google Sheets 데이터 로더
```

## 설치 및 실행

### 요구사항

- Python 3.13+

### 설치

```bash
pip install -r requirements.txt
```

### 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 로 접속하면 대시보드를 확인할 수 있습니다.

## 기술 스택

- **Streamlit** — 웹 대시보드 프레임워크
- **Pandas** — 데이터 처리
- **Plotly** — 인터랙티브 차트
- **Google Sheets gviz API** — 데이터 소스 (인증 불필요, 공개 링크 방식)

## AI 성과해석 — 향후 LLM 연동 가이드

KPI 추진현황, 월별 추이 탭의 "AI 성과해석" 박스는 현재 **룰 기반 자동 생성**입니다.
고객 배포 시 실제 LLM(Claude API 등)으로 교체하여 심층 분석이 가능합니다.

### 수정 대상 (2개 함수만 교체)

| 파일 | 함수 | 용도 |
|---|---|---|
| `pages/llm_briefing.py` | `analyze_org_kpis()` | KPI 추진현황 분석 |
| `pages/trend_view.py` | `_analyze_trend()` | 월별 추이 분석 |

위 함수의 내부 로직만 LLM API 호출로 교체하면 됩니다.
렌더링 코드(`_render_ai_box` 등)는 변경 불필요합니다.

### 비용/속도 최적화 대안

| 방법 | 설명 |
|---|---|
| 캐싱 강화 | 데이터 변경 시에만 LLM 호출 |
| 배치 처리 | 전체 조직을 1회 API 호출로 분석 |
| 수동 트리거 | "AI 분석 실행" 버튼 클릭 시에만 호출 |
| 하이브리드 | 기본 룰 기반 + 사용자 요청 시 LLM 분석 |
