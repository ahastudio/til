# HyperFrames: HTML을 쓰면 비디오로 렌더링되는, 에이전트를 위한 오픈소스 프레임워크

<https://github.com/heygen-com/hyperframes>

Show HN: [Show HN: HyperFrames – Render Video from HTML via Chrome's BeginFrame API](https://news.ycombinator.com/item?id=47797513)

HN 토론: <https://news.ycombinator.com/item?id=47994268> (2점, 1개 댓글)

## 소개

HyperFrames는 HeyGen이 오픈소스로 공개한 HTML 기반 비디오 렌더링 프레임워크다.
슬로건은 “Write HTML. Render video. Built for agents.”로,
HTML 파일을 그대로 작성하면 MP4 비디오로 렌더링되는 구조다.

빌드 단계가 없고, 브라우저에서 즉시 미리보기가 가능하며,
같은 입력에 대해 항상 동일한 출력을 보장하는 결정론적 렌더링을
핵심 특징으로 내세운다.

저장소는 2026년 3월 10일에 만들어졌다.
2026년 11월 10일에 GitHub API로 읽은 값은 스타 81,868개, 포크 7,561개,
열린 이슈 235개이며 최신 릴리스는 같은 날 나온 v0.9.28이다.
라이선스는 Apache 2.0이고 주 언어는 TypeScript다.

### 사용 방식

README는 세 가지 사용 방식을 든다.
CLI로 로컬에서 쓰고, 코딩 에이전트에 스킬을 설치해 쓰고,
호스팅된 저작 도구 뒤의 렌더링 핵심으로 쓴다.
데스크톱 앱 HyperFrames Studio가 macOS, Windows, Linux용으로 있고 무료이며,
Pro 플랜은 HeyGen의 비디오, 이미지, 음성, 음악 모델을 더한다고 한다.
요구 사항은 Node.js 22 이상과 FFmpeg이다.

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

패키지 구성은 다음과 같다.
README의 목록은 8개이고,
저장소의 `packages/` 디렉터리에는 `gcp-cloud-run`도 있다.

| 패키지                            | 역할                                                    |
| --------------------------------- | ------------------------------------------------------- |
| `hyperframes`                     | CLI (생성, 미리보기, 린트, 렌더링)                      |
| `@hyperframes/core`               | 타입, 파서, 생성기, 린터, 런타임, 프레임 어댑터         |
| `@hyperframes/engine`             | Puppeteer와 FFmpeg로 시크 가능한 페이지를 캡처          |
| `@hyperframes/producer`           | 캡처, 인코딩, 오디오 믹스를 잇는 전체 렌더링 파이프라인 |
| `@hyperframes/studio`             | 브라우저 기반 컴포지션 편집기                           |
| `@hyperframes/player`             | `<hyperframes-player>` 웹 컴포넌트                      |
| `@hyperframes/shader-transitions` | 컴포지션용 WebGL 셰이더 트랜지션                        |
| `@hyperframes/aws-lambda`         | 분산 렌더링을 위한 AWS Lambda SDK와 배포 구성           |

## 제품 구조

README는 HyperFrames를 렌더링 엔진과 그 둘레의 도구 모음으로 설명한다.
도구마다 상태를 적어 두었다.

| 구성 요소              | README가 적은 상태 | 하는 일                                                    |
| ---------------------- | ------------------ | ---------------------------------------------------------- |
| CLI                    | 사용 가능          | 로컬 비디오 프로젝트의 생성, 미리보기, 린트, 점검, 렌더링  |
| Core, Engine, Producer | 사용 가능          | 컴포지션 파싱, 헤드리스 Chrome 구동, 인코딩, 오디오 믹스   |
| 카탈로그               | 사용 가능          | 전환, 오버레이, 캡션, 차트, 지도, 효과의 재사용 블록       |
| 에이전트 스킬          | 사용 가능          | 일반 웹 문서가 놓치는 비디오 제작 패턴을 에이전트에 가르침 |
| Studio                 | 사용 가능, 발전 중 | 컴포지션을 미리 보고 편집하는 브라우저 화면                |
| AWS Lambda 렌더링      | 사용 가능          | 분산 렌더링 스택을 배포하고 노트북이나 CI에서 구동         |
| hyperframes.studio     | 사용 가능          | 미리보기, 반복, 공유, 렌더링을 하는 커뮤니티 놀이터        |
| frame.md               | 사용 가능          | 디자인 시스템을 카메라용으로 뒤집은 `DESIGN.md` 상위 집합  |

frame.md는 웹 맥락의 디자인 명세를 비디오 프레임에 맞게 다시 쓰는 변환층이라고
README가 설명한다.
에이전트가 크기를 짐작하거나 웹 장식에 기대지 않고 홍보 영상을 구성하게 하려는
것이다.

렌더링 경로는 저장소의 `docs/deploy/overview.mdx`가 정리한다.
CI나 작업 중에는 CLI, Node 애플리케이션에는 Producer, 프레임 캡처를 직접
제어하려면 Engine을 쓴다.
인프라를 직접 운영하지 않으려면 HyperFrames Cloud(`hyperframes cloud render`)를,
자신의 계정에서 분산 렌더링을 하려면 AWS Lambda나 Google Cloud Run을 쓴다.
문서는 가장 높은 수준에서 일을 끝내는 표면을 고르라고 권한다.

카탈로그는 `npx hyperframes add flash-through-white`처럼 블록을 편집 가능한
소스로 설치한다.
`/hyperframes-registry` 스킬 설명은 약 450개의 블록과 컴포넌트가 있다고 적는다.

ADOPTERS.md는 프로덕션 사용 조직으로 HeyGen(자사 비디오 제품의 컴포지션과
렌더링), tldraw(풀 리퀘스트 설명 영상 자동 생성)를 든다.
TanStack과 OptinMonster는 탐색 중이라고 적혀 있다.
이 목록은 조직이 직접 PR로 추가하는 자기 신고이며 이 문서는 사용 여부를 확인하지
않았다.

## 에이전트 통합

HyperFrames는 에이전트 우선(Agent-first) 설계를 표방한다.
CLI는 기본적으로 비인터랙티브(non-interactive)로 동작하며,
에이전트가 직접 호출할 수 있도록 설계됐다.

Claude Code에는 버전이 붙은 플러그인을 설치한다.

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

OpenCode처럼 플러그인이 없는 환경에는 `npx skills add heygen-com/hyperframes`를
쓰고, 어느 환경에서든 `npx hyperframes skills update`는 CLI 버전과 같은 릴리스
태그의 핵심 스킬을 설치한다.
README는 skills.sh 레지스트리가 `main`보다 몇 시간 늦을 수 있어서 후자를 권하는
이유라고 적는다.
Copilot, VS Code, Cursor, Gemini CLI용 안내는 저장소의 플러그인 가이드에 있다.

README는 스킬이 9개라고 한다.
핵심 여섯 개와 필요할 때 설치하는 세 개로 나뉜다.

| 스킬                       | 구분    | 내용                                                             |
| -------------------------- | ------- | ---------------------------------------------------------------- |
| `/hyperframes`             | 핵심    | 렌더링 규약과 작업 순환. 비디오 관련 요청에서 먼저 읽는다        |
| `/hyperframes-cli`         | 핵심    | 작업별 CLI 사용법과 빌드, 렌더링 실패 복구                       |
| `/hyperframes-registry`    | 핵심    | 카탈로그 블록과 컴포넌트를 편집 가능한 소스로 설치               |
| `/media-use`               | 핵심    | 음악, 효과음, 이미지, 음성, 아바타, 자막, 색 보정 등 미디어 확보 |
| `/reverse-any-video`       | 핵심    | 기존 영상을 편집 가능한 프로젝트로 재구성. HyperFrames Pro       |
| `/style-sampling`          | 핵심    | 다섯 가지 검증된 스타일로 새 에피소드 제작. HyperFrames Pro      |
| `/figma`                   | 필요 시 | Figma 자산, 브랜드 토큰, 스토리보드를 영상으로 가져옴            |
| `/slideshow`               | 필요 시 | 렌더링된 MP4가 아니라 탐색 가능한 발표 자료를 출력               |
| `/remotion-to-hyperframes` | 필요 시 | Remotion 등 기존 영상 코드를 프레임 단위로 검증하며 옮김         |

이 목록은 이 문서의 이전 판과 다르다.
이전 판이 적은 `website-to-hyperframes`와 `gsap` 스킬은 이 README의 목록에 없다.

## Remotion과의 비교

| 항목                       | HyperFrames                       | Remotion                                      |
| -------------------------- | --------------------------------- | --------------------------------------------- |
| 저작 방식                  | HTML, CSS, 시크 가능한 애니메이션 | React 컴포넌트                                |
| 빌드 단계                  | 없음. `index.html`이 그대로 재생  | 번들러 필요                                   |
| 에이전트 전달              | 일반 HTML 파일                    | JSX와 React 프로젝트                          |
| 라이브러리 시계 애니메이션 | 어댑터로 시크 가능, 프레임 정확   | 실제 시간 기준 패턴은 주의가 필요             |
| 분산 렌더링                | 로컬과 AWS Lambda 렌더링 경로     | Remotion Lambda, 성숙한 클라우드 렌더러       |
| 라이선스                   | Apache 2.0                        | 소스 공개(source-available) Remotion 라이선스 |

README는 두 도구가 모두 헤드리스 Chrome과 FFmpeg로 비디오를 렌더링하고,
차이는 저작 모델이라고 정리한다.
저장소의 CREDITS.md는 Remotion이 헤드리스 브라우저와 FFmpeg `image2pipe`
파이프라인을 개척했고, 병렬 프레임 캡처의 순서 장벽 같은 설계 아이디어를
Remotion을 연구해 얻었다고 밝히면서, 코드는 독립적으로 구현했고 Remotion과 제휴
관계가 없다고 적는다.

HyperFrames는 Apache 2.0이고 렌더당 요금이나 상업적 사용 문턱이 없다고 README가
말한다.

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

### 분산 렌더링은 있지만 Remotion Lambda와의 성숙도 비교는 근거가 없다

이 문서의 이전 판은 HyperFrames가 단일 머신 렌더링만 지원한다고 썼다.
그것은 오독이었다.
README의 제품 구조 표에는 AWS Lambda 렌더링이 사용 가능으로 올라 있고,
저장소에는 `@hyperframes/aws-lambda`와 `gcp-cloud-run` 패키지, 두 경로의 배포
문서가 있다.
남는 의문은 성숙도다.
README는 비교표에서 Remotion의 클라우드 렌더러를 성숙하다고 적는 반면 자사는
로컬과 Lambda 경로라고만 쓴다.
이 문서는 Lambda 경로를 실행해 보지 못했고, 대규모 렌더링에서 두 도구의 안정성과
비용을 비교한 근거도 찾지 못했다.
대량 렌더링이 목적이라면 도입 전에 직접 부하를 걸어 봐야 하는 항목이다.

### 오픈소스 핵심과 HeyGen 유료 표면의 경계가 스킬 안에 들어와 있다

HeyGen은 AI 비디오 생성 서비스 회사이고, 이 저장소는 HeyGen의 프로덕션에서
쓰인다고 README와 ADOPTERS.md가 밝힌다.
이전 판은 HeyGen과의 관계가 불분명하다고 썼지만 README는 연결을 숨기지 않는다.
Studio 앱은 무료이고 Pro 플랜이 HeyGen의 모델을 더하며,
`/media-use`는 HeyGen 또는 무료 로컬 도구로 미디어를 얻는다고 쓴다.
핵심 스킬 여섯 개 가운데 `/reverse-any-video`와 `/style-sampling`은 설명에
HyperFrames Pro가 붙어 있다.

따라서 문제는 연결 여부가 아니라 경계다.
설치 명령 하나로 받는 핵심 스킬 안에 무료 기능과 Pro 기능이 섞여 있고,
Apache 2.0 라이선스는 저장소의 코드에 해당한다.
어느 기능이 무료로 끝까지 되고
어느 기능이 Pro 플랜이나 HeyGen 모델을 요구하는지는
스킬을 읽고 써 봐야 알 수 있다.
이 문서는 Pro 기능을 사용해 보지 못했다.

저장소의 CREDITS.md는 또 하나를 적는다.
카탈로그의 일부 블록이 쓰는 GSAP 3.14.2가 GSAP Standard License 아래에 있고
OSI 오픈소스 라이선스가 아니라는 것이다.
README의 예제도 GSAP을 CDN에서 불러온다.
그러므로 렌더당 요금이 없다는 README의 문장은 HyperFrames 코드에 대한 것이고,
GSAP을 쓰는 영상에는 GSAP 쪽 조건이 따로 붙는다.
이 문서는 그 조건의 내용은 확인하지 않았다.

### 복잡한 편집 영역은 스킬로 덮었다고 주장하지만 검증은 없다

이전 판은 색 보정, 멀티캠 편집, 고급 오디오 믹싱의 지원 수준이 불명확하다고
썼다.
README는 이제 `/media-use`가 색 보정과 룩, 배치한 오디오의 믹스를 다루고
`/reverse-any-video`가 기존 영상을 원본과 프레임 단위로 대조하며 재구성한다고
설명한다.
이것은 제작자의 주장이고 이 문서는 실제 결과를 보지 못했다.
HTML과 CSS로 표현되지 않는 작업을 스킬이 어디까지 대신하는지, 그 결과가
전문 편집 도구와 어떻게 다른지는 여전히 사용 사례가 쌓여야 판단된다.
HN에서 써 봤느냐는 질문에 답한 uwemaurer는 Bluesky 프로필 통계 영상을 만들었다고
적고 결과 페이지를 링크했다.[^uwemaurer]
이것은 단순한 데이터 영상의 사례이고 위의 복잡한 편집 영역을 검증하지는 않는다.

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

---

[^uwemaurer]: <https://news.ycombinator.com/item?id=48047356>
