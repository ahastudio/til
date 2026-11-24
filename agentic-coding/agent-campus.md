# Agent Campus

<https://mateovalle.github.io/agent-campus/>

<https://github.com/mateovalle/agent-campus>

HN 토론: <https://news.ycombinator.com/item?id=49730005> (5점, 3개 댓글)

## 소개

Agent Campus는 Claude Code 에이전트를 픽셀 사무실의 캐릭터로 보여 주는 데스크톱 앱(Electron)이다.
한때 Pixel Agents라는 이름으로 Show HN에 올라왔고,
`github.com/mateovalle/pixel-agents`는 이름이 겹쳐 개명했다고 알리는 두 파일짜리 저장소로 남아 있다.
현재 저장소는 agent-campus이고 MIT 라이선스, 버전 0.4.1이다.
2026년 11월 25일 GitHub API로 본 별은 10개, 생성일은 2026년 7월 27일,
커밋은 약 245개이며 마지막 커밋은 11월 16일이다.
README의 출처 표기에 따르면 pablodelucca/pixel-agents에서 갈라져 나온 프로젝트이다.

프로젝트 사이트는 이 문서가 열어 읽었다.
소개 문구는 “모든 프로젝트가 한 캠퍼스 지도의 사무실이고, 모든 에이전트가 지켜볼 수 있는 캐릭터”이다.
저장소를 받아 `electron/`, `src/core/`, `shared/`의 코드를 직접 읽었으며 설치하거나 실행하지 않았다.
`webview-ui/`는 파일 목록과 일부 상수만 보았고 렌더링 코드는 끝까지 읽지 못했다.

## 동작 방식

### 모듈 구성

| 경로                           | 줄 수 | 역할                                      |
| ------------------------------ | ----- | ----------------------------------------- |
| `electron/main.ts`             | 3,451 | 창, PTY, 세션 등록, IPC, 휴대폰 화면 시작 |
| `electron/chatAgent.ts`        | 1,113 | Agent SDK 채팅 세션과 권한 중계           |
| `electron/campusServer.ts`     | 421   | 캠퍼스 소켓과 명령 검증                   |
| `electron/phoneServer.ts`      | 237   | 휴대폰 화면 HTTP 서버                     |
| `src/core/transcriptParser.ts` | 396   | JSONL 한 줄을 상태 변화로 바꿈            |
| `src/core/fileWatcher.ts`      | 131   | 파일 감시와 새 줄 읽기                    |
| `shared/protocol.ts`           | 856   | 호스트와 화면 사이 메시지 형식            |

줄 수는 `wc -l`로 세었고 `electron/*.ts` 전체는 9,090줄, `src/core/*.ts`는 1,804줄, `webview-ui/src`는 23,778줄이다.
`CLAUDE.md`는 1,173줄이다.

### 앱이 직접 띄운 세션만 추적한다

앱이 `claude --session-id` 또는 `--resume`으로 세션 식별자를 정해서 띄운다.
외부 터미널에서 따로 시작한 세션은 찾지 않는다(`CLAUDE.md`, `electron/main.ts`).
주된 신호는 `~/.claude/projects/<정리된 작업 경로>/<세션>.jsonl`을
`fs.watch`와 1초 주기 확인으로 읽는 것이다(`src/core/fileWatcher.ts`).
터미널 에이전트는 글만 쓴 턴의 끝을 5초 침묵으로, 권한 대기를 7초로 추측한다(`src/core/constants.ts`).
두 값은 `TEXT_IDLE_DELAY_MS = 5000`, `PERMISSION_TIMER_DELAY_MS = 7000`으로 직접 확인했다.
앱 안의 채팅 에이전트는 Agent SDK가 상태를 알려 주므로 추측이 필요 없다.

훅은 `Stop` 하나뿐이다.
`electron/hookSettings.ts`가 `~/.pixel-agents/hooks/<세션>.json`을 쓰고
`--settings <파일>`로 `claude`를 띄우며, 훅은 `campus idle`을 호출한다.
에이전트가 상태, 진행, 알림을 스스로 보고하는 캠퍼스 소켓도 있다.

### 캠퍼스 모델

`~/.pixel-agents/workspaces.json`에 작업 공간이 저장되고,
`CampusState`는 작업 공간마다 사무실 상태 하나를 갖고
에이전트는 자기 작업 공간 사무실의 좌석을 받는다.
캐릭터 상태는 `IDLE`, `WALK`, `TYPE`, `USE`이고 `isActive`가 이를 몬다.
화면은 2D 캔버스와 `requestAnimationFrame`이며 루프는 `webview-ui/src/office/engine/gameLoop.ts`에 있다.
`IDLE`, `WALK`, `TYPE`, `USE`의 정의는 `webview-ui/src/office/types.ts`에서 확인했고 `CampusState`는 `App.tsx`가 만든다.

### 통신과 설정

캠퍼스 소켓은 임시 디렉터리의 유닉스 소켓 위 HTTP이고 모드 0600, 본문 8KB 제한,
에이전트별 메모리 토큰을 `timingSafeEqual`로 비교한다.
소스 주석은 이것이 공격자가 아니라 사고를 막는 장치라고 말한다.
휴대폰 화면은 기본으로 꺼져 있고, 켜면 `0.0.0.0`의 4517번 포트에서
평문 HTTP로 읽기 전용 화면을 주며 토큰은 주소 `?t=`에 실린다.
앱은 `~/.pixel-agents/` 아래에 쓰고, `campus` 실행 파일을 담은 `bin/`을 에이전트의 PATH 앞에 둔다.
`~/.claude/settings.json`은 직접 고치지 않는다.
훅 설정은 `--settings`로 따로 넘기며, 사용자의 기존 Stop 훅과 합쳐져 함께 돈다고 `hookSettings.ts`의 주석이 설명한다.
권한 우회 설정은 저장되며 `--dangerously-skip-permissions`로 이어진다.

### 입력 신호에서 상태 판정까지

`src/core/fileWatcher.ts`는 감시를 세 겹으로 건다.
`fs.watch`가 주 수단이고, 1초 간격 `fs.watchFile`과 1초 간격 `setInterval`이 뒤를 받친다.
주석은 macOS에서 `fs.watch`가 이벤트를 놓칠 수 있다고 적는다.
`readNewLines`는 저장해 둔 오프셋 이후만 읽고, 파일이 줄어들었으면 오프셋을 0으로 되돌린다.
마지막 개행까지만 바이트 단위로 자른 뒤 디코딩하므로 UTF-8 다바이트 문자가 읽기 경계에서 깨지지 않는다.
새 줄이 들어오면 대기 타이머와 권한 타이머를 취소하고, 이미 띄운 권한 말풍선이 있으면 걷는다.

`src/core/transcriptParser.ts`는 레코드 종류로 가른다.
`tool_use` 블록이 있으면 활성 상태로 바꾸고 `agentToolStart`를 보낸다.
예외 도구가 아닌 도구가 하나라도 있으면 7초 권한 타이머를 시작한다.
예외는 하위 에이전트 도구와 `AskUserQuestion`이다.
7초 뒤에도 예외가 아닌 도구가 남아 있으면 권한 대기 가능성을 알린다.
도구 없이 글만 쓴 턴은 5초 침묵 타이머로 `waiting`을 추측하지만, SDK가 상태를 주는 채팅 에이전트(`hasSessionState`)에는 이 추측을 쓰지 않는다.
`system` 레코드의 `turn_duration`은 확실한 턴 종료로 취급되어 남은 도구 상태를 비우고 `waiting`으로 바꾼다.
도구 완료 표시는 `TOOL_DONE_DELAY_MS = 300`만큼 늦춘다.

### 터미널 에이전트 실행

`launchAgent`(`electron/main.ts`)는 세션 식별자를 `crypto.randomUUID()`로 만들고,
이어 가기면 `--resume <id>`, 아니면 `--session-id <id>`를 붙인 `claude` 명령을 로그인 셸의 PTY에서 돌린다.
`PATH` 앞에 `campus` 실행 파일 경로를 명령 안에서 덧붙이는데, 주석은 로그인 셸의 프로필이 `PATH`를 통째로 덮어쓸 수 있기 때문이라고 설명한다.
`--settings <훅 설정 파일>`이 붙고, 설정의 권한 우회가 켜져 있으면 `--dangerously-skip-permissions`도 붙는다.
에이전트별 환경 변수 `CAMPUS_SESSION`, `CAMPUS_TOKEN`, `CAMPUS_SOCKET`, `CAMPUS_BIN`이 이 프로세스에 전달된다(`campusEnvFor`).
`campus idle`을 받으면 대기 타이머를 취소하고 상태를 `waiting`으로 바꾼다.
5초 추측이 한 번 더 울려 같은 완료를 두 번 알리는 것을 막으려는 처리이다.

### 의존성과 네트워크

런타임 의존성은 `@anthropic-ai/claude-agent-sdk`, `node-pty`, `pngjs`, `zod`뿐이고 개발 의존성에 Electron 43, Vitest 4, TypeScript 5.9가 있다(`package.json`).
`postinstall`이 `electron-rebuild`를 실행하므로 설치만 해도 네이티브 모듈 빌드가 일어난다.
앱이 직접 여는 외부 주소는 업데이트 확인용 `https://api.github.com/repos/<저장소>/releases?per_page=10` 하나만 찾았다(`electron/updates.ts`).
이 확인은 10초 제한, 6시간 간격이며 실패하면 조용히 `null`을 돌려준다.
Agent SDK 자체가 어떤 서버와 통신하는지는 SDK 안의 일이어서 읽지 못했다.

## 분석

### 관찰 도구에서 작업 환경으로

원본 Pixel Agents가 VS Code 확장으로 이미 도는 세션을 보는 데 비해
Agent Campus는 VS Code 대상을 버리고 에이전트를 앱이 직접 소유한다.
다중 프로젝트 캠퍼스, 작업 보드, 작업 트리, 변경 보기와 PR, 비용 추적, 일정, 오케스트레이터,
휴대폰 화면이 붙었다.
소개 문구는 같은 로그인, 같은 설정, 같은 대화 기록의 진짜 Claude Code 세션이라고 설명하고
앱에서 시작해 터미널에서 이어 가는 것이 가능하다고 말한다.
이 문서는 터미널로 이어 가는 부분이 코드(`electron/main.ts`의 `--resume` 사용)와 맞는 것까지 확인했다.
앱이 쓰는 비용 기록은 `~/.pixel-agents/usage.jsonl`에 턴마다 한 줄씩 쌓이는 파일이다.

### 비용 표시의 의미

사이트는 모든 턴을 API 공개 가격으로 환산해 날짜별, 프로젝트별로 보여 준다고 하고,
구독 사용자에게는 청구액이 아니라 일을 얼마나 벌였는지의 척도라고 직접 적는다.
`electron/usage.ts`의 주석도 같은 말을 하며, 한 줄이 그 턴의 증분 비용이라고 정한다.
2026년 9월 1일 이전 기록은 누적값이 들어 있어 합계가 높게 읽힌다고 같은 주석이 인정한다.

## 비평

### 이름과 출처

Show HN 글의 이름은 옛 이름이어서 현재 저장소를 찾으려면 개명 안내 저장소를 거쳐야 한다.
원본과 이름이 같았던 데서 오는 혼란을 저자가 정리한 흔적이다.

### 설명과 코드의 차이

- 사이트의 층수, 벽 양식, 가구 수 같은 에셋 수치는 확인하지 못했다.
- Show HN 글에서 작성자 mateovalle은 포켓몬 같은 분위기를 겨냥했고
  에셋과 가구를 더 그릴 예정이라고 답했다.[^mateovalle]
  에셋이 아직 늘어나는 중이라는 뜻이며 이 문서는 현재 수량을 확인하지 못했다.
- 직접 시작한 터미널 세션은 추적하지 않는다.
- README는 CI가 검사를 돌린다고 하지만 `scripts/gate.sh`는 GitHub Actions가 꺼져 있다고 적는다.
  `.github/workflows/ci.yml`은 저장소에 있고 `main` 푸시와 풀 리퀘스트에 반응하는 `check` 잡을 정의한다.
  워크플로 파일이 있는 것과 실제로 켜져 있는 것은 별개이며, 켜짐 여부는 저장소 설정이어서 이 문서가 확인하지 못했다.
- Windows와 Linux는 같은 스크립트가 시험하지 않았다고 인정한다.
  `gate.sh`는 통과 메시지에 Windows와 Linux 미검증이라는 문구를 붙인다.
  주석은 이 두 플랫폼에서 경로 해석과 홈 디렉터리 오류가 실제로 두 번 나왔다고 적는다.

### 노출 면

주된 위험은 휴대폰 화면이다.
LAN에 평문 HTTP로 열리고 토큰이 주소에 있다.
화면은 읽기 전용이지만 작업 내용이 보인다.
`electron/phoneServer.ts`는 `/`와 `/api/status` 두 경로만 두고 `GET`과 `HEAD`만 받으며, 토큰 검사를 경로 판별보다 먼저 한다.
토큰은 `crypto.randomBytes(16)`의 16진수 문자열(128비트)이고 `tokenMatches`가 바이트 길이를 먼저 비교한 뒤 `timingSafeEqual`을 부른다.
주석에 따르면 이 길이 비교가 문자 수 기준이던 시절 한 번의 인증 없는 GET으로 프로세스가 죽는 버그가 있었다.
응답은 5초 간격으로 폴링되며 에이전트 이름, 사무실, 브랜치와 진행 중 활동 문구(`detail`)를 담는다.
페이지에는 `default-src 'none'` 기반의 CSP와 `Referrer-Policy: no-referrer`가 붙는다.
토큰은 `~/.pixel-agents/settings.json`에 평문으로 저장되고, 이 파일을 쓰는 `saveJsonFile`은 파일 모드를 따로 지정하지 않는다.
반면 캠퍼스 소켓은 명시적으로 `chmod 0600`을 하고 세션별 토큰을 `timingSafeEqual`로 비교한다.
소켓 요청은 알 수 없는 세션과 틀린 토큰에 같은 오류를 돌려주어 세션 존재 여부를 알아내지 못하게 한다.
소켓 쪽 한도는 본문 8KB, 클라이언트 2초 무응답 종료, 동시 연결 32개이다.
Electron 쪽은 컨텍스트 격리와 샌드박스를 켜 두었다.
확인한 값은 `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`이다(`electron/main.ts`).
`electron/preload.ts`는 메시지 전달, 키 입력, 터미널 크기 조절만 노출하고, 주석은 화면이 실행할 명령을 지정할 수 없다고 말한다.
창 밖으로 나가는 이동은 막고 `https://` 주소만 시스템 브라우저로 넘기며 새 창은 거부한다.

### 성숙도

`vitest`로 `it(`과 `test(`가 든 줄이 시험 파일에서 432개 나온다.
이전에 적은 약 517개는 다시 세어 재현되지 않아 고쳤다.
Electron 쪽 코드 9,090줄(`electron/main.ts` 한 파일이 3,451줄), 코어 1,804줄,
화면 2만 3천 줄, 1,173줄의 `CLAUDE.md`가 있다.
시험은 파일 감시, 대본 해석, 캠퍼스 소켓 인증, 휴대폰 서버 통합, 훅 설정 생성처럼 이 문서가 짚은 부분을 직접 겨냥한다.
`electron/__tests__/campusServer.test.ts`가 44개로 가장 많고, `authorizeCampus`의 틀린 토큰과 없는 세션 경우도 시험한다.
시험을 실제로 돌리지는 않았으므로 통과 여부는 확인하지 못했다.
1인 개발이고 변경 기록에 자체 점검 수정이 많다.
macOS 설치 파일은 아직 서명되지 않았다고 사이트가 알린다.

## 인사이트

### 가져갈 것

여러 프로젝트에서 에이전트를 동시에 돌리고 비용과 대기 상태를 한 화면에서 보고 싶다면
관찰 도구보다 작업 환경 쪽이 맞다.
그 대가로 에이전트를 이 앱이 띄워야 하며 이미 열린 터미널은 보이지 않는다.
휴대폰 화면은 켜기 전에 같은 네트워크의 신뢰 범위를 따져야 한다.

### 확인할 관찰

1. 외부 터미널 세션을 읽는 기능이 추가되는지.
2. Windows와 Linux에서의 실제 동작 보고.
3. 달러 환산 표시가 구독 사용자에게 어떻게 받아들여지는지.

위 셋 모두 이 문서가 확인하지 못했다.

---

[^mateovalle]: <https://news.ycombinator.com/item?id=49743563>
