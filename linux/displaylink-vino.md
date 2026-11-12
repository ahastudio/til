# Synaptics가 DisplayLink Linux 드라이버 개발자에게 특허 침해를 주장하며 작업을 멈추게 한 과정

원문: [Synaptics patent claims stop work on DisplayLink drivers](https://lwn.net/SubscriberLink/1102549/acbc92e00cee3a3f/)

HN 토론: <https://news.ycombinator.com/item?id=50443824> (446점, 254개 댓글)

GN 토론: <https://news.hada.io/topic?id=36962>

## 요약

LWN의 Joe Brockmeier가 쓴 이 기사는 스코틀랜드에 사는 개발자 Mike Lothian이
DisplayLink 독 드라이버를 개선하려다 Synaptics의 법무팀에게서 특허 침해 주장과
금전 요구를 받은 과정을 전한다.
Lothian은 Dell의 DisplayLink 칩셋 독을 쓰는데, 제조사의 Linux 소프트웨어가 계속
죽어서 Claude 구독으로 새 드라이버를 만들기로 했다.
DisplayLink는 2022년에 Synaptics에 인수되었다.

제조사 소프트웨어(DisplayLink Manager)는 바이너리만 제공되고 x86 전용이다.
다만 Linux DRM과 맞는 오픈소스 커널 모듈 EVDI는 따로 공개되어 있다.
회사는 DL3라는 독자 그래픽 기술이 USB, 영상, 오디오 채널을 압축해 USB 3로 보내고
다시 풀어 주기 때문에 소스를 공개하지 않는다고 설명한다.

Lothian은 6월 17일에 Rust로 쓴 DRM/KMS 드라이버 Vino의 첫 패치 묶음을 커널의
dri-devel 목록에 RFC로 올리고, 독의 제어 채널과 통신하는 단계에서 막혔다며 DL3
지식이 있는 사람의 도움을 청했다.
Danilo Krummrich가 Rust KMS 바인딩을 쓰도록 구조를 바꾸라는 조언을 했지만 그가
막힌 문제에 대한 답은 없었다.
같은 날 EVDI 저장소에 이슈를 열었으나 답이 없었고, 그가 찾은 EVDI 버그의 수정
요청(pull request)도 몇 달 동안 검토되지 않았다.

7월 20일 Synaptics의 Michal Lukaszek가 답장을 보냈다.
그는 DisplayLink가 열린 표준이 아니며 프로토콜과 코덱이 영국을 포함한 여러
관할의 특허로 보호된다고 알리고, 독자적으로 쓴 클린룸 구현도 특허 침해를 피하지
못할 수 있다고 적었다.
8월 17일에는 Synaptics의 지식재산 담당 부법무실장 Andrew Bateman이 중지 요구서를
보냈다.
이 서한은 특허 125개의 목록을 붙였지만 어느 특허를 침해했다는 것인지는 밝히지
않았고, 개발 중단과 이미 제출한 자료의 회수를 포함한 여덟 가지 요구와 8월
28일까지의 서명 확약을 요구했다.

Lothian은 8월 26일에 Vino 세 번째 판을 올리고, 27일에는 특허 청구항과 코드의
대응표(claim chart)를 요청했다.
그는 Synaptics가 특허 침해 방어를 돕는 Open Invention Network(OIN)의 회원이고
자신도 OIN 사용권자가 되었다고 적었다.
9월 19일 Bateman은 침해 사실을 문서화하고 있으며 그 작업 비용을 회수하는 “상당한
금전 보상”을 요구하겠다고 답했다.
10월 5일 서한에는 영국 특허 GB2484736B와 GB2485613B의 대응표가 붙었고,
25,000달러를 요구하며 매주 25,000달러씩 늘리겠다고 했다. 기한은 10월 11일에서
10월 18일로 연장되었고 더 이상의 연장은 없다고 했다.

OIN은 조사 끝에 Linux System Definition이 코덱을 명시되지 않은 한 포함하지
않으므로 Lothian의 작업에 보호가 미치지 않는다고 결론 내렸다.
OIN의 CEO Keith Bergelt는 10월 23일 기자에게 이를 확인했다고 기사는 전한다.
Lothian은 GitHub 저장소를 내렸고 Vino를 커널에 제출하지 않기로 했다. 그의 말은
방어할 여력이 없다는 것이다.

## 분석

### 특허 분쟁은 코드가 아니라 비용의 비대칭으로 결정되었다

사건의 전개에서 기술적 쟁점은 거의 다뤄지지 않는다.
Synaptics는 특허 125개의 목록을 던졌고, 대응표는 그가 요구한 뒤 두 달이
지나서야, 그리고 그 작성 비용을 청구하겠다는 조건으로 나왔다.
HN 사용자 gwittel은 어느 특허를 침해하는지 밝히는 작업에 수만 달러를 요구하는
것이 영국법에서도 정상인지 물었다.[^gwittel]
Lothian의 결론은 법리의 승패가 아니라 개인이 방어 비용을 감당할 수 없다는
것이다.
특허의 효력이 불확실해도, 다툴 수 있는 쪽이 한 사람이면 서한만으로 개발이
멈춘다.

### 보호 장치가 있다고 믿은 지점이 어긋났다

Lothian은 OIN이 이런 문제를 줄이기 위해 만들어졌다고 믿고 가입했다.
그러나 OIN의 보호 범위는 Linux System Definition에 든 구성 요소에 한정되고,
코덱은 명시된 것 외에는 제외된다.
Bateman도 DisplayLink 자체는 OIN 회원이 아니고 그 기술은 OIN을 통해 사용권을
얻을 수 없다고 두 번 짚었다.
회원 자격과 보호 범위가 별개라는 점이 이 사건의 핵심 오해였다.

### 이 사건은 LLM 개발 이야기이기도 하다

기사 첫머리는 Lothian이 LLM의 도움으로 드라이버를 개발했다고 소개한다.
HN 사용자 joshuafuller는 한 개발자가 AI의 도움으로 제조사가 고치지 못한 하드웨어
지원을 개선했는데 제조사가 이를 환영하는 대신 재정적 파멸로 위협했다는 점을 가장
불편하게 읽었고, AI가 역공학과 상호운용 작업의 문턱을 낮출수록 이런 대응이 늘
것이라고 예상했다.[^joshuafuller]
saghm은 한 사람이 LLM과 여가 시간으로 모든 것을 역공학할 수 있다면 경쟁사도 할
수 있다는 점을 짚었다.[^saghm]
Synaptics가 서한에서 우려했다고 기사가 전한 경쟁 우위 약화 주장은 이 지점에서
스스로 모순된다.

## 비평

### 기사는 특허의 효력을 거의 검토하지 않는다

기사는 Synaptics의 주장과 Lothian의 대응을 충실히 전하지만 특허가 실제로 구현을
덮는지는 다루지 않는다.
xxpor는 역공학 자체가 특허 침해가 아니며 특허는 공개의 대가로 독점권을 주는
제도이므로 비밀 유지를 주장하려면 영업비밀 쪽을 말해야 한다고 짚었다.[^xxpor]
yieldcrv도 경쟁 우위가 비공개 기술에 있다는 주장은 공개와 독점을 맞바꾸는 특허의
성격과 어긋난다고 보았다.[^yieldcrv]
이 반론들은 법률 전문가의 판단이 아니며 영국과 미국의 법 차이도 반영하지 못한다.
그래도 글이 이 쟁점을 한 줄도 다루지 않아 독자는 Synaptics의 주장이 얼마나
강한지 알 수 없다.

### 댓글의 선행 기술 주장은 확인되지 않았다

Beijinger는 GB2484736의 독립 청구항이 원래 네트워크 전송 제한이 없어 선행 기술
때문에 특허를 받을 수 없다고 판정되었다는 심사 기록을 근거로 이 특허가 무효가 될
가능성이 높다고 예측했다.[^Beijinger]
cannonpalms는 몇 분 만에 선행 기술 열두 건을 찾았다고 했다.[^cannonpalms]
둘 다 비전문가의 조사이고 확인되지 않았다.
이런 주장은 무효 심판이 얼마나 가능성이 있는지에 대한 힌트일 뿐, Lothian이
방어할 수 있다는 근거가 되지 않는다. 그가 겪은 문제는 승소 가능성이 아니라
비용이기 때문이다.

### 호환성 문제를 해결할 대안이 이미 있다는 점이 빠졌다

여러 댓글은 DisplayLink가 사라져도 되는 기술이라고 말한다.
kieranl은 최근 Thunderbolt와 USB4 독은 디스플레이 지원이 좋고 DisplayPort 대체
모드로 돌아간다고 썼고,[^kieranl] isityettime은 순수 Thunderbolt 독만 쓰고
있으며 호환성이 훨씬 낫다고 했다.[^isityettime]
steventhedev는 20달러짜리 DP 분배기가 더 낫고 DisplayLink 드라이버가 CPU를 100%
쓰고 매주 커널 패닉을 일으켰다고 썼다.[^steventhedev]
이는 각자의 경험이고 대안은 대역폭과 하드웨어 요건이 있다. 그러나 기사는 이
대안을 언급하지 않아 이 분쟁이 얼마나 많은 사용자에게 영향을 주는지 판단하기
어렵다.

## 인사이트

### LLM이 구현 비용을 낮추면 분쟁은 법률 쪽으로 옮겨 간다

역공학과 드라이버 작성의 비용이 줄면 막을 수 있는 수단이 기술적 장벽에서 법적
위협으로 이동한다.
이 사건에서 Lothian은 6월 17일의 첫 RFC에서 8월 26일의 세 번째 판까지 두 달여
만에 세 세대의 독을 제어하는 단계까지 갔다.
빠르게 만들 수 있는 쪽과 느리게 방어할 수 있는 쪽 사이의 비대칭은 개인
개발자에게 불리하다.
이 해석은 이 문서의 추론이며, Synaptics의 내부 동기는 기사에서 확인되지 않는다.

### 상호운용성 작업은 청구서가 먼저 온다

denkmoon은 독점 하드웨어의 오픈소스 지원을 개선하는 프로젝트를 자기 이름으로
하지 않겠다고 썼다.[^denkmoon]
도움을 구하려고 공개한 행위가 법무팀의 주목을 부른 점이 이 사건의 아이러니다.
Lothian은 질문과 RFC를 공개 목록에 올렸고, 그 공개가 Synaptics가 중지 요구의
근거로 든 “공개 발언”이 되었다.
공개는 커뮤니티 협업의 방식이지만 개인에게는 법적 노출이다. 이 점은 법무 지원이
없는 개인 개발자가 지켜야 할 순서를 바꾼다.

### 결론을 바꿀 관찰

- 대응표가 가리키는 청구항이 Vino의 동작을 실제로 덮는지 독립된 전문가가 검토해
  아니라고 결론 내리면, 이 사건은 법리가 아니라 위협의 사례로 읽힌다.
- Synaptics가 이후 Linux 지원을 자체적으로 개선하거나 EVDI 변경을 받아들이면,
  이번 대응은 개인의 공개 개발에 대한 방어적 반응이었다는 해석이 힘을 얻는다.
- OIN이 코덱 제외 정의를 바꾸면 보호 범위에 대한 오해의 비용이 줄어든다.

---

[^gwittel]: <https://news.ycombinator.com/item?id=50444607>

[^joshuafuller]: <https://news.ycombinator.com/item?id=50445498>

[^saghm]: <https://news.ycombinator.com/item?id=50444720>

[^xxpor]: <https://news.ycombinator.com/item?id=50444813>

[^yieldcrv]: <https://news.ycombinator.com/item?id=50448303>

[^Beijinger]: <https://news.ycombinator.com/item?id=50444444>

[^cannonpalms]: <https://news.ycombinator.com/item?id=50453234>

[^kieranl]: <https://news.ycombinator.com/item?id=50444959>

[^isityettime]: <https://news.ycombinator.com/item?id=50450497>

[^steventhedev]: <https://news.ycombinator.com/item?id=50450022>

[^denkmoon]: <https://news.ycombinator.com/item?id=50447848>
