# Pi — 최소 코딩 에이전트 하네스

<https://pi.dev/>

<https://github.com/earendil-works/pi>

코딩 에이전트 CLI는 모노레포의 하위 패키지다:
<https://github.com/earendil-works/pi/tree/main/packages/coding-agent>

## 히스토리

원래 Mario Zechner(GitHub: `badlogic`)의 개인 저장소 `badlogic/pi-mono`로 시작했다.
이후 `earendil-works` 조직으로 이전되어 현재는 `earendil-works/pi`가 정식 저장소다.
(`badlogic/pi-mono`는 GitHub 리디렉션으로 현재도 접근 가능하다.)

npm 패키지 스코프도 함께 변경되었다.

| 이전                        | 이후                           |
| --------------------------- | ------------------------------ |
| `@mariozechner/pi-coding-agent` | `@earendil-works/pi-coding-agent` |
| `@mariozechner/pi-agent-core`   | `@earendil-works/pi-agent-core`   |
| `@mariozechner/pi-ai`           | `@earendil-works/pi-ai`           |

## 소개

Pi는 별 50,000개 이상을 받은 TypeScript 기반의 터미널 코딩 에이전트 하네스다.
슬로건은 “Adapt pi to your workflows, not the other way around” —
“Pi에 워크플로우를 맞추지 말고, Pi를 워크플로우에 맞춰라.”
코어를 최소화하고 확장성을 극대화하는 설계 철학 아래, Mario Zechner가 제작했다.

```bash
npm install -g @earendil-works/pi-coding-agent
pi
```

모노레포 구조로 다음 패키지를 포함한다.

| 패키지                              | 역할                                              |
| ----------------------------------- | ------------------------------------------------- |
| `@earendil-works/pi-coding-agent`   | 인터랙티브 코딩 에이전트 CLI                      |
| `@earendil-works/pi-agent-core`     | 툴 호출·상태 관리를 갖춘 에이전트 런타임          |
| `@earendil-works/pi-ai`             | 다중 LLM 제공자 통합 API                          |
| `@earendil-works/pi-tui`            | 차등 렌더링 기반 터미널 UI 라이브러리             |
| `@earendil-works/pi-web-ui`         | AI 채팅 인터페이스용 웹 컴포넌트                  |
| `pi-mom`                            | Slack → pi 에이전트 위임 봇                       |
| `pi-pods`                           | GPU 파드 vLLM 배포 관리 CLI                       |

기본 제공 도구는 네 가지로만 구성된다. `read`, `write`, `edit`, `bash`.
선택적으로 `grep`, `find`, `ls`를 추가할 수 있다.
나머지 기능은 스킬(Skill), 확장(Extension), 프롬프트 템플릿, Pi 패키지 형태로 추가한다.

지원 LLM 제공자는 30개 이상이다.

구독 기반 (API 키 불필요): Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot, Google Gemini

API 키 기반: Anthropic, OpenAI, Azure OpenAI, Google Vertex, Amazon Bedrock,
Mistral, Groq, Cerebras, xAI, OpenRouter, Hugging Face, DeepSeek 등

`/login` 명령으로 OAuth 인증을 하거나 API 키를 환경 변수로 설정하면 된다.

## 운영 모드

```text
interactive  ← 기본값. 실시간 대화형 터미널
print/JSON   ← 스크립팅, CI 파이프라인
RPC          ← stdin/stdout으로 프로세스 통합
SDK          ← npm 패키지로 임베딩
```

RPC 모드와 SDK 모드가 특히 흥미롭다.
Pi를 더 큰 시스템의 부품으로 조립할 수 있다.
pi-mom(Slack 봇)이 RPC 모드의 실제 구현체다.

## 인터랙티브 모드

```text
@파일명        ← 파일 참조 (퍼지 검색)
!command       ← 셸 실행 후 LLM에 출력 전달
!!command      ← 셸 실행만 (LLM 전달 안 함)
Shift+Enter    ← 멀티라인 입력
Enter          ← 메시지 큐잉 (모델 작업 중 스티어링)
Alt+Enter      ← 후속 메시지 큐잉
```

이미지는 붙여넣기나 터미널 드래그로 입력할 수 있다.

## 세션 관리

```text
~/.pi/agent/sessions/   ← 자동 저장
  session-xxx.jsonl     ← JSONL 형식, 트리 구조
```

세션은 트리 구조로 브랜치를 지원한다.
파일을 여러 개 만들지 않고 인라인으로 분기한다.

```text
/tree     ← 세션 트리 탐색
/fork     ← 현재 위치에서 분기
/compact  ← 대화 수동 압축 (자동도 지원)
/share    ← 비공개 GitHub Gist로 업로드해 공유 HTML 링크 생성
```

## 컨텍스트 파일

```text
~/.pi/agent/AGENTS.md   ← 전역
.pi/AGENTS.md           ← 프로젝트
./AGENTS.md             ← 디렉터리
```

`CLAUDE.md`도 동일하게 인식한다.
`SYSTEM.md`로 기본 시스템 프롬프트를 교체하거나,
`APPEND_SYSTEM.md`로 기존 시스템 프롬프트에 추가할 수 있다.

## 확장 시스템

Pi의 확장성은 4개 레이어로 구성된다.

### TypeScript Extensions

커스텀 도구, 키보드 단축키, UI 컴포넌트 추가.
에디터, Git 통합, MCP 서버 지원을 Extension으로 구현할 수 있다.

### Skills

`/skill:name` 으로 호출하는 온디맨드 역량 패키지.
`SKILL.md`를 가진 CLI 도구로 에이전트가 자연어로 호출한다.

### Prompt Templates

`/templatename` 으로 확장되는 재사용 가능한 마크다운 파일.

### Pi Packages

Extensions, Skills, Prompts, Themes를 npm 또는 git으로 배포할 수 있는 번들.

## 코드 구조

```text
pi-ai           ← 멀티 프로바이더 LLM API 추상화
  ↓
pi-agent-core   ← 툴 호출 + 상태 관리 에이전트 런타임
  ↓
pi-coding-agent ← 인터랙티브 CLI / SDK 엔트리포인트
```

`@earendil-works/pi-agent-core`는 `prompt()` 호출 시 이벤트 스트림을 발생시킨다.
`agent_start`, `turn_start`, `message_start`, `message_update`, `message_end`,
`tool_execution_start`, `tool_execution_end`, `turn_end`, `agent_end` 순서로 흐른다.
이 이벤트 모델은 스트리밍 응답, 도구 실행, UI 업데이트를 단일 인터페이스로 처리하게 해준다.

`AgentMessage`와 LLM Message를 분리한 구조도 주목할 만하다.
에이전트는 앱 전용 커스텀 메시지 타입을 포함하는 `AgentMessage`로 작업하고,
LLM에 전달할 때만 `convertToLlm`으로 필터링 및 변환한다.
UI 전용 메시지가 LLM 컨텍스트를 오염시키지 않으면서도, 앱에서는 풍부한 메시지 타입을 활용한다.

`src/index.ts`는 순수한 re-export 파일이다.
모노레포 내 하위 모듈들을 단일 API 표면으로 집약한다.

```typescript
export { AgentSession, type AgentSessionConfig } from "./core/agent-session.js";
export { compact, generateSummary, shouldCompact } from "./core/compaction/index.js";
export { createExtensionRuntime, ExtensionRunner } from "./core/extensions/index.js";
export { createAgentSession, createBashTool, createCodingTools } from "./core/sdk.js";
export { InteractiveMode, runPrintMode, runRpcMode } from "./modes/index.js";
```

## 분析

### “의도적 부재”의 설계 철학

Pi 철학의 가장 독특한 부분은 기능을 추가한 목록이 아니라 기능을 빼낸 목록이다.

| 제외 항목               | 대안                                              |
| ----------------------- | ------------------------------------------------- |
| MCP 내장                | Extension으로 직접 구현 가능                      |
| Sub-agents              | Pi 인스턴스 스폰 또는 Extension으로 해결          |
| Permission popups       | 컨테이너 환경 또는 커스텀 확인 흐름 구현          |
| Plan mode / To-dos      | 파일이나 Extension으로 필요에 따라 구현           |
| Background bash         | 보안 모델을 직접 선택                             |

이 각각은 “아직 구현하지 않았다”가 아니라 “의도적으로 코어에 넣지 않았다”는 결정이다.
예를 들어 서브에이전트는 tmux로 Pi 인스턴스를 여러 개 실행하거나, Extension으로 구현하라고 안내한다.
이 패턴은 일관적이다. 코어가 결정하는 대신, 사용자가 자신의 워크플로우에 맞는 방식을 선택하게 한다.

### 이벤트 기반 에이전트 코어

`@earendil-works/pi-agent-core`의 구조는 에이전트 런타임 설계의 좋은 참조 사례다.
이벤트 스트림 모델은 스트리밍 응답, 도구 실행, UI 업데이트를 단일 인터페이스로 처리한다.
`AgentMessage`와 LLM Message를 분리함으로써 UI 전용 메시지가 LLM 컨텍스트를 오염시키지 않는다.
터미널 UI(`pi-tui`)와 웹 UI(`pi-web-ui`)가 동일한 에이전트 코어 위에서 작동하는 것이 이 구조의 실현이다.

### 확장성 모델의 계층 구조

Pi의 확장 계층은 복잡성이 낮은 것부터 높은 것까지 자연스러운 스펙트럼을 형성한다.
스킬은 `SKILL.md` 파일 하나면 되고, Extension은 TypeScript 작성이 필요하며,
Pi 패키지는 이 둘을 번들로 npm이나 git을 통해 배포한다.
OSS 세션 공유 캠페인도 주목할 만하다.
오픈소스 작업에 Pi를 사용하면 세션을 Hugging Face에 게시하도록 권장한다.
장난감 벤치마크가 아닌 실제 개발 워크플로우 데이터로 모델, 프롬프트, 도구, 평가를 개선하려는 목적이다.

## 비평

### 강점: 일관된 철학과 극단적 확장성

48,039개의 별은 이 접근법이 상당한 공명을 일으킨다는 증거다.
“코어를 최소화하고 확장성을 극대화한다”는 철학이 말에서 그치지 않고 실제 설계 결정으로 구현됐다는 점이 신뢰를 준다.
30개 이상 LLM 제공자 지원은 단일 모델·제공자에 종속되지 않으려는 사용자에게 실질적 가치를 제공한다.

### 약점: 높은 입문 장벽

“원하는 기능은 Extension으로 구현하라”는 철학은 기술적으로 숙련된 사용자에게는 자유이지만,
그렇지 않은 사용자에게는 장벽이다.
MCP나 서브에이전트 없이 시작하면 많은 사람이 기대하는 기본 기능이 없는 상태로 느껴질 수 있다.
Pi 패키지 생태계가 아직 초기 단계라면 결국 직접 Extension을 작성해야 한다는 의미고,
이는 TypeScript 숙련도를 전제한다.

### 보완할 시각: 세션 데이터 공유의 프라이버시 트레이드오프

OSS 세션 공유 캠페인은 흥미롭지만, 공개 저장소 작업 세션에서도 민감한 정보(API 키, 개인 데이터,
미공개 코드)가 포함될 수 있다.
“실제 개발 워크플로우 데이터”를 공개 Hugging Face 데이터셋으로 기여한다는 선택은
각 사용자가 신중하게 검토해야 할 결정이다.

## 인사이트

### “도구의 최소화”가 모델 성능에 미치는 영향

Pi의 기본 도구를 네 가지(`read`, `write`, `edit`, `bash`)로 제한한 결정은 단순화 이상의 의미를 가진다.
연구에 따르면 에이전트에게 제공되는 도구의 수가 많아질수록 모델이 어떤 도구를 언제 쓸지
결정하는 오버헤드가 증가하고, 불필요한 도구 호출이 늘어난다.
최소 도구 세트는 모델의 의사결정 공간을 좁혀 핵심 작업에 집중하게 한다.
[mini-SWE-agent](mini-swe-agent.md)가 bash 하나만으로 SWE-bench 74%를 달성한 결과는 이 가설을 극단까지 밀어붙인 증거다.

이 철학은 역설적이다. 더 많은 기능이 아니라 더 적은 기능이 더 신뢰할 수 있는 에이전트를 만든다.
[하네스 엔지니어링](harness-engineering.md)의 핵심 교훈 — “모델을 더 똑똑하게 만들려 하지 말고, 모델이 성공하기 쉬운
환경을 설계하라” — 과 같은 맥락이다.
기본 도구 네 가지는 성공하기 쉬운 최소한의 환경이다.

### 이벤트 스트림 모델이 에이전트 UI의 미래 형태다

`pi-agent-core`의 이벤트 기반 아키텍처는 에이전트 UI 개발의 핵심 패턴을 드러낸다.
에이전트의 실행은 순차적 요청-응답이 아니라 복잡한 이벤트의 흐름이다.
도구 호출 시작, 스트리밍 결과, 다음 LLM 턴 시작이 모두 비동기적으로 얽혀 있다.

이 복잡성을 이벤트 스트림으로 추상화하면 UI 레이어가 특정 에이전트 구현에 종속되지 않는다.
어떤 UI든 이벤트를 구독하고 원하는 방식으로 렌더링한다.
터미널 UI(`pi-tui`)와 웹 UI(`pi-web-ui`)가 동일한 코어 위에서 작동하는 것이 이 구조의 실현이다.
에이전트 런타임을 직접 구현하려는 개발자에게, 이 이벤트 모델은 실용적인 참조 아키텍처다.

### 세션 트리: 비선형 대화의 설계

대부분의 AI 도구는 대화를 선형으로 본다.
Pi의 세션 트리는 대화를 탐색 공간으로 본다.
`/fork`로 분기하고, 잘못된 방향은 버리고, 유망한 방향만 진행한다.
Git의 브랜치 모델을 에이전트 대화에 적용한 것이다.
[re_gent](regent.md)가 에이전트 활동을 별도 VCS로 캡슐화하려는 시도와 같은 문제 — “대화는 커밋이 아니다” — 를 Pi는 도구 내부 세션 트리로 해결한다.

컴팩션(compaction)도 같은 맥락이다.
긴 대화를 요약으로 압축하는 것은 단순한 토큰 절약이 아니라,
무엇을 기억하고 무엇을 잊을지를 의식적으로 설계하는 행위다.
컨텍스트 윈도우 한계를 결함이 아닌 설계 조건으로 받아들인다.

### 오픈소스 세션 데이터가 에이전트 훈련의 새로운 자원이 된다

Pi의 OSS 세션 공유 캠페인은 AI 개발의 데이터 경제에서 흥미로운 실험이다.
에이전트 훈련의 병목 중 하나는 실제 소프트웨어 개발 태스크의 고품질 데이터 부족이다.
장난감 벤치마크(HumanEval, MBPP 등)는 실제 코드베이스의 복잡성 — 레거시 코드, 의존성 충돌,
모호한 스펙 — 을 반영하지 못한다.

Pi의 접근은 이 문제를 커뮤니티 기여로 해결하려 한다.
실제 오픈소스 프로젝트에서의 에이전트 세션은 실패, 수정, 도구 오용, 컨텍스트 손실 등
실제 에이전트가 겪는 어려움을 담고 있다.
더 나아가, 이 캠페인은 Pi 사용자가 도구의 수동적 소비자가 아니라
에이전트 개선의 능동적 기여자가 되게 한다.
