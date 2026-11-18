# OpenCode Browse: 브라우저 연결 도구

<https://opencode.ai/product/browse>

<https://github.com/anomalyco/browse>

HN 토론: <https://news.ycombinator.com/item?id=50523459> (327점, 212개 댓글)

GN 토론: <https://news.hada.io/topic?id=37333>

## 소개

OpenCode를 만드는 Anomaly가 낸 도구로, 코딩 에이전트가 사용자의 실제 브라우저를 쓰게 해 주는 MCP 서버와 Chromium 확장이다.
이 문서는 제품 페이지 전체와 저장소 README의 앞부분(설치 절)을 읽었다. 직접 설치해 써 보지는 않았다.
기능 서술은 모두 제작사의 주장이다.
GitHub API로 읽은 시점(2026년 11월 18일)의 저장소 수치는 별 883개, 포크 69개, 열린 이슈 40개, 라이선스 MIT, 주 언어 TypeScript, 생성일 2026년 10월 27일이다.

핵심 아이디어는 이렇다.
에이전트가 별도의 자동화 브라우저가 아니라 사용자의 탭, 로그인, 확장 프로그램이 있는 진짜 브라우저를 쓴다.
탭은 백그라운드에서 접힌 그룹으로 열려 방해하지 않는다.
로그인, 2단계 인증, 결제처럼 사람이 해야 하는 순간에는 에이전트가 탭을 사용자에게 돌려주고, 사용자가 Continue를 누르면 이어서 진행한다.

제품 페이지가 내세우는 기능은 다음과 같다.

- 지원 브라우저: Chrome, Edge, Brave, Arc, Helium, Vivaldi, Opera, Chromium.
- 인계(handoff): 로그인이나 2FA는 사용자가 하고 Continue를 누른다.
- 탭 빌려주기: 툴바 버튼으로 열려 있는 탭을 에이전트에게 건넨다.
- 기록과 캡처: 스크린샷, 탭 녹화, 네트워크 트래픽.
- 모든 MCP 클라이언트: OpenCode, Claude Code, Cursor, Codex, Zed 등.
- 이미 로그인한 사이트 사용: 키나 설정 없이.
- 허용 사이트: 에이전트의 탭을 사용자가 지정한 사이트로 제한한다.

설치는 확장을 먼저 설치하면 나머지 단계를 안내한다고 한다. CLI를 직접 설치하는 방법은 다음과 같다.

- 셸 스크립트(macOS, Linux)와 PowerShell 스크립트, `npm install -g @opencode/browse && browse install`, `bun add -g`, pnpm, yarn, volta, `npx`이다.
- 설치 스크립트는 Anomaly의 릴리스 서비스에서 채널 매니페스트를 읽고 바이너리의 크기와 SHA-256을 확인한 뒤 설치한다고 한다. 채널은 stable, beta, dev이다.
- `browse install`은 browse를 제자리에 놓고, 에이전트들(OpenCode와 이 컴퓨터에서 찾은 에이전트)의 MCP 설정에 browse 서버를 넣고, 확장을 일회용 페어링 코드로 연결한다.
- 에이전트 안에서 설치 명령을 실행하게 하면 그 에이전트가 스스로 설정한다.

같은 회사의 다른 제품으로 Hex(기기 내 음성 받아쓰기), OpenTunnel(로컬 앱의 공개 HTTPS 주소), OpenTUI(터미널 UI 라이브러리)가 페이지에 소개된다.

## 분석

### 중심 주장은 새 브라우저가 아니라 이미 로그인한 브라우저를 빌려준다는 것이다

에이전트용 브라우저 도구 대부분이 깨끗한 프로필이나 별도 브라우저를 띄우는 반면 이 도구는 사용자의 실제 프로필을 쓴다.
따라서 이미 로그인한 사이트에서 키나 설정 없이 일할 수 있다는 것이 가치이고, 인계 장치가 사람이 반드시 거쳐야 하는 지점을 보장한다.
이는 제품 서술을 이 문서가 압축한 것이다.

### 같은 문제를 푸는 선택지가 이미 여럿이다

HN 스레드에서 기능이 Playwright MCP 서버와 겹친다는 지적이 나왔고, 사용자는 Playwright MCP가 이미 열려 있는 페이지와 세션에 접근을 허용해 줘서 쓴다고 했다.[^jeremyjacob]
Chrome 공식 DevTools MCP를 대안으로 든 댓글도 여럿이다.[^mrdw]
Vercel의 agent-browser가 낫다는 의견이 있었고, 한 사용자는 비교해 보니 14개 과제 중 14개를 끝내 13개의 agent-browser보다 낫고 빠르다고 했다.[^jwblackwell]
이는 개인의 짧은 비교이며 이 문서가 재현하지 못했다.
이 도구를 직접 써 본 사용자는 2주 동안 눈에 띄는 버그가 없었고 포커스를 뺏지 않고 탭을 다루며 CLI와 MCP로 쓸 수 있다고 평가했다.[^tornikeo]

## 비평

### 보안이 가장 큰 쟁점이다

제품 페이지는 허용 사이트 설정과 인계 장치를 내세우지만, 가장 많이 나온 반응은 위험에 대한 것이었다.
한 사용자는 로그인과 확장 프로그램까지 준다는 대목에서 바이러스 연구 시설의 열린 문 같다고 했다.[^keyle]
다른 사용자는 프롬프트 주입이 해결된 문제가 아니라는 에이전트 자신의 답을 전하며, 비밀이 가장 노출되기 쉬운 브라우저나 이메일을 왜 에이전트에게 맡기느냐고 물었다.[^eatfish]
확장이 사용자의 자격 증명과 2FA로 인증된 세션을 쓰게 하는 것을 어떻게 느끼느냐는 질문도 있었다.[^boomskats]
한 사용자는 이런 도구를 쓸 때 치명적 3요소(lethal trifecta)를 경계하고 에이전트용 프로필을 따로 쓰라고 권했다.[^jeremyjacob]
제품 페이지에는 허용 사이트 기능이 있으나, 그 범위와 기본값, 프롬프트 주입에 대한 방어는 이 문서가 읽은 범위에서 설명되지 않는다.

### 제작사의 보안 태도에 대한 비판이 있다

HN에서 한 사용자는 이 회사가 주당 서너 개의 프로젝트를 만들고 보안에 소홀하며 OpenCode V2가 보안을 사실상 내던졌다고 했다.[^testtestmetest]
이에 대해 하네스 안에서의 보안은 허가 피로와 나쁜 사용자 경험만 낳는 잘못된 접근이라는 반박이 나왔다.[^zaptheimpaler]
다른 사용자는 OpenCode를 신뢰할 수 없는 코드로 보고 모든 것을 끄는 설정을 만들어 네트워크 접근이 없는 샌드박스에서 돌린다고 했다.[^regexorcist]
이 가운데 제작사의 실제 보안 관행은 이 문서가 확인하지 못했다.

### 지원 범위가 Chromium 계열이다

Firefox가 빠졌다는 질문에 확장의 API 표면이 달라서라는 답이 있었다.[^guipsp]
제품 페이지는 지원 브라우저 목록만 밝히고 Firefox 계획은 적지 않는다.

### 필요성에 대한 회의

한 사용자는 강력한 추론 모델이 이미 셸로 자기 프로필의 브라우저를 띄울 줄 안다며 필요를 못 느낀다고 했고,[^bob1029]
이에 대해 매번 바퀴를 다시 발명하게 하면 토큰을 태우는 것이라는 반문이 달렸다.[^meatmanek]
MCP 자체가 죽은 기술이라는 비판과 이를 반박하는 글도 있었다. 비판은 별도 서비스가 공격 면적과 유지 부담을 늘린다는 것이고, 반박은 하네스 개발자가 MCP가 풀어 주는 어려운 문제들이 있다는 것이었다.[^sillyusername][^mickeyp]
또 “내 브라우저에서는 되는데 사용자 쪽에서는 안 된다”는 상황에서 에이전트가 사용자 브라우저에 붙어 테스트를 돌리는 쓰임이 무섭지만 효과적이라는 증언도 있었다.[^thund]
이는 이 문서가 확인하지 못한 개인 경험이다.

### 외부 반응

HN 스레드는 327점 212개 댓글이다. 스레드의 상당 부분은 OpenCode 자체에 대한 의견(가격, 품질, 대안 하네스와의 비교)이어서 이 도구의 평가와는 구분해 읽어야 한다.
Lobste.rs에서는 `opencode.ai` 도메인이 올라온 적이 없다.
GeekNews에는 같은 제품의 토픽이 있으나 댓글이 하나이고, 그것도 HN 댓글을 다시 모은 GN⁺ 계정의 요약이라 GeekNews 이용자의 반응은 없다.

## 인사이트

### 가져갈 것은 에이전트에게 브라우저를 줄 때의 권한 분리이다

제품의 구성(백그라운드 탭, 허용 사이트, 로그인과 결제의 인계)은 에이전트에게 실제 계정을 쓰게 할 때 필요한 제어의 목록으로 읽을 수 있다.
도입한다면 에이전트용 별도 브라우저 프로필, 허용 사이트의 최소화, 결제와 인증 단계의 사람 인계, 사용 기록 확인을 먼저 정하는 쪽이 HN의 보안 우려에 대한 현실적인 대응이다.
이는 이 문서의 적용이며 이 문서가 시험하지 못했다.

### 같은 문제를 푸는 도구는 같은 과제로 직접 비교한다

Playwright MCP, Chrome DevTools MCP, agent-browser, 이 도구는 모두 에이전트에게 브라우저를 주는 방법이다.
HN에서 나온 비교는 한 사용자의 짧은 시험이므로, 자기 작업(로그인이 필요한 사이트, 긴 세션)으로 성공률과 속도, 토큰 사용을 직접 재어 보는 것이 신뢰할 수 있다.

### 확인할 관찰

이 도구의 주장을 가를 관찰은 세 가지이다.
프롬프트 주입 상황에서 허용 사이트와 인계 장치가 실제로 피해를 막는지,
다른 브라우저 MCP와 같은 과제로 비교했을 때의 성공률과 토큰 비용,
확장이 실제 프로필에서 안정적으로 오래 도는지이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^jeremyjacob]: <https://news.ycombinator.com/item?id=50524242>

[^mrdw]: <https://news.ycombinator.com/item?id=50524348>

[^jwblackwell]: <https://news.ycombinator.com/item?id=50529078>

[^tornikeo]: <https://news.ycombinator.com/item?id=50531425>

[^keyle]: <https://news.ycombinator.com/item?id=50526151>

[^eatfish]: <https://news.ycombinator.com/item?id=50529221>

[^boomskats]: <https://news.ycombinator.com/item?id=50529398>

[^testtestmetest]: <https://news.ycombinator.com/item?id=50524532>

[^zaptheimpaler]: <https://news.ycombinator.com/item?id=50528555>

[^regexorcist]: <https://news.ycombinator.com/item?id=50529369>

[^guipsp]: <https://news.ycombinator.com/item?id=50524187>

[^bob1029]: <https://news.ycombinator.com/item?id=50526246>

[^meatmanek]: <https://news.ycombinator.com/item?id=50528079>

[^sillyusername]: <https://news.ycombinator.com/item?id=50528034>

[^mickeyp]: <https://news.ycombinator.com/item?id=50528352>

[^thund]: <https://news.ycombinator.com/item?id=50526458>
