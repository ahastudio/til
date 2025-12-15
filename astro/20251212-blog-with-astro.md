# Astro로 블로그 시작하기

Astro는 콘텐츠 중심의 정적 사이트 생성 프레임워크입니다.
Markdown으로 글을 작성할 수 있고,
빠르게 검색 엔진에 최적화된 블로그를 만들 수 있습니다.

## 프로젝트 생성

Node.js이 설치되어 있다면, npm으로 Astro 프로젝트를 만들 수 있습니다.

```bash
npm create astro@latest my-blog -- --template blog --install --git
```

- `--template blog`: 블로그 템플릿으로 프로젝트를 생성합니다.
- `--install`: 의존성을 자동으로 설치합니다.
- `--git`: Git 저장소를 초기화합니다.

프로젝트 디렉터리로 이동해서 개발 서버를 시작합니다.

```bash
cd my-blog

npm run dev
```

<http://localhost:4321/>에 접속해서 잘 동작하는지 확인합니다.

## 블로그 글 작성

블로그 템플릿으로 생성했기 때문에
이미 몇 개의 샘플 글이 포함되어 있습니다.

`src/pages/posts/` 디렉터리를 만들고, 여기에 블로그 글을 추가합니다.

```bash
mkdir -p src/pages/posts
```

`src/content/blog/first-post.md` 파일을 열고, 다음과 같이 수정합니다.

```md
---
title: 첫 번째 글
pubDate: 2025-12-12
description: Astro로 블로그를 시작하는 방법에 대한 안내 글입니다.
author: 홍길동
---

안녕하세요.

이 글은 Astro로 블로그를 시작하는 방법에 대한 안내 글입니다.

Astro는 정적 사이트 생성기로,
빠르고 SEO에 최적화된 블로그를 쉽게 만들 수 있습니다.

더 많은 정보를 원하시면
[Astro 공식 문서](https://docs.astro.build/)를 참고하세요.
```

<http://localhost:4321/blog/first-post/>에 접속해서
블로그 첫 글이 잘 보이는지 확인합니다.

## 정적 사이트 빌드

블로그를 배포하려면 정적 사이트로 빌드해야 합니다.

```bash
npm run build
```

빌드가 완료되면 `dist/` 디렉터리에 정적 파일이 생성됩니다.

간단히 Preview 기능으로 빌드된 사이트를 확인할 수 있습니다.

```bash
npm run preview
```

<http://localhost:4321/>에 접속해서 빌드가 잘 되었는지 확인합니다.

`http-server` 같은 정적 파일 서버로도 직접 확인할 수 있습니다.

```bash
npx npx http-server dist
```

<http://localhost:8080/>에 접속해서 확인합니다.

## 결론

GitHub Pages 등 무료로 정적 사이트를 호스팅할 수 있는 서비스가 많습니다.
Astro 등을 사용하면 이런 무료 호스팅 서비스에 배포할 수 있는
블로그를 쉽고 빠르게 만들 수 있습니다.

GitHub의 Pull Request 기능과 GitHub Actions를 활용하면
팀 블로그를 위한 협업 환경과 자동 배포 환경도 쉽게 구축할 수 있습니다.

Astro를 활용해서 개발자를 위한 팀 블로그를 만들어 봅시다!
