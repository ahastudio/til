# OpenPencil: .fig 파일을 열고 AI와 스크립트로 다루는 오픈소스 디자인 에디터

<https://openpencil.dev>

<https://github.com/open-pencil/open-pencil>

HN 토론: <https://news.ycombinator.com/item?id=47215736> (17점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=27658>

## 소개

OpenPencil은 `.fig`(Figma)와 `.pen`(Pencil) 디자인 파일을 여는 오픈소스
디자인 에디터다.
README는 AI가 내장되어 있고, 헤드리스 Vue SDK를 곁들여 맞춤 에디터를 만드는 도구
모음으로도 쓸 수 있다고 소개한다.
상태는 활발히 개발 중이며, 지금도 쓸 수 있지만 기능이 바뀌면서 거친 부분이
있다고 밝힌다.

저장소는 2026년 2월 27일에 만들어졌고, GitHub API로 읽은 시점의 별은 9,357개,
포크는 979개, 주 언어는 TypeScript다.
라이선스는 MIT이며, 다만 OpenPencil Cloud는 Apache License 2.0이고 정확한 경로는
`REUSE.toml`에 있다.
저작권 표기는 Danila Poyarkov와 OpenPencil contributors다.

이름이 비슷한 `ZSeven-W/openpencil`은 다른 프로젝트다.
TIL의 `design/openpencil-zseven.md`가 그쪽을 다루므로 이 문서와 겹치지 않는다.

## 만든 이유

README의 「Why」는 Figma가 프로그래밍 방식 접근을 막는 닫힌 플랫폼이라고 쓴다.
Figma의 MCP 서버는 읽기 전용이고, Plugin API 밖의 자동화는 점 릴리스 때
깨진다고 한다.
디자인 파일은 해당 소프트웨어만 온전히 읽을 수 있는 독점 바이너리
형식이라는 점도 든다.
OpenPencil은 그 대안으로 오픈소스(MIT), 로컬 우선, `.fig` 네이티브 읽기,
모든 동작의 스크립트화를 내세운다.
제품 방향과 Figma 호환성의 빈틈은 로드맵 페이지에 있다고 한다.

## 주요 기능

README가 나열한 기능은 열세 가지다.
- 파일: `.fig`를 읽고 쓰며, 지원되는 `.pen` 문서를 열고, 앱 사이에서 노드를 복사해 붙인다.
- AI 채팅: 100개가 넘는 도구가 노드를 만들고 고친다. OpenRouter, Anthropic, OpenAI, Google AI, DeepSeek, Z.ai, MiniMax 또는 호환 엔드포인트의 키를 직접 넣는다.
- 프로그래밍: 헤드리스 CLI, XPath 질의, Figma Plugin API, `eval`로 쓰는 `openpencil` API, MCP 서버, 데스크톱 에이전트 연동(Claude Code, Codex, Gemini CLI, Pi).
- 검사와 변환: 이름·레이아웃·접근성 lint, 형식 변환, 색·타이포그래피·간격·클러스터 분석, 디자인 토큰 추출.
- 컴포넌트: 재사용 컴포넌트, 변형(variant)을 묶은 컴포넌트 세트, 로컬 에셋 인스턴스, 인스펙터에서 변형 전환.
- 동작하는 컨트롤: 컴포넌트에 Reka UI 동작(스위치, 슬라이더, 탭, 텍스트 필드 등)을 붙여 캔버스 위에서 실제 입력과 키보드로 미리 본다.
- 이미지 벡터화: Recraft나 fal.ai로 이미지 레이어를 편집 가능한 벡터로 바꾼다.
- 디자인에서 코드로: 선택 영역을 JSX나 Tailwind로 내보내고 토큰 출력을 만든다.
- Vue SDK: 에디터를 다른 앱에 넣거나 작업별 편집 화면을 만드는 헤드리스 컴포넌트와 컴포저블.
- 실시간 협업: 서버와 계정 없이 WebRTC 피어 투 피어 방으로 공유하며 커서, 접속 표시, 따라가기, 음성 통화가 있다.
- 선택형 Cloud: 팀이 직접 띄우는 서버나, 열리면 호스팅 서비스에 문서를 두고 초대로 공유한다.
- 자동 레이아웃: Yoga WASM으로 flex와 CSS Grid를 지원한다.
- 약 15MB 데스크톱 앱: Tauri v2로 macOS, Windows, Linux를 지원하고 브라우저 PWA로도 돈다.

## 설치

macOS에서는 `brew install --cask openpencil`로 깔고,
다른 플랫폼은 릴리스 페이지에서 받으며, 설치 없이 웹 앱도 쓸 수 있다.
요구 사항은 macOS 13 이상, Windows 10 이상, WebKitGTK 2.40 이상의 Linux이고,
웹 앱은 Chrome 111, Edge 111, Firefox 128, Safari 16.4 이상이다.

README는 공식 빌드가 하루에 한 번 익명 신호를 보내고,
사용 통계는 동의할 때만 공유한다고 적는다.
보내는 항목 전체와 끄는 방법은 개인정보 페이지에 있다고 한다.

## CLI

설치는 `npm install -g @open-pencil/cli` 또는 `bun add -g @open-pencil/cli`다.
모든 명령은 `--json`을 지원한다.

```bash
openpencil tree design.fig                    # 노드 트리
openpencil find design.pen --type TEXT        # 이름이나 타입으로 찾기
openpencil query design.fig "//FRAME[@width < 300]"   # XPath 질의
openpencil export design.fig -f tailwind-jsx  # Tailwind JSX로 내보내기
openpencil convert design.pen design.fig      # 문서 형식 변환
openpencil lint design.fig --preset strict    # 이름, 레이아웃, 접근성 검사
openpencil analyze colors design.fig          # 색 사용량 분석
```

내보내기 형식은 PNG, JPG, WEBP, SVG, PDF, PPTX, HTML, JSX,
Storybook 스토리, `.fig`다.
`openpencil import card.html --css card.css`는 HTML과 CSS를 편집 가능한
`.fig`로 바꾼다.

`eval`은 문서에 Figma Plugin API로 JavaScript를 실행하고 `-w`를 붙이면 결과를
파일에 쓴다.
파일 인자를 생략하면 실행 중인 앱에 열린 문서를 대상으로 하며, `documents list`,
`tool call get_selection`, `undo`, `settings set` 같은 명령이 있다.

## AI와 MCP

### 내장 채팅

Cmd+J(Windows와 Linux는 Ctrl+J)로 AI 도우미를 연다.
README는 백엔드도 계정도 없다고 적는다.
모든 공급자가 브라우저에서 되는 것은 아니고 모든 모델이 도구 호출을 제대로
스트리밍하지도 않는다고 인정하며, 측정 결과를 담은 호환성 페이지를 안내한다.

### 코딩 에이전트

데스크톱 앱에서 Claude Code, Codex, Gemini CLI,
Pi를 채팅 패널의 디자인 에이전트로 쓴다.
사용자 본인의 구독으로 돌고, 에디터의 MCP 서버를 통해 캔버스에 닿는다.
에이전트의 ACP 프로그램과 `@open-pencil/mcp`를 설치하고 설정의 안내 마법사를
돌리면 설치와 로그인, 세션 연결을 확인해 준다고 한다.
Pi는 `@open-pencil/harness`라는 동반 패키지로 돈다.

### MCP 서버와 에이전트 스킬

`npm install -g @open-pencil/mcp` 뒤 `claude mcp add --scope user open-pencil --
openpencil-mcp`로 등록한다.
스크립트와 CI용으로는 `openpencil-mcp-http`가 있고,
유닉스 소켓과 `http://127.0.0.1:7600/mcp`를 연다.
`OPENPENCIL_MCP_ROOT`로 파일 접근을 한 디렉터리로 제한하며 기본값은 현재
작업 디렉터리다.

`npx skills add open-pencil/open-pencil`로 에이전트 스킬도 설치한다.
문서 사이트는 `llms.txt`, `llms-full.txt`와 페이지별 Markdown도 낸다.

## 협업

공유 버튼으로 `app.openpencil.dev/rooms/<room-id>` 링크를 만들어 보내면 상대가
직접 WebRTC로 연결된다.
상대의 커서, 선택, 편집이 실시간으로 보이고,
아바타를 누르면 그 사람의 뷰포트를 따라가며,
헤드폰 아이콘으로 방의 음성 통화에 들어간다.

## 기술 스택

| 계층      | 기술                                            |
| --------- | ----------------------------------------------- |
| 렌더링    | Skia (CanvasKit WASM)                           |
| 레이아웃  | Yoga WASM (flex와 grid를 지원하는 포크)         |
| UI        | Vue 3, Reka UI, Tailwind CSS 4                  |
| 파일 형식 | Kiwi 바이너리, Zstd, ZIP                        |
| 협업      | Trystero (WebRTC P2P), Yjs (CRDT)               |
| 데스크톱  | Tauri v2                                        |
| AI와 MCP  | Vercel AI SDK (다중 공급자 BYOK), MCP SDK, Hono |

개발은 `bun install` 뒤 `bun run dev:portless`로 웹 에디터를,
`bun run tauri dev`로 데스크톱 앱을 띄운다.
데스크톱 빌드는 Rust와 Tauri v2 선행 조건이 필요하다.
README의 감사 문구에는 Anthropic이 오픈소스 프로그램으로 프로젝트를 지원하고,
CodeRabbit이 모든 풀 리퀘스트를 무료로 리뷰한다는 내용이 있다.

## 분석

### 형식을 여는 것으로 전환 비용을 낮춘다

이 프로젝트의 출발점은 새 디자인 도구가 아니라 기존 파일을 읽는 도구라는 점이다.
README는 `.fig`를 네이티브로 읽고 쓴다고 하고,
노드 복사와 붙여넣기까지 앱 사이에서 된다고 한다.
디자인 도구를 바꾸는 가장 큰 장벽이 자산의 이동이라면,
파일 호환이 곧 진입 전략이다.
이 문서의 해석으로는 `.pen` 지원과 `convert` 명령이 같은 방향의 보강이다.
독점 바이너리를 읽는 쪽의 부담은 호환성의 빈틈이라는 형태로 남으며,
이를 로드맵이 따로 다룬다고 README가 밝힌다.

### 모든 조작을 명령 하나로 호출 가능하게 만들었다

기능 목록의 공통점은 같은 조작이 GUI, CLI, MCP, `eval`,
SDK 어디서든 가능하다는 점이다.
README가 「Why」에서 말한 스크립트화가 이 구조로 구현된다.
CLI에서 `tool call`로 MCP 도구를 직접 부르고 `undo`로 자동화 변경을 되돌린다는
대목은 같은 도구 집합이 사람용 화면과 에이전트용 인터페이스 양쪽에서
쓰인다는 증거다.
이 문서의 해석으로는 이것이 AI-native라는 표현의 실질이다.
채팅 창이 있어서가 아니라 에이전트가 쓸 수 있는 조작면이 먼저 있기 때문이다.

### 로컬 우선은 선택형 서버와 피어 연결로 구현된다

협업은 서버 없이 WebRTC 방으로 되고, Cloud는 선택이다.
AI도 백엔드 없이 사용자가 가져온 키로 돈다.
서버를 전제하지 않는 구조라서 팀이 쓰는 서버, 호스팅 서비스,
피어 방이 모두 같은 문서 모델 위에 놓인다.
Yjs(CRDT)가 합의 장치 역할을 하는 구성이다.

### 같은 이름의 두 프로젝트는 같은 빈자리를 다른 방식으로 채운다

OpenPencil이라는 이름의 오픈소스 디자인 도구가 둘 있다.
이 문서의 `open-pencil/open-pencil`과, `design/openpencil-zseven.md`가 다루는
`ZSeven-W/openpencil`이다.
두 README에서 읽은 사실을 나란히 놓으면 다음과 같다.

| 항목          | open-pencil/open-pencil                  | ZSeven-W/openpencil                           |
| ------------- | ---------------------------------------- | --------------------------------------------- |
| 포지셔닝      | Figma 대체를 표방하는 디자인 에디터      | 에이전트용 AI 네이티브 벡터 디자인 도구       |
| 구현 언어     | TypeScript, Vue 3, Tauri v2              | Rust 워크스페이스, `winit`과 GPU Skia         |
| 렌더링        | Skia(CanvasKit WASM)                     | 데스크톱은 GPU Skia, 웹은 wasm과 CanvasKit    |
| 고유 파일     | 고유 형식 없이 `.fig`와 `.pen`을 연다    | 사람이 읽는 JSON인 `.op`, `.fig`는 가져오기   |
| AI 방식       | 내장 채팅(100+ 도구), 외부 코딩 에이전트 | 오케스트레이터가 나누는 동시 에이전트 팀      |
| 코드 내보내기 | JSX, Tailwind JSX, Storybook             | React, HTML, Vue, Svelte, Flutter, SwiftUI 등 |
| 협업          | WebRTC 방(Trystero, Yjs), 선택형 Cloud   | 인증된 P2P 세션, 공개 릴레이, Git 3방향 병합  |
| 생성일        | 2026-02-27                               | 2026-02-17                                    |
| 별과 포크     | 9,357과 979(2026-10-28 읽음)             | 6,451과 563(2026-10-23 읽음)                  |
| 라이선스      | MIT, Cloud만 Apache 2.0                  | MIT                                           |

두 프로젝트는 서로 다른 선택을 한다.
open-pencil은 이미 존재하는 형식인 `.fig`를 중심에 두고 그 위에 CLI, MCP,
AI를 얹는다.
ZSeven의 OpenPencil은 새 형식 `.op`를 만들어 Git에서 비교되게 하고,
에이전트 팀과 코드 생성 대상 폭으로 차별화한다.
이 문서의 해석으로는 앞쪽이 전환 비용을 줄이는 길이고 뒤쪽이 새 작업 방식을
제안하는 길이다.
두 README는 서로를 언급하지 않으며, 한쪽이 다른 쪽에서 갈라졌는지는 이 문서가
확인하지 못했다.
별과 포크는 읽은 날짜가 다르므로 정확한 비교가 아니다.

### Pencil 계열 파일에 닿는 오픈소스라는 위치

README는 `.pen`(Pencil) 문서를 앱이나 운영체제 파일 탐색기에서 열 수
있다고 적는다.
GeekNews의 댓글에서 jwseo는 pencil.dev가 나온 지 얼마 안 된 것 같은데 곧바로
오픈소스 대체제가 나왔다고 적었다.[^jwseo]
tested는 같은 스레드에서 pencil.dev와 비교해서 어떠냐고 물었다.[^tested]
이 문서는 pencil.dev를 열어 보지 않았고, 두 댓글에 답이 달리지 않았다.
이 문서의 해석으로는 `.pen` 지원은 Figma만이 아니라 Pencil 쪽 파일의 이동
경로까지 겨냥한 것이다.
다만 어느 범위까지 열리는지는 README의 지원되는 문서라는 표현
이상으로 알 수 없다.

## 비평

### 상태가 거칠다는 말과 호환성 주장 사이의 간격은 측정되어 있지 않다

README는 활발히 개발 중이고 거친 부분이 있다고 인정하지만,
`.fig` 호환이 어디까지 되는지는 이 저장소의 README에서 수치로 알 수 없다.
호환성의 빈틈은 로드맵 페이지에 있다고만 안내한다.
이 문서는 그 페이지를 열어 보지 않았다.
파일을 읽고 쓴다는 문장은 읽어서 보인다는 것인지,
쓴 파일을 Figma가 문제없이 여는지까지 포함하는지가 갈린다.
실제 업무 파일로 왕복 시험을 해 봐야 판단할 수 있다.

### AI 기능의 품질 근거는 호환성 표를 따로 읽어야 한다

내장 채팅은 100개가 넘는 도구를 내세우지만, 도구 수는 품질의 척도가 아니다.
README는 모든 공급자가 브라우저에서 되지는 않고 모든 모델이 도구 호출을 제대로
스트리밍하지는 않는다고 직접 인정한다.
그래서 어떤 모델이 어느 작업에서 쓸 만한지는 별도 호환성 페이지의 측정 결과에
달려 있고, 이 문서는 그 결과를 확인하지 못했다.
디자인 결과물의 질을 비교하는 평가도 README에는 없다.

### 한 저장소에 담긴 범위가 크고 유지 비용은 열려 있다

에디터, 렌더링, 레이아웃 엔진 포크, 협업, CLI, MCP, SDK, 데스크톱 앱,
선택형 Cloud, 문서 사이트가 한 프로젝트에 들어 있다.
GitHub API의 열린 이슈 수는 156이고, 이 값에는 열린 풀 리퀘스트가 포함된다.
이 숫자는 읽은 시점의 값이며 프로젝트 건강도의 판정은 아니다.
Figma 호환처럼 상대가 형식을 바꾸면 따라가야 하는 약속도 있어서,
장기 유지의 기반이 무엇인지는 README에서 읽을 수 없다.
후원 관계로는 Anthropic의 오픈소스 프로그램 지원이 감사 문구에 적혀 있다.

### 공식 빌드의 익명 신호는 로컬 우선과 나란히 놓고 읽어야 한다

로컬 우선과 계정 없음을 내세우면서 공식 빌드는 하루 한 번 익명 신호를 보낸다.
README는 항목을 개인정보 페이지에 전부 적었고 끄는 방법도 있다고 하며,
통계는 동의할 때만 공유한다고 밝힌다.
이는 숨긴 것이 아니라 공개한 것이지만, 로컬 우선이라는 말의 범위를 정확히
읽으려면 그 페이지를 확인해야 한다.
이 문서는 그 페이지를 열지 않았다.

### 오픈소스 Figma 대안으로는 Penpot이 먼저 자리를 잡고 있다

HN의 유일한 댓글에서 exceptione은 Figma의 확립된 대안은 Penpot이라고
짚었다.[^exceptione]
OpenPencil이 자기 사이트의 비교 페이지에서 Penpot과 스스로를 견주었고,
비교가 대체로 균형 있어 보인다고도 했다.[^exceptione]
다만 Penpot 생태계에는 데스크톱 버전이 있는데 그 비교는 이를 인정하지 않는다고
지적했다.[^exceptione]
이 문서는 그 비교 페이지를 열어 보지 않았고,
내용은 댓글 작성자가 전한 범위로만 다룬다.
이 문서의 해석으로는 이 대목이 OpenPencil의 차별점을 가린다.
Penpot과 겹치지 않는 부분은 README가 내세운 `.fig` 네이티브 읽기,
CLI와 MCP를 통한 자동화, 내장 AI다.
그러니 비교의 기준을 오픈소스 여부가 아니라 이 세 가지로 잡아야 한다.

## 인사이트

### 에이전트가 디자인 도구를 쓰기 시작하면 파일 형식의 개방성이 곧 접근권이 된다

README가 Figma의 약점으로 든 것은 사람이 쓰는 기능이 아니라 에이전트가 접근할 수
있는 정도다.
MCP 서버가 읽기 전용이라는 점이 핵심이다.
디자인 파일이 에이전트의 작업 대상이 되면,
형식을 읽고 쓸 수 있는 도구가 에이전트에게 열려 있는 도구가 된다.
이 문서의 추론으로는 그때 경쟁 축은 편집 기능의 우열에서 어느 도구에 에이전트가
쓰기 권한을 가지는지로 이동한다.
이 가설을 뒤집는 관측은 Figma가 쓰기 가능한 공식 MCP와 안정된 자동화 API를
내놓아 격차가 사라지는 경우다.

### 디자인과 코드 사이의 경계가 CLI 하나로 낮아지면 디자인 검사가 CI로 들어온다

`lint`가 이름, 레이아웃, 접근성을 검사하고 `analyze`가 색 사용량을 세며,
HTTP 모드의 MCP가 CI용으로 안내된다.
이 조합이면 디자인 파일이 풀 리퀘스트에서 코드처럼 검사될 수 있다.
디자인 시스템의 일관성은 보통 사람이 눈으로 점검했는데,
기계가 판정하는 항목은 코드의 린트와 같은 방식으로 자동화된다.
시험해 볼 방법은 한 팀의 실제 `.fig` 파일에 `lint --preset strict`를 돌려 나온
지적 가운데 디자이너가 수긍하는 비율을 세어 보는 것이다.
이 비율이 낮으면 검사의 규칙이 디자인 관행과 어긋난다는 뜻이다.

### 두 OpenPencil의 갈림은 디자인 도구가 무엇을 대체하느냐의 질문이다

GeekNews에서 xguru는 예전 같으면 이런 도구가 어도비 제품군을 대체하는 용도였을
텐데 이제는 어도비에 관심이 없다고, 한 세대가 바뀐 것 같다고 적었다.[^xguru]
이 말을 두 프로젝트에 대어 보면, 대체 대상이 Figma인지 사람의 손
작업인지로 나뉜다.
open-pencil은 Figma 파일과 Plugin API를 그대로 끌어안아 Figma의 자리를
채우려 한다.
`design/openpencil-zseven.md`의 OpenPencil은 새 형식과 에이전트 팀으로
디자이너의 수작업 자체를 줄이려 한다.
이 문서의 해석으로는 두 방향이 서로를 대신하지 않고,
팀이 가진 기존 `.fig` 자산의 양에 따라 다른 쪽이 먼저 맞을 수 있다.

실제로 고르려면 질문 둘을 먼저 적어 본다.
첫째, 지금 쓰는 디자인 파일이 `.fig`이고 그것을 계속 읽어야 하는가.
그렇다면 open-pencil의 `.fig` 읽기와 쓰기를 먼저 시험한다.
둘째, 디자인 변경을 코드 리뷰처럼 Git에서 확인하고 싶은가.
그렇다면 사람이 읽을 수 있는 `.op` JSON을 내세운 쪽을 시험한다.
두 질문의 답이 갈리면 두 도구를 같은 샘플 화면으로 돌려 결과와 수정 횟수를
비교하는 것이 이 문서가 권하는 방법이다.
이 가설을 뒤집는 관측은 한쪽이 다른 쪽의 형식과 기능을 모두 흡수해 격차가
사라지는 경우다.

---

[^exceptione]: <https://news.ycombinator.com/item?id=47222796>

[^jwseo]: <https://news.hada.io/topic?id=27658#cid53506>

[^tested]: <https://news.hada.io/topic?id=27658#cid53436>

[^xguru]: <https://news.hada.io/topic?id=27658#cid53400>
