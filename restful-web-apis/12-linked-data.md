# 12장 리소스 서술과 Linked Data: JSON-LD와 RDF

《RESTful Web APIs》(Leonard Richardson, Mike Amundsen, O'Reilly 2013) 12장 정리.

## 개요

12장은 시맨틱 웹 진영이 REST에 접근하는 방식인 Linked Data를 다룬다.
저자의 설명에 따르면 JSON-LD는 논란의 여지는 있으나 가장 중요한 Linked Data 표준이며, 8장에서 간략히 다룬 것을 여기서 다시 본다.
이 장은 또한 RDF 데이터 모델과, 10장에서 다루지 못한 RDF 기반 하이퍼미디어 형식들을 다룬다.
이 정리는 저자의 공식 장별 설명과 해당 장이 다루는 공개 표준을 근거로 하며, 책 본문을 옮긴 것이 아니다.

이 장이 풀려는 문제는 앞선 장들의 문제와 이어져 있다.
하이퍼미디어는 “다음에 어떤 요청을 할 수 있는가”를 알려 주지만, “이 필드가 무엇을 뜻하는가”는 알려 주지 않는다.
8장의 프로파일이 그 빈틈을 미디어 타입 밖에서 메우려 했다면, Linked Data는 같은 문제를 전혀 다른 방향 — 모든 이름을 전역 식별자로 만드는 방향 — 에서 푼다.

## RDF 데이터 모델: 세상을 트리플로 서술한다

RDF는 그래프 데이터 모델이다.
RDF 1.1 Concepts and Abstract Syntax의 정의에 따르면 RDF 그래프는 RDF 트리플(triple)의 집합이며, 하나의 트리플은 세 성분으로 이루어진다.

```text
subject    (주어)   IRI 또는 blank node
predicate  (술어)   IRI
object     (목적어) IRI, 리터럴(literal), 또는 blank node
```

트리플은 관례적으로 주어, 술어, 목적어 순서로 쓴다.
그래프의 노드 집합은 트리플들의 주어와 목적어의 집합이며, 술어로 쓰인 IRI가 같은 그래프에서 노드로 등장할 수도 있다.
IRI, 리터럴, blank node를 통틀어 RDF 항(RDF term)이라 부른다.

RDF 트리플을 주장한다는 것은 술어가 가리키는 어떤 관계가 주어와 목적어에 해당하는 두 리소스 사이에 성립함을 말하는 것이다.
술어 자체는 IRI이며 속성(property)을 가리킨다.

이 모델의 성질 두 가지가 API 설계 관점에서 중요하다.

첫째, 이름이 전역적이다.
`name`이라는 문자열이 아니라 `http://schema.org/name`이라는 IRI가 속성을 식별하므로, 서로 다른 출처의 데이터를 합쳐도 이름 충돌이 없다.
게다가 그 IRI를 역참조(dereference)하면 그 용어의 정의를 얻을 수 있다.

둘째, 문서가 아니라 그래프가 단위다.
RDF 그래프는 트리플의 집합이므로 두 그래프의 병합은 단순한 합집합이다.
API가 돌려주는 문서들을 계속 모아 하나의 큰 그래프로 쌓을 수 있다는 뜻이며, 이것이 “Linked Data”라는 이름의 실질이다.

RDF는 추상 모델이므로 직렬화 형식은 여러 가지다.
RDF/XML, Turtle, N-Triples, TriG, 그리고 JSON-LD가 모두 같은 트리플 집합을 각각 다르게 표기한 것이다.
이 책이 JSON-LD에 무게를 싣는 이유는 그것이 웹 API 개발자가 이미 쓰고 있는 JSON과 형식을 공유하기 때문이다.

## JSON-LD: JSON을 고치지 않고 Linked Data로 만들기

JSON-LD는 Linked Data를 직렬화하는 JSON 기반 형식이다.
JSON-LD 1.1 명세의 초록은 이 형식의 문법이 이미 JSON을 쓰고 있는 시스템에 쉽게 통합되도록 설계됐으며, JSON에서 JSON-LD로 매끄럽게 넘어갈 경로를 제공한다고 밝힌다.
JSON-LD 1.0은 2014년 1월 W3C 권고안이 됐고, 현행 JSON-LD 1.1은 2020년 7월 권고안으로 1.0의 상위집합이다.

명세가 짚는 일반 JSON의 두 가지 한계가 출발점이다.
서로 다른 출처의 JSON은 키가 충돌해 통합이 어렵고, JSON에는 하이퍼링크에 대한 내장 지원이 없다.

명세가 드는 예시로 보면 문제가 분명하다.

```json
{
  "name": "Manu Sporny",
  "homepage": "http://manu.sporny.org/",
  "image": "http://manu.sporny.org/images/manu.png"
}
```

사람은 이것이 어떤 사람에 관한 데이터이고 `homepage`가 그 사람의 홈페이지 URL이라는 것을 곧바로 안다.
기계에는 그런 직관이 없다.
해결책은 `name`, `homepage` 같은 토큰 대신 모호하지 않은 식별자 — IRI — 로 개념을 가리키는 것이다.

### `@context`: 용어를 IRI로 매핑한다

`@context`는 용어(term)를 IRI에 매핑한다.
명세의 비유대로, 두 사람이 대화할 때 공유하는 맥락이 있으면 축약어를 써도 정확성을 잃지 않는 것과 같다.

```json
{
  "@context": {
    "name": "http://schema.org/name",
    "image": {
      "@id": "http://schema.org/image",
      "@type": "@id"
    },
    "homepage": {
      "@id": "http://schema.org/url",
      "@type": "@id"
    }
  }
}
```

용어 정의의 값은 단순 문자열이거나 맵이다.
맵인 경우를 확장 용어 정의(expanded term definition)라 부르며, 위에서는 `image`와 `homepage`의 문자열 값을 IRI로 해석하라고 지시한다.

컨텍스트는 문서에 직접 넣을 수도 있고 URL로 참조할 수도 있다.

```json
{
  "@context": "https://json-ld.org/contexts/person.jsonld",
  "name": "Manu Sporny",
  "homepage": "http://manu.sporny.org/",
  "image": "http://manu.sporny.org/images/manu.png"
}
```

여기가 이 형식의 핵심이다.
기존 JSON 문서에 줄 하나를 더한 것뿐인데, 그 문서는 이제 Linked Data다.
게다가 명세는 JSON 문서를 아예 수정하지 않고도 HTTP `Link` 헤더로 컨텍스트를 붙여 JSON-LD로 해석하게 하는 길을 정의한다(11장의 `Link` 헤더가 여기서 다시 등장한다).

### `@id`: 노드를 식별한다

RDF 그래프의 노드를 외부에서 참조하려면 식별자가 있어야 한다.
JSON-LD에서 노드는 `@id` 키워드로 식별하며, 그 값은 IRI다.

```json
{
  "@context": "https://json-ld.org/contexts/person.jsonld",
  "@id": "http://me.markus-lanthaler.com/",
  "name": "Markus Lanthaler",
  "homepage": "http://www.markus-lanthaler.com/"
}
```

`@id`의 값은 상대 IRI 참조여도 되며, 이 경우 기준 IRI(base IRI)에 대해 해석된다.
그리고 IRI로 해석되는 값을 명시적으로 표시하는 것도 `@id`의 역할이다.

```json
{
  "homepage": { "@id": "http://example.com/" }
}
```

명세가 정리하는 바로, JSON-LD에서 IRI가 생성되는 경우는 세 가지다.
활성 컨텍스트의 용어에 매핑되는 키가 확장되는 경우, `@id`나 `@type`의 문자열 값인 경우, 그리고 `@type`이 `@id` 또는 `@vocab`으로 설정된 타입 강제(type coercion) 규칙이 걸린 키의 문자열 값인 경우다.

중요한 단서가 하나 있다.
IRI로 확장되지 않는 JSON 키는 Linked Data가 아니며, 처리 시 무시된다.
즉 컨텍스트에 정의되지 않은 필드는 그래프에 들어오지 않는다.

### `@type`: 노드와 값의 타입을 지정한다

`@type`은 노드의 타입을 지정한다.
Linked Data에서 타입은 IRI로 고유하게 식별된다.

```json
{
  "@context": "https://json-ld.org/contexts/person.jsonld",
  "@id": "http://example.com/people/markus",
  "@type": "http://schema.org/Person",
  "name": "Markus Lanthaler"
}
```

배열을 쓰면 하나의 노드에 둘 이상의 타입을 줄 수 있고, 활성 컨텍스트에 정의된 용어를 값으로 쓸 수도 있다.
`@type`은 노드뿐 아니라 값의 타입을 지정해 타입 있는 값(typed value)을 만드는 데도 쓰이는데, 값 객체는 타입을 하나만 가질 수 있다는 제약이 붙는다.

### 그 밖의 구조

JSON-LD 데이터 모델은 RDF 데이터 모델을 바탕으로 JSON보다 풍부한 리소스 집합을 다룬다.
명세는 JSON 객체가 쓰이는 형태를 이렇게 구분한다.

| 구조                      | 역할                                                         |
| ------------------------- | ------------------------------------------------------------ |
| 노드 객체(node object)    | 그래프의 노드를 정의한다. 속성을 갖는 리소스의 기본 구조다   |
| 값 객체(value object)     | 리터럴 노드를 서술한다. 확장형에서는 모든 리터럴이 값 객체다 |
| 리스트/집합 객체          | `@list`로 순서 있는 값을, `@set`으로 순서 없는 값을 표현한다 |
| 언어 맵(language map)     | 언어 태그로 여러 값을 색인한다                               |
| 인덱스 맵(index map)      | `@index`로 여러 값을 색인한다                                |
| 그래프 객체(graph object) | 이름 있는 그래프(named graph)를 정의한다                     |
| 컨텍스트 정의             | 그래프의 데이터가 아니라 용어 매핑 규칙이다                  |

여기서 눈여겨볼 것은 `@list`다.
RDF 그래프는 트리플의 집합이라 본래 순서가 없는데, API 응답에서 순서는 거의 항상 의미를 갖는다.
JSON-LD는 배열을 `@list` 아래 감싸는 방식으로 이 간극을 메운다.

## Hydra: RDF로 하이퍼미디어 어포던스를 서술한다

RDF는 데이터를 서술하는 데는 강하지만, 그 자체로는 읽기 전용이다.
“이 리소스에 무슨 요청을 보낼 수 있는가”는 RDF 어휘가 아니라 하이퍼미디어의 영역이다.
Hydra는 이 빈틈을 겨냥한 RDF 기반 하이퍼미디어 어휘다.

Hydra 명세의 초록은 이 어휘를 하이퍼미디어 주도 웹 API를 만들기 위한 경량 어휘로 규정하며, 웹 API에서 흔히 쓰이는 개념들을 명시함으로써 범용 API 클라이언트를 만들 수 있게 한다고 밝힌다.
서론은 목표를 더 분명히 한다.
Linked Data가 여전히 대체로 읽기 전용이라는 문제를 다루면서, 데이터에 상호작용을 가능하게 하는 기계 판독 가능한 어포던스를 덧입힌다는 것이다.

한 가지 전제를 명시해 둔다.
Hydra는 W3C Hydra Community Group이 펴낸 문서이며, 명세 자체가 밝히듯 W3C 표준도 아니고 표준화 트랙에 있지도 않다.

기본 발상은 서버가 유효한 상태 전이를 클라이언트에게 광고하게 하는 어휘를 제공하는 것이다.
상태 전이 정보가 설계 시점에 클라이언트에 하드코딩되는 대신 실행 시점에 기계 처리 가능한 형태로 교환되므로, 클라이언트가 서버로부터 분리되고 변화에 더 쉽게 적응할 수 있다.
네임스페이스는 `http://www.w3.org/ns/hydra/core#`이고 권장 접두사는 `hydra`다.

### Link 클래스: 어떤 속성이 역참조할 링크인가

Linked Data에서 링크 관계 타입은 속성 그 자체에 해당한다.

```json
{
  "urn:iana:link-relations:stylesheet": { "@id": "http://www.example.com/styles.css" }
}
```

문제는 RDF 직렬화에는 HTML의 `<a>`와 `<link>` 같은 구분이 없다는 것이다.
클라이언트가 할 수 있는 최선은 모든 URI를 무작정 역참조해 보는 것뿐이다.
Hydra의 `Link` 클래스는 어떤 속성이 역참조하도록 의도된 링크인지를 기계 판독 가능하게 서술한다.

```json
{
  "@context": "http://www.w3.org/ns/hydra/context.jsonld",
  "@id": "http://api.example.com/vocab#comments",
  "@type": "Link"
}
```

이렇게 정의해 두면, 아래 표현에서 `comments`의 값이 역참조 대상임을 Hydra를 이해하는 클라이언트가 알 수 있다.

```json
{
  "@context": {
    "comments": { "@id": "http://api.example.com/vocab#comments", "@type": "@id" }
  },
  "@id": "http://api.example.com/an-issue",
  "title": "An exemplary issue linking to its comments",
  "comments": "http://api.example.com/an-issue/comments"
}
```

컨텍스트에서 `@type`을 `@id`로 지정한 타입 강제 덕분에 값을 객체로 감싸지 않고 문자열로 쓸 수 있다.
JSON-LD의 기능이 그대로 관용적인 JSON 모양을 되찾아 준다.

### Operation: 읽기 전용을 넘어서

링크만으로는 읽기 전용 API밖에 만들지 못한다.
Hydra는 그래서 오퍼레이션(operation) 개념을 도입한다.
명세의 규정대로, `Operation`은 클라이언트가 서버의 리소스 상태를 조작하는 유효한 HTTP 요청을 구성하는 데 필요한 정보를 나타내며, 그래서 필수 속성은 HTTP `method` 하나다.
선택적으로 서버가 무엇을 기대(`expects`)하고 무엇을 반환(`returns`)하는지, 어떤 상태 코드가 나올 수 있는지를 서술할 수 있다.

명세는 이 정보가 완전한 것으로 간주돼서는 안 되며 어디까지나 힌트라고 명시한다.
개발자는 다른 상태 코드가 반환될 수 있음을 전제하고 클라이언트를 작성해야 한다.

### 주요 클래스와 발견 절차

Hydra 핵심 어휘의 클래스 일부를 정리하면 이렇다.

| 클래스                        | 역할                                            |
| ----------------------------- | ----------------------------------------------- |
| `hydra:ApiDocumentation`      | API 전체를 서술하는 문서                        |
| `hydra:Class`                 | API가 다루는 클래스의 지원 속성·오퍼레이션 서술 |
| `hydra:Collection`            | 멤버들을 담는 컬렉션                            |
| `hydra:PartialCollectionView` | 컬렉션의 부분 뷰(페이지네이션)                  |
| `hydra:Link`                  | 역참조 대상 링크임을 나타내는 속성 타입         |
| `hydra:Operation`             | 유효한 HTTP 요청 하나에 해당하는 어포던스       |
| `hydra:IriTemplate`           | 변수를 갖는 IRI 템플릿                          |
| `hydra:Error`, `hydra:Status` | 오류와 상태 코드 서술                           |
| `hydra:SupportedProperty`     | 클래스가 지원하는 속성과 읽기/쓰기 가능 여부    |

API 진입점 발견은 HTTP `Link` 헤더로 이루어진다.
클라이언트는 관계 타입 `http://www.w3.org/ns/hydra/core#apiDocumentation`을 가진 `Link` 헤더를 찾는다.

```http
HEAD / HTTP/1.1
Host: www.example.com

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Link: <http://api.example.com/doc/>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"
```

그 문서를 가져오면 API의 주 진입점을 얻는다.

```json
{
  "@context": "http://www.w3.org/ns/hydra/context.jsonld",
  "@id": "http://api.example.com/doc/",
  "title": "The example.com API",
  "entrypoint": "http://api.example.com/"
}
```

명세는 API 구현이 모든 응답에 이 `Link` 헤더를 실어 `ApiDocumentation`을 항상 발견 가능하게 만들어야 한다(SHOULD)고 권고한다.

## Linked Data 접근과 하이퍼미디어 접근의 관계

이 장을 이 책 전체 안에 놓고 보면 대비가 선명해진다.

10장까지의 하이퍼미디어 형식들 — Collection+JSON, Siren, HAL 등 — 은 문서 안에 링크와 폼을 넣는 방식으로 어포던스를 표현한다.
의미론은 미디어 타입 명세와 8장의 프로파일이 담당한다.

Linked Data는 반대편에서 출발한다.
모든 이름을 IRI로 만들어 의미론을 먼저 전역화하고, 그 위에 Hydra 같은 어휘로 어포던스를 얹는다.
저자가 Linked Data를 “시맨틱 웹 공동체의 REST 접근법”이라 부른 것이 이 대비를 정확히 짚는다.

두 접근이 배타적이지 않다는 점도 중요하다.
JSON-LD는 기존 JSON에 `@context` 한 줄을 더하거나 `Link` 헤더를 붙이는 것만으로 도입할 수 있으므로, 이미 하이퍼미디어 형식을 쓰는 API가 의미론 층위만 Linked Data로 보강하는 조합이 가능하다.

## 핵심 정리

RDF는 그래프 데이터 모델이며, 단위는 주어·술어·목적어의 트리플이다.
주어는 IRI 또는 blank node, 술어는 IRI, 목적어는 IRI·리터럴·blank node다.
그래프는 트리플의 집합이므로 서로 다른 출처의 데이터를 합집합으로 병합할 수 있고, 모든 이름이 IRI라 충돌하지 않으며 역참조하면 정의를 얻는다.

JSON-LD는 그 모델을 JSON 문법으로 직렬화한다.
`@context`가 용어를 IRI로 매핑하고, `@id`가 노드를 식별하며, `@type`이 노드와 값의 타입을 지정한다.
컨텍스트는 문서에 넣거나 URL로 참조하거나 HTTP `Link` 헤더로 외부에서 붙일 수 있어, 기존 JSON API가 문서를 고치지 않고도 Linked Data가 될 수 있다.
컨텍스트에서 IRI로 확장되지 않는 키는 Linked Data가 아니며 무시된다.

Hydra는 RDF에 빠져 있던 어포던스를 채우는 어휘다.
`Link` 클래스로 역참조 대상 속성을 표시하고, `Operation`으로 유효한 HTTP 요청을 서술하며, `ApiDocumentation`을 `Link` 헤더로 발견하게 한다.
다만 Hydra는 커뮤니티 그룹 문서이지 W3C 표준이 아니다.

이 장의 자리는 분명하다.
하이퍼미디어 형식이 “무엇을 할 수 있는가”를 문서 안에서 풀었다면, Linked Data는 “이 이름이 무엇을 뜻하는가”를 전역 식별자로 풀고 그 위에 어포던스를 다시 얹는다.
두 길은 같은 문제 — 클라이언트가 API를 사전 합의 없이 이해하게 만드는 문제 — 를 서로 다른 순서로 공략한다.
