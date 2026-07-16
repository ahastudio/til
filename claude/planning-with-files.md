# Planning with Files

<https://github.com/OthmanAdi/planning-with-files>

Claude가 긴 작업 중 목표를 잊어버리거나, 컨텍스트가 리셋되면 진행 상황을
잃어버리는 문제를 해결한다.
컨텍스트 윈도우 대신 파일 시스템에 계획을 저장해서 같은 에러를 반복하지
않게 한다.

## 설치

[File-based Planning Workflow](../ai/file-based-planning-workflow.md) 개념을
구현한 Claude Code 플러그인이다.

v2.4.1 기준으로는 그 개념을 "에이전트가 알아서 잘 지키기를 바라는 관례"가
아니라 hook으로 강제되는 시스템으로 구현했다.

```bash
claude plugins install OthmanAdi/planning-with-files
```

## 사용법

복잡한 작업을 시작할 때 다음 명령을 실행한다.

```bash
/planning-with-files
```

그러면 `task_plan.md`, `findings.md`, `progress.md` 3개 파일이 자동
생성된다.

## 동작 원리

### Hook으로 강제되는 계획 재주입

`PreToolUse` hook이 `Write`·`Edit`·`Bash`·`Read`·`Glob`·`Grep` 호출 전에
`task_plan.md`를 자동으로 출력해 계획을 컨텍스트에 다시 주입하고,
`PostToolUse` hook은 파일이 바뀔 때마다 단계 상태 갱신을 상기시키며, `Stop`
hook은 세션이 끝날 때 완료 여부를 스크립트로 검증한다.
"의사결정 전에 계획을 다시 읽으라"는 권고가, 사람이 지키는 규율에서 도구가
강제하는 시스템으로 바뀐 셈이다.

### 세션 재개 시 자동 점검

새 세션을 시작할 때는 `session-catchup.py` 스크립트가 이전 세션에서
동기화되지 않은 컨텍스트가 있는지 자동으로 점검한다.
`git diff --stat`로 실제 코드 변경을 확인한 뒤 계획 파일을 갱신하고 나서야
작업을 재개하도록 강제하므로, "5-Question Reboot Check"처럼 사람이 수동으로
답하던 체크리스트가 스크립트 한 줄로 자동화된 셈이다.

### 3-Strike 에러 처리 프로토콜

에러 처리는 3-Strike 프로토콜로 구체화되어 있다.
1차 시도는 진단과 수정, 2차는 다른 방법으로 전환, 3차는 가정 자체를
재검토하고, 3회 실패 후에는 반드시 사용자에게 에스컬레이션한다.
"같은 실패를 반복하지 않는다"는 원칙이 `if action_failed: next_action !=
same_action`이라는 명시적 규칙으로 코드화된 것이다.

### TodoWrite는 안티패턴으로 명시된다

가장 눈에 띄는 규칙은 TodoWrite와의 관계다.
지금 널리 쓰이는 에이전트 하네스에는 TodoWrite 같은 휘발성 작업 목록 도구가
기본 내장되어 있는데, 이 플러그인은 이를 안티패턴 1순위로 명시한다.
"지속성을 위해 TodoWrite를 쓰지 말고 `task_plan.md` 파일을 만들라"는
것이다.
파일 시스템을 디스크에, 컨텍스트 윈도우를 RAM에 비유하는 것에서 한 단계
나아가, "휘발성 도구를 지속성 도구로 오용하지 말라"는 명시적 경고가 필요할
만큼 TodoWrite류 도구가 보편화됐다는 뜻이기도 하다.

## 3개 파일 패턴

### task_plan.md - 할 일 목록

```markdown
## Phase 1: Setup

- [x] Initialize project
- [ ] Configure dependencies

## Phase 2: Implementation

- [ ] Core features
- [ ] Testing
```

### findings.md - 발견한 것들

```markdown
## Database Schema

- Users table: id, username, email
- Posts table: id, user_id, title, content

## API Endpoints

- POST /api/users - rate limit 100/min
- GET /api/data - auth required
```

### progress.md - 작업 기록

```markdown
## Session 2025-01-20

### Completed

- Fixed auth bug in login.ts:45
- Added rate limiting

### Next

- Deploy to staging
```
