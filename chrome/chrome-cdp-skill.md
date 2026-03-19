# `chrome-cdp` skill

AI 에이전트가 실행 중인 Chrome 브라우저와 직접 상호작용할 수 있게 해주는
경량 CDP(Chrome DevTools Protocol) CLI 도구입니다.

<https://github.com/pasky/chrome-cdp-skill>

## 핵심 가치

**"이미 열려 있는 브라우저를 그대로 씁니다."**

Puppeteer 같은 도구는 격리된 새 브라우저를 띄웁니다. chrome-cdp-skill은
사용자가 실제로 사용 중인 Chrome 탭에 연결합니다. 로그인 상태, 페이지
상태, 열린 탭 전부를 AI 에이전트가 그대로 활용할 수 있습니다.

## 설치

`skills/chrome-cdp/` 디렉토리를 복사.

- Node.js 22+ 필요.
- npm install 불필요.

Chrome에서 `chrome://inspect/#remote-debugging` 토글을 켜야 합니다.

Chrome, Chromium, Brave, Edge, Vivaldi를 자동 감지합니다.

## 명령어

| 명령어                           | 설명                                       |
| -------------------------------- | ------------------------------------------ |
| `list`                           | 열린 탭 목록                               |
| `snap <target>`                  | 접근성 트리 스냅샷                         |
| `eval <target> "expr"`           | JavaScript 실행                            |
| `shot <target> [file]`           | 스크린샷 캡처 (DPR 좌표 매핑 포함)         |
| `html <target> [".selector"]`    | 전체 HTML 또는 CSS 선택자 범위 HTML        |
| `nav <target> <url>`             | URL 이동 후 로드 완료 대기                 |
| `net <target>`                   | 네트워크 리소스 타이밍                     |
| `click <target> "selector"`      | CSS 선택자로 요소 클릭                     |
| `clickxy <target> <x> <y>`       | CSS 픽셀 좌표로 클릭                       |
| `type <target> "text"`           | 포커스된 요소에 텍스트 입력                |
| `loadall <target> "selector"`    | "더 보기" 버튼 반복 클릭                   |
| `evalraw <target> <method> [json]` | 로우 CDP 명령 직접 전송                  |
| `open [url]`                     | 새 탭 열기                                 |
| `stop [target]`                  | 데몬 종료                                  |

`<target>`은 `list` 출력의 targetId 고유 접두사입니다.

## 아키텍처

```
CLI (cdp.mjs)
  │
  ├── list / open ──→ Chrome CDP WebSocket (직접 연결)
  │
  └── 페이지 명령 ──→ Unix Socket (NDJSON) ──→ 탭별 데몬
                                                  │
                                                  └──→ Chrome CDP WebSocket
                                                       (Target.attachToTarget)
```

핵심 설계 결정은 **탭별 상주 데몬**입니다. 첫 접근 시 Chrome의
"디버깅 허용" 모달이 한 번 뜨고, 이후 같은 탭 명령은 데몬을
재사용합니다. 20분 유휴 시 자동 종료됩니다.

## 코드 분석

단일 파일(cdp.mjs) 870줄입니다. 외부 의존성 제로. Node.js 22의
내장 WebSocket만 사용합니다.

### CDP 클래스

WebSocket 기반 CDP 클라이언트입니다. private 필드(`#ws`, `#id`,
`#pending`, `#eventHandlers`)로 캡슐화했습니다.

```javascript
class CDP {
  #ws; #id = 0; #pending = new Map(); #eventHandlers = new Map();

  send(method, params = {}, sessionId) {
    // 요청 ID 기반 프로미스 매핑 + 타임아웃 15초
  }

  waitForEvent(method, timeout) {
    // 취소 가능한 이벤트 대기. cancel() 메서드로 정리.
  }
}
```

요청-응답 매칭을 `#pending` Map으로 관리하고, CDP 이벤트는
`#eventHandlers` Map에 Set으로 누적합니다. `waitForEvent`가
`cancel()` 핸들을 반환해 타임아웃 누수를 방지하는 점이 깔끔합니다.

### 데몬 IPC

CLI와 데몬 사이 통신은 Unix 소켓 위의 NDJSON(Newline-Delimited
JSON) 프로토콜입니다.

```
요청: {"id": 1, "cmd": "snap", "args": []}
응답: {"id": 1, "ok": true, "result": "..."}
```

`net.createServer`로 스트림을 받아 줄 단위로 파싱합니다. 불완전한
마지막 줄은 버퍼에 보관하고 다음 청크와 합칩니다.

### 브라우저 자동 탐지

`getWsUrl()`이 macOS, Linux, Windows의 알려진 경로에서
`DevToolsActivePort` 파일을 순회 탐색합니다. Chrome, Chromium,
Brave, Edge, Vivaldi까지 커버합니다. `CDP_PORT_FILE` 환경 변수로
커스텀 경로도 지원합니다.

### 멀티 프로필 연결

`DevToolsActivePort`는 프로필 단위가 아니라 **Chrome 프로세스
단위** 파일입니다. 코드가 탐색하는 경로는 다음과 같습니다:

```
~/.config/google-chrome/DevToolsActivePort          # 브라우저 루트
~/.config/google-chrome/Default/DevToolsActivePort  # Default 프로필
```

`candidates.find()`로 **첫 번째 발견된 파일**에 연결하므로,
멀티 프로필(Default, Profile 1, Profile 2…)이어도 같은 Chrome
프로세스 안이면 **모든 프로필의 탭이 `list`에 전부** 나옵니다.
프로필 구분 없이 섞여서 표시됩니다.

`Profile 1`, `Profile 2` 같은 커스텀 프로필 경로는 탐색하지
않습니다. 별도 `--user-data-dir`로 완전히 분리된 Chrome
인스턴스를 띄우는 경우, `CDP_PORT_FILE` 환경 변수로 해당
인스턴스의 `DevToolsActivePort` 경로를 직접 지정해야 합니다.

### 좌표 시스템 처리

`shotStr()`이 DPR(Device Pixel Ratio)을 3단계로 감지합니다:
Page.getLayoutMetrics → Emulation.getDeviceMetricsOverride →
`window.devicePixelRatio`. 스크린샷 이미지 픽셀과 CSS 픽셀 간
변환 가이드를 출력에 포함합니다.

### 네비게이션

`navStr()`은 `Page.navigate` 후 `Page.loadEventFired` 이벤트를
대기합니다. `loaderId`가 없으면(같은 페이지 내 이동 등) 이벤트
대기를 건너뜁니다. 이후 `document.readyState === 'complete'`를
200ms 폴링으로 확인합니다.

### 크로스오리진 대응

`typeStr()`은 `Runtime.evaluate` 대신 `Input.insertText` CDP
명령을 사용합니다. 크로스오리진 iframe에서도 동작하는 선택입니다.

## vs chrome-devtools-mcp

| 항목             | chrome-cdp-skill       | chrome-devtools-mcp      |
| ---------------- | ---------------------- | ------------------------ |
| 연결 모델        | 탭별 상주 데몬         | 명령마다 재연결          |
| 허용 모달        | 탭당 1회               | 명령마다 반복            |
| 100+ 탭         | 안정 동작              | 열거 타임아웃            |
| 의존성           | Node.js 22 내장만      | Puppeteer 등             |
| 코드 규모        | 단일 파일 870줄        | 다수 파일                |

## 비평

### 잘한 점

**의존성 제로 설계**. Node.js 22의 내장 WebSocket 하나로 CDP
클라이언트를 구현했습니다. Puppeteer 없이 870줄로 스크린샷, 접근성
트리, JavaScript 실행, 클릭, 타이핑, 네비게이션을 모두 다룹니다.
설치 마찰이 사실상 없습니다.

**탭별 데몬 아키텍처**. Chrome의 "디버깅 허용" 모달 문제를
우아하게 해결했습니다. 한 번 허용하면 데몬이 세션을 유지하므로
이후 명령은 즉시 실행됩니다. chrome-devtools-mcp가 명령마다
재연결하면서 모달이 반복되는 문제를 정면으로 해결한 것입니다.

**NDJSON IPC**. CLI ↔ 데몬 간 프로토콜이 단순합니다. 줄바꿈으로
구분된 JSON이라 디버깅이 쉽고, 외부 스크립트에서도 Unix 소켓에
직접 연결해 자동화할 수 있습니다.

**접근성 트리 활용**. `snap` 명령이 DOM 대신 접근성 트리를
추출합니다. AI 에이전트가 페이지 구조를 파악하기에 DOM보다 훨씬
효율적입니다. `InlineTextBox` 필터링과 깊이 제한(10)으로 출력을
제어합니다.

### 아쉬운 점

**에러 복구 부재**. WebSocket 연결이 끊기면 데몬이 즉시
종료됩니다. 재연결 로직이 없습니다. 네트워크 불안정이나 Chrome
업데이트 시 모든 데몬이 죽고, 사용자가 수동으로 재시작해야
합니다.

**테스트 없음**. 870줄의 코드에 테스트가 하나도 없습니다.
CDP 프로토콜 모킹이 어려운 건 사실이지만, 최소한 `resolvePrefix`,
`formatPageList`, `getDisplayPrefixLength` 같은 순수 함수는
단위 테스트가 가능합니다.

**단일 파일의 한계**. 870줄이 하나의 파일에 있습니다. CDP 클래스,
명령 구현, 데몬 로직, CLI 파싱이 모두 섞여 있습니다. 현재
규모에서는 관리 가능하지만, 명령이 추가될수록 부담이 커질
것입니다.

**보안 경계 부재**. `eval` 명령이 임의의 JavaScript를 페이지
컨텍스트에서 실행합니다. `nav` 명령은 http/https만 허용하지만,
도메인 제한은 없습니다. AI 에이전트가 악의적 프롬프트에 의해
민감한 페이지에서 데이터를 추출하거나 조작할 수 있습니다.

## 인사이트

### 1. "도구의 눈"이 아니라 "사용자의 눈"을 공유하는 것

브라우저 자동화의 역사는 "격리"의 역사였습니다. Selenium은 별도
WebDriver를 띄웠고, Puppeteer는 `--headless`를 기본으로 했고,
Playwright는 브라우저 바이너리까지 자체 번들링합니다. 모두 "깨끗한
슬레이트에서 시작하는 것"을 미덕으로 여겼습니다. 테스트의
재현성을 위해서는 올바른 선택이었습니다.

chrome-cdp-skill은 이 전제를 정면으로 뒤집습니다. "사용자가
지금 보고 있는 그 브라우저"에 연결합니다. 이것은 단순한 편의가
아니라 패러다임 전환입니다. 자동화 도구가 "도구의 세계"에서
작업하는 것과 "사용자의 세계"에서 작업하는 것은 근본적으로
다릅니다.

격리된 브라우저에서 로그인을 재현하려면 쿠키 주입, OAuth 토큰
관리, 2FA 우회 같은 복잡한 인프라가 필요합니다. 라이브 세션
연결은 이 모든 것을 "이미 해결된 문제"로 만들어 버립니다.
사용자가 이미 로그인했으므로 AI는 그냥 쓰면 됩니다. 이것이
얼마나 큰 마찰 제거인지는 직접 써 보면 체감됩니다.

더 중요한 것은 "공유 컨텍스트"의 의미입니다. 사용자가 "이 페이지
좀 봐줘"라고 말했을 때, AI가 실제로 그 페이지를 볼 수 있습니다.
사용자가 채워 넣은 폼 데이터, 스크롤 위치, 열어둔 드롭다운까지
전부. 이것은 "페어 프로그래밍에서 같은 화면을 보는 것"과
같습니다. 격리된 브라우저로는 이 경험을 재현할 수 없습니다.

### 2. 데몬 패턴은 "프로토콜의 마찰"을 흡수하는 범용 전략이다

Chrome의 디버깅 허용 모달은 보안 기능입니다. 하지만 매 명령마다
재연결하면 이 보안 기능이 UX를 파괴합니다. chrome-devtools-mcp가
정확히 이 문제에 걸려 넘어졌습니다.

chrome-cdp-skill의 탭별 데몬은 이 긴장을 우아하게 해결합니다.
"연결은 오래 유지하되, 명령은 IPC로 전달한다"는 분리입니다.
그런데 이 패턴은 CDP에만 해당하는 것이 아닙니다.

SSH 멀티플렉싱(`ControlMaster`)이 정확히 같은 패턴입니다. SSH
연결의 핸드셰이크와 인증이 비싸니, 하나의 마스터 연결을 유지하고
후속 세션은 Unix 소켓을 통해 다중화합니다. Docker 데몬도
마찬가지입니다. containerd와의 gRPC 연결을 데몬이 유지하고,
`docker` CLI는 Unix 소켓으로 데몬에 명령을 전달합니다.

공통 구조는 이렇습니다:

```
[값비싼 연결] ← 데몬이 유지
[가벼운 IPC] ← CLI가 사용
```

"프로토콜이 비싼 초기 비용을 요구할 때, 상주 데몬으로 그 비용을
상각한다." 이 패턴을 알고 있으면, 유사한 문제를 만났을 때 바로
적용할 수 있습니다. 예를 들어 LSP 서버, 데이터베이스 커넥션 풀,
gRPC 채널 관리 등에서도 본질적으로 같은 전략이 작동합니다.

### 3. 접근성 트리는 "의미론적 압축"이다

웹 페이지를 AI에게 전달하는 방법은 세 가지입니다:

1. **DOM**: 수천 줄의 HTML. 스타일, 레이아웃, 스크립트, 광고 태그
   전부 포함. 노이즈가 압도적입니다.
2. **스크린샷**: 시각 정보는 풍부하지만, 비전 모델 비용이 높고,
   텍스트 추출 정확도가 떨어지며, 보이지 않는 상태(aria-label,
   disabled 속성 등)를 놓칩니다.
3. **접근성 트리**: 브라우저가 이미 계산해 둔 "의미 구조".
   `[button] Submit`, `[textbox] Email = user@...` 같은 포맷.

접근성 트리가 AI에게 최적인 이유는 "의미론적 압축"이기 때문입니다.
브라우저는 이미 DOM을 해석해서 "사람에게 의미 있는 요소"만
추출해 놓았습니다. `<div class="btn-primary-lg mt-4 px-6">`이
접근성 트리에서는 `[button] Submit`이 됩니다. CSS 클래스, 중첩된
wrapper div, 장식용 span 따위는 전부 사라지고 순수한 의미만
남습니다.

이것은 "AI를 위한 DOM 파싱"을 처음부터 다시 만들 필요가 없다는
뜻입니다. 브라우저가 이미 수십 년간 스크린 리더를 위해 이
작업을 해 왔습니다. chrome-cdp-skill은 그 성과를 AI 에이전트
용도로 전용한 것입니다.

Playwright의 `page.accessibility.snapshot()`도, 그리고 OpenAI의
Operator와 Anthropic의 computer use도 접근성 트리를 핵심
입력으로 활용합니다. "접근성 트리 = AI의 눈"이라는 공식은 이미
업계 합의에 가깝습니다. chrome-cdp-skill의 `snap` 명령은 이
흐름의 가장 가벼운 구현입니다.

### 4. 870줄이 던지는 질문: "우리는 얼마나 불필요한 것을 짊어지고 있는가"

Puppeteer의 코드베이스는 수만 줄입니다. Playwright는 더 큽니다.
이 도구들은 브라우저 바이너리 다운로드, 자동 대기, 선택자 엔진,
네트워크 인터셉션, 트레이싱, 코드 생성기 등 거대한 추상화 계층을
제공합니다. 그리고 그 추상화 계층 자체가 디버깅의 대상이 되곤
합니다.

chrome-cdp-skill은 870줄로 "AI 에이전트가 브라우저를 조작하는
데 필요한 것"을 전부 구현했습니다. 비결은 간단합니다. **CDP
프로토콜에 직접 말을 건 것**입니다. `Page.navigate`를 호출하기
위해 Puppeteer의 `page.goto()`가 필요하지 않습니다. WebSocket
으로 JSON을 보내면 됩니다.

이것은 "프레임워크 vs 프로토콜" 선택의 극단적 사례입니다.
프레임워크는 편의를 제공하지만 복잡성도 함께 가져옵니다.
프로토콜을 직접 다루면 코드가 극적으로 줄어드는 대신, 개발자가
프로토콜을 이해해야 합니다. chrome-cdp-skill의 저자는 CDP
프로토콜을 충분히 이해하고 있었기에 870줄로 충분했습니다.

Node.js 22가 WebSocket을 내장하면서 이 접근이 가능해졌다는 점도
중요합니다. 1년 전이었다면 `ws` 패키지가 필요했을 것이고,
"의존성 제로"라는 매력이 사라졌을 것입니다. 플랫폼이 성숙하면
래퍼의 존재 이유가 줄어듭니다. 이 패턴은 반복됩니다—fetch API가
axios의 필요성을 줄인 것처럼.

### 5. NDJSON은 "에이전트 시대의 TCP"가 될 수 있다

CLI ↔ 데몬 간 IPC로 NDJSON을 선택한 것은 우연이 아닙니다.
대안들을 비교해 보면 이유가 명확해집니다:

- **JSON-RPC**: 스키마 정의와 에러 코드 체계가 필요합니다.
  870줄짜리 도구에는 과합니다.
- **gRPC**: protobuf 컴파일, HTTP/2, 그리고 빌드 의존성. 경량
  도구와는 방향이 다릅니다.
- **MessagePack/CBOR**: 바이너리라 디버깅이 어렵습니다.
  `socat`으로 파이프에 찍어 볼 수 없습니다.

NDJSON은 이 모든 것의 반대입니다. 줄바꿈으로 메시지를 구분하고,
각 줄이 완전한 JSON입니다. 구현은 `line.split('\n').map(JSON.parse)`
수준이고, 디버깅은 `cat` 하나로 됩니다. 스트리밍도 자연스럽습니다.

MCP(Model Context Protocol)도 JSON-RPC 위에 구축되어 있지만,
전송 계층에서는 결국 NDJSON(stdio 모드)을 씁니다. Docker의
빌드 출력도 NDJSON이고, ndjson.org 스펙 자체가 "스트리밍
JSON"을 위해 만들어졌습니다. AI 에이전트 도구들이 서로 통신하는
경량 프로토콜로 NDJSON이 사실상 표준으로 굳어지고 있습니다.

### 6. "허용 모달"이 드러내는 에이전트 보안의 근본 딜레마

Chrome이 원격 디버깅 연결마다 "허용" 모달을 띄우는 것은 올바른
보안 설계입니다. 하지만 chrome-cdp-skill의 데몬이 이 모달을
탭당 1회로 줄인 것은, 보안과 사용성 사이의 트레이드오프를
명시적으로 선택한 것입니다.

이 트레이드오프는 AI 에이전트 도구 전반에 걸친 근본 딜레마를
드러냅니다. `eval` 명령은 임의의 JavaScript를 실행합니다.
`nav` 명령은 어떤 URL로든 이동합니다. AI가 프롬프트 인젝션에
의해 악의적 명령을 실행하면, 사용자의 라이브 세션—로그인된
은행 사이트, 이메일, 사내 시스템—이 공격 표면이 됩니다.

격리된 브라우저였다면 피해가 제한됩니다. 하지만 chrome-cdp-skill
의 핵심 가치인 "라이브 세션 연결"이 동시에 최대 약점이 됩니다.
이것은 chrome-cdp-skill만의 문제가 아닙니다. AI 에이전트에게
"사용자의 실제 환경"에 대한 접근 권한을 줄수록, 에이전트가
수행할 수 있는 유용한 작업과 위험한 작업이 동시에 늘어납니다.

아직 업계에 정답은 없습니다. 도메인 화이트리스트, 명령별 권한
체계, 샌드박스 실행 모드 같은 것들이 논의되고 있지만, 어느 것도
"라이브 세션의 편의"와 "보안"을 동시에 만족시키지 못합니다.
chrome-cdp-skill은 이 딜레마의 가장 선명한 사례 중 하나입니다.

### 7. "탭별 데몬"이 시사하는 에이전트 아키텍처의 미래

chrome-cdp-skill의 아키텍처를 한 발 물러서 보면, 흥미로운
구조가 보입니다:

```
에이전트(CLI) → 경량 IPC → 리소스별 상주 프로세스 → 실제 시스템
```

이것은 브라우저 탭에만 적용되는 패턴이 아닙니다. AI 에이전트가
다양한 외부 시스템(데이터베이스, API, 파일 시스템, 클라우드
인프라)과 상호작용해야 할 때, 각 리소스에 대해 "연결을 유지하는
경량 데몬"을 두는 것은 자연스러운 확장입니다.

MCP 서버가 이미 이 방향으로 가고 있습니다. 각 MCP 서버는
특정 시스템에 대한 "상주 연결"을 유지하고, 에이전트는 표준화된
프로토콜로 명령을 전달합니다. chrome-cdp-skill의 탭별 데몬은
MCP 서버의 축소판이라고 볼 수 있습니다. 다만 MCP가 표준화와
발견(discovery)을 해결하려는 반면, chrome-cdp-skill은 단일 목적에
집중해서 극단적 단순성을 달성했습니다.

"하나의 거대한 에이전트"가 모든 것을 직접 다루는 것이 아니라,
"리소스별 경량 데몬의 메시"가 에이전트의 팔다리가 되는 구조.
chrome-cdp-skill은 이 미래의 가장 작고 완성된 프로토타입입니다.
