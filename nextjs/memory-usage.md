# Next.js 메모리 사용량 최적화

원문: [How to optimize memory usage](https://nextjs.org/docs/app/guides/memory-usage)

## 요약

Next.js 공식 문서의 가이드이다(문서의 마지막 갱신 표시는 2026년 4월 28일).
앱이 커지면 로컬 개발과 프로덕션 빌드에서 더 많은 자원이 필요하다는 데서 출발해, 메모리를 줄이고 흔한 문제를 해결하는 방법을 모은다.

## 줄이는 방법

- 의존성 줄이기: 의존성이 많은 앱은 메모리를 더 쓴다. 번들 분석기로 큰 의존성을 찾아 뺀다.
- `experimental.webpackMemoryOptimizations`: v15.0.0부터 `next.config.js`에 `true`를 두면 webpack의 최대 메모리 사용량이 줄고 컴파일 시간이 조금 늘 수 있다. 실험 표시이나 위험이 낮다고 본다.
- Webpack 빌드 워커: webpack 컴파일을 별도 Node.js 워커에서 돌려 빌드 메모리를 줄인다. v14.1.0부터 커스텀 webpack 설정이 없으면 기본으로 켜지고, 그 밖에는 `experimental.webpackBuildWorker: true`로 켠다. 일부 커스텀 플러그인과 호환되지 않을 수 있다.
- Webpack 캐시 끄기: 캐시는 모듈을 메모리나 디스크에 저장해 빌드를 빠르게 하는 대신 메모리를 더 쓴다. 커스텀 webpack 설정에서 `dev`가 아닐 때 `config.cache`를 `{ type: 'memory' }`로 고정해 끈다.
- 정적 분석 끄기: 큰 프로젝트에서 타입 검사가 메모리를 많이 쓴다. 빌드의 「Running TypeScript」 단계에서 메모리 부족이 나면 `typescript.ignoreBuildErrors: true`로 끌 수 있다. 가이드는 타입 오류로 잘못된 배포가 될 수 있어 정적 분석이 끝난 뒤에만 프로덕션으로 승격하라고 강하게 권고한다(Vercel은 스테이징 배포 가이드).
- 소스맵 끄기: `productionBrowserSourceMaps: false`와 `experimental.serverSourceMaps: false`를 둔다. 프리렌더 단계(「Generating static pages」 이후)에서도 문제가 지속되면 `enablePrerenderSourceMaps: false`를 둔다. 일부 플러그인이 소스맵을 켤 수 있다.
- Edge 메모리: v14.1.3에서 Edge 런타임의 메모리 문제가 고쳐졌으니 그 이상으로 올린다.
- 엔트리 미리 로드: 서버가 시작할 때 각 페이지의 JavaScript 모듈을 메모리에 미리 올려 응답을 빠르게 하는 대신 처음 메모리 사용이 크다. `experimental.preloadEntriesOnStart: false`로 끌 수 있으나, Next.js는 모듈을 내리지 않아 모든 페이지가 결국 요청되면 메모리 사용은 같아진다.

## 원인을 찾는 방법

- `next build --experimental-debug-memory-usage`: v14.2.0부터 빌드 중에 힙 사용량과 GC 통계를 계속 출력하고, 메모리가 설정된 한도에 가까워지면 힙 스냅샷을 자동으로 찍는다. webpack 빌드 워커와 호환되지 않는다(워커는 커스텀 webpack 설정이 없으면 자동으로 켜짐).
- 힙 프로파일: `node --heap-prof node_modules/next/dist/bin/next build`를 실행하면 끝에 `.heapprofile` 파일이 생기고, Chrome DevTools의 Memory 탭에서 「Load Profile」로 연다.
- 힙 스냅샷: `NODE_OPTIONS=--inspect next build`로 인스펙터를 열고 Chrome DevTools를 연결해 유지된 메모리를 본다. 시작 전에 멈추려면 `--inspect-brk`를 쓴다. 디버그 메모리 모드에서는 프로세스에 `SIGUSR2`를 보내 언제든 스냅샷을 찍고, 스냅샷은 프로젝트 루트에 저장된다.

## 비평

### 수치와 기준이 없다

가이드는 어느 방법이 얼마나 메모리를 줄이는지 수치를 주지 않는다.
버전 번호(14.1.0, 14.1.3, 14.2.0, 15.0.0) 외의 한도나 임계값도 없다. 이 문서는 각 옵션을 직접 시험하지 못했다.

### 줄이는 방법의 대가가 서로 다르다

타입 검사를 끄는 방법은 잘못된 배포의 위험을 낳고, 프리로드를 끄는 방법은 모든 페이지가 요청되면 효과가 없다고 가이드가 스스로 적는다.
webpack 캐시를 끄면 빌드가 느려질 것이지만 얼마나인지는 쓰여 있지 않다.
어떤 순서로 시도해야 하는지도 안내가 없다.

### webpack 중심이다

옵션 대부분이 webpack 설정이다. 최근 Next.js가 Turbopack을 쓰는 경우의 메모리 대처는 이 가이드에서 읽을 수 없다.
이 문서는 이 점을 다른 자료로 확인하지 못했다.

### 외부 반응

HN에는 이 문서 주소로 올라온 글이 없었다(대조 쿼리는 정상이었다).
Lobste.rs의 `nextjs.org` 도메인에는 3건(CVE-2025-29927, Layouts RFC, Next.js 10)이 있고 이 문서는 없다.
GeekNews에서는 `Next.js 메모리 사용량` 등 세 가지 표현으로 검색했고 대조 쿼리는 정상이었으나 이 문서의 토픽은 없었다. 결과는 Bun, Scriptc, tsrs 같은 다른 글이었다.

## 기억할 원칙

- 메모리 문제는 먼저 원인(힙 프로파일, 스냅샷)을 보고 줄이는 옵션을 고른다.
- 옵션마다 대가가 있다. 타입 검사를 끌 때는 CI에서 따로 검사한다.
- 빌드와 서버 시작은 메모리 사용 지점이 다르다. 프리로드는 시작 비용이고 빌드 워커는 빌드 비용이다.
