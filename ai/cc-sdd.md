# cc-sdd

> Spec-driven development for your team's workflow

<https://github.com/gotalab/cc-sdd>

<https://www.npmjs.com/package/cc-sdd>

## 개요

cc-sdd는 AI 코딩 에이전트를 위한 Spec-Driven Development(SDD)
도구다. Kiro IDE의 SDD 방식에서 영감을 받아, 요구사항 → 설계 →
작업 → 구현의 구조화된 워크플로를 제공한다.

## 왜 필요한가: Vibe Coding의 한계

AI 코딩의 가장 큰 함정은 "vibe coding"이다.
AI가 겉보기엔 괜찮아 보이는 코드를 생성하지만,
실제로는 요구사항을 충족하지 못하는 현상이다.

cc-sdd는 이 문제를 **명세를 계약(contract)으로** 다루는 것으로
해결한다. AI에게 "알아서 해줘"라고 하는 대신,
먼저 무엇을 만들지 합의하고, 그 합의를 기반으로 구현한다.

## 핵심 인사이트

### 1. 에이전트는 교체 가능하고, 명세는 남는다

cc-sdd는 8개 AI 에이전트를 지원한다 (Claude Code, Cursor,
Gemini CLI, Codex CLI, GitHub Copilot, Qwen Code, OpenCode,
Windsurf). 같은 `.kiro/specs/` 디렉토리의 명세를 모든 에이전트가
공유한다.

이것이 의미하는 바는 명확하다.
**AI 에이전트는 교체 가능한 실행자이고,
명세(spec)가 진짜 자산이다.**
어떤 에이전트를 쓰든 동일한 결과를 기대할 수 있다면,
팀이 투자해야 할 곳은 프롬프트가 아니라 명세다.

### 2. Sprint가 아니라 Bolt

AI-DLC에서는 기존의 Sprint(주 단위 반복) 대신
"Bolt"라는 개념을 쓴다.
수 시간~수 일의 집중적인 사이클로 기능을 완성한다.

기존 개발 시간의 70%가 회의, 문서화, 컨텍스트 전환에 소비된다.
cc-sdd는 이 행정 오버헤드를 AI가 처리하게 하고,
사람은 **검증(validation)에만 집중**하게 한다.

### 3. AI 실행 + 사람 검증 = 게이트 패턴

cc-sdd의 워크플로에는 모든 단계마다 "게이트"가 있다.
AI가 요구사항을 생성하면 사람이 검토하고,
AI가 설계를 만들면 사람이 승인하고,
AI가 작업을 분해하면 사람이 확인한다.

```txt
AI 실행 → 사람 검증 → AI 실행 → 사람 검증 → ...
```

이것은 "AI를 믿지 않겠다"가 아니라,
**"AI의 출력물에 대한 책임은 사람이 진다"는 설계 원칙**이다.
`-y` 플래그로 자동 승인할 수 있지만,
프로덕션에서는 수동 승인을 권장한다.

### 4. Project Memory로 무상태(stateless) 문제 해결

AI 에이전트의 근본적 한계는 세션 간 컨텍스트를 잃는 것이다.
cc-sdd의 `steering` 명령어는 아키텍처, 기술 스택, 도메인 지식을
`.kiro/steering/*.md` 파일로 영속화한다.

모든 명령어가 이 파일을 참조하므로,
AI가 매 세션마다 "이 프로젝트가 뭔가요?"라고 묻지 않는다.
**컨텍스트의 영속화가 AI 에이전트 활용의 핵심이다.**

### 5. Brownfield가 진짜 어려운 문제

Greenfield(신규 프로젝트)에서 AI를 쓰는 건 비교적 쉽다.
기존 코드와 충돌할 일이 없으니까.
하지만 현실의 대부분은 Brownfield(기존 프로젝트)다.

cc-sdd가 v2에서 `validate-gap`과 `validate-design` 명령어를
추가한 이유가 여기에 있다.
기존 코드와 새 요구사항의 갭을 분석하고,
설계가 기존 아키텍처와 호환되는지 검증한다.

```txt
Greenfield: spec-init → requirements → design → tasks → impl
Brownfield: spec-init → requirements → validate-gap
            → design → validate-design → tasks → impl
```

**AI 도구가 Brownfield 지원을 얼마나 잘 하느냐가
실전 활용 가능성을 결정한다.**

### 6. 발견(Research)과 결정(Design)의 분리

v2에서 `research.md`와 `design.md`를 분리한 것은
사소한 변경이 아니다.

탐색 과정의 모든 발견 사항(research.md)과
최종 결정(design.md)은 서로 다른 독자를 위한 것이다.
리뷰어는 최종 결정만 보면 되고,
나중에 "왜 이렇게 결정했지?"라는 질문이 나오면
research.md를 참조하면 된다.

**AI가 생성하는 문서도 "읽는 사람"을 고려해야 한다.**

### 7. 템플릿 = 조직 수준의 프롬프트 엔지니어링

개인이 프롬프트를 잘 쓰는 것과
조직이 일관된 결과를 내는 것은 다른 문제다.

cc-sdd의 `templates/`와 `rules/` 디렉토리는
**팀 전체의 AI 출력물을 표준화하는 메커니즘**이다.
한 번 정의하면 모든 에이전트, 모든 세션에서
동일한 형식과 기준으로 문서가 생성된다.

이것은 개인의 프롬프트 스킬에 의존하지 않고,
**조직의 품질 기준을 코드화(codify)하는 것**이다.

### 8. EARS 형식: 요구사항에 형식이 필요한 이유

cc-sdd는 요구사항을 EARS(Easy Approach to Requirements
Syntax) 형식으로 작성한다:

- `WHEN <트리거> THE <시스템> SHALL <동작>`
- `IF <조건> THEN THE <시스템> SHALL <동작>`

자연어 요구사항은 모호하다.
"사용자가 로그인할 수 있어야 한다"는 테스트할 수 없다.
EARS 형식은 요구사항을 **테스트 가능한 문장**으로 만든다.

AI에게 "알아서 요구사항 써줘"라고 하면 모호한 문장이 나온다.
형식을 강제하면 구체적이고 검증 가능한 문장이 나온다.
**AI 출력물의 품질은 형식(format)이 결정한다.**

### 9. 병렬 Wave 분해: P0/P1+

작업을 분해할 때 단순히 순서만 매기는 게 아니라,
**병렬 실행 가능 여부를 명시적으로 태깅**한다.

- P0: 직렬 실행 (선행 의존성 있음)
- P1+: 병렬 실행 가능

이것은 단순한 작업 관리를 넘어,
**AI 에이전트의 병렬 실행을 위한 의존성 그래프**다.
Subagent 모드에서 여러 작업을 동시에 실행할 수 있는 근거가
이 태깅에서 나온다.

## Quick Start

```bash
cd your-project
npx cc-sdd@latest --claude --lang ko
```

13개 언어를 지원한다 (en, ja, ko, zh-TW 등).

## 주요 명령어

### Steering (컨텍스트 수집)

| 명령어                  | 설명                          |
|-------------------------|-------------------------------|
| `/kiro:steering`        | 프로젝트 메모리 생성/갱신     |
| `/kiro:steering-custom` | 도메인 특화 steering 문서작성 |

### Spec 워크플로

| 명령어                    | 설명                       |
|---------------------------|----------------------------|
| `/kiro:spec-init`         | 기능 스펙 디렉토리 초기화  |
| `/kiro:spec-requirements` | EARS 형식 요구사항 생성    |
| `/kiro:spec-design`       | 기술 설계 문서 생성        |
| `/kiro:spec-tasks`        | 구현 작업 분해 (병렬 wave) |
| `/kiro:spec-impl`         | TDD 방식 구현 실행         |
| `/kiro:spec-quick`        | 위 단계를 한 번에 실행     |

### 검증 명령어

| 명령어                    | 설명                       |
|---------------------------|----------------------------|
| `/kiro:validate-gap`      | 기존 코드 대비 갭 분석     |
| `/kiro:validate-design`   | 설계 품질 검증             |
| `/kiro:validate-impl`     | 구현 결과 검증             |
| `/kiro:spec-status`       | 진행 상황 확인             |

## 참고 자료

[Kiroの仕様書駆動開発プロセスをClaude Codeで徹底的に再現した - Zenn](https://zenn.dev/gotalab/articles/3db0621ce3d6d2)

[Claude Codeは仕様駆動の夢を見ない - Speaker Deck](https://speakerdeck.com/gotalab555/claude-codehashi-yang-qu-dong-nomeng-wojian-nai)

[Kiro IDE](https://kiro.dev)

[Spec-Driven Development](../ai/spec-driven-development.md)
