# 바이브코딩 UI/UX 디자인 스킬

출처:
<https://twitter.com/0ooooo0/status/2023279976728912357>

AI 바이브코딩을 하면 보라색 그라데이션 중심의
천편일률적인 "AI스러운" 디자인이 나오기 쉽다.
아래 스킬들을 추가하면 디자인 품질이 크게 개선된다.

## ui-ux-pro-max-skill

→ [상세 문서](./ui-ux-pro-max.md)

<https://github.com/nextlevelbuilder/ui-ux-pro-max-skill>

프로페셔널 수준의 UI/UX 디자인을 이해하고
추천할 수 있게 해주는 디자인 AI 스킬.

주요 기능:

- 67개 UI 스타일
  (Glassmorphism, Neumorphism, Brutalism, Bento 등)
- 96개 산업별 색상 팔레트
- 57개 Google Fonts 조합
- 100개 산업별 추론 규칙
- 99개 UX 가이드라인

React, Next.js, Vue, SwiftUI, Flutter,
HTML+Tailwind 등 13개 이상의 기술 스택을 지원한다.

```bash
npx skills add \
  nextlevelbuilder/ui-ux-pro-max-skill
```

## frontend-design

<https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design>

Anthropic이 공식 제공하는 Claude Code 플러그인.
전문적인 프론트엔드 UI를 만들도록 돕는
디자인 가이드 스킬이다.
AI가 만드는 밋밋한 UI가 아니라
독창적이고 고급스러운 웹 UI를 생성하게 해준다.

```bash
npx skills add anthropics/claude-code/plugins\
/frontend-design/skills/frontend-design
```

## web-design-guidelines

<https://github.com/vercel-labs/agent-skills>

Vercel Labs에서 제공하는 최신 웹 디자인 지침 스킬.
100개 이상의 규칙으로 UI 코드를 검토한다.

주요 검토 영역:

- 접근성(Accessibility): ARIA, 시맨틱 HTML,
  키보드 내비게이션
- 폼 디자인: 자동완성, 유효성 검사, 에러 처리
- 애니메이션: 사용자 선호 존중, GPU 최적화
- 타이포그래피: 인용부호, 숫자 포맷
- 이미지 최적화: 지연 로딩, alt 텍스트
- 다크 모드, 터치 인터랙션, 국제화

```bash
npx -y degit \
  vercel-labs/agent-skills/web-design-guidelines \
  .agents/skills/web-design-guidelines
```

## 팁

디자인할 때 레퍼런스 사이트를 함께 제시하면
결과물의 퀄리티가 더 올라간다.

## 관련 문서

- [Vibe Coding](./vibe-coding.md)
- [Claude Code](../claude/claude-code.md)
