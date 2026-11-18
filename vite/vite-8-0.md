# Vite 8.0 정식 출시

원문: [Vite 8.0 is out!](https://vite.dev/blog/announcing-vite8)

HN 토론: <https://news.ycombinator.com/item?id=47360730> (560점, 202개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/gpbzcn/vite_8_0_is_out> (20점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=27485>

## 요약

2026년 3월 12일 Vite 공식 블로그에 실린 Vite 8의 정식 출시 글이다. 저자 표기는 없고 Vite 팀의 글이며, 감사 절은 이번 릴리스를 sapphi-red와 Vite 팀이 이끌었다고 적는다. 이 저장소의 `vite/vite-8.md`는 같은 릴리스의 베타 글(2025년 12월)을 다룬다.

글의 내용은 다음과 같다.

- 핵심 변화: Vite는 개발에 esbuild를, 프로덕션에 Rollup을 썼고 두 파이프라인이 접착 코드를 필요로 하며 서로 어긋났다. Vite 8은 Rust 기반 번들러 Rolldown 하나로 이를 통합한다. 글은 이를 Vite 2 이후 가장 큰 구조 변화라고 부르고 「최대 10에서 30배 빠른 빌드」와 전체 플러그인 호환을 내세운다. Vite는 주당 약 6,500만 번 내려받는다고 하며, Vite, Rolldown, Oxc 플러그인 디렉터리 `registry.vite.dev`도 열었다.
- Rolldown의 목표: 성능(Rollup보다 10에서 30배 빠르고 esbuild 수준), 호환성(Rollup과 Vite와 같은 플러그인 API, 대부분의 플러그인이 동작), 고급 기능(전체 번들 모드, 유연한 청크 분할, 모듈 단위 지속 캐시, Module Federation 지원)이다.
- 안정화 과정: 별도 패키지 `rolldown-vite`가 기술 미리 보기였고 주요 플러그인과 프레임워크를 검증하는 CI 묶음이 있었다. 2025년 12월 베타가 나왔고 그 사이 Rolldown이 베타에서 릴리스 후보가 되었다. SvelteKit, React Router, Storybook, Astro, Nuxt 등이 일찍 시험했다고 감사한다.
- 실제 빌드 시간(미리 보기와 베타 기준): Linear는 46초에서 6초, Ramp는 57% 감소, Mercedes-Benz.io는 최대 38% 감소, Beehiiv는 64% 감소이다. 큰 프로젝트에서 효과가 더 크다고 한다.
- 통합 도구 체인: Vite(빌드 도구), Rolldown(번들러), Oxc(컴파일러)이며 Oxc의 의미 분석이 Rolldown의 트리 셰이킹을 개선한다.
- 요구 사항: Node.js 20.19 이상 또는 22.12 이상(Vite 7과 같음)이고 `require(esm)`을 플래그 없이 지원해 Vite는 ESM 전용으로 배포된다.
- 추가 기능: 통합 개발 도구(`devtools` 옵션), 내장 tsconfig 경로(`resolve.tsconfigPaths: true`, 성능 비용이 작아 기본 꺼짐), `emitDecoratorMetadata` 내장 지원, SSR의 `.wasm?init` 지원, 코딩 에이전트를 감지하면 자동으로 켜지는 브라우저 콘솔 전달(`server.forwardConsole`)이다.
- `@vitejs/plugin-react` v6: React Refresh 변환에 Oxc를 쓰고 Babel 의존성이 사라져 설치 크기가 작다. React Compiler는 `reactCompilerPreset` 도우미와 `@rolldown/plugin-babel`을 쓴다. v5도 Vite 8에서 동작한다.
- 설치 크기: Vite 7보다 약 15MB 크다. 약 10MB는 `lightningcss`가 선택적 피어에서 일반 의존성이 되어서이고 약 5MB는 Rolldown 바이너리이다.
- 이전: 호환 계층이 기존 `esbuild`와 `rollupOptions` 설정을 Rolldown과 Oxc의 대응 설정으로 자동 변환해 많은 프로젝트가 설정을 바꿀 필요가 없다. 큰 프로젝트에는 Vite 7에서 `rolldown-vite`로 먼저 옮긴 뒤 Vite 8로 올리는 두 단계를 권한다. 이전 안내와 변경 기록 링크가 있다.
- 앞으로: 전체 번들 모드(실험, 개발 서버 시작 3배, 전체 새로 고침 40% 빠름, 네트워크 요청 10배 감소), 자바스크립트 플러그인을 위한 원시 AST 전달, 네이티브 MagicString 변환, Environment API 안정화이다.

## 분석

### 중심 주장은 하나의 번들러가 두 환경의 어긋남을 없앤다는 것이다

글의 설득은 속도보다 구조에 있다. 개발과 프로덕션이 다른 도구라서 생기던 불일치와 접착 코드를 한 도구로 없앤다는 것이다.
속도 수치는 그 결과로 제시된다. 이는 글의 서술을 이 문서가 정리한 것이다.

### 점진적 이행으로 위험을 낮춘 릴리스이다

미리 보기 패키지, 플러그인과 프레임워크 검증 CI, 베타, 호환 계층, 두 단계 이전 경로가 겹겹이 있다.
HN에서 한 사용자는 `rolldown-vite`를 3에서 4개월 써 온 큰 모노레포에서 개발 서버 시간이 8초에서 1.5초로, 빌드가 2분 30초에서 35초로 줄었다고 했다.[^h4ch1]
이는 이 점진적 이행이 실제로 작동한 한 사례이다. 사용자의 서술이며 이 문서가 확인하지 못했다.

### 도구 체인 소유 구조를 드러낸다

Vite, Rolldown, Oxc를 같은 팀이 맡는 통합 체인이 되었다. 글은 이를 하나의 장점으로 말한다.
뒤에 올라온 VoidZero의 Cloudflare 합류 글(`vite/cloudflare-vite-support.md`)이 이 체인의 소유 구조를 설명한다.

## 비평

### 수치는 미리 보기 시점의 고객 보고이다

10에서 30배라는 수치는 Rollup과의 벤치마크이고 고객 수치는 `rolldown-vite` 미리 보기와 베타에서의 값이다.
조건과 비교 대상(어떤 프로젝트가 어떤 플러그인 구성인지)은 글에 없다. HN에는 큰 개선(4분에서 30초, 10초에서 1초)을 보고한 사용자와 그 수치에 놀란 질문이 같이 있었다.[^johnfn][^griffinsauce]

### 번들 크기가 커졌다는 반론이 있다

HN에서 한 사용자는 Vite 8에서 빌드 파일 크기가 두 배가 되었다는 이슈를 링크하며 빌드 속도 이득이 이 정도 크기 증가를 정당화하지 못한다고 했다.[^repulsio]
글은 설치 크기(15MB 증가)는 밝히지만 산출물 크기에 대해서는 말하지 않는다. 이 문서는 해당 이슈를 열지 못했다.

### 장기 안정성에 대한 회의가 있다

한 사용자는 10년 뒤에도 돌아가야 하는 프로젝트라서 래퍼가 바뀔 때마다 작업이 생기는 Vite 대신 esbuild를 직접 쓴다고 했고,[^aldipower] 다른 사용자는 esbuild만이 몇 년 뒤에도 깨지지 않은 도구라고 했다.[^emadda]
호환 계층이 이 걱정을 줄인다고 글은 말하지만 장기 호환 약속은 글에 없다.

### 이전 중 만나는 세부 문제가 남는다

한 사용자는 `.js` 파일을 JSX로 해석하는 Vite 7 설정이 Vite 8의 Oxc에서 다르게 동작해 토론 글의 해법을 찾아야 했다고 했다.[^vite-throwaway]
자동 변환이 모든 설정을 덮는지는 이 글에서 확인되지 않는다.

### 외부 반응

HN에서는 속도와 단순해진 설정에 대한 호평이 많았다.[^karel] 일부는 Next.js와 Vercel을 대비해 평했다. 한 사용자는 특정 프레임워크에 묶이지 않은 오픈소스 스택이라는 점을 반겼고,[^moretti] 다른 사용자는 Next.js가 이 성과의 이득을 얻지 못할 것이라고 했으며,[^soulchild77] 이에 한 사용자는 Vercel이 Turbopack을 오랫동안 미리 보기로 두었고 2022년의 벤치마크도 문제가 있었다고 반박했다.[^gherkinnn] 이는 개인 의견이다.
한 기여자는 이번 버전에 들어간 SSR의 Wasm 지원을 자신이 기여했고 팀이 배우고 기여하도록 도왔다고 적었다.[^upsuper]
GeekNews 토픽에는 이용자 댓글이 있다. 한 이용자는 JS는 원래 빌드가 필요 없던 언어인데 빌드 도구의 존재 자체가 잘못된 방향 같다고 했고,[^aer0700] 다른 이용자는 웹앱이 고도화되며 생긴 자연스러운 현상이라고 답했다.[^ahiou]
Lobste.rs 글은 댓글이 없다.

## 인사이트

### 가져갈 것은 큰 전환을 미리 보기와 호환 계층으로 나누는 방식이다

별도 패키지로 먼저 배포하고 생태계 CI로 검증하고 베타를 거치고 자동 변환을 제공하는 순서는 인프라 도구를 바꿀 때의 모범으로 읽힌다. 이는 이 문서의 적용이다.

### 업그레이드 전에 산출물 크기와 플러그인을 확인한다

빌드 시간만이 아니라 산출물 크기, 사용 중인 플러그인과 오래된 설정(esbuild 옵션)을 비교한 뒤 올린다. 큰 프로젝트는 글의 두 단계 경로를 따른다.

### 확인할 관찰

이 글의 주장을 가를 관찰은 세 가지이다.
같은 프로젝트에서 Vite 7과 8의 빌드 시간과 산출물 크기 비교,
호환 계층이 변환하지 못하는 설정의 비율,
전체 번들 모드와 Environment API의 안정화 시점이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^h4ch1]: <https://news.ycombinator.com/item?id=47362454>

[^johnfn]: <https://news.ycombinator.com/item?id=47361089>

[^griffinsauce]: <https://news.ycombinator.com/item?id=47361744>

[^repulsio]: <https://news.ycombinator.com/item?id=47435723>

[^aldipower]: <https://news.ycombinator.com/item?id=47362955>

[^emadda]: <https://news.ycombinator.com/item?id=47363750>

[^vite-throwaway]: <https://news.ycombinator.com/item?id=47364563>

[^karel]: <https://news.ycombinator.com/item?id=47361864>

[^moretti]: <https://news.ycombinator.com/item?id=47362201>

[^upsuper]: <https://news.ycombinator.com/item?id=47365877>

[^aer0700]: <https://news.hada.io/topic?id=27485#cid52998>

[^ahiou]: <https://news.hada.io/topic?id=27485#cid53043>

[^soulchild77]: <https://news.ycombinator.com/item?id=47361369>

[^gherkinnn]: <https://news.ycombinator.com/item?id=47361658>
