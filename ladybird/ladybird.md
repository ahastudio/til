# Ladybird

완전히 새로운 독립 웹 브라우저 엔진.
Blink, WebKit, Gecko 코드를 일절 사용하지 않고
처음부터(from scratch) 만든다.

<https://ladybird.org/>

<https://github.com/LadybirdBrowser/ladybird>

## 왜 새 브라우저 엔진인가

현재 웹은 소수의 브라우저 엔진이 지배한다.
각 엔진은 특정 기업의 이해관계에 묶여 있다.
Ladybird는 이 단일화(monoculture) 문제에 대한
독립적 대안을 목표로 한다.

핵심 원칙:

- 다른 브라우저 코드 미사용
- 사용자 수익화 없음
  (기본 검색 엔진 거래, 광고, 토큰 없음)
- 501(c)(3) 비영리 재단 운영
- 무제한 기부금만 수용
  (이사회 의석 등 영향력 미판매)

## 프로젝트 현황

| 항목         | 내용                        |
|--------------|-----------------------------|
| GitHub Stars | 60,700+                     |
| 라이선스     | BSD 2-Clause                |
| 주요 언어    | C++ 58.8%, Rust 2.0%        |
| WPT 통과율   | 90% 이상 (2025년 10월 기준) |
| 알파 릴리스  | 2026년 (Linux, macOS)       |
| 유급 엔지니어| 8명 풀타임                  |

## 아키텍처 개요

SerenityOS에서 시작했으나 독립 프로젝트로 분리.
32개 내부 라이브러리로 구성된 모듈형 설계.

### 핵심 라이브러리

```
Libraries/
  LibWeb/     -- 웹 렌더링 엔진 (65+ 하위 디렉토리)
  LibJS/      -- JavaScript 엔진
  LibWasm/    -- WebAssembly
  LibGfx/     -- 2D 그래픽, 이미지 디코딩, 폰트
  LibMedia/   -- 오디오/비디오 재생
  LibWebView/ -- 웹 뷰 추상화
```

### 네트워킹 및 보안

```
Libraries/
  LibHTTP/      -- HTTP/1.1 클라이언트
  LibTLS/       -- TLS 구현
  LibCrypto/    -- 암호화 프리미티브
  LibDNS/       -- DNS 리졸버
  LibWebSocket/ -- WebSocket 프로토콜
  LibURL/       -- URL 파싱
```

### 플랫폼 인프라

```
Libraries/
  LibCore/      -- 이벤트 루프, 시스템 추상화
  LibIPC/       -- 프로세스 간 통신
  LibGC/        -- 가비지 컬렉터 (LibJS용)
  LibUnicode/   -- 유니코드, ICU 통합
```

## 멀티프로세스 아키텍처

Chromium 스타일의 프로세스 분리 모델을 채택.

```
Browser (UI)
  ├── WebContent (탭당 1개)
  │     ├── RequestServer (네트워크 I/O)
  │     └── ImageDecoder (이미지 디코딩)
  ├── WebDriver (브라우저 자동화)
  └── WebWorker (Web Workers)
```

- 탭별 프로세스 격리
- 사이트 격리(Site Isolation) 구현 중
- Unix 도메인 소켓 기반 IPC 통신
- `pledge()`/`unveil()`로 시스템 콜 제한

## 렌더링 파이프라인

10단계로 구성된 완전한 파이프라인.

1. **리소스 로딩** --
   RequestServer로 IPC 호출
2. **HTML 파싱** --
   토크나이저 + 파서로 DOM 트리 구축
3. **CSS 파싱** --
   CSSOM 구축, 변수는 캐스케이드까지 미해결
4. **JavaScript 실행** --
   AST 파싱 → 바이트코드 컴파일 → 실행
5. **스타일 계산** --
   우→좌 셀렉터 매칭, 캐스케이드 해석
6. **레이아웃 트리 구축** --
   DOM + 스타일 → 박스 트리 (DOM과 1:1 아님)
7. **레이아웃** --
   BFC, IFC, TFC, FFC, SVG 포매팅 컨텍스트
8. **페인트 트리 생성** --
   최종 메트릭이 확정된 Paintable 객체
9. **스태킹 컨텍스트** --
   z-index 기반 Z축 트리
10. **페인팅** --
    CSS2 부록 E 순서대로 후→전 렌더링

## LibJS: JavaScript 엔진

자체 렉서, 파서, AST, 바이트코드 컴파일러,
mark-and-sweep GC를 갖춘 완전한 엔진.

```
Libraries/LibJS/
  Lexer.cpp/h     -- 토크나이저
  Parser.cpp/h    -- AST 생성 파서
  AST.cpp/h       -- 추상 구문 트리
  Bytecode/       -- 바이트코드 컴파일러/인터프리터
  Runtime/        -- 런타임 빌트인, 객체, 값
  Heap/           -- GC 힙
  Rust/           -- Rust 통합 컴포넌트
```

## LibWeb 내부 구조

웹 스펙별로 디렉토리가 나뉘며
`Web::*` 네임스페이스에 매핑된다.

- **DOM/Core**: `DOM/`, `HTML/`, `CSS/`, `WebIDL/`
- **레이아웃**: `Layout/`, `Painting/`, `SVG/`
- **API**: `Fetch/`, `XHR/`, `WebSockets/`,
  `WebAssembly/`, `WebGL/`, `WebAudio/`
- **보안**: `ContentSecurityPolicy/`, `Crypto/`,
  `MixedContent/`, `PermissionsPolicy/`
- **미디어**: `MediaSourceExtensions/`,
  `EncryptedMediaExtensions/`

## 코드 패턴

### 에러 처리

```cpp
// TRY: Rust의 ? 연산자처럼 에러 전파
auto result = TRY(fallible_operation());

// MUST: 절대 실패하면 안 되는 연산
auto value = MUST(infallible_in_practice());

// ErrorOr<T>: OOM 등 기반 라이브러리 에러
ErrorOr<String> get_name();

// WebIDL::ExceptionOr<T>: LibWeb 에러
WebIDL::ExceptionOr<void> do_web_thing();
```

### 스펙 준수 코딩 컨벤션

함수 내에 스펙 링크와 단계별 주석을 반드시 포함.
미구현 단계는 `FIXME`로, 최적화는
`// OPTIMIZATION:`으로 표시한다.

```cpp
// https://html.spec.whatwg.org/#dom-document-title
// 1. If the document element is an SVG svg element
// FIXME: 2. Handle SVG title element
// 3. Otherwise, ...
```

### 팩토리 메서드

C++ 생성자는 에러를 반환할 수 없으므로
정적 `create()` 메서드를 사용한다.

```cpp
static ErrorOr<NonnullOwnPtr<Widget>>
create(Config const&);
```

## 빌드 시스템

CMake(주) + GN(대안) 듀얼 빌드 시스템.
vcpkg로 30개 이상 의존성 관리.

주요 의존성:

- **그래픽**: Skia, ANGLE, Vulkan
- **미디어**: FFmpeg, libjpeg-turbo, libwebp
- **텍스트**: ICU, HarfBuzz, FreeType
- **네트워크**: curl(HTTP/2/3), OpenSSL
- **파싱**: simdutf, simdjson

## C++에서 Rust로

보안에 민감한 컴포넌트부터 점진적으로
Rust로 전환 중. C++/Rust 상호 운용을 위한
FFI 레이어를 검토하고 있으며,
전환 가속화에 AI 에이전트도 활용한다.

## 인사이트

### 독립 엔진의 가치

기존 엔진을 포크하지 않고 처음부터 만드는 것은
비효율적으로 보이지만, 기술 부채 없이
현대적 설계를 적용할 수 있다는 장점이 있다.
레거시 호환성 코드가 없으므로
아키텍처가 깔끔하게 유지된다.

### 스펙 중심 개발

디렉토리 구조 자체가 웹 스펙을 반영한다.
`Libraries/LibWeb/Fetch/`는 Fetch 스펙,
`Libraries/LibWeb/DOM/`은 DOM 스펙에 대응.
코드를 읽으면 스펙을 읽는 것과 같은 효과가
있으며, 기여자의 진입 장벽을 낮춘다.

### 프로세스 격리 전략

탭별 프로세스 격리에서 오리진별 격리로
진화하는 과정이 흥미롭다.
Chromium이 수년간 겪었던 사이트 격리 문제를
후발 주자의 이점으로 처음부터 설계에
반영하고 있다.

### 비영리 모델의 실험

Mozilla의 이중 구조(재단 + 기업)와 달리
순수 비영리로 운영한다.
검색 엔진 거래 수입 없이 기부만으로
8명의 풀타임 엔지니어를 유지하며,
18개월 분 운영 자금을 확보하는 보수적
재무 전략을 취한다.

### WPT 90% 달성의 의미

2025년 10월 WPT 서브테스트 90% 이상 통과.
Apple이 iOS 대체 브라우저 엔진 허용 기준으로
삼는 수치이기도 하다.
Chrome, Safari, Firefox에 이어 4위로,
처음부터 만든 엔진으로서는 놀라운 성과다.

### Rust 전환 전략

전체 재작성이 아닌 점진적 포팅.
보안 민감 컴포넌트(파싱, 네트워킹)부터
시작하는 실용적 접근.
AI를 활용한 C++ → Rust 변환 가속화는
대규모 코드베이스 마이그레이션의
새로운 패턴을 제시한다.
