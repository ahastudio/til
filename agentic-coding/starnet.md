# StarNet

<https://github.com/androoAGI/starnet>

## 소개

StarNet은 “진짜 AI 에이전트가 진짜 일을 하는 살아 있는 픽셀아트 정거장”을 표방하는
로컬 우선 데스크톱 에이전트 하네스이다.
관찰 도구가 아니라 직접 에이전트를 돌리는 쪽이고
픽셀 정거장은 에이전트 런타임의 이벤트를 소비하는 화면이다.
라이선스는 MIT이며 이름, 로고, 그림은 별도 조건이라고 README(197~204줄)가 적는다.
2026년 11월 25일 GitHub API로 본 별은 1,925개, 생성일은 2026년 6월 14일이고
주 언어는 JavaScript, 버전은 0.15.0이다.
저장소의 홈페이지 항목은 설치 파일을 담은 별도 저장소
`androoAGI/starnet-releases`의 릴리스 페이지를 가리킨다.

저장소를 받아 코드를 읽었으며 설치하거나 실행하지 않았다.
별 수와 생성일은 GitHub API로, 코드에 관한 서술은 클론한 파일을 직접 읽어 확인했다.
`sidecar/index.js`는 31,987줄이라 전부 읽지 못했고 아래에서 다룬 구간만 읽었다.
`src-tauri/src/main.rs`(6,297줄)와 `frontend/app/world.js`(13,030줄)도 마찬가지이다.
`website/`는 읽지 않고 문자열 검색만 했다.
테스트는 실행하지 않았고 파일을 읽기만 했다.

## 동작 방식

### 모듈 구성

규모는 `.js`, `.mjs`, `.rs` 파일만 세어 직접 계산한 값이다.

| 영역            | 위치             | 규모                 | 역할                                              |
| --------------- | ---------------- | -------------------- | ------------------------------------------------- |
| 에이전트 런타임 | `sidecar/`       | 490파일, 181,802줄   | HTTP와 SSE 서버, 루프, 도구, 제공자, 채널         |
| 프런트엔드      | `frontend/`      | 314파일, 216,520줄   | 빌드 없는 정적 JS와 픽셀 화면                     |
| 데스크톱 셸     | `src-tauri/src/` | 17파일, 14,526줄     | sidecar 기동과 감시, 키체인, 업데이터             |
| 중계            | `relay/`         | 6파일, 2,357줄       | 휴대폰과 정거장을 잇는 WebSocket 중계             |
| 공유            | `shared/`        | 5파일                | 이벤트 스키마(`events.js`)와 방송기(`emitter.js`) |
| 테스트          | `test/`          | 2,204파일, 411,391줄 | 단위, HTTP, 종단 시험                             |

`frontend/` 안의 파일은 모두 15,834개이고 그중 15,443개는 `assets/`의 그림 자원이다.

### 자체 에이전트 루프

`sidecar/loop.js`(3,224줄)의 `runAgentLoop`가 에이전트를 돌린다.
메시지 배열 하나를 `while (true)`로 도는 구조이고
매 반복에서 유료 호출 전에 다음 순서로 검사한다.
먼저 취소 신호, 다음 반복 한도, 지출 한도, 자격 증명 변경, 컴퓨터 보유 여부(compute gate) 순이다.
도구 호출이 하나도 없으면 멈추며 종료 사유는 `done`, `cancelled`, `max_iters`, `budget`, `error` 등이다.
반복 한도 `maxIters`는 기본값이 꺼짐이어서 값이 없거나 0이면 무한대로 취급한다(`loop.js` 1002~1004줄, `index.js` 908줄).
한도에 닿으면 도구 없는 마지막 답변 한 번을 허용한 뒤 `max_iters`로 끝낸다.
실행당 비용 한도(`perRun`)와 에이전트당, 전체 한도의 출하 기본값도 0이다.
하루 한도(`perDay`)만 25달러로 켜져 있는 무른 한도이고
이는 2026년 9월 17일에 하룻밤 98번 반복하며 약 98달러를 쓴 사고 뒤에 바뀌었다고 주석이 적는다(`budgetcaps.js` 22~31줄).
구독형 로그인 실행은 달러 한도를 받지 않고 토큰 한도를 따로 받는다(`loop.js` 2137~2144줄).

모델 응답 처리에는 다음 방어가 들어 있다.
- 도구 호출 인자 JSON이 문자열 중간에서 끊겼으면 고치지 않고 거부한다.
  잘린 파일을 완전한 쓰기로 실행한 사고 뒤에 넣었다고 주석이 적는다(`loop.js` 82~100줄).
- 텍스트로 출력된 `<tool_call>` 같은 표지는 실행하지 않고 제거한다.
  파일 내용이 도구 실행을 몰고 가는 주입 경로를 막기 위해서라고 적는다(`loop.js` 106~120줄).
- 모든 도구 호출 id는 다음 모델 호출 전에 결과를 정확히 하나 받는다(`assertPaired`).
- 스트림 재시도 간격은 0.4, 1.2, 4, 10, 30, 60초 여섯 단계이고 잘림 재시도는 한 번이다.
- 컨텍스트가 넘치면 요약 접기를 최대 세 번 한다(`OVERFLOW_FOLDS`).

모델 제공자는 `providers/registry.js`에 19개가 등록되어 있다.
OpenRouter, OpenAI, Anthropic, Gemini, xAI, Groq, Mistral, DeepSeek, Together, Fireworks, Perplexity, Cerebras,
로컬 Ollama와 사용자 지정 엔드포인트, 구독 로그인용 `codex`, `grok`, `kimi`, `claude-cli`, 그리고 자체 크레딧 `starnet`이다.
ChatGPT 구독 로그인은 `chatgpt.com/backend-api/codex`를 쓰고(`providers/codex.js` 38줄)
Grok과 Kimi는 표준 기기 코드 OAuth(RFC 8628)로 로그인한다(`providers/oauth-device.js`).
`claude-cli.js` 어댑터는 로컬 `claude -p`를 자식 프로세스로 띄워 stdin으로 입력하고 `stream-json`을 읽는다.
Claude 로그인은 `claude auth login --claudeai`를 대신 실행할 뿐 StarNet이 구독 자격 증명을 보관하지 않는다고 적는다(`claude-cli-login.js`).
키는 Rust `keyring` 크레이트로 운영체제 키체인에 저장되고,
서비스 이름은 `ai.skynet.harness`이며 제공자 13곳의 키, 채널 토큰, 크레딧 기기 토큰, 커넥터 암호화 키를 항목별로 둔다(`src-tauri/src/credentials.rs`).
셸이 sidecar를 띄울 때 키를 환경 변수로 넘기고 sidecar는 그것을 메모리에서 쓴다(`credential-store.js`).
키체인 항목에서 암호화 키가 이미 있는데 형식이 깨졌으면 덮어쓰지 않고 오류를 낸다.

### 도구와 권한

도구는 shell, 파일, 웹, 브라우저, 데스크톱 제어, MCP 커넥터 등이다.
방에 놓은 오브젝트가 도구를 허용하며 대응표는 `capability/registry.js`의 `CAP_REGISTRY`이다.
오브젝트는 `computer`, `notebook`, `cabinet`, `dish`, `connector`, `plugin`, `workbench`, `orchestrator`, `builder`, `studio`, `jukebox`이다.
`workbench`가 `shell.exec`와 백그라운드 프로세스 도구를, `cabinet`이 `fs.*`를, `dish`가 `web_*`를 준다.
`computer`는 모델 호출 자체의 전제 조건이다.

동의는 `permissions.js`의 `makeConsentBroker`가 정하며 네 단계를 고정된 순서로 본다.
1. 하드라인: 무조건 거부하는 바닥이다. 거부 사유에 다시 시도하지 말라는 문구를 붙인다.
2. 우회: 전체 접근이 켜져 있으면 하드라인이 아닌 모든 것을 허용한다.
3. 캐시: 이 세션이나 영구로 허가한 위험 종류이면 허용한다.
4. 결정: 읽기 전용이고 네트워크가 없으면 자동 허용한다.
   변경은 자율 실행이면 기본 거부하고 대화형이면 사람에게 묻는다.
   묻는 통로가 없으면 거부로 닫힌다.
이 함수는 입출력, 시계, 환경 변수를 직접 건드리지 않는 순수 함수이다.
자율 실행에서 실행 범위(`execute`)의 도구, 곧 shell은 이전에 영구 허가를 받았어도 거부한다(`permissions.js` 235줄).
위험 종류는 도구 이름과 범위의 조합이며 인자나 경로는 보지 않는다.

전체 접근 우회는 세 가지 경로가 있다.
- 환경 변수 `STARNET_FULL_ACCESS`로 부팅 때 고정하는 값이다(`index.js` 4752줄).
- 설정 화면의 마스터 우회 스위치로, `permissions.bypass.json`에 저장되고 `/api/permissions/bypass` 경로로만 바뀐다.
  모델에게 이 경로에 닿는 도구가 없다는 점이 주입 방어의 근거라고 주석이 적는다.
  파일을 읽지 못하면 꺼짐으로 처리한다.
- 에이전트별 `approvalMode === 'full'` 설정이다.
어느 쪽이든 하드라인 바닥은 넘지 못한다.
바닥은 `.env`와 `.git` 내부 경로이며 Windows 대체 데이터 스트림 표기(`.env::$DATA`)까지 막는 정규식이다(`index.js` 5063~5069줄).
우회가 켜져도 물리 마우스와 실제 화면 제어는 별도 임대가 필요하다고 주석이 적는다.

`taint.js`는 웹 페이지, 브라우저 읽기, 커넥터 결과처럼 사용자가 쓰지 않은 내용이 실행 맥락에 들어오면
그 실행이 끝날 때까지 `shell.exec`, `web_request`, 커넥터 쓰기와 실행을 거둬들이는 규칙이다.
내용을 탐지하지 않고 쓸 수 있는 권한을 없앤다는 접근이며,
셸 출력과 로컬 파일 읽기는 출처로 치지 않아 남는 경로라고 주석이 스스로 적는다.
`tools/fence.js`의 외부 내용 울타리는 조언일 뿐 강제가 아니라고 적는다.
이 규칙이 어떤 호출 지점에서 실제로 집행되는지는 추적하지 않았다.

shell의 “감옥”은 명령 문자열에 대한 최선 노력의 정규식 규칙이다.
`tools/builtin/shell.js`의 `FLOOR_RULES`는 `..` 경로, `C:\` 같은 드라이브 절대 경로, UNC 경로, 드라이브 루트 상대 경로,
`.checkpoints`와 `ledger.jsonl` 같은 제어 파일 이름을 거부한다.
유닉스 절대 경로(`/etc`)는 옵션 `/S`와 구분할 수 없어 이 정규식 바닥에서 막지 않는다고 주석이 적는다.
명령 머리마다 위험 동사를 보는 거부 목록이 따로 있으며 주석이 스스로 거부 목록은 결의에 찬 주입을 이길 수 없다고 한계를 인정하고,
근본 해법은 운영체제 격리이며 아직 문서상 계획이라고 적는다.
기본 제한은 시간 30초(최대 10분), 출력 64,000바이트이고 시간이 지나면 자식 프로세스 트리를 죽인다.
shell 호출 전에는 작업공간 스냅샷을 만든다고 머리 주석이 적는다.
`code.run`은 모델이 쓴 JavaScript를 별도 자식 프로세스에서 돌리되
`require`, 파일, 네트워크 없이 읽기 도구 호출만 부모에게 요청하게 한다(`tools/builtin/code.js`).
실행 위치는 프로필로 정해진다(`execution-profiles.js`).
`safe-cell`은 docker, `remote-ssh`는 ssh, `trusted-project`와 `this-computer`는 로컬이고
기존 정거장의 기본 프로필 `station-gear`는 현재 백엔드, 곧 호스트를 쓴다.
요청한 docker나 ssh를 쓸 수 없을 때 기본 정책(`STARNET_SANDBOX_FALLBACK=refuse`)은 로컬로 조용히 넘어가지 않고 `sandbox_unavailable` 오류로 거부한다(`execution-router.js`).
`allow`로 바꾸면 로컬로 넘어간다.

### 화면과 통신

에이전트 실행 이벤트(`agent.run.start`, `agent.tool_call`, `agent.run.end` 등)는
`shared/events.js`에 필수 필드가 정의된 이벤트이다.
`GET /api/channels/events`가 SSE로 이를 보내고(`index.js` 14141~14161줄)
프런트엔드(`frontend/app/world.js`)가 구독해 티커, 이름표, 비용을 갱신한다.
SSE는 3초 재연결을 요청하고 25초마다 빈 JSON 메시지로 연결을 유지한다.
실행이 시작되면 에이전트가 책상으로 가고(`goToSeat`, 목표 `work`) 나머지 대기 행동은 장식용 연출이다.
`world.js`의 목표 문자열은 `work`, `awaiting`, `pin`, `post`, `firstwake`, `wander`, `lounge`, `social`, `chase` 등 모두 27종이고
몸의 상태 `state`는 `idle`과 `walk` 둘뿐이다.
27종의 각각이 실행 신호와 얼마나 이어지는지는 하나씩 가르지 않았다.
티커는 실제 이벤트만 한 줄로 서술하며 도구 실패마다 붉은 줄을 쓰지 않는다고 주석이 적는다.
완료 줄은 성공한 실행에만 쓰고 도구 결과나 산출물이 있는 실행만 하루 출하 수를 올린다.
Electron이 아니라 Tauri 2에 Node sidecar를 넣은 구조이다.

sidecar는 `127.0.0.1:8787`에만 열린다(`index.js` 788줄, 13809줄의 `listen`).
`PORT`로 바꿀 수 있다.
`apiauth.js`가 네 겹으로 막는다.
- 호스트 고정: `Host`가 `127.0.0.1`, `localhost`, `::1`이 아니면 거부한다. DNS 재바인딩 방어이다.
- Origin 허용 목록: 루프백 두 개와 Tauri 오리진 네 개이다. 포트 포워딩된 페이지는 Origin과 Host가 같을 때만 허용한다.
- 실행별 토큰: 헤더 `x-starnet-token`(옛 이름 `x-skynet-token`도 허용)에 담고 `timingSafeEqual`로 비교한다. 쿼리 문자열의 마스터 토큰은 거부한다.
- 단기 티켓: 헤더를 달 수 없는 세 요청(파일 열기, SSE, 종료 시 저장 비콘)만 한 요청 범위의 티켓을 쓴다(`apitickets.js`).
토큰이 필요 없는 경로는 `/api/key`, `/api/channels/token`(둘 다 별도 IPC 토큰이 있다), `/api/health`와 OAuth 콜백 두 개뿐이다.
같은 운영체제 사용자로 도는 프로세스는 토큰, 키체인, 데이터 파일을 읽을 수 있고 이는 막지 않는다고 위협 모델 주석이 밝힌다.
`REMOTE_LAN`을 켜면 `0.0.0.0:8797`(사용 중이면 임의 포트)로 열리는데 개발과 시험용 출입구라고 적는다(`index.js` 13081~13110줄).
중계 서버 기본값은 `https://remote.starnetos.com`이고 `STARNET_REMOTE_RELAY=off`로 끈다.
중계 클라이언트는 `remoteStartDoors`가 시작시키며 사용자가 원격을 켤 때만 밖으로 연결한다고 주석이 적는다.
그 호출 경로는 끝까지 추적하지 않았다.

### 원격 접속과 채널

원격 중계(`relay/server.js`)는 휴대폰과 정거장이 모두 밖으로 TLS 연결을 걸고 서로 이어 주는 교환기이다.
정거장은 P-256 키로 서명한 챌린지로 신원을 증명하고 라우팅 id는 공개키 해시이다.
정거장과 휴대폰 사이는 P-256 ECDH, HKDF-SHA256, AES-256-GCM으로 끝에서 끝까지 봉인하며
중계는 누가 누구에게 연결됐는지와 메시지 크기, 시각만 본다고 머리 주석이 적는다(`sidecar/remote/crypto.js`).
휴대폰 알림은 정거장이 VAPID와 aes128gcm으로 직접 각 웹 알림 서비스에 보낸다(`remote/push.js`).
암호 구현의 정확성은 검증하지 않았다.

채널 어댑터는 `channels/registry.js`에 Telegram, Discord, Slack, Matrix, Signal 다섯 개가 등록되어 있다.
Slack은 봇 토큰과 앱 토큰 두 개로 Socket Mode WebSocket을 열고,
Matrix는 임의 홈서버의 `/sync` 장기 조회를 쓰고,
Signal은 별도로 띄운 signal-cli REST 브리지에 연결한다.
무인 채널 대화는 `surface: 'autonomous'`로 돌아 승인이 필요한 변경은 기본 거부되고,
채팅별로 `/approvals on`을 켜면 대화형으로 바뀌어 인라인 버튼으로 묻는다(`index.js` 5084~5090줄 주석).

### 데스크톱 셸과 업데이트

`src-tauri/`는 Tauri 2에 `single-instance`, `updater`, `autostart`, `dialog` 플러그인과 `keyring`을 쓴다.
셸이 sidecar를 띄우고 감시하며(`spawn_guardian`) 10분 창 안에서 연속 6회 비정상 종료하면 재시작을 멈추고 최대 대기는 30초이다.
시작 준비 대기는 60초이다.
웹뷰 CSP의 `connect-src`는 `self`, 루프백, `openrouter.ai`, `api.openai.com`, `chatgpt.com`, `auth.openai.com`, Spotify 두 곳만 허용한다.
기본 창 권한도 이동, 최소화, 닫기 같은 창 조작 위주이다(`capabilities/default.json`).
업데이터는 `latest.json`을 `androoAGI/starnet-releases` 릴리스에서 받으며(`tauri.conf.json`)
공개키는 base64를 풀면 minisign 공개키이다.
프런트엔드 `updates.js`는 켜져 있는 자동 확인으로 6시간마다 확인하고(`updatecore.js`의 `CHECK_INTERVAL_MS`)
알림은 띄우지만 설치는 사용자가 누르는 버튼이 호출한다.
설치 전에는 복구 지점을 만들고 만들지 못하면 설치를 멈춘다(`updates.js` 436~440줄).
macOS 패키지 앱은 시작할 때 `~/.local/bin/starnet` 링크를 만든다.
어떤 셸 프로필에도 `~/.local/bin`이 없을 때만 `~/.zprofile`에 PATH 한 줄을 덧붙인다.
이미 있는 다른 `starnet` 파일은 건드리지 않고 `STARNET_NO_CLI_LINK=1`로 끌 수 있다(`cli-link.js`).

### 테스트가 시험하는 것

`npm test`는 `test:fast`와 `test:http`를 잇는다.
`test/fast.list`는 1,795줄이다.
읽은 시험의 성격은 다음과 같다.
- `test/apiauth.test.js`는 서버를 띄우지 않고 `apiauth.js`의 순수 함수에 단언 71개 안팎을 건다.
  모든 `/api` 경로가 토큰을 요구하는지, 면제 경로가 문서화된 다섯 개뿐인지를 본다.
- `test/permissions.test.js`는 하드라인이 우회보다 아래에 있어도 `.env` 쓰기를 거부하는지,
  자율 실행의 변경이 기본 거부되는지, 허가가 세션 단위인지를 본다.
- `test/fs.jail.test.js`는 실제 임시 폴더에서 `../`, 유닉스 절대 경로, 드라이브 경로, UNC 경로를 거부하는지와 쓰기와 읽기 왕복, 크기 한도를 본다.
- `test/harness.integration.test.js`는 재생 제공자로 웹 검색, 웹 읽기, 파일 쓰기, 최종 답변의 네 단계를 실제 루프에 통과시킨다.
  네트워크와 비용이 없고 도구 이름 규칙과 방 오브젝트-도구 대응 어긋남을 잡는 시험이라고 적는다.
- `test/channels.slack.test.js`, `channels.matrix.test.js`, `channels.signal.test.js`가 있다.
이들은 주입된 가짜 fetch와 WebSocket으로 구동하는 설계이며 실제 서비스에 붙은 시험은 아니다.
시험을 실행하지 않았으므로 통과 여부는 모른다.

## 분석

### 시각화가 아니라 하네스이다

Pixel Agents가 이미 도는 Claude Code를 읽어 캐릭터를 움직이는 것과 달리
StarNet은 모델 호출, 도구 루프, 방 배치 기반 권한, 비용과 기억 저장, 채널, 예약 실행, MCP,
원격 중계까지 직접 갖춘다.
화면은 그 사건을 소비한다.
그래서 이 저장소를 Pixel Agents의 비슷한 도구로 묶는 것은 화면의 겉모양에 한정된다.

### 소스의 완전성

이 저장소는 껍데기가 아니다.
에이전트 런타임, 프런트엔드, Tauri 셸, 중계, 테스트, 릴리스 스크립트가 모두 있고
위 모듈 구성표의 파일과 줄 수는 직접 센 값이다.
`starnet-releases`에는 설치 파일과 `latest.json`만 있다는 서술은 이 클론으로는 확인할 수 없다.
이 저장소에서 확인한 것은 업데이터 주소와 공개키뿐이다.
서명 개인키 파일은 저장소에서 찾지 못했고 워크플로가 `TAURI_SIGNING_PRIVATE_KEY`를 비밀 변수로 읽는다.
크레딧 서비스(StarNet Cloud)는 기기 연결 클라이언트(`credits-link.js`)만 있고 백엔드는 이 저장소에 없다.
`STARNET_CLOUD_URL`이 없으면 연결 경로가 모두 404이다.
실제 빌드는 하지 않았다.

## 비평

### 샌드박스는 약하다

정규식 규칙은 우회 가능성을 열어 두고 호스트 실행이 기본이다.
코드 주석이 스스로 거부 목록은 완전할 수 없다고 인정한다.
기본 프로필 `station-gear`에서 shell은 호스트에서 돈다.
Full Access 우회를 켜면 자율 실행이 변경 작업을 할 수 있다.
다만 완화 장치도 코드에 있다.
하드라인 바닥, 자율 실행의 shell 영구 거부(우회가 꺼져 있을 때), 요청한 docker를 못 쓰면 거부하는 기본 정책, 작업공간 스냅샷, 오염 규칙이다.
이 문서는 그 구성이 실제로 어떤 사고로 이어지는지는 시험하지 않았다.

### 외부에 대한 의존과 변경

자동 업데이트는 minisign 공개키가 고정된 Tauri 업데이터이고 파일은 `starnet-releases`에서 받는다.
확인은 자동이고 설치는 사용자가 누른다.
macOS에서는 `~/.local/bin` 링크를 만들고 프로필에 `~/.local/bin`이 없으면 `~/.zprofile`에 한 줄을 덧붙인다(`cli-link.js`).
`PRIVACY.md`는 텔레메트리가 없다고 하며
Sentry, PostHog, Mixpanel, Segment, Google Analytics, Amplitude, Datadog를 코드 전체에서 찾아도 없다고 적는다.
저장소 전체(웹사이트, 중계, 프런트엔드, Rust 셸 포함)를 `sentry`, `posthog`, `gtag(`, `googletagmanager`, `google-analytics`, `mixpanel`, `plausible.io`로 직접 검색했다.
결과는 아이콘 이름, 시험 문자열, 비밀값 마스킹 시험 목록에 나온 이름뿐이고 SDK 호출이나 스크립트 태그는 없었다.
다만 문자열 검색이므로 웹사이트 코드를 읽어 확인한 것은 아니고 다른 이름의 수집 코드는 배제하지 못한다.
`PRIVACY.md`는 업데이트 확인과 사용자가 고른 제공자 호출 외에, 크레딧을 사면 청구용 계정이 생긴다는 예외를 적는다.
ChatGPT 백엔드와 `claude -p` 어댑터는 제3자 클라이언트 표면에 기댄다.
의존성은 런타임 6개(`@huggingface/transformers`, `ajv`, `kokoro-js`, `node-pty`, `ogg-opus-decoder`, `undici`)이다.
`transformers`와 `kokoro-js`는 오프라인 음성 때문에 필요할 때 동적으로 불러온다(`local-voice.js`).
`main.rs` 머리 주석은 sidecar를 의존성 없는 Node 프로세스라 적는데 이 목록과 맞지 않는다.

### 설명과 코드의 차이

- Slack, Signal, Matrix는 어댑터, 전송, 메시지 변환 코드와 시험 파일이 모두 있다. 라이브 서비스에서의 동작은 확인하지 못했다.
- README(39줄)는 Anthropic, OpenAI, Google 계정 로그인을 지원한다고 적는다. 코드에서 확인한 범위는 다음과 같다.
  OpenAI는 ChatGPT 기기 코드 흐름(`codex`)이다.
  Anthropic은 StarNet이 직접 로그인하지 않고 사용자 `claude` 명령에 위임하며 API 키 방식도 있다.
  Google 모델 제공자 `gemini`는 `api_key`뿐이고 `GEMINI_API_KEY` 등을 읽는다.
  Google OAuth(`mcp/google-client.js`)는 Workspace 커넥터용이며 배포자가 넣는 데스크톱 클라이언트 등록(`STARNET_GOOGLE_DESKTOP_CLIENT_JSON`)이 없으면 쓰지 못한다.
  README의 Google 로그인은 모델 제공자 로그인으로는 코드에서 찾지 못했다.
  이 소비자 로그인 흐름을 실제 계정으로 시험하지는 않았다.
- `output/`이 10,105파일, `docs/`가 1,790파일, `website/`가 16,184파일이어서 웹사이트, 디자인 산출물, 옛 계획서가 소스와 섞여 있다. 전체 파일은 `website/`를 빼도 32,892개이다. `website/app/app/`은 `frontend/app/`의 사본으로 보인다.
- 옛 이름 `skynet`이 키체인 서비스 이름 `ai.skynet.harness`, 헤더 `x-skynet-token`, `SKYNET_*` 환경 변수에 남아 있다. `PRIVACY.md`는 이를 의도한 호환용 별칭이라고 적는다.
- `CODE_MAP.md`의 수치는 낡았다. 문서 자체가 숫자는 어림이라고 적지만 차이가 크다.
  `sidecar/`는 약 2.3만 줄, 82파일이라 적었으나 직접 센 값은 181,802줄, 490파일이다.
  `index.js`는 약 6.5천 줄이라 적었으나 31,987줄이고 `loop.js`는 약 460줄이라 적었으나 3,224줄이다.
  `world.js`는 약 5.6천 줄이라 적었으나 13,030줄이고 `test/`는 약 409파일이라 적었으나 2,204파일이다.

### 규모

sidecar가 약 18만 줄(490파일), 프런트엔드 약 21만 7천 줄,
테스트 약 41만 줄(2,204파일)이고 `index.js` 하나가 31,987줄이다.
CI 워크플로가 14개이다.
이 문서는 테스트를 실행하지 않았다.

## 인사이트

### 가져갈 것

에이전트 감독 화면이 필요하면 관찰 도구를 쓰고,
에이전트를 직접 돌리는 하네스에 시각화가 붙은 형태가 필요하면 이 도구가 대상이다.
쓰기 전에 키체인 접근, 호스트 셸 실행, 자동 업데이트, `~/.zprofile` 수정 네 가지를 점검해야 한다.
점검 때는 `index.js`가 아니라 `permissions.js`, `apiauth.js`, `execution-profiles.js`, `cli-link.js`를 먼저 읽는 편이 빠르다.
앞의 둘과 `cli-link.js`는 결정 규칙이 순수 함수로 분리된 짧은 파일이기 때문이다.

### 확인할 관찰

1. 호스트 셸 실행의 기본값이 격리로 바뀌는지.
2. 텔레메트리 없음 주장이 웹사이트 코드를 읽는 독립 점검에서도 유지되는지.
3. 채널 어댑터와 계정 로그인 흐름이 실제 서비스와 계정에서 동작하는지.
4. 오염 규칙이 실제 호출 지점에서 집행되는지와 우회가 켜진 상태의 사고 사례.

위 넷 모두 이 문서가 확인하지 못했다.
