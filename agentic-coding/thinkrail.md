# ThinkRail: pi 코딩 에이전트를 둘러싼 JetBrains의 에이전트 IDE

<https://thinkrail.ai/>

<https://github.com/JetBrains/thinkrail>

HN 토론: <https://news.ycombinator.com/item?id=50233294> (192점, 144개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50219186> (56점, 82개 댓글)

GN 토론: <https://news.hada.io/topic?id=35994>

## 소개

ThinkRail은 JetBrains가 인큐베이터 프로젝트로 공개한 에이전트 IDE다.
저장소 설명은 pi와 함께 사용자의 작업 방식에 맞춰 스스로를 조정하는 가벼운 진짜
IDE에서 바이브 코딩을
한다는 것이고, README는 쓸수록 나아지는 에이전트 IDE로 오늘은 살아 있는 명세로
프로젝트를 배우고
내일은 스스로 기능을 만든다고 소개한다.
`pi` 코딩 에이전트 주위에 풍부한 인터페이스를 만들고, 작업을 별도의 작업
공간으로 격리하고,
에이전트에 살아 있는 명세와 재사용 가능한 스킬로 지속되는 프로젝트 지식을
주었다는 구성이다.
다음 단계로 전체 확장 지원을 더해 사용자가 일하는 방식에 따라 필요한 도구를
스스로 만들게 하겠다고 한다.

저장소는 2026년 7월 8일에 만들어졌고 TypeScript이며 Apache-2.0이다.
확인한 시점에 별 1,937개, 포크 110개, 열린 이슈 206개였고 마지막 푸시는 10월
26일이었다.

## 주요 기능

- 격리된 작업 공간: 아무 git 저장소나 프로젝트로 열고 `git worktree`로 작업
공간을 자른다.
각 공간은 자기 브랜치와 작업 디렉터리를 가지며, 에이전트는 사용자의 체크아웃을
건드리지 않고 병렬로
  일한다.
끝났거나 한동안 쓰지 않은 작업 공간은 PR이 병합되거나 닫히거나 일주일이 조용하면
프로젝트별 선반으로
  내려간다.
상단 바는 활성 브랜치가 `origin`과 PR 대비 어디에 있는지를 보이고 게시, 푸시, PR
열기를 한 번에 잇는다.
GitHub PR이 열리면 CI 검사와 리뷰 결정을 보이고 실패한 검사를 에이전트에게
넘기거나 병합할 수 있다.
- 에이전트 주위의 진짜 IDE: 쪼갤 수 있는 작업대에 Monaco 편집기 탭, git 변경
표시가 있는 파일 트리,
  터미널, 문서가 있다.
  파일과 diff에 고정된 리뷰 댓글을 남기고 구조화된 맥락으로 채팅에 보낼 수 있다.
- 채팅: 작업 공간마다 여러 `pi` 세션이 동시에 돌며 세션별 모델과 토큰과 비용을
표시한다.
실행 중인 턴을 조종하거나 후속을 대기열에 넣고, 하위 에이전트에 위임하고,
에이전트가 갱신하고 사용자가
  고치는 공유 계획을 따른다.
- 명세가 기준: 코드 옆의 `SPEC.md` 파일 그래프를 에이전트가 `spec_*` 도구로 읽고
검색하고 유지한다.
- 스킬과 워크플로: 다른 코딩 에이전트용으로 이미 가진 이식 가능한 Agent Skills를
제자리에서 읽고,
  프로젝트 설정, 설계 브레인스토밍, PR 제출을 안내하는 워크플로가 있다.
- MCP 서버: `pi`의 `mcp.json`에 있는 서버를 연결하고, 읽기 전용으로 표시되지
않은 호출은 채팅에서 묻고,
  저장소가 정의한 서버는 승인할 때까지 꺼 둔다.
- 공급자와 자격 증명: JetBrains AI로 로그인하거나 `pi`의 인증으로 아무 공급자나
연결하며 ThinkRail 자체의
  계정은 없다.
- 데스크톱 앱 또는 브라우저: 네이티브 데스크톱 앱과, 같은 앱을 브라우저에서 여는
`thinkrail` CLI가 같은
  엔진 호스트를 쓴다.
- 언어: 영어와 간체 중국어가 내장되어 있고 `~/.thinkrail/locales`에 번역 파일을
두어 추가할 수 있다.

## 설치와 실행

설치는 데스크톱 설치 프로그램과 독립형 CLI 두 가지이고, 모두 릴리스 페이지에
`SHA256SUMS`와 함께 올라온다.
README는 macOS(Apple Silicon)용 DMG, Windows x64용 설치 압축 파일, Linux x64와
ARM64용 설치 tarball을
안내하며 macOS Intel용 데스크톱 빌드는 없다고 적는다.
Linux 데스크톱은 glibc 2.38 이상과 GTK 3, WebKitGTK 4.1 등이 필요하다.
CLI는 아래 한 줄이고, 설치 프로그램이 알맞은 바이너리를 받아 SHA-256 체크섬을
검증하고 PATH에 올린다.

```bash
curl -fsSL https://raw.githubusercontent.com/JetBrains/thinkrail/main/install.sh | bash
thinkrail ~/code/my-repo   # git 저장소를 프로젝트로 열기
```

`thinkrail`은 PATH에 `git`이 있어야 하고 모델 공급자가 필요하다.
서명 상태는 플랫폼마다 달라 Windows 바이너리는 JetBrains가 서명했고, macOS CLI는
서명되었지만 아직 공증되지
않았으며, Linux 산출물은 서명되지 않았다고 README가 적는다.

## 구조

README는 ThinkRail을 `pi`를 프로세스 안에서 돌리고 풍부한 웹 UI에 잇는 얇은
호스트라고 설명한다.
`pi`가 모델, 스킬, 압축, 비용, 세션 상태를 맡고 앱은 작업 공간과 편집기와
통신선을 맡으며
프롬프트를 몰래 조립하지 않는다.
세 개의 고리가 있다.
엔진 호스트는 `Bun.serve` 기반 HTTP와 WebSocket 호스트로 채팅마다 프로세스 안에
`pi` 세션 하나를 둔다.
통신선은 `packages/contracts`의 타입이 있고 버전이 매겨진 프로토콜이고,
UI 클라이언트는 React 19, Zustand, Tailwind v4로 독립 배포되며 계약에만
의존한다.

저장소의 설계 문서는 같은 구조를 설명하고 `pi-web-access`, `pi-spec-graph`,
`pi-thinkrail-workflow`,
`pi-todos` 같은 pi 확장을 모든 세션에 포함한다고 적는다.[^architecture]
제품 문서는 원칙으로 pi가 유일한 엔진이고 기능은 pi에 무엇을 먹이느냐로만
에이전트에 영향을 주며,
호스트는 pi가 보고하는 것을 다시 계산하지 않고 보여 주고, 사용자 자신의 도구와
자격 증명을 쓰며,
신뢰는 명시적이어야 한다는 것을 든다.[^goal]
개발은 명세 우선이어서 모듈마다 `SPEC.md`가 있고 경계나 계약을 바꾸면 같은
변경에서 명세를 갱신한다.

개인정보 면에서 README는 실행, 채팅 생성, 메시지 전송, 공급자 연결 같은 기본
사용 이벤트를 무작위 설치
ID에 묶어 수집하고, 오류 보고는 항상 같은 ID로 전송되며 오류 유형과 코드와
ThinkRail 코드 내 위치만
포함한다고 적는다.
추가 사용 데이터 공유는 첫 실행 때 켜고 끌 수 있고 `thinkrail --no-analytics`로
한 번 끌 수 있다.

## 분석

### 이 도구의 논지는 에이전트의 문제가 에이전트 밖에 있다는 것이다

제품 문서는 pi의 유연함이 시간을 치르게 한다고 쓴다.
초심자는 조작을 배우는 데 오래 걸리고 숙련자도 에이전트 주변의 일에서 터미널이
어색하다는 것이다.
문제로 든 것은 병렬 에이전트가 하나의 작업 트리에서 충돌하는 것, 에이전트의
변경을 CLI에서 검토하기
어려운 것, 의도가 세션과 함께 사라지는 것이다.[^goal]
ThinkRail은 이를 각각 worktree 격리, 편집기와 리뷰 댓글, 명세 그래프로 푼다.
에이전트의 능력을 높이는 것이 아니라 에이전트를 둘러싼 작업의 경계를 정리하는
접근이다.

### 엔진을 하나로 고정하고 UI를 얇게 둔다

원칙은 pi를 유일한 엔진으로 두고 기능은 pi가 받는 것을 먹이는 방식으로만 영향을
준다는 것이다.
이 선택은 두 번째 에이전트를 만들지 않고 표면만 더한다는 약속이다.
대가는 pi의 제약과 변경에 종속된다는 점이고, 저장소에 pi 호환성 문서가 따로
있다.
이는 이 문서의 읽기이며 그 문서는 열어 보지 않았다.

### 명세를 기준으로 삼는 점이 가장 차별적이다

`SPEC.md` 그래프를 에이전트가 전용 도구로 읽고 유지하며 개발 자체도 명세
우선이라는 점이 이 도구의 자기
서술이다.
개발 방식과 제품 기능이 같은 방향이어서 자기 도구로 자기를 만드는 구조를 보인다.
그 효과가 실제로 있는지는 문서의 서술일 뿐이다.

## 비평

### 명세가 에이전트에게 실제로 읽힌다는 주장은 확인되지 않았다

HN의 troupo는 에이전트가 실제로 읽는 명세 그래프라는 표현이 틀렸다며 에이전트는
무작위로 맥락에 끌어오고
무작위로 지운다고 했다.[^troupo]
swingboy는 소프트웨어의 종류에 따라 다르지만 6개월 전보다 명세 주도 개발이 덜
필요해졌고 오래된 명세는
잡음이 된다고 했다.[^swingboy]
zihotki는 명세는 과도적이고 장기적 가치가 낮으며 진실은 구현과 발견한 함정에서
나온 문서라고 했고,[^zihotki]
bpicolo는 거의 모든 소프트웨어는 작성 전에 명세가 부족하다고 덧붙였다.[^bpicolo]
저장소는 효과를 보여 주는 측정을 싣지 않고 이 문서도 확인하지 못했다.

### JetBrains의 AI 전략 안에서의 위치가 불분명하다

HN의 Deukhoofd는 JetBrains가 최근 Air를 냈는데 같은 전제에 구현만 다른 것 같다고
물었고,[^deukhoofd]
crummy는 전체 IDE 판매의 장기적 재무 생존에 확신이 없어 만들 수 있는 것을 던져
보고 안 되는 것은 죽일
것이라고 짐작했다.[^crummy]
다른 스레드에서 rbehrends는 Air와 ThinkRail이 모두 기능이 불완전한 상태이고 기존
AI Assistant가 방치되는
듯해 불만이라고 했다.[^rbehrends]
dr_faustus는 JetBrains IDE를 십 년 넘게 썼지만 여러 worktree를 동시에 다루기
불편해 거의 열지 않는다고 했다.[^dr_faustus]
저장소의 설명은 JetBrains 제품군 안에서의 역할을 말하지 않는다.

### 경쟁 도구 대비 이유가 문서에 없다

aliasxneo는 oh-my-pi와 Paseo를 떠나려면 강하게 설득되어야 한다고
했고,[^aliasxneo]
charlie0는 Claude Code로 이들이 제공하는 것을 다 할 수 있어 해자가 어디냐고
물었으며,[^charlie0]
lemagedurage는 diff를 보는 UI가 꽤 좋다고 답했다.[^lemagedurage]
README는 다른 도구와의 비교를 두지 않으므로 선택의 이유는 독자가 직접 시험해야
한다.

### 제품의 서술 방식이 신뢰에 영향을 준다

exizt88은 AI가 쓴 README를 가진 저장소는 진지하게 받아들이기 어렵다고
했고,[^exizt88]
asteroidburger는 설계 문서와 저장소를 주고 에이전트에게 README를 쓰게 하는 것이
무엇이 문제냐고 반문했다.[^asteroidburger]
이 문서는 README가 AI로 쓰였는지 판정하지 않는다.
다만 첫 인상이 갈리는 지점이라는 점은 도구를 처음 접하는 독자에게 영향을 준다.

## 인사이트

### worktree 격리는 병렬 에이전트의 충돌을 푸는 현재의 합의가 되었다

HN의 VMG는 jj에 익숙해진 다음 날 모두가 git worktree에 몰두한다고 했고,[^vmg]
mpalmer는 최신 jj가 같은 위치의 git worktree를 작업 공간 기능으로 지원한다고
답했다.[^mpalmer]
이 교환은 병렬 에이전트의 충돌을 푸는 방식이 도구마다 같은 형태로 모여들고
있음을 보여 준다.
이는 이 문서의 관찰이다.
이를 따르면 도구의 차별점은 격리 그 자체가 아니라 격리 위에 올린 검토와 PR
흐름이다.

### 에이전트가 많은 일을 하는 시점에는 로컬 IDE의 전제가 흔들린다

HN의 InsideOutSanta는 에이전트가 대부분의 일을 하고 코드 실행, 스크린샷,
클릭까지 자유를 주고 싶은데
이 모든 것이 로컬 컴퓨터에서 일어나는 구성은 이치에 맞지 않는다고
했다.[^insideoutsanta]
ThinkRail은 호스트와 UI를 분리하고 브라우저에서 같은 앱을 열 수 있게 해 이
방향을 일부 받아들인다.
설계 문서는 휴대폰이 Tailscale로 호스트에 닿는 것도 상정한다.[^architecture]
그러나 에이전트 실행 환경 자체의 격리(샌드박스)는 이 문서가 읽은 범위에서
확인되지 않았다.

### 기존 IDE 제조사의 딜레마는 사용자의 시간이 에이전트 쪽으로 옮겨 간 것이다

HN의 PippaSedai는 코딩 하네스를 처음 만난 것이 JetBrains IDE였지만 한 달도 안
되어 그 플랫폼을 쓰지
않게 되었다고 했다.[^pippasedai]
throwaw12는 JetBrains가 죽어 가며 살아남으려 애쓰는 것 같다고 했다.[^throwaw12]
이는 사용자의 인상이며 이 문서가 검증한 것이 아니다.
다만 도구의 이름이 늘어나는 것(Air와 ThinkRail)은 제조사가 어느 형태가 남을지
모르고 시험하고 있다는
신호로 읽을 수 있다.
이는 이 문서의 해석이다.

### 이 글을 읽는 방법

이 문서는 저장소의 README와 설계 문서와 제품 문서, 그리고 두 HN 스레드를 읽었다.
도구를 설치하거나 실행하지 않았고 pi 호환성 문서와 명세 파일의 실제 내용은 열어
보지 않았다.
GeekNews 토픽 35994에는 HN 댓글을 다시 모은 것뿐이라 GeekNews 사용자 댓글은
없다.
Lobste.rs에는 이 저장소의 스레드가 없었다.

주장을 가를 관찰은 두 가지다.
하나는 명세 그래프를 켠 세션과 끈 세션에서 같은 과제의 결과(회귀 수와 되돌림)를
비교한 결과다.
다른 하나는 Air나 다른 에이전트 IDE와 같은 저장소에서 같은 과제를 시켜 검토
시간과 충돌 빈도를 견준 자료다.
앞의 것이 있으면 명세가 기준이라는 주장을, 뒤의 것이 있으면 이 도구를 고를
이유를 알 수 있다.

---

[^architecture]: GitHub, [ThinkRail — top-level architecture](https://github.com/JetBrains/thinkrail/blob/main/architecture.md)

[^goal]: GitHub, [ThinkRail — product goal and scope](https://github.com/JetBrains/thinkrail/blob/main/goal-and-requirements.md)

[^exizt88]: <https://news.ycombinator.com/item?id=50235595>

[^asteroidburger]: <https://news.ycombinator.com/item?id=50235750>

[^vmg]: <https://news.ycombinator.com/item?id=50235329>

[^mpalmer]: <https://news.ycombinator.com/item?id=50235339>

[^deukhoofd]: <https://news.ycombinator.com/item?id=50235872>

[^crummy]: <https://news.ycombinator.com/item?id=50235945>

[^dr_faustus]: <https://news.ycombinator.com/item?id=50235680>

[^aliasxneo]: <https://news.ycombinator.com/item?id=50235307>

[^insideoutsanta]: <https://news.ycombinator.com/item?id=50235621>

[^throwaw12]: <https://news.ycombinator.com/item?id=50236417>

[^pippasedai]: <https://news.ycombinator.com/item?id=50219736>

[^rbehrends]: <https://news.ycombinator.com/item?id=50219882>

[^troupo]: <https://news.ycombinator.com/item?id=50219668>

[^swingboy]: <https://news.ycombinator.com/item?id=50219886>

[^zihotki]: <https://news.ycombinator.com/item?id=50220506>

[^bpicolo]: <https://news.ycombinator.com/item?id=50236004>

[^charlie0]: <https://news.ycombinator.com/item?id=50220013>

[^lemagedurage]: <https://news.ycombinator.com/item?id=50220186>
