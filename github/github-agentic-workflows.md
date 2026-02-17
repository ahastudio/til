# GitHub Agentic Workflows

마크다운에 자연어로 지시사항을 쓰면, AI 에이전트가 GitHub Actions 위에서
실행한다. YAML을 직접 작성할 필요 없이 "무엇을 해줘"라고 쓰면 된다.

<https://github.com/github/gh-aw>

## 5분 안에 시작하기

```bash
# 설치
gh extension install github/gh-aw

# 저장소에 워크플로우 추가 (위자드가 안내)
gh aw add-wizard githubnext/agentics/daily-repo-status

# 바로 실행해보기
gh aw run daily-repo-status
```

위자드가 AI 엔진 선택(Copilot, Claude, Codex), 시크릿 설정, 워크플로우 배포까지
안내한다. 실행하면 저장소 활동을 분석한 리포트가 이슈로 생성된다.

## 바로 쓸 수 있는 워크플로우

`gh aw add-wizard`로 추가하면 바로 동작한다.

### 매일 저장소 리포트

```bash
gh aw add-wizard githubnext/agentics/daily-repo-status
```

열린 이슈, PR 현황, 최근 머지 등 저장소 상태를 매일 이슈로 정리해준다.

### 이슈 자동 분류

```bash
gh aw add-wizard githubnext/agentics/issue-triage
```

새 이슈가 올라오면 내용을 읽고 적절한 라벨을 붙여준다.

### CI 실패 자동 조사

```bash
gh aw add-wizard githubnext/agentics/ci-doctor
```

CI가 실패하면 로그를 분석하고 원인과 해결 방법을 코멘트로 남긴다.

### PR 자동 수정

```bash
gh aw add-wizard githubnext/agentics/pr-fix
```

CI 체크가 실패한 PR에 `/fix`를 코멘트하면 에이전트가 코드를 고쳐서 커밋한다.

### 주간 리서치

```bash
gh aw add-wizard githubnext/agentics/weekly-research
```

관련 업계 동향과 기술 트렌드를 매주 조사해서 정리한다.

### 그 외

- **daily-plan** - 이슈 기반 일일 계획 수립
- **daily-team-status** - 팀 활동 요약
- **repo-ask** - `/ask`로 저장소에 대해 질문
- **code-simplifier** - 코드 가독성 개선
- **test-coverage-improver** - 테스트 커버리지 확대
- **dependabot-pr-bundler** - Dependabot PR 통합

전체 목록: <https://github.com/githubnext/agentics>

## 직접 워크플로우 만들기

`.github/workflows/`에 마크다운 파일을 만든다. 프론트매터에 설정, 본문에 자연어
지시사항을 쓴다.

```markdown
---
description: PR에 접근성 리뷰를 수행합니다
on:
  pull_request:
    types: [opened, synchronize]
engine: copilot
tools:
  bash: ["gh pr diff"]
safe-outputs:
  - pull-request-reviews
---

# Accessibility Review

이 PR의 변경사항에서 접근성 문제를 확인하세요.

## 확인 항목

- alt 텍스트 누락
- 색상 대비 부족
- 키보드 네비게이션 지원 여부
- ARIA 속성 적절성

## 결과

문제가 있으면 PR 리뷰 코멘트로 남기세요. 문제가 없으면 승인하세요.
```

```bash
# 마크다운 → YAML 컴파일
gh aw compile

# 테스트 (임시 저장소에서 안전하게)
gh aw trial accessibility-review

# 커밋 & 푸시
git add .github/workflows/accessibility-review.*
git push
```

## 트리거 패턴

### 스케줄 (정기 실행)

```yaml
# 퍼지 구문 - 시간을 자동 분산
on: daily
on: weekly on monday

# 크론 구문
on:
  schedule:
    - cron: "0 9 * * 1-5"
```

### 이벤트 (이슈/PR)

```yaml
on:
  issues:
    types: [opened, labeled]

on:
  pull_request:
    types: [opened, synchronize]
```

### 슬래시 커맨드 (ChatOps)

```yaml
on:
  slash_command:
    name: review
    events: [pull_request_comment]
```

이슈나 PR에 `/review`를 코멘트하면 실행된다.

## 코딩 에이전트로 워크플로우 생성

직접 마크다운을 쓰지 않아도 된다. 코딩 에이전트에게 다음과 같이 프롬프트하면
워크플로우를 생성해준다.

```
Create a workflow for GitHub Agentic Workflows
using https://raw.githubusercontent.com/github/gh-aw/main/create.md

The purpose of the workflow is to automatically
review PRs for security vulnerabilities.
```

## 보안

에이전트는 기본적으로 읽기 전용이다. 쓰기 작업은 Safe Outputs라는 구조를 통해
별도 잡(job)에서 검증 후 실행된다. 에이전트가 직접 저장소를 수정할 수 없다.

- 네트워크 격리 및 도메인 허용 목록
- 의존성 SHA 고정
- 위협 탐지 잡이 출력을 사전 검사
- `roles` 필드로 실행 권한 제한 가능
