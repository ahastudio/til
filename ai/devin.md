# Devin - AI Software Engineer

<https://devin.ai/>

Cognition이 만든 자율형 AI 소프트웨어 엔지니어.
2024년 3월에 처음 공개되었고,
2024년 12월에 정식 출시(GA)되었다.

## Cognition

<https://cognition.ai/>

Scott Wu가 설립한 AI 스타트업.
"AI teammates"를 만드는 것을 목표로 한다.

## 주요 특징

### 자율적 개발 환경

Devin은 자체적으로 샌드박스 환경을 갖추고 있다.
쉘(Shell), 코드 에디터, 웹 브라우저를
하나의 환경 안에서 직접 사용한다.
사람이 컴퓨터 앞에서 작업하는 것처럼
필요한 도구를 스스로 전환하며 작업을 수행한다.

### 계획 수립과 실행

작업 지시를 받으면 단계별 계획(Plan)을
스스로 수립하고, 계획에 따라 실행한다.
진행 상황을 타임라인으로 보여주며,
사용자는 중간에 개입하거나 방향을 수정할 수 있다.

### 풀스택 개발

프론트엔드, 백엔드, 인프라를 가리지 않고
다양한 기술 스택으로 작업할 수 있다.
새 프로젝트 세팅, 기존 코드베이스 수정,
버그 수정, 리팩터링 등을 처리한다.

### 외부 도구 학습

Devin에게 문서 URL이나 가이드를 제공하면
해당 내용을 읽고 학습하여 작업에 적용한다.
익숙하지 않은 기술이나 사내 도구도
문서를 통해 사용법을 파악할 수 있다.

### Git/GitHub 연동

GitHub 저장소와 직접 연동되어
브랜치 생성, 커밋, PR 생성까지 자동으로 수행한다.
기존 PR에 대한 코드 리뷰 반영이나
GitHub Issue를 할당받아 처리하는 것도 가능하다.

### Slack 통합

Slack에서 Devin을 멘션하여 작업을 요청할 수 있다.
대화 형식으로 지시를 주고받으며,
작업 완료 시 결과를 Slack으로 알려준다.
별도 대시보드 없이 팀 워크플로에 자연스럽게 녹아든다.

### 세션 기반 작업

각 작업은 독립된 세션(Session)으로 관리된다.
세션마다 별도의 실행 환경이 생성되어
여러 작업을 동시에 병렬로 진행할 수 있다.
세션의 스냅샷(Snapshot)을 통해
특정 시점의 환경 상태를 재현할 수도 있다.

## Claude Code와 비교

Devin과 [Claude Code](../claude/claude-code.md)는
모두 AI 코딩 에이전트이지만 접근 방식이 다르다.

### 작업 방식

Devin은 **비동기(Asynchronous)** 중심이다.
작업을 맡기면 Devin이 독립적으로 수행하고
완료 후 결과(PR 등)를 전달한다.
사람이 지켜보지 않아도 된다.

Claude Code는 **동기(Synchronous)** 중심이다.
개발자가 터미널에서 대화하며 함께 작업한다.
코드를 작성하는 과정에서 실시간으로 협업한다.

### 실행 환경

Devin은 클라우드 샌드박스에서 실행된다.
자체 VM에 쉘, 에디터, 브라우저를 갖추고 있어
로컬 환경 설정 없이 바로 작업을 시작할 수 있다.

Claude Code는 개발자의 로컬 터미널에서 실행된다.
기존 개발 환경(IDE, 도구 체인, 설정)을
그대로 활용한다.

### 인터페이스

Devin은 웹 UI와 Slack을 통해 상호작용한다.
비개발 직군도 Slack에서 작업을 요청할 수 있다.

Claude Code는 CLI(터미널)가 기본이고,
IDE 확장(VS Code, JetBrains)도 지원한다.
개발자 친화적인 인터페이스다.

### 적합한 사용 사례

| Devin                          | Claude Code                  |
|--------------------------------|------------------------------|
| 독립적인 기능 개발             | 탐색적 코딩과 프로토타이핑   |
| 잘 정의된 버그 수정            | 복잡한 디버깅                |
| 반복적인 마이그레이션 작업     | 코드 리뷰와 리팩터링        |
| CI/CD 파이프라인 실패 수정     | 아키텍처 논의와 설계         |
| 비개발자의 간단한 작업 요청    | 학습과 코드 이해             |

### 코드 퀄리티

Devin은 자율적으로 작업하는 만큼
결과물의 품질 편차가 크다.
잘 정의된 소규모 작업에서는 좋은 결과를 내지만,
대규모 코드베이스나 복잡한 로직에서는
의도와 다른 코드를 생성하거나
기존 컨벤션을 무시하는 경우가 있다.
PR을 만들어 주지만 사람의 리뷰가 반드시 필요하다.

Claude Code는 개발자가 과정을 실시간으로 보면서
즉시 수정 지시를 내릴 수 있다.
잘못된 방향으로 갈 때 바로 교정할 수 있어
최종 결과물의 품질을 제어하기 쉽다.
다만 개발자가 계속 관여해야 하므로
자율성과 품질 제어는 트레이드오프 관계다.

### 컨텍스트 이해

Devin은 작업마다 새 세션을 시작하기 때문에
프로젝트 전체의 맥락을 파악하는 데 시간이 걸린다.
Knowledge(지식 베이스)를 설정해
프로젝트 컨텍스트를 보완할 수 있지만,
팀의 암묵적인 규칙까지 이해하기는 어렵다.

Claude Code는 로컬 코드베이스를 직접 탐색하며
파일 구조, 의존성, 테스트 패턴 등을
실시간으로 파악한다.
CLAUDE.md 파일을 통해 프로젝트 규칙을
명시적으로 전달할 수도 있다.

### 요금 체계

Devin은 시트 기반($500/월)으로 과금된다.
독립 에이전트를 "고용"하는 개념이다.

Claude Code는 API 토큰 사용량 기반이거나
Claude Pro/Max 구독($20~$200/월)에 포함된다.

## 문서

<https://docs.devin.ai/>

## Coding Agents 101

Devin 팀이 작성한 코딩 에이전트 활용 가이드.

[Coding Agents 101: The Art of Actually Getting Things Done](https://devin.ai/agents101)

## 요금제

<https://devin.ai/pricing>

| 플랜       | 가격              |
|------------|-------------------|
| Core       | $500/월 (시트당)  |
| Enterprise | 별도 문의         |

## Articles

[Cognition introduces Devin, an AI software engineering teammate - TechCrunch](https://techcrunch.com/2024/03/12/cognitions-new-ai-agent-devin-can-write-and-execute-code/)

[Cognition's AI coding agent, Devin, is now generally available - TechCrunch](https://techcrunch.com/2024/12/06/cognitions-ai-coding-agent-devin-is-now-generally-available/)
