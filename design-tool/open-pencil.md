# OpenPencil: .fig 파일을 열고 AI와 스크립트로 다루는 오픈소스 디자인 에디터

<https://openpencil.dev>

<https://github.com/open-pencil/open-pencil>

HN 토론: <https://news.ycombinator.com/item?id=47215736> (17점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=27658>

## 목차

- [소개](#소개)
- [만든 이유](#만든-이유)
- [주요 기능](#주요-기능)
- [설치](#설치)
- [CLI](#cli)
- [AI와 MCP](#ai와-mcp)
  - [내장 채팅](#내장-채팅)
  - [코딩 에이전트](#코딩-에이전트)
  - [MCP 서버와 에이전트 스킬](#mcp-서버와-에이전트-스킬)
- [협업](#협업)
- [기술 스택](#기술-스택)
- [오픈소스 디자인 도구의 사각 구도](#오픈소스-디자인-도구의-사각-구도)
  - [네 주자와 각자의 내기](#네-주자와-각자의-내기)
  - [돈과 라이선스가 갈리는 지점](#돈과-라이선스가-갈리는-지점)
  - [파일 형식이 전장이다](#파일-형식이-전장이다)
  - [렌더러가 Skia와 WebGL로 수렴한다](#렌더러가-skia와-webgl로-수렴한다)
  - [에이전트 면이 새 경쟁 축이다](#에이전트-면이-새-경쟁-축이다)
  - [서버냐 기기냐가 팀의 선택을 가른다](#서버냐-기기냐가-팀의-선택을-가른다)
  - [공식 비교 페이지는 어디까지 믿을 수 있나](#공식-비교-페이지는-어디까지-믿을-수-있나)
  - [로드맵은 무엇을 이미 했고 무엇을 약속했나](#로드맵은-무엇을-이미-했고-무엇을-약속했나)
- [분석](#분석)
  - [형식을 여는 것으로 전환 비용을 낮춘다](#형식을-여는-것으로-전환-비용을-낮춘다)
  - [모든 조작을 명령 하나로 호출 가능하게 만들었다](#모든-조작을-명령-하나로-호출-가능하게-만들었다)
  - [로컬 우선은 선택형 서버와 피어 연결로 구현된다](#로컬-우선은-선택형-서버와-피어-연결로-구현된다)
- [비평](#비평)
  - [호환성은 약속이고 측정은 아직 없다](#호환성은-약속이고-측정은-아직-없다)
  - [비교 페이지의 승패표는 한쪽이 채점한 결과다](#비교-페이지의-승패표는-한쪽이-채점한-결과다)
  - [AI 기능의 품질은 모델과 공급자에 달려 있고 그 표는 사용자가 채워야 한다](#ai-기능의-품질은-모델과-공급자에-달려-있고-그-표는-사용자가-채워야-한다)
  - [한 저장소에 담긴 범위가 크고 유지 비용은 열려 있다](#한-저장소에-담긴-범위가-크고-유지-비용은-열려-있다)
  - [로컬 우선과 익명 신호는 나란히 놓고 읽어야 한다](#로컬-우선과-익명-신호는-나란히-놓고-읽어야-한다)
  - [오픈소스 대안이라는 서사는 Penpot이 이미 차지하고 있다](#오픈소스-대안이라는-서사는-penpot이-이미-차지하고-있다)
- [인사이트](#인사이트)
  - [이 싸움은 편집기 기능이 아니라 파일 형식과 에이전트 면의 소유권을 두고 벌어진다](#이-싸움은-편집기-기능이-아니라-파일-형식과-에이전트-면의-소유권을-두고-벌어진다)
  - [도구 선택은 두 질문으로 갈리고 결과는 시험으로만 확정된다](#도구-선택은-두-질문으로-갈리고-결과는-시험으로만-확정된다)
  - [로컬 우선과 서버 우선은 가운데에서 만나므로 선택 기준이 다시 바뀐다](#로컬-우선과-서버-우선은-가운데에서-만나므로-선택-기준이-다시-바뀐다)
  - [승패를 가를 관찰은 세 가지다](#승패를-가를-관찰은-세-가지다)

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
TIL의 `design-tool/openpencil-zseven.md`가 그쪽을 다루므로 이 문서와 겹치지 않는다.
Figma의 오픈소스 대안으로 먼저 자리를 잡은 Penpot은 `design-tool/penpot.md`가 다룬다.
세 문서는 같은 구도를 각자의 자리에서 그리며,
네 도구의 비교는 이 문서의 「오픈소스 디자인 도구의 사각 구도」에 모았다.

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

홈페이지는 명령을 24개로 센다.
analyze, convert, diff, documents, eval, export, find, fonts, formats, import,
info, libraries, lint, node, pages, query, redo, selection, settings, tokens,
tool, tree, undo, variables다.

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

공식 문서의 코딩 에이전트 안내는 Claude Code에 필요한 것을 네 가지로 적는다.[^os-agents]
데스크톱 앱(브라우저 버전은 사용자 컴퓨터에서 프로그램을 시작할 수 없어 안 된다),
`npm install -g @agentclientprotocol/claude-agent-acp`로 까는 ACP 프로그램,
앱 버전에 맞는 `@open-pencil/mcp`,
`claude`에서 `/login`으로 로그인한 계정이다.
그다음 설정의 AI & agents에서 Run guided setup을 열고,
Coding agents on this computer에서 Claude Code를 고른다.
이미 터미널에서 Claude Code를 쓴다면 카드의 Copy setup prompt를 눌러
붙여 넣는 것으로 설치와 `PATH` 확인과 로그인 확인을 맡길 수 있다.
코딩 에이전트는 Design agent 역할만 맡고,
시각 검토와 계획 검토와 백그라운드 작업에는 API 모델이 필요하다.[^os-agents]

문제가 생기는 경우도 문서에 적혀 있다.
Dock이나 시작 메뉴에서 연 앱은 터미널의 `PATH` 일부를 보지 못해
설치한 항목이 not found로 보일 수 있다.
이때는 패키지 관리자의 전역 폴더를 로그인 셸의 `PATH`에 넣고 앱을 다시 켠다.
update needed가 보이면 MCP 서버를 앱 버전에 맞추고,
에이전트가 캔버스를 고치지 못하면 MCP 서버가 없거나 실행 중이 아닌 것이므로
맞는 버전을 다시 설치하고 다시 시작한다.[^os-agents]

### MCP 서버와 에이전트 스킬

`npm install -g @open-pencil/mcp` 뒤 `claude mcp add --scope user open-pencil --
openpencil-mcp`로 등록한다.
스크립트와 CI용으로는 `openpencil-mcp-http`가 있고,
유닉스 소켓과 `http://127.0.0.1:7600/mcp`를 연다.
`OPENPENCIL_MCP_ROOT`로 파일 접근을 한 디렉터리로 제한하며 기본값은 현재
작업 디렉터리다.

stdio 방식은 실행 중인 앱을 자동으로 찾는다.
macOS와 Linux에서는 유닉스 소켓을 먼저 쓰고 안 되면 localhost TCP로
돌아간다.
문서는 문서가 하나 열린 데스크톱 앱을 켜 둔 상태로 쓰라고 안내한다.[^os-mcp]
HTTP 방식의 엔드포인트는 `GET /health`, `POST /rpc`, `POST /mcp`이고
기본은 `127.0.0.1`의 7600번 포트다.
`PORT=0`을 주면 macOS와 Linux에서 TCP가 꺼지고 Windows는 TCP가 필수다.[^os-mcp]
HTTP 방식에서도 앱이 켜져 있어야 하는지는 문서에 명시돼 있지 않다.

도구 수는 페이지마다 다르게 적혀 있다.
홈페이지는 122개, 자동화 페이지는 90개,
MCP 서버 페이지는 100개 이상이라고 한다.[^os-programmable][^os-mcp]

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

## 오픈소스 디자인 도구의 사각 구도

이 문서의 OpenPencil은 혼자 서 있지 않다.
같은 시기에 같은 빈자리를 노리는 도구가 넷 있고, 서로 다른 내기를 건다.
`design-tool/penpot.md`의 Penpot, `design-tool/openpencil-zseven.md`의
ZSeven-W/openpencil(이름이 같지만 다른 프로젝트),
그리고 이전 이름이 Pencil이었던 pen.dev(`design-tool/pen-dev.md`)다.
세 문서는 같은 지도를 서로 다른 자리에서 그린다.
이 절이 지도 전체를 그리고, 나머지 두 문서는 자기 쪽에서 본 모양을 적는다.

### 네 주자와 각자의 내기

| 항목        | Penpot                                                                                 | open-pencil (이 문서)                      | ZSeven-W/openpencil                          | pen.dev                                         |
| ----------- | -------------------------------------------------------------------------------------- | ------------------------------------------ | -------------------------------------------- | ----------------------------------------------- |
| 내기        | 서버가 있는 팀용 오픈소스 디자인 플랫폼                                                | Figma 파일을 그대로 여는 로컬 우선 편집기  | 에이전트가 쓰는 JSON 디자인 형식과 Rust 코어 | 에이전트가 캔버스에서 직접 그리는 상용 도구     |
| 파일        | `.penpot`(ZIP 안의 JSON)                                                               | `.fig`를 읽고 쓰며 `.pen`을 연다           | `.op`(사람이 읽는 JSON), `.fig` 가져오기     | `.pen`(JSON, 스키마 공개), `.fig` 가져오기      |
| 구현        | Clojure, ClojureScript, Rust                                                           | TypeScript, Vue 3, Tauri v2                | Rust 워크스페이스                            | 공개된 정보 없음                                |
| 렌더링      | SVG가 기본, WebGL은 옵트인 베타                                                        | Skia(CanvasKit WASM)                       | GPU Skia(`skia-safe`), 웹은 CanvasKit        | 맞춤 WebGL 파이프라인이라고 밝힘                |
| 에이전트 면 | 공식 MCP 서버(호스팅 또는 직접 설치)                                                   | CLI, MCP, `eval`, 내장 채팅                | MCP 서버, CLI `op`, 에이전트 팀              | MCP, WebMCP, CLI, 편집기 확장                   |
| 서버        | 있음(셀프 호스팅 지원)                                                                 | 없음(선택형 Cloud를 준비 중)               | 없음                                         | 공유 링크와 웹 버전이 있음                      |
| 라이선스    | MPL-2.0                                                                                | MIT, Cloud만 Apache-2.0                    | MIT                                          | 오픈소스 주장이 없음                            |
| 요금        | Professional $0, Unlimited 편집자당 월 $7, Enterprise 구성원당 월 $25[^penpot-pricing] | $0, 자기 AI 공급자 비용, Cloud 가격 미공개 | $0, 자기 AI 공급자 비용                      | Free $0, Pro 월 $16, Ultra 월 $48[^pen-pricing] |
| 규모        | 별 61,785, 포크 4,310                                                                  | 별 9,358, 포크 979                         | 별 6,764, 포크 590                           | High Agency Inc., a16z speedrun 후원            |

위 표의 별과 포크 숫자는 2026년 10월 28일에 GitHub API로 읽은 값이다.
Penpot의 렌더링과 MCP 칸은 Penpot의 공식 페이지에서,[^penpot-webgl][^penpot-mcp]
pen.dev 칸은 pen.dev 자체 소개에서 가져왔다.[^pen-dev]
pen.dev는 소스 공개 여부를 밝히지 않으므로 표의 구현 칸을 채울 수 없었다.
별과 포크는 모두 같은 날 읽은 값이라 서로 견줄 수 있고,
나머지 칸은 각 프로젝트가 자기 문서에서 한 주장이다.

네 도구의 내기는 두 축으로 정리된다.
첫 축은 데이터가 어디 사는가다.
Penpot은 서버에, open-pencil과 ZSeven은 사용자의 기기에,
pen.dev는 아직 공개된 구조가 없다.
둘째 축은 기존 Figma 자산을 얼마나 가져오는가다.
open-pencil은 `.fig` 충실도를 희생하지 않겠다고 로드맵의 비목표에까지 적어
두었고,[^os-roadmap] ZSeven과 pen.dev는 가져오기를 제공하며,
Penpot에는 `.fig` 가져오기가 없다고 open-pencil의 비교 페이지가
적는다.[^os-compare]
이 문서의 해석으로는 이 두 축이 네 도구가 서로의 약점을 겨누는 방향을 정한다.

### 돈과 라이선스가 갈리는 지점

이 구도에서 도구를 고르는 사람이 묻는 질문은 서로 다른 네 가지다.
소스가 공개되어 있는가, 돈을 내지 않고 쓸 수 있는가, 돈을 낸다면 얼마인가,
그 돈이 무엇에 값을 매기는가다.
기준선으로 Figma를 함께 놓았다.

| 도구                | 소스 공개                               | 무료로 쓸 수 있는 것                                   | 돈이 들어가는 곳                                                      | 돈이 매겨지는 단위              |
| ------------------- | --------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------- | ------------------------------- |
| Figma(기준선)       | 아니오                                  | Starter, MCP 도구 호출 월 20회                         | 좌석 월 $3~$90, AI 크레딧[^figma-pricing]                             | 좌석 종류, MCP 호출 한도        |
| Penpot              | 예(MPL-2.0)                             | Professional(구성원 8명, 저장 10GB), 셀프 호스팅       | Unlimited 편집자당 월 $7, Enterprise 구성원당 월 $25[^penpot-pricing] | 편집자 수, 저장 용량, 운영 항목 |
| open-pencil         | 예(MIT, Cloud만 Apache-2.0)             | 편집기, CLI, MCP 전부                                  | 자기 AI 공급자의 토큰, Cloud는 가격 미공개                            | 모델 사용량                     |
| ZSeven-W/openpencil | 예(MIT)                                 | 편집기, CLI, MCP 전부                                  | 자기 AI 공급자의 토큰                                                 | 모델 사용량                     |
| pen.dev             | 밝히지 않음(스키마만 공개)[^pen-format] | 편집기, CLI, MCP 무제한, 에이전트 월 5일[^pen-pricing] | Pro 월 $16, Ultra 월 $48[^pen-pricing]                                | 에이전트 일수와 병렬도          |

표의 Figma, Penpot, pen.dev 칸은 각 가격 페이지의 정가이고 이 문서가 결제를
시험한 것은 아니다.
오픈소스 두 도구의 모델 비용은 공급자와 모델에 따라 다르며,
호환성 표에서 가장 싼 권장 모델은 입출력 100만 토큰당 0.15~0.35유로
수준이다.[^os-byok]
한 팀의 한 달 정가를 열 명 기준으로 어림한 계산은 `design-tool/pen-dev.md`의
인사이트에 있다.

무료라는 말이 네 가지 뜻으로 쓰인다.
라이선스가 자유롭다는 뜻(Penpot, open-pencil, ZSeven),
무료 요금제가 있다는 뜻(Figma Starter, Penpot Professional, pen.dev Free),
로컬에서 서버 없이 돈다는 뜻(open-pencil, ZSeven, pen.dev의 무료 단계),
자기 모델 비용만 낸다는 뜻이다.
이 네 뜻은 서로 겹치지 않는다.
pen.dev는 로컬 편집기와 CLI와 MCP를 무료 단계에서 제한 없이 주지만,
에이전트와 디자인하는 날을 월 5일로 막고 자기 키를 연결해도 이 한도는 풀리지
않는다.[^pen-pricing]
같은 장벽이 오픈소스 두 도구의 문서에는 적혀 있지 않다.
무료의 범위가 편집기에 있는지 에이전트에 있는지가 도구마다 다르다.

에이전트 시대에 새로 생긴 가격 축은 MCP 호출 한도다.
Figma의 MCP 서버는 Starter에서 월 20회, Professional에서 일 200회와 분당 10회,
Organization에서 일 200회와 분당 15회, Enterprise에서 일 600회와 분당 20회로
제한된다.[^figma-pricing]
pen.dev는 모든 요금제에서 디자인하는 동안의 MCP 호출을 무제한이라고
적고,[^pen-pricing] open-pencil과 ZSeven은 로컬 도구라서 호출 한도 자체가 없다.
Penpot의 MCP 서버는 무료이고 오픈소스라고 하지만 호출 한도나 가격은 소개
페이지에 적혀 있지 않다.[^penpot-mcp]
이 문서의 해석으로는 에이전트가 하루에 수백 번 도구를 부르는 작업 방식에서
Figma의 호출 한도가 가장 먼저 닿는 천장이고,
이 천장이 도전자들이 내세우는 가장 직접적인 가격 논거다.

오픈소스 쪽에서 돈이 나올 구멍은 둘이다.
open-pencil은 선택형 Cloud를 준비하며 계정, 조직, 역할, SSO,
버전 기록을 약속하지만 가격은 이 문서가 읽은 범위에 없다.[^os-roadmap]
ZSeven의 README는 앞부분에 두 API 중개 서비스의 후원 문구와 추천 코드를 두고
공식 가격의 10분의 1이나 최대 70% 절감을 내세운다.
어느 쪽이든 무료인 도구가 유료 서비스를 곁에 두는 구조이고,
선택형이 필수로 바뀌지 않는지가 지켜볼 지점이다.
open-pencil은 로드맵의 비목표에 계정이 필수이거나 클라우드 전용인 문서 모델을
만들지 않겠다고 적었다.[^os-roadmap]

### 파일 형식이 전장이다

디자인 파일은 사용자가 도구를 떠날 때 가져가는 유일한 자산이다.
그래서 형식을 누가 읽고 쓸 수 있는지가 곧 이동의 자유다.
`.fig`는 Figma의 독점 바이너리이고, open-pencil의 README는 이것이 Figma의
약점이라고 쓴다.
Penpot의 2022년 HN 스레드에서 dsmmcken은 셀프 호스팅이 된다는 말을 듣고 곧바로
Figma에서 가져올 수 있는지 물었다.[^dsmmcken]
simulo는 그런 가져오기 논의가 있었지만 복잡한 형식을 완벽하게 옮기는 것은 어렵고
불가능한 경우가 많다고 답했다.[^simulo]
dsmmcken은 Sketch에서 Figma로 옮길 때 불완전하게나마 가져오기가 있어서 며칠의
정리로 시작할 수 있었고, 수년 치 작업이 든 파일을 처음부터 다시 만드는 일은
부담이 크다고 되받았다.[^dsmmcken-2]
open-pencil은 바로 이 지점을 첫 번째 목표로 삼은 도구로 읽힌다.
다만 이 문서는 2022년의 한 답변이 지금도 맞는지 확인하지 못했고,
아래의 비교 페이지가 Penpot에 `.fig` 가져오기가 없다고 적은 것을 그대로 전한다.

`.pen`은 또 하나의 전장이다.
README는 open-pencil이 지원되는 `.pen` 문서를 열 수 있다고 하고,
로드맵은 `.pen`을 가져오기 전용이나 자동화 전용이 아니라 앱, CLI, MCP,
SDK 어디서나 편집하고 저장할 수 있는 형식으로 만들겠다고 적는다.[^os-roadmap]
pen.dev는 `.pen`을 에이전트가 바로 다룰 수 있는 JSON 파일이고 스키마를 완전히
공개했다고 소개한다.[^pen-dev]
ZSeven의 README도 `.pen` 파일에서 UIKit를 가져오고 내보낸다고 적는다.
GeekNews에서 jwseo는 pencil.dev가 나온 지 얼마 안 된 것 같은데 곧바로 오픈소스
대체제가 나왔다고 적었고,[^jwseo] tested는 pencil.dev와 비교해서 어떠냐고
물었다.[^tested]
이 문서의 해석으로는 `.pen`을 열어 주는 오픈소스 도구가 둘이라는 사실이,
상용 도구의 파일이 오픈소스 쪽에서 읽히는 구조를 이미 만들었다는 뜻이다.
JSON이라서 사람과 에이전트가 읽기 쉽다는 공통점은 ZSeven의 `.op`,
pen.dev의 `.pen`, Penpot의 ZIP 안 JSON이 모두 갖는다.
그러나 같은 JSON이어도 스키마가 서로 달라서,
한 도구의 JSON을 다른 도구가 어디까지 이해하는지는 열어 본 사람이 없다.

### 렌더러가 Skia와 WebGL로 수렴한다

Penpot의 오래된 약점은 렌더링이었다.
2024년 HN 스레드에서 v3ss0n은 Penpot이 클라이언트와 서버 모두 너무 느리고
비효율적이며 WASM과 WebGL로 프런트엔드를 다시 써야 한다고 적었다.[^v3ss0n]
FractalHQ는 SVG 렌더러를 고집한 것이 플랫폼을 있는 그대로 쓴다는 철학에서 나온
것으로 보였고 그래서 성능의 한계가 처음부터 정해졌다고 적었으며,
v3ss0n은 자기 경험으로 한 화면에 다섯 페이지 정도를 넘기면 줌이 끊기고
브라우저가 죽었다고 답했다.[^fractalhq][^v3ss0n-2]
adpirz는 Figma의 성능이 놀라웠다며 WebGL로 만든 맞춤 렌더러 이야기를 꺼냈고,
throwaway0665는 Figma를 사실상 브라우저 안의 네이티브 앱으로
묘사했다.[^adpirz][^throwaway0665]

Penpot은 렌더러를 바꾸는 중이다.
Penpot 커뮤니티 글에 따르면 WebGL 렌더러는 2026년 6월 3일 Penpot 2.16과 함께
나온 옵트인 베타이고 기본값이 아니며, 설계 작업 캔버스에만
적용된다.[^penpot-webgl]
보기 모드, 내보내기, 텍스트 편집은 아직 이전 SVG와 DOM 경로를 쓰고,
우선순위는 내보내기, 캔버스 기반 텍스트 편집기,
보기 모드 순이며 정식 출시일은 없다.[^penpot-webgl]
같은 글은 성능 수치를 내지 않고, 일부 파일은 오히려 더 느리게 열린다고
적는다.[^penpot-webgl]
2025년 11월 19일의 블로그 글은 보이는 영역만 그리고 곧 보일 타일을 캐시에 두는
타일 렌더링을 설명하며, 벤치마크는 없다.[^penpot-render]

세 오픈소스 도구가 이제 모두 Skia 계열을 쓴다는 점이 눈에 띈다.
open-pencil은 CanvasKit WASM, ZSeven은 네이티브에서 `skia-safe`와 GL,
웹에서 CanvasKit과 WebGL2를 쓴다.
Penpot의 WASM 렌더러도 Rust와 Skia라고 open-pencil의 비교 페이지가
적는다.[^os-compare]
이 문서의 해석으로는 이는 Figma가 보여 준 기준선,
곧 브라우저 안에서 네이티브급 캔버스 성능을 내는 방식에 모두가
수렴한다는 뜻이다.
그러므로 렌더링 성능은 차별점이라기보다 입장료가 되었고,
차이는 렌더러 위의 데이터 모델과 에이전트 면에서 나온다.

### 에이전트 면이 새 경쟁 축이다

open-pencil의 README는 Figma가 프로그래밍 방식 접근을 막는다고 쓰며
에이전트를 앞세운다.
네 도구 모두 MCP를 낸다.
Penpot 홈페이지는 상단 공지로 어떤 에이전트든 Penpot에서 디자인할 수 있다고
알리며 공식 MCP 서버를 내세운다.[^penpot-home]
Penpot의 MCP 소개 페이지는 서버가 Penpot의 플러그인 API를 통해 디자인을 읽고
고치고 새로 만든다고 설명한다.[^penpot-mcp]
Codex, Cursor, VS Code, Claude를 클라이언트로 들고,
Penpot이 호스팅하는 서버와 직접 띄우는 서버 둘을 안내하며,
서버가 무료이고 오픈소스라고 하지만 라이선스는 적지 않는다.[^penpot-mcp]
이 문서가 아는 한 개별 도구 목록은 그 페이지에 없다.

open-pencil의 차별점은 같은 조작이 GUI, CLI, MCP, `eval`,
SDK에서 모두 가능하다는 구조다.
로드맵도 이를 원칙으로 적고, 편집기에 있는 기능이 CLI나 MCP에 빠졌을 때 잡아내는
검사를 만들겠다고 한다.[^os-roadmap]
ZSeven은 에이전트 팀이 병렬로 화면을 그리는 쪽으로 간다.
pen.dev는 편집기 확장과 구독 연동을 앞세운다.[^pen-dev]
이 문서의 해석으로는 에이전트 면이 둘로 갈린다.
하나는 사람이 쓰는 편집기를 에이전트에게 빌려주는 방식이고,
다른 하나는 처음부터 에이전트가 쓰는 도구에 사람이 편집기로 합류하는 방식이다.

### 서버냐 기기냐가 팀의 선택을 가른다

Penpot은 서버 쪽 협업, 접근 통제, 셀프 호스팅,
오래 쌓인 프로덕션 경험이 강점이다.
open-pencil의 비교 페이지도 이 일곱 가지를 Penpot이 더 잘하는 점으로
인정한다.[^os-compare]
2022년 HN에서 wanderingmind는 FOSS의 장점을 일상 도구를 잃을 걱정이 없다는 사업
연속성에서 찾았고,[^wanderingmind] bolt7469는 거친 부분이 있는 도구로 매일
일하기는 어렵다고 답했다.[^bolt7469]
alberth는 오픈소스가 협업 제품에서 지는 이유가 기술이 아니라 네트워크 효과에
있다고 보았다.[^alberth]

open-pencil의 로드맵은 이 구도에 변화를 예고한다.
선택형 Cloud, 조직과 역할, OIDC 기반 SSO, 버전 기록, 셀프 호스팅 배포,
데이터 거버넌스까지 Penpot이 가진 영역을 근미래 작업으로 적었다.[^os-roadmap]
반면 비목표에는 계정이 필수이거나 클라우드 전용인 문서 모델,
AI 키를 프록시하는 호스팅 서비스, 읽기 전용 자동화 면,
`.fig` 충실도를 희생하는 편의 기능이 있다.[^os-roadmap]
Penpot은 반대 방향으로 움직여, 서버 위에 에이전트 면과 새 렌더러를 얹는다.
이 문서의 해석으로는 로컬 우선과 서버 우선이 가운데에서 만나는 모양이다.

### 공식 비교 페이지는 어디까지 믿을 수 있나

open-pencil의 문서 사이트에는 Penpot과 비교한 페이지가 있다.[^os-compare]
핵심 주장은 코드 규모가 약 26,000줄 대 299,000줄(약 11배)이고,
단일 프로세스 클라이언트라서 서버·데이터베이스·컨테이너가 필요 없고,
렌더링과 Figma 호환과 개발자 진입 장벽에서 앞선다는 것이다.[^os-compare]
시작 시간은 2초 미만 대 10초 이상, 연산 지연은 1ms 미만 대 10~50ms,
메모리 기준선은 약 50MB 대 300MB 이상으로 적었다.[^os-compare]
페이지는 Penpot이 더 나은 일곱 가지로 서버 협업, PDF 내보내기, 플러그인 시스템,
디자인 토큰, CSS Grid, 셀프 호스팅, 성숙도를 꼽는다.[^os-compare]

이 페이지는 자기 프로젝트가 쓴 자기 평가라서 조심해서 읽어야 한다.
첫째, 코드 줄 수의 비교는 Penpot이 백엔드, 내보내기 서비스,
Rust 렌더러까지 포함한 전체이고 open-pencil은 편집기 클라이언트뿐이라는 점에서
같은 범위가 아니다.
둘째, 시작 시간과 지연과 메모리 표에는 측정 방법과 환경이 적혀 있지 않다.
셋째, 이 페이지에는 오래된 부분이 보인다.
Penpot이 헤드리스 스크립팅 API도 MCP 연동도 없다고 적었지만,[^os-compare]
Penpot은 공식 MCP 서버를 내놓았다.[^penpot-mcp]
페이지의 AI 도구 수는 90개이고 README는 100개가 넘는다고 하며,[^os-compare]
페이지가 Tauri 데스크톱 앱을 약 5MB라고 적은 것도 README의 약 15MB와 다르다.
페이지가 말하지 않는 것도 있다.
Penpot의 WebGL 렌더러가 베타로 나온 뒤의 성능 비교는 없고,
`.fig` 충실도를 실제 파일로 잰 결과도 이 페이지에는 없다.
이 문서가 이 수치들을 직접 재현하지 못했으므로,
페이지의 구조적 서술(단일 프로세스, 서버 불필요)과 수치 주장을 분리해서
읽어야 한다.

### 로드맵은 무엇을 이미 했고 무엇을 약속했나

로드맵의 현재 초점은 `.fig` 가져오기와 내보내기의 충실도, 저장과 복구의 안정성,
큰 디자인 시스템에서의 반응성, 비라틴 문자와 RTL 같은 국제
텍스트다.[^os-roadmap]
최근 나온 v0.15.0과 v0.15.1은 눈금자 가이드와 스냅,
다차원 컴포넌트 변형과 공개 라이브러리, 저장하지 않은 문서의 로컬 복구,
도구별 권한이 있는 WebMCP 접근을 담았다고 한다.[^os-roadmap]
최신 릴리스는 v0.16.0이다.
다음 릴리스에 들어갈 개발 버전 항목으로는 Reka UI로 동작하는 컴포넌트 미리보기,
W3C 디자인 토큰으로서의 변수, Lint 패널, 캔버스 위에 보이는 AI 에이전트,
되돌릴 수 있는 AI 채팅 턴, 협업 방에서 CRDT로 동기화되는 레이어 트리가
있다.[^os-roadmap]
에이전트 흐름 쪽 약속은 inspect, act, render, compare,
iterate 순환을 공식 스킬 문서로 다듬고,
모든 주요 작업이 렌더나 구조 diff나 lint 결과를 남기게 하고,
lint 규칙의 정밀도를 측정한 뒤에야 차단 게이트로 켜겠다는 것이다.[^os-roadmap]
약속 가운데 눈에 띄는 것은 스크린샷과 참조 이미지를 에이전트의 일급 입력으로
받는 일, 그리고 Stitch와 Pixso 같은 다른 디자인 출처를 위한 어댑터
계약이다.[^os-roadmap]
이 문서가 읽은 부분에는 이 약속들의 날짜가 적혀 있지 않다.

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

## 비평

### 호환성은 약속이고 측정은 아직 없다

README는 활발히 개발 중이고 거친 부분이 있다고 인정한다.
그러나 `.fig` 호환이 어디까지 되는지는 README에서 수치로 알 수 없다.
로드맵의 첫 번째 현재 초점이 `.fig` 가져오기와 내보내기의 충실도를 실제 Figma
파일과 Figma 자신의 렌더링에 맞춰 올리는 일이라는 점이 오히려 현재 충실도가 아직
낮다는 뜻으로 읽힌다.[^os-roadmap]
로드맵은 Figma 기능을 지원, 부분 지원, 왕복만 보존,
미지원으로 나누는 호환성 표를 두고,[^os-roadmap] 이 구분이 정직한 점이다.
왕복만 보존한다는 범주는 파일을 열고 다시 써도 내용이 남지만 편집기에서
렌더하거나 고칠 수는 없다는 뜻이다.
그러니 파일을 읽고 쓴다는 문장이 내 파일의 모든 요소를 편집한다는 뜻은 아니다.
실제 업무 파일로 왕복 시험을 해서 표의 어느 칸에 자기 파일이 걸리는지 봐야 한다.

### 비교 페이지의 승패표는 한쪽이 채점한 결과다

open-pencil의 비교 페이지는 요약표에서 열 가지 차원 가운데 일곱에서
open-pencil이 이긴다고 적고, 협업은 무승부,
셀프 호스팅과 성숙도만 Penpot이라고 적는다.[^os-compare]
채점자가 한쪽 당사자이고, 코드 줄 수의 비교는 범위가 다르며,
성능 수치는 측정 환경이 없다는 점은 앞 절에서 살폈다.
더 근본적인 문제는 승패의 기준이다.
페이지는 아키텍처의 단순함과 코드 유지 가능성을 승리의 항목으로 두지만,
그것이 사용자가 얻는 가치인지는 다른 문제다.
Penpot의 서버 구조는 복잡하지만 접근 통제와 영속성을 준다고 페이지 자신이
인정한다.[^os-compare]
이 문서는 비교 페이지를 사실 주장과 평가로 나눠 읽었다.
Penpot이 베타로 내놓은 WebGL 렌더러와 공식 MCP 서버가 나온 뒤에는 페이지의 일부
항목이 사실로도 맞지 않는다.

### AI 기능의 품질은 모델과 공급자에 달려 있고 그 표는 사용자가 채워야 한다

내장 채팅은 100개가 넘는 도구를 내세우지만 도구 수가 품질을 말해 주지는 않는다.
호환성 페이지는 에이전트 루프가 최대 50단계까지 돌며 매 단계에서 도구 스키마를
다시 보내기 때문에 입력 토큰이 많고, 토큰당 가격이 높으면 비용이 빠르게
불어난다고 적는다.[^os-byok]
도구 호출이 깨지는 방식도 둘로 나눈다.
스트리밍된 도구 호출의 `id`가 빠지면 AI SDK가 `Expected 'id' to be a
string.`이라는 오류를 내며 스트림이 죽고,
인자 조각이 잘못 이어 붙으면 도구가 조용히 실행되지 않는다.[^os-byok]
측정표에서 Scaleway의 `mistral-small-3.2-24b-instruct-2506`은 세 프롬프트 모두
호출을 냈고 비전도 되어 가장 싼 권장 모델이며,
`moonshotai/Kimi-K3`는 흠이 없지만 `gpt-oss-120b`의 약 20배 비용이고,
`openai/gpt-oss-120b`는 같은 모델이 Scaleway에서는 멀쩡한데 Nebius에서만
깨진다.[^os-byok]
웹 빌드에서는 공급자가 CORS 헤더를 제대로 주는지도 문제다.
Scaleway와 TensorX는 성공 응답에만 헤더를 달고 오류 응답에는 달지 않아서,
잘못된 키가 네트워크 실패처럼 보인다고 페이지는 적는다.[^os-byok]
이 표는 2026년 7월 30~31일에 측정한 것이고 페이지 스스로 몇 달 지나면 확인되지
않은 것으로 보라고 한다.[^os-byok]
측정 조건도 섞여 있어서 Scaleway 행은 출력 토큰 한도 16,384,
Nebius와 TensorX 행은 2,000으로 쟀으므로 직접 비교할 수 없다고 페이지가
밝힌다.[^os-byok]
정직한 기록이지만 사용자는 이 위에서 자기 모델을 직접 시험해야 한다.
디자인 결과물의 질을 평가한 자료는 어디에도 없다.

### 한 저장소에 담긴 범위가 크고 유지 비용은 열려 있다

에디터, 렌더링, 레이아웃 엔진 포크, 협업, CLI, MCP, SDK, 데스크톱 앱,
선택형 Cloud, 문서 사이트가 한 프로젝트에 들어 있다.
GitHub API의 열린 이슈 수는 156이고, 이 값에는 열린 풀 리퀘스트가 포함된다.
이 숫자는 읽은 시점의 값이며 프로젝트 건강도의 판정은 아니다.
로드맵은 여기에 Cloud, SSO, 버전 기록, 셀프 호스팅 배포, 데이터 거버넌스,
셰이더 레이어, 프로토타이핑, 모션, 표 노드, 코멘트까지 더한다.[^os-roadmap]
각 항목이 사람 몇 명의 몇 달 치 일인지 적혀 있지 않다.
Figma가 형식을 바꾸면 따라가야 하는 약속도 있어서,
장기 유지의 기반이 무엇인지는 README에서 읽을 수 없다.
README의 감사 문구에는 Anthropic이 오픈소스 프로그램으로 프로젝트를
지원한다고 적혀 있다.

### 로컬 우선과 익명 신호는 나란히 놓고 읽어야 한다

README는 로컬 우선과 계정 없음을 내세우면서 공식 빌드가 하루 한 번 익명 신호를
보낸다고 적는다.
개인정보 페이지에 따르면 신호에는 버전, 플랫폼, 아키텍처, 앱 종류, 브라우저,
사용 통계 동의 여부가 들어가며 `feedback.openpencil.dev`로 간다.[^os-privacy]
식별자는 없고, 사용 통계는 동의할 때만 PostHog의 EU 클라우드로 서버를 거쳐
전달되고, 설정에서 끄거나 `OPENPENCIL_TELEMETRY=0` 또는 `DO_NOT_TRACK=1`로 끌 수
있고, 직접 빌드한 앱이나 포크는 아무것도 보내지 않는다.[^os-privacy]
디자인과 레이어 이름과 프롬프트와 키는 사용자가 공유하거나 동기화하지 않는 한
기기를 떠나지 않는다고 한다.[^os-privacy]
이는 숨긴 것이 아니라 공개한 것이다.
다만 로컬 우선이라는 말의 범위는 네트워크 표에서 정확해진다.
업데이트 확인은 GitHub Releases, 모델 목록은 models.dev,
없는 글꼴은 Google Fonts, 아이콘은 Iconify,
스톡 이미지는 Unsplash나 Pexels로 나가고,
협업 방은 공개 중개 서버가 피어를 소개하며 직접 연결이 안 되면 TURN 릴레이를
거친다.[^os-privacy]
이 가운데 협업 릴레이는 로컬 우선과 가장 긴장하는 부분이다.

### 오픈소스 대안이라는 서사는 Penpot이 이미 차지하고 있다

HN의 유일한 댓글에서 exceptione은 Figma의 확립된 대안은 Penpot이라고
짚었다.[^exceptione]
OpenPencil이 자기 사이트의 비교 페이지에서 Penpot과 스스로를 견주었고,
비교가 대체로 균형 있어 보인다고도 했다.[^exceptione]
다만 Penpot 생태계에는 데스크톱 버전이 있는데 그 비교는 이를 인정하지 않는다고
지적했다.[^exceptione]
비교 페이지를 읽어 보면 이 지적은 맞다.
페이지는 Penpot을 브라우저 전용이라고 적고 Tauri 데스크톱을 open-pencil의
강점으로 둔다.[^os-compare]
이 문서는 Penpot의 데스크톱 버전을 확인하지 못했으므로 exceptione의 말을 그가
전한 범위로만 다룬다.

Penpot과 겹치지 않는 부분은 README가 내세운 `.fig` 네이티브 읽기,
CLI와 MCP를 통한 자동화, 내장 AI다.
그러나 2024년 HN에서 thallavajhula는 독점 디자인 도구가 쌓아 온 UX와 성능 개선을
오픈소스가 따라잡기는 어렵다고 보았다.[^thallavajhula]
이 반론은 Penpot에도 open-pencil에도 같은 무게로 걸린다.
앞으로의 비교는 오픈소스 여부가 아니라 같은 파일로 같은 작업을 했을 때의 속도와
충실도에서 나와야 한다.

## 인사이트

### 이 싸움은 편집기 기능이 아니라 파일 형식과 에이전트 면의 소유권을 두고 벌어진다

여기까지 읽은 사실을 합치면 네 도구가 겨루는 것은 캔버스의 매끄러움이 아니다.
렌더러는 Skia와 WebGL로 수렴하고 있어서 입장료가 되었다.
남는 것은 두 가지다.
어떤 형식으로 파일이 저장되는지, 그 파일을 에이전트가 어떤 면으로 읽고 쓰는지다.
`.fig`, `.pen`, `.op`, `.penpot`, `design.md`가 서로 다른 형식이고,
MCP 서버와 CLI와 플러그인 API가 서로 다른 면이다.
이 문서의 해석으로는 에이전트가 디자인 작업의 상당 부분을 맡게 되면,
에이전트가 가장 매끄럽게 다루는 형식과 면을 가진 도구가 작업이 모이는
자리가 된다.

이 자리의 값은 네트워크 효과로 굳는다.
alberth가 2022년에 협업 제품은 기술이 아니라 네트워크 효과로 이긴다고 쓴 것은
사람의 협업을 두고 한 말이다.[^alberth]
에이전트 시대의 네트워크 효과는 에이전트용 스킬과 레시피,
에이전트가 학습한 형식의 양에서 나올 수 있다.
open-pencil 로드맵이 공식 스킬 문서와 검증된 워크플로 레시피를 적어 둔 것은 이
경쟁을 인식한 흔적으로 읽힌다.[^os-roadmap]
GeekNews에서 xguru는 예전 같으면 이런 도구가 어도비 제품군을 대체하는 용도였을
텐데 이제는 어도비에 관심이 없고 한 세대가 바뀐 것 같다고 적었다.[^xguru]
이 말은 대체 대상이 바뀌었다는 관찰이고,
이 문서의 해석으로는 사람의 수작업을 대체하는 에이전트가 새 대체 대상이다.
이 가설을 뒤집는 관측은 에이전트가 형식과 상관없이 어떤 도구든 비슷하게 잘
다루게 되어 형식과 면의 차이가 의미를 잃는 경우다.

### 도구 선택은 두 질문으로 갈리고 결과는 시험으로만 확정된다

세 문서의 사실을 팀의 상황에 대어 보면 선택 규칙이 나온다.
이 규칙은 이 문서의 해석이며 측정 결과가 아니다.

| 팀의 상황                                                | 먼저 시험할 도구                          | 이유                                                                                     |
| -------------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------- |
| 기존 `.fig` 자산이 크고 계속 읽어야 한다                 | open-pencil                               | `.fig` 읽기와 쓰기가 첫 번째 목표이고 호환성 표가 공개되어 있다                          |
| 서버를 운영할 수 있고 접근 통제와 셀프 호스팅이 필요하다 | Penpot                                    | 서버 협업, 접근 통제, 셀프 호스팅이 강점이라고 비교 페이지도 인정한다                    |
| 디자인 변경을 코드 리뷰처럼 Git에서 보고 싶다            | ZSeven-W/openpencil                       | 사람이 읽는 `.op` JSON과 Git 3방향 병합을 내세운다                                       |
| 에이전트가 화면을 처음부터 그리는 속도가 중요하다        | pen.dev와 ZSeven-W/openpencil             | 에이전트가 캔버스에서 직접 그리고 에이전트 팀이 병렬로 그린다고 한다                     |
| 오픈소스 여부가 필수 조건이다                            | Penpot, open-pencil, ZSeven-W/openpencil  | pen.dev는 오픈소스 주장이 없다                                                           |
| 예산이 가장 중요하다                                     | open-pencil, ZSeven-W/openpencil, Penpot  | 라이선스 비용이 없고 Penpot은 편집자 5명에 월 $35 수준이다                               |
| 에이전트가 하루 종일 도구를 호출한다                     | open-pencil, ZSeven-W/openpencil, pen.dev | Figma는 MCP 호출이 월 20회에서 일 600회로 제한되고 이 도구들은 호출 한도가 없다고 밝힌다 |

시험 방법은 같은 샘플 파일 하나를 네 도구에 넣어 보는 것이다.
측정 항목은 열리는 시간, 메모리, 원본과의 시각 차이,
100개 이상의 레이어를 가진 화면에서 줌과 이동이 끊기는 정도,
에이전트에게 같은 수정을 시켰을 때 실패한 횟수다.
이 중 시각 차이는 open-pencil의 로드맵이 말하는 Figma 렌더링 기준 비교와 같은
방식으로 잴 수 있다.
결과가 도구마다 갈리면 팀에서 가장 비싼 작업이 무엇인지로 선택하면 된다.

### 로컬 우선과 서버 우선은 가운데에서 만나므로 선택 기준이 다시 바뀐다

open-pencil은 Cloud와 SSO와 버전 기록으로 서버 쪽으로 걸어가고,
Penpot은 WebGL 렌더러와 MCP로 로컬 성능과 에이전트 쪽으로
걸어간다.[^os-roadmap][^penpot-webgl]
두 방향이 만나면 지금의 구분, 곧 서버가 없는 도구와 서버가 있는 도구의
구분은 약해진다.
그때 차이로 남는 것은 서버 없이도 모든 기능이 되는지,
곧 오프라인에서의 완결성이다.
open-pencil은 비목표에서 계정이 필수이거나 클라우드 전용인 문서 모델을 만들지
않겠다고 적었다.[^os-roadmap]
이 약속이 지켜지는지는 Cloud가 실제로 나온 뒤에 문서가 Cloud 없이 얼마나 온전히
열리는지로 확인된다.

사업 연속성의 논리도 이 지점에서 갈린다.
wanderingmind가 2022년에 FOSS의 가치로 든 것은 상용 도구가 사라질 때의 위험을
피하는 것이었다.[^wanderingmind]
그러나 형식이 개방되어 있고 도구가 로컬에서 돌며 소스가 공개되어 있을 때와,
오픈소스지만 서버가 필수일 때의 연속성은 다르다.
앞쪽은 도구가 없어져도 파일과 도구를 가져갈 수 있고,
뒤쪽은 서버를 운영할 사람이 있어야 한다.
이 구분은 이 문서의 해석이며, 두 경우의 실제 이주 비용을 비교한 사례는
확인하지 못했다.

### 승패를 가를 관찰은 세 가지다

첫째는 같은 `.fig` 파일을 연 결과의 충실도 비교가 누군가에 의해 공개되는 일이다.
open-pencil이 호환성 표를 갱신하며 보여 주는 충실도가 올라가면 `.fig` 이동의
장벽이 낮아지고, 정체되면 약속이 약해진다.
둘째는 Penpot의 WebGL 렌더러가 기본값이 되고 내보내기와 텍스트 편집까지 옮겨
가는 시점이다.
셋째는 에이전트가 같은 디자인 과제를 네 도구에서 수행한 결과를 비교한 평가가
나오는 일이다.
세 관찰 모두 이 문서가 확인하지 못했다.
그때까지 이 문서가 권하는 것은 어느 한 도구에 파일을 묻어 두지 않는 것,
곧 내보내기 경로를 정기적으로 시험하는 습관이다.

---

[^exceptione]: <https://news.ycombinator.com/item?id=47222796>

[^jwseo]: <https://news.hada.io/topic?id=27658#cid53506>

[^tested]: <https://news.hada.io/topic?id=27658#cid53436>

[^xguru]: <https://news.hada.io/topic?id=27658#cid53400>

[^os-compare]: OpenPencil, [Open Pencil vs Penpot: Architecture & Performance Comparison](https://openpencil.dev/overview/comparison)

[^os-roadmap]: OpenPencil, [Roadmap](https://openpencil.dev/development/roadmap)

[^os-privacy]: OpenPencil, [Privacy and Usage Stats](https://openpencil.dev/overview/privacy)

[^os-byok]: OpenPencil, [BYOK provider and model compatibility](https://openpencil.dev/programmable/byok-provider-compatibility)

[^os-mcp]: OpenPencil, [MCP Server](https://openpencil.dev/programmable/mcp-server)

[^os-agents]: OpenPencil, [Coding agents](https://openpencil.dev/programmable/coding-agents)

[^os-programmable]: OpenPencil, [Automation](https://openpencil.dev/programmable/)

[^penpot-webgl]: Penpot Community, [What's next for the Penpot WebGL renderer](https://community.penpot.app/t/whats-next-for-the-penpot-webgl-renderer/10627), 2026-06-03

[^penpot-render]: Penpot, [Penpot's New Rendering System](https://penpot.app/blog/penpots-new-rendering-system/), 2025-11-19

[^penpot-mcp]: Penpot, [Penpot MCP Server](https://penpot.app/penpot-mcp-server)

[^penpot-home]: Penpot, [Penpot: The open-source design platform for teams.](https://penpot.app/)

[^pen-dev]: Pen, [pen.dev](https://www.pen.dev/)

[^dsmmcken]: <https://news.ycombinator.com/item?id=32852615>

[^simulo]: <https://news.ycombinator.com/item?id=32854272>

[^dsmmcken-2]: <https://news.ycombinator.com/item?id=32855959>

[^v3ss0n]: <https://news.ycombinator.com/item?id=40221928>

[^fractalhq]: <https://news.ycombinator.com/item?id=40240993>

[^v3ss0n-2]: <https://news.ycombinator.com/item?id=40255673>

[^adpirz]: <https://news.ycombinator.com/item?id=40219780>

[^throwaway0665]: <https://news.ycombinator.com/item?id=40220027>

[^wanderingmind]: <https://news.ycombinator.com/item?id=32851517>

[^bolt7469]: <https://news.ycombinator.com/item?id=32851914>

[^alberth]: <https://news.ycombinator.com/item?id=32852803>

[^thallavajhula]: <https://news.ycombinator.com/item?id=40219970>

[^figma-pricing]: Figma, [Pricing](https://www.figma.com/pricing/)

[^penpot-pricing]: Penpot, [Penpot Pricing | From Professional to Enterprise Plans](https://penpot.app/pricing)

[^pen-pricing]: pen.dev, [Pricing](https://www.pen.dev/pricing)

[^pen-format]: pen.dev, [The .pen Format](https://docs.pencil.dev/for-developers/the-pen-format)
