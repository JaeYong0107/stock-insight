# Stock Insight API 명세 초안

## 1. 문서 목적

이 문서는 [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md), [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)를 바탕으로 MVP에서 필요한 백엔드 API 계약을 정의한다.

목표는 다음과 같다.

- 프론트엔드와 백엔드의 책임을 명확히 나눈다.
- 조회 중심 MVP에 필요한 엔드포인트를 먼저 고정한다.
- Claude가 FastAPI 라우트와 응답 스키마를 구현할 수 있도록 기준을 만든다.

---

## 2. API 설계 원칙

### 2.1 MVP는 조회 API 우선

MVP 단계에서는 사용자가 보는 화면을 우선 지원한다.

우선순위:

- 종목 검색
- 관심 종목 탐색
- 종목 상세 조회
- 가격 조회
- 뉴스 조회
- 인사이트 조회
- 인사이트 검증 조회

### 2.2 최신값과 이력을 구분한다

- 감성 분석: 기사 목록에서는 최신 결과 중심
- 인사이트: 종목 상세에서는 최신 결과 중심, 필요 시 이력 조회 분리

### 2.3 대형 단일 응답보다 화면 단위 조합을 선호한다

종목 상세 화면에 필요한 데이터를 전부 한 번에 주는 거대한 API보다, 아래처럼 나누는 방식을 우선한다.

- 기본 정보
- 가격 데이터
- 뉴스 목록
- 최신 인사이트
- 인사이트 평가

단, 프론트 편의를 위해 종목 상세 summary API는 제공할 수 있다.

### 2.4 탐색 제안은 추천이 아니라 설명 가능한 후보 제안이어야 한다

관심 종목 제안 API는 점수만 반환하지 않고, 반드시 근거 요약을 함께 제공해야 한다.

---

## 3. 공통 규칙

### 3.1 Base URL

초기 기준:

- `/api/v1`

### 3.2 응답 형식

기본적으로 JSON 응답을 사용한다.

성공 예시:

```json
{
  "data": {}
}
```

목록 응답 예시:

```json
{
  "data": [],
  "meta": {
    "total": 0
  }
}
```

에러 응답 예시:

```json
{
  "error": {
    "code": "stock_not_found",
    "message": "Stock not found"
  }
}
```

### 3.3 날짜/시간 규칙

- 날짜: `YYYY-MM-DD`
- 시간: ISO 8601 string

### 3.4 페이지네이션

목록 API는 기본적으로 아래 파라미터를 지원한다.

- `limit`
- `offset`

필요 시 추후 cursor pagination으로 변경 가능하다.

---

## 4. 엔드포인트 목록

MVP 기준 추천 엔드포인트:

- `GET /health`
- `GET /stocks/search`
- `GET /stocks/{stock_id}`
- `GET /stocks/{stock_id}/prices`
- `GET /stocks/{stock_id}/news`
- `GET /stocks/{stock_id}/insights/latest`
- `GET /stocks/{stock_id}/insights`
- `GET /insights/{insight_id}/evaluations`
- `GET /discovery/candidates`

선택 추가:

- `GET /stocks/{stock_id}/summary`

---

## 5. 상세 명세

## 5.1 `GET /health`

설명:

서버 상태 확인.

### 응답

```json
{
  "data": {
    "status": "ok"
  }
}
```

---

## 5.2 `GET /stocks/search`

설명:

종목명 또는 종목코드로 종목 검색.

### Query Params

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `query` | string | Y | 종목명 또는 종목코드 |
| `market` | string | N | `KOSPI`, `KOSDAQ` |
| `limit` | integer | N | 기본 20 |
| `offset` | integer | N | 기본 0 |

### 응답 예시

```json
{
  "data": [
    {
      "id": 1,
      "symbol": "005930",
      "name": "삼성전자",
      "market": "KOSPI",
      "status": "active"
    }
  ],
  "meta": {
    "total": 1,
    "limit": 20,
    "offset": 0
  }
}
```

### 비고

- 초기 검색은 prefix/contains 기반으로 시작 가능

---

## 5.3 `GET /stocks/{stock_id}`

설명:

종목 기본 정보 조회.

### Path Params

| 이름 | 타입 | 설명 |
|---|---|---|
| `stock_id` | integer | 종목 PK |

### 응답 예시

```json
{
  "data": {
    "id": 1,
    "symbol": "005930",
    "name": "삼성전자",
    "market": "KOSPI",
    "status": "active",
    "listed_at": "1975-06-11"
  }
}
```

---

## 5.4 `GET /stocks/{stock_id}/prices`

설명:

종목 일봉 가격 조회.

### Query Params

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `from_date` | date | N | 시작일 |
| `to_date` | date | N | 종료일 |
| `limit` | integer | N | 기본 100 |

### 응답 예시

```json
{
  "data": [
    {
      "trade_date": "2026-03-31",
      "open_price": 70100.0,
      "high_price": 71500.0,
      "low_price": 69900.0,
      "close_price": 71200.0,
      "volume": 12345678
    }
  ]
}
```

### 비고

- 기본 정렬은 최신일 내림차순 또는 차트용 오름차순 중 하나로 고정해야 함
- 프론트 차트 사용성을 위해 오름차순 반환이 더 자연스러움

---

## 5.5 `GET /stocks/{stock_id}/news`

설명:

종목 관련 뉴스 목록 조회.

### Query Params

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `limit` | integer | N | 기본 20 |
| `offset` | integer | N | 기본 0 |
| `from_at` | datetime | N | 시작 시각 |
| `to_at` | datetime | N | 종료 시각 |

### 응답 예시

```json
{
  "data": [
    {
      "id": 101,
      "title": "삼성전자, AI 반도체 수요 확대 기대",
      "summary": "AI 수요 확대와 관련한 기대가 반영됐다.",
      "source_name": "연합뉴스",
      "url": "https://example.com/news/1",
      "published_at": "2026-03-31T09:00:00+09:00",
      "sentiment": {
        "label": "positive",
        "reason_summary": "수요 확대 기대가 긍정적으로 해석됨"
      }
    }
  ],
  "meta": {
    "total": 1,
    "limit": 20,
    "offset": 0
  }
}
```

### 비고

- 기사 카드에는 최신 감성 결과 1건만 포함
- 전체 감성 이력은 별도 API가 필요해질 때 확장

---

## 5.6 `GET /stocks/{stock_id}/insights/latest`

설명:

종목 최신 인사이트 1건 조회.

### 응답 예시

```json
{
  "data": {
    "id": 501,
    "headline": "반도체 수요 회복 기대가 유효함",
    "summary": "최근 가격 흐름과 뉴스 기준으로...",
    "thesis": "단기적으로는 수요 기대가 주가 해석의 핵심이다.",
    "evidence_summary": "최근 7일 뉴스 증가, 긍정 기사 비중 상승",
    "reference_close_price": 71200.0,
    "created_at": "2026-03-31T18:00:00+09:00",
    "model": {
      "provider": "anthropic",
      "name": "claude-x"
    }
  }
}
```

### 비고

- 모델 정보는 사용자 노출 여부와 무관하게 응답에 포함 가능

---

## 5.7 `GET /stocks/{stock_id}/insights`

설명:

종목 인사이트 이력 조회.

### Query Params

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `limit` | integer | N | 기본 20 |
| `offset` | integer | N | 기본 0 |

### 응답 예시

```json
{
  "data": [
    {
      "id": 501,
      "headline": "반도체 수요 회복 기대가 유효함",
      "reference_close_price": 71200.0,
      "created_at": "2026-03-31T18:00:00+09:00"
    }
  ],
  "meta": {
    "total": 1,
    "limit": 20,
    "offset": 0
  }
}
```

---

## 5.8 `GET /insights/{insight_id}/evaluations`

설명:

인사이트 사후 검증 결과 조회.

### 응답 예시

```json
{
  "data": [
    {
      "evaluation_window_days": 7,
      "baseline_date": "2026-03-31",
      "baseline_close_price": 71200.0,
      "evaluation_date": "2026-04-07",
      "evaluation_close_price": 72400.0,
      "price_change_rate": 1.6854,
      "direction_label": "up",
      "is_direction_match": true
    }
  ]
}
```

### 비고

- 응답은 `evaluation_window_days` 오름차순 정렬 권장

---

## 5.9 `GET /discovery/candidates`

설명:

최근 뉴스/이슈 기반 관심 종목 후보 조회.

이 API는 추천이 아니라 탐색 보조용 후보 제안 API다.

### Query Params

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `limit` | integer | N | 기본 20 |
| `market` | string | N | `KOSPI`, `KOSDAQ` |
| `window_days` | integer | N | 기본 7 |

### 응답 예시

```json
{
  "data": [
    {
      "stock": {
        "id": 1,
        "symbol": "005930",
        "name": "삼성전자",
        "market": "KOSPI"
      },
      "reason_summary": "최근 7일간 AI 반도체 관련 뉴스 언급이 증가했습니다.",
      "news_count": 12,
      "price_change_rate": 3.1245,
      "top_keywords": ["AI", "반도체", "HBM"]
    }
  ],
  "meta": {
    "total": 1
  }
}
```

### 비고

- 블랙박스 점수만 반환하지 않음
- `reason_summary`는 필수

---

## 5.10 `GET /stocks/{stock_id}/summary`

설명:

종목 상세 화면 초기 렌더링을 위한 종합 summary API.

이 API는 선택 사항이다.

### 응답 예시

```json
{
  "data": {
    "stock": {
      "id": 1,
      "symbol": "005930",
      "name": "삼성전자",
      "market": "KOSPI",
      "status": "active"
    },
    "latest_price": {
      "trade_date": "2026-03-31",
      "close_price": 71200.0,
      "price_change_rate": 1.4218
    },
    "latest_insight": {
      "id": 501,
      "headline": "반도체 수요 회복 기대가 유효함",
      "summary": "최근 가격 흐름과 뉴스 기준으로..."
    },
    "news_preview": [
      {
        "id": 101,
        "title": "삼성전자, AI 반도체 수요 확대 기대",
        "published_at": "2026-03-31T09:00:00+09:00"
      }
    ]
  }
}
```

### 비고

- 프론트 속도 개선용 편의 API
- 초기 구현 시 없어도 됨

---

## 6. 리소스 스키마 요약

## 6.1 Stock Resource

```json
{
  "id": 1,
  "symbol": "005930",
  "name": "삼성전자",
  "market": "KOSPI",
  "status": "active"
}
```

## 6.2 News Resource

```json
{
  "id": 101,
  "title": "기사 제목",
  "summary": "기사 요약",
  "source_name": "연합뉴스",
  "url": "https://example.com",
  "published_at": "2026-03-31T09:00:00+09:00",
  "sentiment": {
    "label": "positive",
    "reason_summary": "긍정 해석 근거"
  }
}
```

## 6.3 Insight Resource

```json
{
  "id": 501,
  "headline": "한 줄 요약",
  "summary": "인사이트 본문",
  "thesis": "핵심 주장",
  "evidence_summary": "근거 요약",
  "reference_close_price": 71200.0,
  "created_at": "2026-03-31T18:00:00+09:00"
}
```

---

## 7. 에러 코드 초안

추천 에러 코드:

- `stock_not_found`
- `insight_not_found`
- `invalid_query_parameter`
- `internal_error`

---

## 8. 구현 우선순위

### Phase 1

- `GET /health`
- `GET /stocks/search`
- `GET /stocks/{stock_id}`
- `GET /stocks/{stock_id}/prices`
- `GET /stocks/{stock_id}/news`

### Phase 2

- `GET /stocks/{stock_id}/insights/latest`
- `GET /stocks/{stock_id}/insights`
- `GET /insights/{insight_id}/evaluations`

### Phase 3

- `GET /discovery/candidates`
- `GET /stocks/{stock_id}/summary`

---

## 9. 다음 단계

다음 문서는 `pipeline.md`로 진행하는 것이 좋다.

이유:

- 저장 구조와 조회 구조가 정리되었으므로,
- 이제 데이터 수집, 감성 분석, 인사이트 생성, 사후 평가를 어떤 순서와 트리거로 돌릴지 정리할 차례다.
