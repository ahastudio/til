# 13장 CoAP: HTTP를 쓰지 않는 RESTful 프로토콜

《RESTful Web APIs》(Leonard Richardson, Mike Amundsen, O'Reilly 2013) 13장 정리.

## 개요

13장은 책 본론의 마지막 장으로, HTTP를 전혀 쓰지 않는 RESTful 프로토콜인 CoAP를 다룬다.
이 정리는 저자의 공식 장별 설명과 해당 장이 다루는 공개 표준을 근거로 하며, 책 본문을 옮긴 것이 아니다.

이 장을 마지막에 놓은 배치 자체가 논지다.
앞의 열두 장이 REST를 HTTP 위에서 설명했지만, REST는 아키텍처 스타일이지 프로토콜이 아니다.
CoAP는 그 사실의 실증이다 — 리소스, URI, 표현, 메서드, 하이퍼미디어라는 REST의 골격을 유지하면서 전송 계층부터 메시지 인코딩까지 전부 다르게 만든 프로토콜이 실제로 존재하고 표준화됐다.

시점을 하나 짚어 둔다.
책이 나온 2013년 시점에 CoAP는 IETF CoRE 워킹그룹의 초안 단계였고, RFC 7252 The Constrained Application Protocol (CoAP)로 표준화된 것은 2014년 6월이다.
아래 서술은 RFC 7252와 그 확장 명세들을 기준으로 한다.

## 왜 별도의 프로토콜인가: 제약된 환경

CoAP의 설계 목표는 제약된 노드(constrained node)와 제약된 네트워크를 위한 웹 전송 프로토콜이다.
전형적인 대상은 8비트 마이크로컨트롤러에 수십 KB 수준의 메모리를 가진 센서·액추에이터이고, 네트워크는 6LoWPAN 같은 저전력 무손실 보장이 없는 링크다.

이 환경에서 HTTP/1.1은 두 가지 이유로 부담이다.
텍스트 기반 파싱과 큰 헤더가 코드 크기와 대역폭을 잡아먹고, TCP의 연결 수립과 상태 유지가 배터리로 도는 노드에 비싸다.

CoAP의 답은 의미론은 유지하고 표현을 압축하는 것이다.
GET/POST/PUT/DELETE와 리소스·URI 개념은 그대로 두고, 전송을 UDP로 바꾸고 헤더를 이진으로 압축한다.

## 전송: 기본은 UDP다

RFC 7252 3절은 CoAP가 간결한 메시지 교환에 기반하며 기본적으로 UDP 위에서 전송된다고 규정한다.
CoAP 메시지 하나가 하나의 UDP 데이터그램의 데이터 부분을 차지한다.

보안이 필요하면 DTLS(Datagram TLS) 위에서 쓴다.
SMS, TCP, SCTP 같은 다른 전송 위에서도 쓸 수 있으나 그 명세는 RFC 7252의 범위 밖이다.
UDP-lite와 UDP zero checksum은 지원하지 않는다.

URI 스킴과 기본 포트는 이렇다.

| 스킴    | 전송     | 기본 포트 |
| ------- | -------- | --------- |
| `coap`  | UDP      | 5683      |
| `coaps` | DTLS/UDP | 5684      |

```text
coap://example.com:5683/~sensors/temp.xml
```

## 메시지 형식: 4바이트 고정 헤더

CoAP 메시지는 단순한 이진 형식으로 인코딩되며, 4바이트 고정 크기 헤더로 시작한다.
그 뒤에 0~8바이트의 가변 길이 토큰(Token)이 오고, 이어서 TLV 형식의 옵션 0개 이상이 오며, 마지막으로 선택적 페이로드가 데이터그램의 나머지를 차지한다.

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ver| T |  TKL  |      Code     |          Message ID           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Token (if any, TKL bytes) ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Options (if any) ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|1 1 1 1 1 1 1 1|    Payload (if any) ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

각 필드는 다음과 같다.

| 필드               | 크기   | 뜻                                                               |
| ------------------ | ------ | ---------------------------------------------------------------- |
| Ver (Version)      | 2비트  | CoAP 버전. 이 명세의 구현은 1로 설정한다                         |
| T (Type)           | 2비트  | Confirmable(0), Non-confirmable(1), Acknowledgement(2), Reset(3) |
| TKL (Token Length) | 4비트  | 토큰 길이 0~8바이트. 9~15는 예약이며 메시지 형식 오류로 처리한다 |
| Code               | 8비트  | 3비트 클래스 + 5비트 detail. `c.dd` 표기                         |
| Message ID         | 16비트 | 중복 검출과 ACK/RST 대응에 쓰는 식별자                           |

페이로드가 있으면 고정 1바이트 페이로드 마커 `0xFF`가 앞에 붙어 옵션의 끝과 페이로드의 시작을 표시한다.
페이로드 길이는 데이터그램 크기에서 계산한다 — 즉 `Content-Length` 같은 헤더가 필요 없다.

토큰과 Message ID의 역할 분담이 중요하다.
Message ID는 메시지 계층의 중복 검출과 확인 응답 대응에 쓰이고, 토큰은 요청과 응답을 상관시키는 데 쓰인다.
이 분리 덕분에 아래에서 볼 분리 응답(separate response)이 가능하다.

## 메시지 계층: 확인 가능한 메시지와 확인 불가능한 메시지

UDP는 신뢰성을 보장하지 않으므로, CoAP는 애플리케이션 계층에서 선택적 신뢰성을 제공한다.
이것이 메시지 타입 네 가지의 존재 이유다.

Confirmable(CON) 메시지는 신뢰성 있는 전송을 요청한다.
수신자는 반드시 (a) Acknowledgement(ACK) 메시지로 확인하거나, (b) 메시지를 제대로 처리할 맥락이 없으면 Reset(RST) 메시지를 보내 거절해야 한다.
송신자는 ACK나 RST를 받거나 시도 횟수를 소진할 때까지 지수적으로 늘어나는 간격으로 재전송한다.

기본 전송 파라미터는 `ACK_TIMEOUT`이 2초, `MAX_RETRANSMIT`이 4다.
초기 타임아웃은 `ACK_TIMEOUT`과 `ACK_TIMEOUT * ACK_RANDOM_FACTOR` 사이의 무작위 값으로 잡는다.

Non-confirmable(NON) 메시지는 확인을 요구하지 않는다.
주기적으로 값을 흘려 보내는 센서처럼 개별 메시지 하나가 유실돼도 무방한 경우에 쓴다.

이 메시지 계층이 요청/응답 계층과 분리돼 있다는 점이 CoAP 설계의 핵심이다.
“신뢰성 있게 보낼 것인가”와 “무엇을 요청할 것인가”가 서로 직교한다.

## 요청/응답: 피기백 응답과 분리 응답

응답이 요청과 어떻게 짝지어지는지에 두 가지 방식이 있다.

피기백 응답(piggybacked response)은 CON 요청에 대한 응답이 그 ACK 메시지에 함께 실려 오는 것이다.
왕복 하나로 끝나므로 가장 효율적이며, 별도의 확인이 필요 없다 — ACK가 유실되면 클라이언트가 요청을 재전송하기 때문이다.

```text
Client              Server       Client              Server
   |                  |             |                  |
   |   CON [0xbc90]   |             |   CON [0xbc91]   |
   | GET /temperature |             | GET /temperature |
   |   (Token 0x71)   |             |   (Token 0x72)   |
   +----------------->|             +----------------->|
   |                  |             |                  |
   |   ACK [0xbc90]   |             |   ACK [0xbc91]   |
   |   2.05 Content   |             |  4.04 Not Found  |
   |   (Token 0x71)   |             |   (Token 0x72)   |
   |     "22.5 C"     |             |   "Not found"    |
   |<-----------------+             |<-----------------+
```

분리 응답(separate response)은 서버가 즉시 응답할 수 없을 때 쓴다.
서버는 먼저 빈 ACK를 보내 클라이언트의 재전송을 멈추게 하고, 응답이 준비되면 새 CON 메시지로 보낸다 — 이번엔 클라이언트가 그것을 ACK한다.

```text
Client              Server
   |                  |
   |   CON [0x7a10]   |
   | GET /temperature |
   |   (Token 0x73)   |
   +----------------->|
   |                  |
   |   ACK [0x7a10]   |
   |<-----------------+
   |                  |
   ... Time Passes  ...
   |                  |
   |   CON [0x23bb]   |
   |   2.05 Content   |
   |   (Token 0x73)   |
   |     "22.5 C"     |
   |<-----------------+
   |                  |
   |   ACK [0x23bb]   |
   +----------------->|
```

두 흐름에서 Message ID는 바뀌지만 토큰(0x73)은 유지된다.
클라이언트가 응답을 원래 요청과 짝짓는 것은 토큰이다.

## 메서드와 코드 체계

CoAP의 Code 필드는 8비트를 3비트 클래스와 5비트 detail로 쪼개 `c.dd`로 표기한다.
클래스는 요청(0), 성공 응답(2), 클라이언트 오류 응답(4), 서버 오류 응답(5)을 나타낸다.
Code 0.00은 특별히 빈(Empty) 메시지를 뜻한다.

메서드는 네 개다.

| 코드 | 메서드 |
| ---- | ------ |
| 0.01 | GET    |
| 0.02 | POST   |
| 0.03 | PUT    |
| 0.04 | DELETE |

응답 코드는 HTTP의 세 자리 코드와 눈에 띄게 닮았지만 같지는 않다.
3.xx 대역은 예약돼 있고 리다이렉션 코드가 없다는 점이 특히 다르다.

| 코드 | 뜻                         |
| ---- | -------------------------- |
| 2.01 | Created                    |
| 2.02 | Deleted                    |
| 2.03 | Valid                      |
| 2.04 | Changed                    |
| 2.05 | Content                    |
| 4.00 | Bad Request                |
| 4.01 | Unauthorized               |
| 4.02 | Bad Option                 |
| 4.03 | Forbidden                  |
| 4.04 | Not Found                  |
| 4.05 | Method Not Allowed         |
| 4.06 | Not Acceptable             |
| 4.12 | Precondition Failed        |
| 4.13 | Request Entity Too Large   |
| 4.15 | Unsupported Content-Format |
| 5.00 | Internal Server Error      |
| 5.01 | Not Implemented            |
| 5.02 | Bad Gateway                |
| 5.03 | Service Unavailable        |
| 5.04 | Gateway Timeout            |
| 5.05 | Proxying Not Supported     |

성공 코드가 HTTP보다 세분화된 것을 눈여겨볼 만하다.
HTTP가 `200 OK` 하나로 뭉뚱그리는 자리를, CoAP는 `2.05 Content`(GET 성공), `2.04 Changed`(PUT/POST로 변경됨), `2.03 Valid`(조건부 요청에서 유효함), `2.02 Deleted`(DELETE 성공)로 나눈다.
2.03 Valid가 HTTP의 `304 Not Modified` 자리를 대신하는 셈이다.

## 옵션: HTTP 헤더에 해당하는 것

HTTP의 헤더 필드에 대응하는 것이 CoAP의 옵션(Option)이다.
문자열 이름 대신 숫자 옵션 번호를 쓰고, 메시지 안에서는 옵션 번호 순으로 정렬한 뒤 앞 옵션과의 델타만 인코딩한다 — 이것이 헤더 압축의 실체다.

RFC 7252가 정의하는 옵션은 다음과 같다.

| 번호 | 이름           | 형식   | 길이   | 기본값      |
| ---- | -------------- | ------ | ------ | ----------- |
| 1    | If-Match       | opaque | 0-8    | (없음)      |
| 3    | Uri-Host       | string | 1-255  | (아래 참조) |
| 4    | ETag           | opaque | 1-8    | (없음)      |
| 5    | If-None-Match  | empty  | 0      | (없음)      |
| 7    | Uri-Port       | uint   | 0-2    | (아래 참조) |
| 8    | Location-Path  | string | 0-255  | (없음)      |
| 11   | Uri-Path       | string | 0-255  | (없음)      |
| 12   | Content-Format | uint   | 0-2    | (없음)      |
| 14   | Max-Age        | uint   | 0-4    | 60          |
| 15   | Uri-Query      | string | 0-255  | (없음)      |
| 17   | Accept         | uint   | 0-2    | (없음)      |
| 20   | Location-Query | string | 0-255  | (없음)      |
| 35   | Proxy-Uri      | string | 1-1034 | (없음)      |
| 39   | Proxy-Scheme   | string | 1-255  | (없음)      |
| 60   | Size1          | uint   | 0-4    | (없음)      |

옵션은 Critical/Elective, Safe/Unsafe, NoCacheKey, Repeatable로 분류된다.
Critical 옵션을 이해하지 못하면 메시지를 거절해야 하고, Elective 옵션은 무시해도 된다.
이 분류는 HTTP에 없는 장치로, 확장이 도입돼도 옛 구현이 안전하게 동작하도록 보장한다.

몇 가지가 API 설계와 직결된다.

URI가 통째로 실리지 않고 쪼개져 실린다.
`Uri-Host`, `Uri-Port`, `Uri-Path`, `Uri-Query`가 각각의 옵션이며, 경로 세그먼트 하나가 `Uri-Path` 옵션 하나다.
즉 `/sensors/temp`는 `Uri-Path: sensors`와 `Uri-Path: temp` 두 옵션이 된다.

조건부 요청은 그대로 있다.
`ETag`, `If-Match`, `If-None-Match`가 HTTP와 같은 역할을 한다 — 11장에서 본 조건부 요청 개념이 프로토콜을 갈아타도 살아남는다.

캐싱도 있다.
`Max-Age` 옵션이 응답의 신선도 수명을 초 단위로 지정하며 기본값은 60초다.
HTTP의 `Cache-Control: max-age`에 해당하는데, 지시어가 하나뿐이고 기본값이 있다는 점이 제약된 환경에 맞춘 단순화다.

콘텐츠 협상도 있다.
`Content-Format`과 `Accept`가 미디어 타입을 나타내되, 문자열이 아니라 숫자 ID를 쓴다.

| 미디어 타입                 | ID  |
| --------------------------- | --- |
| `text/plain; charset=utf-8` | 0   |
| `application/link-format`   | 40  |
| `application/xml`           | 41  |
| `application/octet-stream`  | 42  |
| `application/exi`           | 47  |
| `application/json`          | 50  |

미디어 타입을 문자열이 아니라 레지스트리 번호로 부른다는 것은 이 책의 논지에 흥미로운 각주다.
미디어 타입이라는 개념 자체는 유지되지만, 그것을 지시하는 방식은 대역폭 제약에 맞춰 완전히 다시 짜였다.

## Observe: 폴링 없이 변화를 받기

CoAP의 GET은 그 순간의 표현 하나만 준다.
센서 값을 계속 지켜보려면 폴링해야 하는데, 배터리로 도는 노드에게 폴링은 비싸다.

RFC 7641 Observing Resources in CoAP(2015)가 이 문제를 푼다.
옵션 번호 6번인 `Observe` 옵션이 GET 메서드를 확장해, 현재 표현을 가져올 뿐 아니라 서버에게 그 리소스의 관찰자 목록에 항목을 추가하거나 제거하도록 요청한다.
목록의 항목은 클라이언트 엔드포인트와 클라이언트가 요청에 지정한 토큰으로 이루어진다.

옵션 값의 의미는 요청과 응답에서 다르다.

```text
요청에서:  0 = register   (관찰자 목록에 추가)
           1 = deregister (관찰자 목록에서 제거)
응답에서:  재정렬 검출용 순번(sequence number)
```

클라이언트는 `Observe: 0`을 담은 GET으로 관심을 등록한다.
서버가 `Observe` 옵션을 포함한 2.xx 응답을 돌려주면 등록이 성공한 것이며, 이후 리소스 상태가 바뀔 때마다 알림(notification)을 받는다.

우아한 점은 실패 시 동작이다.
`Observe`는 처리에 필수인 옵션(critical)이 아니다.
서버가 새 항목을 추가할 의사나 능력이 없으면 요청은 그냥 평범한 GET으로 떨어지고, 응답에 `Observe` 옵션이 포함되지 않는다.
클라이언트는 응답에 `Observe`가 있는지만 보고 관찰이 성립했는지 판별한다.

알림은 요청의 토큰을 그대로 달고 오므로 클라이언트가 어느 관찰에 대한 것인지 구분할 수 있다.
알림에도 `Max-Age`가 실려, 그 시간이 지나도 새 알림이 없으면 클라이언트는 관찰이 끊겼다고 보고 재등록한다.

이것이 REST 관점에서 흥미로운 이유는, Observe가 새 메서드를 만들지 않고 GET의 의미를 확장했다는 점이다.
통일 인터페이스를 깨지 않으면서 푸시에 가까운 동작을 얻는다.

## 리소스 디스커버리: /.well-known/core

사람이 개입하지 않는 M2M 환경에서는 리소스 발견이 특히 중요하다.
RFC 7252 7.2절은 이 점을 명시하며, CoAP 엔드포인트가 RFC 6690의 CoRE Link Format을 지원해야 한다(SHOULD)고 권고한다 — 완전 수동 설정을 의도하는 경우만 예외다.
어떤 리소스를 발견 가능하게 할지는 서버가 정한다.

발견 지점은 잘 알려진 URI인 `/.well-known/core`다.

```text
REQ: GET /.well-known/core

RES: 2.05 Content
</sensors/temp>;if="sensor",
</sensors/light>;if="sensor"
```

응답의 미디어 타입은 `application/link-format`(Content-Format ID 40)이며, 문법은 11장에서 본 HTTP `Link` 헤더의 값 문법과 같은 계보다.
꺾쇠로 감싼 URI 참조 뒤에 세미콜론으로 구분된 속성을 붙이고, 쉼표로 여러 링크를 잇는다.

링크 속성에는 `rt`(resource type), `if`(interface description), `ct`(content type), `sz` 등이 있다.
RFC 7252는 `ct` 속성을 새로 정의해, 그 리소스가 반환하는 Content-Format에 대한 힌트를 준다 — 예컨대 `application/xml`은 `ct=41`이다.
다만 이것은 힌트일 뿐이며, 실제로 표현을 요청해 얻은 응답의 Content-Format 옵션을 무시하지 못한다.

질의 필터링도 가능하다.

```text
GET /.well-known/core?rt=temperature-c
```

이렇게 하면 Resource Type이 `temperature-c`인 리소스만 요청한다 — 다만 서버가 필터링을 지원할 의무는 없다.

이 메커니즘의 REST적 의미는 분명하다.
`/.well-known/core`가 API의 진입점(billboard URL) 역할을 하고, 링크 포맷 문서가 하이퍼미디어 역할을 한다.
클라이언트가 URI 구조를 미리 알 필요 없이 링크를 따라가는, 이 책이 줄곧 주장한 그 구조다.

## HTTP와의 매핑

RFC 7252 10절은 CoAP와 HTTP 사이의 교차 프로토콜 프록시를 규정한다.
CoAP가 HTTP 기능의 제한된 부분집합을 지원하므로 HTTP로의 교차 프로토콜 프록시는 직관적이라는 것이 명세의 전제다.

방향은 둘이다.

CoAP-HTTP 프록시는 CoAP 클라이언트가 중간자를 통해 HTTP 서버의 리소스에 접근하게 한다.
CoAP 요청에 `http` 또는 `https` URI를 담은 `Proxy-Uri`나 `Proxy-Scheme` 옵션을 실어 개시한다.

HTTP-CoAP 프록시는 HTTP 클라이언트가 중간자를 통해 CoAP 서버의 리소스에 접근하게 한다.
HTTP 요청의 요청 라인에 `coap` 또는 `coaps` URI를 지정해 개시한다.

여기서 명세가 분명히 못을 긋는 대목이 핵심이다.
어느 방향이든 매핑되는 것은 CoAP의 요청/응답 모델뿐이며, Confirmable/Non-confirmable 메시지 같은 하부 모델은 프록시 기능에 보이지 않고 아무 영향도 주지 않아야 한다.

이 문장이 CoAP 설계의 층위 분리를 요약한다.
메시지 계층(CON/NON/ACK/RST)은 UDP의 비신뢰성을 메우기 위한 CoAP 고유의 장치이고, 그 위의 요청/응답 계층은 HTTP와 개념을 공유한다.
그래서 매핑이 가능하다.

프록시 실패 시의 응답 코드도 정의돼 있다.
프록시가 HTTP URI 요청을 처리할 수 없거나 하지 않으려 하면 `5.05 Proxying Not Supported`, 제3자와 상호작용해 합리적 시간 안에 결과를 얻지 못하면 `5.04 Gateway Timeout`, 결과를 얻었으나 이해하지 못하면 `5.02 Bad Gateway`를 돌려준다.

GET을 예로 들면, 프록시는 성공 시 `2.05 Content`를 반환해야 하며(SHOULD) 응답 페이로드는 대상 HTTP 리소스의 표현이고 Content-Format 옵션을 그에 맞게 설정해야 한다.

명세가 규정하지 않는 것도 있다.
리버스 프록시는 명세되지 않았는데, 프록시 기능이 클라이언트에게 투명하고 프록시가 원 서버처럼 동작하기 때문이다.

## 그 밖의 확장

CoAP 생태계는 RFC 7252 이후 여러 확장으로 채워졌다.

블록 단위 전송(RFC 7959)은 UDP 데이터그램에 담기지 않는 큰 표현을 나눠 보내는 `Block1`/`Block2` 옵션을 정의한다.
데이터그램 하나에 메시지 하나라는 CoAP의 전제 때문에 필요한 확장이다.

멀티캐스트 지원은 RFC 7252 8절에 있다.
IP 멀티캐스트 그룹으로 요청을 보낼 수 있는데, 이 경우 NON 메시지를 쓰고 응답 폭주를 막기 위해 응답을 지연시킨다.

보안은 DTLS로 처리한다(RFC 7252 9절).
`coaps` 스킴과 5684 포트가 이에 대응한다.

## 핵심 정리

CoAP는 REST가 HTTP와 같은 것이 아님을 보이는 증거다.
리소스, URI, 표현, 통일 인터페이스, 하이퍼미디어라는 REST의 골격을 그대로 두고, 전송과 인코딩을 제약된 환경에 맞춰 전부 새로 짰다.

전송은 기본이 UDP이며 보안이 필요하면 DTLS를 쓴다.
스킴은 `coap`(포트 5683)과 `coaps`(포트 5684)다.

메시지는 4바이트 고정 헤더로 시작한다.
버전 2비트, 타입 2비트, 토큰 길이 4비트, 코드 8비트, Message ID 16비트다.
그 뒤에 0~8바이트 토큰, TLV 옵션들, `0xFF` 마커와 페이로드가 온다.

신뢰성은 메시지 계층에서 선택적으로 제공한다.
Confirmable 메시지는 ACK를 요구하고 지수 백오프로 재전송하며(기본 `ACK_TIMEOUT` 2초, `MAX_RETRANSMIT` 4), Non-confirmable 메시지는 확인을 요구하지 않는다.
응답은 ACK에 실리는 피기백 응답이거나, 빈 ACK 후 별도 CON으로 오는 분리 응답이다.
요청과 응답을 짝짓는 것은 Message ID가 아니라 토큰이다.

메서드는 GET(0.01), POST(0.02), PUT(0.03), DELETE(0.04) 네 개다.
응답 코드는 `c.dd` 형식이며 2.xx 성공, 4.xx 클라이언트 오류, 5.xx 서버 오류다 — 3.xx 리다이렉션은 예약 상태로 존재하지 않는다.
`2.05 Content`, `2.04 Changed`, `2.03 Valid`, `2.02 Deleted`처럼 HTTP의 `200 OK` 자리를 세분화한 것이 특징이다.

옵션이 HTTP 헤더를 대신하며, 번호와 델타 인코딩으로 압축된다.
`ETag`/`If-Match`/`If-None-Match`(조건부 요청), `Max-Age`(캐싱, 기본 60초), `Content-Format`/`Accept`(협상, 숫자 ID)가 HTTP의 대응 기능을 그대로 담고 있다.
URI는 `Uri-Host`/`Uri-Port`/`Uri-Path`/`Uri-Query` 옵션으로 쪼개져 실린다.

Observe 확장(RFC 7641)은 옵션 6번으로 GET을 확장해 관찰 등록(0)과 해제(1)를 표현한다.
새 메서드를 만들지 않고 통일 인터페이스 안에서 푸시에 가까운 동작을 얻는다는 점이 설계상 중요하며, 서버가 지원하지 않으면 평범한 GET으로 자연스럽게 떨어진다.

리소스 디스커버리는 `/.well-known/core`에서 `application/link-format`(RFC 6690, Content-Format 40) 문서를 GET하는 방식이다.
이것이 CoAP API의 진입점이자 하이퍼미디어이며, `rt`/`if`/`ct` 같은 링크 속성으로 리소스를 서술한다.

HTTP와의 매핑은 요청/응답 계층에서만 이루어진다.
CoAP-HTTP 프록시는 `Proxy-Uri`/`Proxy-Scheme` 옵션으로, HTTP-CoAP 프록시는 HTTP 요청 라인의 `coap` URI로 개시한다.
CON/NON 같은 메시지 계층은 프록시에 보이지 않으며 영향을 주지 않아야 한다 — 이 층위 분리가 매핑을 가능하게 하는 근거다.
