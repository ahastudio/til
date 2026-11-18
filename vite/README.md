# Vite

<https://vite.dev/>

<https://vitejs.dev/>

<https://github.com/vitejs/vite>

## 소개

Vite는 프런트엔드 빌드 도구이다. 홈페이지의 문구는 「웹을 위한 빌드 도구」이고 차세대 웹 애플리케이션을 움직이는 매우 빠른 프런트엔드 빌드 도구라고 소개한다. 이름은 프랑스어로 「빠르다」를 뜻하며 「비트」로 읽는다고 안내 문서가 적는다.
이 문서는 `vite.dev` 홈페이지, 안내(`/guide/`)와 「왜 Vite인가」 페이지, 블로그 목록, GitHub API 수치와 최신 릴리스를 읽었다. 직접 써 보지 않았고 설정, 플러그인, 팀, 릴리스, 감사 페이지와 `llms.txt`는 열지 못했다.
설명은 모두 프로젝트의 주장이다.
헤더의 `vitejs.dev`는 이전 문서와 옛 글 주소가 쓰던 도메인이다. 이 문서는 현재 `vite.dev`와의 연결(이동)을 확인하지 못했다.

GitHub API로 읽은 시점(2026년 11월 19일)의 수치는 별 83,982개, 포크 10,423개, 열린 이슈와 풀 리퀘스트 809개, 라이선스 MIT, 언어 TypeScript, 생성일 2020년 4월 21일, 마지막 푸시 2026년 11월 18일이다. 저장소의 홈페이지 필드는 `vite.dev`이다.
최신 릴리스는 v8.3.8(2026년 11월 11일)이다. 릴리스 노트는 버그 수정 여섯 건(번들 개발 모드의 인라인 워커, 네이티브 로더의 타입 전용 임포트 검사, `build.cssCodeSplit: false`일 때의 CSS 진입점, 의존성 갱신, Windows 콘솔 창과 `net use` 동작 등)과 `sass`를 파일마다가 아니라 한 번만 불러오는 성능 개선, `@types/node` 26 갱신이다. 홈페이지 내비게이션의 문서 버전은 v8.3.7이어서 릴리스보다 한 단계 늦다.
홈페이지의 주장은 별 8만 개 이상, 주간 npm 내려받기 8,000만 회 이상이다. 별 수는 API 값과 맞고 내려받기 수는 이 문서가 확인하지 못했다. 블로그 글은 Vite 8이 나온 3월에 주간 약 6,500만 회, 8.1을 낸 6월에 Vite 8만 4,160만 회라고 적는다.

## 사용법

- 새 프로젝트: `npm create vite@latest`(yarn, pnpm, bun은 `create vite`, deno는 `deno init --npm vite`)이고 프롬프트를 따른다. 템플릿을 지정할 때는 `npm create vite@latest my-vue-app -- --template vue`처럼 npm 7 이상에서 `--`가 필요하다. `--no-interactive`와 현재 디렉터리를 뜻하는 `.`도 쓸 수 있다.
- 템플릿: vanilla, vue, react, react-compiler, preact, lit, svelte, solid, qwik과 각 `-ts` 변형이다. 온라인에서는 `vite.new/{템플릿}`으로 StackBlitz에서 연다.
- React: 저장소에 React 프로젝트용 올인원 플러그인([`packages/plugin-react`](https://github.com/vitejs/vite/tree/main/packages/plugin-react))과 React 템플릿([`template-react`](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react))이 있다. 커뮤니티 자료로 Vite 기반 React 도구 모음([`fwh1990/vite-react`](https://github.com/fwh1990/vite-react))과 Vite로 React 앱을 만드는 글이 있다.[^section]
- 요구 사항: Node.js 20.19 이상 또는 22.12 이상이며 일부 템플릿은 더 높은 버전이 필요하다.
- 수동 설치: `npm install -D vite` 뒤 `npx vite`로 `http://localhost:5173`에서 개발 서버가 뜬다. 기본 스크립트는 `dev`가 `vite`, `build`가 `vite build`, `preview`가 `vite preview`이다.
- 브라우저 대상: 개발은 `esnext` 변환 대상, 프로덕션은 2026년 1월 1일 기준 「널리 쓰이는 기준선(Baseline Widely Available)」(대략 2023년 중반 브라우저)이다. 옛 브라우저는 `@vitejs/plugin-legacy`로 지원한다.
- 미공개 커밋: `pkg.pr.new`로 설치할 수 있으며 최근 한 달의 커밋만 된다.

안내 문서는 Vite가 두 부분으로 이루어진다고 설명한다. 하나는 네이티브 ESM 기반의 기능(HMR 포함)을 가진 개발 서버이고, 다른 하나는 Rolldown으로 번들해 최적화된 정적 자산을 내는 빌드 명령이다. 합리적인 기본값을 가진 「의견이 있는」 도구이며 플러그인 API와 자바스크립트 API로 확장한다.

## 기능

홈페이지의 기능 카드는 다음과 같다.

- 즉각적인 서버 시작: 소스를 네이티브 ESM으로 필요할 때 제공하고 의존성은 미리 번들한다.
- 빠른 HMR: 앱 규모와 상관없이 저장하면 반영된다.
- 기본 기능: TypeScript, JSX, CSS, 워커, WebAssembly 등을 플러그인과 함께 다룬다.
- 최적화된 빌드: 트리 셰이킹, 내장 압축, 청크 제어를 Rolldown이 맡는다.
- 유연한 플러그인: Rollup 플러그인 인터페이스를 Vite 전용 옵션으로 확장한다.
- 완전한 타입 API, 일급 SSR 지원, 생태계 CI(하위 프로젝트를 상대로 Vite 변경을 시험)이다.

「왜 Vite인가」는 큰 앱의 느린 개발 서버 시작, 느린 갱신, 긴 프로덕션 빌드에서 출발했다고 설명한다. 브라우저가 ESM을 지원하면서 의존성을 한 번 미리 번들하고 소스를 필요할 때 ESM으로 제공해 시작이 앱 크기와 상관없이 거의 즉각적이라고 한다. Snowpack, WMR, `@web/dev-server`에서 영향을 받았다고 적는다. 프로덕션은 번들하지 않는 ESM이 네트워크 왕복을 늘리므로 여전히 번들한다.
이 도구를 쓰는 곳으로 Nuxt, SvelteKit, Astro, React Router, Analog, SolidStart, Vitest, Storybook, Laravel, Ruby on Rails를 든다. 홈페이지는 OpenAI, Shopify, Stripe, Linear 등의 로고를 「세계 최고의 소프트웨어 팀이 신뢰한다」는 문구 아래 싣는다.

## 거버넌스와 흐름

홈페이지는 Vite가 MIT 라이선스이며 항상 무료 오픈소스로 남는다고 하고 VoidZero가 제공한다고 표시한다. 푸터의 저작권은 VoidZero Inc.와 Vite 기여자이다.
2026년 6월 4일 글은 VoidZero가 Cloudflare에 합류하고 VoidZero 소속 Vite 팀원이 모두 Cloudflare로 옮기지만 Vite는 오픈소스와 공급자 중립을 유지하며 100만 달러의 생태계 기금이 생긴다고 밝혔다. 이는 `vite/cloudflare-vite-support.md`에 정리했다. 홈페이지와 안내 문서에는 Cloudflare 언급이 없다.

블로그 목록은 다음과 같다.

| 날짜             | 글                                                                            |
| ---------------- | ----------------------------------------------------------------------------- |
| 2026년 11월 11일 | 최신 릴리스 v8.3.8(GitHub 릴리스)                                             |
| 2026년 6월 23일  | Vite 8.1(`vite/vite-8-1.md`)                                                  |
| 2026년 6월 4일   | Cloudflare의 지원 발표(`vite/cloudflare-vite-support.md`)                     |
| 2026년 3월 12일  | Vite 8(`vite/vite-8-0.md`)                                                    |
| 2025년 12월 3일  | Vite 8 베타(`vite/vite-8.md`)                                                 |
| 2025년 6월 24일  | Vite 7                                                                        |
| 2024년 11월 26일 | Vite 6                                                                        |
| 2024년 2월 8일   | Vite 5.1                                                                      |
| 2023년 11월 16일 | Vite 5                                                                        |
| 2023년 4월 20일  | Vite 4.3                                                                      |
| 2022년 12월 9일  | Vite 4                                                                        |
| 2022년 7월 23일  | Vite 3                                                                        |
| 2021년 2월 16일  | [Vite 2.0](https://vitejs.dev/blog/announcing-vite2.html)(`vite/vite-2-0.md`) |

가장 최근 글이 6월이고 현재 릴리스는 11월이라서 목록과 릴리스 사이에 간격이 있다. 홈페이지에는 2026년 10월 15일 온라인 ViteConf 배너가 남아 있다.
번역은 중국어 간체, 일본어, 스페인어, 한국어, 독일어 사이트가 있고 `llms.txt`로 LLM용 문서를 제공한다고 한다.

## 분석

### 중심 주장은 개발 경험과 공유 기반이다

홈페이지의 두 축은 「개발 경험의 재정의」와 「함께 쌓을 공유 기반」이다. 빠른 시작과 HMR이 앞의 것이고 프레임워크와 도구가 위에 올라타는 생태계가 뒤의 것이다.
Vite 8이 Rolldown으로 번들러를 통합한 뒤 홈페이지의 최적화 빌드 설명도 Rolldown으로 바뀌었다. 이는 사이트의 서술을 이 문서가 정리한 것이다.

### 이름이 프로젝트의 정체성을 이끈다

안내 문서는 빠름을 이름과 설계의 이유로 반복하고, 블로그 글들은 속도 수치를 중심에 둔다.
다만 최근 글(8.1)의 관심은 큰 앱의 개발 서버, 청크 캐시, CSS 변환기로 옮겨 가는 중이다. 이는 이 문서의 해석이다.

## 비평

### 수치의 근거가 약하다

홈페이지의 내려받기 수 8,000만 회 이상은 출처가 없고 블로그의 수치와 단위도 다르다(Vite 전체와 Vite 8만의 구분). 사용 기업 로고도 사용 범위를 말하지 않는다.
독립된 평가는 이 문서가 읽지 못했다. 블로그 글들의 성능 수치에 대한 비평은 각 글의 문서에 있다.

### 문서 사이트가 스스로 어긋난다

내비게이션의 문서 버전이 릴리스보다 늦고 지난 행사 배너가 남아 있다. 작은 일이지만 사이트가 갱신되는 속도를 보여 준다.

### 소유 구조의 변화가 홈페이지에는 보이지 않는다

VoidZero와 Cloudflare의 관계는 블로그 글에 있고 홈페이지는 VoidZero가 제공한다고만 표시한다.
중립 약속의 이행은 앞으로 지켜볼 일이다.

### 외부 반응

Lobste.rs의 `vitejs.dev`와 `vite.dev` 도메인에는 홈페이지가 아니라 각각 Vite 4와 Vite 8.0 블로그 글뿐이다.
GeekNews에는 Vite 8.0 출시와 Vite+, VoidZero 합류 토픽이 있으나 홈페이지를 원문으로 삼은 것은 확인하지 못했다.
HN에서 홈페이지 주소로 올라온 글은 `main.vitejs.dev`로 2022년에 올라온 글이며 지금의 평가가 아니다.

## 인사이트

### 가져갈 것은 Vite를 도입하는 순서이다

새 프로젝트는 템플릿으로 시작하고, 기존 프로젝트는 Node 버전과 플러그인 호환부터 확인한다. 번들 개발 모드 같은 실험 기능은 별도 브랜치에서 시험한다. 이는 이 문서의 적용이다.

### 도구의 소유 구조를 함께 본다

Vite를 중심으로 Rolldown, Oxc, Vitest, Vite+가 한 회사의 소유가 되었다. 이 도구들에 의존하는 팀은 릴리스 노트와 거버넌스 글을 함께 추적한다.

### 함께 읽을 문서

- `vite/vite-2-0.md`, `vite/vite-8-0.md`, `vite/vite-8-1.md`, `vite/vite-8.md`(베타): 릴리스 글
- `vite/cloudflare-vite-support.md`: VoidZero의 Cloudflare 합류와 기금
- [Vinext](../vinext): Vite 위에 Next.js API를 재구현한 프로젝트
- 예제: [Vite 설정 예제 모음](https://j.mp/3AoIY5B)(`ahastudio/CodingLife`의 `20211009/vite`)

### 확인할 관찰

이 프로젝트의 주장을 가를 관찰은 세 가지이다.
Vite 7과 8을 같은 프로젝트에서 비교한 빌드 시간과 산출물 크기,
Environment API의 안정화(Vite 9 목표)와 번들 개발 모드의 승격,
소유 변경 뒤의 중립 약속 이행이다.
셋 모두 이 문서가 확인하지 못했다.

[^section]: [Creating a React.js App using Vite | Section](https://www.section.io/engineering-education/creating-a-react-app-using-vite/)
