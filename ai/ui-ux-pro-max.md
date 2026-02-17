# UI/UX Pro Max

AI 코딩 어시스턴트에 디자인 인텔리전스를 부여하는
오픈소스 AI 스킬.
UI 스타일, 색상, 타이포그래피, UX 가이드라인 등
검색 가능한 데이터베이스를 제공해서
AI가 프로페셔널 수준의 UI/UX를 만들 수 있게 한다.

<https://uupm.cc/>

<https://github.com/nextlevelbuilder/ui-ux-pro-max-skill>

## 리소스 규모

| 항목                       | 수량 |
|----------------------------|------|
| UI 스타일                  | 67   |
| 산업별 색상 팔레트         | 96   |
| Google Fonts 조합          | 57   |
| 차트 타입                  | 25   |
| UX 가이드라인              | 99   |
| 산업별 추론 규칙 (v2.0)   | 100  |
| 지원 기술 스택             | 13+  |

## Design System Generator (v2.0)

v2.0의 핵심 기능.
프로젝트 요구사항을 분석해 맞춤형 디자인 시스템을
자동 생성하는 AI 추론 엔진이다.

동작 과정:

1. 5개 병렬 검색으로 제품 유형, 스타일, 색상,
   패턴, 타이포그래피를 탐색한다.
2. BM25 랭킹과 안티패턴 필터링으로 추론한다.
3. 패턴, 스타일, 색상, 타이포그래피, 효과,
   안티패턴, 사전 전달 체크리스트를 출력한다.

SaaS, Fintech, Healthcare, E-commerce 등
100개 이상의 산업 카테고리를 지원한다.

## 지원 기술 스택

- 웹: HTML+Tailwind, React, Next.js, Astro,
  Vue, Nuxt.js, Svelte, shadcn/ui
- 모바일: SwiftUI, Jetpack Compose,
  React Native, Flutter

## 지원 AI 어시스턴트

Skill 모드(자동 활성화):
Claude Code, Cursor, Windsurf, Codex CLI,
Gemini CLI, Continue, OpenCode 등

Workflow 모드(슬래시 커맨드):
Kiro, GitHub Copilot, Roo Code

## 설치

CLI(권장):

```bash
npm install -g uipro-cli
uipro init --ai claude
```

npx:

```bash
npx skills add \
  nextlevelbuilder/ui-ux-pro-max-skill
```

## 디자인 시스템 유지

세션 간 일관성을 위해 계층 구조를 만든다:

- `design-system/MASTER.md` — 글로벌 기준
- `design-system/pages/[page].md` — 페이지별 오버라이드

페이지 파일이 있으면 해당 규칙이 우선 적용되고,
없으면 마스터 규칙만 적용된다.

## 관련 문서

- [바이브코딩 UI/UX 디자인 스킬](./ui-ux-skills.md)
- [Direct Design](../design/direct-design.md)
