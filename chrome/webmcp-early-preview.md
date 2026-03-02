# WebMCP: 브라우저가 AI 에이전트의 도구가 되다

- 출처: [WebMCP is available for early preview](https://developer.chrome.com/blog/webmcp-epp)
- 게시일: 2026년 2월 10일 · Chrome for Developers Blog

---

## 핵심 요약

WebMCP(Web Model Context Protocol)는 웹페이지가 자신의
기능을 구조화된 도구(Tool)로 AI 에이전트에게 선언할 수
있게 하는 새로운 브라우저 API다.

기존 에이전트는 스크린샷을 해석하거나 DOM을 파싱해서
웹사이트와 상호작용했다. WebMCP는 이 방식을 완전히
뒤집는다. **웹사이트가 직접 "나는 이런 일을 할 수 있다"고
에이전트에게 알려주는 것이다.** 항공권 예약, 지원 티켓
등록, 데이터 조회 등의 작업을 스키마로 정의하면 에이전트가
정확하고 빠르게 실행할 수 있다.

Google과 Microsoft 엔지니어가 공동 작성했고, W3C Web
Machine Learning Community Group에서 표준화를 진행 중이다.
Chrome 146 Canary에서 플래그 뒤에 얼리 프리뷰로 사용할
수 있다.

---

## 두 가지 API

### Declarative API: HTML 폼에 속성 추가

기존 HTML 폼에 `toolname`, `tooldescription` 속성을
추가하는 것만으로 에이전트가 사용할 수 있는 도구가 된다.

```html
<form id="login-form"
      toolname="login"
      tooldescription="이메일과 비밀번호로 로그인"
      toolautosubmit="true">
  <input type="email" name="email" />
  <input type="password" name="password" />
  <button type="submit">Log In</button>
</form>
```

브라우저가 폼 필드를 자동으로 JSON Schema로 변환한다.
에이전트가 도구를 호출하면 브라우저가 필드를 채우고
제출한다. `SubmitEvent.agentInvoked` 플래그로 에이전트
제출인지 구분할 수 있고, `respondWith()`로 결과를 에이전트에
반환한다.

**이미 잘 구조화된 HTML 폼이 있다면 80%는 완성된 셈이다.**

### Imperative API: JavaScript로 동적 도구 등록

`navigator.modelContext.registerTool()`로 런타임에
도구를 등록하고 해제할 수 있다.

```js
navigator.modelContext.registerTool({
  name: 'search_flights',
  description: '출발지, 목적지, 날짜로 항공편 검색',
  inputSchema: {
    type: 'object',
    properties: {
      origin: {
        type: 'string',
        description: '출발 공항 코드'
      },
      destination: {
        type: 'string',
        description: '도착 공항 코드'
      },
      date: {
        type: 'string',
        description: 'YYYY-MM-DD 형식 출발일'
      }
    },
    required: ['origin', 'destination', 'date']
  },
  async execute(args) {
    const results = await flightAPI.search(args);
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(results)
      }]
    };
  }
});
```

도구 이름, 자연어 설명, JSON Schema 입력 정의, 핸들러
함수로 구성된다. 복잡한 동적 인터랙션에 적합하다.
`provideContext()`로 페이지 상태 변화에 따라 도구 집합을
통째로 교체할 수도 있다.

---

## 보안 모델: Permission-First 설계

WebMCP의 보안은 **브라우저 중재(Browser Mediation)**가
핵심이다. 에이전트는 서버와 직접 통신할 수 없고, 반드시
브라우저를 통해야 한다.

두 가지 신뢰 경계(Trust Boundary):

1. **도구 등록 시점**: 웹사이트가 능력을 노출하는 순간.
   HTTPS 필수, Same-Origin Policy, CSP가 적용된다.
2. **도구 호출 시점**: 에이전트가 실제로 도구를 실행하는
   순간. 사용자 동의 프롬프트(User Consent Manager)를
   통해 "AI가 이 항공편을 예약하도록 허용할까요?" 같은
   확인을 거친다.

핵심 원칙:

- **Human-in-the-Loop**: `requestUserInteraction()`으로
  민감한 작업 전 사용자 확인을 요청할 수 있다.
- **세션 상속**: 에이전트는 사용자의 기존 브라우저 세션을
  그대로 사용한다. 별도의 OAuth 플로우가 필요 없다. 사용자가
  로그인한 상태에서 그 권한 범위 내에서만 동작한다.
- **페이지 생명주기 스코핑**: 도구는 페이지가 살아있는 동안만
  존재한다. 네비게이션하면 모든 도구가 해제된다.

---

## WebMCP vs Anthropic MCP

| 구분         | WebMCP               | Anthropic MCP       |
|--------------|----------------------|---------------------|
| 실행 환경    | 클라이언트(브라우저) | 서버(백엔드)        |
| 프로토콜     | 브라우저 네이티브 API | JSON-RPC            |
| 통신 방식    | postMessage          | HTTP/SSE/stdio      |
| 인증         | 브라우저 세션 상속   | OAuth 2.1           |
| 도구 범위    | 프론트엔드 JS       | 백엔드 서비스       |
| 사용자 관여  | Human-in-the-Loop    | 자동화 중심         |

**둘은 경쟁이 아닌 보완 관계다.** 여행사를 예로 들면:
백엔드 MCP 서버로 ChatGPT나 Claude 같은 AI 플랫폼에
API를 직접 연결하면서, 동시에 소비자 웹사이트에는
WebMCP 도구를 구현해 브라우저 기반 에이전트도 예약 흐름에
접근하게 할 수 있다.

이름에 "MCP"가 들어 있지만, JSON-RPC 스펙을 따르지
않는다. 개념적 계보와 API 표면(도구 + 스키마)은
공유하되, 아키텍처는 완전히 다르다.

---

## 현재 상태와 한계

- **Chrome 146 Canary**에서 `chrome://flags`의
  "WebMCP for testing" 플래그로 사용 가능
- Microsoft가 공동 저자이므로 Edge 지원 가능성 높음
- Firefox, Safari는 아직 구현 계획 미발표
- W3C Candidate Recommendation 목표: 2026년 3분기

알려진 한계:

- **도구 발견에 네비게이션 필요**: 어떤 사이트가 도구를
  제공하는지 방문하지 않으면 알 수 없다. 향후
  `.well-known/webmcp` 매니페스트가 논의 중이다.
- **클라이언트 사이드 전용**: 프론트엔드 JS에 한정된다.
  백엔드 직접 접근에는 Anthropic MCP가 적합하다.
- **단일 탭 스코프**: 도구는 페이지 생명주기에 묶인다.
  탭 간 도구 공유는 불가능하다.
- **미해결 보안 이슈**: 프롬프트 인젝션, 도구 체이닝을
  통한 데이터 유출, 파괴적 작업 방지 등이 완전히
  해결되지 않았다.

---

## 인사이트

### 1. 웹의 에이전트화: 반응형 디자인의 재림

모바일 시대에 반응형 디자인이 등장해 "모든 웹사이트는
모바일 친화적이어야 한다"가 상식이 됐던 것처럼,
**WebMCP는 "모든 웹사이트는 에이전트 친화적이어야 한다"는
새로운 상식을 만들려 한다.** 19억 개 웹사이트가 존재하는
현실 인터넷에서 에이전트가 작동하려면, API를 따로 만드는
게 아니라 기존 웹 자체가 도구가 되어야 한다.

### 2. 선언적 접근의 파괴력

Declarative API의 설계가 탁월하다. HTML 폼에 속성
세 개를 추가하는 것만으로 에이전트 도구가 되는 진입장벽은
극도로 낮다. 스크린샷 기반 대비 **89% 토큰 효율 개선**이라는
수치가 이를 뒷받침한다. 기존 웹사이트의 점진적 채택
(Progressive Enhancement)을 가능하게 하는 영리한 설계다.

### 3. 브라우저가 미들웨어가 된다

WebMCP에서 브라우저는 단순한 렌더러가 아니라 **에이전트와
웹사이트 사이의 신뢰된 중재자**다. 인증 세션을 상속시키고,
사용자 동의를 관리하고, 도구 생명주기를 제어한다.
브라우저의 역할이 "콘텐츠 표시"에서 "에이전트 런타임"으로
확장되는 것이다. 이것은 브라우저 벤더에게 새로운
전략적 위치를 부여한다.

### 4. Human-in-the-Loop은 제약이 아닌 설계 철학

완전 자율 에이전트가 아닌 **협력적 워크플로우**를 명시적으로
선택한 것이 눈에 띈다. "AI가 이 항공편을 예약할까요?"
같은 확인은 속도를 희생하는 것처럼 보이지만, 신뢰를
확보하는 유일한 방법이다. 자율 에이전트가 틀렸을 때의
비용(잘못된 결제, 의도치 않은 계약)을 생각하면,
사용자 확인은 제약이 아니라 **현실적 필수 조건**이다.

### 5. Google-Microsoft 공동 작성의 의미

두 최대 브라우저 벤더가 스펙을 공동 작성한다는 것은
사실상 **표준이 될 것**이라는 신호다. 역사적으로 두
벤더가 합의한 웹 표준은 대부분 살아남았다. Firefox와
Safari가 아직 참여하지 않았지만, W3C 프로세스에
들어간 이상 압력은 커질 수밖에 없다.

### 6. 도구 발견 문제가 진짜 병목이다

현재 가장 큰 구조적 한계는 **도구 발견에 페이지 방문이
필요하다**는 점이다. 에이전트가 "항공편을 예약해줘"라는
요청을 받았을 때, 어떤 사이트에 예약 도구가 있는지
알려면 일단 방문해야 한다. `.well-known/webmcp`
매니페스트가 구현되면 이 문제를 해결할 수 있겠지만,
그때까지는 검색 엔진이 도구 카탈로그 역할을 하게 될
가능성이 높다. **Google이 이 스펙을 주도하는 이유**가
여기에 있을 수 있다.

### 7. 프론트엔드 개발자의 역할 변화

WebMCP 시대에 프론트엔드 개발자는 **사람과 에이전트**
모두를 위한 인터페이스를 설계해야 한다. 폼의 `name`
속성, `description` 텍스트, 입력 스키마의 품질이
에이전트의 작업 정확도를 직접 좌우한다. "좋은 HTML을
작성하라"는 오래된 조언이 새로운 의미를 갖는다.
시맨틱 HTML을 잘 작성해온 개발자는 이미 유리한
위치에 있다.

### 8. MCP 생태계와의 수렴

Anthropic MCP(백엔드)와 WebMCP(프론트엔드)가 각각의
영역을 담당하면서, **"도구 + 스키마"라는 공통 인터페이스
패턴**이 AI 에이전트 상호작용의 사실상 표준으로
수렴하고 있다. 백엔드 서비스든 웹 UI든, 에이전트에게
자신의 능력을 구조화된 도구로 선언하는 방식이 보편화되고
있다. 이 패턴을 이해하고 있으면 어느 쪽이든 적용할 수
있다.

---

## 시작하기

1. Chrome 146 Canary 설치
2. `chrome://flags`에서 "WebMCP for testing" 활성화
3. 기존 HTML 폼에 `toolname` 속성 추가로 시작
4. 복잡한 워크플로우는 `navigator.modelContext`
   Imperative API 활용
5. `navigator.modelContext` 존재 여부를 반드시 체크
   (미지원 브라우저 대비)

```js
if ('modelContext' in navigator) {
  // WebMCP 지원 환경
  navigator.modelContext.registerTool({ /* ... */ });
}
```

크로스 브라우저 지원이 필요하면 MCP-B 폴리필 사용:

```html
<script src="https://unpkg.com/@mcp-b/global@latest/dist/index.iife.js"></script>
```

---

## 관련 링크

- [Chrome Developer Blog: WebMCP Early Preview](https://developer.chrome.com/blog/webmcp-epp)
- [WebMCP 공식 스펙](https://webmachinelearning.github.io/webmcp/)
- [WebMCP GitHub 저장소](https://github.com/webmachinelearning/webmcp)
- [WebMCP 예제 코드](https://github.com/WebMCP-org/examples)
