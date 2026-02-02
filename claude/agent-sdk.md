# Claude Agent SDK

> **Claude Agent SDK**는 Claude Code의 에이전트 하네스를 라이브러리로 제공하여,
> 프로덕션 수준의 AI 에이전트를 구축할 수 있게 해주는 SDK입니다.
> 코드베이스 이해, 파일 편집, 명령 실행, 복잡한 워크플로 수행이 가능합니다.

<https://platform.claude.com/docs/ko/agent-sdk/overview>

<https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk>

<https://github.com/anthropics/claude-agent-sdk-demos>

## 시작하기

Node.js 18 이상, Claude Code CLI가 필요합니다.

```bash
npm install -g @anthropic-ai/claude-code
```

프로젝트 생성:

```bash
mkdir my-agent && cd my-agent
npm init -y
npm install @anthropic-ai/claude-agent-sdk
```

## 개발 워크플로 자동화

Agent SDK의 진짜 힘은 개발 워크플로 전체를 자동화하는 데 있습니다.

### Step 1: 프로젝트 분석 → 문서 생성

새 프로젝트에 투입됐을 때, 코드베이스를 분석해서 문서를 만듭니다.

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

기능 요청을 받으면 구현 전에 스펙 문서를 먼저 작성합니다.

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

스펙을 바탕으로 구현 계획을 세웁니다. 아직 코드는 건드리지 않습니다.

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

계획대로 코드를 작성합니다.

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

구현이 끝나면 의미 있는 단위로 커밋합니다.

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

커밋된 코드를 리뷰합니다.

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

리뷰 결과를 반영합니다.

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

위 단계들을 하나의 파이프라인으로 연결할 수 있습니다.

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

## 다음 단계

- [Demo Repository](https://github.com/anthropics/claude-agent-sdk-demos)에서
  Research Agent (멀티에이전트) 예제 확인
- [Python SDK](https://github.com/anthropics/claude-agent-sdk-python)의
  Hooks로 위험한 명령 차단하기
