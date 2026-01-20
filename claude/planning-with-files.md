# Planning with Files

파일 기반 지속적 계획을 적용한 Claude Code 스킬

<https://github.com/OthmanAdi/planning-with-files>

## 소개

Planning with Files는 **Manus-style persistent markdown planning** 워크플로를 구현한 Claude Code 스킬입니다. Meta가 20억 달러에 인수한 Manus AI의 패턴을 기반으로, AI 에이전트가 복잡한 작업을 처리하는 방식을 혁신적으로 개선합니다.

### 핵심 철학

**Context Window = RAM (휘발성, 제한적)**
**Filesystem = Disk (영구적, 무제한)**

중요한 정보는 제한된 컨텍스트에 담지 말고 파일 시스템에 기록해야 합니다.

## 3-File Pattern

복잡한 작업마다 세 개의 마크다운 파일을 생성하여 관리합니다.

### 1. task_plan.md

단계별 목표와 진행 상황을 체크박스로 추적합니다.

```markdown
## Phase 1: Setup
- [x] Initialize project
- [ ] Configure dependencies
- [ ] Set up environment

## Phase 2: Implementation
- [ ] Core features
- [ ] Testing
```

### 2. findings.md

리서치, 발견 사항, 중요한 데이터를 저장합니다.

```markdown
## Database Schema Analysis
- Users table has 5 indexes
- Performance bottleneck in JOIN query
- Migration files in /db/migrations/

## API Endpoints
- POST /api/users - rate limited to 100/min
- GET /api/data - requires authentication
```

### 3. progress.md

세션 로그와 테스트 결과를 기록합니다.

```markdown
## Session 2025-01-20

### Completed
- Fixed authentication bug in login.ts:45
- Added rate limiting middleware
- Updated tests

### Test Results
- Unit tests: 45/45 passed
- Integration tests: 12/12 passed

### Next Steps
- Deploy to staging
- Update documentation
```

## 주요 기능

### 자동 활성화

Hooks(PreToolUse, PostToolUse, Stop)를 통해 Claude가 의사 결정 전에 계획 파일을 자동으로 재확인합니다.

### 세션 복구

컨텍스트 리셋 후에도 동기화되지 않은 작업을 복원할 수 있습니다.

### 멀티 IDE 지원

- Claude Code
- Cursor
- Kilocode
- OpenCode
- Codex
- FactoryAI Droid
- Antigravity

### 에러 지속성

실패 로그를 기록하여 같은 오류를 반복하지 않습니다.

### 크로스 플랫폼

Windows PowerShell과 Unix 셸 스크립트를 모두 지원합니다.

## 설치

### Claude Code Plugin

```bash
claude plugins install OthmanAdi/planning-with-files
```

### 수동 설치

저장소를 클론하여 스킬로 직접 설정할 수 있습니다.

## 사용법

### 명령어로 실행

```bash
/planning-with-files
```

### 자동 실행

Hooks가 활성화되면 복잡한 작업 시작 시 자동으로 계획 파일이 생성됩니다.

## 효과

이 패턴을 사용하면 AI 에이전트의 다음 문제들을 극복할 수 있습니다:

- **목표 표류(Goal drift)**: 작업 중 원래 목표를 잊어버리는 문제
- **불완전한 에러 추적**: 이전에 발생한 오류를 다시 반복하는 문제
- **컨텍스트 손실**: 세션이 리셋되면 진행 상황을 잃어버리는 문제
- **계획 부재**: 체계적인 접근 없이 즉흥적으로 작업하는 문제

## 왜 효과적인가?

1. **명확한 구조**: 세 가지 파일로 정보를 명확히 분류
2. **영구 저장**: 파일 시스템을 활용한 지속적 메모리
3. **자동화**: Hooks를 통한 자동 계획 확인
4. **확장성**: 컨텍스트 윈도우 제한 없이 무한 확장 가능

## 참고

이 프로젝트는 10.3k 스타를 받았으며, AI 에이전트의 한계를 극복하는 구조화된 계획 파일의 효과를 입증했습니다.
