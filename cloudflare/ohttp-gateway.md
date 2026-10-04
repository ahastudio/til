# Cloudflare OHTTP Gateway: 사용자 IP를 모르는 백엔드를 관리형 서비스로 만든다

원문: [Announcing Cloudflare OHTTP Gateway – expanding access to Cloudflare’s privacy-preserving infrastructure | Cloudflare Blog](https://blog.cloudflare.com/announcing-cloudflare-ohttp-gateway/)

HN 토론: <https://news.ycombinator.com/item?id=49941091> (190점, 90개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/l5ev1t/announcing_cloudflare_ohttp_gateway> (1점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=34719>

## 요약

Cloudflare의 Lara Schull과 Akshat Mahajan이 2026년 10월 2일 Birthday Week 글로
Cloudflare OHTTP Gateway를 발표했다.
글은 온라인 프라이버시의 부담을 지금은 최종 사용자가 너무 많이
진다는 진단에서 출발한다.
사용자는 추적과 표적 광고를 피하려고 VPN을 쓰고 쿠키를 끄고 광고
차단기를 깔라는 말을 듣는다.
반대로 일부 앱 개발자는 원치 않을 만큼 사용자를 많이 알게 되는데,
평범한 클라이언트-서버 교환만으로 클라이언트 IP 주소와 TLS 지문 같은
흔적이 남기 때문이다.
글은 이런 가시성이 부담이 될 수 있다고 말한다.

Oblivious HTTP(OHTTP)는 앱 백엔드가 사용자 IP 주소를 보지 않고 HTTP 요청을 받게
하려고 설계된 IETF 표준이다.
요청은 독립적으로 운영되는 두 홉, 즉 릴레이와 게이트웨이를 지난다.
릴레이는 암호화된 요청을 내용을 모른 채 전달하면서 클라이언트 식별자를 앱
서버에서 감추고, 게이트웨이는 요청을 복호화하고 응답을 암호화해 앱 서버가 OHTTP
요청을 평범한 HTTP처럼 다루게 한다.
요청과 응답은 Hybrid Public Key Encryption(HPKE)으로 감싸므로
릴레이는 암호문만 본다.
글은 이를 이중 맹검 모델이라 부르며, 릴레이는 클라이언트 식별자만,
게이트웨이와 앱 서버는 요청 내용만 보고 둘 다 보는 주체는 없다고 설명한다.

Cloudflare는 2022년에 OHTTP 릴레이 제품인 Privacy Gateway를 내놓았다.
Flo Health가 앱의 Anonymous Mode에, Apple의 Private Cloud Compute가 AI 추론
요청을 사용자 신원과 떼어 내는 데 OHTTP를 쓴다고 글은 소개한다.
그런데 이미 Cloudflare 뒤에 서버를 둔 고객은 Cloudflare가 운영하는
릴레이를 함께 쓸 수 없었다.
그러면 Cloudflare가 클라이언트 메타데이터와 복호화된 요청 내용을 모두 보게 되어
OHTTP의 프라이버시 모델이 깨지기 때문이다.
이번 발표로 Cloudflare는 셀프서비스 OHTTP Gateway의 비공개 베타를 시작하고,
기존 Privacy Gateway의 이름을 Cloudflare OHTTP Relay로 바꾼다.
Gateway는 zone의 유료 부가 기능으로 이번 가을에 출시할 예정이며,
지금은 대기자 명단을 받는다.

고객의 선택지는 둘이다.
앱 서버가 Cloudflare 밖에 있고 게이트웨이를 직접 운영할 수
있으면 OHTTP Relay를 쓰고, 앱 서버가 이미 Cloudflare의 CDN이나 Workers 위에
있거나 Apple의 LiveCallerID처럼 제3자에게서 OHTTP 요청을 받는다면 제3자 릴레이와
함께 새 Gateway를 쓴다.
Cloudflare는 Gateway를 전 세계 엣지의 모든 서버에서 돌려 릴레이에서
게이트웨이까지의 지연을 줄이고, CDN 고객이라면 복호화와 오리진 처리가 같은
Cloudflare 장비에서 일어나 게이트웨이에서 오리진까지의 지연도 아낀다고 설명한다.

구현 면에서 Gateway는 zone의 기능으로 붙는다.
클라이언트는 zone의 `/.well-known/ohttp-gateway` 엔드포인트로 OHTTP
요청을 보내고, Gateway가 이를 가로채 복호화한 뒤 앱 서버에 하위 요청을 보내고
암호화된 응답을 돌려준다.
OHTTP가 아닌 요청은 Gateway를 거치지 않고 그대로 서버로 간다.
표준 OHTTP와 청크 OHTTP를 모두 지원하며,
요청을 조각 단위로 처리할 수 있는 청크 방식을 성능 때문에 권장한다.
Gateway를 zone에 묶었기
때문에 `example.com` zone으로 온 요청은 `foo.example.com`에는 갈 수 있어도
wikipedia.com 같은 다른 도메인에는 갈 수 없다.
키는 Cloudflare가 전부 관리하며 같은 엔드포인트에 GET을 보내면 공개 HPKE 키
설정을 돌려주고, 더 강한 프라이버시를 원하면 클라이언트가 요청을 보내는 IP와
다른 IP로 키를 받을 수 있다.
릴레이 인증은 복호화보다 먼저 실행되는 Cloudflare Access로 처리해 상호 TLS,
고정 서비스 자격 증명, 외부 사용자 정의 로직을 쓸 수 있다.
마지막으로 Gateway는 Cloudflare Workers나 Cloudflare에서 프록시되는
호스트에서 온 요청은 복호화를 거부해,
고객이 실수로 릴레이와 게이트웨이를 모두 Cloudflare에 두는 일을 막는다.

시작하려면 대기자 명단에 등록하고,
ohttp.info나 Cloudflare의 예제 라이브러리를 참고해 OHTTP 클라이언트를 구현하고,
릴레이를 직접 마련해야 한다.
글은 OHTTP가 네트워크 수준의 프라이버시만 주고 내부 요청 본문은 건드리지
않으므로 이메일 주소나 사용자 이름 같은 식별 정보를 본문에 넣지 않는 것은
개발자의 몫이라고 경고한다.
릴레이는 어느 인프라에서나 돌릴 수 있을 만큼 단순하지만,
클라이언트 식별자가 담긴 로그를 보지 않겠다는 약속을 사용자에게 검증 가능하게
해야 한다는 점이 전용 릴레이 제공자를 쓰는 이유라고 설명한다.
배포 후 테스트와 디버깅에는 `pvcli` 클라이언트를 쓸 수 있다.

## 분석

### 핵심 주장은 신뢰를 운영 주체 단위로 나누는 일이다

OHTTP의 보장은 암호학만으로 성립하지 않는다.
HPKE는 릴레이가 내용을 못 보게 할 뿐이고,
릴레이가 본 IP와 게이트웨이가 본 내용을 다시 잇지 못하게 하는 것은 두 홉을 서로
다른 회사가 운영하고 서로 결탁하지 않는다는 조직적 전제다.
글은 이 전제를 여러 번 반복하며, 2022년의 릴레이 제품이 Cloudflare 고객 중
상당수에게 쓸모가 없었던 이유도 바로 이것이었다고 고백한다.
CDN 사업자는 이미 수많은 오리진의 TLS를 종료하므로 같은 회사가 릴레이까지 맡으면
이중 맹검이 단일 맹검으로 무너진다.

그래서 이번 발표의 구조적 의미는 새 기능보다 역할의 재배치에 있다.
Cloudflare는 자기가 원래 서 있던 자리, 즉 오리진 바로 앞에 게이트웨이를 두고
클라이언트 쪽 홉은 다른 회사에 넘긴다.
Workers와 프록시 호스트에서 온 요청을 복호화하지 않는다는 규칙은 이 분리를
정책이 아니라 제품 동작으로 강제하려는 장치다.
HN에서 gruez는 Cloudflare가 두 홉을 모두 Cloudflare로 구성할 수 없게 일부러
막았으므로 이를 중간자 공격이라 부르는 것은 틀렸다고 반박했다.[^gruez]

### 제품의 논리는 지연과 운영 부담을 흡수하는 데 있다

글이 게이트웨이를 직접 운영하기 어렵다고 말할 때 드는 근거는 프로토콜의
복잡성보다 성능이다.
프록시 구조는 홉이 하나 이상 늘어나고 여기에 복호화와 암호화 비용이 더해지므로,
자체 구축한 OHTTP 구성의 지연이 상당할 수 있다는 것이다.
Cloudflare의 답은 애니캐스트로 모든 엣지 서버에서 게이트웨이를 돌리고, CDN
고객이라면 게이트웨이와 오리진 처리가 같은 장비에서 일어나게 하는 것이다.
1.1.1.1과 iCloud Private Relay를 운영한 경험이 같은 기반이라는
언급도 이 논리를 받친다.

키 관리, 릴레이 인증, 남용 방지를 Cloudflare가 대신한다는 설명도 같은 방향이다.
`/.well-known/ohttp-gateway`라는 고정 경로와 zone 범위 제한은 고객이 기존 HTTP
트래픽을 그대로 둔 채 OHTTP만 옆에 붙일 수 있게 하는 설계다.
결국 글은 OHTTP를 쉽게 만들기만
하면 도입될 프로토콜로 보고, 그 쉬움을 유료 부가 기능으로 판다.

### OHTTP가 맞는 문제는 생각보다 좁다

글은 OHTTP의 쓰임새를 넓게 말하지만 실제 사례는 Flo Health의 익명 모드,
Apple의 Private Cloud Compute,
LiveCallerID처럼 상태 없는 단발성 요청에 몰려 있다.
HN에서 gsnedders는 OHTTP가 게이트웨이가 같은
클라이언트의 여러 요청을 서로 엮지 못하게 하려는 좁은 용도의 설계라고 설명하고,
DNS-over-HTTPS를 대표 사례로 들었다.[^gsnedders]
SOCKS5 같은 일반 프록시로 같은 효과를 내려면 요청마다 새 TCP, TLS, HTTP 연결을
만들어야 하는 등 상태 공유를 극도로 조심해야 한다는 것이 그의 지적이다.
즉 OHTTP의 가치는 IP를 숨기는 데보다 요청 사이의 연결 고리를 끊는 데 있고,
그만큼 로그인 세션이 있는 일반 웹 서비스와는 맞지 않는다.

이 저장소의 `apple/apple-reference-image.md`가 다룬 Apple의 타임스탬프 요청도
Oblivious HTTP로 IP를 감추는 같은 유형이다.
이 해석대로라면 Cloudflare가 겨냥하는 시장은 브라우저 트래픽 전체가 아니라 앱이
특정 엔드포인트로 보내는 프라이버시 민감 요청이다.

## 비평

### 프라이버시를 유료 부가 기능으로 파는 것은 글의 목표와 어긋난다

글은 인터넷 전체의 프라이버시 기준을 높이고 싶다고 말하지만 Gateway는
zone의 유료 부가 기능이다.
HN에서 freedomben은 Cloudflare가 모든 것을 무료로 할 수는 없다고 인정하면서도,
웹사이트가 프라이버시를 더하려면 돈을 더 내야 한다는 구조는 프라이버시를
넓히려는 목표에 나쁜 유인이라고 썼다.[^freedomben]
글은 가격을 밝히지 않으므로 이 우려에 답하지 않는다.

더 큰 문제는 비용이 두 번 든다는 점이다.
Gateway를 쓰는 고객은 릴레이를 직접 가져와야 하고, 글 스스로 릴레이의 어려움은
코드가 아니라 로그를 보지 않겠다는 약속을 검증 가능하게 만드는 데 있다고 말한다.
그렇다면 고객은 Cloudflare에 게이트웨이 비용을 내고 다른 전용 릴레이
제공자에게 또 비용을 내야 한다.
글이 말하는 쉬움은 구조의 절반에만 적용된다.

### 글은 Cloudflare 자신이 보는 메타데이터를 설명하지 않는다

이중 맹검 설명은 게이트웨이와 앱 서버가 요청 내용만 본다고 말한다.
하지만 Gateway를 켠 zone이 Cloudflare CDN 뒤에 있다면 Cloudflare는 복호화된 요청
내용에 더해, 어느 릴레이에서 언제 얼마나 많은 요청이 왔는지도 본다.
HN에서 thayne은 단일 거래로는 훌륭하지만 인터넷의 큰 부분을 한 회사가 맡으면 그
회사가 어떤 사이트가 어떤 IP에게서 방문을 받았는지 알게 된다고 지적하면서도,
원래 IP와 내용을 모두 갖는 것보다는 낫다고 덧붙였다.[^thayne]
arshxyz는 TLS 지문에 기대는 Cloudflare WAF가 OHTTP를 켜면 동작을 멈추는지,
아니면 Cloudflare가 클라이언트 메타데이터를 읽고 처리하되 앱 서버에만 넘기지
않는 것인지 물었다.[^arshxyz]
글은 이 질문에 답할 정보를 담고 있지 않으며,
Gateway 앞에서 어떤 보안 기능이 무엇을 보는지 쓰지 않는다.

### 남용 대응의 비용을 고객에게 넘긴다

OHTTP는 앱 서버가 IP를 보지 못하게 하므로 IP 기반 차단도 함께 사라진다.
HN에서 Joker_vD는 남용을 먼저 식별한 뒤 이를 발신 IP나 다른 식별자와 연결해야
하는데 이 구조에서 남용자 차단을 어떻게 더하느냐고 물었다.[^Joker_vD]
someonebaggy는 남용자는 어차피 주거용 프록시를 사서 IP 차단을
피한다고 답했지만,[^someonebaggy] yencabulator는 먼 데이터센터 몇 곳을 ASN
단위로 막아 봇 트래픽의 80% 이상을 걸러 냈다며 그렇게 쉽게 피하지 못한다고
반박했다.[^yencabulator]

글은 남용 문제를 Access로 릴레이를 인증하고 릴레이가 클라이언트를 책임 있게
인증한다는 신뢰로 처리한다.
그러나 그 신뢰가 깨질 때 고객이 쓸 수 있는 수단은 릴레이 전체를 끊는 것뿐이고,
개별 클라이언트를 가려낼 방법은 글에 없다.

## 인사이트

### 결탁하지 않는 두 회사라는 전제가 가장 비싼 부품이 된다

OHTTP의 보안은 결국 계약과 평판의 문제로 환원된다.
릴레이와 게이트웨이 운영자가 결탁하지 않는다는 조건을 사용자가 검증할 길은
없고, 그 조건을 믿게 해 주는 것은 두 회사의 이름이다.
HN에서 ranger_danger는 iCloud Private Relay가 OHTTP를 쓴다는 답글에 대해,
Apple이 릴레이와 게이트웨이 양쪽에 서는 구조라면 결탁이 OHTTP의 프라이버시를
깬다는 경고 그대로의 상황이라고 반박했다.[^ranger_danger]

이 구조에서 시장은 기술보다 신뢰받는 운영자의 수에 제약을 받는다.
게이트웨이 시장은 Cloudflare처럼 이미 오리진 앞에 선 회사가 쉽게 가져가지만,
릴레이 시장은 사용자에게 로그를 보지 않는다고 믿게 할 수 있는 독립
사업자가 있어야 한다.
이 해석에서 Cloudflare가 Relay와 Gateway를 모두 파는 것은 같은 고객의 양쪽 홉을
동시에 맡지 않는다는 조건 아래에서만 성립하는 미묘한 위치다.
그래서 OHTTP 보급의 병목은 게이트웨이의 성능이 아니라 Cloudflare와 결탁하지
않는다고 믿을 만한 릴레이 사업자가 몇이나 생기느냐가 될 것이다.

### 익명 통신의 오래된 교훈이 상업적 형태로 돌아왔다

릴레이와 게이트웨이를 나누는 구조는 믹스 네트워크와 Tor의 회로가 오래 다뤄 온
문제를 가장 짧은 경로로 줄인 것이라고 해석할 수 있다.
HN에서 maayank는 OHTTP를 게이트웨이가 정해진 2홉 Tor
회로에 비유했고,[^maayank] palata는 Tor만큼 멀리 가지 않으면서 훨씬 빠른
대신 훨씬 덜 사적인 절충이라고 정리했다.[^palata]
홉을 여러 개 두는 설계는 한 홉이 오염되어도 양 끝을 잇지 못하게 하려는
여유인데, 이 비유대로라면 OHTTP는 그 여유를 지연과 바꾼 셈이다.

익명성 시스템의 강도는 암호보다 익명 집합의 크기에 좌우된다.
palata가 친구끼리 쓰는 자체 호스팅 릴레이를 묻는 질문에 그렇게
하면 제3자 서비스가 그 서버에서 오는 요청이 친구 중 하나라는 것을 알게 된다고
답한 것도 같은 원리다.[^palata-crowd]
OHTTP의 프라이버시는 릴레이를 지나는 사용자가 많을수록 강해지므로,
작은 앱이 작은 릴레이와 짝을 지으면 보장은 문서상으로만 남는다.
글은 이 규모 의존성을 언급하지 않지만,
실무에서는 릴레이의 사용자 수가 HPKE의 강도보다 더 중요한 변수가 된다.

### 데이터를 덜 갖는 것이 규제 비용을 줄이는 수단이 된다

글의 첫머리는 사용자를 너무 많이 아는 것이 개발자에게 부담이라고 말하지만 그
부담이 무엇인지는 설명하지 않는다.
HN에서 jt2190은 그 부담이 무엇이냐고 물었고,[^jt2190] 9dev는 보관하는
데이터는 모두 유출되거나 오용될 수 있어 보호해야 하고,
규제를 지키며 고객이 떠나면 익명화하거나 지워야 하며,
백업을 불변으로 둘지 정리할지 같은 문제를 풀어야 한다고 답했다.[^9dev]

이 관점에서 OHTTP는 프라이버시 기술이라기보다 컴플라이언스 비용을
줄이는 아키텍처 선택이다.
처음부터 IP를 받지 않으면 IP를 지우는 절차, 보관 기한,
유출 시 신고 범위가 함께 줄어든다.
이는 데이터 최소 수집이라는 원칙을 정책 문서가 아니라 네트워크 구조로 구현하는
방식이라고 볼 수 있다.
그러나 글의 경고대로 요청 본문에 이메일이나 사용자 이름을 넣으면 이 이득은
사라지므로, OHTTP를 도입하는 팀은 네트워크 계층보다 API 설계에서 식별자를 빼는
작업에 더 많은 시간을 쓰게 될 것이다.

### 프라이버시 인프라는 신뢰가 낮은 사업자에게 더 어렵다

HN 스레드의 상당 부분은 OHTTP의 기술보다 Cloudflare라는 회사에
대한 불신으로 채워졌다.
ZiiS는 사용자 프라이버시를 지키고
싶다면 Cloudflare 같은 거대한 행동 수집 네트워크를 피하겠다며,
그들에게 추적을 넘기는 것보다 자기 로그를 익명화하는 편이 낫다고 썼다.[^ZiiS]
반면 johnhess는 이 구조가 누가 무엇을 보는지를 나누는 것이며,
누구와 이야기하는지와 무엇을 이야기했는지가 각각은 민감하지 않아도 둘을 함께
알면 위험한 위협 모델이 많다고 설명했다.[^johnhess]

이 대립은 프라이버시 제품이 지닌 역설을 드러낸다.
OHTTP 같은 설계는 특정 회사를 믿지 않아도 되게 하려는 것인데,
실제 보급은 이미 거대한 트래픽을 다루는 회사의 영업력과 인프라에 기댄다.
그 회사가 커질수록 제품은 쉬워지지만,
결탁하지 않는 두 주체라는 전제를 믿기는 어려워진다.
Cloudflare가 자기 자신을 두 홉에서 배제하는 규칙을 제품에 넣은 것은 이 역설에
대한 부분적인 답이지만, 사용자가 그 규칙이 지켜지는지 확인할 수단은 여전히 없다.

---

[^gruez]: <https://news.ycombinator.com/item?id=49946193>

[^gsnedders]: <https://news.ycombinator.com/item?id=49949431>

[^freedomben]: <https://news.ycombinator.com/item?id=49944816>

[^thayne]: <https://news.ycombinator.com/item?id=49946331>

[^arshxyz]: <https://news.ycombinator.com/item?id=49942183>

[^Joker_vD]: <https://news.ycombinator.com/item?id=49942567>

[^someonebaggy]: <https://news.ycombinator.com/item?id=49943819>

[^yencabulator]: <https://news.ycombinator.com/item?id=49945983>

[^ranger_danger]: <https://news.ycombinator.com/item?id=49950192>

[^maayank]: <https://news.ycombinator.com/item?id=49946480>

[^palata]: <https://news.ycombinator.com/item?id=49948101>

[^palata-crowd]: <https://news.ycombinator.com/item?id=49945743>

[^jt2190]: <https://news.ycombinator.com/item?id=49943848>

[^9dev]: <https://news.ycombinator.com/item?id=49944016>

[^ZiiS]: <https://news.ycombinator.com/item?id=49942822>

[^johnhess]: <https://news.ycombinator.com/item?id=49945607>
