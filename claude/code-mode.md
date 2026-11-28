# Claude Code Code Mode

원문: [Run tool calls from code with Code Mode](https://code.claude.com/docs/en/code-mode)

HN 토론: <https://news.ycombinator.com/item?id=50538346> (3점, 0개 댓글)

## 소개

Code Mode는 Claude가 도구를 직접 하나씩 부르는 대신 JavaScript를 써서 여러 도구 호출을 한 번에 하게 하는 실험 기능이다.
문서는 이 기능이 실험적이고 기본으로 꺼져 있으며 어느 릴리스에서든 바뀌거나 사라질 수 있다고 밝힌다.
설명은 모두 Anthropic 문서의 서술이다.

## 동작 방식

Code Mode가 없을 때 Claude는 Bash, Read, Edit 같은 도구 호출을 요청하고 결과를 읽은 뒤 다음 행동을 정한다.
Code Mode에서는 Claude가 도구 호출을 담은 JavaScript를 쓰고 Claude Code가 그 코드를 세션 안에서 실행한다.
한 코드가 명령을 병렬로 돌리고, 한 결과를 다음 호출에 쓰고, Claude가 읽어야 할 출력만 돌려줄 수 있다.

문서의 예는 재시도 한도를 올리는 작업이다.
코드가 `rg`로 파일을 찾고, `edit`로 값을 바꾸고, 테스트를 돌린 뒤 마지막 줄에서 파일 경로와 테스트 출력을 Claude에게 돌려준다.
대화에는 코드가 아니라 편집의 diff 같은 도구 호출이 보인다.
코드는 `Ctrl+O`로 트랜스크립트 보기를 열면 접힌 **Code** 행으로 볼 수 있다.

문서가 권하는 쓰임은 다음 세 가지이다.

- 여러 파일에서 되풀이되는 변경
- 읽기 전에 걸러야 하는 검색 결과
- 동시에 돌릴 수 있는 독립된 명령 여럿

## 켜고 끄기

요구 사항은 다음과 같다.

- 버전: Claude Code v2.1.323 이상(`stable`과 `latest` 모두). 에이전트 팀과 함께 쓰려면 v2.1.326 이상이다.
- 계정: Claude 구독 또는 Console 계정. 게이트웨이, Amazon Bedrock, Claude Platform on AWS, Google Cloud의 Agent Platform, Microsoft Foundry, Claude Models on Google Cloud(Anthropic 관리형)로는 쓸 수 없다.
- 조직: HIPAA 구성이나 제로 데이터 보존(zero data retention)을 쓰지 않아야 한다.
- 모델: Claude Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.2.
- 환경: 터미널의 대화형 `claude` 세션이다. `-p`, Agent SDK, VS Code 패널, Desktop 앱, 클라우드 세션에서는 되지 않는다. 네이티브 빌드가 필요하고 Windows에서는 Git for Windows가 필요하다.
- 설정: API 키 도우미, OpenTelemetry 내보내기, `DISABLE_TELEMETRY` 같은 설정이 켜져 있으면 시작하지 않는다.

켜는 순서는 다음과 같다.

1. `claude --version`으로 버전을 확인하고 낮으면 `claude update`를 실행한다.
2. 환경변수 `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE`를 `1`로 두고 `claude`를 시작한다. 셸에서 지정해도 되고 `~/.claude/settings.json`의 `env` 블록에 써도 된다.
3. 첫 세션에서 확인 창이 뜨면 **Yes, turn on Code Mode**를 고른다. Claude Code가 다시 시작하고 상단에 Code Mode가 켜졌다는 줄이 나온다.
4. 도구 호출이 많은 작업을 준다. 문서의 예는 모든 Markdown 파일을 읽고 존재하지 않는 로컬 파일을 가리키는 링크를 나열하게 하는 것이다.
5. `Ctrl+O`로 Claude가 쓴 코드를 읽는다.

프로젝트의 설정 파일에 쓴 이 변수는 Claude Code가 무시한다. 내려받은 저장소가 스스로 Code Mode를 켜지 못하게 하려는 것이다.

끄려면 셸과 사용자 설정에서 변수를 지우거나 값을 `0`으로 둔 뒤 새 세션을 시작한다. 한 곳이라도 `0`이면 다른 곳이 `1`이어도 꺼진다.
조직은 관리형 설정(managed settings)의 `env`에 같은 변수를 `0`으로 넣어 사용을 막을 수 있다. 관리형 설정으로 사용자 대신 켜는 것은 되지 않는다.

## 권한과 오래 걸리는 코드

코드 안의 도구 호출은 `deny`와 `ask` 권한 규칙, `PreToolUse` 훅에 도구의 평소 이름(예: `Bash`)으로 걸린다.
그 위에서 모드에 따라 검사가 달라진다.

- 자동(auto) 모드: 분류기가 도구 호출마다가 아니라 코드를 실행 전에 한 번 검토한다. 경로처럼 실행 중에 계산되는 값은 분류기가 보지 못하므로, 반드시 통제할 호출에는 규칙이나 훅을 둔다.
- 그 밖의 모드: 검토 없이 코드가 시작하고, 그 모드에서 물어봤을 도구 호출마다 사용자에게 묻는다.

훅에서 쉘 명령을 검사한다면 명령의 각 부분을 확인해야 한다. 문서는 `app` 폴더에서의 `git push`가 훅에 `cd 'app' && git push`로 도착할 수 있다고 예를 든다.
코드 자체를 검사하려면 코드를 실행하는 도구 이름 `REPL`에 매칭되는 `PreToolUse` 훅을 쓰고 `tool_input.code`에서 JavaScript를 읽는다.
Bash 규칙은 명령 텍스트에 매칭되므로 Code Mode와 무관하게 우회될 수 있고, 텍스트에 의존하지 않는 제한은 샌드박스가 맡는다고 문서가 적는다.

오래 걸리는 코드는 두 가지로 갈린다.

| 방식       | 사용자                             | 시간 제한                        |
| ---------- | ---------------------------------- | -------------------------------- |
| 기다리기   | 코드가 끝난 뒤에 Claude가 답한다   | 10분(권한 창에서 보낸 시간 포함) |
| 백그라운드 | 코드가 도는 동안 Claude와 대화한다 | 최대 2시간                       |

백그라운드 실행은 세션을 auto 또는 `bypassPermissions` 모드로 시작해야 한다.
다른 모드로 바꿨다면 `Shift+Tab`으로 돌아가고, 다른 모드로 시작했거나 `claude --resume` 목록에서 골랐다면 `claude --continue --permission-mode auto`로 Code Mode를 켠 채 다시 시작한다. `--tools`에 도구 이름을 넘겼다면 그 플래그를 빼고 auto 모드로 다시 시작한다.

## 제약

켜기 전에 받아들일 수 있는지 확인할 항목으로 문서가 든 것은 다음과 같다.

- 세션 재개: Code Mode 세션은 터미널에서 Code Mode를 켠 채로만 이어 갈 수 있다. `claude --continue`나 `--resume`에서도 변수를 `1`로 유지해야 하고, 꺼져 있으면 재개를 거부한다. Code Mode 없이 시작한 세션은 변수가 켜져 있어도 Code Mode 없이 재개된다.
- auto 모드: 분류기가 코드를 검토하므로 호출 단위 검토가 없다.
- 오래 걸리는 코드: 백그라운드가 아니면 끝날 때까지 기다리고 10분 뒤에 멈춘다.
- 훅: `PreToolUse` 훅이 실행되지 못하거나 시간이 초과되면 호출이 거부되고, `UserPromptSubmit` 훅이 코드 출력을 막을 수 있다.
- 쓸 수 없는 기능: Remote Control, Claude in Chrome, computer use.
- 세션 이동: Desktop 앱으로 옮기거나 백그라운드 세션으로 바꿀 수 없고 `/fork`로 백그라운드 복사본을 시작할 수 없다.

## 문제 해결

Code Mode가 시작하지 않으면 세션 상단에 `Code Mode (experimental) isn't available`와 이유가 나오고 `/status`에도 보인다. 이유별 조치는 다음과 같다.

| 이유에 포함된 문구                     | 조치                                                                                                                                                  |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 계정에 아직 열리지 않았다              | v2.1.323 미만이면 업데이트하고, 아니면 네트워크를 확인한 뒤 다시 시작한다. 남으면 다른 날 다시 시도한다                                               |
| Anthropic API에서만 동작한다           | 클라우드 공급자, 게이트웨이, 사용자 지정 `ANTHROPIC_BASE_URL` 설정을 제거한다                                                                         |
| API 키 도우미와 안 된다                | `apiKeyHelper`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_CUSTOM_HEADERS`의 `Authorization`과 `X-Api-Key`를 제거하고 로그인하거나 `ANTHROPIC_API_KEY`를 둔다 |
| 지원하지 않는 모델이다                 | 지원 모델로 시작한다(예: `--model opus`)                                                                                                              |
| 백그라운드 작업에서 안 된다            | 포그라운드에서 `--remote-control` 없이 시작한다. 팀원의 분할 창이면 in-process 표시 모드를 쓴다                                                       |
| Anthropic에서 내려받는 설정이 필요하다 | 기능 플래그 내려받기를 끄는 `DISABLE_TELEMETRY` 같은 변수를 해제한다                                                                                  |
| OpenTelemetry가 켜져 있다              | `CLAUDE_CODE_ENABLE_TELEMETRY`와 `ENABLE_BETA_TRACING_DETAILED`를 해제한다                                                                            |
| 플러그인과 아직 안 된다                | `/plugin`에서 이유에 이름이 나온 플러그인을 끈다. 조직이 켠 것이면 관리자에게 끄도록 요청한다                                                         |
| 설치된 모드(mod)와 아직 안 된다        | 도구 호출을 검사하는 모드를 끈다                                                                                                                      |
| 에이전트 팀과 함께 못 쓴다             | v2.1.326 이상으로 업데이트하거나 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`를 해제한다                                                                    |
| 이번 실행의 도구 옵션                  | `--restricted`를 빼고 `--tools`에 `REPL`을 넣고 `--disallowedTools`와 `deny` 규칙에서 `REPL`을 뺀다                                                   |
| 답을 저장하지 못했다                   | `~/.claude.json`을 쓰기 가능하게 한다                                                                                                                 |
| 조직 설정이 허용하지 않는다            | 관리자에게 관리형 설정을 문의한다                                                                                                                     |

이유가 목록에 없으면 요구 사항을 확인한다. Code Mode 줄이 전혀 없으면 버전과 `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE`가 `1`인지 확인하고, 셸과 사용자 설정과 `--settings` 파일에 남은 `0`을 지운다.

세 가지 증상이 따로 설명되어 있다.

- 카운트다운이 있는 권한 창: auto 모드에서 앞선 코드가 도는 중에 Claude가 새 코드를 시작하면 앞선 코드는 분류기 검토를 잃는다. 그러면 앞선 코드의 남은 호출 중 검토가 필요한 것을 사용자에게 묻고, IDE가 연결되어 있지 않으면 카운트다운(예: 1분 59초)이 뜬다. 시간 안에 답하지 않으면 그 호출은 거부되고 이후 같은 창은 묻지 않고 거부된다. 다시 창을 보려면 Claude에게 메시지를 보낸다.
- 훅이 거부한 도구 호출: 오류가 `the hook failed`이면 훅이 시작하지 못했거나 종료되었거나 코드 126, 127, 128 초과로 끝났거나 HTTP 오류나 잘못된 출력을 냈다는 뜻이다. `the hook did not finish`이면 훅이 시간 초과된 것이다. 이때 `timeout`을 늘리고, 실패나 시간 초과에도 진행시키려면 `command`나 `http` 훅에 `"onFailure": "continue"`를 둔다. `command` 훅이 1 같은 일반 종료 코드로 끝나면 `"onFailure": "block"`을 두지 않는 한 호출은 진행된다.
- 훅이 막은 코드 출력: 코드가 백그라운드에서 돌 수 있으면 `UserPromptSubmit`의 `command`, `http`, `mcp_tool` 훅이 코드 출력에도 실행된다. 입력의 `source`가 `poll_event`일 때 막지 않도록 훅을 고친다.

## 비평

### 코드가 보이지 않는 곳에서 권한 판단이 약해진다

대화에는 코드가 아니라 도구 호출이 보이고 코드는 `Ctrl+O`로 열어야 한다.
auto 모드의 분류기는 코드를 한 번 검토하며 실행 중에 계산되는 값은 보지 못한다고 문서가 직접 적는다.
그래서 호출마다 검토하던 때보다 통제가 얇아지는 지점이 있고, 문서는 이를 규칙과 훅으로 보완하라고 안내한다.

### 이득을 보여 주는 수치가 없다

문서는 어떤 작업에서 얼마나 빨라지거나 토큰이 줄어드는지 수치를 주지 않는다.
쓰임도 도구 호출이 많은 작업이라는 범주로만 제시된다.

### 제약이 일상 도구와 겹친다

재개가 터미널과 변수가 켜진 상태에 묶이고, Remote Control, Claude in Chrome, computer use, Desktop 앱, VS Code 패널, `-p`를 쓸 수 없다.
조직 쪽도 HIPAA 구성이나 제로 데이터 보존을 쓰면 못 쓴다.
실험 기능이라는 문서의 선언과 맞물려 현재는 시험용 범위로 읽힌다. 이는 이 문서의 해석이다.

## 인사이트

### 도입은 읽기 전용 작업의 시험에서 시작한다

문서의 예시 프롬프트인 깨진 로컬 링크 찾기는 파일을 읽기만 하고 고치지 않는다.
이런 작업으로 한 세션을 시험하고 `Ctrl+O`로 코드를 읽어 무엇이 실행되었는지 보는 것이 권한 문제를 만나기 전의 안전한 첫 단계이다. 이는 이 문서의 적용이다.

### 훅은 호출 단위와 코드 단위를 따로 설계한다

호출 단위 훅은 `Bash` 같은 평소 이름으로, 코드 단위 훅은 `REPL`과 `tool_input.code`로 건다.
쉘 명령 훅은 `cd 'app' && git push`처럼 합쳐진 형태를 받는다는 점을 가정해 부분마다 검사해야 한다.

### 확인할 관찰

이 기능의 가치를 가르는 관찰은 세 가지이다.
같은 작업에서 켰을 때와 껐을 때의 소요 시간과 토큰,
auto 모드 분류기가 실행 중에 계산된 값 때문에 놓치는 경우의 빈도,
실험 단계를 벗어나 제약 목록이 줄어드는지이다.
