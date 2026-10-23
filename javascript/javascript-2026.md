# 2026년의 JavaScript: 6년의 공백을 건너 Temporal과 TypeScript 7, 그리고 AI가 바꾼 표준

원문: [2026년과 이후 JavaScript의 동향 - JavaScript(ECMAScript)](https://d2.naver.com/helloworld/2675915)

GN 토론: <https://news.hada.io/topic?id=35745>

## 요약

네이버 D2의 박재성이 2026년 10월 20일에 올린 글이다.
2016년부터 이어 오다 2020년을 마지막으로 쉬었던 “JavaScript의 동향” 연재를 6년 만에 되살린 첫 편이며, 이번 연재는 ECMAScript, 브라우저 밖의 JavaScript, WebAssembly, 라이브러리와 프레임워크의 네 편으로 구성된다.
글은 2026년 10월을 기준으로 쓰였다.

글은 2020년 글의 예상을 점검하는 것으로 시작한다.
2020년 글은 세 번째 주기의 JavaScript에서 CommonJS와 AMD가 ESM으로 전환되고, 도구가 JavaScript로 쓰일 필요가 없어지며, TypeScript와 JavaScript가 서로 영향을 주며 발전하리라고 예상했다.
6년 뒤 세 가지 모두 예상한 방향으로 갔지만 속도와 모습이 달랐다고 한다.
ESM 전환은 예상보다 느렸다.
ESM을 제공하는 인기 npm 패키지의 비율은 2021년 8월 7.8%에서 2024년 11월 25.9%, 2026년 6월 38.0%로 늘었지만, 2025년 12월부터 집계 대상의 출처가 바뀌어 이전 수치와 바로 비교하기는 어렵다.
도구의 언어 전환은 예상보다 빨랐다.
TypeScript 컴파일러가 Go로 옮겨져 2026년 7월 TypeScript 7.0이 나왔다.
2020년 글에 한 줄도 없던 AI가 이번에는 가장 큰 변수로 등장한다.

2020년 글에서 소개한 제안들의 결말도 표로 정리한다.
Top-level await와 클래스 필드 관련 제안은 ES2022가 되었다.
Pipeline Operator는 Hack 스타일로 Stage 2에 올랐지만 진척이 거의 없다.
Records & Tuples는 2025년 4월 철회되어 Composites로 이어졌고, Composites는 2026년 9월 Stage 2에 올랐다.
Temporal은 2026년 3월 Stage 4에 올라 ES2027에 포함될 예정이다.
TC39의 가장 큰 변화는 2023년 11월 합의한 Stage 2.7의 신설이다.
Stage 3으로 가기 전에 테스트를 쓰고 경험을 쌓는 구간을 따로 둔 것으로, Decorators와 Decorator Metadata는 2026년 5월 이 단계로 되돌아갔다.

ECMAScript 2026은 2026년 6월 30일 Ecma 총회에서 승인됐고 일곱 가지 기능을 담는다.
`Array.fromAsync`, `Error.isError`, `Math.sumPrecise`, `Uint8Array`의 base64와 hex 변환, `Iterator.concat`, `JSON.parse`의 원본 텍스트 접근(`JSON.rawJSON`), `Map`의 upsert(`getOrInsert`)다.
ES2027에는 Temporal, Explicit Resource Management(`using`), `Atomics.pause`, Joint Iteration(`Iterator.zip`), Iterator Chunking, Includes, Join이 들어갈 예정이다.

글의 후반은 엔진과 TypeScript, AI를 다룬다.
Chrome 69.28%, Safari 15.92%, Edge 5.39%, Firefox 2.98%라는 2026년 8월 점유율에서 Chromium 계열이 80% 가까이라는 점과, Ladybird가 엔진을 처음부터 새로 만든다는 점을 짚는다.
JavaScript 상표는 Deno가 Oracle을 상대로 낸 취소 심판이 합의 협상 때문에 중지된 상태라고 전한다.
TypeScript는 State of JS 2025 응답자가 TypeScript에 쓰는 시간 비중이 평균 77%였고, 컴파일러를 Go로 옮긴 7.0이 전체 빌드를 보통 8~12배 빠르게 했다.
AI 절에서는 GitHub Octoverse 2025가 TypeScript를 1위로 올린 배경에 AI가 있다고 보았다고 전하고, 학습 데이터의 시차 문제, Ladybird의 LibJS 이식, TC39의 AI 정책, 외부 PR을 받지 않기로 한 Ladybird의 결정을 정리한다.

## 분석

### 글의 구조: 6년 전 예측을 채점하는 방식

글은 새로운 동향을 나열하기 전에 2020년 글의 예상을 먼저 채점한다.
예상 세 가지(ESM, 도구의 비JavaScript화, TypeScript와의 공진화)가 맞았다고 하되 속도의 차이를 구체적인 수치로 보여 준다.
이 구조는 글의 신뢰를 높인다.
틀린 부분을 인정하는 글이 이후의 전망도 믿을 만하게 보이게 하기 때문이다.
다만 채점 기준은 저자가 정한 것이다.
세 예상이 방향상 맞았다는 판단은 예상이 느슨하게 쓰였기 때문에 성립한다.

### 표준의 속도: 기능이 쓰이고 나서 명세가 따라온다

글이 반복해서 보여 주는 사실은 명세 연도가 기능을 쓸 수 있게 된 시점보다 늦다는 점이다.
`Array.fromAsync`는 2024년 1월 Chrome 121에 이미 출시됐는데, 명세 PR이 2025년 12월에야 병합되어 ES2025가 아닌 ES2026에 들어갔다.
Stage 4는 두 개 이상의 엔진이 출시한 경험을 요구하므로, 명세 연도는 사용 가능 시점을 뒤따른다.
Temporal도 Stage 4를 요청할 때 Firefox는 약 1년 전부터, V8 기반 브라우저는 몇 달 전부터 플래그 없이 출시한 상태였다.

이 관찰은 독자의 판단 기준을 바꾼다.
기능을 쓸지는 ES 연도가 아니라 대상 환경의 지원 표(글의 표 4와 표 5)가 정한다.
GeekNews에서 wozo1004는 Temporal이 Stage 4까지 온 것이 가장 반갑고, DST 경계에서 하루씩 어긋나는 버그를 겪어 `ZonedDateTime`이 들어오면 `date-fns-tz` 같은 의존을 줄일 수 있겠다고 하면서, 폴리필 없이 프로덕션에서 쓸 수 있는 수준인지 물었다.[^wozo1004]
글의 표 5가 이 질문에 답한다.
Firefox 139, Chrome과 Edge 144, Node.js 26(기본 활성), Deno 2.7에서 지원하고 Safari는 Technology Preview 단계다.
Safari 지원이 필요한 제품이라면 폴리필이 아직 필요하다는 뜻이다.

### Stage 2.7은 합의가 아니라 검증의 단계를 만든 것이다

Stage 2.7은 명세가 원칙적으로 승인되었지만 테스트와 검증이 끝나지 않은 상태를 표시한다.
이전에는 명세가 완성되면 바로 Stage 3에 올랐고, Test262 테스트는 Stage 4 전까지만 갖추면 됐다.
그래서 Stage 3의 구현을 시작해도 된다는 신호와 실제 테스트 준비 상태 사이에 차이가 생겼다.
Decorators가 Stage 3에 오른 뒤 TypeScript 5.0이 구현을 내놓았지만 브라우저 엔진은 출시하지 못했고, 2026년 5월 Stage 2.7로 돌아간 일이 이 차이의 사례다.
Explicit Resource Management는 조건부 Stage 4를 받고도 남은 Test262 리뷰가 늦어져 조건이 충족되기까지 1년이 걸렸다.
글은 이 지연의 원인을 Test262 리뷰어 부족으로 요약한다.
표준화의 병목이 설계가 아니라 검증 인력에 있다는 서술이다.

### AI는 검증이 쉬운 일에서 먼저 효과를 냈다

글이 AI 절에서 반복하는 구조는 결과를 판정할 기준이 분명할 때 AI의 효과가 크다는 것이다.
Ladybird는 약 2만 5천 줄의 LibJS 코드를 2주 만에 Rust로 옮겼고, Test262 테스트 52,898개와 자체 회귀 테스트 12,461개에서 회귀가 없었다고 한다.
Bun도 Zig 코드 53만 줄을 Rust로 옮겼다.
글은 새 기능을 설계하거나 명세를 해석하는 일에 같은 방식이 통할지는 사례가 부족하다고 선을 긋는다.
이 구분은 글에서 가장 신중한 대목이다.

## 비평

### 글의 AI 인과는 인용된 보고서에 기댄다

글은 TypeScript가 GitHub 1위가 된 배경으로 AI를 꼽는다.
이는 Octoverse 보고서가 그렇게 설명했다는 전달이고, 글쓴이 자신의 검증이 아니다.
보고서의 논거 가운데 하나인 LLM이 생성한 코드의 컴파일 오류 중 94%가 타입 검사 실패였다는 수치는 TypeScript 선택의 이유를 직접 증명하지 않는다.
타입 검사 실패가 많다는 사실은 타입 시스템이 오류를 잡아 준다는 것과 같은 말이지만, 기여자가 TypeScript를 고르는 이유가 그것인지는 별개의 문제다.
프레임워크가 프로젝트를 TypeScript로 생성하는 기본값도 설명의 일부로 함께 제시되므로, AI의 기여가 어느 정도인지는 분리되지 않는다.

### 상표 소송 서술은 비대칭이다

글은 JavaScript 상표 사건의 경과를 자세히 정리하고, 합의 협상 때문에 사건이 중지되었다고 전한다.
그러나 양측이 어떤 조건으로 협상하는지는 공개되지 않았다고 스스로 인정한다.
글의 마지막 문장은 다음 회차 글의 제목에서 괄호 속 ECMAScript가 사라질지 지켜볼 만하다는 것이다.
이는 협상이 상표 포기로 끝날 수도 있다는 기대를 암시하지만, 사용 허락 같은 다른 결말도 가능하다고 글 자신이 말한다.
기대와 증거 사이의 간격은 글이 명시한 만큼이다.

### 도구의 네이티브 전환 비용은 짧게 다뤄진다

글은 JavaScript 도구가 Rust나 Go로 옮겨 가면서 기여의 진입 장벽이 높아졌다는 점을 한 문단으로 짚는다.
JavaScript 개발자가 자신이 쓰는 도구의 코드를 읽고 고치려면 이제 Rust나 Go를 알아야 하는 경우가 많다는 것이다.
이 비용은 속도 이득의 반대편에 있는데, 글은 TypeScript 7이 안정된 프로그래밍 API를 아직 제공하지 않아 Vue, Svelte, Astro, MDX 같은 언어 플러그인 기반 워크플로가 7.0을 온전히 쓰기 어렵다는 사실을 따로 적는다.
두 사실이 같은 구조에서 나온다는 점은 연결해 말하지 않는다.
성능 개선과 생태계 분리가 함께 온다는 것이다.

## 인사이트

### 기능의 채택은 연도가 아니라 지원 표가 정한다

글이 보여 준 사례(`Array.fromAsync`, Temporal, `using`)는 모두 명세 이전에 쓸 수 있게 됐다.
실무에서는 명세의 ES 연도를 따라가기보다 대상 브라우저와 런타임의 최소 버전을 정하고, 그 범위에서 쓸 수 있는 기능을 고르는 편이 현실에 맞다.
GeekNews에서 hbin09는 `await using`이 C#의 것을 그대로 가져온 것 같다고 했다.[^hbin09]
글도 `using`이 C#의 `using`, Python의 `with`, Java의 try-with-resources와 같은 역할을 한다고 설명하므로 비슷한 발상이다.
다만 JavaScript의 `using`은 `[Symbol.dispose]()`와 `[Symbol.asyncDispose]()`라는 메서드 규약과 `DisposableStack`, `SuppressedError`를 함께 도입한 것이 다른 언어와 구분되는 점이다.

### 검증 기준이 있는 일은 AI에게, 설계는 사람에게 맡기는 경계가 생겼다

글이 말하는 사례의 공통점은 기존 구현과 공식 테스트가 있다는 것이다.
LibJS 이식에는 Test262가, 타입 검사에는 타입 시스템이 판정 기준이었다.
TC39 위원들도 AI가 잘못 생성할 만한 코드일수록 언어가 올바른 구현을 직접 제공해야 한다고 말했다.
이 경계는 팀이 AI 도구를 쓸 때의 규칙으로 옮길 수 있다.
판정할 테스트가 있는 작업을 먼저 맡기고, 테스트가 없는 작업은 테스트를 먼저 만든다.

### 오래된 패턴을 도구가 알려 주는 시대가 된다

글은 학습 데이터의 시차 문제를 짚는다.
`Object.groupBy`, `Promise.withResolvers`, Temporal은 2023년 이후의 기능이라 학습 데이터에는 Lodash의 `groupBy`, `new Promise((resolve) => ...)`, Moment.js와 `Date` 코드가 더 많을 것이라는 서술이다.
MDN의 MCP 서버 공개와 Next.js의 `AGENTS.md` 자동 삽입이 이 문제에 대한 대응이다.
글의 관찰은 TypeScript 6.0과 7.0이 오래된 설정을 오류로 바꾼 것, `eslint-plugin-unicorn`의 `prefer-temporal` 규칙이 같은 역할을 한다는 것이다.
이 방향이 맞다면 린트 규칙과 컴파일러 옵션이 사람의 기억을 대신해 오래된 패턴을 걸러 내는 안전망이 된다.

### 이 글을 읽는 방법

당장 할 수 있는 일은 두 가지다.
자신이 지원해야 하는 브라우저와 런타임의 최소 버전을 적어 놓고, 글의 표 4와 표 5로 쓸 수 있는 기능을 확인하는 것이다.
TypeScript 6.0으로 옮겨 폐기 예정 옵션을 정리하는 것이 7.0 이전의 준비 단계라고 글이 설명한다.

이 글의 서술을 가를 관찰은 두 가지다.
TypeScript 7.1이 약속한 새 API가 나와 Vue와 Svelte의 언어 플러그인이 7.x에서 동작하는지가 하나다.
Safari가 Temporal을 안정판에서 지원하는 시점이 다른 하나다.
둘 다 이뤄지면 글이 전하는 전환은 생태계 전체의 이동이었던 것이 되고, 어느 하나가 늦어지면 속도 이득이 일부 환경에 한정된 이야기였다는 뜻이다.

---

[^wozo1004]: <https://news.hada.io/topic?id=35745#cid68238>

[^hbin09]: <https://news.hada.io/topic?id=35745#cid68220>
