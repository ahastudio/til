# HyperFrames

<https://github.com/heygen-com/hyperframes>

## 소개

HyperFrames는 HeyGen이 오픈소스로 공개한 HTML 기반 비디오 렌더링 프레임워크다.
슬로건은 “Write HTML. Render video. Built for agents.”로,
HTML 파일을 그대로 작성하면 MP4 비디오로 렌더링되는 구조다.

빌드 단계가 없고, 브라우저에서 즉시 미리보기가 가능하며,
같은 입력에 대해 항상 동일한 출력을 보장하는 결정론적 렌더링을
핵심 특징으로 내세운다.

2026년 3월 공개 이후 GitHub 스타 약 12,000개, 포크 1,000개 이상을 기록하며
빠르게 주목받고 있다.

## 아키텍처

컴포지션(Composition)은 `data-` 어트리뷰트를 사용하는 HTML 파일이다.
`data-start`, `data-duration`, `data-track-index` 등으로
클립의 타임라인 위치와 레이어를 지정한다.

```html
<div id="stage"
  data-composition-id="my-video"
  data-start="0"
  data-width="1920"
  data-height="1080">
  <video
    id="clip-1"
    data-start="0"
    data-duration="5"
    data-track-index="0"
    src="intro.mp4"
    muted playsinline
  ></video>
  <img
    id="overlay"
    class="clip"
    data-start="2"
    data-duration="3"
    data-track-index="1"
    src="logo.png"
  />
</div>
```

렌더링 파이프라인은 Puppeteer로 헤드리스 Chrome을 구동하고,
프레임을 캡처한 뒤 FFmpeg로 MP4로 인코딩하는 구조다.
Remotion이 개척한 Chrome 기동 플래그, image2pipe → FFmpeg 스트리밍,
프레임 버퍼링 패턴을 계승했다.

패키지 구성은 다음과 같다:

| 패키지                        | 역할                                   |
| ----------------------------- | -------------------------------------- |
| `hyperframes`                 | CLI (init, preview, render, lint)      |
| `@hyperframes/core`           | 타입, 파서, 린터, 런타임, 프레임 어댑터 |
| `@hyperframes/engine`         | Puppeteer + FFmpeg 캡처 엔진           |
| `@hyperframes/producer`       | 전체 렌더링 파이프라인                 |
| `@hyperframes/studio`         | 브라우저 기반 컴포지션 편집기          |
| `@hyperframes/player`         | `<hyperframes-player>` 웹 컴포넌트     |
| `@hyperframes/shader-transitions` | WebGL 셰이더 트랜지션              |

## 에이전트 통합

HyperFrames는 에이전트 우선(Agent-first) 설계를 표방한다.
CLI는 기본적으로 비인터랙티브(non-interactive)로 동작하며,
에이전트가 직접 호출할 수 있도록 설계됐다.

Skills 시스템을 통해 Claude Code, Cursor, Gemini CLI, Codex 등
주요 AI 에이전트에 프레임워크 지식을 주입할 수 있다:

```bash
npx skills add heygen-com/hyperframes
```

설치되는 스킬 목록은 다음과 같다:

| 스킬                       | 내용                                          |
| -------------------------- | --------------------------------------------- |
| `hyperframes`              | 컴포지션 작성, 캡션, TTS, 오디오 리액티브 애니메이션 |
| `hyperframes-cli`          | CLI 명령어 레퍼런스                           |
| `hyperframes-registry`     | `hyperframes add`로 블록/컴포넌트 설치        |
| `website-to-hyperframes`   | URL을 비디오로 변환하는 파이프라인             |
| `gsap`                     | GSAP 애니메이션 API, 타임라인, 이징           |

## Remotion과의 비교

| 항목           | HyperFrames              | Remotion                        |
| -------------- | ------------------------ | ------------------------------- |
| 저작 방식      | HTML + CSS + GSAP        | React 컴포넌트 (TSX)            |
| 빌드 단계      | 없음                     | 필요 (번들러)                   |
| 라이선스       | Apache 2.0 (오픈소스)    | 커스텀 라이선스 (소스 공개)     |
| 분산 렌더링    | 단일 머신                | Lambda, 프로덕션 레디           |
| GSAP 애니메이션 | 시크 가능, 프레임 정확  | 렌더링 중 wall-clock 재생       |

HyperFrames는 Apache 2.0 하에 완전히 오픈소스다.
반면 Remotion은 소스 코드는 공개되어 있으나
일정 규모 이상의 기업에서는 유료 라이선스가 필요한 소스 공개(source-available) 모델이다.

## 분석

### HTML이 비디오 저작 언어가 되는 구조적 전환

HyperFrames의 핵심 아이디어는 HTML을 비디오 타임라인 명세 언어로 재해석하는 것이다.
`data-start`, `data-duration`, `data-track-index` 같은 어트리뷰트가
NLE(Non-Linear Editor)의 타임라인 트랙 개념을 HTML 어트리뷰트로 매핑한다.

빌드 단계 없이 `index.html`이 그대로 프리뷰로 재생된다는 점은
웹 개발자의 기존 워크플로우와 완전히 정렬된다.
새로운 DSL이나 컴포넌트 모델을 학습할 필요 없이
이미 알고 있는 HTML/CSS 문법으로 비디오를 작성할 수 있다.

### 에이전트가 HTML을 “이미 알고 있다”는 전제

README는 “AI agents already speak HTML”을 핵심 근거로 내세운다.
이것은 단순한 마케팅 언어가 아니라 실질적인 설계 선택의 근거다.

LLM은 수십억 개의 HTML 문서로 사전 학습되어 있다.
반면 Remotion의 TSX 기반 컴포지션이나 Adobe After Effects의 독점 형식은
에이전트 입장에서 추가적인 학습이 필요한 도메인 특화 언어다.

에이전트가 HTML을 생성하는 비용이 TSX를 생성하는 비용보다 구조적으로 낮다면,
에이전트 중심 워크플로우에서 HyperFrames가 유리한 위치를 점한다.

### Frame Adapter 패턴과 애니메이션 런타임 다양성

“Bring Your Own Animation Runtime” 철학을 구현하는 Frame Adapter 패턴이 주목할 만하다.
GSAP, Lottie, CSS 애니메이션, Three.js 등 어떤 런타임도 어댑터를 통해 통합할 수 있다.

이것은 애니메이션 생태계가 이미 성숙해 있다는 사실을 인정하고,
바퀴를 재발명하는 대신 기존 도구를 렌더링 파이프라인에 연결하는 현실적 선택이다.
특히 GSAP 애니메이션을 시크 가능한(seekable) 방식으로 프레임 정확하게 재생하는 것은
wall-clock 기반으로 재생하는 Remotion 대비 명확한 기술적 우위다.

## 비평

### 강점: 에이전트 시대의 설계 철학이 일관적이다

CLI의 비인터랙티브 기본값, Skills 시스템을 통한 에이전트 지식 주입,
다양한 에이전트 플랫폼(Claude Code, Cursor, Codex)에 대한 플러그인 지원까지
에이전트 우선 설계가 단순한 슬로건에 그치지 않고 구현 전체에 관통한다.

Apache 2.0 라이선스를 택한 것도 전략적으로 일관된다.
Remotion을 대체하거나 경쟁하려는 포지셔닝에서,
라이선스 리스크 없이 상업적으로 자유롭게 사용할 수 있다는 점은
엔터프라이즈 도입 장벽을 낮추는 실질적 차별점이다.

### 약점: 분산 렌더링 미지원이 확장성 한계를 만든다

단일 머신 렌더링만 지원한다는 점은 현재 시점의 명확한 한계다.
Remotion은 AWS Lambda를 활용한 분산 렌더링을 프로덕션 레디 수준으로 지원한다.
대규모 비디오 생성 파이프라인을 구축하려는 팀 입장에서는
이 차이가 도입 결정에 직접적 영향을 줄 수 있다.

### 약점: HeyGen의 이해관계 투명성

HeyGen은 AI 비디오 생성 서비스 회사다.
HyperFrames가 완전히 독립적인 오픈소스 프로젝트인지,
HeyGen의 서비스 생태계와 어떻게 연결될지는 명확하지 않다.
Apache 2.0이지만 프로젝트의 장기적 방향이 HeyGen의 사업 전략에
종속될 가능성은 커뮤니티 입장에서 모니터링이 필요한 리스크다.

### 약점: 복잡한 비디오 편집 시나리오에 대한 검증 부족

HTML/CSS로 표현할 수 없는 복잡한 비디오 편집 시나리오,
예를 들어 색 보정(color grading), 멀티캠 편집,
고급 오디오 믹싱 등에 대한 지원 수준이 불명확하다.
“Write HTML, Render video”라는 슬로건이 얼마나 넓은 범위를 커버하는지는
프로덕션 사용 사례가 축적되어야 판단할 수 있다.

## 인사이트

### AI 에이전트가 1인 비디오 프로덕션을 재정의한다

HyperFrames가 드러내는 더 큰 그림은 비디오 제작 진입 장벽의 붕괴다.
전통적으로 비디오 제작은 스크립트 작성, 촬영, 편집, 렌더링이라는
분리된 전문 도메인의 협업이 필요했다.

에이전트가 HTML을 생성하고, HyperFrames가 그것을 비디오로 렌더링하는 흐름은
“설명 → 비디오”라는 단일 인터페이스로 이 파이프라인 전체를 추상화한다.
“Using /hyperframes, create a 10-second product intro with a fade-in title”이라는
한 문장이 완성된 비디오가 되는 것이다.

이것은 단순한 생산성 향상이 아니라 비디오 생산의 주체 자체가 바뀌는 변화다.
Adobe Premiere나 DaVinci Resolve를 쓸 수 없는 개인이나 소규모 팀이
에이전트를 통해 정교한 비디오 콘텐츠를 제작할 수 있게 된다.
진입 장벽이 낮아지면 비디오 콘텐츠의 총량이 증가하고,
이는 콘텐츠 생태계의 구조적 변화로 이어진다.

### HTML은 이미 가장 검증된 “범용 레이아웃 언어”다

HyperFrames의 가장 날카로운 통찰은 새로운 DSL을 만들지 않은 것이다.
수십 년간 수십억 개의 문서가 HTML로 작성되어 있고,
수백만 명의 개발자가 HTML을 구사하며,
모든 LLM이 HTML을 사전 학습 데이터로 학습했다.

반면 비디오 저작 도구들은 저마다 다른 독점적 추상화를 만들어왔다.
After Effects의 키프레임, Remotion의 TSX, Lottie의 JSON 형식 등
서로 호환되지 않는 언어들이 난립한다.

HTML을 비디오 컴포지션 언어로 선택한 것은 이 단편화 문제를 우회하는 영리한 선택이다.
에이전트가 HTML을 “이미 알고 있다”는 사실은 학습 비용과 오류율을 동시에 낮춘다.
이 선택이 옳다면, 앞으로 더 많은 미디어 도구들이
기존 웹 표준을 저작 언어로 채택하는 흐름을 만들 수 있다.

### Skills 시스템은 새로운 소프트웨어 배포 레이어다

HyperFrames가 `npx skills add heygen-com/hyperframes`로
에이전트에 지식을 주입하는 방식은 소프트웨어 배포의 새로운 패러다임을 시사한다.

전통적인 소프트웨어는 라이브러리나 CLI 도구로 배포된다.
에이전트 시대의 소프트웨어는 “에이전트가 올바르게 사용하는 방법에 대한 지식”도
함께 배포되어야 한다.
프레임워크를 설치하는 것과, 그 프레임워크를 에이전트가 올바르게 사용하도록
가르치는 것은 이제 같은 배포 행위의 두 측면이다.

Skills 시스템은 이 아이디어를 표준화하려는 시도다.
Claude Code의 슬래시 커맨드, Cursor 플러그인, Codex 플러그인으로
동시에 노출되는 구조는 에이전트 플랫폼 다변화 시대의 “패키지 매니저”가 어떤 모습이어야
하는지에 대한 하나의 답안을 제시한다.

이 방향이 확산된다면, 미래의 라이브러리는 API 문서와 함께
“에이전트 스킬”을 공식 배포물의 일부로 포함하게 될 것이다.
npm의 `README.md`처럼, skills 폴더가 라이브러리의 필수 구성요소가 되는 시대가
올 수 있다.
