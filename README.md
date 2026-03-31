# Stock Insight Dashboard

주식 데이터를 분석하고 인사이트를 도출하는 대시보드 프로젝트입니다.

## 프로젝트 개요

주가 데이터와 뉴스를 수집·분석하여 현재 키워드, 최신 동향에 기반한 주식 인사이트를 도출하고, 예측 데이터와 실제 데이터를 비교하는 대시보드입니다.

## 주요 기능

- 실시간 및 과거 주가 차트 조회 (국내/해외)
- 뉴스 스크래핑 및 감성 분석
- AI 기반 주식 인사이트 도출
- 예측 vs 실제 데이터 비교

## 기술 스택

### Frontend
- **Next.js 14** (App Router, TypeScript)
- **TailwindCSS** + **shadcn/ui**
- **TradingView Lightweight Charts** — 주식 차트

### Backend
- **FastAPI** (Python)
- **Celery** + **Redis** — 주기적 데이터 수집 스케줄링

### 데이터 수집
- **FinanceDataReader** — 국내/해외 주가 (무료)
- **한국투자증권 KIS API** — 실시간 국내 주가 (무료)
- **네이버/다음/구글 뉴스 RSS** — 뉴스
- **Playwright** — 뉴스 본문 스크래핑

### AI 분석
- **Claude API (Anthropic)** — 뉴스 감성 분석, 인사이트 도출

### Database
- **PostgreSQL** — 주가·뉴스·예측 데이터 저장
- **Redis** — 실시간 캐싱

### 배포
- **Vercel** — 프론트엔드
- **Railway** — 백엔드/DB

## 프로젝트 구조

```
stock-insight/
├── frontend/          # Next.js 14
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   └── package.json
├── backend/           # FastAPI
│   ├── app/
│   │   ├── api/       # API 라우터
│   │   ├── core/      # 설정
│   │   ├── models/    # DB 모델 (SQLAlchemy)
│   │   ├── services/  # 비즈니스 로직
│   │   │   ├── stock/ # 주가 수집
│   │   │   ├── news/  # 뉴스 스크래핑
│   │   │   └── ai/    # Claude API
│   │   └── tasks/     # Celery 태스크
│   ├── alembic/       # DB 마이그레이션
│   ├── requirements.txt
│   └── .env.example
├── docker-compose.yml # PostgreSQL + Redis
└── README.md
```

## 시작하기

### 사전 요구사항
- Node.js 18+
- Python 3.11+
- Docker

### 설치

```bash
# 저장소 클론
git clone https://github.com/JaeYong0107/stock-insight.git
cd stock-insight

# DB & Redis 실행
docker-compose up -d

# 프론트엔드
cd frontend
npm install
npm run dev

# 백엔드
cd ../backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # 환경변수 설정 후
alembic upgrade head       # DB 마이그레이션 적용
uvicorn app.main:app --reload
```

## 커밋 컨벤션

```
<type>: <subject>
```

| type | 설명 |
|------|------|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 수정 |
| `style` | 코드 포맷, 세미콜론 등 (로직 변경 없음) |
| `refactor` | 리팩토링 |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드, 패키지, 환경 설정 등 |

**예시**
```
feat: 주가 차트 컴포넌트 구현
fix: 뉴스 RSS 파싱 오류 수정
chore: 초기 개발 환경 세팅
docs: 커밋 컨벤션 추가
```

## 라이선스

MIT
