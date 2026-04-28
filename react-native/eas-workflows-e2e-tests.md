# EAS Workflows로 Maestro 기반 모바일 E2E 테스트 구성하기

<https://docs.expo.dev/eas/workflows/examples/e2e-tests/>

참고: Maestro GitHub — <https://github.com/mobile-dev-inc/maestro>

## 소개

EAS Workflows는 Expo가 제공하는 클라우드 기반 CI/CD 파이프라인이다.
빌드, 제출(submit), OTA 업데이트, 테스트 등 모바일 앱 라이프사이클 전반을
하나의 매니지드 환경에서 자동화한다.
이 문서는 EAS Workflows에 Maestro를 통합해 풀 리퀘스트마다 모바일 E2E
테스트를 자동 실행하는 방법을 안내한다.

Maestro는 YAML 기반의 선언적 모바일 UI 테스트 프레임워크다.
Appium, Detox 등 기존 도구에 비해 문법이 단순하고 학습 곡선이 낮다는
점이 장점이며, 모바일 위주 스타트업에서 빠르게 채택되고 있다.
문서는 Expo 기본 템플릿(template)을 예제로 사용하지만, 실제 프로덕션
앱에서는 인증, 시드 데이터, 외부 의존성 처리 등 맞춤 작업이 필요함을
명시한다.

가이드의 핵심은 다음 네 가지 산출물이다. `.maestro/` 디렉터리에 두는 YAML
플로우, `eas.json`의 `e2e-test` 빌드 프로필, `.eas/workflows/`에 두는
워크플로우 파일, 그리고 `eas-cli` 또는 PR 이벤트로 트리거되는 실행
경로다.

## 설정 흐름

`.maestro/home.yml`처럼 `appId`, `launchApp`, `assertVisible` 같은
지시어로 테스트 플로우를 작성한다.
`eas.json`에는 `withoutCredentials: true`, `ios.simulator: true`,
`android.buildType: “apk”`로 구성한 `e2e-test` 빌드 프로필을 추가하여
시뮬레이터용 가벼운 바이너리를 생성한다.

`.eas/workflows/e2e-test-android.yml`은 두 잡(job)으로 구성된다.
`type: build` 잡이 안드로이드 APK를 만들고, `type: maestro` 잡이
`needs`와 `outputs.build_id`를 통해 그 산출물을 받아 Maestro 플로우를
실행한다. iOS도 동일한 구조에 플랫폼별 파라미터만 다르다.

## 실행 방법

`npx eas-cli@latest workflow:run .eas/workflows/e2e-test-android.yml`로
수동 실행이 가능하다.
`on.pull_request.branches: ['*']` 트리거를 두면 PR이 열릴 때마다
워크플로우가 자동으로 시작된다.
실행 진행 상황과 결과는 EAS 대시보드(dashboard)에서 확인한다.

## 분석

### 모바일 CI/CD의 수직 통합 전략

EAS Workflows는 빌드(EAS Build), 제출(EAS Submit), 업데이트(EAS
Update), 테스트(Maestro)를 하나의 워크플로우 그래프로 묶는다.
GitHub Actions이나 CircleCI에서 모바일 E2E를 돌릴 때 골치가 되는
시뮬레이터 캐싱, 코드 사이닝(code signing), 머신 풀 관리 문제를
EAS가 단일 벤더 솔루션으로 흡수한다.
이는 Vercel이 Next.js 빌드/배포/엣지 함수를 통합한 전략과 동일한
패턴이며, 프레임워크 벤더가 인프라까지 수직 통합해 개발자 경험을
독점하는 흐름의 모바일 버전이다.

### Maestro 채택의 기술적 근거

YAML 기반 선언형 문법은 QA 엔지니어나 비개발자도 작성/리뷰하기 쉽다.
Detox는 JavaScript, Appium은 다중 언어를 지원하지만 그만큼 디버깅
표면이 넓다.
Maestro는 단순함을 선택해 “테스트 작성의 한계비용”을 낮추는 데
집중했고, EAS는 그 단순성을 PR 자동화와 결합해 ROI를 키우는 구조를
의도한다.

### `needs`/`outputs` 의존성 그래프

GitHub Actions의 `jobs.<id>.needs`, `outputs` 관용구를 거의 그대로
가져온 점이 눈에 띈다.
`build_id`를 outputs로 넘겨 후속 잡이 소비하는 패턴은 CI 파이프라인
설계의 사실상 표준이다.
EAS Workflows가 별도 DSL을 만들지 않고 GitHub Actions의 멘탈모델을
의도적으로 채택한 것은 학습 비용을 낮추는 동시에 사용자 이주를
용이하게 만든다.

## 비평

### 강점

공식 문서다운 단계별 명확함이 돋보인다.
`.maestro` 디렉터리 위치, `eas.json` 프로필, 워크플로우 YAML이 모두
복사해서 바로 쓸 수 있는 완성도다.
iOS와 Android의 차이를 별도 워크플로우로 분리해 보여준 것도 실무적
판단이 좋다.

### 약점

프로덕션 시나리오가 거의 없다.
인증된 사용자 흐름, 결제, 푸시 알림, 외부 API 모킹 같은 현실적
복잡도를 다루지 않는다.
`withoutCredentials: true`만 있고, 자격증명이 필요한 테스트를 어떻게
다룰지에 대한 가이드가 없다.

테스트 실패 시 디버깅 방법도 빠져 있다.
스크린샷/비디오 아티팩트 확보, 플레이키(flaky) 테스트 재시도, 백엔드
상태 시드 같은 운영 이슈를 전혀 언급하지 않는다.

비용 모델에 대한 침묵은 가장 아쉬운 부분이다.
EAS Build는 분 단위 과금이므로 PR마다 빌드+테스트를 돌리면 크레딧
소모가 가속된다.
GitHub Actions의 `paths-ignore`, `concurrency`, draft PR 필터 같은
비용 절감 패턴을 이 문서는 다루지 않는다.

### 누락된 관점

Maestro Cloud, LambdaTest, BrowserStack App Live 같은 경쟁 솔루션과의
비교가 없다.
EAS에 lock-in되는 비용과 풀 매니지드의 운영 부담 절감 사이의
트레이드오프를 독자가 스스로 추론해야 한다.
또한 단일 디바이스/시뮬레이터에서만 테스트하는 한계, 즉 디바이스
파편화(fragmentation)를 어떻게 다룰지에 대한 답도 없다.

## 인사이트

### 테스트는 빌드의 부산물이 아니라 빌드의 첫 번째 사용자다

전통적 CI 관점에서 “build → test”는 단방향 파이프다.
그러나 EAS Workflows의 `needs`/`outputs` 패턴은 테스트가 빌드
산출물을 명시적 입력으로 소비하는 구조를 강제한다.
이 멘탈모델 차이는 데이터 파이프라인에서 lineage(계보)를 명시화한
변화와 닮았다.
산출물의 정체와 출처가 그래프의 1급 시민(first-class citizen)이 되는
순간, 시스템에 대한 추론 가능성이 한 단계 올라간다.

테스트를 빌드의 첫 사용자로 보면, 빌드 캐시 누락, 환경 변수 차이,
사이닝 분기 같은 “빌드 품질”이 곧 테스트 품질의 상한선이 된다.
빌드 산출물을 신뢰하지 못하는 한, 그 위에서 도는 테스트는 본질적으로
오염되어 있다.
이 인식은 빌드 결정성(determinism)과 재현성(reproducibility)에 대한
투자를 정당화한다.

세 번째 함의는 멀티-아티팩트 검증의 경제학이다.
같은 빌드 산출물을 `home.yml`, `expand_test.yml` 등 N개의 Maestro
잡이 병렬 소비한다.
“빌드 1번 - 테스트 N번” 패턴은 빌드 비용을 N분의 1로 분할하는 강력한
비용 최적화 수단이며, 빌드가 비싼 모바일 도메인에서는 특히
중요하다.
나아가 이 패턴은 “테스트를 더 잘게 쪼갤수록 한계비용이 0에
수렴한다”는 직관과 결합해, 자연스럽게 테스트 분할(sharding) 문화를
유도한다.

### 친숙한 DSL은 vendor lock-in의 가장 부드러운 형태다

EAS Workflows는 `name`, `on`, `jobs`, `needs`, `outputs` 등 GitHub
Actions와 의도적으로 닮은 문법을 쓴다.
이는 “익숙함의 함정”과 “이주의 사다리”가 동시에 작동하는 구조다.
GitHub Actions 사용자는 학습 비용 없이 EAS로 넘어올 수 있지만,
`type: build`, `type: maestro` 같은 EAS 전용 액션은 표준이 아니다.
표면적으로는 이식 가능해 보이는 워크플로우 파일이 실제로는 EAS에
종속된다.

이는 Hashicorp의 Terraform이 Cloud 시장 확장에 사용한 전략과 거의
같다.
친숙한 DSL을 제공하되 핵심 가치는 매니지드 백엔드에서 발생하게
한다.
사용자는 DSL의 친숙함 때문에 lock-in을 인식조차 하지 못한 채 점점
깊이 빠져든다.
“표준처럼 보이지만 표준이 아닌 DSL”은 SaaS 시대 가장 효과적인 lock-in
도구다.

조직 차원에서는 명시적 선택이 필요하다.
작은 팀이라면 EAS lock-in의 비용보다 풀 매니지드의 운영 부담 절감이
훨씬 크므로 합리적이다.
그러나 팀이 커지고 모바일 외 영역(웹, 백엔드)과 워크플로우를 통합할
필요가 생기면, 자체 인프라 + 표준 CI(GitHub Actions, Buildkite)
조합이 장기적으로 비용 우위를 갖는다.
“언제 빠져나올지”를 도입 시점에 미리 정해두지 않으면, 빠져나올 수
있는 시점은 영원히 오지 않는다.

### 모바일 E2E의 구조적 난제는 “빌드-테스트 간극”이다

웹 E2E는 정적 자산만 있으면 즉시 실행 가능하지만, 모바일 E2E는
네이티브 바이너리(`.apk`, `.ipa`)를 빌드해야 시뮬레이터에서 돌릴 수
있다.
이 빌드 시간(수 분~십수 분)은 PR 피드백 루프의 가장 큰 변수다.
EAS가 EAS Build 인프라를 EAS Workflows에 통합한 핵심 이유가 바로
이 간극을 줄이는 것이다.

그러나 빌드 시간은 여전히 테스트 시간을 압도한다.
이 때문에 모바일 진영에서는 “JS 번들만 교체하는 OTA 기반 E2E”
같은 우회 전략, Maestro Cloud나 LambdaTest의 사전 빌드 캐싱 같은
패턴이 등장한다.
모두 같은 문제 — 빌드 시간을 테스트 피드백 루프에서 분리해내려는
시도 — 에 대한 다른 답이다.

EAS Workflows가 `e2e-test` 프로필에서 `withoutCredentials: true`를
쓰는 것도 같은 맥락이다.
사이닝(signing) 단계 생략으로 빌드를 가볍게 만든다.
이는 “테스트 빌드 ≠ 출시 빌드”라는 분기를 설계 차원에서 명시적으로
인정한 결정이다.
모바일 CI 전반에서 정착하고 있는 베스트 프랙티스이며, 빌드 단계의
분기를 잘 설계할수록 테스트 피드백 루프가 짧아진다는 통찰을
보여준다.

장기적으로는 “빌드 없는 모바일 E2E”가 가능해질지가 핵심 질문이다.
Hermes 바이트코드, OTA 번들 교체, JS 코어만 시뮬레이션하는 경량
런타임 등 여러 시도가 진행 중이다.
이 흐름이 성숙하면 모바일 E2E의 경제학은 웹 E2E에 가까워질 것이고,
EAS 같은 통합 플랫폼의 가치 명제도 함께 재편될 것이다.

### PR 트리거의 비용 비대칭성과 테스트 피라미드 재해석

`on: pull_request: branches: ['*']`는 모든 PR마다 빌드+테스트를
강제한다.
작은 팀에서는 합리적이지만, 모노레포(monorepo)나 활동적 오픈소스
프로젝트에서는 EAS 빌드 크레딧이 빠르게 소진된다.
GitHub Actions의 무료 분량과 달리 EAS Build는 분당 과금이므로,
“테스트 추가의 한계비용”이 0이 아닌 양수다.
이 비대칭성은 워크플로우 설계 전반에 압력으로 작용한다.

문서는 `paths-ignore`, `concurrency.cancel-in-progress`, draft PR
필터 같은 미세 제어 패턴을 다루지 않는다.
그러나 실무에서는 이런 가드(guard)가 없으면 비용이 통제 불능 상태로
폭주한다.
“모든 PR에 E2E”가 아니라 “필요한 PR에만 E2E”를 어떻게 식별할
것인지가 진짜 설계 문제다.

이 압력은 결국 테스트 피라미드(test pyramid)의 모바일 컨텍스트
재해석을 강제한다.
유닛 테스트는 거의 공짜고, 컴포넌트 테스트는 적당히 싸며, E2E는
비싸다.
비용 곡선이 가파를수록 피라미드의 위쪽은 좁아져야 한다.
EAS Workflows의 비용 모델은 “E2E를 더 많이 돌릴수록 좋다”는
순진한 신화에 명시적 가격표를 붙여, 팀이 테스트 전략을 합리적으로
설계하도록 유도하는 부작용을 낳는다.

장기적으로는 “PR이 어떤 컴포넌트를 건드렸는가”에 기반한 선택적
테스트 실행, 즉 영향 분석(impact analysis) 기반 CI가 모바일에서도
표준이 될 가능성이 높다.
Bazel의 affected targets, Nx의 affected projects 같은 패턴이
모바일에 침투하면, EAS Workflows의 다음 진화 방향도 그쪽이 될
것이다.
비용 비대칭성은 결국 “더 똑똑한 트리거”를 향한 시장 압력이다.
