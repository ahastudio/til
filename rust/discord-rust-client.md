# Discord가 Electron을 버리고 전체 클라이언트를 Rust와 GPUI로 옮긴다는 발표

원문: [Discord is ditching Electron and its new app uses less RAM](https://www.theverge.com/news/1027379/discord-ditching-electron-web-app)

HN 토론: <https://news.ycombinator.com/item?id=50378625> (493점, 432개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50403507> (409점, 411개 댓글)

GN 토론: <https://news.hada.io/topic?id=36657>

GN 토론: <https://news.hada.io/topic?id=36778>

## 요약

The Verge의 Tom Warren이 2026년 11월 5일에 쓴 짧은 뉴스 기사다.
Discord가 데스크톱 앱을 Rust로 완전히 옮기며 Electron을 버린다는 내용이다.
기사는 Electron이 시스템 자원을 많이 쓰기로 악명 높은 프레임워크이고,
Discord가 마침내 그것을 포기한다고 쓴다.

근거는 Discord 최고기술책임자(CTO) Stanislav Vishnevskiy의 Twitter 글이다.
기사가 옮긴 그의 말은 이렇다.
Discord는 2018년부터 Rust를 일찍 도입했고 인프라와 음성 기술과
현재 클라이언트 일부가 이미 Rust인데,
클라이언트 전체를 Rust로 옮기는 것이 숙원이었다는 것이다.
그래서 Electron이 사라지고 React Native도 사라지며,
모바일은 네이티브 UI를 유지하되 앱 코드는 Rust를 통해 데스크톱과
공유한다고 한다.

Vishnevskiy는 Windows 클라이언트가 RAM을 290MB만 쓰는 화면도 올렸다.
기사는 서버를 몇 개만 쓰는 사용자라도 현재 Windows 앱의 RAM 사용량이
1GB 이상에 쉽게 이른다고 덧붙이며 이를 분명한 개선으로 본다.
언제 완전히 전환될지는 분명하지 않고,
Vishnevskiy는 곧 사용자 테스트에 들어가기를 바란다고 했다.

Windows Latest의 Abhijith M B는 2026년 11월 6일 기사에서
같은 발표 직후 올라온 시연 영상을 프레임 단위로 살폈다고 전한다.[^windowslatest]
15초짜리 영상에서 현재 Electron 클라이언트와 새 Rust 클라이언트를
ThinkPad 두 대에서 나란히 켠다.
Electron 앱이 먼저 실행되어 약 3초간 어두운 빈 창을 보이다가 팁 문구를 띄우고,
새 클라이언트는 1.5초쯤 뒤에 실행했는데도 1초 안에 창이 나타났다고 한다.
옛 앱이 실행 약 5초 만에 인터페이스에 이르렀을 때
Rust 앱은 이미 친구 목록을 불러온 상태였다는 것이다.[^windowslatest]
Discord 직원들은 둘 다 콜드 스타트였다고 확인했고,
트레이에서 뜬 것이 아니냐는 질문에 영상을 찍은 직원은
그랬다면 친구 목록이 이미 불러와져 있었을 것이라고 답했다고 한다.[^windowslatest]

기사에 없는 정보가 원본 글에 하나 더 있다.
이 문서가 Twitter에서 직접 읽은 그의 글에서
그는 Tauri가 아니라 GPUI이니 모두의 추측이 좋았다고 덧붙였다.[^tweet]
HN의 한 댓글이 인용한 GPUI 사이트는 이를 GPU 가속 Rust UI 프레임워크라고
소개한다.[^throwaway2037]

## 분석

### 프레임워크 교체가 아니라 코드 공유 구조의 재편이다

발표의 핵심은 Electron을 다른 UI 도구로 바꾼다는 것이 아니라
앱의 중심을 웹 기술에서 Rust로 옮긴다는 것이다.
Discord는 이미 인프라와 음성 기술에 Rust를 써 왔고,
이제 클라이언트 로직까지 같은 언어로 옮겨 데스크톱과 모바일이 앱 코드를 나눠
쓰게 한다.
모바일은 네이티브 UI를 유지하므로 공유되는 것은 화면이 아니라 그 아래의 앱
코드다.[^tweet]
React Native를 걷어 내는 것도 같은 이유로 읽힌다.
웹 기술을 모바일에서 재사용하던 층이 Rust 코어로 대체된다는 뜻이다.

HN의 1024bits는 자신들이 만든 협업 앱 Totem도
Rust 엔진 위에 모바일에서는 Swift 같은 네이티브 UI를 얹는 비슷한 길을 택했고
지금까지 잘 되고 있다고 했다.[^1024bits]
두 사례는 같은 구조가 한 회사의 선택이 아니라 하나의 설계 경향일 수 있음을
보여 준다.
다만 이는 댓글 작성자 한 명의 보고다.

### 선택된 UI 도구는 GPUI다

기사는 어떤 UI 프레임워크를 쓰는지 말하지 않는다.
HN의 the__alchemist는 EGUI인지 GPUI인지 직접 만든 것인지 물으며
기사가 팝업 때문에 읽기 어려웠다고 했고,[^the__alchemist]
댓글들이 GPUI를 지목했으며 Vishnevskiy의 글이 이를 확인한다.[^tweet]
UI를 프레임워크가 아니라 코드로 쓰는 Rust 방식은 호불호가 갈린다.
kayson은 GPUI 첫 화면의 CSS 같은 메서드 체이닝이 끔찍해 보인다고 했고,[^kayson]
ogoffart는 Rust가 UI를 기술하기에 좋은 언어가 아니라며 Slint는 그 때문에 별도
언어를 쓴다고 답했다.[^ogoffart]
이 논쟁은 이 발표가 어떤 UI 개발 경험을 택했는지를 보여 주는 맥락이다.
GN에서 sudosudo는 새 프로그램을 만들 때 GPUI를 쓰는 편이 나을지 고민된다며
속도는 앞서지만 선뜻 손이 가지 않는다고 했다.[^sudosudo]

Windows Latest는 웹 기술이 남는 자리도 정리한다.
YouTube 임베드와 Activities는 시스템 웹뷰를 쓰고
Vishnevskiy는 Tauri와 비슷한 방식이라고 했다고 한다.
웹 앱은 화면은 HTML로 그리되 로직은 JavaScript가 아니라 WebAssembly로 돌리고,
로그인 토큰은 Windows의 자격 증명 관리자 같은 시스템 키링에 둔다는 설명이다.
앱의 모양과 동작은 현재와 같다고 한다.[^windowslatest]
Tauri를 쓰지 않은 이유로 HN의 giancarlostoro는 리눅스의 WebKitGTK에서
WebRTC가 기본으로 동작하지 않는다는 점을 들었다.
이는 한 사용자의 경험이며 Discord가 밝힌 이유는 아니다.[^giancarlostoro]

### 시작 속도는 업데이트 방식과 함께 읽어야 한다

Windows Latest에 따르면 현재 앱은 업데이트를 확인하며 시작 화면을 보이고,
X의 한 사용자는 이것이 매번 5~10초 걸린다고 했다.
새 클라이언트가 이를 건너뛰는 이유로 Discord 직원은
아주 빨리 부팅하고 새 아키텍처라서 그런 화면이 필요 없으며
업데이트는 백그라운드에서 자동으로 한다고 답했다.
Microsoft Store나 Windows 업데이트 조정 플랫폼으로 넘기지는 않는다고도 했다.[^windowslatest]
HN에서 gloosx는 Discord를 켤 때마다 업데이트를 받는데,
완전히 업데이트된 두 클라이언트의 시작 시간을 비교하는 것은 의미가 적다고 했다.[^gloosx]
이는 한 사용자의 경험이다.
영상이 보여 주는 속도 차가 업데이트 방식의 차이에서 왔는지,
코드 구조의 차이에서 왔는지는 이 영상만으로 가를 수 없다.
petterroea는 제품이 출시되어 실제로 쓰이기 전에는 이미 보여 줬다고 말하기
어렵다고 했다.[^petterroea]
기사는 Discord가 Electron 안에서도 고치려 했다고 덧붙인다.
9월 패치 노트에 Electron 42로 올리자 CPU 중앙값이 약 17% 줄었지만
p50 메모리가 약 4% 늘었다고 적혀 있었다는 것이다.[^windowslatest]

## 비평

### 기사가 1차 자료보다 얇다

HN의 hbn은 기사에 Rust 클라이언트를 만들고 있다는 말과
누군가 초기 빌드가 290MB를 쓴다는 것을 보여 줬다는 말 외에는 내용이 없다고
했다.[^hbn]
기사는 Vishnevskiy의 글에 있던 GPUI라는 가장 구체적인 정보를 싣지 않았다.
이 보도만 읽은 사람은 어떤 기술로 옮기는지 알 수 없다.
기사가 말한 사실은 모두 CTO의 글에서 왔으므로,
이 문서는 독자가 원본 글을 먼저 읽는 편이 낫다고 판단한다.

### 290MB라는 수치는 비교 조건이 없다

기사는 스크린샷의 290MB를 분명한 개선으로 읽는다.
그러나 그 화면이 몇 개의 서버에 접속한 상태인지,
음성이나 영상 같은 기능이 켜져 있었는지,
같은 조건에서 현재 앱이 얼마를 쓰는지는 적혀 있지 않다.
현재 앱이 1GB 이상에 쉽게 이른다는 것도 기사의 서술이지 측정이 아니다.
아직 사용자 테스트에 들어가지 않은 빌드의 한 장면이므로,
기능이 모두 옮겨진 뒤에도 이 수치가 유지되는지는 알 수 없다.

Windows Latest 기사는 이 질문 가운데 하나에 답을 싣는다.
290.2MB는 계정 두 개를 동시에 로그인한 상태의 수치였다고
Vishnevskiy가 답했고, 새 클라이언트는 계정 동시 실행을 지원한다고 한다.[^windowslatest]
같은 기사는 현재 앱이 보통 1GB 아래라는 Discord 직원의 2025년 12월 발언과
견주어 약 70% 낮다고 계산한다.
이는 다른 시점의 다른 측정을 비교한 것이고,
기사 스스로도 초기 빌드의 한 장면이며 Discord가 두 클라이언트의 같은 조건
벤치마크를 내놓지 않았다고 적는다.[^windowslatest]
그래서 같은 조건에서 현재 앱이 얼마를 쓰는지라는 질문은 여전히 남는다.
HN에서 Neywiny는 계정 두 개라는 설명만 되풀이될 뿐 뒷받침이 없다고 했고,[^neywiny]
ycui7은 70% 줄어든 290MB도 여전히 끔찍하다고 했다.[^ycui7]

### Electron이 나쁘다는 전제에 대한 반론이 있다

hendrikmans는 Electron이 나쁘다는 말이 공학적 트레이드오프를 배우기 전의
말이라고 했다.
브라우저를 다시 만드는 셈이고,
접근성과 입력기(IME)와 오른쪽에서 왼쪽으로 쓰는 문자 지원을 놓치기 쉬우며,
Rust로 만든 앱은 반복이 느려서 결국 스크립트 층을 얹게 된다는
것이다.[^hendrikmans]
delta_p_delta_x는 채팅 앱이 브라우저가 하는 모든 것을 해야 할 이유가 없고
그런 기능은 운영체제 차원에서 오래전부터 해결되어 있다고
반박했다.[^delta_p_delta_x]
stasomatic은 Slack이나 Discord에서 성능 문제를 겪은 적이 없고
문제는 Electron이 아니라 끊임없는 광고와 유도라고 했다.[^stasomatic]
vmg12는 Electron이 나쁜 것은 맞지만
Electron과 Rust 계열 모두 다른 선택지를 무시한다고 했다.[^vmg12]
어느 쪽이 맞는지는 이 발표만으로 가릴 수 없고,
Discord가 접근성과 입력기를 어떻게 처리했는지가 근거가 된다.

### 전면 재작성의 위험은 발표에 나오지 않는다

HN의 Swiffy0은 이 전환이 거의 전부 AI의 손으로 이루어질 것이 분명하다고
가정하고,
손으로 쓴 기존 코드베이스와 그 코드를 쓴 사람들을 버리는 것이 좋은 생각인지
물었다.[^Swiffy0]
kombookcha는 공유된 이해가 사라지면 되돌리기가 거의 불가능하다고
했고,[^kombookcha]
gjsman-1000은 비행기나 CPU를 아무도 전부 이해하지 못해도 쓰이고 있다고
반박했다.[^gjsman-1000]
spunker540은 선택지가 직원들이 아는 웹 프레임워크와
직원들이 덜 아는 성능 좋은 네이티브 앱이었고 후자를 골랐을 뿐이라고
했다.[^spunker540]
다만 이 논쟁의 출발점인 AI가 재작성을 한다는 말은 기사에도 Vishnevskiy의
글에도 없다.
댓글 작성자의 가정이다.

## 인사이트

### 접근성과 입력기는 UI 도구를 바꿀 때 숨은 비용이다

Daedren은 GPUI가 접근성과 제대로 된 CJK 글자 표시를 보장하는지,
그리고 Activities가 계속 Tauri를 쓴다면 WebKit 호환성이 문제가 되지 않는지
물었다.[^Daedren]
mintflow는 GPUI가 받아들일 만한 중국어 글자를 그리고
검색창 같은 컨트롤에서 입력기가 작동한다고 답했고,[^mintflow]
tensor는 접근성이 저장소 안에는 없지만 다른 라이브러리와 통합해 만들 수 있고
gpui-kit 같은 프로젝트가 그것을 해 준다고 했다.[^tensor]
eviks는 아직 접근성이 없고 공개된 프레임워크가 방치되어 있어 도달하지 못할 수도
있다고 했다.[^eviks]
1024bits는 Rust UI 프레임워크 전반에서 접근성이 가장 큰 걱정이고
다른 생태계에서는 거의 공짜로 얻는 것이 여기서는 상당한 노력을 요구한다고
했다.[^1024bits]
이 문서의 해석으로는 웹 기술의 가장 큰 자산이 렌더링 성능이 아니라
수십 년간 쌓인 접근성과 국제화 지원이고,
네이티브 UI 프레임워크로 옮기면 이 자산을 다시 쌓아야 한다.
Discord처럼 사용자가 많고 언어가 다양한 앱이 이를 어떻게 풀지가 이 발표의 진짜
시험대다.

### 자원 제약이 설계의 기준을 되돌린다

Insanity는 RAM 위기에서 나올 좋은 결과가 엔지니어들이 다시 메모리 사용량을 신경
쓰게 되는 것이라고 농담처럼 적었다.[^Insanity]
이 댓글이 70개쯤의 답글을 끌어낸 것은 같은 느낌이 널리 퍼져 있다는 뜻이다.
개발 속도를 위해 자원을 쓰던 시기에 Electron이 자리 잡았다면,
메모리가 비싸지는 시기에는 같은 계산이 다른 답을 낼 수 있다.
다만 이는 Discord가 그런 이유로 옮긴다는 뜻이 아니다.
Vishnevskiy의 글이 든 이유는 오래된 Rust 도입의 연장이라는 것이다.

### 외부 생태계가 가장 먼저 치르는 비용이다

Telaneo는 Vencord가 어떤 형태로든 계속 작동하기를 바란다며
CSS의 유연성을 포기하는 대신 RAM을 5분의 1로 줄이는 앱과 맞바꿀 수 있다고
했다.[^Telaneo]
웹 기술로 만든 앱은 사용자가 CSS와 스크립트로 고칠 수 있었고,
그것이 확장 생태계를 낳았다.
네이티브 렌더링으로 옮기면 그 통로가 닫히므로
공식 플러그인이나 테마 체계가 생기지 않는 한 외부 확장은 사라진다.
Discord가 이를 어떻게 다룰지는 발표에 없다.

### 결론을 바꿀 관찰

사용자 테스트가 시작되어 같은 조건에서 메모리와 시작 시간과 CPU를 비교한
측정이 나오면
290MB라는 한 장면이 확인되거나 흔들린다.
스크린 리더와 입력기와 오른쪽에서 왼쪽으로 쓰는 문자가 새 앱에서 작동한다는
확인이 나오면
네이티브 전환의 가장 큰 의문이 풀린다.
Vencord 같은 확장을 위한 공식 통로가 발표되면
생태계의 비용이 얼마나 줄어드는지 판단할 수 있다.

---

[^tweet]: Twitter, [We've been early adopters of Rust since 2018 and a lot of our infra, voice tech, and even some of the current client is already Rust](https://twitter.com/svishnevskiy/status/2118081920194203799), 2026-11-05

[^1024bits]: <https://news.ycombinator.com/item?id=50381542>

[^the__alchemist]: <https://news.ycombinator.com/item?id=50379999>

[^hbn]: <https://news.ycombinator.com/item?id=50380296>

[^hendrikmans]: <https://news.ycombinator.com/item?id=50379872>

[^delta_p_delta_x]: <https://news.ycombinator.com/item?id=50379993>

[^stasomatic]: <https://news.ycombinator.com/item?id=50383306>

[^vmg12]: <https://news.ycombinator.com/item?id=50380098>

[^Swiffy0]: <https://news.ycombinator.com/item?id=50379261>

[^kombookcha]: <https://news.ycombinator.com/item?id=50379303>

[^gjsman-1000]: <https://news.ycombinator.com/item?id=50379282>

[^spunker540]: <https://news.ycombinator.com/item?id=50381635>

[^Daedren]: <https://news.ycombinator.com/item?id=50379235>

[^mintflow]: <https://news.ycombinator.com/item?id=50379359>

[^tensor]: <https://news.ycombinator.com/item?id=50383192>

[^eviks]: <https://news.ycombinator.com/item?id=50380894>

[^Insanity]: <https://news.ycombinator.com/item?id=50379110>

[^throwaway2037]: <https://news.ycombinator.com/item?id=50384929>

[^kayson]: <https://news.ycombinator.com/item?id=50379724>

[^ogoffart]: <https://news.ycombinator.com/item?id=50380850>

[^Telaneo]: <https://news.ycombinator.com/item?id=50379308>

[^windowslatest]: Windows Latest, [Every Windows 11 app should kill Electron, and Discord just showed why: no “Starting” screen and 70% less RAM, even with two accounts signed in](https://www.windowslatest.com/2026/11/06/every-windows-11-app-should-kill-electron-and-discord-just-showed-why-no-starting-screen-and-70-less-ram-even-with-two-accounts-signed-in/), 2026-11-06

[^neywiny]: <https://news.ycombinator.com/item?id=50403983>

[^ycui7]: <https://news.ycombinator.com/item?id=50410552>

[^gloosx]: <https://news.ycombinator.com/item?id=50413505>

[^petterroea]: <https://news.ycombinator.com/item?id=50403965>

[^giancarlostoro]: <https://news.ycombinator.com/item?id=50407695>

[^sudosudo]: <https://news.hada.io/topic?id=36778#cid69427>
