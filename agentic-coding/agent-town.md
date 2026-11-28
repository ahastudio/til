# Agent Town

<https://github.com/geezerrrr/agent-town>

HN 토론: <https://news.ycombinator.com/item?id=47293523> (3점, 0개 댓글)

## 소개

Agent Town은 “픽셀아트 AI 에이전트 온라인 협업 플랫폼”을 표방하는 Next.js 기반 웹 앱이다.
2026년 11월 25일 GitHub API로 본 별은 263개, 생성일은 2026년 3월 5일,
커밋은 82개이고 마지막 커밋은 10월 10일(버전 0.5.0)이다.
GitHub API는 라이선스를 비어 있다고 돌려주고 저장소 안에 `LICENSE` 파일이 없다.
`package.json`은 MIT라고 선언하고 README가 존재하지 않는 `./LICENSE`를 링크한다.
작성자는 한 사람이고 커밋에 Claude 공동 저자 표기가 붙어 있다.
별도 홈페이지는 없다.

저장소를 받아 코드를 읽었으며 설치하거나 실행하지 않았다.
`lib/reducer.ts`와 `lib/store.ts`는 일부만, 테스트는 구조만 읽었다.
HUD 컴포넌트 대부분과 `Worker.ts`의 세부는 읽지 못했다.
별, 생성일, 커밋 수와 GitHub API의 라이선스 값은 이번에 다시 확인하지 못했다.

## 동작 방식

### 모듈 구성

| 위치                                    | 역할                                                                                         |
| --------------------------------------- | -------------------------------------------------------------------------------------------- |
| `server.ts`                             | 개발·`pnpm start`용 HTTP 서버. Next.js 핸들러와 내부 엔드포인트, 프록시 또는 브리지를 붙인다 |
| `server.prod.mjs`, `bin/agent-town.mjs` | npx용 서버와 CLI. 옵션 `--port`, `--gateway`, `--provider`를 환경 변수로 바꾼다              |
| `lib/ws-proxy.ts`                       | 브라우저와 OpenClaw 게이트웨이 사이 WebSocket 중계                                           |
| `lib/auggie-bridge.ts`                  | 게이트웨이 프로토콜을 흉내 내고 `auggie`를 자식 프로세스로 띄운다                            |
| `lib/mcp/agent-town-mcp.mjs`            | 의존성 없는 stdio MCP 서버. 도구는 `dispatch_to_worker` 하나다                               |
| `lib/gateway.ts`                        | 브라우저 쪽 게이트웨이 클라이언트. 핸드셰이크, 재연결, 요청 타임아웃                         |
| `lib/gateway-handler.ts`                | 게이트웨이 이벤트를 reducer 액션과 게임 이벤트로 바꾼다                                      |
| `lib/reducer.ts`, `lib/store.ts`        | 상태 정의와 React 컨텍스트 제공자                                                            |
| `lib/events.ts`                         | HUD와 Phaser 사이의 이벤트 버스(`gameEvents`)                                                |
| `components/game/`                      | Phaser 장면, 워커, 경로 탐색, 상호작용                                                       |
| `app/api/agents/discover/route.ts`      | 하나뿐인 Next.js API 경로                                                                    |

`lib/ws-proxy.mjs`와 `lib/auggie-bridge.mjs`는 `.ts` 파일의 JavaScript 사본이다.
사본은 `WebSocket`, `WebSocketServer`를 인자로 받는 점이 다르다.
`scripts/prepare-package.mjs`가 이 사본을 npm 패키지에 복사한다.

### 에이전트를 직접 돌리지 않는다

이 저장소에는 에이전트 루프가 없고 LLM API도 부르지 않는다.
런타임 의존성은 `ws` 하나뿐이다.
두 가지 경로로 에이전트를 연결한다.

- 바깥에 있는 OpenClaw 게이트웨이로 WebSocket을 중계한다(`lib/ws-proxy.ts`).
- 게이트웨이를 흉내 내는 브리지가 `auggie` CLI를 프로세스로 띄운다(`lib/auggie-bridge.ts`).

받은 이벤트를 화면에 매핑하는 것이 이 저장소의 일이다(`lib/gateway-handler.ts`).
협업은 사용자가 워커에게 작업을 배정하는 방식이고 세션 키별 대기열이 있다.
`auggie` 모드에서는 MCP 도구 `dispatch_to_worker`로 워커끼리 위임한다.
이 위임 경로는 개발 서버(`server.ts`)에서만 이어지고 npx용 서버는 이어지지 않는다.
근거는 아래 서버 진입점 절에 있다.

### 서버 진입점

`server.ts`는 `AGENT_PROVIDER`(기본 `openclaw`)에 따라 프록시나 브리지를 붙인다(124~145줄).
포트는 `PORT`(기본 3000), 게이트웨이는 `GATEWAY_URL`(기본 `ws://127.0.0.1:18789/`)이다.
`auggie` 모드일 때만 `/api/internal/dispatch`와 `/api/internal/seat-sync`를 Next.js보다 먼저 가로챈다.
`server.prod.mjs`는 모든 요청을 Next.js에 넘기고 이 두 경로를 가로채지 않는다(44~46줄).
따라서 npx로 실행하면 `auggie` 모드에서도 좌석 명단 동기화가 Next.js의 404로 끝난다.
명단이 비면 `writeMcpConfig`가 MCP 설정을 만들지 않으므로(`auggie-bridge.ts` 455줄) 위임 도구가 붙지 않는다.
이 결론은 코드를 읽은 추론이며 실행해서 확인하지 않았다.

### 이벤트가 화면에 닿기까지

사용자가 작업을 배정하면 `assignTask`가 `ADD_TASK`와 `task-assigned`를 낸다(`useTaskRouter.ts`).
`SceneEventBridge.ts`는 명시된 좌석, 세션에 묶인 좌석, 아무 유휴 워커 순으로 대상을 고른다.
대상이 작업 중이면 워커 쪽 대기열에 넣고(`enqueueTask`), 책상을 떠나 있으면 먼저 돌아오게 한다.
워커가 준비되면 `task-ready`가 나가고 `sendTaskToGateway`가 `chat.send`를 요청한다.
같은 세션 키에 실행 중이거나 제출된 작업이 있으면 브라우저 쪽 대기열에 넣어 하나씩 보낸다.
이 대기열은 `task-completed`, `task-failed`, `task-aborted`가 올 때 비운다.
따라서 대기열이 두 겹이다. 워커별 Phaser 대기열과 세션별 브라우저 대기열이다.

게이트웨이가 돌려주는 이벤트는 `lib/gateway-handler.ts`가 처리한다.
`agent` 이벤트의 `lifecycle` 스트림이 시작, 끝, 오류를 알려 준다.
`tool` 스트림은 말풍선에 도구 이름을 3초간 띄우고 채팅 기록에 도구 입력과 출력을 쌓는다.
`assistant` 스트림의 델타는 150ms로 묶어 말풍선에 보이고(`BUBBLE_THROTTLE_MS`), 5만 자까지 누적한다.
말풍선은 80자를 넘으면 뒤쪽 77자만 보여 준다.
`chat` 이벤트의 `final`은 `lifecycle`의 끝이 오지 않았을 때를 위한 보조 완료 신호다.
세션 키에 `subagent:`가 들어 있으면 하위 작업으로 보고 빈 워커나 지정 좌석에 `[Sub]` 작업을 배정한다.
중단한 실행(`stoppedRunIds`)의 늦은 이벤트는 버린다.

### 화면

Phaser 3(Arcade 물리, 픽셀 렌더링)와 Tiled 맵 위에 React HUD를 얹었다.
워커의 상태는 대기, 작업 중, 완료, 실패 네 가지(`worker/types.ts`)이고
상태 점의 색, 말풍선, 말줄임 이모트로 보여 준다.
도구별 애니메이션은 없다.
쉬는 워커는 무작위로 돌아다니며 장소를 들른다.
`components/game/entities/worker/idle.ts`는 3~10초 뒤에 움직이기 시작한다.
그때 35% 확률로 맵의 장소(물, 프린터, 책, 화이트보드, 소파, 커피)로 가고 나머지는 자리에서 이모트를 보인다.
한 워커가 시작한 뒤 1.8초 안에는 다른 워커가 시작하지 못하게 시차를 둔다.
작업을 받으면 말풍선을 4초 보이고 4.2초 뒤에 말줄임 이모트를 띄운다.
완료와 실패 상태는 4.5초 유지한 뒤 대기로 돌아가 다음 대기열 항목을 시작한다(`task.ts`).
경로 탐색은 16픽셀 격자 위의 A*이며 반복을 2만 번으로 막는다(`Pathfinder.ts`, `constants.ts`).
맵은 `public/maps/office2.json`(Tiled)이고 `OfficeScene.ts`가 불러온다.
기본 워커 이름은 Alice, Bob, Carol, Dave 넷이다(`animations.ts`).

### 연결과 재시도

`lib/gateway.ts`는 `connect.challenge` 이벤트를 받으면 `connect` 요청을 보낸다.
프로토콜 범위는 3~4이고 요청하는 권한 범위는 `operator.read`, `operator.write`, `operator.admin`이다.
핸드셰이크 제한은 15초, 일반 요청 제한은 30초다.
재연결은 1초에서 시작해 두 배씩 늘려 최대 30초까지 두되 시도는 3번으로 끝나고 이후 `unreachable`이 된다.
핸드셰이크가 거부되면 재시도를 멈추고 메시지에 따라 `protocol_mismatch`, `rate_limited`, `auth_failed`로 나눈다.
`lib/ws-proxy.ts`는 업스트림 연결이 열리기 전 클라이언트 메시지를 최대 100개 모아 두고 15초 안에 못 열면 닫는다.
닫힘 코드는 허용 범위만 그대로 전달하고 나머지는 코드 없이 닫는다.
브라우저가 보내는 토큰은 프록시를 거쳐 그대로 게이트웨이에 간다.
프록시는 토큰을 검사하지 않는다.

### auggie 브리지

`lib/auggie-bridge.ts`는 `/api/gateway` 업그레이드에서 `connect.challenge`를 먼저 보낸다.
`connect` 요청의 토큰을 보지 않고 `hello-ok`와 읽기·쓰기 권한을 돌려준다(404~409줄).
처리하는 메서드는 `chat.send`, `chat.abort`, `sessions.list`, `sessions.preview`, `models.list`뿐이다.
세션 목록과 미리보기는 빈 배열을 돌려준다.
`chat.send`는 `auggie --print --output-format json [--mcp-config 파일] [--resume 세션] -- 메시지`로 실행한다.
인자를 배열로 넘기고 셸을 거치지 않으며 `--`로 메시지를 옵션과 분리한다.
메시지 앞에 좌석 이름과 역할을 알리는 문장을 붙이고, 다른 워커가 있으면 위임 도구 안내를 덧붙인다.
출력은 모두 모았다가 종료한 뒤 한 번에 해석하므로 토큰 단위 스트리밍은 없다.
종료 코드가 0이 아니거나 출력이 JSON이 아니면 오류 이벤트를 보낸다.
`session_id`를 세션 키에 묶어 다음 요청에서 `--resume`으로 이어 간다.
중단 요청은 해당 자식 프로세스에 `SIGTERM`을 보내고, 연결이 끊기면 남은 프로세스를 모두 종료한다.
`models.list`는 `auggie model list --json`을 10초 제한으로 실행하고 실패하면 컨텍스트 128000짜리 고정 항목을 돌려준다.
위임 시 `dispatchToWorker`가 좌석별 세션(`dispatch:좌석ID`)으로 새 `auggie` 프로세스를 띄우고 결과 텍스트를 도구 결과로 돌려준다.
위임 프로세스에는 제한 시간이 코드에 없다.
`auggie` CLI 자체의 동작은 읽지 못했다.

### “온라인”은 아직 구현이 없다

방, 접속자 표시, 인증, 여러 사용자의 동기화가 없고
상태는 브라우저 `localStorage`에 저장된다.
`auggie` 브리지는 연결마다 상태를 따로 만들지만 모듈 변수 `activeClientState`에는 마지막 연결 하나만 남는다.
위임 요청은 그 마지막 연결로만 이벤트를 보낸다(`auggie-bridge.ts` 30, 678줄).
연결 수를 제한하는 코드는 없다.
README가 설명하는 공유 온라인 세계, 백엔드와 커넥터 구조, `cloud.agent.town`, 마켓플레이스는
코드에서 찾지 못했고(해당 문자열 검색 결과 없음) README도 이를 목표 구조와 로드맵으로 적는다.

### 저장과 의존성

상태는 `lib/persistence.ts`를 통해 `localStorage`의 `agent-town:` 접두 키 여덟 개에 저장한다.
작업은 200개, 채팅은 400개, 세션은 20개까지만 자른다.
읽기 실패는 기본값으로 대체하고 쓰기 실패는 경고만 남긴다.
게이트웨이 설정(주소와 토큰)은 연결에 성공한 뒤에만 저장한다(`useGateway.ts`).
런타임 의존성은 `ws`뿐이다.
`next`, `phaser`, `react`는 개발 의존성으로 선언되어 있고 npm 패키지는 `output: "standalone"` 빌드 산출물을 담는다.
`next.config.ts`는 CSP, `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy`를 모든 경로에 붙인다.
`connect-src`는 자기 출처와 localhost 계열 WebSocket만 허용하고 `CSP_CONNECT_SRC`로 늘릴 수 있다.
`script-src`에는 `unsafe-eval`과 `unsafe-inline`이 들어 있다.

## 분석

### 연출 층만 있는 구조

저장소의 구현은 외부 에이전트가 주는 스트림을 working, done, failed 연출로 바꾸는
얇은 층이다.
Pixel Agents가 도구 호출 하나하나를 동작으로 바꾸는 것과 대비된다.
사용자가 게임 안에서 작업을 배정하고 `chat.send`나 `auggie` 실행으로 에이전트를 직접 구동한다는 점이
관찰 도구와 다르다.

## 비평

### 보안 경계

서버가 호스트 지정 없이 `listen(port)`로 열린다(`server.ts` 147줄, `server.prod.mjs` 54줄).
WebSocket 업그레이드는 Origin 헤더가 있을 때만 Host와 비교하고 헤더가 없으면 통과시킨다.
이 검사는 `ws-proxy.ts`와 `auggie-bridge.ts`에 같은 모양으로 있다.
`auggie` 브리지는 `connect`의 토큰을 보지 않는다.
이 코드를 읽은 결과, 포트에 닿고 Origin을 보내지 않는 클라이언트는 `chat.send`로 `auggie` 실행을 시킬 수 있다.
자식 프로세스는 `process.env` 전체를 상속한다(198~206줄).
`auggie`가 도구를 얼마나 자율로 쓰는지는 CLI를 읽지 못해 알 수 없다.
`/api/internal/seat-sync`는 비밀값 검사와 로컬 주소 검사가 없고 본문 크기 제한도 없다(`server.ts` 86~117줄).
반대로 `/api/internal/dispatch`는 로컬 주소와 `x-dispatch-secret`을 모두 검사한다(41~53줄).
디스패치 비밀값은 `at_` 뒤에 시각과 `Math.random` 문자열을 붙여 서버 시작 때 한 번 만든다(443줄).
비교는 일반 문자열 비교다.
`/api/agents/discover`는 인증이 없고 `~/.openclaw/openclaw.json`과 `agents/` 아래를 읽는다.
돌려주는 것은 에이전트 ID, 작업 공간 경로, 모델, 이름과 이모지, `SOUL.md` 앞 200자다.
에이전트 ID는 정규식으로 거르지만 설정이 가리키는 작업 공간 경로는 `isSafePath` 검사를 받지 않는다.
게이트웨이 토큰은 `localStorage`에 평문 JSON으로 저장된다(`persistence.ts`).

### 설명과 코드의 차이

- 중국어 `CLAUDE.md`의 디렉터리 그림은 `status`, `agents`, `ws` 경로를 적는다(87~90줄).
  실제 API 경로는 `app/api/agents/discover/route.ts` 하나이다.
- README는 `auggie` 제공자를 언급하지 않지만 코드에서는 비중이 크다.
- `CLAUDE.md` 20줄은 에셋이 itch.io의 LimeZu Modern 시리즈이고 구매한 라이선스라고 적는다.
  `public/`에는 이 시리즈의 캐릭터와 타일셋이 들어 있으나 저장소에는 재배포 조건이 없다.
- README는 `./LICENSE`를 링크하지만 파일이 없다.
- 내부 엔드포인트 두 개는 npx용 서버에 연결되지 않아 `auggie` 위임이 그 경로에서 동작하지 않는다고 읽힌다.

### 성숙도

테스트는 `lib/__tests__` 아래 4개 파일이고 `it(` 호출을 세면 178개다.
`gateway-handler.test.ts` 59개, `reducer.test.ts` 78개, `persistence.test.ts` 25개, `utils.test.ts` 16개다.
`gateway-handler` 시험은 가짜 클라이언트에 이벤트를 흘려 reducer 액션과 게임 이벤트가 맞는지 본다.
시작, 끝, 오류, 도구, 델타, 말풍선 묶음, 세션 키 해석, 하위 작업 판별, 중단 정리를 다룬다.
`reducer` 시험은 액션별 상태 변화와 좌석 병합을, `persistence`는 `localStorage` 읽기와 자르기를 다룬다.
`gateway.ts`, `ws-proxy.ts`, `auggie-bridge.ts`, MCP 서버, API 경로, Phaser 코드에 대한 시험은 찾지 못했다.
`vitest.config.ts`의 커버리지 문턱은 `lib/` 기준 40%이고 `lib/hooks/`는 제외한다.
CI는 포맷, 린트, 타입 검사, 빌드, 테스트, 감사(`continue-on-error`)를 돌린다.
테스트가 아닌 TypeScript와 MJS는 약 1만 1,300줄이며 `.mjs` 사본이 중복해서 센 값이다.
`.ts`와 `.tsx`만 세면 약 1만 200줄이다.

## 인사이트

### 가져갈 것

외부 게이트웨이의 이벤트를 게임 화면으로 옮기는 얇은 프런트엔드 예로 읽을 수 있다.
온라인 협업 플랫폼이라는 이름과 달리 지금은 단일 사용자 로컬 도구이다.
브리지 포트를 네트워크에 열어 두지 않아야 한다.

### 확인할 관찰

1. 공유 온라인 세계가 실제 구현으로 들어오는지.
2. 라이선스 파일과 에셋 재배포 조건이 정리되는지.
3. 브리지 인증이 추가되는지.

위 보안 서술은 코드 읽기에 근거하고 실행으로 재현하지 않았다.
