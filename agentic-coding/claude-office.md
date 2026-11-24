# Claude Office

<https://github.com/W17ant/Claude-Office>

## 소개

Claude Office는 Claude Code 세션과 서브 에이전트를 아이소메트릭 픽셀아트 사무실로 보여 주는 로컬 앱이다.
저장소 설명은 “AI 에이전트가 실시간으로 일하는 모습을 보여 주는 픽셀아트 가상 사무실”이다.
MIT 라이선스에 TypeScript로 작성되었다.
2026년 11월 25일 GitHub API로 본 별은 413개이고 생성일은 2026년 3월 17일,
커밋은 116개이며 마지막 커밋은 2026년 11월 18일이다.
저장소에 별도의 홈페이지는 등록되어 있지 않다.

이 문서는 저장소를 받아 코드를 직접 읽고 썼다.
설치, 빌드, 서버 실행, 테스트 실행은 하지 않았고 읽기만 했다.
직접 읽은 파일은 `server/index.js`(5,099줄)의 인증·훅 이벤트·채팅·WebSocket 구간,
`hooks/agent-tracker.sh`와 `hooks/agent-tracker.py`, `hooks/install-hooks.sh`다.
`server/permissions.js`, `server/prompt-queue.js`, `server/config.js`,
`server/chat-db.js`, `server/lan.js`의 머리말과 `scripts/chat-ai-watcher.sh`도 읽었다.
화면 쪽은 `src/agentManager.ts`, `src/officeReducer.ts`의 상수와 휴식 판정,
`src/App.tsx`의 애니메이션 루프, `src/hooks/useAgentSocket.ts`의 상수를 읽었다.
`package.json`, `.github/workflows/ci.yml`, `tests/` 파일 목록과 각 파일의 `describe` 제목도 확인했다.
읽지 못했거나 일부만 읽은 곳은 아래 “확인하지 못한 것”에 모았다.

## 동작 방식

### 모듈 구성

| 경로                          | 줄 수 | 역할                                        |
| ----------------------------- | ----- | ------------------------------------------- |
| `hooks/agent-tracker.sh`      | 409   | 훅 진입점, 서명, POST, 권한 폴링, Stop 인계 |
| `hooks/agent-tracker.py`      | 1480  | 훅 payload를 이벤트로 변환, Bash 신호 분류  |
| `hooks/install-hooks.sh`      | 713   | 훅 23개와 상태 줄 등록, 백업, 제거          |
| `hooks/status-line.sh`        | 274   | 비용과 컨텍스트 값을 `POST /status`로 전달  |
| `hooks/office-relay.py`       | 126   | 다른 AI 도구의 훅 payload를 중계            |
| `server/index.js`             | 5099  | HTTP, WebSocket, 인증, 이벤트 처리 전체     |
| `server/permissions.js`       | 360   | 권한 창 대기열과 응답 증명                  |
| `server/prompt-queue.js`      | 242   | 채팅 프롬프트 대기열                        |
| `server/sessions.js`          | 593   | 세션 등록부 읽기                            |
| `server/tasks.js`             | 676   | 작업 목록과 팀 보드                         |
| `server/status.js`            | 469   | 비용, 토큰, 컨텍스트 미터                   |
| `server/chat-db.js`           | 241   | SQLite 채팅 기록                            |
| `server/lan.js`               | 630   | 폰 모드와 Tailscale 호스트 허용             |
| `src/officeReducer.ts`        | 2075  | 캐릭터 상태와 이벤트 반영                   |
| `src/App.tsx`                 | 1890  | 화면 조립과 애니메이션 루프                 |
| `src/hooks/useAgentSocket.ts` | 516   | WebSocket 연결과 재접속                     |
| `scripts/chat-ai-watcher.sh`  | 417   | 채팅 줄에 짧게 답하는 감시 스크립트         |
| `electron/main.cjs`           | 874   | 데스크톱 앱, 서버를 자식 프로세스로 실행    |

### 훅이 중심이고 서버가 상태를 가진다

설치 스크립트 `hooks/install-hooks.sh`가 Claude Code의 훅 이벤트 23개를 등록한다.
스크립트 안의 `EVENTS` 튜플을 세어 23개임을 확인했다.
`WorktreeCreate`는 일부러 뺐다.
이 이벤트에 명령 훅을 걸면 git의 워크트리 생성을 대신하게 되어 경로를 출력해야 하기 때문이라고 주석이 적는다.
이미 같은 훅이 있으면 경로만 현재 체크아웃으로 고치고, 중복 항목은 지운다.
플러그인과 이 훅이 함께 켜져 있으면 모든 이벤트가 두 번 도착한다고 경고를 출력한다.

훅은 `agent-tracker.sh`를 거쳐 `python3 -I agent-tracker.py`를 돌린다.
`-I` 옵션은 환경 변수와 현재 디렉터리를 파이썬 경로에서 뺀다.
Python은 이벤트 JSON, POST 서명, 대기 종류를 줄 단위로 출력하고 셸이 이를 읽는다.
이벤트는 `curl`로 `http://127.0.0.1:3334/event`에 보낸다.
일반 이벤트는 백그라운드로 보내며 `--max-time 1`이라 서버가 꺼져 있어도 훅이 막히지 않는다.
토큰이 없으면 서명 없이 보내고 서버는 401로 답하며, 훅은 이를 무시한다.

### 요청 서명

토큰은 명령줄 인자에 실리지 않는다.
토큰은 `~/.agent-office/auth-token`에서 읽어 환경 변수로만 파이썬에 넘긴다.
요청 본문은 `HMAC-SHA256(token, 메서드 + 줄바꿈 + 경로 + 줄바꿈 + 시각 + 줄바꿈 + 본문)`으로 서명한다.
서명과 밀리초 시각은 `X-Office-Timestamp`, `X-Office-Signature` 헤더로 간다.
서버의 `signatureValid`(`server/index.js`)는 시각이 ±60초(`SIGNATURE_WINDOW_MS`) 안일 때만 받고,
`timingSafeEqual`로 상수 시간 비교한다.
`hmac` 모듈 대신 `hashlib`로 직접 HMAC을 구현한 이유는 모듈 import에 훅 한 번당 약 5ms가 든다는 주석이다.
이 이유는 코드 주석이 적은 것이며 측정은 하지 않았다.

### 이벤트 종류

서버가 받는 이벤트 종류는 `KNOWN_EVENT_TYPES`에 22개다.
종류는 `agent_spawned`, `agent_started`, `agent_working`, `agent_completed`, `agent_linked`,
`mcp_call`, `mcp_done`, `session_started`, `session_ended`, `session_prompt`,
`session_turn_end`, `session_needs_you`, `session_tool_done`, `session_error`,
`session_compact`, `session_cwd`, `session_model`, `session_elicitation_done`,
`signal`, `task_created`, `task_completed`, `teammate_idle`이다.
목록에 없는 종류는 `Unknown event type`으로 거절한다.
본문은 `/event`만 64kb, 훅 중계(`/hook/:tool`)는 1mb, 나머지는 10kb까지 받는다.
한 이벤트에 붙는 신호는 최대 8개다(`MAX_SIGNALS_PER_EVENT`).

### 서브 에이전트 처리

서브 에이전트 처리는 `agent-tracker.py`에서 직접 확인했다.
`PreToolUse`에서 도구 이름이 `Agent`나 `Task`이면 `agent-<tool_use_id>`를 식별자로 `agent_spawned`를 만든다.
작업 설명은 80자로 자르고, 백그라운드 실행 여부는 `run_in_background`에서 읽는다.
서브 에이전트 안에서 다시 `Agent`를 호출하면 그 서브 에이전트의 `agent_id`가 `parentSubagentId`가 된다.
`SubagentStart`는 `agent_started`로 보내며 여기서 `agent_id`는 새로 생긴 서브 에이전트 자신이다.
서버는 `agent_spawned`와 `agent_started`를 도착 순서와 관계없이 `agent_type`으로 잇는다.
끝은 `SubagentStop`이 알리고, `TaskStop` 도구로 멈춘 백그라운드 에이전트는
`PostToolUse`의 `task_id`(없으면 `shell_id`)를 `taskId`로 보내 서버가 그 에이전트를 끝낸다.
`TaskStop`은 `SubagentStop`을 일으키지 않아서 이 경로가 따로 필요하다고 주석이 적는다.

### 팀 기능

팀 기능은 `TeammateIdle` 훅과 `~/.claude/teams`, `~/.claude/tasks`를 읽는 정도다.
`server/tasks.js`는 팀 설정 파일의 구성원 이름만 읽고 작업 디렉터리, 창 식별자, 시작 프롬프트는 버린다.
작업 목록 디렉터리는 `fs.watch`로 지켜보며, 쓰기가 가라앉은 뒤 250ms(`DEFAULT_DEBOUNCE_MS`) 지나 읽는다.
저자의 문서 `docs/reference.md`(180번째 줄)는 실제 팀으로는 돌려 보지 않았다고 적는다.
이 문장은 직접 확인했다.

### 보조 경로

훅 말고도 대화 기록(JSONL)을 읽는 `server/transcript.js`가 있다.
이 파일은 파일 끝 256KiB(`TAIL_BYTES`)만 읽고, 한 카드에 최대 8개 항목, 항목당 200자까지만 보여 준다.
경로는 절대 경로이고 `.jsonl`로 끝나며 `..` 구간이 없는 것만 연다(`isTranscriptPath`).
사고 블록(thinking)은 읽지 않는다.
`~/.claude/sessions`의 세션 등록부는 `server/sessions.js`가 읽는다.
훅이 없는 세션도 이 등록부로 찾아 회색 점선 알약으로 보여 주고,
프로세스 시작 시각까지 비교해 재부팅 뒤 남은 낡은 파일을 걸러 낸다.
훅이 있는 세션의 상태는 등록부가 덮어쓰지 않는다.
단 하나, 등록부 상태가 `waiting`에서 벗어나면 터미널에서 권한 창이 닫힌 것으로 보고 사무실의 권한 카드를 거둔다.
권한 창을 Esc로 닫으면 훅이 발생하지 않기 때문이다.

### 화면은 캔버스가 아니라 DOM과 CSS이다

사무실 장면은 캔버스, Pixi, three.js 어느 것으로도 그리지 않는다.
`package.json`에 렌더링 라이브러리는 React와 React DOM뿐이다.
미리 그려 둔 방 배경 이미지(`public/rooms/*.webp`) 위에 스프라이트 이미지를 절대 위치로 올린다.
`src/hat.ts`에 `document.createElement('canvas')`가 하나 있지만 장면이 아니라
스프라이트의 투명도를 읽어 머리 위치를 재서 모자를 얹는 용도다.
그림 없는 방의 미리보기는 `src/components/RoomBackdrop.tsx`가 인라인 SVG로 만든다.

`src/App.tsx`의 `requestAnimationFrame` 루프가 프레임 간격을 16.67ms 단위로 바꾼 `dt`(최대 3)를 만들어
`src/officeReducer.ts`의 `stepOffice`에 넘긴다.
리듀서가 바뀐 상태를 돌려 줄 때만 화면을 갱신한다.
이벤트와 걸음 단계가 겹쳐도 이벤트로 바뀐 상태를 덮어쓰지 않는다는 점은 `tests/officeReducer.test.ts`의 `animation tick composes with events` 묶음이 시험한다.

캐릭터의 상태는 대기, 매니저에게 걷기, 매니저와 대화, 책상으로 걷기, 일하기,
커피 휴식, 완료, 신입, 탈의실, 기다림이다(`src/types.ts`의 `AgentState`).
세션마다 따로 두는 “세션의 Claude”는 `working`, `waiting`, `idle`, `needs-you`, `error`, `compacting`의 `MainState`를 쓴다.

휴식과 잠의 조건은 다음과 같다.
책상에 20초(`BREAK_MIN_DESK_TIME`) 앉은 뒤 초당 0.008(`BREAK_CHANCE_PER_SEC`)의 확률로 8초(`BREAK_DURATION`) 쉰다.
확률은 매 프레임 `0.008 * (dt / 60)`로 계산해 프레임 속도와 무관하게 초당 값이 된다.
이 휴식은 서브 에이전트 같은 일꾼과 보스에게만 적용되고 세션의 Claude에게는 적용되지 않는다.
세션의 Claude는 턴 사이에 책상에서 존다고 `officeReducer.ts`가 적는다.
잠 말풍선은 휴식과 별개로 `idle` 상태가 30초를 넘으면 뜬다(`src/agentManager.ts`의 `getEffect`).
휴식 중 쉬는 사람이 물을 고르는 비율은 0.35다.

2시간 동안 소식이 없는 에이전트를 내보내는 것은 서버 쪽이다.
`server/index.js`의 `sweepStale`이 5분마다 돌며 `STALE_AGENT_MS`(기본 120분,
`AGENT_OFFICE_STALE_MINUTES`로 바꿈)가 넘은 에이전트를 완료 처리한다.
같은 기준으로 세션도 끝내지만 등록부에 살아 있는 프로세스가 있는 세션은 건너뛴다.
MCP 호출 기록은 따로 5분(`MCP_STALE_MS`)이 지나면 버린다.

### 서버와 설정

서버는 `127.0.0.1`에만 바인딩된다(`server/config.js`의 `readHost`).
`AGENT_OFFICE_HOST`에 `localhost`는 허용하되 같은 `127.0.0.1`로 묶고, `::1`과 그 밖의 주소는 이유를 로그에 남기고 거절한다.
거절 이유는 열린 경로들이 토큰 없이 도는 구조라 비루프백 바인딩이 프롬프트와 응답을 네트워크에 드러내기 때문이라고 주석이 적는다.
기본 포트는 3334(서버와 빌드된 화면)이고 개발용 Vite는 3333이다.

토큰은 `~/.agent-office/auth-token`에 저장된다.
32바이트 난수를 16진수 64자로 쓰며, 기존 파일은 소유자가 같고 권한 비트에 그룹·기타가 없고 심볼릭 링크가 아닐 때만 재사용한다(`readTokenFile`).
새로 쓸 때는 지운 뒤 `wx` 플래그로 모드 0600 파일을 만든다.
런타임 디렉터리는 0700으로, `chat.db`와 `-wal`, `-shm`은 0600으로 매번 시작할 때 고친다.
Host 헤더는 루프백 이름이어야 하며(421), Origin은 루프백 호스트의 3333, 3334, 설정한 UI 포트만 허용한다(403).
DNS 리바인딩 방어를 위한 것이라고 주석이 적는다.

WebSocket은 핸드셰이크의 `Sec-WebSocket-Protocol`에 토큰을 실어 보낸다.
토큰이 맞으면 신뢰 연결이고 전체 스냅샷과 UI 토큰을 받는다.
토큰이 없거나 틀리면 거절하지 않고 읽기 전용으로 열어, 대화 본문과 권한 창의 명령줄을 뺀 이벤트만 보낸다(`redactForReadOnly`).
UI 토큰은 프로세스마다 새로 만드는 24바이트 난수이며 메모리에만 있다.

`~/.claude/settings.json`에는 훅 23개와 `statusLine`, `subagentStatusLine`이 들어간다.
기존 상태 줄은 `~/.agent-office/statusline-prev`에 저장해 두고 그 출력을 그대로 보여 주는 식으로 연결해 쓴다.
설치 전에는 설정 파일의 백업을 만들고, JSON 병합이 실패하면 백업 경로를 알리고 끝낸다.
`--uninstall`로 훅과 상태 줄을 따로 또는 함께 걷어 낼 수 있다.

서버로 가는 내용의 한도는 코드에서 직접 확인했다.
프롬프트와 응답은 각각 2,000자(`clamp(prompt, 2000)`, `clamp(last_assistant_message, 2000)`),
상태 문구에 들어가는 Bash 명령은 앞 60자,
권한 요청의 도구 입력은 400자(`permission_detail`), 요약은 120자, 제안은 4개까지다.
저장은 `logPrompts` 설정이 정한다.
`off`는 0자, `summary`(기본값)는 200자, `full`은 2,000자다.

### 데이터 저장

모든 파일은 `~/.agent-office`(또는 `AGENT_OFFICE_HOME`)에 둔다.
`agents.json`은 에이전트와 세션을 담아 이벤트마다 통째로 다시 쓴다.
`chat.db`는 `better-sqlite3`의 WAL 모드 SQLite이며 메시지 표에 보낸 이, 역할, 본문, 시각, 시스템 여부, 반응, 확인 여부를 둔다.
재시작하면 `agents.json`에서 `STALE_AGENT_MS`보다 오래된 에이전트를 빼고 복원한다.
설정(`logPrompts`, `answerPermissions`, `notifyPermissions`, `language`)은 `settings.json`에 있다.

### 의존성

런타임 의존성은 `better-sqlite3`, `electron-updater`, `express`, `qrcode-terminal`, `ws` 다섯 개다.
Node 22 이상이 필요하다(`engines`).
React, Vite, Vitest, TypeScript, Electron은 개발 의존성이다.
훅은 파이썬 표준 라이브러리만 쓴다고 파일 머리말이 적는다.

## 분석

### 읽기 도구를 넘어 쓰기 도구가 되었다

Pixel Agents가 신호를 받아 보여 주기만 하는 데 비해
Claude Office는 Claude Code 쪽으로 되돌아 쓴다.
되돌아 쓰는 경로는 두 개이고 둘 다 코드에서 확인했다.

첫째는 권한 요청이다.
`PermissionRequest` 훅은 `~/.agent-office/answer-permissions` 표시 파일이 있을 때만 서버에 보내고 응답을 기다린다.
이 파일은 `answerPermissions` 설정(기본값 켜짐)을 서버가 따라 만든다.
서버는 대기 중인 권한을 만들어 `permissionId`를 돌려주고, 훅은 `GET /permission/:id`를 최대 40번 길게 폴링한다.
화면에서 누르면 `POST /permission/:id`에 `allow`, `allow-remember`, `deny` 중 하나를 보낸다.
이 호출은 UI 토큰이나 파일 토큰이 있어야 한다.
훅은 결정 단어만 받고 출력 JSON은 스스로 만든다.
받은 응답이 `HMAC(token, nonce + permissionId + decision)` 증명과 맞을 때만 출력한다.
nonce는 훅이 이벤트마다 만든 난수라서 포트를 가로챈 프로세스는 위조하지 못한다.
`allow-remember`는 Claude Code가 준 `permission_suggestions`를 그대로 되돌려 보낼 뿐 서버가 만든 규칙은 싣지 않고, `updatedInput`도 싣지 않는다.
거부 메시지는 고정 문구이고 `interrupt`는 거짓이다.

대기에는 시한이 있다.
세션이 터미널에서 대화형인지 모르는 동안은 15초(`PERMISSION_WAIT_MS`) 뒤 만료된다.
`claude -p` 같은 비대화형 실행은 훅이 끝나는 순간 자동 거부하기 때문이다.
알림 이벤트가 한 번이라도 오면 대화형으로 보고 최대 10분(`PERMISSION_WAIT_MAX_MS`)까지 늘린다.
터미널에서 먼저 답하면 이후 도구 호출, 턴 종료, 새 요청, 세션 종료, 등록부의 `waiting` 이탈 등으로 대기를 풀어 사무실의 늦은 클릭은 409를 받는다.
터미널이 언제나 이기게 설계했다는 것이 `server/permissions.js` 머리말의 설명이다.

둘째는 채팅 프롬프트다.
채팅에서 `@세션이름 내용`으로 쓰면 서버가 그 세션을 찾아 `server/prompt-queue.js`에 쌓는다.
세션당 5개(`MAX_QUEUED_PER_SESSION`), 2,000자, 1시간(`PROMPT_TTL_MS`) 안에 전달되지 않으면 만료된다.
대기열은 메모리에만 있어서 서버가 재시작하면 사라진다.
오래 지난 프롬프트가 엉뚱한 상황에 실행되지 않게 하려는 의도라고 주석이 적는다.
대기열이 비어 있지 않은 세션에는 표시 파일이 생기고, `Stop` 훅이 그 파일을 확인하면 이벤트를 포그라운드로 보내 nonce를 붙인다.
서버가 증명을 달아 프롬프트를 내주면 훅은 `{"decision": "block", "reason": ...}`를 출력해 Claude가 멈추지 않고 그 프롬프트를 다음 지시로 이어 가게 한다.
쓸 수 있는 호출자는 UI 토큰이나 파일 토큰이 있는 쪽뿐이고, 폰 접속과 프록시 이름으로 들어온 요청, 훅이 없는 세션은 거절한다(`mayQueuePrompt`).
한계도 코드에 적혀 있다.
프롬프트 입력창에서 쉬는 세션은 훅이 돌지 않으므로 다음 턴이 끝날 때까지 전달되지 않는다.

채팅 패널의 일반 대화는 이와 별개의 경로다.
`scripts/chat-ai-watcher.sh`가 8초마다 서버를 읽어 사람이 쓴 줄에만 `claude -p`로 답한다.
옵션은 `--max-turns 1 --safe-mode --strict-mcp-config --tools "" --no-session-persistence --name agent-office-bot`이다.
이 옵션이 훅, `CLAUDE.md`, MCP, 스킬, 플러그인을 모두 끄고 도구도 없앤다.
기본 모델은 `claude-haiku-5-5`, 시간 제한은 60초, 분당 답 5개 상한이 있다.
답은 15단어(한중일 글자는 40자)로 잘리는 페르소나 대사다.
프롬프트에는 `scripts/gather-context.sh`가 모은 git 브랜치, 마지막 커밋 제목, 바뀐 파일 3개와 에이전트 5명의 이름·역할·작업 40자가 들어간다.
따라서 이 경로는 사용자 질문에 답하는 도구라기보다 사무실 분위기를 내는 대사 생성기다.

### 서버가 상태를 가진 구조

화면은 서버가 보낸 상태를 그리는 껍데기이고
캐릭터의 상태 전이는 클라이언트 리듀서가 시간으로 돌린다.
훅이 먼저이고 대화 기록은 보조라서 대화 기록 형식이 바뀌어도 핵심 경로는 영향이 작다.
`server/transcript.js`는 형식이 달라져도 항목이 줄 뿐 오류를 내지 않게 방어적으로 쓰여 있다고 머리말이 적는다.
재접속은 `src/hooks/useAgentSocket.ts`가 500ms에서 시작해 두 배씩 늘려 최대 30초까지 기다린다.
연결이 5초 이상 열려 있거나 스냅샷을 받아야 간격을 되돌려, 열자마자 닫는 서버를 두드리지 않는다.

### 다른 AI 도구

Codex, Gemini CLI, OpenCode, Antigravity, Kimi용 중계가 `hooks/office-relay.py`와 `server/tools/`에 있다.
중계는 payload를 그대로 `/hook/<tool>`에 서명해 보내고 서버의 번역 모듈이 이벤트로 바꾼다.
필드 이름이 틀려도 재설치 없이 서버 갱신만으로 고친다는 설계다.
루프백 주소만 쓰며 `AGENT_OFFICE_EVENT_URL`은 무시한다.
README와 `docs/reference.md`는 다섯 도구 모두 실험적이고 실제 세션이 아닌 문서와 포크의 payload에 근거한다고 적는다.

## 비평

### 설명과 코드의 차이

- README는 실시간 화면이 3333번 포트라고 적지만 그 포트는 Vite 개발 서버이고
  빌드된 화면은 3334번에서 제공된다.
  `server/config.js`의 `DEFAULT_PORT`가 3334, `DEFAULT_UI_PORT`가 3333이고 Origin 허용 목록도 둘 다 받는다.
- `scripts/generate-office-bg.mjs`는 `replicate`와 `dotenv`를 import한다.
  `package.json`의 직접 의존성에 둘 다 없다.
  `package-lock.json`에는 `replicate`가 아예 없고, `dotenv`는 `dev: true`로 다른 개발 패키지의 하위 의존성으로만 있다.
  이 스크립트는 `files` 목록에도 없어 배포 패키지에 들어가지 않는다.
- 새 훅과 팀 보드는 저자도 실제 시험하지 못했다고 밝힌다.
  `docs/reference.md`가 팀 보드는 문서와 Claude Code 2.1.321 바이너리를 보고 만들었고 실제 팀으로 돌려 보지 않았다고 적는다.
  다른 AI 도구용 훅에는 실험적이라는 표시가 있다.
- 테스트 수 “972개”라는 README의 주장은 이 문서가 실행으로 확인하지 못했다.
  다만 정적으로 세면 `tests/`에 `*.test.ts` 파일이 85개이고 `it(`·`test(`로 시작하는 줄이 1,713개다.
  `tests/` 안의 항목은 88개이며 테스트 85개에 `helpers.ts`, `hook-smoke.mjs`, `fixtures` 폴더가 더해진 수다.
  README의 972는 최신이 아닌 수치로 보이며, 이는 추정이다.
  `CHANGELOG.md`에서는 972를 찾지 못했다.

### 전달되는 내용의 범위

프롬프트와 응답 일부가 로컬 서버로 간다.
저장되는 프롬프트 글은 기본이 200자 요약(`logPrompts: summary`)이다.
이 값은 `server/index.js`에서 `settings.logPrompts`의 초깃값으로 확인했다.
서버는 루프백에만 열려 있고, 이제 열린 경로와 토큰 경로를 코드에서 직접 확인했다.

| 구분                   | 경로                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 파일 토큰 필수         | `POST /event`, `/hook/:tool`, `/chat/reply`, `/a2a`, `/chat/seen`, `/chat/react`, `/chat/video-mode`, `GET /permission/:id`, `POST /status` |
| UI 토큰 또는 파일 토큰 | `POST /permission/:id`, `POST /settings`, `@세션` 프롬프트                                                                                  |
| 열림                   | 대부분의 GET, `POST /chat`의 일반 줄, `/chat/typing`, `/chat/cron-state`                                                                    |

열린 GET이라도 대화 본문은 토큰이 있어야 나온다.
`GET /chat`은 토큰 없이는 프롬프트·응답 행을 걸러 내고,
`GET /sessions`는 `main`의 마지막 프롬프트·응답 글을 빼고,
`GET /signals`는 명령과 출력을 뺀다.
`GET /agents`, `GET /roster`는 에이전트의 작업 문구와 MCP 서버 이름을 토큰 없이 보여 준다고 코드 주석이 밝힌다.
`POST /chat`은 일반 줄에는 토큰이 필요 없고, `/clear` 같은 파괴적 슬래시 명령과 `@세션` 프롬프트에만 토큰이 필요하다.
`/clear`는 `PRIVILEGED_COMMANDS`에 있고 토큰이 없으면 401과 함께 채팅에 이유를 남긴다.
정리하면 몇몇 GET과 `POST /chat`의 일반 줄은 토큰 없이 열려 있고, 그 범위를 코드로 확인했다.

`tests/hardening.test.ts`와 `tests/ws-auth.test.ts`는 이 경계를 시험한다.
`hardening`에는 토큰 필수 경로, 슬래시 명령, 상수 시간 비교, 토큰 파일 권한, 서명 요청, Host 헤더 방어, 런타임 파일 권한, 오류 응답에 스택이나 경로가 없음이 `describe`로 나뉘어 있다.
`ws-auth`는 핸드셰이크의 신뢰·읽기 전용 구분과 토큰 파일 재사용, 시작 때 출력하는 링크를 다룬다.
이 시험 묶음의 통과 여부는 실행하지 않아 모른다.

### 보안상 표면

- 루프백 바인딩이 기본이지만 옵트인 예외가 셋 있다(`server/lan.js` 머리말).
  `AGENT_OFFICE_LAN=1`은 사설 LAN 주소의 3335번에 보기 전용 두 번째 리스너를 연다.
  `AGENT_OFFICE_LAN=full`은 같은 자리에서 HTTPS만 열고 폰 비밀 값이 있는 기기에 노선 허용 목록의 경로를 연다.
  `AGENT_OFFICE_ALLOWED_HOSTS`는 `tailscale serve` 같은 HTTPS 프록시의 호스트 이름을 루프백 리스너가 받게 한다.
  Tailscale Funnel 요청은 `Tailscale-Funnel-Request` 헤더를 보고 403으로 거절한다.
  “서버는 `127.0.0.1`에만 열린다”는 기본 설정에 대한 서술이며 이 옵션들을 켜면 달라진다.
- `server/index.js`가 외부 명령을 실행하는 곳은 `execFile('bash', [notify.sh, 제목, 내용])` 하나다.
  `server/sessions.js`는 프로세스 시작 시각을 비교하려고 `ps`를 `execFileSync`로 부른다.
  `notify.sh`는 텍스트를 AppleScript 소스에 끼우지 않고 `osascript`의 `argv` 항목으로 넘겨, 따옴표나 줄바꿈이 코드가 되지 않게 한다.
  `server`, `hooks/*.py`, `cli`, `electron/*.cjs`에서 `eval`, `new Function`, `shell: true`는 찾지 못했다.
- 훅이 서버의 답을 믿는 범위가 좁다.
  권한은 결정 단어와 증명이 맞을 때만, 프롬프트 인계는 증명이 맞을 때만 출력하며 출력 JSON은 항상 훅이 만든다.

## 인사이트

### 가져갈 것

세션이 여럿일 때 누가 사용자를 기다리는지 알려 주는 화면이 목적이라면
훅 기반으로 서버가 상태를 가지는 구조가 대화 기록 읽기보다 단순하다.
다만 화면에서 권한을 대신 답하는 기능은 켜기 전에 무엇이 허용되는지 확인해야 한다.
관찰용으로만 쓰려면 `answerPermissions`와 채팅 기능을 꺼 두는 쪽이 안전하다.
`answerPermissions`를 끄면 서버가 표시 파일을 지우고, 훅은 그 파일이 없으면 서버에 응답을 기다리지 않는다.
채팅 쪽에서는 `@세션` 프롬프트가 UI 토큰 소유자에게만 열려 있다.
일반 대화 답변을 끄려면 `scripts/chat-ai-watcher.sh`를 띄우지 않으면 된다는 점이 `scripts/start-office.sh`에서 이 스크립트를 시작한다는 사실에서 따라온다.
이 마지막 문장은 시작 스크립트의 한 줄만 읽고 이은 추론이다.

### 확인할 관찰

1. 팀 기능이 실제 에이전트 팀에서 작동하는지.
2. 권한 응답 기능의 오작동 사례가 보고되는지.
3. Claude Code의 훅 사양이 바뀔 때 설치 스크립트가 어떻게 따라가는지.

위 셋 모두 이 문서가 확인하지 못했다.

### 확인하지 못한 것

- 테스트와 빌드를 실행하지 않아 통과 여부와 실제 테스트 수를 모른다.
- `server/index.js`의 `processEvent` 전체와 `server/tasks.js`, `server/status.js`, `server/lan.js`의 본문은 머리말과 일부 구간만 읽었다.
- `src/officeReducer.ts`의 걷기·좌석 배정·방 이동 로직과 Electron 자동 업데이트(`electron/*.cjs`)는 읽지 못했다.
- LAN 전체 모드의 인증서 생성(`server/lan-cert.js`)과 폰 비밀 값 절차는 읽지 못했다.
- 훅 이벤트별 실제 Claude Code payload가 파일 주석의 captured 2.1.300 설명과 같은지는 확인하지 못했다.
