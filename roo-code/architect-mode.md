# Roo Code - Architect 모드

<https://docs.roocode.com/>

Roo Code는 VS Code용 오픈소스(Apache 2.0) AI 코딩
에이전트 확장이다. Cline에서 포크되었고, 이전 이름은
Roo Cline이었다. 모델 불가지론(Model Agnostic)
— Claude, GPT, Gemini, DeepSeek, Ollama 등
어떤 LLM이든 사용자가 API 키를 가져오는(BYOK)
방식으로 연결한다. 확장은 무료, LLM API 비용만
사용자가 부담한다.

## 왜 Architect 모드인가

AI 코딩 도구의 고질적 문제가 있다.
"코드부터 쓰고 본다." LLM에게 구현을 맡기면
전체 아키텍처와 맞지 않는 코드가 나오고,
에지 케이스를 놓치고, 기술 부채가 쌓인다.

Roo Code는 이 문제를 **도구 접근 권한 수준**에서
해결한다. Architect 모드에서는 코드 파일 편집이
**불가능**하다. 프롬프트로 "계획부터 세워"라고
부탁하는 것과 근본적으로 다르다 — 시스템이
구조적으로 강제한다.

## 모드 시스템 개요

Roo Code의 핵심 혁신은 역할 기반 모드 시스템이다.

| 모드         | 역할                 | 파일 편집   |
| ------------ | -------------------- | ----------- |
| Code         | 코딩, 편집, 리팩터링 | 모든 파일   |
| Architect    | 설계, 계획, 구조     | .md 파일만  |
| Ask          | 질문, 정보 조회      | 불가        |
| Debug        | 버그 진단, 수정      | 모든 파일   |
| Orchestrator | 워크플로우 조율      | 모드에 위임 |

각 모드는 서로 다른 도구 권한을 갖는다. Code 모드는
파일 편집, 터미널, MCP 등 모든 도구에 접근한다.
Architect 모드는 읽기 전용 + 마크다운 편집만 허용된다.
이 제약이 핵심이다.

## Architect 모드 동작 방식

1. 프로젝트 파일을 **읽는다** (코드 구조 파악)
2. .md 파일로 **구현 계획을 작성**한다
3. 다른 파일 형식 편집 시 `FileRestrictionError`
4. 계획에 합의하면 Code 모드로 전환하여 실행

코드 편집이 불가능하므로 모델은 마크다운 형태의
계획을 출력하도록 **강제**된다. 이것이 "사고"
단계를 만들어낸다.

### 모드별 모델 할당

모드마다 서로 다른 LLM을 지정할 수 있다.

- Architect: 추론에 강한 모델 (o3, Gemini 2.5)
- Code: 코딩에 강한 모델 (Claude Sonnet)

비싼 추론 모델은 계획에만 쓰고, 실행에는 효율적인
모델을 쓰는 전략이 가능하다. 비용과 품질을 동시에
최적화할 수 있다.

## 차별점: 타 도구와 비교

| 특성               | Roo Code     | Cursor     |
| ------------------ | ------------ | ---------- |
| 전용 Architect     | 내장         | 없음       |
| 계획/실행 분리     | 도구 권한 수준 강제 | 프롬프트 수준 |
| 모드별 모델 할당   | 지원         | 불가       |
| 커스텀 모드        | 무한 확장    | 불가       |
| 멀티에이전트 조율  | Orchestrator | 없음       |
| 가격               | 무료(+API)   | $20/월     |

| 특성               | Roo Code     | Claude Code |
| ------------------ | ------------ | ----------- |
| 전용 Architect     | 내장         | 없음        |
| 계획/실행 분리     | 도구 권한 수준 강제 | 사용자 재량 |
| 컨텍스트 윈도우    | 모델 의존    | 200K 토큰   |
| 코드베이스 탐색    | VS Code 내   | 터미널 기반 |
| MCP 지원           | 지원         | 지원        |
| 커스텀 모드        | 무한 확장    | Skills      |

Cursor, GitHub Copilot은 단일 에이전트가 계획과
실행을 동시에 수행한다. "계획부터 세워줘"라고
프롬프트할 수 있지만, 모델이 무시할 수도 있다.
Roo Code는 **아키텍처 수준에서 분리를 강제**한다.

Claude Code는 200K 토큰 컨텍스트와 터미널 기반의
깊은 코드베이스 탐색이 강점이지만, 구조화된 모드
전환 시스템은 없다. 접근 방식 자체가 다르다
— Roo Code는 역할 분리, Claude Code는 깊은 추론.

## 인사이트

### 계획과 실행의 분리는 프롬프트가 아니라 구조다

LLM에게 "먼저 계획을 세워"라고 말하는 것과,
계획 외에는 아무것도 할 수 없게 만드는 것은
완전히 다르다. Roo Code의 Architect 모드는
후자다. 표준 Cline 대비 할루시네이션이 약 40%
감소한다는 보고가 이를 뒷받침한다.

### 컨텍스트 윈도우는 유한한 자원이다

모드 분리는 컨텍스트 윈도우도 보호한다.
Architect 모드에서는 설계 관련 정보만,
Code 모드에서는 구현 관련 정보만 다루므로
불필요한 정보로 컨텍스트가 희석되지 않는다.
모델이 "줄거리를 잃을" 가능성이 줄어든다.

### 추론 모델을 안전하게 활용하는 방법

o3, DeepSeek R1 같은 추론 모델은 사고력이
뛰어나지만 실수로 코드를 깨뜨릴 위험이 있다.
Architect 모드에서 사용하면 추론 능력은 최대한
활용하면서 코드 변경 위험은 제거된다.

### Orchestrator는 멀티에이전트의 실험장

Orchestrator 모드는 작업을 하위 작업으로 분해하고
각각을 적절한 모드에 위임한다. 각 하위 작업은
**독립된 컨텍스트**에서 실행되고, 완료 시 요약만
상위로 반환된다. Spec → Architecture → Coding →
Testing → Refinement의 전체 사이클을 자동화할 수
있다.

### 커스텀 모드는 팀의 워크플로우를 코드화한다

Security Reviewer, Test Writer, Documentation
Writer 같은 전문 모드를 만들 수 있다.
`.roomodes` 파일로 프로젝트에 커밋하면 팀 전체가
동일한 AI 워크플로우를 공유한다.
커뮤니티 마켓플레이스에는 171개 이상의 전문
에이전트 설정이 있다.

## MCP 지원

MCP(Model Context Protocol)로 외부 도구와
서비스에 연결한다. 글로벌 설정과 프로젝트 수준
설정을 분리할 수 있고, 모드마다 MCP 접근 권한이
다르다. Architect 모드는 MCP 접근이 제한되고,
Code 모드는 전체 접근이 가능하다.

Memory Bank MCP 서버를 사용하면 프로젝트의
"기억"을 파일 기반으로 저장하여 세션 간 컨텍스트를
유지할 수 있다.

## 실무 권장 사항

- 복잡한 작업은 반드시 Architect 모드에서 시작
- 자신이 이해할 수 없는 작업은 AI에게 맡기지
  말 것 — 코드가 복잡해질수록 AI에게 도움을
  요청하기도 어려워진다
- 각 작업의 범위를 최소한으로 유지 — LLM 응답
  품질은 입력 크기에 반비례한다

## 참고 자료

- [Roo Code Docs](https://docs.roocode.com/)
- [Roo Code GitHub](https://github.com/RooCodeInc/Roo-Code)
- [Using Modes](https://docs.roocode.com/basic-usage/using-modes)
- [Custom Modes](https://docs.roocode.com/features/custom-modes)
- [Boomerang Tasks](https://docs.roocode.com/features/boomerang-tasks)
- [MCP Overview](https://docs.roocode.com/features/mcp/overview)
