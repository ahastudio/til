# Back-end for Front-end Pattern (BFF)

![Evolution of BFF](https://www.thoughtworks.com/content/dam/thoughtworks/images/photography/inline-image/insights/blog/frontend/blg_inline_bff_soundcloud_03.png)

## 소개

Backend for Frontend(BFF)는 여러 프론트엔드(웹, iOS, Android, 서드파티 등)가
하나의 범용 API를 공유하는 대신, 프론트엔드마다 전용 백엔드 계층을 두는
아키텍처 패턴이다.

여러 마이크로서비스에 흩어진 데이터를 BFF가 취합해
클라이언트에 최적화된 형태로 노출한다.
이 패턴은 Phil Calçado가 SoundCloud에서 근무하던 중 정리했고,
이후 SoundCloud, Sam Newman, 카카오페이지 등이
각자의 맥락에서 확장해 왔다.

## 해결하는 문제

단일 범용 API를 모든 클라이언트가 공유하면 다음과 같은 문제가 쌓인다.

- 화면 하나를 조립하는 데 여러 번의 HTTP 호출이 필요해,
  모바일처럼 불안정한 네트워크에서 성능이 떨어진다.
- API를 변경할 때마다 모든 클라이언트, 특히 서드파티 연동까지
  깨지지 않는지 조율해야 해서 개발 속도가 느려진다.
- 웹과 모바일은 화면 크기, 대역폭, 배터리 제약이 서로 다른데도
  같은 응답 형태를 강요받는다.
- 여러 팀이 하나의 공유 API(또는 배포 아티팩트)를 두고 경쟁하면서
  팀 간 마찰과 커뮤니케이션 오버헤드가 커진다.

카카오페이지 사례처럼 프론트엔드가 백엔드 API를 직접 호출하는 구조에서는
추가로 다음 문제가 나타난다.

- 원하는 데이터 형태를 만들기 위해 여러 API 응답을 조합·가공하는
  로직이 프론트엔드 코드베이스에 쌓여 통제하기 어려워진다.
- 이 계산 로직이 브라우저의 UI 렌더링과 같은 스레드에서 경합해
  렌더링 성능이 떨어진다.
- 플랫폼마다 다른 인증 방식을 프론트엔드가 각각 처리해야 한다.
- 필요한 필드만 받는 partial response가 불가능해
  불필요한 데이터까지 함께 내려받는다.

## 작동 방식

BFF는 "애플리케이션이 사용하는 API가 아니라, 애플리케이션의 일부"다.
프론트엔드 팀이 자신의 플랫폼에 맞춰 전용 API 계층을 직접 설계하고,
그 안에서 여러 마이크로서비스를 호출해 하나의 굵은 단위(coarse-grained)
엔드포인트로 응답을 합친다.

Sam Newman은 이를 "모두를 위한 백엔드 하나" 대신
"사용자 경험 하나당 백엔드 하나"를 두는 것으로 요약한다.
각 BFF는 특정 UI에 강하게 결합되고, 해당 UI를 만드는 팀이 소유한다.
그래서 다른 팀과 조율하지 않고도 클라이언트와 서버를 함께
빠르게 반복 개발할 수 있다.

SoundCloud는 이 원칙을 팀 자율성으로 확장해,
프론트엔드 팀이 공유 모놀리스 변경을 요청하는 대신
엔드포인트를 직접 구현하고 데이터를 어디서 가져와
어떻게 취합할지 스스로 결정하게 했다.
대신 모니터링, 인증, rate limiting 같은 공통 관심사는
경량 프레임워크(Finagle 기반)로 표준화해 중복을 줄였다.

## 사례

SoundCloud는 사용자 프로필 페이지처럼 여러 세분화된 호출이 필요하던 화면을
`GET /user-profile/123.json` 같은 단일 엔드포인트로 통합했고,
웹에는 더 풍부한 데이터를, 모바일에는 더 가벼운 응답을 차등 제공했다.
이후 수십 개의 BFF로 시간당 수억 건의 요청을 처리하는 규모로 확장했으며,
Mobile API, Web API, Public/Partner API 등
클라이언트 유형별로 게이트웨이를 나눴다.
기존 모놀리스 API를 마이크로서비스로 점진적으로 대체하는
"public-api-strangler" BFF도 함께 운용했다.

Sam Newman은 이커머스 위시리스트 사례를 든다.
Wishlist, Catalog, Inventory 세 마이크로서비스의 데이터를
BFF가 하나의 최적화된 응답으로 취합하는 방식이다.
REA는 모바일 플랫폼별로 별도 BFF를 뒀고,
반대로 SoundCloud의 iOS·Android 리스너 앱은 BFF 하나를 함께 썼다.

카카오페이지는 iOS, Android, Web을 모두 지원하지만
BFF는 Web에서만 적용했다.
다중 플랫폼을 지원하지 않는 곳에는 BFF를 둘 이유가 없다고 봤기 때문이다.
스택은 Next.js와 Apollo Server(BFF), Urql(클라이언트), Redux를 조합했고,
GraphQL을 BFF 구현체로 채택해
REST 두 번 호출로 받던 불필요한 필드(`create_dt`, `user_id`,
`response_time` 등)를 걷어내고 resolver에서 필요한 필드만
가공(camelCase 변환, 날짜 포맷 변경 포함)해 단일 쿼리로 응답하게 했다.

## 트레이드오프

BFF는 팀 자율성, 클라이언트별 최적화, 장애 격리(한 BFF의 장애가
전체로 번지지 않음), 빠른 배포 주기라는 이점을 준다.
반면 여러 BFF에 걸쳐 비즈니스 로직이 중복되기 쉽고,
추가 서비스 계층이 늘어난 만큼 배포·인프라 복잡도와
지연이 커질 수 있다.

HN에서 cdnsteve는 Sam Newman의 글이 이 트레이드오프를
더 구체적으로 다룬다고 지적하며,
SoundCloud가 Scala와 Finagle을 쓰는 배경에서
하위 서비스로의 블로킹 호출과 어떤 서비스를 critical로
선언할지의 문제, 그리고 중복 코드가 불가피하다는 점을
짚었다[^cdnsteve].
기술 선택지가 제한된다는 이 관찰은
본문이 말하는 배포·인프라 복잡도 증가를
실제 운영 사례로 뒷받침한다.

Sam Newman과 SoundCloud 모두 공통으로 강조하는 원칙은
성급한 일반화를 피하라는 것이다.
"세 번째 사용 사례가 나올 때까지 일반화를 미루라"는
rule of three를 따라, 같은 패턴이 3개 이상의 BFF에서
반복 확인된 뒤에야 공유 라이브러리나 서비스로 추출할 것을 권장한다.
SoundCloud는 또한 플랫폼 공통 기능 없이 좁은 유스케이스마다
BFF를 만들면 오히려 BFF가 난립하고,
페이지네이션 같은 처리가 서버 쪽 로직으로 떠밀려
타임아웃과 장애 위험이 커질 수 있다고 지적한다.

카카오페이지 사례는 GraphQL 기반 BFF에서
캐싱 전략 선택이 추가 고려사항이 됨을 보여준다.
Apollo Client의 정규화 캐싱은 같은 타입·ID를 가진
서로 다른 쿼리 결과(예: `categoryFilter:1`과 `categoryFilter:2`)를
서로 덮어쓰는 문제를 일으켰고,
카카오페이지는 id 기반 캐싱 대신 document 기반 캐싱을 쓰는
Urql로 전환해 이를 해결했다.
또한 GraphQL과 캐시 조합만으로는 클릭이나 스크롤 시
비동기로 중간 데이터를 수정하는 케이스를 다루기 어려워,
GraphQL 데이터를 normalize한 뒤 Redux에 저장하는 방식을 더해
데이터 fetch와 저장·사용의 역할을 분리했다.

## 비평

BFF는 결국 "어디에 조합 로직을 둘 것인가"의 문제를
프론트엔드에서 별도 계층으로 옮기는 결정이다.
문제 자체가 사라지는 것이 아니라,
소유권과 배포 단위가 바뀌는 것에 가깝다.
따라서 BFF를 도입하는 이유가 성능 최적화인지,
팀 간 결합도를 낮추기 위함인지,
아니면 단지 유행을 따르는 것인지를 먼저 구분해야
카카오페이지처럼 "이 프론트엔드에는 필요 없다"는
판단도 정당하게 내릴 수 있다.
BFF마다 로직이 중복되는 문제는 마이크로서비스 전반에서
반복되는 딜레마와 같은 형태이며,
rule of three 같은 경험칙은 그 판단을 늦추는 장치이지
해결책은 아니다.

이 질문에 대한 하나의 답은 애초에 별도 계층을 두지 말자는 것이다.
HN에서 jtmarmon은 Netflix가 API 게이트웨이로 접근했던 이 문제를
GraphQL이나 Falcor 같은 클라이언트 사이드 쿼리 언어로
대체하고 있다며, 클라이언트마다 API를 배포하고 버전을
관리하는 부담 자체가 사라진다고 주장했다[^jtmarmon].
virmundi는 BFF가 사실 이미 이름이 있던 패턴,
즉 API 게이트웨이 패턴과 같다고 짚었다[^virmundi].
두 지적을 합치면 BFF의 정체성 자체가 흔들린다 —
조합 로직을 어디에 둘지가 아니라,
애초에 클라이언트별 계층을 코드로 짤 필요가 있는지의
문제가 된다.

Lobsters에서도 정확히 이 지점을 두고 논쟁이 벌어졌다.
brandonbloom은 BFF가 나쁜 패턴은 아니지만
API 설계의 실패를 인정하는 것에 가깝다고 봤다 —
GraphQL이나 Falcor 같은 기술로 대부분의 연산에서
왕복 횟수를 범용적인 방식으로 크게 줄일 수 있다는
것이다[^brandonbloom].
반론은 두 방향에서 나왔다.
0x2ba22e11은 GraphQL만큼 강력한 API를 낯선 외부에
노출하는 것 자체가 위험하다고 지적했다 —
BFF가 생성하기로 정한 쿼리 외에는 백엔드에 도달할 방법이
없다는 통제력이 사라진다는 것이다[^0x2ba22e11].
danielrheath는 조직 구조를 근거로 들었다 —
GraphQL을 기각하는 이유는 DOS 공격에 더 취약해서가 아니라,
서버 코드를 짜는 팀과 클라이언트 코드를 짜는 팀이 가까이
앉을 수 있는 조직에서는 그 유연성이 필요 없기 때문이라는
것이다[^danielrheath].
lmm은 이 논쟁 자체를 한 문장으로 정리했다 —
명시적인 BFF는 비정규화된 데이터베이스 스키마와 같은
종류의 실패 인정이지만, GraphQL이나 사전 렌더링 서비스가
아직 그만큼 믿고 쓸 만큼 성숙하지 않았을 뿐이라는
것이다[^lmm].

zaroth는 조합 로직을 프론트엔드나 별도 BFF가 아니라
핵심 마이크로서비스 자체에 API로 추가하고,
nginx의 lua 스크립트로 단일 요청을 여러 서비스에 나눠 보내
하나의 응답으로 묶는 방식을 대안으로 제시했다 —
조합을 위해 또 다른 서비스 계층을 만드는 것 자체가
마음에 들지 않는다는 것이다[^zaroth].
이 대안이 성립하려면 클라이언트마다 다른 요구를
핵심 서비스가 흡수해야 하는데,
_xnmw는 바로 그 지점에서 GraphQL·Falcor류 해법의 한계를
짚었다 — 어떤 필드 조합을 요청하느냐에 따라 성능 차이가
크게 날 수 있는데, 잘 설계된 BFF라면 클라이언트 요구를
반영해 미리 최적화된 개별 엔드포인트를 제공할 수 있지만
GraphQL 세계에서는 결국 "이 필드는 성능에 안 좋으니
피하라"는 문서화된 관행에 의존하게 된다는 것이다[^_xnmw].
결국 이 논쟁은 최적화 책임을 어디에 둘 것인가로
되돌아온다 — 스키마 뒤에 숨기고 관행으로 관리할지,
아니면 BFF 코드로 명시할지의 선택이다.

HN에서 drudru11이 인용한 David Wheeler의 격언과
Kevlin Henney의 반박이 이 계층 논쟁 전체를 요약한다 —
"컴퓨터 과학의 모든 문제는 또 하나의 간접 계층으로 풀 수
있다, 다만 간접 계층이 너무 많아지는 문제는 예외로
하고"[^drudru11].
BFF, API 게이트웨이, GraphQL은 모두 같은 간접 계층을
어디에 얼마나 둘 것인가에 대한 서로 다른 답일 뿐이다.

## 인사이트

BFF는 "프론트엔드 전용 백엔드"라는 이름표보다
"이 API는 누구의 화면을 위한 것인가"라는 질문에 대한 답이라는 점이
핵심이다.
플랫폼이 하나뿐이거나 클라이언트 요구사항이 크게 다르지 않다면
BFF는 불필요한 계층일 뿐이고,
카카오페이지가 Web에만 BFF를 둔 판단은 이 원칙을
그대로 따른 결과로 읽힌다.
반대로 SoundCloud처럼 클라이언트 종류가 늘고
팀 간 조율 비용이 병목이 되는 시점에는
BFF가 그 비용을 팀 경계 안으로 되돌리는 역할을 한다.
결국 BFF 도입 여부는 기술적 우아함보다
조직의 팀 구조와 배포 자율성 문제에 더 가깝다.

이 판단은 HN 댓글에서도 되풀이된다.
scotty79는 팀 경계를 넘는 화살표 하나하나에 비용이 든다는
것을 강조했다 — 그 비용은 대개 화살표를 받는 쪽 팀이
진다는 것이다[^scotty79].
PaulHoule은 한 걸음 더 나아가, 통신 오버헤드가 이렇게 큰
상황에서는 프론트엔드와 백엔드를 함께 책임지는
"하나의 정신"이 있어야 한다고 봤다 —
그것이 한 사람일 필요는 없고 여러 사람의 합의일 수도 있지만,
분산 시스템을 최적화할 완전한 기술과 태도를 갖춘 개발자는
드물기 때문에 팀 전체가 부분의 합보다 큰 하나로 움직여야
한다는 것이다[^paulhoule].
BFF가 팀 경계 안으로 되돌리는 비용이 바로 이것이다 —
화살표를 아예 없애는 것이 아니라,
화살표를 받는 쪽과 보내는 쪽을 같은 팀 안에 두는 것이다.

## 참고 자료

- [The Back-end for Front-end Pattern (BFF) by Phil Calçado (Sep 18, 2015)](https://philcalcado.com/2015/09/18/the_back_end_for_front_end_pattern_bff.html)
  (Lobsters 토론: <https://lobste.rs/s/nrd1ma/back_end_for_front_end_pattern_bff> (6점, 9개 댓글))
- [BFF @ SoundCloud | Thoughtworks](https://www.thoughtworks.com/insights/blog/bff-soundcloud)
  (HN 토론: <https://news.ycombinator.com/item?id=10730806> (130점, 23개 댓글))
- [Service Architecture at SoundCloud — Part 1: Backends for Frontends | SoundCloud Backstage Blog](https://developers.soundcloud.com/blog/service-architecture-1/)
- [Sam Newman - Backends For Frontends](https://samnewman.io/patterns/architectural/bff/)
  (HN 토론: <https://news.ycombinator.com/item?id=10648486> (53점, 11개 댓글))
- [카카오페이지는 BFF(Backend For Frontend)를 어떻게 적용했을까?](https://fe-developers.kakaoent.com/2022/220310-kakaopage-bff/)

---

[^cdnsteve]: <https://news.ycombinator.com/item?id=10737402>
[^jtmarmon]: <https://news.ycombinator.com/item?id=10661353>
[^virmundi]: <https://news.ycombinator.com/item?id=10661102>
[^brandonbloom]: <https://lobste.rs/c/92vhxp>
[^0x2ba22e11]: <https://lobste.rs/c/6rwcbp>
[^danielrheath]: <https://lobste.rs/c/817pgt>
[^lmm]: <https://lobste.rs/c/v6sif4>
[^zaroth]: <https://news.ycombinator.com/item?id=10661190>
[^_xnmw]: <https://news.ycombinator.com/item?id=10663123>
[^drudru11]: <https://news.ycombinator.com/item?id=10740338>
[^scotty79]: <https://news.ycombinator.com/item?id=10662857>
[^paulhoule]: <https://news.ycombinator.com/item?id=10738110>

