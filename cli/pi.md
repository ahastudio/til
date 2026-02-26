# Pi - Minimal Terminal Coding Harness

<https://pi.dev/>

<https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent>

Pi는 Mario Zechner가 만든 터미널 코딩 에이전트다.
슬로건은 "Adapt pi to your workflows, not the other way around"—
도구를 워크플로우에 맞춰라, 워크플로우를 도구에 맞추지 말라.

```bash
npm install -g @mariozechner/pi-coding-agent
pi
```

## 핵심 철학: 의도적 최소주의

Pi가 의도적으로 코어에서 **제외**한 것들:

| 제외 항목               | 이유                                      |
| ----------------------- | ----------------------------------------- |
| MCP 내장                | Extension으로 직접 구현 가능              |
| Sub-agents              | Pi 인스턴스 스폰 또는 Extension으로 해결  |
| Permission popups       | 컨테이너 환경 또는 커스텀 확인 흐름 구현  |
| Plan mode / To-dos      | 파일이나 Extension으로 필요에 따라 구현   |
| Background bash         | 보안 모델을 직접 선택                     |

이것은 단순한 미완성이 아니다.
코어를 최소로 유지하고 **확장성을 1등 시민**으로 설계한 결과다.

## 4가지 운영 모드

```
interactive  ← 기본값. 실시간 대화형 터미널
print/JSON   ← 스크립팅, CI 파이프라인
RPC          ← stdin/stdout으로 프로세스 통합
SDK          ← npm 패키지로 임베딩
```

RPC 모드와 SDK 모드가 특히 흥미롭다.
Pi를 더 큰 시스템의 **부품**으로 조립할 수 있다.

## 기본 제공 도구

코어에는 4개만 있다:

- `read` — 파일 읽기
- `write` — 파일 쓰기
- `edit` — 파일 편집
- `bash` — 셸 실행

선택적으로 `grep`, `find`, `ls`를 추가할 수 있다.
이 미니멀한 기본 세트가 Pi 철학의 핵심이다.

## 확장 시스템 아키텍처

Pi의 확장성은 4개 레이어로 구성된다:

### 1. TypeScript Extensions

```typescript
// 커스텀 도구, 키보드 단축키, UI 컴포넌트 추가
// 에디터, Git 통합, MCP 서버 지원 구현 가능
```

### 2. Skills (Agent Skills 표준)

`/skill:name` 으로 호출하는 온디맨드 역량 패키지.

### 3. Prompt Templates

`/templatename` 으로 확장되는 재사용 가능한 마크다운 파일.

### 4. Pi Packages

Extensions, Skills, Prompts, Themes를
npm 또는 git으로 배포할 수 있는 번들.

## 세션 관리

```
~/.pi/agent/sessions/   ← 자동 저장
  session-xxx.jsonl     ← JSONL 형식, 트리 구조
```

세션은 트리 구조로 **브랜치**를 지원한다.
파일을 여러 개 만들지 않고 인라인으로 분기한다.

```
/tree     ← 세션 트리 탐색
/fork     ← 현재 위치에서 분기
/compact  ← 대화 수동 압축 (자동도 지원)
```

컴팩션(compaction)은 긴 대화를 요약으로 압축해
컨텍스트 윈도우를 효율적으로 관리한다.

## 컨텍스트 파일 우선순위

```
~/.pi/agent/AGENTS.md   ← 전역
.pi/AGENTS.md           ← 프로젝트
./AGENTS.md             ← 디렉터리
```

`CLAUDE.md`도 동일하게 인식한다.
`SYSTEM.md`로 기본 시스템 프롬프트를 교체하거나,
`APPEND_SYSTEM.md`로 기존 시스템 프롬프트에 추가할 수 있다.

## 멀티 프로바이더 지원

20개 이상의 LLM 프로바이더를 지원한다:

**구독 기반** (API 키 불필요):
Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot, Google Gemini

**API 키 기반**:
Anthropic, OpenAI, Azure OpenAI, Google Vertex,
Amazon Bedrock, Mistral, Groq, Cerebras, xAI,
OpenRouter, Hugging Face 등

## 인터랙티브 모드 주요 기능

```
@파일명        ← 파일 참조 (퍼지 검색)
!command       ← 셸 실행 후 LLM에 출력 전달
!!command      ← 셸 실행만 (LLM 전달 안 함)
Shift+Enter    ← 멀티라인 입력
Enter          ← 메시지 큐잉 (모델 작업 중 스티어링)
Alt+Enter      ← 후속 메시지 큐잉
```

이미지는 붙여넣기나 터미널 드래그로 입력할 수 있다.

## 코드 구조 분석: 모노레포 레이어

```
pi-ai           ← 멀티 프로바이더 LLM API 추상화
  ↓
pi-agent-core   ← 툴 호출 + 상태 관리 에이전트 런타임
  ↓
pi-coding-agent ← 인터랙티브 CLI / SDK 엔트리포인트
```

부가 패키지:

| 패키지          | 역할                                      |
| --------------- | ----------------------------------------- |
| `pi-tui`        | 차등 렌더링(differential rendering) TUI   |
| `pi-web-ui`     | AI 채팅용 웹 컴포넌트                     |
| `pi-mom`        | Slack → pi 에이전트 위임 봇               |
| `pi-pods`       | GPU 파드 vLLM 배포 관리 CLI               |

### index.ts: 단일 진입점 패턴

`src/index.ts`는 순수한 re-export 파일이다.
모노레포 내 하위 모듈들을 단일 API 표면으로 집약한다:

```typescript
export { AgentSession, type AgentSessionConfig } from "./core/agent-session.js";
export { AuthStorage, FileAuthStorageBackend } from "./core/auth-storage.js";
export { compact, generateSummary, shouldCompact } from "./core/compaction/index.js";
export { createExtensionRuntime, ExtensionRunner } from "./core/extensions/index.js";
export { createAgentSession, createBashTool, createCodingTools } from "./core/sdk.js";
export { InteractiveMode, runPrintMode, runRpcMode } from "./modes/index.js";
```

이 패턴은 내부 구조를 자유롭게 리팩터하면서도
외부 소비자에게는 안정적인 API를 제공한다.

## 인사이트

### "No MCP"는 반(反) MCP가 아니다

Pi가 MCP를 코어에서 제외한 것은 MCP를 부정하는 것이 아니다.
사용자가 자신의 보안 모델과 워크플로우에 맞는
**MCP 통합을 직접 설계**하게 하는 것이다.
모든 것을 제공하는 도구는 모든 것을 강제한다.

### 컴팩션은 에이전트의 망각 설계다

세션 컴팩션은 긴 대화를 요약으로 압축한다.
이것은 단순한 토큰 절약이 아니다.
**무엇을 기억하고 무엇을 잊을지를 의식적으로 설계**하는 행위다.
컨텍스트 윈도우 한계를 결함이 아닌 설계 조건으로 받아들인다.

### RPC 모드: 에이전트를 부품으로

RPC 모드는 Pi를 stdin/stdout 프로토콜로 노출한다.
이는 Pi가 더 큰 오케스트레이션 시스템에서
**교체 가능한 부품**으로 작동할 수 있음을 의미한다.
pi-mom(Slack 봇)이 이 패턴의 실제 구현체다.

### 세션 트리: 비선형 대화의 설계

대부분의 AI 도구는 대화를 선형으로 본다.
Pi의 세션 트리는 대화를 **탐색 공간**으로 본다.
`/fork`로 분기하고, 잘못된 방향은 버리고,
유망한 방향만 진행한다.
Git의 브랜치 모델을 에이전트 대화에 적용한 것이다.

### 확장성이 철학을 완성한다

"Adapt pi to your workflows"는 슬로건이 아니라 설계 결정이다.
MCP, sub-agents, plan mode를 제외한 것은
그 기능들이 **사용자마다 다르게 필요**하기 때문이다.
코어가 의견을 강요하지 않아야 확장이 의견을 표현할 수 있다.
