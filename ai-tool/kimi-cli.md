# Kimi CLI

<https://github.com/MoonshotAI/kimi-cli>

## 소개

Moonshot AI가 개발한 터미널 AI 에이전트다.
소프트웨어 개발 작업과 터미널 작업을 지원한다.
코드 읽기·편집, 셸 명령 실행, 웹 검색·패치를 자율적으로 계획하며 실행한다.

현재 Kimi Code CLI로 발전 중이며, 기존 kimi-cli 프로젝트는 단계적으로 종료된다.
`pip install kimi-cli`로 설치 시 Kimi Code CLI로 자동 마이그레이션된다.

## 주요 기능

### 셸 명령 모드

`Ctrl-X`로 셸 명령 모드와 에이전트 모드를 전환한다.
셸 명령 모드에서는 kimi-cli를 벗어나지 않고 직접 셸 명령을 실행할 수 있다.
(내장 셸 명령 `cd` 등은 아직 미지원)

### VS Code 확장

Kimi Code VS Code Extension으로 VS Code와 통합된다.

### ACP(Agent Client Protocol) 지원

ACP를 통해 Zed, JetBrains 같은 ACP 호환 에디터·IDE와 통합된다.

## 분석

### Claude Code와 같은 터미널 에이전트 접근

Claude Code가 선도한 “터미널 AI 에이전트” 포지셔닝을
중국 AI 기업 Moonshot AI가 Kimi 모델로 동일하게 적용한 것이다.
기능 구성이 Claude Code와 유사하다.
셸 통합, 코드 에디터 확장, 웹 검색, 자율 계획 실행이 핵심 기능 세트다.

### Kimi Code CLI로의 전환

기존 kimi-cli가 Kimi Code CLI로 발전한다는 공지는
브랜딩 변경 이상으로 “코딩 에이전트”라는 카테고리로의 명확한 포지셔닝을 의미한다.
“Kimi CLI”가 범용적이었다면 “Kimi Code CLI”는 코딩에 특화됨을 명확히 한다.

## 비평

### 기존 사용자의 전환 부담

kimi-cli가 단계적 종료를 발표하고 Kimi Code CLI로 전환을 권고하는 것은
현재 사용자에게 전환 작업을 요구한다.
자동 마이그레이션을 제공하지만, 기능 변경이 있을 수 있어 검증이 필요하다.

## 인사이트

### AI 코딩 에이전트가 글로벌 경쟁 상품이 됐다

Claude Code(Anthropic), Codex(OpenAI), Gemini CLI(Google), Kimi Code(Moonshot AI)가
거의 동일한 기능 세트로 경쟁하는 시장이 형성됐다.
터미널 AI 에이전트가 AI 개발 도구의 핵심 카테고리가 됐음을 보여준다.
이 경쟁에서 차별화 요소는 기반 모델 품질, 한국어·중국어 지원, 특정 도구 통합 깊이가 될 것이다.
