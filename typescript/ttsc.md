# ttsc — TypeScript-Go 기반 컴파일러 도구 모음

<https://ttsc.dev/>

<https://github.com/samchon/ttsc>

HN 토론: <https://news.ycombinator.com/item?id=48004293> (2점, 8개 댓글)

## 소개

ttsc는 “Compile-powered TypeScript without the wait”를 표방하는 TypeScript-Go 기반의
독립형(standalone) 컴파일러 도구 모음이다.
Microsoft의 `@typescript/native-preview`(TypeScript-Go) 위에 구축되어 Go 네이티브 속도의
컴파일을 제공하면서, 플러그인 우선(plugin-first) 설계와 타입 안전 실행, 그리고 컴파일 오류를
처리하는 린트 엔진을 통합한다.

세 가지 핵심 CLI로 구성된다.

| CLI               | 역할                                             |
| ----------------- | ------------------------------------------------ |
| `ttsc`            | 빌드 / 체크 / 이미트(emit)를 수행하는 컴파일러  |
| `ttsx`            | 실행 전 실제 타입 검증을 수행하는 런타임         |
| `ttscserver`      | 플러그인 진단을 에디터에 노출하는 LSP 서버       |

## CLI 및 기능

### ttsc — 컴파일러

플러그인 지원 빌드, 타입 검사, 코드 이미트를 단일 패스로 처리한다.
Vite, Webpack, Rollup, esbuild, Rspack, Next.js, Farm, Bun 등 9개 번들러와 통합된다.
`ttsc fix` 명령으로 컴파일 오류 수정 사항을 파일에 직접 기록할 수 있다.

### ttsx — 타입 안전 런타임

`tsx`와 유사한 경험을 제공하되, 실행 전 진정한 타입 검사를 수행하는 점이 다르다.
기존 `tsx`나 `ts-node`가 타입 검사를 생략하고 transpile-only 방식으로 실행하는 것과
대비된다.

### ttscserver — LSP 서버

플러그인 진단 결과를 에디터에 표시하는 Language Server Protocol 서버다.
빌드 단계와 에디터 단계가 동일한 플러그인 계약(contract)을 공유하므로, 개발 환경
전반에서 일관된 오류 메시지를 얻을 수 있다.

### @ttsc/lint — 린트 엔진

140개 규칙을 내장하며, ESLint 스타일의 Wadler 형식 리플로우를 지원한다.
컴파일 오류를 린트 스트림으로 통합하여 단일 파이프라인에서 처리한다.
GitHub에서는 “20x faster TS lint integrated into compiler”로 소개한다.

## 저장소 현황

GitHub 저장소의 언어 구성은 Go 55.4%, TypeScript 34.9%, MDX 6.0%이다.
별(star) 136개, 포크 3개로 초기 단계의 프로젝트다.
개발자는 typia와 nestia 등 TypeScript 생태계 도구로 알려진 Jeongho Nam(samchon)이다.
라이선스는 MIT다.

### 공식 플러그인

| 플러그인       | 기능                               |
| -------------- | ---------------------------------- |
| typia          | 런타임 검증자, JSON, LLM 도구 생성 |
| nestia         | NestJS 라우트 자동 생성            |
| `@ttsc/banner` | JSDoc 배너 삽입                    |
| `@ttsc/paths`  | `tsconfig` 경로 별칭 해석          |
| `@ttsc/strip`  | 디버그 코드 제거                   |

## 분석

### TypeScript-Go를 기반으로 선택한 이유

Microsoft는 2025년 TypeScript 컴파일러를 Go로 재작성하는 프로젝트를 공개했다.
Go로 재작성한 컴파일러는 기존 JavaScript 구현 대비 10배 이상의 성능 향상을 목표로 한다.
ttsc는 이 네이티브 컴파일러 위에 올라탐으로써 V8 콜드 스타트 없이 Go 런타임의 속도를
직접 활용한다.

### 플러그인 우선 아키텍처

기존 TypeScript 생태계에서 플러그인은 컴파일 단계, 번들 단계, 에디터 단계마다 서로 다른
인터페이스를 구현해야 했다.
ttsc는 “빌드, 실행, 편집기가 동일한 플러그인 계약을 공유한다”는 원칙을 중심 아키텍처로
삼는다.
TypeScript AST와 Checker를 Go 컴파일러와 JavaScript 플러그인 디스크립터 사이에서 공유하는
방식으로 이를 구현한다.

이 아키텍처의 실질적 차이는 HN에서 oxlint와의 비교 질문에 대한 답변에서 잘 드러난다[^esafak].
oxlint는 TypeScript 컴파일러와 독립된 별도 프로그램이어서 컴파일 이후에 실행해야 하지만,
`@ttsc/lint`는 컴파일러 내부의 플러그인이므로 컴파일 중에 위반 사항이 감지된다.
“컴파일과 린트를 별도 단계로 실행한다”와 “컴파일 중에 린트가 함께 수행된다”는 파이프라인
설계의 근본적 차이다.

### ttsx가 타입 검사를 포함하는 이유

`tsx`와 `ts-node --transpile-only`는 빠른 실행을 위해 타입 검사를 건너뛴다.
이는 타입 오류가 있는 코드를 런타임에서 실행하게 만들어, 개발 중 타입 시스템의 보호막을
무력화한다.
`ttsx`는 TypeScript-Go의 빠른 검사 속도를 이용해 실행 전 타입 검사 비용을 현실적인
수준으로 낮추려 시도한다.

HN에서 k-taro56은 “Node.js가 이미 TypeScript를 직접 실행할 수 있는데 왜 ttsc가
필요한가”라고 반문했다[^k-taro56].
autobe는 현재 Node.js의 네이티브 TS 지원은 플러그인을 지원하지 않고 타입 검사도
수행하지 않는다는 점을 들어 차별점을 명확히 했다.
k-taro56은 한 발 더 나아가 “런타임에서 타입 검사가 정말 필요한가? Python처럼 그냥
동작하기만 하면 되는 게 아닌가”라는 철학적 의문을 던졌다[^k-taro56-2].
autobe의 답은 ttsx의 존재 이유를 드러낸다: `typia`처럼 컴파일 타임 타입 정보를 런타임
검증 코드로 변환하는 라이브러리를 개발하려면, 편의 런타임 환경에서도 타입 검사가
필수라는 것이다[^autobe].

## 비평

### 강점

TypeScript-Go라는 거대한 성능 도약 위에 실용적인 도구 레이어를 빠르게 구축했다는 점이
인상적이다.
플러그인 계약의 통일은 도구 체인 파편화라는 TypeScript 생태계의 오랜 문제를 정면으로
겨냥한다.
`ttsc fix`처럼 컴파일러가 수정까지 수행하는 방향은 AI 코드 편집 보조 흐름과도 자연스럽게
맞닿는다.

### 약점 및 한계

`@typescript/native-preview`는 아직 프리뷰(preview) 단계이며, 공식 TypeScript 릴리스와
동기화 속도 및 호환성이 불분명하다.
ttsc가 제공하는 플러그인 API가 Microsoft 공식 컴파일러의 확장 모델과 어떻게 정렬될지는
미지수다.
typia처럼 강력한 플러그인은 유용하지만, 특정 런타임 검증 라이브러리에 대한 의존성이
생태계 록인(lock-in)으로 이어질 수 있다.

### 관점의 공백

공식 `tsc`의 Language Plugin API와 ttsc 플러그인 계약의 장기적 수렴 가능성에 대해 문서가
침묵한다.
Vite나 esbuild 같은 번들러들이 이미 자체 TypeScript 통합을 발전시키고 있는 상황에서,
ttsc의 번들러 통합 레이어가 차별점을 유지할 수 있는지 근거가 부족하다.

## 인사이트

### 컴파일러 재작성이 열어주는 “레이어 경쟁”의 시대

TypeScript-Go는 단순한 성능 개선이 아니라 생태계 지형을 바꾸는 사건이다.
기존에는 컴파일러 자체가 느렸기 때문에, 번들러들이 타입 검사를 생략하고 transpile-only로
동작하는 것이 합리적인 트레이드오프였다.
TypeScript-Go가 컴파일 비용을 10분의 1 이하로 낮추면 이 트레이드오프의 전제가 무너진다.

이 변화는 도구 생태계 전반에 “레이어 경쟁”을 촉발한다.
번들러, 린터, 런타임, 에디터 플러그인 각각이 “이제 타입 검사를 포함할 수 있다”고 주장하며
기능 경계를 넓히려 할 것이다.
ttsc는 그 경쟁에서 컴파일러 계층을 장악하고 나머지를 흡수하려는 전략적 포지셔닝이다.
이런 상황은 Go 재작성 이후 1-2년 안에 도구 생태계가 상당 부분 재편될 가능성을 시사한다.

### 플러그인 계약 통일이 개발자 경험(DX)에 미치는 영향

오늘날 TypeScript 개발자는 ESLint 플러그인, babel 플러그인, webpack 로더, tsc 트랜스포머를
따로따로 설정하고 유지한다.
동일한 변환 의도가 네 벌의 구현으로 중복되는 이 상황은 유지 비용과 동작 불일치라는 이중
부담을 만든다.
ttsc의 “단일 플러그인 계약”은 이 파편화를 제거하려는 시도다.

역사적으로 Babel이 플러그인 계약의 단일화로 컴파일러 생태계를 한동안 지배했던 선례가
있다.
그러나 Babel은 타입 정보 없이 AST만 다루었기 때문에 타입 시스템과의 통합이 한계였다.
ttsc는 TypeScript AST와 Checker를 플러그인에 직접 노출함으로써 Babel이 할 수 없었던
타입 인식(type-aware) 변환을 하나의 계약 안에 담으려 한다.
이것이 성공한다면 개발자 경험의 단순화는 상당히 크고, 생태계 흡인력도 강해진다.

### “타입 안전 실행”이 정상화될 때 달라지는 것들

`tsx`나 `ts-node --transpile-only`가 빠르게 정착한 이유는 타입 검사 비용이 너무 높았기
때문이다.
그 결과 TypeScript를 사용하면서도 런타임 직전에는 타입 보호가 없는 아이러니한 상황이
표준 워크플로우가 되었다.
`ttsx`가 “실행 전 타입 검사”를 현실적인 속도로 제공한다면, 이 타협이 사라진다.

타입 검사가 실행 경로에 포함되면 개발 루프의 성격이 바뀐다.
런타임 오류가 발생하기 전에 컴파일 단계에서 더 많은 오류가 잡히고, 스크립트 실행용 코드에도
타입 규율이 유지된다.
나아가 CI 파이프라인에서 타입 검사를 별도 단계로 분리할 필요가 줄고, 빌드 파이프라인이
단순해진다.
이는 “TypeScript를 쓰는 이유”가 런타임 이전에 실질적으로 작동하게 되는, 언어 설계 의도와
실제 사용 방식의 재정렬이다.

---

[^k-taro56]: <https://news.ycombinator.com/item?id=48005982>
[^k-taro56-2]: <https://news.ycombinator.com/item?id=48006303>
[^autobe]: <https://news.ycombinator.com/item?id=48006372>
[^esafak]: <https://news.ycombinator.com/item?id=48005319>
