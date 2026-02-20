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
30초마다 heartbeat을 보내서
프록시/방화벽 타임아웃을 방지한다.

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
이것이 모바일 제어의 핵심이다.

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

dmux에 터널 기능이 내장되어 있다.
이 API를 호출하면 외부에서 접근 가능한
URL이 생성된다.
별도의 ngrok 설정 없이도 원격 접근이 가능하다.

### Health — 헬스 체크

| 메서드 | 경로           | 설명           |
| ------ | -------------- | -------------- |
| GET    | `/api/health`  | 서버 상태 확인 |

## 내장 웹 프론트엔드

dmux는 API만 제공하는 것이 아니다.
`frontend/src/`에 대시보드와 터미널 UI가 있다.

- `dashboard.html` / `dashboard.ts` —
  pane 상태를 시각적으로 관리하는 대시보드
- `terminal.html` / `terminal.ts` —
  브라우저에서 pane 터미널 출력을 보는 뷰
- `components/` — UI 컴포넌트

즉, `http://localhost:42000`에 접속하면
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
- `DMUX_WORKTREE_PATH` — worktree 경로

### 실행 모드

- **비동기** (`triggerHook`) — 백그라운드 실행,
  dmux를 블로킹하지 않음
- **동기** (`triggerHookSync`) — 30초 타임아웃,
  성공 여부와 출력을 반환

## 아키텍처

```txt
[브라우저/모바일/Slack Bot/CI]
    │
    ▼ HTTP (포트 42000~42004)
[h3 서버 (src/server/)]
    ├── routes/panesRoutes.ts
    ├── routes/keysRoutes.ts
    ├── routes/streamRoutes.ts (SSE)
    ├── routes/actionsRoutes.ts
    ├── routes/settingsRoutes.ts
    ├── routes/tunnelRoutes.ts
    └── routes/healthRoutes.ts
         │
         ▼
[StateManager] ←→ [TmuxService]
    │                    │
    ▼                    ▼
[설정 파일 (JSON)]   [tmux 세션/pane]
    │                    │
    ▼                    ▼
[Lifecycle Hooks]    [Git worktree]
    │                    │
    ▼                    ▼
[외부 알림]          [AI 에이전트]
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

## 참고

- [dmux GitHub](https://github.com/standardagents/dmux)
- [소스: src/server/routes/](https://github.com/standardagents/dmux/tree/main/src/server/routes)
- [소스: src/utils/hooks.ts](https://github.com/standardagents/dmux/blob/main/src/utils/hooks.ts)
