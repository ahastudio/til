# figma-use — CDP 기반 Figma CLI 및 MCP 서버

<https://github.com/dannote/figma-use>

## 소개

`figma-use`는 터미널에서 Figma를 제어하는 오픈소스 CLI 도구다.
Chrome DevTools Protocol(CDP)을 통해 Figma 데스크탑 앱과 직접 통신하므로 플러그인
설치 없이 동작한다.
100개 이상의 명령으로 도형·텍스트·컴포넌트 생성, 스타일 설정, 이미지 내보내기,
디자인 시스템 검사를 수행할 수 있다.
TypeScript로 작성되었으며 MIT 라이선스다(v0.13.3, 별 549개, 포크 38개).

## 시작하기

Figma를 원격 디버깅 포트를 열어 실행한 뒤 `figma-use`를 설치한다.

```bash
# macOS — Figma 디버깅 모드 시작
open -a Figma --args --remote-debugging-port=9222

# 설치
npm install -g figma-use

# 연결 확인
figma-use status
```

## 두 가지 사용 방식

### 명령형(Imperative)

플래그로 요소를 직접 생성한다.

```bash
figma-use create frame --width 400 --height 300 --fill "#FFF"
figma-use create icon mdi:home --size 32 --color "#3B82F6"
figma-use create text "Hello" --size 24 --color "#000"
```

### 선언형(Declarative) — JSX

JSX를 파이프로 넘기면 Figma 노드로 렌더링한다.

```bash
echo '<Frame style={{p: 24, gap: 16}}>
  <Text>Card Title</Text>
</Frame>' | figma-use render --stdin
```

## 주요 기능

### 요소 및 레이아웃

Frame, Rectangle, Ellipse, Text, Line, Star, Polygon, Vector, Group, Icon, Image를
생성할 수 있다.
CSS Grid 레이아웃(`cols`, `rows`, `gap`)을 지원해 캘린더, 대시보드, 갤러리 같은
격자 구조를 만들 수 있다.

### 아이콘 시스템

Iconify에서 150,000개 이상의 아이콘을 `mdi:home`, `lucide:star` 형태로 직접
삽입한다.
별도 다운로드나 가져오기 없이 이름만으로 사용 가능하다.

### 컴포넌트 및 변형

`defineComponent`로 마스터 컴포넌트를 만들고, `defineComponentSet`으로 모든 변형
조합을 Figma ComponentSet으로 자동 생성한다.

### JSX 내보내기 및 Storybook

Figma 노드를 React JSX로 변환하고, Storybook 스토리로도 내보낼 수 있다.

### 검사 및 분석

XPath 선택자로 노드를 검색하고, 색상 팔레트·타이포그래피·간격·반복 패턴을 분석한다.

```bash
figma-use query "//FRAME[@width < 300]"
figma-use analyze colors --show-similar
figma-use analyze typography --group-by size
```

### Diff 및 Patch

두 프레임 간의 패치를 생성·적용하고, 변경된 픽셀을 시각적으로 강조한다.

### Lint (실험)

17개 규칙으로 디자인 시스템 일관성, 접근성, 모범 사례를 검증한다.

| 범주          | 규칙 예시                                    |
| ------------- | -------------------------------------------- |
| 디자인 토큰   | 하드코딩된 색상 금지, 일관된 간격·반지름     |
| 레이아웃      | Auto Layout 선호, 픽셀 완벽성                |
| 타이포그래피  | 텍스트 스타일 필수, 최소 텍스트 크기         |
| 접근성        | 색상 대비, 터치 목표 크기                    |
| 구조          | 기본 이름 제거, 숨겨진 레이어 금지           |
| 컴포넌트      | 분리된 인스턴스 금지                         |

## MCP 서버 및 AI 에이전트 지원

### MCP 서버

90개 이상의 도구를 MCP 프로토콜로 노출한다.

```bash
figma-use mcp serve
```

### SKILL.md

Claude Code와 Cursor를 위한 `SKILL.md` 파일이 저장소에 포함되어 있다.

### 주석 기반 워크플로 (실험)

AI 에이전트가 Figma 주석을 감시하고 응답하는 워크플로를 지원한다.

## 데몬 모드

데몬을 띄우면 순차 명령 실행이 약 25% 빨라진다.
Figma 126 이상에서는 Pipe 전송 모드로 관리자 권한 없이 실행할 수 있다.

```bash
figma-use daemon start
figma-use daemon start --pipe  # Figma 126+
```

## 분석

### CDP 직접 통신의 의미

공식 Figma Plugin API는 Figma 앱 내부에서만 동작하고, REST API는 파일 읽기 중심
이다.
`figma-use`는 Chrome DevTools Protocol로 Figma 데스크탑 앱의 렌더링 컨텍스트에
직접 접근한다.
이 접근 방식은 플러그인 샌드박스를 우회해 더 넓은 권한을 가지지만, Figma 앱을
로컬에서 디버깅 포트를 열어 실행해야 한다는 전제가 붙는다.

### 명령형과 선언형의 공존

CLI 플래그 방식(명령형)과 JSX 렌더링(선언형)을 모두 지원하는 설계는 두 가지
사용자를 동시에 겨냥한다.
셸 스크립트에서 Figma를 조작하는 자동화 파이프라인에는 명령형이 적합하고,
AI 에이전트가 구조화된 UI를 생성할 때는 선언형이 더 자연스럽다.
JSX라는 익숙한 문법을 Figma 렌더링 대상으로 삼은 점은 프론트엔드 개발자의
진입 장벽을 낮추는 선택이다.

### MCP + SKILL.md의 이중 전략

90개 이상의 MCP 도구와 별도의 `SKILL.md`를 함께 제공하는 것은 두 종류의 AI 에이전트
통합을 커버하는 이중 전략이다.
MCP는 프로토콜 수준의 통합(Claude, Cursor 등 MCP 클라이언트)이고, `SKILL.md`는
컨텍스트 주입 방식의 통합(Claude Code, Cursor의 규칙 파일)이다.
공식 Figma MCP 서버와 병렬로 독립 MCP 서버를 제공한다는 점에서 생태계 내 경쟁
포지셔닝도 읽힌다.

## 비평

### 강점

CDP를 활용해 플러그인 없이 Figma를 제어하는 아이디어가 독창적이다.
Iconify 통합으로 150,000개 아이콘을 이름 하나로 삽입하는 경험은 실용성이 높다.
Diff/Patch, Lint, XPath 쿼리처럼 개발자 워크플로에 익숙한 패러다임을 Figma에
이식한 점이 인상적이다.

### 약점 및 한계

CDP 통신은 Figma 데스크탑 앱이 로컬에 설치되어 있고 디버깅 포트를 열어 실행
중이어야 한다는 강한 전제 조건이 있다.
CI/CD 환경이나 서버 사이드 자동화에는 적합하지 않다.
Figma 앱 업데이트가 CDP 인터페이스를 변경하면 도구 전체가 동작하지 않을 수 있는
취약성이 있다.

### 관점의 공백

Figma 공식 MCP 서버와 `figma-use` MCP 서버 간의 기능 차이와 공존 시나리오가
명확하지 않다.
Lint 규칙과 Diff 기능이 실험(experimental) 단계인 것들이 많아, 프로덕션 디자인
워크플로에 얼마나 신뢰할 수 있는지 판단하기 어렵다.
팀 환경에서 여러 사람이 동시에 같은 Figma 파일을 CDP로 조작할 때의 충돌 처리
방식이 언급되지 않는다.

## 인사이트

### “플러그인 없는 Figma 제어”가 열어주는 자동화의 새 지평

공식 Figma Plugin API는 플러그인 샌드박스 내에서만 실행된다.
이 구조는 Figma가 생태계를 통제하고 보안을 유지하는 메커니즘이지만, 동시에 자동화의
범위를 제한한다.
`figma-use`는 CDP라는 우회로를 통해 이 제약을 해소하고, 터미널과 CI 파이프라인에서
Figma를 직접 다룰 수 있는 가능성을 열었다.

이 접근법은 Selenium이 브라우저를 웹 드라이버로 제어하기 시작했을 때와 유사한
패러다임 전환이다.
웹 브라우저도 처음에는 사람만이 조작하는 도구였지만, 프로그래밍 가능한 인터페이스가
생기자 자동화 테스트, 스크래핑, 봇 등 새로운 사용 사례가 폭발적으로 등장했다.
Figma의 CDP 열린 포트는 그 시작점이 될 수 있다.
단, Figma가 공식적으로 CDP 접근을 지원하지 않으므로 언제든 차단될 수 있다는
불안정성은 이 패러다임의 구조적 약점이다.

### JSX as 디자인 언어 — 두 세계의 합류

`figma-use`의 선언형 JSX 렌더링은 흥미로운 질문을 제기한다: 코드로 UI를 선언하고
Figma에 렌더링하는 것이 디자인 작업인가, 아니면 개발 작업인가?
이 질문 자체가 무의미해지는 방향으로 도구 생태계가 이동하고 있음을 보여준다.
JSX는 React 개발자에게 익숙한 언어이고, Figma는 디자이너의 언어다.
`figma-use`는 그 사이에 번역 계층을 만든다.

이 방향은 Airbnb의 React Sketch.app(2017)이 처음 시도한 것과 같은 궤도다.
당시 코드로 Sketch 파일을 생성하는 시도는 생태계가 준비되지 않아 광범위하게 채택되지
못했다.
그러나 AI 에이전트가 JSX를 생성하고 Figma에 직접 렌더링할 수 있게 된 지금, 이 개념의
실용성은 당시와 크게 달라졌다.
AI가 설계를 코드로 표현하고 즉시 Figma에서 확인하는 워크플로는 디자인 검토 속도를
근본적으로 바꿀 수 있다.

### 독립 MCP 서버가 공식 통합과 공존하는 방식

`figma-use`는 Figma의 공식 MCP 서버와 나란히 독립 MCP 서버를 제공한다.
이는 커뮤니티가 SaaS 공급업체의 공식 통합보다 더 빠르게 기능을 추가하는 전형적인
패턴이다.
공식 MCP 서버가 안정성과 공식 지원을 제공하는 반면, `figma-use`는 Lint, Diff,
XPath 쿼리, 주석 기반 워크플로 같은 실험적 기능을 더 빠르게 제공한다.

이 공존은 지속 가능한가? 역사는 두 가지 결말을 보여준다.
하나는 공식 도구가 커뮤니티 도구의 인기 기능을 흡수하며 독립 프로젝트가 소멸하는
경로다.
다른 하나는 독립 도구가 충분한 사용자 기반을 확보해 공식 통합과 다른 포지션으로
안착하는 경로다.
`figma-use`가 CDP에 의존하는 한 Figma의 정책 변경에 취약하지만, 그 취약성이
오히려 Figma가 이 도구를 공식화하거나 흡수하는 동기가 될 수도 있다.
