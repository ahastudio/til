# OpenGame: 코딩 에이전트용 게임 스튜디오

<https://github.com/nexu-io/opengame>

## 소개

OpenGame은 로컬에서 돌아가는 코딩 에이전트(Claude Code, Codex 등)에
게임 제작 도구와 작업 절차를 붙여 주는 오픈소스 저장소다.
제작사 OpenDesign은 이것을 “첫 번째 Super Game Agent”라고 소개한다.
저장소 설명은 “Unity & Unreal for AI agents”라는 표현을 쓴다.
라이선스는 Apache 2.0이고 언어는 TypeScript다.

저장소에 등록된 홈페이지 주소는 비어 있다.
README와 `package.json`에도 OpenGame 전용 사이트는 없다.
README가 연결하는 외부 주소는 제작사 조직의 사이트 open-design.ai와
모델 구독 서비스 OpenDesign Go다.
open-design.ai에서 `/game/`과 `/opengame/` 경로는 404를 돌려주었다.
내려받은 홈 화면의 HTML에서도 게임 페이지로 가는 링크를 찾지 못했다.[^od]
그래서 이 문서는 저장소만을 대상으로 하며, 헤더에도 저장소 주소만 둔다.

읽은 시점은 2026년 11월 27일이고, GitHub API가 보고한 값은 다음과 같다.

| 항목        | 값                                |
| ----------- | --------------------------------- |
| 생성        | 2026년 11월 25일                  |
| 마지막 푸시 | 2026년 11월 26일                  |
| 스타        | 747                               |
| 포크        | 140                               |
| 열린 이슈   | 10                                |
| 커밋        | 115                               |
| 기여자      | 13명(첫 페이지 기준, 봇 1개 포함) |
| 릴리스      | 없음                              |

`package.json`의 이름은 `openmotion`이고
버전은 0.0.1이며 비공개로 표시되어 있다.
CHANGELOG와 아키텍처 문서도 OpenMotion이라는 이름을 그대로 쓴다.
MCP 도구 이름 `openmotion_game_*`와
스킬 이름 `openmotion-game`을 바꾸지 않았다고 문서가 직접 밝힌다.
저장소 루트에는 OpenMotion이라는 영상 도구의 README도 함께 들어 있다.

## 구조

README가 설명하는 구성은 세 갈래다.

첫째는 Game Studio다.
로컬에서 뜨는 웹 화면으로, 템플릿 목록과 미리보기, 코드 보기,
Remix 버튼을 제공한다.
Remix는 템플릿을 복사해 독립된 편집 가능한 초안으로 만든다.

둘째는 에이전트 연결이다.
로컬 stdio MCP 서버(`mcp.ts`)가 `openmotion_game_*` 도구 12개를 노출한다.
여기에 미디어 도구 2개가 더해진다.
이름은 `openmotion_media_use`와 `openmotion_assets_use`다.
README는 지원 에이전트를 22종이라고 쓴다.

셋째는 Model Gateway다.
이미지, 음악, 음성, 짧은 영상 생성 모델을 사용자의 API 키로 연결한다.
키가 없으면 절차적으로 만든 Canvas, SVG, Web Audio 대체물을 쓴다고 한다.

게임 하나는 폴더 하나다.
`game.json`(메타데이터), `index.html`(진입점), 결정론적 `logic.js`,
`design/plan.md`, `design/style.md`, `design/assets.csv`,
`design/verification.md`가 기본 구성이다.
3D 게임은 Three.js를 폴더 안에 포함한다.

### 검증 절차

README는 게임을 `ready`로 표시하기 전에 다섯 단계를 거친다고 설명한다.

1. `validate`: 정적 검사와 50틱 스모크 테스트
2. `simulate`: 모범, 약한, 방치 경로를 브라우저 없이 돌리는
   3단계 시뮬레이션
3. `playtest`: 헤드리스 Chromium으로 키보드, 마우스, 터치 입력과
   390×844 화면, 콘솔 오류 확인
4. `capture_cover`: 1280×720 커버 이미지 캡처
5. `trailer`: 5초짜리 실제 플레이 클립 3개를 이어 약 19초 예고편 MP4 생성

아키텍처 문서는 한계도 적는다.
`ready` 표시가 검사 통과의 증거는 아니고,
조작감과 재미는 사람이 판단해야 한다는 내용이다.

### 배포 경로

README의 배포 표는 “지금 가능한 것”과 “로드맵”을 나눈다.
지금 가능한 것은 로컬 카탈로그 게시, OpenDesign Cloud를 통한 웹 공유 링크,
9:16 Playable Ad 모드다.
로드맵에 있는 것은 광고 네트워크 포장 프리셋, WeChat·Douyin·TikTok·itch.io
등을 위한 단계별 게시 안내, 여러 LLM이 같은 게임에서 겨루는 Arena다.

## 사용법

README의 빠른 시작은 에이전트에게 설치 문서를 읽게 하는 방식이다.
사용자가 에이전트에 붙여 넣는 지시문은 저장소의 `docs/opengame-setup.md`를
따라 연결하고, 얕은 복제와 LFS 건너뛰기를 쓰라고 말한다.

직접 설치하려면 Git, Git LFS, npm, Node.js 22.18 이상이 필요하다.

```sh
git -c filter.lfs.process= -c filter.lfs.smudge= -c filter.lfs.required=false \
  clone --depth 1 --single-branch --branch main \
  https://github.com/nexu-io/opengame.git
cd opengame
git lfs install --local --skip-smudge
npm ci
npm run build:studio
npm start
```

메인 스킬은 Skills CLI로 설치한다.

```sh
npx skills add https://github.com/nexu-io/opengame/tree/skills --skill opengame
```

Studio와 MCP는 같은 `MOTION_DATA_DIR`을 가리켜야 같은 게임 폴더를 본다.
이 디렉터리는 저장소 밖에 두라고 문서가 권한다.
Claude Code는 stdio MCP 항목을 추가하고 `openmotion-game` 스킬을 설치한 뒤
`/mcp`로 확인한다.

## 분석

### 에이전트가 아니라 도구 상자를 판다

OpenGame은 자체 에이전트를 내놓지 않는다.
사용자가 쓰던 에이전트를 그대로 두고, 그 에이전트가 부를 도구 12개와
읽을 참고 문서(README 기준 18개)를 제공한다.
[Open Design](../design/open-design.md)과 같은 조직이 만들었고,
“사용자의 에이전트를 쓴다”는 틀도 같다.
디자인용으로 만든 틀을 게임에 옮긴 것으로 읽힌다.

### 게임을 코드와 검증 기록의 묶음으로 본다

게임 폴더에 계획, 스타일, 자산 목록, 검증 결과가 함께 들어간다.
에이전트가 세션을 바꿔도 같은 폴더를 읽으면 이어서 작업할 수 있다는 뜻이다.
아키텍처 문서는 이 설계 문서가 “자동 장기 기억이 아니라
에이전트에게 주는 작업 맥락”이라고 선을 긋는다.
[Claude Code Game Studios](claude-code-game-studios.md)가 에이전트 역할을
나누는 쪽이라면, OpenGame은 산출물과 검증 기록을 표준화하는 쪽이다.

### 템플릿과 Remix가 제품의 입구다

사용자는 빈 화면에서 시작하지 않고 템플릿을 골라 Remix한다.
README의 예시 지시문도 템플릿을 가져와 캐릭터와 미술만 바꾸는 요청이 첫째다.
빈 상태에서 좋은 게임을 만들기 어렵기 때문에
검증된 규칙은 두고 겉모양만 바꾼다는 것이 README가 설명하는 논리다.
이 논리가 맞다면 제품의 품질은 에이전트보다 템플릿 목록에 크게 좌우된다.

## 비평

### 문서가 말하는 규모가 서로 맞지 않는다

저장소 설명은 “100+ viral games”와 “20+ coding agents”라고 쓴다.
README 본문은 템플릿 25개와 에이전트 22종이라고 쓰고,
아키텍처 문서는 에이전트 클라이언트 정의를 29개라고 쓴다.
`templates/games/`를 GitHub API로 열어 보니 항목이 278개였고,
`.gitattributes` 파일을 빼면 폴더가 277개다.
README는 스킬 참고 문서를 18개라고 하지만, 같은 README의 표에 나열된
링크는 16개다.

### 문구가 지금 가능한 범위보다 넓다

README 첫머리와 저장소 설명은 WeChat, Douyin, TikTok, itch.io 게시를
앞세운다.
그러나 같은 README의 배포 표에서 이 항목은 로드맵 칸에 있다.
오늘 가능하다고 적힌 것은 자체 HTML5 프로젝트 내보내기와 수동 포장이다.
아키텍처 문서도 이 플랫폼 배포가 별도 릴리스 통합을 통한다고 적는다.
사용자가 기대할 범위는 표의 “지금 가능한 것” 칸으로 읽는 편이 안전하다.

### 검증 루프가 보여 주는 것은 결함이 없다는 증거가 아니다

시뮬레이션은 결정론적 로직 계약을 따르는 게임에만 적용된다.
플레이 테스트는 오류가 나지 않는지와 입력이 반응하는지를 본다.
재미나 균형이 좋은지는 보지 못한다고 아키텍처 문서가 밝힌다.
저장소의 사례도 이를 보여 준다.
Tidebreaker의 DESIGN.md는 2026년 11월 20일 검증에서 DOM과 캔버스를 흉내 낸
하니스로 115개 단언이 통과했고, 격리 환경의 제한으로 실제 브라우저 확인은
하지 못했다고 직접 적는다.
기록이 솔직하다는 점은 장점이지만, 템플릿 277개 각각에 이런 기록이 있는지는
확인하지 못했다.

### 오픈소스 저장소가 제작사 서비스로 이어진다

README는 로컬 스택에 소프트웨어 구독이 없다고 밝힌다.
동시에 웹 공유 링크는 OpenDesign Cloud를 거치고,
모델 접속은 OpenDesign Go 구독을 권한다.
OpenDesign Go 첫 화면에는 Black Friday 할인 문구가 있었다.[^go]
설치 문서는 스킬 설치가 `nexu-io/opengame`의 설치 수로 집계되도록 한다고 쓰고,
텔레메트리 거부 환경 변수는 유지하라고 적는다.
무료 사용 경로와 유료 경로가 분리되어 있다는 점은 문서에 있지만,
어느 기능이 서비스 계정을 요구하는지는 사용자가 확인해야 한다.

### 에이전트에게 저장소의 지시문을 따르게 한다

빠른 시작의 지시문은 에이전트에게 저장소의 문서를 읽고 따르라고 한다.
이 방식은 편하지만, 저장소 문서가 바뀌면 에이전트가 하는 일도 바뀐다.
지시문은 재현 가능한 버그를 찾으면 `nexu-io/opengame`에 PR을 열어도 좋다고
덧붙인다.
저장소가 이틀 된 단계이므로, 첫 설치는 문서를 먼저 읽은 뒤
명령을 직접 실행하는 쪽이 안전하다.

## 인사이트

### 승부처는 템플릿 목록의 품질이다

에이전트는 사용자가 이미 쓰는 것을 쓰고 모델도 바꿀 수 있다.
그렇다면 남는 차별점은 검증된 시작점의 수와 질이다.
README가 25개를 내세우면서 저장소에는 277개 폴더가 있는 것은,
제품이 양을 앞세우는 단계에서 질의 기준을 어떻게 지킬지 묻게 한다.
템플릿마다 검증 기록과 자산 출처가 있는지가 이 제품의 신뢰를 정한다.

### 같은 틀을 다른 분야에 복제하는 방식

Open Design, OpenMotion, OpenGame은 같은 조직의 같은 틀(MCP, 스킬, 게이트웨이,
템플릿)이다.
분야가 바뀌어도 이름과 식별자가 남아 있는 것이 그 흔적이다.
복제 속도는 빠르지만, 분야별 품질 기준이 얼마나 새로 만들어졌는지는
저장소 나이(이틀) 때문에 아직 알 수 없다.

---

[^od]: OpenDesign, [OpenDesign — Best Open Source Claude Design Alternative](https://open-design.ai/), 2026-11-27

[^go]: OpenDesign, [OpenDesign Go | Affordable, Transparent AI Model Subscriptions for Teams](https://go.open-design.ai/), 2026-11-27
