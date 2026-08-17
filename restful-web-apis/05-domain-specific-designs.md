# 5장 도메인 특화 설계: Maze+XML로 새 표준을 만든다는 것

《RESTful Web APIs》(Leonard Richardson, Mike Amundsen, O'Reilly 2013) 5장 정리.

## 개요

저자는 이 장을 이렇게 소개한다 — 뻔한 전략은 자기 문제에 정확히 맞는 완전히 새로운 표준을 설계하는
것이며, 저자는 Maze+XML 표준을 그 예로 든다.

이 정리는 저자의 공식 장별 설명과 해당 장이 다루는 공개 표준을 근거로 하며, 책 본문을 옮긴 것이 아니다.

4장이 하이퍼미디어가 무엇인지를 HTML로 설명했다면, 5장부터 8장까지는 그 하이퍼미디어를 실제 API에
적용하는 네 가지 전략을 차례로 다룬다.
5장은 그중 가장 먼저 떠오르는 전략, 즉 내 도메인만을 위한 미디어 타입을 새로 만드는 길을 살핀다.
저자가 예로 드는 Maze+XML은 미로 탐험이라는 좁은 도메인을 위해 Mike Amundsen 자신이 만든 미디어
타입이며, 이 책의 예제 코드 저장소에 서버와 세 개의 클라이언트로 구현돼 있다.[^ref-example]

## 도메인 특화 미디어 타입이라는 전략

새 미디어 타입을 만든다는 것은 클라이언트와 서버가 공유할 어휘를 직접 정의한다는 뜻이다.
HTML이 문서를 위한 어휘(`h1`, `p`, `a`, `form`)를 정의하듯, 미로를 위한 어휘(`maze`, `cell`,
`rel=“north”`)를 정의하는 것이다.

이 전략이 매력적인 이유는 명확하다.
4장에서 봤듯 하이퍼미디어는 “다음에 어떤 요청을 할 수 있는가”까지만 답하고 “그 요청이 무슨 뜻인가”는
답하지 않는데, 미디어 타입을 직접 정의하면 그 두 번째 질문의 답을 타입 명세 안에 함께 넣을 수 있다.[^ref-04]
`rel=“north”`가 “북쪽 방으로 이동한다”를 뜻한다고 명세가 규정해 두면, 그 명세를 구현한 클라이언트는
링크의 실세계 의미를 안다.
프로토콜 수준의 규칙과 도메인 수준의 의미가 하나의 문서에 모이므로 설계가 가장 단순해진다.

미디어 타입 이름 자체도 표준이 정한 자리를 쓴다.
`application/vnd.amundsen.maze+xml`에서 `vnd.` 접두사는 RFC 6838이 정의한 벤더 트리를 뜻하고,
`+xml` 접미사는 이 타입이 XML 기반임을 알린다.
누구나 IETF 표준화 절차 없이 자기 미디어 타입을 만들 수 있게 열어 둔 자리가 바로 이 벤더 트리이며,
도메인 특화 설계 전략은 그 자리를 쓰는 전략이다.

## Maze+XML의 구조

명세 원문은 확인하지 못했다.
Maze+XML 명세가 있던 `amundsen.com/media-types/maze/` 는 현재 다른 사이트로 바뀌어 접근할 수 없고,
Internet Archive도 확인 시점에 응답하지 않았다.
따라서 아래 구조는 명세를 옮긴 것이 아니라, 이 책의 공식 예제 코드가 실제로 생성하는 문서와 제3자
구현이 검증하는 요소를 근거로 정리한 것이다.

문서의 뼈대는 루트 `maze` 요소와 그 아래 세 종류의 문맥 요소다.
예제 서버는 응답 XML을 문자열 템플릿으로 조립하며, 그 템플릿이 곧 이 미디어 타입의 문법을 드러낸다.

```javascript
template.mazeStart       = '<maze version="1.0">';
template.collectionStart = '<collection href="{l}/">';
template.itemStart       = '<item href="{l}" title="{t}">';
template.cellStart       = '<cell href="{l}" rel="current" title="{t}">';
template.link            = '<link href="{l}" rel="{d}"/>';
template.titleLink       = '<link href="{l}" rel="{d}" title="{t}" />';
template.error           = '<error><title>{t}</title></error>';
```

세 문맥 요소가 각각 다른 종류의 리소스를 나타낸다 — `collection`은 미로들의 목록, `item`은 하나의
미로, `cell`은 미로 안의 한 방이다.
`link`는 그 어느 문맥에나 들어갈 수 있는 전이이고, `error`는 오류 응답의 자리다.
이 구조는 제3자 구현인 `malevy/mazeagent`의 직렬화 테스트가 기대하는 출력과도 일치한다 —
`<maze version=“1.0” />`, `<collection href=“...”>`, `<item href=“...”>`, `<cell href=“...” side=“10”
total=“80”>`, `<link href=“...” rel=“maze” />` 가 그 테스트의 단언값이다.
같은 테스트가 인정하는 링크 관계 집합은 `collection`, `current`, `east`, `exit`, `maze`, `north`,
`south`, `west`, `start` 아홉 개다.

실제 응답이 어떤 모양인지는 예제 서버의 조립 순서를 따라가면 나온다.
미로 목록은 이렇다.

```xml
<maze version="1.0">
  <collection href="/">
    <link href="/five-by-five" rel="maze" title="A Beginner's Maze" />
  </collection>
</maze>
```

미로 하나를 가리키는 문서는 진입점 하나만 준다.

```xml
<maze version="1.0">
  <item href="/five-by-five" title="A Beginner's Maze">
    <link href="/five-by-five/0" rel="start"/>
  </item>
</maze>
```

방 하나의 표현이 이 미디어 타입의 핵심이다.

```xml
<maze version="1.0">
  <cell href="/five-by-five/7" rel="current" title="Hall of Knives">
    <link href="/five-by-five/6" rel="north"/>
    <link href="/five-by-five/8" rel="south"/>
    <link href="/five-by-five/12" rel="east"/>
    <link href="/five-by-five/999" rel="exit"/>
    <link href="/five-by-five" rel="maze" title="A Beginner's Maze" />
    <link href="/" rel="collection"/>
  </cell>
</maze>
```

## 서버가 도메인 지식을 링크로 번역한다

이 미디어 타입이 실제로 무슨 일을 하는지는 서버 코드에서 가장 잘 드러난다.
예제 서버의 미로 데이터는 각 방마다 네 방향의 벽 여부를 담은 배열 하나다.

```javascript
"cell0": {"title":"Entrance Hallway", "doors":[1,1,1,0]}
```

서버는 이 배열을 좌표 계산으로 이웃 방 번호로 바꾼 뒤, 문이 열린 방향에 대해서만 링크를 만든다.

```javascript
rel = ['north', 'west', 'south', 'east'];
mov = [z-1, z+(sq*-1), z+1, z+sq];

for(i=0,x=data.doors.length;i<x;i++) {
    if(data.doors[i]===0) {
        body += template.link.replace('{l}',root+'/'+maze+'/'+mov[i]).replace('{d}',rel[i]);
    }
}
```

여기서 벌어지는 일이 도메인 특화 설계의 요점이다.
좌표계, 한 변의 크기(`sq`), 벽 배열 같은 도메인 내부 지식은 전부 서버 안에 남고, 클라이언트에게 나가는
것은 “지금 갈 수 있는 방향과 그 URL”뿐이다.
클라이언트는 미로가 몇 칸짜리인지, 방 번호가 어떻게 매겨지는지 알 필요가 없다.

그 결과가 이 저장소의 예제 코드 분석에서 확인한 세 클라이언트의 공존이다.[^ref-example]
사람이 조작하는 브라우저 클라이언트, 사람 없이 미로 전체를 탐험해 ASCII 지도를 그리는 봇, 그리고 규격만
지키고 일은 하지 않는 the-boaster가 모두 같은 서버에 붙으며, 서버 코드는 한 줄도 달라지지 않는다.
둘을 잇는 계약은 오직 미디어 타입과 그 안의 링크 관계뿐이다.

## 링크 관계가 곧 이 API의 어휘다

Maze+XML에서 상태 전이의 의미를 나르는 것은 요소가 아니라 `rel` 값이다.
`north`, `south`, `east`, `west`는 이동, `exit`는 출구, `start`는 미로의 시작 방, `maze`는 이 방이 속한
미로, `collection`은 전체 목록, `current`는 지금 있는 방을 뜻한다.

이 관계들이 4장에서 본 IANA 레지스트리의 관계들과 성격이 다르다는 점이 중요하다.[^ref-04]
`collection`과 `item`은 RFC 6573이 정의한 공용 어휘라 어떤 도메인에서도 같은 뜻이지만, `north`와 `exit`는
미로 밖에서는 아무 뜻도 없다.
도메인 특화 설계란 정확히 이 두 번째 종류의 어휘를 자기 손으로 만들어 쓰는 일이며, 그래서 얻는 것과
잃는 것이 함께 따라온다.

얻는 것은 표현력이다.
`rel=“north”`는 그 자체로 도메인 행위를 완전히 서술하므로 클라이언트 코드가 “어떤 rel을 찾을 것인가”로
단순해진다.
잃는 것은 재사용성이다.
이 어휘를 이해하는 클라이언트는 미로 서버 외에는 어디에도 쓸 데가 없고, 다른 도메인은 이 타입에서 아무것도
가져다 쓸 수 없다.

## 이 전략이 치르는 대가

도메인마다 새 미디어 타입을 만들면 도메인마다 새 클라이언트를 만들어야 한다.
브라우저 하나가 모든 웹사이트를 여는 것과 달리, Maze+XML 클라이언트는 미로만 열고 주문 관리 타입
클라이언트는 주문만 연다.
미디어 타입의 수만큼 클라이언트 구현 비용이 곱해지는 구조이며, 이것이 이 전략의 근본적 대가다.

명세를 유지할 책임도 따라온다.
이 정리가 명세 원문을 확인하지 못한 사정 자체가 그 대가의 사례다 — 새 표준을 만든 사람이 그 문서를 계속
호스팅하지 않으면, 그 타입을 구현하려는 사람은 남의 구현을 역추적해야 한다.
IANA 레지스트리에 등록된 관계나 IETF RFC로 발행된 형식이 갖는 지속성을 개인이 만든 벤더 타입은 갖기
어렵다.

또 하나의 대가는 진화 가능성이다.
미디어 타입이 도메인 의미를 직접 담으면, 도메인이 바뀔 때 미디어 타입도 바뀌어야 한다.
예제 서버에 위층·아래층 링크를 추가하려던 흔적이 주석으로 남아 있는데(`up`, `down`), 이런 확장은 곧
타입 명세의 개정이고 기존 클라이언트와의 호환 문제다.

이 대가들이 5장 다음의 세 장을 설명한다.
6장은 여러 도메인이 공유하는 컬렉션 패턴을, 7장은 도메인 의미를 담지 않는 범용 하이퍼미디어 형식(HTML,
HAL, Siren)을, 8장은 형식과 도메인 의미를 분리해 프로파일로 따로 공급하는 길을 다룬다.[^ref-readme]
저자가 5장의 전략을 “뻔한(obvious)” 전략이라고 부른 것은 칭찬이 아니라 위치 표시에 가깝다 — 가장 먼저
떠오르지만 가장 비싼 길이라는 뜻이다.
같은 예제 저장소에 Maze+XML과 Collection+JSON을 나란히 둔 구성이 그 비교를 코드로 보여 준다.[^ref-example]

## 핵심 정리

도메인 특화 설계는 자기 문제에 정확히 맞는 미디어 타입을 새로 정의하는 전략이며, 하이퍼미디어가 답하지
못하는 “이 전이가 실세계에서 무슨 뜻인가”를 타입 명세 안에 함께 담을 수 있다는 것이 최대 장점이다.

Maze+XML(`application/vnd.amundsen.maze+xml`)은 그 예로, `vnd.` 벤더 트리와 `+xml` 접미사를 쓰는
XML 기반 타입이다.
명세 원문은 현재 접근할 수 없어 확인하지 못했으며, 이 문서의 구조 설명은 공식 예제 서버가 생성하는
문서와 제3자 구현의 테스트 단언값을 근거로 한다.

문서 구조는 루트 `maze` 아래 `collection`(미로 목록), `item`(미로 하나), `cell`(방 하나), 그리고 어디에나
들어가는 `link`와 오류용 `error`로 이뤄진다.
전이의 의미는 `rel` 값이 나르며, 확인된 집합은 `north`, `south`, `east`, `west`, `exit`, `start`, `maze`,
`collection`, `current`다.

서버는 벽 배열과 좌표 계산 같은 도메인 내부 지식을 전부 자기 안에 두고 클라이언트에게는 링크만 내보낸다.
그 덕에 성격이 전혀 다른 세 클라이언트가 서버 코드를 바꾸지 않고 같은 표현을 소비한다.

대가는 세 가지다 — 타입마다 클라이언트를 새로 만들어야 하는 비용, 명세를 계속 유지해야 하는 책임,
도메인이 바뀌면 타입도 바꿔야 하는 경직성이다.
이 대가들이 6장의 컬렉션 패턴, 7장의 범용 하이퍼미디어 형식, 8장의 프로파일로 이어지는 동기가 된다.

## 참고

- 관련 문서: [RESTful Web APIs 정리 (색인)](README.md), [4장 하이퍼미디어](04-hypermedia.md), [RESTful Web APIs 예제 코드](example-code.md), [RESTful Web Services에서 RESTful Web APIs로](whats-new.md)
- 예제 저장소의 Maze 서버: <https://github.com/RESTful-Web-APIs/example-code/blob/master/Maze/server/app.js>
- 제3자 Maze+XML 구현(구조 교차 확인에 사용): <https://github.com/malevy/mazeagent>
- RFC 6838 Media Type Specifications and Registration Procedures: <https://www.rfc-editor.org/rfc/rfc6838>

---

[^ref-readme]: 저자 공식 장별 설명과 5~8장의 전략 구분은 이 저장소의 [RESTful Web APIs 색인 문서](README.md)에 정리해 두었다.
[^ref-04]: 하이퍼미디어의 정의, 링크 관계와 IANA 레지스트리, 하이퍼미디어가 풀지 못하는 문제는 이 저장소의 [4장 정리](04-hypermedia.md)에 정리해 두었다.
[^ref-example]: Maze 서버의 라우팅과 데이터 구조, 세 클라이언트(the-game, the-mapmaker, the-boaster)의 동작, Collection+JSON과의 대비는 이 저장소의 [예제 코드 문서](example-code.md)에 정리해 두었다.
