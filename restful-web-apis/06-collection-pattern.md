# 6장 컬렉션 패턴: API 설계에서 반복되는 하나의 모양

《RESTful Web APIs》(Leonard Richardson, Mike Amundsen, O'Reilly 2013) 6장 정리.

## 개요

6장은 API 설계에서 거듭 나타나는 하나의 패턴 — 컬렉션 패턴 — 을 이름 붙여 정의하고, 그것을 명시적으로 담아낸 두 표준 Collection+JSON과 AtomPub을 보인다.
이 정리는 저자의 공식 장별 설명과 해당 장이 다루는 공개 표준을 근거로 하며, 책 본문을 옮긴 것이 아니다.

저자가 공식 사이트에 올린 이 장의 설명은 다음과 같다.

```text
One pattern in particular - the collection pattern - shows up over and over
again in API design. In this chapter, I show off two different standards that
capture this pattern: Collection+JSON and AtomPub.
```

앞 장(5장)이 자기 문제에 정확히 맞는 새 미디어 타입을 처음부터 설계하는 전략(Maze+XML)을 보였다면, 6장은 정반대 방향을 다룬다.
대부분의 API는 새 표준을 만들 필요가 없다 — 이미 있는 패턴 하나로 충분하기 때문이다.

## 컬렉션 패턴의 구조

컬렉션 패턴은 리소스를 두 종류로 나눈다.

아이템(item)은 하나의 레코드에 대응하는 리소스다.
자기 URI를 가지며, GET으로 읽고 PUT으로 통째로 교체하고 DELETE로 지운다.

컬렉션(collection)은 아이템들을 담는 리소스다.
GET으로 목록을 읽고, POST로 새 아이템을 추가한다.

여기서 메서드 배분이 핵심이다.
새 아이템을 만드는 일은 아이템 URI가 아직 없으므로 컬렉션에 POST해야 하고, 서버가 URI를 정해 `Location` 헤더로 알려 준다.
반면 이미 URI가 있는 아이템은 PUT과 DELETE로 다룬다 — PUT은 클라이언트가 URI를 아는 리소스를 교체하는 것이지 생성하는 것이 아니다.

```http
GET    /collection/      -> 목록
POST   /collection/      -> 새 아이템 생성, 201 Created + Location
GET    /collection/1     -> 아이템 읽기
PUT    /collection/1     -> 아이템 통째로 교체
DELETE /collection/1     -> 아이템 삭제
```

이 배분이 이른바 CRUD API의 뼈대이며, 저자가 REST API의 상당수를 이 패턴이 덮는다고 본 이유다.
이 저장소의 [whats-new 문서](whats-new.md)에 정리한 대로, 저자는 이른바 REST API의 약 80%가 이 패턴에 포섭되지만 REST는 그보다 크다고 봤다.
패턴에 이름을 주는 행위 자체가 그 너머를 보게 한다는 것이 이 장의 방법론적 주장이다.

## Collection+JSON: 패턴을 통째로 형식으로 만든 것

Collection+JSON은 Mike Amundsen이 2011년에 만든 읽기·쓰기 하이퍼미디어 타입이다.
미디어 타입은 `application/vnd.collection+json`이고, 명세는 스스로를 “단순한 목록(연락처, 할 일, 블로그 글 등)에 대한 완전한 읽기·쓰기 능력을 지원하도록 설계됐다”고 규정한다.
지원하는 애플리케이션 의미론은 CRUD와 질의 템플릿이며, 여기서 갱신(Update)은 부분 수정이 아니라 통째 교체를 뜻한다.

문서의 최상위에는 `collection` 객체 하나만 온다.

```json
{
  "collection": {
    "version": "1.0",
    "href": "http://example.org/my-collection/",
    "links": [],
    "items": [],
    "queries": [],
    "template": {},
    "error": {}
  }
}
```

`version`은 이 릴리스에서 `1.0`이어야 하고, `href`는 이 문서를 가져오는 데 쓰인 주소를 담으며 새 레코드를 추가하는 데 쓰일 수도 있다.
나머지 다섯은 모두 선택 사항이다.

### items와 data: 데이터에 이름을 붙이는 방식

`items` 배열의 각 원소는 `href`(그 아이템의 URI), `data` 배열, `links` 배열을 가진다.
`data` 배열의 각 원소는 `name`(필수), `value`(선택), `prompt`(선택)로 이루어진다.

```json
{
  "href": "http://example.org/my-collection/1",
  "data": [
    {"name": "first-name", "value": "Bob", "prompt": "First Name"},
    {"name": "email", "value": "bob@example.org", "prompt": "Email"}
  ],
  "links": [
    {"rel": "avatar", "href": "http://example.org/img/1.png", "render": "image"}
  ]
}
```

이 구조가 특이한 점은 도메인 데이터를 JSON 객체의 키로 두지 않고 `name`/`value` 쌍의 배열로 평평하게 편다는 것이다.
그 대가로 형식 자체는 어떤 도메인에도 중립이 되고, 도메인 의미는 `name` 값에만 실린다.
`links` 배열 원소는 `href`와 `rel`이 필수이며, `render`는 `image` 또는 `link`만 허용하고 생략하면 `link`로 간주된다.

### template: 쓰기 양식을 표현에 실어 보낸다

Collection+JSON에서 쓰기 연산은 서버가 응답 표현 안에 실어 보낸 `template` 객체로 정의된다.
`template`은 `data` 배열 하나를 자식으로 가지며, 문서당 하나만 올 수 있다.

```json
{
  "template": {
    "data": [
      {"prompt": "Text of message", "name": "text", "value": ""}
    ]
  }
}
```

클라이언트는 이 템플릿을 그대로 복사해 `value`를 채운 뒤 컬렉션 URI로 POST한다.
명세가 규정하는 흐름은 다음과 같다.

```http
POST /my-collection/ HTTP/1.1
Host: www.example.org
Content-Type: application/vnd.collection+json

{ "template" : { "data" : [ ... ] } }

201 Created HTTP/1.1
Location: http://www.example.org/my-collection/1
```

교체할 때도 같은 템플릿을 채워 아이템 URI로 PUT하고 성공 시 200을 받으며, 삭제는 DELETE에 204를 돌려주기를 권한다.
아이템 하나를 GET한 응답조차 아이템 하나만 담긴 완전한 `collection` 문서라는 점이 명세에 명시돼 있다 — 형식이 아이템 표현을 따로 두지 않는다.

이것이 이 형식의 하이퍼미디어적 핵심이다.
클라이언트는 “이 API에 무엇을 어떤 이름으로 보내야 하는가”를 문서에서 미리 읽고 하드코딩할 필요 없이, 방금 받은 응답에서 읽는다.
이 저장소의 [예제 코드 문서](example-code.md)에 정리한 You Type It, We Post It 서버가 정확히 이 구조를 보인다 — 서버 템플릿이 `text`라는 이름의 필드 하나를 실은 `template` 객체를 모든 응답에 함께 내고, 테스트 클라이언트는 그 모양대로 POST와 PUT을 보낸다.
같은 문서에서 본 대로 그 서버의 API 라우팅은 `/api/`가 GET·POST를, `/api/{id}`가 GET·PUT·DELETE를 받는 형태이며, 컬렉션 패턴의 메서드 배분이 코드로 그대로 나타난다.

### queries: 질의도 표현 안에서 알려 준다

`queries` 배열은 클라이언트가 실행할 수 있는 질의 템플릿을 담는다.
각 원소는 `href`와 `rel`이 필수이고 `data` 배열을 가질 수 있다.

```json
{
  "queries": [
    {
      "href": "http://example.org/search",
      "rel": "search",
      "prompt": "Enter search string",
      "data": [
        {"name": "search", "value": ""}
      ]
    }
  ]
}
```

클라이언트는 `data`의 이름·값 쌍을 `href` 뒤에 물음표로 이어 붙여 URI를 만든다 — 위 예에서 값이 `JSON`이면 `http://example.org/search?search=JSON`이 된다.
HTML의 GET 폼과 같은 일을 JSON으로 하는 셈이다.

### 링크 관계와 확장

명세가 직접 정의하는 링크 관계는 넷뿐이다 — `collection`, `item`, `template`, `queries`.
나머지는 구현자가 자유롭게 쓰되 IANA 링크 관계 레지스트리나 마이크로포맷의 기존 rel 값처럼 이미 정의된 것을 쓰기를 권하고, 필요하면 RFC 5988의 방식으로 고유한 값을 만들라고 안내한다.
오류는 `error` 객체 하나로 표현하며 `title`, `code`, `message`를 가질 수 있다.

## AtomPub: 컬렉션 패턴을 개척한 프로토콜

AtomPub(Atom Publishing Protocol, RFC 5023, 2007)은 컬렉션 패턴을 개척한 표준이다.
Atom 형식의 표현을 HTTP로 주고받아 웹 리소스를 발행하고 편집하는 애플리케이션 수준 프로토콜이며, 컬렉션·서비스·편집의 세 가지를 제공한다.

RFC 5023이 정의하는 메서드 배분은 컬렉션 패턴의 원형 그대로다.

- GET은 알려진 리소스의 표현을 가져온다.
- POST는 새로운, 서버가 이름을 정하는 리소스를 만든다.
- PUT은 알려진 리소스를 편집하며, 리소스 생성에는 쓰지 않는다.
- DELETE는 알려진 리소스를 제거한다.

컬렉션에 나열된 IRI를 가진 리소스를 멤버 리소스(Member Resource)라 부르고, 이는 다시 Atom 엔트리 문서로 표현되는 엔트리 리소스와 임의의 미디어 타입을 가질 수 있는 미디어 리소스로 나뉜다.
미디어 리소스는 컬렉션 안에서 미디어 링크 엔트리(Media Link Entry)라는 엔트리로 서술된다.
컬렉션 자체는 Atom 피드 문서로 표현되며, 피드의 엔트리들이 멤버 리소스의 IRI와 메타데이터를 담는다.

생성 흐름은 Collection+JSON과 같은 모양이다 — 컬렉션 URI로 멤버 표현을 POST하면 성공 시 201과 새 엔트리 리소스의 IRI를 담은 `Location` 헤더가 돌아온다.
편집은 멤버 URI로 PUT해 200을, 삭제는 DELETE해 200을 받는다.

### 서비스 문서: 컬렉션 자체를 발견하게 한다

AtomPub이 Collection+JSON보다 한 겹 더 두는 것이 서비스 문서다.
클라이언트가 편집을 시작하려면 어떤 컬렉션이 어디에 있고 무엇을 받는지 먼저 알아야 하며, 서비스 문서가 그 발견을 담당한다.

```xml
<?xml version="1.0" encoding='utf-8'?>
<service xmlns="http://www.w3.org/2007/app"
         xmlns:atom="http://www.w3.org/2005/Atom">
  <workspace>
    <atom:title>Main Site</atom:title>
    <collection href="http://example.org/blog/main">
      <atom:title>My Blog Entries</atom:title>
      <categories href="http://example.com/cats/forMain.cats" />
    </collection>
    <collection href="http://example.org/blog/pic">
      <atom:title>Pictures</atom:title>
      <accept>image/png</accept>
      <accept>image/jpeg</accept>
    </collection>
  </workspace>
</service>
```

서비스 문서는 컬렉션들을 워크스페이스(Workspace)로 묶는다.
워크스페이스는 이름은 있지만 IRI도 없고 명세가 부여하는 처리 의미도 없는, 순수한 묶음일 뿐이다.
`accept` 요소는 그 컬렉션이 받는 미디어 타입을, `categories`는 허용되는 분류를 알려 준다.
서비스 문서는 `application/atomsvc+xml`, 카테고리 문서는 `application/atomcat+xml`로 식별된다.

흥미로운 점은 명세가 피드를 컬렉션 피드로 표시하는 유일한 수단으로 “그 피드의 IRI가 서비스 문서에 등장하는 것”만을 든다는 것이다.
컬렉션임을 형식이 아니라 발견 경로가 정한다.

### 서버에 넓은 재량을 주는 설계

RFC 5023이 명시적으로 밝히는 특징 하나는 서버에 클라이언트 요청 처리에 대한 넓은 재량을 준다는 것이다.
명세는 서버가 제출된 콘텐츠를 받아들이거나, 거절하거나, 지연하거나, 검열하거나, 재포맷하거나, 번역하거나, 옮기거나, 다시 분류하기를 선택할 수 있다고 적는다.
그중 일부만 즉시 응답으로 클라이언트에 전달되고 나머지는 나중에 피드나 발행된 엔트리에서 드러난다.

그 결과 명세는 클라이언트 소프트웨어가 “서버가 결정한 결과를 받아들이도록” 유연하게 작성돼야 한다고 요구한다.
같은 요청 순서를 두 발행 사이트에 보내면 서로 다른 응답, 서로 다른 피드, 서로 다른 엔트리 내용이 나올 수 있다는 것이다.
명세가 컬렉션에 대해 GET과 POST의 동작만 정의한다고 해서 PUT·DELETE가 금지된다는 뜻은 아니며, 단지 그 응답을 명세가 규정하지 않을 뿐이라는 단서도 붙는다.

## 두 표준의 비교

같은 패턴을 담지만 강조점이 다르다.

| 항목        | Collection+JSON                    | AtomPub                              |
| ----------- | ---------------------------------- | ------------------------------------ |
| 미디어 타입 | `application/vnd.collection+json`  | Atom 피드·엔트리 + `atomsvc`/`atomcat` |
| 직렬화      | JSON                               | XML                                  |
| 컬렉션 표현 | `collection` 객체의 `items` 배열   | Atom 피드 문서의 엔트리들            |
| 쓰기 서술   | `template` 객체(응답에 동봉)       | 프로토콜 명세로 규정                 |
| 질의 서술   | `queries` 배열                     | 명세 범위 밖                         |
| 발견        | 문서의 `href`와 링크 관계          | 서비스 문서 + 워크스페이스           |
| 생성 응답   | 201 + `Location`                   | 201 + `Location`                     |
| 삭제 응답   | 204 권장                           | 200                                  |

가장 큰 차이는 쓰기 양식을 어디에 두는가다.
AtomPub은 무엇을 어떻게 보낼지를 프로토콜 명세와 서비스 문서의 `accept`로 알려 주고, Collection+JSON은 그것을 매 응답의 `template` 객체에 함께 실어 보낸다.
후자가 더 하이퍼미디어에 가깝다 — 클라이언트가 명세를 구현하는 대신 응답을 읽으면 되기 때문이다.

## 핵심 정리

컬렉션 패턴은 리소스를 아이템과 컬렉션 둘로 나누고, 아이템에는 GET·PUT·DELETE를, 컬렉션에는 GET과 POST를 배분한다.
새 리소스를 만드는 일이 컬렉션의 POST로 가는 이유는 아직 URI가 없기 때문이고, 서버가 URI를 정해 `Location`으로 돌려준다.

Collection+JSON은 이 패턴을 통째로 JSON 형식으로 만든 것이다.
`collection` 객체 하나 아래 `items`, `links`, `queries`, `template`, `error`를 두며, 도메인 데이터는 `name`/`value`/`prompt` 삼중항의 평평한 배열로 표현해 형식 자체를 도메인 중립으로 유지한다.
쓰기는 서버가 응답에 실어 보낸 `template`을 클라이언트가 채워 보내는 방식으로 정의된다.

AtomPub은 이 패턴을 개척한 2007년 표준이며, 서비스 문서로 컬렉션 자체를 발견하게 하는 층을 하나 더 둔다.
동시에 서버에 넓은 재량을 명시적으로 허용해, 클라이언트가 서버의 결정을 받아들이도록 유연하게 작성되기를 요구한다.

두 표준의 진짜 교훈은 개별 형식이 아니라 패턴에 이름을 준 것이다.
컬렉션 패턴이 이름 없이 대부분의 API를 덮고 있을 때는 그것이 REST 자체로 보이지만, 이름을 얻는 순간 하나의 선택지가 되고 그것이 맞지 않는 경우를 물을 수 있게 된다.
그 물음의 답이 다음 장의 순수 하이퍼미디어 설계다.

## 참고

- 관련 문서: [RESTful Web APIs 정리 (색인)](README.md), [7장 순수 하이퍼미디어 설계](07-pure-hypermedia-designs.md), [RESTful Web APIs 예제 코드](example-code.md), [RESTful Web Services에서 RESTful Web APIs로](whats-new.md)
- Collection+JSON 명세: <https://github.com/collection-json/spec>
- RFC 5023 (The Atom Publishing Protocol): <https://www.rfc-editor.org/rfc/rfc5023.txt>
- 저자 공식 장별 설명: <http://restfulwebapis.com/chapters.html>
