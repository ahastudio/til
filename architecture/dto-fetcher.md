# DTO Fetcher

## 문제: 도메인 모델은 Query에 적합하지 않다

DDD를 적용하면 도메인 레이어에 Aggregate, Entity, Value Object로 구성된 풍부한 모델이 만들어진다.
이 모델은 Command — 비즈니스 규칙을 검증하고 상태를 변경하는 작업 — 에는 강하다.
그러나 Query에 이 모델을 그대로 재사용하면 문제가 생긴다.

화면이나 API 응답에 필요한 데이터는 도메인 경계를 넘나든다.
주문 목록 화면에는 주문 정보와 함께 고객 이름, 상품 썸네일, 배송 상태가 한 번에 필요하다.
도메인 모델을 통해 이를 조합하면 여러 Aggregate를 순차적으로 로드하는 N+1 쿼리가 발생하거나,
필요 없는 데이터까지 함께 로드하게 된다.

더 근본적인 문제는 동기의 불일치다.
도메인 모델은 "변경 시 무엇을 보호해야 하는가"를 기준으로 설계된다.
Query는 "화면에 무엇을 보여줄 것인가"를 기준으로 설계된다.
두 관심사가 하나의 모델을 공유하면 어느 쪽도 잘 하기 어렵다.

## 해법: Query 전용 경로

DTO Fetcher는 Query를 위한 전용 읽기 경로다.
도메인 모델을 경유하지 않고, 필요한 데이터를 필요한 형태로 직접 조합해 반환한다.

```text
Command 경로:
  UI → Application Service → Domain Model → Repository → DB

Query 경로:
  UI → DTO Fetcher → DB (또는 Read Store)
```

DTO Fetcher는 도메인 로직을 포함하지 않는다.
비즈니스 규칙 검증, 불변식 유지, 이벤트 발행 — 이 모든 것은 Command 경로의 책임이다.
DTO Fetcher의 유일한 책임은 "이 화면/API에 필요한 데이터를 올바른 형태로 가져오는 것"이다.

## 구조

```text
┌──────────────────────────────────────────────────┐
│                    UI Layer                      │
│                                                  │
│  ┌──────────────────┐   ┌─────────────────────┐  │
│  │  Command 처리    │   │    Query 처리       │  │
│  │  (버튼, 폼 등)   │   │    (화면 렌더링)    │  │
│  └────────┬─────────┘   └──────────┬──────────┘  │
│           │                        │             │
└───────────┼────────────────────────┼─────────────┘
            │                        │
┌───────────▼──────────┐  ┌──────────▼───────────────┐
│  Application Layer   │  │      DTO Fetcher         │
│                      │  │                          │
│  Application Service │  │  SQL / ORM projection /  │
│  Domain Model        │  │  View / Materialized     │
│  Repository (write)  │  │  query                   │
└──────────────────────┘  └──────────────────────────┘
```

UI는 Command가 필요하면 Application Service를 호출하고,
Query가 필요하면 DTO Fetcher를 직접 호출한다.
Application Layer를 Query 경로가 경유할 이유가 없다.

## DTO Fetcher의 특성

### 도메인 레이어를 우회한다

Aggregate를 로드한 후 DTO로 변환하지 않는다.
필요한 컬럼을 직접 SELECT해 DTO에 매핑한다.
이를 통해 불필요한 로드를 제거하고 N+1을 방지한다.

### 읽기 모델(Read Model)을 정의한다

DTO는 화면이나 API 계약에 맞게 설계된다.
도메인 개념과 1:1로 대응하지 않아도 된다.
여러 Aggregate의 데이터를 하나의 DTO로 평탄화(flatten)하는 것이 자연스럽다.

### 쓰기 모델과 독립적으로 진화한다

도메인 모델이 바뀌어도 DTO Fetcher를 수정하지 않아도 되는 경우가 많다.
반대로 화면 요구사항이 바뀌어도 도메인 모델에 영향이 없다.

### 트랜잭션 경계가 느슨하다

Command는 강한 일관성을 보장하는 트랜잭션 안에서 실행된다.
DTO Fetcher는 읽기 전용이므로 트랜잭션이 필요 없거나, 필요한 경우 읽기 전용 트랜잭션으로 충분하다.

## CQRS와의 관계

DTO Fetcher는 CQRS(Command Query Responsibility Segregation)의 Query 측 구현 전략 중 하나다.
CQRS는 "Command와 Query를 분리하라"는 원칙이고,
DTO Fetcher는 그 Query 경로를 어떻게 구현하는지에 대한 패턴이다.

CQRS의 Query 구현 스펙트럼은 넓다.

```text
단순 ──────────────────────────────────────────── 복잡

도메인 모델    DTO Fetcher    별도 Read DB    Event-sourced
재사용         (동일 DB)      (CQRS 풀모델)   Projection
```

인프라 투자 없이 Query 성능과 관심사 분리를 얻으려면 DTO Fetcher가 실용적인 출발점이다.
쓰기와 읽기가 같은 DB를 공유하면서도 Query 경로를 명확히 분리한다.

## 구현 시 고려사항

### 어디에 위치시킬 것인가

DTO Fetcher는 UI Layer에서 직접 호출하므로, UI가 의존할 수 있는 레이어에 위치해야 한다.
별도 Query Infrastructure 레이어나 UI와 같은 레이어 내에 두는 것이 일반적이다.
Domain 레이어에 두면 안 된다 — 도메인 모델이 특정 쿼리 구현에 의존하게 된다.

### 인터페이스를 정의할 것인가

테스트 가능성을 위해 인터페이스를 정의하고 구현을 분리하는 것이 좋다.
UI는 인터페이스에 의존하고, 실제 SQL/ORM 구현은 Infrastructure 레이어에 위치한다.

### 얼마나 세분화할 것인가

화면 하나당 DTO Fetcher 하나가 적절한 출발점이다.
공통으로 재사용되는 부분이 생기면 그때 분리한다.
과도한 추상화는 오히려 가독성을 해친다.

### 페이징과 정렬을 어떻게 다룰 것인가

Query 파라미터(페이지, 정렬 기준)를 DTO Fetcher가 받아 SQL에 반영한다.
도메인 모델의 컬렉션을 메모리에서 정렬하는 방식은 피한다.

## 도메인 모델 재사용과의 비교

| | 도메인 모델 재사용 | DTO Fetcher |
| ----------- | ------------------- | ----------- |
| 쿼리 효율   | N+1 발생 가능       | 최적화 가능 |
| 코드 중복   | 적음                | 읽기 모델 별도 |
| 관심사 분리 | Command/Query 혼재  | 명확히 분리 |
| 변경 영향   | 도메인 변경이 Query에 파급 | 독립적 |
| 복잡도      | 낮음                | 중간        |

도메인 모델이 단순하고 Query 수가 적다면 재사용이 합리적이다.
Query가 많아지고 화면 요구사항이 복잡해질수록 DTO Fetcher의 이점이 커진다.

## 관련 패턴

- **CQRS** — DTO Fetcher가 구현하는 Query 분리 원칙의 상위 개념
- **Repository** — Command 경로의 쓰기 추상화. DTO Fetcher는 Repository가 아니다
- **Read Model / Projection** — 별도 Read DB를 두는 더 강한 형태의 Query 분리
- **Query Object** — 쿼리 파라미터를 객체로 캡슐화하는 패턴. DTO Fetcher와 함께 쓰임
