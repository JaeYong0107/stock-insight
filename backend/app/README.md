# Backend App Guide

## 목적

이 문서는 `backend/app` 내부 구조를 빠르게 파악하기 위한 안내 문서다.

사람이나 에이전트가 백엔드 코드를 읽을 때:

- 어디서부터 봐야 하는지
- 어떤 폴더가 어떤 역할을 하는지
- 현재 무엇이 구현되었고 무엇이 아직 비어 있는지

를 빠르게 이해할 수 있도록 만든다.

---

## 빠른 진입점

### 앱 실행 진입점

- [main.py](C:/Users/123/개발/stock-insight/backend/app/main.py)
  - FastAPI 앱 생성
  - CORS 설정
  - 현재는 `GET /health`만 구현

### 설정 진입점

- [config.py](C:/Users/123/개발/stock-insight/backend/app/core/config.py)
  - 환경 변수 및 설정 로딩

### DB 진입점

- [session.py](C:/Users/123/개발/stock-insight/backend/app/db/session.py)
  - async SQLAlchemy engine / session 구성

### 모델 진입점

- [__init__.py](C:/Users/123/개발/stock-insight/backend/app/models/__init__.py)
  - 전체 모델 re-export
- [base.py](C:/Users/123/개발/stock-insight/backend/app/models/base.py)
  - Base 및 공통 mixin

---

## 폴더 역할

### `api/`

역할:

- FastAPI 라우트 정의
- 요청/응답 흐름의 HTTP 진입점

현재 상태:

- 구조는 생성되어 있음
- 실제 기능 라우트 구현은 아직 초기 단계

### `core/`

역할:

- 설정
- 공통 애플리케이션 레벨 구성

현재 상태:

- `config.py` 구현됨

### `db/`

역할:

- DB 엔진
- 세션 팩토리
- FastAPI dependency

현재 상태:

- `session.py` 구현됨

### `models/`

역할:

- SQLAlchemy ORM 모델 정의

현재 상태:

- MVP 핵심 모델 구현됨

현재 주요 모델:

- [stock.py](C:/Users/123/개발/stock-insight/backend/app/models/stock.py)
- [stock_price_daily.py](C:/Users/123/개발/stock-insight/backend/app/models/stock_price_daily.py)
- [news_article.py](C:/Users/123/개발/stock-insight/backend/app/models/news_article.py)
- [news_article_stock.py](C:/Users/123/개발/stock-insight/backend/app/models/news_article_stock.py)
- [news_sentiment_run.py](C:/Users/123/개발/stock-insight/backend/app/models/news_sentiment_run.py)
- [stock_insight.py](C:/Users/123/개발/stock-insight/backend/app/models/stock_insight.py)
- [stock_insight_evaluation.py](C:/Users/123/개발/stock-insight/backend/app/models/stock_insight_evaluation.py)
- [collection_job.py](C:/Users/123/개발/stock-insight/backend/app/models/collection_job.py)
- [collection_run.py](C:/Users/123/개발/stock-insight/backend/app/models/collection_run.py)

### `schemas/`

역할:

- Pydantic 요청/응답 스키마

현재 상태:

- 구조만 있고 실제 API 스키마 구현은 아직 거의 없음

### `repositories/`

역할:

- DB 접근 로직 분리 계층

현재 상태:

- 구조만 있고 실제 구현은 초기 단계

### `services/`

역할:

- 비즈니스 로직
- 외부 API/수집 로직
- AI 분석 로직

하위 역할:

- `services/stock/`
- `services/news/`
- `services/ai/`

현재 상태:

- 구조는 잡혀 있음
- 실제 세부 구현은 앞으로 진행 예정

### `tasks/`

역할:

- Celery 또는 배치 실행 단위

현재 상태:

- 구조는 있음
- 실제 수집/분석 배치 작업은 앞으로 구현 예정

---

## 현재 구현 수준 요약

현재 백엔드는 아래 수준까지 준비되어 있다.

- FastAPI 앱 초기화
- 환경 변수 로딩
- async DB 세션 구성
- SQLAlchemy 모델 정의
- Alembic 마이그레이션과 연결 가능한 모델 export 구조

아직 본격 구현 전인 영역:

- 기능별 API 라우트
- Pydantic 스키마
- repository 계층
- 데이터 수집 서비스
- 감성 분석 / 인사이트 생성 서비스
- Celery 배치 작업

---

## 에이전트용 권장 읽기 순서

백엔드 코드를 처음 분석할 때 권장 순서:

1. [README.md](C:/Users/123/개발/stock-insight/README.md)
2. [docs/INDEX.md](C:/Users/123/개발/stock-insight/docs/INDEX.md)
3. [main.py](C:/Users/123/개발/stock-insight/backend/app/main.py)
4. [config.py](C:/Users/123/개발/stock-insight/backend/app/core/config.py)
5. [session.py](C:/Users/123/개발/stock-insight/backend/app/db/session.py)
6. [models/__init__.py](C:/Users/123/개발/stock-insight/backend/app/models/__init__.py)
7. 개별 모델 파일
8. 이후 `api/`, `services/`, `tasks/` 순으로 확인

---

## 구현 전 참고 문서

백엔드 구현 전에 함께 보면 좋은 문서:

- [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)
- [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)
- [claude-implementation-tasks.md](C:/Users/123/개발/stock-insight/docs/claude-implementation-tasks.md)

---

## 메모

- 현재는 레이어 구조를 먼저 잡아둔 상태다.
- 파일 수가 늘어나면 이후 도메인 기준 하위 구조로 재편이 필요할 수 있다.
- 지금 단계에서는 "빠른 구현 착수"와 "에이전트 분석 용이성" 사이의 균형을 우선한다.
