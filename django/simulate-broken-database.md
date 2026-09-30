# Django 테스트에서 데이터베이스 연결이 끊긴 상황 흉내 내기

원문: [How to simulate a broken database connection for testing in Django | Neil Kakkar](https://neilkakkar.com/test-database-connection-django.html)

Lobste.rs 토론: <https://lobste.rs/s/t0hd2c/how_simulate_broken_database_connection> (14점, 4개 댓글)

## 소개

Neil Kakkar가 2023년 1월 15일, PostHog에서 데이터베이스가 내려가도 500 오류를 돌려주지 않는 방어 코드를 쓰다가 정리한 짧은 글이다.
문제는 원시 커서(raw cursor)만이 아니라 데이터베이스에 닿는 모든 모델 호출이 실패해야 한다는 것이었다.
`Model.objects.filter()`, `Model.objects.all()`, `connection.cursor()` 어디서 부르든 연산이 실패해야 한다.

그는 Google과 ChatGPT 모두 실망스러운 결과를 내서 Django 소스 코드를 뒤졌다고 쓴다.
미래의 자기와 미래의 ChatGPT가 올바른 답을 찾을 수 있게 기록해 둔다는 것이 글을 쓴 이유다.

글은 세 가지 방법을 비교하고, 셋째인 데이터베이스 실행 래퍼(execute wrapper)를 가장 좋은 방법으로 권한다.
이 방법은 Django 문서의 데이터베이스 계측(database instrumentation) 기능을 테스트에 쓰는 것이고, 동료 Karl이 알려 줬다고 한다.

## 동작 방식

### 세 방법이 끼어드는 층

| 방법           | 끼어드는 곳                                 | 막는 범위                | 원문의 평가                          |
| -------------- | ------------------------------------------- | ------------------------ | ------------------------------------ |
| 원시 커서 패치 | `django.db.connection.cursor`               | 그 이름을 쓰는 코드만    | 모든 곳에서 통하지 않아 깨지기 쉽다  |
| 쿼리 내부 패치 | `django.db.models.sql.compiler.SQLCompiler` | ORM 모델 쿼리            | 내부 구현에 기대 업그레이드에 약하다 |
| 실행 래퍼      | `connection.execute_wrapper()`              | 그 연결의 모든 쿼리 실행 | 가장 높은 추상 수준이라 덜 깨진다    |

원시 커서 패치는 `connection.cursor`를 직접 부르는 코드에서만 통한다.
ORM은 모듈 속성 `django.db.connection`을 거치지 않고 자기 연결을 쓰므로, 모델 쿼리는 그대로 성공한다.
그렇다고 모든 모델을 하나씩 패치하는 것은 현실적이지 않다.

쿼리 내부 패치는 모델이 데이터베이스에 접근할 때마다 `SQLCompiler`가 만들어진다는 점을 이용한다.
그래서 모든 모델 쿼리가 실패하지만, Django 내부 클래스에 기대므로 업그레이드 한 번에 테스트가 깨질 수 있다.

실행 래퍼는 Django가 공식으로 제공하는 확장 지점이다.
`connection.execute_wrapper()`는 그 연결에서 실행되는 모든 쿼리를 감싸는 컨텍스트 관리자이고, 래퍼는 `execute`와 인자를 받아 원래 쿼리를 실행하거나 대신 예외를 던질 수 있다.
문서는 주로 계측 용도를 권하지만, 무엇이든 할 수 있고 테스트에 이상적이라고 저자는 쓴다.

### 실행 래퍼가 부르는 순서

래퍼가 설치된 동안 모델 쿼리 하나는 이렇게 지나간다.

1. `Model.objects.filter(...)`가 평가되면 ORM이 SQL을 만든다.
2. 연결의 커서가 그 SQL을 실행하려 한다.
3. 실행 직전에 등록된 래퍼들이 차례로 불린다.
4. 래퍼가 `execute(*args, **kwargs)`를 부르지 않고 `OperationalError`를 던지면, 쿼리는 데이터베이스에 가지 않고 호출한 쪽으로 예외가 올라간다.

## 구현하기

### 연결 하나를 끊긴 것처럼 만들기

```python
import pytest
from django.db import connection
from django.db.utils import OperationalError


class QueryTimeoutWrapper:
    def __call__(self, execute, sql, params, many, context):
        # 실제 쿼리를 실행하지 않고 연결 장애를 흉내 낸다.
        raise OperationalError("Connection timed out")
        # 쿼리를 통과시키려면 대신 이렇게 한다.
        # return execute(sql, params, many, context)


@pytest.mark.django_db
def test_flags_endpoint_survives_database_outage(client):
    with connection.execute_wrapper(QueryTimeoutWrapper()):
        response = client.post("/decide/", {"distinct_id": "user-1"})

    # 방어 코드가 캐시나 기본값으로 응답해야 한다.
    assert response.status_code == 200
```

예제는 pytest-django의 `client` 픽스처를 쓴다.
원문은 래퍼 시그니처를 `(self, execute, *args, **kwargs)`로 쓴다.
Django 문서가 정한 인자는 `execute, sql, params, many, context`이므로 이름을 명시하면 읽기 쉽고, 특정 쿼리만 골라 막을 수도 있다.

### 특정 쿼리만 실패시키기

```python
class FailMatchingQueries:
    def __init__(self, needle):
        self.needle = needle
        self.blocked = 0

    def __call__(self, execute, sql, params, many, context):
        if self.needle in sql:
            self.blocked += 1
            raise OperationalError("Connection timed out")
        return execute(sql, params, many, context)


@pytest.mark.django_db
def test_person_lookup_falls_back_to_cache(client):
    blocker = FailMatchingQueries("posthog_persondistinctid")
    with connection.execute_wrapper(blocker):
        response = client.post("/decide/", {"distinct_id": "user-1"})

    assert response.status_code == 200
    # 막힌 쿼리가 실제로 시도되었는지도 확인한다. 0이면 테스트가 아무것도 검증하지 않은 것이다.
    assert blocker.blocked > 0
```

### 여러 데이터베이스를 쓰는 경우

`execute_wrapper()`는 호출한 연결 하나에만 걸린다.
읽기 복제본이나 별도 데이터베이스로 라우팅되는 쿼리는 그대로 성공한다.
모든 연결을 막으려면 연결마다 래퍼를 건다.

```python
from contextlib import ExitStack

from django.db import connections


def all_databases_down():
    stack = ExitStack()
    for conn in connections.all():
        stack.enter_context(conn.execute_wrapper(QueryTimeoutWrapper()))
    return stack


@pytest.mark.django_db
def test_everything_down(client):
    with all_databases_down():
        response = client.post("/decide/", {"distinct_id": "user-1"})
    assert response.status_code == 200
```

저자의 PostHog 코드는 기능 플래그 판정 쿼리가 별도 데이터베이스(`DATABASE_FOR_FLAG_MATCHING`)로 가도록 구성되어 있었다.
이런 구성에서는 어느 연결에 래퍼를 걸었는지가 테스트 결과를 바꾼다.

## 트레이드오프

### 흉내 낸 장애는 실제 장애의 한 모양일 뿐이다

실행 래퍼는 쿼리 실행 시점에 예외를 던진다.
실제 데이터베이스 장애는 여러 모양으로 온다.
연결을 여는 단계에서 실패하기도 하고, 쿼리가 몇 초 동안 매달렸다가 시간 초과로 끝나기도 하고, 연결 풀이 고갈되기도 하고, 트랜잭션 도중에 연결이 끊기기도 한다.

즉시 던지는 `OperationalError`는 그중 가장 친절한 경우다.
시간 초과를 흉내 내지 않으면, 방어 코드가 예외는 잘 잡지만 요청이 몇 초씩 매달리는 문제는 드러나지 않는다.
래퍼 안에서 `time.sleep()`을 넣고 예외를 던지면 지연까지 흉내 낼 수 있지만, 그만큼 테스트가 느려진다.

### 모킹이 버그를 가린다는 반론

Lobste.rs에서 sirupsen은 Shopify에서 모든 외부 호출에 대해 이런 작업을 대대적으로 했던 경험을 전했다.[^sirupsen]
모킹이 드러내는 버그만큼 가리는 버그도 많다는 직감이 있었고, 그래서 애플리케이션과 서비스 사이에 앉는 Toxiproxy의 첫 버전을 만들었다고 한다.
그 도구로는 특정 서비스를 내린 상태에서 코드를 실행하는 테스트를 쓸 수 있고, 모킹으로는 발견하지 못한 Rails의 연결 처리 로직 버그를 여럿 찾았으며 일부는 매우 심각했다고 적었다.
이런 일을 자주 한다면 몽키 패치 대신 그 수준까지 가라는 권고다.

저자는 흥미롭다면서도 PostHog에서는 아직 그 트레이드오프가 값어치가 없다고 답했다.[^neilkakkar]
실행 래퍼는 Django 안에서 끝나는 가벼운 방법이고, 프록시는 실제 네트워크 계층의 장애를 흉내 내지만 테스트 환경에 구성 요소를 하나 더 둔다.
연결 처리 로직 자체를 믿지 못한다면 프록시가, 애플리케이션의 예외 처리와 캐시 경로를 확인하는 것이 목적이라면 실행 래퍼가 맞다.

### 같은 방법을 담은 라이브러리

Tenzer는 전 동료가 만든 `django-sans-db`를 소개했다.[^Tenzer]
저자가 들여다보니 글의 셋째 방법과 정확히 같은 코드를 쓰고 있었다고 한다.[^neilkakkar-sans-db]
같은 기법을 여러 사람이 따로 찾아냈다는 것은 이것이 Django에서 사실상 표준적인 방법이라는 뜻이기도 하다.

## 함정

### 테스트 케이스의 트랜잭션 쿼리도 막힐 수 있다

Django의 `TestCase`는 각 테스트를 트랜잭션으로 감싸고, 코드 안의 `atomic()` 블록은 세이브포인트를 만든다.
세이브포인트 생성과 해제도 연결의 커서로 실행되므로, 래퍼가 모든 SQL을 막으면 비즈니스 쿼리보다 먼저 세이브포인트 SQL이 실패할 수 있다.
그러면 테스트는 의도한 경로가 아니라 트랜잭션 오류 경로를 검증하게 된다.
앞의 `FailMatchingQueries`처럼 막을 쿼리를 테이블 이름 등으로 좁히면 이 문제를 피할 수 있다.

### 래퍼가 걸린 연결과 쿼리가 가는 연결이 다를 수 있다

데이터베이스 라우터가 쿼리를 다른 별칭으로 보내면, `django.db.connection`에 건 래퍼는 아무것도 막지 않는다.
테스트는 통과하지만 아무 장애도 흉내 내지 않은 것이다.
막힌 쿼리 수를 세어 0이 아닌지 확인하는 것이 이런 거짓 통과를 잡는 가장 싼 방법이다.

### 캐시가 먼저 응답하면 방어 코드를 시험하지 못한다

저자는 이 방법이 캐시가 제대로 도는지 확인하는 데도 좋다고 쓴다.
함수가 캐시 대신 데이터베이스를 쓰면 곧바로 `OperationalError`가 나기 때문이다.
반대로 말하면, 테스트 전에 캐시를 채워 두지 않았거나 이미 채워진 캐시가 남아 있으면 테스트가 보는 경로가 달라진다.
캐시 상태를 테스트마다 명시적으로 초기화하거나 채워야 한다.

### 원시 커서 패치는 이름 바인딩 때문에 조용히 실패한다

첫째 방법은 `django.db.connection`을 패치하지만, 코드가 `from django.db import connection`으로 이미 가져온 이름이나 `connections["default"]`를 쓰면 패치가 닿지 않는다.
예외가 나지 않으니 테스트는 성공하고, 사용자는 방어 코드가 동작한다고 믿는다.
원문이 이 방법을 깨지기 쉽다고 한 이유가 이것이다.

## 확인하기

1. 데이터베이스를 쓰는 뷰 하나에 대해, 래퍼 없이 테스트가 통과하는지 본다.
2. 모든 쿼리를 막는 래퍼를 걸고, 방어 코드가 없을 때 500이 나는지 확인한다. 이것이 테스트가 실제로 장애를 흉내 낸다는 증거다.
3. 방어 코드를 넣고 같은 테스트가 200을 돌려주는지 본다.
4. 막힌 쿼리 수를 세어 0보다 큰지 확인한다.
5. 여러 데이터베이스를 쓰면, 라우팅되는 연결에 래퍼를 걸었을 때와 기본 연결에만 걸었을 때 결과가 다른지 비교한다.

```bash
# 테스트 하나만 돌려 흉내 낸 장애의 효과를 본다
python manage.py test app.tests.test_outage -v 2
```

## 체크리스트

- 래퍼를 쿼리가 실제로 가는 연결 모두에 걸었는가?
- 막힌 쿼리 수가 0이 아님을 테스트가 확인하는가?
- 세이브포인트 같은 트랜잭션 SQL까지 막아 테스트가 엉뚱한 경로를 보고 있지는 않은가?
- 캐시 상태를 테스트마다 명시적으로 정했는가?
- 즉시 실패만이 아니라 지연 뒤 실패도 흉내 내야 하는 코드인가?
- 연결 처리 로직 자체를 검증해야 한다면 Toxiproxy 같은 네트워크 계층 도구를 검토했는가?

## 기억할 원칙

### 장애는 공식 확장 지점에서 흉내 낸다

세 방법의 차이는 끼어드는 층의 안정성이다.
모듈 속성과 내부 클래스는 언제든 바뀌지만, `execute_wrapper()`는 Django가 약속한 공개 API다.
테스트용 장애 주입도 제품 코드처럼 공개된 확장 지점에 기대야 업그레이드를 견딘다.

그리고 장애를 흉내 낸 테스트는 장애가 실제로 흉내 내졌는지부터 확인해야 한다.
아무것도 막지 못한 장애 테스트는 통과하는 테스트 가운데 가장 위험한 종류다.

---

[^sirupsen]: <https://lobste.rs/s/t0hd2c/how_simulate_broken_database_connection#c_fs5hue>

[^neilkakkar]: <https://lobste.rs/s/t0hd2c/how_simulate_broken_database_connection#c_xz7rhk>

[^Tenzer]: <https://lobste.rs/s/t0hd2c/how_simulate_broken_database_connection#c_z46fea>

[^neilkakkar-sans-db]: <https://lobste.rs/s/t0hd2c/how_simulate_broken_database_connection#c_n874uz>
