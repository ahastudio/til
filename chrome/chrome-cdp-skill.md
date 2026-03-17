# chrome-cdp-skill

AI 에이전트가 실행 중인 Chrome 브라우저와 직접 상호작용할 수 있게 하는
경량 CDP(Chrome DevTools Protocol) CLI 도구.

<https://github.com/pasky/chrome-cdp-skill>

## 핵심 가치

**"이미 열려 있는 브라우저를 그대로 쓴다."**

Puppeteer 같은 도구는 격리된 새 브라우저를 띄운다. chrome-cdp-skill은
사용자가 실제로 사용 중인 Chrome 탭에 연결한다. 로그인 상태, 페이지
상태, 열린 탭 전부를 AI 에이전트가 그대로 활용할 수 있다.

## 설치

```bash
# pi skill 사용자
pi install git:github.com/pasky/chrome-cdp-skill@v1.0.2

# 다른 에이전트 (Claude Code, Cursor 등)
# skills/chrome-cdp/ 디렉토리를 복사. Node.js 22+ 필요, npm install 불필요.
```

Chrome에서 `chrome://inspect/#remote-debugging` 토글을 켜야 한다.
Chrome, Chromium, Brave, Edge, Vivaldi를 자동 감지한다.

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

`<target>`은 `list` 출력의 targetId 고유 접두사다.

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

핵심 설계 결정: **탭별 상주 데몬**. 첫 접근 시 Chrome의 "디버깅
허용" 모달이 한 번 뜨고, 이후 같은 탭 명령은 데몬을 재사용한다.
20분 유휴 시 자동 종료.

## 코드 분석

단일 파일(cdp.mjs) 870줄. 외부 의존성 제로. Node.js 22의 내장
WebSocket만 사용한다.

### CDP 클래스

WebSocket 기반 CDP 클라이언트. private 필드(`#ws`, `#id`,
`#pending`, `#eventHandlers`)로 캡슐화했다.

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
`#eventHandlers` Map에 Set으로 누적한다. `waitForEvent`가
`cancel()` 핸들을 반환해 타임아웃 누수를 방지하는 점이 깔끔하다.

### 데몬 IPC

CLI와 데몬 사이 통신은 Unix 소켓 위의 NDJSON(Newline-Delimited
JSON) 프로토콜이다.

```
요청: {"id": 1, "cmd": "snap", "args": []}
응답: {"id": 1, "ok": true, "result": "..."}
```

`net.createServer`로 스트림을 받아 줄 단위로 파싱한다. 불완전한
마지막 줄은 버퍼에 보관하고 다음 청크와 합친다.

### 브라우저 자동 탐지

`getWsUrl()`이 macOS, Linux, Windows의 알려진 경로에서
`DevToolsActivePort` 파일을 순회 탐색한다. Chrome, Chromium,
Brave, Edge, Vivaldi까지 커버한다. `CDP_PORT_FILE` 환경 변수로
커스텀 경로도 지원한다.

### 좌표 시스템 처리

`shotStr()`이 DPR(Device Pixel Ratio)을 3단계로 감지한다:
Page.getLayoutMetrics → Emulation.getDeviceMetricsOverride →
`window.devicePixelRatio`. 스크린샷 이미지 픽셀과 CSS 픽셀 간
변환 가이드를 출력에 포함한다.

### 네비게이션

`navStr()`은 `Page.navigate` 후 `Page.loadEventFired` 이벤트를
대기한다. `loaderId`가 없으면(같은 페이지 내 이동 등) 이벤트
대기를 건너뛴다. 이후 `document.readyState === 'complete'`를
200ms 폴링으로 확인한다.

### 크로스오리진 대응

`typeStr()`은 `Runtime.evaluate` 대신 `Input.insertText` CDP
명령을 사용한다. 크로스오리진 iframe에서도 동작하는 선택이다.

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
클라이언트를 구현했다. Puppeteer 없이 870줄로 스크린샷, 접근성
트리, JavaScript 실행, 클릭, 타이핑, 네비게이션을 모두 다룬다.
설치 마찰이 사실상 없다.

**탭별 데몬 아키텍처**. Chrome의 "디버깅 허용" 모달 문제를
우아하게 해결했다. 한 번 허용하면 데몬이 세션을 유지하므로
이후 명령은 즉시 실행된다. chrome-devtools-mcp가 명령마다
재연결하면서 모달이 반복되는 문제를 정면으로 해결한 것이다.

**NDJSON IPC**. CLI ↔ 데몬 간 프로토콜이 단순하다. 줄바꿈으로
구분된 JSON이라 디버깅이 쉽고, 외부 스크립트에서도 Unix 소켓에
직접 연결해 자동화할 수 있다.

**접근성 트리 활용**. `snap` 명령이 DOM 대신 접근성 트리를
추출한다. AI 에이전트가 페이지 구조를 파악하기에 DOM보다 훨씬
효율적이다. `InlineTextBox` 필터링과 깊이 제한(10)으로 출력을
제어한다.

### 아쉬운 점

**에러 복구 부재**. WebSocket 연결이 끊기면 데몬이 즉시
종료된다. 재연결 로직이 없다. 네트워크 불안정이나 Chrome
업데이트 시 모든 데몬이 죽고, 사용자가 수동으로 재시작해야
한다.

**테스트 없음**. 870줄의 코드에 테스트가 하나도 없다.
CDP 프로토콜 모킹이 어려운 건 사실이지만, 최소한 `resolvePrefix`,
`formatPageList`, `getDisplayPrefixLength` 같은 순수 함수는
단위 테스트가 가능하다.

**단일 파일의 한계**. 870줄이 하나의 파일에 있다. CDP 클래스,
명령 구현, 데몬 로직, CLI 파싱이 모두 섞여 있다. 현재 규모에서는
관리 가능하지만, 명령이 추가될수록 부담이 커질 것이다.

**보안 경계 부재**. `eval` 명령이 임의의 JavaScript를 페이지
컨텍스트에서 실행한다. `nav` 명령은 http/https만 허용하지만,
도메인 제한은 없다. AI 에이전트가 악의적 프롬프트에 의해
민감한 페이지에서 데이터를 추출하거나 조작할 수 있다.

## 인사이트

### 1. "라이브 세션 연결"이라는 발상의 전환

브라우저 자동화 도구는 대부분 격리된 새 인스턴스를 전제한다.
chrome-cdp-skill은 "사용자의 실제 브라우저"에 연결하는 역발상을
취했다. 이로써 로그인, 쿠키, 확장 프로그램, 페이지 상태 등
"컨텍스트"가 공짜로 따라온다. AI 에이전트가 "사용자가 보고 있는
것"을 함께 볼 수 있다는 것은 협업의 질을 근본적으로 바꾼다.

### 2. 데몬 패턴이 CDP의 구조적 약점을 보완한다

Chrome의 원격 디버깅은 연결당 한 번 "허용" 모달을 띄운다.
이것은 보안 기능이지만, 매 명령마다 재연결하면 UX가 파괴된다.
탭별 상주 데몬은 이 긴장을 해결하는 실용적 패턴이다.
"연결은 오래 유지하되, 명령은 IPC로 전달한다"는 분리가 핵심.

### 3. 접근성 트리는 AI 에이전트의 최적 시각이다

DOM은 AI에게 너무 많은 정보를 준다. 스크린샷은 해석 비용이 높다.
접근성 트리는 "사람이 인지하는 수준의 구조"를 제공하면서
토큰 효율이 높다. `[role] name = value` 포맷은 AI가 파싱하기에도
이상적이다. 브라우저 자동화에서 접근성 트리가 "AI의 눈"으로
자리잡는 추세를 확인할 수 있다.

### 4. 870줄이 보여주는 "충분한 소프트웨어"

Puppeteer는 수만 줄이다. chrome-cdp-skill은 870줄로 핵심
유스케이스를 모두 커버한다. 의존성 제로, 설치 마찰 제로,
Node.js 내장 API만 사용. 이것은 "최소한의 추상화로 프로토콜에
직접 말 걸기"의 힘을 보여준다. 복잡한 래퍼 대신 프로토콜을
직접 다루면 코드가 극적으로 줄어든다.

### 5. NDJSON이 에이전트 도구의 사실상 표준이 되고 있다

CLI ↔ 데몬 간 프로토콜로 NDJSON을 선택한 것은 우연이 아니다.
JSON-RPC, gRPC 같은 대안이 있지만, NDJSON은 구현이 간단하고
디버깅이 쉽고 스트리밍에 적합하다. AI 에이전트 도구 생태계에서
NDJSON이 경량 IPC의 공통어로 자리잡고 있다.
