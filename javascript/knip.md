# Knip: 진입점에서 닿지 않는 파일·export·의존성을 찾아 잘라 내는 도구

<https://knip.dev/>

<https://github.com/webpro-nl/knip>

HN 토론: <https://news.ycombinator.com/item?id=49624899> (2점, 0개 댓글)

## 소개

Knip은 JavaScript와 TypeScript 프로젝트에서
쓰지 않는 파일, export, 의존성을 찾아 주고 상당수는 직접 지워 주는 CLI다.
이름은 네덜란드어로 “자르다”라는 뜻이고 K를 세게 발음한다.
README가 내세우는 효과는 세 가지다.
코드와 의존성이 줄면 성능이 좋아지고, 유지보수가 줄고, 리팩터링이 쉬워진다.

만든 사람은 Lars Kappert(`webpro`)다.
2022년 10월 4일 Exportman이라는 이름으로 첫 커밋을 했고,
닷새 뒤 Knip v0.1.2로 이름을 바꿔 처음 배포했다.
2026년 10월 기준 저장소 스타는 1만 2천여 개, 라이선스는 ISC다.
npm 월간 다운로드는 2026년 9월 12일부터 한 달 동안 약 7,161만 회였고,
최신 릴리스는 10월 9일에 나온 6.41.0이다.

비슷한 일을 하던 도구는 대부분 멈췄다.
문서의 비교 페이지에 따르면 depcheck, unimported, ts-prune, tsr은
모두 보관(archived) 처리되었고, 저장소에서 Knip을 쓰라고 안내한다.
Knip은 이들이 각자 다루던 범위를 한 도구에 모았다.

| 기존 도구         | 다루던 범위               | 비슷한 Knip 명령                                 |
| ----------------- | ------------------------- | ------------------------------------------------ |
| depcheck          | 쓰지 않거나 누락된 의존성 | `knip --dependencies`                            |
| unimported        | 매달린 파일과 의존성      | `knip --production --dependencies --files`       |
| ts-prune          | 쓰지 않는 export          | `knip --include exports,types,nsExports,nsTypes` |
| ts-unused-exports | 쓰지 않는 export          | `knip --include exports,types,nsExports,nsTypes` |
| tsr               | 쓰지 않는 export 제거     | `knip --fix-type exports,types`                  |

보고하는 문제 유형은 17가지다.
그중 기본으로 켜진 핵심은 다음과 같다.

| 유형                  | 의미                                           | 자동 수정 | 키             |
| --------------------- | ---------------------------------------------- | --------- | -------------- |
| Unused files          | 어떤 진입점에서도 닿지 않는 파일               | 예        | `files`        |
| Unused dependencies   | 어디서도 가져오지 않는 의존성                  | 예        | `dependencies` |
| Unlisted dependencies | 가져다 쓰는데 `package.json`에 없는 의존성     | 아니요    | `unlisted`     |
| Unlisted binaries     | 스크립트에서 쓰는데 설치 목록에 없는 실행 파일 | 아니요    | `binaries`     |
| Unresolved imports    | 해석할 수 없는 import 지정자                   | 아니요    | `unresolved`   |
| Unused exports        | 다른 파일이 가져가지 않는 export               | 예        | `exports`      |
| Unused exported types | 다른 파일이 쓰지 않는 type·interface·enum      | 예        | `types`        |
| Duplicate exports     | 같은 것을 두 번 이상 export                    | 아니요    | `duplicates`   |
| Circular dependencies | 실행 시점에 서로를 가져오는 파일들             | 아니요    | `cycles`       |

`cycles`는 기본 규칙이 `warn`이라 보고는 하지만 실패로 세지 않는다.
네임스페이스 안의 export(`nsExports`, `nsTypes`)는 기본으로 꺼져 있다.

## 동작 방식

### 그래프를 한 번 만들고 질의한다

Knip은 두 단계로 돈다.
빌드 단계는 진입 파일에서 출발한다.
파일을 읽고 파싱해 import와 export를 모으고,
각 import를 다른 파일로 해석한 뒤,
새로 닿은 파일마다 같은 일을 반복한다.
결과는 닿을 수 있는 모든 파일과 그 사이의 import 관계를 담은 모듈 그래프다.

분석 단계는 다시 파싱하지 않고 이 그래프만 질의한다.
판정 기준은 단순하다.

- 어떤 진입점에서도 닿지 않는 파일은 쓰지 않는 파일이다.
- 다른 파일이 가져가지 않는 export는 쓰지 않는 export다.
- 어떤 파일도 가져오지 않는 의존성은 쓰지 않는 의존성이다.
- 가져다 쓰는데 `package.json`에 없으면 목록에 없는(unlisted) 의존성이다.

따라서 결과의 정확도는 그래프의 완성도를 넘지 못하고,
그래프의 완성도는 진입 파일을 얼마나 빠짐없이 찾았는지에 달려 있다.

### 진입 파일은 여러 곳에서 모인다

기본 진입 패턴은 루트와 `src/` 아래의 `index`, `main`, `cli`이고,
확장자는 `js`, `mjs`, `cjs`, `jsx`, `ts`, `mts`, `cts`, `tsx`다.
기본 설정을 풀어 쓰면 다음과 같다.

```json
{
  "entry": [
    "{index,cli,main}.{js,cjs,mjs,jsx,ts,cts,mts,tsx}",
    "src/{index,cli,main}.{js,cjs,mjs,jsx,ts,cts,mts,tsx}"
  ],
  "project": ["**/*.{js,cjs,mjs,jsx,ts,cts,mts,tsx}!"]
}
```

여기에 다음이 더해진다.

- `package.json`의 `main`, `bin`, `exports` 필드
- 활성화된 플러그인이 알려 주는 진입 파일과 설정 파일
- `require()`, `import()`, `require.resolve()`, `import.meta.resolve()`
- `new URL('./file.js', import.meta.url)`와 `new Worker(…)`
- `module.register('./loader.js')`
- 스크립트 파서가 뽑아낸 명령: `package.json`의 `scripts`,
  CI 워크플로의 `run`, 소스 안의 `execa`·`zx` 호출 등

`.gitignore`에 걸린 파일은 진입 파일로 넣지 않는다.
사용자가 `entry`를 지정하면 기본값과 합쳐지지 않고 덮어쓴다.

### 플러그인이 설정 파일을 읽는다

플러그인은 `package.json`에 해당 패키지가 있으면 자동으로 켜진다.
`astro`가 의존성에 있으면 Astro 플러그인이,
`vitest`가 있으면 Vitest 플러그인이 켜지는 식이다.
저장소의 플러그인 디렉터리에는 2026년 10월 기준 195개 항목이 있다.

플러그인이 하는 일은 셋이다.
설정 파일을 읽어 의존성을 뽑고,
그 도구가 쓰는 진입 파일 패턴을 더하고,
그 도구의 명령행 인자를 해석한다.
예를 들어 `vitest.config.ts`의 `environment: 'happy-dom'`은
`vitest-environment-happy-dom`이라는 의존성으로 바뀐다.
`playwright.config.ts`의 `testDir`과 `testMatch`는
`integration/**/*-test.ts` 같은 진입 패턴이 된다.

여기서 중요한 점이 하나 있다.
FAQ는 플러그인 파서가 동적 설정 파일을 실제로 불러와 실행한 뒤
export한 값을 읽는다고 밝힌다.
ESLint flat config, tsdown, tsup 같은 일부 플러그인은
v6에서 정적 분석으로 바뀌었지만,
나머지 다수는 여전히 설정 파일을 실행한다.

### 결과는 연쇄로 나온다

도구가 생성하는 진입 파일을 Knip이 모르면 그 파일이 쓰지 않는 파일로 잡힌다.
그 파일만 가져오던 파일도 모두 쓰지 않는 파일이 되고,
그 파일들의 export와 그 파일들만 쓰던 의존성도 함께 보고된다.
진입점 하나를 놓치면 수십 건이 쏟아지고,
그 진입점을 추가하면 한꺼번에 사라진다.
그래서 문서는 결과를 위에서부터, 즉 파일, export, 의존성 순으로 읽으라고 한다.

### v6에서 TypeScript를 떼어 냈다

2026년 3월 20일 나온 v6은 파서와 해석기를 TypeScript API에서
`oxc-parser`와 `oxc-resolver`로 바꿨다.
TypeScript 백엔드는 IDE용이라 프로그램 전체와 타입 검사기를 엮어야 했지만,
Knip에 필요한 것은 AST를 한 번 훑어 import와 export를 모으는 일뿐이었다.
공지에 실린 측정값은 다음과 같다.

| 프로젝트   | v5.88.0 | v6.0.0 |
| ---------- | ------- | ------ |
| astro      | 4.0s    | 2.0s   |
| query      | 3.8s    | 1.7s   |
| rolldown   | 3.7s    | 1.7s   |
| sentry     | 11.0s   | 4.0s   |
| TypeScript | 3.7s    | 0.9s   |

대가도 있었다.
클래스 멤버 검사(`classMembers`)는 `ts.LanguageService`의 `findReferences`에
기대고 있었는데,
Go로 다시 쓰인 TypeScript 7에서는 이 JS API를 쓸 수 없어 빠졌다.
Node.js 18 지원도 끊겼고, v6은 Node.js 20.19.0 이상이나 Bun을 요구한다.

## 설정하기

### 설치와 첫 실행

권장 경로는 설정 생성기다.

```bash
npm init @knip/config
npm run knip
```

직접 설치할 때는 `typescript`와 `@types/node`를 피어 의존성으로 함께 넣는다.

```bash
npm install -D knip typescript @types/node
npx knip
```

설정 파일은 `knip.json`, `knip.jsonc`, `.knip.json`, `knip.ts`,
`knip.config.ts`, `package.json`의 `knip` 속성 등에서 찾는다.

### 진입과 범위를 정한다

`entry`는 출발점이고 `project`는 분석 범위다.
`project`에서 빠진 파일은 쓰지 않는 파일로 보고되지 않는다.
패턴 끝의 `!`는 운영 코드라는 표시다.

```json
{
  "$schema": "https://unpkg.com/knip@6/schema.json",
  "entry": ["src/index.ts!", "scripts/{build,create}.js"],
  "project": ["src/**/*.ts!", "!src/test-helpers/**!", "scripts/**/*.js"],
  "ignoreDependencies": ["@reportportal/agent-js-playwright"],
  "rules": {
    "files": "error",
    "dependencies": "error",
    "exports": "warn",
    "duplicates": "off"
  }
}
```

각 줄이 담는 결정은 다음과 같다.

- `src/index.ts!`: 배포되는 코드의 진입점이라 운영 모드에서도 남는다.
- `scripts/...`: 빌드 스크립트는 운영 모드에서 제외한다.
- `!src/test-helpers/**!`: 운영 모드에서 테스트 도우미를 범위에서 뺀다.
- `ignoreDependencies`: 설정 파일 안의 조건문 때문에
  분석 시점에 보이지 않는 의존성을 예외로 둔다.
- `rules`: 정리를 끝낸 유형만 `error`로 올린다.

플러그인 설정 파일 위치가 기본값과 다르고
스크립트에서도 참조하지 않는다면 직접 알려 준다.

```json
{
  "playwright": { "config": ["e2e/playwright.config.ts"] },
  "vite": "packages/*/vite.config.ts"
}
```

### CI에 넣는다

문제가 하나라도 있으면 종료 코드 1로 끝나므로 그대로 CI 게이트가 된다.
문서의 GitHub Actions 예시는 다음과 같다.

```yaml
name: Lint project
on: push
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: 24
      - name: Install dependencies
        run: npm install --ignore-scripts
      - name: Run knip
        run: npm run knip
```

## 값 정하기

| 결정                  | 시작값                           | 근거                                                         | 바꿀 때                                    |
| --------------------- | -------------------------------- | ------------------------------------------------------------ | ------------------------------------------ |
| 실행 모드             | 기본 모드와 `--production` 두 번 | 기본은 도구 설정까지, 운영 모드는 배포 코드만 본다           | 테스트 쪽 정리가 끝나면 운영 모드만 게이트 |
| 첫 게이트 유형        | `files`, `dependencies`          | 파일이 연쇄의 뿌리이고 의존성은 오탐 비용이 작다             | 보고가 0이 되면 `exports`를 `error`로      |
| 예산                  | `--max-issues <현재 건수>`       | 새로 늘어나는 것만 막고 기존 부채는 천천히 줄인다            | 건수가 줄 때마다 낮춘다                    |
| 자동 수정 범위        | `--fix-type dependencies`        | `package.json` 변경은 리뷰가 쉽고 되돌리기도 쉽다            | 설정 힌트가 0일 때 `exports,types`         |
| 파일 삭제             | 쓰지 않음                        | `--allow-remove-files` 없이는 지우지 않는다                  | 사람이 목록을 확인한 뒤에만                |
| 진입 파일 export 보고 | 끔(기본)                         | 라이브러리의 공개 API를 오탐으로 잡지 않는다                 | 앱이라면 `includeEntryExports`를 켠다      |
| 캐시                  | CI에서만 `--cache`               | 반복 실행이 빨라지지만 설정·별칭 변경에 오래된 결과가 남는다 | 이상한 결과가 나오면 캐시를 지운다         |

측정할 것은 세 가지다.
설정 힌트(configuration hints)의 개수,
유형별 보고 건수의 추이,
`--performance`로 본 실행 시간이다.
설정 힌트가 0이 아니면 다른 숫자는 믿을 수 없다.

## 트레이드오프

### 포괄성과 오탐은 같은 손잡이에 달려 있다

Knip의 설계 철학은 포괄성이다.
파일, export, 의존성을 한 도구에서 함께 봐야
플러그인이 찾은 진입점이 export 판정을 고치고,
더 많은 파일을 분석해야 의존성 판정이 정확해진다는 논리다.
이 시너지는 진짜다.
depcheck만 돌리면 설정 파일에서만 쓰는 패키지를 판정하기 어렵고,
ts-prune만 돌리면 테스트가 가져가는 export를 쓰는 것으로 착각한다.

그러나 포괄성은 그래프에 빈틈이 생길 자리도 늘린다.
195개 플러그인 중 하나가 설정을 잘못 읽거나,
아직 플러그인이 없는 도구가 진입점을 생성하면
그 아래로 연쇄 오탐이 생긴다.
문서도 큰 레거시 프로젝트에서는 오탐과 설정 작업을 각오하라고 적는다.
오탐을 줄이려면 설정을 늘려야 하고,
설정이 늘수록 “설정 없이”라는 출발점에서 멀어진다.
이 둘을 동시에 갖는 방법은 없다.
2025년 말 나온 MCP 서버가 “configure knip”을 에이전트에게 맡기자고 제안한 것도
이 비용이 사람에게 무겁다는 인정이다.

이 지식이 곧 Knip의 해자라는 점은 경쟁 도구 쪽에서도 드러난다.
Knip보다 20배 빠르다는 Go 도구 rev-dep의 Show HN에서
astegmaier는 `webpack.config.js`를 읽어 의존성을 모든 검사에 되먹이는
Knip 플러그인 같은 기능이 있는지 물었다.[^astegmaier]
rev-dep 저자 jayu_dev는 성능에 집중하는 컴파일 언어 도구라
JavaScript 도구처럼 확장하기 어렵고,
플러그인 시스템은 현실적이지 않다고 답했다.[^jayu_dev]
속도와 플러그인 생태계 중 하나를 고르라는 선택지가 그대로 드러난 대화다.

### 설정 파일을 실행하면 정확해지고 위험해진다

`next.config.ts`의 `pageExtensions`처럼 설정 값이 진입 패턴을 바꾸는 경우,
값을 알려면 파일을 실행하는 편이 가장 정확하다.
정적 분석으로는 함수 호출과 조건문을 모두 따라가기 어렵다.

대가는 두 가지다.
하나는 환경 의존성이다.
환경 변수가 없으면 설정 파일이 예외를 던지고,
Knip은 종료 코드 2로 멈추며 `--no-exit-code`로도 막을 수 없다.
조건문 속 의존성은 분석 시점의 환경에 따라 보였다 안 보였다 한다.
다른 하나는 실행 자체다.
Knip을 돌리는 일은 저장소의 설정 파일 코드를 돌리는 일과 같다.
외부 기여자의 PR을 CI에서 검사할 때
이 사실은 테스트를 돌리는 것과 같은 무게를 갖는다.
문서의 CI 예시가 `npm install --ignore-scripts`로 설치 스크립트를 막으면서도
바로 다음 단계에서 설정 파일을 실행한다는 점은 눈여겨볼 만하다.
v6이 ESLint, tsdown, tsup 플러그인을 정적 분석으로 돌린 것은
속도뿐 아니라 이 위험을 줄이는 방향이지만, 아직 일부다.

### 기본 모드와 운영 모드는 서로 다른 것을 놓친다

기본 모드는 테스트와 스토리까지 진입점으로 삼는다.
그래서 테스트만 가져가는 운영 코드는 쓰는 것으로 보인다.
지워도 되는 함수와 그 테스트가 서로를 살려 두는 셈이다.
운영 모드는 이것을 잡지만,
대신 도구 설정 속 쓰지 않는 플러그인 같은 개발 쪽 부채는 보지 못한다.
FAQ가 어느 쪽을 기본값으로 할지 고민했다고 적은 이유다.
둘 다 돌리는 것이 권장이지만, 그러면 CI 시간과 설정 관리가 두 배가 된다.
`project`의 `!` 표시는 두 모드가 한 설정을 공유하게 해 주지만,
표시를 빠뜨린 패턴은 운영 모드에서 조용히 사라진다.

### 파일 사이만 보고 파일 안은 보지 않는다

Knip은 파일 사이의 의존을 본다.
파일 안의 쓰지 않는 지역 변수나 import는 ESLint나 Biome의 몫이다.
그래서 정리는 한 번에 끝나지 않는다.
Knip이 export를 떼면 그 심볼은 지역 변수가 되고,
린터가 그것을 지우면 그 심볼만 쓰던 import가 사라지고,
다시 Knip이 새 결과를 낸다.
문서는 이를 “헹구고 반복하라”고 표현한다.
여러 도구를 번갈아 돌리는 수렴 과정을 자동화하는 장치는 없다.

린터 안에서 끝내고 싶은 사람도 있다.
silverwind는 쓰지 않는 코드를 린팅 단계에서 잡고 싶지만
ESLint가 `no-unused-modules` 같은 규칙을 받쳐 주던 API를 없애기로 해서,
린트 규칙 몇 개 대신 Knip 같은 별도 도구를 돌리는 것이
비현실적으로 느껴진다고 적었다.[^silverwind]
FAQ는 파일 단위 린터는 프로젝트 전체 그래프를 만들 수 없어서
Knip이 ESLint 플러그인이 아니라고 설명한다.
두 설명을 합치면, 파일 사이 분석은 린터 생태계 밖으로 밀려났고
그 비용은 도구 하나를 더 운영하는 팀이 진다.

## 함정

### `--fix`는 파일을 남겨 둔 채 export만 뗄 수 있다

직접 확인한 사례다.
아래 데모에서 `legacy.ts`는 아무 진입점에서도 닿지 않고,
`greet.ts`의 `shout`을 가져다 쓴다.
`knip --fix`는 `shout`의 `export`를 떼고
`lodash-es`를 `package.json`에서 지웠지만,
`--allow-remove-files`가 없어서 `legacy.ts`는 남겼다.
그 결과 `legacy.ts`는 이제 존재하지 않는 export와
설치 목록에 없는 패키지를 가져오는 파일이 되었다.
타입 검사나 빌드가 이 파일을 포함한다면 깨진다.
파일 삭제를 허용하지 않을 거라면
`--fix-type exports`도 함께 미루는 편이 안전하다.

### 첫 실행 결과를 바로 지우면 안 된다

FAQ는 설정이 안정되기 전에 `--fix`를 돌리는 것을 위험하다고 명시한다.
진입점이 빠진 상태에서는 실제로 쓰는 코드도 쓰지 않는 코드로 보인다.
설정 힌트를 먼저 0으로 만들고, 파일 목록을 사람이 읽은 뒤에 지운다.

### `ignore`는 분석에서 빼지 않는다

ESLint처럼 `ignore` 패턴으로 오탐을 감추고 싶어지지만,
Knip의 `ignore`는 보고만 막고 그래프에서는 빼지 않는다.
원인이 된 진입점 누락은 그대로 남고 다른 곳의 오탐도 그대로다.
분석 범위는 `project`로, 개별 예외는 `@lintignore`·`@internal` 같은
JSDoc 태그나 `ignoreDependencies`로 다룬다.
Knip은 `// knip-ignore` 같은 전용 주석을 일부러 두지 않았다.

### 동적 import 경로는 따라가지 못한다

`import(path.join(baseDir, 'entry.ts'))`처럼 계산된 경로는 해석하지 않는다.
플러그인 시스템이나 라우트 자동 등록처럼
런타임에 파일 이름을 조립하는 코드는 그 대상 파일을 `entry`에 직접 넣어야 한다.
외부 라이브러리 함수를 거쳐 쓰는 export
(`loadable(..., { resolveComponent: c => c.Orange })` 같은 경우)도
놓칠 수 있다.

### 캐시는 설정 변경을 모른다

`--cache`를 켠 상태에서 경로 별칭이나 설정을 바꾸면
없던 파일을 추가했는데도 해석 실패가 계속 보고될 수 있다.
새로 생긴 `.gitignore`도 감지하지 못한다.
결과가 이상하면 `node_modules/.cache/knip`를 지우고 다시 돌린다.

### 메모리가 적은 환경에서 파서가 실패한다

RAM이 적은 머신이나 Node.js 22 이상의 Windows에서는
oxc-parser의 raw transfer가 `RangeError: Array buffer allocation failed`로
실패할 수 있다.
`KNIP_DISABLE_RAW_TRANSFER=1`로 일반 경로를 쓴다.

## 확인하기

연쇄 보고와 자동 수정을 작은 프로젝트로 재현한다.
Knip 6.41.0, Node.js 24.11.0에서 실행했다.

```bash
mkdir -p knip-demo/src && cd knip-demo
cat > package.json <<'EOF'
{
  "name": "knip-demo",
  "private": true,
  "type": "module",
  "scripts": { "knip": "knip" },
  "dependencies": { "lodash-es": "^4.17.21" },
  "devDependencies": { "knip": "^6.41.0", "typescript": "^5.9.0", "@types/node": "^24.0.0" }
}
EOF
cat > src/index.ts <<'EOF'
import { greet } from './greet.ts';
console.log(greet('knip'));
EOF
cat > src/greet.ts <<'EOF'
export const greet = (name: string) => `hello ${name}`;
export const shout = (name: string) => greet(name).toUpperCase();
EOF
# 진입점(src/index.ts)에서 닿지 않는 파일. 이 파일이 연쇄의 뿌리가 된다.
cat > src/legacy.ts <<'EOF'
import { chunk } from 'lodash-es';
import { shout } from './greet.ts';
export const legacy = () => chunk([shout('a')], 1);
EOF
npm install --ignore-scripts
npx knip
```

출력은 다음과 같고 종료 코드는 1이다.
파일 하나를 놓친 결과가 의존성과 export로 번진 것을 볼 수 있다.

```text
Unused files (1)
src/legacy.ts
Unused dependencies (1)
lodash-es  package.json
Unused exports (1)
shout  src/greet.ts:2:14
```

`legacy.ts`가 실제로 어떤 도구의 진입점이었다고 치고 알려 주면
세 건이 함께 사라진다.

```bash
echo '{ "entry": ["src/index.ts", "src/legacy.ts"] }' > knip.json
npx knip   # 출력 없음, 종료 코드 0
rm knip.json
```

이번에는 자동 수정을 단계별로 돌린다.

```bash
npx knip --fix
# lodash-es  package.json  (removed)
# shout  src/greet.ts:2:14  (removed)
# src/legacy.ts 는 남는다 → legacy.ts 가 없는 export 와 패키지를 가져오는 상태
npx knip --fix --allow-remove-files
# src/legacy.ts  (removed)
```

첫 번째 수정 뒤 `greet.ts`의 `shout`은 `export`만 떨어진 지역 상수로 남는다.
이것을 지우는 일은 린터의 몫이다.

## 체크리스트

- 설정 힌트가 0건인가?
- 결과를 파일, export, 의존성 순서로 읽었는가?
- 쓰지 않는 파일로 잡힌 것 중 다른 도구가 생성하거나 런타임에 조립하는 진입점은 없는가?
- 오탐을 `ignore`가 아니라 `entry`, `project`, 플러그인 설정, JSDoc 태그로 처리했는가?
- 운영 모드에서 남겨야 할 패턴에 `!`를 붙였는가?
- 기본 모드와 운영 모드를 둘 다 돌렸는가?
- `--fix` 전에 작업 트리가 깨끗하고 되돌릴 수 있는가?
- export 수정과 파일 삭제를 같은 단계에서 하거나, 둘 다 미뤘는가?
- 수정 뒤 타입 검사, 린터, 테스트를 다시 돌렸는가?
- 외부 기여자의 PR에서 Knip이 설정 파일을 실행해도 되는 환경인가?
- `--cache`를 쓰는 CI에서 설정 변경 시 캐시를 비우는가?

## 비평

### “설정 없이”라는 약속은 플러그인이 있는 동안만 성립한다

문서는 좋은 기본값으로 “zero config”를 지향한다고 쓴다.
작은 프로젝트에서는 맞는 말이다.
그러나 그 약속의 실체는 Knip의 기본값이 아니라 195개 플러그인이 쌓은 지식이다.
플러그인이 없는 사내 도구, 버전이 바뀌어 설정 형식이 달라진 도구,
코드 생성기가 만드는 진입점을 만나는 순간
약속은 설정 작업으로 바뀐다.
State of Knip 글이 Next.js 설정 하나를 제대로 읽으려고
설정 파일을 실행해야 했던 사례를 길게 적은 것은
이 지식을 유지하는 비용이 얼마나 큰지 보여 준다.

이 구조는 도구의 지속성을 한 사람에게 묶는다.
FAQ는 프로그래매틱 API, 로컬 플러그인, Deno 지원 같은 요청을
시간과 후원이 부족해 미루고 있다고 솔직하게 적는다.
같은 범주의 도구가 대부분 보관 처리된 지금,
월 7천만 회 내려받는 도구가 같은 길을 가면 대안이 마땅치 않다.
Knip을 CI 게이트로 들이는 팀은 이 의존을 함께 들인다는 점을
알고 들이는 편이 낫다.

빈자리는 이미 보인다.
skybrian은 rev-dep 스레드에서 Deno 지원을 물으며
자신이 알기로 Knip은 Deno에서 동작하지 않는다고 적었고,
Deno의 import는 `deno.json`으로 해석해야 해서
표준과 다르다고 덧붙였다.[^skybrian]
FAQ의 미뤄 둔 요청 목록에도 Deno 지원이 있다.
e1g는 같은 스레드에서 `oxc-parser`와 `oxc-resolver`로 자체 정적 분석을 만들었고
10만 줄 남짓한 코드에서 1초가 안 걸린다고 전했다.[^e1g]
Knip v6과 같은 부품이다.
범용 도구가 닿지 않는 곳에서는 같은 부품으로 직접 만드는 팀이 늘 수 있다.

### 설정 파일 실행은 문서에서 보안 문제로 다뤄지지 않는다

문서는 설정 파일 실행을 정확도의 문제로만 설명한다.
환경 변수가 없으면 실패하고, 조건부 의존성을 놓칠 수 있다는 식이다.
그러나 신뢰할 수 없는 코드를 다루는 CI에서
린터가 저장소의 TypeScript 파일을 실행한다는 사실은
정확도보다 먼저 따져야 할 문제다.
테스트 러너는 코드를 실행한다는 것을 모두가 알지만,
“쓰지 않는 코드를 찾는 정적 분석기”라는 설명을 듣고
실행을 예상하는 사람은 드물다.
v6에서 정적 분석으로 돌아선 플러그인이 늘어난 것은 반가운 일이지만,
어느 플러그인이 아직 실행하는지는 사용자가 알기 어렵다.
플러그인별로 실행 여부를 표시하거나,
실행을 전부 끄는 모드를 두는 편이 맞다.

### 자동 수정의 단위가 사용자의 기대와 다르다

`--fix`가 export와 의존성은 고치고 파일은 남기는 기본값은
가장 위험한 작업(파일 삭제)을 옵트인으로 둔다는 점에서 신중해 보인다.
그러나 확인하기 절의 데모처럼,
연쇄의 뿌리인 파일을 남긴 채 그 파일이 쓰던 export와 의존성만 지우면
결과는 신중함이 아니라 깨진 중간 상태다.
연쇄를 설명하는 바로 그 문서가
수정 단위는 연쇄를 고려하지 않는다.
파일 삭제를 허용하지 않을 때는 그 파일 때문에 보고된 항목도
함께 건너뛰는 편이 연쇄 모델과 일관된다.

## 기억할 원칙

### 쓰지 않는다는 판정은 진입점 목록에 대한 판정이다

Knip이 “쓰지 않는다”고 말할 때 그 뜻은
“내가 아는 진입점에서 닿지 않는다”다.
코드에 대한 사실이 아니라 진입점 목록에 대한 사실이다.
그래서 결과가 이상할 때 고칠 대상은 결과가 아니라 진입점 목록이고,
결과를 숨기는 모든 방법은 다음 오탐을 예약하는 일이다.
이 원칙은 죽은 코드 탐지 전반에 통한다.
커버리지 도구가 “실행되지 않았다”고 말할 때도
그것은 코드가 아니라 테스트가 무엇을 실행했는지에 대한 판정이다.

### 정리는 여러 도구가 번갈아 수렴시키는 과정이다

파일 사이를 보는 도구와 파일 안을 보는 도구는 서로의 결과를 바꾼다.
한쪽이 지우면 다른 쪽에 새 결과가 생긴다.
그래서 정리는 한 번의 명령이 아니라
보고 건수가 더 줄지 않을 때까지 도는 반복이고,
그 사이마다 타입 검사와 테스트가 깨지지 않았는지 확인해야 한다.
한 번에 한 유형씩 정리하고 정리한 유형만 게이트로 올리는 문서의 점진 도입 방식은
이 반복을 팀의 속도에 맞춰 나누는 방법이다.

---

[^astegmaier]: <https://news.ycombinator.com/item?id=47183378>

[^jayu_dev]: <https://news.ycombinator.com/item?id=47210275>

[^silverwind]: <https://news.ycombinator.com/item?id=47171472>

[^skybrian]: <https://news.ycombinator.com/item?id=47176995>

[^e1g]: <https://news.ycombinator.com/item?id=47170751>
