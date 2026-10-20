# Hycli: 웹사이트를 타입이 있는 CLI와 MCP 서버로 바꾸는 도구

<https://github.com/Hybirdss/Hycli>

## 소개

Hycli는 웹사이트 주소와 하고 싶은 일을 주면
그 사이트를 다루는 타입이 있는 CLI와 MCP 도구 묶음을 만들어 주는 도구다.
README는 세 개의 AI 작업자가 사이트의 문서, 프런트엔드 번들,
실제 브라우저의 네트워크 트래픽을 살펴
읽기와 쓰기 동작을 모두 구성한다고 설명한다.
준비 단계에서는 계정을 바꾸는 요청을 실행하지 않는다는 것이 핵심 약속이다.

저장소는 Rust로 작성되었고 라이선스는 Apache-2.0이다.
README가 안내하는 최신 릴리스는 v0.1.0이다.
저장소는 2026년 10월 9일에 만들어졌으므로 아직 초기 단계의 프로젝트다.
웹사이트 엔진과 로컬 대시보드(`http://127.0.0.1:4318`)가
하나의 네이티브 바이너리에 들어 있고,
릴리스 패키지를 실행하는 데는 Rust도 Node.js도 필요 없다고 한다.

## 동작 방식

Hycli가 사이트를 이해하는 근거는 네 가지 인터페이스다.

| 사이트의 인터페이스  | 준비되는 기능                                                      |
| -------------------- | ------------------------------------------------------------------ |
| REST와 OpenAPI       | JSON/YAML 스키마와 API 문서에 근거한 읽기와 쓰기 동작              |
| GraphQL              | 파싱된 query와 mutation 문서, 타입이 있는 JSON 변수                |
| HTML과 JS 렌더링     | 구조화된 레코드, 링크, 페이지 넘김, 로컬 Chromium을 쓰는 읽기      |
| JSON과 URL 인코딩 폼 | 입력과 기본값이 문서화된 폼 제출(`POST`, `PUT`, `PATCH`, `DELETE`) |

동작의 종류에 따라 실행 규칙이 다르다.
읽기와 검색은 근거가 있고 안전한 읽기로 분류되면 바로 실행한다.
만들기, 보내기, 고치기, 지우기는 준비 중에는 절대 실행하지 않고
CLI에 합성만 해 둔다.
이 동작들은 기본적으로 꺼져 있고(`writes: false`),
AI 에이전트가 CLI마다 한 번 사용자에게 허용 여부를 묻는다.
효과가 불분명한 동작은 검토할 수 있도록 전송 전에 보류한다.
인증 요구나 요청 제한에 걸리면 전송 방식을 바꾸거나 멈춘다.
순서는 HTTP, 페이지 안의 `window.fetch`, 스텔스 Chromium이다.

## 사용하기

README의 30초 예시는 네 단계다.

```sh
# 1. 사이트와 목표를 알려 준다 (읽기와 쓰기를 준비하되 실제 변경은 하지 않는다)
hycli prepare https://your-website.example \
  --intent "Search posts, save drafts, and publish articles"

# 2. 준비된 읽기, 쓰기, 여러 단계 워크플로를 본다
hycli describe your-website

# 3. 읽기 동작은 바로 실행한다
hycli your-website search-posts --query "release notes"

# 4. 쓰기를 이 CLI에 한 번 허용한 뒤 만들기와 고치기를 실행한다
hycli writes your-website allow
hycli your-website create-draft --title "Hello from Hycli" \
  --body "Automated from my terminal."
```

로그인이 필요한 사이트에서는 대시보드(`hycli open`)의 계정 메뉴에서
브라우저 세션을 로컬 보관소로 가져온다.
README는 연결할 수 있는 AI로 OpenAI, Anthropic Claude,
xAI, Z.ai, 로컬 ChatGPT Codex 로그인을 나열한다.

코딩 에이전트에서는 MCP 서버로 붙인다.

```json
{
  "mcpServers": {
    "hycli": {
      "command": "hycli",
      "args": ["mcp"]
    }
  }
}
```

`hycli mcp --sites-only`는 설치된 웹사이트 도구만 노출하고,
`--only-site SITE`는 사이트 하나로 범위를 줄인다.
README가 밝히는 MCP 도구는 `hycli_prepare`, `hycli_writes`, `hycli_run`,
`hycli_check`, `hycli_result`, `hycli_activity`이고,
자격 증명을 읽는 도구는 노출하지 않는다고 한다.

## 설계가 답하는 다섯 가지 걱정

README는 사용자가 가질 만한 걱정을 다섯 가지로 묶어 설계로 답한다.
아래는 README의 주장이며 직접 검증한 것이 아니다.

- AI가 실수로 글을 올리거나 지우지 않는가:
  준비와 점검(`prepare`, `request`, `recon`, `check`) 중에는 쓰기 요청을 실행하지 않는다.
  경로가 `/delete`인 `GET`, GraphQL `mutation`, `method="post"` 폼처럼
  변경을 위장한 요청도 검증 중에는 막는다.
  쓰기 요청은 자동으로 재시도하지 않으며,
  전송 뒤 연결이 끊기면 `action_outcome_unknown`으로 보고한다.
- 쿠키와 토큰이 모델에 가는가:
  쿠키, 저장소 토큰, API 키는 로컬 보관소에만 둔다.
  운영체제 키체인을 쓰거나 `0600` 권한으로 제한한다.
  모델은 계정 이름, 저장소 키 이름, 가려진 응답 스키마만 본다.
  실제 비밀 값은 실행 시점에 Hycli가 로컬에서 주입하고 출력과 로그에서 지운다.
- CAPTCHA나 계정 정지를 부르는가:
  엔드포인트를 추측하거나 퍼징하지 않는다.
  사이트와 계정마다 요청을 직렬화하고 속도를 제한하며 `Retry-After`를 따른다.
  차단되면 같은 요청을 반복하지 않고 전송 방식을 바꾸거나 멈춘다.
- 리디렉션으로 세션이 새거나 명세에 내 경로가 실리는가:
  인증 헤더와 쿠키는 대상 출처에 묶고 다른 출처로 리디렉션되면 즉시 제거한다.
  사설 주소와 루프백은 `--allow-local`을 주지 않으면 막는다.
  브라우저 실행 파일과 프로필 경로는 이식 가능한 `SiteSpec`에 쓰지 않는다.
- 로그인이 만료되면 토큰을 낭비하는가:
  `hycli check`는 LLM 없이 검증된 읽기 체인을 다시 실행해
  `signed_out`, `site_changed`, `blocked`, `unreachable`을 구분한다.

## 트레이드오프

### 사이트가 약속하지 않은 인터페이스에 기댄다

Hycli는 공식 API뿐 아니라 프런트엔드 번들과
브라우저 네트워크 관찰도 입력으로 쓴다.
그래서 API가 없는 사이트도 다룰 수 있다.
대신 사이트가 화면을 바꾸면 계약이 조용히 깨진다.
`hycli check`가 `site_changed`를 따로 구분하는 것은
이 위험을 설계가 인정한 결과다.
다만 점검은 읽기 체인만 다시 실행하므로 쓰기 동작이 깨졌는지는
실제로 실행해 보기 전에는 알 수 없다고 보는 것이 안전하다.
이는 README를 바탕으로 이 글에서 추론한 것이다.

### 안전의 큰 부분이 한 번의 허용에 걸린다

쓰기 확인은 CLI마다 한 번이다.
허용하면 그 CLI의 모든 쓰기 동작이 사용자가 요청하는 대로 바로 실행된다.
동작 하나하나를 확인받는 방식보다 마찰이 적지만,
허용 시점에 어떤 쓰기 동작이 준비되어 있었는지와 이후 `hycli request`로
동작이 추가되었을 때 허용이 그대로 적용되는지는 README만으로는 알 수 없다.
쓰기를 허용하기 전에 `hycli describe`로 목록을 직접 읽어야 하는 이유다.

### 자동화의 합법성은 사용자 몫이다

README는 승인받은 사이트와 계정에만 쓰라고 하고,
이용 제한이나 계정 정지에 대해 저작자는 책임지지 않는다고 밝힌다.
스텔스 Chromium이나 로그인 세션 재사용은
사이트 약관이 금지하는 자동화일 수 있다.
도구가 요청 속도를 낮춰 주더라도 약관 위반 여부를 판단해 주지는 않는다.

## 함정

- 읽기 동작도 로그인한 세션으로 실행되므로
  읽기가 서버에 흔적(조회 기록, 읽음 표시)을 남기는 사이트가 있다.
  README의 안전한 읽기 분류가 이런 부작용을 알아낸다고 보장하지 않는다.
- 준비된 동작은 AI가 합성한 것이다.
  이름과 설명이 그럴듯해도 실제 요청이 의도와 다를 수 있으므로
  쓰기를 허용하기 전에 동작의 입력과 효과를 읽는다.
- Windows 앱 바운드 암호화나 비공개 컨테이너에 잠긴 세션은 자동으로 가져오지 못한다.
  그때는 대시보드에서 계정을 직접 연결하거나 쿠키 파일을 가져온다.
  README는 쿠키를 AI 채팅에 붙여 넣지 말라고 경고한다.
- 쓰기가 `action_outcome_unknown`으로 끝났다면 같은 명령을 다시 실행하지 말고
  사이트에서 결과를 먼저 확인한다.

## 확인하기

README가 권하는 검증 절차는 합성된 로컬 웹사이트와 고정 데이터로만 돌린다.

```sh
npm --prefix dashboard ci
npm --prefix dashboard run check
npm --prefix dashboard run build
cargo test --all-targets --locked
cargo build --locked --bin hycli --example dashboard_fixture
node scripts/test-e2e.mjs --full
```

README는 실제 제3자 계정에서 쓰기 동작을 시험하지 말라고 분명히 적어 둔다.
처음 써 볼 때도 내 계정이 아닌 연습용 사이트나 읽기 전용 동작부터 시작한다.

## 체크리스트

- 대상 사이트와 계정에 자동화 접근 권한이 있는가.
- 쓰기를 허용하기 전에 `hycli describe`로 준비된 동작 목록을 읽었는가.
- 쓰기 허용을 되돌리는 명령(`hycli writes SITE deny`)을 아는가.
- 로그인이 만료된 것 같을 때 `hycli check`로 원인을 구분하는가.
- 쿠키 파일을 AI 채팅이 아니라 대시보드로만 가져오는가.
- 릴리스 체크섬(`sha256sum -c`)을 확인하고 설치했는가.

## 기억할 원칙

### 준비와 실행을 갈라 위험을 한 곳에 모은다

Hycli는 동작을 발견하고 합성하는 단계에서는 부작용을 막고,
실행하는 단계에서만 사용자의 허용을 받는다.
AI가 만든 결과물을 믿을 수 없다는 전제에서
검토 가능한 중간 산물(CLI 명세)을 두고 그 위에서 허용을 받는 구조다.
다른 에이전트 도구를 평가할 때도 사람이 읽고
승인하는 지점이 어디인지를 먼저 찾아보면 안전 주장을 따져 보기 쉽다.
