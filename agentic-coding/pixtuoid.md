# Pixtuoid

<https://pixtuoid.dev/>

<https://github.com/pixtuoid/pixtuoid>

HN 토론: <https://news.ycombinator.com/item?id=49039960> (2점, 0개 댓글)

## 소개

Pixtuoid는 실행 중인 AI 코딩 에이전트 세션마다
캐릭터 하나를 픽셀아트 사무실에 두는 Rust 터미널 앱이다.
저장소 설명은 “AI 코딩 에이전트가 살아 움직이는 아늑한 픽셀 사무실”이다.
같은 엔진이 wgpu 데스크톱 창, WASM 캔버스, LAN `serve` 모드로도 돈다.
MIT 라이선스이다.
2026년 11월 25일 GitHub API로 본 별은 580개, 포크는 43개,
생성일은 2026년 5월 21일이고
커밋은 2,130개, 마지막 커밋은 11월 24일, 버전은 0.23.0이다.
`docs/HOW-WE-BUILD.md`는 이 프로젝트를
AI 코딩 에이전트가 한 사람의 소유자를 위해 쓰고 검토하고 유지한다고 밝힌다.

저장소를 받아 `crates/` 아래 코드를 직접 읽어 확인했다.
설치, 빌드, 테스트 실행, 서버 실행은 하지 않았다.
그래서 아래의 동작은 모두 코드를 읽은 결과이고 실행으로 확인한 것이 아니다.
추측한 부분은 추측이라고 적었다.

## 동작 방식

### 구성과 데이터 흐름

`crates/` 아래에 여섯 크레이트가 있다.
줄 수는 각 크레이트의 `.rs` 파일을 테스트까지 합쳐 센 값이다.

| 크레이트             | 줄 수   | 역할                                              |
| -------------------- | ------- | ------------------------------------------------- |
| `pixtuoid-core`      | 98,806  | 소스 해독, 상태 판정, 원격 와이어                 |
| `pixtuoid-scene`     | 101,224 | 배치, 움직임, 그리기 엔진                         |
| `pixtuoid`           | 86,977  | 바이너리: TUI, floating 창, 설치, `serve`, doctor |
| `pixtuoid-hook`      | 2,485   | 에이전트가 부르는 훅 껍데기                       |
| `pixtuoid-web`       | 2,918   | WASM 캔버스 그리기                                |
| `pixtuoid-web-music` | 93      | 사이트용 음악                                     |

`AGENTS.md`는 core와 scene이
터미널, 창, 오디오 장치 크레이트에 기대지 않는다고 적는다.
`deny-arch.toml`이 그 두 크레이트의 의존 허용 목록이다.
`pixtuoid-scene`은 `lib.rs`에 `#![forbid(unsafe_code)]`가 있다.
`unsafe {` 블록은 core에 66곳, 바이너리에 71곳, 훅 껍데기에 22곳 있다.

데이터는 다음 순서로 흐른다.

1. 훅 껍데기가 보낸 줄은 `Transport::Hook`, 대화 기록을 읽은 것은 `Transport::Jsonl` 태그를 단다.
2. 도구별 해독기가 줄을 `AgentEvent`로 바꾼다. 이벤트는 16종이다.
3. 모든 이벤트는 용량 256의 채널 하나로 `reducer_task`에 들어간다(`runtime/pipeline.rs`).
4. 연결하지 않은 도구의 이벤트는 `apply_gated_event`가 버린다(`runtime/gate.rs`).
5. `Reducer::apply`가 `SceneState`를 바꾸고, 값이 달라졌을 때만 `watch` 채널로 게시한다.
6. 1초 간격의 sweep tick이 종료 유예, 오래된 항목 정리, 날짜 변경을 처리한다.
7. 화면은 게시된 `SceneState`를 읽어 그린다.

OpenClaw 같은 마스코트는 `AgentEvent`가 아닌 별도의 존재 채널로 들어간다.
`Reducer::apply`는 거치지 않는다.

### 지원하는 도구와 얻는 방법

`crates/pixtuoid-core/src/source/registry.rs`의 `REGISTRY`에
15개 항목이 있는 것을 확인했다.
항목을 하나씩 열어 보니 아래 분류가 맞았다.

- 훅과 대화 기록 읽기를 모두 쓰는 도구: Claude Code, Codex, Antigravity, omp, Grok.
- 훅만 쓰는 도구: Reasonix, CodeWhale, opencode, Cursor, Hermes, Kimi, Jcode, DeepSeek Harness.
- 대화 기록만 읽는 도구: Copilot(훅이 없다).
- OpenClaw는 책상이 없이 돌아다니는 마스코트로만 나온다.

각 항목은 `SourceDescriptor`이다.
이름, 두 글자 라벨 접두사, 검증한 CLI 버전,
버전 확인 명령, 홈 위치 환경 변수를 가진다.
종류는 책상을 만드는 `Agent`와 마스코트만 만드는 `Daemon` 둘이다.
훅 해독은 두 가지이다.
하나는 Claude Code 모양의 봉투를 함께 쓰는 `Shared`이고,
다른 하나는 도구가 전부 맡는 `ClaimsAll`이다.
한 항목이 훅과 대화 기록 중 하나는 가져야 한다고 주석이 적고 있다.

`SourceCaps`는 도구의 통신 방식에 관한 여섯 가지 사실이다.
종료 신호가 있는지, 다음 프롬프트에 되살아나는지,
위임이 훅에 안 보이는지 등이다.
정리 정책은 이 값에서 계산된다.
종료 신호가 없고 프롬프트로 되살아나는 Codex, opencode, Grok만
5분짜리 짧은 대기 정리를 쓴다.
위임이 훅에 안 보이는 Reasonix, CodeWhale, Cursor, Kimi는
위임 중인 슬롯에 60분을 준다.

설치 방식은 네 갈래이다.
`install/target.rs`의 `Pickup`과 `Primary`로 구분된다.

- 호스트 CLI의 플러그인 명령으로 등록한다: Claude, Codex, Reasonix, Hermes, Antigravity.
- 도구 디렉터리에 통째로 소유하는 파일을 둔다: opencode와 omp의 `.ts`, Grok의 `hooks/pixtuoid.json`.
- 소유 파일과 설정 병합을 함께 쓴다: OpenClaw(`openclaw.json`과 플러그인 폴더), DeepSeek Harness(`.mjs`와 YAML 패치 한 줄).
- 사용자 설정에 항목을 합친다: Cursor, Kimi, Jcode, CodeWhale.

호스트 CLI는 `claude`, `codex`, `hermes`, `agy` 등이다.
한 번 실행에 300초 제한을 두고
넘으면 프로세스 그룹을 죽인다(`install/io.rs`).

살아 있는지는 여러 신호를 겹쳐 확인한다.

- `<claude_home>/sessions/<pid>.json`을 읽고 `kill(pid, 0)`과 시작 시각 비교로 재사용된 pid를 거른다(`cc_probe.rs`). Windows에서는 이 탐사가 항상 실패로 돌아간다.
- Codex는 `codex` 프로세스가 연 롤아웃 파일을 본다. macOS는 `proc_pidinfo`, Linux는 `/proc`를 읽는다(`fd_probe.rs`).
- macOS는 kqueue, Linux는 pidfd, Windows는 프로세스 핸들 대기로 종료를 즉시 알아챈다(`exit_watch.rs`).
- 훅 껍데기가 부모 프로세스를 거슬러 올라가 첫 비셸 조상의 pid를 `_pid`로 찍는다(`cli_pid.rs`). 거슬러 올라가는 횟수는 최대 8번이다.
- 탐사가 사라졌다고 판정하려면 건강한 탐사 두 번이 60초 이상 간격으로 모두 그 세션을 놓쳐야 한다(`NEGATIVE_VOUCH_MIN_SPAN`).

### 대화 기록 읽기

대화 기록은 `notify`로 감시한다(`source/jsonl/root_watch.rs`).
60초 폴링이 백업이다(`DEFAULT_POLL_INTERVAL`).
처음 보는 파일의 최근성 창은 기본 1시간이다.
macOS의 FSEvents는 파일을 닫을 때만 쓰기를 알린다.
그래서 파일을 연 채 쓰는 도구는
파일마다 kqueue를 따로 건다(`jsonl/follow.rs`).
아직 읽지 않은 구간이 1MiB를 넘으면
되풀이하지 않고 건너뛴다(`MAX_PENDING_BYTES`).
도구별 환경 변수로 읽는 위치를 옮길 수 있다.
예를 들어 Claude Code는 `CLAUDE_CONFIG_DIR`, Codex는 `CODEX_HOME`이다.

### 통신

훅 껍데기 `pixtuoid-hook`은 표준 입력의 JSON 한 줄을 읽어
네 키를 찍고 소켓에 쓴다.
찍는 키는 `_shim_ts_ms`, `_pixtuoid_source`,
`_pixtuoid_event`, `_pid`이다(`keys.rs`).
출처는 `--source` 인자가 먼저이고 없으면 `PIXTUOID_SOURCE` 환경 변수이다.
들어온 JSON에 이미 있던
`_pixtuoid_source`와 `_pixtuoid_event`는 찍기 전에 지운다.
표준 입력은 1MiB에서 256바이트를 뺀 만큼만 읽는다.
소켓은 유닉스 소켓이고 Windows에서는 이름 있는 파이프이다.

껍데기의 시간 제한은 200ms이다.
감시 스레드는 표준 입력을 읽은 뒤에 켜진다.
프로세스 표 탐색과 전송을 모두 덮고, 넘으면 종료 코드 0으로 끝낸다.
패닉 훅도 종료 코드 0으로 끝낸다.
`unwrap`, `expect`, `panic!`, 인덱싱은 린트로 막혀 있다.

소켓 쪽 보안은 `source/hook/unix.rs`에서 확인했다.

- 기본 경로는 `$XDG_RUNTIME_DIR/pixtuoid.sock`이고, 없으면 `/tmp/pixtuoid-<uid>/pixtuoid.sock`이다.
- 후자의 디렉터리는 0700으로 만들고, 이미 있으면 소유자와 모드를 검사해 남의 것이면 거절한다.
- 바인드는 `<소켓>.lock`을 `O_NOFOLLOW`로 열어 배타 잠금을 잡은 뒤 한다.
- `<소켓>.tmp`에 바인드하고 0600으로 바꾼 다음 이름을 바꿔 제자리에 놓는다.
- 받는 쪽은 동시 128연결, 연결당 1초, 연결당 2MiB로 제한한다.
- 상대 uid 확인은 연결하는 쪽이 한다. 껍데기는 `/tmp` 기본 경로일 때만 `SO_PEERCRED`나 `getpeereid`로 서버 uid를 확인하고, 두 번째 인스턴스의 구독도 같은 확인을 거친다.
- Windows 파이프는 소유자 전용 DACL(`D:P(A;;GA;;;OW)`)이고 원격 클라이언트를 거절한다.

유닉스의 받는 쪽 코드는 연결한 상대의 uid를 따로 보지 않고 소켓 권한에 맡긴다.
같은 사용자의 다른 프로세스는
소켓에 직접 써서 가짜 이벤트를 보낼 수 있다고 읽힌다(추측).
`reducer_task`의 주석도 `_pixtuoid_source`가
소켓 JSON에서 검증 없이 온다고 적는다.

같은 소켓을 여러 인스턴스가 나눈다.
소켓을 쥔 인스턴스는 받은 줄을
구독한 다른 인스턴스에 그대로 전달한다(밀린 줄은 1,024개까지).
쥔 쪽이 끝나면 구독자가 넘겨받는다(`hook/relay.rs`, `router.rs`).

네트워크로 여는 것은 `serve` 모드뿐이다.

- 기본 포트는 47820이고 IPv4 `0.0.0.0`에 바인드한다(`serve/mod.rs`).
- TLS 핸드셰이크 전에 사설망, 링크 로컬, 루프백이 아닌 주소는 끊는다. Tailscale 대역(`100.64/10`)도 여기서 끊긴다.
- TLS 1.3만 쓰고 클라이언트 인증은 없다. 인증서는 실행마다 자체 서명으로 만들고, 기기는 키의 SPKI 해시만 확인한다.
- 동시 연결은 8개이고, 인사를 마치기 전에는 주소당 한 연결이며, 인사 제한 시간은 5초이다.
- 짝짓기용 코드와 기기 토큰은 난수 32바이트이다. 코드는 5분이고 한 번 쓰면 사라진다.
- 저장은 TLS 키, 코드와 토큰의 SHA-256 해시, 기기 이름이며 상태 디렉터리의 한 파일에 둔다. 테스트가 모드 0600을 검사한다.
- 기기가 보내는 한 줄은 256바이트를 넘으면 연결이 끊긴다. 서버는 15초마다 줄을 쓰고 프레임 사이에 250ms 이상 간격을 둔다.
- 기기가 할 수 있는 요청은 둘이다. 도구 목록 읽기, 그리고 레지스트리에 있는 도구의 연결 또는 해제이다.
- 연결 또는 해제는 서버 전체에서 한 번에 하나만, 앞선 시작에서 1초 이상 지나야 돌며, 실행 직전에 짝지은 기기인지 다시 확인한다.
- 서버가 보내는 에이전트 정보는 `project_agent`의 허용 목록이다. 작업 폴더는 마지막 구성 요소만 나가고 세션 id, 라벨, pid, 권한 요청 사유는 나가지 않는다.
- 이 머신을 로컬 네트워크에 알리는 일은 OS의 mDNS 응답기(`_pixtuoid._tcp`)에 맡기며 서버가 멀티캐스트 소켓을 열지 않는다.

`Cargo.lock`의 594개 패키지 이름에서
`reqwest`, `hyper`, `ureq`, `axum`, `tungstenite` 등을 찾았으나 없었다.
`SECURITY.md`는 바깥으로 나가는 연결과 텔레메트리가 없다고 적는다.
이 점검은 그 서술과 어긋나지 않는다.
다만 서드파티 크레이트 내부의 소켓 사용까지 읽은 것은 아니다.

### 화면과 상태

화면은 `--look`의 기본값 `auto`가 정한다.
터미널이 그래픽 프로토콜(kitty, iTerm2, SIXEL)을 그리면 단면도이고,
아니면 `ratatui`의 반 블록 셀로 그린 클래식이다.
ssh나 GNU screen 안에서는 터미널에 묻지 않고 클래식을 쓴다(`graphics/mod.rs`).
그리기 주기는 초당 30프레임이다(`PAINT_FPS`).
`pixtuoid floating`은 `winit`과 `wgpu`로 그리는 별도 창이다.

활동 상태는 `Idle`, `Running`, `RequiresAction` 셋이다.
종료는 상태가 아니라 슬롯의 `exiting_at` 값이다(`state/mod.rs`, `fsm.rs`).
`Running`은 타이핑, `RequiresAction`은 똑바로 앉은 자세에 표시를 단다.
`Idle`이 앉아서 자는 자세인 것도 확인했다.
자는 자세는 에이전트 id로 정해진다(`pose/mod.rs`, `sim/mod.rs`).
`Idle`인 에이전트는 매 주기 id로 정해진 확률(25~60%)로
자리를 떠나 산책하거나 휴게 지점에 들른다(`pose/pure.rs`).

종료와 정리는 `state/reducer/mod.rs`의 상수로 정해진다.

| 상수                        | 값    | 쓰이는 곳                        |
| --------------------------- | ----- | -------------------------------- |
| `EXIT_GRACE_WINDOW`         | 4.5초 | 종료 후 퇴근 걷기 애니메이션     |
| `STALE_TOOL_TIMEOUT`        | 10분  | 도구 실행 중 침묵                |
| `STALE_IDLE_TIMEOUT`        | 30분  | 대기 중 침묵                     |
| `STALE_SHORT_IDLE_TIMEOUT`  | 5분   | 짧은 대기 정리를 쓰는 도구       |
| `STALE_BLOCKED_TIMEOUT`     | 60분  | 권한 요청과 훅이 안 보이는 위임  |
| `STALE_UNKNOWN_CWD_TIMEOUT` | 3분   | 작업 경로를 모르는 슬롯          |
| `PROOF_OF_LIFE_TTL`         | 150초 | 생존 확인이 정리를 면제하는 시간 |

정리는 `sweep_stale`이 한다.
침묵 시간이 문턱을 넘은 슬롯을 종료 처리하고 하위 슬롯까지 함께 보낸다.
권한 요청 중인 슬롯의 부모와 자식은 정리에서 빠진다.
생존이 확인된 슬롯과 그 위임 하위도 빠진다.
턴이 열려 있는데 도구가 없는 `Running`은 10분과 대기 문턱 중 큰 쪽을 쓴다.
같은 호출을 훅과 대화 기록이 모두 알리면 한 호출 기록에 합쳐진다.
`Transport`의 주석이 그렇게 적고 있다.

### 에러 처리와 격리

- 훅 줄이 JSON이 아니거나 해독에 실패하면 경고만 남기고 다음 줄로 간다(`hook/mod.rs`의 `handle_conn`).
- `accept`가 실패하면 100ms에서 5초까지 늘리는 대기로 다시 시도한다(`hook/unix.rs`).
- 소스가 죽으면 건강 상태 채널로 알려 화면 아래쪽에 띄우고, 화면 쪽 구독자가 멈추면 환원기가 스스로 멈춘다(`reducer_task`).
- 탐사가 실패하면 `None`을 돌려 아무것도 바꾸지 않고, 비어 있는 정상 결과와 구분한다.
- 설정 파일이 읽히지 않으면 설치된 것으로 친다. 없다고 단정하지 않는 쪽으로 틀린다(`install/mod.rs`의 `has_hooks`).
- 외부에서 오는 문자열은 제어 문자를 지우고 80자로 자른다(`display_safe`, `MAX_DECODED_FIELD_CHARS`). 도구 대상은 40자이다.

### 의존성

- 런타임은 `tokio`, 터미널은 `ratatui` 0.30과 `crossterm`, 파일 감시는 `notify` 8이다.
- 종료 감시와 프로세스 조회는 `rustix`와 `libc`로 직접 부른다.
- 창은 `winit` 0.30과 `wgpu` 30이다. 소리는 선택 기능이며 `rodio`로 재생하고 소리 자체는 시작할 때 합성한다.
- `serve`는 `tokio-rustls`(`ring`, TLS 1.3만), `rcgen`, `qrcode`, `whoami`, Linux의 `zbus`(Avahi)를 쓴다.
- 설정 편집은 `toml_edit`, `yaml-edit`, `saphyr`, `preserve_order`를 켠 `serde_json`이다.
- 훅 껍데기는 `serde_json`과 `libc`(Windows는 `windows-sys`)에만 기댄다.
- `deny.toml`은 crates.io 외의 레지스트리와 git 의존을 허용하지 않으며 무시하는 권고 목록이 비어 있다.

## 분석

### 훅이 중심이고 소켓이 경계이다

HTTP 서버 없이 로컬 소켓이 경계이므로 `serve`를 켜기 전에는 열린 포트가 없다.
권한은 소켓 파일 모드와 디렉터리 소유자 검사, 연결하는 쪽의 uid 확인으로 닫힌다.
Pixel Agents가 로컬 HTTP와 토큰으로 막는 것과 다른 선택이다.
도구마다 해독기와 설치기를 두는 방식이라 지원 폭이 넓고
대화 기록은 15개 중 6개 도구에서만 읽는다.

### 도구 수와 유지 비용

15개 도구를 각각 다른 설치 방식으로 지원하므로
도구가 바뀔 때의 유지 비용이 크다.
소유자는 이를 AI 에이전트의 개발과 검토로 감당한다고 문서에 적었다.
새 도구는 `registry.rs`에 행을 더하는 구조이다.
구조체 리터럴이라 빠진 열이 컴파일 오류가 된다고 주석이 적는다.

## 비평

### 설정 쓰기의 범위

다른 도구의 디렉터리에 실행 가능한 플러그인 파일을 두는 것을 확인했다.
`.ts`는 opencode와 omp, `.py`는 Hermes,
`.mjs`는 DeepSeek Harness, `.js`는 OpenClaw이다.
훅 껍데기 경로는 `BinaryStrategy::EmbedAbsolute`인 도구에서
파일 안에 절대 경로로 들어간다.
Claude는 Windows가 아니면 이름만 적어 PATH에 맡긴다.
껍데기를 찾는 순서는 `PIXTUOID_HOOK`, PATH, 실행 파일 옆이다(`install/io.rs`).
PATH가 먼저이므로 설치 시점의 PATH가 오염되면
잘못된 껍데기 경로가 설정에 들어갈 수 있다.
이는 코드에서 따라가 확인한 추론이다.
실행을 시작할 때마다 `converge_owned`가
연결된 도구의 소유 파일 중 이 빌드의 렌더와 다른 것만 다시 쓴다.
연결하지 않은 도구의 파일은 다시 쓰지 않는다.
이전 버전이 남긴 빈 껍데기만 연결과 무관하게 고친다.
설정 병합과 호스트 등록은 `connect`가 받은 동의로만 한다.
시작 때의 재작성에는 넣지 않는다고 주석이 적는다.
끊을 때 소유 파일은 지우지 않고 효과 없는 빈 본문으로 바꾼다.
opencode, omp, Grok은 빈 본문으로 바꾸고
DeepSeek Harness와 OpenClaw는 파일을 그대로 둔다.
omp와 DeepSeek Harness의 코드 주석은 이 잔여를 받아들인다고 적는다.
Claude 등 호스트 CLI 플러그인 도구는
연결과 해제 때 도구 설정에서 껍데기를 실행하는 모든 항목을 지운다.
손으로 쓴 항목도 포함이다.
실행하는 외부 프로그램은 호스트 CLI와 도구별 버전 확인 명령이다.
그 밖에 macOS의 `/bin/ps`와 `scutil`이 있다.
Linux에서는 창 관리자 도구 `swaymsg`, `hyprctl`, `niri`를 쓴다.
터미널 탐사에는 `tmux`를 부른다.
`kill`은 테스트 코드에서만 호출한다.

### 설명과 코드의 차이

- README의 지원 도구 표는 OpenClaw를 다른 도구와 같은 줄에 넣지만 코드에서는 `Daemon` 종류의 마스코트이다. 책상도 슬롯도 만들지 않는다(`source/openclaw.rs`, `source/daemon.rs`).
- 엘리베이터에서 1초 안에 걸어 들어온다는 README 설명을 재는 테스트는 찾지 못했다. 코드의 입장 구간은 최대 4초(`ENTRY_ANIMATION_MS`)이고 껍데기의 전송 한도는 200ms이다. `scripts/pace-check.py`는 프레임 끊김을 재며 도착 지연을 재지 않는다.
- 끝나면 존다는 설명은 일부만 맞다. `Idle` 에이전트는 자는 자세를 하다가 25~60%의 확률로 주기마다 자리를 떠난다. `RequiresAction`은 자지 않고 똑바로 앉는다.
- 포커스 클릭을 확인했다. `FocusChannel::Unsupported`가 Copilot과 Jcode이고 `ServerStamp`가 opencode와 Hermes라서 클릭은 아무 일도 하지 않는다. 나머지는 대화 기록 탐사(Claude, Codex, Grok), 껍데기가 찍은 pid(Antigravity, Reasonix, CodeWhale, Cursor, Kimi), 플러그인이 찍은 pid(DeepSeek Harness, omp)로 창을 찾는다.
- 저장소 `LICENSE`는 MIT인데 npm 패키지와 `pixtuoid`, `pixtuoid-scene` 크레이트는 `MIT AND OFL-1.1`로 적는다. `Cargo.toml` 주석은 scene이 묶는 Fusion Pixel 글꼴이 OFL-1.1이기 때문이라고 설명한다. 어긋남이 아니라 글꼴 라이선스를 더한 표기이다.
- iPhone·iPad 앱은 비공개 저장소에 있다. `docs/HOW-WE-BUILD.md`가 이를 적는다.

### 성숙도

`crates/` 아래를 세어 보니 `#[test]`가 4,918곳, `#[tokio::test]`가 315곳이다.
`crates/` 아래 Rust 코드는 292,503줄이다.
`fuzz/`는 별도 워크스페이스라 이 값에 들어 있지 않다.
통합 시험은 다음을 대상으로 한다.

- 훅 껍데기의 입출력 계약: 항상 종료 코드 0이고 막히지 않는다(`pixtuoid-hook/tests/shim.rs`, Windows 쌍은 `shim_pipe.rs`).
- 껍데기와 데몬이 소켓 경로를 같은 규칙으로 고르는지와 껍데기가 찍는 키가 core의 것과 같은지(`socket_path_parity.rs`, `shim_stamp_parity.rs`).
- 도구별 녹화 캡처를 `harness::Drive`에 흘려 해독 결과가 골든과 같은지(`pixtuoid-core/tests/sources/`). README는 직접 쓴 픽스처를 금하고 시나리오마다 `provenance.json`을 요구한다.
- 환원기의 활동, 수명, 위임, 생존 확인(`tests/reducer/`)과 파일 감시(`tests/watcher/`).
- `pixtuoid serve`를 실제 프로세스로 띄워 TLS 짝짓기와 와이어를 시험한다(`pixtuoid/tests/serve.rs`).
- 레이아웃 골든, 걷기 영역 골든, 픽셀 회귀, 스냅샷 회귀 같은 그림 시험.
- 퍼징 대상은 `fuzz/fuzz_targets`의 hook, remote, transcript 셋이다.

툴체인은 `rust-toolchain.toml`에서 1.100.0으로 고정되어 있다.
`.github/workflows`에 워크플로 파일이 23개 있다.
변경 기록에서 `[**breaking**]` 표시가 붙은 항목은
0.20.0이 51개, 0.21.0이 12개, 0.22.0이 5개, 0.23.0이 12개이다.
0.20.0은 2026년 10월 21일, 0.23.0은 11월 13일 날짜이다.

## 인사이트

### 가져갈 것

터미널에서 일하고 여러 도구를 쓰며
에디터 확장 없이 상태를 보고 싶다면 맞는 선택이다.
열린 포트가 없는 소켓 경계와 짝짓기 기반 LAN 모드는 설계 참고가 된다.
설치가 다른 도구의 설정과 플러그인 디렉터리에 쓴다는 점은 알고 있어야 한다.

### 확인할 관찰

1. 호환을 깨는 변경이 계속되는 속도와 도구별 설치기가 따라가는지.
2. LAN `serve`의 원격 쓰기 권한이 독립 점검에서 어떻게 평가되는지.
3. 사이트 본문의 설명과 코드가 맞는지.

1번은 변경 기록의 표시 수까지만 세었고 설치기가 따라가는지는 확인하지 못했다.
2번은 코드와 `SECURITY.md`의 경계 서술을 읽었을 뿐
독립 점검이 있는지는 확인하지 못했다.
3번은 사이트 본문을 읽지 못해 확인하지 못했다.
