# Claude 구현 태스크 문서

## 1. 문서 목적

이 문서는 지금까지 작성된 설계 문서를 바탕으로 Claude가 실제 구현을 진행할 수 있도록 작업 단위를 분해한 실행 문서다.

이 문서의 역할:

- 구현 순서를 고정한다.
- 각 작업이 어떤 설계 문서를 근거로 하는지 연결한다.
- 완료 여부를 체크할 수 있게 한다.
- 문서 곳곳에 흩어진 보류/후속 작업을 중앙에서 추적한다.

---

## 2. 추적 방식

### 2.1 지금까지 각 문서의 "추후 작업"은 추적 가능한가

가능하다. 이미 각 문서에 보류 항목과 다음 단계가 남아 있어서 잃어버리지는 않는다.

하지만 문서가 많아질수록 다음 문제가 생길 수 있다.

- 같은 보류 항목이 여러 문서에 중복 기록됨
- 어떤 항목이 실제 구현 대상인지 한눈에 보기 어려움
- 완료 여부를 문서마다 따로 확인해야 함

그래서 앞으로는 다음 원칙으로 관리한다.

- 요구사항 기준: [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)
- 설계 기준: 각 설계 문서
- 실행 추적 기준: 이 문서

즉, 앞으로 Claude 구현 진행 상황은 이 문서를 기준으로 체크하는 것이 좋다.

---

## 3. 구현 원칙

- 요구사항 변경이 아니면 [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)를 직접 수정하지 않는다.
- 구현 전에는 해당 작업의 근거 문서를 먼저 확인한다.
- 완료 시에는 이 문서 체크박스를 먼저 갱신한다.
- 설계와 구현이 충돌하면 코드보다 문서를 우선 확인한다.

---

## 4. 문서별 근거 맵

- 제품 요구사항: [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)
- 설계 정책: [product-decisions.md](C:/Users/123/개발/stock-insight/docs/product-decisions.md)
- 도메인 정의: [domain-model.md](C:/Users/123/개발/stock-insight/docs/domain-model.md)
- ERD: [erd.md](C:/Users/123/개발/stock-insight/docs/erd.md)
- 스키마: [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
- API 계약: [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
- 파이프라인: [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)

---

## 5. 구현 Phase

## Phase 1. 프로젝트 기본 구조

### 목표

백엔드가 이후 기능 구현을 받을 수 있는 기본 구조를 갖춘다.

### 작업

- [ ] FastAPI 라우터 구조 정리
- [ ] `api`, `schemas`, `models`, `services`, `repositories`, `tasks` 디렉터리 구조 확정
- [ ] 설정 파일과 환경 변수 로딩 구조 정리
- [ ] DB 세션/엔진 구성
- [ ] Alembic 초기 설정 점검

### 근거 문서

- [product-decisions.md](C:/Users/123/개발/stock-insight/docs/product-decisions.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)

---

## Phase 2. DB 모델 및 마이그레이션

### 목표

핵심 스키마를 실제 코드로 옮긴다.

### 작업

- [ ] `stocks` SQLAlchemy 모델 구현
- [ ] `stock_price_daily` SQLAlchemy 모델 구현
- [ ] `news_articles` SQLAlchemy 모델 구현
- [ ] `news_article_stocks` SQLAlchemy 모델 구현
- [ ] `news_sentiment_runs` SQLAlchemy 모델 구현
- [ ] `stock_insights` SQLAlchemy 모델 구현
- [ ] `stock_insight_evaluations` SQLAlchemy 모델 구현
- [ ] `collection_jobs` SQLAlchemy 모델 구현
- [ ] `collection_runs` SQLAlchemy 모델 구현
- [ ] Alembic 마이그레이션 생성
- [ ] 제약조건/인덱스 반영 검증

### 근거 문서

- [erd.md](C:/Users/123/개발/stock-insight/docs/erd.md)
- [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)

---

## Phase 3. 종목 마스터 및 가격 수집

### 목표

종목과 가격 데이터가 실제로 저장되고 조회 가능해야 한다.

### 작업

- [ ] 종목 마스터 수집 서비스 구현
- [ ] 종목 마스터 동기화 작업 구현
- [ ] 일봉 가격 수집 서비스 구현
- [ ] 일봉 가격 동기화 작업 구현
- [ ] `collection_jobs`, `collection_runs` 연동
- [ ] 수집 실패/재시도 기록 처리

### 근거 문서

- [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)

---

## Phase 4. 뉴스 수집 및 매핑

### 목표

뉴스를 수집하고 종목과 연결한다.

### 작업

- [ ] 뉴스 수집 서비스 구현
- [ ] 뉴스 중복 방지 저장 구현
- [ ] 뉴스-종목 매핑 로직 구현
- [ ] `mapping_method` 기록 처리
- [ ] 뉴스 수집/매핑 작업을 `collection_runs`와 연결

### 근거 문서

- [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)

---

## Phase 5. 조회 API 1차

### 목표

MVP 기본 조회 API를 제공한다.

### 작업

- [ ] `GET /health`
- [ ] `GET /stocks/search`
- [ ] `GET /stocks/{stock_id}`
- [ ] `GET /stocks/{stock_id}/prices`
- [ ] `GET /stocks/{stock_id}/news`
- [ ] Pydantic 응답 스키마 정의
- [ ] 공통 에러 응답 포맷 적용

### 근거 문서

- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)

---

## Phase 6. 감성 분석

### 목표

뉴스 기사별 감성 결과를 생성하고 최신 결과를 조회에 반영한다.

### 작업

- [ ] 감성 분석 서비스 인터페이스 구현
- [ ] 감성 분석 실행 작업 구현
- [ ] `news_sentiment_runs` append-only 저장 구현
- [ ] 종목 뉴스 조회 시 최신 감성 결과 join 로직 구현

### 근거 문서

- [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)
- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)

---

## Phase 7. 인사이트 생성 및 조회

### 목표

종목 기준 인사이트를 생성하고 조회할 수 있어야 한다.

### 작업

- [ ] 인사이트 생성 서비스 구현
- [ ] 인사이트 생성 작업 구현
- [ ] `stock_insights` 스냅샷 저장 구현
- [ ] `GET /stocks/{stock_id}/insights/latest`
- [ ] `GET /stocks/{stock_id}/insights`

### 근거 문서

- [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)

---

## Phase 8. 사후 평가

### 목표

과거 인사이트를 실제 가격 흐름과 비교할 수 있어야 한다.

### 작업

- [ ] 인사이트 평가 로직 구현
- [ ] `7`, `30`, `90`, `180`일 평가 배치 구현
- [ ] `stock_insight_evaluations` 저장 구현
- [ ] `GET /insights/{insight_id}/evaluations`

### 근거 문서

- [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)

---

## Phase 9. 관심 종목 탐색

### 목표

최근 뉴스/이슈 기반 관심 종목 후보를 조회할 수 있어야 한다.

### 작업

- [ ] 탐색 후보 계산 쿼리 또는 서비스 구현
- [ ] `reason_summary` 생성 규칙 구현
- [ ] `GET /discovery/candidates`
- [ ] 시장 필터/기간 필터 반영

### 근거 문서

- [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)
- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)

---

## Phase 10. 종목 상세 편의 API 및 통합 점검

### 목표

프론트가 종목 상세 화면을 쉽게 붙일 수 있게 한다.

### 작업

- [ ] `GET /stocks/{stock_id}/summary` 구현 여부 결정
- [ ] 필요 시 summary API 구현
- [ ] 조회 성능 점검
- [ ] 인덱스 및 쿼리 튜닝 1차 적용

### 근거 문서

- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
- [erd.md](C:/Users/123/개발/stock-insight/docs/erd.md)

---

## 6. 문서별 후속 작업 추적

## 6.1 `requirements.md`

- [ ] 각 요구사항 체크박스를 구현 완료 시점에 반영할 운영 방식 결정
- [ ] MVP 범위 이후 Phase 5 고도화 항목을 언제 백로그로 분리할지 결정

## 6.2 `product-decisions.md`

- [ ] 종목 메타데이터 필드 범위 최종 확정
- [ ] 뉴스-종목 연결 방식 고도화 여부 결정
- [ ] 인사이트 입력 뉴스 명시 연결 필요 여부 결정

## 6.3 `domain-model.md`

- [ ] `DiscoveryCandidate`를 계속 계산형으로 둘지 추후 테이블화할지 판단

## 6.4 `erd.md`

- [ ] `stock_insights`와 `news_articles` 연결 테이블 추가 여부 결정
- [ ] `collection_runs.stock_id` 유지 여부 최종 확정

## 6.5 `schema.md`

- [ ] `news_articles` 중복 방지 강화 정책 검토
- [ ] `is_direction_match`를 안정적으로 계산하기 위한 인사이트 포맷 확정

## 6.6 `api-spec.md`

- [ ] 정렬 방식과 페이지네이션 세부 규칙 확정
- [ ] `summary` API를 실제 구현 대상으로 둘지 결정

## 6.7 `pipeline.md`

- [ ] 인사이트 생성 대상 종목 선정 규칙 구체화
- [ ] 탐색 후보 계산 캐시 필요 여부 검토

---

## 7. Claude에게 바로 넘길 1차 작업 묶음

가장 먼저 구현 시작하기 좋은 묶음은 아래다.

### Bundle A

- [ ] 프로젝트 구조 정리
- [ ] DB 세션/엔진 구성
- [ ] SQLAlchemy 모델 구현
- [ ] Alembic 초기 마이그레이션 작성

### Bundle B

- [ ] 종목 마스터 수집
- [ ] 가격 수집
- [ ] 종목/가격 조회 API

### Bundle C

- [ ] 뉴스 수집
- [ ] 뉴스-종목 매핑
- [ ] 뉴스 조회 API

### Bundle D

- [ ] 감성 분석
- [ ] 인사이트 생성
- [ ] 인사이트 조회 API

### Bundle E

- [ ] 인사이트 평가
- [ ] 탐색 후보 API

---

## 8. 추천 전달 방식

Claude에게는 아래 순서로 전달하는 것이 좋다.

1. 이 문서를 먼저 공유한다.
2. 이번 턴에서 구현할 Bundle을 하나 고른다.
3. Claude가 작업을 끝내면 이 문서 체크박스를 갱신한다.
4. 설계 충돌이 생기면 관련 설계 문서를 먼저 다시 확인한다.

---

## 9. 다음 단계

지금 시점에서 가장 자연스러운 다음 액션은 아래 둘 중 하나다.

1. Claude에게 `Bundle A`부터 구현 시작시키기
2. 내가 이 문서를 바탕으로 Jira 티켓 형식까지 쪼개주기
