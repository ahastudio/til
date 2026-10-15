# Apple HomeView: 얼굴로 사용자를 알아보는 Apple의 가정용 스마트 디스플레이

<https://www.apple.com/apple-homeview/>

HN 토론: <https://news.ycombinator.com/item?id=50071017> (724점, 850개 댓글)

GN 토론: <https://news.hada.io/topic?id=35305>

## 소개

Apple HomeView는 Apple이
2026년 10월 13일 발표한 7인치 가정용 스마트 디스플레이다.[^newsroom]
보도자료는 HomeView를 집의 중심에 두면서
집 안 모두에게 개인적인 기기로 설명하며,
음악, FaceTime 통화, 집 모니터링,
음성 자동화를 한곳에 모았다고 소개한다.[^newsroom]
같은 날 차세대 HomePod mini, 새 Apple TV 4K,
스마트 홈 액세서리 라인업 Apple Home Collection도
함께 발표되었다.[^newsroom-rss]

탁상형과 벽걸이형 두 가지가 있다.
탁상형은 실버, 스타라이트, 로즈 핑크, 스페이스 그레이 네 가지 색이고,
돔 모양 알루미늄 받침에 스테인리스 경첩을 달아 화면 각도를 조절한다.[^product]
벽걸이형은 스페이스 그레이와 실버 두 가지이며
현관이나 복도 같은 곳에 두는 용도다.[^product]

## 주요 기능

### 하드웨어

| 항목   | 사양                                                                   |
| ------ | ---------------------------------------------------------------------- |
| 칩     | A18                                                                    |
| 화면   | 7인치 Liquid Retina, True Tone, 밝기 500니트~0.3니트                   |
| 카메라 | 12MP Center Stage                                                      |
| 마이크 | 빔포밍 마이크 4개                                                      |
| 스피커 | 화면에 풀레인지 드라이버 2개, 받침에 하향 우퍼와 패시브 라디에이터 2개 |

사양은 제품 페이지 기준이다.[^product]
0.3니트는 Apple이 “역대 가장 낮은” 밝기라고 부르는 값으로,
침실 머리맡에서 쓰는 경우를 겨냥한다.[^product]
일부 기능은 사용자가 가까이 다가올수록 더 많은 정보를 보여 준다.[^product]

### 여러 사용자와 Secure Exclaves

HomeView는 최대 6명을 얼굴로 알아보고 사람마다 다른 화면을 보여 준다.[^product]
개인 콘텐츠는 세 조건이 모두 맞을 때만 열린다.
짝지은 iPhone이나 iPad가 같은 Wi-Fi에 연결되어 있고, 최근에 잠금이 풀렸으며,
HomeView가 그 사람의 얼굴을 알아봐야 한다.[^product]

얼굴과 목소리 인식은 A18 칩 안의 Secure Exclaves에서 처리한다.
Apple은 이 영역이 카메라와 마이크 입력을 운영체제나 Apple이 접근할 수 없는
분리된 공간에서 처리하므로,
인식에 쓰는 영상과 음성이 운영체제에 노출되지 않는다고 설명한다.[^product]

### Siri AI

HomeView에는 Apple Intelligence 기반의 새 Siri인 Siri AI가 들어 있다.
보도자료는 Siri AI를 훨씬 더 유능하고 대화가 자연스러우며
폭넓은 세계 지식을 가진 완전히 새로운 Siri라고 소개한다.[^newsroom]
Apple Intelligence를 지원하는 기기와 짝지으면 그 사용자의 캘린더, 메시지 등
개인 맥락을 바탕으로 답한다.[^newsroom]
HomeView에서 나눈 대화는 다른 Apple 기기의 Siri 앱과 동기화된다.[^product]
처음에는 영어만 지원하며 사용량 제한이 있을 수 있다.[^product]

### 홈 허브와 엔터테인먼트

HomeView는 스마트 홈 액세서리의 중앙 허브로 동작한다.
Home 앱이 내장되어 있어 현관 방문자 확인, 카메라 영상 최대 9개 동시 보기,
조명과 온도 조절, 장면과 자동화 실행을 할 수 있다.[^product]
연기와 일산화탄소 경보기 소리를 감지해 iPhone, iPad, Apple Watch로 알리고,
Apple Intelligence가 가족의 귀가, 문 잠금 해제, 경보 해제 같은
관련 알림을 하나로 묶는다.[^product]

엔터테인먼트는 Apple 앱 일부와 iPhone의 호환되는
타사 오디오·비디오 앱을 지원한다.[^product]
Photos, Snoopy, Calendar, Weather, 사용자의 움직임에 반응하는 Flow 같은
화면(face)을 골라 디지털 액자처럼 쓸 수도 있다.[^product]

## 가격과 출시

| 모델                          | 가격(미국)             |
| ----------------------------- | ---------------------- |
| Apple HomeView                | 299달러                |
| Apple HomeView (Wall Mounted) | 299달러                |
| Power Mount USB-C 벽 커넥터   | 59.95달러부터          |
| Power Mount AC 유선           | 79.95달러부터          |
| Power Mount PoE 유선          | 129.95달러 (2027년 초) |

벽걸이용 마운트는 Schneider Home이 만든다.[^newsroom]
미국, 영국, 캐나다, 호주, 뉴질랜드, 인도에서 발표 당일부터 사전 주문을 받고,
11월 13일부터 판매한다.[^newsroom]
싱가포르는 10월 15일부터 사전 주문을 받는다.[^newsroom]
한국은 출시 국가 목록에 없다.

유럽연합에서는 팔지 않는다.
Apple은 EU의 iOS에서 Siri AI를 아직 쓸 수 없기 때문이라고 밝히고,
EU와 해결책을 찾기 위해 협력하고 있다고 했다.[^newsroom]

## 분석

### 경쟁자는 Echo Show가 아니라 서랍 속의 옛 iPad다

HN에서 가장 많은 답글을 받은 schmichael의 댓글은
이 제품의 가장 큰 경쟁자가 “옛 iPad”라고 했다.
옛 iPad에는 배터리가 있고, 앱이 있고,
대개 더 큰 화면이 있다는 것이다.[^schmichael]
BurritoAlPastor는 HomeView가 존재하는 이유를 Matter 허브에서 찾았다.
iPad나 다른 휴대용 Apple 기기는 Matter 기기를 관리하는
홈 허브로 설정할 수 없다는 것이다.[^BurritoAlPastor]
smileybarry는 기술 사양에 Thread 라디오가 있고
HomeKit이나 Matter Thread 액세서리와 호환된다고
적혀 있다는 점을 짚었다.[^smileybarry]
jdminhbg는 옛 iPad가 모든 면에서 낫지만
가족이 함께 쓰는 기기에서 가장 중요한 멀티유저 지원만은
없다고 반박했다.[^jdminhbg]

이 반박이 제품의 정체를 드러낸다.
HomeView의 핵심은 화면이나 스피커가 아니라
여러 사람이 같은 기기를 쓰면서도 각자의 메시지와 캘린더를 지키는 구조다.
얼굴 인식, Secure Exclaves,
짝지은 iPhone의 잠금 해제 상태를 조건으로 거는 설계는
모두 이 하나의 문제를 위한 것이다.
iPadOS가 10년 넘게 풀지 못한 멀티유저를 새 기기에서 처음부터 설계한 셈이다.

### 늦게 들어온 시장, 그리고 Siri

Amazon Echo Show는 2017년, Google Nest Hub는 2018년에 나왔다.
tantalor는 기존 제품들이 이미 여러 세대를 거치며 크기와 기능이 다양해졌는데
Apple은 2026년에야 들어왔다고 지적했다.[^tantalor]
joshstrange는 소문에 따르면 하드웨어는 몇 년 전에 준비되었지만
쓸 만한 Siri가 나올 때까지 출시를 미뤘다고 전했다.[^joshstrange-siri]
EU 출시를 포기한 이유가 Siri AI라는 점은 이 해석을 뒷받침한다.
timpera는 Google Nest Hub를 몇 년 써 봤지만 AI 없이도 충분히 유용했다며,
Apple이 Siri AI 없이는 이 제품을 팔 수 없다고 본 점이 흥미롭다고 했다.[^timpera]

### 299달러라는 가격의 의미

vessenes는 디자인이 좋고 가격이 매우 공격적이라며,
Apple이 이 기기를 많은 집에 넣으려고 진지하다는 신호로 읽었다.[^vessenes]
r0fl은 Apple TV와 같은 가격이라며 부모님과 처가에 선물하겠다고 했다.[^r0fl]
harrouet은 진입 가격은 싸지만 시스템을 넓히려면
액세서리에 돈을 더 쓰게 될 것이라고 경고했다.[^harrouet]
같은 날 발표된 Apple Home Collection과 벽걸이용 마운트의 가격을 보면
HomeView는 스마트 홈 생태계로 들어가는 입구 상품에 가깝다.

## 비평

### “앱 없음”은 의도인가, 한계인가

HomeView는 App Store를 지원하지 않는다.
Brendinooo는 요리하면서 하는 영상 통화는
실제로는 Messenger나 Snapchat으로 하는데
App Store에 제대로 접근하지 못하면 자신에게는 쓸모가 없다고 했다.[^Brendinooo]
santah는 앱도 영상 스트리밍도 없다는 점이 충격적이라며,
그것만 있으면 이상적인 주방용 TV였을 것이라고 했다.[^santah]
제품 페이지는 iPhone의 호환 앱을 지원한다고 하지만
어떤 앱이 어떤 조건에서 호환되는지는 밝히지 않는다.[^product]

반론도 있다.
notfried는 Apple TV도 첫 세대 뒤 8년이 지나서야 App Store를 얻었다며
Apple이 앱 범주를 제한해 나중에 열 것이라고 봤다.[^notfried]
npunt는 앱이 주의를 빼앗는 문제를 만들어 왔고,
노인과 아이에게는 앱 없는 기기가 오히려 낫다고 했다.[^npunt]
문제는 Apple이 어느 쪽인지 말하지 않는다는 점이다.
앱이 없는 것이 설계 철학이라면 그렇게 설명해야 하고,
일시적인 제약이라면 언제 풀리는지 밝혀야 한다.

### 프라이버시 약속은 검증할 수 없다

fmarasho는 Secure Exclaves 설명이 흥미롭다고 했지만,[^fmarasho]
cromka는 같은 방식이 최신 Apple Watch의 상시 녹음에도 쓰였다며
기술의 허용 범위가 한 걸음 더 넓어지는 것으로 봤다.[^cromka]
isodev는 Apple이 집 안의 모든 것을 기록하되 쓰지는
않겠다고 약속하는 것을 믿기 어렵다며,
Apple도 이제 광고 사업을 한다고 지적했다.[^isodev]

Apple의 설명은 운영체제와 Apple이 카메라·마이크 입력에 접근할 수 없다는 것이다.
그러나 이 주장은 외부에서 검증할 방법이 제시되지 않았다.
제품 페이지와 보도자료 어디에도 외부 연구자가
이를 확인할 방법은 언급되지 않는다.
거실에 상시 카메라와 마이크 네 개를 두는
기기라면 약속보다 검증 경로가 먼저여야 한다.

### 가족 광고는 사용 이유를 증명하지 못했다

atourgates는 자기 가족이 광고 속 가족과 똑같은데도
이 기기가 무엇을 낫게 할지 상상하기 어렵다고 했다.
캘린더, FaceTime,
메시지가 필요한 가족은 이미 모두 휴대폰으로 하고 있다는 것이다.[^atourgates]
tqi는 광고에
나온 용도(레시피 찾기, 나의 찾기, 잡학 질문, 캘린더 확인)가 최선이라면
휴대폰 대신 이것을 쓸 이유가 거의 없다고 했다.[^tqi]
반면 postalcoder는 HN의 압도적인 냉소가
오히려 흥행의 신호라고 했다.[^postalcoder]

## 인사이트

### 멀티유저는 하드웨어 문제가 되었다

iPad의 멀티유저 지원이 오래 요구되었는데도 나오지 않은 이유는
단순한 소프트웨어 기능이 아니기 때문이다.
HomeView는 사람을 구분하는 일을 얼굴 인식과 Secure Exclaves,
짝지은 iPhone 상태에 맡겼다.
즉 “누가 이 화면을 보고 있는가”를 칩 수준의 격리와 다른 기기의 신호로 판단한다.

이 설계가 성공하면 같은 구조가 iPad, Mac, Apple TV로 번질 가능성이 크다.
멀티유저가 계정 전환 메뉴가 아니라
기기가 사람을 알아보는 방식으로 바뀌는 것이다.
반대로 그만큼 공용 기기의 프라이버시는 하드웨어 격리에 대한 신뢰에 기대게 된다.

### 규제가 AI 기기의 출시 지도를 바꾸고 있다

HomeView는 하드웨어가 아니라 AI 기능 때문에 EU에서 팔리지 않는다.
Apple이 Siri AI 없이는 제품이 성립하지 않는다고 판단했다는 뜻이다.
앞으로 AI가 핵심인 기기일수록 규제 환경에 따라 출시 국가가 갈릴 것이고,
같은 브랜드의 같은 제품군이 지역마다 다른 기능을 가진 채 나뉘게 된다.

한국이 출시 국가 목록에 없는 것도 같은 맥락에서 볼 수 있다.
Siri AI는 영어만 지원하므로,
언어 지원이 하드웨어 출시의 선행 조건이 되었다.

### 스마트 디스플레이는 화면이 아니라 허브로 경쟁한다

Echo Show와 Nest Hub가 증명한 것은
작은 화면 자체로는 큰 가치를 만들기 어렵다는 점이다.
HomeView가 Thread 라디오, Matter 허브, Home 앱, Apple Home Collection을
한꺼번에 내놓은 것은 경쟁 무대를 화면에서 집 전체의 허브로 옮기려는 시도다.
299달러는 그 생태계로 들어오는 입장료이고,
실제 매출은 그 뒤에 따라오는 카메라,
도어락, 온도 조절기, 설치 서비스에서 나온다.

## 구매 전에 확인할 세 가지

첫째, 가족이 같은 화면을 공유하면서 개인 정보를 분리해야 하는가.
그렇지 않다면 이미 가진 태블릿이나 스마트 스피커가
더 단순한 대안일 수 있다.

둘째, 꼭 필요한 앱과 영상 서비스가 제품에서 실제로 동작하는가.
App Store가 없고 타사 앱 지원 범위도 설명되지 않았으므로,
광고의 사용 장면만으로 원하는 앱의 호환성을 추정해서는 안 된다.

셋째, 얼굴과 음성 인식의 처리 경계를 신뢰할 수 있는가.
제품 설명은 Secure Exclaves를 근거로 들지만,
사용자가 확인할 수 있는 감사 방법은 제시하지 않는다.
민감한 공간에 둘 예정이라면 개인 정보 처리 설명,
카메라·마이크 비활성화 방법,
각 가족 구성원의 동의와 사용 습관까지 구매 조건에 넣어야 한다.

따라서 HomeView의 가치는 7인치 화면의 기능 수가 아니라
공용 기기에서 사용자 식별과 집 제어를 얼마나 안심하고 맡길 수 있는지로
판단해야 한다.

---

[^newsroom]: Apple Newsroom, [Meet Apple HomeView, a new way to enjoy entertainment, stay connected, and manage the home](https://www.apple.com/newsroom/2026/10/meet-apple-homeview-a-new-way-to-enjoy-entertainment-and-manage-the-home/), 2026-10-13

[^newsroom-rss]: Apple Newsroom, [Apple Newsroom RSS feed](https://www.apple.com/newsroom/rss-feed.rss), 2026-10-13 항목들

[^product]: Apple, [Apple HomeView - Apple](https://www.apple.com/apple-homeview/), 게시일 표시 없음 (2026-10-14 열람)

[^schmichael]: <https://news.ycombinator.com/item?id=50073524>

[^BurritoAlPastor]: <https://news.ycombinator.com/item?id=50077508>

[^smileybarry]: <https://news.ycombinator.com/item?id=50082207>

[^jdminhbg]: <https://news.ycombinator.com/item?id=50073881>

[^tantalor]: <https://news.ycombinator.com/item?id=50072053>

[^joshstrange-siri]: <https://news.ycombinator.com/item?id=50071214>

[^timpera]: <https://news.ycombinator.com/item?id=50071097>

[^vessenes]: <https://news.ycombinator.com/item?id=50071266>

[^r0fl]: <https://news.ycombinator.com/item?id=50071722>

[^harrouet]: <https://news.ycombinator.com/item?id=50072438>

[^Brendinooo]: <https://news.ycombinator.com/item?id=50071584>

[^santah]: <https://news.ycombinator.com/item?id=50071191>

[^notfried]: <https://news.ycombinator.com/item?id=50071976>

[^npunt]: <https://news.ycombinator.com/item?id=50080803>

[^fmarasho]: <https://news.ycombinator.com/item?id=50072808>

[^cromka]: <https://news.ycombinator.com/item?id=50072866>

[^isodev]: <https://news.ycombinator.com/item?id=50073131>

[^atourgates]: <https://news.ycombinator.com/item?id=50073157>

[^tqi]: <https://news.ycombinator.com/item?id=50079074>

[^postalcoder]: <https://news.ycombinator.com/item?id=50071664>
