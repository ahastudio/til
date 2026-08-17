# 7장 순수 하이퍼미디어 설계: HAL과 Siren으로 무엇이든 표현하기

《RESTful Web APIs》(Leonard Richardson, Mike Amundsen, O'Reilly 2013) 7장 정리.

## 개요

7장은 컬렉션 패턴이 요구사항에 맞지 않을 때 쓰는 전략 — 범용 하이퍼미디어 형식으로 원하는 표현을 전달하는 것 — 을 다루며, HTML·HAL·Siren 셋을 예로 든다.
이 정리는 저자의 공식 장별 설명과 해당 장이 다루는 공개 표준을 근거로 하며, 책 본문을 옮긴 것이 아니다.

저자가 공식 사이트에 올린 이 장의 설명은 다음과 같다.

```text
When the collection pattern doesn't fit your requirements, you can convey any
representation you want using a general-purpose hypermedia format. This chapter
shows how it works using three general hypermedia formats (HTML, HAL, and
Siren) as examples. This chapter also introduces HTML microformats and
microdata, which lead in to the next chapter.
```

앞의 두 장이 양극단을 보였다면 — 5장은 도메인마다 새 미디어 타입을 만드는 길, [6장](06-collection-pattern.md)은 이미 있는 컬렉션 패턴을 그대로 쓰는 길 — 7장은 그 사이를 다룬다.
형식은 범용인 채로 두고, 도메인 의미는 링크 관계와 이름으로 얹는 방식이다.

## 세 형식의 위치

세 형식은 같은 문제를 서로 다른 지점에서 푼다.

HTML은 이미 있는, 가장 널리 구현된 범용 하이퍼미디어 형식이다.
링크(`<a>`)와 폼(`<form>`)으로 읽기와 쓰기를 모두 표현할 수 있고, 브라우저라는 범용 클라이언트가 이미 존재한다.
문제는 도메인 의미가 없다는 것이며, 그 공백을 메우려는 시도가 마이크로포맷과 마이크로데이터다.

HAL은 JSON에 링크만 얹는 최소주의 선택이다.
Siren은 링크에 더해 쓰기 동작까지 표현한다.

## HAL: 링크 규약만 더한 최소 형식

HAL(Hypertext Application Language)은 Mike Kelly가 2011년에 만들었고 미디어 타입은 `application/hal+json`과 `application/hal+xml`이다.
명세는 자기 위치를 분명히 한다 — HAL은 JSON이나 XML에서 하이퍼링크를 표현하는 규약의 집합이고, 문서의 나머지는 그냥 평범한 JSON 또는 XML이다.

명세가 HAL을 “기계를 위한 HTML 비슷한 것”이라 설명하는 대목이 이 형식의 자기 인식을 잘 보여준다 — HTML이 사람 행위자가 웹 애플리케이션을 통과하도록 돕는 기능을 가진 반면, HAL은 자동 행위자가 웹 API를 통과해 목표를 이루도록 돕는 것을 의도한다는 것이다.

HAL의 모델은 두 개념뿐이다.
리소스는 링크, 삽입된 리소스, 상태(평범한 JSON 데이터)를 가진다.
링크는 대상 URI, 관계(rel), 그리고 폐기 표시나 콘텐츠 협상을 돕는 몇몇 선택 속성을 가진다.

### `_links`

링크는 리소스 객체의 직접 속성인 `_links` 해시 안에 담긴다.
rel은 그 해시의 키가 되고, 값이 `href` 등을 담은 링크 객체다.

```json
{
  "_links": {
    "self": { "href": "/orders" },
    "next": { "href": "/orders?page=2" },
    "ea:find": { "href": "/orders{?id}", "templated": true }
  }
}
```

같은 rel에 링크가 여럿일 수 있으면 배열을 쓴다.
명세는 단수인지 복수인지 확신이 없으면 복수로 가정하라고 권한다 — 단수로 골랐다가 바꿔야 하면 새 링크 관계를 만들거나 기존 클라이언트를 깨야 하기 때문이다.

유효한 최소 HAL 문서는 빈 리소스, 즉 `{}` 하나다.
대부분의 경우 리소스는 `self` 링크로 자기 URI를 가져야 한다.

### CURIE: 문서를 발견 가능하게 만드는 장치

HAL에서 링크 관계는 단순한 식별 문자열이 아니라 URL이어야 하며, 개발자가 그것을 따라가 해당 링크의 문서를 읽을 수 있어야 한다.
이것이 명세가 말하는 발견 가능성(discoverability)이며, 개발자가 API에 들어가 링크 문서를 읽고 코를 따라가듯 탐색한다는 발상이다.

그런데 URL은 키로 쓰기에 길고 불편하다.
그래서 HAL은 `curies`라는 예약 링크 관계를 둔다.

```json
{
  "_links": {
    "curies": [
      {
        "name": "doc",
        "href": "http://haltalk.herokuapp.com/docs/{rel}",
        "templated": true
      }
    ],
    "doc:latest-posts": { "href": "/posts/latest" }
  }
}
```

`curies` 항목은 `name`과 `{rel}` 자리표시자를 포함한 템플릿 `href`를 가진다.
클라이언트가 `doc:latest-posts`의 문서를 원하면 CURIE를 확장해 `http://haltalk.herokuapp.com/docs/latest-posts`를 얻는다.

### `_embedded`

다른 리소스를 문서 안에 삽입할 때는 `_embedded`를 쓴다.
삽입된 리소스도 자기 `_links`와 상태를 가진 완전한 리소스다.

```json
{
  "_links": {
    "self": { "href": "/orders" },
    "curies": [{ "name": "ea", "href": "http://example.com/docs/rels/{rel}", "templated": true }]
  },
  "currentlyProcessing": 14,
  "shippedToday": 20,
  "_embedded": {
    "ea:order": [{
      "_links": {
        "self": { "href": "/orders/123" },
        "ea:basket": { "href": "/baskets/98712" },
        "ea:customer": { "href": "/customers/7809" }
      },
      "total": 30.00,
      "currency": "USD",
      "status": "shipped"
    }]
  }
}
```

`currentlyProcessing`과 `shippedToday`처럼 밑줄 없는 키는 그냥 리소스의 상태다.
HAL이 규정하는 것은 `_links`와 `_embedded` 둘뿐이고 나머지 이름 공간은 온전히 애플리케이션의 것이다.

명세 자신이 “비교적 비형식적이고 미완성이며 진행 중”이라고 밝히며, 완전한 이해를 위해서는 인터넷 드래프트 `draft-kelly-json-hal`을 보라고 안내한다.

## Siren: 링크에 더해 동작까지 표현

Siren은 Kevin Swiber가 만든, 엔티티(entity)를 표현하기 위한 하이퍼미디어 명세다.
미디어 타입은 `application/vnd.siren+json`이다.
명세는 자기 목표를 이렇게 규정한다 — HTML이 웹사이트에서 문서를 시각적으로 표현하는 데 쓰이듯, Siren은 웹 API를 통해 엔티티를 제시하기 위한 명세이며, 엔티티에 관한 정보를 전달하는 구조, 상태 전이를 실행하는 동작(actions), 클라이언트 탐색을 위한 링크를 제공한다.

엔티티는 프로퍼티와 동작을 가진 URI 주소지정 가능 리소스이고, 하위 엔티티와 탐색 링크를 담을 수 있다.

### 엔티티의 다섯 속성

- `class` — 현재 표현에 근거한 엔티티 내용의 성격을 서술한다. 문자열 배열이어야 하며 가능한 값은 구현에 달렸고 문서화돼야 한다. 선택.
- `properties` — 엔티티의 상태를 서술하는 키·값 쌍의 집합. JSON Siren에서는 객체다. 선택.
- `entities` — 관련된 하위 엔티티들의 모음. 배열. 선택.
- `links` — 엔티티 관계와 구별되는, 탐색 링크들의 모음. 선택.
- `actions` — 동작 객체들의 배열. 선택.
- `title` — 엔티티에 대한 서술 텍스트. 선택.

루트 엔티티와 삽입 표현인 하위 엔티티는 `rel` 값이 `self`이고 `href`가 엔티티 URI인 항목을 최소 하나 담은 `links` 모음을 가져야 한다(SHOULD).

### 하위 엔티티: 링크인가 표현인가

`entities` 배열의 원소는 두 가지 형태를 취한다.
`href` 값을 가지면 삽입 링크(embedded link)로 다루며, 클라이언트가 낙관적으로 미리 불러올 수 있다.
`href`가 없으면 삽입 표현(embedded representation)이고, 보통 엔티티의 모든 특성을 가진다.
차이는 하나 — 하위 엔티티는 부모와의 관계를 서술하는 `rel` 속성을 반드시 가져야 한다.

명세는 두 가지 구별을 따로 강조한다.
링크 관계는 두 리소스 사이의 관계를 정의하고, 클래스는 요소(엔티티든 동작이든)의 성격을 현재 표현에서 분류한다.
그리고 하위 엔티티는 맥락 안에서 엔티티들 사이의 관계를 전달하기 위해 존재하는 반면, 링크는 주로 탐색을 위한 것이고 클라이언트가 엔티티 그래프 바깥으로 나가는 길을 알려 준다.

### actions: 쓰기를 표현 안에 담는다

Siren이 HAL과 갈라지는 지점이 `actions`다.
동작은 엔티티가 노출하는 가용한 행위를 보인다.

- `name` — 수행할 동작을 식별하는 문자열. 한 엔티티의 동작 집합 안에서 유일해야 한다. 필수.
- `href` — 동작의 URI. 필수.
- `method` — 프로토콜 메서드. HTTP에서는 `GET`, `PUT`, `POST`, `DELETE`, `PATCH` 등. 생략하면 `GET`으로 가정한다. 선택.
- `type` — 요청의 인코딩 타입. 생략됐고 `fields`가 있으면 기본값은 `application/x-www-form-urlencoded`. 선택.
- `fields` — 필드 객체들의 배열. 선택.
- `class`, `title` — 선택.

필드는 동작 안의 컨트롤이다.
`name`은 필수이고 한 동작의 필드 집합 안에서 유일해야 하며, `type`은 HTML5의 입력 타입(`hidden`, `text`, `number`, `date`, `checkbox` 등)을 쓸 수 있고 생략하면 `text`가 기본이다.
`value`와 `title`도 선택으로 둘 수 있으며, `title`은 클라이언트가 레이블로 쓸 수 있다.

명세의 주문 예제가 이 구조를 한눈에 보인다.

```json
{
  "class": [ "order" ],
  "properties": {
    "orderNumber": 42,
    "itemCount": 3,
    "status": "pending"
  },
  "entities": [
    {
      "class": [ "items", "collection" ],
      "rel": [ "http://x.io/rels/order-items" ],
      "href": "http://api.x.io/orders/42/items"
    },
    {
      "class": [ "info", "customer" ],
      "rel": [ "http://x.io/rels/customer" ],
      "properties": { "customerId": "pj123", "name": "Peter Joseph" },
      "links": [
        { "rel": [ "self" ], "href": "http://api.x.io/customers/pj123" }
      ]
    }
  ],
  "actions": [
    {
      "name": "add-item",
      "title": "Add Item",
      "method": "POST",
      "href": "http://api.x.io/orders/42/items",
      "type": "application/x-www-form-urlencoded",
      "fields": [
        { "name": "orderNumber", "type": "hidden", "value": "42" },
        { "name": "productCode", "type": "text" },
        { "name": "quantity", "type": "number" }
      ]
    }
  ],
  "links": [
    { "rel": [ "self" ], "href": "http://api.x.io/orders/42" },
    { "rel": [ "previous" ], "href": "http://api.x.io/orders/41" },
    { "rel": [ "next" ], "href": "http://api.x.io/orders/43" }
  ]
}
```

첫 하위 엔티티는 `href`만 있으므로 삽입 링크이고, 둘째는 `properties`를 가진 삽입 표현이다.
`add-item` 동작은 HTML 폼과 정확히 같은 정보 — 메서드, 대상 URL, 인코딩, 필드 목록과 각 필드의 타입 — 를 JSON으로 전달한다.

명세는 사용 고려 사항에서 이 설계 의도를 밝힌다 — Siren은 주로 CRUD 기반일 필요가 없는 리소스 설계 스타일을 지원하며, 루트 엔티티가 동작을 통해 하위 엔티티의 변경을 주관할 수 있고, 이를 통해 과업 기반(task-based) 인터페이스를 웹 API로 쉽게 제공할 수 있다.

## 두 형식의 비교

| 항목        | HAL                                | Siren                                     |
| ----------- | ---------------------------------- | ----------------------------------------- |
| 미디어 타입 | `application/hal+json`             | `application/vnd.siren+json`              |
| 상태        | 문서 최상위의 평범한 JSON 키       | `properties` 객체 안                      |
| 링크        | `_links` 해시, rel이 키            | `links` 배열, `rel`이 문자열 배열         |
| 삽입 리소스 | `_embedded` 해시                   | `entities` 배열(링크형/표현형 둘 다)      |
| 쓰기 서술   | 없음                               | `actions` 배열(`method`·`href`·`fields`)  |
| 분류        | 없음                               | `class` 배열                              |
| 문서 발견   | CURIE로 rel을 문서 URL로 확장      | rel URI, `class` 값의 문서화              |

핵심 차이는 두 가지다.

첫째, 쓰기다.
HAL 문서를 받은 클라이언트는 어떤 URL이 있는지는 알지만 그 URL에 무엇을 어떤 방법으로 보내야 하는지는 알 수 없다 — 그것은 링크 관계 문서를 사람이 읽고 코드에 반영해야 한다.
Siren은 `actions`로 메서드·인코딩·필드까지 표현에 실어 보내므로, 클라이언트가 응답만 보고 쓰기 요청을 조립할 수 있다.
이 점에서 Siren의 `actions`는 [6장](06-collection-pattern.md)에서 본 Collection+JSON의 `template`과 같은 문제를 더 일반적으로 푼 것이다 — 필드 하나짜리 고정 템플릿이 아니라, 이름과 메서드와 대상이 다른 동작을 여럿 실을 수 있다.

둘째, 상태와 링크의 분리다.
HAL은 상태를 문서 최상위에 두고 링크만 `_links`로 격리하는 반면, Siren은 `properties`·`links`·`entities`·`actions`를 모두 나란한 최상위 키로 둔다.
HAL 문서는 기존 JSON API에 `_links`만 얹으면 되므로 이행 비용이 거의 없고, Siren은 문서 전체를 다시 설계해야 한다.

이 대비가 두 형식의 채택 차이를 상당 부분 설명한다.
HAL은 값싸고 읽기 중심 API에 딱 맞았고, Siren은 표현력이 크지만 그만큼 요구가 컸다.
이 저장소의 [whats-new 문서](whats-new.md)에 정리한 대로, 실무는 결국 어느 쪽으로도 크게 가지 않고 하이퍼미디어 없는 컬렉션 패턴 JSON에 머물렀다.

## HTML 마이크로포맷과 마이크로데이터

같은 장이 HTML을 범용 하이퍼미디어 형식으로 다루면서 마이크로포맷과 마이크로데이터를 함께 소개하는 이유는, 둘이 다음 장(프로파일)으로 이어지는 다리이기 때문이다.
HTML은 링크와 폼으로 “다음에 무엇을 할 수 있는가”는 잘 전달하지만, “이 문단이 사람 이름이고 저 문단이 주소다”라는 도메인 의미는 전달하지 못한다.
마이크로포맷과 마이크로데이터는 그 의미를 기존 HTML 속성에 얹는 두 가지 방식이다.

마이크로포맷은 `class`와 `rel` 속성에 합의된 값을 넣는 방식이다.
새 문법을 만들지 않고 이미 있는 속성을 재사용하므로 어떤 HTML 파서로도 읽을 수 있다.

```html
<div class="vcard">
  <span class="fn">Peter Joseph</span>
  <a class="url" href="http://example.org/pj">홈페이지</a>
</div>
```

마이크로데이터는 HTML 표준이 정의한 별도 속성 집합을 쓴다.
`itemscope`가 항목의 범위를 열고, `itemtype`이 어휘를 가리키는 URL을 주며, `itemprop`이 각 프로퍼티의 이름을 지정한다.

```html
<div itemscope itemtype="http://schema.org/Person">
  <span itemprop="name">Peter Joseph</span>
  <a itemprop="url" href="http://example.org/pj">홈페이지</a>
</div>
```

둘의 공통점이 8장으로 이어지는 지점이다.
어느 쪽도 새 미디어 타입을 만들지 않는다 — 형식은 여전히 `text/html`이고, 그 위에 “이 문서의 이 부분이 무엇을 뜻하는가”라는 어휘 층을 얹을 뿐이다.
이것이 정확히 프로파일의 발상이다 — 여러 API가 공유하는 데이터 형식과 특정 API 구현 사이의 틈을 형식 교체 없이 메우는 것.
저자가 8장에서 ALPS를 도입하며 XMDP와 JSON-LD를 함께 다루는 배경이 여기에 있다.

## 핵심 정리

컬렉션 패턴이 맞지 않는 API도 새 미디어 타입을 만들 필요는 없다.
범용 하이퍼미디어 형식을 쓰면 형식은 도메인 중립인 채로 두고 도메인 의미를 링크 관계와 이름으로 얹을 수 있다.

HAL은 최소주의 선택이다.
규정하는 것은 `_links`와 `_embedded` 둘뿐이고 나머지는 평범한 JSON이며, 링크 관계를 URL로 두고 CURIE로 줄여 쓰게 해 API 문서를 표현 자체에서 발견하게 한다.
기존 JSON API에 얹기 쉬운 대신, 쓰기 요청을 어떻게 조립할지는 알려 주지 않는다.

Siren은 `class`·`properties`·`entities`·`links`·`actions`의 다섯 축으로 엔티티를 표현한다.
`actions`가 메서드·URI·인코딩·필드까지 담으므로 클라이언트가 응답만 보고 쓰기를 수행할 수 있고, 이 덕분에 CRUD가 아닌 과업 기반 인터페이스를 표현할 수 있다.
Collection+JSON의 `template`이 컬렉션 패턴 안에서 푼 문제를, Siren은 임의의 도메인으로 일반화해 푼다.

HTML은 이미 링크와 폼을 가진 범용 형식이지만 도메인 의미가 없고, 마이크로포맷(`class`/`rel` 재사용)과 마이크로데이터(`itemscope`/`itemtype`/`itemprop`)가 그 의미 층을 형식 교체 없이 얹는 두 방식이다.
새 미디어 타입 없이 의미를 공급한다는 이 발상이 그대로 8장 프로파일의 문제의식으로 이어진다.

## 참고

- 관련 문서: [RESTful Web APIs 정리 (색인)](README.md), [6장 컬렉션 패턴](06-collection-pattern.md), [RESTful Web APIs 예제 코드](example-code.md), [RESTful Web Services에서 RESTful Web APIs로](whats-new.md)
- HAL 명세: <https://stateless.co/hal_specification.html>
- Siren 명세: <https://github.com/kevinswiber/siren>
- 저자 공식 장별 설명: <http://restfulwebapis.com/chapters.html>
