# Reticle: AI 에이전트 작업 검증 도구

<https://docs.reticle.sh/>

<https://app.reticle.sh/>

<https://github.com/reticlehq/reticle>

HN 토론: <https://news.ycombinator.com/item?id=50163896> (11점, 6개 댓글)

GN 토론: <https://news.hada.io/topic?id=37440>

## 소개

Reticle은 코딩 에이전트가 「끝났다」고 한 작업을 실제로 돌아가는 앱에서 확인해 주는 도구이다.
README의 문구는 에이전트가 끝났다고 하면 Reticle이 그것이 사실인지 알아낸다는 것이다.
실제로 돌아가는 앱을 조작하고 일어난 일을 읽어서 통과, 실패, 판단 불가의 판정과 고칠 파일과 줄 번호를 돌려준다.
저장소 설명은 AI 에이전트가 코드를 만들어도 만든 것을 이해하지 못하는 문제를 두고, Jev 방식의 기계 친화적 런타임 인식을 웹과 데스크톱 앱에 가져온다고 한다.
직접 설치해 써 보지 않았다.
저장소의 홈페이지 필드인 `app.reticle.sh`는 대시보드로 보이며 JavaScript 앱이라 본문을 읽지 못했다.
문서 사이트의 나머지 페이지(도구 개요, 데스크톱, 프로덕션 모드, 텔레메트리 등)와 `SECURITY.md`는 열지 못했다.
설명은 모두 프로젝트의 주장이다.

GitHub API로 읽은 시점(2026년 11월 19일)의 수치는 별 1,303개, 포크 254개, 열린 이슈와 풀 리퀘스트 279개, 언어 TypeScript, 생성일 2026년 6월 11일, 마지막 푸시 2026년 11월 17일이다. GitHub의 라이선스 표시는 `NOASSERTION`이다. 라이선스 파일은 Apache License 2.0(저작권 Reticle Labs, 2026)이고 짧은 개요이며 각 패키지의 `LICENSE`와 `NOTICE`가 우선한다고 적는다. Tauri용 Rust 크레이트 `reticle-tauri`는 MIT이다. 상업과 OEM 문의는 `hey@reticle.sh`이다.
최신 릴리스는 v3.10.7(2026년 11월 17일)이고 11월 15일부터 17일까지 5개 릴리스가 나왔다.

## 사용법

### 설치 없이 점검

`npx @reticlehq/server`를 웹 프로젝트에서 실행하면 설정을 바꾸지 않고 페이지 로딩, 콘솔 오류, 실패한 요청, 내부 링크를 점검하고 `verified: yes`일 때만 종료 코드 0을 낸다. 문서는 `npx reticle`이 무관한 npm 패키지를 받으므로 반드시 `npx @reticlehq/server`를 쓰라고 경고한다. Node 20.11 이상이 필요하다.

### 프로젝트에 연결

- `npx @reticlehq/server init`: 프로젝트를 연결한다. 플래그는 `--dry-run`, `--app <dir>`, `--env KEY=VALUE`, `--files-only`, `--json`, `--no-mcp`, `--no-prompt-capture`이다.
- 한 번만 점검: `npx @reticlehq/server verify <url> --expect '<json>'`
- 설치 스크립트: macOS와 Linux는 `curl -fsSL .../install/install.sh | sh`, Windows는 `irm .../install/install.ps1 | iex`이다. 파이프 없는 대안은 `npm install -g @reticlehq/server` 뒤 `reticle setup mcp`이다.
- 스킬: `npx skills add reticlehq/reticle --skill reticle`
- Claude Code 플러그인: `/plugin marketplace add reticlehq/reticle`, `/plugin install reticle@reticlehq`, `/reload-plugins`
- 일반 MCP 항목: 명령 `npx`, 인자 `["@reticlehq/server", "mcp"]`
- 대시보드(선택): `reticle connect --project "My App"` 뒤 `reticle sync`이다.
- CI 관문: `reticle gate --since HEAD~1`

`init`은 파일을 바꾼다. 개발 의존성과 빌드 설정 플러그인과 `reticle-dev` 모듈을 더하고 `CLAUDE.md`와 `AGENTS.md`에 내용을 덧붙이며 `RETICLE.md`와 `.claude/commands/reticle.md`를 쓰고, 찾은 에이전트마다 MCP 항목을 등록하고 프롬프트 훅을 에이전트 설정(`.claude/settings.json`, `.cursor/hooks.json` 등)에 넣는다. 문제 해결 페이지는 에이전트가 `package.json`의 스크립트로 개발 서버를 백그라운드에서 띄울 수 있고 두 번째 서버를 띄우거나 프로세스를 죽이지 말라고 지시받는다고 적는다.

### 설정

`.reticle.json`은 `framework`, `projectId`, `port`(4400이 아닐 때만)를 담고 `"shareRequests": false`로 프롬프트를 로컬에 둔다. `RETICLE_PORT`, `RETICLE_API_KEY`(대시보드 CI 실행용), `RETICLE_PAIRING_TOKEN_DIR`(기본 `~/.reticle/pairing-token`) 환경 변수가 있다. Codex는 설치기가 `~/.codex/config.toml`의 `[mcp_servers.reticle]` 아래에 `default_tools_approval_mode = "approve"`를 더하며 Reticle 자신의 도구만 승인한다.

## 동작 방식

앱 안의 개발용 SDK가 DOM, 네트워크, 콘솔, 스토어 상태, 라우팅, React 파이버를 구조화된 이벤트로 읽고 픽셀은 읽지 않는다. 로컬 데몬(`127.0.0.1:4400`)과 MCP 도구가 이를 에이전트에 연결한다.
에이전트는 행동하기 전에 기대하는 결과를 먼저 정하고, 판정은 요청, 상태 변화, 콘솔 증거와 소스 파일과 줄을 담는다. 판정은 `yes`, `no`, `unknown`(판단 불가이며 통과가 아님), `no-fault`(증명할 선언이 없음)이다.
검증한 흐름은 저장해 모델 없이 다시 재생한다. 선택 기능인 하네스(Harness)는 에이전트나 사람이 여정을 설명하면 플랫폼이 이를 조작한다.
기본으로 광고되는 MCP 도구는 열 개이다. `reticle_navigate`, `reticle_look`, `reticle_act`, `reticle_act_and_wait`, `reticle_observe`, `reticle_assert`, `reticle_session`, `reticle_verify`, `reticle_tools`, `reticle_run`이다. 판정은 `reticle_act_and_wait`, `reticle_assert`, 단계가 `expect`를 선언한 `reticle_act`, `reticle_verify`에서만 나오고 `verified: yes`만 통과이다. 나머지(`reticle_screenshot`, `reticle_visual_diff`, `reticle_storage`, `reticle_network_mock`, `reticle_clock`)는 광고하지 않고 `reticle_run {tool, args}`로 부른다. 임의의 JavaScript를 페이지에서 실행하는 「evaluate」 도구는 없다.

## 지원 범위

문서의 프레임워크 표는 지원 수준을 구분한다.

| 수준                                    | 프레임워크                                                                                       |
| --------------------------------------- | ------------------------------------------------------------------------------------------------ |
| CI가 판정까지 구동                      | React + Vite, Next.js                                                                            |
| CI가 세션 부팅과 점검만                 | Remix, Astro                                                                                     |
| 설치는 막아 두었고 구동은 검증되지 않음 | SvelteKit, Nuxt, React Router 프레임워크 모드, Create React App, Angular 17 이상, Vue(Nuxt 제외) |
| 연결만 되고 검증되지 않음               | TanStack Start, 일반 HTML, 서버 렌더링 스택(Django, Flask, FastAPI, Rails)                       |

Preact는 센서만 있고 구동은 검증되지 않았다. 소스 파일과 줄은 React와 Svelte에서 되고 Vue와 Angular에서는 안 된다. 데스크톱은 Electron과 Tauri이며 IPC 경계를 포함한다. 시험한 브라우저는 Chromium이고 운영체제는 macOS, Linux, Windows이다. 연결 대상 에이전트는 Claude Code, Cursor, Codex, Windsurf, VS Code, Gemini CLI 등이다.
패키지는 `@reticlehq/server`(CLI와 데몬), `core`, `engine`, `browser`(프레임워크 중립 SDK), `react`, `next`, `electron`, `vite-plugin`, `babel-plugin`, `eslint-plugin`, `init`, `test`(스펙 실행기) 등이다.

## 보안과 프라이버시

- 로컬 우선: 브리지는 `127.0.0.1`에서 듣고 토큰은 소유자만 읽는 `~/.reticle/`에 둔다. 판정은 계정 없이 로컬에서 낸다. `reticle connect`나 `RETICLE_API_KEY`를 쓰지 않으면 앱의 DOM, 네트워크 본문, 콘솔, 상태, 소스가 기계 밖으로 나가지 않는다고 한다.
- 프롬프트: 각 프롬프트는 가려진 채 `.reticle/`에 보관되고, 연결된 프로젝트는 기본으로 실행과 함께 프롬프트를 보낸다. 비밀번호, 토큰, 카드 번호는 캡처 전에 `[REDACTED]`로 바뀐다.
- 텔레메트리: 익명 사용 횟수가 기본으로 켜져 있다. 어떤 명령과 도구가 쓰였는지와 무작위 식별자뿐이고 앱 내용, IP, 위치는 없다고 한다. 끄려면 `reticle telemetry disable`, `RETICLE_TELEMETRY=0`, `DO_NOT_TRACK=1`을 쓴다.
- 프로덕션 빌드는 프로덕션 모드(서명된 로더)를 고르지 않으면 SDK를 포함하지 않는다.

## 용도와 코드로 쓰는 검증

문서의 용도 페이지는 다음을 든다.

- 에이전트가 바꾼 기능: `POST /api/orders` 네트워크 조건(상태 201, 호출 횟수 1)과 장바구니 스토어 확인, 콘솔 오류 없음을 한꺼번에(`allOf`) 확인하고, 저장한 흐름을 모델 없이 재생하며 `gate --since HEAD~1`로 CI에 건다.
- 보안: 403 확인, 호출되지 않아야 할 엔드포인트의 무발화 확인, `[REDACTED]` 값, CSP 위반(콘솔 오류로 나타남)이다.
- 접근성: 역할과 이름 조회, 대화상자의 포커스, Enter와 Escape 입력이다. 탭 순서는 검증할 수 없어 판단 불가로 보고한다.
- 성능: 중복 요청 발견, LCP와 누적 레이아웃 이동과 긴 작업 이벤트, CI의 `verify <url>`이다.
- SEO: 제목과 경로, 링크 주소, 리다이렉트 조건, 크롤 검증이다.
- 페르소나 탐색: `explore --persona`, 격리된 컨텍스트를 위한 `reticle_lease`, 커버리지 동작이다.

코드로 검증하려면 `@reticlehq/test`의 `reticleTest`와 `bootSession({driveUrl, headless: true})`, `runSpecs`를 쓰며 `t.act`, `t.fill`, `t.actAndWait`, `t.expectSignal`, `t.expectNet`, `t.expectElement`, `t.expectText`, `t.expectAbsent`, `t.expectNoConsoleErrors`, `t.clock.freeze` 같은 메서드가 있다. 건너뛴 시험은 실패가 아니지만 전부 건너뛴 묶음은 `ok`가 거짓이다. 저장한 흐름은 `registerFlowSpecs('.reticle/flows', ...)`로 vitest 시험처럼 돌린다.
도구 광고 면적도 문서가 수치로 제시한다. 기본 열 개는 스키마 토큰이 약 4,650(2026년 10월 8일 측정)이고 `RETICLE_ADVERTISE_ALL_TOOLS=1`로 30개를 광고하면 약 35,000이다. 읽기 응답에는 `{bytes: 944, tokens: 236}` 같은 비용 필드가 붙는다.

## 데스크톱과 프로덕션 모드

데스크톱 앱은 앱이 데몬(예시에서 `localhost:4400`)으로 접속하는 구조이며 `npx @reticlehq/server serve`와 `status`를 쓰고 데스크톱에는 열기와 구동 명령이 없다. IPC는 `ipc://<채널>`로 기록된다. Electron과 Tauri 모두 핵심 도구, IPC, 스크린샷, 헤드리스가 되고 `network_mock`과 `viewport`는 안 된다. Electron은 렌더러 설정에 `reticle({desktop: true})`와 프리로드 첫 줄 `require('@reticlehq/electron/preload')`가 필요하고, 샌드박스된 프리로드는 번들링이나 `sandbox: false`가, 패키징된 렌더러는 `vite build --mode development`가 필요하다. Tauri는 CSP의 `connect-src`에 `ws://localhost:4400`과 `ipc: http://ipc.localhost`가 있어야 하며 없으면 조용히 실패한다. Windows WebView2 캡처는 컴파일만 되고 시험되지 않았고 `fullPage`는 Tauri의 Linux에서만 된다고 한다.

프로덕션 모드는 구동마다 활성화해야 하는 선택 기능이다. 티켓 서비스(404면 미지원), 연결된 프로젝트, 로더(`@reticlehq/browser/activate`), 로그인한 브라우저가 필요하다. 티켓은 Ed25519 서명이고 난스는 60분 유효하며 `?reticle_activate=<티켓>`으로 연다. `observe` 범위는 모든 행동을 거부하고 `act` 범위도 결제, 프로젝트와 워크스페이스 삭제, 키 폐기와 교체, 초대와 이메일, 구독 취소, 역할 변경은 의도에 명시하지 않으면 거부한다. 거부는 리스된 브라우저에서 요청마다 강제된다(403).

## 기록과 텔레메트리

- 기록: 판정은 계정 없이 로컬에서 낸다. 로컬에는 실행(runs), 흐름(flows, git에 넣는 용도), 메모리(`coverage.json`, `notes.json`, `requests.jsonl`), 에피소드(`episodes/`, 증거이며 git에 넣지 않음)가 쌓인다. 비밀 필드는 `<redacted: supply at replay>`로 저장되고 재생이 `RETICLE_SECRET_<필드>` 환경 변수를 읽는다. 가림은 이름 기반이다. 네트워크 본문은 기본으로 끄고 HTTP 400 이상의 오류 본문만 4KB까지 둔다(`captureNetworkBodies: true`로 켬).
- 연결 후 동기화: `config --runs|--flows|--memory on|off`로 고른다. 프롬프트는 `"shareRequests": false`나 `"promptCapture": false`(또는 `RETICLE_PROMPT_CAPTURE=0`)가 아니면 기본으로 공유된다. 데몬이 연결된 앱을 10초마다 플랫폼에 알리고 구동 스크린샷은 JPEG로 초당 약 1장이다.
- 텔레메트리: 사용 횟수만 보내며 PostHog(미국 클라우드)로 가고 `$ip`는 0.0.0.0, 지오IP는 끈다. 익명 UUID는 `~/.reticle/telemetry-id`에 있고 이벤트 종류는 25가지(표에는 26행이나 `identified`는 이 버전에서 보내지 않음)이다. 코드, DOM, 네트워크, 콘솔, 상태, 스크린샷, 경로, 프로젝트와 흐름 이름, 환경 변수, 입력한 글자는 보내지 않는다고 한다. 피드백은 수동이며 클라이언트에서 가려지고 `RETICLE_FEEDBACK=0`으로 끈다. 식별 삭제는 `hey@reticle.sh`로 요청한다.
- 보안 제보: `SECURITY.md`는 `hey@reticle.sh`로 비공개 제보하면 영업일 2일 안에 접수한다고 한다. 브리지는 `127.0.0.1`에서만 듣고 SDK는 개발용이며 런타임이 `NODE_ENV=production`을 거부한다. 지원 범위는 기본 브랜치의 최신 마이너 릴리스이다.

## 한계와 벤치마크

README가 인정하는 한계는 다음과 같다. 조용히 실패한 요청, 화면과 다른 상태, 낡은 캐시, 이중 제출에는 강하다. 한 행동 주변의 경쟁 조건에는 부분적으로만 강하고 완전한 경쟁 분석기가 아니다. IndexedDB, Web Worker, 닫힌 shadow root, 교차 출처 iframe은 아직 보지 못한다.
벤치마크 페이지는 모두 제작사가 돌린 값이다.

| 비교                       | Reticle                                                        | Playwright 스크립트                     |
| -------------------------- | -------------------------------------------------------------- | --------------------------------------- |
| 버그 88개 목록에서 잡은 수 | 85(구조적으로 잡을 수 있는 86 중 85, 거짓 통과 1, 거짓 경보 0) | 59(60 중 57, 거짓 통과 29, 거짓 경보 0) |
| 버그당 출력 바이트         | 9,261                                                          | 5,849                                   |

범주별로 콘솔, 네트워크, 스토리지, 시각 UI는 둘 다 만점이고 상태 8 대 0, 비즈니스 로직 6 대 0, 신호 4 대 0, 네트워크 상태 4 대 1, 스트림 3 대 0, 성능 3 대 1, 깊은 DOM 2 대 2(3 중)이다. 이 값은 「2.9.0 브랜치」에서 다시 구한 것이라 인용 전에 다시 돌리라고 문서가 적는다.
MCP 도구와의 비교(2026년 6월 22일, `@playwright/mcp@0.0.76`, `chrome-devtools-mcp@1.3.0`)에서 Reticle은 10 중 10, 한 번 보기당 815토큰이고 DevTools는 10 중 8에 758토큰, Playwright MCP는 10 중 9에 1,292토큰이다. 실제 대시보드의 한 번 관찰은 Reticle 1,023, DevTools 1,357, Playwright MCP 2,193토큰이다. 재생은 흐름당 실행 약 239토큰(2026년 8월 11일), 네 흐름 묶음 약 480토큰(10월 6일)이며 큰 페이지는 전체 스냅샷 약 3,636 대 표적 반복 약 279토큰이다. 흐름 16개는 직렬 35.4초 대 컨텍스트 8개 병렬 5.2초(6.78배)이다. 기업 규모 계산(하루 200개 풀 리퀘스트에 흐름 50개)은 「추정」으로 표시되어 흐름 실행당 약 240 대 30,000토큰, 약 125배라고 한다.
SDK 부담은 전체 1.669초(바쁜 비율 20.9%), 관찰자만 1.627초, Reticle 없음 1.610초이고 계측 +0.21%p는 잡음(±1.23%p) 안이며 예산은 3% 미만이라고 한다. 문서는 Reticle이 지는 곳도 적는다. DevTools가 한 번 보기당 약간 더 쌀 수 있고, 실제 픽셀을 보지 못하며, 스크린샷 에이전트와의 비교는 하지 않았다.
README 캡션의 토큰 수치(100회 실행에서 12만 8천 대 1,210만)와 이 페이지의 흐름별 수치는 측정 단위가 달라 직접 대응시키지 못했다. 가격은 요금제 이름과 금액이 문서에 없다. 로컬 도구는 무료이고 계정이 필요 없으며, 새 계정은 하네스용 무료 크레딧을 받고 카드를 등록하면 14일 체험(500 크레딧)이 시작된다고 한다.

## 분석

### 중심 주장은 에이전트의 완료 선언에 증거를 붙인다는 것이다

에이전트가 코드를 고치고 끝났다고 말하는 지점에 앱을 실제로 돌려 확인하는 단계를 끼운다. 판정에 「판단 불가」를 따로 두어 확인하지 못한 것을 통과로 세지 않는 설계가 중심이다.
이는 README의 서술을 이 문서가 정리한 것이다.

### 픽셀이 아니라 구조화된 이벤트를 읽는다

SDK가 앱 안에서 DOM과 네트워크와 상태를 직접 읽는 것은 화면 캡처를 해석하는 방식과 다른 접근이다. 같은 기능을 하는 Playwright MCP와의 비교에서 토큰이 100배 가까이 적다는 주장은 이 구조에서 나온다고 설명된다. 이는 이 문서의 해석이다.

### 같은 주제의 다른 도구와 놓인다

같은 영역에 앱 조작 검증과 하네스를 다룬 이 저장소의 다른 문서(`agentic-coding/frontierharness-eval-v1-1.md`, `agentic-coding/claude-code-team-verification.md`)가 있다.

## 비평

### 벤치마크가 제작사의 것이고 시점이 흩어져 있다

85 대 59와 토큰 수치는 제작사가 직접 만든 버그 목록과 흐름에서의 값이다. 버그 목록의 구성(어떤 종류의 회귀를 넣었는지)이 Reticle에 유리하게 정해졌을 가능성을 독립 재현 없이는 가릴 수 없다.
같은 페이지의 값이 「2.9.0 브랜치」(버그 목록), 2026년 6월 22일(MCP 비교), 8월과 10월(재생 토큰)로 측정 시점이 다르고 현재 릴리스는 3.10.7이다. 어느 값이 현재 버전의 것인지는 페이지가 날짜로만 알려 준다. 가장 큰 격차(상태, 비즈니스 로직, 신호 범주의 8 대 0 등)는 Reticle이 읽는 구조화된 이벤트가 선언된 기대와 맞물릴 때의 값이며 그렇지 않은 일반 시험에서는 다를 수 있다. 이는 이 문서의 해석이다.

### 범위가 CI로 검증된 조합에 한정된다

CI가 판정까지 구동하는 조합은 React + Vite와 Next.js뿐이다. Svelte, Vue, Angular, Nuxt 등은 설치만 막아 두었거나 연결만 되고 검증되지 않았다. 홍보 문구의 범위보다 문서의 표가 좁다.

### 설치가 많은 것을 바꾼다

`init`이 의존성, 빌드 설정, `CLAUDE.md`와 `AGENTS.md`, 에이전트 설정의 훅, 여러 에이전트의 MCP 항목을 한꺼번에 바꾼다. 설치 스크립트는 `curl | sh`와 `irm | iex` 형태로 안내된다. 프롬프트를 캡처하는 훅이 기본으로 켜져 있어, 연결한 프로젝트는 기본으로 프롬프트를 대시보드에 보낸다.
README는 가려 두고(redact) `shareRequests: false`나 `--no-prompt-capture`로 끌 수 있다고 하지만, 처음 쓰는 사람이 기본값이 무엇인지 알아야 하는 구조이다.

### 라이선스 표시가 헷갈린다

GitHub가 `NOASSERTION`으로 표시하고 라이선스 파일이 개요일 뿐이며 패키지마다 라이선스가 다르다(npm 패키지는 Apache-2.0, `reticle-tauri`는 MIT). 도입하는 팀은 쓰는 패키지의 `LICENSE`와 `NOTICE`를 따로 확인해야 한다.

### 초기 프로젝트의 빠른 변화이다

생성한 지 다섯 달 남짓에 열린 이슈가 279개이고 사흘 사이에 릴리스가 다섯 번이다. 릴리스 노트의 내용은 판단 불가를 실패로 잘못 세던 문제, 스크린샷이 페이드 인한 행을 빠뜨리던 문제 등 세부 수정이다. 인터페이스가 안정되었는지는 읽은 범위에서 알 수 없다.

### 외부 반응

HN의 Show HN 글에는 댓글 여섯 개가 모두 질문이었다.
Lobste.rs의 `reticle.sh` 도메인에는 글이 없었고 `reticle` 검색 결과는 모두 다른 주제였다.

## 인사이트

### 가져갈 것은 판단 불가를 통과와 구분하는 검증 설계이다

확인하지 못한 것을 실패나 통과로 세지 않고 별도 상태로 두면, 에이전트의 「됐다」를 믿을지 판단하는 근거가 생긴다. 자기 팀의 에이전트 검증 단계를 설계할 때 이 판정 체계를 점검표로 쓸 수 있다. 이는 이 문서의 적용이다.

### 처음에는 설치 없이 한 번 돌려 본다

`npx @reticlehq/server`는 설정을 바꾸지 않고 로딩, 콘솔 오류, 실패한 요청, 내부 링크를 확인한다. 이 결과를 보고 `init`의 변경 범위(`--dry-run`)를 확인한 뒤 연결한다.

### 도입 전에 조건을 확인한다

쓰는 프레임워크가 CI로 판정까지 구동되는 수준인지, 프롬프트 캡처와 텔레메트리의 기본값을 끌 것인지, 패키지 라이선스가 맞는지를 먼저 확인한다.

### 확인할 관찰

이 프로젝트의 주장을 가를 관찰은 세 가지이다.
제작사 밖에서 같은 조건으로 잰 검출률과 토큰 비용,
CI 판정을 지원하는 프레임워크의 확대,
릴리스가 안정되는 속도와 이슈 처리이다.
