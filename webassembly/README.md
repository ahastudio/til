# WebAssembly

<https://webassembly.org/>

- <https://developer.mozilla.org/en-US/docs/WebAssembly>
- <https://en.wikipedia.org/wiki/WebAssembly>
- <https://github.com/WebAssembly>
- [2020년과 이후 JavaScript의 동향 - WebAssembly](https://d2.naver.com/helloworld/8257914)
- [FE개발자의 성장 스토리 08 : WebAssembly 개발기](https://tech.kakao.com/2021/05/17/frontend-growth-08/)

## 소개

WebAssembly(Wasm)는 스택 기반 가상 머신을 위한 이진 명령어 형식(binary instruction format)이다.
이식 가능한 컴파일 타깃으로 설계되어, C/C++/Rust 등 다양한 언어로 작성된 코드를 웹 브라우저와 서버 환경 모두에 배포할 수 있다.
2017년 11월 Chrome, Firefox, Safari, Edge의 주요 브라우저 벤더들이 MVP(Minimum Viable Product) 설계에 합의하며 공식화됐다.
현재 W3C Community Group과 W3C Working Group이 공동으로 표준을 개발하고 있다.

## 설계 원칙

WebAssembly의 다섯 가지 고수준 목표(High-Level Goals)는 이 기술의 설계 방향을 명확히 드러낸다.

| 목표             | 내용                                                |
| ---------------- | --------------------------------------------------- |
| 효율적 이진 형식 | 네이티브 속도에 근접한 컴팩트 바이너리 포맷         |
| 점진적 발전      | 하위 호환성과 언어 중립성을 유지하며 기능 추가      |
| 웹 플랫폼 통합   | JavaScript와 동기적 상호 호출, 동일 보안 정책 준수  |
| 비브라우저 지원  | 서버, 모바일, IoT 등 다양한 임베딩 환경 지원        |
| 플랫폼 우수성    | 공식 시맨틱 명세, 결정론적 실행, 도구 생태계 지원   |

텍스트 형식(WAT, WebAssembly Text Format)을 이진 형식과 상호 변환할 수 있어 디버깅과 교육 목적으로 활용된다.
실행 환경은 메모리 안전 샌드박스로, 브라우저에서는 JavaScript와 동일한 보안 정책을 따른다.

## 주요 사용 사례

**브라우저 내**: 게임(캐주얼~AAA), 이미지/영상 편집, 음악 스트리밍, CAD 툴, VPN, VR/AR, 브라우저 내 컴파일러·디버거.
기존 C/C++/Rust 코드를 JavaScript/HTML 애플리케이션 안에 점진적으로 통합하는 방식도 지원한다.

**브라우저 외**: 서버에서 신뢰되지 않는 코드를 안전하게 실행하는 샌드박스, 모바일 하이브리드 앱, 분산 컴퓨팅 노드.
WASI(WebAssembly System Interface)가 이 방향을 확장하는 주요 표준이다.

## 분析

### JavaScript 이후 웹의 컴파일 타깃 레이어

웹 브라우저는 역사적으로 JavaScript를 유일한 실행 언어로 가정해왔다.
TypeScript, CoffeeScript, Dart처럼 JavaScript로 컴파일하는 언어들이 생겨났지만, 모두 JavaScript VM에 종속됐다.
WebAssembly는 VM의 상위 계층이 아니라 VM 아래의 새로운 계층을 만들어 이 구조를 바꾼다.
이진 형식을 직접 실행하는 VM이 생기자 JavaScript가 유일한 게이트키퍼였던 시대가 끝난다.

이 구조적 전환은 “웹은 JavaScript다”라는 30년 가정에 대한 반례다.
Wasm이 있다면 언어 선택은 런타임 제약이 아니라 팀 역량과 성능 요구사항에 따른 설계 결정이 된다.
C로 작성된 게임 엔진, Rust로 작성된 암호화 라이브러리, Go로 작성된 로직이 동일한 브라우저 탭 안에서 실행될 수 있다.

### 샌드박스로서의 보안 모델

WebAssembly의 샌드박스 실행 모델은 보안 측면에서 주목할 만하다.
Wasm 모듈은 선언적으로 허용된 메모리 영역과 가져온(imported) 함수만 접근할 수 있다.
호스트 환경이 어떤 기능을 제공할지를 결정하며, 모듈 스스로는 파일 시스템이나 네트워크에 직접 접근할 수 없다.
이 설계는 신뢰되지 않는 코드를 안전하게 실행하는 플러그인 아키텍처의 기반이 된다.

WASI는 이 샌드박스를 브라우저 밖으로 표준화한다.
POSIX와 유사한 시스템 인터페이스를 정의하되, 기능 기반(capability-based) 보안 모델로 최소 권한 원칙을 구현한다.
“Docker가 없었다면 우리는 Wasm을 발명했을 것이다”라는 Solomon Hykes의 발언은 이 방향의 잠재력을 함축한다.

### 점진적 도입 전략

WebAssembly의 현실적 강점 중 하나는 점진적 도입이 가능하다는 점이다.
전체 애플리케이션을 Wasm으로 전환하지 않아도, 성능이 중요한 특정 모듈만 Wasm으로 교체할 수 있다.
JavaScript로 구현된 이미지 처리 루프를 Rust+Wasm으로 교체하면 나머지 코드는 그대로 유지된다.
이것은 asm.js 시절부터 이어진 웹 플랫폼의 “기존 투자를 보존하며 진화”하는 전통과 일치한다.

## 비평

### 여전히 높은 진입 장벽

WebAssembly 자체는 저수준 이진 형식이다.
개발자가 직접 Wasm을 작성하는 경우는 드물고, 대부분 Emscripten(C/C++), wasm-pack(Rust), TinyGo(Go) 같은 툴체인을 거친다.
이 툴체인들은 각자 학습 비용이 있고, 브라우저의 JavaScript API와 연동하기 위한 글루 코드(glue code)가 여전히 복잡하다.
“네이티브 코드를 웹에서 실행”이라는 약속이 간단해 보이지만, 실제 워크플로우는 여전히 마찰이 많다.

### 디버깅 경험의 미성숙

Source Maps와 DWARF 디버그 정보 지원이 추가됐지만, JavaScript 대비 디버깅 경험은 여전히 뒤처진다.
브라우저 DevTools에서 Wasm 코드를 원본 소스 수준으로 디버깅하는 것이 가능해졌지만, 메모리 직접 조작, 스택 트레이스의 가독성 문제는 실무 개발자에게 도전이다.
가비지 컬렉션(GC) 제안이 표준화 진행 중이지만, 안정화되기까지 Java나 Python 같은 GC 언어를 효율적으로 컴파일하는 것은 제한적이다.

### 비브라우저 생태계의 분열

WASI가 표준을 제시했지만, 런타임 생태계가 Wasmtime, WasmEdge, Wasmer, WAMR 등으로 분열되어 있다.
각 런타임의 WASI 지원 수준이 다르고, WASI 자체도 preview1에서 preview2로 이행하는 과정에서 호환성 문제가 발생한다.
“한 번 작성하면 어디서나 실행”이라는 약속이 Java의 그것과 유사한 현실적 한계를 드러내고 있다.

## 인사이트

### 웹 플랫폼의 두 번째 어셈블리어 시대

컴퓨팅 역사에서 어셈블리어는 특정 하드웨어에 종속된 저수준 언어였다.
웹은 플랫폼 독립성을 위해 JavaScript라는 고수준 언어 하나를 공통 실행 환경으로 선택했다.
WebAssembly는 이 선택을 다시 쓴다. 플랫폼 독립성을 유지하면서도 저수준 이진 형식을 도입함으로써, 웹은 처음으로 플랫폼 중립적인 “어셈블리어 계층”을 갖게 됐다.

이 변화의 의미는 단순히 성능 향상이 아니다.
어셈블리어가 생기자 언어 설계자들이 어셈블리어로 컴파일하는 고수준 언어를 자유롭게 만든 것처럼, Wasm이 생기자 웹을 위한 새로운 언어를 설계하는 자유도가 생겼다.
Zero 언어(Vercel Labs)가 Wasm을 타깃으로 실험하고, AssemblyScript가 TypeScript 문법으로 Wasm을 생성하는 것은 이 가능성의 초기 발현이다.
장기적으로 Wasm은 웹을 위한 언어 다양성의 기반 인프라가 된다.

과거 JVM이 “한 번 작성하면 어디서나 실행”을 목표로 했지만 결국 Java 생태계에 종속됐던 것과 달리, Wasm은 의도적으로 언어 중립적으로 설계됐다.
특정 언어의 런타임을 내장하지 않고, 이진 형식과 실행 시맨틱만을 명세한다.
이것이 Wasm을 진정한 컴파일 타깃 레이어로 만드는 핵심 결정이다.

### 플러그인 아키텍처의 재발명

소프트웨어 플러그인 아키텍처는 신뢰할 수 없는 코드를 실행하는 문제를 항상 안고 있었다.
Native 플러그인은 프로세스 공간을 공유하므로 악의적이거나 버그가 있는 플러그인이 전체 호스트를 충돌시킬 수 있다.
이를 해결하려면 별도의 프로세스로 격리하거나 언어 VM을 내장해야 했는데, 두 방법 모두 복잡성과 오버헤드를 수반한다.

WebAssembly는 이 문제에 대한 표준화된 해법을 제공한다.
Envoy Proxy가 WASM 필터를 동적으로 로드하고, Fastly와 Cloudflare가 엣지 함수를 Wasm으로 실행하며, Shopify가 앱 확장을 Wasm으로 격리하는 것은 모두 같은 원리의 적용이다.
브라우저 밖에서 Wasm의 주요 가치가 성능이 아니라 **안전한 서드파티 코드 실행**이 되는 이유다.

이 방향이 성숙하면, 소프트웨어 확장성(extensibility)의 표준 인터페이스가 Wasm 기반으로 수렴할 가능성이 있다.
운영체제의 커널 모듈, 데이터베이스의 UDF(사용자 정의 함수), 웹 서버의 미들웨어, 에디터의 플러그인이 모두 Wasm으로 작성된다면, 플러그인 개발자는 하나의 컴파일 타깃을 배우면 어디에나 기여할 수 있게 된다.
eBPF가 리눅스 커널에서 이 역할을 하고 있다면, Wasm은 더 넓은 애플리케이션 계층에서 같은 역할을 노린다.

### 신뢰 경계의 이동

전통적인 웹 보안 모델에서 “신뢰되지 않는 코드”는 외부에서 가져온 JavaScript를 의미했다.
CSP(Content Security Policy), CORS, SameSite 쿠키 등은 모두 이 경계를 관리하는 메커니즘이다.
WebAssembly가 서버 사이드로 확산되면서 신뢰 경계의 위치가 달라진다.
서버에서 임의의 Wasm 모듈을 실행하는 것은 JavaScript를 서버에서 실행하는 것과는 다른 보안 고려사항을 낳는다.

기능 기반(capability-based) 보안 모델이 이 변화에 대응한다.
Wasm 모듈은 호스트가 명시적으로 제공한 인터페이스만 사용할 수 있고, 파일 시스템 접근, 네트워크 연결, 시스템 콜은 모두 호스트의 허가가 필요하다.
이것은 최소 권한 원칙(Principle of Least Privilege)을 런타임 수준에서 강제하는 구조다.

Wasm의 확산이 의미하는 더 큰 그림은 “실행 환경이 코드를 신뢰하는 것”에서 “코드가 요청하는 권한을 실행 환경이 심사하는 것”으로의 이동이다.
이 패러다임이 정착하면, 임의의 코드를 실행하는 두려움이 줄어들고 소프트웨어 생태계의 조합 가능성(composability)이 높아진다.
마이크로서비스가 네트워크 경계로 서비스를 격리했듯, Wasm은 프로세스 내부에서 모듈을 격리하는 다음 단계가 될 수 있다.

## DOOM Rendered via Checkboxes

WebAssembly로 브라우저에서 실행되는 DOOM을 HTML 체크박스로 렌더링한 실험이다.

- <https://healeycodes.com/doom-rendered-via-checkboxes>
- <https://healeycodes.github.io/doom-checkboxes/>
- <https://github.com/healeycodes/doom-checkboxes>
