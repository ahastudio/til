# dmux HTTP API

dmux는 키보드 단축키뿐 아니라
HTTP API로도 제어할 수 있다.
h3 프레임워크 기반의 로컬 서버가
포트 42000~42004에서 실행되며,
0.0.0.0에 바인딩되어
같은 네트워크의 다른 장치에서도 접근 가능하다.

소스 코드: `src/server/` 디렉토리.

<https://github.com/standardagents/dmux>

## API 엔드포인트

소스 코드 분석 결과,
7개 라우트 모듈로 구성되어 있다.

### Panes — 에이전트 pane 관리

| 메서드 | 경로                      | 설명                  |
| ------ | ------------------------- | --------------------- |
| GET    | `/api/panes`              | 전체 pane 목록        |
| GET    | `/api/panes/:id`          | 특정 pane 상세        |
| POST   | `/api/panes`              | 새 pane 생성          |
| GET    | `/api/panes/:id/snapshot` | tmux pane 내용 캡처   |
| PUT    | `/api/panes/:id/test`     | 테스트 상태 업데이트  |
| PUT    | `/api/panes/:id/dev`      | 개발 서버 상태 변경   |

`POST /api/panes`가 핵심이다.
prompt, agent 종류, projectPath를 받아
worktree를 만들고 에이전트를 실행한다.
agent를 지정하지 않으면 시스템 PATH에서
claude, opencode, codex를 자동 탐색한다.
여러 에이전트가 발견되면
`needsAgentChoice: true`와 함께
사용 가능한 에이전트 목록을 반환한다.

```bash
curl -X POST http://localhost:42000/api/panes \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "로그인 버그 수정", "agent": "claude"}'
```

### Keys — 키 입력 전송

| 메서드 | 경로                  | 설명                    |
| ------ | --------------------- | ----------------------- |
| POST   | `/api/keys/:paneId`   | pane에 키 입력 전송     |

단일 키(`key`)와 벌크 텍스트(`text`) 모두 지원.
Ctrl, Alt, Shift 같은 수식키 조합도 가능하다.
tmux `send-keys` 포맷으로 변환하여 전달한다.

```bash
# 단일 키
curl -X POST http://localhost:42000/api/keys/pane-1 \
  -H 'Content-Type: application/json' \
  -d '{"key": "Enter"}'

# 벌크 텍스트
curl -X POST http://localhost:42000/api/keys/pane-1 \
  -H 'Content-Type: application/json' \
  -d '{"text": "yes"}'
```

### Stream — 터미널 출력 스트리밍

| 메서드 | 경로                       | 설명                  |
| ------ | -------------------------- | --------------------- |
| GET    | `/api/stream/:dmuxId`      | SSE로 터미널 출력     |
| GET    | `/api/stream-stats`        | 스트리밍 통계         |

SSE(Server-Sent Events) 방식이다.
메시지 형식은 `TYPE:JSON\n`이며,
타입은 `init`(전체 상태), `patch`(변경분),
`resize`, `heartbeat`(30초), `error`가 있다.
`tmux pipe-pane`으로 출력을 캡처하고
16ms 버퍼링(60fps)으로 전달한다.
2초마다 전체 리프레시로 drift를 보정한다.

### Actions — 액션 실행

| 메서드 | 경로                                    | 설명             |
| ------ | --------------------------------------- | ---------------- |
| GET    | `/api/actions`                          | 전체 액션 목록   |
| GET    | `/api/panes/:id/actions`                | pane 액션 목록   |
| POST   | `/api/panes/:paneId/actions/:actionId`  | 액션 실행        |
| POST   | `/api/callbacks/confirm/:callbackId`    | 확인 응답        |
| POST   | `/api/callbacks/choice/:callbackId`     | 선택 응답        |
| POST   | `/api/callbacks/input/:callbackId`      | 입력 응답        |

에이전트가 확인, 선택, 입력을 요청하면
callback API로 원격에서 응답할 수 있다.
콜백은 인메모리 Map에 저장되며 5분 후
자동 정리된다.

사용 가능한 액션 ID:

| 액션 ID            | 설명                   | 키  |
| ------------------ | ---------------------- | --- |
| `view`             | pane으로 이동          | `j` |
| `close`            | pane 닫기              | `x` |
| `merge`            | main에 병합            | `m` |
| `rename`           | 이름 변경              |     |
| `toggle_autopilot` | 자동 수락 모드 전환    | `a` |
| `run_test`         | 테스트 실행            | `t` |
| `run_dev`          | 개발 서버 시작         | `d` |
| `open_output`      | 출력 보기              | `o` |

`toggle_autopilot`은 에이전트가 위험하지 않은
옵션을 자동 수락하는 모드다.
LLM이 터미널 출력을 분석하여
`potentialHarm.hasRisk`가 false일 때만
자동 수락한다.

### Settings — 세션/설정/훅/로그

| 메서드 | 경로                 | 설명                   |
| ------ | -------------------- | ---------------------- |
| GET    | `/api/session`       | 세션 정보              |
| GET    | `/api/settings`      | 설정 조회              |
| PATCH  | `/api/settings`      | 설정 변경              |
| GET    | `/api/hooks`         | 훅 상태 조회           |
| GET    | `/api/logs`          | 로그 조회 (필터 지원)  |
| POST   | `/api/logs/mark-read`| 로그 읽음 처리         |

설정은 global과 project 두 scope로 나뉜다.
로그는 level, source, paneId로 필터링 가능하다.

### Tunnel — 원격 접근

| 메서드 | 경로            | 설명               |
| ------ | --------------- | ------------------ |
| POST   | `/api/tunnel`   | 터널 생성          |

`untun` 라이브러리 기반으로
터널 기능이 내장되어 있다.
이 API를 호출하면 45초 타임아웃 내에
외부에서 접근 가능한 URL이 생성된다.
별도의 ngrok 설정 없이도 원격 접근이 가능하다.

### Health — 헬스 체크

| 메서드 | 경로           | 설명           |
| ------ | -------------- | -------------- |
| GET    | `/api/health`  | 서버 상태 확인 |

## 이중 인터페이스

dmux에는 두 가지 UI가 있다.

**TUI** — React + Ink 기반 터미널 UI.
`src/DmuxApp.tsx`가 진입점이다.
tmux 안에서 직접 조작할 때 쓴다.

**웹 대시보드** — Vue 3 + Vite 기반.
`frontend/src/`에 있으며
빌드 결과가 TypeScript 문자열로 임베딩된다.

- `/` — 대시보드 (pane 상태 관리)
- `/panes/:id` — 개별 pane 터미널 뷰

두 인터페이스 모두 동일한 HTTP API를 사용한다.
`http://localhost:42000`에 접속하면
웹 브라우저에서 dmux를 조작할 수 있다.
모바일 브라우저에서도 된다.

## Lifecycle Hooks

`src/utils/hooks.ts`에 구현되어 있다.
11가지 훅을 지원한다.

| 훅                       | 시점                     |
| ------------------------ | ------------------------ |
| `before_pane_create`     | pane 생성 직전           |
| `pane_created`           | pane 생성 직후           |
| `worktree_created`       | worktree 생성 직후       |
| `before_pane_close`      | pane 닫기 직전           |
| `pane_closed`            | pane 닫힌 직후           |
| `before_worktree_remove` | worktree 삭제 직전       |
| `worktree_removed`       | worktree 삭제 직후       |
| `pre_merge`              | 병합 직전                |
| `post_merge`             | 병합 직후                |
| `run_test`               | 테스트 실행 시           |
| `run_dev`                | 개발 서버 실행 시        |

### 훅 탐색 우선순위

3단계로 탐색한다:

1. `.dmux-hooks/` — 팀 훅 (버전 관리 대상)
2. `.dmux/hooks/` — 로컬 훅 (gitignore)
3. `~/.dmux/hooks/` — 글로벌 사용자 훅

### 환경 변수

훅 스크립트에 다음 환경 변수가 전달된다:

- `DMUX_ROOT` — 프로젝트 루트
- `DMUX_PANE_ID` — pane 식별자
- `DMUX_SLUG` — pane 슬러그
- `DMUX_BRANCH` — 브랜치 이름
- `DMUX_TARGET_BRANCH` — 병합 대상 브랜치
- `DMUX_WORKTREE_PATH` — worktree 경로
- `DMUX_AGENT` — 에이전트 종류
- `DMUX_PROMPT` — pane 프롬프트
- `DMUX_SERVER_PORT` — HTTP 서버 포트

### 실행 모드

- **비동기** (`triggerHook`) — 백그라운드 실행,
  dmux를 블로킹하지 않음
- **동기** (`triggerHookSync`) — 30초 타임아웃,
  성공 여부와 출력을 반환

## 내부 구조

### Pane 변경 감지

dmux는 두 가지 방식으로
pane 상태 변화를 감지한다.

**tmux 훅 (이벤트 기반).**
tmux 세션에 `after-split-window`,
`pane-exited`, `client-resized`,
`after-select-pane` 훅을 등록한다.
이벤트 발생 시 SIGUSR2 시그널로
dmux 프로세스에 알린다.
100ms 디바운싱으로 이벤트 폭주를 방지한다.

**Worker Thread 폴링 (폴백).**
tmux 훅을 사용할 수 없으면
pane마다 전용 Worker Thread가 돌면서
주기적으로 상태를 확인한다.
최대 3회 자동 재시작(지수 백오프).

### 에이전트 상태 감지

**패턴 매칭** — `"(esc to interrupt)"`
같은 문자열로 working/idle/waiting을 판단.

**LLM 분석** — OpenRouter API를 통해
터미널 출력을 분석한다.
`gemini-2.5-flash`, `grok-4-fast`,
`gpt-4o-mini` 3개 모델을 `Promise.any()`로
병렬 실행하여 첫 성공 응답을 사용한다.
MD5 해시 기반 캐싱(5초 TTL, 최대 100개).

### 아키텍처 다이어그램

```txt
[TUI (Ink/React)]   [웹 (Vue 3)]
        \               /
         \             /
          ▼           ▼
    [h3 HTTP 서버 (42000~42004)]
        │           │
        ▼           ▼
[StateManager] [TmuxService]
    │       │         │
    ▼       ▼         ▼
[JSON]  [Hooks]   [tmux pane]
                      │
                      ▼
                 [worktree]
                      │
                      ▼
   [Worker Thread ←→ AI 에이전트]
        │
        ▼ (OpenRouter)
   [LLM 상태 분석]
```

## 활용 사례

### 모바일에서 에이전트 관리

내장 터널 + 웹 프론트엔드 조합이면
별도 설정 없이 모바일에서 바로 쓸 수 있다.

```bash
# 터널 생성
curl -X POST http://localhost:42000/api/tunnel
# → {"url": "https://xxx.tunnel.dev"}
```

반환된 URL을 모바일 브라우저에서 열면
대시보드가 뜬다. pane 생성, 상태 확인,
키 입력까지 전부 가능하다.

### Slack Bot 연동

Slack slash command → dmux API 호출.
callback API로 에이전트 질문에 응답.
lifecycle hook으로 Slack에 결과 알림.

### CI/CD 자동화

```bash
# 이슈 기반 자동 에이전트 실행
curl -X POST http://localhost:42000/api/panes \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Fix #42", "agent": "claude"}'

# 상태 폴링
curl http://localhost:42000/api/panes/pane-id
```

### 스케줄러

```bash
# crontab: 매일 새벽 2시 기술 부채 정리
0 2 * * * curl -X POST http://localhost:42000/api/panes \
  -d '{"prompt": "TODO 주석 정리하고 PR 생성"}'
```

## 인사이트

**터미널 도구에서 플랫폼으로.**
dmux는 단순한 터미널 도구가 아니라
HTTP API + 웹 프론트엔드 + 터널을 갖춘
에이전트 관리 플랫폼이다.
`POST /api/panes`로 에이전트를 띄우고,
SSE로 출력을 보고,
callback API로 상호작용하는
완전한 원격 제어가 가능하다.

**내장 터널이 게임 체인저.**
`POST /api/tunnel` 한 번이면
외부에서 접근 가능한 URL이 생긴다.
ngrok이나 Cloudflare Tunnel 같은
별도 도구가 필요 없다.
dmux 자체가 원격 접근을 1급 기능으로
지원한다는 뜻이다.

**Callback API로 완전한 원격 상호작용.**
에이전트가 "이 파일을 삭제해도 될까요?"
같은 확인을 요청할 때,
`/api/callbacks/confirm/:id`로
원격에서 응답할 수 있다.
터미널 앞에 앉아 있지 않아도
에이전트와의 대화가 끊기지 않는다.

**어댑터 패턴으로 UI 분리.**
`apiActionHandler.ts`(웹)와
`tuiActionHandler.ts`(터미널)가
동일한 ActionResult를 각 인터페이스에 맞게
변환한다.
새 인터페이스(Slack Bot, CLI 등)를 추가할 때
어댑터만 하나 더 만들면 된다.

## 참고

- [dmux GitHub](https://github.com/standardagents/dmux)
- [소스: src/server/routes/](https://github.com/standardagents/dmux/tree/main/src/server/routes)
- [소스: src/utils/hooks.ts](https://github.com/standardagents/dmux/blob/main/src/utils/hooks.ts)
