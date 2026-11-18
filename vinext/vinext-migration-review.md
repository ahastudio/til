# Vinext 1.0 이전 검토 글

원문: [Should You Move Your Next.js App to Vinext 1.0?](https://privatedevops.com/articles/move-nextjs-app-to-vinext)

## 요약

2026년 9월 29일 privatedevops.com에 실린 글이다. 글에 필자 표기는 없다.
Vinext 1.0이 나온 이튿날, 기존 Next.js 앱을 옮길 만한지 판단하는 기준을 다룬다.

글이 설명하는 Vinext는 Cloudflare가 2026년 9월 28일 Birthday Week에 낸 MIT 라이선스의 Vite 플러그인이다. 공개 Next.js API를 재구현하며 `next build`나 그 출력을 쓰지 않는다. Vite 8에서 돌고 Next.js 16만 대상으로 한다.
Cloudflare Workers가 주 대상이고 독립 Node.js 서버를 만들 수 있으며 Nitro 플러그인으로 Vercel, Netlify, AWS, Deno Deploy에도 닿는다고 한다.

완성도는 두 가지로 제시된다. Cloudflare는 가장 많이 요청된 기능의 호환성 테스트가 캐시 컴포넌트를 제외하고 99% 넘게 통과한다고 하고, 저장소 README는 Next.js 16 API 표면의 약 94%(전부 또는 부분 지원)라고 한다.
알려진 공백은 캐시 컴포넌트와 Partial Prerendering(`"use cache"`는 부분 구현), 빌드 시 이미지와 글꼴 최적화, App Router 개발 모드에서의 네이티브 모듈(`sharp`, `satori`, `resvg`, `lightningcss`) 실패 가능성, `preferredRegion` 무시이다.
Turbopack과 webpack 설정은 적용되지 않아 커스텀 로더는 Vite 플러그인으로 바꿔야 하고 `next/jest`는 Vitest로 대체된다. 문서화되지 않은 Next.js 동작은 재현하지 않는다.

## 보안 질문을 먼저 한다

글은 Next.js 권고가 `next` 패키지의 코드에 대한 것이고 Vinext는 다른 코드로 렌더링하므로 권고의 적용 여부는 Vinext만 알려 줄 수 있다고 쓴다.
Vinext는 Cloudflare의 취약점 공개 프로그램으로 제보를 받고, 9월 29일 기준 저장소에 공개된 보안 권고가 없었다고 한다.
`vinext init`은 의존성에서 `next`를 지우지 않아 `npm audit`가 Next.js 권고를 계속 보고하는데, `next`를 지우면 `npm audit`은 Next.js에 대해 아무 말도 하지 않는다. Vinext가 `next`를 요구하는 기능은 styled-jsx 정도라고 한다.
9월 30일 Next.js가 16.3.8과 15.5.27로 7개 권고를 고쳤다고 하고, Next.js는 올리면 되지만 Vinext는 해당 동작을 재현했는지에 달려 있다고 쓴다.

## 이전해도 되는 경우

- 적합: 앱이 Cloudflare Workers에서 돌고(통합이 가장 깊음), 빌드와 개발 서버 시간이 실제 비용이며, 캐시 컴포넌트와 커스텀 webpack 설정을 쓰지 않는 경우.
- 부적합: `"use cache"`나 Partial Prerendering에 의존하거나, 다시 써야 하는 webpack 로더가 있거나, 두 번째 프레임워크의 릴리스와 권고를 추적할 사람이 없는 경우.
- 자체 호스팅: Kubernetes나 Docker에서 Next.js를 돌리는 팀은 이점이 약하다. `next start`와 standalone 출력이 이미 Node.js가 도는 곳이면 어디서나 돌아서, 이전해도 얻는 것은 Vite 도구이고 없던 이식성이 아니라는 설명이다.
- 주의: Vinext의 standalone 서버는 바인드 주소를 `HOSTNAME`이 아니라 `HOST`에서 읽는다. 기본은 `0.0.0.0`의 3000 포트라서 `HOSTNAME`만 둔 매니페스트는 더 이상 수신 주소를 정하지 못한다.

## 위험 없이 시험하기

브랜치에서 다음을 실행한다.

```text
npx vinext check
npx vinext init --platform=node
```

`vinext init`은 기존 Next.js 설정을 그대로 두고 `dev:vinext`, `build:vinext`, `start:vinext` 스크립트를 옆에 더하며 `next.config`, `tsconfig.json`, 소스 파일을 건드리지 않는다.
다만 `package.json`에 `"type": "module"`을 더하고 `postcss.config.js` 같은 CommonJS 설정 파일을 이름을 바꾸므로 병합 전에 그 변경을 확인하라고 한다.
이후 두 빌드에 자기 종단 간 테스트를 돌려 리다이렉트, 미들웨어, 캐시 헤더, ISR 재검증을 비교하라고 한다. 캐싱을 가장 주의하라고 하는데, Vinext 팀의 상류 변경 일일 검토가 안전하지 않은 캐싱 동작을 계속 잡아내고 있기 때문이라고 한다.

## 비평

### 근거가 Cloudflare 글과 README의 재서술이다

호환성 수치와 공백 목록은 Cloudflare 글과 README에서 온 것이고 글 필자가 직접 시험한 결과는 없다.
필자 표기가 없고 글이 글 끝에 유료 프로덕션 점검 안내를 두므로 이해관계가 있는 자료이다. 이 문서가 점검 서비스의 내용을 읽지는 않았다.

### 보안 서술이 하루 시점에 묶여 있다

글은 9월 29일 기준으로 권고가 없다고 쓰고, 이튿날 Next.js가 7개 권고를 고쳤다고 덧붙인다.
Vinext가 그 권고에 영향을 받는지는 글에서 판단하지 않는다. 지금 이 서술이 유효한지는 이 문서가 확인하지 못했다.

### 기준이 이분법에 가깝다

적합과 부적합의 조건이 몇 가지로 나뉘지만 비용 기준(예: 빌드 시간 몇 분 이상)은 제시되지 않는다.
`npm audit`이 Next.js 권고를 보고하지 않게 되는 점은 정확한 지적이지만 대안(Vinext 쪽 권고를 구독하는 방법)은 저장소 보안 정책 링크만 안내한다.

### 외부 반응

HN에는 이 글 주소로 올라온 글이 없었다(대조 쿼리는 정상이었다).
Lobste.rs에는 `vinext` 검색 결과가 이 글이 아닌 다른 글 1건이었다.
GeekNews에는 Vinext 2월 글의 토픽만 있고 이 글의 토픽은 없었다.

## 기억할 원칙

- 프레임워크를 재구현한 대체재로 옮기면 상류의 보안 권고가 자동으로 적용되지 않는다. 권고마다 대체재에도 해당하는지 확인하는 절차가 필요하다.
- `next`를 의존성에서 지우면 감사 도구가 상류 권고를 더 이상 보고하지 않는다. 지우기 전에 대체 감시 방법을 정한다.
- 이미 Node가 도는 곳에서 자체 호스팅하는 팀은 이식성이 아니라 빌드 도구 때문에 옮기는 것이므로 그 이득이 필요한지 따진다.
- 이전은 브랜치에서 하고, 양쪽 빌드에 같은 종단 간 테스트를 돌려 캐시와 재검증을 비교한다.
