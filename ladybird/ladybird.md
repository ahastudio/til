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

### NIH에서 선택적 실용주의로

2024년 6월 Andreas Kling은 Ladybird를 SerenityOS에서
포크하며 BDFL 자리에서 물러났다.
SerenityOS는 "서드파티 코드 금지"라는
엄격한 NIH(Not Invented Here) 정책을 고수했다.
Ladybird는 이를 정면으로 뒤집었다.

직접 만드는 것과 빌려 쓰는 것의 경계가 명확하다.

**직접 만드는 것** -- 브라우저 정체성의 핵심:

- LibJS (JavaScript 엔진)
- LibWeb (렌더링 엔진)
- AK (자체 표준 라이브러리)
- LibIPC (프로세스 간 통신)

**빌려 쓰는 것** -- 도메인 전문 인프라:

- Skia: GPU 최적화에 수십 년이 녹아 있다
- HarfBuzz: 아랍어, 히브리어, 데바나가리 등
  복합 문자 조판에는 언어학 전문성이 필요하다.
  도입 후 "major milestone"로 불렸다
- FFmpeg: 코덱 구현은 특허 지뢰밭이다
- ICU: 유니코드 준수만으로 거대한
  룩업 테이블과 복잡한 알고리즘이 필요하다

패턴이 보인다.
아키텍처적 레버리지를 제공하는 코드는 직접 만들고,
최고 수준의 구현이 이미 존재하는
도메인 특화 인프라는 빌려 쓴다.
이 경계를 식별하는 능력 자체가
엔지니어링 성숙도의 지표다.

### AK: C++ 표준 라이브러리를 거부한 이유

AK 디렉토리에는 약 198개 파일이 있다.
C++ STL을 완전히 대체하는 자체 표준 라이브러리다.
허세가 아니라 구조적 필연이다.

**C++ 예외를 거부했다.**
`ErrorOr<T>` 반환 타입과 `TRY()` 매크로를 만들어
Rust의 `Result<T, E>`와 `?` 연산자를
C++에서 구현했다.
STL은 예외 기반 에러 보고를 전제하므로
(`std::vector::at()`, `std::map::at()` 등)
근본적으로 맞지 않았다.

**OOM 안전성을 설계에 녹였다.**
AK의 침입형 리스트(intrusive list)는
메타데이터를 요소 자체에 내장한다.
삽입 시 힙 할당이 불필요하므로
OOM 에러 처리 코드가 극적으로 단순해진다.

**자기 문서화하는 기술 부채 추적.**
`release_value_but_fixme_should_propagate_errors()`
라는 메서드명이 있다.
에러 전파가 필요하지만 아직 구현하지 못한 지점을
이름 자체로 표시한다.
TODO 주석보다 강력하다.
컴파일러가 호출 지점을 추적해주기 때문이다.

### 코드가 곧 스펙이다

Ladybird의 코딩 컨벤션은 코드베이스를
웹 표준의 실행 가능한 번역본으로 만든다.

**주석 접두어 시스템:**

- `NOTE:` -- 스펙에서 그대로 복사한 메모
- `AD-HOC:` -- 스펙에 없는 자체 구현.
  이 접두어의 존재 자체가 놀랍다.
  스펙 이탈 지점을 명시적으로 표시한다는 뜻이다
- `FIXME:` -- 미구현 스펙 단계
- `// OPTIMIZATION:` -- 스펙과 다른 최적화 경로

**함수명이 스펙을 따른다.**
`HTMLInputElement::suffering_from_being_missing()`
같은 메서드명이 실제로 존재한다.
스펙이 어색한 표현을 쓰더라도 그대로 보존한다.
코드와 스펙 사이의 번역 비용을 제거하기 위해서다.

**스펙 단계 번호가 주석으로 들어간다.**
W3C/WHATWG 알고리즘의 각 단계가
코드 내 번호 주석과 1:1로 대응한다.
스펙 변경 시 코드 어디를 수정해야 하는지
즉시 알 수 있다.

**스펙에 역으로 피드백한다.**
기여자들이 구현 중 발견한 스펙 모호성을
스펙 메인테이너에게 보고한다.
"스펙을 비판적으로 읽고 잘못된 점을
보고하는 것"을 프로젝트 가치로 삼는다.

### WPT를 역발상으로 활용한다

기존 브라우저는 WPT(Web Platform Tests)를
회귀 방지용으로 쓴다.
기능을 구현한 후 테스트가 깨지지 않는지 확인한다.

Ladybird는 WPT를 **생성적으로** 쓴다.
실패하는 WPT 테스트가 곧 "다음에 무엇을
만들지"의 백로그다.
테스트와 코드의 관계가 역전된다.

2025년 1월, LibJS는 test262(ECMAScript 공식
적합성 테스트)에서 **최고 점수**를 기록했다.
자체 제작 JavaScript 엔진이
V8이나 SpiderMonkey를 특정 테스트에서
앞선다는 뜻이다.

기여자 온보딩에도 활용한다.
공식 가이드는 "C++를 전혀 모르더라도
JavaScript 지식만으로 WPT 테스트 실패를
분석하고 원인을 상당 부분 분리할 수 있다"고
안내한다.
브라우저 엔진 기여의 진입 장벽을
JavaScript 수준으로 낮춘 것이다.

### YouTube로 브라우저를 만든다

Andreas Kling은 개발 과정을 YouTube에
실시간으로 공개한다.
편집된 튜토리얼이 아니라
날것의 디버깅, 설계 결정, 실패와 수정을
그대로 보여준다.

LibJS 전체가 카메라 앞에서 탄생했다.
Ladybird 자체도 2022년 7월 4일
Kling이 LibWeb용 Qt GUI를 만드는
영상에서 시작됐다.

이 투명성이 만든 구조적 효과가 있다.

**채용 파이프라인이 된다.**
유급 엔지니어 8명 전원이 자원봉사 기여자
출신이다.
Kling은 이를 "가능한 한 가장 건전한
채용 방식"이라고 부른다.
YouTube → 기여 → 고용의 경로가 자연스럽게
형성된다.

**접근성 철학의 구현체다.**
Kling의 목표는 "누구나 자기가 좋아하는
웹사이트의 버그 하나를 고치기 위해
브라우저 개발자가 될 수 있는 것"이다.
영상은 이 철학의 직접적 실현이다.

**개인적 맥락.**
Kling은 SerenityOS를 중독 회복 과정에서
시작했다(이름은 "평온의 기도"에서 따왔다).
이 서사가 프로젝트 커뮤니티에
독특한 공감 문화를 형성했다.

### Servo와 다른 질문에 답한다

현재 활발히 개발 중인 브라우저 엔진은 6개.
그중 독립 엔진은 Servo와 Ladybird.
둘은 겉보기에 비슷하지만
근본적으로 다른 질문에 답한다.

**Servo**: 브라우저 엔진을 Rust로,
병렬 렌더링으로 만들 수 **있는가?**
Mozilla 연구 프로젝트에서 출발.
SpiderMonkey(Mozilla의 JS 엔진)을 그대로 사용.
임베딩 가능한 엔진이 목표다.

**Ladybird**: 소규모 팀과 커뮤니티가
완전한 독립 브라우저를 처음부터
만들 수 **있는가?**
JS 엔진까지 자체 제작.
엔드투엔드 브라우저 경험이 목표다.

Kling은 Servo에 대해 이렇게 말했다.
"Servo는 무엇보다 실험이라고 이해했고,
거기서 많은 좋은 것이 나왔다."
큰 엔진에서 하기 불편한 시도를
계속하기를 바란다고 했다.

코드 규모로 보면 Ladybird와 Servo는 비슷하다.
둘 다 WebKit의 약 1/15, Chromium의 약 1/50.
그러나 Servo는 SpiderMonkey를 빌려 쓰고,
Ladybird는 LibJS를 직접 만들었다.
"독립"의 범위가 다르다.

### 비영리의 구조적 딜레마

Mozilla는 연간 4억 달러 이상의
Google 검색 거래 수입이 있다.
Ladybird는 이를 명시적으로 거부한다.

**강점:**

Kling은 "Mozilla보다 훨씬 좁은 목표를
설정하고, 브라우저에만 집중하면
재정적으로 더 지속 가능할 것"이라고 말한다.
8명으로 할 수 없는 일은 커뮤니티에 맡긴다.
기여를 극도로 쉽게 만들어
커뮤니티가 스케일링 메커니즘이 되도록 한다.

**리스크:**

- 기부 의존: 지속적 자선 관심이
  전제되어야 한다
- 규모 불일치: "우리는 절대 억만장자가
  될 수 없다. 경쟁자 중 일부는 그렇지만."
  (Kling)
- 표준 진화 속도: Google이 Blink에
  기능을 추가하는 속도를
  Ladybird가 따라잡을 수 있을까
- Mozilla 전철: 사업 모델 없이 시작하면
  "윤리를 조정하게 된다"는 우려.
  Mozilla의 미션 표류(Pocket, VPN, AI 투자)가
  반면교사다

**Kling의 답:**
지속 가능성 자체를 설계 문제로 취급한다.
펀딩 문제가 아니라 엔지니어링 문제로 본다.
"제한된 자금으로 브라우저를 개발하는
지속 가능한 방법을 찾는 것"이
가장 좋아하는 작업이라고 말한다.

### 클린 슬레이트의 양면

Chromium은 약 3,500만 줄.
Ladybird는 그 1/50 규모다.
처음부터 시작하면 무엇을 얻고 잃는가.

**얻는 것:**

- C++20/23을 네이티브로 사용.
  레거시 코드에 이식하는 것이 아니다
- GC 우선 객체 모델.
  ref-counting 래퍼 클래스를 거쳐야 했던
  구조를 "구현체가 곧 JS 객체"로 단순화했다.
  래퍼 제거로 ref-counting 순환 문제를 회피
- 멀티프로세스를 처음부터 설계.
  Chrome의 Site Isolation은 수년이 걸렸다.
  Ladybird는 아키텍처 단계에서 반영
- 쿼크 모드 부채 없음.
  표준을 정확히 구현하면 다른 엔진의
  버그에 의존하는 사이트가 깨질 수 있다.
  Kling은 이 트레이드오프를 수용한다

**잃는 것:**

Kling이 인정하듯 "다른 주요 브라우저가
약 10배 빠르다."
클린 슬레이트의 이점은 코드 유지보수성과
아키텍처 명확성에 나타나지,
아직 성능에는 반영되지 않았다.

### WebIDL 코드 생성이 규모를 만든다

처음부터 만드는 프로젝트가
방대한 웹 API를 커버하는 비결.
빌드 시 `BindingsGenerator`가 WebIDL `.idl`
파일을 파싱해 C++ 래퍼 클래스를
자동 생성한다.

Chrome(V8 바인딩)이나 Firefox(mozwebidlcodegen)와
동일한 접근 방식이다.
새 웹 API를 추가하려면 스펙의 `.idl` 파일을
복사하고 C++ 구현만 작성하면 된다.
보일러플레이트가 극적으로 줄어든다.

Chromium의 1/50 규모로
놀라울 정도로 넓은 API를 커버하는 이유 중
하나가 이 코드 생성 전략이다.

### 일관성이라는 진짜 강점

개별 기술 결정보다 중요한 것은
선택들 사이의 **일관성**이다.

AK의 `ErrorOr<T>`, 스펙 연결 주석,
WPT 기반 로드맵, 디렉토리별 스펙 매핑,
YouTube 투명 개발 -- 이것들은 서로를 강화한다.

기여자의 경로가 자연스럽게 형성된다:

1. YouTube에서 Kling이 기능을 만드는 걸 본다
2. LibWeb에서 해당 스펙 디렉토리를 찾는다
3. 스펙 단계와 1:1 대응하는 주석을 읽는다
4. 실패하는 WPT 테스트를 구현 대상으로 삼는다
5. `TRY()`/`ErrorOr` 컨벤션으로 패치를 제출한다

이 경로의 각 단계가 다음 단계의
마찰을 줄이도록 설계되어 있다.
개별 결정이 아닌 시스템의 정합성이
Ladybird의 진짜 경쟁력이다.
