# OpenHands - AI Software Development Platform

<https://openhands.dev/>

All Hands AI가 만든 오픈소스 AI 소프트웨어 개발 플랫폼.
AI 에이전트가 코드 작성, 수정, 디버깅, 실행까지 수행한다.
핵심 구성 요소가 MIT 라이선스로 공개되어 있다.

## 주요 구성 요소

### Software Agent SDK

에이전트 기술의 핵심 엔진. Python 라이브러리로 에이전트를
정의하고 로컬 또는 클라우드에서 실행할 수 있다.

<https://github.com/OpenHands/software-agent-sdk/>

### CLI

터미널에서 바로 사용하는 인터페이스. Claude, GPT 등
다양한 LLM을 지원한다. Claude Code나 Codex CLI와 유사한
경험을 제공한다.

<https://github.com/OpenHands/OpenHands-CLI>

### Local GUI

REST API와 React SPA로 구성된 로컬 인터페이스.
데스크톱에서 에이전트를 실행하고 결과를 확인할 수 있다.

### Cloud

GitHub/GitLab 인증으로 접속하는 클라우드 플랫폼.
무료 $10 크레딧을 제공한다.
Slack, Jira, Linear 연동과 팀 협업 기능을 갖추고 있다.

<https://app.all-hands.dev/>

### Enterprise Edition

Kubernetes 기반으로 프라이빗 VPC에 자체 호스팅하는
엔터프라이즈 버전. 소스 어베일러블 라이선스로 제공된다.

<https://openhands.dev/enterprise>

## 아키텍처

EventStream을 중심으로 구성 요소가 통신한다.

```text
Agent → LLM 요청 → Action 생성
→ Runtime 실행 → Observation 반환
→ State 업데이트 → Agent 반복
```

핵심 클래스:

| 클래스          | 역할                              |
| --------------- | --------------------------------- |
| LLM             | LiteLLM 기반 모델 통신 중개       |
| Agent           | State를 보고 Action을 생성        |
| AgentController | Agent 초기화, State 관리, 루프    |
|                 | 제어                              |
| EventStream     | 이벤트 발행/구독의 중앙 허브      |
| Runtime         | Action 실행, Observation 반환     |
| Sandbox         | Docker 등 격리 환경에서 명령 실행 |

## CLI 설치 및 사용

### 설치

uv 사용 (Python 3.12+ 필요):

```bash
uv tool install openhands --python 3.12
```

바이너리 설치:

```bash
curl -fsSL https://install.openhands.dev/install.sh | sh
```

### 실행 모드

| 모드     | 명령어            | 용도             |
| -------- | ----------------- | ---------------- |
| TUI      | `openhands`       | 대화형 개발 작업 |
| IDE 연동 | `openhands acp`   | IDE 지원         |
| Headless | `openhands`       | 자동화, CI/CD    |
|          | `  --headless -t` |                  |
|          | `  "task"`        |                  |
| 웹       | `openhands web`   | 브라우저 기반    |
| GUI 서버 | `openhands serve` | 웹 GUI 배포      |
| 클라우드 | `openhands cloud` | 클라우드 실행    |
|          | `  -t "task"`     |                  |

### 승인 모드

기본적으로 각 액션마다 사용자 승인을 요청한다.

- `--always-approve` 또는 `--yolo`:
  모든 액션 자동 승인
- `--llm-approve`:
  AI 기반 보안 분석 후 자동 승인

### 세션 이어가기

```bash
openhands --resume          # 최근 세션 목록
openhands --resume <id>     # 특정 세션 재개
openhands --resume --last   # 가장 최근 세션 재개
```

### 설정 파일

`~/.openhands/` 디렉토리에 저장된다.

- `agent_settings.json`: 에이전트 설정
- `cli_config.json`: 터미널 UI 설정
- `mcp.json`: MCP 서버 설정

환경 변수(`LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`)는
`--override-with-envs` 플래그와 함께 사용한다.

## Claude Code와 비교

|              | OpenHands             | Claude Code         |
| ------------ | --------------------- | ------------------- |
| 라이선스     | MIT (코어)            | 프로프라이어터리    |
| 실행 환경    | 로컬, 클라우드 모두   | 로컬 터미널         |
| LLM 지원     | Claude, GPT 등 다수   | Claude 전용         |
| 인터페이스   | CLI, GUI, 웹, IDE     | CLI, IDE 확장       |
| 샌드박스     | Docker 기반 격리      | 로컬 실행           |
| 에이전트 SDK | Python SDK 제공       | Agent SDK 제공      |
| 가격         | 오픈소스 (LLM 비용별) | Pro/Max $20~$200/월 |

## 홈페이지가 말하는 현재 제품 구성

홈페이지(2026년 10월 확인)는 OpenHands를 에이전트 소프트웨어 개발을 위한 열린
플랫폼이라고 소개한다.
앞쪽 수치는 GitHub 스타 91.7K이며 같은 날 GitHub API가 돌려준 값은 91,679개로
맞는다.
제품 메뉴는 Agent Canvas, Cloud, Agent Control Plane, SDK로 나뉜다.

### 자동화가 중심 메시지다

화면의 중심은 대화형 코딩보다 자동화다.
GitHub, Slack, Jira, Linear, 스케줄에서 오는 신호를 받아 계획, 실행, 검증, 반영,
모니터링의 여섯 단계로 에이전트 작업을 돌린다고 설명한다.
템플릿으로는 Slack의 @openhands 멘션 처리, 새 Linear 이슈 분류, Jira 장애 분류,
모든 PR 리뷰, 장애 회고 초안, 보안 알림 대응, CI 실패 자동 수정이 있다.
사용 사례는 PR 리뷰와 CI 수정, 이슈 분류와 초안 PR, QA 자동화, 장애 조사, 문서
갱신, 의존성 갱신 같은 반복 작업이다.
엔지니어가 리뷰와 승인과 병합을 쥔다고 밝히지만, 어떤 승인 단계가 기본으로 켜져
있는지는 홈페이지에 없다.

### 에이전트와 모델과 실행 환경을 따로 고른다

홈페이지는 에이전트를 하나로 표준화하지 않고 워크플로 실행 방식만 표준화한다고
한다.
Claude Code, Codex, Gemini CLI, OpenHands 자체 에이전트 중에서 고르고, 폐쇄
모델뿐 아니라 Kimi, DeepSeek, Qwen 같은 오픈 가중치 모델도 로컬이나 클라우드나
VPC 안에서 돌린다고 한다.
실행 환경은 로컬 VM, 노트북과 데스크톱, 클라우드 샌드박스, 상시 가동, 기업 VPC로
나뉜다.

### 요금 단계 대신 세 사용자층을 나눈다

개인은 로컬에서 에이전트를 병렬로 돌리고 노트북이 한계가 되면 VM으로 옮긴다.
팀은 자동화를 공유하고 노트북이 닫혀 있어도 에이전트를 돌린다.
기업은 VPC 배포, 샌드박스 격리, 접근 범위 정의, 모든 동작의 감사, 사용량과 예산
관리를 얻는다.
Agent Control Plane은 누가 에이전트를 실행하고, 무엇에 접근하고, 어디서
실행하고, 얼마를 쓰고, 무엇을 바꾸는지를 플랫폼과 보안 팀이 중앙에서 통제하게
하는 층이라고 소개한다.

### 후기와 수치는 홍보 자료다

후기에는 제3자의 트윗이 섞여 있고, 그중 하나는 OpenHands가 1,880만 달러를
투자받았고 클라우드 코딩 에이전트가 버그 티켓의 87%를 당일 해결한다고 적었다.
이 수치는 인용된 트윗의 주장이며 홈페이지가 근거를 밝히지 않았고 이 문서가
확인하지 못했다.
위 비교표의 SWE-Bench 77.6%처럼 측정 조건이 있는 수치와 구분해서 읽어야 한다.

## SWE-Bench

SWE-Bench Verified에서 77.6% 해결률을 기록했다.

## 관련 저장소

- 메인: <https://github.com/All-Hands-AI/OpenHands>
- SDK: <https://github.com/OpenHands/software-agent-sdk/>
- CLI: <https://github.com/OpenHands/OpenHands-CLI>
- 벤치마크: <https://github.com/OpenHands/benchmarks>

## 커뮤니티

Slack: <https://dub.sh/openhands>

## 논문

<https://arxiv.org/abs/2511.03690>

## 문서

<https://docs.openhands.dev/>
