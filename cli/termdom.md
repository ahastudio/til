# TermDOM: HTML과 CSS로 터미널 앱을 만드는 라이브러리

<https://termdom.org/>

<https://github.com/bikeshaving/termdom>

HN 토론: <https://news.ycombinator.com/item?id=49261987> (18점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=33760>

## 소개

TermDOM은 HTML과 CSS를 터미널에 렌더링하는 JavaScript/TypeScript 라이브러리다.
실제 DOM 노드를 터미널 출력으로 그리고, 노드가 변경되면 화면을 다시 그린다.
그래서 TUI와 대화형 CLI를 바닐라 JavaScript로, 또는 프런트엔드 프레임워크로 작성할 수 있다.

이 라이브러리가 내세우는 계약은 위젯 API를 없앤다는 것이다.
기존 터미널 UI 라이브러리는 `Box`, `List`, `Screen` 같은 자체 위젯과 거기 딸린 임의의 API를 배우라고 요구한다.
TermDOM은 그 대신 명세를 따르는 진짜 DOM과 CSSOM API를 구현했다.
`div`를 만들고, 스타일을 주고, `body`에 붙인다. 브라우저와 마찬가지로 렌더 호출이 없고 변경은 자동으로 화면에 반영된다.

계약의 경계도 명시되어 있다.
TermDOM은 웹 명세를 최대한 따르되, 터미널에서 의미가 성립하지 않는 개념에 대해서만 갈라진다.
어떤 브라우저 기능이 구현되었는지는 별도의 호환성 표에서 확인하게 되어 있고, 이는 곧 전부 구현되어 있지는 않다는 뜻이다.
현재 버전은 `0.1.x`대이며 MIT 라이선스다.

가장 작은 예제는 이렇게 생겼다.

```typescript
import {TermDOM} from "@b9g/termdom";

const term = new TermDOM();
term.attach();
const {document} = term;

const heading = document.createElement("div");
heading.style.backgroundColor = "blue";
heading.style.color = "white";
heading.style.padding = "0 1ch";
heading.textContent = "Hello, terminal";

const subtitle = document.createElement("div");
subtitle.style.color = "yellow";
subtitle.style.marginTop = "1px";
subtitle.textContent = "HTML and CSS, drawn with ANSI escape sequences";

document.body.appendChild(heading);
document.body.appendChild(subtitle);
```

`new TermDOM()`으로 인스턴스를 만들고 `attach()`로 터미널에 붙인 뒤, 그 인스턴스의 `document`를 꺼내 쓴다.
브라우저 코드와 다른 지점은 이 세 줄뿐이고 나머지는 평범한 DOM 조작이다.

## 동작 방식

### 셀이 픽셀이다

TermDOM을 이해하는 핵심 하나는 길이 단위다.
CSS 길이의 기준 단위가 문자 셀이며, `1px`과 `1ch`가 둘 다 셀 하나를 뜻한다.
브라우저에서 `1px`과 `1ch`는 전혀 다른 값이지만 여기서는 같다. 터미널에는 셀보다 작은 단위가 없기 때문이다.

이 사실은 레이아웃 코드를 읽을 때 계속 따라다닌다.
`padding: "1px 2px"`는 위아래 한 줄, 좌우 두 칸을 뜻한다.
브라우저 감각으로 `padding: 8px`을 쓰면 여덟 줄과 여덟 칸이 생기므로, 웹에서 가져온 스타일시트는 길이 값을 전부 다시 잡아야 한다.

### 레이아웃은 브라우저 알고리즘, 출력은 셀 격자

TermDOM은 박스를 브라우저의 알고리즘으로 배치한다.
플렉스박스, 그리드, 테이블, 박스 모델이 모두 동작하며, 그 결과가 문자 셀 격자에 맞춰 그려진다.
텍스트는 자기 박스의 끝에서 줄바꿈되고, 터미널 크기가 바뀌면 다시 흐른다.

여기서 중요한 것은 공백 처리까지 브라우저를 따른다는 점이다.
여러 줄로 쓴 마크업이 브라우저에서처럼 배치되며, 항목 사이의 공백은 항목이 아니다.
`display: flex`를 주고 자식들을 여러 줄에 걸쳐 써도 그 사이 개행이 별도의 칸을 만들지 않는다는 뜻이고, 이는 직접 만든 TUI 레이아웃 엔진에서는 보통 직접 처리해야 하는 부분이다.

### 스타일은 진짜 캐스케이드를 거쳐 ANSI로 나간다

스타일시트와 인라인 스타일이 실제 캐스케이드를 통과하고, 계산된 스타일이 ANSI 이스케이프 시퀀스로 화면에 기록된다.
색은 터미널 팔레트에 맞춰 해석되고, 텍스트 장식은 터미널 속성으로 그려진다. 굵게, 기울임, 밑줄, 취소선이 모두 대응된다.

우선순위 규칙도 그대로다.
아래 예제는 캐스케이드가 실제로 동작함을 보여 주기 위해 만들어진 것이다.

```typescript
import {TermDOM} from "@b9g/termdom";

const term = new TermDOM();
term.attach();
const {document} = term;

document.head.innerHTML = `
  <style>
    p { color: gray; }
    .warm { color: yellow; }
    .warm.hot { color: red; font-weight: bold; }
    a { color: cyan; text-decoration: underline; }
    del { color: #888; text-decoration: line-through; }
    .badge { background-color: blue; color: white; padding: 0 1ch; }
  </style>
`;

document.body.innerHTML = `
  <p>A paragraph made gray by a CSS rule.</p>
  <p class="warm">A class makes this paragraph yellow.</p>
  <p class="warm hot">Two classes beat one: red and bold.</p>
  <p class="warm hot" style="color: green">An inline style beats all rules.</p>
  <p>Text can be <b>bold</b>, <i>italic</i>, <a>underlined</a> or <del>struck through</del>.</p>
  <p><span class="badge">A background</span> paints its cells.</p>
`;
```

클래스 두 개가 하나를 이기고, 인라인 스타일이 모든 규칙을 이긴다.
`#888` 같은 16진수 색을 쓰면 터미널이 자기 팔레트에서 가장 가까운 값으로 해석한다.

### 입력은 stdin 이스케이프 시퀀스에서 DOM 이벤트로

TermDOM은 stdin의 이스케이프 시퀀스를 DOM 이벤트로 디코딩해 실제 타깃에 전달한다.
`keydown`은 포커스된 요소에, `click`은 포인터 아래 요소에, `paste`는 붙여 넣은 텍스트와 함께 발생한다.
Tab은 포커스를 이동시키고 `:focus` 스타일이 그것을 따라간다.

이 설계의 의미는 이벤트 위임이 그대로 성립한다는 것이다.
`document.addEventListener("keydown", ...)`로 전역 단축키를 받고, 개별 입력 필드는 자기 `input` 이벤트를 받는 구조를 별도 장치 없이 쓸 수 있다.

### 브라우저 라이브러리가 수정 없이 돌아간다

진짜 DOM을 구현한 대가로 얻는 것이 이 항목이다.
브라우저용 라이브러리를 수정 없이 터미널에서 쓸 수 있고, 약간의 설정을 더하면 대부분의 프런트엔드 프레임워크와도 함께 동작한다.

공식 예제 중 가장 설득력 있는 것이 Prism 예제다.
Prism이 소스 텍스트를 `<span class="token keyword">` 같은 마크업으로 바꾸고, Prism의 CSS 테마(Tomorrow Night)가 그 클래스들을 색으로 옮기고, TermDOM이 그 결과를 셀로 그린다.
웹 하이라이터와 웹 스타일시트가 터미널에서 그대로 작동하는 것이다.
같은 예제에는 `@media (max-width: 72ch)`로 화면이 좁아지면 줄 번호 거터를 숨기는 규칙이 들어 있고, 터미널 크기가 바뀔 때마다 이 미디어 쿼리가 다시 평가된다.

## 폼 만들기

입력 위젯은 사용자 에이전트 섀도 트리로 구현되어 있다.
즉 `<input>`을 쓰면 브라우저에서처럼 값과 포커스를 관리하고 `input` 이벤트를 발생시킨다.

```typescript
import {TermDOM} from "@b9g/termdom";

const term = new TermDOM();

term.attach();
const {document} = term;

const style = document.createElement("style");
style.textContent = `
  .form { padding: 1ch 2ch; }
  .title { color: cyan; font-weight: bold; }
  .field { display: flex; flex-direction: row; padding: 1 0 0 0; }
  .label { color: white; width: 8ch; padding: 1 0 0 0; }
  input { background: #1d3557; color: white; width: 28ch; }
  input:focus { background: #264f78; }
  .preview { color: #888; padding: 1 0 0 0; }
  .done { color: green; font-weight: bold; padding: 1 0 0 0; }
  .hint { color: #666; padding: 1 0 0 0; }
`;
document.head.appendChild(style);

const form = document.createElement("div");
form.className = "form";
form.innerHTML = `
  <div class="title">New profile</div>
  <div class="field"><div class="label">Name</div><input id="name" type="text" autofocus></div>
  <div class="field"><div class="label">Email</div><input id="email" type="text"></div>
  <div class="field"><div class="label">Handle</div><input id="handle" type="text"></div>
  <div class="preview" id="preview"></div>
  <div class="done" id="done"></div>
  <div class="hint">tab next field · enter submit · ctrl+c quit</div>
`;
document.body.appendChild(form);

const fields = ["name", "email", "handle"].map(
  (id) => document.getElementById(id) as HTMLInputElement,
);
const preview = document.getElementById("preview")!;
const done = document.getElementById("done")!;

function updatePreview(): void {
  const [name, email, handle] = fields.map((f) => f.value);
  preview.textContent = name || email || handle
    ? `» ${name || "?"} <${email || "?"}> @${handle || "?"}`
    : "» start typing to build a profile";
  done.textContent = "";
}

// 표준 이벤트를 그대로 쓴다. 어느 필드든 편집될 때마다 발생한다.
for (const field of fields) {
  field.addEventListener("input", updatePreview);
}

// 전역 단축키는 document에서 받는다. 포커스가 어느 입력에 있든 동작한다.
document.addEventListener("keydown", (event: Event) => {
  if ((event as KeyboardEvent).key !== "Enter") {
    return;
  }
  const [name, email, handle] = fields.map((f) => f.value.trim());
  if (!name && !email && !handle) {
    return;
  }
  done.textContent = `✓ saved: ${name || "anonymous"} <${email || "n/a"}> @${handle || "n/a"}`;
});

updatePreview();
```

주목할 점이 두 가지 있다.
첫째, `autofocus` 속성이 동작하고 `input:focus` 선택자로 포커스된 필드의 배경을 바꿀 수 있다. Tab 이동은 라이브러리가 처리한다.
둘째, 값 읽기가 `field.value`다. 별도의 상태 저장소를 만들지 않고 DOM을 상태의 소유자로 두는 구조이며, 이는 웹에서와 같은 트레이드오프를 그대로 가져온다.

## 값 정하기

| 항목           | 출발값                           | 근거                                                                             |
| -------------- | -------------------------------- | -------------------------------------------------------------------------------- |
| 길이 단위      | `1ch`로 통일                     | `1px`과 같은 값이지만 셀 기준임이 코드에 드러나 웹 감각의 오해를 줄인다          |
| 색 지정        | 기본 색 이름 우선, 16진수는 보조 | 16진수는 터미널 팔레트로 근사되므로 의도한 색과 달라질 수 있다                   |
| 폭 기준        | 80칸을 기본 가정                 | 예제들이 80칸 화면을 기준으로 작성되어 있고, 가장 좁은 흔한 환경이다             |
| 반응형 분기점  | `@media (max-width: 72ch)` 부근  | 80칸에서 좌우 여백과 거터를 빼면 실제 본문이 좁아지기 시작하는 지점이다          |
| 상태 보관 위치 | DOM(`input.value`)               | 소규모 폼에서는 가장 짧지만, 화면이 커지면 별도 상태 모델로 옮길 기준이 필요하다 |

무엇을 측정해 이 값들을 고칠지도 정해 두는 편이 낫다.
터미널 폭은 실행 환경마다 다르므로, 개발 중 화면 크기를 80칸과 120칸 두 가지로 바꿔 보면서 분기점이 실제로 맞는지 확인하는 것이 가장 싼 검증이다.
색은 터미널 에뮬레이터와 테마에 따라 달라지므로, 대상 환경이 하나가 아니라면 밝은 배경과 어두운 배경에서 각각 확인해야 한다.

## 트레이드오프

### 위젯 API를 배우지 않는 대신 명세의 일부만 얻는다

TermDOM의 판매 논리는 학습 비용의 이전이다.
`blessed`나 `ink` 같은 라이브러리의 위젯 목록을 외우는 대신, 이미 아는 DOM과 CSS를 쓰라는 것이다.
웹 개발 경험이 있다면 이 거래는 명백히 이득으로 보인다.

문제는 이미 안다는 전제가 어디까지 참이냐다.
TermDOM은 명세를 따르되 터미널에서 의미가 없는 개념에서는 갈라진다고 밝히고, 어디가 갈라지는지는 호환성 표에 있다.
즉 실제 작업에서 개발자가 알아야 하는 것은 DOM 전체가 아니라 “DOM 중 TermDOM이 구현한 부분”이고, 이것은 위젯 목록과 마찬가지로 하나의 API 표면이다.
차이는 그 표면이 익숙한 이름을 쓴다는 것인데, 이것은 이점이자 함정이다. 없는 기능을 없다고 알아채는 것보다, 있는 줄 알았던 기능이 조용히 다르게 동작하는 것이 더 비싸다.

명백한 손해도 하나 있다.
위젯 라이브러리는 터미널에서 자주 쓰는 구성 요소, 예컨대 스크롤되는 목록, 테이블 정렬, 진행 표시줄, 모달을 완성된 형태로 준다.
DOM은 그중 아무것도 주지 않는다. 웹에서도 이 위젯들은 직접 만들거나 UI 라이브러리를 가져다 쓰는 것이기 때문이다.
그래서 “브라우저 라이브러리를 수정 없이 쓸 수 있다”는 이점이 실제로 얼마나 큰지는, 필요한 그 라이브러리가 TermDOM이 구현한 DOM 부분만 쓰는지에 달려 있다.

### 브라우저 알고리즘의 비용을 터미널에서 치른다

플렉스박스와 그리드와 테이블을 명세대로 구현하면 레이아웃 계산 비용이 따라온다.
브라우저에서는 이 비용을 최적화된 네이티브 엔진이 부담하지만, 여기서는 JavaScript가 부담한다.
그리고 터미널 앱은 대체로 키 입력마다 화면을 다시 그린다.

여기서 눈에 띄지 않는 함정이 생긴다.
TUI는 웹 페이지보다 갱신 빈도가 높고 지연에 훨씬 민감하다. 웹에서 16ms는 한 프레임이지만, 터미널에서 키를 누르고 16ms 뒤에 글자가 나타나는 것은 사람이 느낀다.
셀 격자라서 요소 수가 적다는 점이 이 비용을 상당 부분 상쇄하지만, 상쇄되는 지점이 어디까지인지는 프로젝트 문서가 답하지 않는다.
전체 화면을 채우는 목록을 빠르게 스크롤하는 것이 실질적인 성능 시험대이고, 도입 전에 직접 재 봐야 하는 항목이다.

명백한 우회책도 없다.
성능이 문제가 되면 웹에서는 가상 스크롤이나 `will-change` 같은 수단을 쓰지만, 그 수단들 자체가 브라우저 엔진의 구현에 기댄 것이라 여기서 그대로 통하리라 기대하기 어렵다.
결국 요소 수를 줄이거나 갱신 범위를 좁히는 직접적인 방법만 남는다.

### 접근성은 웹 어휘를 쓰지만 웹의 보조 기술은 따라오지 않는다

`<input>`, `<a>`, `role` 같은 웹 어휘를 쓴다는 사실이 접근성을 보장하지 않는다.
브라우저에서 그 어휘가 의미를 갖는 이유는 접근성 트리를 만들어 스크린 리더에 전달하는 계층이 있기 때문이고, 터미널에는 그 계층이 없다.
터미널에서 스크린 리더는 화면에 출력된 문자를 읽으며, 전체 화면을 다시 그리는 TUI는 그 방식과 잘 맞지 않는다.

그래서 여기에는 얻는 것과 잃는 것이 비대칭으로 존재한다.
얻는 것은 시맨틱 마크업을 쓰는 습관이고, 잃는 것은 그 마크업이 실제로 보조 기술에 전달되는 경로다.
`<button>`이라고 적었으니 접근성이 챙겨졌다고 여기기 쉬운데, 이 환경에서 그 추론은 성립하지 않는다.

이 문제는 TermDOM만의 것이 아니라 TUI 전반의 것이고, 우회책도 TUI 전반의 것과 같다.
화면을 다시 그리는 범위를 최소화하고, 상태 변화를 텍스트로도 출력하고, 키보드만으로 모든 동작에 닿을 수 있게 하는 것이다.
다만 웹 어휘를 쓰는 라이브러리는 이 문제를 더 잘 숨기기 때문에, 명시적으로 짚어 둘 필요가 있다.

### 프레임워크를 얹으면 얻는 것과 늘어나는 것

프런트엔드 프레임워크와 함께 쓸 수 있다는 것은 강력한 선택지다.
컴포넌트, 상태 관리, 조건부 렌더링 같은 것을 이미 아는 방식으로 쓸 수 있다.

늘어나는 것은 계층이다.
React나 Vue의 가상 DOM은 실제 DOM 조작을 줄이기 위한 장치인데, 여기서는 그 실제 DOM 자체가 이미 JavaScript 구현체이고 그 아래에 다시 셀 격자 렌더링이 있다.
프레임워크 → 가상 DOM → TermDOM의 DOM → 레이아웃 계산 → ANSI 출력이라는 사슬이 되며, 각 단계가 디버깅 시 들여다봐야 할 층이 된다.
바닐라로 쓰면 이 사슬이 두 단계 짧다.

판단 기준은 화면의 상태 복잡도다.
상태가 몇 개의 값이고 갱신이 국소적이면 바닐라 DOM 조작이 짧고 빠르다.
상태가 트리 구조이고 여러 곳이 동시에 반응해야 하면 프레임워크가 값을 한다.
중간 지대에서는 바닐라로 시작해 필요해질 때 옮기는 편이 낫다. TermDOM이 진짜 DOM이므로 그 이전이 가능한 것이 이 라이브러리의 실질적 이점이다.

## 함정

터미널 폭에 대한 가정이 코드에 흩어진다.
예제들이 80칸을 전제하고 줄 길이를 64칸 아래로 유지하는 식으로 작성되어 있는데, 이 가정은 주석에만 남고 코드에는 드러나지 않는다.
분기점을 상수로 두고 미디어 쿼리와 함께 관리하지 않으면, 나중에 폭 가정을 바꿀 때 어디를 고쳐야 하는지 알 수 없게 된다.

유니코드 폭이 셀 수와 어긋난다.
예제 곳곳에 이모지가 쓰이는데, 이모지와 한중일 문자는 셀 두 개를 차지한다.
레이아웃 계산이 이것을 정확히 처리하는지는 문자와 터미널 에뮬레이터 조합에 따라 달라지며, 한글을 쓰는 UI라면 폭 계산이 어긋나 테두리가 밀리는 현상이 가장 먼저 만나게 될 문제다.
도입 전에 한글 텍스트로 정렬이 맞는지 확인하는 것이 순서다.

색이 환경에 따라 달라진다.
`color: “#888”` 같은 지정은 터미널 팔레트로 근사되므로, 사용자의 테마에 따라 대비가 무너질 수 있다.
배경색을 지정하면서 전경색을 기본값으로 두면 어떤 테마에서는 읽히지 않는 조합이 나온다. 배경을 지정할 때는 전경도 함께 지정하는 편이 안전하다.

`0.1.x` 버전이다.
호환성 표가 존재한다는 것은 미구현 영역이 있다는 뜻이고, 버전 번호는 API가 바뀔 수 있다는 뜻이다.
평가와 개인 도구에는 충분하지만, 장기 유지보수 대상에 넣을 때는 필요한 CSS 속성과 DOM API가 지금 구현되어 있는지 먼저 확인해야 한다.

## 확인하기

설치는 한 줄이다.

```bash
npm install @b9g/termdom
```

가장 빠른 검증은 앞의 `hello-world.ts`를 실행한 뒤 터미널 크기를 바꿔 보는 것이다.
텍스트가 다시 흐르면 리사이즈 처리가 동작하는 것이고, 배경색이 셀 단위로 정확히 칠해지면 색 해석이 의도대로 된 것이다.

그다음으로 확인할 것은 자기 환경에 특화된 두 가지다.

```typescript
// 한글과 이모지의 셀 폭이 레이아웃과 맞는지 확인한다.
const box = document.createElement("div");
box.style.backgroundColor = "blue";
box.style.color = "white";
box.style.width = "20ch";
box.textContent = "한글 텍스트와 🚀 이모지";
document.body.appendChild(box);
```

배경색이 칠해진 영역이 정확히 20칸인지, 텍스트가 그 안에서 잘리거나 넘치지 않는지를 눈으로 확인하면 된다.
넘친다면 그 조합에서는 폭 계산이 어긋나는 것이고, 한글 UI를 만들 계획이라면 이 단계에서 도입 여부가 갈린다.

성능은 요소 수를 늘려 재는 것이 가장 직접적이다.
수백 개의 행을 만들어 붙인 뒤 키 입력으로 하나씩 클래스를 바꿔 가며 반응 지연을 체감해 보면, 앞에서 말한 갱신 비용이 자기 용도에서 문제가 되는지 답이 나온다.

## 체크리스트

- 필요한 CSS 속성과 DOM API가 호환성 표에 구현됨으로 표시되어 있는가
- 한글 또는 이모지를 포함한 텍스트에서 박스 폭이 의도대로 맞는가
- 배경색을 지정한 모든 요소에 전경색도 함께 지정했는가
- 길이 값을 `1ch` 기준으로 통일했고, 웹 감각의 픽셀 값이 남아 있지 않은가
- 터미널 폭 가정이 상수 한 곳에 모여 있는가
- 가장 큰 화면에서 키 입력 반응 지연을 실제로 측정했는가
- 키보드만으로 모든 동작에 닿을 수 있는가
- 프레임워크를 얹기 전에 바닐라로 만들어 보았는가

## 기억할 원칙

### 익숙한 API를 빌려 오는 것은 학습 비용이 아니라 학습의 방향을 바꾼다

TermDOM의 설계 판단은 새 API를 만들지 않는 것이었고, 그 이득은 진입 장벽이 아니라 전이 가능성에 있다.
DOM을 배우는 시간은 이 라이브러리를 쓰지 않게 되어도 남지만, `blessed`의 위젯 API를 배운 시간은 `blessed`를 떠나면 사라진다.
도구를 고를 때 이 구분은 기능 비교표보다 오래 유효하다.

다만 같은 이유로 비용이 옮겨 가는 곳도 분명하다.
익숙한 이름은 익숙한 동작을 기대하게 만들고, 그 기대가 어긋나는 지점은 낯선 API에서보다 찾기 어렵다.
그래서 이런 라이브러리를 쓸 때 가장 먼저 읽어야 할 문서는 튜토리얼이 아니라 호환성 표다.
무엇이 되는지가 아니라 무엇이 다른지가 실제 작업에서 시간을 잡아먹는 쪽이기 때문이다.
