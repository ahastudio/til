# GitHub Agentic Workflows

자연어 마크다운으로 에이전틱 워크플로우를 작성하고,
GitHub Actions에서 실행할 수 있게 해주는 도구.

저장소: <https://github.com/github/gh-aw>

문서: <https://github.github.com/gh-aw/>

## 개요

GitHub Agentic Workflows는 Actions + Agent + Safety를
결합한 자동화 프레임워크다.
기존의 고정된 if-then 자동화 대신,
AI 에이전트가 컨텍스트를 이해하고 상황에 맞는
판단을 내려 작업을 수행한다.

마크다운 파일에 자연어로 지시사항을 작성하면,
컴파일러가 이를 보안이 강화된 GitHub Actions YAML
(`.lock.yml`)로 변환하여 실행한다.

## 설치

`gh` CLI 확장으로 설치한다.

```bash
gh extension install github/gh-aw
```

## 주요 CLI 명령어

| 명령어          | 설명                              |
|-----------------|-----------------------------------|
| `gh aw init`    | 저장소 초기 설정                  |
| `gh aw add`     | 워크플로우 가져오기               |
| `gh aw new`     | 워크플로우 템플릿 생성            |
| `gh aw compile` | 마크다운을 YAML로 컴파일          |
| `gh aw run`     | 워크플로우 즉시 실행              |
| `gh aw trial`   | 임시 저장소에서 테스트            |
| `gh aw logs`    | 실행 로그 확인                    |
| `gh aw audit`   | 실행 상세 분석                    |
| `gh aw status`  | 워크플로우 상태 확인              |
| `gh aw secrets` | 시크릿 관리                       |

## 워크플로우 파일 구조

`.github/workflows/` 디렉토리에 마크다운 파일로
작성한다.
파일은 YAML 프론트매터(설정)와
마크다운 본문(자연어 지시사항) 두 부분으로 구성된다.

```markdown
---
description: 매일 저장소 상태를 요약합니다
on:
  schedule:
    - cron: "0 9 * * 1-5"
permissions:
  issues: write
engine: copilot
tools:
  bash: ["gh issue list", "gh pr list"]
safe-outputs:
  - issues
---

# Daily Repo Status

저장소의 현재 상태를 분석하고 요약하세요.

## 포함할 내용

- 열린 이슈와 PR 현황
- 최근 머지된 PR 목록
- 주요 논의 사항 요약

## 출력 형식

분석 결과를 이슈로 생성하세요.
```

## 프론트매터 주요 필드

- `on` - 트리거(trigger) 설정.
  퍼지(fuzzy) 구문도 지원한다
  (`on: daily`, `on: weekly on monday`).
- `permissions` - 접근 권한.
  명시하지 않은 권한은 `none`으로 설정된다.
- `engine` - AI 엔진 선택
  (Copilot, Claude, Codex).
- `tools` - 사용 가능한 도구
  (bash, edit, github, web-fetch 등).
- `safe-outputs` - 에이전트의 쓰기 작업 대상
  (issues, pull-requests 등).
- `roles` - 워크플로우를 트리거할 수 있는 역할.
- `network` - 네트워크 접근 제어.
- `strict` - 강화된 검증 모드 (기본값: `true`).

## 보안 아키텍처

다층 방어(Defense-in-Depth) 구조를 채택한다.

### 핵심 원칙

- **읽기 전용 기본값**: 에이전트는 기본적으로
  쓰기 권한이 없다.
- **Safe Outputs**: 쓰기 작업은 별도의
  권한 제어 잡(job)에서 실행된다.
  에이전트가 구조화된 출력으로 작업을 요청하면,
  검증 후 별도 잡이 수행한다.
- **샌드박스 실행**: 네트워크 격리, 입력 살균,
  도구 허용 목록(allowlist) 적용.
- **SHA 고정 의존성**: 공급망 보안을 위해
  액션을 SHA로 고정한다.
- **위협 탐지**: 에이전트 실행 후
  보안 분석 잡이 출력을 검사한다.

### Agent Workflow Firewall (AWF)

에이전트를 컨테이너화하고 Squid 프록시를 통해
도메인 허용 목록 기반으로 네트워크를 제어한다.

### MCP Gateway

Model Context Protocol(MCP) 서버를 격리된
컨테이너에서 실행하여 도구 접근을 제어한다.

## 활용 사례

- 이슈 분류(triage) 및 라벨링
- 코드 리뷰 자동화
- 일간/주간 저장소 상태 리포트
- 릴리스 관리
- 의존성 모니터링
- 코드 개선 및 리팩토링

## 관련 프로젝트

- [Agent Workflow Firewall](https://github.com/github/agent-workflow-firewall)
  \- AI 에이전트의 네트워크 이그레스(egress) 제어
- [MCP Gateway](https://github.com/github/mcp-gateway)
  \- MCP 라우팅을 위한 통합 HTTP 게이트웨이
