# FlowBite - Open-source component library built with Tailwind CSS

<https://flowbite.com/>

<https://github.com/themesberg/flowbite>

## 개요

Flowbite는 Tailwind CSS 유틸리티 클래스 위에 구축된
오픈소스 UI 컴포넌트 라이브러리다.
30개 이상의 컴포넌트를 제공하며, MIT 라이선스로 배포된다.
GitHub 스타 9.2k 이상, Discord 커뮤니티 90만 명 이상의 규모를 가지고 있다.

## 주요 컴포넌트

| 분류           | 컴포넌트                                          |
| -------------- | ------------------------------------------------- |
| 레이아웃       | Navbar, Breadcrumb, Sidebar                       |
| 폼             | Input, Checkbox, Radio, Toggle, Date Picker       |
| 인터랙티브     | Modal, Dropdown, Tab, Accordion, Tooltip          |
| 데이터 표시    | Table, Pagination, Progress Bar, Timeline         |
| 피드백         | Toast, Alert, Spinner                             |
| 기타           | Badge, Button, Card, Typography                   |

## 기술적 특징

### Data Attribute 기반 동작

JavaScript 없이 HTML data attribute만으로 컴포넌트를 제어할 수 있다.

```html
<button data-modal-target="myModal" data-modal-toggle="myModal">
  Open Modal
</button>
```

`data-modal-target`, `data-modal-toggle`, `data-dropdown-toggle` 등
컴포넌트별 data attribute를 제공한다.

### JavaScript API

프로그래밍 방식의 제어도 가능하다.
TypeScript 타입 정의를 포함한다.

```javascript
import { Modal } from 'flowbite'
const modal = new Modal($element, options)
modal.show()
```

`initFlowbite()`, `initModals()` 등의 초기화 함수로
data attribute에 이벤트 리스너를 자동 연결한다.

### 테마

CSS import로 테마를 선택할 수 있다.
Default, Minimal, Enterprise, Playful, Mono 테마가 제공된다.
RTL(Right-to-Left) 지원이 내장되어 있다.

## 설치

### npm

```bash
npm install flowbite
```

CSS에 테마 변수를 import하고 Tailwind 플러그인을 등록해야 한다.

### CDN

jsDelivr CDN으로 빌드 도구 없이 빠르게 사용할 수 있다.

## 프레임워크 통합

### 프론트엔드

전용 라이브러리가 있는 프레임워크:

- React (Flowbite React)
- Vue (Flowbite Vue)
- Svelte (Flowbite Svelte)
- Angular (Flowbite Angular)
- Qwik (Flowbite Qwik)

셋업 가이드가 있는 메타 프레임워크:
Next.js, Remix, Nuxt, Astro, Gatsby, SolidJS, MeteorJS

### 백엔드

Laravel, Symfony, Ruby on Rails, Phoenix(Elixir), Django, Flask

## 생태계

- **Flowbite Blocks:** 마케팅, 애플리케이션 UI 등 사전 구성된 페이지 섹션
- **Flowbite Icons:** 아이콘 라이브러리
- **Flowbite Figma:** 디자인 시스템
- **Flowbite Pro:** 프리미엄 컴포넌트 및 템플릿
