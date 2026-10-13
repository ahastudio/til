# Hono Web application framework

> Fast, lightweight, built on Web Standards. Support for any JavaScript runtime.

<https://hono.dev/>

<https://github.com/honojs/hono>

HN 토론: <https://news.ycombinator.com/item?id=40047212> (300점, 86개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=39313891> (181점, 54개 댓글)

GN 토론: <https://news.hada.io/topic?id=11685>

## 소개

Hono는 일본어로 불꽃(炎)을 뜻하는 이름의 웹 프레임워크로,
Web Standards API만으로 만들어져 어떤 JavaScript 런타임에서도 돈다는 것을
내세운다.
README가 꼽는 런타임은 Cloudflare Workers, Fastly Compute, Deno, Bun, Vercel,
AWS Lambda, Lambda@Edge, Node.js이고,
공식 문서는 여기에 WASI의 `wasi:http`를 통한 WebAssembly까지 더한다.
같은 코드가 모든 플랫폼에서 돈다는 것이 핵심 약속이다.

저장소는 2021년 12월에 만들어졌고,
2026년 10월 기준으로 스타 약 32,500개, 포크 약 1,400개다.
라이선스는 MIT이고 작성자는 Yusuke Wada다.
README는 RegExpRouter, SmartRouter, LinearRouter, PatternRouter를
Taku Amano가 만들었다고 따로 밝힌다.
npm의 최신 안정판은 4.13.13이고,
2026년 10월 8일과 10일에 v5.0.0 RC가 연달아 나왔다.

README의 특징 목록은 다섯 줄이다.

| 특징               | README의 설명                                                               |
| ------------------ | --------------------------------------------------------------------------- |
| Ultrafast          | `RegExpRouter`가 선형 루프를 쓰지 않아 빠르다                               |
| Lightweight        | `hono/tiny` 프리셋은 12kB 미만이고, 의존성이 없으며 Web Standard API만 쓴다 |
| Multi-runtime      | 같은 코드가 모든 플랫폼에서 돈다                                            |
| Batteries Included | 내장 미들웨어, 사용자 미들웨어, 서드파티 미들웨어를 모두 갖췄다             |
| Delightful DX      | 깔끔한 API와 일급 TypeScript 지원                                           |

공식 문서의 철학 페이지는 출발점을 솔직하게 적는다.
처음에는 Cloudflare Workers에서 웹 앱을 만들고 싶었는데 거기서 쓸 만한
프레임워크가 없어서 시작했고,
Trie 트리로 라우터를 만드는 법을 배워 보려던 차에 친구가 RegExpRouter를
들고 왔다는 것이다.
Web Standards만 쓴 덕분에 Deno와 Bun에서도 돌았고,
“Bun용 Express가 있느냐”는 질문에 “없지만 Hono가 있다”고 답할 수 있었다고
쓴다.

## 동작 방식

### 다섯 개의 라우터와 세 개의 프리셋

공식 문서는 라우터를 Hono의 가장 중요한 기능이라고 부른다.
라우터는 다섯 가지다.

| 라우터        | 방식                                                       | 쓰임                                        |
| ------------- | ---------------------------------------------------------- | ------------------------------------------- |
| RegExpRouter  | 모든 경로 패턴을 정규식 하나로 합쳐 한 번에 매칭한다       | 가장 빠르지만 모든 패턴을 지원하지는 않는다 |
| TrieRouter    | Trie 트리 알고리즘, 선형 루프 없음                         | 모든 패턴을 지원한다                        |
| SmartRouter   | 등록된 라우터 중 가장 빠른 것을 시작 시점에 골라 계속 쓴다 | 여러 라우터를 묶는다                        |
| LinearRouter  | 문자열을 컴파일하지 않고 선형으로 경로를 등록한다          | 요청마다 초기화되는 “일회성” 환경           |
| PatternRouter | 가장 작은 라우터                                           | 자원이 제한된 환경                          |

문서의 설명에 따르면 path-to-regexp를 쓰는 Express류 라우터는 이름과 달리
경로마다 정규식을 차례로 대 보는 선형 루프라서,
경로가 늘수록 느려진다.
RegExpRouter는 경로 전체를 “큰 정규식 하나”로 바꿔 한 번의 매칭으로 결과를
얻는데,
대부분의 경우 radix 트리 같은 트리 기반 알고리즘보다 빠르다고 한다.
대신 등록 단계가 조금 느려서,
요청마다 앱을 새로 초기화하는 환경에는 맞지 않는다.

프리셋은 이 라우터들의 조합에 이름을 붙인 것이다.
세 프리셋이 내보내는 `Hono` 클래스는 같고 라우터만 다르다.

| 프리셋       | 라우터                                | 문서가 권하는 환경                                                       |
| ------------ | ------------------------------------- | ------------------------------------------------------------------------ |
| `hono`       | SmartRouter(RegExpRouter, TrieRouter) | 대부분. Deno·Bun·Node.js 서버, 일정 시간 유지되는 V8 isolate(Workers 등) |
| `hono/quick` | SmartRouter(LinearRouter, TrieRouter) | 요청마다 앱이 초기화되는 환경                                            |
| `hono/tiny`  | PatternRouter                         | 자원이 제한된 환경                                                       |

Cloudflare Workers와 Deno Deploy도 `hono`가 적합하다고 문서가 말하는 이유는,
isolate가 부팅 후 한동안 유지되어 등록 비용이 여러 요청에 나뉘기 때문이다.
Fastly Compute는 경로 등록이 앱 빌드 단계에서 일어나므로 역시 `hono`를 권한다.

### Web Standards가 이식성을 만드는 방식

Hono가 런타임을 가리지 않는 이유는 요청과 응답을 `fetch`의 `Request`,
`Response`, `URL`, `Headers` 같은 표준 객체로만 다루기 때문이다.
Cloudflare Workers, Deno, Bun은 모두 `fetch` 핸들러를 내보내는 모듈을
서버로 인식하므로,
`export default app` 한 줄로 앱이 그대로 서버가 된다.
Node.js처럼 표준 서버 인터페이스가 다른 런타임에는 어댑터를 둔다.

### RPC: 서버 타입을 클라이언트가 그대로 쓴다

RPC 기능은 서버 앱의 타입을 `typeof`로 내보내고,
클라이언트가 `hono/client`의 `hc`에 그 타입을 제네릭으로 넘겨 쓰는 방식이다.
검증기(Zod 등)에서 입력 타입을, `c.json()`을 돌려주는 핸들러에서 출력 타입을
추론하므로 코드 생성 단계가 없다.
문서는 모노레포에서 이 기능이 제대로 동작하려면 서버와 클라이언트의
`tsconfig.json` 모두에 `"strict": true`가 필요하다고 경고한다.

## 사용법

### 시작하기

```bash
npm create hono@latest my-app
cd my-app
npm install
npm run dev
```

`create hono`는 대상 런타임을 묻고 그에 맞는 템플릿을 만든다.
다음은 Bun이나 Cloudflare Workers에서 그대로 도는 최소 앱이다.

```ts
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.text('Hono!'))

// 경로 파라미터는 c.req.param()으로 읽는다
app.get('/users/:id', (c) => c.json({ id: c.req.param('id') }))

// fetch 핸들러를 가진 객체를 내보내면 Workers·Bun·Deno가 서버로 쓴다
export default app
```

### RPC로 서버와 클라이언트 타입 맞추기

서버 쪽은 핸들러를 체이닝해서 하나의 값으로 만들어야 타입이 끝까지
추론된다.
다음 예시는 Zod 검증기 미들웨어(`@hono/zod-validator`)를 쓴다.

```ts
// server.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

// 체이닝한 결과를 변수에 담아야 클라이언트가 경로 타입을 받는다
const route = app.post(
  '/posts',
  zValidator('json', z.object({ title: z.string(), body: z.string() })),
  (c) => c.json({ ok: true, message: 'Created!' }, 201)
)

export type AppType = typeof route
export default app
```

```ts
// client.ts
import { hc } from 'hono/client'
import type { AppType } from './server'

const client = hc<AppType>('http://localhost:8787/')

const res = await client.posts.$post({
  json: { title: 'Hello', body: 'Hono' },
})
if (res.status === 201) {
  const data = await res.json() // { ok: boolean; message: string }
  console.log(data.message)
}
```

### 경로가 많아지면 타입을 미리 계산해 둔다

문서는 RPC의 알려진 문제로 IDE 성능을 든다.
경로 하나마다 큰 타입 인스턴스화가 일어나고,
IDE의 `tsserver`가 앱을 쓸 때마다 이를 다시 계산하기 때문에 경로가 많을수록
느려진다.
문서가 권하는 첫 번째 해법은 `tsc`로 미리 컴파일해 타입을 고정하는 것이다.

```ts
// client-typed.ts: tsc로 빌드한 뒤 hc 대신 hcWithType을 쓴다
import { app } from './app'
import { hc } from 'hono/client'

// 컴파일 시점에 클라이언트 타입을 한 번만 계산해 둔다
const client = hc<typeof app>('')
export type Client = typeof client

export const hcWithType = (...args: Parameters<typeof hc>): Client =>
  hc<typeof app>(...args)
```

그 밖에 서버와 클라이언트의 Hono 버전을 반드시 맞출 것,
분리된 저장소라면 TypeScript 프로젝트 참조를 쓸 것,
앱을 여러 하위 앱으로 나누고 하위 앱마다 클라이언트를 따로 만들 것을
권한다.
또 핸들러가 `.then()` 체인을 바로 돌려주면 응답 타입이 `unknown`이 되므로
`async`/`await`로 쓰라고 한다.

## 분석

### 라우터의 속도는 요청 처리 비용이 아니라 콜드 스타트 비용의 문제다

Hono의 다섯 라우터와 세 프리셋은 결국 하나의 트레이드오프를 다룬다.
등록을 느리게 하고 매칭을 빠르게 할 것인가,
등록을 빠르게 하고 매칭을 조금 느리게 할 것인가다.
RegExpRouter는 앞쪽, LinearRouter는 뒤쪽을 고른다.
이 선택이 의미를 갖는 것은 서버리스와 엣지에서 앱의 수명이 짧기 때문이다.

오래 도는 서버에서는 등록 비용이 한 번만 들고 모든 요청이 빠른 매칭의 이득을
본다.
요청마다 앱이 초기화되는 환경에서는 등록 비용이 매번 다시 든다.
문서가 LinearRouter 벤치마크에 굳이 “등록 단계를 포함한” 결과를 붙인 것도
그래서다.
Hono의 라우터 설계는 “가장 빠른 라우터”보다 “실행 환경의 수명에 맞는 라우터”를
고르게 하는 장치로 읽는 편이 정확하다.

### 런타임 중립성은 프레임워크가 아니라 표준이 준 것이다

Hono가 어디서나 도는 이유는 Hono가 특별해서가 아니라,
Workers·Deno·Bun이 모두 `fetch` 핸들러라는 같은 인터페이스를 택했기 때문이다.
공식 문서도 WinterCG의 웹 상호 운용성 논의를 따라가겠다고 쓴다.
Hono는 그 공통 인터페이스 위에 라우팅과 미들웨어라는 얇은 층을 얹었다.

HN에서 iansinnott은 런타임 중립성을 고른 이유로,
Bun을 써 보고 싶지만 문제가 생기면 Node로 돌아갈 수 있도록 Bun 전용 API에
묶이고 싶지 않았다고 했다.[^iansinnott]
rafter는 같은 코드로 브라우저 메인 스레드와 서비스 워커,
Cloudflare Worker에서 라우팅과 템플릿을 처리한다고 답했다.[^rafter]
반면 MrAlex94는 정적 파일 제공처럼 플랫폼마다 다른 부분이 있어서
“한 번 쓰면 어디서나”는 아니지만,
플랫폼을 옮겨야 할 때 드는 노력은 크게 줄어든다고 봤다.[^MrAlex94]
이식성은 핵심 경로에서는 실제이고, 가장자리에서는 여전히 어댑터의 몫이다.

### 경쟁 상대는 Express가 아니라 생 `fetch` 핸들러다

HN의 axhl은 Cloudflare Worker에서 Hono가 그냥 Worker로는 할 수 없는 무엇을
가능하게 하느냐고 물었다.[^axhl]
yawnxyz는 모든 것을 더 낫게 만드는 추상화일 뿐,
직접 만들 수 없는 새로운 것은 없다고 답했다.[^yawnxyz]
이 대답이 Hono의 위치를 정확히 짚는다.
Hono가 대체하는 것은 Express보다 Worker 안에 직접 쓰는 `if`/`switch` 라우팅이다.

그래서 Hono의 가치는 성능보다 개발 경험에서 나온다.
soulchild77은 `@hono/zod-openapi`와 Scalar API 문서 미들웨어,
RPC를 엮으면 엔드포인트를 한 번 정의해 검증, OpenAPI 명세, 문서 브라우저,
프런트엔드 타입까지 코드 생성 없이 얻는다고 했다.[^soulchild77]
dejaydev는 앱 대부분이 Workers에 있어서 속도는 중요하지 않고,
개발 경험이 비할 데 없어서 쓴다고 했다.[^dejaydev]

## 비평

### 벤치마크는 실제 병목이 아닌 곳을 잰다

README의 첫 특징은 “Ultrafast”이고 공식 문서에는 벤치마크 페이지가 따로 있다.
그런데 그 숫자가 실제 앱의 성능을 얼마나 바꾸는지는 문서가 다루지 않는다.
HN의 bastawhiz는 두 가지 이유로 그 벤치마크가 아무것도 말해 주지 않는다고
반박했다.
서버리스에서는 요청이 동시에 별도 호출로 처리되어 프레임워크 오버헤드가 쌓이지
않고,
가장 느린 프레임워크도 초당 20만 요청을 넘으니 프레임워크 비용은 요청당
수 마이크로초의 반올림 오차라는 것이다.[^bastawhiz]
JodieBenitez는 요청-라우터-응답 경로가 병목이었던 적이 정확히 0번이라고
했다.[^JodieBenitez]

게다가 공식 벤치마크 페이지의 Deno 결과는 Hono 3.0.0과 Deno 1.22를 쓴 측정이다.
지금 안정판이 4.13이고 5.0 RC가 나온 시점에 이 숫자를 첫인상으로 쓰는 것은
낡은 비교다.
DB 왕복이 수십 밀리초 걸리는 앱에서 라우터의 마이크로초는 의사결정 변수가
아니다.
속도는 Hono를 고르는 이유가 되기 어렵고,
문서가 그 점을 정직하게 말하지 않는다.

### 엣지 실행은 데이터가 멀면 오히려 느려진다

Hono의 정체성은 “엣지용 프레임워크”지만,
문서는 데이터가 어디 있는지에 대해 거의 말하지 않는다.
GN에서 heycalmdown은 프레임워크는 엣지에서 돌아도 데이터베이스는 리전에 있으니
접속 지역마다 지연이 크게 달라질 것 같다고 물었다.[^heycalmdown]
pitzcarraldo는 Workers + Hono + Supabase 서울 리전 조합으로 DB에 바로
접속해 봤는데,
통신사에 따라 Worker가 LA나 홍콩, 싱가포르에서 떠서 연결이 매우 느렸다고
답했다.
데이터 쪽 가까이 띄워 주는 Smart Placement 옵션도 요청량이 적어서인지 잘
동작하지 않았다고 한다.[^pitzcarraldo]

이 경험은 HN의 axelthegerman이 던진 질문과 같은 지점을 가리킨다.
엣지가 매번 업스트림으로 요청을 넘겨야 한다면 얻는 것이 제한적이라는
것이다.[^axelthegerman]
Hono는 이 문제를 풀지 않는다.
풀 수 있는 곳은 플랫폼 쪽이고,
GN 스레드에서도 caniel이 이런 경우에 Hyperdrive가 유용할 것이라고
답했다.[^caniel]
Hono 문서가 “엣지”를 장점으로 내세울 때 그 전제는 따로 확인해야 한다.

### 기능이 커질수록 “작고 단순하다”는 정체성과 부딪힌다

v4.0 HN 스레드의 첫 반응들은 축하가 아니라 우려였다.
arminluschin은 Cloudflare 함수용 간단한 라우터로만 써 왔는데 이번 방향이
프레임워크를 비대하게 만들지 걱정했고,[^arminluschin]
evnix는 SSR과 React식 훅이 백엔드 코드에 들어오는 게 싫어서 다른 라우터로
옮기겠다고 했다.[^evnix]
pdyc와 lioeters도 API 표면이 너무 커져
더는 작지도 단순하지도 않다고 했다.[^pdyc][^lioeters]

반대 증언도 있다.
drewbitt은 코어가 비대해지지 않았고 백엔드 부분은 그대로 쓸 수 있다고
짚었다.[^drewbitt]
실제로 `hono/tiny` 프리셋과 미들웨어 분리 구조는 코어를 작게 유지한다.
하지만 Kennnan의 지적은 그대로 남는다.
GraphQL이나 RPC 같은 미들웨어도 문서와 완성도가 부족했는데,
풀스택 SSR로 범위를 넓히면 현재 팀이 감당하기 어렵다는 것이다.[^Kennnan]
lf-non은 GraphQL 미들웨어에 컨텍스트를 넘길 방법이 없어서 Yoga로 돌아갔다고
했다.[^lf-non]
“Batteries Included”가 넓어질수록 배터리 하나하나의 품질이 문제가 된다.

### 미들웨어 생태계는 같은 이름 아래 다른 통합 수준을 섞는다

HN의 franciscop은 `@hono/zod-openapi`가 `OpenAPIHono`라는 별도 클래스를
쓰게 해서,
기본 Hono를 확장하는 대신 나란히 존재하는 구조라고 지적했다.[^franciscop]
soulchild77은 실제로 전역 에러 핸들러를 OpenAPI 경로에 재사용할 방법이 없어
이슈를 열었더니 우회책이 정답이라는 답을 들었다고 했다.[^soulchild77-openapi]
README가 “내장, 사용자, 서드파티 미들웨어”를 하나의 특징으로 묶지만,
그 안의 통합 수준은 균일하지 않다.

보안에서도 그 차이는 드러났다.
2022년 10월 병합된 PR #608은 bearer-auth와 basic-auth 미들웨어가
인증에 실패해도 핸들러를 실행하던 문제를 고쳤다.
제목 그대로 “인증되지 않았을 때 핸들러가 실행되면 안 된다”는 수정이었고,
PR 본문은 이전 버전을 모두 회수하자고 제안했다.
내장 미들웨어라는 이름이 품질 보증을 뜻하지는 않는다는 사례다.

## 인사이트

### RPC의 타입 비용은 서버 코드의 구조를 정한다

Hono의 RPC는 코드 생성 없이 타입을 공유한다는 점에서 매력적이지만,
그 비용은 컴파일러가 낸다.
경로마다 생기는 타입 인스턴스화가 IDE를 느리게 만들고,
문서가 내놓는 해법은 모두 코드 구조를 바꾸라는 것이다.
핸들러를 체이닝하고, 앱을 하위 앱으로 나누고, 클라이언트를 하위 앱마다 만들고,
타입을 미리 컴파일해 두라고 한다.

이는 2차 효과를 낳는다.
라우트를 어떻게 나눌지가 도메인 경계가 아니라 타입 검사기의 한계로
정해진다.
HN의 eddd-ddde가 Elysia에서 비슷한 이유로 WebStorm의 TypeScript 언어 서버가
망가졌다고 한 것도 같은 현상이다.[^eddd-ddde]
“엔드 투 엔드 타입 안전”을 내세우는 TypeScript 프레임워크는 모두 언젠가
이 벽에 닿는다.

sqwxl은 클라이언트가 같은 저장소에 없으면 RPC를 쓸 수 없어서 OpenAPI 명세로
클라이언트를 생성할 계획이라고 했고,[^sqwxl]
soulchild77은 그런 경우 Orval로 타입이 붙은 TanStack Query 클라이언트를
만들어 좋은 경험을 했다고 답했다.[^soulchild77-orval]
결국 코드 생성을 없애려던 RPC는 저장소 경계에서 다시 코드 생성으로 돌아온다.
타입 공유는 모노레포라는 조직 구조를 전제한 기능이다.

### Hono의 성공은 프레임워크가 아니라 표준의 성공이다

Hono가 2021년에 Cloudflare Workers용 작은 라우터로 시작해 스타 3만 개를
넘긴 과정은,
`fetch` 핸들러가 서버 측 JavaScript의 공통 인터페이스가 되어 간 과정과
겹친다.
Express가 Node의 `http` 모듈 위에서 생태계를 독점했듯,
Hono는 `Request`/`Response` 위에서 그 자리를 노린다.
문서 스스로 “웹 표준의 표준”이 되고 싶다고 쓴다.

이 구조는 역사적으로 익숙하다.
Rack이 Ruby 웹 서버와 프레임워크 사이의 공통 인터페이스가 되자 Sinatra 같은
얇은 프레임워크가 번성했고,
WSGI가 Python에서 Flask를 가능하게 했다.
공통 인터페이스가 생기면 그 위의 얇은 층은 이식성을 공짜로 얻는다.
HN의 dreadnip이 Hono를 Silex나 Lumen 같은 PHP 마이크로 프레임워크에 비유한
것도 같은 계보다.[^dreadnip]

그렇다면 Hono의 장기적 경쟁력은 라우터 속도가 아니라 미들웨어 생태계와
문서에서 결정된다.
같은 표준 위에서는 누구든 비슷하게 빠른 라우터를 만들 수 있고,
실제로 itty-router, h3, Elysia 같은 대안이
HN 댓글마다 등장했다.[^eddd-ddde-itty][^cosbgn]
표준이 이식성을 평준화하면, 차이는 표준 바깥에서 난다.

### 요청 취소 같은 표준의 빈틈이 AI 시대의 비용이 된다

HN의 orph는 Hono가 요청 취소를 아직 잘 지원하지 않아서,
LLM 토큰을 스트리밍하다가 클라이언트가 요청을 취소하면 돈을 낭비하게 된다고
지적했다.[^orph]
2024년의 이 지적은 지금 더 무거워졌다.
엣지 함수가 LLM API를 감싸는 얇은 프록시로 쓰이는 일이 흔해졌기 때문이다.

요청 취소는 `AbortSignal`이라는 표준 수단이 있지만,
런타임마다 클라이언트 연결이 끊어졌을 때 그 신호를 언제, 어떻게 전달하는지가
다르다.
Hono가 표준만 쓴다는 원칙은 여기서 약점이 된다.
표준이 런타임 사이의 차이를 덮지 못하는 곳에서는,
프레임워크가 그 차이를 메우거나 사용자에게 넘길 수밖에 없다.
5.0처럼 메이저 버전이 바뀌는 시점에 이런 운영상의 빈틈이 어떻게 다뤄지는지가,
속도 벤치마크보다 실무 선택에 더 큰 영향을 줄 것이다.

---

[^iansinnott]: <https://news.ycombinator.com/item?id=40047938>

[^rafter]: <https://news.ycombinator.com/item?id=40048978>

[^MrAlex94]: <https://news.ycombinator.com/item?id=39315747>

[^axhl]: <https://news.ycombinator.com/item?id=40048791>

[^yawnxyz]: <https://news.ycombinator.com/item?id=40048799>

[^soulchild77]: <https://news.ycombinator.com/item?id=40050244>

[^dejaydev]: <https://news.ycombinator.com/item?id=40080120>

[^bastawhiz]: <https://news.ycombinator.com/item?id=40059762>

[^JodieBenitez]: <https://news.ycombinator.com/item?id=40055026>

[^heycalmdown]: <https://news.hada.io/topic?id=11685#cid20375>

[^pitzcarraldo]: <https://news.hada.io/topic?id=11685#cid20393>

[^axelthegerman]: <https://news.ycombinator.com/item?id=40049869>

[^arminluschin]: <https://news.ycombinator.com/item?id=39314110>

[^evnix]: <https://news.ycombinator.com/item?id=39314697>

[^pdyc]: <https://news.ycombinator.com/item?id=39316398>

[^lioeters]: <https://news.ycombinator.com/item?id=39323835>

[^drewbitt]: <https://news.ycombinator.com/item?id=39318715>

[^Kennnan]: <https://news.ycombinator.com/item?id=39314545>

[^lf-non]: <https://news.ycombinator.com/item?id=39314720>

[^franciscop]: <https://news.ycombinator.com/item?id=40051401>

[^soulchild77-openapi]: <https://news.ycombinator.com/item?id=40052703>

[^eddd-ddde]: <https://news.ycombinator.com/item?id=40079705>

[^sqwxl]: <https://news.ycombinator.com/item?id=40056524>

[^soulchild77-orval]: <https://news.ycombinator.com/item?id=40061009>

[^dreadnip]: <https://news.ycombinator.com/item?id=40049765>

[^eddd-ddde-itty]: <https://news.ycombinator.com/item?id=39314216>

[^cosbgn]: <https://news.ycombinator.com/item?id=39314152>

[^orph]: <https://news.ycombinator.com/item?id=40051121>

[^caniel]: <https://news.hada.io/topic?id=11685#cid37949>
