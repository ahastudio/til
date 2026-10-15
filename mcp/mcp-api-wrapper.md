# 기존 REST API에 MCP 엔드포인트를 붙여 LLM에 노출하기

원문: [Wrapping an Existing API with MCP: How to Expose Your Current APIs to LLMs](https://www.linkedin.com/pulse/copy-wrapping-existing-api-mcp-how-expose-your-current-apis-llms-gzbte/)

## 소개

프리랜서 개발자 매칭 회사 Gun.io가 2025년 5월 23일 LinkedIn에 올린 글이다.
엔지니어들이 실제로 쓰는 도구를 소개하는 Open Spaces 연재의 두 번째 편으로,
풀스택 아키텍트 Tim Kleier가 썼다.
요지는 기존 API를 고치지 않고 같은 서버에 `/mcp` 엔드포인트를 하나 더 열면
Claude 같은 LLM이 그 API의 기능을 도구로 쓸 수 있다는 것이다.

예시는 고객 지원 티켓을 만드는 SaaS 회사의 Node.js API다.
지원팀이 Claude에 프롬프트를 주면 Claude가 `create_ticket` MCP 도구를 호출하고,
그 도구가 기존 API와 같은 함수로 Milwaukee에 사는 Mark의 티켓을 만든다.
글은 전체 코드를
GitHub 저장소 `upgrade-solutions/mcp-api-wrapper`에 두었다고 하지만,
2026년 10월 현재 이 저장소는 GitHub API에서 찾을 수 없다.
본문의 코드는 모두 이미지로 들어 있어 아래 내용은 이미지를 읽어 옮긴 것이다.

## 동작 방식

### MCP 도구의 세 요소

글은 MCP 도구를 모델이 취할 수 있는 행동의 설명으로 정의하고,
이름(`create_ticket`), 설명(“Creates a new support ticket”),
입력 스키마(`customer_email`, `customer_name`, `issue_message`, `issue_type`)
세 가지로 구성된다고 설명한다.
모델은 설명과 스키마를 읽고 언제 어떤 인자로 도구를 부를지 정한다.

### 같은 함수, 두 개의 입구

글의 핵심 설계는 비즈니스 로직 함수 `createTicket()`을 공유하는 것이다.
기존 REST 엔드포인트 `POST /tickets`도 이 함수를 부르고,
MCP 도구 `create_ticket`도 이 함수를 부른다.
LLM 전용 로직을 따로 만들지 않으므로 검증 규칙과 저장 방식이 두 경로에서 같다.

별도의 MCP 서버 프로세스를 띄우지 않고,
기존 Express 앱에 `/mcp` 라우트를 추가해
Streamable HTTP 전송으로 MCP를 노출한다.
MCP 클라이언트가 이 엔드포인트에 연결하면
`initialize`와 `tools/list`를 거쳐 사용 가능한 도구 목록을 받는다.
글은 MCP Inspector로 연결해 `create_ticket`과 그 인자가 보이는지 확인한다.

### 요청 흐름

```text
지원팀 프롬프트 → Claude Desktop
  → mcp-remote (로컬 stdio ↔ 원격 HTTP 다리)
  → POST /mcp (Streamable HTTP)
  → create_ticket 도구 핸들러
  → createTicket()  ← POST /tickets도 같은 함수를 부른다
```

글을 쓸 당시 Claude Desktop 설정 파일은 로컬 명령을 실행하는 방식이라,
`npx mcp-remote <URL>`로 원격 HTTP 엔드포인트를 stdio로 이어 붙였다.

## 구현하기

### 원문 코드

기존 REST 엔드포인트다.

```typescript
// Create ticket through POST request
app.post('/tickets', async (req: Request, res: Response) => {
  const { customer_email, customer_name, issue_message, issue_type } = req.body;
  const ticket = await createTicket({
    customer_email,
    customer_name,
    issue_message,
    issue_type,
  });
  res.status(201).json({
    message: 'Ticket created successfully',
    data: ticket,
  });
});
```

같은 함수를 부르는 MCP 도구다.
입력 스키마는 zod로 정의하고,
`.describe()`의 문자열이 모델에 전달되는 설명이 된다.

```typescript
// A create_ticket server tool exposed at /mcp
server.tool(
  'create_ticket',
  'Creates a new support ticket',
  {
    customer_email: z.string().describe('Customer email address'),
    customer_name: z.string().describe('Customer name'),
    issue_message: z.string().describe('Customer message'),
    issue_type: z.enum(['bug', 'feature_request', 'other']).describe('Type of issue'),
  },
  async ({ customer_email, customer_name, issue_message, issue_type }) => {
    const ticket = { customer_email, customer_name, issue_message, issue_type };
    await createTicket(ticket);
    return {
      content: [{ type: 'text', text: `Ticket created for ${customer_name} (${customer_email}).` }],
    };
  }
);
```

원문 이미지의 마지막 `text` 값에는 백틱이 빠져 있어
그대로 옮기면 문법 오류가 난다.
위 코드는 템플릿 리터럴로 고친 것이다.

`/mcp` 엔드포인트다.

```typescript
// Expose the MCP server over HTTP
app.post('/mcp', async (req: Request, res: Response) => {
  const transport: StreamableHTTPServerTransport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
  });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});
```

`sessionIdGenerator: undefined`는 세션을 만들지 않는 무상태(stateless) 모드다.

### 실행 가능한 전체 예제

원문 조각을 하나의 파일로 합친 것이다.
원문은 서버 객체 하나를 모든 요청에서 재사용하지만,
아래 코드는 요청마다 서버와 전송을 새로 만든다.
무상태 모드에서 여러 클라이언트가 동시에 들어오면
하나의 서버 객체에 전송이 계속 다시 연결되며 요청 ID가 섞일 수 있기 때문이다.

```typescript
// index.ts
// npm i express zod @modelcontextprotocol/sdk && npm i -D tsx @types/express
import express, { Request, Response } from 'express';
import { z } from 'zod';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';

type Ticket = {
  customer_email: string;
  customer_name: string;
  issue_message: string;
  issue_type: 'bug' | 'feature_request' | 'other';
};

const tickets: (Ticket & { id: number })[] = [];

// REST와 MCP가 공유하는 유일한 비즈니스 로직
async function createTicket(input: Ticket) {
  const ticket = { id: tickets.length + 1, ...input };
  tickets.push(ticket);
  return ticket;
}

function buildMcpServer() {
  const server = new McpServer({ name: 'support-api', version: '1.0.0' });
  server.tool(
    'create_ticket',
    'Creates a new support ticket',
    {
      customer_email: z.string().email().describe('Customer email address'),
      customer_name: z.string().describe('Customer name'),
      issue_message: z.string().describe('Customer message'),
      issue_type: z.enum(['bug', 'feature_request', 'other']).describe('Type of issue'),
    },
    async (args) => {
      const ticket = await createTicket(args);
      return {
        content: [{ type: 'text', text: `Ticket #${ticket.id} created for ${ticket.customer_name}.` }],
      };
    }
  );
  return server;
}

const app = express();
app.use(express.json());

app.post('/tickets', async (req: Request, res: Response) => {
  const ticket = await createTicket(req.body);
  res.status(201).json({ message: 'Ticket created successfully', data: ticket });
});

app.post('/mcp', async (req: Request, res: Response) => {
  // 무상태 모드: 요청마다 서버와 전송을 새로 만들고, 응답이 끝나면 닫는다
  const server = buildMcpServer();
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  res.on('close', () => {
    transport.close();
    server.close();
  });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

const port = Number(process.env.PORT ?? 3000);
app.listen(port, () => console.log(`support-api on http://localhost:${port}`));
```

```bash
npx tsx index.ts
```

### Claude Desktop 연결

원문의 설정이다.
`mcp-remote`가 Claude Desktop과 원격 HTTP 엔드포인트 사이를 잇는다.

```json
{
  "mcpServers": {
    "support-api": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:3000/mcp"]
    }
  }
}
```

설정을 고친 뒤 Claude를 다시 시작해야 도구가 보인다.

## 확인하기

MCP Inspector로 연결해 도구 목록을 본다.

```bash
npx @modelcontextprotocol/inspector
```

Transport Type을 Streamable HTTP로,
URL을 `http://localhost:3000/mcp`로 두고 연결한다.
History에 `initialize`와 `tools/list`가 찍히고
`create_ticket`이 보이면 노출은 된 것이다.
Inspector에서 도구를 직접 실행해 본 뒤 REST로 같은 데이터가 보이는지 확인하면
두 입구가 같은 함수를 쓰는지까지 검증된다.

원문 스크린숏의 Inspector는 `localhost:4000/mcp`에,
Claude 설정은 `localhost:3000/mcp`에 연결되어 있다.
따라 할 때는 둘 중 하나로 맞춰야 한다.

## 트레이드오프

### 같은 서버에 두면 간단하지만 경계가 사라진다

`/mcp`를 기존 API에 붙이면 배포 단위도, 인증 미들웨어도, 로깅도 그대로 공유한다.
별도 MCP 서버를 운영할 때 생기는 버전 불일치나 네트워크 홉이 없다.
글이 “별도의 MCP 서버를 만들 필요가 없다”고 강조하는 이유다.

대가는 사람이 쓰는 API와 모델이 쓰는 API가 같은 장애 도메인에 묶인다는 점이다.
에이전트가 루프에 빠져 도구를 수천 번 호출하면
그 부하는 고객이 쓰는 API에 그대로 간다.
속도 제한, 감사 로그, 권한 범위를 MCP 경로에만 따로 걸 수 있도록
라우트 수준에서라도 분리해 두지 않으면 나중에 떼어 내기 어렵다.

### 함수 공유는 일관성을 주지만 사람용 계약을 그대로 넘긴다

`createTicket()`을 공유하면 검증과 저장 규칙이 하나다.
그러나 사람용 API는 호출자가 화면을 보고 입력을 확인했다는 가정 위에 있다.
LLM은 대화에서 이메일 주소를 추측하거나 잘못 옮길 수 있다.
원문 스키마는 `customer_email`을 단순 `z.string()`으로 받는데,
사람용 폼에서는 화면이 막아 주던 오류가 모델 경로에서는 그대로 저장된다.
도구 스키마는 사람용 API보다 엄격해야 한다.

### 자동 래핑은 쉽지만 좋은 도구가 되지는 않는다

API 엔드포인트 하나를 도구 하나로 옮기는 방식은 시작하기 쉽다.
하지만 REST API는 프로그래머가 조합해 쓰도록 잘게 나뉘어 있고,
모델은 도구가 많고 잘게 쪼개질수록 고르기 어려워한다.
티켓 생성처럼 하나의 작업이 하나의 엔드포인트에 대응하는 경우는 잘 맞지만,
조회, 수정, 승인을 여러 번 오가야 하는 작업이라면
작업 단위로 묶은 도구를 따로 설계해야 한다.

## 안전한 도입 순서

처음부터 생성·수정 도구를 열지 말고
조회 전용 도구 하나로 권한과 호출 기록을 시험한다.
모델이 잘못된 입력을 만들었을 때
스키마와 서버 검증이 각각 어디서 막는지도 확인한다.

그다음 부작용이 있는 도구를 추가할 때는
허용된 작업과 대상 범위를 명시하고,
중복 호출을 막을 키와 사람의 승인 조건을 정한다.
성공 응답에는 이후 대화에서 다시 쓸 식별자와
실제로 완료된 작업을 함께 돌려준다.

운영에서는 도구별 호출량, 오류, 재시도,
사용자 취소를 구분해 관찰한다.
정상 요청과 공격성 입력을 모두 시험하고,
문제가 생겼을 때 MCP 경로만 즉시 비활성화할 수 있어야 한다.
이 경계가 없다면 간편한 라우트 추가가
기존 고객 API 전체의 장애나 권한 위험으로 번질 수 있다.

## 함정

- 원문에는 인증이 없다.
  `/mcp`를 공개 주소에 열면 누구나 티켓을 만들 수 있다.
  글은 MCP가 LLM이 “안전하게” 시스템과 상호작용하게 한다고 하지만,
  안전은 MCP가 아니라 엔드포인트 앞의 인증과 권한이 만든다.
- 도구 설명은 사실상 프롬프트다.
  “Creates a new support ticket”만으로는 모델이 언제 호출해야 하는지,
  중복 티켓을 피해야 하는지 알 수 없다.
  호출 조건과 부작용을 설명에 적어야 한다.
- 생성처럼 부작용이 있는 도구는 모델이 재시도할 때 중복 생성을 만든다.
  멱등 키나 중복 검사가 없으면 같은 티켓이 여러 번 생긴다.
- 원문의 MCP 도구 핸들러는 `createTicket()`의 결과를 버리고
  이름과 이메일만 돌려준다.
  생성된 티켓 ID를 돌려줘야 모델이 이후 대화에서 그 티켓을 가리킬 수 있다.
- 이 글은 2025년 5월 기준이다.
  `mcp-remote` 다리, 설정 파일 형식, SDK의 도구 등록 API는 이후 바뀌었을 수 있다.
  현재 명세는 [MCP 2026-07-28 명세](mcp-2026-07-28-spec.md) 문서를 참고한다.

## 체크리스트

- [ ] REST와 MCP 도구가 같은 비즈니스 로직 함수를 호출하는가
- [ ] `/mcp` 앞에 인증과 권한 검사가 있는가
- [ ] MCP 경로에만 따로 속도 제한과 감사 로그를 걸었는가
- [ ] 도구 입력 스키마가 사람용 API보다 엄격한가 (이메일 형식, enum, 길이)
- [ ] 부작용이 있는 도구에 중복 방지 장치가 있는가
- [ ] 도구 응답에 이후 대화에서 참조할 식별자가 들어 있는가
- [ ] MCP Inspector에서 `tools/list`와 실제 호출을 모두 확인했는가

## 기억할 원칙

### MCP는 새 시스템이 아니라 새 입구다

이 글에서 가장 쓸모 있는 생각은 MCP 서버를 별도의 시스템이 아니라
기존 API의 또 다른 입구로 보는 관점이다.
비즈니스 로직은 하나로 두고, 사람용 입구와 모델용 입구를 나란히 연다.
이렇게 하면 MCP 도입이 아키텍처 변경이 아니라 라우트 하나의 추가가 된다.

다만 입구가 늘면 지켜야 할 문도 는다.
모델용 입구는 사람용 입구보다 더 엄격한 검증, 더 좁은 권한,
더 자세한 기록이 필요하다.
로직을 공유하는 것과 계약을 공유하는 것은 다르다.
