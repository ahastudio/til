# Open Design

<https://github.com/nexu-io/open-design>

## 소개

Open Design은 Claude Design의 로컬 퍼스트 오픈소스 대체제다. 독자적인 AI
에이전트를 내장하는 대신, 사용자의 시스템 PATH에 설치된 16종 코딩 에이전트
CLI를 자동 감지해 디자인 엔진으로 활용한다. Claude Code, Codex, Devin, Cursor
Agent, Gemini CLI 등이 지원된다.

31개 내장 스킬과 72개 큐레이션 디자인 시스템을 탑재했으며, Apache 2.0
라이선스로 공개되었다.

## 주요 기능

### 에이전트 자동 감지

데몬이 PATH를 스캔해 호환 CLI 도구를 찾는다. “CLI가 없어도 OpenAI 호환 BYOK
프록시로 동일한 루프를 실행할 수 있다”고 명시한다.

### 31개 내장 스킬

두 가지 모드로 분류된다.

- **Prototype Mode** (27개): 웹 페이지, 모바일 앱, 대시보드 등 인터랙티브
  프로토타입
- **Deck Mode** (4개): 프레젠테이션 슬라이드

각 스킬은 Claude Code 컨벤션을 따르는 `SKILL.md` 프론트매터로 정의된 폴더
구조다.

### 72개 디자인 시스템

Linear, Stripe, Vercel, Notion, Apple, Tesla 등 브랜드급 디자인 시스템을
9개 섹션(색상, 타이포그래피, 간격, 레이아웃, 컴포넌트, 모션, 보이스, 브랜드
가이드라인, 안티패턴)으로 정리한 `DESIGN.md` 파일 형태로 제공한다.

### Interactive Discovery Form

첫 번째 턴에서 강제 실행되는 인터랙티브 질문 폼으로, 서피스 유형, 대상,
톤, 브랜드 컨텍스트, 규모를 확정한다. “AI 생성 결과물의 임의성”을 방지하기
위한 Anti-AI-slop 메커니즘이다.

### 미디어 생성 통합

HTML 아티팩트를 넘어 이미지(gpt-image-2), 비디오(Seedance 2.0,
HyperFrames HTML→MP4), 오디오 생성을 동일한 채팅 인터페이스에서 지원한다.
93개 템플릿을 제공한다.

## 아키텍처

스택이 세 레이어로 명확히 분리된다.

- **Frontend**: Next.js 16 App Router + React 18 (Vercel 배포 가능)
- **Daemon**: Node 24 + Express + SQLite, CLI 에이전트를 자식 프로세스로 실행
- **Agent Transport**: 각 CLI 출력 형식(JSON 이벤트 스트림, JSON-RPC, stdout)
  별 어댑터

데몬이 로컬에서 실행되므로 에이전트는 프로젝트 폴더에 대한 실제 `Read`,
`Write`, `Bash`, `WebFetch` 권한을 갖는다. 데이터는 `.od/app.sqlite`에 저장되고
아티팩트는 디스크에 남는다.

## 사용법

```bash
# 데스크톱 앱 (권장, 별도 설치 불필요)
# open-design.ai 에서 다운로드

# 소스 빌드
git clone https://github.com/nexu-io/open-design.git
cd open-design
corepack enable
pnpm install
pnpm tools-dev run web

# Docker
cd deploy && docker compose up -d
# http://localhost:7456 접속
```

Claude Design ZIP 임포트: 기존 Claude Design 내보내기 파일을 드래그 앤 드롭하면
로컬 에이전트가 이어서 편집할 수 있는 프로젝트로 변환된다.

## 분석

### “BYOA(Bring Your Own Agent)” 모델의 의미

Open Design의 핵심 차별점은 AI 엔진을 번들하지 않는다는 점이다. 사용자가
이미 사용하는 CLI 에이전트를 그대로 활용하게 함으로써, 라이선스 비용과 벤더
종속을 동시에 회피한다. Claude Code를 사용하는 개발자는 Claude Code를, Gemini
CLI를 선호하는 개발자는 Gemini CLI를 연결하면 된다.

이 접근은 Claude Design과 직접 경쟁하면서도, Claude Code 사용자에게는 오히려
Claude Design의 기능을 로컬에서 재현하는 도구가 된다.

### 디자인 시스템의 Markdown화

72개 디자인 시스템을 9개 섹션 `DESIGN.md` 파일로 표현한 것은 흥미로운
선택이다. Figma 컴포넌트나 Storybook 같은 기존 디자인 도구 대신 텍스트
문서로 디자인 시스템을 정의함으로써, LLM이 맥락으로 소비하기 적합한 형태를
택했다. 에이전트가 “Linear의 디자인 언어”를 이해하는 방식이 사람이 스타일
가이드를 읽는 방식과 동일해진다.

### Anti-AI-slop 설계

첫 턴에서 인터랙티브 폼을 강제 실행해 맥락을 확정하는 메커니즘은 LLM 생성
UI의 고질적 문제를 직접 겨냥한다. 맥락 없이 생성된 임의적 결과물(“AI slop”)을
방지하기 위해 명시적 제약을 생성 전에 수집하는 구조다.

## 비평

### 긍정적 측면

Claude Design 오픈소스화를 기다리는 대신, Claude Code 컨벤션을 그대로 채용해
기존 Claude Code 사용자에게 자연스러운 경험을 제공한다. BYOA 모델은 벤더
종속 없이 AI 디자인 도구를 사용하고 싶은 개발자에게 실질적인 대안이다.

### 한계

“72개 디자인 시스템”의 품질은 큐레이션 수준에 따라 크게 달라진다. Figma
Variables나 실제 컴포넌트 라이브러리와의 동기화 없이 Markdown 문서만으로
최신 디자인 시스템을 유지하는 것은 운영 부담이 크다. 실제 브랜드 가이드라인이
자주 변경되는 대형 프로젝트에서는 이 접근의 한계가 드러날 수 있다.

또한 16종 CLI 에이전트 각각에 대한 어댑터를 유지보수해야 한다는 점에서,
에이전트 생태계가 빠르게 변하는 현재 상황에서 커뮤니티 기여 없이는 유지가
어렵다.

## 인사이트

### 로컬 퍼스트 AI 도구의 생태계 포지셔닝

Open Design은 “Claude Design의 대체제”라고 스스로를 정의하지만, 더 정확하게는
“에이전트 CLI 위에 올라타는 UI 레이어”다. 이 포지셔닝은 향후 AI 도구 시장의
중요한 패턴을 예고한다. LLM 능력이 상향 평준화될수록, 경쟁은 인터페이스,
워크플로우 통합, 도메인 특화 컨텍스트로 이동한다. Open Design은 이 중 두
번째와 세 번째를 공략하는 셈이다.

오픈소스 전략은 Claude Code, Codex, Gemini CLI 등 어느 에이전트가 시장에서
우위를 점하더라도 생존할 수 있게 한다. 특정 AI 제공업체에 배팅하지 않는
“에이전트 불가지론적” 설계는 빠르게 변하는 시장에서 합리적 선택이다.

### 디자인 도구의 Markdown 시대

전통적인 디자인 도구(Figma, Sketch)는 독자적인 파일 형식으로 디자인 자산을
소유한다. Open Design이 디자인 시스템을 Markdown으로 표현한 것은 이 패러다임에
대한 도전이다. Git으로 버전 관리하고, 텍스트 에디터로 편집하며, LLM이 직접
소비하는 디자인 시스템이 실용적이라면, Figma가 독점해온 “디자인의 진실 원천”
지위가 흔들릴 수 있다.

물론 현재는 복잡한 인터랙션 디자인이나 실제 컴포넌트 구현에서 Figma를
대체하기 어렵다. 하지만 LLM이 시각적 결과물을 직접 생성하는 능력이 향상될수록,
“디자인 파일”과 “코드”의 경계는 더욱 흐려질 것이다.

### 커뮤니티 주도 디자인 시스템 큐레이션의 가능성

72개 디자인 시스템을 단일 팀이 유지하는 것은 장기적으로 지속 가능하지 않다.
그러나 이를 커뮤니티가 기여하는 구조로 발전시키면 다른 그림이 그려진다.
npm처럼 누구나 디자인 시스템 패키지를 게시하고, Open Design이 이를 설치하는
에코시스템이 형성된다면, 이 프로젝트는 단순한 도구를 넘어 AI 시대의 디자인
시스템 표준화 플랫폼이 될 수 있다.
