# CodeRabbit - AI Code Reviews

<https://www.coderabbit.ai/>

## Review instructions

<https://docs.coderabbit.ai/guides/review-instructions>

`.coderabbit.yaml` 파일 예시:

```yaml
language: ko-KR
```

## Issue Planner

<https://www.coderabbit.ai/issue-planner>

<https://docs.coderabbit.ai/issues/planner>

이슈, 스펙, 코드베이스를 분석해 코딩 에이전트에게 넘길 수 있는 Coding Plan을
생성하는 기능. 현재 오픈 베타.

CodeRabbit의 지속적 코드 분석을 통해 코드베이스를 깊이 이해하고 있기 때문에, 각
플랜은 프로젝트의 아키텍처와 컨벤션에 맞춰 작성됨.

### 지원 플랫폼

GitHub Issues, GitLab, Jira, Linear.

### 사용 방법

이슈에 `@coderabbitai plan`이라고 코멘트하면 Coding Plan이 생성됨. 이슈와
코드베이스의 복잡도에 따라 보통 5~10분 소요.

자동 플래닝(Auto-planning)을 활성화하면 설정한 조건에 맞는 이슈가 생성될 때마다
자동으로 Coding Plan이 생성됨.

### Coding Plan 확인 및 개선

GitHub/GitLab에서는 이슈 코멘트로 Coding Plan이 직접 게시됨. 플랜 코멘트에
답글을 달아 세부 사항을 수정하거나 설계 결정에 대해 논의할 수 있음.

Jira/Linear에서는 CodeRabbit 웹 앱에서 Coding Plan을 확인할 수 있음. 오른쪽 채팅
패널을 사용해 플랜을 다듬은 뒤 코딩 에이전트에게 최종 프롬프트를 전달.

### 특징

코딩 에이전트가 생성하는 플랜은 보통 소수의 파일만 참조하지만, CodeRabbit의
Coding Plan은 지속적 코드 분석과 광범위한 지식 베이스를 기반으로 작성됨. 따라서
올바른 파일을 참조하고, 기존 패턴을 따르며, 기존 코드와 자연스럽게 통합됨.

조직 내 누구나 플랜을 확인하고, CodeRabbit과 논의하고, 재플래닝을 요청할 수
있음.

## Articles

[코드 리뷰 요정, CodeRabbit이 나타났다 🐰](https://tech.inflab.com/20250303-introduce-coderabbit/)

## CodeRabbit CLI - AI Code Reviews in CLI

<https://www.coderabbit.ai/cli>

## Startup Program

<https://www.coderabbit.ai/startup-program>

초기 스타트업을 위한 AI 코드 리뷰 지원 프로그램.

### 지원 내용

14일 무료 체험 이후 CodeRabbit Pro 구독을 3개월간 50% 할인 제공.

### 자격 요건

VC 또는 액셀러레이터(Accelerator) 지원을 받는 스타트업이 대상.

### 신청 방법

1. 신청 페이지에서 양식 작성.
2. CodeRabbit 팀이 영업일 기준 2일 이내에 검토.
3. 승인 여부를 이메일로 안내.

신청: <https://resources.coderabbit.ai/startup-program>

### 신청 예시 문구

양식에서 자주 묻는 항목과 영어 예시. `[...]` 부분을 자신의 상황에 맞게 수정.

회사 소개(Company Description):

> We are an early-stage startup building a [SaaS / e-commerce / fintech]
> platform. Our development team has [N] engineers.

(우리는 [SaaS / 이커머스 / 핀테크] 플랫폼을 만드는 초기 스타트업입니다. 개발팀은
[N]명의 엔지니어로 구성되어 있습니다.)

투자 단계(Funding Stage):

VC/액셀러레이터 투자를 받은 경우:

> We raised our [seed / pre-A / Series A] round from [투자사/액셀러레이터 이름].

([seed / pre-A / Series A] 라운드를 [투자사/액셀러레이터 이름]으로부터
유치했습니다.)

정부 지원 사업에 선정된 경우:

> We are part of [프로그램 이름], a government-backed startup program in South
> Korea.

([프로그램 이름]에 선정된 한국 정부 지원 스타트업입니다.)

예시: TIPS, 창업성장기술개발, K-Startup 그랜드챌린지, 예비창업패키지 등.

> We were selected for the TIPS program, a government-funded accelerator program
> run by Korea's Ministry of SMEs and Startups (MSS).

(중소벤처기업부(MSS) 산하 정부 지원 액셀러레이터 프로그램인 TIPS에
선정되었습니다.)

CodeRabbit 사용 목적:

> We want to improve our code review process and maintain code quality with a
> small team. AI-powered reviews would help us ship faster while catching bugs
> early.

(소규모 팀으로 코드 리뷰 프로세스를 개선하고 코드 품질을 유지하고 싶습니다. AI
기반 리뷰를 통해 버그를 조기에 발견하면서 더 빠르게 배포하고 싶습니다.)

추가 메시지(선택):

> We currently use GitHub for version control and have [N] active repositories.
> We'd love to try CodeRabbit Pro to streamline our development workflow.

(현재 GitHub으로 버전 관리를 하고 있으며 [N]개의 활성 저장소가 있습니다.
CodeRabbit Pro를 사용해 개발 워크플로를 효율화하고 싶습니다.)

### 참고

- 오픈소스 프로젝트(Public Repository)는 별도 신청 없이 무료로 리뷰 이용 가능.
- PR을 생성하는 개발자 수 기준으로 과금(Seat 기반).
- 리뷰 가능한 PR 수나 저장소 수 제한 없음.

## 아샬의 트윗

### 2024년 7월 24일

[CodeRabbit을 적용해 봤는데, 일반 정적 분석기 수준에도 못 미치는 걸 달아놔서 오해하지 말라고 댓글을 추가했더니 대화가 시작됨. 이 대화를 통해 조정이 돼서 유용하겠다는 생각이 들었다.](https://twitter.com/ahastudio/status/1816065378612830406)

## 2025년 2월 27일

[CodeRabbit은 실용성을 떠나서 \*재미\*란 측면에서 크게 도움이 된다고 생각하는데, Poem은 무료 버전에서도 계속 누릴 수 있는 혜택이니 별 생각 없이 적용해 보는 걸 추천.](https://twitter.com/ahastudio/status/1895055399554031954)

## 2025년 10월 11일

[CodeRabbit이 프롬프트까지 시각화하네... 😮](https://twitter.com/ahastudio/status/1976970778332823881)
