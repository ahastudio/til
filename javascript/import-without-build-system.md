# 빌드 시스템 없이 프런트엔드 자바스크립트 라이브러리 가져오기

원문: [Importing a frontend Javascript library without a build system](https://jvns.ca/blog/2024/11/18/how-to-import-a-javascript-library/)

HN 토론: <https://news.ycombinator.com/item?id=42173623> (5점, 3개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/4tc5lt/importing_frontend_javascript_library> (14점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=17909>

## 요약

Julia Evans가 2024년 11월 18일에 쓴 실무 안내다.

동기가 첫 문단에 있다. 빌드 시스템 없이 자바스크립트를 쓰는 것을 좋아하는데, **백만 번째로** 빌드 시스템 없이 라이브러리를 가져오는 방법을 알아내야 하는 문제에 부딪혔고, **라이브러리의 설치 안내가 빌드 시스템을 쓴다고 전제하기 때문에** 알아내는 데 영원히 걸렸다는 것이다.

이제는 이 상황을 헤쳐 나가는 법을 대체로 익혀서 라이브러리를 성공적으로 쓰거나 너무 어렵다고 판단해 다른 것으로 바꿀 수 있게 되었다며, **몇 년 전에 있었으면 좋았을 안내서**를 쓴다고 밝힌다.

범위를 명확히 긋는다. **프런트엔드에서, 빌드 시스템 없는 구성에서만** 다룬다는 것이다.

## 세 가지 파일 종류

라이브러리가 제공할 수 있는 자바스크립트 파일이 기본적으로 세 종류다.

| 종류        | 브라우저에서 바로 되는가  | 판별 단서                             |
| ----------- | ------------------------- | ------------------------------------- |
| “고전” 방식 | 된다. `<script src>`면 끝 | `.umd.js` 확장자, CDN 사용 안내 배너  |
| ES 모듈     | 조건부로 된다             | `import`/`export` 구문, `.mjs` 확장자 |
| CommonJS    | **빌드 없이는 불가능**    | `require()`, `module.exports`, `.cjs` |

“고전”은 전역 변수를 정의하는 파일이다. 그냥 `<script src>`하면 **그냥 동작하는** 종류이며, 얻을 수 있으면 좋지만 언제나 있는 것은 아니다.

CommonJS는 Node용이고 **빌드 시스템 없이는 브라우저에서 전혀 쓸 수 없다**.

저자는 “고전”에 더 나은 이름이 있는지 모르겠다고 적고, AMD라는 종류도 있지만 2024년에 얼마나 관련 있는지 모르겠다고 덧붙인다.

그리고 판별을 어렵게 만드는 사실 하나를 짚는다.
**`.js`나 `.min.js` 확장자는 셋 중 무엇이든 될 수 있다.** 그래서 파일명이 `something.js`라면 직접 조사해야 한다.

## 어디서 파일을 찾는가

파일을 찾는 곳이 NPM 빌드다.

여기서 저자가 예상되는 반문을 먼저 꺼낸다. 요점이 Node를 안 쓰는 것인데 왜 NPM 이야기를 하느냐는 것이다.

답은 이렇다. `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js` 같은 CDN 링크를 쓰고 있다면 **여전히 NPM 빌드를 쓰고 있는 것**이다. CDN의 모든 파일이 원래 NPM에서 온다.

그래서 Node로 빌드할 계획이 전혀 없어도 `npm install`을 해 보기를 권한다.

```bash
# 임시 폴더를 만들어 설치하고, 다 보면 지운다
mkdir /tmp/whatever && cd /tmp/whatever
npm install chart.js
cd node_modules/chart.js/dist
ls *.*js
```

이유가 명확하다. 파일시스템에서 직접 뒤져 보면 **라이브러리가 빌드에서 제공하는 전부를 보고 있다고 100% 확신할 수 있고 CDN이 무언가 숨기고 있지 않다는 것도 확실해지기 때문**이다.

### 빌드 파일이 항상 `dist`에 있지는 않다

많은 라이브러리가 `dist`에 빌드를 두지만 **언제나 그렇지는 않다**. 위치는 `package.json`에 적혀 있다.

Chart.js의 예다.

```json
{
  "jsdelivr": "./dist/chart.umd.js",
  "unpkg": "./dist/chart.umd.js",
  "main": "./dist/chart.cjs",
  "module": "./dist/chart.js"
}
```

ES 모듈을 쓰려면 `module`이 가리키는 `dist/chart.js`를, jsDelivr와 unpkg CDN은 `dist/chart.umd.js`를 쓰라는 뜻으로 읽힌다. `main`은 Node용인 것 같다는 것이다.

`"type": "module"`도 있는데, 이것이 Node에게 파일을 기본적으로 ES 모듈로 취급하라고 알려 준다.
저자는 **정확히 어떤 파일이 ES 모듈이고 어떤 것이 아닌지는 알려 주지 않는 것 같고, 다만 그 안에 무언가가 ES 모듈이라는 것은 알려 준다**고 적는다.

## 세 가지 실제 사례

### Chart.js — UMD가 있는 경우

```bash
$ ls *.*js
chart.cjs  chart.js  chart.umd.js  helpers.cjs  helpers.js
```

셋으로 갈린다.
`chart.cjs`는 `.cjs` 확장자가 CommonJS임을 알려 주므로 브라우저에서 직접 쓸 수 없다.
`chart.js`는 확장자만으로는 모르지만 열어 보니 `import '@kurkle/color';`가 있어 **ES 모듈이라는 즉각적 신호**다.
`chart.umd.js`의 UMD는 Universal Module Definition이며, 기본 `<script src>`로도 CommonJS로도 AMD로도 쓸 수 있다는 뜻으로 이해된다.

저자는 세 번째를 골랐다.

```html
<script src="./chart.umd.js"></script>
```

이러면 전역 `Chart` 변수로 라이브러리를 쓸 수 있다. **더 쉬울 수 없다**는 것이다.
그리고 `chart.umd.js`를 **자기 Git 저장소에 복사해 넣어서** NPM이나 CDN이 사라지는 것을 걱정하지 않아도 되게 했다고 밝힌다.

### @atcute/oauth-browser-client — 의존성 있는 ES 모듈

```bash
$ ls *js
constants.js  dpop.js  environment.js  errors.js  index.js  resolvers.js
```

`index.js`가 유일하게 그럴듯한 루트 파일이고 내용이 이렇다.

```javascript
export { configureOAuth } from './environment.js';
export * from './errors.js';
export * from './resolvers.js';
```

`export` 구문이므로 **ES 모듈**이고, 빌드 없이 브라우저에서 쓸 수 있다.

그런데 `<script src="whatever.js">`처럼 간단하지는 않다. 이 모듈이 의존성을 가지므로 세 단계가 필요하다.

1. HTML에 임포트 맵을 설정한다
2. JS 코드에 `import { configureOAuth } from '@atcute/oauth-browser-client';` 같은 임포트 문을 넣는다
3. HTML에 `<script type="module" src="YOURSCRIPT.js"></script>`로 포함한다

왜 임포트 맵이 필요한가.
`import { X } from "./oauth-client-browser.js"` 같은 상대 경로로 안 되는 이유는, **모듈 내부에 `import {something} from @atcute/client` 같은 임포트 문이 더 있고 브라우저에게 그 코드를 어디서 가져올지 알려 줘야 하기 때문**이다.

```html
<script type="importmap">
{
  "imports": {
    "nanoid": "./node_modules/nanoid/bin/dist/index.js",
    "nanoid/non-secure": "./node_modules/nanoid/non-secure/index.js",
    "nanoid/url-alphabet": "./node_modules/nanoid/url-alphabet/dist/index.js",
    "@atcute/oauth-browser-client": "./node_modules/@atcute/oauth-browser-client/dist/index.js",
    "@atcute/client": "./node_modules/@atcute/client/dist/index.js",
    "@atcute/client/utils/did": "./node_modules/@atcute/client/dist/utils/did.js"
  }
}
</script>
```

저자의 평가가 솔직하다. **임포트 맵을 동작하게 만드는 일이 꽤 까다로우며, 자동 생성해 주는 도구가 있어야 할 것 같은데 아직 찾지 못했다**는 것이다.
esbuild의 metafile로 자동 생성 스크립트를 쓰는 것이 분명 가능하지만 해 보지 않았고 더 나은 방법이 있을지도 모른다고 덧붙인다.

글 끝의 미해결 질문 목록에서 이 질문에 **jspm이 답인 것 같다**고 밝힌다.

그리고 Simon Willison의 `download-esm`도 소개받았다고 적는다. ES 모듈을 내려받아 **임포트를 직접 JS 파일을 가리키도록 다시 써 주어서 임포트 맵이 필요 없게** 만드는 것이며, 아직 써 보지는 않았지만 훌륭한 발상 같다는 것이다.

### 의존성 없는 ES 모듈

의존성이 없으면 훨씬 쉽다. 임포트 맵이 필요 없다.

```html
<script type="module" src="YOURCODE.js"></script>
```

```javascript
import { whatever } from "https://example.com/whatever.js";
```

`type="module"`이 중요하다.

### @atproto/oauth-client-browser — CommonJS

같은 Bluesky 인증용인데 다른 라이브러리다. `index.js`를 열면 이렇다.

```javascript
__exportStar(require("@atproto/oauth-client"), exports);
__exportStar(require("./browser-oauth-client.js"), exports);
var util_js_1 = require("./util.js");
```

`require()`는 CommonJS 구문이므로 **브라우저에서 전혀 쓸 수 없고 빌드 단계가 필요하며 esbuild도 안 된다**.
`package.json`의 `"type": "commonjs"`도 같은 신호다.

원래 저자는 빌드 시스템을 배우지 않고는 CommonJS 모듈을 쓰는 것이 불가능하다고 생각했는데, Bluesky에서 누가 **esm.sh**를 알려 줬다고 한다. **무엇이든 ES 모듈로 변환해 주는 CDN**이다.

```html
<script type="module" src="script.js"></script>
```

```javascript
import { BrowserOAuthClient } from "https://esm.sh/@atproto/oauth-client-browser@0.3.0";
```

`skypack.dev`도 비슷한 일을 하며, 하나가 안 되면 다른 것을 시도한다는 사람도 있었다고 덧붙인다.

## 트레이드오프

### esm.sh는 빌드를 남에게 맡기는 것이다

저자가 esm.sh가 “그냥 동작해서 멋지다”고 하면서도 곧바로 단서를 단다.

**물론 이것도 여전히 일종의 빌드 시스템을 쓰는 것이며, 다만 내가 아니라 esm.sh가 빌드를 돌리는 것**이라는 점이다.

그리고 걱정 세 가지를 명시한다.

CDN이 영원히 동작하리라고 별로 신뢰하지 않으며, 보통은 미래에 어떤 이유로 사라지지 않도록 **의존성을 자기 저장소로 복사해 두기를 좋아한다**는 것이 첫째다.
**CDN의 보안 침해 사례를 들어 본 적이 있어 무섭다**는 것이 둘째다.
**esm.sh가 무엇을 하고 있는지 잘 이해하지 못한다**는 것이 셋째다.

세 번째가 특히 정직하다. 이해하지 못하는 것을 의존성으로 삼는 것에 대한 불편함이다.

그래서 저자는 esbuild 쪽이 더 끌린다고 정리한다. **이미 자기 컴퓨터에 있는 도구라서 더 신뢰한다**는 이유다.
다만 esbuild로 CommonJS를 ES 모듈로 바꾸는 데는 제약이 있어서 `import { X } from` 구문이 동작하지 않는다고 짚는다.

이 선택의 구조를 정리하면 이렇다.

| 방법      | 빌드를 누가 하나 | 언제 하나     | 위험                       |
| --------- | ---------------- | ------------- | -------------------------- |
| UMD 복사  | 아무도 안 함     | —             | 거의 없음. 파일이 저장소에 |
| 임포트 맵 | 아무도 안 함     | —             | 파일 수. 경로 관리         |
| esm.sh    | CDN              | 요청할 때마다 | CDN 소멸, 보안 침해        |
| esbuild   | 나               | 배포 전       | 도구 의존. 학습            |

“빌드 시스템 없이”라는 목표가 실제로는 **“빌드를 언제 누가 하는가”의 선택**이라는 것이 이 표의 요점이다.
빌드가 사라지는 경우는 UMD 하나뿐이다.

### 임포트 맵은 파일 수를 문제로 만든다

저자가 실제로 겪은 문제를 적는다.

브라우저에서 임포트 맵을 쓰는데 **사이트를 띄우려고 수십 개의 자바스크립트 파일을 내려받아야 했고, 개발용 웹서버가 어떤 이유로 감당하지 못했다**는 것이다.
파일들이 무작위로 로드에 실패하는 것을 계속 보았고 페이지를 새로 고쳐 이번에는 성공하기를 바라야 했다.

프로덕션에 배포하니 문제가 없어져서 로컬 개발 환경의 문제였던 것 같다고 정리한다.

그리고 ES 모듈 전반에 대해 조금 성가신 점을 하나 덧붙인다. **웹서버를 돌려야 한다**는 것이다. 분명 좋은 이유가 있겠지만 `index.html`을 그냥 열 수 있는 편이 쉽다는 것이다.

결론이 유보적이다. 이 “파일이 너무 많다” 문제 때문에 **임포트 맵을 이런 식으로 실제로 쓰는 것이 자기에게 그렇게 매력적이지는 않지만 가능하다는 것을 아는 것은 좋다**는 것이다.

이 판단은 상황에 따라 뒤집힌다.
HTTP/2 이상에서는 다중화가 되므로 파일 수의 대가가 훨씬 작고, 프로덕션에서 문제가 없었다는 저자의 관찰이 그것을 뒷받침한다.
병목은 파일 수 자체가 아니라 **개발 서버의 동시 연결 처리**였을 가능성이 크다.

### 브라우저 지원에 대한 판단은 지금 달라졌다

저자가 CanIUse를 근거로 임포트 맵이 “Baseline 2023: 주요 브라우저에서 새로 사용 가능”이므로 **2024년에는 아직 조금 너무 새로운 것 같다**고 적는다.

그래서 기준을 이렇게 세운다.
**나와 열두 명 정도만 쓰면 되는 재미있는 실험적 코드에는 임포트 맵을 쓰겠지만, 코드가 더 널리 쓰이기를 원한다면 esbuild를 쓰겠다**는 것이다.

이 판단이 2024년 11월 시점의 것이다.

Baseline에서 “newly available”은 주요 브라우저가 모두 지원하기 시작했다는 뜻이고, 30개월이 지나면 “widely available”로 바뀐다.
2023년에 newly available이었으므로 그 전환이 이미 지났다.

즉 이 글의 신중함은 그 시점에 타당했고 **지금은 근거가 약해졌다**.
2026년에 임포트 맵을 피할 이유는 구형 브라우저 지원이 실제로 필요한 경우로 좁혀진다.

## 함정

### `type` 필드가 어느 파일을 가리키는지 모른다

저자가 `package.json`의 `"type"` 필드에 대해 **정확히 어떤 파일을 가리키는지 분명하지 않다**고 두 번 적는다. 판별 요약에서도 “아마도”라는 단서를 붙였다.

이 혼란은 정당하다. 규칙이 직관적이지 않기 때문이다.

`"type"`은 **그 패키지 안의 `.js` 확장자 파일을 어떻게 해석할지**만 정한다.
`.mjs`는 `type`과 무관하게 언제나 ES 모듈이고, `.cjs`는 언제나 CommonJS다.

```text
"type": "module"    → .js 파일을 ES 모듈로 읽는다
"type": "commonjs"  → .js 파일을 CommonJS로 읽는다 (기본값)
"type" 없음         → commonjs와 같다
```

그리고 이것이 **Node의 규칙**이라는 점이 중요하다. 브라우저는 `package.json`을 읽지 않는다.
브라우저에게는 `<script type="module">`인지 아닌지만 있다.

그래서 저자의 실전 조언 — **파일을 열어서 `import`/`export`가 있는지 `require()`가 있는지 본다** — 가 메타데이터를 읽는 것보다 확실하다.

### 확장자가 아무것도 보장하지 않는다

저자가 짚은 대로 `.js`는 셋 중 무엇이든 될 수 있다.

그런데 더 나쁜 경우도 있다. **하나의 파일이 여러 형식을 동시에 만족하려 드는 경우**다. UMD가 정확히 그것이다.

```javascript
// UMD 파일의 전형적인 시작 부분
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined'
    ? factory(exports)                    // CommonJS
    : typeof define === 'function' && define.amd
      ? define(['exports'], factory)      // AMD
      : factory(global.Chart = {});       // 전역 변수
}(this, function (exports) { /* ... */ }));
```

이 래퍼가 실행 환경을 탐지해 셋 중 하나로 동작한다.
그래서 UMD 파일은 브라우저에서 전역 변수를 만들고 Node에서는 CommonJS로 동작한다.

확장자가 아니라 **이 래퍼의 존재**가 UMD의 진짜 판별 단서다.

### CDN 링크를 그대로 두면 저장소가 재현 불가능해진다

저자가 `chart.umd.js`를 Git 저장소에 복사한 이유를 “NPM이나 CDN이 사라지는 것을 걱정하지 않으려고”라고 적는다.

이 습관이 esm.sh 방식과 정면으로 충돌한다는 점을 짚어 둘 만하다.

```javascript
// 이 한 줄은 저장소에 아무것도 남기지 않는다
import { X } from "https://esm.sh/some-package@0.3.0";
```

버전이 고정되어 있어도 **esm.sh가 그 버전을 어떻게 변환하는지는 고정되지 않는다**. 변환기가 바뀌면 결과가 바뀐다.

저자가 “esm.sh가 무엇을 하고 있는지 잘 이해하지 못한다”고 한 불편함의 실체가 이것이다.
**의존성의 버전은 고정했는데 빌드 과정은 고정하지 않은 상태**다.

### Lobste.rs의 반응이 이 글의 배경을 요약한다

alper가 한 줄로 적었다.[^alper]

**자바스크립트 빌드는 완전한 난장판이며, 이런 사람들이 파이썬 패키징 상황에 대해 뻔뻔하게 논평했을 것**이라는 것이다. 파이썬이 아무리 나빴어도 **의존성을 로드하는 호환되지 않는 방법이 세 가지나 있지는 않았다**는 지적이다.

그리고 자기는 프런트엔드를 Rust로 쓰고 있는데, 그것이 아무리 성가시더라도 **자바스크립트 도구를 전혀 다루지 않아도 되는 것이 모든 면에서 큰 장점**이었다고 덧붙였다.

이 반응이 이 글의 존재 이유를 뒤집어 설명한다.
저자는 마지막에 이 글의 목표가 자바스크립트에 대한 불평이 아니며 **도구를 자기에게 맞는 방식으로 쓸 수 있도록 지형을 이해하는 것**이라고 명시했는데, 정확히 그 지형이 이만큼 복잡하다는 사실 자체가 반응을 부른다.

HN 쪽 반응도 같은 방향이다.
hippo77은 **여전히 구식 자바스크립트를 쓰는 사람들은 라이브러리가 평범한 고전 배포 파일을 제공할 때 정말 고마워한다**고 적었고,[^hippo77]
anitil은 이것이 자기에게도 흔한 고통의 원천이며 **뇌가 기억하기를 거부해서 늘 같은 단계를 되짚게 된다**고 했다.[^anitil]
pacifika는 여기 누군가 남은 질문들에 답해 주기를 바랐다고 적었다.[^pacifika]

라이브러리를 가져오는 방법을 **매번 다시 알아내야 한다**는 것이 이 영역의 상태다.

## 체크리스트

- 라이브러리를 고르기 전에 `npm install`로 실제 빌드 파일 목록을 봤는가
- `package.json`의 `jsdelivr`/`unpkg`/`main`/`module` 필드를 확인했는가? `dist`에 있다고 가정하지 않았는가
- 파일을 열어 `import`/`export`인지 `require()`인지 직접 확인했는가? 확장자만 믿지 않았는가
- `.umd.js`가 있다면 그것을 먼저 시도했는가? 가장 단순한 경로다
- ES 모듈을 쓴다면 `<script type="module">`을 붙였는가
- 의존성이 있는 ES 모듈인데 임포트 맵 없이 쓰려 하고 있지 않은가
- CDN에서 직접 임포트하고 있다면, 그 CDN이 사라져도 되는 코드인가
- 오래 유지할 코드라면 의존성 파일을 저장소에 복사해 두었는가

## 기억할 원칙

### 설치 안내가 전제하는 것이 그 라이브러리의 진짜 요구사항이다

이 글이 시작된 이유가 라이브러리의 설치 안내가 **빌드 시스템을 쓴다고 전제하기 때문**이었다.

이것이 자바스크립트만의 문제가 아니다.

설치 안내는 대체로 **저자가 쓰는 환경**을 기술한다. 그것이 유일한 방법이어서가 아니라 저자가 그것만 시험했기 때문이다.
그래서 안내를 벗어나는 순간, 그 라이브러리가 실제로 무엇을 요구하는지 직접 알아내야 한다.

이 글의 방법론이 정확히 그 작업이다. 안내를 읽는 대신 **빌드 산출물을 직접 뒤지는 것**이다.
`npm install` 후 `ls`하고 파일을 열어 보는 세 단계가 안내서 전체보다 많은 것을 알려 준다.

일반화하면, 문서가 말하는 사용법과 산출물이 허용하는 사용법은 다르고, **후자가 실제 계약**이다.

그리고 이 차이는 문서가 나쁠 때만 생기는 것이 아니다. 문서는 하나의 경로만 설명할 수 있고 산출물은 여러 경로를 허용하기 때문에 **구조적으로 생긴다**.

### 표준이라는 것이 도구를 버릴 수 있게 만든다

이 글에서 가장 값진 한 문단이 ES 모듈이 표준이라는 점에 대한 것이다.

저자가 CommonJS와 ES 모듈의 주된 차이를 **ES 모듈이 실제로 표준이라는 것**으로 본다.
브라우저가 웹 표준에 대해 영원히 하위 호환을 약속하므로, 오늘 ES 모듈로 코드를 쓰면 **15년 뒤에도 같은 방식으로 동작하리라고 확신할 수 있다**는 것이다.

그런데 그다음 문장이 더 흥미롭다.

표준이라는 사실이 **esbuild 같은 도구를 쓰는 것에 대해서도 기분이 나아지게 만든다**는 것이다.
esbuild 프로젝트가 죽더라도 **표준을 구현하고 있으므로 대체할 비슷한 도구가 미래에 있을 것 같기 때문**이다.

이 논리 구조가 일반적으로 쓸 만하다.

도구를 고를 때 흔히 묻는 것은 “이 도구가 오래갈까”다. 그런데 그 질문에는 답할 방법이 없다.
대신 물어야 할 것은 **“이 도구가 죽으면 무엇이 남는가”**다.

표준을 구현하는 도구가 죽으면 표준이 남고, 대체재를 찾으면 된다.
표준이 없는 영역의 도구가 죽으면 그 도구의 관습에 맞춰 쓴 코드 전체가 남고, 그것은 부채다.

그러므로 도구의 수명보다 **그 도구가 서 있는 지반이 표준인지**가 중요하다.

이 원칙이 이 글의 선택들을 설명한다.
esm.sh보다 esbuild를 선호한 것, UMD 파일을 저장소에 복사한 것, 임포트 맵이 아직 새롭다고 판단한 것이 전부 **무엇이 사라져도 남는가**를 계산한 결과다.

### 좋은 안내서는 선택지가 아니라 판별법을 준다

이 글의 구조가 특이하다. “이렇게 하세요”가 아니라 **“무엇인지 알아내세요”**로 시작한다.

세 종류를 먼저 설명하고, 어떻게 판별하는지 알려 주고, 각각을 어떻게 쓰는지는 그다음이다.

이 순서가 중요한 이유가 있다.

“라이브러리를 가져오는 법”을 절차로 쓰면 라이브러리 수만큼 절차가 필요하다.
반면 **판별법을 주면 독자가 처음 보는 라이브러리에도 적용할 수 있다**.

저자가 요약 절을 종류별 “쓰는 법”과 “판별하는 법”으로 나눠 놓은 것이 그 설계다.
그리고 “`.js`는 셋 중 무엇이든 될 수 있으니 더 조사해야 한다”는 문장이 그 설계의 핵심을 드러낸다. **판별이 실패할 수 있다는 것까지 알려 주는 것**이다.

anitil이 “뇌가 기억하기를 거부해서 늘 같은 단계를 되짚게 된다”고 한 것이 이런 안내서가 필요한 이유다.
외울 수 없는 종류의 지식이 있고, 그런 지식은 절차가 아니라 **판별 기준의 형태로 적어 두어야** 다시 찾아 쓸 수 있다.

---

[^alper]: <https://lobste.rs/s/4tc5lt/importing_frontend_javascript_library#c_a9robu>

[^hippo77]: <https://news.ycombinator.com/item?id=42258530>

[^anitil]: <https://news.ycombinator.com/item?id=42178802>

[^pacifika]: <https://news.ycombinator.com/item?id=42181254>
