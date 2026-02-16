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
