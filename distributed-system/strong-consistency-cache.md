# That's not strong consistency cache architecture

[That's not strong consistency cache architecture](https://blog.magical.dev/tossbank-strong-cache)

토스뱅크의 캐시 아키텍처 글을 분석하며
Strong Consistency(강한 일관성)가 실제로 보장되는지
TLA+를 활용한 Formal Method로 검증한 아티클.

원문:
[캐시를 적용하기 까지의 험난한 길 (TPS 1만 안정적으로 서비스하기)](https://toss.tech/article/34481)

## 요약

### 토스뱅크 원문 요약

토스뱅크의 약관(Terms) 서버는 TPS 평균 1만,
최대 2만까지 늘어나면서 단일 Leader DB로는 한계에 도달.
Redis를 캐시 레이어로 도입하여 성능 문제를 해결했다.

- Write 시 Cache Evict(Unlink),
  Read 시 Cache Fill 방식의 Look-aside 패턴
- DB Commit 이후 Redis Unlink 수행
  (`@TransactionalEventListener`의 `AFTER_COMMIT`)
- Unlink 실패 대비 Circuit Breaker 적용
- Kafka Event 발행 순서 조정

### 이 글의 핵심 주장

**토스뱅크가 주장하는 강한 일관성은
실제로 보장되지 않는다.**

DB Commit과 Redis 조작이 원자적(Atomic)이지
않기 때문에 동시 요청 시 일관성이 깨지는
반례가 존재한다.
TLA+로 160만~300만 가지 시나리오를 검증하여
어떤 방식이 Read-Your-Writes를 만족하는지
체계적으로 증명했다.

## 일관성 모델 정의

### Strong Consistency (Linearizability)

모든 연산이 전역적으로 단일 순서를 가지며,
어떤 클라이언트든 최신 쓰기 결과를 즉시 읽는다.
분산 환경에서 구현 비용이 매우 높다.

### Read-Your-Writes (RYW)

사용자가 쓰기를 완료한 후
**그 사용자의** 다음 읽기에서
반드시 쓰기 결과를 반환해야 한다.
세션(Session) 기준 일관성 모델이다.

토스뱅크의 실제 요구사항:

> “약관 동의 또는 철회 요청 API 처리가 완료된 순간,
> 바로 다음 요청에 DB에 저장된 값이
> 응답되어야 한다.”

이것은 Linearizability가 아니라 RYW에 가깝다.
그런데 **이 RYW조차 보장되지 않는다**는 것이
이 글의 핵심이다.

## 기본 모델과 반례

### Look-aside 패턴의 의사 코드

```go
func read(userID string) string {
    result := redis.get(userID)
    if result != nil {
        return result
    }

    dbResult := db.findByID(userID)
    redis.set(userID, dbResult)

    return dbResult
}

func write(userID, newValue string) string {
    db.openTransaction()
    db.update(userID, newValue)
    db.commit()

    redis.unlink(userID)
    return newValue
}
```

### 핵심 반례

동시 요청에서 Read의 `redis.set`이
Write의 `redis.unlink` 이후에 도착하면
**이전 값으로 캐시가 채워진다.**

```txt
Read  : DB.get(v1) ---------> Redis.set(v1)
Write :     DB.commit(v2) -> Redis.unlink -> 응답
```

Write가 성공적으로 완료되었지만,
Read의 지연된 `set`이 캐시를 이전 값으로 오염시킨다.
이후 모든 Read는 TTL 만료 또는 다음 Write까지
**잘못된 값을 계속 반환**한다.

## 시도했지만 실패한 방법들

### 1. Circuit Breaker

Redis 호출 자체는 항상 성공한다.
Unlink도 성공하고, Set도 성공한다.
**정합성 문제는 장애가 아니라 순서 문제**이므로
Circuit Breaker가 열리지 않는다.

### 2. Unlink를 Transaction 안에서 수행

DB Commit 전에 Unlink를 해도 동일한 문제가 남는다.
DB Commit과 Unlink의 순서와 Read Path의
DB Read → Set 순서가 원자적이지 않기 때문이다.

심지어 DB Commit과 동시에 Unlink가
마법적으로 일어난다고 가정해도
Read Path의 비원자성 때문에 문제가 지속된다.

### 3. SET NX 사용

값이 이미 있으면 무시하는 SET NX를 써도
근본 원인인 **DB 순서와 Redis 순서의 불일치**가
해결되지 않는다.

### 4. Write에서 Cache Fill

Write 시 `redis.set`으로 최신 값을 채워도
동시 Write 요청 시 DB의 직렬화 순서와
Redis의 저장 순서가 달라질 수 있다.

### 5. Write에서 SET NX로 Cache Fill

동시 Write에서 먼저 SET NX에 성공한 값이
DB 기준으로는 이전 값일 수 있다.

### 6. Write에서만 Cache Fill (Read는 채우지 않음)

Write 간의 충돌이 여전히 존재하므로
DB와 Redis의 순서 불일치 문제가 그대로 남는다.

## 해결 방법

### 방법 1: 분산 Lock

Write 시점에 분산 Lock을 잡아
DB Commit과 Redis SET의 순서를 보장한다.

```go
func write(userID, newValue string) string {
    l := distLock.lock(userID)
    defer distLock.unlock(l)

    db.openTransaction()
    db.update(userID, newValue)
    db.commit()

    redis.set(userID, newValue)
    return newValue
}
```

Read에서는 SET NX를 사용한다.
TLA+로 160만 가지 시나리오 검증 통과.

장점: Write-only Lock이므로
Read Heavy 트래픽에 적합.
단점: Lock으로 인한 latency 증가.

### 방법 2: Versioned Conditional Set (VCS)

각 값에 version을 부여하고,
Redis는 **더 높은 version의 값만** 수용한다.
MVCC의 단순화된 형태.

```lua
local curVersion = tonumber(
    redis.call("GET", verKey)
) or 0

if newVersion > curVersion then
    redis.call("SET", verKey, newVersion)
    redis.call("SET", dataKey, newData)
    return 1
else
    return 0
end
```

#### 단, VCS만으로는 부족하다

- Read에서만 VCS 사용: Unlink와 순서 꼬임 발생
- Write에서 VCS + Read에서 SET NX:
  TTL이 없으면 동작하지만
  **TTL(캐시 만료)이 있으면 RYW 위반**

### TTL 문제

Redis 캐시는 TTL로 만료된다.
TTL 만료, 메모리 부족에 의한 eviction,
관리자의 수동 삭제 등으로
캐시가 사라지면 순서 보장이 깨진다.

TTL이 있는 환경에서의 해결책:

| 방법                            | RYW 보장     |
|---------------------------------|--------------|
| Write VCS + Read SET NX         | TTL 시 위반  |
| Write VCS + Read VCS            | TTL 시 위반  |
| Write Lock + Read SET NX        | TTL 시 위반  |
| Read&Write 전체 Lock            | 보장됨       |
| Read(miss 시 Lock+VCS) + Write  | 보장됨       |

TTL 환경에서 RYW를 보장하려면
**Read의 Cache Miss 시점에서
DB Read 이전에 Lock을 잡아야** 한다:

```go
func read(userID string) string {
    result := redis.get(userID)
    if result != nil {
        return result
    }

    l := distLock.lock(userID)

    dbResult := db.findByID(userID)
    redis.VCS(userID, dbResult)

    distLock.unlock(l)

    return dbResult
}
```

## 분석

### 왜 이 문제가 어려운가

1. **비원자적 복합 연산**: DB와 Redis는 독립된
   저장소이며 두 연산을 원자적으로 수행할 수 없다.
2. **지수적 시나리오 폭발**: 동시 프로세스가
   늘어나면 상태 공간이 지수적으로 증가한다.
   개발자의 직관으로는 모든 경우를 탐색할 수 없다.
3. **확률의 함정**: 낮은 확률이라도 대규모 트래픽에서
   시간이 지나면 반드시 발생한다.

### 확률 추정 (원문의 산술)

```txt
읽기: 10,000건/초, 쓰기: 10건/초(피크)
동시 접속: 5,000명, 쓰기 duration: 200ms

동시 쓰기 = 10 × 0.2 = 2건
동일 유저 충돌 확률 = 2 / 5,000 = 0.04%
하루 충돌 횟수 ≈ 346건
```

0.04%는 무시할 수 있어 보이지만,
MSA에서 하나의 요청이 여러 내부 호출로
파생되면 **거의 동시에** 도착할 수 있다.
약관처럼 정합성이 치명적인 도메인에서
하루 346건의 잠재적 불일치는 심각하다.

## 비평

### 반박 대상이 원문의 주장이 아니라 원문이 쓴 단어다

제목은 그것은 강한 일관성 캐시 아키텍처가 아니라는 선언이다.
그런데 글 스스로 토스뱅크의 실제 요구사항이 선형화 가능성이 아니라 읽기 후 쓰기 보장에 가깝다고 정리한다.

그렇다면 원문이 잘못한 것은 설계가 아니라 용어 선택이고, 그 둘은 무게가 전혀 다르다.
강한 일관성이라는 말을 느슨하게 쓴 것은 흔한 일이며,
같은 글이 그 용어의 정의를 앞에서 직접 제시해야 했다는 사실 자체가
원문이 그 엄밀한 의미로 말하지 않았음을 보여 준다.

실질적인 발견은 따로 있다.
원문이 실제로 달성하려던 읽기 후 쓰기조차 보장되지 않는다는 것이고, 이것이 이 글의 진짜 기여다.
제목과 첫 주장이 용어 쪽에 서 있으면 그 기여가 논쟁처럼 읽히고,
읽는 쪽에서는 표현을 고치면 끝나는 문제로 오해할 여지가 생긴다.

### 시나리오 수가 검증 범위의 증거로 쓰인다

TLA+로 160만에서 300만 가지 시나리오를 검증했다는 진술이 논증의 무게를 지탱한다.

상태 공간의 크기는 모델이 얼마나 촘촘한지를 말할 뿐 얼마나 현실에 가까운지를 말하지 않는다.
모델에 프로세스를 몇 개 두었는지, 연산을 어느 단위까지 쪼갰는지에 따라 이 수는 크게 달라지고,
같은 시스템에서 파라미터 하나만 올려도 숫자가 한 자릿수 커진다.

더 중요한 것은 모델에 들어가지 않은 것들이다.
네트워크 분단, Redis 노드 장애와 승격, 클라이언트 재시도, 요청 타임아웃 후의 늦은 도착,
복제 지연이 있는 읽기 전용 노드, 서버 간 시계 차이가 그렇다.
이 중 무엇을 모델에 넣었고 무엇을 추상화했는지가 결론의 적용 범위를 정하는데,
그 목록이 제시되지 않으면 검증 통과라는 결과가 어디까지 유효한지 알 수 없다.
형식 기법의 가치는 무엇을 증명했는지보다 무엇을 가정했는지를 명시하는 데 있다는 점에서 아쉬운 공백이다.

### 최종 해법이 캐시를 도입한 이유와 충돌한다

TTL이 있는 환경에서 읽기 후 쓰기를 보장하는 방법으로 제시된 것은
읽기 경로의 캐시 미스 시점에 데이터베이스를 읽기 전에 분산 잠금을 잡는 구성이다.

이 구성의 비용이 논의되지 않는다.
원문의 출발점은 초당 1만에서 2만의 읽기를 단일 리더 데이터베이스로 감당할 수 없다는 것이었고,
캐시는 그 읽기를 데이터베이스에서 떼어 내기 위한 장치였다.
그런데 캐시 미스마다 잠금을 잡으면, 캐시가 비는 순간마다 읽기 경로에 직렬화 지점이 생긴다.

특히 문제가 되는 상황이 TTL 만료와 노드 재시작과 대량 축출이다.
같은 키를 찾는 읽기 수천 건이 동시에 미스를 내고 모두 같은 잠금을 기다린다.
그 기다림이 곧 지연이고, 잠금 서버는 이제 읽기 경로 전체가 의존하는 새로운 단일 장애점이 된다.
잠금 획득에 실패하거나 잠금 서버가 느려졌을 때 무엇을 할지가 정해지지 않으면,
정합성을 얻고 가용성을 잃는 교환이 조용히 일어난다.

방법 1의 단점으로 잠금에 따른 지연 증가가 한 줄 적혀 있지만,
그것은 쓰기 경로의 잠금에 대한 서술이고 최종 해법의 읽기 경로 잠금에 대한 것이 아니다.

### 충돌 확률 계산이 잘못된 축을 잰다

하루 346건이라는 추정이 위험의 크기를 보여 주는 숫자로 제시된다.
초당 쓰기 10건에 지속 시간 200밀리초를 곱해 동시 쓰기 2건을 얻고,
동시 접속 5천 명으로 나누어 0.04%를 얻는 계산이다.

이 산술은 사용자가 균등하게 분포하고 요청이 서로 독립이라고 가정한다.
실제 트래픽은 그렇지 않다.
공지 발송 직후나 약관 개정 시점처럼 같은 키에 쓰기가 몰리는 순간이 있고,
글 스스로 지적하듯 하나의 요청이 여러 내부 호출로 파생되면 같은 사용자의 요청이 거의 동시에 도착한다.
두 조건 모두 충돌 확률을 평균값보다 훨씬 높이는 방향인데, 계산은 평균으로만 이루어진다.

축 자체도 어긋나 있다.
이 반례의 피해는 충돌이 일어난 횟수가 아니라 오염된 캐시가 유지되는 시간이다.
한 번의 충돌로 잘못된 값이 캐시에 들어가면 TTL이 만료되거나 다음 쓰기가 올 때까지 모든 읽기가 그 값을 받는다.
초당 1만 건의 읽기에서 TTL이 몇 분이라면, 한 번의 충돌이 수백만 건의 잘못된 응답이 된다.
346건이라는 수를 적을 자리에 필요한 것은 그 곱셈이다.

## 인사이트

### 1. “Hope is not a strategy”

머릿속으로 한두 가지 케이스를 상상해서
잘 동작하는 것을 확인하는 것은 전략이 아니다.
**일관성 모델을 명확히 정의하고,
체계적으로 검증해야 한다.**

### 2. Formal Method의 실용성

TLA+를 사용하면 수백만 가지 시나리오를
자동으로 탐색할 수 있다.
사람이 놓치는 교묘한 인터리빙을 잡아내며,
모델을 변형하면서 빠르게 검증-반복할 수 있다.
**분산 시스템 설계에 TLA+는
선택이 아니라 필수에 가깝다.**

### 3. 캐시 일관성의 근본 난제

DB와 캐시는 독립된 상태 저장소다.
두 저장소 간의 순서를 맞추려면
**반드시 추가 메커니즘(Lock 또는 VCS)이 필요**하다.

- Look-aside 패턴 자체는 일관성을 보장하지 않는다.
- Circuit Breaker는 장애 차단이지
  일관성 보장 도구가 아니다.
- SET NX, TTL 조정 등 단순한 Redis 기능으로는
  해결할 수 없다.

### 4. 가정을 명시하라

> “이 가정이 깨졌을 때 우리 시스템은
> 어떻게 동작하는가?”

대답이 “모르겠다”라면
리스크를 관리하는 게 아니라
**운에 맡기는 것**이다.

네트워크 지연, GC STW, TTL 만료,
Redis 메모리 eviction 등
**어떤 가정에 기대고 있는지 아는 것**이
분산 시스템 설계의 출발점이다.

### 5. 트레이드오프를 인식하라

| 메커니즘       | 비용                   |
|----------------|------------------------|
| 분산 Lock      | Latency 증가           |
| VCS            | 구현 복잡도 증가       |
| TTL 제거       | 메모리 비용 증가       |
| 전체 Lock      | 동시성 대폭 감소       |

일관성은 공짜가 아니다.
비즈니스 요구사항에 따라
어떤 일관성 모델을 선택하고,
그에 맞는 **최소한의 정확한 구현**을
하는 것이 핵심이다.

### 6. 겸손한 비판의 자세

저자는 토스뱅크를 비난하지 않으며,
블로그 글의 제약으로 생략된 부분이 있을 수 있고,
내부적으로 Lock이나 추가 메커니즘을
사용할 가능성이 높다고 전제한다.
기술 비평은 **시스템을 더 잘 이해하기 위한
훈련**이어야 한다.
