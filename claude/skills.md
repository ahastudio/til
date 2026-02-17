# Claude Code Skills

> Skills explained: How Skills compares to prompts, Projects,
> MCP, and subagents

<https://claude.com/blog/skills-explained>

## Skill이란

Skill은 폴더에 담긴 지시문, 스크립트, 리소스의 묶음이다.
Claude가 작업 중 동적으로 발견하고 로드한다.
특정 도메인에 대한 전문 매뉴얼을 Claude에게 제공하는 것과 같다.

실행 가능한 코드가 아니다.
Python이나 JavaScript를 실행하지 않고,
HTTP 서버나 함수 호출도 없다.
Skill은 도메인별 지시를 대화 컨텍스트에 주입하는
특수한 프롬프트 템플릿이다.

## Skill의 동작 원리: 점진적 공개

Skill은 점진적 공개(Progressive Disclosure)로 효율성을
유지한다.

1. 메타데이터 스캔 시 ~100 토큰만 사용
2. 활성화 시 전체 내용 로드 (5,000 토큰 미만)
3. 번들된 리소스는 필요할 때만 로드

실제로 사용하기 전까지는 이름과 설명만 비용이 든다.

## SKILL.md 구조

모든 Skill은 `SKILL.md` 파일이 필요하다.
YAML 프론트매터와 마크다운 본문으로 구성된다.

```yaml
---
name: explain-code
description: >-
  Explains code with visual diagrams and analogies.
  Use when explaining how code works.
---

코드를 설명할 때 항상 포함할 것:

1. **비유로 시작**: 일상적인 것에 비유
2. **다이어그램 그리기**: ASCII 아트로 흐름 표시
3. **코드 워크스루**: 단계별 설명
4. **주의사항 강조**: 흔한 실수나 오해
```

## 프론트매터 필드

| 필드                       | 필수 여부 | 설명                           |
|----------------------------|-----------|-------------------------------|
| `name`                     | 아니오    | 스킬 이름. `/슬래시 명령`이 됨  |
| `description`              | 권장      | 용도 설명. Claude가 판단에 사용 |
| `argument-hint`            | 아니오    | 자동완성 시 인자 힌트           |
| `disable-model-invocation` | 아니오    | `true`면 수동 호출만 가능       |
| `user-invocable`           | 아니오    | `false`면 `/` 메뉴에서 숨김    |
| `allowed-tools`            | 아니오    | 스킬 활성 시 허용할 도구        |
| `model`                    | 아니오    | 스킬 활성 시 사용할 모델        |
| `context`                  | 아니오    | `fork`로 서브에이전트 실행      |
| `agent`                    | 아니오    | `context: fork` 시 에이전트 유형 |

## 저장 위치와 우선순위

| 위치       | 경로                                     | 적용 범위          |
|------------|------------------------------------------|-------------------|
| Enterprise | 관리형 설정                              | 조직 전체 사용자   |
| Personal   | `~/.claude/skills/<name>/SKILL.md`       | 모든 프로젝트      |
| Project    | `.claude/skills/<name>/SKILL.md`         | 해당 프로젝트만    |
| Plugin     | `<plugin>/skills/<name>/SKILL.md`        | 플러그인 활성 시   |

같은 이름이 여러 위치에 있으면 우선순위가 적용된다:
Enterprise > Personal > Project.

## 호출 제어

기본적으로 사용자와 Claude 모두 스킬을 호출할 수 있다.
두 가지 프론트매터 필드로 제어한다.

### disable-model-invocation: true

사용자만 호출 가능하다.
부수 효과가 있는 워크플로에 사용한다.
배포, 커밋, 메시지 전송 등 타이밍 제어가 필요한 작업이다.

### user-invocable: false

Claude만 호출 가능하다.
사용자가 직접 실행할 필요 없는 배경 지식에 사용한다.
레거시 시스템 컨텍스트 같은 참고 정보이다.

| 프론트매터                       | 사용자 | Claude | 컨텍스트 로드 시점          |
|----------------------------------|--------|--------|----------------------------|
| (기본값)                         | O      | O      | 설명은 항상, 본문은 호출 시 |
| `disable-model-invocation: true` | O      | X      | 사용자 호출 시에만          |
| `user-invocable: false`          | X      | O      | 설명은 항상, 본문은 호출 시 |

## 인자 전달

`$ARGUMENTS` 플레이스홀더로 인자를 전달한다.

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

GitHub 이슈 $ARGUMENTS를 코딩 표준에 따라 수정한다.
```

`/fix-issue 123` 실행 시
"GitHub 이슈 123을 코딩 표준에 따라 수정한다"가 된다.

위치별 접근도 가능하다:

- `$ARGUMENTS[0]` 또는 `$0`: 첫 번째 인자
- `$ARGUMENTS[1]` 또는 `$1`: 두 번째 인자

## 스킬 디렉터리 구조

```text
my-skill/
├── SKILL.md           # 핵심 지시문 (필수)
├── template.md        # Claude가 채울 템플릿
├── examples/
│   └── sample.md      # 기대 출력 예시
└── scripts/
    └── validate.sh    # 실행 가능한 스크립트
```

`SKILL.md`는 500줄 이하로 유지한다.
상세한 참조 자료는 별도 파일로 분리한다.

## 동적 컨텍스트 주입

`` !`command` `` 구문으로 셸 명령 결과를 주입한다.
명령이 먼저 실행되고, 출력이 프롬프트에 삽입된다.

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
---

## PR 컨텍스트
- PR diff: !`gh pr diff`
- PR 코멘트: !`gh pr view --comments`
- 변경 파일: !`gh pr diff --name-only`

## 작업
이 PR을 요약한다...
```

이것은 전처리이다.
Claude는 명령 자체가 아닌 최종 결과만 본다.

## Skill vs. 다른 도구 비교

### Skill vs. Prompt

Prompt는 일회성 지시이다.
즉각적이고 대화형이며 반응적이다.

Skill은 반복 사용하는 절차나 전문 지식이다.
Claude가 적절한 시점을 판단하여 적용한다.

같은 프롬프트를 반복해서 입력하고 있다면
Skill로 만들 때이다.

### Skill vs. Project

Project는 특정 작업에 대한 지속적 컨텍스트를 제공한다.
Skill은 작업 수행 방법을 가르친다.

Project가 제품 출시 배경 정보를 담는다면,
Skill은 팀의 글쓰기 표준이나 코드 리뷰 절차를 담는다.

여러 Project에 같은 지시를 복사하고 있다면
Skill로 만들어야 한다.

### Skill vs. Subagent

Subagent는 독립적인 컨텍스트 윈도우, 시스템 프롬프트,
도구 권한을 가진 전문 AI 어시스턴트이다.

Skill과 함께 사용하면 강력하다.
코드 리뷰 서브에이전트가 언어별 모범 사례 Skill을 활용하면
서브에이전트의 독립성과 Skill의 이식 가능한 전문성을
결합할 수 있다.

### Skill + MCP

MCP 지시는 서버와 도구의 올바른 사용법을 다룬다.
Skill 지시는 특정 프로세스나 다중 서버 워크플로에서의
활용법을 다룬다.

이 분리가 아키텍처의 조합 가능성을 유지한다.
하나의 Skill이 여러 MCP 서버를 조율할 수 있고,
하나의 MCP 서버가 수십 개의 Skill을 지원할 수 있다.

## 슬래시 명령과의 관계

커스텀 슬래시 명령이 Skill로 통합되었다.
`.claude/commands/review.md`와
`.claude/skills/review/SKILL.md`는
둘 다 `/review`를 만들고 같은 방식으로 동작한다.

기존 `.claude/commands/` 파일은 계속 동작한다.
Skill은 추가 기능을 제공한다:
보조 파일을 위한 디렉터리, 호출 제어 프론트매터,
Claude의 자동 로드 기능이다.

## 크로스 플랫폼

같은 Skill이 Claude.ai, Claude Code, API에서
수정 없이 실행된다.
Agent Skills 오픈 표준을 따른다.

<https://agentskills.io>
