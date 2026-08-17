# 10장 하이퍼미디어 동물원: 스무 가지 표준 형식의 지형도

《RESTful Web APIs》(Leonard Richardson, Mike Amundsen, O'Reilly 2013) 10장 정리.

## 개요

저자의 공식 설명은 이 장의 성격을 이렇게 밝힌다.
“하이퍼미디어가 무엇을 할 수 있는지 보이려는 시도로, 이 장은 약 20종의 표준화된 하이퍼미디어 데이터 형식을 논한다. 대부분은 책의 다른 곳에서 다루지 않은 것들이다.”
“동물원(zoo)”이라는 제목은 이 장이 각 형식을 깊이 파는 곳이 아니라 종의 다양성을 보여 주는 전시장임을 드러낸다.

이 정리는 저자의 공식 장별 설명과 해당 장이 다루는 공개 표준을 근거로 하며, 책 본문을 옮긴 것이 아니다.

그래서 아래는 “10장의 목차”가 아니다.
책이 정확히 어떤 형식을 어떤 순서로 다뤘는지는 본문 없이 알 수 없으므로, 여기서는 저자가 다른 장에서 다룬다고 밝힌 형식들과 하이퍼미디어 논의에서 표준으로 인정되는 형식들을 각 명세에 근거해 정리하고, 그것들이 어떤 축으로 갈라지는지를 지도로 그린다.
저자가 말한 “약 20종”이라는 규모만 인용하고, 형식의 개수를 단정하지 않는다.

## 동물원을 가르는 축

형식들을 나란히 늘어놓기만 하면 지형이 보이지 않는다.
실제 명세를 놓고 보면 세 개의 축이 이 동물원을 가른다.

첫째 축은 도메인 특화인가 범용인가다.
Maze+XML처럼 하나의 문제 영역만을 위해 설계된 형식이 있고, HTML이나 HAL처럼 어떤 도메인에도 쓸 수 있는 형식이 있다.
[8장](08-profiles.md)의 프로파일은 정확히 이 축의 긴장에서 태어났다 — 범용 형식을 쓰면서 도메인 의미를 잃지 않으려는 시도다.

둘째 축은 어떤 종류의 하이퍼미디어 컨트롤을 지원하는가다.
링크만 있는 형식과 폼까지 있는 형식은 클라이언트에게 허용하는 일의 범위가 다르다.
링크만 있으면 클라이언트는 서버가 정해 준 URL로 GET밖에 못 하지만, 폼이 있으면 클라이언트가 데이터를 구성해 안전하지 않은 전이까지 수행할 수 있다.

셋째 축은 완결된 표현 형식인가 다른 형식에 얹히는 조각인가다.
`Link` 헤더나 마이크로포맷은 그 자체로 문서 형식이 아니라 다른 표현에 하이퍼미디어를 덧붙이는 장치다.

## 도메인 특화 형식들

### Maze+XML

이 책 자신의 예제 형식이며 미디어 타입은 `application/vnd.amundsen.maze+xml`이다.
5장의 도메인 특화 설계를 보이기 위해 Mike Amundsen이 만들었고, 이 저장소의 [example-code.md](example-code.md)에 서버와 세 클라이언트의 구현이 정리돼 있다.

미로라는 단일 도메인만을 위한 형식이므로 링크 관계도 도메인 어휘 그대로다 — `north`, `south`, `east`, `west`, `exit`, `maze`, `collection`, `start`다.
클라이언트는 벽 배열이나 좌표계를 이해할 필요 없이 표현에 실린 rel만 따라가면 되고, 미로가 5×5든 100개 방이든 같은 코드가 작동한다.

도메인 특화 형식의 장점과 대가가 여기 다 드러난다.
장점은 의미가 형식 자체에 들어 있어 별도의 설명이 필요 없다는 것이고, 대가는 이 형식을 아는 클라이언트만 쓸 수 있으며 도메인마다 새 형식을 만들어야 한다는 것이다.

### OpenSearch

검색이라는 한 가지 상호작용만을 위한 형식이다.
OpenSearch 기술 문서(description document)는 미디어 타입 `application/opensearchdescription+xml`을 쓰고, 검색 엔진이 자기 검색 인터페이스를 기계가 읽을 수 있게 노출한다.

핵심은 `Url` 요소의 템플릿이다.

```xml
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>Example Search</ShortName>
  <Description>Search example.com</Description>
  <Url type="application/atom+xml"
       template="http://example.com/?q={searchTerms}&amp;start={startIndex?}" />
</OpenSearchDescription>
```

`{searchTerms}`, `{count}`, `{startIndex}`, `{startPage}`, `{language}`, `{inputEncoding}`, `{outputEncoding}` 같은 1.1 표준 파라미터가 정의돼 있고, 물음표가 붙은 파라미터는 선택이다.
HTML이나 RSS/Atom 문서에서 자동 발견(autodiscovery)할 수 있게 하는 규약도 명세에 들어 있다.

하이퍼미디어 관점에서 OpenSearch가 흥미로운 이유는 이것이 사실상 “검색 폼”이기 때문이다.
URI 템플릿 하나로 클라이언트가 스스로 요청 URL을 구성할 수 있게 하며, 링크만 있고 폼이 없는 형식이 어떻게 폼의 일부 기능을 흉내 내는지를 보여 준다.

### SVG

SVG는 하이퍼미디어 형식으로 분류하기 어색해 보이지만 정확히 그렇다.
W3C의 벡터 그래픽 형식이며, `<a>` 요소로 도형 어디에나 링크를 걸 수 있다.

SVG가 동물원에 있어야 하는 이유는 하이퍼미디어가 텍스트 문서의 전유물이 아님을 보이기 때문이다.
그림 안의 특정 영역이 링크가 될 수 있고, 그 링크를 따라가면 다른 리소스로 이동한다 — 매체가 무엇이든 표현이 다음 전이를 실어 나를 수 있다.

### VoiceXML

W3C의 음성 대화 애플리케이션 형식이다.
전화 음성 응답 시스템 같은 곳에서 쓰이며, 사용자는 화면을 보는 대신 듣고 말한다.

VoiceXML은 `<form>`, `<field>`, `<goto>`, `<submit>` 같은 요소로 대화의 상태 기계를 기술한다.
서버가 다음에 무엇을 물을지, 사용자의 대답을 어디로 보낼지를 문서 안에서 지시하므로, 구조적으로는 HTML 폼과 같은 일을 음성 매체에서 한다.

이 형식이 동물원에서 맡는 역할은 SVG와 짝을 이룬다.
SVG가 “하이퍼미디어는 텍스트가 아니어도 된다”를 보인다면, VoiceXML은 “하이퍼미디어는 시각적이 아니어도 된다”를 보인다.
하이퍼미디어의 본질은 매체가 아니라 “표현이 다음에 가능한 전이를 알려 준다”는 구조에 있다는 것이다.

## 컬렉션 패턴을 담은 형식들

저자는 컬렉션 패턴을 REST API의 약 80%를 포섭하는 반복 구조로 규정했다.
이 저장소의 [whats-new.md](whats-new.md)에 정리했듯, 이 패턴에 이름을 붙인 것 자체가 책의 방법론적 기여다.

### Atom과 AtomPub

Atom Syndication Format은 RFC 4287이고, Atom Publishing Protocol은 RFC 5023이다.
AtomPub이 컬렉션 패턴을 개척한 표준이며, 저자는 이 패턴을 “AtomPub이 개척한 CRUD 유사 설계”로 설명한다.

구조는 단순하다.
어떤 리소스는 GET/PUT/DELETE에 응답하는 아이템이고, 어떤 리소스는 아이템을 담고 POST로 추가에 응답하는 컬렉션이다.
AtomPub은 여기에 서비스 문서(service document)와 카테고리 문서를 더해, 클라이언트가 어떤 컬렉션이 있고 각 컬렉션이 어떤 미디어 타입을 받는지 런타임에 발견하게 한다.

Atom은 원래 블로그 피드 형식이었지만 그 구조가 도메인 중립이라 온갖 API의 뼈대로 재사용됐다.
그러나 XML 기반이라는 점이 JSON 시대에 한계가 됐고, 그 자리를 Collection+JSON 같은 형식이 이어받았다.

### Collection+JSON

Mike Amundsen이 만든 형식이며 미디어 타입은 `application/vnd.collection+json`이다.
AtomPub의 컬렉션 패턴을 JSON으로 옮기되, JSON에 없던 하이퍼미디어 능력을 규약으로 채워 넣었다.

문서는 최상위 `collection` 객체 하나를 갖고, 그 안에 `version`, `href`, `links`, `items`, `queries`, `template`, `error` 같은 자리가 있다.
이 가운데 `queries`와 `template`이 폼에 해당한다 — `queries`는 검색용 읽기 폼이고, `template`은 새 아이템을 만들거나 고칠 때 쓰는 쓰기 폼이다.

```json
{
  "collection": {
    "version": "1.0",
    "href": "http://example.org/api/",
    "items": [],
    "template": {
      "data": [
        { "name": "text", "value": "" }
      ]
    }
  }
}
```

이 저장소의 [example-code.md](example-code.md)에 정리한 “You Type It, We Post It” 서버가 이 형식의 실제 구현이다.
컬렉션(`/api/`)이 GET과 POST를, 아이템(`/api/{id}`)이 GET, PUT, DELETE를 받는 구조가 코드에 그대로 나타난다.

Collection+JSON이 동물원에서 갖는 위치는 “JSON으로도 온전한 하이퍼미디어가 가능하다”는 증명이다.
링크와 폼을 모두 갖췄고, 컬렉션이라는 특정 패턴에 특화돼 있어 그 패턴에 맞는 API에는 거의 그대로 쓸 수 있다.

## 범용 하이퍼미디어 형식들

### HTML

동물원에서 가장 오래되고 가장 능력이 많은 종이다.
저자가 4장에서 하이퍼미디어를 설명할 때 주로 HTML을 쓴 이유가 여기 있다 — 링크(`<a>`, `<link>`)와 폼(`<form>`)을 모두 갖췄고, 폼은 GET과 POST를 모두 낼 수 있으며, 입력 필드의 종류와 제약까지 표현한다.

API 형식으로 HTML을 쓰는 것이 이상해 보이지만 저자는 7장에서 이를 정면으로 권한다.
HTML은 이미 표준이고 파서가 어디에나 있으며, 마이크로포맷과 마이크로데이터로 의미를 덧붙일 수 있기 때문이다.

### HAL

JSON Hypertext Application Language이며 미디어 타입은 `application/hal+json`이다.
Mike Kelly가 만들었고 IETF 인터넷 드래프트로 유지된다.

설계 목표는 명세가 직접 밝히듯 일반성과 단순함 두 가지다.
“하이퍼미디어 웹 API의 핵심 요구를 커버하는 데 필요한 최소한의 구조만 부과한다”는 것이다.

문서의 루트는 리소스 객체이고, 예약된 속성은 둘뿐이다.
`_links`는 다른 리소스로의 링크를 담고, `_embedded`는 내장된 리소스를 담는다.
나머지 모든 속성은 리소스의 현재 상태다.

```json
{
  "_links": {
    "self": { "href": "/orders/523" },
    "warehouse": { "href": "/warehouse/56" },
    "invoice": { "href": "/invoices/873" }
  },
  "currency": "USD",
  "status": "shipped",
  "total": 10.20
}
```

HAL의 결정적 특징은 폼이 없다는 것이다.
명세의 FAQ에 “HAL에는 왜 폼이 없는가”라는 항목이 따로 있을 만큼 자주 나오는 질문이며, 이는 설계 목표인 단순함을 위해 의도적으로 치른 대가다.
링크만 있는 형식이므로 클라이언트는 상태 변경 요청을 어떻게 만들지 형식 밖에서 알아야 한다.

명세는 미디어 타입 파라미터로 `profile`을 정의하는데, 이것이 [8장](08-profiles.md)에서 본 RFC 6906의 권고를 그대로 따른 것이다.

### Siren

Kevin Swiber가 만든 엔티티 표현 형식이며 미디어 타입은 `application/vnd.siren+json`이다.
명세는 자기 위치를 이렇게 규정한다 — “HTML이 웹사이트에서 문서를 시각적으로 표현하는 데 쓰이듯, Siren은 웹 API로 엔티티를 제시하기 위한 명세다.”

Siren 문서는 다섯 자리를 갖는다.
`class`는 엔티티의 성격을 나타내는 분류이고, `properties`는 상태이며, `entities`는 하위 엔티티(내장 링크 또는 내장 표현), `actions`는 상태 전이를 실행하는 컨트롤, `links`는 탐색용 링크다.

HAL과 갈라지는 지점이 `actions`다.

```json
{
  "actions": [
    {
      "name": "add-item",
      "title": "Add Item",
      "method": "POST",
      "href": "http://api.x.io/orders/42/items",
      "type": "application/x-www-form-urlencoded",
      "fields": [
        { "name": "productCode", "type": "text" },
        { "name": "quantity", "type": "number" }
      ]
    }
  ]
}
```

`method`, `href`, `type`, `fields`가 모두 들어 있으므로 클라이언트는 이 정보만으로 요청을 구성할 수 있다.
이것이 HTML 폼에 가장 가까운 JSON 형식이며, HAL이 포기한 능력을 Siren이 채웠다고 볼 수 있다.

### JSON-LD와 Hydra

JSON-LD는 W3C 권고안이며 `@context`로 JSON 키를 IRI에 대응시켜 Linked Data를 직렬화한다.
[8장](08-profiles.md)에서 프로파일 형식의 하나로 다뤘듯, JSON-LD 자체는 데이터의 의미는 주지만 상태 전이 개념이 없다.

Hydra Core Vocabulary가 그 빈칸을 겨냥한다.
W3C Hydra 커뮤니티 그룹이 낸 문서이며, 명세는 자신을 “하이퍼미디어 주도 웹 API를 만들기 위한 가벼운 어휘”로 소개한다.
Hydra의 문제 의식은 명세 서문에 분명히 적혀 있다 — Linked Data는 여전히 대체로 읽기 전용이며, Hydra는 데이터에 기계가 읽을 수 있는 어포던스(affordance)를 실어 상호작용을 가능하게 한다.

Hydra는 `hydra:Operation`으로 연산을, `hydra:Collection`으로 컬렉션을, `hydra:IriTemplate`으로 템플릿 링크를 표현하고, `hydra:ApiDocumentation`으로 API 전체를 기술한다.
다만 Hydra는 W3C 표준도 아니고 표준화 트랙에 있지도 않다고 명세 자신이 밝힌다.

이 계보가 동물원에서 갖는 의의는 하이퍼미디어 문제에 시맨틱 웹 진영이 내놓은 답이라는 점이다.
저자는 이 계보를 12장 Linked Data에서 본격적으로 다룬다고 밝혔다.

## HTML에 의미를 덧붙이는 방식들

### 마이크로포맷

마이크로포맷은 HTML의 `class` 속성을 재사용해 구조화된 데이터를 표현하는 관례 모음이다.
hCard(연락처), hCalendar(일정), rel-tag, XFN 같은 개별 마이크로포맷이 각자의 어휘를 정의한다.

RFC 6906이 프로파일의 대표 예로 hCard를 든 것이 이 방식의 성격을 정확히 짚는다.
hCard는 (X)HTML의 처리 규칙과 의미를 전혀 바꾸지 않으면서 추가 의미를 뽑아낼 규칙만 더하므로 새 미디어 타입이 아니라 프로파일이다.
ALPS 드래프트가 자기 복잡도를 “HTML 마이크로포맷과 비슷한 수준”이라고 표현한 것도 같은 맥락이다.

### 마이크로데이터

마이크로데이터는 HTML 표준에 포함된 메커니즘으로, `itemscope`, `itemtype`, `itemprop` 속성을 써서 구조화된 데이터를 표시한다.

```html
<div itemscope itemtype="http://schema.org/Person">
  <span itemprop="name">Ann Arbuckle</span>
  <span itemprop="email">aa@example.org</span>
</div>
```

마이크로포맷이 커뮤니티 관례라면 마이크로데이터는 명세에 들어간 문법이고, `itemtype`이 어휘를 URL로 가리키므로 schema.org 같은 전역 어휘와 자연스럽게 결합한다.
저자는 7장에서 이 둘을 소개하며 8장의 프로파일 논의로 이어진다고 밝혔다.

## 형식이 아닌 하이퍼미디어 조각들

동물원에는 완결된 문서 형식이 아닌 종도 있다.
다른 표현에 얹혀 하이퍼미디어 능력을 보태는 것들이다.

### `Link` 헤더

RFC 5988이 정의했고 지금은 RFC 8288이 대체한 웹 링킹 메커니즘이다.
HTTP 헤더로 링크를 보내므로, 본문 형식이 하이퍼미디어가 아니어도 링크를 붙일 수 있다.

```http
HTTP/1.1 200 OK
Content-Type: application/json
Link: <http://example.org/api/?page=2>; rel="next"
Link: <http://alps.io/profiles/contacts>; rel="profile"
```

이 장치의 실용적 가치는 크다.
순수 `application/json`에는 링크를 표현할 표준 방법이 없는데, `Link` 헤더는 형식을 바꾸지 않고 그 한계를 우회한다.
[8장](08-profiles.md)에서 본 대로 ALPS 드래프트도 표현이 링크 능력을 갖지 못한 경우 `Link` 헤더를 쓰라고 안내한다.

### `text/uri-list`

RFC 2483이 등록한 미디어 타입으로, URI 목록을 한 줄에 하나씩 담는 극도로 단순한 형식이다.
주석은 `#`으로 시작한다.

```text
# 검색 결과
http://example.org/contacts/1
http://example.org/contacts/100
```

이것이 동물원에 있어야 하는 이유는 하이퍼미디어의 하한선을 보여 주기 때문이다.
링크 관계도 없고 폼도 없고 메타데이터도 없지만, “다음에 갈 수 있는 곳들”을 담고 있으므로 이미 하이퍼미디어다.

### 홈 문서(JSON Home)

Mark Nottingham의 인터넷 드래프트가 정의하는, HTTP API의 시작점 문서다.
드래프트가 밝히는 문제 의식은 하이퍼미디어 논증 그 자체다 — HTTP 애플리케이션이 흔히 클라이언트가 알아야 할 정적 URL 목록을 문서로 적어 정의되는데, 그 범위를 벗어난 상호작용은 미지의 영역이 되고 인터페이스가 진화하면 문제가 생긴다.

홈 문서는 링크 관계와 미디어 타입이라는 공유 어휘로 런타임에 리소스를 발견하게 한다.
드래프트가 꼽는 이득은 확장성(새 기능을 새 API 버전 없이 링크 관계로 얹을 수 있다), 진화 가능성, 클라이언트별 맞춤, 유연한 배포(URL이 문서에 고정되지 않으므로 서버가 URL을 자유롭게 고를 수 있다)다.

마지막 항목이 특히 [9장](09-design-procedure.md)의 논의와 맞닿는다.
하이퍼미디어를 제대로 쓰면 URI 설계가 클라이언트와의 계약에서 서버 내부의 편의로 내려간다는 것이 홈 문서의 전제다.

### URI 템플릿

RFC 6570이 정의하는 URI 템플릿 문법이다.
`http://example.com/search{?q,page}` 같은 표현을 변수 값으로 채워 실제 URI를 만든다.

그 자체로는 하이퍼미디어 형식이 아니지만 여러 형식이 폼을 흉내 내는 데 쓰는 부품이다.
HAL의 `templated` 링크, Collection+JSON의 `queries`, Hydra의 `IriTemplate`, OpenSearch의 `Url` 템플릿이 모두 같은 발상이다.

## 기술(description) 형식과의 경계

동물원의 한쪽 끝에는 하이퍼미디어가 아니라 인터페이스 기술서에 해당하는 종들이 있다.
WADL(Web Application Description Language, 2009년 W3C 회원 제출)과 WSDL이 대표적이며, XLink와 XForms처럼 XML 세계에서 링크와 폼을 일반화한 명세도 있다.

이들이 하이퍼미디어와 갈라지는 지점은 정보가 어디에 실리는가다.
하이퍼미디어는 다음에 가능한 전이를 응답 표현 안에 실어 런타임에 전달한다.
기술 형식은 그 정보를 별도 문서로 사전에 배포하므로, 인터페이스가 바뀌면 문서와 클라이언트를 함께 고쳐야 한다.

이 경계가 흐릿한 사례도 있다.
Hydra의 `ApiDocumentation`이나 JSON Home 문서는 사전 기술서에 가까워 보이지만, 런타임에 가져오는 리소스이고 링크 관계라는 공유 어휘로 표현되므로 하이퍼미디어 쪽에 선다.
결국 판단 기준은 “클라이언트가 이 정보를 컴파일 시점에 갖는가, 실행 시점에 받는가”다.

## 동물원이 증명하는 것

이렇게 늘어놓고 보면 저자가 왜 이 장을 넣었는지가 드러난다.
표면적 목적은 “하이퍼미디어가 무엇을 할 수 있는지 보이는 것”이지만, 실제 효과는 두 가지다.

첫째, 하이퍼미디어가 API 설계의 특수한 유행이 아니라 이미 널리 표준화된 기법임을 보인다.
Atom은 블로그 피드에서, SVG는 그래픽에서, VoiceXML은 음성 응답에서, OpenSearch는 검색에서 각자 독립적으로 같은 구조에 도달했다.

둘째, 새 형식을 만들 이유가 대개 없음을 보인다.
약 20종의 표준이 이미 있고 대부분의 문제는 그중 하나에 맞는다면, 5장이 “뻔한 전략”이라 부른 도메인 특화 형식 신설은 마지막 선택지가 된다.
그리고 범용 형식을 골랐을 때 남는 의미의 문제는 [8장](08-profiles.md)의 프로파일이 처리한다.

## 핵심 정리

10장은 약 20종의 표준화된 하이퍼미디어 데이터 형식을 훑는 전시장이며, 대부분 책의 다른 곳에서 다루지 않은 것들이다.

형식들은 세 축으로 갈린다.
도메인 특화인가 범용인가, 링크만 있는가 폼까지 있는가, 완결된 문서 형식인가 다른 표현에 얹히는 조각인가다.

도메인 특화 쪽에는 Maze+XML, OpenSearch, SVG, VoiceXML이 있다.
SVG와 VoiceXML은 하이퍼미디어가 텍스트나 시각 매체에 국한되지 않음을 보인다.

컬렉션 패턴 쪽에는 AtomPub(RFC 5023)과 Collection+JSON이 있다.
AtomPub이 이 패턴을 개척했고, Collection+JSON이 `queries`와 `template`으로 JSON에서 폼까지 갖춰 이어받았다.

범용 형식 쪽에는 HTML, HAL, Siren, JSON-LD와 Hydra가 있다.
HAL은 `_links`와 `_embedded` 둘만 예약해 단순함을 택했고 폼이 없다.
Siren은 `actions`에 `method`, `href`, `type`, `fields`를 실어 HTML 폼에 가장 가까운 JSON 형식이 됐다.

형식이 아닌 조각으로는 `Link` 헤더(RFC 8288), `text/uri-list`(RFC 2483), JSON Home 문서, URI 템플릿(RFC 6570)이 있다.
이들은 본문 형식이 하이퍼미디어가 아니어도 링크와 폼 비슷한 능력을 보탠다.

WADL이나 WSDL 같은 기술 형식과의 경계는 정보가 실리는 자리로 갈린다.
하이퍼미디어는 응답 표현 안에서 런타임에 전이를 알려 주고, 기술 형식은 별도 문서로 사전에 배포한다.

## 참고

- Atom Syndication Format (RFC 4287): <https://www.rfc-editor.org/rfc/rfc4287>
- Atom Publishing Protocol (RFC 5023): <https://www.rfc-editor.org/rfc/rfc5023>
- JSON Hypertext Application Language (HAL): <https://datatracker.ietf.org/doc/draft-kelly-json-hal/>
- Siren: <https://github.com/kevinswiber/siren>
- Hydra Core Vocabulary: <https://www.hydra-cg.com/spec/latest/core/>
- JSON-LD 1.1: <https://www.w3.org/TR/json-ld11/>
- OpenSearch: <https://github.com/dewitt/opensearch>
- Web Linking (RFC 8288): <https://www.rfc-editor.org/rfc/rfc8288>
- text/uri-list (RFC 2483): <https://www.rfc-editor.org/rfc/rfc2483>
- URI Template (RFC 6570): <https://www.rfc-editor.org/rfc/rfc6570>
- Home Documents for HTTP APIs: <https://datatracker.ietf.org/doc/draft-nottingham-json-home/>
- 저자 공식 장별 설명: <http://restfulwebapis.com/chapters.html>
- 이 저장소의 관련 문서: [whats-new.md](whats-new.md), [example-code.md](example-code.md), [08-profiles.md](08-profiles.md)
