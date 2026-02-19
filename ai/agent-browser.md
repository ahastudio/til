# agent-browser

- 원문: <https://github.com/vercel-labs/agent-browser>
- 사이트: <https://agent-browser.dev/>

## 요약

AI 에이전트를 위한 헤드리스 브라우저 자동화 CLI다.
Rust 네이티브 바이너리로 50ms 이내에 기동되며,
Node.js 폴백을 지원한다.

핵심은 Snapshot + Refs 시스템으로, DOM 전체 대신
압축된 요소 참조(`@e1`, `@e2`)를 반환해
Playwright MCP 대비 컨텍스트 토큰을 93% 줄인다.

## 아키텍처

```
CLI (Rust) → Daemon (Node.js) → Playwright → Chromium
```

클라이언트-데몬 모델을 사용한다.
Rust CLI가 명령을 받아 Node.js 데몬으로 전달하고,
데몬이 Playwright 브라우저 인스턴스를 관리한다.

네이티브 바이너리가 없으면 Node.js가 직접 실행한다.
Chromium이 기본이고 Firefox, WebKit도 지원한다.

## 핵심 기능

### Snapshot + Refs

AI 에이전트와 브라우저 상호작용의 핵심 워크플로우다.

```
스냅샷 조회 → 접근성 트리에서 ref 파싱
→ ref로 액션 실행 → 재스냅샷
```

접근성 트리 전체를 보내면 15,000+ 토큰을
소비하지만, Snapshot + Refs는 `@e1`, `@e2` 같은
결정적 참조로 요소를 특정하므로 토큰 효율이
극적으로 개선된다.

### 시맨틱 로케이터

CSS 셀렉터 대신 의미 기반으로 요소를 찾는다.

| 로케이터     | 설명                    |
|--------------|-------------------------|
| `role`       | ARIA 역할               |
| `text`       | 텍스트 내용             |
| `label`      | 레이블                  |
| `placeholder`| 플레이스홀더            |
| `alt`        | 대체 텍스트             |
| `testid`     | 테스트 ID               |

### 세션 격리

이름 기반 세션으로 병렬 브라우저 인스턴스를 운영한다.
각 세션은 쿠키, localStorage, 탐색 히스토리, 인증
상태를 독립적으로 유지한다.

AES-256-GCM으로 세션을 암호화할 수 있다.

### 주요 명령어

108개 이상의 명령어를 지원한다.

- **탐색**: `open`, `back`, `forward`, `reload`
- **상호작용**: `click`, `fill`, `type`, `hover`,
  `select`, `check`, `drag`, `upload`
- **정보 조회**: `get text/html/value/attr/title/url`
- **대기**: `wait` (요소, 시간, 텍스트 패턴, URL,
  JavaScript 조건)
- **네트워크**: 요청 가로채기, 목킹, 커스텀 헤더
- **디버그**: 트레이스 기록, DevTools 프로파일링

## 설치 및 사용

```bash
npm install -g agent-browser
agent-browser install  # Chromium 다운로드

# 기본 사용
agent-browser open "https://example.com"
agent-browser snapshot -i  # 인터랙티브 요소만 반환
agent-browser click @e3    # ref로 클릭
```

Claude Code에서 스킬로 설치할 수도 있다:

```bash
mkdir -p .claude/skills/agent-browser
curl -o .claude/skills/agent-browser/SKILL.md \
  https://raw.githubusercontent.com/vercel-labs/\
agent-browser/main/skills/agent-browser/SKILL.md
```

## 클라우드 및 통합

Browserbase, Browser Use, Kernel 등 원격 브라우저
인프라와 연동할 수 있다.

iOS 시뮬레이터 및 실제 디바이스도 Appium을 통해
지원한다.

## 인사이트

### 1) 토큰 효율이 에이전트 브라우저의 핵심 경쟁력이다

LLM의 컨텍스트 윈도우는 유한한 자원이다.
접근성 트리 전체를 보내는 방식은 페이지가 복잡해질수록
토큰을 기하급수적으로 소비한다.

agent-browser의 Snapshot + Refs는 이 문제를
구조적으로 해결한다.
93% 토큰 절감은 단순한 최적화가 아니라, 에이전트가
더 많은 단계를 하나의 컨텍스트 안에서 수행할 수 있게
만드는 질적 변화다.

이것은 "더 싸게"가 아니라
"더 많이 할 수 있게"의 문제다.

### 2) CLI 인터페이스는 에이전트 통합의 최소 저항 경로다

MCP 서버를 설정하고 프로토콜을 맞추는 대신, CLI를
bash로 직접 호출하는 방식은 설정 비용이 거의 없다.

어떤 LLM 에이전트든 셸 명령을 실행할 수 있으므로
통합 장벽이 사실상 사라진다.

이것은 "프로토콜 표준화"와 "실용적 접근성" 사이에서
후자를 선택한 설계 결정이다.

### 3) Rust + Node.js 이중 구조가 실용적이다

Rust로 CLI 기동 속도(50ms 이내)를 확보하면서,
실제 브라우저 자동화는 Playwright(Node.js) 생태계를
그대로 활용한다.

성능이 필요한 인터페이스 계층만 네이티브로 가져가고,
브라우저 제어라는 복잡한 영역은 검증된 도구에 위임한다.

"전부 Rust로 다시 짠다"는 유혹을 피한 현실적 선택이다.

### 4) 시맨틱 로케이터는 AI에 맞는 추상화 수준이다

CSS 셀렉터나 XPath는 DOM 구조에 강하게 결합된다.
페이지 레이아웃이 바뀌면 셀렉터가 깨진다.

ARIA 역할, 텍스트 내용, 레이블 같은 시맨틱 로케이터는
"사용자가 보는 것"에 가까운 추상화다.

LLM이 페이지를 이해하는 방식과 정렬되므로, 에이전트가
생성하는 명령의 정확도와 견고함이 모두 올라간다.

### 5) 세션 격리가 에이전트 병렬 실행의 전제 조건이다

여러 에이전트가 동시에 서로 다른 웹사이트를 탐색하려면
상태 충돌이 없어야 한다.

이름 기반 세션으로 쿠키, 스토리지, 인증을 완전히
분리하고, 암호화까지 지원하는 것은 프로덕션 환경에서의
멀티 에이전트 운영을 염두에 둔 설계다.

## 시장 맥락

에이전틱 브라우저 시장은 2024년 45억 달러에서
2034년 768억 달러로 성장이 전망된다.

agent-browser는 GitHub 스타 14,000+를 확보하며
오픈소스 진영의 주요 도구로 자리잡고 있다.

LLM의 웹 페이지 추론 능력 향상, 브라우저 자동화 도구
성숙, 에이전트 프레임워크 확산이라는 세 가지 흐름이
합류하면서 이 분야가 본격화되고 있다.
