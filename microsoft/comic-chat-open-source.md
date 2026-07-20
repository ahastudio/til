# Microsoft Comic Chat, 오픈소스로 공개

원문: <https://opensource.microsoft.com/blog/2026/07/16/microsoft-comic-chat-is-now-open-source/>

HN 토론: <https://news.ycombinator.com/item?id=48936426> (799점, 174개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/qbvfll/microsoft_comic_chat_is_now_open_source>

GN 토론: <https://news.hada.io/topic?id=31503>

## 요약

Microsoft가 1990년대 IRC 클라이언트인 Comic Chat의 소스 코드를
GitHub에 공개했다.
Comic Chat은 IRC 대화를 실시간으로 만화 패널로 변환하는 소프트웨어로,
1995년 Microsoft Research의 David "DJ" Kurlander가 구상하고
1996년 Internet Explorer 3과 함께 배포됐다.

핵심 기능은 단순한 텍스트의 시각화가 아니라 대화의 단서를 해석해
캐릭터의 자세, 표정, 제스처, 패널 배치를 실시간으로 결정하는
"편집 시스템"에 있었다.
이 기술은 DJ Kurlander, Tim Skelly, David Salesin이 1996년
SIGGRAPH 학술대회에서 발표했다.
비주얼은 독립 만화 예술가 Jim Woodring이 디자인했으며,
24개 언어로 현지화돼 Windows 98에도 번들로 포함됐다.

Comic Sans 폰트의 첫 번째 실제 용도가 이 소프트웨어였다는 사실도
함께 알려졌다.
1994년 타이포그래피 전문가 Vincent Connare가 설계한 Comic Sans가
Comic Chat에 처음 쓰이면서 세상에 나왔다.

공개된 저장소에는 Visual C++ 4.0과 MFC(Microsoft Foundation Classes)로
작성된 원본 코드와 함께, AI를 활용해 현대 Visual Studio에서 빌드하고
최신 IRC 서버에 연결하며 고해상도 환경에서 실행할 수 있도록
현대화한 작업도 포함되어 있다.
GitHub 저장소: <https://github.com/microsoft/comic-chat>

## 분석

### "시각화"가 아니라 "편집 결정"이었다

Comic Chat을 단순한 IRC 클라이언트의 시각적 테마로 보면 핵심을
놓친다.
이 소프트웨어가 당시에 주목받은 이유는 채팅 텍스트를 그림으로
"보여줬기" 때문이 아니라, 텍스트의 의미를 해석해 "편집 결정을
자동으로 내렸기" 때문이다.
느낌표가 많으면 캐릭터를 흥분한 자세로, 의문문이 연속되면
고개를 갸웃하는 제스처로 변환하는 방식은 오늘날 감성 분석
(sentiment analysis)이라 부르는 작업의 초기 형태다.
1996년 당시 이 수준의 대화 의미 해석을 실시간으로 처리했다는
점은 기술적으로 선구적인 시도였다.

Lobsters 토론에서 한 댓글은 이 점을 "단순한 인터페이스 스킨을
넘어선 의미 해석 능력"이라고 평가하며, 문자 기반 IRC 프로토콜
위에서 시각적 문맥을 만들어내는 방식에 기술적 관심을 표했다[^david_chisnall].

### Comic Sans의 기원이 이 소프트웨어였다는 것이 주는 아이러니

Comic Sans는 인터넷에서 "가장 미움받는 폰트"로 오랫동안 자리매김해
왔다.
그런데 그 출발점이 대화를 만화로 바꾸겠다는 혁신적 발상의 소프트웨어에
있었다는 사실은, 도구의 탄생 맥락과 그 이후의 사용 역사가 얼마나
다른 방향으로 갈 수 있는지를 보여주는 사례다.
Comic Chat의 목적—IRC 대화를 만화 문법으로 재구성하기—에는 Comic Sans가
맥락상 적절한 선택이었지만, 이후 사용자들이 그 폰트를 전혀 다른
맥락에 무분별하게 쓰면서 폰트 자체가 조롱의 대상이 됐다.
Lobsters 댓글에서는 Comic Sans 폰트 파일이 저장소에 MIT 라이선스 표시
없이 포함되어 있다는 점이 지적됐고, Microsoft는 이후 해당 파일을
저장소에서 제거했다[^invlpg][^kreeft].

### 제어 문자 문제가 IRC 생태계에 남긴 흔적

Comic Chat는 IRC 서버를 통해 다른 사용자에게도 암호화된 제어 문자를
함께 전송했다.
일반 IRC 클라이언트(예: mIRC)를 쓰는 사용자에게는 이 문자들이
의미 없는 쓰레기 문자로 나타났고, 이는 공유 IRC 서버에서 종종
불쾌한 경험을 만들었다.
Lobsters에서 david_chisnall은 이 문제 때문에 Comic Chat에서
mIRC로 전환했던 경험을 공유했다[^david_chisnall].
이는 Comic Chat의 혁신이 폐쇄적인 설계로 인해 생태계와 마찰을
일으켰음을 보여준다.
다른 클라이언트와 호환 가능한 형태로 설계했다면 더 널리 쓰였을
가능성이 있지만, 그 대신 독자적인 시각화 효과를 위해 상호운용성을
희생했다.

HN에서 Athas는 이 문자들이 "IRC 커뮤니티에서 비판받던 역사의
일부"라고 회상하며, Comic Chat이 캐릭터 모양과 감정 표현을
인코딩한 문자열을 IRC 프로토콜 확장으로 전송했음을 설명했다.
일반 클라이언트 사용자에게는 대화 내용 사이에 끼어드는 노이즈처럼
보였다는 것이다[^Athas].

HN에서 kylemaxwell은 다른 방향의 오해를 공유했다.
Chat를 사용하던 대학 시절, 채팅방의 다른 사람들도 모두 시각화를
보고 있다고 착각했다는 것이다.
수십 년이 지난 지금도 그 기억이 민망하다고 했다[^kylemaxwell].

## 비평

### 역사 보존의 의미와 AI 현대화 작업의 충돌

Microsoft가 밝힌 오픈소스 공개 목적은 "소프트웨어 역사 보존과
학습 기회 제공"이다.
그런데 공개된 저장소에는 AI를 활용한 현대화 코드가 함께 포함되어
있다.
원본 30년 된 코드를 역사적 기록으로 보존한다는 취지와,
그 코드를 AI 도구로 수정·현대화한 결과물을 같은 저장소에 두는 것은
서로 다른 목적이다.
어디까지가 원본이고 어디서부터 AI가 개입했는지 경계가 명확하지
않다면, 역사 자료로서의 신뢰도가 떨어진다.
Lobsters에서 natkr는 AI 기반 현대화 시도에 대한 우려를
표현했다[^natkr].

### "초기 웹의 실험 정신"이라는 프레이밍의 선택성

Microsoft의 블로그 글은 Comic Chat을 "초기 웹의 실험 정신"과
"장난스럽고 비관습적인 혁신"의 상징으로 묘사한다.
그러나 이 소프트웨어가 공개된 시점은 Microsoft가 넷스케이프를
상대로 브라우저 전쟁을 벌이며 인터넷 표준을 자사 플랫폼으로
끌어들이던 때와 겹친다.
Comic Chat이 Internet Explorer 3과 함께 번들로 제공됐다는 사실은,
혁신적 실험이 동시에 플랫폼 종속 전략의 일부였다는 맥락을
지운다.
30년이 지난 공개에서 당시의 경쟁 맥락이 빠진 채 "순수한 혁신의
역사"로만 서술되는 것은 지나치게 선택적인 역사 해석이다.

HN에서 afavour는 이 비판과 다른 방향에서 Comic Chat을 평가했다.
"채팅방이 만화처럼 보이면 어떨까?"라는 발상 자체는 당시 기준으로
얼마나 파격적이었는지 잊기 쉽지만, 실제로 그것이 개발되고 출시되어
24개 언어로 번역되고 Windows 98에 번들로 포함됐다는 사실이 인상적이라고
했다.
현대 개발이 검증된 패턴을 따르는 경향이 있는 것과 달리, 초기 웹은
이런 과감한 실험을 용납했다는 회고다[^afavour].

이번 오픈소스 공개를 직접 추진한 Robert Standefer는 HN에 직접 나타나
"이 일이 일어나기까지 6년이 걸렸으며, 적절한 시기에 적절한 장소에
있었던 덕분"이라고 밝혔다.
원개발자 DJ Kurlander도 공개에 적극적으로 지지하고 열정을
보였다고 전했다[^outintospace].

## 인사이트

### 1990년대 "만화 채팅"은 2020년대 "AI 아바타"의 선구자였다

Comic Chat이 해결하려 했던 문제—텍스트 기반 커뮤니케이션에
감정과 맥락을 입히기—는 오늘날 AI 아바타, 이모지 반응, 감성 분석
기반 UX로 다른 형태로 계속 시도되고 있다.
30년 전 IRC 위에서 만화 패널을 생성한 발상과,
오늘날 메시지 앱에서 표정 AI가 스티커를 자동 추천하는 발상은
같은 문제의식을 다른 기술로 구현한 것이다.
이 소프트웨어의 오픈소스 공개가 단순한 향수(nostalgia) 이상의
의미를 가지려면, 이 초기 연구가 현재의 감성 인식 UI 연구와
어떻게 연결되는지를 추적하는 학술적 작업이 뒤따라야 한다.

HN에서 JeremyHerrman은 Comic Chat에서 영감을 받아 2008년 Chogger라는
만화 창작 웹앱 스타트업을 창업했다고 밝혔다.
K-12 교육자들 사이에서 월간 3만 명 사용자까지 성장했으며, Adobe Flex와
ActionScript 3.0으로 구축했다고 한다.
말풍선 꼬리의 드래그 동작 하나를 완성도 있게 만드는 데 얼마나 많은
시간을 쏟았는지 회고하며, Comic Chat이 만화 인터페이스 창작 도구의
가능성을 보여준 선구자였음을 증언했다[^JeremyHerrman].

이 소프트웨어가 상업적 창작 환경에서도 사용됐다는 증언도 있었다.
klondike_klive는 BBC 디지털 채널의 코미디 스케치를 Comic Chat으로
제작하는 첫 번째 직업을 가졌다고 회상했다.
매우 낮은 프레임레이트의 만화처럼 촬영했다는 것으로, 당시 이 소프트웨어가
아마추어 채팅 도구가 아니라 전문 제작 현장에서도 쓰였음을 보여준다[^klondike_klive].

### 오래된 코드의 공개가 의미를 갖는 조건

Microsoft가 30년 된 코드를 오픈소스로 공개한 것은 긍정적인 움직임이다.
그러나 오래된 코드의 공개가 실질적 가치를 갖기 위해서는
단순히 저장소를 만드는 것 이상이 필요하다.
원본 설계 문서, 개발 배경에 대한 저자들의 회고, 당시 기술적
선택의 이유, 상용화 과정에서의 타협점 등이 함께 기록으로 남겨야
후대 연구자들이 이 코드에서 의미를 끌어낼 수 있다.
코드 자체는 "무엇을 만들었는가"를 보여주지만, 문서 없이는
"왜 그렇게 만들었는가"를 알 수 없다.
이번 공개에서 가장 아쉬운 것은 코드가 아니라 그 맥락의 부재다.

---

[^david_chisnall]: <https://lobste.rs/s/qbvfll/microsoft_comic_chat_is_now_open_source#c_19mgna>
[^invlpg]: <https://lobste.rs/s/qbvfll/microsoft_comic_chat_is_now_open_source#c_zogvik>
[^kreeft]: <https://lobste.rs/s/qbvfll/microsoft_comic_chat_is_now_open_source#c_tdsexf>
[^natkr]: <https://lobste.rs/s/qbvfll/microsoft_comic_chat_is_now_open_source#c_vl3q14>
[^Athas]: <https://news.ycombinator.com/item?id=48936972>
[^kylemaxwell]: <https://news.ycombinator.com/item?id=48940832>
[^afavour]: <https://news.ycombinator.com/item?id=48941619>
[^outintospace]: <https://news.ycombinator.com/item?id=48938312>
[^JeremyHerrman]: <https://news.ycombinator.com/item?id=48937630>
[^klondike_klive]: <https://news.ycombinator.com/item?id=48937921>
