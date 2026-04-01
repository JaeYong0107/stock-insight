# Docs Index

## 목적

이 문서는 사람과 에이전트가 `docs/` 아래 문서를 빠르게 탐색할 수 있도록 만든 문서 허브다.

읽는 순서와 용도를 한눈에 정리해서, 코드 분석이나 구현 전 문맥 파악 시간을 줄이는 것이 목적이다.

---

## 가장 먼저 읽을 문서

### 1. 제품과 범위 이해

- [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)
  - 무엇을 만드는지, MVP 범위가 어디까지인지 정의

### 2. 설계 의사결정 이해

- [product-decisions.md](C:/Users/123/개발/stock-insight/docs/product-decisions.md)
  - 요구사항을 어떤 정책으로 구현할지 정의

### 3. 도메인 구조 이해

- [domain-model.md](C:/Users/123/개발/stock-insight/docs/domain-model.md)
  - 핵심 개념과 관계를 설명

### 4. DB 구조 이해

- [erd.md](C:/Users/123/개발/stock-insight/docs/erd.md)
- [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
  - 실제 엔티티 관계와 컬럼 구조 확인

### 5. API와 데이터 흐름 이해

- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)
  - 조회 계약과 배치 흐름 확인

### 6. 구현 작업 이해

- [claude-implementation-tasks.md](C:/Users/123/개발/stock-insight/docs/claude-implementation-tasks.md)
- [jira-ticket-plan.md](C:/Users/123/개발/stock-insight/docs/jira-ticket-plan.md)
  - 실제 구현 순서와 티켓 구조 확인

---

## 목적별 빠른 진입 가이드

### 제품 이해가 목적일 때

1. [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)
2. [product-decisions.md](C:/Users/123/개발/stock-insight/docs/product-decisions.md)

### DB/백엔드 모델 이해가 목적일 때

1. [domain-model.md](C:/Users/123/개발/stock-insight/docs/domain-model.md)
2. [erd.md](C:/Users/123/개발/stock-insight/docs/erd.md)
3. [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)

### API 구현이 목적일 때

1. [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
2. [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
3. [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)

### 배치/수집 구현이 목적일 때

1. [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)
2. [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
3. [claude-implementation-tasks.md](C:/Users/123/개발/stock-insight/docs/claude-implementation-tasks.md)

### Jira/작업 관리가 목적일 때

1. [claude-implementation-tasks.md](C:/Users/123/개발/stock-insight/docs/claude-implementation-tasks.md)
2. [jira-ticket-plan.md](C:/Users/123/개발/stock-insight/docs/jira-ticket-plan.md)

---

## 문서별 역할 요약

- [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)
  - 프로젝트의 고정 요구사항 기준

- [product-decisions.md](C:/Users/123/개발/stock-insight/docs/product-decisions.md)
  - 요구사항을 실제 설계 정책으로 번역한 문서

- [domain-model.md](C:/Users/123/개발/stock-insight/docs/domain-model.md)
  - 도메인 개념과 책임 정의

- [erd.md](C:/Users/123/개발/stock-insight/docs/erd.md)
  - 실제 저장되는 엔티티와 관계 정의

- [schema.md](C:/Users/123/개발/stock-insight/docs/schema.md)
  - 컬럼/타입/인덱스/제약조건 정의

- [api-spec.md](C:/Users/123/개발/stock-insight/docs/api-spec.md)
  - FastAPI 구현용 API 계약

- [pipeline.md](C:/Users/123/개발/stock-insight/docs/pipeline.md)
  - 수집/분석/평가 파이프라인 정의

- [discovery-feature-proposal.md](C:/Users/123/개발/stock-insight/docs/discovery-feature-proposal.md)
  - 탐색 기능 배경 설명용 제안 문서

- [claude-implementation-tasks.md](C:/Users/123/개발/stock-insight/docs/claude-implementation-tasks.md)
  - Claude 구현 추적 문서

- [jira-ticket-plan.md](C:/Users/123/개발/stock-insight/docs/jira-ticket-plan.md)
  - Jira 에픽/스토리/태스크 설계 문서

---

## 권장 원칙

- 요구사항 판단은 [requirements.md](C:/Users/123/개발/stock-insight/docs/requirements.md)를 기준으로 한다.
- 설계 충돌이 있으면 [product-decisions.md](C:/Users/123/개발/stock-insight/docs/product-decisions.md)부터 확인한다.
- 구현 순서가 필요하면 [claude-implementation-tasks.md](C:/Users/123/개발/stock-insight/docs/claude-implementation-tasks.md)를 본다.
- 티켓 관리가 필요하면 [jira-ticket-plan.md](C:/Users/123/개발/stock-insight/docs/jira-ticket-plan.md)를 본다.
