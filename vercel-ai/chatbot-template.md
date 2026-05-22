# Vercel Chatbot Template

<https://github.com/vercel/chatbot>

<https://chatbot.ai-sdk.dev/demo>

<https://chatbot.ai-sdk.dev/docs>

## 소개

Vercel이 공개한 오픈소스 챗봇 템플릿(Chatbot Template)이다. 과거 “AI Chatbot”이라는 이름으로
알려져 있었으나 현재는 단순히 “Chatbot”으로 리브랜딩되었다. Next.js App Router와
Vercel AI SDK를 기반으로 하며, 프로덕션 수준의 챗봇 애플리케이션을 빠르게 구축할 수 있도록
설계된 풀스택 스타터 프로젝트다.

주요 기술 스택은 다음과 같다.

- **Next.js 16** App Router, React Server Components(RSC), Server Actions
- **AI SDK 6** (`ai` 패키지) — 텍스트 생성, 구조화 객체, 도구 호출(tool call)을 위한 통합 API
- **Vercel AI Gateway** — 단일 엔드포인트로 여러 LLM 제공사를 라우팅
- **shadcn/ui + Tailwind CSS + Radix UI** — 접근성 중심의 UI 컴포넌트
- **Neon Serverless Postgres + Drizzle ORM** — 채팅 이력 및 사용자 데이터 저장
- **Vercel Blob** — 파일 저장
- **Auth.js(next-auth v5 beta)** — 인증

## 주요 기능

### Artifacts 패널

대화 옆에 콘텐츠를 나란히 표시하는 사이드 패널이다. `code`(스크립트), `text`(문서),
`sheet`(스프레드시트), `image` 네 가지 아티팩트 종류를 지원한다. 아티팩트는 스트리밍으로
실시간 변경이 반영된다.

도구(tool) 기반으로 동작하며, `createDocument`, `editDocument`, `updateDocument`,
`requestSuggestions` 네 가지 도구가 아티팩트 생명주기를 관리한다. `editDocument`는
`old_string`/`new_string` 방식의 find-and-replace로 부분 수정을 지원하고,
`updateDocument`는 전체 재작성에만 사용한다.

### Vercel AI Gateway 통합

`providers.ts`의 `getLanguageModel()` 함수는 `gateway.languageModel(modelId)` 하나로
모든 모델을 처리한다. `models.ts`에는 DeepSeek V3.2, Kimi K2.5, GPT OSS 20B/120B,
Grok 4.1 Fast 등이 정의되어 있으며, 각 모델마다 `gatewayOrder`(라우팅 우선순위 백엔드 목록)와
`reasoningEffort`를 설정할 수 있다. Vercel 배포 환경에서는 OIDC 토큰으로 자동 인증되고,
그 외 환경에서는 `AI_GATEWAY_API_KEY` 환경 변수가 필요하다.

### 모델 능력(Capabilities) 동적 조회

`getCapabilities()` 함수는 AI Gateway의 `/v1/models/:id/endpoints` 엔드포인트를 호출해
각 모델이 `tools`, `vision`, `reasoning`을 지원하는지를 런타임에 확인한다. 결과는
`next: { revalidate: 86_400 }`으로 하루 단위로 캐싱된다.

### 엔타이틀먼트(Entitlements)

`entitlements.ts`에서 사용자 유형별(`guest`/`regular`) 시간당 최대 메시지 수를 관리한다.
현재는 두 유형 모두 시간당 10개로 동일하게 설정되어 있다.

## 분석

프로젝트의 핵심 설계 철학은 “AI SDK를 통한 추상화 계층 최소화”다. LLM 공급사를 교체해도
`getLanguageModel()` 한 줄만 바꾸면 되도록 설계되어 있으며, AI Gateway가 실제 백엔드
라우팅 로직을 모두 흡수한다.

아티팩트 시스템은 `documentHandlersByArtifactKind` 레지스트리 패턴으로 구현되어 있다.
새로운 아티팩트 종류를 추가하려면 `artifacts/` 디렉토리에 핸들러를 추가하고 레지스트리에
등록하는 것으로 충분하다. 이는 OCP(Open/Closed Principle)를 잘 따른 구조다.

프롬프트 엔지니어링도 체계적으로 관리된다. `prompts.ts`에 `regularPrompt`,
`artifactsPrompt`, `codePrompt`, `sheetPrompt`, `updateDocumentPrompt`,
`titlePrompt`가 분리되어 있다. 특히 `artifactsPrompt`는 “한 응답에 도구를 하나만
호출할 것”, “아티팩트 생성 직후 내용을 채팅에 반복하지 말 것” 같은 행동 제약을 명시적으로
포함하고 있어, LLM의 과도한 출력을 억제하는 역할을 한다.

스트리밍 데이터 전달에는 `UIMessageStreamWriter`를 활용하며, `data-kind`, `data-id`,
`data-title`, `data-clear`, `data-finish` 등의 타입 키를 통해 클라이언트 사이드에
아티팩트 상태를 실시간으로 전달한다.

## 비평

몇 가지 설계 결정에 의문이 든다.

첫째, `entitlements.ts`에서 `guest`와 `regular` 사용자 모두 시간당 10개로 동일한
제한을 두고 있다. 실질적으로 엔타이틀먼트 시스템이 유의미하게 동작하지 않는 상태로, 프로덕션
배포를 위해서는 반드시 커스터마이징이 필요한 미완성 영역이다.

둘째, Auth.js `next-auth@5.0.0-beta.25`를 의존성으로 사용한다. 베타 버전을 프로덕션
스타터 템플릿의 핵심 인증 라이브러리로 채택하는 것은 안정성 위험을 수반한다. v5 정식
릴리스 전까지는 API 변경 가능성이 상존한다.

셋째, 기본 모델이 OpenAI나 Anthropic이 아닌 `moonshotai/kimi-k2.5`로 설정되어 있다.
이는 Vercel이 특정 파트너 모델을 기본값으로 노출하는 전략적 결정으로 보이며, 커뮤니티
입장에서는 다소 낯선 선택이다.

넷째, `image` 아티팩트 종류가 존재하지만 `create-document.ts`의 프롬프트에는 포함되어
있지 않다. 내부 구현과 공개 인터페이스 사이의 불일치가 있다.

## 인사이트

### AI SDK의 `gateway` 추상화가 만드는 새로운 경쟁 구도

Vercel AI SDK v6의 `gateway` 객체는 단순한 편의 기능이 아니다. 이것은 LLM 공급사와
애플리케이션 개발자 사이에 Vercel이 중개자(broker)로 자리 잡겠다는 선언이다. 과거에는
개발자가 OpenAI SDK, Anthropic SDK를 직접 통합하며 공급사에 종속되었다. 이제 Vercel
AI Gateway를 경유하면 공급사 교체는 `models.ts`의 `id` 문자열 수정 한 줄로 끝난다.

이 구조에서 LLM 공급사들은 품질과 가격으로만 경쟁해야 한다. 개발자가 특정 SDK에 익숙해져
생기는 전환 비용이 사라지기 때문이다. 동시에 Vercel은 모든 트래픽을 자신의 게이트웨이로
집중시키면서 사용 데이터와 라우팅 통제권을 갖는다. `gatewayOrder` 배열이 그 증거다.
개발자가 `[“fireworks”, “bedrock”]`이라고 적으면, 실제 어느 인프라를 쓸지는 Vercel이
결정한다.

장기적으로 이 패턴은 클라우드 인프라 시장에서 AWS/GCP/Azure가 한 것과 동일하다. 편의성을
제공하는 대가로 트래픽 집중과 가격 결정권을 획득하는 방식이다. 개발자 생태계에서 이 접근은
매우 효과적이며, Vercel의 오픈소스 템플릿 전략은 그 확산 수단이다.

### Artifacts 패널이 제시하는 “대화형 문서 편집기” 패러다임

Artifacts 시스템은 채팅 인터페이스와 문서 편집기의 경계를 지우는 실험이다. 기존 챗봇은
대화 결과물이 채팅 버블 안에 갇혀 있었다. 코드를 생성해도, 글을 써줘도, 사용자는
복사-붙여넣기를 해야만 실제 작업에 활용할 수 있었다.

Artifacts는 대화와 결과물을 분리해 나란히 표시한다. 더 중요한 것은 `editDocument`의
find-and-replace 접근법이다. 전통적인 문서 편집기는 사용자가 직접 커서를 위치시켜야 한다.
여기서는 “3번째 함수의 변수명을 바꿔줘”라는 자연어 요청이 곧 편집 명령이 된다. LLM이
`old_string`을 찾아 `new_string`으로 교체하는 방식은, 사람이 텍스트를 다루는 방식과
LLM의 텍스트 이해 방식을 자연스럽게 연결한다.

이 패러다임은 Cursor나 GitHub Copilot의 코드 편집 경험을 일반 문서와 스프레드시트로
확장한 것이기도 하다. 앞으로 워드 프로세서나 스프레드시트 도구들이 이와 유사한 “채팅 패널
+ 문서 패널” 구조를 채택할 가능성이 높다. Vercel Chatbot Template은 그 참조 구현으로서
역할을 하고 있다.

### 프롬프트 엔지니어링의 코드화(Codification)와 유지보수 문제

`prompts.ts`의 구조는 프롬프트를 코드 아티팩트로 취급하는 성숙한 관점을 보여준다. 역할별
프롬프트(`regularPrompt`, `artifactsPrompt`, `codePrompt`)를 별도 상수로 분리하고,
`systemPrompt()` 함수로 런타임 조합한다. 이는 프롬프트가 단순한 문자열이 아니라 유지보수
가능한 소프트웨어 컴포넌트임을 인정하는 것이다.

특히 주목할 점은 `artifactsPrompt` 안의 행동 제약(behavioral constraints)이다. “한
응답에 도구를 하나만 호출할 것”, “아티팩트 생성 후 내용을 채팅에 반복하지 말 것”이라는
규칙들은 LLM의 기본 성향(다음 토큰 예측)과 사용자 경험이 요구하는 행동 사이의 간극을
메우기 위한 것이다. 이런 제약이 없으면 LLM은 아티팩트를 만든 뒤 그 내용을 채팅 버블에도
출력하는 중복 행동을 하게 된다.

이 접근법은 동시에 유지보수 부채를 만들기도 한다. 모델이 업그레이드되면 이 제약들이
여전히 필요한지, 혹은 새로운 제약이 필요한지를 지속적으로 재검토해야 한다. 프롬프트는
모델 버전에 종속된 소프트웨어이기 때문이다. “프롬프트 테스트”와 “프롬프트 버저닝”이 점점
중요한 엔지니어링 과제가 될 것이라는 점을 이 프로젝트 구조가 잘 보여준다.

### Next.js App Router와 AI 스트리밍의 결합이 주는 아키텍처 교훈

이 프로젝트는 Next.js 16 App Router의 React Server Components(RSC)와 AI 스트리밍을
함께 활용한다. Server Actions가 LLM API 호출을 담당하고, `UIMessageStreamWriter`를
통해 스트리밍 데이터를 클라이언트로 흘려보낸다. 이 패턴은 API 라우트 없이도 서버-클라이언트
스트리밍을 구현할 수 있음을 보여준다.

`instrumentation.ts`와 `instrumentation-client.ts`의 분리, OpenTelemetry 통합은
AI 애플리케이션에서 관측 가능성(observability)이 얼마나 중요한지를 보여준다. LLM 호출은
비결정적이고 비용이 크기 때문에, 어떤 요청이 얼마나 걸렸고 어느 모델로 라우팅되었는지를
추적하는 것이 운영 필수 요소다.

`resumable-stream` 패키지를 의존성으로 포함하고 있다는 점도 흥미롭다. 네트워크 단절 시
스트리밍을 재개하는 이 기능은, AI 응답이 수십 초씩 걸리는 상황에서 사용자 경험을 크게
향상시킨다. 전통적인 REST API 패러다임에서는 불필요했던 이 문제가, 스트리밍 AI 응답 시대에
새로운 프론트엔드 과제로 부상하고 있음을 알 수 있다.
