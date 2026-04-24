# Honker: SQLite 기반 Pub/Sub 및 작업 큐

원문: <https://github.com/russellromney/honker>

## 소개

Honker는 SQLite 확장으로 구현된 Pub/Sub 메시징, 작업 큐, 이벤트 스트림 시스템이다.
Redis나 별도 메시지 브로커 없이 단일 `.db` 파일 안에서
PostgreSQL 스타일의 `NOTIFY`/`LISTEN` 의미론을 구현한다.
Rust 코어(`honker-core`)를 기반으로 SQLite 로더블 확장(loadable extension)과
Python, Node.js, Rust, Go, Ruby, Bun, Elixir 언어 바인딩을 제공한다.
Apache 2.0 라이선스다.

핵심 기능은 다섯 가지다:
크로스 프로세스 알림(단일 자리 ms 지연), 재시도·우선순위·지연 실행·데드레터를 갖춘
작업 큐, 비즈니스 쓰기와 메시지 발송을 같은 트랜잭션에 묶는 원자적 결합,
소비자별 오프셋을 추적하는 내구성 스트림, cron 표현식과 리더 선출을 갖춘 스케줄러.
의도적으로 제외한 것은 태스크 파이프라인/워크플로 DAG, 멀티 라이터 복제,
원격 서버 아키텍처다.

## 작동 원리

### WAL 파일 폴링

Honker는 SQLite의 WAL(Write-Ahead Logging) 모드를 핵심 조율 메커니즘으로 활용한다.
데이터베이스를 지속적으로 폴링하는 대신,
데이터베이스당 단 하나의 stat 스레드가 `.db-wal` 사이드카 파일을 1ms 주기로 감시한다.
파일 크기나 mtime이 변경되면 바운디드 채널을 통해 모든 구독자에게 웨이크 신호를 보내고,
구독자는 인덱스 기반 `SELECT`만 실행한다.
대기 중에는 CPU를 거의 소비하지 않고, 알림 지연은 평균 1~2ms(M 시리즈 기준)다.

Honker는 의도적으로 “과잉 트리거(overtrigger)” 전략을 쓴다.
WAL 변경이 발생하면 무조건 모든 구독자를 깨우고,
관련 없는 알림은 저렴한 인덱스 조회로 걸러낸다.
선택적 트리거로 중요한 업데이트를 놓치는 위험보다
불필요한 조회 비용을 감수하는 것이 낫다는 판단이다.

### 큐 스키마와 클레임 연산

```
_honker_live: 대기 중·처리 중 작업
  인덱스: (queue, priority DESC, run_at, id) PARTIAL WHERE state='pending'

_honker_dead: 재시도 소진 작업
```

클레임은 `UPDATE … RETURNING`을 부분 인덱스를 통해 단 한 번 실행하고,
확인(ack)은 `DELETE` 한 번이다.
트랜잭션 아웃박스(transactional outbox) 패턴이 자동으로 구현된다—
`enqueue()`, `publish()`, `notify()` 함수는 호출자의 트랜잭션 안에서 행을 삽입하므로
비즈니스 로직 쓰기와 메시지 발송이 원자적으로 커밋되거나 롤백된다.

## 사용법

### Python: 작업 큐

```python
import honker
db = honker.open("app.db")
emails = db.queue("emails")

# 비즈니스 로직과 원자적으로 인큐
with db.transaction() as tx:
    tx.execute("INSERT INTO orders (user_id) VALUES (?)", [42])
    emails.enqueue({"to": "alice@example.com"}, tx=tx)

# 워커: 자동 웨이크로 소비
async for job in emails.claim("worker-1"):
    send(job.payload)
    job.ack()
```

### Python: 태스크 데코레이터

```python
@emails.task(retries=3, timeout_s=30)
def send_email(to: str, subject: str) -> dict:
    return {"sent_at": time.time()}

result = send_email("alice@example.com", "Hi")
print(result.get(timeout=10))  # 워커 완료까지 블록
```

### Python: 내구성 스트림

```python
stream = db.stream("user-events")

with db.transaction() as tx:
    tx.execute("UPDATE users SET name=? WHERE id=?", [name, uid])
    stream.publish({"user_id": uid, "change": "name"}, tx=tx)

async for event in stream.subscribe(consumer="dashboard"):
    await push_to_browser(event)
```

### SQLite 확장 직접 사용

```sql
.load ./libhonker_ext
SELECT honker_bootstrap();

INSERT INTO _honker_live (queue, payload)
  VALUES ('emails', '{"to":"alice"}');

SELECT honker_claim_batch('emails', 'worker-1', 32, 300);
SELECT honker_ack_batch('[1,2,3]', 'worker-1');

SELECT honker_scheduler_register('nightly', 'backups', '0 3 * * *', '"go"', 0, NULL);
SELECT honker_scheduler_tick(unixepoch());
```

## 보존 정책

| 대상     | 정책                                                        |
| -------- | ----------------------------------------------------------- |
| 큐       | 확인(ack)까지 유지, 재시도 소진 시 `_honker_dead`로 이동   |
| 스트림   | 무기한 유지, 소비자별 오프셋을 `_honker_stream_consumers`에 추적 |
| 알림     | 자동 정리 없음, `db.prune_notifications(older_than_s=…)` 수동 호출 |

보존 정책이 라이브러리 기본값 내부에 숨겨지지 않고 애플리케이션 코드에 명시된다.

## 분석

### 트랜잭셔널 아웃박스의 자동 구현

Honker의 가장 큰 기술적 기여는 트랜잭셔널 아웃박스 패턴을
라이브러리 수준에서 자동화한다는 점이다.
분산 시스템에서 비즈니스 쓰기와 메시지 발송을 원자적으로 처리하는 것은
고전적인 난제다.
“주문을 DB에 저장했지만 이메일 큐 발송 전에 장애가 발생하면?”이라는 문제가
SQLite의 트랜잭션 경계 안에서 자연스럽게 해결된다.
`enqueue()`를 같은 트랜잭션 안에서 호출하면 두 연산은 원자적으로 커밋되거나 롤백되므로
이중 발송이나 누락 발송이 불가능하다.

PostgreSQL, MySQL에서 이 패턴을 구현하려면 별도의 아웃박스 테이블과
폴링 워커를 설계·운영해야 한다.
Honker는 단일 파일 SQLite의 ACID 보장 위에서 이 복잡성을 흡수한다.

### WAL 폴링의 영리함과 트레이드오프

`.db-wal` 파일 stat 폴링은 SQLite 내부 API를 우회하지 않고도
“뭔가 바뀌었다”는 신호를 크로스 프로세스로 전달하는 영리한 방법이다.
SQLite는 기본적으로 다중 프로세스 알림 메커니즘을 제공하지 않는다.
파일 시스템의 mtime은 OS가 관리하는 공유 상태이므로
별도의 IPC(프로세스 간 통신) 인프라 없이 이벤트를 감지할 수 있다.

그러나 1ms 폴링은 완전한 푸시 방식이 아니다.
최선의 경우 1ms, 최악의 경우 2ms의 지연이 항상 존재한다.
실시간성이 매우 중요한 맥락—고빈도 트레이딩, 실시간 게임—에는 적합하지 않지만,
웹 서비스의 백그라운드 작업 큐, 이벤트 알림 등 대부분의 비즈니스 맥락에는 충분하다.

### “하나의 파일로 충분하다”는 철학

Honker는 Redis, RabbitMQ, Kafka처럼 별도 인프라를 요구하지 않는다.
단일 `.db` 파일이 메시지 브로커, 큐, 스트림 스토리지를 모두 담는다.
이 철학은 배포 복잡성을 극적으로 낮춘다.
Redis 클러스터를 운영하고 연결 풀을 관리하고 복제를 구성하는 대신,
파일 하나를 공유 디렉터리에 두면 된다.

이 접근법은 단일 서버 또는 소수 서버 환경에서 최적화되어 있다.
SQLite는 단일 라이터(single writer) 제약이 있으므로,
다중 라이터가 경쟁하는 고트래픽 분산 환경에서는 병목이 발생한다.
“의도적으로 제외한” 멀티 라이터 복제가 이 한계를 명시하고 있다.

## 비평

### 강점

7개 언어 바인딩을 Rust 코어 하나에서 공유하는 구조는 언어 생태계 호환성을 보장한다.
크로스 언어 통합 테스트로 스키마 호환성을 검증한다는 점도 신뢰할 수 있다.
보존 정책을 애플리케이션 코드에 노출하는 설계 결정은
“라이브러리 기본값이 프로덕션 데이터를 조용히 삭제한다”는 함정을 피한다.
비명시적 전제보다 명시적 설계가 장기 운영에서 훨씬 안전하다.

### 약점

SQLite의 단일 라이터 제약은 큐 처리량의 상한을 결정한다.
`UPDATE … RETURNING`으로 작업을 클레임하는 방식은
다수의 워커가 동시에 클레임을 시도할 때 쓰기 잠금 경쟁이 발생한다.
초당 수천 건이라는 성능 수치는 단일 라이터 기준이며,
워커 수가 늘어날수록 쓰기 경합이 증가해 실제 처리량이 비선형으로 저하될 수 있다.

또한 WAL 모드는 기본적으로 단일 라이터만 허용하므로,
동일한 `.db` 파일에 접근하는 애플리케이션이 다른 곳에서도 쓰기를 수행한다면
잠금 타임아웃이 발생할 수 있다. 운영 환경에서 이 트레이드오프를 미리 검증해야 한다.

## 인사이트

### “작은 데이터” 시스템에서 브로커의 과잉 복잡성

현대 백엔드 개발에서 Redis는 거의 당연한 의존성이 되었다.
캐싱, 세션, Pub/Sub, 작업 큐를 Redis 하나로 처리하는 패턴이 일반화되었지만,
대다수 애플리케이션의 실제 메시징 트래픽은 Redis가 감당해야 할 규모와 거리가 멀다.
하루 수천에서 수만 건의 이벤트를 처리하는 서비스에서
Redis 클러스터를 운영하는 것은 명백한 과잉 복잡성이다.

Honker는 이 과잉을 인식하고 SQLite라는 이미 존재하는 인프라 위에 메시징을 구현한다.
SQLite는 이미 대부분의 애플리케이션에서 임베디드 스토리지로 사용되거나,
Litestream, LiteFS 같은 도구로 복제·백업이 가능한 단일 파일 데이터베이스로 진화했다.
“메시지 브로커를 추가한다”는 결정 대신
“기존 SQLite에 메시징을 추가한다”는 결정은
운영 복잡성을 더하는 방향이 아니라 기존 복잡성 안에 흡수하는 방향이다.
이 차이는 소규모 팀에게 특히 의미 있다.

### 로컬 퍼스트(local-first) 아키텍처의 메시징 레이어

Honker가 해결하는 문제는 로컬 퍼스트 소프트웨어 패러다임과 깊이 연결된다.
로컬 퍼스트 아키텍처에서 SQLite는 애플리케이션 상태의 중심이 된다.
그러나 동일한 `.db` 파일을 여러 프로세스 또는 탭이 공유할 때
“A가 데이터를 변경했다는 사실을 B에게 어떻게 알리는가”라는 문제가 남는다.
서버 없는 환경에서 WebSocket, SSE, 폴링 없이 이 문제를 해결하려면
파일 시스템 수준의 이벤트가 필요하다.

WAL 파일 stat 폴링은 이 문제에 대한 파일 시스템 기반 해법이다.
OS가 관리하는 파일 mtime을 신호로 사용하면
네트워크 소켓이나 OS 레벨 IPC 없이도 프로세스 간 이벤트 전파가 가능하다.
이 접근법은 SQLite를 “단순한 파일 DB”에서
“프로세스 경계를 넘는 이벤트 버스”로 승격시킨다.
Honker의 진짜 가치는 특정 기능이 아니라 SQLite의 역할을 재정의한다는 점에 있다.

### 언어 생태계 다중화와 Rust 코어의 전략적 위치

Honker가 7개 언어 바인딩을 제공하는 것은 단순한 포팅 작업이 아니다.
Rust로 작성된 단일 코어(`honker-core`)가 SQLite 확장과 모든 언어 바인딩의
기반이 된다는 구조는 여러 이점을 갖는다.

첫째, 버그 수정과 성능 개선이 모든 언어 바인딩에 동시에 반영된다.
각 언어 포트를 독립적으로 유지했다면 언어별로 버그가 다르게 나타나는
“생태계 단편화” 문제가 발생했을 것이다.
둘째, PyO3(Python), NAPI(Node.js), `cgo`(Go) 같은 외부 함수 인터페이스가
Rust 코어와 각 언어를 직접 연결하므로
크로스 런타임 데이터 직렬화 비용이 최소화된다.
셋째, Rust의 메모리 안전성이 SQLite 확장 레이어에서 발생할 수 있는
use-after-free, 버퍼 오버플로 같은 취약점을 구조적으로 방지한다.

SQLite 확장을 Rust로 작성하는 패턴은
`cr-sqlite`, `sqlite-vec` 같은 다른 SQLite 확장 생태계에서도 확산되고 있다.
SQLite의 C 인터페이스가 넓고 강력하지만 안전하지 않은 반면,
Rust의 FFI를 통한 래핑은 SQLite의 확장성과 Rust의 안전성을 결합하는
현실적인 전략으로 자리잡고 있다.
