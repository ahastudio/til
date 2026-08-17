# RESTful Web APIs (Richardson & Amundsen) 정리

<http://restfulwebapis.com/>

Leonard Richardson과 Mike Amundsen이 쓰고 Sam Ruby가 서문을 붙인 O'Reilly 책 《RESTful Web
APIs》(2013)를 정리한 노트 모음이다.
이 책은 2007년의 《RESTful Web Services》(Richardson & Ruby)의 후속작이며, 이 폴더는 그
자매 폴더인 [restful-web-services](../restful-web-services/README.md)와 짝을 이룬다.

## 자료의 근거 (먼저 밝혀 둠)

이 폴더의 장별 문서는 《RESTful Web Services》 폴더와 근거가 다르다.
전작은 무료 전문이 공개돼 있어 원문에 근거해 정리했지만, 《RESTful Web APIs》는 무료 전문이
공개돼 있지 않다.

그래서 이 폴더의 장별 문서는 세 가지에만 근거한다 — 저자가 공식 사이트에 올린
[장별 설명](http://restfulwebapis.com/chapters.html), 각 장이 다루는 공개 표준의 실제 명세(RFC
9110·6838·5789·5023·8288·6906·7252, Collection+JSON·HAL·Siren·ALPS·JSON-LD 명세 등), 그리고
저자가 공개한 [예제 코드](https://github.com/RESTful-Web-APIs/example-code)다.
책 본문을 옮긴 것이 아니며, 어느 문서에도 책의 직접 인용이나 페이지 번호는 쓰지 않았다.
각 장 문서의 `## 개요`가 이 한계를 다시 밝힌다.

명세를 확보하지 못한 경우도 그대로 적어 두었다 — 예컨대 Maze+XML은 저자의 원 명세 사이트가
사라져 예제 코드의 실제 XML 출력과 제3자 구현으로 교차 확인했고, 그 사실을 5장 문서에 밝혔다.

## 이 책의 논지

REST의 인기가 커지면서 아키텍처의 이점을 대부분 담지 못한 “거의 RESTful한” API가 폭증했다.
이 책은 시간이 지나도 진화하는 사용 가능한 REST API를 설계하는 법을 다루며, 세계에서 가장 성공한
분산 컴퓨팅 시스템인 월드 와이드 웹을 위해 설계된 도구로 강력하고 안전한 애플리케이션을 만드는
법을 보인다.

전작 《RESTful Web Services》가 HTTP의 “리소스(resource)” 개념에 초점을 맞춰 사실상 서버 측을
강조했다면, 《RESTful Web APIs》는 표현(representation) — 클라이언트와 서버가 주고받는 문서 — 에
초점을 맞춘다.
저자의 말대로 REST가 사는 곳이 바로 그 표현이며, 이 책은 클라이언트와 서버가 표현을 주고받으며
서로의 상태를 조작하는 상호작용에 일관되게 초점을 둔다.
4장에 이르면 하이퍼미디어(hypermedia) — 서버가 클라이언트에게 다음에 할 수 있는 HTTP 요청을
알려 주는 최선의 방법 — 에 대한 관심이 책 전체에 퍼진다.

## 전작과의 세 가지 큰 차이

저자 Leonard Richardson이 직접 정리한 두 책의 차이는 세 가지다(자세한 분석은 아래 문서 참고).

먼저 전작은 “유효한 JSON이면서 동시에 하이퍼미디어인 문서를 어떻게 설계하는가”를 명시적으로
다루지 않았다 — 2007년에는 JSON이 지배적 API 문서 형식이 아니었기 때문이다.
둘째, JSON의 하이퍼미디어 부재에서 벗어나기 위한 새 기술(Collection+JSON, Siren, HAL, JSON-LD
등)이 전작 출간 이후 발명됐고, 이 책이 그것들을 다룬다.
셋째, 하이퍼미디어를 넘어 분야를 계속 전진시킬 프로파일(profile) 같은 최첨단 아이디어를 다룬다.

- 상세 문서: [RESTful Web Services에서 RESTful Web APIs로: 세 가지 큰 변화](whats-new.md)

## 예제 코드

책의 클라이언트·서버 예제는 별도 저장소로 공개돼 있다 — 5장의 Maze+XML 서버와 세 클라이언트,
6장의 Collection+JSON 마이크로블로깅 서버다.

- 상세 문서: [RESTful Web APIs 예제 코드: 하나의 서버, 세 개의 클라이언트](example-code.md)
- 저장소: <https://github.com/RESTful-Web-APIs/example-code>

## 목차

각 항목의 설명은 저자 공식 장별 설명을 옮긴 것이고, 링크는 이 폴더의 장별 문서다.

### 1~4장: 웹 API에 적용되는 REST의 개념

- [1장 Surfing the Web](01-surfing-the-web.md) — 이미 익숙한 RESTful 시스템, 즉 웹사이트를 예로 기본 용어를 설명한다.
- [2장 A Simple API](02-a-simple-api.md) — 1장의 웹사이트와 동일한 기능을 하는 프로그래밍 가능한 API로 웹의 교훈을 옮긴다.
- [3장 Resources and Representations](03-resources-and-representations.md) — 리소스는 HTTP의 근본 개념, 표현은 REST의 근본 개념이며, 이 장은 둘의 관계를 설명한다.
- [4장 Hypermedia](04-hypermedia.md) — 하이퍼미디어는 표현들을 하나의 일관된 API로 묶는 빠진 재료다. 이미 익숙한 하이퍼미디어 형식인 HTML을 주로 써서 하이퍼미디어의 능력을 보인다.

### 5~8장: 하이퍼미디어 API 설계 전략

- [5장 Domain-Specific Designs](05-domain-specific-designs.md) — 자기 문제에 정확히 맞는 완전히 새로운 표준을 설계하는 뻔한 전략. Maze+XML 표준을 예로 든다.
- [6장 The Collection Pattern](06-collection-pattern.md) — API 설계에서 반복해서 나타나는 컬렉션 패턴. 이 패턴을 담은 두 표준 Collection+JSON과 AtomPub을 보인다.
- [7장 Pure-Hypermedia Designs](07-pure-hypermedia-designs.md) — 컬렉션 패턴이 안 맞을 때, 범용 하이퍼미디어 형식으로 원하는 표현을 전달한다. 범용 형식 셋(HTML, HAL, Siren)을 예로 들고, 다음 장으로 이어지는 HTML 마이크로포맷과 마이크로데이터를 소개한다.
- [8장 Profiles](08-profiles.md) — 프로파일은 (여러 API가 쓸 수 있는) 데이터 형식과 특정 API 구현 사이의 틈을 메운다. 저자가 권하는 형식은 ALPS이며 XMDP와 JSON-LD도 다룬다. 이 장부터 저자의 조언이 집필 당시의 최신 기술을 앞서가기 시작하며, 저자는 이 책을 위해 ALPS 형식을 직접 개발했다.

### 9~13장: 실무 주제

- [9장 The Design Procedure](09-design-procedure.md) — 책의 모든 논의를 모아 RESTful API를 설계하는 단계별 안내를 준다.
- [10장 The Hypermedia Zoo](10-hypermedia-zoo.md) — 하이퍼미디어의 능력을 보이려 약 20종의 표준 하이퍼미디어 데이터 형식을 다룬다(대부분 다른 곳에서 다루지 않은 것).
- [11장 HTTP for APIs](11-http-for-apis.md) — API 구현에서 HTTP를 쓰는 베스트 프랙티스. 다가올 HTTP 2.0을 포함한 HTTP 확장도 논한다.
- [12장 Resource Description and Linked Data](12-linked-data.md) — Linked Data는 시맨틱 웹 진영의 REST 접근이며, JSON-LD가 가장 중요한 Linked Data 표준이다. RDF 데이터 모델과 10장에서 다루지 못한 RDF 기반 하이퍼미디어 형식도 다룬다.
- [13장 CoAP: REST for Embedded Systems](13-coap.md) — HTTP를 전혀 쓰지 않는 RESTful 프로토콜 CoAP를 다루며 본문을 마무리한다.

### 부록과 용어집

- [부록 A/B/C](appendices.md) — 상태 코드, 헤더, Fielding 학위논문
  - **부록 A The Status Codex** — 11장의 확장으로, HTTP 명세의 41개 표준 상태 코드와 몇몇 확장 코드를 깊이 있게 본다.
  - **부록 B The Header Codex** — 11장의 확장으로, HTTP 명세의 46개 요청·응답 헤더와 몇몇 확장을 상세히 정리한다.
  - **부록 C An API Designer's Guide to the Fielding Dissertation** — REST의 토대 문서인 Roy Fielding의 학위논문을 API 설계 관점에서 깊이 논한다.
- **Glossary** — RESTful 웹 API를 다룰 때 자주 만나는 용어의 정의(별도 문서로 정리하지 않았다).

## 두 책의 장 대응

전작과 이 책은 장 구성이 다르다.
같은 주제를 두 책이 어떻게 다르게 다루는지 비교해 읽고 싶을 때 쓰는 표다.

| 주제                    | 《RESTful Web Services》(2007)                                      | 《RESTful Web APIs》(2013)                                          |
| ----------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| REST의 기본 개념 소개   | [1장 프로그래머블 웹](../restful-web-services/01-programmable-web.md) | [1장 Surfing the Web](01-surfing-the-web.md)                        |
| 리소스와 표현           | [3장 무엇이 다른가](../restful-web-services/03-what-makes-restful-different.md) | [3장 Resources and Representations](03-resources-and-representations.md) |
| 아키텍처의 형식적 정의  | [4장 ROA](../restful-web-services/04-resource-oriented-architecture.md) | [4장 Hypermedia](04-hypermedia.md)                                  |
| 설계 절차               | [5·6장 서비스 설계](../restful-web-services/05-read-only-services.md) | [9장 The Design Procedure](09-design-procedure.md)                  |
| 표현 형식과 하이퍼미디어 | [9장 구성 요소](../restful-web-services/09-building-blocks.md)       | [6·7·10장 형식들](06-collection-pattern.md)                         |
| HTTP 실무               | [8장 베스트 프랙티스](../restful-web-services/08-best-practices.md)  | [11장 HTTP for APIs](11-http-for-apis.md)                           |
| 상태 코드·헤더 레퍼런스 | [부록 B/C](../restful-web-services/appendices.md)                    | [부록 A/B](appendices.md)                                           |
| 클라이언트 작성         | [2·11장 클라이언트와 Ajax](../restful-web-services/02-web-service-clients.md) | [2장 A Simple API](02-a-simple-api.md), [예제 코드](example-code.md) |
| 대안 아키텍처 비교      | [10장 ROA 대 빅 웹 서비스](../restful-web-services/10-roa-vs-big-web-services.md) | 해당 없음(SOAP 논쟁이 끝난 뒤 쓰인 책이다)                          |
| 새로 생긴 주제          | 해당 없음                                                            | [8장 프로파일](08-profiles.md), [12장 Linked Data](12-linked-data.md), [13장 CoAP](13-coap.md) |

## 초기 서평

- John Musser(Programmable Web 창립자): “대단한 책이다. 오늘날 API의 가장 중요한 흐름과 관행을 다룬다.”
- Steve Klabnik(《Designing Hypermedia APIs》 저자): “이 주제를 이토록 철저히 탐구하면서 이토록 명료하게 설명하는 다른 책을 찾지 못할 것이다.”
- Stefan Tilkov(REST 전도사): “REST에서 가장 이해가 덜 된 원칙인 하이퍼미디어 형식을 훌륭하게 다뤘다.”

## 전작 《RESTful Web Services》 (2007)

전작은 이 책으로 대체됐다.
저자는 “이제 《Services》를 살 필요가 전혀 없다, 낡았고 인터넷에서 합법적으로 무료로 얻을 수
있다”고 밝혔으며, O'Reilly는 《Services》를 절판했다.

- 전작 공식 페이지: <http://restfulwebapis.com/rws.html>
- 전작 온라인으로 무료로 읽기: <http://restfulwebapis.com/RESTful_Web_Services/>
- 이 저장소의 전작 정리: [restful-web-services](../restful-web-services/README.md)
