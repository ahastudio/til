# PgQue — 데드 튜플 없는 Postgres 큐

<https://github.com/NikolayS/pgque>

HN 토론: <https://news.ycombinator.com/item?id=47817349> (145점, 37개 댓글)

## 소개

PgQue는 순수 PL/pgSQL로 구현한 Postgres 기반 메시지 큐 라이브러리다.
핵심 문제의식은 명확하다: `SKIP LOCKED`와 `DELETE`/`UPDATE` 조합으로 구현한
전통적인 Postgres 큐는 지속적인 부하에서 데드 튜플(dead tuple) 비대화(bloat)를 유발하고,
이것이 결국 VACUUM 사이클을 마비시켜 “죽음의 소용돌이(death spiral)”로 이어진다.

PgQue는 Skype에서 수억 명 규모로 운용됐던 PgQ 엔진을 현대적인 Postgres 환경에 맞게
재구현해, 이 문제를 구조적으로 해결한다.
초당 약 86,000건 삽입·240만 건 읽기 성능을 달성하면서 30분 지속 테스트에서
데드 튜플 증가가 0건이었다는 것이 핵심 주장이다.

## 아키텍처

### 3가지 핵심 메커니즘

**스냅샷 기반 배치 처리**
소비자는 행 단위 클레임이 아닌 데이터베이스 스냅샷을 사용해 원자적 배치로 메시지를 수신한다.

**TRUNCATE 기반 테이블 순환**
개별 행을 삭제하는 대신 3개의 테이블을 순환하며 만료된 테이블을 TRUNCATE한다.
이것이 데드 튜플 생성을 원천 차단하는 핵심 기법이다.

**소비자별 독립 커서**
각 소비자가 공유 이벤트 로그 위의 자신만의 위치(포지션)를 유지한다.
데이터 복제 없이 자연스러운 팬아웃(fan-out)이 가능하다.

### 틱(Tick) 메커니즘

큐는 주기적인 “틱”(기본: 1초)으로 배치를 전진시킨다.
`pg_cron` 또는 외부 스케줄러가 틱을 구동한다.
이것이 PgQue의 근본적인 트레이드오프를 만든다: 엔드-투-엔드 전달 지연이
일반적으로 1–2초다(다음 틱까지 최대 1초 + 폴링 인터벌).

## 기존 솔루션과의 비교

| 기능             | PgQue | PGMQ | River | Que  | pg-boss |
| ---------------- | ----- | ---- | ----- | ---- | ------- |
| 제로 블로팅 설계 | ✅    | ❌   | ❌    | ❌   | ❌      |
| 외부 데몬 불필요 | ✅    | ✅   | ❌    | ❌   | ❌      |
| 매니지드 Postgres | ✅    | ✅   | ✅    | ✅   | ✅      |
| 팬아웃           | ✅    | ❌   | ❌    | ❌   | ✅*     |

*pg-boss의 팬아웃은 큐별 복사 방식으로, 공유 이벤트 로그와 다름

## 사용법

설치는 의도적으로 최소화됐다:

```sql
\i sql/pgque.sql
select pgque.start();  -- pg_cron 틱 활성화
```

기본 워크플로(각 단계는 별도 트랜잭션):

```sql
select pgque.create_queue('orders');
select pgque.subscribe('orders', 'processor');
select pgque.send('orders', '{"order_id": 42}'::jsonb);
select pgque.force_tick('orders');   -- 큐 전진
select * from pgque.receive('orders', 'processor', 100);
select pgque.ack(batch_id);
```

**역할(Role) 기반 접근 제어:**

- `pgque_reader` — 모니터링·대시보드
- `pgque_writer` — 프로듀서/컨슈머 (대부분의 앱)
- `pgque_admin` — 스키마 변경·유지 관리

## 분석

### Postgres 큐의 고질적 문제와 그 해법

SKIP LOCKED 패턴이 Postgres 큐 구현의 사실상 표준이 된 것은 단순성 때문이다.
하지만 Brandur가 Heroku에서 문서화한 것처럼, 이 패턴은 높은 처리량에서 필연적으로
VACUUM 경쟁을 야기한다.
PgQue의 TRUNCATE 기반 테이블 순환은 이 문제를 회피가 아닌 구조적 해소로 접근한다.

TRUNCATE는 DDL 연산으로 개별 행 삭제와 달리 데드 튜플을 생성하지 않는다.
3개 테이블을 순환하면서 현재 배치가 소비된 후 해당 테이블을 TRUNCATE하는 방식은,
PgQ 엔진이 Skype에서 수억 명 규모를 지원한 근거와 동일한 원리다.

mind-blight는 SKIP LOCKED 기반 큐에서 겪은 실제 프로덕션 장애를 공유했다.[^mind_blight]
큐 상태를 확인하는 쿼리 자체가 주요 성능 병목이 됐고, 처리량이 낮아질수록 큐가 쌓이며,
워커를 늘릴수록 DB 폴링 스트레스가 증가해 오히려 상황이 악화됐다고 전했다.
SKIP LOCKED는 단순해 보이지만, 높은 트래픽에서 예측 불가능하게 무너지는
패턴이 실제 운영 환경에서 반복적으로 확인된다.

### Skype 계보의 재등장

PgQ는 2000년대 중반 Skype가 구축했고, Londiste 복제 시스템의 기반이 됐다.
이 엔진을 현대 Postgres(매니지드 Postgres 포함)에서 순수 PL/pgSQL로 재구현했다는 것은,
수십 년의 실전 검증된 아키텍처를 접근 가능하게 만들었다는 의미다.

### PgQue는 큐인가, 로그인가

killingtime74는 PgQue가 SKIP LOCKED 큐의 대체재가 아니라 Kafka 유사 시스템에 가깝다고
재정의했다.[^killingtime74]
“SQS보다 SNS에 가깝고, RabbitMQ보다 Kafka에 가깝다”는 표현이 핵심이다.
각 소비자가 독립 커서로 공유 이벤트 로그를 구독하는 구조는 Kafka의 컨슈머 그룹과
같은 패턴이다.

adhocmobility는 같은 맥락에서 “이것은 큐가 아니라 로그”라고 직접적으로 주장했다.[^adhocmobility]
전통적인 큐는 워커 간 로드 밸런싱, ACK 시 삭제, 가시성 타임아웃을 갖는다.
PgQue는 이 의미론을 충족하지 않으므로 SKIP LOCKED 큐의 “대체”가 아닌 “보완”으로
포지셔닝해야 한다는 것이다.
이 구분은 실용적으로 중요하다: 잡 스케줄러가 필요한 팀과 이벤트 팬아웃이 필요한 팀은
서로 다른 도구를 찾고 있다.

## 비평

### 강점

지연-안정성 트레이드오프를 명시적으로 공개하는 정직함이 돋보인다.
1–2초의 전달 지연을 단점으로 명시하고, “서브 3ms 지연이 필요하면 맞지 않는다”고 인정한다.
TRUNCATE 기반 설계의 원리와 근거가 명확하게 설명된다.

### 약점

pg_cron 의존성은 모든 Postgres 환경에서 사용 가능하지 않다.
일부 매니지드 Postgres(예: 일부 RDS 구성)에서 pg_cron 설치가 불가능하거나 제한된다.
틱 주기가 1초로 고정되면 부하에 따른 동적 조정이 불가능하다.

“예비 벤치마크(preliminary benchmarks)”라는 표현은 실제 프로덕션 환경에서의
성능 검증이 아직 부족함을 인정한다.
86,000 이벤트/초 삽입이라는 숫자는 구체적인 하드웨어 스펙 없이는 해석이 어렵다.

saberd는 문서에서 지연 수치가 충돌한다고 지적했다.[^saberd]
“그래프에는 0.25ms 소비자 지연이 나오는데, 트레이드오프 섹션에는 엔드-투-엔드 1–2초라고
나온다”는 것이다.
이 혼란은 “소비자 함수 호출 자체의 지연”과 “메시지 발행부터 소비까지의 전체 지연”을
문서가 명확히 구분하지 않은 데서 온다.
틱 기반 아키텍처에서 이 두 지표의 의미 차이를 분명히 설명하는 문서 개선이 필요하다.

## 인사이트

### Postgres를 메시지 버스로 쓰는 판단의 유효성

Redis, Kafka, RabbitMQ 대신 Postgres 큐를 선택하는 이유는 “인프라 단순성”이다.
이미 Postgres를 사용하는 팀은 별도의 메시지 시스템을 추가하지 않고 큐를 운용할 수 있다.
운영·모니터링·트랜잭션 보장이 기존 데이터베이스 인프라 안에서 해결된다.

PgQue는 이 선택의 가장 큰 약점—블로팅—을 구조적으로 해소한다.
1–2초의 지연이 허용되는 사용 사례—이벤트 드리븐 백그라운드 처리, 비동기 알림,
팬아웃 이벤트—에서 PgQue는 Kafka나 RabbitMQ 도입 없이 신뢰할 수 있는 큐를 제공한다.
“인프라를 단순하게 유지하라”는 원칙과 정확히 맞닿는 도구다.

### 공유 이벤트 로그 패턴의 Postgres 구현

소비자별 독립 커서를 사용하는 공유 이벤트 로그 아키텍처는 Kafka의 핵심 설계 원리다.
Kafka에서 파티션과 컨슈머 그룹 오프셋이 하는 역할을,
PgQue에서는 Postgres 테이블과 소비자 커서가 담당한다.

이 설계의 장점은 팬아웃이 데이터 복제 없이 이루어진다는 것이다.
같은 이벤트를 10개의 서비스가 각자 소비하더라도, 저장 공간은 1배다.
Kafka를 도입하기엔 규모가 작고, 단순 큐로는 팬아웃이 어려운 중간 지점의 사용 사례에서
PgQue는 독보적인 포지션을 갖는다.

---

[^mind_blight]: <https://news.ycombinator.com/item?id=47820748>
[^killingtime74]: <https://news.ycombinator.com/item?id=47820975>
[^adhocmobility]: <https://news.ycombinator.com/item?id=47821775>
[^saberd]: <https://news.ycombinator.com/item?id=47819971>
