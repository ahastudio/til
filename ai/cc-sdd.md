# cc-sdd

> Spec-driven development for your team's workflow

<https://github.com/gotalab/cc-sdd>

<https://www.npmjs.com/package/cc-sdd>

## 개요

cc-sdd는 AI 코딩 에이전트를 위한 Spec-Driven Development(SDD) 도구다.
Kiro IDE의 SDD 방식에서 영감을 받아, 요구사항 → 설계 → 작업 → 구현의
구조화된 워크플로를 제공한다.

개발 시간의 70%를 회의, 문서화, 흩어진 컨텍스트에 소비하는 문제를
해결하기 위해 만들어졌다.
AI-DLC(AI-Driven Development Lifecycle) 기반으로 기능 기획을
체계적으로 진행할 수 있다.

## 지원 에이전트

8개의 AI 에이전트를 하나의 워크플로로 통합한다:

- Claude Code (Commands / Subagents)
- Cursor
- Gemini CLI
- Codex CLI
- GitHub Copilot
- Qwen Code
- OpenCode
- Windsurf

## Quick Start

```bash
cd your-project
npx cc-sdd@latest --claude --lang ko
```

13개 언어를 지원한다 (en, ja, ko, zh-TW 등).

## 워크플로

### Greenfield (신규 프로젝트)

```txt
steering → spec-init → spec-requirements
→ spec-design → spec-tasks → spec-impl
```

### Brownfield (기존 프로젝트)

```txt
steering → spec-init → spec-requirements
→ validate-gap → spec-design
→ validate-design → spec-tasks → spec-impl
```

## 주요 명령어

### Steering (컨텍스트 수집)

| 명령어                  | 설명                          |
|-------------------------|-------------------------------|
| `/kiro:steering`        | 프로젝트 메모리 생성/갱신     |
| `/kiro:steering-custom` | 도메인 특화 steering 문서작성 |

### Spec 워크플로

| 명령어                   | 설명                       |
|--------------------------|----------------------------|
| `/kiro:spec-init`        | 기능 스펙 디렉토리 초기화  |
| `/kiro:spec-requirements`| EARS 형식 요구사항 생성    |
| `/kiro:spec-design`      | 기술 설계 문서 생성        |
| `/kiro:spec-tasks`       | 구현 작업 분해 (병렬 wave) |
| `/kiro:spec-impl`        | TDD 방식 구현 실행         |

### 검증 명령어

| 명령어                   | 설명                       |
|--------------------------|----------------------------|
| `/kiro:validate-gap`     | 기존 코드 대비 갭 분석     |
| `/kiro:validate-design`  | 설계 품질 검증             |
| `/kiro:validate-impl`    | 구현 결과 검증             |
| `/kiro:spec-status`      | 진행 상황 확인             |

## Spec-Driven Development 단계

1. **Steering** - 아키텍처, 기술 스택, 제품 컨텍스트 수집
2. **Spec Init** - 기능별 워크스페이스 생성
   (`.kiro/specs/<feature>/`)
3. **Requirements** - EARS 형식의 테스트 가능한 요구사항 작성
4. **Design** - 요구사항을 기술 설계로 변환
   (Mermaid 다이어그램 포함)
5. **Tasks** - 설계를 구현 가능한 작업으로 분해
   (P0: 직렬, P1+: 병렬 가능)
6. **Implementation** - TDD 사이클로 구현
   (RED → GREEN → REFACTOR)
7. **Validation** - 요구사항 대비 구현 검증

각 단계마다 사람의 승인을 위한 게이트가 있다.
`-y` 플래그로 자동 승인할 수 있지만,
프로덕션 작업에서는 수동 승인을 권장한다.

## 커스터마이징

`.kiro/settings/` 디렉토리에서 팀에 맞게 조정할 수 있다:

- `templates/` - 문서 구조 정의
  (requirements, design, tasks)
- `rules/` - AI 생성 원칙 및 판단 기준 정의

## 참고 자료

[Kiroの仕様書駆動開発プロセスをClaude Codeで徹底的に再現した - Zenn](https://zenn.dev/gotalab/articles/3db0621ce3d6d2)

[Claude Codeは仕様駆動の夢を見ない - Speaker Deck](https://speakerdeck.com/gotalab555/claude-codehashi-yang-qu-dong-nomeng-wojian-nai)

[Kiro IDE](https://kiro.dev)

[Spec-Driven Development](../ai/spec-driven-development.md)
