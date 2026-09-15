# Amazon SQS의 최소 한 번 전달: 중복은 예외가 아니라 계약이다

Amazon SQS 표준 큐는 모든 메시지를 적어도 한 번 전달하지만,
어떤 메시지는 두 번 이상 전달된다.
버그가 아니라 계약이고, 중복 방어는 애플리케이션의 몫이다.
이 문서는 그 계약 위에서 소비자를 어떻게 만들고 어떻게 검증하는지를 다룬다.

## 목차

- [30초 요약](#30초-요약)
- [중복은 어디서 오는가](#중복은-어디서-오는가)
  - [가장 흔한 경로를 시간순으로 따라가기](#가장-흔한-경로를-시간순으로-따라가기)
  - [생산자 재시도는 성격이 다르다](#생산자-재시도는-성격이-다르다)
- [소비자 만들기](#소비자-만들기)
  - [기본 골격](#기본-골격)
  - [처리가 길면 하트비트로 연장한다](#처리가-길면-하트비트로-연장한다)
- [멱등성 구현하기](#멱등성-구현하기)
  - [키부터 제대로 고른다](#키부터-제대로-고른다)
  - [조건부 쓰기로 잠금을 잡는다](#조건부-쓰기로-잠금을-잡는다)
  - [이 구조가 만드는 새로운 함정](#이-구조가-만드는-새로운-함정)
- [큐 유형 고르기](#큐-유형-고르기)
  - [FIFO가 실제로 보장하는 범위](#fifo가-실제로-보장하는-범위)
  - [선택 기준](#선택-기준)
  - [중복 제거 구간의 경계](#중복-제거-구간의-경계)
- [재시도와 DLQ 설정하기](#재시도와-dlq-설정하기)
- [값 정하기](#값-정하기)
  - [감시할 지표](#감시할-지표)
- [로컬에서 직접 확인하기](#로컬에서-직접-확인하기)
- [트레이드오프: 어느 쪽을 골라도 아픈 지점](#트레이드오프-어느-쪽을-골라도-아픈-지점)
  - [가시성 타임아웃: 늘려도 줄여도 손해다](#가시성-타임아웃-늘려도-줄여도-손해다)
  - [멱등성 저장소: 문제를 옮길 뿐 없애지 못한다](#멱등성-저장소-문제를-옮길-뿐-없애지-못한다)
  - [FIFO 전환: 기대한 것의 절반만 온다](#fifo-전환-기대한-것의-절반만-온다)
  - [`maxReceiveCount`: 중복과 유실 사이의 눈금](#maxreceivecount-중복과-유실-사이의-눈금)
  - [전체 조망](#전체-조망)
- [배포 전 체크리스트](#배포-전-체크리스트)
- [기억할 원칙](#기억할-원칙)
  - [시간 예산이 정확성을 결정한다](#시간-예산이-정확성을-결정한다)
  - [보장의 이름이 아니라 예외 조항을 읽는다](#보장의-이름이-아니라-예외-조항을-읽는다)

## 30초 요약

1. 중복은 세 가지 경로로 생기고, 실무에서는 **가시성 타임아웃 만료**가 압도적이다.
2. 멱등성 키는 `MessageId`가 아니라 **도메인 식별자**여야 한다.
3. FIFO 큐로 옮겨도 **소비자 멱등성은 여전히 필요하다**.
4. 중복을 겪으면 코드보다 **설정값(타임아웃, P99)** 을 먼저 본다.
5. `maxReceiveCount`는 사실상 **중복 횟수의 상한**을 정하는 값이다.

## 중복은 어디서 오는가

대응 방법이 경로마다 다르므로 뭉뚱그리면 안 된다.

| 경로            | 원인                                | 빈도             | 막는 방법                     |
| --------------- | ----------------------------------- | ---------------- | ----------------------------- |
| 저장소 이중화   | 사본 보유 서버가 삭제 시점에 불가용 | 드묾             | 소비자 멱등성                 |
| 가시성 타임아웃 | 처리가 타임아웃을 넘겨 재전달       | 매우 흔함        | 타임아웃 조정 + 하트비트      |
| 생산자 재시도   | 전송 응답 유실로 생산자가 재전송    | 상황에 따라 다름 | FIFO 중복 제거 또는 도메인 키 |

### 가장 흔한 경로를 시간순으로 따라가기

AWS 문서가 설명하는 경로는 저장소 이중화지만, 실제로 겪는 것은 대개 아래다.
기본 가시성 타임아웃 30초, 처리 시간 45초인 소비자를 가정한다.

```text
t=0s    워커 A가 메시지 M 수신 → M은 30초간 안 보임
t=10s   워커 A가 결제 API 호출 (부수 효과 1회차 발생)
t=30s   가시성 타임아웃 만료 → M이 큐에 다시 나타남
        ※ 워커 A는 이 사실을 통보받지 못한다. 계속 처리 중.
t=31s   워커 B가 같은 메시지 M 수신 (ApproximateReceiveCount=2)
t=41s   워커 B가 결제 API 호출 (부수 효과 2회차 발생 — 중복 결제)
t=45s   워커 A가 처리 완료 → DeleteMessage 호출 → 실패
        워커 A는 여기서 처음으로 자기가 늦었음을 안다
t=76s   워커 B가 처리 완료 → DeleteMessage 성공
```

여기서 배울 점이 세 가지다.

- 부수 효과는 이미 두 번 일어난 뒤에야 문제를 알게 된다.
- 워커 A는 만료를 통보받지 못한다. 가시성 타임아웃은 락처럼 보이지만 락이 아니다.
- 원인은 희귀한 인프라 사고가 아니라 `45초 > 30초`라는 결정론적 관계다.
  같은 부하가 걸리면 반드시 재현된다.

### 생산자 재시도는 성격이 다르다

`SendMessage`가 성공했는데 응답이 유실되면 생산자가 다시 보낸다.
큐에는 **서로 다른 `MessageId`를 가진 두 메시지**가 들어간다.
SQS 입장에서는 중복이 아니라 별개의 두 메시지이므로,
`MessageId` 기반 방어는 이 경로를 전혀 걸러 내지 못한다.

## 소비자 만들기

### 기본 골격

긴 폴링(`WaitTimeSeconds=20`)을 쓰고, 처리에 성공한 메시지만 삭제한다.

```python
import boto3

sqs = boto3.client("sqs")
QUEUE_URL = "https://sqs.ap-northeast-2.amazonaws.com/123456789012/orders"

def poll_forever():
    while True:
        resp = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,  # 긴 폴링: 빈 응답과 API 호출 비용을 줄인다
            VisibilityTimeout=60,
            MessageSystemAttributeNames=["ApproximateReceiveCount"],
        )
        for msg in resp.get("Messages", []):
            receive_count = int(msg["Attributes"]["ApproximateReceiveCount"])
            if receive_count > 1:
                # 재전달이다. 원인 분석을 위해 반드시 계측한다.
                metrics.increment("sqs.redelivered", tags=[f"count:{receive_count}"])
            try:
                handle(msg)
            except Exception:
                # 삭제하지 않는다 → 타임아웃 후 재전달되거나 DLQ로 간다
                logger.exception("handling failed", extra={"id": msg["MessageId"]})
                continue
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"],
            )
```

`ApproximateReceiveCount`는 삭제되지 않은 채 수신된 횟수다.
2 이상이면 재전달이라는 뜻이지만, 첫 전달에서는 항상 1이므로
중복을 판정하는 데는 쓸 수 있어도 막는 데는 쓸 수 없다.
이 값을 지표로 내보내는 것이 나중에 원인을 찾는 가장 빠른 길이다.

### 처리가 길면 하트비트로 연장한다

가시성 타임아웃은 만료를 알려 주지 않으므로, 사용하는 쪽이 직접 관리해야 한다.
처리 시간이 유동적이면 별도 스레드에서 주기적으로 연장한다.

```python
import threading

class VisibilityHeartbeat:
    """처리 중 주기적으로 가시성 타임아웃을 연장한다.

    interval 마다 visibility_timeout 으로 재설정하므로,
    interval 은 visibility_timeout 보다 충분히 짧아야 한다(여기서는 1/3).
    """

    def __init__(self, receipt_handle, visibility_timeout=60):
        self.receipt_handle = receipt_handle
        self.visibility_timeout = visibility_timeout
        self.interval = visibility_timeout / 3
        self.done = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self.done.wait(self.interval):
            try:
                sqs.change_message_visibility(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=self.receipt_handle,
                    VisibilityTimeout=self.visibility_timeout,
                )
            except sqs.exceptions.ClientError:
                # 이미 만료되었거나 삭제된 경우. 연장은 더 이상 의미가 없다.
                logger.warning("visibility extension failed; another worker may have it")
                return

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.done.set()


with VisibilityHeartbeat(msg["ReceiptHandle"], visibility_timeout=60):
    handle(msg)
```

연장에는 천장이 있다.
12시간 한도는 최초 수신 시점부터 계산되고, 연장해도 재설정되지 않는다.
그보다 긴 작업이라면 SQS 메시지 하나로 표현하지 말고
Step Functions를 쓰거나 작업을 쪼갠다.
작업이 길수록 SQS는 실행자가 아니라 실행을 촉발하는 신호여야 한다.

## 멱등성 구현하기

### 키부터 제대로 고른다

가장 흔한 실수가 여기서 나온다.

| 키 후보                     | 막는 중복                | 놓치는 중복   |
| --------------------------- | ------------------------ | ------------- |
| `MessageId`                 | 재전달(이중화, 타임아웃) | 생산자 재시도 |
| 도메인 식별자(주문 번호 등) | 세 경로 전부             | —             |

업무적으로 같은 사건인지를 판정해야 하므로 도메인 식별자를 쓴다.
메시지 본문에 그런 식별자가 없다면, 그것부터 생산자에 추가한다.

### 조건부 쓰기로 잠금을 잡는다

멱등성 검사와 실제 처리가 원자적이지 않다는 것이 근본 문제다.
검사를 통과한 두 워커가 동시에 처리에 들어갈 수 있으므로,
단순한 조회 후 기록 방식으로는 부족하다.
DynamoDB 조건부 쓰기로 잠금을 잡고 상태를 진행 중과 완료로 나눈다.

```python
import time
import botocore

ddb = boto3.client("dynamodb")
TABLE = "idempotency"
LOCK_TTL = 900     # 진행 중 잠금 유효 시간(초). 처리 최대 시간보다 길게.
RECORD_TTL = 86400 # 완료 레코드 보존 시간(초). 재전달 가능 범위보다 길게.

def process_once(key: str, work):
    now = int(time.time())
    try:
        ddb.put_item(
            TableName=TABLE,
            Item={
                "pk": {"S": key},
                "state": {"S": "IN_PROGRESS"},
                "lock_expires_at": {"N": str(now + LOCK_TTL)},
                "expires_at": {"N": str(now + RECORD_TTL)},
            },
            # 레코드가 없거나, 있어도 잠금이 만료된 경우에만 획득한다.
            ConditionExpression=(
                "attribute_not_exists(pk) OR "
                "(#s = :inprog AND #l < :now)"
            ),
            ExpressionAttributeNames={"#s": "state", "#l": "lock_expires_at"},
            ExpressionAttributeValues={
                ":inprog": {"S": "IN_PROGRESS"},
                ":now": {"N": str(now)},
            },
        )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] != "ConditionalCheckFailedException":
            raise
        item = ddb.get_item(
            TableName=TABLE,
            Key={"pk": {"S": key}},
            ConsistentRead=True,
        ).get("Item")
        if item and item["state"]["S"] == "DONE":
            return  # 이미 처리 완료. 조용히 성공 처리하고 메시지를 삭제한다.
        raise AlreadyInProgress(key)  # 다른 워커가 처리 중. 삭제하지 말고 재전달에 맡긴다.

    try:
        work()
    except Exception:
        # 잠금을 즉시 풀어 다음 재전달이 곧바로 재시도할 수 있게 한다.
        ddb.delete_item(TableName=TABLE, Key={"pk": {"S": key}})
        raise

    ddb.update_item(
        TableName=TABLE,
        Key={"pk": {"S": key}},
        UpdateExpression="SET #s = :done",
        ExpressionAttributeNames={"#s": "state"},
        ExpressionAttributeValues={":done": {"S": "DONE"}},
    )
```

직접 만들지 않아도 된다.
Lambda를 쓴다면 AWS Lambda Powertools의 멱등성 유틸리티가 같은 구조를 제공한다.

### 이 구조가 만드는 새로운 함정

멱등성 저장소를 도입하면 그 저장소만의 실패 양식이 생긴다.
도입 전에 알고 있어야 한다.

- **진행 중 상태로 굳는 문제.**
  워커가 강제 종료되면 레코드가 진행 중으로 남아 그 작업이 막힌다.
  위 코드의 `lock_expires_at` 조건이 이것을 푼다.
  이 장치가 없으면 기본 만료 시간까지 해당 키가 잠긴다.
- **TTL 삭제는 즉시가 아니다.**
  DynamoDB TTL은 최대 48시간까지 지연될 수 있으므로,
  만료 판정을 저장소의 삭제에 의존하지 말고 조회 시점에 직접 한다.
- **비용이 는다.** 처리 한 건마다 쓰기가 두 번 추가된다.
- **크기 제한.** 응답까지 저장한다면 400KB를 넘는 순간 저장이 실패한다.
- **만료 시간의 하한.**
  완료 레코드의 보존 시간이 재전달 가능 범위보다 짧으면,
  레코드가 사라진 뒤 도착한 재전달을 새 요청으로 처리한다.
  `maxReceiveCount` × 가시성 타임아웃보다 넉넉히 길게 잡는다.

## 큐 유형 고르기

### FIFO가 실제로 보장하는 범위

AWS는 FIFO 큐를 정확히 한 번 처리라고 부르지만,
이 이름을 그대로 믿으면 정확히 반대 방향의 결정을 하게 된다.

FIFO가 하는 일은 5분의 중복 제거 구간 안에서
같은 `MessageDeduplicationId`로 보낸 전송을 하나로 접는 것이다.
곧 세 경로 중 **생산자 재시도만** 막는다.

가시성 타임아웃 만료로 생기는 재전달은 FIFO에서도 그대로 일어난다.
AWS 문서는 두 큐 유형 모두에 대해,
최소 한 번 전달 모델 때문에 타임아웃 구간 안에 메시지가
두 번 이상 전달되지 않는다는 절대적 보장은 없다고 적는다.

따라서 **FIFO로 옮겨도 소비자 멱등성은 걷어 낼 수 없다.**
사라지는 것은 생산자 재시도로 인한 중복과 순서 문제뿐이다.

### 선택 기준

| 기준             | 표준 큐               | FIFO 큐                                    |
| ---------------- | --------------------- | ------------------------------------------ |
| 처리량           | 사실상 무제한         | 배치 없이 초당 300회, 배치 시 초당 3,000건 |
| 높은 처리량 모드 | —                     | 초당 30,000건 (그룹 내 순서 완화 조건)     |
| 순서             | 최선 노력             | 그룹 내 엄격한 순서                        |
| 생산자 중복 제거 | 없음                  | 5분 구간                                   |
| 소비자 멱등성    | 필요                  | 필요                                       |

FIFO를 고를 상황은 순서가 업무적으로 중요하거나,
생산자 재시도 중복이 실제로 관측될 때다.
멱등성 구현을 피하려는 목적이라면 잘못된 선택이다.

### 중복 제거 구간의 경계

`ContentBasedDeduplication`을 켜면 본문의 SHA-256 해시로
`MessageDeduplicationId`를 자동 생성한다.
이때 **메시지 속성은 해시 대상이 아니므로**,
본문이 같고 속성만 다른 두 메시지는 중복으로 접힌다.

5분 구간에도 한계가 있다.
전송은 성공했는데 응답이 유실되어 구간이 지난 뒤 같은 ID로 다시 보내면
SQS는 중복을 감지하지 못한다.
생산자의 재시도 정책이 이 5분 안에서 끝나도록 맞춘다.

## 재시도와 DLQ 설정하기

`maxReceiveCount`는 메시지가 DLQ로 옮겨지기 전까지 수신될 수 있는 횟수다.
동시에 이 값이 **중복 처리 횟수의 상한**을 정한다.
최소 한 번이라는 이름은 하한만 말하고 상한에는 침묵하는데,
실제 상한은 이 설정이 정한다.

지킬 것이 세 가지다.

- **`maxReceiveCount`를 1로 두지 않는다.**
  SQS가 전달로 기록했는데도 소비자가 실제로는 받지 못하는 경우가 있고,
  이때 추가 전달 시도가 없다.
  1로 두면 그 메시지는 한 번도 처리되지 못한 채 DLQ로 간다.
  AWS 자신이 이 설정을 권하지 않는다.
- **DLQ 보존 기간을 원본 큐보다 길게 잡는다.**
  표준 큐에서는 DLQ로 옮겨져도 최초 인큐 시각이 유지된다.
  원본 큐에서 하루를 보낸 메시지는 DLQ에서 남은 기간만 머문다.
- **DLQ에 메시지가 쌓이면 알림이 오게 한다.**
  DLQ는 만들어 두는 것으로 끝이 아니라 감시해야 의미가 있다.

참고로 표준 큐에서 `maxReceiveCount`가 3보다 클 때,
삭제되지 않은 채 3회 이상 수신된 메시지는 큐의 뒤로 보내진다.

## 값 정하기

처음 시작할 때 쓸 만한 기준이다. 측정한 뒤 조정한다.

| 설정                    | 시작값             | 정하는 근거                              |
| ----------------------- | ------------------ | ---------------------------------------- |
| 가시성 타임아웃         | 처리 P99 × 2       | 짧으면 중복, 길면 재시도 지연            |
| 하트비트 주기           | 타임아웃 ÷ 3       | 만료 전 최소 두 번의 연장 기회 확보      |
| `WaitTimeSeconds`       | 20 (최댓값)        | 빈 응답과 API 호출 비용 감소             |
| `maxReceiveCount`       | 3~5                | 일시 장애는 넘기고 독약 메시지는 격리    |
| 잠금 TTL                | 처리 최대 시간 × 2 | 워커 사망 시 자동 해제                   |
| 멱등성 레코드 TTL       | 재전달 총 기간 × 3 | 마지막 재전달 도착까지 레코드 유지       |
| DLQ 보존 기간           | 원본 큐보다 길게   | 최초 인큐 시각이 유지되므로              |

### 감시할 지표

- `ApproximateReceiveCount`가 2 이상인 메시지의 비율.
  이 값이 높으면 원인은 멱등성 부족이 아니라 타임아웃 설정이다.
- `ApproximateNumberOfMessagesNotVisible`(인플라이트).
  표준 큐 한도는 약 120,000건이다.
  한도에 닿으면 짧은 폴링은 `OverLimit` 오류를 받고,
  긴 폴링은 오류 없이 새 메시지를 받지 못한다.
- `ApproximateAgeOfOldestMessage`. 소비가 밀리는지를 본다.
- DLQ의 메시지 수.

## 로컬에서 직접 확인하기

읽는 것보다 한 번 재현해 보는 편이 빠르다.
ElasticMQ는 SQS 호환 API를 제공하는 가벼운 서버라 이 실험에 적합하다.
[kumo](../golang/kumo.md), [floci](../tool/floci.md),
[MiniStack](./ministack.md) 같은 로컬 AWS 에뮬레이터도 같은 `4566` 포트에서 쓸 수 있다.

```bash
# ElasticMQ 실행 (SQS 호환)
docker run -d --name elasticmq -p 9324:9324 softwaremill/elasticmq-native

export AWS_ACCESS_KEY_ID=x AWS_SECRET_ACCESS_KEY=x AWS_DEFAULT_REGION=ap-northeast-2
ENDPOINT="--endpoint-url http://localhost:9324"

# 가시성 타임아웃 5초짜리 큐를 만든다
aws $ENDPOINT sqs create-queue \
  --queue-name demo \
  --attributes VisibilityTimeout=5

QUEUE=$(aws $ENDPOINT sqs get-queue-url --queue-name demo --output text)

aws $ENDPOINT sqs send-message --queue-url "$QUEUE" --message-body '{"orderId":"A-1"}'

# 1) 받되 삭제하지 않는다
aws $ENDPOINT sqs receive-message --queue-url "$QUEUE" \
  --message-system-attribute-names ApproximateReceiveCount

# 2) 6초 기다린 뒤 다시 받는다 → 같은 메시지가 다시 온다
sleep 6
aws $ENDPOINT sqs receive-message --queue-url "$QUEUE" \
  --message-system-attribute-names ApproximateReceiveCount
```

두 번째 수신에서 같은 메시지가 `ApproximateReceiveCount=2`로 돌아온다.
처리 시간이 타임아웃을 넘겼을 때 벌어지는 일이 바로 이것이다.
여기에 하트비트를 붙여 같은 실험을 반복하면
연장이 재전달을 막는 것을 눈으로 확인할 수 있다.

## 트레이드오프: 어느 쪽을 골라도 아픈 지점

표로 정리하면 균형 잡힌 선택처럼 보이지만,
실제로는 어느 쪽을 골라도 감수해야 하는 통증이 있다.
그 통증이 무엇인지 알고 고르는 것과 모르고 고르는 것의 차이가 크다.

### 가시성 타임아웃: 늘려도 줄여도 손해다

이것이 가장 자주 마주치는 딜레마다.
양쪽 끝이 모두 나쁘고, 중간값도 조건이 바뀌면 다시 나빠진다.

| 선택        | 얻는 것          | 대가                                          |
| ----------- | ---------------- | --------------------------------------------- |
| 길게 잡는다 | 중복 재전달 감소 | 진짜 죽은 워커의 메시지도 그만큼 묶여 있다    |
| 짧게 잡는다 | 빠른 실패 재시도 | 정상 처리 중인 메시지까지 재전달된다          |

길게 잡을 때의 진짜 문제는 인플라이트 누적이 아니라
**장애 복구 시간이 그대로 늘어난다**는 것이다.
타임아웃을 10분으로 잡으면, 워커가 죽는 순간 그 메시지는 10분간 아무도 못 건드린다.
큐에 쌓인 수천 건이 같은 상황이면 복구가 분 단위가 아니라 시간 단위가 된다.

짧게 잡으면 정상 처리 중인 메시지가 재전달되어 중복 부수 효과가 상시로 발생한다.
그래서 하트비트로 푸는데, 하트비트도 공짜가 아니다.
처리마다 스레드가 하나 더 붙고, 연장 API 호출이 늘고,
무엇보다 **워커가 살아 있지만 멈춰 있는 경우(무한 루프, 외부 API 무응답)에는
하트비트가 계속 돌면서 죽은 작업의 잠금을 무한정 연장한다.**
프로세스 생존과 작업 진행은 다른 것인데 하트비트는 전자만 증명한다.

진짜 어려운 점은 P99가 고정값이 아니라는 것이다.
외부 API가 느려지는 날, 배포 직후 캐시가 비어 있는 시간대,
특정 고객의 큰 주문이 들어온 순간에 처리 시간이 몇 배로 튄다.
평상시 P99에 맞춘 타임아웃은 **하필 장애가 시작될 때 중복을 쏟아내기 시작한다.**
가장 필요 없을 때 문제가 커지는 구조다.

### 멱등성 저장소: 문제를 옮길 뿐 없애지 못한다

"멱등성을 구현하면 된다"는 말은 맞지만, 그 구현이 새로운 분산 시스템 문제를 만든다.

- **저장소가 새로운 단일 실패 지점이 된다.**
  DynamoDB가 느려지거나 스로틀링되면 멱등성 검사가 실패하고,
  그러면 처리 자체를 못 한다.
  중복을 막으려고 넣은 장치가 가용성을 떨어뜨린다.
  검사 실패 시 그냥 처리할 것인가(중복 위험), 실패 처리할 것인가(가용성 손실)?
  이 질문에 정답이 없다.
- **처리와 기록이 여전히 원자적이지 않다.**
  조건부 쓰기로 잠금을 잡아도, 실제 부수 효과(결제 API 호출)와
  완료 표시 사이에는 틈이 있다.
  그 틈에서 프로세스가 죽으면 결제는 됐는데 완료 기록은 없는 상태가 된다.
  다음 재전달이 결제를 한 번 더 한다.
  **이 틈은 원리적으로 없앨 수 없고, 좁힐 수만 있다.**
  최종적으로는 외부 시스템 쪽의 멱등성 키(결제 API가 제공하는 `Idempotency-Key`)에
  기대야 하는데, 모든 외부 시스템이 그것을 제공하지는 않는다.
- **레코드 만료 시간을 정할 근거가 약하다.**
  짧으면 늦게 온 재전달을 새 요청으로 처리하고,
  길면 저장소가 계속 커진다.
  재전달이 언제까지 올 수 있는지는 `maxReceiveCount`와 타임아웃으로 추정할 뿐
  확정할 수 없다. DLQ 재구동까지 고려하면 며칠 뒤에 올 수도 있다.

### FIFO 전환: 기대한 것의 절반만 온다

중복이 괴로워서 FIFO로 옮기려는 결정이 가장 흔한 함정이다.

얻는 것은 순서 보장과 생산자 재시도 중복 제거뿐이고,
가장 흔한 중복 경로인 가시성 타임아웃 재전달은 그대로 남는다.
멱등성 구현을 걷어 낼 수 없으므로, 비용만 지불하고 문제는 남는다.

게다가 FIFO의 순서 보장은 처리량을 직접 깎는다.
같은 `MessageGroupId`의 메시지는 한 번에 하나씩만 처리되므로,
그룹을 잘게 나누지 않으면 병렬성이 사라진다.
그런데 그룹을 잘게 나누면 나눈 만큼 순서 보장 범위도 좁아져서,
순서를 지키려고 FIFO를 골랐는데 처리량을 얻으려면 순서 범위를 포기하게 된다.

여기에 한 가지 더. 그룹 안의 한 메시지가 계속 실패하면
그 그룹 전체가 그 메시지 뒤에서 막힌다.
독약 메시지 하나가 그룹 하나를 통째로 멈추므로,
FIFO에서는 DLQ 설정이 표준 큐보다 더 급하다.
그런데 DLQ로 메시지를 빼내는 것 자체가 순서를 깨뜨린다.
AWS 문서도 순서가 정말 중요하면 FIFO에 DLQ를 쓰지 말라고 적는다.
곧 순서 보장과 장애 격리를 동시에 가질 수 없다.

### `maxReceiveCount`: 중복과 유실 사이의 눈금

이 값은 재시도 횟수처럼 보이지만 실제로는 두 가지를 동시에 정한다.

낮추면 중복 처리 상한이 내려가는 대신,
일시적 장애(배포 중 순단, 외부 API의 짧은 장애)를 넘기지 못한 메시지가
정상인데도 DLQ로 간다.
1로 두면 안 되는 이유가 극단적 사례일 뿐,
3도 배포 시간이 길면 부족할 수 있다.

높이면 일시 장애를 넘기지만,
독약 메시지가 그만큼 오래 큐에 남아 워커 자원을 계속 먹는다.
처리에 30초 걸리는 메시지를 10번 재시도하면 5분을 버리고,
그런 메시지가 수백 건이면 정상 메시지의 처리가 밀린다.

어려운 점은 이 둘을 구별할 방법이 큐 레벨에는 없다는 것이다.
일시적 장애로 실패한 메시지와 영원히 실패할 메시지가 같은 취급을 받는다.
구별하려면 애플리케이션이 예외 유형을 보고
재시도 가치가 없는 실패는 즉시 DLQ로 보내야 하는데,
그 판단 로직은 직접 만들어야 한다.

### 전체 조망

| 결정                     | 얻는 것                  | 대가와 남는 어려움                                 |
| ------------------------ | ------------------------ | -------------------------------------------------- |
| 표준 큐 선택             | 무제한 처리량            | 중복·순서 방어를 전부 직접 구현                    |
| FIFO 큐 선택             | 순서, 생산자 중복 제거   | 처리량 급감, 멱등성은 여전히 필요, DLQ와 순서 충돌 |
| 가시성 타임아웃 늘리기   | 중복 재전달 감소         | 장애 복구 시간이 그대로 늘어남                     |
| 가시성 타임아웃 줄이기   | 빠른 실패 재시도         | 정상 처리 중 재전달, 하트비트 복잡도 추가          |
| `maxReceiveCount` 늘리기 | 일시 장애 극복           | 독약 메시지가 자원을 오래 점유                     |
| 멱등성 저장소 도입       | 세 경로의 중복 모두 차단 | 새 단일 실패 지점, 원자성 틈은 여전히 남음         |

## 배포 전 체크리스트

- [ ] 처리 로직이 같은 메시지를 두 번 처리해도 안전한가.
- [ ] 멱등성 키가 `MessageId`가 아니라 도메인 식별자인가.
- [ ] 멱등성 레코드 TTL이 `maxReceiveCount` × 타임아웃보다 긴가.
- [ ] 잠금이 워커 사망 시 자동으로 풀리는가.
- [ ] 가시성 타임아웃이 처리 시간 P99보다 충분히 긴가.
- [ ] 처리 시간이 유동적이라면 하트비트로 연장하는가.
- [ ] 처리가 12시간을 넘길 가능성이 있는가. 있다면 작업을 나눴는가.
- [ ] `maxReceiveCount`가 1보다 큰가.
- [ ] DLQ가 있고, 보존 기간이 원본 큐보다 길고, 알림이 걸려 있는가.
- [ ] 순서가 뒤바뀐 메시지를 처리 로직이 견디는가. (표준 큐)
- [ ] 재전달 비율과 인플라이트 수를 지표로 내보내는가.

## 기억할 원칙

### 시간 예산이 정확성을 결정한다

처리 시간이 가시성 타임아웃보다 짧아야 하고,
연장의 총합이 12시간을 넘지 못하며,
생산자 재시도가 5분의 중복 제거 구간 안에 들어와야 하고,
멱등성 레코드의 만료 시간이 재전달 간격보다 길어야 한다.
어느 하나가 어긋나면 나머지가 모두 정상이어도 중복이 새어 나온다.

멱등성을 구현했는지는 예 아니오로 답할 수 있지만,
그 멱등성이 유효한 시간 범위가 재전달이 일어나는 범위를 덮는지는
숫자를 맞춰 봐야 답할 수 있다.
그래서 중복 처리 버그를 만나면 코드보다 설정값을 먼저 본다.

### 보장의 이름이 아니라 예외 조항을 읽는다

최소 한 번과 정확히 한 번은 강도의 차이처럼 들리지만,
실제로 둘을 가르는 것은 적용 범위다.
어떤 보장을 평가할 때는 이름을 비교하지 말고
어떤 경로로 그것이 깨지는지를 나열해 본다.
SQS의 세 가지 중복 경로를 나눠 보면
FIFO가 그중 하나만 막는다는 것이 바로 드러난다.

## 참고 자료

- [Amazon SQS at-least-once delivery](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html)
- [Amazon SQS visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
- [Amazon SQS queue types](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html)
- [Exactly-once processing in Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)
- [FIFO queue delivery logic in Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html)
- [Avoiding inconsistent message processing in Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/avoiding-inconsistent-message-processing.html)
- [Using dead-letter queues in Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- [ReceiveMessage — Amazon SQS API Reference](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html)
- [SendMessage — Amazon SQS API Reference](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html)
- [Idempotency — Powertools for AWS Lambda (Python)](https://docs.aws.amazon.com/powertools/python/latest/utilities/idempotency/)
