# Stock Insight ERD 초안

## 1. 문서 목적

이 문서는 [domain-model.md](C:/Users/123/개발/stock-insight/docs/domain-model.md)을 실제 데이터베이스 엔티티 관계로 구체화한 ERD 초안이다.

이 단계에서 정리하는 내용:

- 어떤 엔티티를 실제 테이블로 저장할지
- 엔티티 간 cardinality
- primary key, foreign key, unique 제약 방향
- 계산형 조회로 둘 항목과 영속 저장할 항목의 구분

---

## 2. ERD 설계 원칙

### 2.1 원천 데이터와 분석 결과를 분리한다

- 원천 데이터: 종목, 가격, 뉴스
- 분석 결과: 감성 분석, 인사이트, 인사이트 평가

이렇게 분리하면 재분석과 이력 관리가 쉬워진다.

### 2.2 탐색 기능은 초기에는 계산형 조회로 둔다

`DiscoveryCandidate`는 현재 별도 테이블로 만들지 않는다.

이유:

- 탐색 후보는 `stocks`, `news_articles`, `news_article_stocks`, `news_sentiment_runs`, `stock_price_daily`의 집계 결과로 만들 수 있다.
- 별도 테이블로 먼저 만들면 중복 저장과 갱신 정책이 필요해져 MVP 복잡도가 높아진다.

### 2.3 인사이트와 평가는 append-only로 관리한다

- `stock_insights`는 과거 스냅샷을 보존한다.
- `stock_insight_evaluations`도 평가 구간별 결과를 누적 저장한다.

---

## 3. 실제 테이블 목록

MVP 기준 실제 테이블은 아래와 같다.

- `stocks`
- `stock_price_daily`
- `news_articles`
- `news_article_stocks`
- `news_sentiment_runs`
- `stock_insights`
- `stock_insight_evaluations`
- `collection_jobs`
- `collection_runs`

계산형 또는 논리 도메인:

- `discovery_candidates`

`discovery_candidates`는 현재 DB 테이블이 아니라 API 레벨 또는 SQL 조회 레벨의 파생 결과로 본다.

---

## 4. 엔티티 관계 요약

### 4.1 핵심 관계

- `stocks` 1:N `stock_price_daily`
- `stocks` N:M `news_articles` via `news_article_stocks`
- `news_articles` 1:N `news_sentiment_runs`
- `stocks` 1:N `stock_insights`
- `stock_insights` 1:N `stock_insight_evaluations`
- `collection_jobs` 1:N `collection_runs`

### 4.2 선택 관계 후보

- `stock_insights` N:M `news_articles`

이 관계는 현재 ERD 초안에서는 보류한다.

이유:

- 인사이트 생성에 사용된 입력 뉴스 목록을 정확히 남기면 추적성이 좋아진다.
- 하지만 MVP 초기에는 입력 범위 요약만 저장해도 출발 가능하다.

이 항목은 스키마 정의서 단계에서 다시 결정한다.

---

## 5. 텍스트 ERD

```text
stocks
  ├─< stock_price_daily
  ├─< news_article_stocks >─ news_articles ─< news_sentiment_runs
  └─< stock_insights ─< stock_insight_evaluations

collection_jobs ─< collection_runs
```

---

## 6. 엔티티별 관계 상세

## 6.1 `stocks`

설명:

국내 일반 상장 주식 마스터 테이블.

주요 관계:

- 1:N `stock_price_daily`
- 1:N `news_article_stocks`
- 1:N `stock_insights`

핵심 제약:

- `symbol` 또는 종목코드는 unique
- 일반 국내 주식 범위를 벗어나는 자산은 MVP 수집 대상에서 제외

예상 PK:

- `id` bigint or uuid

추천 unique:

- `(symbol)`

---

## 6.2 `stock_price_daily`

설명:

종목별 일봉 가격 테이블.

주요 관계:

- N:1 `stocks`

핵심 제약:

- 같은 종목의 같은 거래일 가격 데이터는 1건만 존재

예상 FK:

- `stock_id -> stocks.id`

추천 unique:

- `(stock_id, trade_date)`

추천 인덱스:

- `(stock_id, trade_date desc)`

---

## 6.3 `news_articles`

설명:

뉴스 원문 메타와 요약/정제 본문을 저장하는 테이블.

주요 관계:

- 1:N `news_article_stocks`
- 1:N `news_sentiment_runs`

핵심 제약:

- 동일 URL 뉴스는 중복 저장하지 않음

예상 PK:

- `id`

추천 unique:

- `(url)`

추천 인덱스:

- `(published_at desc)`

주의:

- URL 정규화 정책이 필요할 수 있다.
- URL만으로 중복 방지가 부족하면 추후 해시 기반 중복 방지 컬럼을 추가할 수 있다.

---

## 6.4 `news_article_stocks`

설명:

뉴스와 종목의 N:M 연결 테이블.

주요 관계:

- N:1 `news_articles`
- N:1 `stocks`

핵심 제약:

- 같은 뉴스-종목 조합은 1번만 연결

예상 FK:

- `news_article_id -> news_articles.id`
- `stock_id -> stocks.id`

추천 unique:

- `(news_article_id, stock_id)`

추천 인덱스:

- `(stock_id, news_article_id)`
- `(news_article_id, stock_id)`

비고:

- `match_source` 또는 `mapping_method` 컬럼을 두면 수동/규칙/검색 기반 연결을 추적할 수 있다.

---

## 6.5 `news_sentiment_runs`

설명:

뉴스 기사에 대한 감성 분석 실행 이력 테이블.

주요 관계:

- N:1 `news_articles`

핵심 제약:

- append-only 이력 모델
- 같은 기사에 대해 여러 번 실행될 수 있음

예상 FK:

- `news_article_id -> news_articles.id`

추천 인덱스:

- `(news_article_id, created_at desc)`

선택 unique:

- 강한 unique 제약은 두지 않음

이유:

- 동일 기사에 대해 같은 날 재분석할 수도 있기 때문이다.

---

## 6.6 `stock_insights`

설명:

종목별 AI 인사이트 스냅샷 테이블.

주요 관계:

- N:1 `stocks`
- 1:N `stock_insight_evaluations`

핵심 제약:

- append-only 스냅샷
- 과거 결과 보존

예상 FK:

- `stock_id -> stocks.id`

추천 인덱스:

- `(stock_id, created_at desc)`

선택 unique:

- 강한 unique 제약은 두지 않음

이유:

- 같은 종목에 대해 같은 날 여러 버전 생성 가능성을 열어둔다.

---

## 6.7 `stock_insight_evaluations`

설명:

인사이트 사후 평가 테이블.

주요 관계:

- N:1 `stock_insights`

핵심 제약:

- 같은 인사이트에 대해 같은 평가 구간은 1건만 존재

예상 FK:

- `stock_insight_id -> stock_insights.id`

추천 unique:

- `(stock_insight_id, evaluation_window_days)`

추천 인덱스:

- `(stock_insight_id, evaluation_window_days)`
- `(evaluated_at)`

비고:

- `evaluation_window_days`는 `7`, `30`, `90`, `180`을 사용

---

## 6.8 `collection_jobs`

설명:

정기 실행 작업 정의 테이블.

주요 관계:

- 1:N `collection_runs`

예상 PK:

- `id`

추천 unique:

- `(job_name)`

비고:

- 작업 유형 예: `stock_master_sync`, `daily_price_sync`, `news_sync`, `news_sentiment_analysis`, `stock_insight_generation`, `insight_evaluation`

---

## 6.9 `collection_runs`

설명:

작업 실행 이력 테이블.

주요 관계:

- N:1 `collection_jobs`

예상 FK:

- `collection_job_id -> collection_jobs.id`

추천 인덱스:

- `(collection_job_id, started_at desc)`
- `(status, started_at desc)`

선택 확장:

- 특정 종목 대상 실행을 추적하려면 `stock_id` nullable FK를 둘 수 있다.

이 항목은 스키마 단계에서 확정한다.

---

## 7. `discovery_candidates` 처리 방안

현재 결정:

- 별도 테이블로 만들지 않는다.
- 탐색 API에서 집계 조회로 계산한다.

초기 계산 입력:

- 최근 N일간 뉴스 수
- 특정 종목의 뉴스 증가량
- 최근 가격 변화율
- 감성 요약 결과

초기 출력 예:

- `stock_id`
- `stock_name`
- `reason_summary`
- `news_count_7d`
- `price_change_7d`
- `top_keywords`

향후 테이블화가 필요한 경우:

- 후보 결과를 저장해 랭킹 이력을 남겨야 할 때
- 배치 생성 비용이 커질 때
- 추천 품질 평가를 따로 관리해야 할 때

---

## 8. 보류 중인 구조 결정

아래는 아직 ERD 초안에서 열어둔 항목이다.

### 8.1 인사이트 입력 뉴스 연결 테이블

후보:

- `stock_insight_news_articles`

장점:

- 어떤 뉴스로 인사이트가 만들어졌는지 추적 가능

단점:

- MVP 초기 구현 복잡도 증가

현재 판단:

- 스키마 단계에서 재검토

### 8.2 작업 실행 대상 추적

후보:

- `collection_runs.stock_id`

장점:

- 특정 종목 단위 실패 추적 가능

단점:

- 범용 작업과의 일관성 설계가 필요

현재 판단:

- 스키마 단계에서 재검토

---

## 9. 다음 단계

다음 문서는 `schema.md`다.

거기서는 각 테이블별 컬럼, 타입, nullable, 기본값, 인덱스, 제약조건을 구체적으로 정의한다.
