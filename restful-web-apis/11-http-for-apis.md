# 11장 API를 위한 HTTP: 표준 기능을 제대로 쓰기

《RESTful Web APIs》(Leonard Richardson, Mike Amundsen, O'Reilly 2013) 11장 정리.

## 개요

11장은 API 구현에서 HTTP를 쓸 때의 모범 사례를 다루고, 여기에 더해 HTTP의 확장들 — 저자의 표현으로는 “the forthcoming HTTP 2.0 protocol”을 포함한 — 을 논의한다.
이 정리는 저자의 공식 장별 설명과 해당 장이 다루는 공개 표준을 근거로 하며, 책 본문을 옮긴 것이 아니다.

이 장의 위치는 분명하다.
1장부터 10장까지가 “표현을 어떻게 설계하는가”를 다뤘다면, 11장은 그 표현을 실어 나르는 프로토콜 자체를 다시 본다.
많은 API가 HTTP를 단순한 전송 파이프로만 쓰고 조건부 요청, 캐싱, 인증, 콘텐츠 협상 같은 이미 표준화된 기능을 직접 재발명한다는 것이 이 장의 문제의식이다.

한 가지 시점을 먼저 정리해 둘 필요가 있다.
책이 나온 2013년의 HTTP/1.1 규범 문서는 RFC 2616(1999)이었고, 그 이듬해인 2014년에 RFC 7230~7235가 이를 대체했으며, 다시 2022년 6월에 RFC 9110(HTTP Semantics), RFC 9111(HTTP Caching), RFC 9112(HTTP/1.1)가 그것을 대체했다.
따라서 아래에서는 개념은 이 장의 주제를 따르되, 조문 참조는 현행 RFC 9110/9111을 기준으로 적는다.

## 조건부 요청: 검증자(validator)로 대역폭과 충돌을 함께 줄인다

조건부 요청은 클라이언트가 이미 가진 표현이 아직 유효한지를 서버에 묻는 방식이다.
서버는 표현마다 검증자(validator)를 붙여 응답하고, 클라이언트는 다음 요청에서 그 값을 되돌려 보낸다.

검증자는 두 가지다.
`ETag`는 표현의 불투명한 식별 문자열이고, `Last-Modified`는 표현의 마지막 변경 시각이다.
RFC 9110은 `ETag`를 강한 검증자와 약한 검증자로 나누며, 약한 검증자는 `W/` 접두사를 붙인다.

요청 쪽 조건부 헤더는 RFC 9110 13.1절에 다섯 개가 정의돼 있다.

```text
If-Match             (13.1.1)  강한 검증자 일치를 요구 — 주로 갱신 충돌 방지
If-None-Match        (13.1.2)  검증자 불일치를 요구 — 주로 캐시 재검증
If-Modified-Since    (13.1.3)  지정 시각 이후 변경된 경우에만
If-Unmodified-Since  (13.1.4)  지정 시각 이후 변경되지 않은 경우에만
If-Range             (13.1.5)  범위 요청의 검증자
```

읽기와 쓰기에서 쓰임이 갈린다.
읽기에서는 `If-None-Match`(또는 `If-Modified-Since`)를 보내고, 표현이 그대로면 서버는 본문 없이 `304 Not Modified`를 돌려준다.
쓰기에서는 `If-Match`(또는 `If-Unmodified-Since`)를 보내고, 그사이 다른 클라이언트가 리소스를 바꿔 검증자가 어긋났으면 서버는 `412 Precondition Failed`를 돌려준다.
후자가 이른바 낙관적 동시성 제어(optimistic concurrency control)이며, API에서 “덮어쓰기 사고”를 막는 표준 수단이다.

```http
GET /orders/42 HTTP/1.1
Host: api.example.com

HTTP/1.1 200 OK
ETag: "a1b2c3"
Last-Modified: Mon, 17 Aug 2026 09:00:00 GMT
Content-Type: application/json

GET /orders/42 HTTP/1.1
Host: api.example.com
If-None-Match: "a1b2c3"

HTTP/1.1 304 Not Modified
ETag: "a1b2c3"
```

```http
PUT /orders/42 HTTP/1.1
Host: api.example.com
If-Match: "a1b2c3"
Content-Type: application/json

HTTP/1.1 412 Precondition Failed
```

RFC 9110은 조건부 헤더의 평가 순서도 규정한다.
`If-Match`가 있으면 그것을 먼저 보고, 없을 때만 `If-Unmodified-Since`를 본다.
`If-None-Match`가 있으면 그것을 먼저 보고, 없을 때만 `If-Modified-Since`를 본다.
즉 엔티티 태그가 날짜보다 우선한다.

## 캐싱: Cache-Control이 정책의 언어다

캐싱은 REST의 여섯 제약 중 하나가 프로토콜 수준에서 구현된 것이다.
현행 규범은 RFC 9111이며, 캐시 정책은 `Cache-Control` 헤더의 지시어(directive)로 표현한다.

요청 지시어와 응답 지시어가 나뉜다.

| 구분 | 지시어             | 뜻                                               |
| ---- | ------------------ | ------------------------------------------------ |
| 요청 | `max-age`          | 이보다 오래된 응답은 받지 않겠다                 |
| 요청 | `max-stale`        | 지정 시간만큼 오래된 응답은 감수하겠다           |
| 요청 | `min-fresh`        | 최소 이만큼은 신선한 응답을 달라                 |
| 요청 | `no-cache`         | 저장본을 쓰기 전에 원 서버에서 검증하라          |
| 요청 | `no-store`         | 이 요청/응답을 저장하지 말라                     |
| 요청 | `no-transform`     | 중간자가 표현을 변형하지 말라                    |
| 요청 | `only-if-cached`   | 캐시에 있으면 주고 없으면 네트워크로 나가지 말라 |
| 응답 | `max-age`          | 이 응답의 신선도 수명(초)                        |
| 응답 | `s-maxage`         | 공유 캐시에 한한 신선도 수명                     |
| 응답 | `public`           | 공유 캐시도 저장 가능                            |
| 응답 | `private`          | 개인 캐시만 저장 가능                            |
| 응답 | `no-cache`         | 저장은 하되 쓸 때마다 재검증하라                 |
| 응답 | `no-store`         | 저장하지 말라                                    |
| 응답 | `must-revalidate`  | 신선도가 만료되면 반드시 재검증하라              |
| 응답 | `proxy-revalidate` | 공유 캐시에 한해 만료 시 반드시 재검증           |
| 응답 | `must-understand`  | 상태 코드 의미를 이해하는 캐시만 저장하라        |
| 응답 | `no-transform`     | 중간자가 표현을 변형하지 말라                    |

API 설계에서 중요한 조합은 두 가지다.
공개 컬렉션처럼 자주 읽히고 드물게 바뀌는 리소스에는 `public, max-age=...`를, 사용자별 데이터에는 `private`을 붙인다.
인증이 걸린 응답을 공유 캐시에 흘리지 않으려면 `private` 또는 `no-store`가 필요하다.

`Vary` 헤더도 함께 봐야 한다.
`Accept`나 `Accept-Language`로 콘텐츠 협상을 하는 API가 `Vary`를 붙이지 않으면, 캐시는 한 표현을 다른 협상 조건의 요청에 잘못 재사용한다.

## 인증: 프레임워크는 이미 표준화돼 있다

HTTP 인증은 RFC 9110 11절에 프레임워크로 정의돼 있다.
서버가 `401 Unauthorized`와 함께 `WWW-Authenticate`로 챌린지를 보내면, 클라이언트가 `Authorization`으로 자격 증명을 제시하는 구조다.
프록시 경로에는 `407 Proxy Authentication Required`, `Proxy-Authenticate`, `Proxy-Authorization`이 대응한다.

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="api", error="invalid_token"
```

핵심은 인증 방식(scheme)이 IANA 레지스트리에 등록된 확장 지점이라는 것이다.
Basic(RFC 7617), Digest(RFC 7616), Bearer(RFC 6750)가 모두 이 프레임워크 위에 얹힌다.
API가 자체 헤더로 토큰을 실어 나르는 관행은 이 확장 지점을 무시하고 표준 클라이언트·중간자의 이해를 포기하는 선택이다.

인증과 인가의 상태 코드 구분도 여기서 정리된다.
`401`은 “자격 증명이 없거나 유효하지 않다”이고, `403 Forbidden`은 “자격 증명은 이해했으나 권한이 없다”이다.

## 압축: 콘텐츠 코딩은 협상 대상이다

압축은 콘텐츠 코딩(content coding)으로 다룬다.
클라이언트는 `Accept-Encoding`으로 받아들일 코딩을 알리고, 서버는 실제 적용한 코딩을 `Content-Encoding`으로 알린다.

```http
GET /orders HTTP/1.1
Accept-Encoding: gzip, br

HTTP/1.1 200 OK
Content-Encoding: gzip
Vary: Accept-Encoding
```

`gzip`, `deflate`, `compress`가 RFC 9110에 정의돼 있고, Brotli(`br`, RFC 7932)와 Zstandard(`zstd`, RFC 8878)가 뒤에 추가됐다.
JSON은 텍스트라 압축률이 높아, 압축 협상은 JSON API에서 비용 대비 효과가 큰 편이다.
`Vary: Accept-Encoding`을 빠뜨리면 캐시가 압축본을 압축을 못 받는 클라이언트에게 넘길 수 있다.

## PATCH: 부분 수정을 위한 별도 메서드

PATCH는 RFC 5789(2010)에 정의됐다.
RFC 5789의 정의를 그대로 옮기면, PUT의 본문은 서버에 저장된 리소스의 수정된 버전 전체인 반면, PATCH의 본문은 서버의 현재 리소스를 어떻게 고쳐 새 버전을 만들지 기술하는 명령 집합이다.

PATCH는 안전하지도 멱등하지도 않다.
다만 요청을 멱등하게 되도록 구성할 수는 있으며, RFC 5789는 그렇게 하는 것이 동시 PATCH 충돌의 나쁜 결과를 막는 데 도움이 된다고 적는다.
그래서 PATCH에는 `If-Match`를 함께 쓰는 것이 사실상 필수에 가깝다.

패치 문서는 미디어 타입으로 식별된다.
서버는 `Accept-Patch` 응답 헤더로 자신이 받는 패치 형식을 알린다.
널리 쓰이는 형식은 두 가지다.

```text
application/json-patch+json    JSON Patch (RFC 6902) — op/path/value 연산 배열
application/merge-patch+json   JSON Merge Patch (RFC 7396) — null이 삭제를 뜻하는 부분 문서
```

```http
PATCH /orders/42 HTTP/1.1
Content-Type: application/json-patch+json
If-Match: "a1b2c3"

[
  { "op": "replace", "path": "/status", "value": "shipped" },
  { "op": "remove", "path": "/coupon" }
]
```

## Link 헤더: 표현 밖에서 하는 하이퍼미디어

`Link` 헤더는 표현 형식이 하이퍼미디어를 지원하지 않아도 링크를 실어 나르게 해 준다.
JSON처럼 링크 개념이 없는 형식을 쓰는 API에게는 이것이 가장 손쉬운 하이퍼미디어 진입로다.

규범은 RFC 8288 Web Linking(2017)이며, 책이 나올 당시의 RFC 5988을 대체했다.
문법은 다음과 같다.

```text
Link       = #link-value
link-value = "<" URI-Reference ">" *( OWS ";" OWS link-param )
```

즉 대상 URI를 꺾쇠로 감싸고, 세미콜론으로 구분된 파라미터를 붙인다.
`rel`이 링크 관계 타입을 지정하고, 이 값은 IANA 링크 관계 레지스트리에 등록된 토큰이거나 확장 URI다.
`type`, `title`, `hreflang`, `anchor` 같은 파라미터가 함께 정의돼 있다.

```http
HTTP/1.1 200 OK
Content-Type: application/json
Link: <https://api.example.com/orders?page=3>; rel="next",
      <https://api.example.com/orders?page=1>; rel="first",
      <https://api.example.com/docs/orders>; rel="profile"
```

`Link` 헤더는 이 책의 다른 주제와도 직접 이어진다.
8장의 프로파일은 `profile` 링크 관계로 표현에 의미론을 붙이고, JSON-LD는 `http://www.w3.org/ns/json-ld#context` 관계의 `Link` 헤더로 일반 JSON 문서에 컨텍스트를 외부에서 붙일 수 있게 한다.

## HTTP/2: 2013년의 “forthcoming”이 지금은 표준이다

저자가 이 장을 쓸 때 HTTP 2.0은 아직 표준이 아니었다.
저자의 표현 그대로 “the forthcoming HTTP 2.0 protocol”이며, 당시에는 SPDY를 바탕으로 IETF HTTPbis 워킹그룹이 초안을 다듬는 단계였다.

지금의 상태는 이렇다.
HTTP/2는 2015년 5월 RFC 7540으로 표준화됐고, 2022년 6월 RFC 9113이 RFC 7540과 RFC 8740을 대체해 현행 규범이 됐다.
헤더 압축 알고리즘 HPACK은 RFC 7541에 별도로 정의돼 있다.
그 뒤 QUIC 위에서 도는 HTTP/3가 2022년 6월 RFC 9114로 표준화됐다(헤더 압축은 QPACK, RFC 9204).

중요한 점은 HTTP/2가 바꾼 것이 무엇이고 바꾸지 않은 것이 무엇인가이다.
바뀐 것은 전송 계층이다.
텍스트 기반 요청/응답이 이진 프레이밍으로 바뀌었고, 한 TCP 연결 위에서 여러 요청을 동시에 다중화(multiplexing)해 HTTP/1.1의 head-of-line blocking을 완화했으며, 헤더를 HPACK으로 압축한다.

바뀌지 않은 것은 의미론이다.
메서드, 상태 코드, 헤더 필드, 조건부 요청, 캐싱 규칙은 그대로다.
그래서 RFC 9110이 버전과 무관한 “HTTP Semantics”로 따로 떨어져 나왔고, RFC 9112/9113/9114가 각각 1.1/2/3의 전송 방식만 규정한다.

API 설계자에게 이 분리가 뜻하는 바는 분명하다.
HTTP/2로 옮긴다고 해서 API 설계가 달라지지 않는다.
다만 HTTP/1.1 시절의 우회책 중 일부 — 요청 수를 줄이려고 응답을 과도하게 뭉치거나 도메인을 쪼개던 관행 — 는 근거를 잃는다.
반대로 조건부 요청과 캐싱처럼 의미론 층위의 최적화는 버전이 올라가도 그대로 유효하다.

한 가지 덧붙일 것은 서버 푸시다.
RFC 7540의 서버 푸시는 기대만큼 쓰이지 않았고 주요 브라우저가 지원을 걷어냈으며, RFC 9113은 이 기능을 여전히 규정하되 실무에서는 사실상 사장된 상태다.

## 오류 표현: 상태 코드만으로는 부족하다

11장의 모범 사례와 자연스럽게 이어지는 확장이 오류 표현의 표준화다.
상태 코드는 오류의 종류를 알려 주지만 무엇이 왜 잘못됐는지는 알려 주지 않는다.

RFC 9457 Problem Details for HTTP APIs(2023, RFC 7807을 대체)가 이 빈틈을 메운다.
`application/problem+json` 미디어 타입으로 `type`, `title`, `status`, `detail`, `instance` 필드를 담는다.

```http
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json

{
  "type": "https://example.com/probs/out-of-credit",
  "title": "You do not have enough credit.",
  "status": 403,
  "detail": "Your current balance is 30, but that costs 50.",
  "instance": "/account/12345/msgs/abc"
}
```

이 형식은 이 책의 논지와 정확히 맞물린다.
API마다 오류 JSON을 새로 발명하지 말고, 이미 정의된 미디어 타입을 재사용하라는 것이다.

## 핵심 정리

11장의 논지는 하나로 요약된다.
HTTP는 이미 API가 필요로 하는 대부분의 기능을 표준으로 갖고 있으며, API 설계자의 일은 그것을 새로 발명하는 것이 아니라 제대로 쓰는 것이다.

조건부 요청은 두 방향으로 쓴다.
읽기에서는 `If-None-Match`/`If-Modified-Since`로 `304`를 유도해 대역폭을 아끼고, 쓰기에서는 `If-Match`/`If-Unmodified-Since`로 `412`를 유도해 갱신 충돌을 막는다.
검증자는 `ETag`가 `Last-Modified`보다 우선한다.

캐싱은 `Cache-Control` 지시어로 정책을 명시하는 일이다.
`public`/`private`으로 공유 가능성을, `max-age`/`s-maxage`로 신선도를, `no-cache`/`must-revalidate`로 재검증 시점을 정한다.
콘텐츠 협상을 한다면 `Vary`를 반드시 붙인다.

인증은 `WWW-Authenticate`/`Authorization` 프레임워크 위에 등록된 스킴을 얹는 것이지, 자체 헤더를 만드는 일이 아니다.
`401`과 `403`의 구분은 자격 증명의 유효성과 권한의 차이다.

압축은 `Accept-Encoding`/`Content-Encoding`의 협상이며, JSON API에서 효과가 크다.

PATCH는 부분 수정을 위한 별도 메서드이고, 본문은 리소스가 아니라 변경 명령이다.
안전하지도 멱등하지도 않으므로 `If-Match`와 함께 쓴다.
형식은 JSON Patch(RFC 6902)나 JSON Merge Patch(RFC 7396)를 쓰고, `Accept-Patch`로 알린다.

`Link` 헤더(RFC 8288)는 표현 형식과 무관하게 링크를 실어 나른다.
하이퍼미디어 능력이 없는 JSON을 쓰는 API가 가장 적은 비용으로 하이퍼미디어를 도입하는 길이다.

HTTP/2는 2013년 시점에서는 다가오는 프로토콜이었고, 지금은 RFC 7540을 거쳐 RFC 9113으로 표준화됐다.
바뀐 것은 이진 프레이밍·다중화·헤더 압축 같은 전송 계층이고, 메서드와 상태 코드와 헤더의 의미론은 그대로다.
따라서 이 장의 모범 사례는 버전이 올라가도 유효하며, 오히려 RFC 9110이 의미론을 별도 문서로 떼어 내면서 그 사실이 규범 구조에 반영됐다.
