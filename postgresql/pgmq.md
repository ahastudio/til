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

## 클라이언트 라이브러리

공식 지원:

- Rust
- Python (psycopg3)

커뮤니티 지원:

- Go, Elixir, Java, Kotlin
- Node.js, TypeScript
- .NET, Ruby, PHP 등

### Java (Spring Boot)

<https://github.com/adamalexandru4/pgmq-spring>

```java
// 큐 생성
PGMQueue queue = new PGMQueue("my_queue");
pgmqClient.createQueue(queue);

// 메시지 전송
long messageId = pgmqClient.send(queue, "{\"key\": \"value\"}");

// 메시지 읽기 (visibility timeout 30초)
PGMQMessage message = pgmqClient.read(queue,
    new PGMQVisiblityTimeout(30)).orElseThrow();

// 메시지 삭제
pgmqClient.delete(queue, messageId);
```

### Kotlin

<https://github.com/vdsirotkin/pgmq-kotlin-jvm>

```kotlin
// Spring 설정
@Bean
fun pgmqConnectionFactory(dataSource: DataSource) =
    PgmqConnectionFactory {
        DataSourceUtils.getConnection(dataSource)
    }

@ConfigurationProperties(prefix = "pgmq")
data class PgmqConfigurationProps(
    override val defaultVisibilityTimeout: Duration = 30.seconds
) : PgmqConfiguration
```

### TypeScript

<https://github.com/Muhammad-Magdi/pgmq-js>

```typescript
import { Pgmq } from 'pgmq-js';

// 연결
const pgmq = await Pgmq.new({
  host: 'localhost',
  database: 'postgres',
  password: 'password',
  port: 5432,
  user: 'postgres',
});

// 큐 생성
await pgmq.queue.create('my_queue');

// 메시지 전송
interface Msg { id: number; name: string; }
const msg: Msg = { id: 1, name: 'test' };
const msgId = await pgmq.msg.send('my_queue', msg);

// 메시지 읽기 (visibility timeout 30초)
const received = await pgmq.msg.read<Msg>('my_queue', 30);

// 메시지 아카이빙
await pgmq.msg.archive('my_queue', msgId);
```

### Python (SQLAlchemy)

<https://github.com/jason810496/pgmq-sqlalchemy>

```python
from pgmq_sqlalchemy import PGMQueue

pgmq = PGMQueue(dsn='postgresql://user:pass@localhost:5432/db')

# 큐 생성
pgmq.create_queue('my_queue')

# 메시지 전송
msg = {'key': 'value'}
msg_id = pgmq.send('my_queue', msg)

# 배치 전송
msg_ids = pgmq.send_batch('my_queue', [msg, msg])

# 메시지 읽기
msg = pgmq.read('my_queue')

# 배치 읽기
msgs = pgmq.read_batch('my_queue', 10)
```

### Ruby

<https://github.com/mensfeld/pgmq-ruby>

```ruby
# 큐 생성
client.create('my_queue')

# 메시지 전송
msg_id = client.produce('my_queue', '{"key":"value"}')

# 메시지 읽기 (visibility timeout 30초)
msg = client.read('my_queue', vt: 30)
puts msg.message

# 메시지 삭제
client.delete('my_queue', msg.msg_id)

# 큐 삭제
client.drop_queue('my_queue')
```

## 사용 사례

- Tembo
- Supabase
- Sprinters
- pgflow

## 참고

[Postgres 큐 기술 선택 | GeekNews](
https://news.hada.io/topic?id=11042)
