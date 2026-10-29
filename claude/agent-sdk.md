# Claude Agent SDK: 에이전트 루프를 라이브러리와 `claude -p`로 쓰는 법

<https://code.claude.com/docs/en/agent-sdk/overview>

<https://platform.claude.com/docs/ko/agent-sdk/overview>

<https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk>

<https://github.com/anthropics/claude-agent-sdk-demos>

## 목차

- [소개](#소개)
  - [설치와 전제](#설치와-전제)
- [어떤 도구를 쓸까](#어떤-도구를-쓸까)
- [claude -p와 SDK의 차이](#claude--p와-sdk의-차이)
- [SDK 쓰는 법](#sdk-쓰는-법)
  - [가장 작은 예제](#가장-작은-예제)
  - [에이전트 루프의 메시지와 종료 조건](#에이전트-루프의-메시지와-종료-조건)
  - [이름 변경과 기본값 변경](#이름-변경과-기본값-변경)
  - [권한 평가 순서](#권한-평가-순서)
  - [hooks](#hooks)
  - [subagents](#subagents)
  - [사용자 정의 도구와 MCP](#사용자-정의-도구와-mcp)
  - [구조화 출력](#구조화-출력)
  - [세션](#세션)
  - [비용 추적](#비용-추적)
- [배포](#배포)
  - [실행 형태와 자원](#실행-형태와-자원)
  - [보안](#보안)
- [고르는 기준](#고르는-기준)
- [개발 워크플로 자동화](#개발-워크플로-자동화)
  - [Step 1: 프로젝트 분석 → 문서 생성](#step-1-프로젝트-분석--문서-생성)
  - [Step 2: 스펙 문서 작성](#step-2-스펙-문서-작성)
  - [Step 3: 계획 수립 (Plan 모드)](#step-3-계획-수립-plan-모드)
  - [Step 4: 구현 (Edit 모드)](#step-4-구현-edit-모드)
  - [Step 5: 커밋](#step-5-커밋)
  - [Step 6: 코드 리뷰](#step-6-코드-리뷰)
  - [Step 7: 리뷰 피드백 반영](#step-7-리뷰-피드백-반영)
- [전체 워크플로 통합](#전체-워크플로-통합)
- [비평](#비평)
  - [같은 에이전트의 두 입구라는 설명은 어디까지 맞는가](#같은-에이전트의-두-입구라는-설명은-어디까지-맞는가)
  - [비용 수치는 예산 도구이지 청구 근거가 아니다](#비용-수치는-예산-도구이지-청구-근거가-아니다)
  - [권한 규칙은 샌드박스가 아니다](#권한-규칙은-샌드박스가-아니다)
- [체크리스트](#체크리스트)
- [기억할 원칙](#기억할-원칙)
- [다음 단계](#다음-단계)

## 소개

Claude Agent SDK는 Claude Code가 쓰는 도구, 에이전트 루프(agent loop),
컨텍스트 관리를 Python과 TypeScript에서 프로그램으로 부르게 해 주는
라이브러리다.
공식 개요 문서는 이 SDK를 Claude Code 바이너리를 실행하는 라이브러리로 설명한다.
따라서 SDK로 만든 에이전트와 터미널의 Claude Code는 같은 루프를 돈다.
npm 레지스트리 기준으로 TypeScript 패키지 `@anthropic-ai/claude-agent-sdk`의
최신판은 0.3.312(2026-10-27)이고, Python 패키지 이름은 `claude-agent-sdk`다.

이 문서는 두 가지를 다룬다.
첫째, SDK와 `claude -p`(헤드리스 실행)와 Client SDK와 Managed Agents 중
무엇을 고를지.
둘째, SDK에서 권한, hooks, subagents, MCP, 구조화 출력, 세션,
비용을 다루는 방법이다.
`claude -p` 자체의 사용법은 [별도 문서](claude-code-print-mode.md)에 있다.
끝에는 기존에 정리해 둔 개발 워크플로 자동화 예제를 그대로 남겼다.

### 설치와 전제

Node.js 18.14 이상 또는 Python 3.10 이상이 필요하다.[^quickstart]
TypeScript와 Python SDK는 모두 네이티브 Claude Code 바이너리를 함께
내려받으므로, 대부분의 설치에서는 Claude Code를 따로 설치하지 않아도
된다.[^quickstart]
바이너리는 SDK 패키지 버전에 고정되어 있어서,
SDK를 올리는 일이 곧 CLI를 올리는 일이다.[^hosting]
이전 문서에서 안내하던 `npm install -g @anthropic-ai/claude-code`는 SDK 사용에
필수가 아니다.

```bash
mkdir my-agent && cd my-agent
npm init -y
npm install @anthropic-ai/claude-agent-sdk
```

```bash
pip install claude-agent-sdk
```

인증은 API 키나 Amazon Bedrock, Google Cloud, Microsoft Foundry로 한다.
Anthropic은 사전 승인이 없는 한 제3자 개발자가 claude.ai 로그인이나 그 사용량
한도를 자기 제품에 제공하는 것을 허용하지 않는다.

## 어떤 도구를 쓸까

공식 개요는 Agent SDK, Claude Code CLI, Client SDK,
Managed Agents를 “누가 에이전트를 실행하고, 무엇이 기본으로 들어 있고,
어떻게 접근하는가”로 구분한다.
다섯 번째 선택지는 개요가 따로 안내한다.
Python이나 TypeScript가 아닌 언어에서 같은 에이전트 루프를 쓰려면 `-p` 플래그와
`--output-format json`으로 CLI를 하위 프로세스로 실행하라는 것이다.

| 하고 싶은 일                              | 고를 것         | 얻는 것                                                               |
| ----------------------------------------- | --------------- | --------------------------------------------------------------------- |
| 내가 운영하는 Python/TypeScript 앱에 삽입 | Agent SDK       | 내장 도구, 권한, 세션, hooks를 가진 라이브러리                        |
| 터미널에서 상호작용으로 개발              | Claude Code CLI | 일상 사용을 위한 터미널 인터페이스                                    |
| 다른 언어, 셸 스크립트, CI에서 같은 루프  | `claude -p`     | 프롬프트 한 번에 결과 한 번을 돌려주는 비상호작용 실행                |
| Claude API를 직접 호출                    | Client SDK      | 도구 루프를 직접 작성하거나 beta 도구 실행기(tool runner)에 맡김      |
| Anthropic이 에이전트를 호스팅             | Managed Agents  | 호스팅되는 루프와 Anthropic 관리 클라우드 샌드박스 또는 자체 샌드박스 |

`claude -p`의 공식 문서는 스스로를 “CLI로 쓰는 Agent SDK”로 소개하며, CLI,
Python, TypeScript 어느 쪽에서든 같은 루프를 프로그램으로 실행한다고
설명한다.[^headless]
그래서 두 길은 서로 다른 제품이 아니라 같은 에이전트의 두 입구다.
차이는 입구에 있다.
SDK는 함수 호출과 콜백과 타입이 있는 메시지를 주고,
`claude -p`는 플래그와 표준 입출력과 JSON을 준다.

## `claude -p`와 SDK의 차이

아래 표는 공식 문서에서 확인한 사실만 담았다.
“프로세스 수명” 행은 문서의 설명에서 이끌어 낸 추론이라 따로 표시했다.

| 항목             | `claude -p`                                                             | Agent SDK                                                                               |
| ---------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 호출 방식        | 셸에서 실행하고 stdout을 읽음[^headless]                                | `query()` 같은 함수가 메시지를 하나씩 돌려줌[^loop]                                     |
| 언어             | 아무 언어에서나 하위 프로세스로 호출                                    | Python, TypeScript                                                                      |
| 출력             | `text`, `json`, `stream-json`[^cli]                                     | 타입이 있는 메시지 객체(`SystemMessage`, `AssistantMessage`, `ResultMessage` 등)[^loop] |
| hooks            | 설정 파일에 적은 셸 명령 hooks                                          | 옵션에 넘기는 콜백 함수, 그리고 `settingSources`가 켜져 있으면 설정 파일 hooks[^hooks]  |
| 사용자 정의 도구 | `--mcp-config`로 외부 MCP 서버를 연결[^cli]                             | 같은 프로세스 안의 MCP 서버(`@tool`, `tool()`)[^tools]                                  |
| 권한 응답        | `--permission-mode`, `--allowedTools`, `--permission-prompt-tool`[^cli] | 위 옵션에 더해 `canUseTool` 콜백[^perms]                                                |
| 구조화 출력      | `--json-schema`[^cli]                                                   | `outputFormat` / `output_format` 옵션[^structured]                                      |
| 세션 이어가기    | `--continue`, `--resume`, `--fork-session`[^cli]                        | `continue`, `resume`, fork 옵션과 `SessionStore`[^sessions]                             |
| 비용·횟수 제한   | `--max-turns`, `--max-budget-usd`[^cli]                                 | `max_turns`, `max_budget_usd`와 결과 메시지의 `total_cost_usd`[^cost]                   |
| 프로세스 수명    | 호출 한 번에 프로세스 하나(추론)                                        | 스트리밍 입력 모드에서는 한 호출이 여러 사용자 턴을 이어감[^cost]                       |

## SDK 쓰는 법

### 가장 작은 예제

두 언어 모두 `query()`가 메시지 스트림을 돌려주고,
에이전트가 끝나면 `ResultMessage`가 마지막에 온다.[^loop]

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "auth.py의 버그를 찾아서 고쳐줘",
  options: { allowedTools: ["Read", "Edit", "Bash"] },
})) {
  if (message.type === "result") console.log(message.result);
}
```

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="auth.py의 버그를 찾아서 고쳐줘",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)

asyncio.run(main())
```

### 에이전트 루프의 메시지와 종료 조건

메시지는 다섯 종류다.
`SystemMessage`(`init`, `compact_boundary` 등), `AssistantMessage`,
`UserMessage`, `StreamEvent`, `ResultMessage`다.[^loop]
결과의 하위 유형은 `success`, `error_max_turns`, `error_max_budget_usd`,
`error_during_execution`, `error_max_structured_output_retries`로 나뉜다.[^loop]
`max_turns`와 `max_budget_usd`로 루프를 제한하고, `effort`로 추론 강도(`low`,
`medium`, `high`, `xhigh`, `max`)를 정한다.[^loop]

### 이름 변경과 기본값 변경

이 SDK는 Claude Code SDK에서 이름이 바뀐 것이다.
Python의 `ClaudeCodeOptions`는 `ClaudeAgentOptions`가 되었고,
패키지는 `claude_code_sdk`에서 `claude_agent_sdk`로 바뀌었다.[^migration]
시스템 프롬프트는 더 이상 Claude Code 기본값이 아니다.
Claude Code의 프롬프트를 쓰려면 `systemPrompt: { type: “preset”,
preset: “claude_code” }`로 명시해야 한다.[^migration]
`settingSources`를 생략하면 사용자, 프로젝트,
로컬 설정을 모두 읽어 CLI와 같게 동작한다.[^migration]
다른 사용자의 데이터를 다루는 서비스라면 `settingSources: []`로 파일 설정을 끊어
격리해야 한다.[^migration]

### 권한 평가 순서

도구 호출은 hooks, 거부 규칙, 확인 규칙, 권한 모드, 허용 규칙,
`canUseTool` 콜백 순서로 평가된다.[^perms]
권한 모드는 `default`, `acceptEdits`, `plan`, `dontAsk`, `auto`,
`bypassPermissions`다.[^perms]
앞 단계에서 이미 결정된 호출은 뒤 단계까지 가지 않으므로,
막아야 할 것은 hooks나 거부 규칙에 두는 편이 확실하다.

### hooks

hooks는 도구 호출 전후나 세션 시작, 중지 같은 이벤트에서 코드를 실행하는
콜백이다.[^hooks]
`PreToolUse`에서 `permissionDecision: "deny"`를 돌려주면 호출을 막을 수
있다.[^hooks]
다만 `Write|Edit` 매처는 Write와 Edit 도구만 걸러서,
Claude가 Bash 명령으로 `.env`를 쓰면 그 hook은 돌지 않는다.[^hooks]
이벤트 종류는 Python과 TypeScript가 다르다.
`PreToolUse`, `PostToolUse`, `Stop`, `SubagentStart`, `SubagentStop`,
`UserPromptSubmit`, `PermissionRequest`, `Notification` 등은 양쪽에 있고,
`SessionStart`, `SessionEnd`, `PostToolBatch` 등은 TypeScript에만 있다.[^hooks]

### subagents

subagent는 메인 에이전트가 띄우는 별도의 에이전트 인스턴스로, 컨텍스트 격리,
병렬 실행, 전용 지시문, 도구 제한을 준다.[^subagents]
`agents` 옵션으로 프로그램에서 정의하며,
`description`과 `prompt`가 필수이고 `tools`, `model`, `maxTurns`,
`permissionMode` 등을 고른다.[^subagents]
subagent는 부모의 대화 기록을 받지 않고,
부모가 Agent 도구 호출에 적은 프롬프트 문자열만 받는다.[^subagents]
필요한 파일 경로나 오류 메시지는 그 프롬프트에 직접 적어야 한다.[^subagents]
기본적으로 subagent는 백그라운드에서 돌고,
결과는 이후 턴에 도착한다.[^subagents]

### 사용자 정의 도구와 MCP

사용자 정의 도구는 이름, 설명, 입력 스키마, 핸들러 네 요소로 만든다.[^tools]
TypeScript는 `tool()`과 Zod 스키마를, Python은 `@tool` 데코레이터를 쓰고,
`create_sdk_mcp_server` 또는 `createSdkMcpServer`로 같은 프로세스 안의 MCP
서버로 묶어 `mcpServers`에 넘긴다.[^tools]
부작용이 없는 도구에 `readOnlyHint: true`를 달면 Claude가 그 도구를 병렬로
호출할 수 있다.[^tools]
외부 MCP 서버는 같은 `mcpServers` 옵션으로 연결하며,
도구가 많으면 tool search로 필요할 때만 불러온다.[^mcp]

### 구조화 출력

JSON Schema를 `outputFormat`(TypeScript)이나 `output_format`(Python)에 넘기면
결과 메시지의 `structured_output`에 검증된 데이터가 담긴다.[^structured]
SDK는 JSON Schema draft-07로 검증하므로 Zod는 `target: "draft-7"`로 변환해야
한다.[^structured]
검증이 재시도 한도 안에 성공하지 못하면 데이터 대신
`error_max_structured_output_retries` 결과가 돌아온다.[^structured]

### 세션

세션은 대화 기록을 디스크에 저장하고, `continue`는 가장 최근 세션을,
`resume`은 ID로 지정한 세션을 이어가며,
fork는 원본을 보존한 채 갈라진다.[^sessions]
서버리스 함수나 자동 확장 워커처럼 파일 시스템을 공유하지 않는 환경에서는
`SessionStore`로 대화 기록을 객체 저장소나 데이터베이스에 미러링해,
한 호스트에서 만든 세션을 다른 호스트에서 이어간다.[^sessionstore]

### 비용 추적

결과 메시지의 `total_cost_usd`는 클라이언트가 번들된 가격표로 계산한 추정치이며,
청구 데이터가 아니다.[^cost]
가격이 바뀌었거나, 설치한 SDK가 모델을 모르거나,
클라이언트가 모델링하지 못하는 청구 규칙이 있으면 실제 청구액과 어긋난다.[^cost]
사용자에게 요금을 매기거나 재무 판단을 하는 데 이 값을 쓰면 안 되고,
정확한 값은 Usage and Cost API나 Console의 Usage 페이지에서 확인해야
한다.[^cost]
같은 메시지 ID를 가진 어시스턴트 메시지는 사용량이 같으므로 ID로 중복을 제거해야
이중 집계가 없다.[^cost]
`-p`의 `--max-budget-usd`도 같은 추정치를 기준으로 상한을 건다.[^cli]

## 배포

### 실행 형태와 자원

호스팅 공식 문서는 단발 실행(ephemeral), 장기 실행(long-running), 혼합(hybrid),
한 컨테이너에 여러 에이전트를 두는 형태를 소개한다.[^hosting]
에이전트 하나당 RAM 1GiB, 디스크 5GiB, CPU 1개를 시작점으로 권하지만,
이는 막 시작한 인스턴스의 값이고 세션이 길어지면 메모리가 늘어난다.[^hosting]
SDK는 `claude` 하위 프로세스를 stdio로 띄워 관리하므로,
컨테이너 안에 그 프로세스가 돌 자리와 Node.js 18.14 이상 또는 Python 3.10 이상이
있어야 한다.[^hosting]

### 보안

에이전트는 처리하는 파일, 웹페이지, 사용자 입력에 든 지시에 영향을 받을 수 있다.
공식 보안 가이드는 이를 프롬프트 인젝션(prompt injection)이라 부르고,
다층 방어를 권한다.[^secure]
권한 시스템은 bash 명령을 AST로 해석해 규칙과 맞춰 보지만,
샌드박스가 아니라 권한 관문(permission gate)이라고 가이드는 분명히
밝힌다.[^secure]
네트워크 통제와 샌드박스 모드를 함께 써야,
악성 파일이 고객 데이터를 외부로 보내라고 시켜도 요청 자체를 막을 수
있다.[^secure]
여러 사용자를 한 환경에서 다루면 `settingSources: []`와 환경 변수
`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`로 설정과 자동 메모리를 끊는다.[^secure]

## 고르는 기준

| 상황                                          | 선택                                    | 이유                                                       |
| --------------------------------------------- | --------------------------------------- | ---------------------------------------------------------- |
| 셸 스크립트나 CI에서 한 번 실행               | `claude -p --bare`                      | 플래그만으로 끝나고, 머신마다 같은 결과를 얻음             |
| Python/TypeScript 서비스 안에 에이전트를 넣음 | SDK                                     | 콜백, 타입이 있는 메시지, 같은 프로세스의 사용자 정의 도구 |
| 도구 호출마다 코드로 승인하거나 거부          | SDK의 `canUseTool`과 hooks              | 승인 로직을 함수로 쓸 수 있음                              |
| Go, Ruby, Rust 등 다른 언어 서비스            | `claude -p --output-format stream-json` | SDK가 없는 언어에서 같은 루프를 하위 프로세스로 구동       |
| 여러 사용자의 데이터를 다루는 서비스          | SDK + `settingSources: []`              | 사용자별 설정 유입을 끊음                                  |
| 루프를 직접 통제하고 싶음                     | Client SDK                              | 도구 루프를 직접 작성                                      |
| 호스팅까지 맡기고 싶음                        | Managed Agents                          | Anthropic이 루프와 샌드박스를 운영                         |

두 입구를 섞는 것도 가능하다.
예를 들어 개발 중에는 `claude -p`로 프롬프트와 도구 허용 목록을 빠르게 다듬고,
값이 정해지면 같은 옵션을 SDK의 `options`로 옮긴다.
두 입구가 같은 루프를 쓰므로 옵션 이름만 다를 뿐 동작이 같다는 점이 이
방식을 받쳐 준다.
다만 이 대응이 모든 옵션에서 일대일이라는 공식 보증은 찾지 못했다.
옮긴 뒤에는 결과를 다시 확인해야 한다.

## 개발 워크플로 자동화

Agent SDK로 개발 워크플로 전체를 자동화하는 예제다.
이 절의 코드는 이전 판의 문서에서 가져온 것으로,
이번에 공식 문서와 다시 맞춰 실행해 보지는 않았다.
옵션 이름과 기본값은 위의 이름 변경과 기본값 변경 절을 기준으로 확인해야 한다.

### Step 1: 프로젝트 분석 → 문서 생성

새 프로젝트에 투입됐을 때, 코드베이스를 분석해서 문서를 만든다.

```typescript
// analyze-project.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

async function analyzeAndDocument(projectPath: string) {
  const prompt = `
이 프로젝트를 분석해서 ARCHITECTURE.md 파일을 만들어줘.

포함할 내용:
- 프로젝트 개요 (무엇을 하는 프로젝트인지)
- 디렉터리 구조와 각 폴더의 역할
- 주요 모듈과 의존성 관계
- 데이터 흐름
- 외부 의존성 (API, DB 등)

package.json, 설정 파일들, 소스 코드를 모두 확인해.
`;

  for await (const message of query({
    prompt,
    options: {
      allowedTools: ["Read", "Glob", "Grep", "Write"],
      permissionMode: "acceptEdits",
      cwd: projectPath,
    },
  })) {
    if (message.type === "assistant") {
      console.log(message.content);
    }
  }
}

analyzeAndDocument(process.cwd());
```

### Step 2: 스펙 문서 작성

기능 요청을 받으면 구현 전에 스펙 문서를 먼저 작성한다.

```typescript
// write-spec.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

async function writeSpec(featureName: string, featureRequest: string) {
  const prompt = `
다음 기능 요청에 대한 스펙 문서를 작성해줘.

기능 요청:
${featureRequest}

출력 위치: specs/${featureName}/spec.md

스펙 문서에 포함할 내용:
1. 배경 및 목적
2. 요구사항 (필수/선택)
3. API 설계 (있다면)
4. 데이터 모델 변경사항
5. 영향받는 기존 코드
6. 테스트 시나리오
7. 고려사항 및 제약

먼저 기존 코드베이스를 분석해서 현재 구조를 파악한 뒤 작성해.
`;

  for await (const message of query({
    prompt,
    options: {
      allowedTools: ["Read", "Glob", "Grep", "Write"],
      permissionMode: "acceptEdits",
      cwd: process.cwd(),
    },
  })) {
    if (message.type === "assistant") {
      console.log(message.content);
    }
  }
}

writeSpec("avatar-upload", "사용자 프로필에 아바타 이미지 업로드 기능 추가");
```

### Step 3: 계획 수립 (Plan 모드)

스펙을 바탕으로 구현 계획을 세운다.
아직 코드는 건드리지 않는다.

```typescript
// plan-implementation.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

async function planImplementation(featureName: string) {
  const prompt = `
specs/${featureName}/spec.md 스펙 문서를 읽고 구현 계획을 세워줘.

출력 위치: specs/${featureName}/plan.md

포함할 내용:
1. 변경/생성할 파일 목록
2. 각 파일별 변경 내용 요약
3. 구현 순서 (의존성 고려)
4. 예상되는 위험 요소

코드는 작성하지 말고 계획만 세워.
`;

  for await (const message of query({
    prompt,
    options: {
      allowedTools: ["Read", "Glob", "Grep", "Write"],
      permissionMode: "acceptEdits",
      cwd: process.cwd(),
    },
  })) {
    if (message.type === "assistant") {
      console.log(message.content);
    }
  }
}

planImplementation("avatar-upload");
```

### Step 4: 구현 (Edit 모드)

계획대로 코드를 작성한다.

```typescript
// implement.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

async function implement(featureName: string) {
  const prompt = `
specs/${featureName}/plan.md 계획 문서를 읽고 구현해줘.

규칙:
- 계획에 있는 파일만 수정
- 기존 코드 스타일 따르기
- 각 파일 수정 후 무엇을 했는지 설명

테스트 코드도 함께 작성해.
`;

  for await (const message of query({
    prompt,
    options: {
      allowedTools: ["Read", "Glob", "Grep", "Write", "Edit", "Bash"],
      permissionMode: "acceptEdits",
      cwd: process.cwd(),
    },
  })) {
    if (message.type === "assistant") {
      console.log(message.content);
    }
  }
}

implement("avatar-upload");
```

### Step 5: 커밋

구현이 끝나면 의미 있는 단위로 커밋하는 단계다.

```typescript
// commit-changes.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

async function commitChanges() {
  const prompt = `
현재 변경사항을 확인하고 적절한 커밋을 만들어줘.

규칙:
- git status로 변경사항 확인
- 관련 있는 파일끼리 묶어서 커밋
- 제목은 동사 원형으로 시작 (Add, Fix, Update, Remove 등)
- 제목은 50자 이내
- 제목과 본문 사이에 빈 줄
- 본문에 왜(why) 이 변경을 했는지 설명
- 본문은 72자에서 줄바꿈

큰 변경이면 여러 커밋으로 나눠.
`;

  for await (const message of query({
    prompt,
    options: {
      allowedTools: ["Read", "Bash"],
      cwd: process.cwd(),
    },
  })) {
    if (message.type === "assistant") {
      console.log(message.content);
    }
  }
}

commitChanges();
```

### Step 6: 코드 리뷰

커밋된 코드를 리뷰한다.

```typescript
// review-code.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

async function reviewCommits(baseBranch: string = "main") {
  const prompt = `
${baseBranch} 브랜치 대비 현재 브랜치의 변경사항을 리뷰해줘.

확인 항목:
1. 버그 가능성
2. 보안 취약점
3. 성능 이슈
4. 코드 스타일 일관성
5. 테스트 커버리지
6. 에러 처리

문제가 있으면 파일명:라인번호 형식으로 알려줘.
`;

  for await (const message of query({
    prompt,
    options: {
      allowedTools: ["Read", "Glob", "Grep", "Bash"],
      cwd: process.cwd(),
    },
  })) {
    if (message.type === "assistant") {
      console.log(message.content);
    }
  }
}

reviewCommits("main");
```

### Step 7: 리뷰 피드백 반영

리뷰 결과를 반영한다.

```typescript
// apply-feedback.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

async function applyFeedback(featureName: string) {
  const prompt = `
specs/${featureName}/review.md 파일의 리뷰 피드백을 읽고 코드를 수정해줘.

각 피드백 항목마다:
1. 해당 코드 찾기
2. 수정하기
3. 무엇을 왜 수정했는지 설명

수정 후 다시 커밋해.
`;

  for await (const message of query({
    prompt,
    options: {
      allowedTools: ["Read", "Glob", "Grep", "Write", "Edit", "Bash"],
      permissionMode: "acceptEdits",
      cwd: process.cwd(),
    },
  })) {
    if (message.type === "assistant") {
      console.log(message.content);
    }
  }
}

applyFeedback("avatar-upload");
```

## 전체 워크플로 통합

위 단계들을 하나의 파이프라인으로 연결할 수 있다.

```typescript
// dev-pipeline.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

type Stage = "spec" | "plan" | "implement" | "commit" | "review";

async function runPipeline(featureRequest: string, startFrom: Stage = "spec") {
  const stages: Stage[] = ["spec", "plan", "implement", "commit", "review"];
  const startIndex = stages.indexOf(startFrom);

  for (const stage of stages.slice(startIndex)) {
    console.log(`\n=== ${stage.toUpperCase()} ===\n`);

    // 각 단계별 프롬프트와 도구 설정
    // ... (위 함수들 조합)

    // 사용자 확인 후 다음 단계로
    const proceed = await askUser(`${stage} 완료. 계속할까요? (y/n)`);
    if (!proceed) break;
  }
}

runPipeline("사용자 프로필에 아바타 이미지 업로드 기능 추가");
```


## 비평

### 같은 에이전트의 두 입구라는 설명은 어디까지 맞는가

공식 문서는 `claude -p`를 CLI로 쓰는 Agent SDK라고 소개한다.[^headless]
이 설명이 가장 강하게 성립하는 범위는 에이전트 루프와 도구와 권한 규칙이다.
두 입구가 같은 바이너리를 쓰기 때문이다.
그 설명이 약해지는 곳은 기본값이다.
`claude -p`는 작업 디렉터리와 `~/.claude`의 설정을 읽는 상호작용 세션처럼
시작하고, SDK는 `settingSources`를 생략하면 사용자, 프로젝트,
로컬 설정을 읽는다.[^headless][^migration]
둘 다 환경의 설정을 끌어들이는 쪽이 기본이므로,
같은 코드를 개발자 노트북과 CI에서 돌리면 결과가 갈릴 수 있다.
이 주장을 뒤집는 관찰은 `--bare`로 같은 프롬프트를 서로 다른 머신에서 돌렸는데도
결과가 갈리는 경우다.
그런 경우가 나오면 원인은 설정 유입이 아니라 모델이나 도구 환경의 차이일 것이다.

### 비용 수치는 예산 도구이지 청구 근거가 아니다

`--max-budget-usd`와 `max_budget_usd`는 클라이언트가 계산한 추정치에 상한을
건다.[^cost][^cli]
그 추정치는 가격이 바뀌거나 SDK가 모델을 모르면 어긋난다.[^cost]
그러므로 이 상한은 과도한 지출을 막는 안전장치로는 유용하지만,
사용자별 과금이나 예산 집행의 근거가 될 수 없다.
정확한 지출을 알아야 하는 서비스는 Usage and Cost API를 별도로 읽어야
한다.[^cost]

### 권한 규칙은 샌드박스가 아니다

hooks 문서의 예제는 Write와 Edit 호출만 막고,
Bash로 같은 파일을 쓰는 길은 열려 있다고 스스로 경고한다.[^hooks]
보안 가이드도 권한 시스템이 샌드박스가 아니라 권한 관문이라고 밝힌다.[^secure]
이 두 문서를 함께 읽으면, 허용 목록과 hook만으로 민감한 파일을 지켰다고 판단하는
설계는 근거가 약하다.
Bash를 허용하는 에이전트에는 파일 시스템과 네트워크 단위의 격리를
따로 둬야 한다.

## 체크리스트

1. 실행 형태를 정했는가: 스크립트 한 번이면 `claude -p`, 서비스 내부면 SDK.
2. CI와 무인 실행에는 `--bare`를 붙였고, `ANTHROPIC_API_KEY`를 환경에 두었는가.
3. 승인해 줄 사람이 없는 실행에 `--permission-mode`와 `--allowedTools` 또는 `--permission-prompts none`을 정했는가.
4. 외부에서 받은 저장소를 여는 자동화에서 프로젝트의 hooks와 `.mcp.json`이 돌아도 되는지 확인했는가.
5. 다중 사용자 서비스에 `settingSources: []`와 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`을 적용했는가.
6. `max_turns`와 `max_budget_usd`(또는 `--max-turns`, `--max-budget-usd`)를 걸었는가.
7. 결과를 프로그램이 읽는다면 `--json-schema`나 `outputFormat`으로 구조화했고, 검증 실패 결과를 처리하는가.
8. Bash를 허용했다면 샌드박스나 컨테이너 격리를 따로 두었는가.
9. 비용 필드를 청구 근거로 쓰지 않고 Usage and Cost API와 대조하는가.
10. SDK를 올릴 때 번들된 CLI 바이너리도 함께 바뀐다는 점을 릴리스 노트로 확인하는가.

## 기억할 원칙

SDK와 `claude -p`는 입구만 다른 같은 에이전트이므로,
먼저 `claude -p --bare`로 프롬프트와 권한을 정하고,
앱 안에서 콜백이나 같은 프로세스의 도구가 필요해지는 시점에 SDK로 옮긴다.
옮길 때는 설정 유입(`settingSources`)과 시스템 프롬프트 기본값을 명시해 두
환경이 같은 조건에서 돌게 한다.

## 다음 단계

- [Demo Repository](https://github.com/anthropics/claude-agent-sdk-demos)에서 Research Agent(멀티에이전트) 예제를 확인한다.
- [Python SDK](https://github.com/anthropics/claude-agent-sdk-python)의 hooks로 위험한 명령을 차단해 본다.

---

[^quickstart]: Anthropic, [Quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)

[^hosting]: Anthropic, [Hosting the Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting)

[^headless]: Anthropic, [Run Claude Code programmatically](https://code.claude.com/docs/en/headless)

[^cli]: Anthropic, [CLI reference](https://code.claude.com/docs/en/cli-reference)

[^loop]: Anthropic, [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop)

[^hooks]: Anthropic, [Intercept and control agent behavior with hooks](https://code.claude.com/docs/en/agent-sdk/hooks)

[^tools]: Anthropic, [Give Claude custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools)

[^perms]: Anthropic, [Configure permissions](https://code.claude.com/docs/en/agent-sdk/permissions)

[^structured]: Anthropic, [Get structured output from agents](https://code.claude.com/docs/en/agent-sdk/structured-outputs)

[^sessions]: Anthropic, [Work with sessions](https://code.claude.com/docs/en/agent-sdk/sessions)

[^sessionstore]: Anthropic, [Persist sessions to external storage](https://code.claude.com/docs/en/agent-sdk/session-storage)

[^cost]: Anthropic, [Track cost and usage](https://code.claude.com/docs/en/agent-sdk/cost-tracking)

[^migration]: Anthropic, [Migrate to Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/migration-guide)

[^subagents]: Anthropic, [Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents)

[^mcp]: Anthropic, [Connect to external tools with MCP](https://code.claude.com/docs/en/agent-sdk/mcp)

[^secure]: Anthropic, [Securely deploying AI agents](https://code.claude.com/docs/en/agent-sdk/secure-deployment)
