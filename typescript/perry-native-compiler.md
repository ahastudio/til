# Perry — TypeScript 네이티브 컴파일러

<https://github.com/PerryTS/perry>

GeekNews: <https://news.hada.io/topic?id=30287>

## 소개

Perry는 Rust로 작성된 TypeScript 네이티브 컴파일러다.
TypeScript를 Node.js, Electron, 브라우저 엔진 없이 직접 LLVM 기계어로 컴파일해 독립 실행 가능한 바이너리를 생성한다.

```bash
perry compile src/main.ts -o myapp
./myapp    # 런타임 의존성 없는 독립 바이너리
```

TypeScript 파싱에 SWC를, 네이티브 코드 생성에 LLVM을 사용한다.
버전 0.5.908 기준으로 GitHub 스타 3,699개를 보유하고 있다.

## 주요 기능

**단일 코드베이스, 모든 플랫폼**: 하나의 TypeScript 소스로 macOS, iOS, Android, Linux, Windows용 바이너리를 생성한다.

**런타임 없음**: Node.js나 V8 엔진이 없어도 실행된다.
생성된 바이너리는 “Hello, World!” 수준에서 약 330KB 크기다.

**진짜 TypeScript 지원**: TypeScript-like 언어가 아닌 실제 TypeScript Strict Mode 기반이다.

**서브초 콜드 스타트**: JIT 워밍업 없이 즉시 실행된다.

## 성능

M1 Max에서의 벤치마크(v0.5.908):

| 벤치마크         | Perry | Rust | C++  | Go   | Node  | Bun  |
| ---------------- | ----: | ---: | ---: | ---: | ----: | ---: |
| fibonacci (ms)   |   309 |  316 |  309 |  446 |   987 |  518 |
| closure (ms)     |    50 |    — |    — |    — |   304 |   51 |
| binary_trees (ms)|     2 |    — |    — |    — |    10 |    7 |
| string_concat (ms)|    0 |    — |    — |    — |     3 |    1 |

fibonacci 기준으로 Rust, C++와 동일한 수준이며 Node.js 대비 3배 빠르다.

핵심 최적화:
- **Scalar Replacement**: 이스케이프하지 않는 객체를 힙 할당 없이 레지스터로 처리한다.
- **i64 특수화**: 순수 재귀 수치 함수에 대한 정수 타입 최적화다.
- **Inline Bump Allocator**: 이스케이프하는 객체에 대한 빠른 메모리 할당이다.

## 실제 사용 사례

README에 Perry로 구축된 프로젝트들이 소개된다.

**Mango**: macOS·Windows·Linux·iOS·Android를 지원하는 네이티브 MongoDB GUI.
~7MB 바이너리, 100MB 미만 메모리 사용.

**Bloom Engine**: Metal, DirectX 12, Vulkan, OpenGL을 지원하는 TypeScript 네이티브 게임 엔진.

**Hone**: AI 기반 네이티브 코드 에디터.
빌트인 터미널, Git, LSP를 포함하며 모든 주요 플랫폼을 지원한다.

## 현재 한계

- 정적 컴파일 특성상 동적 JavaScript 기능이 지원되지 않는다.
- Node.js 모듈 에뮬레이션이 알파 단계이며 Express 같은 일부 라이브러리의 호환성이 불완전하다.
- 기존 프로젝트 마이그레이션보다 새 프로젝트 시작에 적합하다.

## 분석

### TypeScript를 LLVM으로 직접 컴파일하는 것의 기술적 의미

TypeScript는 원래 JavaScript의 정적 타입 슈퍼셋으로 설계됐고, 컴파일 타겟은 항상 JavaScript였다.
Perry가 TypeScript를 LLVM IR로 직접 변환하는 것은 이 전제를 바꾸는 것이다.

핵심 도전은 TypeScript/JavaScript의 동적 특성이다.
덕 타이핑, 런타임 프로토타입 변형, 동적 프로퍼티 추가는 LLVM의 정적 컴파일 모델과 근본적으로 충돌한다.
Perry가 이를 해결하는 방식은 Strict Mode를 전제로 하고 동적 기능을 제한하는 것이다.
결과적으로 Perry가 컴파일하는 TypeScript는 완전한 TypeScript가 아니라 정적으로 분석 가능한 부분집합이다.

Scalar Replacement 최적화는 이 제약을 활용한다.
객체가 함수 밖으로 이스케이프하지 않는다는 것을 정적으로 증명할 수 있을 때, 해당 객체의 필드를 레지스터로 처리할 수 있다.
이것이 `binary_trees` 벤치마크에서 Node.js(10ms) 대비 5배 빠른 2ms를 가능하게 한다.

### JavaScript 생태계에서 네이티브 컴파일이 실질적 이득을 갖는 영역

서버 사이드 Node.js 애플리케이션의 대부분은 컴퓨팅 집약적이 아니라 I/O 집약적이다.
데이터베이스 쿼리, 네트워크 요청을 기다리는 시간이 대부분이고 CPU 처리 시간은 적다.
이런 워크플로에서 네이티브 컴파일이 주는 성능 이점은 I/O 대기 시간에 가려진다.

Perry가 실질적 이득을 주는 영역은 다르다.
배포 크기가 중요한 CLI 도구, 모바일 앱처럼 의존성 없는 단일 바이너리가 가치를 갖는 환경, 그리고 콜드 스타트가 중요한 서버리스 환경이다.
Mango(MongoDB GUI)나 Hone(코드 에디터) 같은 데스크탑 앱이 Perry의 자연스러운 타겟인 이유다.

### TypeScript 생태계 확장의 의미

Perry의 더 흥미로운 함의는 TypeScript 개발자가 네이티브 앱을 작성하는 경로가 열린다는 것이다.
기존에는 TypeScript로 네이티브 앱을 만들려면 Electron(Chromium+Node.js 번들로 수백 MB)이나 React Native(네이티브 브리지)를 사용해야 했다.

Perry는 이 대안으로 수 MB의 진짜 네이티브 바이너리를 제공한다.
TypeScript 개발자가 Swift, C++, Kotlin을 배우지 않고도 네이티브 iOS/Android 앱이나 고성능 CLI 도구를 만들 수 있는 가능성이 생긴다.
물론 동적 기능 제약이라는 비용이 따르지만, 새 프로젝트에서는 이 제약 내에서 설계하는 것이 가능하다.

## 비평

### 빠른 수치가 가장 유리한 벤치마크를 선택한 결과다

README의 벤치마크는 Perry가 강한 워크로드를 중심으로 구성됐다.
binary_trees와 fibonacci는 정적 컴파일이 유리한 CPU 바운드 작업이다.
실제 서버 애플리케이션에서 중요한 JSON 파싱, 네트워크 처리, 문자열 조작의 성능은 이 수치로 예측하기 어렵다.

README가 자체 비판적으로 “trivially-foldable 누산 마이크로벤치마크에서의 큰 수치를 의도적으로 제거했다”고 명시하는 것은 정직한 태도이지만, 여전히 선택된 벤치마크는 Perry에게 유리한 시나리오들이다.
실제 애플리케이션에서의 성능을 평가하려면 직접 자신의 워크로드로 측정해야 한다.

### Node.js 생태계 호환성 부재가 채택의 실질적 장벽이다

Node.js 생태계의 가치는 npm에 있다.
Express, Fastify, Prisma, AWS SDK, Stripe SDK — 이것들이 동작하지 않으면 TypeScript 개발자가 Perry로 이동하기 어렵다.
Node.js 모듈 에뮬레이션이 “알파 단계”라는 것은 현재 Perry로 일반적인 백엔드 서비스를 구축하기 어렵다는 의미다.

이것은 Perry가 기존 JavaScript/TypeScript 생태계를 대체하는 것이 아니라, 특정 니치(CLI 도구, 데스크탑 앱, 게임)에 집중하는 도구임을 시사한다.
그 니치에서는 실제 가치를 제공하지만, “TypeScript로 모든 것을”이라는 더 넓은 약속은 현재 상태에서 실현되지 않는다.

## 인사이트

### TypeScript의 타입 시스템이 컴파일 최적화의 기반이 되는 역설

TypeScript의 타입 정보는 원래 JavaScript로 컴파일될 때 모두 제거됐다(type erasure).
Perry는 이 제거됐던 정보를 LLVM 최적화에 활용한다.
타입이 정적으로 알려진 변수는 JIT 컴파일러가 런타임에 추론해야 하는 작업을 컴파일 타임에 미리 처리할 수 있게 한다.

이것은 TypeScript의 타입 시스템이 런타임에서 다른 방식으로 가치를 만들 수 있다는 것을 보여주는 흥미로운 예다.
JavaScript 생태계에서 “타입은 개발 시점에만 의미 있다”는 통념이 Perry에서는 “타입이 런타임 성능을 결정한다”로 바뀐다.
TypeScript 타입 정확성이 코드 품질뿐 아니라 성능에도 직접 영향을 미치는 환경이다.

### 크로스플랫폼 네이티브 앱 개발의 새로운 경쟁 구도

크로스플랫폼 네이티브 앱 개발 공간에는 Flutter(Dart), React Native(JavaScript), Kotlin Multiplatform(Kotlin), .NET MAUI(C#)가 있다.
Perry가 TypeScript 개발자에게 진짜 네이티브 바이너리 경로를 제공하면, 이 생태계의 언어 선택에 새로운 변수가 추가된다.

TypeScript는 이미 프론트엔드, 백엔드, CLI 영역에서 가장 넓게 사용되는 언어 중 하나다.
이 개발자들이 같은 언어로 네이티브 앱을 만들 수 있다면, 새 언어 학습 비용 없이 플랫폼을 확장할 수 있다.
Perry의 궤적이 Node.js 생태계 호환성과 동적 기능 지원을 어디까지 넓힐 수 있는지가 이 잠재력이 실현되는 속도를 결정한다.
