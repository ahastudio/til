# 데이터베이스는 이런 용도로 설계되지 않았다

<https://arpitbhayani.me/blogs/defensive-databases>

## 요약

40년간 데이터베이스 아키텍처를 지탱해 온 암묵적 계약이 있다.
"호출자는 사람이 작성한 결정론적 코드이며, 예측 가능한 쿼리를
실행하고, 배포 전 개발자가 검토한다." 에이전트 AI 시스템은
이 계약의 모든 계층을 동시에 위반한다.

글의 핵심 주장은 다음 다섯 가지 가정이 무너지고 있다는 것이다:

1. **결정론적 호출자** — 에이전트는 추론 경로에 따라
   매번 다른 쿼리를 생성한다
2. **의도된 쓰기** — 에이전트는 자율적으로, 반복적으로,
   잘못된 판단에 기반해서도 쓴다
3. **짧은 커넥션** — LLM 추론 시간만큼 커넥션을
   물고 있고, 팬아웃으로 세션이 폭증한다
4. **실패의 가시성** — 의미적으로 틀린 쿼리는 예외를
   발생시키지 않아 조용히 전파된다
5. **스키마는 엔지니어와의 계약** — 이제 스키마는
   LLM이 읽는 API 명세가 되었다

이에 대한 방어 패턴으로 역할별 타임아웃, 소프트 삭제,
이벤트 소싱, 멱등성 키, 전용 커넥션 풀, PgBouncer 트랜잭션
풀링, 쿼리 태깅, 에이전트별 최소 권한 역할(Role)을 제시한다.

## 본문 번역

### 암묵적 계약

모든 데이터베이스 아키텍처 결정의 기저에는 암묵적 계약이
존재한다. 아무도 문서화하지 않았다. 그냥 존재했다.

계약은 이렇다: 호출자는 사람이 작성한 애플리케이션이고,
결정론적 코드를 실행하며, 예측 가능한 쿼리를 발행하고,
배포 전 개발자가 리뷰한다. 쓰기는 의도적이다. 커넥션은
짧다. 문제가 생기면 사람이 알아챈다. 애플리케이션 계층이
똑똑하고 신중하기 때문에 데이터베이스는 단순하고 빠르기만
하면 됐다.

40년간 이 계약은 유효했다. 스키마 설계, 커넥션 풀 사이징,
권한 부여, 장애 모드 전부 이 계약 위에 세워졌다.

더 이상 유효하지 않다. 에이전트 AI 시스템은 이 계약의
모든 계층을 동시에 위반한다.

### 가정 1: 결정론적 호출자

에이전트 이전에 배포한 모든 애플리케이션에서 데이터베이스에
도달하는 쿼리는 사람이 작성한 것이었다.

- 개발자가 SQL을 작성했다
- 개발자가 코드 리뷰했다
- 개발자가 테스트하고 배포했다

이 가정이 너무 깊이 뿌리내려서 도구 자체가 이를 반영한다.
Postgres 쿼리 플래너는 관찰된 쿼리 패턴을 기반으로 통계를
구축하고, 캐시 레이어는 반복 쿼리에 맞춰 워밍업되며,
커넥션 풀은 알려진 복잡도의 예상 동시 쿼리 수에 맞춰
튜닝된다.

에이전트는 다르게 작동한다. 추론 과정을 거쳐 쿼리에
도달한다. 서로 다른 추론 경로는 같은 테이블에 대해
서로 다른 쿼리를 생성한다.

고객 분석 작업을 수행하는 에이전트가 이전에 한 번도
실행된 적 없는 5개 테이블 조인을 발행하고, 결과를
생각하는 동안 커넥션을 물고 있다가, 완전히 다른 후속
쿼리를 실행할 수 있다. 인덱스는 정상 경로만 커버한다.
커넥션 풀은 관측된 피크에 맞춰 사이징되어 있다. 에이전트가
필요한 데이터에 따라 어떤 쿼리든 만들어낼 수 있을 때,
이 둘 다 유효하지 않다.

#### 문장 타임아웃

문장 타임아웃은 첫 번째 방어선이다. 30초 걸리는
사람 작성 쿼리는 누군가 알아챌 버그다. 30초 걸리는
에이전트 쿼리는 아무도 보지 않는 추론 루프일 수 있다.

```sql
CREATE ROLE agent_worker;
ALTER ROLE agent_worker
  SET statement_timeout = '5s';
ALTER ROLE agent_worker
  SET idle_in_transaction_session_timeout = '10s';
```

`idle_in_transaction_session_timeout`이 특히 중요하다.
열린 트랜잭션을 물고 추론 중에 멈추는 에이전트는
충분히 있을 수 있는 상황이다.

### 가정 2: 쓰기는 의도적이다

데이터베이스 아키텍처에서 가장 위험한 가정은 모든 쓰기가
실행 전 사람의 검토를 거쳤다는 것이다.

에이전트는 자율적으로 쓴다. 현재의 작업 이해에 기반해서
쓰는데, 그 이해가 틀릴 수 있다. 도구가 예상치 못한 결과를
반환하면 루프를 돌며 쓴다. 일시적 네트워크 오류로 첫 번째
시도가 실패했다고 "판단"하면 재시도하며 쓴다. Slack
알림을 받기까지의 시간 동안 수천 행을 쓸 수 있다.

실제 문서화된 장애 패턴이 있다. 레거시 API를 호출하는
에이전트가 HTTP 200과 빈 결과를 받는다. 하류의 커넥션 풀
고갈로 API가 조용히 실패한 것이다. 에이전트는 "데이터
없음"을 "문제 없음"으로 해석하고 불완전한 데이터로 500건의
트랜잭션을 처리한다. 예외 없음. 알림 없음. 로그에는 모든
레코드에 "decision: approved"가 찍혀 있었다.

핵심 해법은 호출자가 틀릴 수 있고, 재시도할 수 있으며,
결과를 보고 있지 않을 수 있다고 가정하고 쓰기 경로를
설계하는 것이다.

#### 소프트 삭제

에이전트가 하드 삭제를 하게 두면 안 된다. 에이전트가
쓸 수 있는 모든 테이블에 소프트 삭제를 기본으로 적용한다.

```sql
ALTER TABLE orders
  ADD COLUMN deleted_at TIMESTAMPTZ;
ALTER TABLE orders
  ADD COLUMN deleted_by TEXT;
  -- 'agent:customer-support-v2', 'user:abc123'
ALTER TABLE orders
  ADD COLUMN delete_reason TEXT;

-- 에이전트는 이 뷰를 쿼리한다.
-- 삭제된 행을 보지 못하고 실수로 복원할 수도 없다.
CREATE VIEW active_orders AS
  SELECT * FROM orders WHERE deleted_at IS NULL;
```

`deleted_by` 컬럼은 보이는 것보다 중요하다. 2시간 전에
무슨 일이 있었는지 디버깅할 때 "에이전트 X가 삭제한 것
전부 보여줘"는 반드시 실행하게 될 쿼리다.

#### 추가 전용 이벤트 로그

금융 기록, 재고 변경, 사용자 상태 변이처럼 위험도가
높은 작업은 더 나아가 테이블을 추가 전용(append-only)으로
만든다. 에이전트는 UPDATE나 DELETE를 실행하지 않는다.
새 상태와 사유를 담은 INSERT만 실행한다.

```sql
CREATE TABLE order_state_log (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  order_id UUID NOT NULL REFERENCES orders(id),
  previous_status TEXT,
  new_status TEXT NOT NULL,
  changed_by TEXT NOT NULL,
  changed_at TIMESTAMPTZ DEFAULT now(),
  reason TEXT,
  idempotency_key TEXT UNIQUE
);
```

테이블 수준에서 적용한 이벤트 소싱 패턴이다. 가장 민감한
엔티티에 대한 단일 추가 전용 로그 테이블은 완전한 감사
추적을 제공하며, "되돌리기"는 프로젝션 쿼리로 해결된다.

#### 멱등성 키는 선택이 아니다

에이전트는 재시도한다. 설계상 그렇다. 모든 오케스트레이션
프레임워크는 최소 한 번(at-least-once) 전달 의미론으로
동작한다. 단계가 실패하면 다시 실행된다. 쓰기 경로는
이를 전제로 설계해야 한다.

멱등성 키는 에이전트가 모든 쓰기에 포함하는 안정적
식별자다. 데이터베이스가 유니크 제약조건으로 중복을
조용히 거부한다. 에이전트는 어느 쪽이든 성공 응답을
받는다. 연산을 두 번 실행해도 한 번 실행한 것과
같은 결과를 낸다.

```sql
ALTER TABLE order_state_log
  ADD CONSTRAINT uq_idempotency_key
    UNIQUE (idempotency_key);
```

```python
import hashlib

def make_idempotency_key(
    task_id: str,
    operation: str,
    target_id: str,
) -> str:
    raw = f"{task_id}:{operation}:{target_id}"
    return hashlib.sha256(
        raw.encode()
    ).hexdigest()[:32]
```

task ID는 오케스트레이션 레이어에서 오며 같은 논리적
작업의 재시도 간에 안정적이다. 에이전트가 필요한 만큼
재시도해도 데이터베이스는 논리적 작업당 정확히 하나의
쓰기만 본다.

### 가정 3: 커넥션은 짧다

전통적인 커넥션 풀 사이징은 단순한 모델을 따른다.
애플리케이션이 N개의 동시 요청을 처리하고, 각 요청은
짧은 시간 동안 하나의 커넥션이 필요하며, 예상 동시성
피크보다 약간 크게 풀을 설정하고 여유분을 더하면 끝이다.

에이전트는 이 모델을 세 가지 방식으로 깨뜨린다.

**1. 에이전트는 커넥션을 더 오래 물고 있다.**
다단계 추론 작업은 쿼리를 실행하고, LLM으로 결과를
처리하기 위해 멈추고, 다른 쿼리를 실행하고, 다시 멈추기를
반복한다. 작업당 커넥션 시간은 더 이상 "쿼리 실행 시간"이
아니라 "쿼리 실행 시간 + LLM 추론 시간 × 추론 단계 수"다.

**2. 에이전트는 팬아웃한다.**
하나의 상위 에이전트 작업이 병렬로 작동하는 하위
에이전트들을 생성한다. 하나의 작업이 5개의 동시
데이터베이스 세션이 된다.

**3. 에이전트는 예상 외로 증식한다.**
개발 환경에서 3개였던 에이전트가 운영 환경에서 30개가
된다. 아무도 커넥션 풀 설정을 업데이트하지 않았다.

해법은 에이전트 워크로드 전용 커넥션 풀을 사람 대상
트랜잭션 트래픽과 분리하여 독립적으로 사이징하는 것이다.

```python
# 경험 법칙:
# (에이전트_워커_수 * 평균_동시_단계 * 0.5)
# 0.5는 대부분의 에이전트 단계가 DB 시간이 아닌
# LLM 시간임을 반영한다

agent_engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=5,
    pool_timeout=3,        # 큐잉 대신 빠른 실패
    pool_recycle=300,
    pool_pre_ping=True,
    connect_args={
        "options":
            "-c statement_timeout=5000"
            " -c idle_in_transaction_session_timeout"
            "=10000"
    },
)
```

`pool_timeout=3`은 의도적이다. 3초 안에 커넥션을 얻지
못하면 무한 대기 대신 빠르게 실패하고 백오프 재시도해야
한다. 포화 상태의 풀에서 큐잉된 요청은 연쇄 장애의 원인이
된다.

많은 에이전트를 동시에 운영하는 시스템에는 에이전트와
Postgres 사이에 PgBouncer를 추가한다. PgBouncer는
트랜잭션 풀링 모드로 동작하여, 전체 세션이 아닌 각
트랜잭션 후에 커넥션을 풀로 반환한다.

```ini
# pgbouncer.ini
[databases]
mydb = host=postgres_host dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 500
default_pool_size = 20
reserve_pool_size = 5
reserve_pool_timeout = 1.0
```

트랜잭션 풀링 모드에서 20개의 실제 Postgres 커넥션이
500개의 에이전트 커넥션을 서비스할 수 있다. 각 에이전트가
다단계 작업 전체가 아닌 단일 트랜잭션 동안만 Postgres
커넥션을 점유하기 때문이다.

### 가정 4: 잘못된 쿼리는 시끄럽게 실패한다

사람이 운영하는 시스템에서 느리거나 잘못된 쿼리는 금방
표면화된다. 대시보드가 느리게 로딩된다. API가 타임아웃된다.
엔지니어가 EXPLAIN ANALYZE를 실행하고 문제를 찾는다.
피드백 루프가 짧다.

에이전트는 이 피드백 루프를 닫아버린다. 느린 쿼리 결과를
받은 에이전트는 그냥 결과를 사용한다. 빈 결과를 받은
에이전트는 데이터가 정말 없는 건지 쿼리가 잘못된 건지
구분하지 못한다. 잘못된 읽기에 기반한 의사결정을 쓰면서
작업을 계속한다.

이것은 애플리케이션 오류와는 다른 종류의 장애다. 예외는
관찰 가능하다. 의미적으로 틀렸지만 행을 반환하는 쿼리는
관찰 불가능하다.

완화책은 데이터베이스 접근 계층에 에이전트 전용
관측가능성(observability)을 구축하는 것이다. 표준 슬로우
쿼리 로그로는 부족하다. 어떤 에이전트가, 어떤 작업에서,
어떤 추론 단계에서 쿼리를 생성했는지 알아야 한다.
Postgres에서 가장 실용적인 방법은 쿼리 코멘트다.

```python
from sqlalchemy import text, event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "before_cursor_execute")
def add_agent_context_comment(
    conn, cursor, statement,
    parameters, context, executemany,
):
    agent_ctx = getattr(
        conn.info, "agent_context", None
    )
    if agent_ctx:
        statement = (
            f"/* agent_id={agent_ctx['agent_id']},"
            f" task_id={agent_ctx['task_id']},"
            f" step={agent_ctx['step']}"
            f" */ {statement}"
        )
    return statement, parameters

# 사용: 실행 전 커넥션에 컨텍스트 설정
with engine.connect() as conn:
    conn.info["agent_context"] = {
        "agent_id": "fulfillment-v3",
        "task_id": "task-abc-123",
        "step": "check-inventory",
    }
    conn.execute(text("SELECT ..."))
```

이 코멘트는 `pg_stat_activity`, `pg_stat_statements`,
슬로우 쿼리 로그에 나타난다.
`agent_id=fulfillment-v3, task_id=task-abc-123,
step=check-inventory`로 태깅된 슬로우 쿼리는 즉시
조치 가능하다. 이것 없이는 고고학을 하는 셈이다.

에이전트별로 그룹화된 쿼리를 보여주는 모니터링 뷰:

```sql
SELECT
  (regexp_match(
    query, 'agent_id=([^,]+)'))[1]
    AS agent_id,
  (regexp_match(
    query, 'task_id=([^,]+)'))[1]
    AS task_id,
  count(*) AS call_count,
  round(mean_exec_time::numeric, 2)
    AS avg_ms,
  round(total_exec_time::numeric, 2)
    AS total_ms
FROM pg_stat_statements
WHERE query LIKE '%agent_id=%'
GROUP BY 1, 2
ORDER BY total_ms DESC;
```

### 가정 5: 스키마는 엔지니어와의 계약이다

대부분의 팀이 깨질 때까지 생각하지 않는 가정이다.
스키마는 개발자 편의를 위해 설계되었다. 엔지니어에게
의미 있는 이름, 쿼리 편의를 위한 구조, 원본 마이그레이션
코멘트를 읽어야만 "의미가 있는" nullable 컬럼.

에이전트가 스키마를 볼 수 있을 때 — Text-to-SQL,
도구 정의, 데이터베이스를 감싸는 MCP 서버를 통해 —
스키마는 언어 모델과의 계약이 된다. 컬럼 이름, 테이블
구조, null 허용 여부가 LLM이 올바른 쿼리를 생성할지
자신감 넘치는 헛소리를 생성할지를 결정한다.

```sql
-- 대부분의 스키마가 이렇게 생겼다
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  usr_id UUID,       -- 어떤 사용자?
  stat_cd INT,       -- 2가 뭐고 7이 뭔데?
  flg_1 BOOLEAN,     -- ???
  upd_ts TIMESTAMPTZ -- 업데이트? 누가?
);

-- 에이전트가 읽을 수 있는 스키마
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  customer_id UUID NOT NULL
    REFERENCES customers(id),
  fulfillment_status TEXT NOT NULL CHECK (
    fulfillment_status IN (
      'pending', 'processing',
      'shipped', 'delivered', 'cancelled'
    )
  ),
  requires_signature BOOLEAN
    NOT NULL DEFAULT false,
  last_modified_at TIMESTAMPTZ
    NOT NULL DEFAULT now()
);
```

이름을 바꿀 수 없는 스키마(레거시 시스템, 마이그레이션
비용이 높은 테이블)에는 에이전트용 뷰 레이어를 구축한다.

```sql
CREATE VIEW agent_orders AS
SELECT
  id,
  usr_id    AS customer_id,
  CASE stat_cd
    WHEN 1 THEN 'pending'
    WHEN 2 THEN 'processing'
    WHEN 5 THEN 'shipped'
    WHEN 7 THEN 'delivered'
    WHEN 9 THEN 'cancelled'
  END       AS fulfillment_status,
  flg_1     AS requires_signature,
  upd_ts    AS last_modified_at
FROM orders
WHERE deleted_at IS NULL;
```

컬럼 코멘트를 독스트링처럼 작성한다. Text-to-SQL
에이전트에게 이것이 실제로 독스트링이기 때문이다:

```sql
COMMENT ON COLUMN
  agent_orders.fulfillment_status IS
  'Current state of the order in the '
  'fulfillment pipeline. Use this to '
  'filter orders that need action: '
  'pending and processing orders '
  'are active. Cancelled orders should '
  'never be modified.';
```

### 폭발 반경 제한

모든 가정을 관통하는 장애 모드가 하나 더 있다.
잘못 동작하는 에이전트의 폭발 반경은 부여된 접근 권한이
결정한다.

전통적 애플리케이션은 데이터베이스 역할을 공유하거나
기껏해야 서비스별로 몇 개의 역할을 둔다. 애플리케이션
코드가 가드레일이라는 가정이었다. 코드가 사용자 자신의
레코드만 업데이트하도록 허용했으므로, 데이터베이스
역할이 이를 강제할 필요가 없었다.

에이전트는 이 가정을 위험하게 만든다. 잘못된 상태로
추론한 에이전트는 개발자가 예상하지 못한 쿼리를 실행할
수 있다. 에이전트는 알려진 유한한 코드 경로 집합이
아니라, 데이터베이스 커넥션에 접근할 수 있는 범용
추론기다.

해법은 에이전트 유형별 역할(Role)에 최소한의 필수
권한만 부여하는 것이다:

```sql
CREATE ROLE agent_fulfillment;
CREATE ROLE agent_customer_support;
CREATE ROLE agent_analytics;

-- agent_analytics: 읽기 전용, 필요한 테이블만
GRANT SELECT ON agent_orders
  TO agent_analytics;
GRANT SELECT ON customers
  TO agent_analytics;
-- 결제, 인증정보, PII 테이블 접근 없음

-- agent_customer_support:
-- 주문 상태 변경 가능, 재무 접근 불가
GRANT SELECT ON agent_orders
  TO agent_customer_support;
GRANT INSERT ON order_state_log
  TO agent_customer_support;
-- orders에 UPDATE 없음 — 이벤트 로그를 통한다

-- agent_fulfillment:
-- 배송 관련 필드만 읽기/수정 가능
GRANT SELECT, UPDATE (
  fulfillment_status, shipped_at,
  tracking_number
) ON orders TO agent_fulfillment;
```

접근 설계 리뷰에서 물어야 할 질문은 "이 에이전트가
뭐가 필요한가?"가 아니라 "이 에이전트의 추론이
잘못되거나 자격 증명이 유출되면 최악의 경우는?"이다.

### 방어적으로 설계된 데이터 계층

종합하면 이렇다. 이것들 중 어느 것도 새로운 기술이
아니다. 전투에서 검증된 데이터베이스 도구에 모두 존재한다.

- 에이전트 유형별 자체 DB 역할 + 역할 수준 타임아웃
- 에이전트 전용 커넥션 풀 + PgBouncer 트랜잭션 풀링
- 소프트 삭제 + `deleted_by` 컬럼으로 에이전트 신원 추적
- 고위험 쓰기 경로에 추가 전용 이벤트 로그 + 멱등성 키
- 가독성 높은 스키마 + 뷰 레이어 + 컬럼 코멘트
- 모든 쿼리에 에이전트 ID/작업 ID/추론 단계 태깅
- 서킷 브레이커: 작업당 최대 쓰기 수, 문장당 최대 영향
  행 수, 최대 작업 지속시간

소프트 삭제, 추가 전용 로그, 최소 권한 역할, 행 수준
보안, 멱등성 키, 쿼리 태깅 — 수년간 존재해 온 패턴들이다.
에이전트가 강제하는 전환은 이 패턴들이 "언젠가 구현하려던
모범 사례"에서 "하중을 지탱하는 인프라"로 바뀌는 것이다.

## 분석

### 정확히 짚은 것들

글의 가장 큰 기여는 **프레이밍**이다. "에이전트는
데이터베이스의 암묵적 계약을 위반한다"는 관점은 개별
패턴을 나열하는 것보다 훨씬 강력한 사고 틀을 제공한다.
왜 이 패턴들이 필요한지를 근본 원인에서 도출하기 때문에,
글에서 다루지 않은 새로운 장애 모드가 나타나도 같은
프레임으로 분석할 수 있다.

소프트 삭제, 멱등성 키, 이벤트 소싱, 최소 권한 역할 등
제시된 패턴 하나하나는 검증된 것들이다. 특히 쿼리 코멘트를
통한 에이전트별 관측가능성 패턴은 실무에서 즉시 적용
가능하면서도 간과되기 쉬운 통찰이다. `pg_stat_statements`에
에이전트 컨텍스트가 남는다는 것만으로 장애 대응 시간이
극적으로 줄어든다.

"스키마는 이제 LLM과의 계약"이라는 관찰은 특히 날카롭다.
`usr_id`와 `customer_id`의 차이가 Text-to-SQL 정확도에
미치는 영향을 체감한 팀은 이 주장에 즉각 공감할 것이다.
컬럼 코멘트를 독스트링처럼 쓰라는 조언은 단순하지만
파괴적이다 — 스키마 설계의 대상 독자(audience)가
영구적으로 바뀌었음을 선언하는 것이기 때문이다.

### 놓치거나 약하게 다룬 것들

**비용 분석이 빠져 있다.** 모든 테이블에 소프트 삭제,
모든 고위험 테이블에 이벤트 소싱, 에이전트별 역할 분리를
적용하면 운영 복잡도가 대폭 증가한다. 어디까지가
적정한지에 대한 기준선이 없다. "에이전트가 쓸 수 있는
모든 테이블"이라는 표현은 경계가 모호하다.

**읽기 경로의 방어가 부족하다.** 가정 4에서 의미적으로
틀린 쿼리 문제를 지적하면서 해법으로 관측가능성만
제시한다. 관찰은 사후 대응이다. 에이전트가 조인 없이
단일 테이블만 조회해서 불완전한 데이터를 가져가는 것을
사전에 방지하는 메커니즘(허용 쿼리 패턴 화이트리스트,
결과 검증 레이어 등)은 논의하지 않는다.

**멀티 데이터베이스 환경을 고려하지 않는다.** 실제 운영
환경에서 에이전트가 접근하는 데이터 저장소는 Postgres
하나가 아니다. Redis, Elasticsearch, S3, 외부 API 등
여러 저장소에 걸친 트랜잭션 일관성 문제는 단일
데이터베이스 방어 패턴으로 해결되지 않는다.

**오케스트레이션 레이어와의 책임 경계가 불분명하다.**
서킷 브레이커(작업당 최대 쓰기 수, 최대 작업 지속시간)를
언급하면서 이것이 오케스트레이션에서 강제된다고만 한다.
데이터베이스 계층과 오케스트레이션 계층이 어떻게 협력해야
하는지, 어디에서 어떤 방어를 담당하는지의 아키텍처적
논의가 빠져 있다.

### 비판적 관점

이 글은 **데이터베이스를 방어적 계층으로 만들라**고
주장한다. 맞는 말이지만, 더 근본적인 질문을 회피한다:
**에이전트에게 직접 데이터베이스 접근을 주는 것 자체가
올바른 아키텍처인가?**

글의 모든 패턴은 "에이전트가 SQL을 직접 실행한다"는
전제 위에 있다. 하지만 현실에서 더 견고한 아키텍처는
에이전트에게 SQL 접근을 주지 않는 것이다. 잘 정의된
API 엔드포인트나 도구(Tool) 인터페이스를 통해 사전에
검증된 연산만 허용하는 것이 데이터베이스 수준에서
방어벽을 세우는 것보다 폭발 반경을 더 효과적으로 제한한다.

물론 글에서도 MCP 서버, Text-to-SQL 시나리오를 언급한다.
이런 경우 에이전트가 임의의 쿼리를 생성하는 것은
피할 수 없고, 글의 방어 패턴이 정확히 필요하다.
하지만 "모든 에이전트 워크로드에 이 패턴을 적용하라"는
톤은 과도하다. 에이전트 아키텍처의 첫 번째 결정은
"어떤 수준의 데이터베이스 접근을 허용할 것인가"여야
하며, 이 글은 그 결정을 이미 내린 후의 이야기만 한다.

또 하나의 빠진 관점은 **성능 비용**이다. 모든 쿼리에
코멘트 삽입, 모든 쓰기에 이벤트 로그 INSERT,
소프트 삭제로 인한 인덱스 팽창, 뷰 레이어의 쿼리 최적화
저하 — 이것들의 누적 비용은 무시할 수 없다. "에이전트
워크로드의 안전성"과 "시스템 전체의 성능"은 트레이드오프
관계인데, 이 글은 안전성 쪽만 이야기한다.

## 인사이트

### 에이전트 시대, 데이터베이스의 정체성이 바뀐다

40년간 데이터베이스는 "신뢰할 수 있는 호출자를 위한
고성능 저장소"였다. 에이전트의 등장은 데이터베이스의
정체성을 "신뢰할 수 없는 호출자를 위한 방어적 게이트
키퍼"로 전환시킨다. 이것은 기능 추가가 아니라
패러다임 전환이다.

이 전환의 진짜 함의는 데이터베이스 팀의 역할 변화에
있다. DBA는 더 이상 성능 튜닝과 백업만 하는 사람이
아니다. 에이전트의 행동 패턴을 이해하고, 접근 정책을
설계하며, 이상 탐지 파이프라인을 구축하는 "데이터
보안 아키텍트"가 된다.

### "언젠가 하려던" 패턴에서 "하중 지탱 인프라"로

글의 결론이 가장 중요한 통찰이다. 소프트 삭제,
멱등성 키, 최소 권한 역할은 수년간 "모범 사례"로
불리며 미뤄져 왔다. 에이전트는 이 미룸의 대가를
즉각적이고 가시적으로 만든다.

이것이 시사하는 미래가 있다. 에이전트 워크로드를
먼저 경험하는 팀이 이 패턴들을 먼저 구현하고, 그 결과
에이전트가 없는 워크로드의 안정성까지 높아진다.
에이전트가 역설적으로 데이터베이스 운영 성숙도를
끌어올리는 촉매가 되는 것이다.

### 스키마 가독성은 새로운 API 설계다

"컬럼 코멘트를 독스트링처럼 쓰라"는 조언 뒤에 더 큰
흐름이 있다. 스키마가 LLM의 입력이 되는 순간, 스키마
설계는 곧 프롬프트 엔지니어링이 된다. `stat_cd` 대신
`fulfillment_status`를 쓰는 것은 코드 가독성이 아니라
LLM 정확도를 위한 것이다.

이 논리를 확장하면, 앞으로 스키마 마이그레이션의
승인 기준에 "에이전트가 올바른 쿼리를 생성할 수
있는가?"가 추가될 것이다. 스키마 리뷰에 LLM 기반
Text-to-SQL 정확도 테스트를 포함하는 팀이 등장할
것이다.

### 진짜 전쟁터는 데이터베이스가 아니다

이 글이 열어놓고 닫지 않은 가장 큰 질문: 에이전트
아키텍처에서 방어의 최적 위치는 어디인가? 데이터베이스는
최후의 방어선이지, 최선의 방어선은 아니다.

더 견고한 접근은 계층적 방어다. 오케스트레이션 레이어에서
의도(intent)를 검증하고, API/도구 레이어에서 연산을
제한하고, 데이터베이스 레이어에서 최소 권한과 감사를
강제하는 다층 방어. 데이터베이스만으로 모든 것을
방어하려는 것은, 성의 마지막 탑에 모든 병사를 배치하는
것과 같다.

에이전트 시대의 데이터 아키텍처를 설계하는 팀이 물어야
할 첫 번째 질문은 "데이터베이스를 어떻게 방어할
것인가?"가 아니라 "에이전트가 데이터베이스에 도달하기
전에 몇 겹의 방어를 거치게 할 것인가?"다.
