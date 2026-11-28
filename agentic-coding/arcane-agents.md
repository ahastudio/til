# Arcane Agents

<https://github.com/thomasrice/arcane-agents>

HN 토론: <https://news.ycombinator.com/item?id=47265928> (4점, 3개 댓글)

## 소개

Arcane Agents는 터미널 AI 에이전트를 픽셀아트 지도 위의 캐릭터로 보여 주고
실제 tmux 터미널을 브라우저 패널에 이어 주는 로컬 앱이다.
저장소 설명은 “터미널 AI 에이전트를 위한 시각적 관제실”이다.
MIT 라이선스에 TypeScript이고 npm 버전은 1.3.1이다.
2026년 11월 25일 GitHub API로 본 별은 12개, 생성일은 2026년 3월 3일이고
커밋은 약 177개, 마지막 커밋은 10월 7일이다.
Show HN으로 올라왔다.
별도 홈페이지는 등록되어 있지 않다.

저장소를 받아 코드를 읽었으며 설치하거나 실행하지 않았다.
서브 에이전트가 먼저 코드를 분석했고, 이후 핵심 파일을 직접 읽어 그 보고를 확인하거나 고쳤다.
아래 코드 근거는 파일 경로로 적었다.
읽기만 했으므로 실제 동작을 시험한 것은 아니다.

## 동작 방식

### 모듈 구성

| 경로                                   | 역할                                           |
| -------------------------------------- | ---------------------------------------------- |
| `server/bootstrapApp.ts`, `bootstrap/` | 시작, HTTP와 WebSocket 연결, 종료 처리         |
| `server/http/`                         | 라우트 19개, zod 입력 검증, 오류 응답          |
| `server/orchestrator/`                 | 띄우기, 중지, 재시작, 입양, 위치와 아바타 배정 |
| `server/tmux/`                         | tmux 호출 모음과 attach 명령 조립              |
| `server/status/`                       | 신호 수집, 어댑터, 판정, 대화 기록 추적        |
| `server/ws/`                           | 실시간 이벤트 허브, 터미널 브리지              |
| `server/persistence/`                  | SQLite 저장소                                  |
| `server/config/`, `cli/`               | 설정 읽기, 프로젝트 탐색, 명령어               |
| `client/`                              | React 화면, 지도 렌더링, 단축키, 상태 저장소   |

### 에이전트를 직접 띄우고 소유한다

각 에이전트는 자기 tmux 서버에서 돈다(`tmux -L arcane-agents ...`, `tmuxAdapter.ts`).
`OrchestratorService.spawn`(`orchestrator/orchestratorService.ts`)이 8자 nanoid를 에이전트 번호로 만든다.
창 이름은 프로젝트 약칭, 런타임, 번호 앞 4자를 `[a-z0-9-]`로 정리해 이은 것이다(`spawn/windowName.ts`).
명령은 토큰마다 `shellQuote`로 감싸 한 줄로 만들고 `tmux new-window`에 넘긴다.
이때 환경 변수 `ARCANE_AGENTS_WORKER_ID`를 `-e`로 함께 준다.
Claude의 경우 사용자 명령에 `--session-id <uuid>`를 덧붙인다.
런타임 ID나 실행 파일 이름에 claude가 들어 있고 이미 `--session-id`가 없을 때만 붙는다(`spawn/command.ts`).

창에는 `@arcane_agents_*` 옵션으로 에이전트 번호, 프로젝트, 런타임, 경로를 적어 둔다.
서버를 다시 켜면 이 값으로 창을 찾아 저장된 기록과 맞춘다(`reconcile/planReconciliation.ts`).
기록이 없는 관리 대상 창은 새 에이전트로 받아들이고 클라이언트에 알린다(`bootstrap/serverContext.ts`).
`bootstrap/shutdown.ts`에는 tmux를 다루는 코드가 없다.
서버를 끄면 연결과 데이터베이스만 닫고, 제한 시간은 기본 2초이며 tmux 창은 그대로 남는다.
중지는 `C-c`를 보내고 220ms 뒤에 `kill-window`를 하는 방식이다.

브라우저 터미널은 `node-pty`로 `tmux attach`를 실행해 `xterm.js`에 이어 준다.
`ws/terminalBridge.ts`는 첫 resize 메시지가 와야 pty를 연다.
크기는 최소 20열 5행으로 맞춘다.
attach 때마다 `arcane-view-<uuid>` 세션을 새로 만들고 대상 창을 `link-window`로 이어 붙인다.
그 세션은 상태줄과 prefix 키를 끈다(`buildTmuxAttachArgs`).
그래서 브라우저 화면이 다른 에이전트의 창으로 넘어갈 수 없다.
pty는 서버 프로세스의 환경 변수를 모두 물려받고 `TERM`만 덮어쓴다.

여러 줄 입력은 `ESC[200~`와 `ESC[201~`로 감싼 `send-keys -l` 뒤에 Enter를 보낸다.
한 줄은 `send-keys -l`로 보낸 뒤 Enter를 누른다(`sendInput`).

### 상태는 폴링으로 추측한다

에이전트 훅을 쓰지 않는다.
`src/server` 전체에서 훅, `settings.json`, `PreToolUse` 같은 이름을 검색했으나 해당하는 코드가 나오지 않았다.
상태 입력은 모두 tmux 화면, 프로세스 목록, Claude 대화 기록 파일이다.
`StatusMonitor.start`(`statusMonitor.ts`)가 `setInterval`로 폴링을 돌린다.
간격은 설정 `backend.tmux.pollIntervalMs`이고 기본값은 2500, 최솟값은 250이다(`config/schema.ts`).
터미널에 입력이 들어가거나 출력이 나오면 간격을 기다리지 않고 35ms 또는 20ms 뒤에 추가 폴링을 요청한다.
폴링이 진행 중이면 겹쳐 돌리지 않고 끝난 뒤 한 번 더 돌린다(`pollOnce`).
에이전트별 평가는 기본 4개씩 병렬이며 환경 변수 `ARCANE_AGENTS_STATUS_POLL_CONCURRENCY`로 최대 32까지 올린다.

한 번의 평가에서 `collectSignals.ts`가 다음을 모은다.

- `tmux capture-pane`으로 화면 글, 줄 수는 Claude 60, 일반 어댑터 35, 나머지 420이다.
- 창의 명령, 프로세스 번호, 죽었는지 여부
- `pgrep -P`와 `ps`로 셸 아래의 에이전트 프로세스 탐색
- 각 TUI 화면의 정규식 일치(Claude, Codex, OpenCode, omp, 일반 예비 어댑터)

화면 글은 `paneObservation.ts`가 마지막 40개 비어 있지 않은 줄의 요약으로 바뀌었는지 본다.
바뀐 시각이 `outputQuietForMs`의 기준이 된다.
처음 보는 창은 30초 전에 바뀐 것으로 시작한다.

런타임 어댑터는 `resolveRuntimeAdapter`(`runtimes/adapter.ts`)가 고른다.
확실한 근거(런타임 ID, 하위 프로세스, 앞에 떠 있는 명령)를 Claude, OpenCode, Codex, omp 순으로 먼저 본다.
없으면 화면 글에서 각 어댑터의 신호를 찾는다.
Codex도 Claude와 같은 글머리 기호를 쓰므로, Claude는 다른 런타임 신호가 없을 때만 이긴다.
그래도 없으면 설정한 프롬프트 서명의 런타임, 마지막으로 일반 어댑터를 쓴다.
하위 프로세스 분류는 `ps`의 명령과 인자를 합친 문자열에 `\bclaude(?:-code)?\b`, `\bcodex\b`, `\bomp\b`를 적용한다(`runtimeProcess.ts`).
OpenCode는 `opencode`가 문자열 어디에든 들어 있으면 일치한다.
이 분류는 앞에 떠 있는 명령이 `bash`, `zsh`, `sh`이거나 `node`, `bun`, `deno`, `python`, `python3`일 때만 돈다.
셸 아래를 내려가는 깊이는 최대 5단계이다.

### 판정 순서와 시간값

판정은 `decide.ts`의 `deriveWorkerStatusDecision`이 위에서 아래로 처음 맞는 조건에서 끝난다.
상태는 `idle`, `working`, `attention`, `error`, `stopped` 다섯 가지이다(`shared/types.ts`).

| 순서 | 조건                                    | 결과(확신도)        |
| ---- | --------------------------------------- | ------------------- |
| 1    | 사용자 정의 규칙 일치                   | 규칙이 정한 상태(1) |
| 2    | 대화 기록이 attention                   | attention(0.96)     |
| 3    | Claude, Codex, omp의 질문 대기 화면     | attention(0.96)     |
| 4    | Codex 승인 대화상자                     | attention(0.94)     |
| 5    | 일반 파서가 입력 요구를 인식            | attention(0.9)      |
| 6    | 대화 기록이 error                       | error(0.92)         |
| 7    | 15초 안의 치명적 오류 글                | error(0.87)         |
| 8    | 프롬프트가 지배하는 화면                | idle(0.9)           |
| 9    | 셸 명령, 시작 유예, 오래된 출력         | idle(0.86)          |
| 10   | 강한 작업 증거                          | working(0.88)       |
| 11   | 마지막 출력 3.5초 안의 이전 working     | working(0.66)       |
| 12   | 약한 증거와 신선도 창 안의 이전 working | working(0.62)       |
| 13   | 약한 증거와 명령 변경 2.25초 안         | working(0.56)       |
| 14   | 그 밖                                   | idle(0.74)          |

3, 4, 5, 7번은 설정의 `interactiveCommands`에 든 명령에서는 건너뛴다.
시간 상수는 `decide.ts`에 있다.
파서 작업 증거 8초, 최근 오류 15초, 명령 워밍업 2.25초, 끈끈한 working 3.5초, 캐시된 활동 12초이다.
출력이 조용해도 working으로 남는 신선도 창은 Claude, Codex, omp가 10초, OpenCode가 12초, 일반이 20초이다.
설정의 런타임별 `freshnessWindowMs`가 이 값을 덮어쓴다.
Claude, OpenCode, Codex는 띄운 뒤 5초 동안 활성 신호가 없으면 idle로 둔다.

에이전트 런타임은 화면의 도구 이름 글자(`Read`, `git` 등)만으로는 working이 되지 않는다.
주석에 따르면 이 단어들이 작업이 끝난 뒤에도 몇 초간 화면에 남아 거짓 working을 만들었기 때문이다.
working 근거는 어댑터의 활성 신호, Claude 작업 요약과 진행 표시, 대화 기록, 하위 프로세스이다.
일반 셸 작업에만 파서가 읽은 도구와 경로가 working 근거로 쓰인다.
하위 프로세스는 Claude, Codex, omp가 프롬프트에서 쉬고 있으면 근거에서 뺀다.

### Claude 대화 기록 묶기

Claude는 화면 글에 더해 대화 기록 파일(`.jsonl`)을 읽는다.
`ClaudeTranscriptTracker.poll`(`claudeTranscriptTracker.ts`)이 에이전트마다 파일 하나를 정해 읽는다.
파일을 정하는 순서는 `resolveTranscriptPath`(`claudeTranscript/io.ts`)에 있다.

1. 이미 묶은 파일이 아직 있으면 그대로 쓴다.
2. 실행 중인 Claude의 명령줄에서 읽은 세션 ID, `/proc/<pid>/cmdline`을 쓴다.
3. 서버가 붙인 `--session-id`로 만든 `<id>.jsonl`이 있으면 쓴다.
4. Claude가 임시 폴더에 만드는 세션 디렉터리의 생성 시각이 프로세스 시작과 10초 안이면 쓴다.
5. 프로세스 시작 시각을 알면 첫 기록 시각이 가장 가까운 파일을 쓴다. 맞는 파일이 없으면 아무것도 묶지 않는다.
6. 시작 시각을 아직 모르면 수정 시각이 가장 최근인 후보를 약하게 묶는다. 첫 기록이 에이전트 생성 2분 전보다 늦고 10분 안이어야 한다.
7. 마지막으로 화면이 바뀐 폴링에서 수정 시각이 5초 안인 후보 하나가 연속 3번 따라 움직이면 약하게 묶는다.

한 파일은 한 에이전트에게만 묶인다.
강한 근거(2, 3, 4, 5번)가 약한 근거(6, 7번)를 밀어낸다.
후보는 3일 안에 수정된 파일이고, 처음에는 끝부분 196,608바이트만 읽는다(`claudeTranscript/constants.ts`).
대화 기록의 판정은 `claudeTranscript/snapshot.ts`에 있다.
`AskUserQuestion` 도구가 진행 중이면 attention이다.
진행 중인 도구가 있거나 마지막 텍스트 이후 5초가 지나지 않았으면 working이다.
진행 중인 도구는 기록이 45초 동안 조용하면 모두 버린다.
약하게 묶인 기록이 working이라고 해도 화면이 신선도 창보다 오래 조용하면 믿지 않는다(`hasTrustedTranscriptWorkingSignal`).
세션 시작 시각 조회가 실패하면 15초 뒤 다시 시도한다.

### 화면과 서버

Canvas 2D와 하나의 `requestAnimationFrame` 루프이다(`client/map/runtime/useMapRuntime.ts`).
캐릭터 그림은 걷기, 일하기, 대기 세 가지이다(`workerLayer.ts`).
걷기는 위치가 0.3보다 크게 바뀐 뒤 450ms 동안이다(`workerVisualState.ts`).
일하기는 상태가 working일 때이다.
working, attention, error일 때는 캐릭터 위에 활동 배지가 뜬다.
배지는 `activityText`를 최대 64자로 자르고, 글이 없으면 `READ`, `RUN`, `ERR` 같은 약어를 쓴다.
attention 이름표는 주기 1700ms로 맥동하고 완료 대기 이름표는 금색 반짝임이다.
error는 이름표가 바뀌지 않고 배지 글로만 나타난다.
READY는 서버가 기록한다.
`WorkerRepository.updateStatus`가 working에서 idle로 바뀌면 `completedAt`을 적는다.
이 기록은 소리를 끈 에이전트에는 남기지 않는다.
사용자가 그 터미널을 열면 클라이언트가 `completion-reviewed`를 호출해 검토 시각을 적는다.
브라우저가 꺼져 있던 동안 끝난 작업도 READY로 남는다.

캐릭터는 기본값 `hold`에서는 사용자가 놓은 자리에 가만히 있다.
에이전트마다 `wander`로 바꿀 수 있고 이 경우 클라이언트가 스스로 돌아다닌다.
돌아다니기는 쉬는 시간 2~5초, 이동 시간 1~2초이다(`movementSimulation.ts`).
위치는 서버에 저장된다.
서버는 Express와 `ws`로 `127.0.0.1:7600`에 기본으로 열린다.
주소와 포트는 설정 `server.host`, `server.port`이거나 환경 변수 `ARCANE_AGENTS_API_HOST`, `ARCANE_AGENTS_API_PORT`이다(`bootstrapApp.ts`).
브라우저는 `/api/ws`에서 처음에 `init`(전체 에이전트와 설정)을 받고 이후 생성, 갱신, 삭제 이벤트를 받는다.
연결이 끊기면 2초 뒤 다시 잇고 폴링 예비 경로도 있다(`hooks/useServerSync.ts`).
운영 빌드에서는 같은 서버가 `dist/client`도 서빙한다(`bootstrap/httpApp.ts`).

### 데이터 흐름

1. 폴링 또는 터미널 입출력이 `StatusMonitor.pollOnce`를 깨운다.
2. 에이전트마다 `collectSignals`가 화면 글과 프로세스, 대화 기록을 모은다.
3. `decide`가 상태와 활동 글, 확신도, 이유 목록을 만든다.
4. 바뀐 것만 SQLite에 쓰고 `RealtimeHub`가 모든 브라우저에 `worker-updated`를 보낸다.
5. 클라이언트가 Zustand 저장소에 반영하고 지도와 목록을 다시 그린다.

저장은 `better-sqlite3`로 `workers` 표 하나에 한다(`persistence/workerRepository.ts`).
WAL 모드이고 파일은 홈 디렉터리의 `.local/state/arcane-agents/arcane-agents.db`이다.
설정은 홈 디렉터리의 `.config/arcane-agents`에 있는 `config.yaml`과 `config.local.yaml`을 합친다.
`--session <이름>`을 주면 데이터베이스, tmux 세션, 소켓 이름이 따로 생긴다(`config/loadConfig.ts`).
에이전트의 위치, 이름, 소리 끄기, 완료 시각은 모두 여기에 남는다.

### 에러 처리

에이전트 하나의 평가가 예외를 내면 그 에이전트를 `error`, 활동 글 `Status check failed`, 확신도 0.25로 둔다(`statusMonitor.ts`).
tmux 세션이나 창이 없으면 `error` 상태에 활동 글 `Terminal unavailable`을 적는다.
`bootstrap/processGuards.ts`는 잡히지 않은 예외와 거부된 약속을 기록만 하고 서버를 계속 돌린다.
주석에 따르면 터미널 100개가량을 한 프로세스가 맡아서 pty 하나의 오류로 전체가 죽는 일을 막으려는 것이다.
HTTP 오류는 `{ error, code }` 모양으로 돌려주고, JSON이 아닌 본문은 400이다(`http/errorResponse.ts`).
사용자 정의 정규식은 시작할 때 `promptPatternSafety.ts`가 역참조, 전방탐색, 모호한 반복을 거부한다.
폴링 루프가 정규식 하나에 멈추는 것을 막으려는 장치이다.

### 의존성과 명령어

실행 의존성은 `express`, `ws`, `node-pty`, `better-sqlite3`, `zod`, `yaml`, `fast-glob`, `nanoid`이다.
화면은 `react` 18, `zustand`, `@xterm/xterm` 6과 두 애드온이 맡는다.
`node-pty`와 `better-sqlite3`는 네이티브 모듈이다.
Node 20 이상이 필요하다(`package.json`).
CLI는 `start`, `init`, `setup`, `config`, `doctor`, `sessions`, `status learn-prompt`이다(`cli.ts`).
`doctor`는 Node 버전, tmux, 설정 파일, 외부 터미널 도구를 점검한다.
`status learn-prompt`는 실행 중인 에이전트의 화면에서 프롬프트 서명을 만들어 로컬 설정에 적어 준다.
프로젝트 탐색은 `git worktree list`, 디렉터리 순회, glob 세 규칙을 지원한다(`config/discovery.ts`).

## 분석

### 사무실이 아니라 작전 지도이다

실시간 전략 게임의 지도처럼 여러 에이전트를 놓고 입력, 방송, 묶음 제어를 한다.
Pixel Agents가 보는 것에 집중하는 데 비해 이 도구는 터미널의 주인이 되어
어떤 명령이든 에이전트로 띄운다.
그 대가로 상태는 화면 글을 긁어 얻는 추측이어서 에이전트 화면 UI가 바뀌면 어긋난다.
방송은 `POST /api/workers/broadcast-input`이다.
최대 4096자의 글을 고른 에이전트 모두에게 `tmux send-keys`로 보낸다.

## 비평

### README와 코드 대조

| README                       | 코드에서 확인한 것                                               |
| ---------------------------- | ---------------------------------------------------------------- |
| 기본 주소 127.0.0.1:7600     | 일치한다(`config/schema.ts`)                                     |
| 내장 인증이 없다             | 일치한다. 라우트와 WebSocket 어디에도 인증 코드가 없다           |
| macOS에서 핵심이 동작한다    | `/proc`과 `ps etimes`를 읽는 코드가 있다. 실행은 확인하지 못했다 |
| 외부 터미널은 Linux 위주이다 | `xdg-terminal-exec`만 쓴다(`tmuxAdapter.ts`)                     |
| 사용자 규칙이 우선한다       | 일치한다. 판정 순서 1번에서 확신도 1로 끝난다                    |
| 0.0.0.0 바인딩은 위험하다    | 코드는 호스트 값을 그대로 쓰고 경고를 출력하지 않는다            |

### 열린 제어 면

서버는 에이전트의 pty에 붙고 임의의 명령을 띄울 수 있다
(`POST /api/workers/spawn`이 `command: string[]`을 받는다).
`resolveSpawnPlan.ts`는 프로젝트 ID와 런타임 ID가 설정에 있는지만 확인한다.
작업 폴더는 설정된 프로젝트로 제한되지만 명령은 요청에 든 배열이 그대로 쓰인다.
`src/server`에서 `cors`, `origin`, 인증, 토큰을 검색했으나 해당하는 코드가 나오지 않았다.
`bootstrap/httpApp.ts`는 `express.json()`만 걸고, `websocketUpgrade.ts`는 경로만 확인한다.
경로는 `/api/ws` 또는 `/api/terminal/<id>`이고 번호는 영문 숫자 `_` `-` 1~128자로 검사한다.
README는 내장 인증이 없다고 직접 경고하고 있으므로 인증 부재 자체는 알려진 설계이다.
확인하지 못한 것은 브라우저 안의 다른 사이트가 이 서버에 닿을 수 있느냐이다.
코드로 읽은 범위의 추론은 다음과 같다.
WebSocket 연결에는 CORS 사전 확인이 없고 서버도 Origin을 보지 않으므로 다른 사이트의 스크립트가 `ws://127.0.0.1:7600`에 연결을 시도할 수 있어 보인다.
`/api/ws`의 `init` 이벤트가 모든 에이전트 번호를 알려 주므로 그다음 터미널 연결로 이어질 수 있다.
서버는 Host 헤더도 검사하지 않으므로 DNS 재바인딩도 가능해 보인다.
반대로 `spawn` 같은 POST는 `application/json`이어야 본문이 읽히고 CORS 응답 헤더가 없어서, 다른 사이트의 일반 요청으로는 막힐 것으로 보인다.
이 추론은 시험하지 않았다.
`/api/workers/:id/status-fixture`는 저장된 화면 글(`output`, `visibleOutput`)을 돌려준다.
마지막 전환 5개까지 서버 메모리에 남는다(`statusMonitor.ts`).
터미널 pty는 서버의 환경 변수를 모두 물려받는다.

### 플랫폼과 분류의 느슨함

Claude 대화 기록을 묶는 코드가 `/proc/<pid>/cmdline`(`claudeTranscript/process.ts`)과
`/proc/<pid>/environ`(`claudeTranscript/io.ts`), `ps -o etimes=`를 읽는다.
앞의 둘은 Linux에만 있는 파일이고, 오류를 삼키고 기본값으로 돌아간다.
`environ`은 `CLAUDE_CONFIG_DIR`을 찾는 데만 쓰고 없으면 기본 대화 기록 폴더로 간다.
지원하지 않으면 프로세스 시작 시각을 얻지 못하고 15초마다 다시 시도한다.
이 경우에도 서버가 띄운 Claude는 명령에 `--session-id`가 있어 3번으로 묶인다.
다만 직접 입양한 창이나 이어서 연 세션은 4번 이하의 근거에 기대게 된다.
이 해석은 코드 읽기에서 나온 것이고 macOS에서 확인하지 않았다.
외부 터미널 열기 버튼은 `xdg-terminal-exec`를 써서 Linux 전용이다.
프로세스 분류가 인자 어디서든 `\bclaude\b`, `\bcodex\b`, `\bomp\b`에 일치한다.
그래서 인자에 그 단어가 든 다른 프로그램도 해당 런타임으로 분류될 수 있다.
셸 목록도 두 곳이 다르다.
분류 쪽은 `bash`, `zsh`, `sh`만 보고, 판정 쪽은 `fish`, `nu`, `pwsh`도 셸로 본다.

### 성숙도

테스트 파일 48개(약 1만 줄)와 `Vitest`, 실제 tmux 테스트가 있고
CI는 Ubuntu에서 타입 검사, 린트, 테스트, 빌드를 돌린다.
비테스트 TypeScript는 약 2만 3천 줄이다.
서버가 약 1만 1천 4백 줄, 클라이언트가 약 1만 1천 5백 줄이다.
1인 개발이라는 점은 이번 코드 읽기에서 다시 확인하지 않았다.
테스트가 무엇을 시험하는지는 파일 이름과 `it` 제목으로 읽었다.
`status/statusDecision.integration.test.ts`는 화면 글 입력에 대한 판정을 런타임별로 시험한다.
Claude 작업 중, 끝난 뒤 남은 도구 이름, 승인 대화상자, 시작 유예, 치명적 오류가 사례이다.
`tmux/tmuxAdapter.integration.test.ts`는 임시 소켓에서 진짜 tmux를 불러 따옴표 처리와 창 메타데이터를 시험한다.
tmux가 없으면 건너뛴다.
`ws/terminalBridge.test.ts`는 첫 resize 전에 pty를 열지 않는 것과 크기 하한을 시험한다.
`bootstrap/websocketUpgrade.test.ts`는 잘못된 번호와 모르는 경로의 거부를 시험한다.
인증이나 Origin을 시험하는 테스트는 찾지 못했다.

## 인사이트

### 가져갈 것

훅이 없는 도구도 tmux 화면 글과 프로세스 트리로 상태를 추정할 수 있다는 예이다.
이 방식은 도구가 훅을 제공하지 않을 때만 의미가 있고 도구의 화면이 바뀔 때마다 갱신해야 한다.
이 저장소는 그 갱신 비용을 어댑터 파일과 사용자 규칙, 서명 학습 명령으로 나눠 흡수한다.
로컬 서버를 신뢰할 수 있는 환경에서만 쓰고, 브라우저로 여는 동안 다른 탭을 조심해야 한다.

### 확인할 관찰

1. 서버에 인증이나 Origin 검사가 추가되는지.
2. macOS에서의 대화 기록 묶음이 실제로 동작하는지.
3. 에이전트 TUI가 바뀔 때 어댑터가 따라가는 속도.
