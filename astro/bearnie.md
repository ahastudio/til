# Bearnie

Astro와 Tailwind CSS를 위한 접근성 있는 컴포넌트 라이브러리입니다.
shadcn/ui처럼 컴포넌트를 프로젝트에 복사하는 방식으로 동작하며,
의존성 없이 코드를 직접 소유하고 제어할 수 있습니다.

<https://bearnie.dev/>

<https://github.com/michael-andreuzza/bearnie>

## 특징

- Astro + Tailwind CSS 전용 컴포넌트
- 접근성(Accessibility) 고려
- 라이트/다크 모드 지원
- CLI로 컴포넌트를 프로젝트에 복사
- 의존성 없음, 락인 없음
- 완전한 커스터마이징 가능
- MIT 라이선스

## 시작하기

프로젝트를 초기화합니다.

```bash
npx bearnie init
```

npm 외에 다른 패키지 매니저도 사용할 수 있습니다.

```bash
bunx bearnie init
pnpm dlx bearnie init
yarn dlx bearnie init
```

## 컴포넌트 추가

CLI로 원하는 컴포넌트를 추가합니다.

```bash
npx bearnie add aspect-ratio
```

추가된 컴포넌트는 프로젝트 내에서 직접 import하여 사용합니다.

```astro
---
import { AspectRatio } from "@/components/bearnie/aspect-ratio";
---

<AspectRatio ratio={16 / 9}>
  <img src="image.jpg" alt="예시 이미지" />
</AspectRatio>
```

## shadcn/ui와의 비교

shadcn/ui가 React(Next.js) 생태계에서 컴포넌트를 복사하는 방식을
대중화했다면, Bearnie는 같은 접근 방식을 Astro 생태계에 적용한
프로젝트입니다. 별도의 npm 패키지로 설치하는 것이 아니라 CLI를
통해 소스 코드를 프로젝트에 직접 복사하므로, 원하는 대로 수정하고
확장할 수 있습니다.
