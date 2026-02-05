# PGMQ - Postgres Message Queue

<https://github.com/pgmq/pgmq>

AWS SQS와 RSMQ처럼 PostgreSQL 위에서 작동하는 경량 메시지 큐.
별도의 백그라운드 워커나 외부 의존성 없이 PostgreSQL 확장(extension)으로
구현되었다.

## 핵심 특징

### 메시지 전달 보장

- "정확히 한 번(exactly once)" 전달 보장
- 가시성 타임아웃(visibility timeout) 메커니즘으로 중복 처리 방지
- 타임아웃 내에 삭제/아카이빙되지 않으면 재처리 가능

### 주요 기능

- FIFO 큐 지원 (메시지 그룹 키로 순서 처리)
- 메시지 아카이빙 (삭제 대신 장기 보관 가능)
- 배치 작업 지원
- 파티션된 큐 (pg_partman 활용)

## PostgreSQL 통합 방식

각 큐는 `pgmq` 스키마의 독립적인 테이블로 생성된다.

- 큐 테이블: `q_[큐이름]`
- 아카이브 테이블: `a_[큐이름]`
- SQL 함수로 직접 조작 가능

지원 버전: PostgreSQL 14-18

## 주요 API

| 작업             | 함수                                  |
|------------------|---------------------------------------|
| 큐 생성          | `pgmq.create('큐이름')`               |
| 메시지 전송      | `pgmq.send(queue_name, msg, delay)`   |
| 메시지 읽기      | `pgmq.read(queue_name, vt, qty)`      |
| 메시지 팝(삭제)  | `pgmq.pop(queue_name)`                |
| 메시지 아카이빙  | `pgmq.archive(queue_name, msg_id)`    |
| 메시지 삭제      | `pgmq.delete(queue_name, msg_id)`     |

## 빠른 시작

### Docker

```bash
docker run -d --name pgmq-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  ghcr.io/pgmq/pg18-pgmq:v1.7.0
```

### 기본 사용법

```sql
-- 확장 활성화
CREATE EXTENSION pgmq;

-- 큐 생성
SELECT pgmq.create('my_queue');

-- 메시지 전송
SELECT pgmq.send('my_queue', '{"key": "value"}');

-- 메시지 읽기 (visibility timeout 30초, 1개 읽기)
SELECT * FROM pgmq.read('my_queue', 30, 1);

-- 메시지 삭제
SELECT pgmq.delete('my_queue', 1);
```

## PubSub 패턴 구현

PGMQ는 Point-to-Point 메시징만 지원한다. PubSub이 필요하면 컨슈머별 큐를
만들고 Fan-out하는 방식을 사용한다.

```sql
-- 컨슈머별 큐 생성
SELECT pgmq.create('topic_consumer_a');
SELECT pgmq.create('topic_consumer_b');

-- Fan-out: 모든 큐에 전송
SELECT pgmq.send('topic_consumer_a', '{"event": "created"}');
SELECT pgmq.send('topic_consumer_b', '{"event": "created"}');
```

메시지 본문이 크면 별도 테이블에 저장하고 ID만 참조하면 write
amplification을 줄일 수 있다.

참고: <https://github.com/tembo-io/pgmq/issues/255>

## Transactional Outbox 패턴

PGMQ는 PostgreSQL 확장이므로 일반 트랜잭션 내에서 동작한다.
비즈니스 로직과 메시지 발행을 원자적으로 처리할 수 있다.

```sql
BEGIN;
-- 비즈니스 로직
INSERT INTO orders (id, user_id, total) VALUES (123, 1, 50000);

-- 같은 트랜잭션에서 메시지 전송
SELECT pgmq.send('order_events', '{"order_id": 123, "event": "created"}');
COMMIT;
```

실패 시 둘 다 롤백된다. 별도 outbox 테이블 없이 PGMQ 큐 자체가 outbox
역할을 한다.

## 사용 사례

- Tembo
- Supabase
- Sprinters
- pgflow

## 참고

[Postgres 큐 기술 선택 | GeekNews](
https://news.hada.io/topic?id=11042)

## Java (Spring Boot) 예제

<https://github.com/adamalexandru4/pgmq-spring>

```java
// 큐 생성
PGMQueue queue = new PGMQueue("order_events");
pgmqClient.createQueue(queue);

// 트랜잭션 내에서 비즈니스 로직 + 메시지 전송
@Transactional
public void createOrder(Order order) {
    orderRepository.save(order);
    pgmqClient.send(queue, toJson(new OrderCreatedEvent(order.getId())));
}

// 메시지 읽기 (visibility timeout 30초)
PGMQMessage message = pgmqClient.read(queue,
    new PGMQVisiblityTimeout(30)).orElseThrow();

// 메시지 삭제
pgmqClient.delete(queue, message.getMsgId());
```

## Python (SQLAlchemy) 예제

<https://github.com/jason810496/pgmq-sqlalchemy>

```python
from pgmq_sqlalchemy import PGMQueue
from sqlalchemy.orm import Session

pgmq = PGMQueue(dsn='postgresql://user:pass@localhost:5432/db')

# 큐 생성
pgmq.create_queue('order_events')

# 트랜잭션 내에서 비즈니스 로직 + 메시지 전송
def create_order(session: Session, order: Order):
    session.add(order)
    pgmq.send('order_events', {'order_id': order.id, 'event': 'created'})
    session.commit()

# 메시지 읽기
msg = pgmq.read('order_events')

# 배치 읽기
msgs = pgmq.read_batch('order_events', 10)
```
