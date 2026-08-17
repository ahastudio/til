# RESTful Web Services (Richardson & Ruby) 정리

<http://restfulwebapis.com/rws.html>

Leonard Richardson과 Sam Ruby가 쓰고 David Heinemeier Hansson(Rails 창시자)이 서문을 붙인
O'Reilly 책 《RESTful Web Services》(2007)를 장별로 정리한 노트 모음이다.
이 폴더의 각 파일은 책의 한 장(章) 또는 부록에 대응한다.

이 책은 2013년의 후속작 《RESTful Web APIs》(Richardson & Amundsen)로 대체됐고 O'Reilly가
절판했다.
저자는 옛 책을 살 필요가 없으며 온라인에서 무료로 읽을 수 있다고 밝혔다.

- 공식 페이지: <http://restfulwebapis.com/rws.html>
- 웹에서 읽기: <http://restfulwebapis.com/RESTful_Web_Services/>
- Internet Archive: [RESTful Web Services : Leonard Richardson : Free Download, Borrow, and Streaming : Internet Archive](https://archive.org/details/RESTfulWebServices)
- 후속작: [RESTful Web APIs](../restful-web-apis)

## 이 책의 논지

저자들의 출발점은 도발적이다 — 오늘날의 “웹 서비스” 대부분은 웹과 아무 상관이 없다.
그것들은 웹의 단순함에 맞서, COM이나 CORBA처럼 분산 객체 접근을 위한 무거운 아키텍처(SOAP,
WSDL, WS-* 스택)를 택했고, 웹을 성공시킨 기능을 재발명하거나 무시한다.
이 책은 그 반대편에 선다 — “웹 서비스”에 다시 “웹”을 넣자는 것이다.

핵심 주장은 모든 웹 사이트가 이미 서비스라는 것이다.
Google 검색은 거대한 데이터베이스에 질의해 형식화된 응답을 돌려주는 원격 서비스이며, 웹을
거스르지 않고 웹과 함께 일하면 그 힘을 프로그래밍 가능한 애플리케이션에 쓸 수 있다.
사람이 쓰기 쉬운 웹 사이트를 만드는 원리를, 서퍼가 컴퓨터 프로그램인 경우로 번역하면 좋은 웹
서비스 API의 설계 원리가 된다.

도구는 세 가지뿐이다 — HTTP(애플리케이션 프로토콜), URI(이름 표준), XML(마크업 언어).
이 셋을 관통하는 원리가 REST(Representational State Transfer)이며, 저자들은 그것을 추상적 형태가
아니라 구체적 설계 지침 — 리소스 지향 아키텍처(Resource-Oriented Architecture, ROA) — 으로
제시한다.

## 꼭 기억할 두 골격

책 전체를 떠받치는 두 분류 체계가 있다.

세 가지 웹 서비스 아키텍처를 구분한다.
RESTful(리소스 지향, 통일 인터페이스를 그대로 씀), RPC 스타일(모든 것을 하나의 엔드포인트로
보내고 메서드 정보를 본문에 담음), 그리고 그 둘을 섞은 REST-RPC 하이브리드(현실의 많은 API가
여기 속한다)다.

리소스 지향 아키텍처(ROA)는 네 개념과 네 속성으로 이루어진다.
네 개념은 리소스(resource), 그 이름(URI), 그 표현(representation), 그리고 리소스 사이의 링크(link)다.
네 속성은 주소 지정 가능성(addressability), 무상태성(statelessness), 연결성(connectedness), 통일
인터페이스(uniform interface)다.
좋은 서비스는 이 네 속성으로 평가된다.

## 목차

- [1장 프로그래머블 웹과 그 거주자들](01-programmable-web.md) — 웹 서비스란 무엇이고, 세 아키텍처(RESTful/RPC/하이브리드)는 어떻게 다른가
- [2장 웹 서비스 클라이언트 작성하기](02-web-service-clients.md) — HTTP 라이브러리와 XML/JSON 파서로 기존 서비스의 클라이언트 만들기(del.icio.us 예제)
- [3장 RESTful 서비스는 무엇이 다른가](03-what-makes-restful-different.md) — Amazon S3를 사례로 리소스·표현·통일 인터페이스
- [4장 리소스 지향 아키텍처(ROA)](04-resource-oriented-architecture.md) — REST의 형식적 소개, 네 개념과 네 속성 (책의 핵심)
- [5장 읽기 전용 리소스 지향 서비스 설계](05-read-only-services.md) — 요구사항을 리소스 집합으로 바꾸는 절차(지도 서비스 예제)
- [6장 읽기/쓰기 리소스 지향 서비스 설계](06-read-write-services.md) — 클라이언트가 리소스를 생성·수정·삭제하게 확장하기
- [7장 서비스 구현: 소셜 북마킹](07-service-implementation.md) — RPC 스타일 서비스를 순수 RESTful로 다시 설계해 Rails로 구현
- [8장 REST와 ROA 베스트 프랙티스](08-best-practices.md) — 설계 지침 총정리와 HTTP 표준 기능의 활용
- [9장 서비스의 구성 요소](09-building-blocks.md) — HTTP·URI·XML 위에 얹는 표현 포맷·APP·하이퍼미디어 기술
- [10장 ROA 대 빅 웹 서비스(SOAP/WS-*)](10-roa-vs-big-web-services.md) — SOAP·WSDL·UDDI·WS-* 스택과의 비교
- [11장 REST 클라이언트로서의 Ajax 애플리케이션](11-ajax-as-rest-clients.md) — 브라우저 안에서 도는 웹 서비스 클라이언트
- [12장 RESTful 서비스를 위한 프레임워크](12-frameworks.md) — Ruby on Rails, Restlet(Java), Django(Python)
- [부록: REST 자료, HTTP 상태 코드, HTTP 헤더 레퍼런스](appendices.md) — 부록 A/B/C

## 후속작과 함께 읽기

같은 저자가 2013년에 쓴 후속작도 이 저장소에 장별로 정리돼 있다 —
[restful-web-apis](../restful-web-apis).

두 책은 초점이 다르다.
이 책은 HTTP의 “리소스” 개념에 초점을 맞춰 사실상 서버 측을 강조하지만, 후속작은 클라이언트와
서버가 주고받는 문서, 즉 “표현”에 초점을 맞춘다.
후속작의 4장 이후로는 하이퍼미디어 — 서버가 클라이언트에게 다음에 할 수 있는 요청을 알려 주는
방법 — 에 대한 관심이 책 전체를 관통한다.

이 책에서 시대의 흔적이 가장 짙은 부분은 후속작에서 다시 읽는 것이 낫다.
9장의 표현 포맷 논의는 2007년의 XML 중심이라 JSON 시대의 형식들(Collection+JSON, HAL, Siren)을
다루지 못하므로 후속작 [6장](../restful-web-apis/06-collection-pattern.md)·[7장](../restful-web-apis/07-pure-hypermedia-designs.md)으로,
10장의 SOAP·WS-\* 비교는 그 논쟁이 끝난 뒤라 후속작에 대응 장이 없다.
반대로 이 책에만 있는 것도 있다 — 4장의 ROA 네 속성(주소 지정 가능성·무상태성·연결성·통일
인터페이스)은 후속작이 전제로 깔고 반복하지 않으므로, REST의 형식적 정의를 잡으려면 이 책의
[4장](04-resource-oriented-architecture.md)이 여전히 출발점이다.

장 대응표는 후속작 폴더의 [README](../restful-web-apis)에 정리해 두었다.

## 읽기 경로

저자들이 제안하는 경로는 독자의 목적에 따라 갈린다.

웹 서비스 경험이 많지 않고 처음부터 배우려면, 1장부터 9장까지 순서대로 읽은 뒤 관심에 따라
이어 가는 것이 가장 단순한 길이다.
기존 서비스의 클라이언트만 만들 것이라면 1·2·3·11장에 집중하면 되고, 서비스 설계 부분은 크게
쓸모가 없다.
자기 웹 서비스를 만들거나 REST가 무엇인지 파악하려면 4장부터 9장까지가 책의 핵심이다.
10·11·12장은 각각 책 한 권이 될 수 있는 특화 주제다.

## 한 가지 유의점

이 책은 2007년에 쓰였다.
REST·ROA의 개념과 설계 원리(4·5·6·8장)는 지금도 그대로 유효하지만, 구체적 도구와 생태계 서술 —
12장의 프레임워크 버전, 9장의 일부 포맷(WADL 등), del.icio.us 같은 예제 서비스 — 은 시대의
흔적을 담고 있다.
개념은 원전 그대로 읽되, 특정 라이브러리·서비스의 현재 상태는 별도로 확인하는 것이 좋다.
