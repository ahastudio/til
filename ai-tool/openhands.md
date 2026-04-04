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
| AgentController | Agent 초기화, State 관리, 루프     |
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

| 모드     | 명령어              | 용도             |
| -------- | ------------------- | ---------------- |
| TUI      | `openhands`         | 대화형 개발 작업 |
| IDE 연동 | `openhands acp`     | IDE 지원         |
| Headless | `openhands`         | 자동화, CI/CD    |
|          | `  --headless -t`   |                  |
|          | `  "task"`          |                  |
| 웹       | `openhands web`     | 브라우저 기반    |
| GUI 서버 | `openhands serve`   | 웹 GUI 배포     |
| 클라우드 | `openhands cloud`   | 클라우드 실행    |
|          | `  -t "task"`       |                  |

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

|              | OpenHands             | Claude Code          |
| ------------ | --------------------- | -------------------- |
| 라이선스     | MIT (코어)            | 프로프라이어터리     |
| 실행 환경    | 로컬, 클라우드 모두   | 로컬 터미널          |
| LLM 지원     | Claude, GPT 등 다수   | Claude 전용          |
| 인터페이스   | CLI, GUI, 웹, IDE     | CLI, IDE 확장        |
| 샌드박스     | Docker 기반 격리      | 로컬 실행            |
| 에이전트 SDK | Python SDK 제공       | Agent SDK 제공       |
| 가격         | 오픈소스 (LLM 비용별) | Pro/Max $20~$200/월  |

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
