# Planning with Files

<https://github.com/OthmanAdi/planning-with-files>

Claude가 긴 작업 중 목표를 잊어버리거나,
컨텍스트 리셋되면 진행 상황을 잃어버리는 문제를 해결합니다.
컨텍스트 윈도우 대신 파일 시스템에 계획을 저장해서
같은 에러를 반복하지 않게 합니다.

## 설치

```bash
claude plugins install OthmanAdi/planning-with-files
```

## 사용법

복잡한 작업 시작할 때:

```bash
/planning-with-files
```

그러면 3개 파일이 자동 생성됩니다.

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
