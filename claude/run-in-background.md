# Claude Code — Run in Background

Claude Code는 Bash 명령과 서브에이전트를 백그라운드에서 실행할 수
있다. 장시간 걸리는 작업을 비동기로 처리하면서 메인 대화를 계속
진행할 수 있다.

## 백그라운드 Bash 명령

### 실행 방법

두 가지 방법이 있다.

1. Claude에게 백그라운드 실행을 요청한다.

```text
run npm build in the background
```

2. 실행 중인 Bash 명령에서 `Ctrl+B`를 눌러 백그라운드로 전환한다.
   tmux 사용자는 `Ctrl+B`가 tmux prefix 키와 겹치므로 두 번
   눌러야 한다.

### 동작 원리

백그라운드로 전환하면 고유한 태스크 ID가 즉시 반환된다. 명령은
비동기로 계속 실행되고, 출력은 버퍼에 쌓인다. Claude는
`TaskOutput` 도구로 버퍼된 출력을 가져올 수 있다.

### 적합한 명령

- 빌드 도구: webpack, vite, make
- 패키지 매니저: npm, yarn, pnpm
- 테스트 러너: jest, pytest
- 개발 서버
- 장시간 프로세스: docker, terraform

## 백그라운드 서브에이전트

서브에이전트도 백그라운드에서 실행할 수 있다. Claude가 작업의
성격에 따라 포그라운드/백그라운드를 자동으로 결정하지만, 직접
요청할 수도 있다.

### 포그라운드 vs 백그라운드

| 구분         | 포그라운드        | 백그라운드             |
| ------------ | ----------------- | ---------------------- |
| 메인 대화    | 차단됨            | 계속 진행 가능         |
| 권한 요청    | 사용자에게 전달   | 사전 승인만 사용       |
| 질문         | 사용자에게 전달   | 실패 (계속 진행)       |
| MCP 도구     | 사용 가능         | 사용 불가              |

### 권한 처리

백그라운드 서브에이전트는 시작 전에 필요한 도구 권한을 미리
요청한다. 사전 승인된 권한만 사용하고, 승인되지 않은 권한이
필요하면 해당 도구 호출이 자동 거부된다.

권한 부족으로 실패한 백그라운드 서브에이전트는 포그라운드에서
재개(resume)하여 대화형 권한 요청으로 재시도할 수 있다.

## 태스크 관리

### /tasks 명령

`/tasks` 명령으로 백그라운드 태스크 목록을 확인한다.

### Ctrl+B로 전환

실행 중인 Bash 명령이나 서브에이전트에서 `Ctrl+B`를 누르면
백그라운드로 전환된다. "run this in the background"라고
요청해도 된다.

### 비활성화

백그라운드 기능을 끄려면 환경 변수를 설정한다.

```bash
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1
```

## 참고

- [Background bash commands](https://code.claude.com/docs/en/interactive-mode#background-bash-commands)
- [Run subagents in foreground or background](https://code.claude.com/docs/en/sub-agents#run-subagents-in-foreground-or-background)
