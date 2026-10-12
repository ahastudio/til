# Eve: 디렉터리 하나로 에이전트를 정의하고 운영하는 Vercel 프레임워크

<https://vercel.com/eve>

<https://github.com/vercel/eve>

HN 토론: <https://news.ycombinator.com/item?id=48568061> (9점, 0개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=48580964> (4점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=35140>

## 소개

eve는 Vercel이 만든 오픈소스 에이전트 프레임워크다.
홈페이지는 스스로를 웹 앱의 Next.js 같은 것을 에이전트에 옮긴 것이라고 소개한다.
지침과 스킬은 Markdown으로, 도구는 TypeScript로 쓰고,
실행은 기본적으로 내구성(durable)을 갖춘다는 것이 한 줄 요약이다.
README는 eve를 “filesystem-first framework for durable AI agents”라고 부른다.
에이전트의 핵심 기능이 정해진 위치에 놓이므로 프로젝트를 들여다보고,
확장하고, 운영하기 쉬워진다는 주장이다.

발표 글 Introducing eve는 2026년 6월 17일에 올라왔다.
Vercel은 v0를 포함해 여러 해 동안 에이전트를 만들어 왔는데,
코딩 에이전트 덕분에 누구나 에이전트를 만들게 되자 팀마다 같은 배관을
반복해서 다시 짜고 있었다고 적는다.
에이전트에는 정해진 모양이 있고, eve는 그 모양을 프레임워크로 만든 것이라는
설명이다.
글에 따르면 Vercel은 사내에서 100개가 넘는 에이전트를 eve로 운영한다.
Slack에서 데이터 웨어하우스 질문에 답하는 d0는 한 달에 3만 건 넘는 질문을
처리하고, 지원 에이전트 Vertex는 티켓의 92%를 스스로 해결한다고 한다.
영업 리드를 다루는 Lead Agent는 연간 운영비가 약 5,000달러이고
그 32배를 돌려준다는 수치도 실려 있다.
이 수치는 모두 Vercel의 자체 발표다.

저장소 `vercel/eve`는 2026년 6월 16일에 만들어졌고 라이선스는 Apache-2.0이다.
10월 11일 기준 스타 5,517개, 포크 614개, 열린 이슈와 PR이 합쳐 760개다.
npm 패키지 이름은 그대로 `eve`이고, 최신 릴리스는 10월 10일의 `eve@0.76.3`이다.
10월 8일부터 10일 사이에만 `0.74.0`, `0.75.0`, `0.75.1`, `0.76.0`, `0.76.2`,
`0.76.3`이 나왔을 정도로 릴리스가 잦다.
README는 eve가 베타이며 정식 출시 전까지 프레임워크, API, 문서, 동작이
바뀔 수 있다고 밝힌다.
문서는 `eve.dev/docs`에 있고, 패키지 안에도 `node_modules/eve/docs`로 들어 있어
코딩 에이전트가 로컬에서 읽을 수 있다.

Vercel Labs는 소프트웨어 팩토리, 마케팅 팀, 콘텐츠 에이전트,
Contentful 연동 같은 eve 템플릿 저장소를 따로 공개하고 있다.
이 저장소의 `ai-tool/agent-device.md`도 Callstack이 eve로 모바일 QA 에이전트를
만든 글을 참고 자료로 언급한다.

## 동작 방식

### 디렉터리가 곧 에이전트 정의다

eve 에이전트는 `agent/` 디렉터리다.
필수 파일은 `instructions.md` 하나뿐이고, 나머지는 필요할 때 더한다.

| 경로                 | 역할                                                       |
| -------------------- | ---------------------------------------------------------- |
| `instructions.md`    | 항상 붙는 시스템 프롬프트, 이것만 있어도 동작하는 에이전트 |
| `agent.ts`           | 모델과 런타임 설정, 없으면 기본 모델 사용                  |
| `tools/*.ts`         | 모델이 호출하는 타입 있는 함수, 파일 이름이 도구 이름      |
| `skills/*.md`        | 필요할 때만 불러오는 절차서                                |
| `subagents/<이름>/`  | 자기 지침, 도구, 샌드박스를 가진 하위 에이전트             |
| `channels/*.ts`      | Slack, Discord, Teams, 웹 채팅 같은 접점                   |
| `connections/*.ts`   | MCP 서버나 OpenAPI 서비스 연결과 인증                      |
| `schedules/*`        | cron으로 스스로 시작하는 작업                              |
| `sandbox/sandbox.ts` | 샌드박스 백엔드와 초기 설정                                |

발표 글은 이를 Next.js가 폴더를 라우트로 바꾸는 방식에 빗댄다.
라우팅을 프레임워크가 쥐기 때문에 폴더가 라우트가 되듯,
eve가 에이전트 루프를 쥐기 때문에 파일 하나가 능력 하나가 된다는 것이다.
빌드할 때 eve가 도구와 스킬을 찾아 모델에 설명을 넘기고, 등록 코드는 따로 없다.

스킬은 `SKILL.md` 관례를 따르는 점진적 공개(progressive disclosure) 방식이다.
시스템 프롬프트에는 각 스킬의 이름과 설명만 올라가고,
요청이 설명과 맞으면 모델이 `eve__skill({ name })`으로 본문을 불러온다.
그래서 문서는 설명을 이름표가 아니라 라우팅 힌트로 쓰라고, 즉 그 스킬을
불러야 할 작업을 적으라고 권한다.
스킬이 많으면 `deferred: true`로 목록에서 빼고 `eve__search`로 찾게 할 수 있다.
스킬은 지침만 더할 뿐 새 실행 경로를 만들지 않으므로,
타입 있는 동작이 필요하면 도구를 써야 한다.

### 세션, 턴, 스텝

실행은 세 단계로 겹쳐 있다.
세션은 며칠이나 몇 주에 걸칠 수 있는 대화 전체이고,
턴은 사용자 메시지 하나와 그에 따른 모든 작업이며,
스텝은 턴 안의 내구성 체크포인트다.
기본적으로 스텝 하나는 모델 호출 한 번과 그 뒤에 이어지는 도구 호출을 담는다.

세션 하나가 오픈소스 Workflow SDK 위의 워크플로 하나로 돈다.
Vercel에 배포하면 Vercel Workflow가 쓰이고,
로컬 개발이나 직접 띄운 `eve start`에서는 `.eve/.workflow-data`에 상태를 쓰는
로컬 world가 쓰인다.
프로세스가 죽거나 시간 초과가 나거나 턴 도중 재배포가 일어나도
마지막으로 끝난 스텝부터 다시 이어 간다.
끝난 스텝은 다시 실행하지 않고 기록된 결과를 재생하지만,
실행 도중 끊긴 스텝은 처음부터 다시 실행한다.

승인이나 질문을 기다리는 턴은 컴퓨트를 쓰지 않고 멈춰(park) 있다가,
답이 오면 몇 초 뒤든 며칠 뒤든 멈춘 자리에서 이어진다.
긴 세션은 컨텍스트가 넘치기 전에 압축(compaction)되는데,
기본값은 컨텍스트 창의 90%에서 시작하고 `agent.ts`의
`compaction.thresholdPercent`로 바꾼다.
압축이 끝나면 eve는 쉬고 있는 세션을 같은 배포의 새 워크플로 실행으로 옮겨
실행 기록이 끝없이 쌓이지 않게 한다.

### 앱 런타임과 샌드박스의 경계

에이전트는 두 실행 환경에 걸쳐 있다.
앱 런타임은 신뢰하는 쪽으로, 에이전트 루프, 모델 호출, 직접 쓴 도구의
`execute`, 연결 클라이언트가 전부 여기서 `process.env`와 Node.js 전체를 쓰며
돈다.
Vercel에서는 이것이 Vercel Function이다.
샌드박스는 격리된 쪽으로, 모델이 셸 명령을 돌리고 파일을 읽고 쓰는 곳이다.
샌드박스에는 `process.env`도, 비밀도, 앱 런타임으로 돌아가는 길도 없다.

내장 `bash`, `read_file`, `write_file` 도구도 앱 런타임에 있으면서
샌드박스로 요청을 대신 넘긴다.
문서의 예로, 모델이 `charge_card` 도구를 부르면 `execute`가 앱 런타임에서
`STRIPE_KEY`를 읽어 Stripe를 호출하고 모델은 `{ ok: true }`만 본다.
MCP와 OpenAPI 연결의 토큰도 스텝 단위로 캐시될 뿐 내구성 상태에
직렬화되지 않고, 모델은 연결의 URL과 자격 증명을 보지 못한다.
샌드박스 안에서 비공개 저장소를 `git clone`해야 할 때는 Vercel Sandbox
방화벽이 일치하는 도메인 요청에 인증 헤더를 대신 넣어 주는
자격 증명 중개(credential brokering)를 쓴다.

루프와 샌드박스는 수명이 따로다.
워크플로가 멈춰 있는 동안 샌드박스 컴퓨트를 붙잡고 있지 않고,
코드가 필요할 때만 샌드박스를 열거나 다시 쓴다.
샌드박스 백엔드는 어댑터다.
Vercel에서는 하드웨어 수준 격리를 갖춘 Vercel Sandbox 마이크로VM이고,
그 밖의 환경에서는 Docker, microsandbox,
just-bash 순서로 쓸 수 있는 것을 고른다.

## 시작하기

Node.js 24 이상과 모델 자격 증명이 필요하다.
자격 증명은 ChatGPT 구독, Vercel 계정, AI Gateway, OpenAI, Anthropic API 키 중
하나를 터미널 UI에서 연결하면 되고, 로컬에서 대화할 때는 Vercel 프로젝트가
없어도 된다.

```bash
# 프로젝트 생성, 의존성 설치, Git 초기화 후 터미널 UI까지 연다
npx eve@latest init my-agent

# 다른 AI Gateway 모델과 추론 강도로 시작할 때
npx eve@latest init my-agent --model openai/gpt-6-luna --reasoning high

# 이미 package.json이 있는 프로젝트에 붙일 때, agent/ 파일을 만들기 전에 실행
npx eve@latest init .

# 나중에 다시 띄울 때
cd my-agent
npm run dev
```

README의 최소 예제는 지침 한 줄, 도구 하나, 모델 설정으로 끝난다.

```ts
// agent/tools/get_weather.ts — 파일 이름이 곧 도구 이름 get_weather
import { defineTool } from "eve/tools";
import { z } from "zod";

export default defineTool({
  description: "Return mock weather data for a city.",
  inputSchema: z.object({ city: z.string().min(1) }),
  async execute({ city }) {
    return { city, condition: "Sunny", temperatureF: 72 };
  },
});
```

```ts
// agent/agent.ts — 문자열 모델 ID는 Vercel AI Gateway를 거친다
import { defineAgent } from "eve";

export default defineAgent({
  model: "openai/gpt-6-luna-fast",
  reasoning: "high",
});
```

외부 쓰기 작업이 있는 도구에는 승인 정책을 붙인다.
현재 문서의 필드 이름은 `approval`이고,
`never()`, `once()`, `always()`, `auto()` 네 가지 도우미가 있다.
`auto()`는 별도의 결정 모델(기본값 `typesafe-ai/jev`)이 호출마다
`clear`인지 `caution`인지 판단하게 하며, 이때 도구 입력이 그 모델 제공자에게
전송된다.
입력에 따라 판단하려면 함수를 넘긴다.

```ts
// agent/tools/refund_charge.ts — 다른 테넌트는 거부, 1,000 초과만 사람 승인
import { defineTool } from "eve/tools";
import { z } from "zod";

export default defineTool({
  description: "Refund a charge.",
  inputSchema: z.object({
    tenantId: z.string(),
    chargeId: z.string(),
    amount: z.number(),
  }),
  approval: ({ session, toolInput }) => {
    const callerTenant = session.auth.current?.attributes.tenantId;
    if (callerTenant === undefined || callerTenant !== toolInput?.tenantId) {
      return { type: "denied", reason: "Caller cannot access this tenant." };
    }
    return (toolInput?.amount ?? 0) > 1000 ? "user-approval" : "not-applicable";
  },
  async execute(input) {
    // 실제 환불 호출은 여기서 앱 런타임의 비밀로 수행한다
    return { ok: true, chargeId: input.chargeId };
  },
});
```

웹 채팅을 붙이고 배포하는 흐름은 다음과 같다.

```bash
npx eve link                 # Vercel 프로젝트 연결
npx eve add channel/web      # Next.js 또는 TanStack Start 채팅 UI 생성
npx eve deploy               # vercel deploy --prod를 돌리고 환경 변수를 받아 온다
```

Vercel에 배포하면 생성된 출력으로 웹 런타임, Vercel Workflow,
Vercel Cron(스케줄), Vercel Sandbox가 함께 구성된다.
직접 운영하려면 `eve build` 뒤 `.output/`의 Nitro 서버를 `eve start`로 띄운다.

## 트레이드오프

### 관례가 배관을 대신하지만, 관례는 곧 Vercel 스택이다

eve가 덜어 주는 배관은 실제로 무겁다.
내구성 실행, 승인 대기 중 컴퓨트 해제, 세션 단위 샌드박스, 채널 서명 검증,
OAuth 토큰 갱신, OpenTelemetry 추적을 직접 엮으면 에이전트 자체보다
주변 코드가 더 커진다.
GN 소개글이 짚듯 이것은 파일 구조와 실행 인프라를 한꺼번에 주는 제안이다.

대가는 그 인프라의 기본값이 거의 전부 Vercel 제품이라는 점이다.
홈페이지는 AI Gateway, Vercel Sandbox, Drives, Workflows, Connect를
“no gluing point solutions together”라는 문구와 함께 묶어서 내세운다.
문자열 모델 ID는 AI Gateway를 거치고, 승인용 `auto()`와 자동 모델 선택의
기본 결정 모델도 Gateway로 호출된다.
문서가 직접 운영 경로를 제공하는 것은 사실이지만,
그 경로에서는 Workflow world, 샌드박스 제공자, 라우트 인증, 리버스 프록시를
스스로 골라 붙여야 한다.
즉 eve가 없애 준다는 배관 작업이 Vercel 밖에서는 상당 부분 되돌아온다.
HN에서 rishabhpoddar는 n8n이나 crewai 같은 도구와 쓰임새가 무엇이 다른지,
차별점이 결국 Next.js식 사용 편의와 배포인지를 물었다.[^rishabhpoddar]
문서를 읽은 뒤의 해석으로는, 차별점은 에이전트 기능 자체보다
내구성 실행과 격리 경계를 기본값으로 묶은 운영 모델에 있고,
그 운영 모델이 가장 매끄러운 곳이 Vercel이다.

### 내구성은 공짜가 아니라 재실행 의미론을 요구한다

체크포인트 덕분에 크래시와 재배포를 견디지만,
끊긴 스텝은 처음부터 다시 실행된다.
문서는 결제나 이메일처럼 멱등하지 않은 부작용은 멱등하게 만들거나
승인으로 막으라고 명시한다.
스텝이 이미 스트림에 쓴 이벤트는 남고 재실행이 같은 이벤트를 새 id로
다시 내보내므로, 스트림 소비자는 두 시도를 모두 본다.
실험 옵션 `workflow.modelCallsPerStep`으로 여러 모델 호출을 한 스텝에 묶으면
체크포인트 비용은 줄지만, 묶음 전체가 하나의 재실행 단위가 되어
앞선 도구 실행까지 반복될 수 있다.
체크포인트 오버헤드와 중복 실행 범위 사이에서 고를 수는 있어도,
둘 다 없앨 수는 없다.

### 긴 세션과 잦은 업그레이드는 서로 부딪힌다

세션은 기본 30일(`sessionTimeoutMs`)까지 살 수 있는데,
워크플로 실행은 그것을 시작한 eve 버전만 재생할 수 있다.
Vercel Workflow에서는 실행이 원래 배포에 남고 쉬는 세션만 새 배포로 넘어가지만,
로컬 world나 Postgres 같은 다른 world에서는 eve 버전이 바뀌는 업그레이드마다
기존 세션이 좌초(stranded)된다.
좌초된 루트 세션은 채널 주소로 새 메시지가 오면 초기화되고 새 세션이 시작되며,
도구, 승인, 파일, 샌드박스 내용, 상태는 넘어오지 않는다.
사흘에 여섯 번 릴리스가 나오는 베타 프레임워크에서 직접 운영한다면
업그레이드 시점이 곧 세션을 잃는 시점이다.
문서도 Vercel 밖에서는 `package.json`에 eve 버전을 정확히 고정하라고 권한다.

## 함정

### 기본값은 허용적이다

`approval`을 생략하면 `never()`와 같아서 도구가 사람 승인 없이 실행된다.
Responsible Use 문서는 별도로 설정하지 않으면 승인 없는 도구 실행과
전부 막지 않은 샌드박스 네트워크 출구 같은 허용적 설정으로 동작할 수 있다고
밝히고, 모델의 행동에만 기대어 되돌릴 수 없는 작업을 막지 말라고 한다.
반대로 라우트 인증은 닫힌 쪽이 기본이다.
스캐폴드의 `placeholderAuth()`는 프로덕션 브라우저 트래픽을 거부하므로,
배포했는데 401만 돌아온다면 이것을 실제 인증으로 바꾸지 않은 것이다.

### markdown 스케줄은 승인을 기다릴 수 없다

`markdown` 형식 스케줄은 채널이 없는 세션으로 돈다.
사람에게 묻거나 후속 메시지를 받을 수 없어서,
승인이 필요한 도구를 부르면 기다리지 않고 세션이 실패한다.
또 `eve dev`는 cron 주기로 스케줄을 실행하지 않으며,
Vercel에서는 cron 식을 UTC로 해석한다.
`"0 9 * * 1-5"`는 한국 시간 평일 오후 6시다.

### 직접 운영할 때 프록시 경로 하나를 빠뜨리기 쉽다

리버스 프록시는 `/eve/`와 `/.well-known/workflow/` 두 접두사를 모두,
경로를 바꾸지 않고 넘겨야 한다.
`/eve/`만 열어 두면 세션은 시작되지만 워크플로 콜백이 닿지 않아
실행이 멈춘다.
로컬 world를 쓴다면 `.eve/.workflow-data`를 영속 저장소에 마운트해야
컨테이너 교체 뒤에도 실행이 살아남는다.

### 발표 글의 코드는 이미 현재 API와 다르다

6월 발표 글은 승인 조건을 `needsApproval` 필드로,
스케줄 핸들러를 `receive(slack, ...)`로 보여 준다.
10월 현재 문서는 `approval` 필드와 `to` 인자를 쓴다.
베타 기간 동안 API가 바뀔 수 있다는 README 문구가 실제로 일어나고 있으므로,
블로그나 템플릿의 예제보다 설치한 버전의 `node_modules/eve/docs`를 기준으로
삼는 편이 안전하다.

### 서브에이전트는 부모의 능력을 물려받지 않는다

선언된 서브에이전트는 빈 컨텍스트와 자기에게 준 도구만으로 시작하며,
부모가 작성한 능력을 상속하지 않고 별도의 채널 엔드포인트도 없다.
선택적인 절차만 필요하다면 서브에이전트가 아니라 스킬이 맞다.

## 확인하기

아래는 문서가 제시하는 검증 순서이며, 직접 실행해 확인한 결과는 아니다.

```bash
# 배포 뒤 헬스 라우트 확인
curl https://your_agent.example.com/eve/v1/health

# 개발용 TUI를 배포본에 붙여 실제 턴 하나를 끝까지 돌린다
eve remote connect --url https://your_agent.example.com

# 인증 없는 프로덕션 요청이 401을 받는지 확인(세션 생성 경로는 발표 글 기준)
curl -i https://your_agent.example.com/eve/v1/session -X POST
```

에이전트 동작은 `evals/` 아래 평가 파일로 검증한다.
발표 글의 예는 질문 하나를 보내고 턴이 완료됐는지,
`run_sql` 도구를 불렀는지, 답에 `net of refunds`가 들어 있는지를 확인한다.
`eve eval`은 로컬이나 배포된 앱을 대상으로 돌릴 수 있어서,
프롬프트나 모델을 바꿨을 때 무엇이 깨졌는지 CI에서 먼저 볼 수 있다.

```ts
// evals/revenue.eval.ts
import { defineEval } from "eve/evals";
import { includes } from "eve/evals/expect";

export default defineEval({
  description: "The analyst answers revenue questions by the team's rules.",
  async test(t) {
    await t.send("What was revenue last week?");
    t.completed();
    t.calledTool("run_sql");
    t.check(t.reply, includes("net of refunds"));
  },
});
```

## 체크리스트

- [ ] 외부에 부작용을 남기는 모든 도구에 `approval`을 명시했는가
- [ ] 재실행될 수 있는 결제, 메일 발송 도구가 멱등한가
- [ ] `placeholderAuth()`를 실제 인증으로 바꾸고 401을 확인했는가
- [ ] 샌드박스 네트워크 정책을 `allow-all`보다 좁혔는가
- [ ] 비밀이 `process.env`에만 있고 샌드박스로 넘어가지 않는가
- [ ] 스케줄 cron 식을 UTC 기준으로 계산했는가
- [ ] Vercel 밖에서 운영한다면 eve 버전을 정확히 고정했는가
- [ ] 직접 운영 시 `/.well-known/workflow/`까지 프록시가 넘기는가

---

[^rishabhpoddar]: <https://news.ycombinator.com/item?id=48581099>
