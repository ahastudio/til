# Stagehand: 확장 프로그램 안에서 도는 에이전트용 브라우저 SDK

<https://github.com/browserbase/stagehand>

HN 토론: <https://news.ycombinator.com/item?id=49756671> (133점, 35개 댓글)

GN 토론: <https://news.hada.io/topic?id=33959>

## 소개

Browserbase가 만든 브라우저 자동화 SDK이며,
저장소 설명은 웹의 어떤 사이트에서든 데이터를 뽑고 상호작용하는 SDK라고 적는다.
README의 한 문장이 위치를 더 정확히 드러낸다.
Playwright는 테스트를 위해 만들어졌고 Stagehand는 에이전트를 위해 만들어졌다는 것이다.

TypeScript, Python, Go 세 언어를 지원하고 MIT 라이선스이며,
별 24,562개, 포크 1,698개, 미해결 이슈 396개를 기록하고 있다.
언어는 TypeScript다.

v4는 구조를 처음부터 다시 짠 판본이다.
HN에서 개발자 wittydeveloper가 밝힌 동기가 명확하다.
2년 전에 Stagehand를 만들었고 별 2만 4천 개와 월 400만 npm 내려받기를 기록하는 동안
가장 큰 결함이 왕복 지연이었다는 것이다.
모든 동작이 스크립트와 브라우저 사이를 왕복해야 했고, 로컬에서는 짧지만 클라우드에서는 길어졌다.
Playwright MCP의 과도한 토큰 소비에 대한 불만도 여러 번 봤다고 적는다.
그래서 v4에서는 브라우저 시작 시 자동으로 로드되는 확장 프로그램이 브라우저를 제어하며,
일괄 명령과 토큰 효율적인 `act()`, `extract()`를 갖추고
새 구조로 Playwright 대비 속도 2배, 토큰 사용량 80퍼센트 절감을 냈다고 밝힌다.[^wittydeveloper]

## 세 가지 원시 동작

```typescript
import { localBrowser, Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod/v4";

// 쿠키가 ./browser-data에 남으므로 다음 실행은 이미 로그인된 상태로 시작한다
const browser = await localBrowser.launch({ userDataDir: "./browser-data" });
const stagehand = await Stagehand.create({
  browser,
  model: { modelName: "openai/gpt-5.4-mini", apiKey: process.env.OPENAI_API_KEY },
});

const [page] = await browser.context.pages();
await page.goto("https://app.example.com/login");

// observe()는 실제 선택자를 돌려주므로 자격 증명이 모델에 닿지 않는다
const { data: email } = await stagehand.observe("find the email input");
const { data: password } = await stagehand.observe("find the password input");
await page.locator(email[0].selector).fill(process.env.APP_EMAIL!);
await page.locator(password[0].selector).fill(process.env.APP_PASSWORD!);

// act()는 사이트가 폼을 다시 디자인해도 스스로 복구한다
await stagehand.act("click the sign in button");
await stagehand.act("open the billing page");

// extract()는 스키마로 검증된 데이터를 돌려준다
const { data } = await stagehand.extract(
  "extract every invoice in the table",
  z.object({
    invoices: z.array(z.object({ number: z.string(), amount: z.number(), paid: z.boolean() })),
  }),
);
```

이 예제에서 가장 눈여겨볼 설계가 `observe()`다.
자연어로 요소를 찾되 모델이 돌려주는 것은 값이 아니라 선택자이고,
값을 채우는 일은 보통의 `locator`가 한다.
그래서 비밀번호 같은 값이 모델 컨텍스트에 들어가지 않는다.
자연어 인터페이스를 쓰면서도 민감한 값을 모델에서 떼어 놓는 방법이며,
주석이 그 의도를 명시하고 있다.

| 동작        | 역할                                                                |
| ----------- | ------------------------------------------------------------------- |
| `act()`     | 자연어 지시로 동작을 수행한다. 사이트가 바뀌면 수행 방식을 갱신한다 |
| `observe()` | 자연어로 요소를 찾아 실제 선택자를 돌려준다                         |
| `extract()` | 스키마를 주면 검증된 구조화 데이터를 돌려준다                       |

## 설치와 실행

```bash
pnpm add @browserbasehq/stagehand 'zod@~4.4.3'
pip install stagehand
go get github.com/browserbase/stagehand/packages/sdk-go/v4@v4.0.0
```

로컬 실행에는 Chrome이 설치되어 있어야 한다.

Browserbase에 같은 스크립트를 가리키면 Playwright 클라우드 대비 2배 빠른 실행을 얻는다고 적는다.
모델 게이트웨이를 설정하면 제공자를 직접 연결할 필요가 없고,
서버 측 캐싱을 켜면 동일한 호출이 캐시에서 돌아와 토큰을 쓰지 않는다.

```typescript
import { browserbase, Stagehand } from "@browserbasehq/stagehand";

const browser = await browserbase.launch({ apiKey: process.env.BROWSERBASE_API_KEY! });

// 모델 설정 없음: 게이트웨이가 동작마다 가장 싼 모델을 고른다
// cache: true: 동일한 호출은 Browserbase에서 돌아오고 토큰을 쓰지 않는다
const stagehand = await Stagehand.create({ browser, cache: true });
```

코딩 에이전트에 브라우저를 붙이는 경로도 따로 있다.
호스팅되는 Browserbase MCP 서버가 `navigate`, `act`, `observe`, `extract`를
아무 MCP 클라이언트에나 넣어 주며 설치도 로컬 브라우저도 필요 없다.

```bash
claude mcp add --transport http browserbase https://mcp.browserbase.com/mcp \
  --header "Authorization: Bearer $BROWSERBASE_API_KEY"
```

브라우저 없이 쓰는 보조 기능도 있다.
`Fetch`는 임의의 URL 내용을 마크다운으로 가져오고,
`Search`는 토큰 효율적인 웹 검색 결과를 준다.

## v4가 내세우는 것

| 항목            | 내용                                                                                  |
| --------------- | ------------------------------------------------------------------------------------- |
| 익숙한 API      | `goto`, `click`, `locator`, `screenshot` 같은 Playwright 스타일 메서드                |
| 토큰 효율       | 접근성 트리를 혼합 방식으로 다듬어 필요한 맥락만 준다                                 |
| 프로덕션 속도   | 브라우저 옆 확장 프로그램으로 돌아 동작마다의 왕복 지연을 줄인다                      |
| 자기 복구       | 사이트가 바뀌면 동작 수행 방식을 갱신한다                                             |
| 에이전트용 기능 | WebMCP, 클립보드, 일괄 명령, 중첩 iframe과 닫힌 Shadow DOM용 깊은 로케이터, OTel 추적 |
| 세 언어         | TypeScript, Python, Go에 걸친 하나의 브라우저 드라이버                                |

## 분석

### 확장 프로그램으로 옮긴 것이 v4의 전부다

v4의 성능 주장은 알고리즘 개선이 아니라 실행 위치의 변경에서 나온다.
이전에는 별도 런타임의 스크립트가 CDP로 브라우저를 조종했고,
이제는 브라우저 안의 확장 프로그램이 같은 CDP를 쓴다.

HN에서 cl685가 CDP 대비 무엇을 잃었느냐고 물었고,
교차 출처 iframe이나 확장을 로드할 수 없는 환경에서의 다운로드를 예로 들었다.[^cl685]
개발자의 답은 여전히 CDP를 쓰며 다만 별도 런타임이나 더 나쁘게는 다른 지역에서 도는 스크립트가 아니라
브라우저 안의 확장에서 통신한다는 것이었다.[^wittydeveloper-cdp]

이 답이 성능 주장의 범위를 정한다.
2배라는 수치는 프로토콜이 빨라져서가 아니라 네트워크 구간이 사라져서 나온 것이며,
로컬에서만 돌리는 사용자에게는 이득이 작다.
반대로 클라우드 브라우저를 쓰거나 지역이 갈리는 구성에서는 그 차이가 그대로 나타난다.

### agent()를 없앤 결정

v4는 이전의 `agent()`를 제거했다.
ishankunam이 왜 새 원시 동작들과 함께 남겨 두지 않았느냐고 물었고,[^ishankunam]
개발자는 생태계에 훌륭한 하네스가 워낙 많아서 없앴다고 답했다.
대신 Stagehand v4를 인기 있는 하네스들과 더 잘 통합되게 만들기로 했으며,
코딩 에이전트 수준에서는 Codex와 Claude Code,
프레임워크 수준에서는 Eve와 Deep Agents와 Mastra 등이 그 대상이라고 밝혔다.[^wittydeveloper-agent]

이 선택이 이 도구의 정체성을 정한다.
Stagehand는 에이전트가 되기를 포기하고 에이전트가 쓰는 드라이버가 되기로 했다.
README가 Playwright는 테스트용이고 Stagehand는 에이전트용이라고 적은 것과 같은 자리이며,
위로는 하네스에, 아래로는 브라우저에 붙는 중간 계층을 겨냥한다.

### 하네스가 평가 결과를 바꾼다는 주장

alyssamaru가 평가에서 하네스가 실제로 얼마나 중요하냐고 물었을 때 나온 답이 흥미롭다.
성능 면에서 특히 많이 중요하며 그래서 모델과 하네스를 함께 고려하는 자체 벤치마크를 만들었다는 것이다.
예로 Claude Opus 5에서 Deep Agents와 Eve와 Fx 중 무엇을 쓰느냐에 따라
정확도 차이가 최대 3퍼센트, 성능 차이가 최대 200밀리초까지 난다고 밝혔다.[^alyssamaru-reply]

모델 성능을 비교할 때 하네스를 상수로 두는 통상의 방식이
실제로는 상당한 변수를 고정하지 않은 채 두고 있다는 뜻이다.

## 비평

### 2배와 80퍼센트가 무엇에 대한 비교인지 좁게 정의되어야 한다

제목이 내세우는 두 숫자는 서로 다른 대상에 대한 것이다.
2배는 Playwright와의 실행 속도 비교이고,
80퍼센트는 토큰 사용량 비교인데 그 비교 대상은 Playwright가 아니라 Playwright MCP다.
Playwright 자체는 토큰을 쓰지 않는다.

개발자가 HN 첫 댓글에서 두 맥락을 모두 설명하므로 의도적인 호도는 아니다.
다만 저장소 제목과 GeekNews 제목은 두 수치를 한 줄에 붙여 놓았고,
그러면 같은 기준선에 대한 두 개선처럼 읽힌다.
실제로는 아키텍처 변경이 지연을 줄였고, 접근성 트리 다듬기가 토큰을 줄였다.
서로 다른 두 변경의 효과다.

### 캐시의 위치가 오픈소스와 상품 경계에 걸쳐 있다

ulrikrasmussen이 캐싱 아이디어가 마음에 든다면서 자기 복구 CI 테스트에 흥미롭다고 평한 뒤
정확한 질문 셋을 던졌다.
캐시된 `act()`가 실패해 다시 평가해야 하는 시점을 어떻게 판정하는가,
캐시가 클라우드에 저장된다면 같은 캐시에 대해 서로 다른 버전의 사이트가 도는 CI에서
캐시 이탈이 심해지지 않는가,
그리고 캐시가 스크립트와 함께 커밋되는 로컬 파일이면 안 되는 기술적 이유가 있는가다.
로컬 파일이라면 개발자가 실패한 테스트를 직접 고칠 수 있다는 점을 덧붙였다.[^ulrikrasmussen]

이 질문이 날카로운 이유는 경계선을 정확히 짚기 때문이다.
SDK는 MIT이고 로컬 브라우저에서 무료로 동작하지만,
서버 측 캐싱과 모델 게이트웨이와 2배 빠른 클라우드 실행은 Browserbase 쪽에 있다.
캐시를 로컬 파일로 두면 이 도구는 완결된 오픈소스가 되고,
클라우드에 두면 상품의 일부가 된다.
기술적 이유가 있을 수도 있으나 README에는 답이 없다.

### 자기 복구가 테스트 도구로 쓰일 때의 성격 변화

`act()`가 사이트 변경에 맞춰 스스로 복구한다는 성질은 자동화에는 장점이지만
테스트에는 양면적이다.
vishalanton이 1,000개짜리 Playwright 테스트 스위트를 가진 기업에게
CI 시간이 2배 빨라진다는 뜻이냐고 물었고 개발자가 그렇다고 답했으므로,[^vishalanton]
테스트 대체는 이 도구가 염두에 둔 용도다.

그런데 테스트의 목적은 사이트가 바뀌었을 때 실패하는 것이다.
버튼의 위치나 이름이 바뀌었는데 자기 복구가 그것을 찾아내 통과시키면,
그 변경이 의도된 것인지 회귀인지 판정할 기회가 사라진다.
자동화에서 이득인 성질이 테스트에서는 탐지 실패가 된다.
이 긴장은 저장소 문서에서 다뤄지지 않으며,
테스트 용도로 도입하는 팀이 먼저 정해야 할 정책이다.

### 봇 탐지 측면의 냉소

shashanoid는 아무리 빠르게 만들어도 Playwright는 Playwright이며 봇임을 드러내는 표시라고 적었다.[^shashanoid]
swingboy는 많은 사람이 Playwright를 UI 테스트에 쓴다고 답했다.[^swingboy]

이 짧은 교환이 이 도구의 두 용도가 서로 다른 제약을 받는다는 점을 드러낸다.
자기 사이트를 테스트하는 데는 탐지가 문제가 되지 않지만,
남의 사이트에서 데이터를 뽑는 데는 탐지가 핵심 제약이다.
README는 웹의 어떤 사이트에서든 데이터를 뽑는다고 적지만
탐지 회피에 대해서는 언급하지 않으며,
Browserbase 쪽의 검증 모드와 주거용 프록시가 그 자리를 채우는 상품이라는 점이 암시될 뿐이다.

## 인사이트

### 값이 아니라 선택자를 돌려주게 하면 민감한 데이터가 모델을 우회한다

`observe()`가 선택자를 돌려주고 값 채우기는 보통의 로케이터가 하는 구성은
자연어 인터페이스를 쓰는 도구 전반에 적용할 만한 패턴이다.

모델에게 무엇을 하라고 시키되 실제 데이터는 모델을 거치지 않게 만드는 방식이며,
비밀번호, 결제 정보, 개인정보를 다루는 자동화에서 특히 값어치가 있다.
모델이 다루는 것은 페이지의 구조이고 값은 코드가 다룬다.

같은 발상이 다른 곳에도 있다.
SQL을 생성하되 파라미터는 바인딩으로 넘기는 것,
파일 경로를 찾게 하되 내용은 읽지 않게 하는 것,
API 호출을 구성하되 자격 증명은 런타임이 주입하는 것이 그렇다.
공통점은 모델의 출력이 데이터가 아니라 데이터를 가리키는 참조라는 점이다.

### 성능 개선의 출처가 알고리즘인지 배치인지 구별해야 한다

v4의 2배는 코드가 똑똑해져서가 아니라 코드가 옮겨 가서 생긴 것이다.
이 구별이 중요한 이유는 이득이 환경에 따라 완전히 달라지기 때문이다.
네트워크 구간을 제거해 얻는 개선은 그 구간이 길었던 사용자에게만 나타난다.

그러므로 성능 수치를 볼 때 물어야 할 것은 얼마나 빨라졌는가가 아니라
무엇이 사라졌는가다.
사라진 것이 왕복이라면 내 구성에 그 왕복이 있는지를 먼저 확인해야 하고,
사라진 것이 연산이라면 대개 어디서나 이득이 된다.

### 도구가 에이전트이기를 포기하면 통합 대상이 늘어난다

`agent()`를 없애고 하네스들과의 통합에 집중하겠다는 결정은
에이전트 생태계에서 반복적으로 나타나는 층위 정리의 사례다.
모든 도구가 자기 에이전트 루프를 갖던 단계가 지나고,
루프는 하네스가 갖고 도구는 능력을 제공하는 구조로 정리되는 중이다.

이 정리가 도구 제작자에게 주는 이득은 분명하다.
루프를 유지보수하지 않아도 되고, 모델 변화에 따라가지 않아도 되며,
여러 하네스의 사용자를 동시에 얻는다.
대가는 차별화 지점이 좁아진다는 것이고,
그래서 Stagehand의 경쟁 축이 지연과 토큰 효율 같은 측정 가능한 수치로 이동한 것도 자연스럽다.

---

[^wittydeveloper]: <https://news.ycombinator.com/item?id=49756672>

[^cl685]: <https://news.ycombinator.com/item?id=49756952>

[^wittydeveloper-cdp]: <https://news.ycombinator.com/item?id=49756974>

[^ishankunam]: <https://news.ycombinator.com/item?id=49757863>

[^wittydeveloper-agent]: <https://news.ycombinator.com/item?id=49757944>

[^alyssamaru-reply]: <https://news.ycombinator.com/item?id=49757129>

[^ulrikrasmussen]: <https://news.ycombinator.com/item?id=49763632>

[^vishalanton]: <https://news.ycombinator.com/item?id=49757041>

[^shashanoid]: <https://news.ycombinator.com/item?id=49763499>

[^swingboy]: <https://news.ycombinator.com/item?id=49765108>
