# F-Droid 2.0: 10년 만의 재작성이 자유 앱 스토어를 평범한 앱 스토어처럼 쓰게 만든다

원문: [F-Droid 2.0: A New Chapter for Android Freedom | F-Droid - Free and Open Source Android App Repository](https://f-droid.org/2026/09/24/f-droid-2.0-a-new-chapter-for-android-freedom.html)

HN 토론: <https://news.ycombinator.com/item?id=49831968> (1248점, 349개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/opt2ma/f_droid_2_0> (42점, 5개 댓글)

GN 토론: <https://news.hada.io/topic?id=34230>

## 요약

F-Droid가 2026년 9월 24일, 공식 F-Droid 앱을 완전히 다시 설계한 F-Droid 2.0을 발표했다.
1년 넘는 작업 끝에 나온, 10년 만의 가장 큰 앱 업데이트이며, 14번의 시험 릴리스를 거쳐 앞으로 몇 주에 걸쳐 사용자에게 순차적으로 배포된다.
겉모습만 바꾼 것이 아니라 Material Design 같은 현재의 Android 관례에 맞춰 사용자 경험을 다시 짰고, 핵심 구성 요소를 Kotlin과 Jetpack Compose로 다시 썼다.

탐색은 발견(Discover), 검색(Search), 내 앱(My Apps)의 세 영역으로 단순해졌다.
카테고리는 발견 화면에 통합됐고, 설정과 Nearby Swap은 상단 막대로 옮겨졌다.
발견 화면은 새로 추가되거나 최근 갱신된 앱과 함께 저장소에서 가장 많이 내려받은 앱을 보여 준다.
카테고리는 VPN, 방화벽, 비밀번호 관리자, 런처, 내비게이션 같은 세분화된 분류로 크게 늘었고, 이를 묶는 상위 “메타” 카테고리가 생겼으며, 게임은 17개 장르로 나뉘었다.
검색은 앱 이름뿐 아니라 설명, 카테고리, 번역된 내용까지 찾고, 중국어, 일본어, 한국어 검색이 크게 좋아졌으며, 최근 검색어를 기억한다.
카테고리, 기기 호환성, 안티 기능(anti-feature)을 조합하는 필터로, 예컨대 기기와 호환되는 액션 게임 가운데 비자유 네트워크 서비스에 기대지 않는 것만 볼 수 있다.

설치 경험도 바뀌었다.
EU 디지털시장법(DMA)과 세계 곳곳의 반독점 조치의 압력 덕분에 Android가 모든 앱 스토어에 더 매끄럽고 자동적인 설치와 업데이트 선택지를 주게 됐고, F-Droid 2.0은 이를 이용한 통합 설치기를 쓴다.
사전 승인 API를 써서, 지원하는 기기에서는 앱을 내려받은 뒤가 아니라 설치를 결정한 직후에 사용자가 확인할 수 있다.
업데이트 확인과 설치는 기본적으로 자동이 됐고, 당겨서 새로 고침 동작은 없어졌으며, 수동 확인은 내 앱 화면의 더 보기 메뉴로 옮겨졌다.

빠진 것도 있다.
“Tor 사용” 설정은 일반 프록시 설정으로 옮겨졌고, 앞으로는 Tor VPN이 권장된다.
계산기처럼 위장하던 앱 숨김 기능은 아이콘과 이름만 바꾸는 표준적인 방식으로 단순해졌는데, 설정의 앱 목록에는 여전히 보이고 포렌식 검사에서 드러날 수 있다는 한계를 사용자가 알게 하려는 선택이라고 설명한다.
Ripple 같은 비상 트리거 앱에 반응해 앱을 지우는 기능은 아직 돌아오지 않았으며, 이 기능에 기대는 사용자는 업데이트를 미룰 수 있다고 밝힌다.
F-Droid Privileged Extension(FPE)은 2.0에서 지원하지 않으며, Android의 “세션” 설치기만으로 최근 Android 버전 어디서나 백그라운드 업데이트를 할 수 있게 했다.
Android 7에 들어간 수정에 기대는 도구 때문에 Android 6 지원은 끊겼고, 옛 릴리스는 옛 Android에서 계속 동작한다.

개발은 NLnet의 Mobifree 기금이 Torsten Grote의 작업을 지원했고, Open Technology Fund의 UX 연구실이 Ura Design과 함께 사용자 조사와 디자인을, OTF 보안 연구실이 Convocation과 함께 독립 보안 검토를 맡았으며, NGI와 Calyx Institute도 지원했다.
F-Droid는 Kotlin과 Compose로의 재작성이 새 기여자의 진입 장벽을 낮추고 다음 10년의 기반이 될 것이라고 말하며, 서버 없이 기기끼리 앱을 나누는 Nearby는 새 구현을 개발 중이라고 밝힌다.

## 분석

### 자유 소프트웨어 스토어가 “평범한 앱 스토어”의 문법을 받아들였다

F-Droid 1.x는 기능적이었지만 오래된 Android 앱처럼 느껴졌다.
Lobste.rs에서 wezm은 이 업데이트가 환상적으로 보인다며, 1.x 앱은 제 기능은 했지만 확실히 옛날 Android 앱 같았다고 적었다.[^wezm]
Hacker News에서 silverbluep는 F-Droid의 UI가 형편없고 Privileged Extension을 설정하기가 고통스러워서 몇 년 동안 GrapheneOS에서 Droid-ify를 써 왔다고 했고,[^silverbluep] outadoc도 같은 이유로 Droid-ify를 쓰다가 공식 앱으로 돌아가겠다고 했다.[^outadoc]

2.0의 변화는 대부분 상용 앱 스토어가 오래전에 정한 문법을 따른다.
세 탭 탐색, 인기 앱 목록, 세분화된 카테고리, 자동 업데이트, 설치 전 확인은 Play 스토어 사용자에게 익숙한 것들이다.
F-Droid는 이것을 “추적하지 않고, 앱에 더 오래 머물게 하려 하지 않는다”는 조건 아래 가져왔다고 강조한다.
자유 소프트웨어의 가치를 지키면서 사용성의 격차를 줄이는 것이 이번 재작성의 목표다.

### 매끄러운 설치를 가능하게 한 것은 기술이 아니라 규제다

글에서 가장 정치적인 문장은 설치 경험에 관한 것이다.
F-Droid는 오랫동안 설치와 업데이트 경험이 Android에 의해 “2등급으로 강요받았다”고 말하며, 이제 그것이 바뀐 것은 대체로 EU 디지털시장법과 세계 곳곳의 반독점 조치 덕분이라고 밝힌다.
F-Droid가 오래 Privileged Extension이라는 우회로를 유지해야 했던 이유도, 일반 앱 스토어에게는 기본 스토어만큼의 설치 권한이 주어지지 않았기 때문이다.

그래서 FPE를 끊은 결정은 기술 부채의 정리이면서 규제 환경 변화의 결과다.
Hacker News에서 mzajc는 FPE를 지원하지 않는 것이 아쉽다며 유지 부담이 그렇게 크냐고 물었다.[^mzajc]
F-Droid의 답은 세션 설치기만으로 최근 Android 어디서나 백그라운드 업데이트가 가능해졌으니, 시스템 깊숙이 설치해야 하는 확장을 따로 유지할 이유가 줄었다는 것이다.
플랫폼이 스스로 문을 열자, 문을 억지로 열던 도구가 필요 없어졌다.

### 기능을 덜어낸 방식이 이 프로젝트의 사용자층을 보여 준다

글은 빠진 기능을 숨기지 않고 길게 설명한다.
특히 앱 숨김과 비상 삭제 기능에 대한 설명은, F-Droid의 사용자 가운데 어떤 앱을 설치했다는 사실만으로 주목받을 수 있는 환경의 사람들이 있다는 점을 전제로 한다.
계산기로 위장하던 기능을 아이콘과 이름만 바꾸는 방식으로 줄인 것은, 사용자가 위장의 한계를 오해하지 않게 하려는 선택이라고 설명한다.

비상 삭제 기능을 “사용자층이 작지만 개인의 안전에 관한 것”이라며, 돌아올 때까지 업데이트를 미루라고 안내한 것도 같은 맥락이다.
상용 앱 스토어라면 쓰는 사람이 적은 기능을 조용히 없앴을 것이다.
F-Droid는 그 기능이 생명과 관련될 수 있다는 것을 인정하면서도, 소수의 기능이 다수의 개선을 막지 않게 하겠다는 절충을 공개적으로 설명한다.

## 비평

### 발표와 실제 배포 사이의 간극이 첫인상을 흐렸다

발표는 2.0을 몇 주에 걸쳐 순차 배포한다고 적었지만, 새 버전을 어디서 받는지는 적지 않았다.
Lobste.rs에서 wezm은 글에 새 버전으로 가는 링크가 없고, 웹사이트의 다운로드 링크도 저장소의 최신 릴리스도 여전히 1.23.2라고 지적했다.[^wezm]
kj는 F-Droid 패키지의 버전 목록에서 최신 APK를 받을 수 있다고 누군가 알려 줬다며, 글에 링크를 넣었어야 한다고 했다.[^kj]
wezm은 F-Droid 앱 안에서 F-Droid의 버전 목록을 보면 2.0.0이 있지만 1.23.2가 여전히 “권장”으로 표시돼 있어 자동 업데이트가 아직 켜지지 않은 것 같다고 덧붙였다.[^wezm-versions]

Hacker News에서도 같은 혼란이 이어졌다.
amiga386은 업데이트 화면도, 저장소 새로 고침도 “앱이 최신”이라고만 말하고, F-Droid를 직접 검색하면 “오래된 Android 버전용으로 만들어져 자동으로 업데이트할 수 없다”는 메시지가 뜬다며, “절대 변하지 마, F-Droid”라고 꼬집었다.[^amiga386]
Lobste.rs의 adrien은 기존 설치본이 천천히 업데이트되게 해서 버그가 작업 흐름을 깨지 않게 하는 것은 합리적이지만 확실히 혼란스러운 상황이라고 정리했다.[^adrien]
자동 업데이트를 새 기능으로 내세운 발표가, 정작 자기 자신의 업데이트에서는 혼란을 준 셈이다.

### 발견을 개선했다면서 품질 신호는 여전히 빠져 있다

발표는 발견을 2.0의 주요 목표로 내세운다.
그러나 Hacker News에서 magnat은 여전히 인기 등급도, 다운로드 수도, 사용자 리뷰 체계도 없다고 지적했고,[^magnat] hauget은 F-Droid의 문제는 늘 앱 리뷰가 없어 좋은 앱과 나쁜 앱을 가릴 방법이 없다는 것이었다고 적었다.[^hauget]
landdate는 어떤 앱이 많이 받아졌는지 볼 방법이 없어 F-Droid에서 계속 형편없는 앱을 받게 돼 Neo Store를 깔았는데, 이제 F-Droid로 돌아가겠다고 했다.[^landdate]

landdate의 반응은 발견 화면에 “가장 많이 내려받은 앱”이 생긴 것이 이 불만의 일부를 풀었다는 것을 보여 준다.
그러나 인기 목록은 이미 유명한 앱을 더 드러낼 뿐, 같은 카테고리의 비슷한 앱 가운데 무엇이 나은지는 알려 주지 않는다.
추적하지 않는다는 원칙과 품질 신호를 모으는 일은 긴장 관계에 있고, 발표는 그 긴장을 다루지 않는다.
hashworks는 사람들이 카테고리로 새 앱을 찾기는 하느냐며, 자신이 아는 사람은 모두 검색만 쓴다고 적어,[^hashworks] 카테고리 확장이 발견 문제의 핵심을 짚었는지 의문을 던졌다.

### 가장 큰 위협에 대해서는 아무 말도 없다

발표는 규제 덕분에 설치 경험이 나아졌다고 말하지만, 반대 방향의 변화는 다루지 않는다.
Hacker News에서 jjice는 Google이 내년에 잠금을 시작하면 F-Droid 같은 것의 미래가 어떻게 되느냐고 물었다.[^jjice]
creatonez는 Google이 사용자가 자기 앱을 설치하기 시작하기 전에 24시간을 기다리게 하는 사기 방지용 “고급 흐름”을 허용할 것으로 보이니, 계획이 다시 바뀌지 않는다면 F-Droid는 계속 동작할 것이라고 답했다.[^creatonez]
반면 Android 개발자라고 밝힌 tomjuggler는 F-Droid의 모든 앱이 앱별로 개발자가 Google에 인증해야 하고 그러지 않으면 아예 동작하지 않을 것이며, 그 과정은 Play 스토어 인증 개발자에게도 쉽지 않고, 평균 사용자는 그 설정을 하지 않을 것이라고 비관했다.[^tomjuggler]
meredithbloom도 Google이 서드파티 설치를 막으면 이 모든 것이 곧 의미 없어질 수 있다고 적었다.[^meredithbloom]

F-Droid 2.0이 다음 10년의 기반을 말하는 글이라면, 그 10년의 가장 큰 변수에 대한 입장이 한 문단쯤은 있었어야 한다.
사용성의 격차를 줄이는 작업이 아무리 성공해도, 플랫폼이 설치 경로 자체를 좁히면 그 성과는 소수의 고급 사용자에게만 닿는다.

## 인사이트

### 대체 클라이언트의 생태계가 공식 앱을 다시 쓰게 만들었다

2.0 이전 F-Droid의 불편함은 Droid-ify, Neo Store 같은 대체 클라이언트를 낳았다.
Lobste.rs에서 slondr는 이것이 Neo Store와 어떻게 비교될지 궁금하다고 적었고,[^slondr] Hacker News에서 aorth는 1년쯤 전에 Obtainium으로 옮겨 이제 모든 앱을 개발자의 GitHub 릴리스에서 곧바로 받는다고 했다.[^aorth]
nout은 사회적 신뢰망으로 앱을 검증하는 Zapstore를, rom1v는 컴퓨터에서 adb로 기기에 앱을 설치하는 F-Droid 패키지 관리자 클라이언트를 원했다.[^nout][^rom1v]

이 흐름은 오픈소스 생태계에서 흔한 역학이다.
공식 도구가 정체되면 포크와 대체 도구가 사용자를 가져가고, 그 압력이 공식 도구의 재작성을 이끈다.
F-Droid의 강점은 앱 자체보다 앱을 빌드하고 서명하는 저장소에 있고, 클라이언트는 그 저장소를 보여 주는 여러 창 가운데 하나일 뿐이다.
2.0이 성공하면 사용자가 공식 앱으로 돌아오겠지만, 대체 클라이언트들이 만든 경쟁 압력은 앞으로도 공식 앱의 속도를 정할 것이다.

### 저장소가 직접 빌드한다는 모델은 강점이자 지연의 원인이다

pritambaral은 F-Droid 저장소가 모든 앱을 직접 빌드하므로, 현실적인 해법은 Google이 저장소의 서명 키를 인정하는 것이라고 제안했다.[^pritambaral]
F-Droid의 모델은 개발자가 올린 바이너리가 아니라 공개된 소스에서 저장소가 직접 빌드한 바이너리를 배포하는 것이고, 이것이 재현 가능한 빌드와 소스 일치를 보장한다.

그러나 같은 모델이 지연을 만든다.
meredithbloom은 F-Droid 저장소에서 받은 바이너리를 앱의 공식 사이트에서 받은 것만큼 믿을 수 있을지 확신이 없고, 몇몇 앱은 F-Droid 저장소가 몇 버전 뒤처져 있으니 자기 페이지에서 받으라고 명시했다고 적었다.[^meredithbloom]
Google의 개발자 인증 요구가 “개발자가 서명한 앱”을 기준으로 삼는다면, 저장소가 서명하는 F-Droid의 모델은 바로 그 지점에서 부딪힌다.
F-Droid의 가장 큰 강점인 독립적인 빌드와 서명이, 다음 10년에는 가장 큰 제도적 약점이 될 수 있다.

### 자유 소프트웨어의 사용성은 기부가 아니라 기금이 만든다

발표의 마지막 부분은 이번 재작성이 누구의 돈으로 가능했는지를 자세히 밝힌다.
NLnet의 Mobifree, Open Technology Fund의 UX 연구실과 보안 연구실, NGI, Calyx Institute가 개발, 사용자 조사, 디자인, 보안 감사를 나눠 맡았다.
사용자 조사와 외부 디자인 회사와 독립 보안 검토는, 자원봉사만으로는 거의 이루어지지 않는 일이다.

Hacker News에서 idle_zealot은 F-Droid가 요소 사이에 선을 긋지 않는 요즘의 디자인 관례를 따라, 무엇을 누를 수 있는지, 어디가 스크롤되는지 알려 주지 않는다고 비판하면서도, 텍스트 정렬이나 여백 문제는 무급으로 일하는 아마추어 디자이너의 탓으로 돌릴 수 있다고 적었다.[^idle_zealot]
그러나 이번 재작성의 디자인은 무급 아마추어가 아니라 기금이 지원한 전문 디자인 회사가 참여한 결과다.
자유 소프트웨어의 사용성 격차가 좁혀지는 것은 개발자의 의지보다 공공 기금이 디자인과 사용자 조사에 돈을 쓰기 시작했기 때문이며, 그 기금이 끊기면 격차는 다시 벌어질 수 있다.

---

[^wezm]: <https://lobste.rs/s/opt2ma/f_droid_2_0#c_av7eio>

[^silverbluep]: <https://news.ycombinator.com/item?id=49832443>

[^outadoc]: <https://news.ycombinator.com/item?id=49832308>

[^mzajc]: <https://news.ycombinator.com/item?id=49832357>

[^kj]: <https://lobste.rs/s/opt2ma/f_droid_2_0#c_cv2qd9>

[^wezm-versions]: <https://lobste.rs/s/opt2ma/f_droid_2_0#c_ltt8g3>

[^amiga386]: <https://news.ycombinator.com/item?id=49836254>

[^adrien]: <https://lobste.rs/s/opt2ma/f_droid_2_0#c_s92q2w>

[^magnat]: <https://news.ycombinator.com/item?id=49832605>

[^hauget]: <https://news.ycombinator.com/item?id=49840410>

[^landdate]: <https://news.ycombinator.com/item?id=49839789>

[^hashworks]: <https://news.ycombinator.com/item?id=49841507>

[^jjice]: <https://news.ycombinator.com/item?id=49832601>

[^creatonez]: <https://news.ycombinator.com/item?id=49834280>

[^tomjuggler]: <https://news.ycombinator.com/item?id=49842124>

[^meredithbloom]: <https://news.ycombinator.com/item?id=49840016>

[^slondr]: <https://lobste.rs/s/opt2ma/f_droid_2_0#c_ciswno>

[^aorth]: <https://news.ycombinator.com/item?id=49832486>

[^nout]: <https://news.ycombinator.com/item?id=49838245>

[^rom1v]: <https://news.ycombinator.com/item?id=49832643>

[^pritambaral]: <https://news.ycombinator.com/item?id=49832830>

[^idle_zealot]: <https://news.ycombinator.com/item?id=49837707>
