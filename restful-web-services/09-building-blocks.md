# 9장 서비스의 구성 요소

《RESTful Web Services》(Leonard Richardson, Sam Ruby, O'Reilly 2007) 9장 정리.

## 개요

웹 서비스는 HTTP, URI, XML이라는 세 가지 근본 기술 위에 서 있지만, 그 위에 쌓아 올릴 수 있는 기술이 많이 있다.
도메인 특화 XML 어휘, HTTP의 균일 인터페이스(uniform interface)로 리소스를 노출하는 표준 규칙 같은 것들이다.
이런 추가 기술을 도입하면 직접 만들어야 할 일이 줄고, 서비스를 이해하는 대상 범위도 넓어진다.

이 장은 서비스를 개선할 수 있는 여러 기술을 세 갈래로 나누어 다룬다.
첫째는 표현 포맷(Representation Formats)으로, 서비스가 실제로 주고받을 데이터를 어떻게 표현할지에 대한 것이다.
둘째는 사전 포장된 제어 흐름(Prepackaged Control Flows)으로, 리소스 설계와 응답 코드를 묶어 재사용 가능한 패턴으로 정리한 것이며 대표적으로 Atom 출판 프로토콜(APP)이 있다.
셋째는 하이퍼미디어 기술(Hypermedia Technologies)로, 링크와 폼을 통해 서비스 간 차이를 표현하는 방법이다.

## 표현 포맷

어떤 표현 포맷을 보내고 받을지는 방대한 질문이다.
저자의 목표는 데이터의 의미(semantics)를 담아내는 포맷을 고르게 해서, 아무도 쓰지 않을 일회용 XML 어휘를 또 하나 만드는 일을 피하게 하는 것이다.
클라이언트가 어떤 포맷이든 받을 수 있다고 가정하되, 클라이언트의 알려진 요구가 이 장의 어떤 조언보다 우선한다.
데이터가 Microsoft Excel로 직접 들어간다면 Excel 포맷이나 호환되는 CSV로 제공해야 한다.
사람만 이해할 수 있는 문서 포맷(예: 오디오 파일)은 이 조언의 대상이 아니다.

### XHTML

미디어 타입은 `application/xhtml+xml`이다.
흔히 쓰이는 `text/html`은 XHTML에 대해서는 권장되지 않지만, Internet Explorer가 HTML로 처리하는 유일한 미디어 타입이다.
브라우저에 XHTML을 직접 제공할 가능성이 있다면 `text/html`로 보내는 편이 나을 수 있다.

저자의 첫 번째 추천 포맷은 XHTML이다.
HTML이 사람의 웹(human web)을 이끌듯, XHTML은 프로그래밍 가능한 웹(programmable web)을 이끌 수 있다.
XHTML은 HTML에 몇 가지 제약을 더해 모든 XHTML 문서가 유효한 XML이 되도록 한 것이다.
자기 닫힘(self-closing) 태그를 표기하는 방식 같은 구문 차이가 있지만, 태그 이름과 속성은 HTML과 같고 표현력도 같다.

저자는 HTML을 표현 포맷으로 직접 권하지는 않는다.
HTML은 XML 파서로 안정적으로 파싱할 수 없기 때문이다.
다만 훌륭하고 관대한 HTML 파서가 많으므로, XHTML을 제공할 수 없거나 원치 않는다면 클라이언트에게 선택지가 있다.
다양한 클라이언트가 데이터를 다루길 기대한다면 지금으로서는 XHTML이 더 나은 선택이다.

HTML은 여러 흔한 데이터 유형을 표현할 수 있다.
`ul`, `li`로 중첩 리스트를, `dl`과 그 자식으로 키-값 쌍을, `table`과 그 자식으로 표 형태 데이터를 표현한다.
여러 종류의 하이퍼미디어도 지원한다.
그러나 단점도 있다.
하이퍼미디어 폼(form)이 제한적이고, HTML 5가 나오기 전까지는 HTTP의 균일 인터페이스를 온전히 지원하지 못한다.

HTML은 의미 정보(semantic content) 면에서도 빈약하다.
태그 어휘가 매우 컴퓨터 중심이어서 코드나 출력에 대한 태그는 있어도 시(poetry) 같은 인간 활동의 산물을 위한 태그는 없다.
리소스 간 관계를 나타내는 표준 속성 `rel`과 `rev`가 있지만, HTML 표준이 정의한 리소스 관계는 `alternate`, `stylesheet`, `next`, `prev`, `glossary` 등 15가지뿐이다.
리소스는 무엇이든 될 수 있으므로 이 15가지로는 표면조차 긁지 못한다.
직접 `rel`, `rev` 값을 만들 수 있지만 모두가 그렇게 하면 같은 관계에 서로 다른 값을 쓰게 되어 혼란이 생긴다.
이것이 사람들이 마이크로포맷으로 XHTML에 표준 의미를 더하기 시작한 이유다.

### 마이크로포맷을 얹은 XHTML

미디어 타입은 `application/xhtml+xml`이다.
마이크로포맷(microformats)은 XHTML을 확장해 HTML 태그에 도메인 특화 의미를 부여하는 경량 표준이다.
리스트 같은 데이터 저장 기법을 새로 만드는 대신 `ol`, `span`, `abbr` 같은 기존 HTML 태그를 사용한다.
의미 정보는 보통 `class`, `rel`, `rev` 같은 속성의 커스텀 값에 담긴다.
예를 들어 hCard 마이크로포맷으로 집 전화번호를 표현하면 다음과 같다.

```html
<span class="tel">
  <span class="type">home</span>:
  <span class="value">+1.415.555.1212</span>
</span>
```

마이크로포맷 문서는 XHTML이므로 어떤 XHTML 페이지에도 삽입할 수 있다.
서비스는 마이크로포맷 문서와 다른 리소스로 향하는 링크, 새 리소스를 만드는 폼을 함께 담은 XHTML 표현을 제공할 수 있다.
이 문서는 마이크로포맷 데이터를 자동 파싱할 수도, 일반 브라우저로 사람이 보도록 렌더링할 수도 있다.

집필 시점의 공식 마이크로포맷 명세는 다음과 같다.

- hCalendar: 달력이나 일정표의 이벤트를 표현하는 방법으로, IETF의 iCalendar 포맷에 기반한다.
- hCard: 사람과 조직의 연락처 정보를 표현하는 방법으로, RFC 2426에 정의된 vCard 표준에 기반한다.
- rel-license: XHTML 문서의 라이선스 조건으로 링크할 때 쓰는 `rel` 속성의 새 값이다. `rel` 속성에 나타난 `license`라는 문자열에 의미를 부여하는 것 외에는 표준 XHTML과 다르지 않다.
- rel-nofollow: 링크한 URI를 반드시 지지하지는 않으면서 링크할 때 쓰는 `rel` 값이다. 구글 엔지니어들이 블로그 댓글 스팸에 맞서기 위해 고안했으며 가장 잘 알려진 마이크로포맷이다.
- rel-tag: 외부 분류 체계에 따라 웹 페이지에 꼬리표를 붙이는 `rel` 값이다.
- VoteLinks: rel-nofollow의 발상을 확장한 것으로, 링크 대상에 대한 감정을 “투표”로 표현하는 `rev` 값(`vote-for`, `vote-against`)이다.
- XFN: XHTML Friends Network의 약자로, 사람 사이의 관계를 담는 `rel` 값들의 집합이다. 예컨대 Alice의 표현에 배우자 Bob으로 향하는 `<a rel=“spouse” href=“Bob”>Bob</a>` 링크를 넣을 수 있다.
- XMDP: XHTML Meta Data Profiles의 약자로, 정의 리스트 태그(`DL`, `DD`, `DT`)를 이용해 자신의 커스텀 속성 값을 기술하는 방법이다. 마이크로포맷을 기술하는 메타 마이크로포맷 성격을 가진다.
- XOXO: Extensible Open XHTML Outlines의 약자로, XHTML 리스트 태그로 개요(outline)를 표현한다. 문서나 리스트를 XOXO로 선언하면 그 리스트가 단순 리스트가 아니라 개요임을 알린다.

집필 시점에는 약 10개의 초안과 50건이 넘는 논의도 있었다.
주목할 만한 초안은 다음과 같다.

- geo: 지구상의 위도와 경도를 마크업하는 방법이다. 다만 지구 외 천체의 좌표 표현 방식을 두고 논쟁이 있었다.
- hAtom: Atom이 XML로 표현하는 데이터를 XHTML로 표현하는 방법이다.
- hResume: 이력서를 표현하는 방법이다.
- hReview: 제품이나 식당 후기 같은 리뷰를 표현하는 방법이다.
- xFolk: 북마크를 표현하는 방법으로, 소셜 북마킹 애플리케이션의 좋은 표현 포맷이 될 수 있다.

마이크로포맷의 힘은 가장 널리 배포된 마크업 포맷인 HTML에 기반한다는 점이다.
HTML이므로 웹 페이지에 삽입할 수 있고, XML이기도 하므로 XML 문서에도 삽입할 수 있다.
사람, 전용 마이크로포맷 처리기, 단순한 HTML 처리기, 더 단순한 XML 처리기가 각기 다른 수준에서 이해할 수 있다.
자신의 문제 영역에 맞는 표준이나 초안이 없더라도 논의가 데이터 구조를 명확히 하는 데 도움이 될 수 있고, 직접 마이크로포맷을 만들 수도 있다.

### Atom

미디어 타입은 `application/atom+xml`이다.
Atom은 타임스탬프가 붙은 항목의 목록을 기술하는 XML 어휘다.
항목은 무엇이든 될 수 있지만 보통 블로그나 뉴스 사이트에서 볼 법한, 사람이 작성한 텍스트를 담는다.
일반 XHTML 리스트 대신 Atom을 쓰는 이유는, Atom이 출판(publishing)의 의미를 담는 전용 태그(작성자, 기여자, 언어, 저작권 정보, 제목, 카테고리 등)를 제공하기 때문이다.
많은 웹 서비스가 넓은 의미에서 정보를 출판하는 일이며, Atom 문서를 이해하는 클라이언트가 이미 많다.
서비스가 주소 지정 가능(addressable)하고 리소스가 Atom 표현을 노출하면 곧바로 큰 사용자층을 얻는다.

Atom 목록은 피드(feed)라 부르고, 목록 안의 항목은 엔트리(entry)라 부른다.
일부 피드는 RSS의 어떤 버전으로 작성되는데, RSS도 Atom과 같은 기본 구조(엔트리를 담은 피드)를 가진다.
RSS에는 여러 변종이 있지만 오늘날 피드를 소비하는 주요 도구는 모두 Atom을 이해하므로 걱정할 필요가 없다.

다음은 하나의 엔트리를 담은 간단한 Atom 피드다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>RESTful News</title>
  <link rel="alternate" href="http://example.com/RestfulNews" />
  <updated>2007-04-14T20:00:39Z</updated>
  <author><name>Leonard Richardson</name></author>
  <contributor><name>Sam Ruby</name></contributor>
  <id>urn:1c6627a0-8e3f-0129-b1a6-003065546f18</id>
  <entry>
    <title>New Resource Will Respond to PUT, City Says</title>
    <link rel="edit" href="http://example.com/RestfulNews/104" />
    <id>urn:239b2f40-8e3f-0129-b1a6-003065546f18</id>
    <updated>2007-04-14T20:00:39Z</updated>
    <summary>
      After long negotiations, city officials say the new resource
      being built in the town square will respond to PUT.
    </summary>
    <category scheme="http://www.example.com/categories/RestfulNews"
      term="local" label="Local news" />
  </entry>
</feed>
```

이 예에서 출판의 의미를 담은 태그(author, title, link, summary, updated 등)를 볼 수 있다.
피드 전체는 공동 작업물이라 author와 contributor를 함께 가지며, 기저 “피드” 리소스의 대체 URI를 가리키는 link도 있다.
엔트리에는 author 태그가 없어 피드에서 작성자 정보를 물려받고, 자신의 link로 리소스로서의 자기 URI를 가리킨다.
엔트리에는 요약만 있으므로 나머지를 얻으려면 클라이언트가 엔트리의 URI에 GET 해야 한다.

Atom 문서는 기본적으로 출판된 리소스의 디렉터리다.
사진 갤러리, 음악 앨범, 검색 결과 목록을 표현하거나, link 태그를 생략하고 상태 보고서나 수신 이메일 같은 원본 콘텐츠의 컨테이너로도 쓸 수 있다.
Atom을 쓰는 두 이유는 출판의 의미를 표현한다는 점과 기존 클라이언트가 많이 소비할 수 있다는 점이다.

애플리케이션이 Atom 스키마에 거의 맞지만 태그 한두 개가 더 필요하다면, 다른 네임스페이스의 XML 태그를 Atom 피드에 삽입할 수 있다.
커스텀 네임스페이스를 정의해 그 태그를 삽입해도 피드가 무효화되지 않는다.
이는 XHTML 마이크로포맷의 Atom 판이며, 태그를 이해하지 못하는 클라이언트는 정상 Atom 피드에 정체불명의 추가 데이터가 담긴 것으로 본다.

### OpenSearch

OpenSearch는 Atom 문서에 흔히 삽입되는 XML 어휘로, 검색 결과 목록을 표현하도록 설계되었다.
질의 결과를 Atom 피드로 반환하고 개별 결과를 Atom 엔트리로 표현하는 방식이다.
다만 총 결과 수처럼 기본 Atom 피드로는 표현할 수 없는 부분이 있어, OpenSearch는 `opensearch` 네임스페이스에 세 요소를 정의한다.

- totalResults: 질의에 맞은 전체 결과 수.
- itemsPerPage: 검색 결과 한 “페이지”에 반환되는 항목 수.
- startIndex: 모든 결과를 0부터 totalResults까지 번호 매겼을 때 이 피드 문서의 첫 결과가 몇 번째인지. itemsPerPage와 함께 쓰면 현재 몇 페이지인지 계산할 수 있다.

OpenSearch는 “description document”라는 간단한 제어 흐름도 정의하지만 이 책에서는 지면상 다루지 않는다.

### SVG

미디어 타입은 `image/svg+xml`이다.
대부분의 그래픽 포맷은 화면에 픽셀을 배치하는 방법일 뿐이어서 내용이 컴퓨터에게는 불투명하다.
Scalable Vector Graphics는 프로그램이 그래픽을 이해하고 조작할 수 있게 하는 XML 어휘로, 도형·텍스트·색·효과 같은 원시 요소로 그래픽을 기술한다.
사진을 SVG로 표현하는 것은 낭비지만, 그래프·다이어그램·관계 집합을 표현하면 클라이언트에게 큰 힘을 준다.
SVG 이미지는 세부 손실 없이 임의 크기로 확대할 수 있고, 편집·재배치하거나 일부를 잘라 다른 그래픽에 넣을 수 있다.
당시 새 버전의 Firefox는 SVG를 네이티브로 지원하기 시작했다.

### 폼 인코딩 키-값 쌍

미디어 타입은 `application/x-www-form-urlencoded`이다.
이 단순한 포맷은 6장에서 다뤘으며, 주로 클라이언트가 서버로 보내는 표현에 쓰인다.
작성된 HTML 폼이 기본적으로 이 포맷으로 표현되고, Ajax 애플리케이션이 만들기도 쉽다.
서버가 보내는 표현에도 쓸 수 있다.
쉼표로 구분된 값이나 RFC 822 스타일 키-값 쌍을 제공하려 한다면 대신 폼 인코딩 값을 써보라.
폼 인코딩은 까다로운 경우를 처리해 주고, 클라이언트가 해독 라이브러리를 가지고 있을 가능성이 높다.

### JSON

미디어 타입은 `application/json`이다.
JavaScript Object Notation은 일반 데이터 구조를 위한 직렬화 포맷이다.
동등한 XML 문서보다 훨씬 가볍고 읽기 쉬워, 하이퍼미디어 문서가 아니라 직렬화된 데이터 구조를 전송할 때 대부분 권장된다.
다음은 리스트의 해시 같은 조금 더 복잡한 JSON 문서다.

```json
{"a":["b","c"], "1":[2,3]}
```

JSON은 11장에서 보듯 Ajax 애플리케이션에 특별한 이점이 있지만 어떤 종류의 애플리케이션에도 유용하다.
데이터 구조가 키-값 쌍보다 복잡하거나 임의 XML 포맷을 정의하려 한다면, 중첩된 해시와 배열로 이루어진 JSON 구조를 정의하는 편이 더 쉬울 수 있다.

### RDF와 RDFa

Resource Description Framework(RDF)는 리소스에 대한 지식을 표현하는 방법이다.
여기서 리소스는 리소스 지향 아키텍처(ROA)에서와 같은 의미로, URL을 가질 만큼 중요한 모든 것이다.
다만 RDF에서는 URI가 `http:`가 아닐 수 있어, `isbn:`(책)이나 `urn:`(거의 모든 것) 같은 추상 URI 스킴도 흔하다.
다음은 이 책의 제목이 RESTful Web Services라고 주장하는 간단한 RDF 단언이다.

```html
<span about="isbn:9780596529260" property="dc:title">
  RESTful Web Services
</span>
```

RDF 단언(트리플, triple)은 세 부분으로 이루어진다.
주어(subject)는 리소스 식별자로 여기서는 `isbn:9780596529260`, 술어(predicate)는 리소스의 속성을 식별하며 여기서는 `dc:title`, 목적어(object)는 속성 값으로 여기서는 “RESTful Web Services”다.
전체는 “ISBN 9780596529260인 책의 제목은 'RESTful Web Services'다”로 읽힌다.

`isbn:` URI 공간과 `dc:title` 술어는 저자가 만든 것이 아니다.
`dc:title`은 출판물에 적용되는 유용한 술어 집합을 정의하는 Dublin Core Metadata Initiative(DCMI)에서 온 것이다.
Dublin Core를 이해하는 자동 클라이언트는 그 용어를 쓴 RDF 문서를 훑어 단언을 평가하고 논리적 추론까지 할 수 있다.

앞의 예는 XHTML 조각처럼 보이는데, 실제로 그렇다.
이는 RDF를 XHTML에 삽입하는 마이크로포맷 같은 표준인 RDFa로 표현한 것이다.
RDF/XML이 더 널리 쓰이는 RDF 표현 포맷이지만 RDF를 실제보다 복잡해 보이게 하고 웹에 통합하기 어렵다.
RDFa 문서는 마이크로포맷 문서처럼 XHTML 파일에 넣을 수 있지만, 미출시 XHTML 2 표준의 아이디어를 일부 가져와 당분간 유효한 XHTML이 되지는 못한다.
유효한 XHTML을 만드는 세 번째 방법으로 eRDF도 있다.

일반형 RDF는 W3C의 Semantic Web 프로젝트의 기반이다.
사람의 웹에는 우리가 링크하는 리소스를 어떻게 이야기할지에 대한 표준이 없고, 기계가 이해하기 어려운 사람 언어로 리소스를 기술한다.
RDF는 사람의 말을 제약해 표준 어휘로 리소스를 이야기하게 하는 방법이다.
기계가 그 어휘를 네이티브로 “이해”하는 것은 아니지만, 이해하도록 프로그래밍될 수 있다.
프로그램은 `dc:title`을 `title`만큼도 이해하지 못하지만, 모두가 `dc:title`을 쓰기로 합의하면 표준 클라이언트를 일관되게 추론하도록 만들 수 있다.

저자의 생각으로 마이크로포맷은 이미 존재하는 웹에 의미를 더하는 일을 잘 해내며 RDF의 일반 주어-술어-목적어 형식보다 복잡도가 낮다.
따라서 기존 RDF 처리기와의 상호운용성을 원하거나, RDF를 리소스에 관한 단언을 표현하는 범용 마이크로포맷처럼 다룰 때만 RDF 사용을 권한다.
RDF의 매우 인기 있는 활용 중 하나는 사람과 그들 사이의 관계 정보를 표현하는 FOAF다.

### 프레임워크 특화 직렬화 포맷

미디어 타입은 `application/xml`이다.
Ruby의 ActiveRecord나 Python의 Django 같은 프레임워크가 데이터베이스 객체를 XML로 직렬화할 때 쓰는 비공식 XML 어휘를 말한다.
해시 또는 해시의 리스트라는 단순한 데이터 구조다.
접근 수단이 있다면 매우 편리하다.
Rails에서는 ActiveRecord 객체나 그 리스트에 `to_xml`을 호출하기만 하면 되고, Rails를 쓰지 않아도 ActiveResource 클라이언트가 서비스를 쓰게 하고 싶을 때 유용하다.
그 밖에는, 빠르게 무언가를 띄우려는 경우가 아니라면 권하지 않는다.
가장 큰 단점은 문서처럼 보이지만 실제로는 직렬화된 데이터 구조일 뿐이라는 것이다.
이 포맷들은 하이퍼미디어 링크나 폼을 절대 담지 않는다.

### 임시(Ad Hoc) XHTML

미디어 타입은 `application/xhtml+xml`이다.
이미 만들어진 어떤 것도 문제 영역에 맞지 않는다면, 우선 다시 생각해 보라.
리소스를 HTTP의 균일 인터페이스에 맞출 수 없다고 결론짓기 전에 다시 생각해야 하는 것과 같다.
HTML, Atom, RDF, JSON으로 리소스를 표현할 수 없다고 여긴다면 문제를 올바른 방식으로 보지 못했을 가능성이 크다.

그래도 맞지 않는다면 다음 단계는 자신의 마이크로포맷을 만드는 것을 고려하는 것이다.
영향력이 큰 방법은 마이크로포맷 프로세스를 거쳐 다른 애호가들과 다듬어 공식 마이크로포맷으로 발표하는 것이다.
많은 사람이 같은 종류의 데이터를 표현하려 하고, 모델로 삼을 큰 표준이 이미 있을 때 가장 적절하다.
hCard와 hCalendar가 이렇게 vCard, iCalendar를 본떠 개발되었다.

영향력이 작은 방법은 어차피 작성할 XHTML에 의미 정보를 더하는 것이다.
남이 쓸 일이 없는 표현 포맷이거나, 마이크로포맷 프로세스를 거치는 동안 실제 서비스를 돌리기 위한 출발점으로 적합하다.
선택한 “미니 마이크로포맷”의 의미는 표준화되지 않지만, 마이크로포맷이 하는 방식대로 표준적인 형태로 제시할 수 있다.
유용한 패턴은 다음과 같다.

- 원하는 의미를 전달하는 HTML 태그가 있으면 그것을 쓴다. 키-값 쌍에는 `dl`, 리스트에는 리스트 태그를 쓰고, 맞는 것이 없으면 `span`이나 `div`를 쓴다.
- `class` 속성을 지정해 태그에 의미를 더한다. 자체 의미가 없는 `span`, `div`에 특히 중요하다.
- 다른 리소스가 이 리소스에 대해 갖는 관계는 링크의 `rel`로, 이 페이지가 외부 URI에 대해 갖는 관계는 `rev`로 지정한다. 대칭 관계라면 `rel`을 쓴다.
- `class`, `rel`, `rev`의 커스텀 값을 기술하는 XMDP 파일 제공을 고려한다.

### 그 밖의 XML 표준과 임시 어휘

미디어 타입은 `application/xml`이다.
XHTML, Atom, SVG 외에도 MathML, OpenDocument, Chemical Markup Language 같은 특화 XML 어휘가 많다.
RDF 단언에 쓸 수 있는 Dublin Core, FOAF 같은 특화 어휘도 있다.
서비스는 이런 어휘를 독립 표현으로 제공하거나 Atom 피드에 삽입하거나 SOAP 봉투로 감쌀 수 있다.
어느 것도 맞지 않으면 리소스 상태(또는 Atom이 다루지 못하는 부분)를 표현할 커스텀 XML 어휘를 정의할 수 있다.

이것을 최후의 수단으로 제시했지만 통상적인 견해는 그렇지 않다.
사람들은 늘 커스텀 XML 어휘를 만들며, 이 책에 언급된 거의 모든 실제 서비스가 커스텀 XML 어휘로 표현을 노출한다.
Amazon S3, Yahoo!의 검색 API, del.icio.us API 모두 Atom이나 XHTML을 쉽게 제공해 기존 어휘를 재사용할 수 있는데도 커스텀 XML 어휘를 쓴다.

여기에는 기술 문화가 일부 작용한다.
마이크로포맷 아이디어가 비교적 새롭고 커스텀 XML 어휘가 더 “공식적”으로 보이지만 이는 착각이다.
스키마 정의를 제공하지 않는 한 커스텀 태그의 지위는 HTML `class` 속성의 커스텀 값과 정확히 같다.
정의를 하더라도 만든 어휘를 성문화할 뿐 정당성을 부여하지는 않는다.
정당성은 오직 “피지배자의 동의”에서, 즉 다른 사람들이 그 어휘를 채택하는 데서 온다.

그래도 커스텀 XML 어휘를 위한 자리는 있다.
XHTML로 대신하기는 대개 쉽지만, 커스텀 속성이 많은 태그가 필요할 때는 쉽지 않다.
그런 상황에서는 커스텀 XML 어휘가 타당하다.
다만 새 XML 어휘가 정말 필요한지 진지하게 생각해 보길 권한다.
지금의 문제는 임시 XML 어휘가 너무 많다는 것이다.

### 인코딩 문제

노출하는 서비스는 서로 다른 언어와 문자 체계를 쓰는 사람들의 산물을 다뤄야 한다.
모든 언어를 이해할 필요는 없지만, 다국어 데이터를 훼손 없이 다루려면 문자 인코딩, 즉 사람이 읽을 텍스트를 바이트 열로 표현하는 규약을 알아야 한다.

모든 텍스트 파일에는 인코딩이 있지만 대개 시스템 속성으로 정해져 사용자가 결정하지 않는다.
미국에서는 보통 UTF-8, US-ASCII, Windows-1252이고, 서유럽에서는 ISO 8859-1도 쓰인다.
웹의 HTML 기본값은 ISO 8859-1인데 Windows-1252와 거의 같지만 완전히 같지는 않다.
일본어 문서는 흔히 EUC-JP, Shift_JIS, UTF-8로 인코딩된다.
이런 인코딩 대부분은 같은 언어를 인코딩할 때조차 서로 호환되지 않는다.

이 혼란에서 벗어나는 길은 Unicode다.
Unicode는 인코딩 자체는 아니지만 좋은 인코딩이 둘 있다.
UTF-8은 영어 같은 알파벳 언어에, UTF-16은 일본어 같은 표어(logographic) 언어에 더 효율적이며, 둘 다 어떤 언어 조합의 텍스트도 다룰 수 있다.
다국어 데이터를 다룰 때 최선의 결정은 모든 데이터를 이 중 하나로 유지하는 것이다.
동아시아에서 많은 업무를 하지 않는 한 대체로 UTF-8이며, 그렇다면 바이트 순서 표시(byte-order mark)가 붙은 UTF-16일 수 있다.

기존 데이터베이스를 변환하거나, 들어오는 데이터에 인코딩 변환기를 설치하거나, 인코딩 감지 코드를 써야 할 수도 있다.
Python의 Universal Encoding Detector(Ruby 포트는 chardet gem)가 뛰어난 자동 감지 라이브러리다.
일단 모든 데이터를 Unicode 인코딩으로 유지하면 대부분의 문제가 사라진다.
이상한 인코딩으로 들어온 데이터는 선택한 UTF-* 인코딩으로 변환할 수 있고, 인코딩을 명시하지 않은 데이터는 추정해 변환하거나 이해 불가로 거부할 수 있다.

나머지 절반은 나가는 표현에서 어떤 인코딩을 쓰는지 클라이언트에게 알리는 것이다.
XML은 첫 줄에 문자 인코딩을 명시할 수 있다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

권장 표현 포맷 중 하나를 제외한 모두가 XML 기반이므로 이것으로 문제 대부분이 해결된다.
그러나 그 예외 하나에 인코딩 문제가 있고, XML과 HTTP의 관계에도 추가 문제가 있다.

#### XML과 HTTP: 인코딩의 충돌

XML 문서는 첫 줄에 인코딩을 정의할 수 있고 그래야 한다.
HTTP 응답은 `Content-Type` 헤더 값을 지정할 수 있고 그래야 한다.
그런데 `Content-Type`은 `charset`으로 문서 인코딩도 지정할 수 있고, 이것이 문서 자체에 적힌 것과 충돌할 수 있다.

```text
Content-Type: application/xml; charset="ebcdic-fr-297+euro"

<?xml version="1.0" encoding="UTF-8"?>
```

누가 이길까?
놀랍게도 HTTP의 문자 인코딩이 문서 자체의 인코딩보다 우선한다(RFC 3023에 명시되어 있다).
문서가 “UTF-8”이라 하고 `Content-Type`이 “ebcdic-fr-297+euro”라 하면 확장 프랑스어 EBCDIC이 된다.
거의 아무도 이런 결과를 예상하지 않고 대부분의 프로그래머는 RFC를 나중에야 확인하므로, `Content-Type`의 인코딩은 신뢰하기 어려운 경향이 있다.

XML 문서를 제공할 때 저자는 `Content-Type`에 문자 인코딩을 굳이 넣기를 권하지 않는다.
정말 확실하다면 넣어도 되지만 큰 도움은 되지 않는다.
정말 중요한 것은 문서 인코딩을 명시하는 것이다.
클라이언트를 작성한다면 `Content-Type`에 명시된 인코딩이 틀릴 수 있음을 유념하고, RFC의 반직관적 규칙에 의존하기보다 상식으로 어느 선언을 믿을지 판단하라.
또한 XML 문서는 `text/xml`이 아니라 `application/xml`로 제공해야 한다.
`text/xml`에 charset이 없으면 올바른 클라이언트 동작은 XML 문서 안의 인코딩을 완전히 무시하고 US-ASCII로 해석하는 것이기 때문이다.

#### JSON 문서의 문자 인코딩

권장 포맷 목록에 평문(plain text)을 넣지 않은 것은 구조가 없기 때문이며, 구조가 없으면 인코딩을 명시할 방법도 없기 때문이다.
JSON은 평문을 구조화하는 방법이지만 인코딩 문제를 스스로 풀지는 않는다.
다행히 표준 규약을 따르면 된다.
RFC 4627은 JSON 파일이 UTF-* 인코딩 중 하나로 인코딩된 Unicode 문자를 담아야 한다고 규정한다.
실질적으로 UTF-8이거나 바이트 순서 표시가 붙은 UTF-16이며, ASCII는 유효한 UTF-8이므로 US-ASCII도 동작한다.
이 제약 덕에 클라이언트는 처음 4바이트만 보고 인코딩을 판정할 수 있어 명시적 인코딩이 필요 없다.
JSON뿐 아니라 평문을 제공할 때 언제나 이 규약을 따라야 한다.

## 사전 포장된 제어 흐름

HTTP에는 균일 인터페이스뿐 아니라 표준 응답 코드 집합, 즉 요청이 끝날 수 있는 가능한 방식들이 있다.
리소스는 무엇이든 될 수 있지만 대개 데이터베이스 테이블과 그 행, 출판물과 그것이 발행하는 글 같은 몇 가지 넓은 범주에 든다.
서비스가 어떤 종류의 리소스를 노출하는지 알면 리소스를 자세히 몰라도 HTTP 요청에 대한 가능한 응답을 예측할 수 있다.

표준 HTTP 응답 코드는 어떤 요청이 오면 무엇을 할지에 대한 제안된 제어 흐름이지만 조언이 막연하다.
여기서는 리소스 설계, 표현 포맷, 응답 코드에 대한 조언을 묶어 실제 서비스를 설계하도록 돕는 여러 사전 포장된 제어 흐름을 제시한다.

### 일반 규칙

이 규칙들은 리소스의 실제 성격과 무관하므로 거의 모든 서비스에 적용할 수 있다.
정상 요청 처리 이전에 실행되는 공통 코드로 구현할 수 있다.

- 클라이언트가 올바른 인가 없이 무언가를 하려 하면 401(“Unauthorized”)과 함께 Authorization 헤더를 올바로 구성하는 지침을 보낸다.
- 클라이언트가 어떤 리소스에도 해당하지 않는 URI에 접근하려 하면 404(“Not Found”)를 보낸다. 유일한 예외는 클라이언트가 그 URI에 새 리소스를 PUT하려는 경우다.
- 클라이언트가 리소스가 지원하지 않는 균일 인터페이스의 일부를 쓰려 하면 405(“Method Not Allowed”)를 보낸다. 읽기 전용 리소스를 DELETE하려 할 때의 올바른 응답이다.

### 데이터베이스 기반 제어 흐름

많은 웹 서비스에서 리소스는 SQL 데이터베이스의 무언가(행, 테이블, 데이터베이스 전체)와 강하게 연결된다.
이런 서비스는 매우 흔해 Rails 같은 프레임워크 전체가 이를 쉽게 작성하도록 맞춰져 있다.
설계가 비슷하므로 제어 흐름도 비슷한 것이 타당하다.
예컨대 들어온 요청이 말이 안 되는 표현을 담으면 올바른 응답은 거의 확실히 415(“Unsupported Media Type”) 또는 400(“Bad Request”)이다.

다음은 일반 규칙 위에서 동작하는, 데이터베이스 기반 애플리케이션의 균일 인터페이스용 표준 제어 흐름이다.

- GET: 리소스를 식별할 수 있으면 표현과 함께 200(“OK”)을 보낸다. 조건부 GET을 꼭 지원하라.
- PUT(기존 리소스): 표현을 파싱해 이 리소스 상태에 대한 일련의 변경으로 바꾼다. 변경이 리소스를 불완전·불일치 상태로 남기면 400(“Bad Request”), 다른 리소스와 충돌하면 409(“Conflict”)를 보낸다. 소셜 북마킹 서비스는 이미 쓰이는 이름으로 사용자명을 바꾸려 하면 409를 보낸다. 문제가 없으면 변경을 적용한다. 변경으로 리소스가 다른 URI에서 제공되면 301(“Moved Permanently”)과 함께 Location 헤더에 새 URI를 담고, 그렇지 않으면 200(“OK”)을 보낸다. 이후 옛 URI 요청은 301, 404, 410(“Gone”) 중 하나가 된다.
- PUT(리소스 없는 URI): 404를 반환하거나 그 URI에 리소스를 생성한다. 생성한다면 표현을 파싱해 초기 상태를 만들고 201(“Created”)을, 정보가 부족하면 400을 보낸다.
- POST(새 리소스 생성): 표현을 파싱해 적절한 URI를 골라 새 리소스를 만든다. 201(“Created”)과 함께 새 리소스의 URI를 Location 헤더에 담는다. 정보가 부족하면 400, 기존 리소스와 충돌하면 409와 함께 문제 리소스를 가리키는 Location 헤더를 보낸다.
- POST(리소스에 덧붙이기): 표현을 파싱한다. 말이 안 되면 400, 아니면 리소스 상태에 정보를 반영하고 200(“OK”)을 보낸다.
- DELETE: 200(“OK”)을 보낸다.

### Atom 출판 프로토콜(APP)

Atom이 출판의 의미를 기술하는 XML 어휘라면, Atom 출판 프로토콜(Atom Publishing Protocol, APP)은 출판의 과정을 담아내는 리소스 집합을 정의한다.
글을 사이트에 올리고, 편집하고, 카테고리를 지정하고, 삭제하는 등의 과정이다.
분명한 응용 대상은 블로그, 사진 앨범, 콘텐츠 관리 시스템 같은 온라인 출판 전반이다.
APP는 네 종류의 리소스를 정의하고, 그 일부가 균일 인터페이스 아래에서 어떻게 동작하는지 규정하며, 주고받을 표현 문서를 정의한다.
URI 설계나 문서에 들어갈 데이터에 대해서는 말하지 않으며 그것은 개별 애플리케이션의 몫이다.

APP는 HTTP의 균일 인터페이스 위에 더 상위의 균일 인터페이스를 얹는다.
많은 애플리케이션이 APP를 따를 수 있고, 범용 APP 클라이언트는 그 모두에 접근할 수 있어야 한다.
개별 애플리케이션은 리소스를 추가하거나 APP 리소스가 더 많은 균일 인터페이스를 노출하게 해 APP를 확장할 수 있지만, APP 표준의 최소 기능은 모두 지원해야 한다.
APP는 Atom 문서에 대응하는 두 리소스와, 클라이언트가 APP 리소스를 찾고 수정하도록 돕는 두 리소스를 정의한다.

#### 컬렉션(Collections)

APP 컬렉션은 표현이 Atom 피드인 리소스다.
피드 리더에서 구독하는 Atom 피드와 APP 클라이언트로 조작하는 Atom 피드 사이에 본질적 차이는 없다.
컬렉션은 APP가 멤버(member)라 부르는 데이터 조각들의 목록 또는 묶음이며, APP는 이 “컬렉션” 유형 리소스 조작에 강하게 맞춰져 있다.
APP는 컬렉션의 GET과 POST 응답을 정의한다.
GET은 Atom 피드 표현을 반환하고, POST는 새 멤버를 추가해 보통 피드에 새 엔트리로 나타난다.
컬렉션을 DELETE하거나 PUT으로 설정을 바꾸는 것은 APP가 다루지 않으며 애플리케이션의 몫이다.

#### 멤버(Members)

컬렉션은 멤버의 모음이다.
멤버는 Atom 피드의 엔트리(블로그 글, 뉴스 기사, 북마크)에 대략 대응한다.
그러나 사진, 노래, 영화, Word 문서처럼 Atom 문서에 XML로 담을 수 없는 이진 포맷일 수도 있다.
클라이언트는 멤버 표현을 컬렉션 URI에 POST해 컬렉션 안에 멤버를 만든다.
멤버는 컬렉션의 종속(subordinate) 리소스로 생성되며, 서버가 새 멤버에 URI를 부여한다.
POST 응답은 201(“Created”)과 새 리소스 위치를 알리는 Location 헤더를 담는다.

다음은 컬렉션에 POST하기 적합한 독립 Atom 엔트리 문서다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<entry>
  <title>New Resource Will Respond to PUT, City Says</title>
  <summary>
    After long negotiations, city officials say the new resource
    being built in the town square will respond to PUT.
  </summary>
  <category scheme="http://www.example.com/categories/RestfulNews"
    term="local" label="Local news" />
</entry>
```

#### 서비스 문서(Service document)

이 리소스는 컬렉션의 묶음일 뿐이다.
모든 컬렉션을 나열하는 단일 서비스 문서를 서비스의 “홈페이지”로 제공하는 것이 흔한 방식이다.
서비스 문서는 특정 어휘로 작성된 XML 문서이며 미디어 타입은 `application/atomserv+xml`이다.
다음은 세 컬렉션을 기술하는 서비스 문서다.
하나는 Atom 엔트리 문서일 때 POST를 받는 “RESTful News” 블로그, 나머지 둘은 이미지 파일일 때 POST를 받는 개인 사진 앨범이다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<service xmlns="http://purl.org/atom/app#"
  xmlns:atom="http://www.w3.org/2005/Atom">
  <workspace>
    <atom:title>Weblogs</atom:title>
    <collection href="http://www.example.com/RestfulNews">
      <atom:title>RESTful News</atom:title>
      <categories href="http://www.example.com/categories/RestfulNews" />
    </collection>
  </workspace>
  <workspace>
    <atom:title>Photo galleries</atom:title>
    <collection href="http://www.example.com/samruby/photos">
      <atom:title>Sam's photos</atom:title>
      <accept>image/*</accept>
      <categories href="http://www.example.com/categories/samruby-photo" />
    </collection>
    <collection href="http://www.example.com/leonardr/photos">
      <atom:title>Leonard's photos</atom:title>
      <accept>image/*</accept>
      <categories href="http://www.example.com/categories/leonardr-photo" />
    </collection>
  </workspace>
</service>
```

컬렉션이 어떤 POST를 받을지는 `accept` 태그로 안다.
`accept`는 HTTP `Accept` 헤더와 비슷하지만 방향이 반대다.
`Accept` 헤더는 보통 클라이언트가 GET과 함께 보내 이해하는 표현 포맷을 서버에 알리지만, `accept` 태그는 서버가 새 멤버를 만드는 POST에서 컬렉션이 받아들일 표현을 클라이언트에게 알린다.
사진 갤러리 둘은 `image/*`를 지정해 이미지일 때만 POST를 받는다.
RESTful News는 `accept`가 없는데, APP 기본값은 컬렉션이 Atom 엔트리 문서일 때만 POST를 받는 것이다.

서비스 문서의 또 다른 중요한 부분은 “카테고리 문서” 리소스로 링크하는 `categories` 태그다.
APP는 서비스 문서의 표현 포맷을 규정하고 GET에 응답해야 한다고 말할 뿐, 문서가 어떻게 서버에 올라오는지는 규정하지 않는다.
미리 하드코딩하든, 새 리소스에 POST해 만들 수 있게 하든, 정적 파일로 노출하든, PUT/DELETE에 응답하게 하든 자유다.
서비스 문서는 컬렉션을 워크스페이스(workspace)로 묶기도 하지만, APP는 워크스페이스를 리소스로 정의하지 않아 고유 URI가 없으며 서비스 문서 표현의 요소로만 존재한다.

#### 카테고리 문서(Category documents)

APP 멤버(Atom 요소에 대응)는 카테고리로 분류될 수 있다.
어떤 카테고리가 존재하는지 누가 정하는가에 대한 답이 카테고리 문서다.
앞의 Atom 엔트리는 카테고리에 `http://www.example.com/categories/RestfulNews`라는 scheme을 주었고, 서비스 문서의 해당 컬렉션도 `categories` 태그에 같은 URI를 주었다.
그 URI가 카테고리 문서를 가리키며, 이는 특정 APP 컬렉션의 카테고리 어휘를 나열한다.
미디어 타입은 `application/atomcat+xml`이다.

```xml
<?xml version="1.0" ?>
<app:categories
  xmlns:app="http://purl.org/atom/app#"
  xmlns="http://www.w3.org/2005/Atom"
  scheme="http://www.example.com/categories/RestfulNews"
  fixed="no">
  <category term="local" label="Local news"/>
  <category term="international" label="International news"/>
  <category term="lighterside" label="The lighter side of REST"/>
</app:categories>
```

`fixed=“no”`는 이 문서에 없는 카테고리에 속한 멤버도 컬렉션에 게시할 수 있음을 뜻한다.
APP는 카테고리 문서의 표현 포맷을 정의하고 GET만 정의할 뿐, 생성·수정·삭제는 규정하지 않는다.

#### APP 멤버로서의 이진 문서

사진 갤러리에 이미지 파일을 POST해 멤버를 만든다고 했는데, 이미지는 이진 문서라 Atom 피드에 담을 수 없다.
그 해법은 하나의 리소스가 여러 표현을 가질 수 있다는 점이다.
업로드하는 사진 하나는 두 표현을 가진다.
하나는 이진 사진이고, 다른 하나는 메타데이터를 담은 XML 문서(Atom 엔트리)이며, 피드에 나타나는 것은 후자다.

JPEG 파일을 사진 갤러리 컬렉션에 POST하는 예는 다음과 같다.

```text
POST /leonardr/photos HTTP/1.1
Host: www.example.com
Content-type: image/jpeg
Content-length: 62811
Slug: A picture of my guinea pig

[JPEG file goes here]
```

`Slug`는 APP가 정의한 커스텀 HTTP 헤더로, 업로드하며 사진 제목을 지정하게 한다.
응답은 201과 새로 만든 APP 멤버의 URI를 담은 Location 헤더로 온다.

```text
201 Created
Location: http://www.example.com/leonardr/photos/my-guinea-pig.atom
```

그 URI 끝에 있는 것은 업로드한 JPEG가 아니라 그것을 기술하고 링크하는 Atom 엔트리 문서다.

```xml
<?xml version="1.0" encoding="utf-8"?>
<entry>
  <title>A picture of my guinea pig</title>
  <updated>2007-01-24T11:52:29Z</updated>
  <id>urn:f1ef2e50-8ec8-0129-b1a7-003065546f18</id>
  <summary></summary>
  <link rel="edit-media" type="image/jpeg"
    href="http://www.example.com/leonardr/photos/my-guinea-pig.jpg" />
</entry>
```

실제 JPEG는 그 링크 끝에 있다.
GET으로 가져오거나 PUT으로 다른 이미지로 덮어쓸 수 있다.
메타데이터 표현의 상태 요소에는 제목(Slug에서 온 것, 나중에 변경 가능), 요약(처음 비어 있고 변경 가능), “마지막 갱신” 시각(임의로 못 바꿈), 이미지 표현의 URI(Slug 기반으로 서버가 선택), 고유 ID(서버가 단독 선택)가 있다.
이 메타데이터 문서는 피드에 포함되며, 수정 후 PUT해 작성자 지정·카테고리 추가·제목 변경 등을 할 수 있다.
두 URI 중 하나에 DELETE를 보내 멤버를 삭제할 수도 있다.

APP는 이렇게 이진 데이터를 두 부분으로 나눈다.
Atom 피드에 담을 수 없는 이진 부분과 담을 수 있는 메타데이터 부분이다.
출판 메타데이터(카테고리, 요약 등)가 뉴스 기사만큼 사진·영화에도 잘 들어맞기에 성립한다.
APP 표준은 이를 두 리소스, 즉 표현이 Atom 문서인 “Media Link Entry”와 표현이 이진 파일인 “Media Resource”로 기술하지만, 저자는 두 표현을 가진 하나의 리소스로 설명한다.
차이는 순전히 철학적이며 실제 HTTP 요청·응답에는 영향이 없다.

#### 정리(APP 리소스와 메서드)

APP는 목록/피드/컬렉션에 항목/요소/멤버가 계속 추가되는 흔한 문제를 잘 다듬은 방식이다.
문제가 이 영역에 맞으면 비슷한 것을 다시 발명하기보다 APP를 쓰는 편이 쉽고 기존 클라이언트 지원의 이점을 얻는다.

| 리소스        | GET                                                             | POST         | PUT                         | DELETE    |
| ------------- | --------------------------------------------------------------- | ------------ | --------------------------- | --------- |
| 서비스 문서   | 표현 반환(XML)                                                  | 미정의       | 미정의                      | 미정의    |
| 카테고리 문서 | 표현 반환(XML)                                                  | 미정의       | 미정의                      | 미정의    |
| 컬렉션        | 표현 반환(Atom 피드)                                            | 새 멤버 생성 | 미정의                      | 미정의    |
| 멤버          | 이 URI가 식별하는 표현 반환(보통 Atom 엔트리, 이진 파일일 수도) | 미정의       | 이 URI가 식별하는 표현 갱신 | 멤버 삭제 |

#### GData

APP는 소수의 리소스와 연산만 정의해 확장 여지가 크다.
그 확장 중 하나가 구글의 GData로, 새로운 종류의 리소스와 인가 메커니즘 같은 부가 기능을 더한다.
집필 시점에 Blogger, Google Calendar, Google Code Search, Google Spreadsheets가 모두 같은 인터페이스, 즉 GData 확장을 얹은 APP를 노출했다.
구글에서 일하지 않는 한 정확한 GData 인터페이스를 만들 일은 없겠지만, 클라이언트 쪽에서 마주칠 수 있고 APP를 어떻게 확장하는지 보는 것이 유용하다.

GData의 가장 큰 변화는 새로운 리소스인 검색 결과 목록을 노출하는 것이다.
APP는 컬렉션 URI에 GET하면 멤버 일부의 표현을 얻는다고만 정하고, 특정 부분집합을 찾거나 전문 검색을 하는 방법은 정하지 않는다.
GData가 이 빈칸을 메운다.
GData는 각 APP 컬렉션에 대해 다양하게 잘라 보는 무한한 추가 리소스를 노출한다.
예컨대 `http://www.example.com/RestfulNews?q=stadium`은 본문에 “stadium”이 든 멤버의 부분집합을, `.../RestfulNews/-/local`은 “local”로 분류된 부분집합을, `?author=Tom%20Servo&max-results=50`은 작성자가 “Tom Servo”인 멤버 최대 50개를 준다.
검색 결과는 보통 Atom 피드로 표현되며, 맞은 멤버마다 entry 요소를 담고 총 개수와 페이지 크기를 담는 OpenSearch 요소도 포함한다.

GData는 자체 `gd` 네임스페이스에 도메인 특화 데이터를 위한 XML 요소도 정의한다.
Google Calendar에서 컬렉션은 누군가의 달력이고 멤버는 이벤트다.
이벤트에는 일반적인 Atom 필드 외에 `gd:when`, `gd:who`, `gd:recurrence` 같은 달력 특화 데이터가 들어간다.
클라이언트가 이 확장을 이해하면 달력 클라이언트로, APP만 이해하면 일반 APP 클라이언트로, 기본 Atom만 이해하면 이벤트 목록을 Atom 피드로 다룰 수 있다.

### POST Once Exactly(POE)

POST는 신뢰성 있는 HTTP의 골칫거리다.
GET, PUT, DELETE는 처음에 전달되지 않았어도 다시 보낼 수 있다.
GET은 심각한 부작용이 없고, PUT과 DELETE는 한 번 보내든 여러 번 보내든 리소스 상태에 같은 효과를 낸다.
그러나 POST는 무엇이든 할 수 있고 두 번 보내면 한 번과 다른 효과를 낼 수 있다.

POST Once Exactly(POE)는 POST를 PUT, DELETE처럼 멱등(idempotent)하게 만드는 방법이다.
POE를 지원하는 리소스는 평생 단 한 번만 POST에 성공적으로 응답하고, 이후 모든 POST에는 405(“Method Not Allowed”)를 준다.
POE 리소스는 단일 POST 요청을 처리할 목적으로 노출된 일회용 리소스다.
POE는 Mark Nottingham이 IETF 초안으로 정의했으나 2005년 만료되었다.

POST에 응답해 새 블로그 글을 만드는 “weblog” 리소스를 생각해 보자.
weblog 자체가 POST를 노출하면 글이 하나만 생길 수 있으므로 그럴 수 없다.
POE에서는 클라이언트가 먼저 특별한 POE 헤더를 담아 GET이나 HEAD를 보낸다.

```text
HEAD /weblogs/myweblog HTTP/1.1
Host: www.example.com
POE: 1
```

응답은 아직 POST되지 않은 POE 리소스의 URI를 담는다.
이 URI는 미래의 POST 요청을 위한 고유 ID일 뿐이며 서버에 존재하지도 않을 수 있다.
GET은 안전한 연산이므로 이 GET이 서버 상태를 바꾸지 않았다.

```text
200 OK
POE-Links: /weblogs/myweblog/entry-factory-104a4ed
```

`POE`와 `POE-Links`는 POE 초안이 정의한 커스텀 HTTP 헤더다.
`POE`는 클라이언트가 POE 리소스로의 링크를 기대함을 서버에 알리고, `POE-Links`는 하나 이상의 POE 리소스 링크를 준다.
클라이언트는 새 글 표현을 `/weblogs/myweblog/entry-factory-104a4ed`에 POST할 수 있고, POST가 처리되면 그 URI는 이후 POST에 405로 응답한다.
POST가 전달됐는지 확실치 않으면 안전하게 다시 보낼 수 있으며, 두 번째 POST가 두 번째 글을 만들 가능성은 없다.
POST가 멱등해진 것이다.

POE의 장점은 오버로드된 POST와도 동작한다는 것이다.
리소스 지향 아키텍처를 완전히 위반하는 방식으로 POST를 쓰더라도, 오버로드된 POST 연산을 POE로 노출하면 클라이언트는 HTTP를 신뢰성 있는 프로토콜로 쓸 수 있다.
POST를 멱등하게 만드는 대안은 POST를 아예 없애는 것이다.
POST는 클라이언트가 어디에 PUT할지 모를 때만 필요하다.
POE가 각 POST 연산에 고유 ID를 만들어 주듯, 클라이언트가 스스로 고유 ID를 만들 수 있게 하면 PUT을 대신 쓸 수 있다.
두 클라이언트가 결코 같은 ID를 만들지 않도록만 보장하면 POST를 전혀 노출하지 않고도 POE의 이점을 얻는다.

## 하이퍼미디어 기술

하이퍼미디어에는 두 종류, 링크와 폼이 있다.
링크는 현재 리소스와 URI로 식별되는 대상 리소스 사이의 연결이며, 덜 형식적으로는 표현 본문에 담긴 URI다.
JSON과 평문조차 텍스트에 URI를 담을 수 있어 일종의 하이퍼미디어 포맷이지만, 이 책에서 “하이퍼미디어 포맷”은 링크와 폼에 대한 구조적 지원이 있는 포맷을 뜻한다.

폼도 두 종류다.
첫째는 애플리케이션 폼(application form)으로, 애플리케이션 상태를 조작하는 방법을 보여준다.
이름이 패턴을 따르는 리소스를 다루는 방식이며, 목적지가 여럿인 링크처럼 작동한다.
검색 엔진은 가능한 모든 검색으로 링크하지 않고, 검색어를 입력할 폼을 준다.
폼을 제출하면 브라우저가 입력에서 URI(예: `http://www.google.com/search?q=jellyfish`)를 구성해 GET한다.
애플리케이션 폼은 무한히 큰 표현 없이 한 리소스가 무한한 리소스로 링크하게 한다.

둘째는 리소스 폼(resource form)으로, 리소스 상태를 바꾸는 표현을 어떻게 구성할지 보여준다.
GET과 DELETE는 표현이 필요 없지만 POST와 PUT은 종종 필요하며, 리소스 폼은 그 표현이 어떤 모습이어야 하는지 말한다.

링크와 애플리케이션 폼은 저자가 말하는 연결성(connectedness), Fielding의 논문이 말하는 “애플리케이션 상태의 엔진으로서의 하이퍼미디어”를 구현한다.
애플리케이션 상태는 클라이언트가 쥐고 있지만, 서버는 링크와 폼을 보내 가능한 다음 상태를 제안할 수 있다.
반면 리소스 폼은 궁극적으로 서버에 있는 리소스 상태를 바꾸는 안내다.

이 절은 네 가지 하이퍼미디어 기술을 다룬다.
집필 시점에 실사용 중인 것은 XHTML 4뿐이다.
XHTML 5는 발표되면 널리 쓰일 것이 확실하고, URI Templates도 XHTML 5에 편입되든 아니든 자리 잡을 것으로 저자는 추측한다.
WADL은 자리 잡을 수도, XHTML 5와 마이크로포맷의 조합에 밀려날 수도 있다.

### URI Templates

URI Templates(당시 인터넷 초안)는 단순한 리소스 폼을 링크처럼 보이게 하는 기술이다.
비슷한 URI를 무한히 보여줄 때 이 구문을 썼다.
예컨대 Amazon S3 서비스는 다음과 같다.

```text
https://s3.amazonaws.com/{name-of-bucket}/{name-of-object}
```

중괄호는 URI에서 유효하지 않아 이 문자열은 유효한 URI가 아니지만 유효한 URI Template이다.
`{name-of-bucket}`은 변수 값으로 대체될 빈칸이다.
이 하나의 템플릿 안에 무한한 URI가 숨어 있다.
URI Templates는 URI로 빈칸 채우기를 정밀하게 해 준다.
이것이 없으면 클라이언트는 영어 설명에 기반한 사전 프로그래밍된 URI 구성 규칙에 의존해야 한다.
URI Templates는 데이터 포맷이 아니지만 어떤 데이터 포맷이든 이를 허용해 하이퍼미디어 능력을 높일 수 있다.
XHTML 5에 URI Templates를 지원하려는 제안이 있고 WADL은 이미 지원한다.

### XHTML 4

HTML은 역대 가장 성공한 하이퍼미디어 포맷이지만, 사람의 웹에서의 성공이 그것을 지저분한 포맷으로 낙인찍어 사람들이 더 구조적인 XML로 향하게 했다.
타협 표준이 XHTML로, HTML과 같은 태그·속성을 쓰는 XML 어휘다.
HTML과 거의 같아 강력한 하이퍼미디어 기능을 가지지만 폼은 다소 빈약하다.

#### XHTML 4 링크

여러 HTML 태그가 링크에 쓰이지만(예: `img`) 주된 둘은 `link`와 `a`다.
`link` 태그는 문서 head에 나타나 문서 전체를 어떤 리소스에 연결하며, 텍스트나 다른 태그를 담지 않는다.
`a` 태그는 body에 나타나 텍스트와 다른 태그를 담을 수 있고, 문서 전체가 아니라 자신의 내용을 다른 리소스에 연결한다.

```html
<!DOCTYPE html
  PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <link rel="alternate" type="application/atom+xml" href="atom.xml">
  <link rel="stylesheet" href="display.css">
</head>
<body>
  <p>
    Have you read
    <a href="Great-Expectations.html"><i>Great Expectations</i></a>?
  </p>
</body>
</html>
```

`link`와 `a`의 중요한 세 속성은 `href`, `rel`, `rev`다.
`href`가 가장 중요하며 링크할 리소스의 URI를 준다.
`href`가 없으면 하이퍼링크가 아니다.
`rel`은 외부 URI가 이 문서에 대해 갖는 관계 의미를 더한다.
위 예에서 `atom.xml`의 관계는 “alternate”(리소스의 대체 표현), `display.css`의 관계는 “stylesheet”(표시용 서식 지침)로, 둘 다 HTML 4의 15가지 정의 값에 속한다.
마이크로포맷은 종종 추가 `rel` 값을 정의한다(예: rel-nofollow의 “nofollow”).
`rev`는 `rel`의 정반대로, 이 문서가 외부 URI에 대해 갖는 관계를 설명한다.
VoteLinks는 `rev`를 “vote-for”나 “vote-against”로 두어 URI에 대한 의견을 표현한다.
`rel`과 `rev`의 차이를 보여주는 예는 다음과 같다.

```html
<a rel="parent" href="/Dad">My father</a>
<a rev="child" href="/Dad">My father</a>
```

#### XHTML 4 폼

이 폼들이 사람의 웹을 이끈다.
HTML 폼은 `form` 태그로 기술한다.
`form`에는 제출 시 쓸 HTTP 메서드를 지정하는 `method` 속성, 접근할 리소스의 (기본) URI를 주는 `action` 속성, 함께 보낼 표현의 미디어 타입을 주는 `enctype` 속성이 있다.
`form`은 `input`, `select` 같은 폼 요소를 담고, 이들은 브라우저에서 텍스트 입력·체크박스·버튼 등의 GUI로 나타난다.
애플리케이션 폼에서는 입력값이 GET 요청의 최종 목적지를 구성하는 데 쓰인다.

```html
<form method="GET" action="http://search.example.com/search">
  <input name="query" type="text" />
  <input type="submit" />
</form>
```

이 애플리케이션 폼은 특정 리소스를 조작하지 않는다.
`action`의 URI를 사용자 생성 URI를 가진 무한한 리소스로의 도약대로 삼는다.
HTML 4의 리소스 폼은 특정 리소스를 식별하고 `action`을 POST로 지정한다.
폼 요소는 POST와 함께 보낼 표현을 구성하는 데 쓰인다.

```html
<form method="POST" action="http://files.example.com/dir/subdir/"
  enctype="multipart/form-data">
  <input type="text" name="description" />
  <input type="file" name="newfile" />
</form>
```

이 폼은 `http://files.example.com/dir/subdir/`라는 “디렉터리” 리소스의 종속 리소스로 새 “파일” 리소스를 만들도록 설계되었다.
표현 포맷은 텍스트 설명과 (이진일 수 있는) 파일을 담은 `multipart/form-data` 문서다.

#### XHTML 4의 한계

HTML 4의 하이퍼미디어 기능은 오늘의 사람의 웹을 이루기에는 충분하지만 웹 서비스에는 부족하다.
폼에 대한 주요 문제는 다섯 가지다.

1. 애플리케이션 폼이 표현할 수 있는 URI가 제한적이다. 기본 URI에 키-값 쌍을 덧붙이는 형태뿐이라 `.../search?q=jellyfish`는 “링크”할 수 있어도 `.../search/jellyfish`는 안 된다. 변수는 질의 문자열에 키-값 쌍으로 들어가야 한다.
2. HTML 4의 리소스 폼은 HTTP POST만 쓸 수 있다. 폼으로 DELETE를 보내라고 하거나 PUT 표현이 어때야 하는지 보여줄 방법이 없다. 사람의 웹은 안전한 연산에 GET, 나머지에 오버로드된 POST를 쓰는, 웹 서비스 전체와는 다른 균일 인터페이스를 쓴다. HTML 4 폼으로 HTTP의 균일 인터페이스를 얻으려면 오버로드된 POST로 PUT과 DELETE를 흉내 내야 한다.
3. 클라이언트가 요청과 함께 보낼 HTTP 헤더를 폼으로 기술할 방법이 없다. 폼 요소 값이 특정 요청 헤더로 들어가게 할 수 없다. APP는 새 멤버를 만드는 POST를 위해 별도 요청 헤더 Slug를 정의했는데, 엔티티 본문이 이진 파일일 수 있어 새 헤더를 정의한 것이다.
4. 키-값 쌍보다 복잡한 표현을 폼으로 지정할 수 없다. “file” 요소를 빼면 모든 폼 요소가 키-값 쌍으로 변환되도록 설계되었다. HTML 표준은 폼 표현에 두 콘텐츠 타입, 키-값 쌍용 `application/x-www-form-urlencoded`와 키-값 쌍 및 업로드 파일 조합용 `multipart/form-data`를 정의한다. `enctype`을 `application/xml`로 두어 XML을 POST하라고 말할 수는 있지만, 그 XML 안에 무엇이 들어가야 하는지 전달할 방법은 없다(키-값 쌍의 XML 표현이 아닌 한). 폼 요소를 중첩하거나 더 복잡한 데이터 구조를 나타내는 요소를 새로 정의할 수 없다.
5. HTML 폼에 반복 필드를 정의할 수 없다. 같은 필드를 두 번, 열 번 정의할 수는 있어도 결국 멈춰야 한다. “이 키-값 쌍에는 원하는 만큼 값을 지정해도 된다”라고 클라이언트에게 말할 방법이 없다.

### XHTML 5

HTML 5는 프로그래밍 가능한 웹에서 HTML을 쓸 때 생기는 여러 문제를 해결한다.
주된 문제는 일정이다.
공식 추정으로는 2008년 말 W3C Proposed Recommendation이 되지만 보수적 추정은 2022년까지 미뤄지며, 어느 쪽이든 이 책 출간 시점에는 표준이 아니다.
진짜 문제는 실제 클라이언트가 언제 이 기능들을 지원하기 시작하느냐이며, 그전에 이 기능을 쓰면 클라이언트가 해석용 커스텀 코드를 작성해야 한다.

HTML 5 폼은 HTTP 균일 인터페이스의 네 기본 메서드 GET, POST, PUT, DELETE를 모두 지원한다.
대부분의 브라우저가 이미 PUT과 DELETE 요청을 보낼 수 있어 오늘날 가장 지원하기 쉬운 기능이다.
아직 HTML 5에 편입되지 않은 제안 하나는 폼이 URI Templates를 쓰게 한다.
이 제안에서 애플리케이션 폼은 `action`이 아닌 `template` 속성에 `http://search.example.com/search/{q}` 같은 URI Template을 두고 `q`를 폼 안 텍스트 필드로 정의할 수 있어, `.../search/jellyfish`로 “링크”할 수 있게 된다.

HTML 4 폼은 같은 이름의 폼 요소를 여러 개 지정해 여러 값을 제출할 수 있게 하지만 개수가 유한하다.
HTML 5 폼은 “repetition model”을 지원해 같은 키를 원하는 만큼 제출해도 된다고 클라이언트에게 알린다.
끝으로 HTML 5는 키-값 쌍을 표현으로 직렬화하는 두 새 방식, 즉 평문과 새로 정의된 XML 어휘(콘텐츠 타입 `application/x-www-form+xml`)를 정의한다.
다만 이는 생각만큼 큰 진전은 아니다.
`input` 같은 폼 엔티티는 여전히 데이터를 키-값 쌍으로 얻는 수단이고, 새 직렬화 포맷은 그 키-값 쌍을 나타내는 새 방식일 뿐이다.
콘텐츠 타입만으로 포맷을 알아낼 수 없는 한, 더 복잡한 표현을 어떻게 구성할지 클라이언트에게 보여줄 방법은 여전히 없다.

HTML 5가 될 표준은 WHATWG(Web Hypertext Application Technology Working Group)가 개발하며, 총괄 표준은 Web Applications 1.0이지만 하이퍼미디어 능력 변화는 모두 Web Forms 2.0 표준에 담겨 있다.

### WADL

Web Application Description Language(WADL)는 HTTP 리소스의 동작을 표현하는 XML 어휘다.
SOAP 기반 RPC 스타일 서비스를 기술하는 XML 어휘인 Web Service Description Language(WSDL)에 빗대어 이름 붙였다.
APP 서비스 문서의 표현이 특정 어휘의 XML 문서로 리소스 집합(APP 컬렉션)과 허용 연산을 기술하듯, WADL은 어떤 리소스에 대해서든 APP 서비스 문서가 APP 컬렉션에 하는 일을 하는 표준 어휘다.

서비스가 노출하는 모든 리소스를 기술하는 WADL 파일을 제공할 수 있다.
이는 SOAP/WSDL 서비스의 WSDL 파일, 사람의 웹의 “사이트맵” 페이지에 대략 대응한다.
또는 HTML 표현에 HTML 폼을 넣듯, 특정 리소스의 XML 표현에 WADL 조각을 넣을 수 있고, 그 조각은 리소스 상태를 조작하는 법을 알려준다.

WADL은 웹 서비스의 클라이언트 작성을 쉽게 한다.
리소스의 WADL 기술은 그 리소스에 대한 여러 프로그래밍 언어 인터페이스를 대신할 수 있고, 적절한 언어의 WADL 클라이언트만 있으면 된다.
WADL은 HTTP 요청의 세부와 표현의 구성·파싱을 추상화하지만 HTTP의 균일 인터페이스를 숨기지는 않는다.
집필 시점에 WADL은 실제로 쓰이기보다 회자되는 편이었다.
Java 클라이언트 구현과 초보적 Ruby 클라이언트가 있었고, 기존 WADL 파일 대부분은 남의 RESTful·REST-RPC 서비스에 대한 비공식 기술이었다.

WADL은 하이퍼미디어 포맷으로서 HTML 5보다 낫다.
URI Templates와 모든 HTTP 메서드를 지원하고, 요청 시 특정 HTTP 헤더를 채우라고 지시할 수 있다.
더 중요하게, 키-값 쌍이 아닌 표현 포맷을 기술할 수 있다.
스키마 정의를 가리켜 XML 표현의 포맷을 지정하고, “키”가 XPath 문인 키-값 쌍으로 문서의 중요한 부분을 짚어낼 수 있다.
HTML로는 XML 표현의 포맷을 콘텐츠 타입을 달리하는 식으로만 지정할 수 있으니 이는 작지만 중요한 진전이다.
다만 이 진전은 XML에만 해당한다.
WADL로 리소스가 JSON을 주고받는다고 말할 수는 있지만, JSON이 해시(다시 키-값 쌍!)가 아닌 한 그 문서가 어때야 하는지 지정할 방법은 없다.
이는 XML 세계에서 스키마 정의로 풀린 일반 문제인데, 다른 포맷에서는 아직 풀리지 않았다.

#### del.icio.us 리소스 기술

다음은 Ruby의 WADL 라이브러리에 기반한 del.icio.us 클라이언트다.

```ruby
#!/usr/bin/ruby
# delicious-wadl-ruby.rb
require 'wadl'

if ARGV.size != 2
  puts "Usage: #{$0} [username] [password]"
  exit
end
username, password = ARGV

# Load an application from the WADL file
delicious = WADL::Application.from_wadl(open("delicious.wadl"))

# Give authentication information to the application
service = delicious.v1.with_basic_auth(username, password)

begin
  # Find the "recent posts" functionality
  recent_posts = service.posts.recent
  # For every recent post...
  recent_posts.get.representation.each_by_param('post') do |post|
    # Print its description and URI.
    puts "#{post.attributes['description']}: #{post.attributes['href']}"
  end
rescue WADL::Faults::AuthorizationRequired
  puts "Invalid authentication information!"
end
```

del.icio.us 서비스는 WADL 라이브러리가 `v1`로 식별하는 리소스를 노출하고, 그 아래 `posts.recent`로 식별되는 하위 리소스가 `https://api.del.icio.us/v1/posts/recent`에 대응한다.
그 리소스에 GET하면 XML 표현을 담은 응답 객체를 얻고, 그중 post들을 XML 요소로 처리해 description과 href를 뽑는다.

WADL 파일은 리소스 정의, 메서드 정의, 표현 정의 세 부분으로 나뉜다.
리소스 정의는 `recent`가 `posts` 안에, `posts`가 `v1` 안에 중첩된 형태다.

```xml
<?xml version="1.0"?>
<!-- This is a partial bootleg WADL file for the del.icio.us API. -->
<application xmlns="http://research.sun.com/wadl/2006/07">
  <!-- The resource -->
  <resources base="https://api.del.icio.us/">
    <doc xml:lang="en" title="The del.icio.us API v1">
      Post or retrieve your bookmarks from the social networking website.
      Limit requests to one per second.
    </doc>
    <resource path="v1">
      <param name="Authorization" style="header" required="true">
        <doc xml:lang="en">All del.icio.us API calls must be authenticated
          using Basic HTTP auth.</doc>
      </param>
      <resource path="posts">
        <resource path="recent">
          <method href="#getRecentPosts" />
        </resource>
      </resource>
    </resource>
  </resources>
</application>
```

`param` 태그는 HTML 폼 요소의 등가물로, 채워야 할 빈칸을 클라이언트에게 알린다.
여기서는 모든 호출에 Basic HTTP auth의 Authorization 헤더가 필요함을 나타낸다.
메서드 정의는 균일 인터페이스로 보낼 요청에 대응하며, `id`는 임의지만 `name`은 항상 HTTP 메서드 이름이다.

```xml
<!-- The method -->
<method id="getRecentPosts" name="GET">
  <doc xml:lang="en" title="Returns a list of the most recent posts." />
  <request>
    <param name="tag" style="form">
      <doc xml:lang="en" title="Filter by this tag." />
    </param>
    <param name="count" style="form" default="15">
      <doc xml:lang="en" title="Number of items to retrieve.">
        Maximum: 100
      </doc>
    </param>
  </request>
  <response>
    <representation href="#postList" />
    <fault id="AuthorizationRequired" status="401" />
  </response>
</method>
```

여기 두 `param`은 “query” 파라미터로, GET에서는 질의 문자열에 덧붙는다.
이 정의 덕에 WADL 클라이언트는 `.../recent?count=100`이나 `.../recent?tag=rest&count=20` 같은 URI에 접근할 수 있다.
이 메서드는 리소스 상태를 조작하는 것이 아니라 가능한 새 애플리케이션 상태를 가리키는 애플리케이션 폼이다.
PUT이나 POST에 대응한다면 그 `request`가 리소스 폼이 되어 함께 보낼 표현을 기술할 것이다.
`response`는 GET 시 돌아오는 응답 표현을 기술하고, 잘못된 Authorization이면 401을 받는다는 결함 조건도 기술한다.

표현 정의는 GET 시 받는 XML 문서를 기술한다.

```xml
<!-- The representation -->
<representation id="postList" mediaType="text/xml" element="posts">
  <param name="post" path="/posts/post" repeating="true" />
</representation>
</application>
```

콘텐츠 타입은 `text/xml`, 루트는 `posts` 태그이며, `param`의 `path` 속성은 클라이언트가 모든 post를 가져오는 데 쓸 XPath 식을 준다.
클라이언트의 `each_by_param('post')` 호출이 그 XPath를 문서에 적용해, XPath나 표현 구조를 몰라도 각 요소를 다루게 한다.
이 표현에는 스키마 정의가 없지만(단순해 형식을 짐작하게 함), 가령 XSD가 있다고 가정하면 표현을 스키마 파일로 정의할 수 있다.

```xml
<?xml version="1.0"?>
<!-- This is a partial bootleg WADL file for the del.icio.us API. -->
<application xmlns="http://research.sun.com/wadl/2006/07"
  xmlns:delicious="https://api.del.icio.us/v1/posts.xsd">
  <grammars>
    <include href="https://api.del.icio.us/v1/posts.xsd" />
  </grammars>
  <representation id="postList" mediaType="text/xml" element="delicious:posts" />
</application>
```

XSD 파일을 `grammars`에서 참조해 `delicious` 네임스페이스에 배정하고 표현의 `element` 속성을 그 네임스페이스로 한정하면, post 태그가 가득하다는 정보를 param으로 말할 필요가 없다.
그 정보가 XSD에 있기 때문이다.
XSD가 포맷을 완전히 기술해도 특히 중요한 부분을 짚기 위해 param을 정의할 수는 있다.

#### APP 컬렉션 기술

WADL로는 균일 인터페이스에 응답하는 어떤 리소스의 동작이든 기술할 수 있다.
앞서 WADL을 APP 서비스 문서에 견주었다.
둘 다 리소스를 기술하는 XML 어휘이며, 서비스 문서는 APP 컬렉션을, WADL 문서는 어떤 리소스든 기술한다.
WADL 표준 자체가 이 예를 제공하며(A.2절), 저자는 이를 단순화해 제시한다.

앞의 서비스 문서는 세 Atom 컬렉션을 기술한다.
하나는 POST로 Atom 엔트리를, 나머지 둘은 이미지 파일을 받는다.
객체지향 시스템에서 클래스 계층으로 차이를 뽑아내듯, WADL에서 두 리소스 타입을 정의한 뒤 그것으로 개별 리소스를 정의할 수 있다.

```xml
<?xml version="1.0"?>
<!-- This is a description of two common types of resources that respond
  to the Atom Publishing Protocol. -->
<application xmlns="http://research.sun.com/wadl/2006/07"
  xmlns:app="http://purl.org/atom/app">
  <!-- An Atom collection accepts Atom entries via POST. -->
  <resource_type id="atom_collection">
    <method href="#getCollection" />
    <method href="#postNewAtomMember" />
  </resource_type>
  <!-- An image collection accepts image files via POST. -->
  <resource_type id="image_collection">
    <method href="#getCollection" />
    <method href="#postNewImageMember" />
  </resource_type>
```

이 두 `resource_type`은 특정 리소스가 아니라 객체지향 설계의 클래스에 해당한다.
둘 다 `getCollection`을 지원하되 Atom 컬렉션은 `postNewAtomMember`, 이미지 컬렉션은 `postNewImageMember`를 지원한다.

```xml
<!-- Three possible operations on resources. -->
<method name="GET" id="getCollection">
  <response>
    <representation href="#feed" />
  </response>
</method>
<method name="POST" id="postNewAtomMember">
  <request>
    <representation href="#entry" />
  </request>
</method>
<method name="POST" id="postNewImageMember">
  <request>
    <representation id="image" mediaType="image/*" />
    <param name="Slug" style="header" />
  </request>
</method>
```

`getCollection`은 Atom 피드를 표현으로 기대하는 GET이고, `postNewAtomMember`는 Atom 엔트리를 보내는 POST다.
`postNewImageMember`도 POST지만 이미지 파일을 보내며 HTTP Slug 헤더 값을 지정할 줄 안다.
표현 둘은 이미 Atom의 XSD에 기술되어 있어 XSD를 참조하기만 하면 되고, 리소스 간 링크를 알리는 param으로 주석을 달 수 있다.

```xml
<!-- Two possible XML representations. -->
<representation id="feed" mediaType="application/atom+xml"
  element="atom:feed" />
<representation id="entry" mediaType="application/atom+xml"
  element="atom:entry" />
</application>
```

이 파일을 웹(예: `http://www.example.com/app-resource-types.wadl`)에 올리면 리소스가 되어 URI로 참조해 재사용할 수 있다.
그러면 세 컬렉션을 몇 줄로 정의할 수 있다.

```xml
<?xml version="1.0"?>
<!-- This is a description of three "collection" resources that respond
  to the Atom Publishing Protocol. -->
<application xmlns="http://research.sun.com/wadl/2006/07"
  xmlns:app="http://purl.org/atom/app">
  <resources base="http://www.example.com/">
    <resource path="RESTfulNews"
      type="http://www.example.com/app-resource-types.wadl#atom_collection" />
    <resource path="samruby/photos"
      type="http://www.example.com/app-resource-types.wadl#image_collection" />
    <resource path="leonardr/photos"
      type="http://www.example.com/app-resource-types.wadl#image_collection" />
  </resources>
</application>
```

APP가 인기 있는 이유는 매우 일반적인 인터페이스라는 점이다.
두 APP 서비스의 주된 차이는 각자의 서비스 문서에 기술되고, 범용 APP 클라이언트는 이를 읽어 여러 서비스의 클라이언트로 스스로 재프로그래밍한다.
그러나 더 일반적인 인터페이스, 즉 HTTP의 균일 인터페이스가 있다.
APP 서비스 문서는 도메인 특화 XML 어휘를 쓰지만, HTML과 WADL 같은 하이퍼미디어 포맷은 어떤 웹 서비스든 기술할 수 있어 그 클라이언트는 APP 클라이언트보다 더 일반적일 수 있다.

하이퍼미디어는 한 서비스가 다른 서비스와 어떻게 다른지 알리는 방법이다.
그 지능이 하이퍼미디어에 담기면 프로그래머가 코드에 덜 하드와이어링해도 된다.
더 중요하게, 하이퍼미디어는 URI 다음으로 중요한 웹 기술인 링크에 접근하게 해 준다.
REST의 잠재력은 웹 서비스가 표현을 밋밋한 미디어가 아니라 링크가 풍부한 하이퍼미디어로 제공하기 시작할 때 비로소 온전히 발휘된다.

#### WADL은 악한가?

WSDL은 SOAP을 단순한 XML 봉투 포맷에서 RPC 스타일 웹 서비스와 동의어인 이름으로 바꿔 놓았다.
WSDL은 HTTP 요청·응답의 세부를 추상화하고 프로그래밍 언어의 메서드 호출 기반 모델로 대체한다.
WADL도 같은 일을 하니, WADL이 클라이언트 편의를 명분으로 평범한 HTTP 웹 서비스를 RPC 스타일에 묶을까 걱정해야 하는가?

저자는 안전하다고 본다.
WADL은 HTTP 요청·응답의 세부를 추상화하지만 그 위에 새로운 추상을 얹지 않는다는 점이 핵심이다.
REST는 HTTP에 묶이지 않으며, RESTful 서비스에서 HTTP를 추상화해도 REST는 남는다.
리소스 지향 웹 서비스는 균일 인터페이스에 응답하는 리소스를 노출한다(그것이 REST다).
WADL 문서는 균일 인터페이스에 응답하는 리소스를 기술하고, WADL을 쓰는 프로그램은 리소스에 대응하는 객체를 만들어 균일 인터페이스를 구현하는 메서드 호출로 접근한다.
RESTful함은 프로토콜이 아니라 인터페이스에 산다.

WADL로 할 수 있는 가장 나쁜 일은 서비스가 균일 인터페이스에 응답한다는 사실을 숨기는 것이다.
저자는 그 방법을 일부러 보여주지 않았다.
균일 인터페이스를 존중하지 않는 웹 애플리케이션이나 REST-RPC 혼합 서비스의 WADL을 쓸 때 그렇게 해야 할 수 있다.

WADL 자체가 WSDL이 SOAP에 한 것처럼 HTTP를 RPC 모델에 묶지는 않으리라고 저자는 꽤 확신한다.
그러나 절차 호출 지향 코드를 단 하나의 URI만 노출하는 “웹 서비스”로 바꾸는 코드 생성기가 걱정거리다.
WADL은 리소스를 정의하게 하지만, 미래의 생성기가 자동 생성 WSDL이 단일 “엔드포인트”를 노출하듯 단일 “리소스”만 노출하는 WADL을 만들면 어떻게 될까?
이는 실제 우려다.
다행히 WADL의 역사는 WSDL과 다르다.
WSDL은 SOAP이 아직 공식적으로 RPC 스타일과 결부되던 때 도입됐지만, WADL은 사람들이 REST의 이점을 인식하기 시작한 때 RESTful 인터페이스를 유지하며 세부를 숨기는 방법으로 소개된다.
WADL을 지원하려는 도구 개발자라면 RESTful 설계 지원에도 관심이 있기를 바란다.

## 핵심 정리

표현 포맷은 데이터의 의미를 담아내는 것이 관건이며, 일회용 XML 어휘를 새로 만드는 것은 최후의 수단이다.
저자가 제안한 대략의 우선순위는 XHTML, 마이크로포맷을 얹은 XHTML, Atom(과 OpenSearch), SVG, 폼 인코딩 키-값 쌍, JSON, RDF/RDFa 순이며, 그다음이 프레임워크 특화 직렬화, 임시 XHTML, 커스텀 XML 어휘다.
클라이언트의 알려진 요구는 이 우선순위보다 앞선다.
XHTML은 프로그래밍 가능한 웹을 이끌 수 있고 마이크로포맷으로 도메인 의미를 더할 수 있으며, Atom은 출판의 의미를 표현하고 기존 클라이언트 지원을 얻는다.

다국어 데이터는 UTF-8(또는 동아시아 중심이면 바이트 순서 표시가 붙은 UTF-16)로 통일하는 것이 최선의 결정이다.
XML은 첫 줄에 문서 인코딩을 명시하고 `application/xml`로 제공해야 하며, `Content-Type`의 charset은 신뢰하기 어렵다는 점을 유념한다.
JSON은 RFC 4627 규약에 따라 UTF-* 인코딩을 쓰면 인코딩을 명시할 필요가 없다.

사전 포장된 제어 흐름은 리소스 설계·표현 포맷·응답 코드를 묶어 재사용한다.
일반 규칙(401/404/405)과 데이터베이스 기반 흐름(GET/PUT/POST/DELETE별 응답 코드)이 그 예다.
Atom 출판 프로토콜(APP)은 HTTP 균일 인터페이스 위에 상위 균일 인터페이스를 얹어, 서비스 문서·컬렉션·멤버·카테고리 문서라는 네 리소스로 출판 과정을 다룬다.
목록에 항목이 계속 추가되는 문제라면 APP를 쓰는 편이 재발명보다 낫고 기존 클라이언트 지원을 얻는다.
GData는 검색 결과 리소스와 데이터 확장으로 APP를 확장한 좋은 사례이며, POST Once Exactly(POE)는 POST를 멱등하게 만들어 신뢰성 있는 요청을 가능하게 한다.

하이퍼미디어는 링크와 폼으로 서비스 간 차이를 알리는 수단이다.
URI Templates는 리소스 폼을 링크처럼 보이게 하고, XHTML 4는 강력한 링크와 다소 빈약한 폼을 제공하며, XHTML 5는 네 HTTP 메서드·URI Templates·반복 모델로 그 한계를 넓힌다.
WADL은 어떤 리소스든 기술하는 XML 어휘로 URI Templates, 모든 HTTP 메서드, HTTP 헤더, 스키마 기반 XML 표현을 지원해 하이퍼미디어 포맷으로서 HTML 5보다 낫다.
WADL은 HTTP를 추상화하되 그 위에 새 추상을 얹지 않으므로, RESTful함은 프로토콜이 아니라 인터페이스에 산다는 원칙을 지킨다.
REST의 잠재력은 서비스가 링크가 풍부한 하이퍼미디어를 제공할 때 온전히 발휘된다.
