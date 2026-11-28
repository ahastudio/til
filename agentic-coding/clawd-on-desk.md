# Clawd on Desk

<https://clawdondesk.com/>

<https://github.com/rullerzhou-afk/clawd-on-desk>

HN 토론: <https://news.ycombinator.com/item?id=48316607> (1점, 0개 댓글)

## 소개

Clawd on Desk는 AI 코딩 에이전트의 상태에 맞춰 움직이는 데스크톱 펫(Electron 앱)이다.
에이전트가 일하면 캐릭터가 일하고, 입력이 필요하면 알리고,
권한 요청이 오면 화면에 허용과 거부 말풍선을 띄운다.
소스는 AGPL-3.0-only이고 그림은 전부 저작권자에게 있는 별도 조건이다.
2026년 11월 25일 GitHub API로 본 별은 6,805개이고
2026년 3월 18일에 시작되어 마지막 푸시는 11월 24일이다.
언어는 JavaScript이고 커밋은 약 3,223개이다.

저장소를 받아 코드를 읽었으며 설치하거나 실행하지 않았다.
읽은 범위는 각 절에 파일 이름으로 적었고 읽지 못한 부분도 따로 적었다.

## 동작 방식

### 모듈 구성

| 경로                                    | 읽어서 확인한 역할                                             |
| --------------------------------------- | -------------------------------------------------------------- |
| `src/main.js`                           | Electron 진입점. 단일 인스턴스 잠금, 설정 경로, 각 모듈 연결   |
| `src/server.js`                         | `127.0.0.1` HTTP 서버, 포트 선택, `~/.clawd/runtime.json` 기록 |
| `src/server-route-state.js`             | `/state` POST 본문 해석, 본문 16KB 제한                        |
| `src/server-route-permission.js`        | `/permission` 처리, 본문 512KB 제한                            |
| `src/state.js`                          | 세션 맵, 표시 상태 판정, 정리 타이머                           |
| `src/state-priority.js`                 | 우선순위 표와 세션 합산 함수                                   |
| `src/state-stale-cleanup.js`            | 세션 만료 상수와 판정                                          |
| `src/permission.js`                     | 말풍선, 단축키, 응답 본문 생성                                 |
| `src/permission-automation-policy.js`   | 자동 승인 정책                                                 |
| `src/prefs.js`                          | `clawd-prefs.json` 스키마와 검증                               |
| `src/network/mobile-preview-server.js`  | LAN WebSocket과 PWA 서빙                                       |
| `hooks/*-install.js`, `hooks/*-hook.js` | 도구별 설치기와 훅 스크립트                                    |
| `agents/registry.js`                    | 도구 설정 29개 등록                                            |

### 도구마다 설치기가 따로 있다

`agents/registry.js`는 도구 설정 29개를 배열로 등록한다.
`agents/` 디렉터리의 파일은 37개인데 나머지는 registry와
Codex·Gemini·Kimi·Kiro 로그 감시기 같은 보조 모듈이다.
설정의 `eventSource` 값은 hook 21개, plugin-event 5개, extension 2개,
hook+log-poll 1개이다.
도구마다 훅, 플러그인, 확장, 대화 기록 읽기 중 하나로 상태를 얻는다.
프로세스 이름은 살아 있는지 확인하는 보조로 쓰인다는 서술은
설정의 `processNames` 필드로만 확인했고 쓰이는 곳은 끝까지 따라가지 않았다.

- Claude Code: `hooks/install.js`가 `~/.claude/settings.json`에 명령 훅을 쓰고
  `hooks/clawd-hook.js`가 실행된다. 권한 요청은 `127.0.0.1:23333/permission`으로
  가는 블로킹 HTTP 훅이다. 훅 스크립트는 대화 기록의 마지막 256KB도 읽는다.
- Codex: `~/.codex/hooks.json`의 공식 훅과, 예비로
  `~/.codex/sessions/**/rollout-*.jsonl`을 1,500ms 주기로 읽는 감시기가 있다.
- Cursor: `~/.cursor/hooks.json`에 훅을 쓰며 권한 말풍선은 없다.
- 그 밖에 약 30개 도구는 도구별 설치기와 플러그인, 확장으로 연결된다.

### 상태의 우선순위

`src/state.js`(4,924줄)와 `src/state-priority.js`가 상태 우선순위를 정한다.
`STATE_PRIORITY`는 오류 8, 알림 7, 청소 6, 주의 5, 저글링·운반 4,
executing 3.5, 작업 3, 생각 2, 대기·roam 1, 수면 0이다.
앞 문서가 빠뜨린 executing과 roam도 같은 표에 있다.
테마 파일(`themes/clawd/theme.json`)의 `timings`에는
최소 표시 시간 1~5.5초, 하품 3초, 깨어남 1.5초,
마우스 대기 20초, 마우스 수면 60초, 깊은 수면 10분이 적혀 있다.
테마는 `clawd`, `calico`, `cloudling`, `template`이고 그림은 SVG이다.

### 서버와 보안 경계

훅 스크립트는 `127.0.0.1`에만 열린 HTTP 서버로 POST한다.
포트는 23333~23337 중에서 고르고 모두 쓰이면 임의 포트로 넘어간다.
로컬 서버에는 토큰이 없고 Origin 헤더가 있는 요청(403),
루프백이 아닌 Host(403), 중복된 Host·Content-Type(400),
JSON이 아닌 Content-Type(415)을 거절한다.
확인한 곳은 `src/server.js`의 `rejectUnsafeLocalHookRequest`이다.
이 함수의 주석이 같은 OS 사용자의 다른 프로세스는 인증하지 못한다고 밝히고,
`docs/guides/known-limitations.md`도 Clawd가 꺼진 뒤 다른 로컬 프로세스가
정적 훅 주소의 포트를 잡을 수 있다고 적는다.
`x-clawd-routing-nonce` 헤더를 단 요청은 로컬 서버가 404로 돌려보낸다.
이 nonce는 Remote SSH 전용 수신구에서만 쓰이므로 로컬 서버의 인증이 아니다.
모바일 미리보기는 별도 서버를 `0.0.0.0`의 23334~23338 포트에 열고
기기별 토큰을 주소에 싣는 읽기 전용이다.

### 신호 수집에서 화면까지

Claude Code 설정(`agents/claude-code.js`)의 `eventMap`은 훅 이벤트를 상태로 바꾼다.
UserPromptSubmit은 thinking, PreToolUse와 PostToolUse는 working,
PostToolUseFailure와 StopFailure는 error, Stop은 attention이다.
SubagentStart는 juggling, PreCompact는 sweeping, Notification은 notification이다.
`hooks/clawd-hook.js`는 대화 기록의 마지막 256KB(`TRANSCRIPT_TAIL_BYTES`)를 읽는다.
일부 이벤트는 이 읽기를 건너뛴다고 주석이 적는다.
이 값으로 세션 제목을 뽑고, Stop이 오면 직전 턴의 API 오류를 찾아 ApiError로 바꾼다.
그리고 상태 서버로 POST한다.

서버의 `handleStatePost`는 본문을 JSON으로 풀고 에이전트 식별자를 검증한 뒤
`src/state.js`의 `updateSession`으로 넘긴다.
알 수 없는 에이전트는 204로 조용히 버린다.
`resolveDisplayState`는 세션들 가운데 우선순위가 가장 높은 상태를 고른다.
`src/state-priority.js`의 `resolveDisplayStateFromSessions`가 그 일을 하며
머리 없는(headless) 세션은 건너뛰고 세션이 없으면 idle을 돌려준다.
압축 중이면 sweeping으로 올리고 권한 말풍선이 떠 있으면 notification으로 덮는다.
고른 상태는 `setState`와 `applyState`를 거쳐 테마의 SVG 파일에 연결된다.

세션 정리는 `cleanStaleSessions`가 10초마다 돈다(`startStaleCleanup`).
`src/state-stale-cleanup.js`의 기본값은 세션 만료 600초, 작업 중 만료 300초,
분리된 대기 세션 30초이다.
Codex와 opencode의 로컬 작업 중 세션은 만료 하한이 20분이다.
`src/prefs.js`는 작업 중 만료를 세션 만료 이하로 낮춘다.

Codex는 훅 말고도 `agents/codex-log-monitor.js`가 rollout 파일을 읽는다.
기본 주기는 `pollIntervalMs` 설정이 없으면 1,500ms이다.
한 번의 폴링에서 파일 하나는 4MB, 전체 요청은 16MB, 파일 시도는 64개로 제한된다.

### 권한 요청의 경로

Claude Code의 PermissionRequest는 `hooks/install.js`의 `HTTP_HOOKS`가
`http://127.0.0.1:23333/permission`, 제한 시간 600초로 등록한다.
명령 훅이 아니라 응답을 기다리는 HTTP 훅이다.
고정 주소이므로 서버가 23333을 못 잡고 다른 포트로 올라가면
이미 떠 있는 CLI는 새 세션이나 훅 재적재가 필요하다고
`docs/guides/known-limitations.md`가 적는다.
`src/server-route-permission.js`는 연결이 끊기면 `res.on("close")`로 요청을 취소한다.
응답 본문은 `src/permission.js`의 `buildCodexPermissionResponseBody` 같은 함수가
`behavior`가 allow 또는 deny인 값만 통과시켜 만든다.
`PASSTHROUGH_TOOLS`(TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop, TaskOutput)는
말풍선 없이 허용된다.

자동 승인은 `src/prefs.js`의 `permissionAutomationMode`로 정해지며
기본값은 off이고 off, auto-tools, unattended 중 하나이다.
unattended는 시작할 때 auto-tools로 내려가 켜진 채 시작하지 않는다.
`src/permission-automation-policy.js`의 `classifyPermissionInteraction`은
에이전트 식별자와 도구 이름만으로 요청 성격을 정하고
페이로드가 보낸 상호작용 필드는 쓰지 않는다고 주석이 밝힌다.
Claude Code와 Qwen Code는 허용 목록(`CLAUDE_COMPATIBLE_TOOL_APPROVAL_NAMES`)에 있는 도구나
`mcp__서버__도구` 꼴의 MCP 도구만 자동 허용 대상이 되고
새 내장 도구는 검토 전까지 자동 허용에서 빠진다.
파괴적 명령 알림과 외부 검토 명령은 자동 허용을 사람에게 돌리기만 하고
허용으로 바꾸지는 못한다.
이 알림은 기본값이 꺼져 있다.
`known-limitations.md`는 이 알림이 heredoc 본문에서 분석 오류를 내면
자동화가 멈출 수 있다고 적는다.

### 저장과 외부 통신

설정은 Electron의 userData 폴더에 `clawd-prefs.json`으로 저장된다.
읽을 수 없는 내용은 `.bak`으로 백업하고 기본값을 쓴다.
서버 주소는 `~/.clawd/runtime.json`에 기록되어 훅이 읽는다.
Claude Code와 Codex의 기본값은 `enabled`와 `integrationInstalled`가 모두 true라서
시작할 때 `syncEnabledStartupIntegrations`가 두 도구의 훅을 맞춘다.
다른 도구는 기본값이 꺼져 있다.
Telegram은 Go 보조 프로그램이 v0.14에서 은퇴했고
`src/telegram-native-client.js`가 `getUpdates` 25초 롱폴링으로 직접 통신한다.
옛 설정은 `src/telegram-migration-state.js`가 새 검증 절차로 안내한다.
따라서 옮기는 중이라던 앞 서술은 코드 쪽에서는 옛 방식이 이미 없다는 쪽이 맞다.
봇 토큰은 userData의 `telegram-approval.env` 파일에 평문으로 저장되며
임시 파일을 0600 권한으로 만들어 쓴다.
Slack 알림은 `hooks.slack.com`에 고정된 웹훅과 `slack.com`의 `chat.postMessage`로 나간다.
이 클라이언트의 주석은 리다이렉트를 따라가지 않도록 막는 이유를 적고 있다.

모바일 미리보기 서버(`src/network/mobile-preview-server.js`)는
기본 포트 23334에서 5개 범위를 쓰고 기기 토큰은 `~/.clawd/mobile-token.json`에 둔다.
새 토큰은 저장하고 실제로 써 본 뒤에야 바뀌며 주석은 읽기 전용(M1)이라 밝힌다.
짝 맞추기 코드는 한 번 쓰는 코드로 60초 안에 연결해야 하고
같은 IP에서 10분 안에 20번 실패하면 막는다.
동시에 짝 맞추는 연결은 4개로 제한된다.
QR은 `mobile-pair-qr.js`가 LAN IP와 코드만 담고 기기 토큰은 담지 않는다.
클라이언트가 보낸 메시지 중 `token_rotate_ack`만 처리하고 나머지는 무시한다.

### 의존성과 테스트

`package.json` 1.7.0의 런타임 의존성은 10개이다.
`@larksuiteoapi/node-sdk`, `electron-updater`, `htmlparser2`, `jsonc-parser`,
`koffi`(고정 2.16.3), `markdown-it`, `multiplex`, `qrcode-generator`, `ws`, `yauzl`이다.
개발 의존성은 `electron` 41.x, `electron-builder`, `esbuild`, `@electron/asar`, `js-yaml`이다.
`koffi`는 네이티브 호출용이며 `src/main.js`, `src/mac-window.js`,
`src/win-foreground-terminal.js`, `src/linux-x11-cursor.js` 등이 불러온다.

테스트는 `test/run-tests.js`가 `node --test test/*.test.js`를 실행한다.
기본 제한 시간은 테스트당 120초이고 Windows에서는 동시성을 2로 낮춘다.
`test/` 아래 `.test.js`는 706개, 전체 `.js`는 753개이다.
앞 문서의 753개는 도우미와 fixture 파일까지 센 값이었다.
`.github/workflows/test.yml`은 ubuntu, macos, windows에서 `npm ci` 뒤 `npm test`를 돌린다.
Linux는 `xvfb-run`을 쓴다.
테스트 이름으로 확인한 범위는 서버 경로(`server-route-state`, `server-route-permission`),
상태(`state`, `tick`), 설치기(`install`, `codex-hook`, `clawd-hook`),
Remote SSH, Telegram·Feishu·Slack 클라이언트이다.
각 테스트의 단언 내용은 읽지 않았다.

## 분석

### 한 마리의 펫으로 모든 도구를 합친다

Pixel Agents가 에이전트 하나에 캐릭터 하나를 주는 데 비해
Clawd는 20여 도구의 상태를 하나의 합산 상태로 접어 캐릭터 하나에 보여 준다.
그 대가로 어느 에이전트가 무엇을 하는지는 알 수 없다.
대신 도구별 설치기를 두어 지원 범위가 넓고,
WebSocket 없이 로컬 HTTP의 `/state`와 `/permission`이 핵심 경로이다.

### 권한 말풍선이 차별점이다

관찰만 하는 도구와 달리 권한 요청에 화면에서 답하는 것이 중심 기능이다.
자동 승인 모드도 있다.
편의가 큰 만큼 승인 경로가 로컬 HTTP 훅이라는 점이 보안 경계가 된다.

## 비평

### 라이선스와 그림의 조건

소스는 AGPL이지만 그림은 AGPL이 아니며 README와 `assets/LICENSE`가
전부 저작권자에게 있다고 적는다.
README는 Clawd 캐릭터가 Anthropic의 것이고 개인 이용 한도의 팬 프로젝트라고 밝힌다.

### 범위가 커진 만큼 면이 넓다

펫에서 출발했지만 대시보드, 사용량 링, 요약, Telegram·Feishu·Slack 연동,
LAN 모바일 앱, SSH 원격 배포까지 붙었다.
첫 실행 때 Claude와 Codex의 훅이 자동으로 등록되고
설정 파일 세 곳(`settings.json`, `hooks.json`, `~/.cursor/hooks.json`)과 `~/.clawd/`에 쓴다.
로그인 시 자동 실행도 등록된다.
알림 연동을 켜면 정보가 컴퓨터 밖으로 나간다.
`known-limitations.md`는 Clawd가 꺼진 뒤 다른 로컬 프로세스가 훅 포트를 잡을 수 있음을 인정한다.

### 설명과 코드의 차이

README의 “12가지 애니메이션 상태”는 코드의 상태 수와 맞지 않는다.
`theme.json`의 `states`는 16개이고 `STATE_PRIORITY`는 12개 이름을 갖는다.
두 수가 다르므로 README가 어느 쪽을 센 것인지는 확인하지 못했다.
Telegram 기능은 Go 보조 프로그램이 v0.14에서 은퇴한 뒤
코드에 옛 방식의 실행 경로가 없고 옛 설정을 안내하는 상태 기계만 남아 있다.
`package.json`의 설명은 아직 Claude Code만 언급하고 README에는 문장이 끊긴 곳이 있다.

### 성숙도

JavaScript와 TypeScript 소스는 `src`, `hooks`, `agents`, `extensions`, `scripts`, `pwa`
합계로 약 26.7만 줄이고 `test/`의 JS는 753개 파일에 약 37.2만 줄이다.
테스트 파일(`.test.js`)은 706개이고 CI 워크플로는 11개이다.
테스트는 실행하지 않았고 실제 동작과 설치 파일 서명은 확인하지 못했다.

## 인사이트

### 가져갈 것

여러 도구를 쓰면서 한 마리 펫으로 큰 흐름만 보고 싶고
권한 요청에 곧바로 답하고 싶다면 이 도구가 맞는다.
에이전트별 상태를 한눈에 보려면 Pixel Agents 계열이 맞다.
설치 전에 설정 파일 세 곳과 `~/.clawd/`가 바뀐다는 점,
AGPL 소스와 별도 조건의 그림을 구분해야 한다는 점을 알아 두어야 한다.

### 확인할 관찰

1. 권한 말풍선의 자동 승인 모드가 오승인을 낸 사례가 있는지.
2. 훅 포트를 다른 프로세스가 가로채는 시나리오의 완화책이 추가되는지.
3. 도구마다 훅 사양이 바뀔 때 설치기가 따라가는 속도.
