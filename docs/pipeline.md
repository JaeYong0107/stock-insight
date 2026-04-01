# Stock Insight 데이터 파이프라인 설계

## 1. 문서 목적

이 문서는 [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md), [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)를 바탕으로 MVP의 데이터 수집, 분석, 인사이트 생성, 검증 흐름을 정의한다.

목표는 다음과 같다.

- 어떤 작업이 어떤 순서로 수행되는지 정리한다.
- 각 단계의 입력과 출력 데이터를 명확히 한다.
- 정기 배치와 조회 API의 책임을 분리한다.
- Claude가 Celery 작업 또는 서비스 로직으로 구현할 기준을 만든다.

---

## 2. 전체 파이프라인 개요

MVP 기준 전체 흐름은 아래와 같다.

1. 종목 마스터 수집
2. 일봉 가격 수집
3. 뉴스 수집
4. 뉴스-종목 매핑
5. 뉴스 감성 분석
6. 종목 인사이트 생성
7. 인사이트 사후 평가
8. 탐색 후보 계산

조회 API는 위 단계를 직접 수행하지 않고, 저장된 결과 또는 계산 가능한 최신 상태를 읽는 역할을 한다.

---

## 3. 파이프라인 설계 원칙

### 3.1 수집과 조회를 분리한다

- 배치/작업은 데이터를 만든다.
- API는 만들어진 데이터를 조회한다.

이 원칙을 지키면 요청 시점마다 외부 수집이나 모델 호출을 하지 않아도 된다.

### 3.2 분석 결과는 재실행 가능해야 한다

- 감성 분석은 재실행 가능해야 한다.
- 인사이트 생성도 재실행 가능해야 한다.
- 재실행은 기존 결과를 덮지 않고 새 이력으로 쌓는다.

### 3.3 실패는 기록하고 복구 가능해야 한다

모든 주요 작업은 `collection_jobs`, `collection_runs`를 통해 상태를 기록한다.

### 3.4 탐색 후보는 파생 결과로 본다

관심 종목 탐색 결과는 별도 영속 저장보다, 최신 데이터 집계 결과로 계산하는 방식을 우선한다.

---

## 4. 단계별 상세

## 4.1 종목 마스터 수집

### 목적

국내 일반 상장 주식 목록을 최신 상태로 유지한다.

### 입력

- 외부 종목 마스터 소스

### 출력

- `stocks`

### 처리 내용

- 국내 일반 상장 주식 목록 수집
- `KOSPI`, `KOSDAQ` 필터링
- 신규 종목 insert
- 기존 종목 정보 update
- 비활성/상장폐지 상태 반영

### 주기

- 일 1회 또는 필요 시 수동 실행

### 작업 유형 예시

- `stock_master_sync`

### 실패 시 처리

- `collection_runs`에 실패 기록
- 다음 실행 시 재시도 가능

---

## 4.2 일봉 가격 수집

### 목적

종목별 일봉 가격 데이터를 최신 상태로 유지한다.

### 입력

- `stocks`
- 외부 가격 데이터 소스

### 출력

- `stock_price_daily`

### 처리 내용

- 활성 종목 대상 가격 데이터 수집
- 최근 N거래일 또는 누락 구간 보정
- `(stock_id, trade_date)` 기준 upsert 또는 중복 방지 insert

### 주기

- 장 마감 후 일 1회

### 작업 유형 예시

- `daily_price_sync`

### 실패 시 처리

- 종목 단위 실패 추적이 가능하면 `collection_runs.stock_id` 사용

---

## 4.3 뉴스 수집

### 목적

국내 주식 관련 최신 뉴스를 수집한다.

### 입력

- 외부 뉴스 소스

### 출력

- `news_articles`

### 처리 내용

- 최근 뉴스 피드 수집
- 기사 URL, 제목, 요약/본문, 출처, 발행 시각 정리
- `url` 기준 중복 방지 저장

### 주기

- 10분~1시간 간격 배치

### 작업 유형 예시

- `news_sync`

### 실패 시 처리

- 실패 소스 및 오류 메시지 기록

---

## 4.4 뉴스-종목 매핑

### 목적

수집된 뉴스와 관련 종목을 연결한다.

### 입력

- `news_articles`
- `stocks`

### 출력

- `news_article_stocks`

### 처리 내용

- 규칙 기반 또는 검색 기반으로 기사와 종목 연결
- 종목명/종목코드 매칭
- 동일 뉴스-종목 조합 중복 방지
- `mapping_method` 기록

### 주기

- 뉴스 수집 직후 후속 작업으로 실행

### 작업 유형 예시

- `news_stock_mapping`

### 비고

- 초기에는 단순 규칙 기반으로 시작
- 추후 `confidence_score` 활용 가능

---

## 4.5 뉴스 감성 분석

### 목적

뉴스 기사별 감성 결과를 생성한다.

### 입력

- `news_articles`
- 필요 시 `news_article_stocks`

### 출력

- `news_sentiment_runs`

### 처리 내용

- 새로 수집된 기사 또는 재분석 대상 기사 선택
- 기사 제목/요약/본문 기반 감성 분석 수행
- 결과를 이력으로 저장

### 주기

- 뉴스 수집 후 비동기 후속 처리

### 작업 유형 예시

- `news_sentiment_analysis`

### 재실행 정책

- 재실행 시 새 row 추가
- 최신 결과 조회는 `created_at desc` 기준

---

## 4.6 종목 인사이트 생성

### 목적

종목 기준 AI 인사이트를 생성한다.

### 입력

- `stocks`
- `stock_price_daily`
- `news_articles`
- `news_article_stocks`
- `news_sentiment_runs`

### 출력

- `stock_insights`

### 처리 내용

- 대상 종목 선정
- 최근 가격 구간 조회
- 최근 뉴스와 최신 감성 결과 집계
- AI 인사이트 생성
- 생성 시점 기준 종가와 입력 범위 저장

### 생성 트리거 후보

- 일 배치
- 특정 종목 수동 재생성
- 뉴스 급증 종목 우선 생성

### 작업 유형 예시

- `stock_insight_generation`

### MVP 권장 방식

- 초기에는 일 배치로 관심 종목 또는 상위 종목만 생성
- 모든 종목 실시간 생성은 피한다

---

## 4.7 인사이트 사후 평가

### 목적

과거 인사이트가 이후 실제 가격 흐름과 얼마나 부합했는지 계산한다.

### 입력

- `stock_insights`
- `stock_price_daily`

### 출력

- `stock_insight_evaluations`

### 처리 내용

- 평가 대상 인사이트 조회
- `7`, `30`, `90`, `180`일 구간별 기준 가격과 평가 가격 계산
- 수익률 계산
- 방향성 평가 계산
- 결과 저장

### 주기

- 일 1회 배치

### 작업 유형 예시

- `insight_evaluation`

### 재실행 정책

- `(stock_insight_id, evaluation_window_days)` 기준 upsert 또는 중복 방지

---

## 4.8 탐색 후보 계산

### 목적

최근 이슈를 바탕으로 관심 가져볼 만한 종목 후보를 계산한다.

### 입력

- `stocks`
- `stock_price_daily`
- `news_articles`
- `news_article_stocks`
- `news_sentiment_runs`

### 출력

- API 응답용 계산 결과

### 처리 내용

- 최근 N일간 종목별 뉴스 수 집계
- 뉴스 증가량 계산
- 최신 감성 분포 요약
- 최근 가격 변화율 계산
- 이유 문구 생성

### 주기

- 초기에는 조회 시 계산

### 향후 확장

- 비용이 커지면 캐시 또는 배치 사전 계산 도입 가능

---

## 5. 파이프라인 순서

권장 실행 순서는 아래와 같다.

1. `stock_master_sync`
2. `daily_price_sync`
3. `news_sync`
4. `news_stock_mapping`
5. `news_sentiment_analysis`
6. `stock_insight_generation`
7. `insight_evaluation`

탐색 후보 계산은 별도 저장 배치가 아니라 조회 레이어에서 수행한다.

---

## 6. API와 파이프라인 연결

## 6.1 종목 검색 API

사용 데이터:

- `stocks`

관련 배치:

- `stock_master_sync`

## 6.2 종목 가격 API

사용 데이터:

- `stock_price_daily`

관련 배치:

- `daily_price_sync`

## 6.3 종목 뉴스 API

사용 데이터:

- `news_articles`
- `news_article_stocks`
- 최신 `news_sentiment_runs`

관련 배치:

- `news_sync`
- `news_stock_mapping`
- `news_sentiment_analysis`

## 6.4 최신 인사이트 API

사용 데이터:

- `stock_insights`

관련 배치:

- `stock_insight_generation`

## 6.5 인사이트 평가 API

사용 데이터:

- `stock_insight_evaluations`

관련 배치:

- `insight_evaluation`

## 6.6 탐색 후보 API

사용 데이터:

- `stocks`
- `stock_price_daily`
- `news_articles`
- `news_article_stocks`
- 최신 `news_sentiment_runs`

관련 처리:

- 조회 시 계산

---

## 7. 운영 관점 체크포인트

### 7.1 최소 모니터링 항목

- 마지막 종목 마스터 수집 성공 시각
- 마지막 가격 수집 성공 시각
- 마지막 뉴스 수집 성공 시각
- 마지막 감성 분석 실행 시각
- 마지막 인사이트 생성 시각
- 마지막 평가 실행 시각

### 7.2 장애 포인트

주요 장애 가능 지점:

- 외부 가격 소스 응답 실패
- 뉴스 수집 파싱 실패
- 뉴스-종목 매핑 정확도 저하
- AI 분석 호출 실패
- 평가 시점 가격 데이터 누락

### 7.3 재처리 전략

- 수집 실패 작업은 재실행 가능해야 한다.
- 감성 분석과 인사이트 생성은 재실행 시 새 이력으로 쌓는다.
- 평가 결과는 같은 구간이면 갱신 또는 재계산 정책을 명확히 해야 한다.

---

## 8. MVP 구현 우선순위

### Phase 1

- `stock_master_sync`
- `daily_price_sync`
- `news_sync`
- `news_stock_mapping`

### Phase 2

- `news_sentiment_analysis`
- `stock_insight_generation`

### Phase 3

- `insight_evaluation`
- `discovery_candidates` 계산 로직

---

## 9. 추후 고도화 포인트

- 뉴스 매핑 품질 점수화
- 탐색 후보 캐시 또는 물질화
- 인사이트 생성 대상 종목 자동 선별
- 유튜브/외부 시황 콘텐츠 입력 확장
- 평가 결과 기반 신뢰도 집계

---

## 10. 다음 단계

설계 문서 기준으로는 핵심 골격이 갖춰졌다.

이제 다음으로 진행할 수 있는 실질 작업은 두 가지다.

1. Claude 구현용 작업 분해 문서 작성
2. 실제 SQLAlchemy 모델/Alembic 초안 구현

현재 흐름상 가장 좋은 다음 단계는 Claude가 바로 구현을 시작할 수 있도록 작업 단위를 나누는 것이다.
