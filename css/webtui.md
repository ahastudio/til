# WebTUI

> Modular CSS Library that brings the beauty of
> Terminal UIs to the browser.

<https://webtui.ironclad.sh/>

<https://github.com/webtui/webtui>

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
  Catppuccin, Gruvbox, Nord, Vitesse, Everforest

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

개별 임포트 가능한 19개 컴포넌트:
Accordion, Badge, Button, Checkbox, Dialog, Input,
Popover, Pre, Progress, Radio, Range, Separator,
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
|----------------------|---------------|-----------------|
| **WebTUI**           | 모던 TUI      | 속성 기반       |
| **TuiCss**           | MS-DOS        | 클래스 기반     |
| **terminal.css**     | 미니멀 터미널 | 시맨틱 HTML     |
| **letieu/terminal**  | 사이버펑크    | Bulma 스타일    |

## 인사이트

### 1. "의미론적 속성"이라는 새로운 패러다임

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

### 3. "프레임워크가 아닌 레이어"라는 포지셔닝

Bootstrap, Tailwind처럼 모든 것을 제공하려 하지 않고
"터미널 미학"이라는 명확한 범위에 집중한다.
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
