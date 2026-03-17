# Chrome DevTools MCP: AI 에이전트에 브라우저 디버깅 능력을 부여하다

- 공식 블로그:
  [Chrome DevTools MCP](https://developer.chrome.com/blog/chrome-devtools-mcp?hl=ko)
- GitHub:
  [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- 참고:
  [Chrome Debugging Profile + MCP](https://raf.dev/blog/chrome-debugging-profile-mcp/)

## 핵심 요약

Chrome DevTools MCP는 AI 코딩 에이전트(Claude, Gemini, Cursor, Copilot 등)가
Chrome DevTools의 디버깅 기능을 직접 사용할 수 있게 해주는 MCP 서버다. Google이
공개 프리뷰로 출시했다.

에이전트가 코드를 수정하고, 브라우저에서 결과를 확인하고, 네트워크 요청을
분석하고, 성능 트레이스를 실행하는 전체 루프를 사람 개입 없이 수행할 수 있다.

## 설치

MCP 클라이언트 설정에 추가한다:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest",
        "--no-performance-crux",
        "--no-usage-statistics"
      ]
    }
  }
}
```

기본 설정은 외부로 데이터를 전송하므로, 보안을 위해 아래 두 옵션을 적용했다.

- `--no-performance-crux`: 성능 도구가 URL을 Google CrUX API에 전송하지 않는다.
- `--no-usage-statistics`: 사용 통계 수집을 비활성화한다.

가벼운 용도라면 slim 모드:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest",
        "--slim",
        "--headless",
        "--no-performance-crux",
        "--no-usage-statistics"
      ]
    }
  }
}
```

요구 사항:

- Node.js v20.19 이상 LTS
- 최신 안정 Chrome
- npm

## 주요 도구 (29개)

| 분류        | 도구 수 | 예시                                               |
| ----------- | ------- | -------------------------------------------------- |
| 입력 자동화 | 9       | click, fill, fill_form, type_text, press_key       |
| 네비게이션  | 6       | navigate_page, new_page, close_page, wait_for      |
| 에뮬레이션  | 2       | emulate, resize_page                               |
| 성능        | 4       | performance_start_trace, performance_stop_trace    |
| 네트워크    | 2       | list_network_requests, get_network_request         |
| 디버깅      | 6       | take_screenshot, evaluate_script, lighthouse_audit |

## 활용 시나리오

### 1. 실시간 코드 검증

에이전트가 코드를 수정한 뒤 브라우저에서 직접 결과를 확인한다. 스크린샷을 찍어
시각적 회귀를 감지하고, 콘솔 에러를 자동으로 잡아낸다.

### 2. 네트워크·콘솔 진단

CORS 오류, 실패한 API 호출, 콘솔 경고를 에이전트가 직접 확인한다. 소스맵이
적용된 스택 트레이스를 읽을 수 있다.

### 3. 사용자 인터랙션 시뮬레이션

페이지 이동, 폼 작성, 버튼 클릭을 자동화한다. Puppeteer 기반이라 결과를 기다리는
것까지 자동 처리된다.

### 4. 스타일·레이아웃 디버깅

실행 중인 페이지의 DOM과 CSS를 검사해서 레이아웃 문제에 대한 구체적인 수정안을
제시한다.

### 5. 성능 분석 자동화

DevTools 성능 트레이스를 실행하고 결과를 분석한다. LCP가 높은 원인을 찾거나
Lighthouse 감사를 실행할 수 있다.

## 주요 설정 옵션

| 옵션                    | 설명                                  |
| ----------------------- | ------------------------------------- |
| `--headless`            | UI 없이 실행                          |
| `--browserUrl` / `-u`   | 기존 Chrome 인스턴스에 연결           |
| `--wsEndpoint` / `-w`   | 원격 WebSocket 연결                   |
| `--channel`             | Chrome 채널 선택 (stable/canary/beta) |
| `--isolated`            | 임시 프로필로 실행, 종료 시 자동 삭제 |
| `--slim`                | 기본 도구 3개만 노출                  |
| `--no-performance-crux` | CrUX API 호출 비활성화                |

## 인증된 세션에서 사용하기

기본 설정은 격리된 프로필로 실행되기 때문에 로그인 상태를 유지할 수 없다. 인증이
필요한 사이트를 디버깅하려면 별도의 디버그 프로필을 만들어 연결한다.

원격 디버깅 포트(9222)는 로컬 프로세스에 브라우저 제어 권한을 노출한다.
개발·테스트 용도로만 사용하고, 디버그 프로필에서 뱅킹이나 이메일 등 민감한
서비스에 로그인하지 않는다.

### 1단계: 디버깅용 Chrome 실행

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"
```

Chrome 136 이후로 기본 프로필에서 원격 디버깅이 차단되므로 `--user-data-dir`로
별도 프로필을 지정해야 한다.

### 2단계: MCP 서버 연결

```bash
claude mcp add --transport stdio chrome-devtools \
  -- npx -y chrome-devtools-mcp@latest \
  --browserUrl=http://127.0.0.1:9222 \
  --no-performance-crux \
  --no-usage-statistics
```

### 3단계: 확인

에이전트에게 사이트로 이동 후 스크린샷을 찍도록 요청해서 연결을 확인한다.

이 디버그 프로필에서 필요한 사이트에 로그인해두면, 에이전트가 인증된 상태로
작업할 수 있다.

## 인사이트

### 1. "에이전트의 눈"이 열렸다

기존 AI 코딩 에이전트의 가장 큰 약점은 코드를 수정한 뒤 결과를 볼 수 없다는
것이었다. Chrome DevTools MCP는 이 피드백 루프를 완성한다. 에이전트가 코드를
고치고, 브라우저에서 확인하고, 문제가 있으면 다시 고치는 자율 디버깅 사이클이
가능해진다. 이것은 단순한 도구 추가가 아니라 에이전트의 능력 범위를 질적으로
확장하는 변화다.

### 2. WebMCP와의 역할 분담

같은 Chrome 팀에서 나온 WebMCP(브라우저 네이티브 API)와 Chrome DevTools MCP(MCP
서버)는 방향이 다르다. WebMCP는 웹사이트가 에이전트에게 자신의 기능을 선언하는
것이고, DevTools MCP는 에이전트가 브라우저를 디버깅 도구로 사용하는 것이다.
하나는 "웹사이트 → 에이전트" 방향이고, 다른 하나는 "에이전트 → 브라우저"
방향이다.

### 3. 29개 도구의 실용적 완성도

입력 자동화 9개, 네비게이션 6개, 디버깅 6개 등 29개 도구 구성은 실제 웹 개발
디버깅 워크플로우를 상당히 포괄한다. 특히 `fill_form`, `handle_dialog`,
`upload_file` 같은 도구는 실무에서 자주 마주치는 시나리오를 정확히 겨냥한다.
도구 하나하나가 "실제로 써보니 이게 필요하더라"라는 경험에서 나온 것으로 보인다.

### 4. 디버그 프로필 패턴의 중요성

공식 설정만으로는 인증된 세션을 다룰 수 없다는 한계가 있다. `--user-data-dir`로
별도 디버그 프로필을 만드는 패턴은 이 한계를 깔끔하게 우회한다. Chrome 136의
보안 강화로 기본 프로필에서 원격 디버깅이 차단됐기 때문에 이 패턴이 더욱
중요해졌다. 공식 문서에서 다루지 않는 실전 지식이다.

### 5. 프론트엔드 개발 워크플로우의 변화

성능 트레이스 → 분석 → 최적화 → 재측정 사이클을 에이전트가 자동으로 돌릴 수 있게
되면, 프론트엔드 개발자의 역할이 "직접 디버깅하는 사람"에서 "에이전트의 디버깅
결과를 검토하는 사람"으로 이동한다. Lighthouse 감사를 에이전트에게 맡기고,
개발자는 아키텍처 결정에 집중하는 분업이 현실화된다.

## 관련 링크

- [Chrome DevTools MCP 공식 블로그](https://developer.chrome.com/blog/chrome-devtools-mcp?hl=ko)
- [GitHub: ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Rafael Mendiola: Chrome Debugging Profile + MCP](https://raf.dev/blog/chrome-debugging-profile-mcp/)
- [WebMCP Early Preview](/chrome/webmcp-early-preview.md)
