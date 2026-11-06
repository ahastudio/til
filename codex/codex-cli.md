# Codex CLI: 터미널에서 도는 코딩 에이전트와 권한을 정하는 옵션

<https://github.com/openai/codex>

<https://learn.chatgpt.com/docs/codex/cli>

<https://learn.chatgpt.com/docs/developer-commands?surface=cli>

<https://learn.chatgpt.com/docs/agent-approvals-security>

<https://learn.chatgpt.com/docs/changelog>

## 소개

Codex CLI는 OpenAI의 코딩 에이전트이고 사용자의 컴퓨터에서 로컬로 돈다.
저장소 설명은 터미널에서 도는 가벼운 코딩 에이전트라고 한다.
같은 이름 아래 IDE 확장, 데스크톱 앱(`codex app`),
클라우드 에이전트인 Codex Web이 따로 있고 CLI와는 다른 제품이라고 README가
밝힌다.
라이선스는 Apache-2.0이다.

2026년 11월 6일에 읽은 저장소의 최신 릴리스는 `rust-v0.167.0`이고
같은 날 나왔다.
CLI 소개 페이지의 터미널 예시 화면은 `v0.143.0`을 보여 주므로,
페이지마다 가리키는 버전이 다르다.

## 설치와 시작

README가 안내하는 설치 방법은 다음과 같다.

- macOS와 Linux: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`
- Windows: PowerShell에서 `install.ps1`을 받아 실행하는 한 줄 명령(README에 있다)
- npm: `npm install -g @openai/codex`
- Homebrew: `brew install --cask codex`

GitHub Releases에서 바이너리를 받아 이름을 `codex`로 바꿔 쓰는 방법도 있다.
독립 설치 스크립트는 기본으로 `releases.openai.com/codex`에서 받고
GitHub Releases로 대체한다.
시작은 `codex`를 실행해 ChatGPT로 로그인하거나 API 키를 쓰는 것이다.

CLI 참조 페이지는 설정의 기본값을 `~/.codex/config.toml`에서 물려받고,
명령줄의 `-c key=value`는 그 호출에서만 우선한다고 설명한다.

## 권한을 정하는 옵션

에이전트 승인과 보안 페이지는 기본값이 네트워크 접근 꺼짐이라고 한다.
로컬에서는 운영체제가 강제하는 샌드박스가 에이전트가 건드릴 수 있는 범위를
대개 현재 작업 공간으로 제한하고,
승인 정책이 어느 때 멈추고 사용자에게 물을지를 정한다.

CLI 참조 페이지의 전역 옵션 중 이 문서가 전문을 읽은 것은 다섯 개다.

| 옵션                                | 설명                                                                                                            |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `--add-dir <path>`                  | 주 작업 공간 외의 디렉터리에 쓰기 권한을 준다. 여러 번 쓸 수 있다                                               |
| `--approve-for-me`, `--not-so-yolo` | `on-request` 승인과 `workspace-write` 샌드박스로 자동 승인 검토를 쓴다. `--sandbox`, `--yolo`와 함께 쓸 수 없다 |
| `--ask-for-approval`, `-a`          | 명령을 실행하기 전에 사람의 승인을 받는 때를 정한다. 값은 `on-request`와 `never`다                              |
| `--cd`, `-C`                        | 요청을 처리하기 전에 에이전트의 작업 디렉터리를 정한다                                                          |
| `--config`, `-c`                    | 설정값을 덮어쓴다                                                                                               |

`--approve-for-me`에 대해 페이지는 대화형 CLI가 `--ask-for-approval`도 거부한다고
덧붙인다.
이 문서가 읽은 요약에는 `--sandbox`(`-s`)가 `read-only`, `workspace-write`,
`danger-full-access`를 받고,
`--dangerously-bypass-approvals-and-sandbox`(별칭 `--yolo`)가 승인과 샌드박스를
모두 건너뛰며 외부에서 강화된 환경에서만 쓰라는 경고가 붙어 있다고 되어 있다.
이 부분은 전문이 아니라 요약으로만 읽었다.

설정 파일로는 읽기 전용 대화형 사용을 이렇게 둔다고 안내한다.

```toml
sandbox_mode = "read-only"
approval_policy = "on-request"
```

같은 페이지는 `approval_policy = "untrusted"`가 더 이상 지원되지 않으며
이 설정이 남아 있으면 클라이언트가 시작되지 않을 수 있으므로
사용자와 프로젝트 설정, 프로필 파일, 시작 스크립트, 관리 기본값에서 지우라고 한다.

## `--full-auto`가 이 버전에 없다는 보고

이 문서를 쓰게 된 계기는 사용자의 Codex CLI 실행 화면이다.
화면에는 `--full-auto`가 이 버전에 없어서
`--sandbox workspace-write`로 바꿔 실행한다는 메시지가 떴다.

이 문서는 그 말을 확인하지 못했다.
CLI 참조와 승인 페이지에서 읽은 부분에는 `--full-auto`가 나오지 않는다.
그러나 참조 페이지의 `exec` 옵션 표와 두 페이지의 뒷부분은 전문을 읽지 못했으므로,
없다는 것이 제거되었다는 증거는 아니다.
변경 기록에서 읽은 항목에도 이 옵션의 제거나 대체를 적은 곳이 없었고,
변경 기록의 중간 부분은 요약으로만 읽었다.
이 문서를 쓰는 환경에는 `codex`가 설치되어 있지 않아 `codex --help`도 돌려 보지
못했다.

확인된 것은 두 가지다.
화면의 메시지가 바꾼 값 `--sandbox workspace-write`는 위 옵션 설명에 나오는
`workspace-write` 샌드박스와 같은 값이다.
`--approve-for-me`의 설명은 같은 샌드박스에 `on-request` 승인을 묶은 조합을
옵션 하나로 제공한다고 읽힌다.
이 문서의 해석으로는 이 조합이 옛 옵션의 후속일 수 있으나,
이는 설명의 짜맞춤이고 문서가 밝힌 대체 관계가 아니다.

## 비평

### 페이지마다 버전이 달라서 어떤 옵션이 현재인지 가려내기 어렵다

소개 페이지의 예시 화면은 `v0.143.0`이고 저장소의 최신은 `rust-v0.167.0`이다.
공식 주소 `developers.openai.com`은 `learn.chatgpt.com`으로 영구 이동되어 있었다.
문서가 어느 버전의 옵션을 설명하는지 페이지에 적혀 있지 않으면,
설치한 버전에서 옵션이 사라졌다는 경험과 문서를 대조하기 어렵다.
이 문서도 같은 한계를 가진다.

### 샌드박스와 승인은 이름이 비슷해도 서로 다른 축이다

`--sandbox`는 에이전트가 건드릴 수 있는 범위를 정하고,
`--ask-for-approval`은 멈추어 묻는 때를 정한다.
`--approve-for-me`가 둘을 한꺼번에 고정하고 다른 옵션과 충돌한다는 설명은
조합이 한 옵션으로 묶일수록 개별 값을 바꾸기 어려워진다는 점을 보여 준다.
스크립트에서 옵션을 쓰는 사람은 이름이 아니라 세부 값을 고정하는 쪽이 안전하다.

## 인사이트

### 옵션 이름 대신 설정 값으로 권한을 적어 두면 버전이 바뀌어도 덜 흔들린다

옵션 이름은 버전에 따라 사라지고, 설정 값 이름은 비교적 오래 남는다는 것이
이 사례가 보여 주는 가능성이다.
`sandbox_mode`와 `approval_policy`를 설정 파일에 적고 호출에서는 `-c`로 덮어쓰면
옵션이 바뀌어도 의도가 코드에 남는다.
다만 `untrusted` 정책이 지원 종료된 사례처럼 값도 사라질 수 있으므로
이 방식이 안전하다고 보장되지는 않는다.

### 결론을 바꿀 관찰

`codex --help`나 `codex exec --help`의 출력에 `--full-auto`가 없고
대체 옵션이 안내되면 이 문서의 보고가 사실로 확인된다.
변경 기록에 해당 버전과 이유가 적히면 후속 관계를 해석이 아닌 사실로 쓸 수 있다.
