# Claude Code mods 공식 개요: 무엇을 할 수 있고, 어디까지 믿어야 하나

원문: [Mods overview - Claude Code Docs](https://code.claude.com/docs/en/plugins/mods/overview)

HN 토론: <https://news.ycombinator.com/item?id=49925800> (3점, 0개 댓글)

## 소개

Claude Code 공식 문서의 mods 개요 페이지다.
mod는 Claude Code의 모양과 동작을 바꾸는 플러그인이고,
JavaScript나 TypeScript로 쓴 이벤트 처리기로 이루어진다.
도구 호출, 제출된 프롬프트, 화면의 일부가 그려지는 순간 같은 이벤트가 일어나면
Claude Code가 처리기를 부르고,
처리기는 그 이벤트를 지켜보거나 바꾸거나 넘겨받는다.

문서는 용어부터 정리한다.
설정 파일에 셸 명령, HTTP 요청,
프롬프트로 적는 기존 훅은 “설정 훅(settings hook)”이고,
이 페이지에서 그냥 “훅”이라고 하면 mod의 처리기,
즉 Claude Code 안에서 도는 함수를 뜻한다.

만드는 법은 블로그 튜토리얼을
정리한 [Claude Code mods 입문](claude-code-mods.md)에,
바로 설치해 쓸 수 있는 모음은
[hamzafer/claude-code-mods](hamzafer-claude-code-mods.md)에,
mod로 이어진 설계 제안은
[Claude Code를 미들웨어로 열겠다는 제안](claude-mods-function-hooks.md)에 있다.
이 문서는 공식 개요가 정한 범위와 신뢰 경계를 중심으로 정리한다.

## mod가 할 수 있는 것

설정 훅, 스킬, 상태 줄,
MCP 서버는 Claude Code 바깥에서 스크립트를 돌리거나 텍스트와 도구를 준다.
mod는 Claude Code 안에서 돌기 때문에 그것들이 못 하는 일을 한다.

| 할 수 있는 일                       | 예                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------- |
| 쓸 수 있는 화면 그리기              | 대화 옆 창, 프롬프트 위 띠, 탭·버튼·텍스트 필드                                       |
| Claude Code 자신의 화면 다시 그리기 | 도구 호출 행, 스피너, Claude가 질문하는 대화 상자의 교체나 꾸밈                       |
| 도구 호출과 요청에 끼어들기         | 사용자에게 묻는 동안 도구 호출 보류, 도구 없이 답하기, 요청 하나를 다른 모델로 보내기 |
| 명령으로 내 코드 실행               | Claude 턴 없이, Claude가 일하는 중에도 바로 실행되는 `/command`                       |
| 훅 사이에 데이터 공유               | 한 훅이 도구 호출을 세고 다른 훅이 스피너 옆에 그 수를 표시                           |

### 처리기가 이벤트로 하는 세 가지

Claude Code는 이벤트를 처리하기 전에 훅을 먼저 부르므로, 다음 일은 훅이 정한다.

- **관찰**: 보기만 하고 그대로 넘긴다.
- **다시 쓰기**: 이벤트를 바꿔서 넘긴다.
- **응답**: 직접 처리해 원래 동작을 막는다. 명령을 거부하는 것이 예다.

화면 그리기, 명령 추가, 모델 호출, 파일 읽기, 프로세스 실행, 네트워크 요청처럼
자기 코드 바깥의 일은 모두 mods API를 거친다.
다른 길이 없기 때문에 Claude Code는
설치 전에 mod가 무엇을 하는지 나열할 수 있다.

### 가장 작은 예

공식 문서의 첫 예제는 파일 세 개로 끝난다.

```text
first-mod/
├── .claude-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json
    └── register.js
```

`register.js`는 도구 호출 수를 세어 스피너 옆에
`Thinking · tool calls: 3…`처럼 표시한다.

```javascript
// The count, shared by the two hooks below
let calls = 0

// Claude Code calls this once when the mod loads
export function register(on) {
  // Runs each time Claude is about to use a tool
  on('tool.call', async ($, e, next) => {
    calls += 1
    // Ask Claude Code to draw the interface again, so the new count shows
    $.ui.invalidate('ui.render')
    // Let the tool run as usual
    return next(e)
  })

  // Runs each time Claude Code draws the spinner
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    // Keep Claude Code's spinner, with the count added after its word
    return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
  })
}
```

`tool.call` 훅은 관찰, `ui.render` 훅은 다시 쓰기다.
두 훅은 파일 맨 위의 `calls` 변수를 함께 쓴다.

## 설치하고 끄기

mod는 플러그인처럼 마켓플레이스에서 설치한다.

```bash
claude plugin install token-chart@your-org
```

세션 안에서는 `/plugin install token-chart@your-org`를 쓴다.
세션이 열린 상태에서 셸로 설치하거나 업데이트했다면
`/reload-plugins`로 불러온다.
Anthropic은 `anthropics/claude-code-playground` 저장소의 `claude-code/mods`에
token-weather, blast-radius, replay-theater 예제를 지원 없이 공개한다.

mod는 기본으로 켜져 있다.
터미널은 Claude Code v2.1.287 이상, 데스크톱 앱은 v2.1.286부터 동작한다.
끄는 범위는 세 가지다.

| 범위                       | 방법                                                   |
| -------------------------- | ------------------------------------------------------ |
| mod 하나                   | `/plugin`의 Installed 탭에서 그 플러그인을 끄거나 제거 |
| 설치한 모든 mod, 한 세션만 | `--safe-mode`로 시작 (다른 사용자 설정도 함께 꺼짐)    |
| 설치한 모든 mod, 모든 세션 | `~/.claude/settings.json`에 `"disableAllHooks": true`  |

`disableAllHooks`는 설정 훅과 사용자 상태 줄도 함께 끄지만,
조직이 관리하는 것은 계속 돈다.
초기 접근 때 쓰던 `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS`는 v2.1.287부터 무시되므로
`0`으로 두어도 mod가 꺼지지 않는다.
세션이 불러온 mod는
`/plugin` 화면의 탭 아래 흐린 줄(`1 mod active · first-mod`)에서 확인한다.

## 어디까지 믿을 것인가

공식 문서가 가장 길게 다루는 것은 신뢰다.
mod는 사용자 권한으로 돌고 샌드박스되지 않는다.
설치하고 나면 mod는 다음을 할 수 있다.

- 사용자 계정이 닿는 모든 파일을 읽고 쓰고, 프로그램을 실행하고, 네트워크 요청을 보낸다.
- 환경 변수와 설정 파일에 든 API 키를 읽는다.
- 보내는 모든 프롬프트와 Claude의 모든 도구 호출을 본다.
- 프롬프트나 도구 호출을 고쳐 쓰고, 사용자가 친 것처럼 프롬프트를 제출하고, 다른 세션에 메시지를 보낸다.
- 사용자가 묻기 전에 도구 호출을 승인한다.
- 요금제나 API 키로 모델을 불러 사용량을 쓴다.

샌드박스를 켜도 격리되는 것은 Claude가 실행하는 Bash 명령이고,
mod가 띄운 프로세스는 그 밖에서 돈다.
도구 호출을 승인하는 mod는 `ask` 규칙이 물어볼 호출이나
사용자의 `PreToolUse` 훅이 막은 호출도 승인할 수 있고,
문서는 `deny` 규칙이 거부한 호출을 승인할 수 있는 경우도 따로 안내한다.
반대로 mod는 권한 확인 창 자체는 다시 그릴 수 없다.

설치 전에는 플러그인 폴더를 받아 실행하지 않고 검사할 수 있다.

```bash
claude plugin validate ./some-mod
```

출력의 `hooks:`와 `calls:` 줄이 mod가 처리하는
이벤트와 Claude Code에 요청하는 일을 보여 준다.

## 어디서 도는가

훅은 플러그인을 불러오는 모든 세션에서 돌지만,
화면은 터미널과 데스크톱 앱에만 그려진다.

| 실행 위치                                              | 훅 실행                           | 화면 표시                  |
| ------------------------------------------------------ | --------------------------------- | -------------------------- |
| 터미널의 `claude` (편집기 내장 터미널, JetBrains 포함) | 예                                | 예                         |
| 데스크톱 앱 Code 탭 (WSL 세션 제외)                    | 예                                | 예 (터미널 전용 요소 제외) |
| 데스크톱 앱의 WSL 세션                                 | 아니요                            | 아니요                     |
| VS Code 확장의 채팅 패널                               | 예                                | 아니요                     |
| `claude -p`와 Agent SDK                                | 예                                | 아니요                     |
| claude.ai나 모바일 앱의 Remote Control                 | 예 (내 컴퓨터의 세션에서)         | 내 컴퓨터의 터미널에       |
| 클라우드 세션                                          | 클라우드에 전달된 플러그인이면 예 | 아니요                     |

화면을 그리는 mod는 어느 앱에서 도는지 확인하고,
그릴 수 없는 곳에서는
대화 기록의 한 줄이나 명령의 텍스트 응답으로 대신할 수 있다.

## mod, 설정 훅, 스킬, MCP 서버 고르기

| 무엇이 필요한가                                      | 고를 것  |
| ---------------------------------------------------- | -------- |
| 창, 프롬프트 위 띠, 사용자 명령, 이벤트 다시 쓰기    | mod      |
| 이미 있는 스크립트로 이벤트를 막거나 허용하거나 기록 | 설정 훅  |
| 같은 지시를 대화에 계속 붙여 넣고 있음               | 스킬     |
| Claude가 외부 시스템에 닿아야 함                     | MCP 서버 |

플러그인 하나에 이 모두를 담을 수 있으므로,
mod는 스킬이나 MCP 서버와 같은 플러그인으로 배포될 수 있다.

## Claude Code에 내장된 mod

Claude Code의 일부 기능도 mod다.
`/plugin`의 Installed 탭에서 Built-in 아래에 보이고,
업데이트나 제거는 할 수 없다.

| 이름                         | 하는 일                                                     |
| ---------------------------- | ----------------------------------------------------------- |
| `cc-plugin-agents-md`        | `AGENTS.md`를 프로젝트 지시로 불러온다                      |
| `cc-plugin-diff`             | `/diff`를 넘겨받아 창을 그린다                              |
| `cc-plugin-plugin-authoring` | mod 작성용 `plugin-authoring` 스킬을 준다 (mod 코드는 없음) |
| `cc-plugin-sec-default`      | 조직이 관리하는 것을 사용자가 설치한 mod로부터 지킨다       |
| `cc-plugin-telemetry`        | Claude Code와 내장 mod의 분석 기록을 보낸다                 |
| `cc-plugin-you-should-know`  | 놓친 것을 알려 주는 보조 에이전트, 직접 켜야 동작한다       |

`disableAllHooks`, `--bare`, `--safe-mode`처럼 설치한 mod를 끄는 설정과 플래그는
내장 mod를 끄지 않는다.
`sec-default`는 사용자가 끌 수 없고, 관리자가 관리 설정에서 순서를 정한다.
`diff`, `agents-md`, `sec-default`,
`telemetry`의 소스는 `anthropics/claude-code` 저장소의 `mods/`에 공개되어 있다.

## 함정

- “샌드박스를 켰으니 안전하다”는 mod에는 맞지 않는다. mod가 띄운 프로세스는 샌드박스 밖이다.
- 권한 규칙을 마지막 방어선으로 믿으면 안 된다. 승인하는 mod는 `ask` 규칙과 `PreToolUse` 훅의 차단을 넘을 수 있다.
- `disableAllHooks`로 텔레메트리까지 꺼진다고 생각하면 틀린다. 내장 mod는 그대로 돌고, 텔레메트리는 따로 꺼야 한다.
- 예전의 `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=0`은 더 이상 mod를 끄지 않는다.
- `claude -p`, Agent SDK, VS Code 확장에서는 훅은 돌지만 화면은 없다. 화면에 기대는 mod는 그곳에서 조용히 아무것도 보여 주지 않는다.
- 샘플 mod 저장소를 마켓플레이스로 추가하면 그 클론을 가리키므로, 클론을 옮기거나 지우면 mod가 불러와지지 않는다.

## 체크리스트

- [ ] 설치 전에 `claude plugin validate`로 `hooks:`와 `calls:`를 확인했는가
- [ ] 이 mod가 도구 호출을 승인하는지, 승인한다면 내 `ask`·`deny` 규칙을 넘을 수 있는지 알고 있는가
- [ ] 꼭 막아야 할 동작을 mod가 아닌 관리 설정이나 샌드박스로 막고 있는가
- [ ] 쓰는 곳(터미널, 데스크톱, VS Code, `claude -p`)에서 이 mod의 화면이 실제로 그려지는가
- [ ] 문제가 생겼을 때 `--safe-mode`로 끄고 비교할 수 있는가

## 기억할 원칙

### mod는 확장이 아니라 내 권한을 빌려 가는 코드다

스킬은 텍스트이고, MCP 서버는 Claude에게 도구를 줄 뿐이다.
mod는 Claude Code 안에서 내 권한으로 돌며,
프롬프트와 도구 호출을 보고 바꾸고 승인한다.
공식 문서가 기능보다 신뢰 경계를 더 길게 설명하는 이유가 여기 있다.
mod를 고를 때의 질문은 “무엇을 해 주는가”보다
“이 코드에게 내 세션 전체를 맡길 수 있는가”가 먼저다.
