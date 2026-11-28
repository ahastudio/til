# myQ 광고 알림과 ratgdo 교체

원문: [Garage Door Spam – Harrison Was Here](https://blog.harrison.page/garage-door-spam/)

HN 토론: <https://news.ycombinator.com/item?id=50519231> (817점, 342개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/tr5ghf/garage_door_spam> (3점, 2개 댓글)

## 요약

2026년 11월 16일 Harrison이 개인 블로그에 쓴 글이다.
저자는 차고 문이 열리거나 닫힐 때 알림을 받으려고 Chamberlain의 myQ 앱을 써
왔다.
집을 비운 사이 문이 열리면 이상 신호라서 알림이 의미 있다고 믿고 계속 썼다고
한다.
앱에는 원래 광고가 많았는데, 2026년 10월에 광고성 알림까지 오기 시작해 저자는
강한 말로 거부감을 밝힌다.

글에 따르면 Chamberlain은 2023년 말 myQ를 통한 제3자 API 접근을 막았다.
저자는 그 대응으로 ratgdo32 두 개를 사서 myQ를 거치지 않기로 했다.
ratgdo는 ratcloud llc가 파는 약 62달러짜리 와이파이 제어 보드이다.
오픈소스 펌웨어가 올라 있고 개폐기의 기존 단자에 연결해 LiftMaster의 Security+
2.0 프로토콜로 로컬에서 통신한다.

설치 뒤 흐름은 다음과 같다.

- 공유기가 보드 두 개에 고정 주소를 주고, Apple HomeKit이 바로 동작해 음성
명령으로 문을 연다.
- 보드는 자체 웹 화면과 JSON 상태 엔드포인트를 제공한다.
- 저자는 어린 시절 아버지가 차고 문에 수은 스위치를 달아 복도 불이 켜지게 했던
방식을 소프트웨어로 되살렸다.
- 밤 9시부터 새벽 5시 사이에 10분마다 `garage-watch` 스크립트가 상태를 확인하고
문이 열려 있으면 Slack으로 알린다.
- 저자가 올린 작은 풀 리퀘스트를 저장소 관리자가 병합하겠다고 답했다.
- 두 보드를 Tailscale 네트워크의 `/32` 경로로 광고해 모니터링 도구가
`/healthcheck`를 읽게 했다.

글은 모든 것이 클라우드 없이 로컬에서 돌고, 알림에 누가 문을 열었는지가 나온다고
맺는다.
이는 myQ가 하지 못한 일이라고 저자는 쓴다.
마지막 문장은 myQ 담당자에게 보내는 강한 비난이다.

## 분석

### 글의 줄거리는 신뢰의 이동이다

저자가 myQ를 쓴 이유는 알림이 의미 있다는 믿음이었다.
광고가 앱에 들어와도 그 믿음 때문에 계속 썼고, 광고가 알림 채널에 들어온 순간
믿음이 깨졌다.
그래서 이 글의 핵심은 광고 자체보다 알림 채널이 한 가지 의미만 갖는다는
전제이다.
이는 글의 서술을 이 문서가 정리한 것이다.

HN에서 avaer도 광고가 알림을 가로채는 점이 가장 거슬린다고 썼다.[^avaer]
wallst07은 광고가 나오는 기기는 팔거나 버리겠다는 기준을 세웠다.[^wallst07]
두 사람의 초점은 광고의 존재가 아니라 알림 채널의 오염이다.
Lobste.rs의 orib은 앱에 광고가 가득하다는 문장을 짚어 선을 그어야 할 곳은 거기였다고 적고, 돈을 낸 제품에 광고가 있으면 앱을 설치하지 않겠다고 했다.[^orib]

### 해법의 형태는 로컬 제어이다

저자는 클라우드를 대체한 다른 클라우드를 고르지 않았다.
기기 안의 오픈소스 펌웨어, 고정 주소, 로컬 프로토콜을 골랐고 결과적으로 광고가
들어올 경로가 없다.
HN의 dhc02는 ratgdo를 Home Assistant에 연결한 뒤 2년 동안 myQ에 한 번도
로그인하지 않았고 가족도 앱을 지웠다고 적었다.[^dhc02]
Lobste.rs의 kornel은 Home Assistant 커뮤니티가 나쁜 앱에서 기기를 해방하는 사람들의 모임이라고 적었다.[^kornel]
경로를 끊는 해법이 광고를 걸러내는 해법보다 단순하다는 점이 이 글들에서 같이
나온다.

다만 로컬 제어도 조건이 있다.
hahajk는 Tailwind를 로컬로 쓰려면 회사 포털에서 키를 받아야 한다고 지적하며, 한
클라우드를 다른 클라우드로 바꾸는 일은 신중하지 않다고 적었다.[^hahajk]
stickfigure는 납땜 없이 쓰는 대안으로 Tailwind를 추천했다.[^stickfigure]

### 아버지의 수은 스위치가 글의 중심 은유이다

글에서 가장 긴 문단은 수은 스위치 이야기이다.
저자는 가정에서 작동하던 단순한 신호를 소프트웨어 몇 줄로 되살렸고, 그 신호는
광고 없는 단일 목적이라는 점에서 같다.
이 대응은 저자의 설명이며, 같은 구조를 다른 기기에서도 재현할 수 있는지는 글에서
다루지 않는다.

## 비평

### 이 해법은 만들 수 있는 사람의 해법이다

HN의 superultra는 AI를 써도 보통 사용자가 해낼 수 없는 일이라고
적었다.[^superultra]
글은 설치 방법을 적지 않겠다고 하고 배선 과정을 생략한다.
납땜이 필요한 직접 제작 경로를 제시한 ryandrake와 납땜 없이 Shelly 릴레이와
ESPHome을 쓴 thedanbob의 사례도 있지만,[^ryandrake][^thedanbob] 이들 역시 기술
숙련자의 선택이다.
광고를 피하려고 직접 만들어야 한다면 문제는 개인이 아니라 제품에 남는다.

### 광고 알림이 규정 위반인지 글은 다루지 않는다

글은 광고성 알림을 불만으로 제시할 뿐 앱스토어 규정과의 관계를 묻지 않는다.
HN에서 AceJohnny2는 Apple의 앱 심사 지침 4.5.4가 홍보 목적 푸시를 사전 동의 없이
보내지 못하게 한다고 인용했다.[^AceJohnny2]
이에 zamadatix는 알림 수신 동의가 이미 있다면 규정 위반이 아닐 가능성이 크고,
광고 알림의 동의를 따로 끌 수 있어야 한다는 문구가 규정에 없다고
반박했다.[^zamadatix]
글의 불만이 규정 위반인지 규정의 공백인지는 열려 있다.

### 제조사 쪽 사정은 글에 없다

글은 myQ를 만든 쪽의 설명을 싣지 않는다.
2023년 말 제3자 접근을 막은 이유와 광고 알림이 어떤 정책에서 나왔는지는 글에서
확인되지 않는다.
HN의 variety8675는 Chamberlain이 새 프로토콜로 이런 우회를 막고 있다고
주장했다.[^variety8675]

### 한 사람의 사례가 시장 전체로 일반화되는 범위

저자의 경험은 한 가구의 한 제품이다.
blantonl은 이런 일을 enshittification이라 부르며 회의에서 누군가는 반대해야
한다고 적었고,[^blantonl] hobo123은 사모펀드에 인수된 작은 회사가 배당을 늘리려
광고를 넣는 경우를 추정했다.[^hobo123]
광고 수익을 노린 결정이 실제로 어떤 경로로 내려졌는지는 글과 댓글 모두 증거를
내놓지 못한다.

## 인사이트

### 알림 채널은 하나의 약속이다

사용자가 알림에 응답하는 이유는 알림이 중요하다고 배웠기 때문이다.
광고가 같은 채널에 들어오면 중요한 알림의 값도 같이 떨어진다.
저자의 문제 제기는 광고 불쾌감보다 문이 열렸다는 알림을 무시하게 될 수 있다는
위험에 가깝다.
이는 이 문서의 해석이다.

이 구조에서 앱 제작사는 알림 채널의 소유자가 아니라 빌려 쓰는 사람이다.
HN의 gwd는 항공편 변경 알림은 받고 홍보는 받지 않도록 분리해 켜고 끌 수 있어야
한다고 적었다.[^gwd]
채널 분리가 플랫폼 요건이 되면 제작사가 약속을 깨는 비용이 올라간다.

### 로컬 우선 제품이 인증 대상이 될 수 있다

gbdubs는 구독료, 데이터 판매, 광고가 없고 표준 프로토콜로만 통신하는 기기에
생태계 사업자가 인증을 주자고 제안했다.[^gbdubs]
MatekCopatek은 IoT에 표준화된 열린 프로토콜이 필요하다고 적었고,[^MatekCopatek]
hattar는 Home Assistant가 그 역할이라고 답했고,[^hattar] joshstrange는 Z-Wave와
Zigbee 기기가 인터넷에 접근하지 못해 푸시를 보내지 못한다고
적었다.[^joshstrange]
세 댓글을 합치면 광고 없는 기기를 만드는 방법은 네트워크 접근을 줄이는 것이고,
인증은 그 사실을 소비자에게 보여 주는 수단이다.
이 해석은 이 문서의 정리이며 인증이 실제로 효과를 낸다는 근거는 없다.

### 닫힌 기기는 전파 환경에도 영향을 준다

HN의 anticorporate는 myQ 기기가 와이파이와 BLE 사이에서 크게 신호를 내는 바람에
공기질 센서가 출력을 높였고, 공유기 채널을 바꿔 해결했다고
적었다.[^anticorporate]
이는 한 가구의 관찰이며 일반화할 수 없다.
다만 기기 하나가 앱과 알림 외에 네트워크 환경에도 영향을 줄 수 있다는 점은 집
안의 IoT를 한 번 점검해 볼 이유가 된다.

### 확인할 관찰

이 문서의 해석을 가를 관찰은 세 가지이다.
myQ가 광고성 알림을 켜는 기본값과 끄는 방법,
앱스토어 지침 4.5.4가 이런 알림에 실제로 적용되었는지,
ratgdo 같은 로컬 제어 장치를 일반 사용자가 설치할 때 걸리는 시간이다.

---

[^avaer]: <https://news.ycombinator.com/item?id=50558951>

[^wallst07]: <https://news.ycombinator.com/item?id=50558842>

[^dhc02]: <https://news.ycombinator.com/item?id=50560826>

[^hahajk]: <https://news.ycombinator.com/item?id=50561844>

[^stickfigure]: <https://news.ycombinator.com/item?id=50561225>

[^superultra]: <https://news.ycombinator.com/item?id=50560311>

[^ryandrake]: <https://news.ycombinator.com/item?id=50558972>

[^thedanbob]: <https://news.ycombinator.com/item?id=50559220>

[^AceJohnny2]: <https://news.ycombinator.com/item?id=50564683>

[^zamadatix]: <https://news.ycombinator.com/item?id=50564833>

[^variety8675]: <https://news.ycombinator.com/item?id=50560092>

[^blantonl]: <https://news.ycombinator.com/item?id=50560570>

[^gwd]: <https://news.ycombinator.com/item?id=50561316>

[^gbdubs]: <https://news.ycombinator.com/item?id=50560695>

[^MatekCopatek]: <https://news.ycombinator.com/item?id=50559855>

[^hattar]: <https://news.ycombinator.com/item?id=50560042>

[^joshstrange]: <https://news.ycombinator.com/item?id=50560303>

[^anticorporate]: <https://news.ycombinator.com/item?id=50559123>

[^hobo123]: <https://news.ycombinator.com/item?id=50562047>

[^orib]: <https://lobste.rs/s/tr5ghf/garage_door_spam#c_iadd40>

[^kornel]: <https://lobste.rs/s/tr5ghf/garage_door_spam#c_focg8c>
