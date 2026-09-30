# MCP-B: 웹사이트가 AI 에이전트에게 도구를 직접 내주는 WebMCP 도구 모음

<https://mcp-b.ai/>

<https://github.com/WebMCP-org/npm-packages>

HN 토론: <https://news.ycombinator.com/item?id=44515403> (336점, 184개 댓글)

GN 토론: <https://news.hada.io/topic?id=21915>

## 소개

MCP-B는 스스로를 WebMCP 회사(The WebMCP Company)라고 소개한다.
홈페이지 첫 문장은 사람과 에이전트가 WebMCP를 쓰도록 돕는 AI 컨설팅과 제품이다.
MCP-B가 WebMCP 명세에 영감을 주었고, 이제 개발자가 에이전트 친화적인(agent-native) 웹 앱을, 회사가 웹 친화적인(web-native) 에이전트를, 사용자가 에이전트로 웹을 탐색하는 일을 모두 WebMCP로 돕는다는 것이다.

WebMCP는 웹 애플리케이션이 구조화된 행동을 AI 에이전트용 도구로 공개하게 하는 Community Group 제안이다.
MCP-B 문서는 WebMCP가 `document.modelContext`로 웹사이트 도구를 공개하는 Draft Community Group Report이며 W3C 표준이 아니라고 먼저 밝힌다.
사이트가 행동과 입력을 정의하고, 에이전트는 스크린샷이나 DOM 구조나 클릭 순서로 동작을 추측하는 대신 그 계약을 쓴다.

MCP-B가 이 제안에서 맡는 부분은 제안 주변의 패키지다.
폴리필, React 바인딩, 전송 계층(transport), iframe 브리지, 로컬 릴레이를 만들고, 브리지로 페이지 도구를 MCP 클라이언트에 연결할 수 있지만 실행 환경은 여전히 브라우저 문서다.
문서는 MCP-B가 WebMCP 제안을 정의하지 않는다고 분명히 한다.
홈페이지에는 이 밖에 컨설팅 예약, 사이트 에이전트(SiteAgent), Chrome 확장 프로그램 Rook, 그리고 9월 3일에 제출이 마감된 OpenAI WebMCP Challenge 해커톤 안내가 함께 올라 있다.
패키지 저장소는 MIT 라이선스이고, 2026년 9월 28일에도 커밋이 올라왔다.

### 프로토콜에서 도구 회사로

이 사이트가 처음 Hacker News에 올라온 2025년 7월에는 제목이 AI 브라우저 자동화를 위한 프로토콜 MCP-B였다.
작성자 miguelspizza(Alex Nahas)는 Amazon에서 사내 MCP 서버를 만들다 떠올린 아이디어를 오픈소스로 공개한다며, 웹사이트를 MCP-B 호환 웹 확장 프로그램이 발견하고 호출할 수 있는 MCP 서버로 다루게 하는 MCP의 확장이라고 설명했다.[^miguelspizza]
당시의 구조는 웹사이트 안에 MCP 서버를 두고, 확장 프로그램이 주입하거나 사이트 JavaScript에 포함된 클라이언트가 탭 전송 계층으로 연결하는 방식이었다.

1년 남짓 지난 지금 그 아이디어는 브라우저 제안이 되었다.
Chrome은 2026년 2월 WebMCP를 조기 프리뷰로 내놓았고(`chrome/webmcp-early-preview.md`), MCP-B 문서는 OpenAI의 site tools 문서가 Codex와 ChatGPT Work의 내장 브라우저에서 WebMCP를 지원한다고 안내한다.
MCP-B의 자리는 프로토콜의 주인에서 제안을 둘러싼 도구와 컨설팅을 제공하는 회사로 바뀌었다.

## 동작 방식

### 사이트가 도구를 등록하고 에이전트가 부른다

문서의 흐름은 다섯 단계다.
웹 애플리케이션이 브라우저의 WebMCP 맥락에 구조화된 도구를 등록하고, 에이전트가 그 맥락에서 도구를 찾아 호출하며, 맥락이 등록된 핸들러를 실행하고, 사이트가 구조화된 결과를 돌려주면, 맥락이 그 결과를 에이전트에게 넘긴다.

브라우저가 이 도구의 자리로 알맞은 이유를 문서는 페이지가 이미 가진 것에서 찾는다.
페이지에는 애플리케이션의 상태, 권한 검사, 눈에 보이는 인터페이스가 있으므로, 도구는 브라우저에만 있는 로직을 별도 서비스로 옮기지 않고 그 맥락을 다시 쓸 수 있다.
입력 검증, 권한 집행, 결과가 중대할 때 확인을 구하는 일은 여전히 애플리케이션의 몫이다.

작성자는 2025년 HN에서 Playwright나 Selenium과의 차이를 이렇게 설명했다.[^miguelspizza-playwright]
그것들은 브라우저 자동화 프레임워크이고 Playwright MCP 서버는 에이전트가 Playwright로 브라우저를 자동화하게 하지만, MCP-B는 웹사이트 소유자가 웹사이트 안에 MCP 서버를 만들고 에이전트는 화면을 해석하는 대신 그 도구를 부른다는 것이다.

### 세 겹의 계층

MCP-B 문서는 관계를 세 겹으로 그린다.

| 계층           | 소유자          | 담는 것                                 |
| -------------- | --------------- | --------------------------------------- |
| WebMCP 제안    | Community Group | 진화하는 `document.modelContext` API    |
| 이식 가능 계층 | MCP-B 패키지    | 타입, 헬퍼, 폴리필                      |
| 확장 계층      | MCP-B 패키지    | `BrowserMcpServer`, MCP 기능, 전송 계층 |

확장 계층의 `BrowserMcpServer`는 `listTools()`, 프롬프트와 리소스 등록, 공식 MCP 서버의 합성을 더한다.
전송 계층, iframe 라우팅, 로컬 릴레이가 그 서버를 명시적인 MCP 클라이언트에 연결한다.
문서는 이것들이 MCP-B의 통합 문제를 푸는 기능일 뿐 브라우저 API 메서드가 아니며, 이 경계를 좁게 두어야 라이브러리가 MCP 서버나 전송 계층에 의존하지 않고 네이티브 구현이나 폴리필로 도구를 공개할 수 있다고 설명한다.

### 런타임 고르기

문서는 순서대로 묻는다.

1. 대상 브라우저가 필요한 WebMCP 동작을 제공하는가. 그렇다면 런타임 패키지가 필요 없을 수 있다.
2. 현재 제안의 타입만 필요한가. Community Group의 `webmcp-types`를 쓴다.
3. MCP-B 호환 타입이나 스키마 추론이 필요한가. `@mcp-b/webmcp-types`를 쓴다.
4. 네이티브 지원이 없는 곳에서 도구 등록과 발견이 필요한가. `@mcp-b/webmcp-polyfill`을 쓴다.
5. MCP 브리지 전송, `listTools`, 프롬프트, 리소스, MCP 서버 직접 접근이 필요한가. `@mcp-b/global`을 쓴다.
6. React 도구 등록만 필요한가. `usewebmcp`를 쓴다.
7. React 프롬프트, 리소스, MCP 클라이언트·공급자 훅이 필요한가. `@mcp-b/react-webmcp`를 쓴다.

| 선택                     | 브라우저 런타임 추가 | 고르는 경우                                         |
| ------------------------ | -------------------- | --------------------------------------------------- |
| 네이티브 브라우저 지원   | 아니오               | 구현이 문서화한 브라우저 동작                       |
| `webmcp-types`           | 아니오               | 현재 제안을 따르는 전역 선언                        |
| `@mcp-b/webmcp-types`    | 아니오               | MCP-B 계약과 스키마 추론                            |
| `@mcp-b/webmcp-polyfill` | 예                   | 도구 등록과 발견 호환성                             |
| `@mcp-b/global`          | 예                   | MCP-B 확장, 서버 접근, 브라우저 전송                |
| `usewebmcp`              | 아니오               | 초기화된 `document.modelContext` 위의 React 도구 훅 |
| `@mcp-b/react-webmcp`    | 아니오               | React 도구, 프롬프트, 리소스, MCP 클라이언트 훅     |

## 구현하기

### 첫 도구 하나 등록하기

문서의 첫 튜토리얼은 빌드 단계 없이 HTML 파일 하나로 도구를 등록한다.
`file:` 출처는 도구 실행이 거부되므로 `localhost`에서 서빙해야 한다.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>My First WebMCP Tool</title>
    <!-- 네이티브 지원이 없는 브라우저를 위해 도구 전용 폴리필을 올린다.
         운영에서는 @latest 대신 특정 버전을 고정한다. -->
    <script src="https://unpkg.com/@mcp-b/webmcp-polyfill@latest/dist/index.iife.js"></script>
  </head>
  <body>
    <h1>My First WebMCP Tool</h1>
    <p id="status">Loading...</p>

    <script>
      void document.modelContext
        .registerTool({
          name: 'get-page-title',
          description: 'Get the current page title',
          // 입력이 없는 도구도 스키마는 명시한다. 에이전트는 이 계약만 보고 호출한다.
          inputSchema: { type: 'object', properties: {} },
          async execute() {
            return {
              content: [{ type: 'text', text: document.title }],
            };
          },
        })
        .then(() => {
          document.getElementById('status').textContent = 'Tool "get-page-title" registered.';
        })
        .catch((error) => {
          document.getElementById('status').textContent = `Registration failed: ${error.message}`;
        });
    </script>
  </body>
</html>
```

```bash
# index.html이 있는 디렉터리에서
python3 -m http.server 8000
```

`http://localhost:8000`을 열어 상태 줄이 등록 완료로 바뀌는지 본다.

### 콘솔에서 확인하기

```javascript
const modelContext = document.modelContext;
const tools = await modelContext.getTools();
console.log(tools);

const tool = tools.find((candidate) => candidate.name === 'get-page-title');
if (!tool) throw new Error('get-page-title is not registered');

// MCP-B 런타임은 직렬화된 JSON을 받는 executeTool()을 노출한다.
// 현재 제안은 객체 입력을 쓰므로, 메서드 존재와 시그니처를 먼저 확인한다.
const executeTool = modelContext.executeTool;
if (typeof executeTool !== 'function') {
  throw new Error('This runtime does not expose a compatible executeTool method');
}

const result = await executeTool.call(modelContext, tool, '{}');
console.log(result === null ? null : JSON.parse(result));
```

결과는 도구 응답을 담은 `content` 배열이다.
데스크톱 에이전트가 이 도구를 쓰려면 로컬 릴레이 같은 브리지가 따로 필요하다.

## 트레이드오프

### 사이트 소유자가 비용을 내고 에이전트가 이익을 본다

MCP-B의 전제는 사이트가 도구를 먼저 정의해야 에이전트가 쓸 수 있다는 것이다.
이것은 에이전트가 화면을 해석하며 추측하는 방식보다 정확하고 싸다.
하지만 그 정확성의 비용은 도구를 만들고 유지하는 사이트 소유자가 낸다.

muratsu는 2025년 HN에서 이 점을 곧바로 짚었다.[^muratsu]
웹사이트 소유자에게 부담을 지우는 구조이고, MCP 서버를 만들고 유지하는 일을 자동화해 줘야 훨씬 가치가 있을 것이라는 것이다.
작성자는 AI 도구로 기존 웹사이트의 MCP 서버를 꽤 자신 있게 만들 수 있고, React Hook Form 같은 폼 생태계는 MCP 도구로 바로 옮길 수 있다며, 에이전트가 웹사이트를 직접 조작하는 것보다 일이 더 많다는 점은 인정했다.[^miguelspizza-burden]

jacquesm은 이것이 RSS와 같은 길을 갈 것이라고 예측했다.[^jacquesm]
회사들은 사용자가 자기 데이터를 어떻게 쓰는지 통제하는 것을 좋아하지 않는다는 이유였다.
GeekNews에서 shindalsoo도 사용자는 브라우저 정보에 접근하는 확장 프로그램을 본능적으로 꺼리고, 웹 개발자는 기존 API 외에 도구를 따로 정의하고 관리해야 하는 부담을 지므로 확대될 여지가 없어 보인다고 평가했다.[^shindalsoo]

그 뒤 Chrome이 제안을 조기 프리뷰로 내고 OpenAI가 내장 브라우저에서 지원하면서 수요 쪽 조건은 달라졌다.
그래도 공급 쪽 비용, 즉 누가 도구를 만들고 계속 맞춰 두느냐는 여전히 사이트 소유자에게 있다.
MCP-B가 프로토콜에서 컨설팅과 도구를 파는 회사로 옮겨 간 것은 바로 그 비용을 줄여 주는 쪽이 사업이 된다는 판단으로 읽을 수 있다.

### 구조화된 도구와 화면 해석은 서로를 대체하지 못한다

_1tem은 AI 에이전트의 요점이 API가 없는 웹사이트에서도 그냥 동작해야 한다는 데 있고, 많은 웹사이트는 좋은 API를 제공할 유인도 자원도 없다고 적었다.[^_1tem]
xnx도 AI 자동화가 흥미로운 이유는 사이트의 협조가 필요 없기 때문이라고 했다.[^xnx]

두 방향은 각자 잃는 것이 있다.
도구 방식은 사이트가 허락한 행동만 할 수 있으므로, 사이트가 공개하지 않은 일은 할 수 없다.
화면 해석 방식은 무엇이든 시도할 수 있지만, UI가 바뀌면 깨지고, 봇 탐지와 싸우고, 매 단계 모델이 추측하는 비용을 낸다.

현실적인 결론은 둘이 공존하는 것이다.
에이전트는 도구가 있으면 도구를 쓰고, 없으면 화면으로 내려간다.
Claude Cowork가 커넥터를 먼저 쓰고 필요할 때 브라우저로, 최후의 수단으로 화면으로 내려간다고 설명하는 것도 같은 순서다.
사이트 소유자에게 WebMCP 도구는 에이전트가 자기 사이트에서 화면 해석으로 내려가지 않게 하는 방법이다.

### 사용자 권한을 그대로 넘기는 것은 편하지만 넓다

도구는 페이지의 인증된 세션 안에서 돌기 때문에 별도 인증이 필요 없다.
작성자는 모델이 사용자보다 더 많은 접근 권한을 갖지 않으며, 제대로 된 보안 구현은 여전히 사이트 소유자의 몫이라고 답했다.[^miguelspizza-auth]
tehryanx는 요점은 에이전트에게 사용자와 같은 권한을 주면 안 된다는 것이라고 반박했다.[^tehryanx]
에이전트는 클라이언트 안의 신뢰할 수 없는 사용자로 다뤄져야 하고, 주어진 작업에 필요한 접근만으로 좁혀진 권한을 받아야 한다는 것이다.

이 반박은 도구 설계의 기준이 된다.
사용자가 할 수 있는 모든 일을 도구로 공개하는 것이 아니라, 에이전트가 해도 되는 일만 공개하고, 되돌리기 어려운 일에는 사람 확인을 붙인다.
MCP-B 문서가 결과가 중대할 때 확인을 구하는 것을 애플리케이션의 책임으로 적은 것도 같은 뜻이다.

## 함정

### 제안과 패키지는 다른 속도로 바뀐다

WebMCP 제안, 브라우저 구현, MCP-B 패키지는 각자의 일정으로 바뀐다.
MCP-B 런타임의 `executeTool()`은 직렬화된 JSON을 받지만, 현재 제안은 객체 입력을 쓴다고 문서가 스스로 적는다.
MCP-B 타입에서 어떤 메서드를 봤다고 그것이 제안에 있다고 추론하지 말라는 경고도 있다.
패키지 문서의 예제를 그대로 옮기기 전에, 대상 브라우저의 네이티브 구현과 시그니처를 확인해야 한다.

### 에이전트가 쓰는 브라우저마다 지원이 다르다

튜토리얼은 Chrome, Edge, Firefox, Safari에서 폴리필로 도구를 등록할 수 있다고 한다.
그러나 도구를 등록하는 것과 에이전트가 그 도구를 발견하는 것은 다르다.
브라우저 안에서 도구를 소비하는 에이전트가 있어야 하고, 데스크톱 에이전트는 로컬 릴레이 같은 브리지가 있어야 한다.
사이트에 도구를 넣어도, 사용자가 쓰는 에이전트가 그 브라우저에서 WebMCP를 읽지 않으면 아무 일도 일어나지 않는다.

### 사이트는 에이전트를 알아볼 수 있다

imcritic은 사이트가 확장 프로그램이 주입한 스크립트를 탐지해, 사람만 쓰게 하고 싶은 소유자가 서비스를 거부할 수 있지 않느냐고 물었다.[^imcritic]
WebMCP에서는 반대로 사이트가 도구를 공개하는 쪽이므로 이 문제가 기능이 된다.
사이트는 어떤 행동을 에이전트에게 열지 스스로 정하고, 공개하지 않은 행동은 도구로 부를 수 없다.
다만 같은 에이전트가 화면 해석으로 내려가면 그 경계는 다시 사라진다.

### 도구가 많아지면 모델이 헷갈린다

slt2021은 OpenAPI 명세를 공개하고 범용 Swagger MCP 클라이언트를 쓰면 되지 않느냐고 물었다.[^slt2021]
작성자는 MCP가 나왔을 때 모두 그렇게 생각했지만, 대개 도구가 너무 많아 잘 작동하지 않는다고 답했다.[^miguelspizza-tools]
WebMCP 도구도 마찬가지다.
사이트의 모든 API를 도구로 옮기면 에이전트는 비슷한 이름의 도구 사이에서 헤맨다.
사용자 작업 단위로 적은 수의 도구를 설계하는 편이 낫다.

## 확인하기

1. 위 HTML을 `localhost`에서 열고 상태 줄이 등록 완료로 바뀌는지 본다.
2. 콘솔에서 `getTools()`가 도구를 돌려주는지 확인한다.
3. `executeTool`의 존재와 입력 형식을 확인하고 도구를 호출한다.
4. 같은 페이지를 `file:`로 열어 도구 실행이 거부되는지 본다.
5. 실제로 쓸 에이전트(브라우저 내장 에이전트나 로컬 릴레이를 거친 데스크톱 에이전트)에서 도구가 보이는지 확인한다.

## 체크리스트

- 대상 브라우저가 네이티브 WebMCP를 지원하는지 먼저 확인했는가?
- 폴리필과 패키지 버전을 `@latest`가 아닌 특정 버전으로 고정했는가?
- 공개한 도구가 사용자 작업 단위로 적은 수로 설계되어 있는가?
- 각 도구의 핸들러가 입력을 검증하고, 서버 쪽 권한 검사를 거치는가?
- 되돌리기 어려운 행동을 하는 도구에 사람 확인이 붙어 있는가?
- 에이전트에게 사용자가 할 수 있는 모든 일이 아니라 필요한 일만 열었는가?
- 제안의 시그니처와 MCP-B 런타임의 시그니처 차이를 코드에서 처리했는가?

## 기억할 원칙

### 에이전트를 위한 인터페이스는 사람을 위한 인터페이스와 같은 곳에 둔다

WebMCP의 설계에서 가장 오래 남을 선택은 도구를 브라우저 문서 안에 둔 것이다.
페이지는 이미 상태, 인증, 권한 검사, 눈에 보이는 화면을 가진다.
에이전트용 도구를 별도 서버에 두면 이것들을 다시 만들어야 하고, 둘은 곧 어긋난다.

같은 곳에 두면 사람이 보는 것과 에이전트가 하는 것이 같은 코드 경로를 지난다.
사람이 버튼을 누르는 것과 에이전트가 도구를 부르는 것이 같은 검증과 같은 권한 검사를 거친다.
그 경로를 하나로 유지하는 것이 에이전트를 받아들이는 사이트가 할 수 있는 가장 싼 안전장치다.

### 에이전트는 사용자가 아니라 사용자가 보낸 손님이다

인증된 세션 안에서 도는 도구는 사용자의 모든 권한을 물려받기 쉽다.
하지만 에이전트는 사용자가 아니라, 사용자가 특정 일을 맡겨 보낸 손님이다.
도구를 설계할 때는 사용자가 할 수 있는 일이 아니라 이 손님에게 맡겨도 되는 일을 기준으로 삼아야 한다.

---

[^miguelspizza]: <https://news.ycombinator.com/item?id=44515404>

[^miguelspizza-playwright]: <https://news.ycombinator.com/item?id=44515766>

[^muratsu]: <https://news.ycombinator.com/item?id=44516047>

[^miguelspizza-burden]: <https://news.ycombinator.com/item?id=44516169>

[^jacquesm]: <https://news.ycombinator.com/item?id=44518514>

[^shindalsoo]: <https://news.hada.io/topic?id=21915#cid41283>

[^_1tem]: <https://news.ycombinator.com/item?id=44519812>

[^xnx]: <https://news.ycombinator.com/item?id=44530646>

[^miguelspizza-auth]: <https://news.ycombinator.com/item?id=44517901>

[^tehryanx]: <https://news.ycombinator.com/item?id=44520053>

[^imcritic]: <https://news.ycombinator.com/item?id=44516014>

[^slt2021]: <https://news.ycombinator.com/item?id=44516620>

[^miguelspizza-tools]: <https://news.ycombinator.com/item?id=44516805>
