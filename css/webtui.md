# WebTUI

> Modular CSS Library that brings the beauty of
> Terminal UIs to the browser.

<https://webtui.ironclad.sh/>

<https://github.com/webtui/webtui>

HN 토론: <https://news.ycombinator.com/item?id=43668250> (321점, 153개 댓글)

GN 토론: <https://news.hada.io/topic?id=20320>

터미널 UI(TUI)의 미학을 브라우저로 가져오는
모듈형 CSS 라이브러리.
Bootstrap이나 Tailwind 같은 풀 프레임워크가 아니라,
터미널 느낌의 스타일링에 집중하는 경량 레이어다.

## 핵심 특징

- **순수 CSS**: JavaScript 런타임 불필요, 의존성 제로
- **모듈형 설계**: 필요한 컴포넌트만 개별 임포트 가능
- **CSS `@layer`**: 스타일 우선순위를 예측 가능하게 제어,
  `!important` 남용 방지
- **속성(Attribute) 기반**: 클래스 대신 HTML 속성으로
  스타일 적용 (`is-`, `box-`, `variant-`, `size-`)
- **테마 시스템**: Light/Dark 기본 지원 +
  Catppuccin, Gruvbox, Nord, Vitesse, Everforest, Osmium
- **플러그인**: 선언형 레이아웃, Nerd Font 통합,
  그리고 여러 공식 테마가 플러그인으로 제공된다

## 설치

```bash
npm i @webtui/css
# 또는
bun i @webtui/css
```

CDN:

```html
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@webtui/css/full.css">
```

## 아키텍처: 3-Layer 구조

```css
@layer base, utils, components;
```

### base (base.css)

리셋/노멀라이즈 + CSS 커스텀 프로퍼티(테마 변수).
모든 프로젝트에서 반드시 임포트.

### utils (utils/box.css 등)

재사용 가능한 유틸리티. `box-` 속성으로
ASCII 스타일 박스 테두리(square, round, double) 적용.

### components (components/*.css)

개별 임포트 가능한 컴포넌트 목록:
Accordion, Badge, Button, Checkbox, Dialog, Input,
Mark, Popover, Pre, Progress, Radio, Range, Separator,
Spinner, Switch, Table, Textarea, Tooltip,
Typography, View.

## 사용법

```css
@layer base, utils, components;
@import '@webtui/css/base.css';
@import '@webtui/css/utils/box.css';
@import '@webtui/css/components/button.css';
@import '@webtui/css/components/input.css';
/* 테마는 마지막에 */
@import '@webtui/theme-catppuccin';
```

```html
<button>기본 버튼</button>
<button variant-="primary">Primary</button>
<span is-="badge" variant-="success">완료</span>
<div box-="round">둥근 테두리 박스</div>
```

공식 문서가 첫 화면에 내거는 예제는 이렇게 짧다.

```html
<button variant-="foreground0">Click</button>
<label>
  <input type="checkbox" is-="switch" />
  Hello there
</label>
```

```css
@import "@webtui/css/base.css";
@import "@webtui/css/components/button.css";
```

여기서 두 가지가 드러난다.
첫째, 스위치는 별도 컴포넌트가 아니라 체크박스에 `is-="switch"`를 붙인 것이다.
동작은 네이티브 체크박스가 그대로 맡고 CSS가 생김새만 바꾸므로, 폼 제출과 키보드 조작과 스크린 리더 인식이 전부 기본값을 따른다.
둘째, `variant-="foreground0"`처럼 변형 이름이 의미가 아니라 팔레트 슬롯을 가리킨다.
`primary`나 `success` 같은 의미 이름과 달리 테마의 색 번호를 직접 쓰는 방식이며, 터미널 배색 체계를 그대로 옮긴 결과다.

속성 끝의 `-`(대시)는 React 등 프레임워크 호환을 위한
설계 선택이다.

## 모노레포 구조

```txt
webtui/
├── packages/
│   ├── css/          ← 코어 라이브러리 (@webtui/css)
│   ├── plugin-nf/    ← Nerd Font 플러그인
│   ├── theme-catppuccin/
│   ├── theme-gruvbox/
│   ├── theme-nord/
│   ├── theme-vitesse/
│   └── theme-everforest/
└── web/              ← 문서 사이트 (Astro + MDX)
```

- **기술 스택**: MDX 35%, Astro 31%, CSS 29%, TS 4%
- **빌드 도구**: Bun + Turbo (모노레포 관리)
- **라이선스**: MIT
- **최신 버전**: 0.1.6 (2026-01-07)

## 코드 분석

### 속성 선택자(Attribute Selector) 패턴

WebTUI의 가장 독특한 설계는 클래스 대신 HTML 속성을
선택자로 활용하는 방식이다:

```css
/* 클래스 기반 (일반적) */
.badge { ... }
.badge--success { ... }

/* 속성 기반 (WebTUI) */
[is-~="badge"] { ... }
[variant-~="success"] { ... }
```

이 접근은 HTML이 더 의미론적(semantic)으로 읽히게 한다.
`class="badge badge--success"` 대신
`is-="badge" variant-="success"`로 의도가 명확하다.

### @layer의 실전 활용

CSS Cascade Layers(2022 도입)를 본격적으로
활용하는 몇 안 되는 라이브러리 중 하나다:

```css
@layer base {
  /* 낮은 우선순위 - 쉽게 오버라이드 가능 */
}
@layer components {
  /* 높은 우선순위 - 컴포넌트 스타일 보호 */
}
/* layer 밖 = 가장 높은 우선순위 (사용자 커스텀) */
```

사용자의 커스텀 스타일이 `@layer` 밖에 있으면
라이브러리 스타일을 자연스럽게 오버라이드할 수 있다.

### Tree-Shaking이 가능한 CSS

각 컴포넌트가 독립 파일이므로 번들러 없이도
사용하지 않는 CSS를 포함하지 않을 수 있다:

```css
/* 전체 임포트 (개발용) */
@import '@webtui/css/full.css';

/* 선택적 임포트 (프로덕션) */
@import '@webtui/css/base.css';
@import '@webtui/css/components/button.css';
/* 필요한 것만 골라서 */
```

## 유사 라이브러리 비교

| 라이브러리           | 미학          | 접근 방식       |
| -------------------- | ------------- | --------------- |
| **WebTUI**           | 모던 TUI      | 속성 기반       |
| **TuiCss**           | MS-DOS        | 클래스 기반     |
| **terminal.css**     | 미니멀 터미널 | 시맨틱 HTML     |
| **letieu/terminal**  | 사이버펑크    | Bulma 스타일    |

## 커뮤니티 반응

### 미학의 이식이 제약의 이식이기도 하다는 비판

HN 스레드에서 가장 날이 선 반응은 미학 자체를 겨눴다.
imiric은 TUI가 그렇게 생긴 이유는 만든 사람들이 그 모양을 원해서가 아니라 터미널의 태생적 제약 때문이며, 풍부한 UI를 지원하는 플랫폼에 그 디자인 언어를 가져오는 것은 할 수 있는 일을 인위적으로 줄이는 것이라고 적었다.[^imiric]
글꼴에 글리프가 없을 때 나오는 빈 사각형까지 흉내 낸다는 그의 비꼼이 이 지적의 요지를 압축한다.
그리고 멀티미디어와 풍부한 상호작용을 포기하지 않는 한 진짜 터미널과 같은 디자인이 되지도 않는다고 덧붙였다.

rollcat은 문서의 한 대목을 근거로 같은 문제를 다르게 짚었다.
`px`, `em`, `rem`, `%` 같은 표준 CSS 단위로 생각하기를 멈추고 문자 셀 단위로 간격과 크기와 위치를 생각하라는 안내다.[^rollcat]
그는 1980년대 터미널에 대한 집착을 이해하기 어렵다며, 복고 애호가인 것과 그것이 현대 CLI를 떠받칠 최고의 기술이라거나 이식 가능한 UI의 튼튼한 기반이라고 주장하는 것은 다른 문제라고 선을 그었다.

이 비판들은 이 라이브러리를 쓸지 정할 때 실제로 물어야 할 질문을 만든다.
셀 격자에 맞춘 치수 체계는 터미널 느낌을 만드는 핵심 장치이면서, 동시에 반응형 웹이 오랫동안 쌓아 온 유동적 레이아웃 기법과 어긋나는 지점이다.
그 어긋남은 스레드에서 실제로 관측됐다. lionkor는 Firefox 모바일에서 검색 필드가 셀 하나만큼 오른쪽으로 삐져나와 화면에 들어오지 않는다고 보고했다.[^lionkor]

### 흉내와 구현 사이의 간극

godelski의 반응이 이 프로젝트의 정체성에 대한 가장 유용한 질문을 던진다.
그는 자신이 원하는 것이 바로 이런 것일 수 있다고 전제하면서도, 그것처럼 보이지만 그것처럼 동작하지는 않는 느낌, 즉 겉모습만 따라간 듯한 인상이 있다고 적었다.[^godelski]
그가 바라는 것은 키 바인딩만으로 완전히 쓸 수 있는 웹 인터페이스이고, 그 기준에서 보면 이 라이브러리는 아직 시각적 층에 머문다는 것이다.

이 지적은 앞의 미학 비판과는 반대 방향에서 온다.
imiric은 터미널을 덜 흉내 내라고 말하고, godelski는 더 제대로 흉내 내라고 말한다.
공통점은 둘 다 현재 상태를 어중간하다고 본다는 것이며, 갈리는 것은 어느 쪽으로 밀어야 하느냐다.

실무적으로는 이 구분이 도입 판단의 축이 된다.
글꼴과 테두리만으로 분위기를 내려는 것이라면 CSS 층만으로 충분하고, 키보드 우선 조작까지 기대한다면 그 부분은 직접 만들어야 한다.
terminaltrove가 언급한 것처럼 WebTUI에 키보드 단축키가 있다는 점은 출발점이지만[^terminaltrove], 터미널 앱 수준의 조작 체계와는 다른 층위다.

### 실제로 어디에 쓰이는가

스레드에는 채택 동기도 드러났다.
kombine은 AI 스타트업 피칭용 페이지를 만들어야 하는데 웹 개발 경험이 거의 없다며, 터미널 미학을 좋아하기도 하고 디자인 고민의 부담을 덜고 내용에 집중할 수 있을 것 같아 TUI 같은 인터페이스를 쓰는 것이 좋은 생각인지 물었다.[^kombine]
이 질문이 이 라이브러리가 실제로 채우는 자리를 정확히 보여 준다. 디자인 결정을 하지 않아도 되게 만들어 주는 장치라는 것이다.

제약이 곧 이점이 되는 구조는 bbor의 관찰과도 이어진다.
그는 이 미학이 괴짜 취향의 블로그에서 먼저 유행할 가능성이 적지 않으며, 그런 것은 대체로 더 넓은 웹으로 번진다고 봤다.[^bbor]
실제로 같은 계열의 시도가 여럿 있다. runlaszlorun은 TuiCss를 언급했고[^runlaszlorun], terminaltrove는 Rust와 WebAssembly로 터미널풍 웹 앱을 만드는 ratzilla를 들었으며, jiehong은 IBM TN5250 터미널을 웹으로 가져오는 실험을 2년 전에 해 봤다고 밝혔다.[^jiehong]

adhamsalama의 한 줄이 이 흐름을 요약한다.
웹 기술로 실제 터미널 에뮬레이터처럼 보이는 터미널 에뮬레이터를 쉽게 만들 수 있게 됐으니, 한 바퀴를 두 번 돈 셈이라는 것이다.[^adhamsalama]

GeekNews 쪽 반응은 훨씬 짧지만 이 미학이 누구에게 닿는지를 보여 준다.
ikspres는 이것을 보는 순간 멋져 보인다고 생각한 자신이 아무래도 구시대 감각을 가진 사람인지 자문했다.[^ikspres]
이 자문 자체가 위의 논쟁이 사실은 세대와 경험의 문제임을 드러낸다.
HN에서 runlaszlorun이 80년대 터보 파스칼로 시작해서 그럴지도 모르겠다고 덧붙인 것과 같은 자리에 있는 반응이다.

## 인사이트

### 1. “의미론적 속성”이라는 새로운 패러다임

BEM(`block__element--modifier`)이나
유틸리티 클래스(`flex items-center gap-2`) 대신
HTML 속성으로 의미를 전달하는 것은 참신한 접근이다.
HTML 자체가 문서화 역할을 하게 된다.

### 2. CSS @layer의 킬러 유스케이스

`@layer`는 2022년에 모든 브라우저에서 지원됐지만
실전에서 적극 활용하는 라이브러리는 많지 않다.
WebTUI는 `@layer`가 왜 필요한지를 잘 보여주는
레퍼런스 구현이다. 라이브러리 스타일과 사용자
커스텀 스타일 간의 충돌을 구조적으로 해결한다.

### 3. “프레임워크가 아닌 레이어”라는 포지셔닝

Bootstrap, Tailwind처럼 모든 것을 제공하려 하지 않고
“터미널 미학”이라는 명확한 범위에 집중한다.
이 접근은 라이브러리가 가벼우면서도
다른 도구와 조합하기 쉽게 만든다.

### 4. 제로 JS의 가치

JavaScript 없이 순수 CSS만으로 Accordion, Dialog,
Tooltip 등 인터랙티브 컴포넌트를 구현한다.
`<details>`, `<dialog>`, `:hover` 등
네이티브 HTML/CSS 기능을 최대한 활용하는 접근이다.

### 5. 모노레포에서의 테마 분리

테마를 별도 패키지로 분리한 것은 핵심 라이브러리의
크기를 최소화하면서도 커뮤니티 테마 기여를
쉽게 만드는 좋은 패턴이다.

---

[^imiric]: <https://news.ycombinator.com/item?id=43671000>

[^rollcat]: <https://news.ycombinator.com/item?id=43670593>

[^lionkor]: <https://news.ycombinator.com/item?id=43671681>

[^godelski]: <https://news.ycombinator.com/item?id=43670410>

[^terminaltrove]: <https://news.ycombinator.com/item?id=43670452>

[^kombine]: <https://news.ycombinator.com/item?id=43670329>

[^bbor]: <https://news.ycombinator.com/item?id=43669777>

[^runlaszlorun]: <https://news.ycombinator.com/item?id=43669807>

[^jiehong]: <https://news.ycombinator.com/item?id=43673817>

[^adhamsalama]: <https://news.ycombinator.com/item?id=43671860>

[^ikspres]: <https://news.hada.io/topic?id=20320#cid37172>
