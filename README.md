# Stock Insight

국내 주식 투자자가 종목 데이터, 뉴스, 해석 근거, AI 인사이트를 한곳에서 보고 스스로 판단할 수 있도록 돕는 개인용 주식 리서치 비서 프로젝트입니다.

## 프로젝트 목적

이 프로젝트는 투자 판단을 대신 내리는 서비스가 아니라, 사용자가 스스로 판단할 수 있도록 근거를 구조화해 주는 도구를 목표로 합니다.

핵심 방향은 다음과 같습니다.

- 국내 주식 중심의 리서치 도구
- 가격, 뉴스, 감성, 인사이트를 한 화면에 통합
- AI 인사이트를 근거와 함께 제공
- 시간이 지난 뒤 과거 인사이트를 실제 결과와 비교해 검증
- 최근 뉴스와 이슈를 바탕으로 관심 종목 탐색 지원

## 현재 구현 상태

현재 저장소 기준 상태는 다음과 같습니다.

- 프론트엔드: Next.js 앱 기본 구조 존재
- 백엔드: FastAPI 앱 기본 구조 존재
- DB 모델: MVP 핵심 테이블 SQLAlchemy 모델 구현됨
- 마이그레이션: MVP 초기 Alembic 마이그레이션 작성됨
- API: 현재는 `GET /health` 수준의 초기 엔드포인트만 구현됨
- 설계 문서: 요구사항, 도메인, ERD, 스키마, API, 파이프라인 문서 정리 완료

즉, 현재는 "설계와 데이터 모델 기반이 정리된 상태"이며, 실제 수집 파이프라인과 조회 API를 순차적으로 구현해 나가는 단계입니다.

## 기술 스택

### Frontend

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS 4
- shadcn/ui
- lightweight-charts

### Backend

- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Redis
- Celery

### Data / Analysis

- FinanceDataReader
- feedparser
- BeautifulSoup
- Playwright
- Anthropic API

## 현재 프로젝트 구조

```text
stock-insight/
├─ frontend/
│  ├─ src/
│  │  ├─ app/
│  │  ├─ components/
│  │  └─ lib/
│  ├─ package.json
│  └─ README.md
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  │  └─ routes/
│  │  ├─ core/
│  │  ├─ db/
│  │  ├─ models/
│  │  ├─ repositories/
│  │  ├─ schemas/
│  │  ├─ services/
│  │  │  ├─ ai/
│  │  │  ├─ news/
│  │  │  └─ stock/
│  │  ├─ tasks/
│  │  └─ main.py
│  ├─ alembic/
│  │  └─ versions/
│  ├─ requirements.txt
│  └─ .env.example
├─ docs/
│  ├─ requirements.md
│  ├─ product-decisions.md
│  ├─ domain-model.md
│  ├─ erd.md
│  ├─ schema.md
│  ├─ api-spec.md
│  ├─ pipeline.md
│  ├─ claude-implementation-tasks.md
│  └─ jira-ticket-plan.md
├─ docker-compose.yml
└─ README.md
```

## 핵심 문서

설계 기준 문서는 `docs/` 아래에 정리되어 있습니다.

- [요구사항 정의서](docs/requirements.md)
- [설계 의사결정 문서](docs/product-decisions.md)
- [도메인 모델](docs/domain-model.md)
- [ERD 초안](docs/erd.md)
- [스키마 정의서](docs/schema.md)
- [API 명세 초안](docs/api-spec.md)
- [데이터 파이프라인 설계](docs/pipeline.md)
- [Claude 구현 태스크 문서](docs/claude-implementation-tasks.md)
- [Jira 티켓 계획](docs/jira-ticket-plan.md)

## 백엔드 데이터 모델

현재 MVP 기준 핵심 테이블은 아래와 같습니다.

- `stocks`
- `stock_price_daily`
- `news_articles`
- `news_article_stocks`
- `news_sentiment_runs`
- `stock_insights`
- `stock_insight_evaluations`
- `collection_jobs`
- `collection_runs`

탐색 기능에서 사용하는 `discovery_candidates`는 현재 별도 테이블이 아니라 계산형 조회 모델로 설계되어 있습니다.

## 실행 방법

### 사전 요구사항

- Node.js 18+
- Python 3.11+
- Docker

### 1. 저장소 클론

```bash
git clone https://github.com/JaeYong0107/stock-insight.git
cd stock-insight
```

### 2. PostgreSQL / Redis 실행

```bash
docker-compose up -d
```

### 3. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

기본 주소:

- `http://localhost:3000`

### 4. 백엔드 실행

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

의존성 설치:

```bash
pip install -r requirements.txt
```

환경 변수 파일 생성:

```bash
copy .env.example .env
```

또는 macOS / Linux:

```bash
cp .env.example .env
```

마이그레이션 적용:

```bash
alembic upgrade head
```

백엔드 실행:

```bash
uvicorn app.main:app --reload
```

기본 주소:

- `http://localhost:8000`

헬스 체크:

- `GET /health`

## 환경 변수

`backend/.env.example` 기준 주요 환경 변수:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/stock_insight
REDIS_URL=redis://localhost:6379/0
KIS_APP_KEY=
KIS_APP_SECRET=
KIS_ACCOUNT_NO=
ANTHROPIC_API_KEY=
```

## 현재 구현 우선순위

현재 설계 기준 구현 우선순위는 아래와 같습니다.

1. 백엔드 기본 구조 및 DB 모델 안정화
2. 종목 마스터 / 일봉 가격 수집
3. 뉴스 수집 및 뉴스-종목 매핑
4. 감성 분석 및 종목 인사이트 생성
5. 인사이트 사후 평가
6. 관심 종목 탐색 API

상세 작업 분해는 [Claude 구현 태스크 문서](docs/claude-implementation-tasks.md)와 [Jira 티켓 계획](docs/jira-ticket-plan.md)을 참고하세요.

## 커밋 규칙

```text
<type>: <subject>
```

예시 타입:

- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`

예시:

```text
feat: add stock price daily model
docs: rewrite project README
chore: add initial alembic migration
```

## 라이선스

MIT
