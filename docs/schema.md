# Stock Insight 스키마 정의서

## 1. 문서 목적

이 문서는 [erd.md](C:/Users/123/개발/stock-insight/docs/erd.md)를 바탕으로 MVP 대상 테이블의 컬럼, 타입, nullable, 기본값, 인덱스, 제약조건을 구체화한다.

이 문서는 구현 직전 단계의 기준 문서이며, 이후 SQLAlchemy 모델과 Alembic 마이그레이션은 이 문서를 기준으로 작성한다.

---

## 2. 공통 규칙

### 2.1 PK 정책

- 모든 테이블의 기본키는 `bigint` 기반 surrogate key를 사용한다.
- 컬럼명은 `id`로 통일한다.

### 2.2 시간 컬럼 정책

- 시간 컬럼은 모두 timezone-aware `timestamp`를 사용한다.
- 공통 생성 시각 컬럼은 `created_at`을 사용한다.
- 수정 시각이 필요한 경우 `updated_at`을 둔다.

### 2.3 문자열 정책

- 코드성 값은 `varchar`
- 긴 텍스트는 `text`

### 2.4 enum 정책

- 초기 구현에서는 DB native enum보다 문자열 + 애플리케이션 검증을 우선 검토한다.
- 이유는 마이그레이션 유연성을 높이기 위해서다.

### 2.5 금액/수치 정책

- 주가 데이터는 `numeric(18, 4)`를 기본으로 사용한다.
- 거래량은 `bigint`를 사용한다.
- 수익률/변화율은 `numeric(8, 4)`를 사용한다.

### 2.6 삭제 정책

- MVP에서는 물리 삭제보다 비활성화 또는 이력 보존을 우선한다.
- FK 삭제 정책은 기본적으로 `RESTRICT` 또는 `NO ACTION` 성격을 선호한다.

---

## 3. 테이블 정의

## 3.1 `stocks`

설명:

국내 일반 상장 주식 마스터.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `symbol` | varchar(16) | N |  | 종목코드 |
| `name` | varchar(200) | N |  | 종목명 |
| `market` | varchar(20) | N |  | `KOSPI`, `KOSDAQ` |
| `status` | varchar(20) | N | `'active'` | `active`, `inactive`, `delisted` |
| `listed_at` | date | Y |  | 상장일 |
| `delisted_at` | date | Y |  | 상장폐지일 |
| `created_at` | timestamptz | N | now() | 생성 시각 |
| `updated_at` | timestamptz | N | now() | 수정 시각 |

### 제약조건

- PK: `id`
- UK: `symbol`
- CHECK 후보: `market in ('KOSPI', 'KOSDAQ')`

### 인덱스

- unique index on `symbol`
- index on `(market, status)`
- index on `name`

### 비고

- 추후 영문명, 섹터, 업종 코드 등은 확장 컬럼으로 추가 가능

---

## 3.2 `stock_price_daily`

설명:

종목별 일봉 가격 데이터.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `stock_id` | bigint | N |  | FK to `stocks.id` |
| `trade_date` | date | N |  | 거래일 |
| `open_price` | numeric(18, 4) | N |  | 시가 |
| `high_price` | numeric(18, 4) | N |  | 고가 |
| `low_price` | numeric(18, 4) | N |  | 저가 |
| `close_price` | numeric(18, 4) | N |  | 종가 |
| `volume` | bigint | N |  | 거래량 |
| `source` | varchar(50) | N |  | 수집 소스 |
| `collected_at` | timestamptz | N | now() | 수집 시각 |
| `created_at` | timestamptz | N | now() | 생성 시각 |

### 제약조건

- PK: `id`
- FK: `stock_id -> stocks.id`
- UK: `(stock_id, trade_date)`

### 인덱스

- unique index on `(stock_id, trade_date)`
- index on `(stock_id, trade_date desc)`
- index on `trade_date`

### 비고

- 조정주가 필요 시 추후 별도 컬럼 또는 별도 정책 추가 가능

---

## 3.3 `news_articles`

설명:

뉴스 기사 메타데이터 및 분석용 본문/요약.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `source_name` | varchar(100) | N |  | 언론사/출처 |
| `source_type` | varchar(50) | N | `'news'` | 콘텐츠 유형 |
| `title` | varchar(500) | N |  | 기사 제목 |
| `summary` | text | Y |  | 기사 요약 |
| `body_text` | text | Y |  | 정제 본문 |
| `url` | text | N |  | 원문 URL |
| `url_hash` | varchar(64) | Y |  | URL 정규화 해시 |
| `published_at` | timestamptz | N |  | 기사 발행 시각 |
| `collected_at` | timestamptz | N | now() | 수집 시각 |
| `created_at` | timestamptz | N | now() | 생성 시각 |

### 제약조건

- PK: `id`
- UK: `url`

### 인덱스

- unique index on `url`
- index on `published_at desc`
- index on `source_name`

### 비고

- `url_hash`는 추후 URL 정규화 중복 방지 강화용
- 현재는 `url` unique로 시작

---

## 3.4 `news_article_stocks`

설명:

뉴스 기사와 종목의 연결 테이블.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `news_article_id` | bigint | N |  | FK to `news_articles.id` |
| `stock_id` | bigint | N |  | FK to `stocks.id` |
| `mapping_method` | varchar(30) | N | `'rule'` | `rule`, `search`, `manual`, `ai` |
| `confidence_score` | numeric(5, 4) | Y |  | 연결 신뢰도 |
| `created_at` | timestamptz | N | now() | 생성 시각 |

### 제약조건

- PK: `id`
- FK: `news_article_id -> news_articles.id`
- FK: `stock_id -> stocks.id`
- UK: `(news_article_id, stock_id)`

### 인덱스

- unique index on `(news_article_id, stock_id)`
- index on `(stock_id, news_article_id)`
- index on `(news_article_id, stock_id)`

### 비고

- `confidence_score`는 초기엔 nullable로 두고, 향후 AI 또는 스코어 기반 연결 시 활용

---

## 3.5 `news_sentiment_runs`

설명:

뉴스 기사 감성 분석 실행 이력.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `news_article_id` | bigint | N |  | FK to `news_articles.id` |
| `sentiment` | varchar(20) | N |  | `positive`, `neutral`, `negative` |
| `reason_summary` | text | Y |  | 감성 근거 요약 |
| `provider` | varchar(50) | Y |  | 모델 공급자 |
| `model_name` | varchar(100) | Y |  | 사용 모델명 |
| `prompt_version` | varchar(50) | Y |  | 프롬프트 버전 |
| `raw_response` | text | Y |  | 원문 응답 저장 옵션 |
| `created_at` | timestamptz | N | now() | 실행 시각 |

### 제약조건

- PK: `id`
- FK: `news_article_id -> news_articles.id`

### 인덱스

- index on `(news_article_id, created_at desc)`
- index on `(sentiment, created_at desc)`

### 비고

- 이력 보존이 목적이므로 강한 unique 제약은 두지 않음

---

## 3.6 `stock_insights`

설명:

종목 기준 AI 인사이트 스냅샷.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `stock_id` | bigint | N |  | FK to `stocks.id` |
| `headline` | varchar(300) | Y |  | 한 줄 요약 제목 |
| `summary` | text | N |  | 종합 인사이트 본문 |
| `thesis` | text | Y |  | 핵심 주장 |
| `evidence_summary` | text | Y |  | 근거 요약 |
| `input_price_from_date` | date | Y |  | 가격 데이터 시작일 |
| `input_price_to_date` | date | Y |  | 가격 데이터 종료일 |
| `input_news_from_at` | timestamptz | Y |  | 뉴스 입력 시작 시각 |
| `input_news_to_at` | timestamptz | Y |  | 뉴스 입력 종료 시각 |
| `reference_close_price` | numeric(18, 4) | N |  | 생성 시점 기준 종가 |
| `provider` | varchar(50) | Y |  | 모델 공급자 |
| `model_name` | varchar(100) | Y |  | 사용 모델명 |
| `prompt_version` | varchar(50) | Y |  | 프롬프트 버전 |
| `created_at` | timestamptz | N | now() | 생성 시각 |

### 제약조건

- PK: `id`
- FK: `stock_id -> stocks.id`

### 인덱스

- index on `(stock_id, created_at desc)`
- index on `created_at desc`

### 비고

- 인사이트는 append-only 스냅샷으로 저장
- 추후 입력 뉴스 명시 연결이 필요하면 조인 테이블 추가

---

## 3.7 `stock_insight_evaluations`

설명:

인사이트 사후 평가 결과.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `stock_insight_id` | bigint | N |  | FK to `stock_insights.id` |
| `evaluation_window_days` | integer | N |  | `7`, `30`, `90`, `180` |
| `baseline_date` | date | N |  | 기준 가격 일자 |
| `baseline_close_price` | numeric(18, 4) | N |  | 기준 종가 |
| `evaluation_date` | date | N |  | 평가 가격 일자 |
| `evaluation_close_price` | numeric(18, 4) | N |  | 평가 종가 |
| `price_change_rate` | numeric(8, 4) | N |  | 수익률/변화율 |
| `direction_label` | varchar(20) | N |  | `up`, `down`, `flat` |
| `is_direction_match` | boolean | Y |  | 방향성 적중 여부 |
| `evaluated_at` | timestamptz | N | now() | 평가 수행 시각 |
| `created_at` | timestamptz | N | now() | 생성 시각 |

### 제약조건

- PK: `id`
- FK: `stock_insight_id -> stock_insights.id`
- UK: `(stock_insight_id, evaluation_window_days)`

### 인덱스

- unique index on `(stock_insight_id, evaluation_window_days)`
- index on `evaluated_at desc`

### 비고

- `is_direction_match`는 인사이트 안에 방향성 판단 결과가 있을 때만 채울 수 있으므로 nullable 허용

---

## 3.8 `collection_jobs`

설명:

정기 실행 작업 정의.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `job_name` | varchar(100) | N |  | 작업명 |
| `job_type` | varchar(50) | N |  | 작업 유형 |
| `is_active` | boolean | N | true | 활성 여부 |
| `schedule_expr` | varchar(100) | Y |  | 크론 또는 스케줄 표현식 |
| `description` | text | Y |  | 설명 |
| `created_at` | timestamptz | N | now() | 생성 시각 |
| `updated_at` | timestamptz | N | now() | 수정 시각 |

### 제약조건

- PK: `id`
- UK: `job_name`

### 인덱스

- unique index on `job_name`
- index on `(job_type, is_active)`

---

## 3.9 `collection_runs`

설명:

작업 실행 이력.

### 컬럼

| 컬럼명 | 타입 | Null | 기본값 | 설명 |
|---|---|---|---|---|
| `id` | bigint | N | identity | PK |
| `collection_job_id` | bigint | N |  | FK to `collection_jobs.id` |
| `stock_id` | bigint | Y |  | 선택적 FK to `stocks.id` |
| `status` | varchar(20) | N |  | `pending`, `running`, `success`, `failed` |
| `started_at` | timestamptz | N | now() | 시작 시각 |
| `finished_at` | timestamptz | Y |  | 종료 시각 |
| `processed_count` | integer | Y |  | 처리 건수 |
| `error_message` | text | Y |  | 오류 메시지 |
| `created_at` | timestamptz | N | now() | 생성 시각 |

### 제약조건

- PK: `id`
- FK: `collection_job_id -> collection_jobs.id`
- FK: `stock_id -> stocks.id`

### 인덱스

- index on `(collection_job_id, started_at desc)`
- index on `(status, started_at desc)`
- index on `(stock_id, started_at desc)`

### 비고

- `stock_id`는 종목 단위 작업 추적용으로 nullable 허용

---

## 4. 계산형 조회 모델

## 4.1 `discovery_candidates`

현재 결정:

- 실제 테이블로 만들지 않는다.
- API 또는 조회 쿼리에서 계산한다.

예상 출력 필드:

- `stock_id`
- `symbol`
- `stock_name`
- `market`
- `reason_summary`
- `news_count_7d`
- `price_change_rate_7d`
- `top_keywords`

기반 테이블:

- `stocks`
- `stock_price_daily`
- `news_articles`
- `news_article_stocks`
- `news_sentiment_runs`

---

## 5. 보류 항목

### 5.1 `stock_insight_news_articles`

보류 이유:

- 인사이트 생성 시 실제 사용한 뉴스 목록을 명시적으로 남기면 좋지만, MVP 초기에는 구현 복잡도를 줄이기 위해 보류한다.

### 5.2 `news_articles` 중복 방지 강화

현재는 `url` unique로 시작하지만, 추후 아래 보완이 필요할 수 있다.

- 정규화 URL 기준 unique
- 제목+발행시각 해시
- 본문 해시

### 5.3 방향성 평가 기준

`stock_insight_evaluations.is_direction_match`를 안정적으로 사용하려면, 인사이트 생성 결과에 방향성 구조화 필드가 필요할 수 있다.

현재는 nullable로 두고 추후 API/인사이트 포맷 설계 단계에서 확정한다.

---

## 6. 다음 단계

다음 문서는 `api-spec.md` 또는 `pipeline.md`로 이어질 수 있다.

추천 순서:

1. `api-spec.md`
2. `pipeline.md`

이유:

- 프론트/백엔드 계약을 먼저 고정하면 구현 착수가 쉬워진다.
- 이후 파이프라인 설계가 API와 저장 구조를 더 자연스럽게 따른다.
