# OpenAI Symphony

<https://github.com/openai/symphony>

프로젝트 작업을 격리된 자율 구현 실행으로 변환하는
작업 관리 플랫폼.

> Engineers do not need to supervise Codex;
> they can manage the work at a higher level.

엔지니어가 코딩 에이전트를 감독하는 대신,
**작업 자체를 관리**하는 수준으로 올라가게 해준다.

---

## 핵심 개념: 하니스 엔지니어링의 확장

[Codex를 이해하는 방법](./how-to-think-about-codex.md)에서
다룬 Model + Harness + Surfaces 프레임워크를 떠올려보자.

Symphony는 이 구조의 위에 놓인 **오케스트레이션 레이어**다.

```
Symphony (오케스트레이션)
  └─ Orchestrator: 이슈 폴링 + 에이전트 디스패치
       └─ AgentRunner: 턴 기반 실행 루프
            └─ Codex AppServer: JSON-RPC로 Codex 제어
                 └─ Model + Harness (GPT-5.3-Codex)
```

개별 Codex 에이전트를 "실행"하는 게 아니라,
이슈 트래커에서 작업을 가져와 여러 에이전트를 동시에
돌리고, 결과를 검증하고, PR을 머지하는 전체 파이프라인을
자동화한다.

---

## 아키텍처 분석

### 동작 흐름

1. **폴링**: Linear 보드에서 활성 이슈를 주기적으로 가져옴
2. **디스패치**: 우선순위·생성일·식별자 기준으로 정렬 후
   사용 가능한 슬롯에 에이전트 배정
3. **실행**: 각 에이전트가 격리된 워크스페이스에서 턴 기반
   작업 수행
4. **증거**: CI 상태, PR 리뷰, 복잡도 분석, 워크쓰루 제공
5. **통합**: 승인 후 PR 머지

### 핵심 모듈 (Elixir 참조 구현)

| 모듈             | 역할                              |
|------------------|-----------------------------------|
| Orchestrator     | GenServer. 폴링 루프 + 에이전트   |
|                  | 라이프사이클 관리                 |
| AgentRunner      | 이슈 하나의 멀티턴 실행 루프      |
| Codex.AppServer  | Codex와 JSON-RPC 2.0 통신         |
| Workflow         | YAML 프론트매터 + Solid 템플릿    |
|                  | 파싱                              |
| PromptBuilder    | 이슈 데이터로 프롬프트 렌더링     |
| Workspace        | 이슈별 격리된 디렉토리 생성       |
| Tracker          | 어댑터 패턴의 이슈 트래커 추상화  |
| Linear.Client    | GraphQL API로 Linear 연동         |
| StatusDashboard  | Phoenix LiveView 관측성 대시보드  |

---

## 설계 결정의 인사이트

### 1. Elixir/OTP 선택은 우연이 아니다

Erlang/BEAM/OTP는 장시간 실행 프로세스 감독에 최적화된
런타임이다. Symphony의 요구사항과 정확히 맞는다:

- **Supervisor 트리**: 에이전트 프로세스 비정상 종료 시
  자동 재시작
- **Task.Supervisor**: 동시 에이전트를 감독 가능한 태스크로
  실행
- **핫 코드 리로딩**: 에이전트 실행 중 시스템 업데이트
- **경량 프로세스**: 수십 개 에이전트를 OS 스레드 걱정 없이
  동시 실행

GenServer의 `handle_info` 콜백으로 `:tick`(폴링),
`{:DOWN, ...}`(에이전트 종료), `{:codex_worker_update, ...}`
(토큰 사용량) 등 비동기 이벤트를 자연스럽게 처리한다.

### 2. 워크스페이스 격리: Git Worktree가 아닌 디렉토리

Git worktree 대신 **단순 디렉토리 복사** 방식을 채택했다.

- 심볼릭 링크 탈출 방지 (보안 강화)
- 경로 순회(Path Traversal) 검증
- 에이전트 간 완전한 파일시스템 격리
- 이슈 식별자를 `[^a-zA-Z0-9._-]` → `_`로 치환하여
  안전한 디렉토리명 생성

단순하지만 병렬 에이전트 실행에서 Git 잠금 충돌을
원천 차단하는 실용적 선택이다.

### 3. WORKFLOW.md: 코드가 아닌 마크다운으로 정의하는 파이프라인

워크플로우를 `.md` 파일로 정의한다:

```markdown
---
tracker:
  kind: linear
  project_slug: my-project
  active_states: [Todo, In Progress, Merging, Rework]
  terminal_states: [Done, Closed, Cancelled]
polling:
  interval_ms: 5000
agent:
  max_concurrent_agents: 10
  max_turns: 20
codex:
  command: codex-cli --model gpt-5.3-codex
  approval_policy: never
---

[프롬프트 템플릿 - Solid/Liquid 문법]
{{ issue.identifier }}: {{ issue.title }}
```

YAML 프론트매터로 설정, 본문으로 프롬프트 템플릿.
**프로그래밍 없이 워크플로우를 정의하고 버전 관리**할 수
있다. 이슈 상태에 따라 에이전트 행동을 분기하는
상태 기반 라우팅도 템플릿 안에서 처리한다.

### 4. Codex 통신: stdio 위의 JSON-RPC 2.0

Codex AppServer와의 통신은 HTTP/WebSocket이 아닌
**Port(stdio) 기반 JSON-RPC 2.0** 프로토콜이다.

```elixir
Port.open(
  {:spawn_executable, executable},
  [:binary, :exit_status, :stderr_to_stdout,
   args: ["-lc", codex_command],
   cd: workspace, line: @port_line_bytes]
)
```

프로토콜 흐름:

1. `initialize` → 클라이언트 역량 교환
2. `initialized` → 알림
3. 스레드 시작 (승인 정책 + 샌드박스 설정)
4. 턴 실행 (프롬프트 + 이슈 데이터)
5. 턴 완료/실패/취소 이벤트 수신

LSP(Language Server Protocol)와 유사한 설계다.
프로세스 간 통신을 네트워크가 아닌 파이프로 처리하여
레이턴시를 최소화하고 배포를 단순화한다.

### 5. 어댑터 패턴으로 트래커 추상화

`Tracker` 모듈은 5개 콜백을 정의하는 behaviour다:

- `fetch_candidate_issues/0`
- `fetch_issues_by_states/1`
- `fetch_issue_states_by_ids/1`
- `create_comment/2`
- `update_issue_state/2`

현재 Linear 어댑터와 메모리 어댑터(테스트용)가 있다.
Jira, GitHub Issues 등 다른 트래커로 확장하려면
어댑터 하나만 구현하면 된다.

### 6. 멀티턴 실행과 컴팩션

AgentRunner는 재귀적 멀티턴 루프를 실행한다:

- 첫 번째 턴: `PromptBuilder`로 전체 프롬프트 생성
- 이후 턴: "현재 워크스페이스 상태에서 재개하라"는
  간결한 지시
- 매 턴 후 이슈 상태 확인 → 활성이면 계속, 종료면 중단
- `max_turns`로 무한 루프 방지

이전 문서에서 다룬 **컨텍스트 관리**가 여기서 실체화된다.

### 7. 토큰 사용량 추적과 레이트 리밋

Orchestrator가 실시간으로 토큰 델타를 집계한다.
`codex_totals`에 세션별 누적량을,
`codex_rate_limits`에 API 제한 정보를 유지한다.
비용 통제와 관측성을 위한 1급 설계다.

---

## Codex 생태계에서의 위치

```
개발자
  │
  ├─ 직접 사용: CLI, VSCode, 웹 → Codex 하니스 → 모델
  │
  └─ Symphony 사용:
       Linear 이슈 → Symphony Orchestrator
         → N개 Codex 에이전트 병렬 실행
         → PR 생성 → 리뷰 → 머지
```

Symphony는 Codex를 **단일 개발자 도구에서 팀 규모
자동화 시스템으로 확장**하는 레이어다.

---

## 시사점

**에이전트 오케스트레이션의 본질은 프로세스 관리다.**
AI 모델이 아무리 뛰어나도, 여러 에이전트를 동시에
실행하고 실패를 처리하고 상태를 추적하는 것은
전통적인 분산 시스템 문제다. Elixir/OTP 선택이
이를 잘 보여준다.

**작업 관리 > 에이전트 감독.**
Symphony의 핵심 제안은 에이전트를 하나하나 들여다보는
대신 이슈 트래커 수준에서 작업을 관리하라는 것이다.
에이전트는 작업자(worker)이고, 엔지니어는
관리자(manager)가 된다.

**마크다운으로 파이프라인을 정의하는 실험.**
WORKFLOW.md 접근은 대담하다. 코드 없이 에이전트
파이프라인을 정의하고 Git으로 버전 관리한다.
프롬프트 엔지니어링이 곧 파이프라인 엔지니어링이 되는
세계를 보여준다.
