# Miniverse

<https://github.com/ianscott313/miniverse>

## 소개

Miniverse는 “에이전트를 위한 작은 픽셀 세계”를 표방하는 TypeScript 도구 모음이다.
작은 Node HTTP·WebSocket 서버가 메모리에 에이전트 상태표를 두고,
캔버스 라이브러리 `@miniverse/core`가 브라우저에 픽셀 주민을 그린다.
MIT 라이선스이다.
2026년 11월 25일 GitHub API로 본 별은 304개, 생성일은 2026년 3월 7일이고
마지막 커밋은 2026년 3월 13일, 커밋은 22개이다.
저장소의 `package.json`에 적힌 버전은 `@miniverse/server` 0.2.8,
`@miniverse/core` 0.2.5, `@miniverse/generate` 0.2.0,
`create-miniverse` 0.2.3이다.
npm에는 core가 0.2.6으로 올라와 있다고 서브 에이전트가 보고했다.
이 문서는 네트워크에 접근하지 않았으므로 npm 쪽 버전은 확인하지 못했다.
저장소에 별도 홈페이지는 등록되어 있지 않지만
README에는 별도 웹사이트와 문서 주소가 적혀 있다.

저장소를 받아 코드를 직접 읽었으며 설치하거나 실행하지 않았다.
끝까지 읽은 파일은 서버 패키지의 `server.ts`, `store.ts`, `events.ts`,
`cli.ts`, `frontend.ts`와 코어의 `index.ts`, `Citizen.ts`,
`Pathfinder.ts`, `Signal.ts`, `protocol.ts`이다.
`Scene.ts`, `SpeechBubble.ts`, `Editor.ts`,
`create-miniverse`의 Vite 플러그인 템플릿, `generate`의 `fal.ts`,
`llm.ts`, `background.ts`는 필요한 부분만 읽었다.
`Editor.ts`(1,740줄) 대부분과 `PropSystem.ts`,
`generate`의 `pipeline.ts`, `process.ts`, `world.ts`의 본문은 읽지 못했다.

## 동작 방식

### 모듈 구성

| 위치                        | 규모       | 역할                                              |
| --------------------------- | ---------- | ------------------------------------------------- |
| `packages/server`           | 약 1,260줄 | HTTP·WebSocket 서버, 상태표, 이벤트 로그, 훅 번역 |
| `packages/core`             | 약 4,700줄 | 렌더러, 주민, 길찾기, 신호 수신, 에디터           |
| `packages/create-miniverse` | 942줄      | 프로젝트 스캐폴드, Vite 개발 서버 플러그인 생성   |
| `packages/generate`         | 약 1,500줄 | fal.ai 호출, 배경 제거, 스프라이트와 월드 생성    |
| `demo`, `my-miniverse`      | 소규모     | 예시 Vite 앱과 월드 데이터                        |

규모는 `wc -l`로 센 값이다.
`packages/react/`는 없다.
`packages` 아래에는 위 네 폴더만 있다.

### 에이전트가 서버를 부르는 밀어 넣기 방식이다

대화 기록을 읽지 않는다.
에이전트나 Claude Code의 HTTP 훅이 서버를 호출해야 한다.
서버의 경로는 다음과 같다(`packages/server/src/server.ts`).

- `POST /api/heartbeat`: `{agent, state, task, ...}`로 상태를 알린다.
- `POST /api/act`: 말하기, 메시지, 상태, 채널 같은 행동과 세계를 고치는 행동을 받는다.
- `POST /api/hooks/claude-code`: `SessionStart`, `UserPromptSubmit`, `PreToolUse` 등을 상태로 바꾼다.
- `POST /api/webhook`: 서버가 호출할 주소를 등록한다.
- `GET /api/inbox`, `/api/observe`, `/api/events`도 있고 WebSocket의 `action`, `observe` 메시지도 받는다.

상태는 저장소의 `onUpdate`에서 WebSocket 방송으로 나가고
`@miniverse/core`의 `Signal`과 `handleSignalUpdate`가 화면에 반영한다.

### 화면과 에셋

캔버스 2D이고 4방향 격자의 A* 길찾기(`Pathfinder.ts`)를 쓴다.
휴리스틱은 맨해튼 거리이고, 열린 목록을 반복마다 `sort`로 정렬하며,
시작 칸이 걸을 수 있는지는 검사하지 않는다.
주민의 상태 열 가지와 상태별 애니메이션 표(`STATE_ANIMATION_MAP`)는
`Citizen.ts` 6~72줄에 있다.
상태 전이 규칙은 이 앞부분에 없다.
서버가 보낸 상태를 따르는 구조이고,
코어 안에서 스스로 상태를 바꾸는 것은 NPC뿐이다(`updateNpcPhase`, 218~271줄).
NPC는 대기, 일 또는 잠, 대기를 돈다.
첫 대기는 3~8초이고 이후 60% 확률로 일, 40% 확률로 잠을 10~30초 하며,
그 사이 대기는 5~15초이다.
앵커에 갈 수 없으면 3~8초 뒤 다시 시도한다.

저장소의 PNG 파일은 543개이다.
`demo`와 `my-miniverse`의 `public` 폴더에도 같은 종류의 파일이 있어
서로 다른 그림의 수는 아니다.
생성 코드는 직접 읽었다.
`packages/generate/src/fal.ts`가 fal.ai의 `fal-ai/nano-banana-pro`를,
`background.ts`가 `fal-ai/bria/background/remove`를 부른다.
`docs/asset-processing.md`도 같은 흐름을 적는다.
543개 각각이 이 경로로 만들어졌는지는 파일만으로 확인하지 못했다.
에셋에 대한 라이선스나 출처 표기 파일은 없다.
저장소의 `LICENSE`는 루트의 MIT 하나이다.

### 서버의 바인딩

`listen(this.port, ...)`이 호스트 인자 없이 호출되어(`server.ts` 84, 89줄)
기본값으로 모든 인터페이스에 열린다.
기본 포트는 4321이고 CORS는 `*`이며(`server.ts` 613줄) 인증은 없다.
포트가 사용 중이면 `start()`가 `EADDRINUSE`를 받아 포트를 1씩 올려 다시 연다(81~85줄).
`cli.ts`는 `--port`와 `--no-browser`만 읽고 바인딩 주소와 타임아웃은 받지 않는다.

### 서버의 상태 판정

입력 신호는 세 갈래로 들어온다.
`POST /api/heartbeat`, `POST /api/act`, `POST /api/hooks/claude-code`이다.
세 곳 모두 `AgentStore.heartbeat()`(`store.ts` 33~58줄)로 모인다.
이 함수는 들어온 필드가 있으면 덮어쓰고 없으면 기존 값을 유지하며,
`state`는 문자열이면 무엇이든 받는다.
`metadata`는 병합하지 않고 통째로 교체한다.

`sweep()`(`store.ts` 85~105줄)은 5초마다(`start()`, 23줄) 돈다.
마지막 신호 뒤 `offlineTimeout`을 넘으면 `sleeping`으로,
`sleeping`인 채로 그 두 배를 넘으면 `offline`으로 바꾼다.
`server.ts` 생성자(39줄)의 기본 `offlineTimeout`이 30,000ms이므로
수면은 30초 초과, 오프라인은 60초 초과이고 판정은 5초 단위로 어긋난다.
`offline`이 된 항목은 `POST /api/agents/remove`로 지우기 전까지 남는다.
상태가 바뀌면 `onUpdate` 리스너가 모든 WebSocket 클라이언트에
전체 목록을 보낸다(`broadcast`, 104~111줄).
`EventLog`(`events.ts`)는 최대 200개의 고리 버퍼이고
`since(id)`로 증분을 돌려준다.

Claude Code 훅은 `handleClaudeCodeHook`(459~581줄)이 번역한다.
에이전트 ID는 `claude-<작업 폴더 이름>-<세션 앞 6자>`이다.
본문 또는 쿼리의 `agent`, `name`이 있으면 그것이 우선한다(737~741줄).

| 훅                   | 상태            | 작업 문구                   |
| -------------------- | --------------- | --------------------------- |
| `SessionStart`       | idle            | 없음, 15초 keepalive 시작   |
| `UserPromptSubmit`   | thinking        | 프롬프트 앞 59자와 말줄임표 |
| `PreToolUse`         | working         | 도구 이름                   |
| `PostToolUse`        | working         | 도구 이름 앞에 완료 표시    |
| `PostToolUseFailure` | error           | 도구 이름 앞에 실패 표시    |
| `Stop`               | idle            | 없음                        |
| `SubagentStart`      | 부 주민 working | 하위 에이전트 작업          |
| `SessionEnd`         | offline         | keepalive 정리              |

`truncate(s, 60)`은 60자를 넘으면 59자에 말줄임표를 붙인다(892~894줄).
`SubagentStart`는 `<부모 ID>-sub-<6자>` ID로 별도 주민을 만들고
부모는 `Running subagent`로 표시한다.
`startKeepalive`는 15초마다 상태를 바꾸지 않는 heartbeat를 보낸다(440~446줄).
이 heartbeat가 `lastSeen`을 갱신하므로
`SessionEnd`가 오지 않으면 `sweep()`의 수면 판정이 일어나지 않는다.
이것은 코드를 읽어 얻은 추론이고 실행으로 시험하지 않았다.

### 코어의 반영과 화면

`Signal.ts`는 `rest`(기본 3초 폴링), `websocket`, `mock` 세 방식이다.
WebSocket은 `agents`, `event`, `message`, `world` 네 종류의 메시지를 처리하고
끊기면 5초 뒤 다시 연결한다(160~165줄).
`websocket` 경로는 서버의 `agent` 필드를 `id`로 바꾸는 `normalizeAgents`를 거치지만
`rest` 경로(126줄)는 거치지 않는다.
서버 응답에는 `id`가 없으므로 `rest` 방식은 주민을 찾지 못할 것으로 보인다.
이것도 코드에서 읽은 추론이다.

`Miniverse.handleSignalUpdate`(`index.ts` 530~579줄)는 NPC를 건너뛰고
`Citizen.updateState`를 부른 뒤 상태가 바뀌었을 때만 이동을 시작한다.
같은 주민의 이동 전환은 8,000ms(`TRANSITION_DEBOUNCE_MS`) 안에는 막되,
`working`으로 가는 경우, `offline`을 오가는 경우, 걷는 중이 아닌 경우는 허용한다.
`handleStateTransition`(651~683줄)의 이동 규칙은 다음과 같다.

- `working`은 본인의 집 앵커로, 안 되면 남의 집이 아닌 `work` 앵커로 간다.
- `sleeping`은 `rest`, `thinking`은 `utility` 앵커로 간다.
- `speaking`은 걷는 중이 아닐 때만 `social` 앵커로 간다.
- 말풍선은 `working`에서 4초, `speaking`에서 5초 보인다.

모르는 에이전트가 오면 `autoSpawnCitizen`(581~638줄)이 주민을 만든다.
`offline`이 아닐 때만 만들고, 스프라이트는 `nova`, `rio`, `dexter`, `morty`를 돌려 쓴다.
다른 주민에게 메시지를 보내면 `index.ts` 110~131줄이
상대 칸의 네 이웃 중 가장 짧은 경로로 보낸 쪽을 걸어가게 한다.
`to`가 문자열일 때만 동작하고 배열이면 걷지 않는다.
주민이 겹치지 않게 하는 분리 조향은 반경 1.5칸, 최대 이동 반 칸이다.
이동 속도는 초당 2칸이다.

### 에러 처리

- 잘못된 WebSocket 메시지는 조용히 무시한다(130~132줄).
- 훅 경로는 오류가 나도 항상 200을 돌려준다(743~748줄).
- `/api/act`는 알 수 없는 행동 종류나 필드가 틀린 행동도 `{ok:true}`로 답한다.
  처리할 수 없는 행동은 188줄 주석대로 조용히 버린다.
- 월드 편집 행동은 비동기로 처리되고 결과와 오류는 `system` 이름의
  인박스 메시지(JSON 문자열)로 돌아간다.
- 웹훅 호출 실패는 삼킨다(`fireWebhook`, 211줄).
- `/api/webhook` 등록 경로(709~721줄)만 `JSON.parse`를 `try`로 감싸지 않았다.
  `handleHttp`는 비동기 함수이고 `cli.ts`에는 처리되지 않은 거부를 받는 핸들러가 없다.
  잘못된 본문이 서버 종료로 이어질 수 있어 보이지만 실행으로 확인하지 않았다.

### 의존성과 테스트

서버의 런타임 의존성은 `ws` ^8.16.0 하나이고 빌드에 `esbuild`를 쓴다.
코어는 런타임 의존성이 없고 `vite`, `vite-plugin-dts`로 빌드한다.
`generate`는 `@fal-ai/client`와 `sharp`,
`create-miniverse`는 `@clack/prompts`와 `picocolors`에 의존한다.
루트의 `lint` 스크립트는 `eslint`를 부르지만 어느 `package.json`에도 `eslint`가 없다.
`typecheck` 스크립트는 코어만 대상으로 한다.
어느 `package.json`에도 테스트 스크립트가 없고 테스트 파일과 `.github` 폴더도 없다.
따라서 시험하는 대상이 없고, 이 문서의 동작 서술은 모두 코드 읽기에 근거한다.

## 분석

### 밀어 넣기와 끌어 오기

Pixel Agents류가 에이전트의 파일과 훅을 끌어 와서 상태를 알아내는 데 비해
Miniverse는 에이전트가 자신의 상태를 보내게 한다.
이 방식은 어떤 에이전트든 붙일 수 있고
`/api/act`의 `speak`, `message`로 에이전트끼리 대화하는 세계를 만들 수 있다.
관찰 도구가 아니라 에이전트가 사는 세계를 만드는 도구에 가깝다.

### 상태가 되돌아오지 않는 경로

서버는 `speak`나 `message`를 받으면 보낸 쪽을 `speaking`으로 바꾸지만
`idle`로 돌려보내는 코드가 없다(`server.ts` 142~171줄).
다음 신호가 오기 전까지 `speaking`이 유지되고,
`idle`일 때만 도는 배회 동작(`Citizen.update`, 205줄)은 멈춘다.
같은 상태가 반복되면 `handleSignalUpdate`가 상태 변화로 보지 않으므로
말풍선도 다시 뜨지 않는다.
30초 동안 신호가 없으면 `sweep()`이 `sleeping`으로 바꾼다.
메시지 내용은 이벤트 로그에 남기지 않지만(`routeMessage`, 254~259줄)
`speak`는 행동 전체를 `/api/events`에 남긴다(149줄).

## 비평

### 설명과 코드의 차이

- README는 `packages/react/`를 나열하지만 저장소와 npm 어디에도 없다.
- README는 4321번 포트에서 픽셀 세계 화면이 뜬다고 하지만
  `GET /`는 상태 페이지만 주고 화면은 스캐폴드로 만든 Vite 앱이 필요하다.
- README는 2분 뒤 수면, 4분 뒤 오프라인이라고 하지만 서버 기본값은 30초와 60초이다.
  `cli.ts`가 타임아웃을 넘기지 않으므로 실행 파일로는 바꿀 방법도 없다.
  README가 권하는 30~60초 간격 heartbeat는 60초 간격이면 수면 판정에 걸린다.
- README의 `/api/info` 예시 버전은 0.2.6이고 코드는 0.2.8을 문자열로 고정해 돌려준다(`server.ts` 638줄).
- `move`와 `emote` 행동은 메타데이터로만 저장된다.
  코어에서 `moveTo`, `emote`, `metadata`를 읽는 코드를 찾지 못했다.
  `Signal.ts`가 `metadata`를 전달만 한다.
- `waiting`, `collaborating`, `listening` 상태는 있으나 서버가 설정하는 경로가 없다.
  `heartbeat`는 어떤 문자열이든 받으므로 클라이언트가 직접 보내면 표시된다.
  `demo/src/main.ts`의 모의 데이터가 `waiting`을 쓴다.

### 인증과 입력 처리

서버가 모든 인터페이스에 열려 있고 본문 크기 제한이 없다(`readBody`, 896~903줄).
아래는 코드를 읽어 확인한 표면이며 실행으로 시험한 것은 아니다.

- 어떤 경로에도 인증이 없다.
  `OPTIONS`에 204로 답하고 CORS가 `*`이므로 방문한 웹 페이지의 스크립트도
  브라우저를 통해 로컬 서버를 부를 수 있어 보인다.
- 에이전트 ID가 곧 신원이다.
  `GET /api/inbox?agent=`는 남의 인박스를 비우고(687~699줄),
  `/api/hooks/claude-code?agent=`와 `/api/heartbeat`는 다른 에이전트로 행세한다.
- 상태 페이지 `frontend.ts` 95~100줄이 `name`, `task`, `state`를
  이스케이프 없이 `innerHTML`에 넣는다.
  `Editor.ts` 931줄도 자동 생성된 주민의 `name`을 같은 방식으로 넣는다.
  heartbeat로 보낸 문자열이 두 화면에 HTML로 들어갈 수 있다.
- `/api/act`의 월드 편집 행동은 `action.world`를 정리하지 않고
  `path.join(publicDir, 'worlds', worldId, 'world.json')`에 쓴다(264~267줄).
  `/api/observe?world=`도 같은 방식으로 읽는다(595~607줄).
  `generate_texture`, `generate_prop`은 `id`를 파일 이름에 그대로 쓴다.
  반면 `/api/generate`(837줄)와 스캐폴드의 Vite 플러그인은 `worldId`를 정리한다.
  쓰기는 대상 위치에 이미 `world.json`이 있어야 하는 행동이 대부분이다.
- `/api/webhook`은 주소를 검증하지 않고 저장하며,
  해당 에이전트의 인박스에 메시지가 쌓일 때마다 서버가 그 주소로 POST한다(203~212줄).
- `/api/generate`는 본문의 `falKey`를 `process.env.FAL_KEY`에 넣고(819줄)
  서버가 살아 있는 동안 유지된다.
  참조 이미지는 임시 파일로 쓰고 지우지 않는다.
- README의 공개 훅 설정은 `PreToolUse`, `PostToolUse`, `Stop` 셋만 등록한다.
  프롬프트는 `UserPromptSubmit`에서만 읽으므로 이 설정으로는 서버가 프롬프트를 받지 않는다.
  서버가 쓰는 필드는 도구 이름, 작업 폴더 이름, 세션 ID이고
  이 값이 외부 호스트의 에이전트 ID와 이름에 들어간다.
  Claude Code가 훅 본문에 실제로 무엇을 담는지는 이 저장소만으로 확인하지 못했다.
  프롬프트 앞부분이 나가는 경우는 `docs/claude-code-quickstart.md`처럼
  `UserPromptSubmit`을 등록한 설정이다.
  그 문서의 주소는 `localhost`이다.
- 상태표는 `offline` 항목을 지우지 않고, 인박스는 에이전트당 100개까지만 막는다.
  에이전트 수에는 제한이 없다.

### 성숙도

테스트와 CI가 없고 소스는 약 9,700줄, 버전은 0.2.x, 커밋은 일주일에 몰려 있다.
직접 센 값은 `ts`, `js`, `mjs` 파일 9,715줄이다.
`my-miniverse/package.json`이 `file:/Users/ian/Developer/...` 절대 경로를 가리켜
다른 곳에서 설치할 수 없다.
`demo`는 상대 경로를 쓴다.
`create-miniverse`는 환경 변수 `MINIVERSE_DEV`가 없으면 `^0.2.0`을 쓴다.
월드 생성을 고르면 사용자가 입력한 프롬프트를 셸 문자열에 넣어 `execSync`로 실행하며
큰따옴표만 이스케이프한다(`create-miniverse/src/index.ts` 332~344줄).

## 인사이트

### 가져갈 것

에이전트가 스스로 상태를 보고하는 세계를 만들 때의 최소 구성 예이다.
공개망이나 신뢰할 수 없는 네트워크에 열기 전에는 호스트 바인딩과 입력 경로 처리를 고쳐야 한다.
관찰용 대시보드가 목적이라면 훅이나 대화 기록 기반 도구가 설치가 더 간단하다.

### 확인할 관찰

1. README와 서버 기본값의 불일치가 정리되는지.
2. 1주 만에 멈춘 커밋이 다시 이어지는지.
3. 에셋의 라이선스가 밝혀지는지.

위 셋 모두 이 문서가 확인하지 못했다.
