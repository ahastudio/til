# Sentry에서 요청 수가 아니라 지속 시간으로 트랜잭션 샘플링하기

원문: [How to setup duration based profiling in Sentry | Neil Kakkar](https://neilkakkar.com/sentry-duration-span-sampling.html)

## 소개

Neil Kakkar가 2023년 10월 4일, PostHog에서 겪은 지연 문제를 추적하며 쓴 짧은 글이다.
매일 아침 약 7~8분 동안 API 지연이 튀었는데, 전체 요청의 0.1% 정도에서만 일어나 재현하기 어려웠다.
그는 Sentry의 프로파일링으로 잡으려 했지만 두 가지 문제가 있었다.

첫째, 모든 요청을 프로파일링하면 비싸다.
대부분 쓸모없는 샘플 10억 개는 돈 낭비다.
Sentry의 샘플링으로 비용은 어느 정도 해결되지만, 둘째 문제가 남는다.
Sentry는 기본적으로 이벤트 개수로 샘플링하므로, 1%로 설정하면 대략 100개 요청 중 1개를 받는다.
대부분의 트랜잭션은 빠르니 여전히 쓸모없고, 10억 개 대신 1,000만 개도 여전히 많은 낭비다.

그가 원한 것은 지속 시간에 따른 샘플링이었다.
2초가 넘게 걸린 요청은 50%, 2초 미만은 0.0001%를 받는 식이다.
문서에는 이것이 가능하다는 말이 없지만, 소스 코드를 뒤져 `before_send_transaction`을 쓰는 방법을 찾았다고 한다.

이 노트는 원문의 코드에 더해, 그가 링크한 PostHog의 실제 변경(PostHog PR #17729, 제목 “chore(decide): More meaningful profiling”, 2023년 10월 3일 병합)에서 확인한 설정을 함께 정리한다.
블로그의 코드만으로는 동작하지 않게 만드는 설정 하나가 PR에만 있기 때문이다.

## 동작 방식

### 샘플링 결정은 두 번 일어난다

Sentry Python SDK에서 트랜잭션의 운명은 두 시점에서 갈린다.

1. 트랜잭션이 시작될 때 `traces_sample_rate`나 `traces_sampler`가 이 트랜잭션을 기록할지 정한다. 여기서 떨어진 트랜잭션은 스팬도, 지속 시간도 남지 않는다.
2. 트랜잭션이 끝나고 전송되기 직전에 `before_send_transaction`이 불린다. 이 함수는 완성된 트랜잭션 이벤트를 받아 이벤트를 돌려주거나 `None`을 돌려주고, `None`이면 트랜잭션은 버려진다.

지속 시간은 트랜잭션이 끝나야 알 수 있으므로, 지속 시간에 따른 결정은 두 번째 시점에서만 할 수 있다.
원문이 강조하는 함정이 여기에 있다.
`traces_sampler` 같은 내장 샘플링은 `before_send_transaction`보다 먼저 적용되므로, 거기서 이미 떨어진 트랜잭션은 두 번째 시점에 도착하지도 않는다.

### 그래서 첫 번째 관문은 모두 통과시켜야 한다

PostHog PR은 이 점을 코드로 보여 준다.
변경 전 `traces_sampler`는 `/decide` 경로에 대해 평소 0.001%, 지연이 튀는 GMT 오전 5시에서 7시 사이에만 0.1%를 돌려줬다.
변경 뒤에는 `/decide`에 대해 1.0, 즉 100%를 돌려주고, 주석에 샘플링은 `before_send_transaction`에서 요청 수 대신 지속 시간으로 한다고 적었다.

블로그는 내장 샘플링 대신 직접 샘플링하라고만 쓰고, 이 부분을 명시하지 않는다.
대상 경로의 트랜잭션 샘플링 비율이 1.0보다 작으면, 느린 요청 대부분은 두 번째 관문에 오기 전에 이미 버려진다.

### 트랜잭션 이벤트에서 쓰는 필드

원문 부록의 샘플 트랜잭션에서 이 방법이 쓰는 필드는 셋이다.

| 필드              | 예시 값                         | 쓰임                       |
| ----------------- | ------------------------------- | -------------------------- |
| `request.url`     | `http://localhost:8000/decide/` | 대상 엔드포인트만 골라낸다 |
| `start_timestamp` | `2023-10-03T09:47:13.542852Z`   | 트랜잭션 시작 시각         |
| `timestamp`       | `2023-10-03T09:47:17.681238Z`   | 트랜잭션 종료 시각         |

같은 이벤트에는 스팬 목록, 트랜잭션 이름(`/decide/[#].*`), 태그, 런타임, SDK 버전(`sentry.python.django` 1.14.0) 같은 정보도 들어 있어, URL 대신 트랜잭션 이름이나 태그로 대상을 고를 수도 있다.

## 설정하기

원문 코드와 PostHog PR의 설정을 합쳐, 그대로 돌아가는 형태로 정리하면 다음과 같다.

```python
from datetime import datetime, timedelta
from random import random

import sentry_sdk
from dateutil import parser

TARGET_PATH = "/decide"

# 느린 요청을 얼마나 남길지 정하는 구간. 위에서부터 차례로 검사한다.
DURATION_RULES = [
    (timedelta(seconds=8), 1.0),  # 8초 이상은 전부 남긴다
    (timedelta(seconds=2), 0.5),  # 2초 초과는 절반을 남긴다
]
BASELINE_RATE = 0.00001  # 나머지 빠른 요청은 0.001%만 남긴다


def _to_datetime(value):
    # 이벤트의 타임스탬프가 문자열로 올 수도, datetime으로 올 수도 있으므로 둘 다 받는다.
    if isinstance(value, datetime):
        return value
    return parser.parse(value)


def traces_sampler(sampling_context: dict) -> float:
    path = sampling_context.get("wsgi_environ", {}).get("PATH_INFO", "")
    if path.startswith(TARGET_PATH):
        # 지속 시간 샘플링은 before_send_transaction에서 한다.
        # 여기서 1.0보다 작으면 느린 요청이 그 전에 버려진다.
        return 1.0
    return 0.01  # 다른 경로는 기존 비율을 유지한다


def before_send_transaction(event, hint):
    url = (event.get("request") or {}).get("url") or ""
    if TARGET_PATH not in url:
        return event

    keep_by_baseline = random() < BASELINE_RATE

    start = event.get("start_timestamp")
    end = event.get("timestamp")
    if not (start and end):
        return event if keep_by_baseline else None

    try:
        duration = _to_datetime(end) - _to_datetime(start)
    except Exception:
        # 파싱에 실패하면 조용히 기본 비율로 떨어진다. 이 분기가 자주 타면 설정이 틀린 것이다.
        return event if keep_by_baseline else None

    for threshold, rate in DURATION_RULES:
        if duration >= threshold:
            return event if random() < rate else None

    return event if keep_by_baseline else None


sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sampler=traces_sampler,
    before_send_transaction=before_send_transaction,
    # 프로파일 샘플링 비율은 트레이스 샘플링 비율에 상대적이다.
    profiles_sample_rate=1.0,
)
```

원문 코드와 다른 점은 셋이다.
대상 경로의 `traces_sampler`가 1.0을 돌려주도록 명시했고, 타임스탬프가 문자열이 아닐 경우를 처리했으며, 구간 규칙을 목록으로 빼서 값을 바꾸기 쉽게 했다.
`traces_sampler`의 `sampling_context`에 어떤 키가 들어오는지는 통합(Django, WSGI, ASGI 등)마다 다르므로, 경로를 꺼내는 부분은 쓰는 통합에 맞게 확인해야 한다.

## 값 정하기

| 값                 | 원문의 값 | 근거                                                      | 바꿔야 할 때                                  |
| ------------------ | --------- | --------------------------------------------------------- | --------------------------------------------- |
| 전부 남기는 기준   | 8초 이상  | 문제의 지연이 이 영역에 있었고, 이런 요청은 드물다        | 기준 이상 요청이 많아 할당량을 넘으면 올린다  |
| 절반 남기는 기준   | 2초 초과  | 느리지만 흔한 영역의 모양을 보기에 충분한 표본            | p99 지연이 바뀌면 그 근처로 옮긴다            |
| 기본 비율          | 0.001%    | 정상 요청의 기준선을 비교용으로 남긴다                    | 기준선 표본이 너무 적어 비교가 안 되면 올린다 |
| 대상 경로 트레이스 | 100%      | 지속 시간을 알려면 모든 트랜잭션이 끝까지 기록되어야 한다 | 기록 오버헤드가 문제가 되면 경로를 더 좁힌다  |

값을 고친 뒤 확인할 것은 Sentry에 도착하는 대상 경로 트랜잭션의 수와 지속 시간 분포다.
기준 이상 구간이 거의 비어 있다면 첫 번째 관문에서 이미 떨어지고 있거나 파싱이 실패하고 있다는 뜻이다.

## 트레이드오프

### 전송 비용은 줄지만 기록 비용은 그대로다

이 방법이 줄이는 것은 Sentry로 보내는 이벤트의 수, 즉 할당량과 요금이다.
대상 경로의 모든 트랜잭션은 여전히 끝까지 기록된다.
스팬을 만들고, 타임스탬프를 찍고, 이벤트를 조립하는 비용은 전송 여부와 상관없이 매 요청마다 든다.

프로파일링까지 켜면 이 차이는 더 커진다.
프로파일은 요청이 도는 동안 수집되므로, 나중에 버릴 트랜잭션에도 수집 비용이 든다.
원문 제목은 프로파일링이지만 코드가 결정하는 것은 트랜잭션의 전송이다.
프로파일이 버려진 트랜잭션과 함께 버려지는지, 수집 오버헤드가 얼마인지는 SDK 버전마다 확인해야 한다.

그래서 이 방법은 요청량이 많은 경로 전체보다, 문제를 추적하는 특정 경로에 한정해 쓰는 편이 맞다.
PostHog도 `/decide` 하나에만 적용했다.

### 느린 요청만 보면 비교할 기준을 잃는다

느린 요청만 모으면 무엇이 느린지는 보이지만, 그것이 평소와 무엇이 다른지는 보이지 않는다.
원문이 빠른 요청에도 0.001%의 기본 비율을 남긴 이유가 여기에 있다.
정상 요청의 스팬 구성과 느린 요청의 스팬 구성을 나란히 봐야, 어느 스팬이 늘어났는지 알 수 있다.

기본 비율을 너무 낮추면 할당량은 아끼지만 비교 표본이 사라진다.
반대로 올리면 원래 문제였던 쓸모없는 샘플이 다시 늘어난다.
기준선 표본은 분석에 필요한 최소한으로 두고, 기간을 정해 모았다가 끄는 방식이 현실적이다.

### 샘플링 편향이 대시보드의 숫자를 바꾼다

지속 시간에 따라 다른 비율로 남기면, Sentry에 도착한 트랜잭션의 지속 시간 분포는 실제와 크게 다르다.
느린 요청의 비중이 실제보다 수만 배 부풀려진다.
그 상태에서 Sentry의 평균 지연이나 백분위 지표를 보면 실제 서비스보다 훨씬 느려 보인다.

그래서 이 설정을 켠 경로의 성능 대시보드는 지표로 쓰면 안 된다.
실제 지연 분포는 별도의 메트릭 시스템에서 보고, Sentry는 느린 요청의 내부를 들여다보는 용도로만 써야 한다.
원문의 PostHog는 이미 Prometheus 미들웨어를 쓰고 있었으므로, 지표와 추적의 역할이 나뉘어 있었다.

## 함정

### 블로그 코드만 옮기면 느린 요청이 도착하지 않는다

가장 흔할 실패는 `before_send_transaction`만 추가하고 트레이스 샘플링 비율을 그대로 두는 것이다.
예를 들어 전역 `traces_sample_rate`가 0.01이라면, 느린 요청의 99%는 두 번째 관문에 도착하기 전에 버려진다.
함수는 정상적으로 돌지만, 볼 수 있는 느린 요청은 원래의 1%에 그친다.

### 예외가 조용히 기본 비율로 떨어진다

원문과 PR의 코드는 모두 파싱 중 예외가 나면 기본 비율로 떨어진다.
타임스탬프 형식이 예상과 다르거나 필드 이름이 SDK 버전에서 바뀌면, 코드는 오류 없이 거의 모든 트랜잭션을 버린다.
배포 뒤 대상 경로에서 도착하는 트랜잭션 수가 기대보다 훨씬 적다면 이 분기를 먼저 의심한다.

### URL 부분 문자열 검사는 넓게 걸린다

원문은 URL에 `decide`가 들어 있는지만 본다.
`/api/decide-something`이나 쿼리 문자열에 그 단어가 들어간 요청도 걸린다.
트랜잭션 이름이나 경로의 접두사로 비교하는 편이 안전하다.

### 기록 비용이 지연을 만들 수 있다

대상 경로의 모든 트랜잭션을 기록하는 오버헤드가 작다고 가정하지 말아야 한다.
0.1%의 요청에서만 나타나는 지연을 쫓는데, 그 추적 자체가 모든 요청에 일정한 비용을 더한다.
켜기 전후의 p50 지연을 비교해 추적의 영향을 확인한다.

## 확인하기

1. 로컬에서 대상 경로가 `slow` 쿼리 파라미터를 받으면 `time.sleep(3)`을 하도록 테스트용 분기를 넣고, `before_send_transaction` 안에서 계산한 `duration`과 반환 여부를 로그로 남긴다.
2. 빠른 요청 여러 개와 느린 요청 여러 개를 보내, 느린 요청의 절반 정도와 빠른 요청의 거의 0개가 반환되는지 본다.
3. 예외 분기에 로그를 넣고, 한 번도 타지 않는지 확인한다.
4. `traces_sampler`의 대상 경로 비율을 일부러 0.01로 바꿔, 느린 요청이 함수에 거의 도착하지 않는 것을 확인한다. 이것이 첫 번째 관문의 효과다.

```bash
# 빠른 요청과 느린 요청을 섞어 보낸다(로컬 개발 서버 기준)
for i in $(seq 1 50); do curl -s -o /dev/null -X POST http://localhost:8000/decide/; done
for i in $(seq 1 10); do curl -s -o /dev/null -X POST "http://localhost:8000/decide/?slow=1"; done
```

## 체크리스트

- 대상 경로의 트레이스 샘플링 비율이 1.0인가?
- `before_send_transaction`이 대상 경로만 정확히 골라내는가?
- 타임스탬프가 문자열과 `datetime` 두 형태 모두에서 처리되는가?
- 예외 분기가 타는지 로그로 확인할 수 있는가?
- 빠른 요청의 기준선 표본을 비교에 쓸 만큼 남기는가?
- 이 경로의 Sentry 성능 지표를 실제 지연 지표로 쓰지 않는다는 것을 팀이 아는가?
- 추적을 켠 뒤 대상 경로의 p50 지연이 달라지지 않았는가?

## 기억할 원칙

### 결정에 필요한 정보가 생기는 시점에 결정한다

이 글의 요점은 샘플링 결정의 시점이다.
지속 시간은 요청이 끝나야 알 수 있으므로, 지속 시간으로 결정하려면 끝날 때까지 결정을 미뤄야 한다.
그러려면 앞 단계의 결정은 모두 통과로 열어 두어야 한다.

이것은 샘플링뿐 아니라 꼬리 기반 샘플링(tail-based sampling) 전반의 원리다.
머리에서 결정하면 싸지만 결과를 모르고, 꼬리에서 결정하면 결과를 알지만 모든 것을 끝까지 들고 있어야 한다.
어느 쪽을 쓰든, 결정에 쓰는 정보가 그 시점에 존재하는지 먼저 확인해야 한다.
