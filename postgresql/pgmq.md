# PGMQ - Postgres Message Queue

<https://github.com/pgmq/pgmq>

HN 토론: <https://news.ycombinator.com/item?id=37036256> (10점, 8개 댓글)

GN 토론: <https://news.hada.io/topic?id=14780>

AWS SQS와 RSMQ처럼 PostgreSQL 위에서 작동하는 경량 메시지 큐. 별도의 백그라운드
워커나 외부 의존성 없이 PostgreSQL 확장(extension) 또는 SQL 전용 설치로
구현된다.
공식 클라이언트로 Rust와 Python을 지원하고,
커뮤니티 구현으로 Go, Node.js, Java, Elixir, Ruby, Kotlin, PHP 등이 있으며,
Tembo, Supabase, Sprinters, pgflow, FFmpegLab Server 등이 사용한다.

## 핵심 특징

### 메시지 전달 보장

- “정확히 한 번(exactly once)” 전달 보장
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

| 작업            | 함수                                |
| --------------- | ----------------------------------- |
| 큐 생성         | `pgmq.create('큐이름')`             |
| 메시지 전송     | `pgmq.send(queue_name, msg, delay)` |
| 메시지 읽기     | `pgmq.read(queue_name, vt, qty)`    |
| 메시지 팝(삭제) | `pgmq.pop(queue_name)`              |
| 메시지 아카이빙 | `pgmq.archive(queue_name, msg_id)`  |
| 메시지 삭제     | `pgmq.delete(queue_name, msg_id)`   |

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

최근 PGMQ는 와일드카드 패턴 매칭을 지원하는 토픽 기반 라우팅(topic-based
routing)을 추가했다.
그럼에도 기본 메시징 모델은 Point-to-Point이며,
단순한 PubSub이 필요하면 컨슈머별 큐를 만들고 Fan-out하는 방식을 쓴다.

```sql
-- 컨슈머별 큐 생성
SELECT pgmq.create('topic_consumer_a');
SELECT pgmq.create('topic_consumer_b');

-- Fan-out: 모든 큐에 전송
SELECT pgmq.send('topic_consumer_a', '{"event": "created"}');
SELECT pgmq.send('topic_consumer_b', '{"event": "created"}');
```

메시지 본문이 크면 별도 테이블에 저장하고 ID만 참조하면 write amplification을
줄일 수 있다.

참고: <https://github.com/tembo-io/pgmq/issues/255>

## Transactional Outbox 패턴

PGMQ는 PostgreSQL 확장이므로 일반 트랜잭션 내에서 동작한다. 비즈니스 로직과
메시지 발행을 원자적으로 처리할 수 있다.

```sql
BEGIN;
-- 비즈니스 로직
INSERT INTO orders (id, user_id, total) VALUES (123, 1, 50000);

-- 같은 트랜잭션에서 메시지 전송
SELECT pgmq.send('order_events', '{"order_id": 123, "event": "created"}');
COMMIT;
```

실패 시 둘 다 롤백된다. 별도 outbox 테이블 없이 PGMQ 큐 자체가 outbox 역할을
한다.

## Spring Boot 예제

<https://github.com/adamalexandru4/pgmq-spring>

```java
// 설정
@Configuration
public class PgmqConfig {

    @Bean
    public PGMQClient pgmqClient(DataSource dataSource) {
        return new PGMQClient(dataSource);
    }

    @Bean
    public PGMQueue orderEventsQueue(PGMQClient pgmqClient) {
        PGMQueue queue = new PGMQueue("order_events");
        pgmqClient.createQueue(queue);
        return queue;
    }
}

// 서비스
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final PGMQClient pgmqClient;
    private final PGMQueue orderEventsQueue;
    private final ObjectMapper objectMapper;

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        // 비즈니스 로직
        Order order = Order.create(request);
        orderRepository.save(order);

        // 같은 트랜잭션에서 메시지 전송
        String payload = objectMapper.writeValueAsString(
            new OrderCreatedEvent(order.getId(), order.getTotal())
        );
        pgmqClient.send(orderEventsQueue, payload);

        return order;
        // 커밋 시 order 저장과 메시지 전송이 함께 반영됨
        // 실패 시 둘 다 롤백
    }
}

// 컨슈머
@Component
@RequiredArgsConstructor
public class OrderEventConsumer {

    private final PGMQClient pgmqClient;
    private final PGMQueue orderEventsQueue;

    @Scheduled(fixedDelay = 1000)
    public void consume() {
        pgmqClient.read(orderEventsQueue, new PGMQVisibilityTimeout(30))
            .ifPresent(message -> {
                try {
                    process(message);
                    pgmqClient.delete(orderEventsQueue, message.getMsgId());
                } catch (Exception e) {
                    // visibility timeout 후 재처리됨
                }
            });
    }
}
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

## 사용 사례

### Tembo

PGMQ 개발사. PostgreSQL 클라우드 플랫폼으로, 확장 생태계(Trunk)를 통해 다양한
PostgreSQL 확장을 쉽게 배포하고 사용할 수 있게 한다.

<https://tembo.io/>

### Supabase

Supabase Queues로 PGMQ를 통합 제공. 별도의 Redis나 외부 메시지 브로커 없이
Supabase 프로젝트 내에서 메시지 큐를 사용할 수 있다.

<https://supabase.com/docs/guides/queues>

### pgflow

Supabase용 워크플로우 엔진. PGMQ, pg_cron, Edge Functions를 조합하여 선언적
워크플로우를 구현한다. 외부 서비스(Bull, Redis, Temporal) 없이 Postgres만으로
워크플로우 상태를 관리한다.

<https://www.pgflow.dev/>

## 분석

### PGMQ의 핵심 가치는 인프라를 하나로 줄인 것이다

PGMQ의 존재 이유는 메시지 큐를 위해 별도 인프라를 두지 않아도 된다는 데 있다.
SQS는 AWS에, Redis는 별도 서버에, Kafka는 클러스터에 의존한다.
PGMQ는 이미 쓰고 있는 PostgreSQL 안에 큐를 넣어,
운영해야 할 시스템의 수를 줄인다.
백그라운드 워커도 외부 의존성도 없다는 강조가 이 지향을 담는다.

이 통합이 중요한 이유는 운영 복잡성이 곧 비용이기 때문이다.
메시지 큐를 위해 Redis나 RabbitMQ를 추가하면,
그 시스템의 배포·모니터링·장애 대응·백업이 새 부담이 된다.
HN에서 cauchyk가 이전 직장에서 RabbitMQ와 Postgres를 함께 썼는데
PGMQ가 있었다면 훨씬 편했을 것이라고 한 것이 이 부담을 증언한다.
큐를 데이터베이스 안으로 넣으면,
데이터베이스의 운영 인프라가 큐의 인프라를 겸한다.

가장 강력한 이점은 트랜잭션 통합이다.
PGMQ가 PostgreSQL 확장이므로 일반 트랜잭션 안에서 동작해,
비즈니스 로직과 메시지 발행을 원자적으로 처리한다.
이것은 별도 outbox 테이블 없이 Transactional Outbox 패턴을 구현하며,
kafka-streams-core-concepts에서 본,
결과 쓰기와 이벤트 발행을 원자적으로 묶는 문제를
데이터베이스 트랜잭션 하나로 푼다.
외부 큐로는 불가능한, 같은 데이터베이스이기에 가능한 정합성이다.

### 가시성 타임아웃이 정확히 한 번의 실체다

PGMQ가 내세우는 정확히 한 번(exactly once) 전달은
가시성 타임아웃 창 안에서의 보장이라는 조건이 붙는다.
메시지를 읽으면 타임아웃 동안 보이지 않게 되고,
그 안에 삭제되면 한 번만 처리된 것이지만,
컨슈머가 타임아웃 전에 처리를 끝내지 못하면
메시지가 다시 보여 재처리된다.

이 조건이 중요한 이유는 sqs-at-least-once-delivery와 정확히 이어지기 때문이다.
SQS도, 어떤 큐도 무조건적 정확히 한 번을 줄 수 없다.
PGMQ의 정확히 한 번은 컨슈머가 타임아웃 안에 처리를 완료할 때만 성립하며,
그렇지 못하면 최소 한 번으로 떨어진다.
따라서 컨슈머는 여전히 멱등해야 하고,
타임아웃 값을 처리 시간에 맞춰 조정해야 한다.
정확히 한 번이라는 이름은 강력하지만,
그 경계는 exactly-once-semantics에서 본 것과 같은 조건부 보장이다.

## 비평

### SQL 전용이 아닌 확장 방식이 매니지드 DB에서의 채택을 막는다

PGMQ의 가장 실질적인 약점은 배포 환경 제약이다.
GN에서 yangeok이 이 플러그인을 AWS RDS 같은 매니지드 DB에 추가할 수 있는지
물었고,
blackbeenie가 매니지드 서비스에서는 벤더가 지원하는 플러그인 외에는
쓸 수 없다고 답했다.
곧 확장으로 설치해야 하는 PGMQ는
RDS가 그것을 공식 지원하지 않으면 쓸 수 없다.

이 제약이 중요한 이유는 PostgreSQL 사용자 다수가 매니지드 DB를 쓰기 때문이다.
자체 호스팅 PostgreSQL에서는 확장을 자유롭게 설치하지만,
RDS, Cloud SQL 같은 매니지드 환경에서는 벤더의 허용 목록에 갇힌다.
personal-ai-router가 특정 하드웨어에, dreeve가 자체 호스팅 역량에 갇혔듯,
PGMQ의 확장 방식은 배포 환경에 갇힌다.
README가 SQL 전용 설치도 지원한다고 밝힌 것은 이 제약을 완화하려는 것이지만,
확장으로 얻는 성능과 기능을 SQL 전용에서 온전히 누릴 수 있는지는 별개다.

HN에서 ants_a가 이 지점을 정확히 짚었다.
왜 plpgsql이 아니라 Rust로 구현했는지,
로더블 확장이 필요한 기능을 쓰는 것 같지 않으며,
순수 SQL 기반이면 매니지드 DB에서 훨씬 쉽게 쓸 수 있다는 것이다.
이 질문은 PGMQ의 근본 설계 트레이드오프를 건드린다.
Rust 확장은 성능을 주지만 배포 유연성을 희생하고,
SQL 전용은 어디서나 돌지만 성능과 기능이 제한될 수 있다.

### 데이터베이스에 큐를 얹는 것이 규모에서 병목이 된다

PGMQ의 통합 이점은 규모에서 대가를 치른다.
큐 트래픽이 데이터베이스의 부하가 되므로,
높은 처리량의 메시징이 데이터베이스의 주 업무인
트랜잭션 처리와 자원을 다툰다.
전용 메시지 브로커가 메시징만 최적화하는 것과 달리,
PGMQ는 데이터베이스의 여유 안에서만 큐를 돌린다.

이 병목이 중요한 이유는 통합의 이점이 역전되는 지점이 있기 때문이다.
낮은 처리량에서는 인프라를 하나로 줄인 이점이 크지만,
높은 처리량에서는 큐가 데이터베이스를 압박해
정작 데이터베이스 본연의 성능을 해친다.
HN에서 pabloem1234가 벤치마크를 보고 싶다고 한 것은
이 규모 특성에 대한 정당한 궁금증이다.
어느 처리량까지 PGMQ가 전용 브로커의 대안이 되고,
어디서부터 데이터베이스가 병목이 되는지가
채택 결정의 핵심인데, README는 이를 명시하지 않는다.

write amplification 문제도 이 규모 우려의 일부다.
문서가 메시지 본문이 크면 별도 테이블에 ID만 참조하라고 권하는 것은,
PGMQ가 모든 메시지를 테이블 행으로 저장하기에
큰 메시지가 데이터베이스 쓰기 부하를 키우기 때문이다.
전용 브로커라면 신경 쓰지 않을 이 최적화를
사용자가 스스로 해야 하는 것은,
데이터베이스에 큐를 얹은 구조의 숨은 비용이다.

## 인사이트

### 하나의 데이터베이스로 충분하다는 흐름이 인프라 단순화를 이끈다

PGMQ가 드러내는 가장 이전 가능한 통찰은
Postgres 하나로 충분하다는 사고가
인프라 단순화의 큰 흐름을 이룬다는 점이다.
큐(PGMQ), 크론(pg_cron), 전문 검색, 벡터 검색(pgvector)까지
전통적으로 별도 시스템이던 것들이 PostgreSQL 확장으로 흡수된다.
GN 검색에 함께 나온 PgQue 같은 유사 프로젝트들이 이 흐름을 증언한다.

이 통찰이 중요한 이유는 modern-nodejs-2025와 같은 원리이기 때문이다.
그 글에서 Node.js가 fetch, 테스트 러너, 감시를 런타임에 흡수했듯,
PostgreSQL은 큐, 크론, 검색을 데이터베이스에 흡수한다.
플랫폼이 흔한 주변 기능을 흡수하면,
사용자는 조립해야 할 시스템의 수가 줄어든다.
그 자리를 채우던 Redis, RabbitMQ, 별도 검색 엔진의 역할이
데이터베이스 하나로 수렴한다.

두 번째 차수의 효과는 이것이 아키텍처 결정의 기본값을 바꾼다는 점이다.
과거에는 큐가 필요하면 먼저 Redis나 RabbitMQ를 떠올렸다.
이제는 이미 쓰는 PostgreSQL로 충분한지 먼저 묻게 된다.
pgflow가 Bull·Redis·Temporal 없이 Postgres만으로 워크플로를 구현하듯,
많은 시스템이 데이터베이스 하나로 재설계될 수 있다.
단순함이 기본값이 되고, 전용 시스템은 규모가 그것을 강제할 때만 도입된다.

### 정확성의 경계는 큐 종류를 가리지 않고 같은 자리에 선다

PGMQ의 정확히 한 번이 가시성 타임아웃 안에서만 성립한다는 것은
SQS, Kafka, PGMQ가 모두 같은 정확성의 경계에 섬을 보여 준다.
어떤 큐도 무조건적 정확히 한 번을 주지 못하고,
모두 조건부 보장과 멱등성 요구로 귀결된다.
큐의 구현이 Postgres든 클라우드든 클러스터든,
정확성의 근본 한계는 같다.

이 통찰이 새로운 프레임을 주는 이유는
큐 선택의 기준을 정확성에서 운영으로 옮기기 때문이다.
정확히 한 번을 어느 큐가 더 잘 주느냐는 사실 잘못된 질문이다.
셋 다 조건부로 주고 멱등성을 요구하기 때문이다.
그렇다면 진짜 선택 기준은 정확성이 아니라,
운영 복잡성, 트랜잭션 통합, 규모 특성이다.
PGMQ는 정확성에서 특별하지 않되,
트랜잭션 통합과 인프라 단순화에서 차별화된다.

세 번째 차수의 함의는 멱등성이 큐 사용의 보편 전제라는 것이다.
sqs-at-least-once-delivery에서 본,
분산 메시징에서 멱등성이 기본 설계 원칙이라는 통찰이
PGMQ에도 그대로 적용된다.
어떤 큐를 고르든 컨슈머는 멱등해야 하고,
그 멱등성이 있으면 큐의 정확성 보장 차이는 대체로 무의미해진다.
큐를 고를 때 정확히 한 번이라는 문구에 현혹되기보다,
자기 컨슈머가 멱등한지를 먼저 확인하는 것이
분산 메시징을 안전하게 쓰는 출발점이다.
