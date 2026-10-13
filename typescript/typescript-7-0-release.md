# TypeScript 7.0 정식 출시: Go로 다시 쓴 네이티브 컴파일러

원문: <https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/>

HN 토론: <https://news.ycombinator.com/item?id=48833715> (720점, 301개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/txmyod/announcing_typescript_7_0> (101점, 37개 댓글)

GN 토론: <https://news.hada.io/topic?id=31249>

## 요약

Microsoft TypeScript 팀의 Daniel Rosenwasser가 2026년 7월 8일
TypeScript 7.0을 정식 발표했다.
핵심은 JavaScript로 작성됐던 컴파일러를 Go로 옮긴 네이티브 포트로,
팀은 이를 “10배 빠른 네이티브 포트”라고 소개하고
글을 “TypeScript 툴셋의 네이티브 시대”라는 문장으로 맺는다.
포트는 원래 코드베이스의 구조와 로직을 최대한 충실하게 유지하며 새로 쓴
것이고,
네이티브 코드 속도와 공유 메모리 멀티스레딩, 여러 최적화가 더해져
전체 빌드에서 보통 8~12배 빨라진다고 한다.
설치는 이전과 같이 `npm install -D typescript`이며,
에디터 지원은 새로 도입한 LSP(Language Server Protocol) 기반 언어 서버로
제공된다.

성능 수치는 큰 오픈소스 프로젝트에서 6.0과 7.0의 전체 빌드를 비교한
것이다.

| 프로젝트   | TypeScript 6 | TypeScript 7 | 배수   | 메모리 변화 |
| ---------- | ------------ | ------------ | ------ | ----------- |
| vscode     | 125.7초      | 10.6초       | 11.9배 | -18%        |
| sentry     | 139.8초      | 15.7초       | 8.9배  | -6%         |
| bluesky    | 24.3초       | 2.8초        | 8.7배  | -26%        |
| playwright | 12.8초       | 1.47초       | 8.7배  | -11%        |
| tldraw     | 11.2초       | 1.46초       | 7.7배  | -15%        |

이 표는 기본값인 `--checkers 4`로 잰 것이고,
같은 기계에서 `--checkers 8`로 돌리면 VS Code는 7.51초(16.7배),
Sentry는 12.08초(11.6배)까지 줄어든다.
에디터에서는 VS Code 코드베이스의 오류 있는 파일을 열고 첫 오류가 보이기까지
약 17.5초 걸리던 것이 1.3초 미만으로 줄었다.

팀은 1년 넘게 사내외 대규모 코드베이스에서 7.0을 시험했다고 밝힌다.
Microsoft 안에서는 Loop, Office, PowerBI, Teams, Xbox가,
밖에서는 Bloomberg, Canva, Figma, Google, Linear, Notion, Sentry, Slack,
Vanta, Vercel, VoidZero 등이 참여했다.
Slack은 머지 큐 시간의 40%를 없애고 CI 타입 체크를 약 7.5분에서 1.25분으로
줄였으며,
언어 서버가 너무 느려 사실상 쓰지 못하던 에디터 타입 체크를 다시 로컬에서
할 수 있게 됐다고 한다.
Vanta는 가장 큰 프로젝트에서 최대 9배,
Microsoft News Services 팀은 CI 대기 시간을 월 400시간 줄였고,
Canva는 에디터에서 첫 오류가 보이기까지의 시간이 약 58초에서 4.8초로 줄었다.
새 언어 서버는 6.0에 비해 실패하는 명령이 80% 넘게,
서버 크래시가 60% 넘게 줄었다고 한다.

7.0은 API를 제공하지 않는다.
7.1에서 새로운, 그리고 기존과 다른 API가 나올 예정이고,
그때까지 typescript-eslint처럼 컴파일러에 프로그래밍 방식으로 접근해야 하는
도구는 6.0을 함께 써야 한다.
이를 위해 `tsc6` 실행 파일을 제공하고 6.0 API를 다시 내보내는
`@typescript/typescript6` 호환 패키지가 나왔다.
도구가 `typescript`를 peer dependency로 직접 가져오기 때문에 팀은 npm 별칭으로
두 버전을 나란히 두는 방법을 권한다.

```json
{
  "devDependencies": {
    "@typescript/native": "npm:typescript@^7.0.2",
    "typescript": "npm:@typescript/typescript6@^6.0.2"
  }
}
```

이렇게 두면 `npx tsc`는 7.0으로 돌고,
`typescript`를 가져오는 도구는 6.0 API를 받는다.
그동안 주간 850만 회 넘게 내려받힌 야간 빌드 패키지
`@typescript/native-preview`는 곧 `typescript@next` 태그로 옮겨 간다.

병렬화 제어로는 세 플래그가 실험적으로 추가됐다.
`--checkers`는 타입 체커 작업자 수를 정하며 기본값은 4다.
작업자들은 같은 입력이면 파일을 항상 같은 방식으로 나눠 같은 결과를 내지만,
드물게 작업자 수를 바꾸면 순서에 의존하는 결과가 드러날 수 있어
팀은 빌드 환경마다 같은 수를 쓰는 방안을 권한다.
`--builders`는 `--build`에서 동시에 빌드할 프로젝트 참조 수를 정하고
`--checkers`와 곱해지므로,
`--checkers 4 --builders 4`면 체커가 최대 16개까지 동시에 돈다.
`--singleThreaded`는 파싱, 타입 체크, 출력까지 모두 단일 스레드로 돌린다.
워치 모드는 VS Code가 쓰던 Parcel의 C++ 파일 감시기를 최소한의 어셈블리
보조 코드와 함께 Go로 옮겨 새로 만들었다.
Go 표준 라이브러리에는 파일 감시 API가 없고,
주기적으로 파일을 훑는 방식은 `node_modules`가 큰 프로젝트에서 너무 비쌌기
때문이다.

7.0은 6.0과 타입 체크 및 명령행 동작이 호환되도록 만들어졌다.
6.0에서 `stableTypeOrdering`을 켜고 `ignoreDeprecations` 없이 깨끗하게
컴파일되는 코드는 7.0에서도 같게 컴파일된다.
대신 6.0의 새 기본값을 그대로 쓰고 6.0에서 폐기 예고된 설정은 모두 오류가
된다.
`strict`는 `true`, `module`은 `esnext`,
`noUncheckedSideEffectImports`는 `true`가 기본이며,
`rootDir`은 `./`, `types`는 빈 배열이 기본값이다.
팀은 `rootDir`과 `types` 변화가 가장 놀라울 수 있다며,
`tsconfig.json`이 `src` 밖에 있으면 `rootDir`을,
전역 선언에 기대는 프로젝트는 `types`를 명시하라고 안내한다.
`target: es5`, `downlevelIteration`, `moduleResolution: node10`과 `classic`,
AMD·UMD·SystemJS 모듈, `baseUrl`은 더 이상 지원되지 않는다.
템플릿 리터럴 타입 추론은 이제 유니코드 코드 포인트를 보존해 이모지를
서로게이트 쌍으로 쪼개지 않는데,
UTF-16 단위를 일부러 모델링한 문자열 길이 유틸리티에는 호환성을 깨는 변경이다.
JavaScript 지원도 `.ts` 분석과 일관되게 다시 손봐서,
`@enum`이나 Closure 스타일 함수 타입 같은 JSDoc 특수 처리가 사라졌다.

VS Code에는 전용 확장이 있고 몇 주 안에 VS Code 자체에 들어갈 예정이며,
Visual Studio는 작업 공간에 따라 자동으로 7.0을 켠다.
다만 Vue, MDX, Astro, Svelte처럼 Volar 같은 도구가 TypeScript를 자체
컴파일러와 언어 서비스에 넣어 쓰는 워크플로는 안정적인 API가 없어 당분간
6.0을 써야 한다.
팀은 이를 일시적인 문제로 보고 해당 프로젝트 관리자들과 함께 해결하겠다고
약속하며,
Angular 프로젝트는 CLI 오류 검사에 7.0을, 에디터 지원에 6.0을 쓰는 조합을
권한다.
7.0 이후에는 새 기능, 사용성 개선, 새 API 작업으로 돌아가며
3~4개월마다 기능 릴리스를 낸다는 이전 주기를 이어 간다.

## 분석

### “충실한 포팅”이라는 전략이 재작성 리스크를 최소화한다

대규모 컴파일러를 다른 언어로 다시 쓰는 프로젝트는 흔히 이
과정에서 새로운 설계를 시도하려는 유혹에 빠지고, 그 결과
기존 동작과의 미묘한 차이(behavioral drift)가 누적되어 생태계
전체가 깨지는 위험을 안는다. TypeScript 팀이 “기존 로직을
최대한 충실하게” 옮기는 전략을 택한 것은 이런 위험을 의도적으로
회피한 선택이다. 새로운 언어가 주는 성능 이점(네이티브 컴파일,
공유 메모리 멀티스레딩)은 그대로 취하되, 타입 체크 알고리즘
자체의 동작은 바꾸지 않음으로써 수백만 개의 기존 TypeScript
프로젝트가 재작성 이후에도 동일한 타입 오류를 동일하게
보고받도록 보장한다.
HN에서 dimitropoulos는 이 프로젝트의 진짜 이야기는 두 개의 코드베이스를
동시에 살려 둔 팀에 있다고 평가했다.[^dimitropoulos]
Rust가 아니라 Go를 고른 이유는 afdbcreid가 정리했다.
팀이 원한 것은 재작성이 아니라 버그까지 그대로 옮기는 파일 단위 번역이었고,
빌림 검사기와 GC 부재 때문에 순환 구조가 많은 컴파일러를 Rust로 옮기면
구조를 바꿔야 했을 것이라는 설명이다.[^afdbcreid]

Lobste.rs에서는 bakkot이 이득의 대부분이 멀티스레딩에서 나온다고 보면서도,
단일 스레드만으로도 3배 빠르다는 점에 놀랐다고 덧붙였다.[^bakkot]
mort는 기존 tsc가 V8이 JIT 컴파일을 마칠 때까지는 빨라지지 않으니,
매번 코드와 함께 컴파일러까지 컴파일하는 셈이었다고 짚었다.[^mort-jit]
fanf는 더 촘촘한 객체와 객체 간 포인터 감소 같은 메모리 배치가 또 다른
이유이며,
그래서 C#이 아니라 Go를 골랐다고 설명했다.[^fanf]
jakebailey는 왜 기존 컴파일러를 Wasm으로 컴파일하지 않았느냐는
질문에,
TS로 쓴 코드를 Wasm으로 바꿔도 결국 같은 인터프리터 위에서 돌 뿐이고
스레딩이 큰 이유였다고 답했다.[^jakebailey-wasm]

### 6.0을 “브릿지 릴리스”로 설계한 것은 생태계 전환 비용을 미리 분산시킨 결정이다

6.0이 이미 7.0과 동일한 기본값(`strict: true`, `module: esnext`,
`types: []`)과 `--stableTypeOrdering` 같은 호환 플래그를
도입해 뒀다는 점은, 이번 7.0 출시가 갑작스러운 단절이 아니라
오랫동안 준비된 계획의 마지막 단계였음을 보여준다. 생태계
전체가 한 번에 새 기본값과 새 컴파일러를 동시에 받아들여야
했다면 마이그레이션 비용이 훨씬 컸을 것이다. 기본값 변경(6.0)과
런타임 교체(7.0)를 시간차를 두고 분리함으로써, 각 단계에서
발생하는 문제를 독립적으로 진단하고 대응할 수 있게 만들었다.

HN에서 ricardobeat은 이 이전이 AI가 도울 수 있기 훨씬 전에 시작돼
수백만 사용자를 둔 프로젝트답게 천천히 신중하게 진행됐다고 평가하며,
하룻밤 사이에 이뤄진 Bun의 Rust 이전과 대비했다.[^ricardobeat]
다만 spartanatreyu는 typescript-go 저장소에서 Copilot이 커밋 수 2위
사용자라며,
초기 포팅은 자동화로, 이후 개발자와 LLM이 손을 댔다고 지적했다.[^spartanatreyu]
“신중한 사람의 이전 대 성급한 AI의 이전”이라는 대비는 생각만큼 깔끔하지
않다.

### 프로덕션 성능 수치를 전면에 내세우는 것은 신뢰 확보 전략이다

VS Code, Slack, Bluesky 같은 실제 대규모 프로젝트의 구체적인
초 단위 수치를 제시한 것은 단순한 벤치마크 그래프보다 훨씬
설득력이 크다. 컴파일러 재작성처럼 리스크가 큰 변경일수록,
추상적인 “N배 빠르다”는 주장보다 이름이 알려진 실제 프로젝트가
이미 프로덕션에서 검증했다는 사실이 채택을 망설이는 팀들에게
더 강한 신호로 작동한다. 이는 대규모 인프라 교체를 발표할 때
반복되는 수사적 전략이다.

### 자체 호스팅을 포기한 드문 방향 전환이다

Lobste.rs에서 lorddimwit은 언어가 자체 호스팅 컴파일러에서 그렇지 않은
컴파일러로 옮겨 가는 일은 드물고 보통은 반대 방향이라고 짚었다.[^lorddimwit]
가장 많은 지지를 받은 mort의 답은 모든 언어가 컴파일러를 쓰기에 좋은 것은
아니며,
자체 호스팅은 언어를 컴파일러 작성에 유리한 쪽으로 진화시키는 압력이 되는데
그 방향이 늘 옳지는 않다는 것이었다.[^mort-selfhost]
pie_flavor는 반대로 언어 설계자가 어떤 식으로든 자기 언어를 직접 써 봐야
한다며,
컴파일러가 그 가장 쉬운 방법이라고 했다.[^pie_flavor]

TypeScript의 경우 이 우려는 상대적으로 작다.
컴파일러는 Go로 떠났지만,
VS Code를 비롯해 같은 회사 안에 TypeScript로 쓴 거대한 제품이 많다.
그래도 한 가지 변화는 남는다.
이제 TypeScript 컴파일러 내부를 고치려면 Go를 읽어야 하고,
타입 시스템을 가장 잘 아는 사용자들이 컴파일러 기여에서 한 걸음 멀어진다.

## 비평

### “임베디드 언어 워크플로 미지원”은 사소한 예외가 아니라 실질적인 채택 장벽이다

발표 글은 Vue, MDX, Astro, Svelte에서 TypeScript 7을 아직 쓸 수 없다는 사실을
분명히 적고,
일시적인 문제로 보고 Volar 같은 도구의 관리자들과 해결하겠다고 약속한다.
하지만 약속에는 시점이 없다.
이 프레임워크들은 프런트엔드 생태계에서 결코 주변적이지 않은데,
이를 쓰는 팀은 언제까지 6.0과 7.0을 함께 운영해야 할지 알 수 없다.
Angular에 권한 조합, 즉 CLI는 7.0이고 에디터는 6.0인 구성도
에디터가 보여 주는 오류와 CI가 보고하는 오류가 서로 다른 컴파일러에서
나온다는 뜻이다.

### 컴파일러 API 의존 도구 생태계의 전환 비용이 과소평가됐다

`@typescript/typescript6` 호환 패키지로 typescript-eslint 같은
도구가 당분간 6.0의 API에 의존한 채 버틸 수 있다는 설명은,
거꾸로 말하면 컴파일러 API에 의존하는 모든 서드파티 도구가
7.1까지는 새 네이티브 컴파일러의 성능 이점을 전혀 누리지 못한다는
뜻이다.
발표 글은 7.1의 API가 기존과 “다를” 것이라고 분명히 적는다.
그렇다면 이 도구들은 7.1을 기다렸다가 버전만 올리는 것이 아니라,
새 API에 맞춰 통합 부분을 다시 써야 한다.
린터, IDE 플러그인, 코드 생성 도구, 테스트 러너가 모두 같은 일을 해야 하는데,
글은 새 API가 어떤 모양일지에 대해서는 아무것도 말하지 않는다.

HN에서 afdbcreid는 Rust로 다시 썼다면 API를 쉽게 노출할 수 있었을 텐데
팀은 아직 방법을 논의하며 7.1로 미루고 있다고 짚었다.[^afdbcreid]
jakebailey는 Wasm 빌드를 곧 내고 싶지만,
사람들이 말하는 Wasm이 Monaco용 LSP인지, 브라우저용 API인지,
지원하지 않는 플랫폼용 CLI인지 분명하지 않다고 밝혔다.[^jakebailey]
herpdyderp는 ESLint 플러그인 간 의존성 불일치 때문에 아직 올리지 못한다고
했고,[^herpdyderp]
settled는 ts-jest가 바로 동작하지 않아 나란히 설치하는 우회로를 써야 했다며
주요 릴리스라면 테스트 도구 지원에 더 확신을 줘야 한다고 적었다.[^settled]
aabbcc1241은 ts-node가 TypeScript 7에서 동작하지 않아 개발 중에 타입 검사와
함께 스크립트를 직접 실행할 방법을 찾지 못했다고 했다.[^aabbcc1241]
skybrian은 Deno가 import 해석을 Rust 쪽에서 처리하며 컴파일러 API에 기대므로
API가 준비될 때까지 올리기 어려울 것이라고 봤고,[^skybrian]
ameliaquining은 Deno에 이미 부분적이고 불안정한 TypeScript 7 지원이 있다고
덧붙였다.[^ameliaquining]
wartywhoa23은 공식 확장이 open-vsx에 없어 VSCodium 사용자는 비공식 포크를
기다려야 한다고 지적했다.[^wartywhoa23]

반대로 영향이 없는 도구도 분명히 해 둘 필요가 있다.
DanRosenwasser는 esbuild는 TypeScript에 전혀 의존하지 않아
문제가 없고,
tsdown은 `--isolatedDeclarations`를 쓰지 않는다면 6.0을 나란히 설치하면 된다고
답했다.[^DanRosenwasser]
결국 영향은 타입 정보를 실제로 읽는 도구에 집중된다.

### 벤치마크로 제시된 프로젝트들이 전형적인 워크로드를 대표하는지 불분명하다

VS Code, Sentry, Bluesky, Playwright는 모두 대규모이고 활발히
관리되는 오픈소스 프로젝트다. 이런 프로젝트들은 이미 타입 구조가
비교적 정돈되어 있고 최신 TypeScript 관행을 따를 가능성이 높다.
반면 레거시 코드가 누적된 중소규모 사내 프로젝트, 특히 `types`
기본값 변경이나 `rootDir` 추론 방식 변경에 영향을 받는 프로젝트가
동일한 배수의 성능 향상을 얻을지, 아니면 마이그레이션 과정에서
예상치 못한 타입 오류가 무더기로 드러나 초기에는 오히려 생산성이
저하될지는 이 벤치마크만으로 판단할 수 없다.
실제로 HN에서 herpdyderp는 6.0 대비 4배,[^herpdyderp-4x]
brikym은 3~3.5배 정도라고 보고했다.[^brikym]
발표된 표는 큰 오픈소스 코드베이스를 기본값 `--checkers 4`로 잰 수치이고,
코어가 적은 CI 러너나 작은 프로젝트에서는 배수가 그보다 작을 수 있다.

메모리 수치도 다시 읽어 볼 만하다.
Lobste.rs에서 peter-leonov는 JS와 Go의 메모리 차이가 10% 안팎에 그친다는 데
놀랐고,[^peter-leonov]
fanf는 타입 체커 작업자들이 공유 가변 데이터 대신 같은 일을 반복하므로
객체는 작아져도 개수가 늘어난 탓일 것이라고 봤다.[^fanf-memory]
발표 글도 작업자들이 공통 작업을 일부 중복한다고 인정한다.
속도를 사기 위해 메모리 절감 일부를 되돌려 쓴 설계이고,
`--checkers`를 늘리면 그 대가는 더 커진다.

## 인사이트

### 컴파일러 재작성의 성공 여부는 결국 하위 호환성 정책에 달려 있다

TypeScript 7.0의 실질적 성패는 Go 네이티브 포트의 성능 수치가
아니라, 기존 생태계(6.0에 의존하는 도구, 임베디드 언어 플러그인,
컴파일러 API 소비자)가 얼마나 매끄럽게 전환하는지에 달려 있다.
이는 Python 2에서 3으로의 전환, 혹은 여러 대규모 언어 런타임
교체 사례에서 반복적으로 확인된 패턴이다. 새 런타임 자체의
기술적 우수성은 전환의 필요조건일 뿐 충분조건이 아니며, 실제
채택 속도는 하위 호환 계층의 완성도와 유지 기간에 의해 결정된다.
TypeScript 팀이 6.0을 브릿지로 설계하고 `@typescript/typescript6`
호환 패키지를 제공한 것은 이 교훈을 이미 반영한 결과로 보이지만,
7.1의 새 API가 실제로 나오기 전까지는 이 하위 호환 전략의
성공 여부를 판단할 수 없다.
HN에서 lelele가 “소프트웨어를 다시 쓰는 것은 최악의 전략적 실수”라는
Joel Spolsky의 글을 꺼내자,[^lelele]
sharlos201068은 이번 일은 재작성이 아니라 JS 로직을 Go로 거의 일대일
번역한 것이라고 답했다.[^sharlos201068]
Joel의 경고가 겨냥한 것은 동작을 다시 발명하는 재작성이고,
TypeScript 팀은 동작을 그대로 두고 런타임만 바꾸는 방식으로 그 함정을 피했다.

### 병렬 타입 체크는 결정성을 설정값으로 바꿔 놓는다

발표 글의 작은 단서 하나가 운영에서는 크게 작용할 수 있다.
`--checkers` 수를 바꾸면 드물게 순서에 의존하는 결과가 드러날 수 있다는
문장이다.
지금까지는 같은 코드와 같은 TypeScript 버전이면 결과가 같았는데,
이제는 체커 수라는 설정이 결과의 일부가 된다.
팀이 빌드 환경마다 같은 수를 쓰라고 권하는 이유다.

이는 개발자 노트북과 CI 러너의 코어 수가 다른 흔한 상황과 정면으로 부딪힌다.
노트북에서는 체커를 8개로 늘려 빠르게 돌리고 CI 러너에서는 메모리 때문에
1~2개로 줄이고 싶어지는데,
그러면 두 환경이 드물게나마 다른 오류를 낼 수 있다.
HN에서 herpdyderp가 CI에서는 6.0을 쓰고 로컬에서만 7.0을 쓰면 로컬 결과가
CI와 어긋난다고 경고한 것과 같은 종류의 문제다.[^herpdyderp-ci]

병렬 빌드 시스템이 오래전에 겪은 일이기도 하다.
재현 가능한 빌드는 입력뿐 아니라 실행 환경의 병렬도까지 고정해야 성립한다.
TypeScript 7을 도입하는 팀은 `tsconfig.json`의 옵션만큼이나
`--checkers` 값을 저장소에 고정된 설정으로 다뤄야 한다.

### “10배 빠른 컴파일러”는 개발자 워크플로의 병목을 다른 곳으로 옮길 뿐이다

타입 체크가 10배 빨라지면, 그동안 컴파일 대기 시간에 가려져
있던 다른 병목(번들링, 테스트 실행, CI 파이프라인의 다른 단계)이
상대적으로 더 크게 부각된다. Slack이 CI 타입 체크를 7.5분에서
1.25분으로 줄였다는 사례는 인상적이지만, 전체 CI 파이프라인의
총 소요 시간이 동일한 비율로 줄었는지는 언급되지 않는다. 이는
성능 개선이 국소적으로 극적일수록, 그 개선이 실제 체감 생산성
향상으로 이어지려면 주변 시스템(빌드 도구, 배포 파이프라인)도
함께 병목을 해소해야 한다는 일반적인 시스템 최적화의 원리를
보여준다. 컴파일러가 더 이상 병목이 아니게 된 조직에서는, 다음
최적화 대상이 무엇인지에 대한 새로운 질문이 제기될 것이다.
HN에서 stymaar는 실무에서 tsc가 rustc보다 자신을 훨씬 더 자주 괴롭혔는데도
웹에서는 rustc가 느리다는 불평이 훨씬 많다는 점이 늘 놀랍다고
적었다.[^stymaar]
notnullorvoid는 큰 프로젝트에서는 증분 빌드나 프로젝트 참조로 성능 문제를
피할 수 있었는데 대부분 설정하지 않았을 뿐이고,
TS7은 그런 옵션을 쓸 이유를 줄여 줄 것이라고 봤다.[^notnullorvoid]
dimitropoulos는 여기서 한 걸음 더 나아가 제번스 역설(Jevons Paradox)을
언급하며,
컴파일이 빨라지면 예전에는 부담스러웠던 고차 타입 같은 패턴이 쓸 만해져
효율 개선분을 다시 써 버릴 수 있다고 지적했다.[^dimitropoulos-jevons]
Lobste.rs의 lilac이 짚었듯 빨라진 것은 컴파일러이지 컴파일된 코드가
아니다.[^lilac]
사용자가 체감하는 제품 속도는 그대로이고,
바뀌는 것은 개발 피드백 루프의 길이뿐이다.

### 언어 툴체인의 “네이티브화”는 개발자 도구 전반의 장기 추세를 다시 확인시킨다

TypeScript의 Go 포팅은 최근 몇 년간 반복되어 온 흐름, 즉 스크립팅
언어로 작성된 개발자 도구를 시스템 프로그래밍 언어로 다시 작성해
극적인 성능 향상을 얻는 패턴의 연장선에 있다. Babel 대신 esbuild와
SWC가 등장하고, Webpack 대신 Rspack과 Turbopack이 등장한 것과
같은 궤적이다. 이런 흐름이 시사하는 것은, 개발자 도구 생태계가
이제 “기능의 완성도”를 넘어 “실행 속도”를 핵심 경쟁 축으로
삼는 단계에 들어섰다는 점이다. 다만 이 흐름에는 대가도 따른다.
도구의 핵심부가 JavaScript/TypeScript가 아닌 언어로 옮겨가면서,
해당 생태계에 기여하려는 개발자는 이제 Go나 Rust까지 이해해야
하는 진입 장벽이 새로 생긴다. 편의성과 접근성이라는 오픈소스
생태계의 오래된 가치와, 성능이라는 새로운 요구 사이의 긴장은
앞으로도 계속될 것으로 보인다.
흥미롭게도 그 반대 방향의 실험도 나왔다.
HN에서 jeswin은 1년 동안 tsgo를 다시 TypeScript로 포팅해 왔고,
지금은 원래 tsc보다 2배, tsgo보다 10배 느리지만
C#과 Rust 타깃으로 스스로를 컴파일하면 tsgo에 가까워질 것이라고
소개했다.[^jeswin]
네이티브화의 비용이 기여 장벽이라면,
같은 코드를 여러 언어로 내보내는 도구가 그 장벽을 다시 낮추려는 시도로 이어진다.

---

[^dimitropoulos]: <https://news.ycombinator.com/item?id=48833856>

[^afdbcreid]: <https://news.ycombinator.com/item?id=48835691>

[^jakebailey]: <https://news.ycombinator.com/item?id=48835360>

[^herpdyderp]: <https://news.ycombinator.com/item?id=48837022>

[^stymaar]: <https://news.ycombinator.com/item?id=48835299>

[^dimitropoulos-jevons]: <https://news.ycombinator.com/item?id=48834613>

[^bakkot]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_f4gjjh>

[^mort-jit]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_hzv35o>

[^fanf]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_ljk0og>

[^jakebailey-wasm]: <https://news.ycombinator.com/item?id=48835387>

[^ricardobeat]: <https://news.ycombinator.com/item?id=48837325>

[^spartanatreyu]: <https://news.ycombinator.com/item?id=48838983>

[^lorddimwit]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_zlp6ro>

[^mort-selfhost]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_berep5>

[^pie_flavor]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_xcruxd>

[^settled]: <https://news.ycombinator.com/item?id=48838460>

[^aabbcc1241]: <https://news.ycombinator.com/item?id=48923999>

[^skybrian]: <https://news.ycombinator.com/item?id=48836740>

[^ameliaquining]: <https://news.ycombinator.com/item?id=48839010>

[^wartywhoa23]: <https://news.ycombinator.com/item?id=48844819>

[^DanRosenwasser]: <https://news.ycombinator.com/item?id=48838009>

[^herpdyderp-4x]: <https://news.ycombinator.com/item?id=48837031>

[^brikym]: <https://news.ycombinator.com/item?id=48839672>

[^peter-leonov]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_azjecd>

[^fanf-memory]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_u7t4ri>

[^lelele]: <https://news.ycombinator.com/item?id=48845048>

[^sharlos201068]: <https://news.ycombinator.com/item?id=48845457>

[^herpdyderp-ci]: <https://news.ycombinator.com/item?id=48837002>

[^notnullorvoid]: <https://news.ycombinator.com/item?id=48837515>

[^lilac]: <https://lobste.rs/s/txmyod/announcing_typescript_7_0#c_d1xaba>

[^jeswin]: <https://news.ycombinator.com/item?id=48839898>
