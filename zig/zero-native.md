# Zero-Native: Zig 기반 네이티브 데스크톱 앱 프레임워크

<https://zero-native.dev/>

<https://github.com/vercel-labs/zero-native>

## 소개

Zero-Native는 Vercel Labs가 개발한 Zig 기반 네이티브 데스크톱·모바일 앱
프레임워크다. 시스템 내장 WebView(macOS의 WKWebView, Linux의 WebKitGTK)를
활용해 Chromium을 번들링하지 않고도 웹 UI를 가진 네이티브 앱을 만들 수 있다.
Electron의 무거움과 Flutter/React Native의 커스텀 렌더링 엔진 없이
"작은 바이너리, 최소 메모리, 즉각적인 리빌드"를 목표로 한다.
Next.js, React, Svelte, Vue 스타터 템플릿을 제공한다.
Apache 2.0 라이선스다.

## 명세

### 아키텍처 구성요소

| 컴포넌트 | 역할                                                        |
| -------- | ----------------------------------------------------------- |
| App      | 앱 메타데이터, WebView 소스, 라이프사이클 훅을 담는 Zig 객체 |
| Runtime  | 이벤트 루프, 윈도우, 브리지 디스패치, 플랫폼 서비스 관리    |
| Bridge   | `window.zero.invoke()`를 통한 JavaScript-to-Zig 통신        |
| Manifest | `app.zon`으로 앱 메타데이터, 권한, 보안 정책, 패키징 설정    |

### 웹 엔진 선택지

두 가지 렌더링 경로를 제공한다.

- **시스템 WebView**: WKWebView(macOS), WebKitGTK(Linux). 경량 앱에 적합하며
  Chromium을 번들링하지 않아 바이너리가 작다.
- **CEF(Chromium Embedded Framework)**: 번들 옵션으로 렌더링 일관성이
  필요할 때 선택한다.

### 보안 모델

WebView는 기본적으로 비신뢰(untrusted) 상태로 취급된다. 네이티브 명령 실행,
네비게이션, 윈도우 API 접근은 모두 명시적 권한 부여가 필요한 옵트인(opt-in)
방식이다. Bridge 통신에는 크기 및 권한 검사가 포함된다.

### 플랫폼 지원

macOS 11 이상, Linux, Windows, iOS, Android를 지원한다.
2026년 5월 현재 v0.1.9까지 출시된 프리릴리즈 소프트웨어다.

## 사용법

```bash
npm install -g zero-native
zero-native init my_app --frontend next
cd my_app
zig build run
```

## 분석

### Tauri와의 비교: Zig vs Rust

Zero-Native는 Tauri와 동일한 포지션에 있다. 시스템 WebView + 경량 네이티브
셸이라는 접근도 같다. 차이는 셸 언어다. Tauri는 Rust, Zero-Native는 Zig다.
Zig는 컴파일 속도가 빠르고, C 상호운용성이 뛰어나며, 번들 크기가 작다.
그러나 생태계가 Rust보다 훨씬 작고, 아직 1.0 버전이 없는 언어다.
Vercel Labs가 Zig를 선택한 것은 컴파일 속도와 바이너리 크기 최적화에 우선순위를
둔 실험적 결정이다. AI 생성 코드 기반의 빠른 개발 이터레이션을 전제로 설계했다면
Zig의 빠른 재빌드가 Rust보다 유리한 요소가 된다.

[GeekNews 댓글](https://news.hada.io/topic?id=29409)에서 xguru는 OpenCode Desktop이
Tauri에서 Electron으로 전환한 사례를 언급하며, 안정성 측면에서는 Electron이
여전히 우위라는 점을 지적했다.

### 시스템 WebView의 기회와 위험

시스템 WebView 전략의 핵심 장점은 바이너리 크기다. Electron 앱은 Chromium을
포함해 최소 100MB를 넘는 반면, 시스템 WebView를 쓰면 셸 바이너리가 수백 KB
수준이 될 수 있다. 그러나 시스템 WebView는 플랫폼마다 다른 버전의 WebKit 또는
EdgeHTML을 쓰기 때문에 렌더링 불일관성이 생긴다. 이것이 Tauri가 선택적 번들
Chromium을 제공하고, Zero-Native가 CEF를 대안으로 두는 이유다.

### Vercel이 데스크톱 프레임워크를 만드는 이유

Vercel은 웹 호스팅·배포 플랫폼 회사다. 그러나 Vercel의 핵심 고객인 웹 개발자들이
점점 더 클라이언트 앱(CLI, 데스크톱 도구, AI 에이전트 UI)을 필요로 하고 있다.
Zero-Native는 웹 개발자가 웹 기술로 네이티브 앱을 만들 수 있는 경로를 제공함으로써
Vercel 생태계를 확장하는 전략으로 읽힌다. 웹 프레임워크(Next.js), 엣지 런타임,
배포 플랫폼에 이어 네이티브 앱 셸까지 도구체인이 전체 스택을 커버하려는 방향이다.

## 비평

### 긍정적 측면

WebView를 비신뢰 상태로 기본 취급하고 모든 네이티브 접근을 옵트인으로 설계한 것은
Electron의 보안 역사에서 교훈을 얻은 접근이다. Electron은 초기에 렌더러 프로세스에서
Node.js API에 자유롭게 접근할 수 있어 다수의 보안 취약점의 원인이 됐다.
Zero-Native는 이 실수를 반복하지 않으려는 의도가 명확하다.
Zig의 빠른 컴파일 속도와 시스템 WebView 우선 + Chromium 번들 옵션 양쪽 지원으로
유연성도 확보했다.

### 한계

Zig는 아직 1.0을 출시하지 않았으며 API가 버전 간에 변경될 수 있다.
Zero-Native 자체도 v0.1.9로 프리릴리즈 상태이고 Windows 지원이 완성되지 않았다.
Tauri 1.0이 2022년에 출시된 것과 비교하면 채택 준비도가 낮다.

"Vercel Labs" 프로젝트는 Vercel의 핵심 제품이 아니다. 실험적 프로젝트로 시작해
중단되거나, 핵심 제품에 흡수되거나, 독립 오픈소스로 분리되는 세 경로 중 하나를
걸을 것이다. 이 불확실성은 장기 의존성으로 채택하기 전에 고려해야 할 리스크다.

## 인사이트

### Electron 대체제 경쟁의 수렴점

Electron은 2013년 GitHub Atom 에디터를 위해 만들어졌고, VS Code, Slack, Discord,
Figma 등 수많은 앱이 이를 채택했다. 그러나 메모리 사용량과 바이너리 크기에 대한
불만이 Tauri, Wails(Go), NeutralinoJS, 그리고 이제 Zero-Native까지 이어지는
"탈 Electron" 흐름을 만들었다. 이 대체제들이 공유하는 설계 — 시스템 WebView,
경량 네이티브 레이어, 안전한 JS-네이티브 브릿지 — 가 수렴하고 있다는 것이
"올바른 설계"가 명확하다는 신호다. 남은 경쟁은 생태계, 안정성, 개발 경험에서
이루어질 것이다.

[GeekNews 댓글](https://news.hada.io/topic?id=29409)에서 tsboard가 지적했듯,
메모리 비용이 높아지는 현시점에서 Electron 방식의 앱은 점점 부담이 된다.
IoT, 엣지 컴퓨팅, 저사양 디바이스 시장이 확대될수록 Zero-Native 같은 접근의
가치는 높아진다.

### 신뢰 경계와 보안 아키텍처

Zero-Native의 `window.zero.invoke()` 브리지와 기본 비신뢰 WebView 모델은
웹과 네이티브의 신뢰 경계를 명시적으로 설계한다. 이것은 단순한 API 선택이 아니라
위협 모델(threat model)의 반영이다. Electron의 초기 `nodeIntegration: true`
기본값은 이 신뢰 경계를 무시한 설계였고, CVE가 쌓이면서 뒤늦게 수정됐다.
Zero-Native는 이 역사를 처음부터 반영해 옵트인 권한 모델로 최소 권한 원칙을
구조적으로 강제한다. 데스크톱 앱 프레임워크가 모바일 앱 권한 모델을 채택한다는
것은 데스크톱과 모바일의 보안 기대치가 수렴하고 있다는 신호다.

### Zig 언어의 도전과 가능성

Rust, Zig, Go가 시스템 수준 도구의 언어로 자리 잡으면서 "고성능이 필요한 레이어는
네이티브 언어로, 사용자 인터페이스는 웹으로"라는 하이브리드 패턴이 굳어지고 있다.
Zero-Native는 이 패턴의 구현체다. Rust가 소유권 시스템으로 메모리 안전성을 컴파일
타임에 강제한다면, Zero-Native는 아키텍처(브리지 권한 모델)로 보안을 구조화하는
접근이다. Zig가 이 레이어에서 장기적인 경쟁력을 가질지는 커뮤니티 성장과 언어 안정성에
달렸다. 그러나 Bun이 Zig로 만들어져 V8 기반 Node.js를 성능으로 압도한 사례처럼,
Zig가 틈새 영역에서 강력한 선택지임은 이미 입증되고 있다. Zero-Native는 그 실험의
연장선이다.
