# Vinext: Next.js API를 Vite로 재구현

<https://vinext.dev/>

<https://github.com/cloudflare/vinext>

<https://vinext.io/>

HN 토론: <https://news.ycombinator.com/item?id=47149811> (17점, 2개 댓글)

GN 토론: <https://news.hada.io/topic?id=26997>

## 소개

Vinext는 Next.js의 공개 API 표면을 Vite 위에 처음부터 다시 구현한 Vite 플러그인이다. 저장소 설명은 Next.js API 표면을 다시 구현해 어디든 배포하게 하는 Vite 플러그인이라고 적고, README는 Cloudflare Workers를 주 배포 대상으로 삼아 Vite 위에서 Next.js 앱을 돌린다고 한다.
`app/`, `pages/`, `next.config.js`를 그대로 두고 도구 체인만 바꾸는 것이 약속이다. Next.js의 포크가 아니고 `next build` 출력을 감싸는 방식도 아니다.
이 문서는 `vinext.dev`의 홈페이지, 문서 첫 페이지, 호환성과 벤치마크 대시보드, 블로그 목록과 1.2 글, 저장소 README 전문과 SECURITY 문서, GitHub API 수치와 최근 릴리스 다섯 개, `vinext.io` 홈페이지를 읽었다. 직접 설치해 써 보지 않았고 문서 사이트의 하위 페이지(설치, 이전, OpenNext에서 이전, 캐싱, 추적, 차이점), 블로그 1.0과 1.1과 1.3과 1.4 본문, 대시보드의 개별 테스트 목록은 열지 못했다.
설명은 모두 프로젝트의 주장이다.

세 주소의 관계는 다음과 같다.

- `vinext.dev`: 프로젝트 자신의 문서와 블로그 사이트이다. 푸터가 Cloudflare의 오픈소스 프로젝트라고 적고 저장소의 홈페이지 필드도 이 주소이다. 소유를 이 문서가 독립적으로 확인하지는 못했다.
- `github.com/cloudflare/vinext`: 저장소이다.
- `vinext.io`: 스스로 독립 공동체 사이트라고 밝힌다. Cloudflare와 제휴하거나 보증받거나 관리받지 않는다고 적고 푸터에 「공동체가 관리하는 사이트」「실험적」이 있다. 수치는 출시 때(2026년 2월)의 값 그대로이다.

GitHub API로 읽은 시점(2026년 11월 19일)의 저장소 수치는 별 9,382개, 포크 480개, 열린 이슈와 풀 리퀘스트 733개, 라이선스 MIT, 언어 TypeScript, 생성일 2026년 2월 24일, 마지막 푸시 2026년 11월 18일이다. 최신 릴리스는 `vinext@1.4.6`, `@vinext/cloudflare@1.4.0`, `@cloudflare/workers-response-store@1.2.0`(모두 2026년 11월 16일)이다. 릴리스는 패키지마다 따로 나온다.

## 사용법

### 새 프로젝트와 이전

- 새 프로젝트: `pnpm create vinext-app@latest my-app`
- 기존 Next.js 프로젝트 이전: `npx vinext init`
- 호환성만 점검: `npx vinext check`
- AI 에이전트에게 맡기기: `npx skills add cloudflare/vinext`를 설치한 뒤 에이전트에게 이 프로젝트를 이전하라고 말한다(Claude Code, OpenCode, Cursor, Codex 등).

`vinext init`이 하는 일은 README에 다음과 같이 적혀 있다.

1. `vinext check`로 호환성을 점검한다.
2. 런타임 패키지와 Vite 도구를 설치한다.
3. CommonJS 설정 파일(예: `postcss.config.js`)의 이름을 `.cjs`로 바꾼다.
4. `package.json`에 `"type": "module"`을 더한다.
5. `dev:vinext`, `build:vinext`, `start:vinext` 스크립트를 기존 스크립트 옆에 더한다.
6. 플랫폼(Cloudflare가 기본, 또는 Node)을 묻는다.
7. `vite.config.ts`를 만든다.
8. Cloudflare이면 `cloudflare.config.ts`도 만든다.

비파괴적이라서 `next.config`, `tsconfig.json`, 소스 파일을 고치지 않고 Next.js 의존성도 지우지 않는다. 그래서 `next dev`는 계속 동작한다. 다만 위 3번과 4번처럼 설정 파일 이름과 `package.json`은 바뀌므로 병합 전에 변경을 확인해야 한다.[^review]
`vinext init`의 플래그는 `--platform`(cloudflare 또는 node, 에이전트는 사용자에게 물어야 함), `--cdn-cache`, `--data-cache`, `--image-optimization`(Cloudflare에서 에이전트와 CI에는 필수), `--port`(기본 3001), `--skip-check`, `--force`, `--legacy-wrangler-cloudflare-init`, `--ignore-wrangler-config`, `--name`이다.

### 수동 설정

```text
npm install vinext
npm install -D vite @vitejs/plugin-react
```

App Router를 쓰면 `react-server-dom-webpack`과 개발 의존성으로 `@vitejs/plugin-rsc`도 설치한다.
설정은 Vite 설정에서 플러그인 하나를 등록하는 것이 전부이다.

```ts
import { defineConfig } from "vite";
import vinext from "vinext";

export default defineConfig({
  plugins: [vinext()],
});
```

`vinext()`는 `app/`이나 `pages/`를 자동으로 찾고 `next.config.js`를 읽는다. `@vitejs/plugin-rsc`는 `app/`이 있으면 Vinext가 자동 등록하므로 직접 등록하면 빌드가 실패한다.
스크립트는 `dev`가 `vite dev`, `build`가 `vite build`, `start`가 `vinext start`이다. 피어 의존성은 React 19.3.1 이상, `react-dom`, `react-server-dom-webpack`, Vite 8 이상이다.

### 명령

| 명령                            | 하는 일                                                      |
| ------------------------------- | ------------------------------------------------------------ |
| `vite dev`                      | HMR이 있는 개발 서버                                         |
| `vite build`                    | 프로덕션 빌드(App Router는 RSC, SSR, 클라이언트의 다중 환경) |
| `vinext start`                  | 로컬 프로덕션 서버                                           |
| `npx @vinext/cloudflare deploy` | 빌드하고 Cloudflare Workers에 배포                           |
| `vinext init`                   | Next.js 프로젝트 이전                                        |
| `vinext check`                  | 호환성 점검                                                  |
| `vinext lint`                   | eslint나 oxlint에 위임                                       |

`vinext dev`와 `vinext build`는 Vite 명령의 얇은 별칭이고 Vite 설정이 필요하다.
Cloudflare 배포의 플래그는 `--preview`, `--env`, `--name`, `--vite-config`, `--message`, `--tag`, `--skip-build`, `--dry-run`, `--warm-cache`, `--traffic-aware-warm-cache`이다.
Vite 8(Rolldown, Oxc, Lightning CSS)을 대상으로 하므로 사용자 설정은 `esbuild`와 `rollupOptions` 대신 `oxc`, `optimizeDeps.rolldownOptions`, `build.rolldownOptions`를 쓰라고 한다. 클라이언트 자산 이름은 기본으로 해시만 쓴다.

## 배포

### Cloudflare Workers

`@cloudflare/vite-plugin`으로 통합하며 준비는 `vinext init --platform=cloudflare`이다.
인증은 `cf auth login`이나 「Edit Cloudflare Workers」 템플릿의 `CLOUDFLARE_API_TOKEN`이고 계정 ID는 `cloudflare.config.ts` 최상위의 `accountId`나 `CLOUDFLARE_ACCOUNT_ID`에 둔다. 배포는 `npx @vinext/cloudflare deploy`(`--env staging`, `--preview`)이다.
서버 컴포넌트와 라우트 핸들러와 서버 액션에서 `import { env } from "cloudflare:workers"`로 바인딩(D1, R2, KV, Durable Objects, AI, Queues, Vectorize, Browser Rendering)에 접근한다.
캐시 어댑터는 `kvDataAdapter`, `workersCacheCdnAdapter`, `staticAssetsAdapter`, `responseStoreAdapter`가 있다. 사이트 소개는 ISR에 KV를 쓴다고 한다.
트래픽 인식 사전 워밍(`--traffic-aware-warm-cache`)은 사용자 지정 도메인과 Zone Analytics Read, Zone Read 권한의 토큰이 필요하고 기본 덮는 비율은 90%라고 한다. 사이트는 `--experimental-tpr` 표기도 보여 준다.
`sharp`, `@resvg/resvg-js`, `@napi-rs/canvas` 같은 네이티브 모듈은 대체되지 않아 Workers에서 실패한다. 클라이언트 쪽 Module Federation은 `@module-federation/vinext`를 `vinext()` 앞에 등록한다.

### 다른 플랫폼

Nitro Vite 플러그인을 `vinext()` 옆에 더한다(`nitro()`는 `nitro/vite`에서 가져온다). 로컬 빌드는 `NITRO_PRESET`(vercel, netlify, deno_deploy, aws_amplify, node)을 쓴다. Vercel, Netlify, AWS Amplify, Deno Deploy, Azure 등이 안내된다. Node 프리셋은 `NITRO_PRESET=node` 빌드 뒤 `node .output/server/index.mjs`로 돈다.

### Node 독립 서버

`output: "standalone"`이면 `vite build`가 `dist/standalone/`을 만들고 `node dist/standalone/server.js`로 돈다. 포트는 `PORT`(기본 3000), 바인드 주소는 `HOST`(기본 `0.0.0.0`)에서 읽는다. Next.js의 `HOSTNAME`이 아니므로 `HOSTNAME`만 둔 배포 설정은 수신 주소를 정하지 못한다.[^review] `startProdServer`의 옵션은 `port`, `host`, `outDir`, `serverDir`, `rscEntryPath`, `serverEntryPath`, `noCompression`이다.
README는 Node 프로덕션 서버를 Workers 배포보다 덜 완전한 경로로 구분하는 것으로 읽힌다. 이 문서는 그 서술이 정확히 어디에 있는지 확인하지 못했다.

## 지원 범위

README의 「현재 동작하는 것」은 다음과 같다. App Router와 Pages Router(개발과 프로덕션), RSC와 서버 액션과 라우트 핸들러와 미들웨어, 정적 생성과 ISR과 `output: "export"`와 독립 Node 출력, 핵심 `next/*` 모듈(link, image, navigation, headers, cache, Metadata API), Cloudflare Workers 배포, 이전 도구(`vinext check`, `vinext init`, 에이전트 스킬)이다.
Next.js 16 API 표면의 약 94%가 전부 또는 부분 지원이고 나머지는 폐기 기능의 의도된 빈칸과 PPR, Cache Components라고 한다.

| 모듈                                  | 상태                                                        |
| ------------------------------------- | ----------------------------------------------------------- |
| `next/link`, `next/cache`, `next/og`  | 전부 지원(`next/og`는 Satori와 resvg)                       |
| `next/image`                          | 부분(원격은 `@unpic/react`로 28개 CDN, 빌드 시 최적화 없음) |
| `next/font/google`, `next/font/local` | 부분(런타임 로딩)                                           |
| `next/amp`, `next/web-vitals`         | 아무 동작 없음                                              |
| i18n                                  | 부분(도메인 라우팅 없음)                                    |
| 라우트 세그먼트 설정                  | 부분(`preferredRegion` 무시)                                |

알려진 공백으로 README는 다음을 든다. Cache Components와 Partial Prerendering(`"use cache"`는 일부 구현), 빌드 시 이미지와 글꼴 최적화(이미지는 Cloudflare에서 요청 시 최적화, Google Fonts는 CDN, 로컬 글꼴 CSS는 런타임 삽입), App Router 개발 모드의 네이티브 모듈 실패 가능성, `preferredRegion` 무시(엣지 App Router 페이지는 Cache Components 밖에서 ISR 캐시되지 않음), 일부 문서화되지 않은 최신 Next.js 동작이다.
의도적으로 지원하지 않는 것은 Vercel 전용 기능, AMP, 옛 `next export`, Turbopack과 webpack 설정, `next/jest`(Vitest를 쓰라고 함), `create-next-app`(`create-vinext-app`을 쓰라고 함), 문서화되지 않은 동작과의 완전한 동일성이다. React Compiler는 `vinext({ react: { compiler: true } })`로 켜며 `@vitejs/plugin-react` 6.1 이상과 `oxc-transform-react`가 필요하다. `.env`는 Next.js의 순서를 따른다.

설계 원칙은 네 가지이다. 어디든 배포(Cloudflare는 네이티브, 나머지는 Nitro), 버그까지 똑같이 만들지 않는 현실적 호환(실제 앱의 95% 이상이 목표), 최신 Next.js(16.x)만 대상, 점진적 도입이다.

## 호환성과 성능 현황

### 호환성 대시보드

`vinext.dev/compatibility`는 Next.js 배포 테스트 스위트를 매일 밤 Vinext에 돌린 결과를 보여 준다. 2026년 11월 18일 실행(Next.js v16.2.6)의 값은 다음과 같다.

| 지표                  | 값    |
| --------------------- | ----- |
| 지원 대상 통과율      | 99.7% |
| 전체 통과율           | 96.2% |
| 지원 표면 커버리지    | 93.9% |
| 실패한 지원 대상 파일 | 4개   |

라우터별로 App Router는 지원 대상 99.7%와 전체 95.0%, Pages Router는 99.7%와 98.0%, 혼합은 100.0%와 96.9%이다. 테스트 파일은 799개이다. 지원 대상 통과율은 연기된 것, Next.js 컴파일러 전용, Vite 쪽 대응을 기다리는 스위트를 뺀 값이고 Next.js가 건너뛴 테스트는 두 비율에서 모두 빠진다고 한다. 개별 파일 목록과 실패 파일 이름은 이 문서가 읽지 못했다.

### 벤치마크

벤치마크는 `main` 병합마다 2코어 GitHub CI에서 돌고 33개 라우트의 App Router 앱을 Turbopack의 Next.js와 Vite 8의 Vinext로 비교한다. 두 앱 모두 `force-dynamic`이고 컴파일과 번들 속도만 재며 프로덕션 서빙 성능이 아니다. 2026년 11월 18일 값은 다음과 같다(중앙값).

| 시나리오                                  | Next.js | Vinext  |
| ----------------------------------------- | ------- | ------- |
| 프로덕션 빌드                             | 3.67초  | 2.69초  |
| 개발 서버 콜드 스타트                     | 1.89초  | 2.27초  |
| 개발 서버 콜드 스타트(큰 Pages Router 앱) | 22.69초 | 18.24초 |
| 클라이언트 번들(gzip)                     | 185.6KB | 152.8KB |

개발 서버 콜드 스타트는 일반 앱에서 Next.js가 더 빠르다. Vinext 쪽에는 클라이언트 진입 141.0KB, RSC 진입 닫힘 143.1KB, 서버 번들 250.5KB도 표시된다.
출시 글의 수치(빌드 7.38초에서 1.67초로 4.4배, 번들 168.9KB에서 72.9KB로 57%)와 홈페이지의 현재 문구(빌드 최대 2배, 번들 약 23%, 185KB에서 143KB)와 대시보드의 값이 서로 다르다. 홈페이지의 143KB가 대시보드의 어느 지표인지는 이 문서가 확인하지 못했다. `vinext.io`는 출시 때의 4.4배, 57%, 테스트 2,080개 이상을 그대로 싣는다.

## 버전 흐름

`vinext.dev/blog`의 목록은 1.0(2026년 9월 28일, 안정 API와 캐시 워밍)에서 1.1(10월 8일, 더 빠른 빌드와 개발 시작), 1.2(10월 14일), 1.3(10월 20일, 요청 수 감소와 Worker 미리 보기), 1.4(10월 28일, 서버 작업 감소와 하이드레이션 개선)까지 한 달 사이에 다섯 번 나왔다. 이 문서는 1.2 본문만 읽었고 나머지는 목록의 요약이다.
1.2의 내용은 `vinext init`이 `runWorkerFirst` 설정을 만들어 `public/` 파일에도 미들웨어를 돌리는 것, 캐시 키 수정(서로 다른 요청이 같은 키를 쓰지 않도록 `unstable_cache` 키를 SHA-256 다이제스트로, `x-api-key` 응답은 공유 Cloudflare 캐시에 저장하지 않음), Pages Router ISR이 `_document`를 포함한 전체 렌더를 하는 것, 서버 액션이 `@vitejs/plugin-rsc` 0.5.37을 요구하는 것, `next-intl` 검증, Module Federation 패키지이다.
출시 글과 1.0 글은 각각 `vinext/vinext.md`와 `vinext/vinext-1-0.md`에 따로 정리했다.

## 분석

### 중심 주장은 API 계약만 지키고 빌드를 바꾼다는 것이다

README는 Next.js의 공개 API를 재구현하고 나머지(빌드, 번들러, 배포)를 Vite 생태계에 맡긴다고 설명한다.
OpenNext가 빌드 출력을 변환한다면 Vinext는 빌드 자체를 대체한다. FAQ가 OpenNext를 더 성숙하고 범위가 넓다고 인정하는 것도 이 위치 설정에서 나온다.
이는 README의 서술을 이 문서가 정리한 것이다.

### 호환성을 숫자로 상시 공개한다

대시보드는 통과율과 분모 정의(연기된 것, 건너뛴 것을 뺀다)를 함께 보여 주고 시간 추이를 그린다.
수치의 의미를 독자가 따져 볼 수 있게 하는 구성이다. 다만 분류는 프로젝트가 정하는 것이어서 지원 대상 통과율 99.7%는 분모가 줄어든 결과이다. 이는 이 문서의 해석이다.

### 빠르게 움직이는 프로젝트이다

한 달에 다섯 번의 큰 릴리스와 몇 번의 패키지 릴리스가 있고 최근 릴리스 노트는 캐시, 하이드레이션, 프리페치 같은 세부 수정이 대부분이다.
출시 글이 설명한 대로 Next.js의 상류 변경을 매일 추적하는 운영이 이 속도의 바탕으로 보인다. 이는 이 문서의 해석이다.

## 비평

### 수치가 출처마다 다르다

위에서 본 것처럼 같은 프로젝트의 출시 글, 홈페이지, 대시보드, `vinext.io`가 서로 다른 성능 수치를 싣는다.
어느 값이 현재 기준인지, 조건이 바뀐 것인지는 사이트가 설명하지 않는다. 독립된 측정도 읽지 못했다.

### 프로덕션 주의가 문서마다 다른 강도로 적혀 있다

README는 프로덕션 사용에 「주의해서 쓸 수 있다」고 답하고 알려진 공백을 나열한다. 출시 글은 고객이 프로덕션에서 쓴다고 적고, 1.0 글은 프로덕션 수준으로 졸업했다고 한다.
어느 앱에 안전한지는 읽은 범위에서 판단할 수 없고, 앱이 `"use cache"`나 PPR이나 webpack 설정에 기대는지가 조건이라는 점만 분명하다.

### 보안 정책이 Cloudflare 전체 제도에 기댄다

SECURITY 문서는 지원 버전 표, 처리 기한, 이메일 주소 없이 Cloudflare 취약점 공개 정책과 HackerOne 프로그램으로 안내한다.
`vinext init`이 `next`를 지우지 않아 감사 도구가 Next.js 권고를 계속 보고한다는 점과 `next`를 지우면 더 이상 보고하지 않는다는 점은 이전 검토 글이 짚었다.[^review] Next.js 권고가 Vinext에 해당하는지를 알려 주는 별도 경로는 읽은 범위에 없다.

### 한 플랫폼으로 기운 통합이다

Cloudflare 쪽은 바인딩, 캐시 어댑터, 트래픽 인식 워밍, 배포 도구가 모두 갖춰져 있고 다른 플랫폼은 Nitro 플러그인 한 줄이다.
Node 독립 서버와 Nitro의 지원 정도가 Workers와 같은지는 문서에서 구분되지 않는다.

### 공동체 사이트와 공식 사이트가 섞인다

`vinext.io`는 이름이 비슷한 비공식 사이트이고 수치가 오래되었다. 검색으로 먼저 만나는 사람이 공식 문서로 오해할 수 있다.
HN에서는 이 저장소 글에 한 사용자가 Next.js API 표면을 다시 구현할 가치가 있느냐는 질문 하나를 달았고 답은 없었다.[^ubercore]

### 외부 반응

HN의 저장소 글은 2026년 2월 25일 것으로 17점에 댓글 2개이고, 하나는 출시 글 토론 링크이다. 출시 글 토론은 540점에 236개 댓글이며 `vinext/vinext.md`에 정리했다. `vinext.dev`로 올라온 글은 1.2 소개 한 건(1점, 댓글 없음)이다.
GeekNews 토픽 26997은 출시 글을 정리한 소개이고 이용자 댓글이 없었다.
Lobste.rs에서는 `vinext` 검색 결과가 이 프로젝트의 글이 아닌 다른 글 1건이었다.

## 인사이트

### 가져갈 것은 이전을 단계별로 점검하는 순서이다

브랜치에서 `vinext check`로 호환성을 보고, `vinext init`으로 스크립트를 옆에 더하고, 양쪽 빌드에 같은 종단 간 테스트를 돌려 리다이렉트와 미들웨어와 캐시 헤더와 ISR 재검증을 비교한다.[^review]
앱이 `"use cache"`, PPR, webpack 로더, 네이티브 모듈에 기대는지 먼저 센다. 이는 이 문서의 적용이다.

### 수치는 대시보드와 날짜를 함께 본다

성능과 호환성 수치는 계속 바뀌므로 글의 수치를 그대로 믿지 말고 대시보드의 날짜와 비교 조건을 확인한다.
자기 앱에서 같은 조건으로 재는 것이 가장 믿을 만하다.

### 함께 읽을 문서

- `vinext/vinext.md`: 출시 글 분석
- `vinext/vinext-1-0.md`: 1.0 출시 글
- `vinext/vinext-inside.md`: 내부 구조 해설
- `vinext/vinext-logrocket.md`: LogRocket 소개 글
- `vinext/vinext-migration-review.md`: 1.0 이전 검토 글
- `nextjs/opennext.md`: 같은 문제를 푸는 다른 접근

### 확인할 관찰

이 프로젝트의 주장을 가를 관찰은 세 가지이다.
같은 조건에서 독립적으로 잰 빌드와 번들 크기,
`"use cache"`와 PPR의 완성과 호환성 대시보드 실패 파일의 해소,
Cloudflare 밖 플랫폼에서의 지원 수준이다.
셋 모두 이 문서가 확인하지 못했다.

---

[^review]: [Should You Move Your Next.js App to Vinext 1.0? | privatedevops](https://privatedevops.com/articles/move-nextjs-app-to-vinext)

[^ubercore]: <https://news.ycombinator.com/item?id=47149985>
