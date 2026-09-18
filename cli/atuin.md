# Atuin: 셸 히스토리를 SQLite 데이터베이스로 바꾸기

<https://atuin.sh/>

<https://github.com/atuinsh/atuin>

HN 토론: <https://news.ycombinator.com/item?id=35839470> (551점, 194개 댓글)

GN 토론: <https://news.hada.io/topic?id=4276>

## 소개

Atuin은 기존 셸 히스토리를 SQLite 데이터베이스로 대체하고, 명령마다 부가 맥락을 함께 기록하는 Rust 도구다.
선택적으로 기기 간 히스토리 동기화를 제공하며, 그 동기화는 종단 간 암호화된다.

전통적인 `~/.zsh_history`가 저장하는 것은 명령 문자열과 (설정에 따라) 타임스탬프뿐이다.
Atuin이 추가로 기록하는 것은 다음과 같다.

| 기록 항목 | 설명                         |
| --------- | ---------------------------- |
| 명령      | 실행한 명령 문자열           |
| 디렉터리  | 명령을 실행한 작업 디렉터리  |
| 시각      | 실행 시각과 소요 시간        |
| 종료 코드 | 명령의 exit code             |
| 호스트    | 기기의 호스트명과 사용자     |
| 세션      | 명령을 실행한 셸 세션 식별자 |

이 부가 맥락이 검색 조건이 된다.
예를 들어 어제 오후 3시 이후에 성공한 `make` 명령만 찾는 질의는 이렇게 쓴다.

```bash
atuin search --exit 0 --after "yesterday 3pm" make
```

지원 셸은 zsh, bash, fish, nushell, xonsh, PowerShell이다.
동기화 서버는 공식 호스팅 서버를 쓰거나, 직접 운영하거나, 아예 쓰지 않을 수 있다.

계약의 경계가 분명하다.
Atuin은 기존 히스토리 파일을 지우거나 대체하지 않는다. 셸의 원래 히스토리 파일은 Atuin 사용 여부와 무관하게 계속 갱신된다.
그리고 업데이트 확인을 끄고 동기화를 설정하지 않으면 Atuin은 스스로 어떤 네트워크 요청도 하지 않는다.

## 동작 방식

Atuin은 셸 훅으로 히스토리를 수집한다. 셸 설정에 `eval "$(atuin init <shell>)"`를 넣으면 명령 수명 주기의 두 지점에 훅이 설치된다.

| 훅      | 시점           | 기록하는 것                            |
| ------- | -------------- | -------------------------------------- |
| preexec | 명령 실행 직전 | 명령 문자열, 타임스탬프, 작업 디렉터리 |
| precmd  | 명령 완료 직후 | 종료 코드, 소요 시간                   |

이 구조를 이해하면 Atuin이 기록하지 않는 경우를 예측할 수 있다.
훅이 설치되려면 셸이 대화형이어야 하고, 셸 설정 파일이 source되어야 하며, 그 안에서 `atuin init`이 실행되어야 한다.
셋 중 하나라도 어긋나면 훅이 설치되지 않고, 명령은 아무것도 기록되지 않는다.

이것이 IDE 내장 터미널이나 컨테이너, AI 코딩 도구가 띄운 셸에서 Atuin이 조용히 동작하지 않는 이유다.
그런 환경은 셸을 평소와 다른 방식으로 띄우기 때문이다.

초기화 시 설정되는 환경 변수도 동작을 설명한다.

| 변수                        | 용도                                                                    |
| --------------------------- | ----------------------------------------------------------------------- |
| `ATUIN_SESSION`             | 이 셸 세션의 고유 식별자                                                |
| `ATUIN_SHLVL`               | 셸 중첩 수준 추적                                                       |
| `ATUIN_HISTORY_ID`          | 현재 실행 중인 명령의 임시 ID                                           |
| `ATUIN_HISTORY_AUTHOR`      | 명령 작성자 식별자. 알려진 에이전트 이름이면 에이전트 실행으로 표시된다 |
| `ATUIN_HISTORY_AUTHOR_KIND` | `user` 또는 `agent`. 이름에서 추론한 분류를 덮어쓴다                    |
| `ATUIN_HISTORY_INTENT`      | 명령의 의도나 근거 텍스트                                               |

`ATUIN_HISTORY_AUTHOR`가 설정되지 않으면 로컬 셸 사용자명이 기본값이 된다.
이 변수들이 최근 추가된 이유는 명확하다. AI 에이전트가 실행한 명령과 사람이 친 명령을 구분해야 하기 때문이다.
Atuin은 에이전트가 실행한 항목에 태그를 달고 대화형 검색에서 기본적으로 감춘다.

## 검색 방식 두 축

검색 동작은 서로 직교하는 두 설정이 결정한다.
필터 모드가 어떤 명령을 대상으로 삼을지를 정하고, 검색 모드가 질의를 어떻게 대조할지를 정한다.

필터 모드는 TUI 안에서 `ctrl-r`을 눌러 순환한다.

| 모드              | 검색 범위                                  |
| ----------------- | ------------------------------------------ |
| `global` (기본)   | 모든 기기의 전체 히스토리                  |
| `host`            | 이 기기의 히스토리만                       |
| `session`         | 현재 셸 세션만                             |
| `directory`       | 현재 디렉터리에서 실행한 것만              |
| `workspace`       | 현재 git 저장소 어디에서든 실행한 것       |
| `session-preload` | 현재 세션 + 세션 시작 이전의 전체 히스토리 |

`workspace` 모드는 `workspaces = true` 설정이 필요하고, git 저장소 안이 아니면 건너뛴다.

검색 모드는 TUI 안에서 `ctrl-s`로 순환한다.

| 모드           | 대조 방식                                     |
| -------------- | --------------------------------------------- |
| `fuzzy` (기본) | fzf 문법을 따르는 퍼지 매칭                   |
| `prefix`       | 질의로 시작하는 명령                          |
| `fulltext`     | 질의를 어디든 포함하는 명령                   |
| `daemon-fuzzy` | 데몬의 인메모리 인덱스로 서비스하는 퍼지 매칭 |

`daemon-fuzzy`는 18.13에서 추가되었고 점수 계산을 조정할 수 있다.

두 축이 나뉘어 있다는 점이 설계의 핵심이다.
무엇을 찾을지와 어떻게 찾을지는 다른 질문이고, 실무에서 바뀌는 빈도도 다르다.
디렉터리 범위로 좁히는 일은 자주 하지만 검색 알고리즘을 바꾸는 일은 드물다.

## 설정하기

설정 파일 두 개가 `~/.config/atuin/`에 있고, 데이터는 `~/.local/share/atuin`에 저장된다.
`XDG_*`로 재정의할 수 있고, 설정 위치는 `ATUIN_CONFIG_DIR`로 바꾼다.

설치와 초기 설정은 이렇다.

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh

atuin register -u <USERNAME> -e <EMAIL>   # 동기화를 쓸 때만
atuin import auto                          # 기존 셸 히스토리 가져오기
atuin sync
```

`atuin import auto`는 현재 셸의 히스토리를 가져오고, `atuin import zsh`처럼 셸을 명시할 수도 있다.
가져오기 후에도 원래 히스토리 파일은 계속 갱신되므로, 되돌릴 길이 남아 있다.

자주 바꾸는 설정은 `~/.config/atuin/config.toml`에 쓴다.

```toml
# 엔터로 바로 실행하지 않고 편집을 위해 삽입만 한다
enter_accept = false

# 전체 화면 TUI가 부담스러우면 높이를 제한하고 조밀한 스타일을 쓴다
inline_height = 40
style = "compact"

# 위쪽 화살표는 현재 디렉터리만, ctrl-r은 전역을 검색한다
filter_mode_shell_up_key_binding = "directory"

[tmux]
enabled = true   # 검색 UI를 현재 페인 위 팝업으로 띄운다
```

키 바인딩을 바꾸는 코드는 반드시 셸 시작 파일(`~/.bashrc`, `~/.zshrc`, `~/.config/fish/config.fish`)에 넣어야 한다.
`atuin init`을 실행하는 바로 그 파일이다.
대화형 세션에서 한 번 실행하거나 셸이 source하지 않는 파일에 넣으면 아무 효과가 없다.

기본 바인딩이 마음에 들지 않으면 개별로 끈다.

```bash
# ctrl-r만 바인딩하고 위쪽 화살표는 두지 않는다
eval "$(atuin init zsh --disable-up-arrow)"

# 아무 키도 바인딩하지 않고 직접 붙인다
export ATUIN_NOBIND="true"
eval "$(atuin init zsh)"
```

macOS에는 Alt 키가 없어서 `Alt-0`부터 `Alt-9`까지의 빠른 점프 단축키가 문제가 된다.
Option을 Alt로 매핑할 수 있지만 영국식 배열에서 `Option + 3`으로 `#`를 치는 것 같은 입력이 막힌다.
그럴 때는 `ctrl_n_shortcuts = true`로 바꾼다.

## 기록에서 제외하기

Atuin은 명령을 히스토리에서 빼는 방법을 네 가지 준다.

가장 빠른 것은 공백으로 시작하는 것이다. 대부분의 셸이 지원하는 `ignorespace` 관례를 Atuin도 따른다.

```bash
 echo "이 명령은 저장되지 않는다"
```

지속적인 제외는 정규식 필터로 한다.

```toml
history_filter = [
  "^ls$",        # 인자 없는 ls만 제외하고 'ls -la'는 남긴다
  "^cd ",        # cd 명령 전부 제외
  "--password",  # 비밀번호 플래그가 들어간 것 전부 제외
]

cwd_filter = [
  "^/tmp",               # /tmp에서 실행한 것 전부
  "/node_modules/",      # 어떤 node_modules 안에서든
  "^/home/user/scratch", # 임시 작업 디렉터리
]
```

두 패턴 모두 앵커가 없다. `secret`이라고 쓰면 명령 어디에 나타나든 매칭된다.
명령 전체와 정확히 맞추려면 `^`와 `$`를 직접 붙여야 한다.

특정 도구가 띄우는 셸에서 아예 기록하지 않으려면 `atuin init` 호출 자체를 감싼다.

```bash
# .bashrc 또는 .zshrc
if [[ -z "${MY_TOOL_SESSION}" ]]; then
  eval "$(atuin init bash)"
fi
```

그리고 도구가 셸을 띄울 때 `MY_TOOL_SESSION=1`을 설정하게 한다.

필터는 앞으로 기록될 것에만 적용된다는 점이 중요하다.
필터를 추가하기 전에 이미 쌓인 항목은 따로 지워야 한다.

```bash
atuin history prune --dry-run  # 무엇이 지워질지 먼저 본다
atuin history prune            # 실제로 지운다
```

이 명령은 현재의 `history_filter`와 `cwd_filter`에 매칭되는 기존 항목을 지운다.

## 동기화와 암호화

등록하면 Atuin이 암호화 키를 생성해 로컬에 저장한다. `atuin key`로 볼 수 있다.

이 키가 전체 모델의 중심이다.
서버는 암호화된 덩어리만 받으므로 히스토리 내용을 볼 수 없고, 그 대가로 키를 잃으면 복구할 방법이 없다.
개발자도 도와줄 수 없다고 문서가 명시한다.

새 기기에서는 사용자명, 비밀번호, 그리고 키로 로그인한다.

```bash
atuin login -u <USERNAME>
atuin sync      # 수동 동기화
atuin sync -f   # 전체 동기화. 누락이 보일 때 쓴다
```

`atuin sync`는 전송량을 아끼려고 증분으로 움직인다.
데이터가 빠진 것 같으면 `-f`로 전체 동기화를 돌리는데, 과거 데이터를 전부 훑으므로 시간이 더 걸린다.

동기화가 켜져 있으면 셸 별칭과 환경 변수도 함께 백업된다.

```toml
[dotfiles]
enabled = true
```

```bash
atuin dotfiles alias set k 'kubectl'
atuin dotfiles alias set ll 'ls -lah'
atuin dotfiles var set FOO 'bar'
atuin dotfiles var set -n foo 'bar'   # export하지 않는 셸 변수
atuin dotfiles alias list
```

별칭이나 변수를 만들거나 지운 뒤에는 셸을 다시 시작해야 반영된다.

## 서버 직접 운영하기

서버는 `atuin-server`라는 별개 바이너리로 배포되며, 릴리스마다 미리 빌드된 바이너리가 올라온다.

```bash
curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/atuinsh/atuin/releases/latest/download/atuin-server-installer.sh | sh
atuin-server start
```

서버 설정은 클라이언트와 분리된 `~/.config/atuin/server.toml`에 있다.

```toml
host = "0.0.0.0"
port = 8888
open_registration = true
db_uri = "postgres://user:password@hostname/database"
```

환경 변수로도 같은 값을 줄 수 있다. `ATUIN_HOST`, `ATUIN_PORT`, `ATUIN_OPEN_REGISTRATION`, `ATUIN_DB_URI`다.

| 설정                | 설명                               | 기본값     |
| ------------------- | ---------------------------------- | ---------- |
| `db_uri`            | 히스토리를 저장할 데이터베이스 URI | 없음(필수) |
| `host`              | 수신할 호스트                      | 127.0.0.1  |
| `port`              | 수신할 TCP 포트                    | 8888       |
| `open_registration` | 새 사용자 등록 허용 여부           | false      |
| `path`              | 모든 라우트 앞에 붙일 경로         | 없음       |

데이터베이스는 PostgreSQL, SQLite, MySQL을 지원한다.
다만 MySQL은 2티어로 분류되어, 지원은 하지만 이슈 우선순위가 PostgreSQL과 SQLite보다 낮다.
SQLite를 쓰면 파일이 없을 때 Atuin이 만들어 준다.

클라이언트에서는 `sync_address`를 자기 서버로 바꿔야 한다. 등록보다 먼저 해야 하는 순서다.

```toml
sync_address = "https://atuin.example.com"
```

## 값 정하기

| 설정                               | 시작값       | 근거                                                                        |
| ---------------------------------- | ------------ | --------------------------------------------------------------------------- |
| `sync_frequency`                   | `5m`         | 기본값. `0`이면 명령마다 동기화하며, 일부 서버는 속도를 제한할 수 있다      |
| `search_mode`                      | `fuzzy`      | fzf 문법이라 이미 몸에 익어 있다. 정확한 접두어 검색이 필요할 때만 `prefix` |
| `filter_mode`                      | `global`     | 전역이 기본. 프로젝트 단위 작업이 많으면 `workspace`가 더 맞는다            |
| `filter_mode_shell_up_key_binding` | `directory`  | 위쪽 화살표는 원래 “여기서 방금 뭐 했더라”를 묻는 키다                      |
| `enter_accept`                     | `false`      | 바로 실행하는 기본값은 잘못 고른 명령을 되돌릴 틈을 주지 않는다             |
| `inline_height`                    | `40`         | 전체 화면 전환은 앞뒤 맥락을 가린다. 화면 일부만 쓰면 위 출력이 남는다      |
| `store_failed`                     | `true`(기본) | 실패한 명령이야말로 다시 찾게 되는 명령이다                                 |
| `secrets_filter`                   | `true`(기본) | 끄지 않는다. 자격 증명이 평문으로 DB에 들어가는 것을 막는 마지막 방어선이다 |
| `update_check`                     | 취향         | 끄면 동기화 없이 쓸 때 네트워크 요청이 완전히 사라진다                      |

값을 바꾼 뒤 재평가할 근거는 `atuin stats`에서 나온다.

```bash
atuin stats today
atuin stats week
atuin stats last friday    # 그 시점부터 24시간
atuin stats                # 전체 히스토리
```

가장 많이 쓴 명령, 실행한 명령 수, 고유 명령 수를 보여 준다.
`ls`나 `cd`가 상위권을 차지한다면 `history_filter`에 넣을 후보다.
날짜 해석은 `dialect` 설정을 따르므로, 한국에서 쓴다면 `dialect = "uk"`가 일(日)/월(月) 순서에 더 가깝다.

## 트레이드오프

### 상시 켜진 인덱스는 마찰을 줄이기도 늘리기도 한다

Atuin이 파는 가치는 `ctrl-r`이 순차 탐색이 아니라 질의가 된다는 것이다.
그런데 그 대가로 모든 `ctrl-r`과 모든 위쪽 화살표가 전체 화면 TUI로 바뀐다.

HN에서 Dowwie는 이 지점에서 손을 뗐다. Atuin이 원래 없던 마찰을 만들었고, 그래서 다시 `.zsh_history`를 ripgrep으로 훑는 쪽으로 돌아갔다고 적었다.[^Dowwie]
notresidenter도 히스토리를 한 칸 올라가는 데 클릭이 하나 더 필요했고 설정으로 그 동작을 바꾸기 쉽지 않았다고 했다. 다만 이후 그 동작을 끌 수 있게 되었고 문서도 훨씬 나아졌다고 덧붙였다.[^notresidenter]

이것이 설정으로 완전히 해소되지는 않는다는 점이 중요하다.
`--disable-up-arrow`로 위쪽 화살표를 원래대로 두면 마찰은 사라지지만, Atuin의 맥락 인식 검색을 가장 자주 쓰게 될 자리를 포기하는 것이다.
`inline_height`로 화면 점유를 줄이는 쪽이 더 나은 타협이지만, 그래도 모달 UI가 뜨는 것 자체는 남는다.

바꿔 말하면 여기서 고르는 것은 기능이 아니라 근육 기억이다.
두 손가락으로 위쪽 화살표를 세 번 치는 동작과, 검색창을 띄우고 단어를 치는 동작은 비용 구조가 다르다.
짧은 명령을 방금 반복하는 경우에는 전자가 항상 싸고, 사흘 전 긴 명령을 찾는 경우에는 후자가 비교할 수 없이 싸다.
Atuin은 후자에 맞춰 설계되었고, 전자의 비중이 큰 사람에게는 손해다.

### 데이터를 넣기는 쉽고 빼기는 어렵다

`atuin import auto`는 기존 히스토리를 한 줄로 가져온다.
반대 방향은 그만큼 매끄럽지 않다.

maleldil은 히스토리를 셸이 다시 읽을 수 있는 형식으로 내보내는 방법이 없어 보인다고 지적했다.
시도해 본다면 자기 명령들이 거기 갇히게 된다는 것이다.[^maleldil]

이 우려는 과장과 사실 사이에 있다.
저장소가 SQLite 파일이고 스키마가 공개되어 있으므로 데이터가 잠기는 것은 아니다. 필요하면 `sqlite3`로 직접 뽑아 셸 히스토리 형식으로 바꿀 수 있다.
그러나 그 작업을 직접 해야 한다는 사실 자체가 전환 비용이며, 도구를 평가하는 시점에는 그 비용이 얼마인지 알 수 없다.

원래 히스토리 파일이 계속 갱신된다는 설계가 이 위험을 크게 줄인다.
Atuin을 쓰는 동안에도 셸의 원본 히스토리는 그대로 쌓이므로, 그만두더라도 잃는 것은 Atuin이 추가로 기록한 맥락뿐이다.
이 설계를 알고 시작하는 것과 모르고 시작하는 것의 차이가 크다.

### 동기화의 가치는 작업 방식에 따라 갈린다

earthboundkid는 동기화가 왜 필요한지 물었다.
기기마다 파일 배치가 다르고 설치된 실행 파일도 다르므로, 공통되는 명령은 우연이거나 실제 원격 관리 시스템으로 다루는 편이 나은 플릿 작업이라는 것이다.[^earthboundkid]

이 비판은 특정 작업 방식에서 정확하다.
개인 노트북과 프로덕션 서버의 히스토리를 섞는 것은 이득보다 소음이 크고, 후자는 애초에 Ansible 같은 도구로 다뤄야 한다.

그런데 Atuin의 필터 모드가 바로 그 소음을 겨냥한다.
`host` 모드로 이 기기만, `directory`나 `workspace`로 이 프로젝트만 좁힐 수 있으므로, 전역 히스토리는 필요할 때만 꺼내는 자원이 된다.
그리고 노트북과 데스크톱처럼 환경이 비슷한 기기 사이에서는 동기화의 값이 분명하다.

동기화를 끄고 로컬 SQLite 인덱스만 쓰는 선택도 온전히 지원된다는 점을 기억할 필요가 있다.
Atuin의 두 가치 제안 — 맥락 있는 검색과 기기 간 동기화 — 는 분리되어 있고, 앞의 것만 취해도 도구의 대부분을 쓰는 것이다.

### 종단 간 암호화는 서버를 안전하게 만들고 사용자를 취약하게 만든다

서버가 평문을 볼 수 없다는 것은 셸 히스토리처럼 민감한 데이터에 대해 타협할 수 없는 요건에 가깝다.
셸 히스토리에는 경로, 호스트명, 내부 서비스 이름, 때로는 자격 증명 조각이 들어 있다.

그 대가가 키 관리다. 키를 잃으면 데이터도 잃는다.
문서가 비밀번호 관리자 같은 안전한 곳에 보관하라고 권하지만, 이것은 해법이 아니라 책임의 이전이다.

그리고 여기서 `secrets_filter`가 왜 기본값이 `true`인지가 설명된다.
암호화가 전송과 저장을 지키더라도, 로컬 SQLite 파일 자체는 평문이다.
백업 도구나 다른 프로세스가 홈 디렉터리를 읽으면 그 파일도 읽는다. 자격 증명이 애초에 들어가지 않게 막는 것이 유일하게 확실한 방어다.

## 함정

기록되지 않는 환경이 있다.
IDE 내장 터미널, 컨테이너, AI 코딩 도구가 띄우는 셸은 셸을 평소와 다르게 띄우므로 훅이 설치되지 않을 수 있다.
“왜 이 명령이 안 남았지”를 디버깅하기 전에 그 셸에서 `echo $ATUIN_SESSION`을 먼저 확인하는 편이 빠르다.

bash는 조건이 하나 더 있다.
설치 스크립트가 넣는 `bash-preexec`에 알려진 한계가 있고, 그중 하나는 `ignorespace`가 온전히 지켜지지 않는다는 것이다.
공백으로 시작한 명령이 Atuin에는 안 들어가지만 bash 히스토리에는 남을 수 있다.

필터는 소급 적용되지 않는다.
`history_filter`를 추가한 순간부터가 아니라 그 이전에 쌓인 것까지 지우려면 `atuin history prune`을 따로 돌려야 한다.

멀티플렉서와 다중 탭에서의 기대치를 정해 두어야 한다.
IanCal과 Waterluvian이 각각 물은 것이 같은 문제다. 여러 터미널 탭이나 페인을 띄우면 히스토리가 일관되지 않거나 서로 안 보인다는 것이다.[^IanCal][^Waterluvian]
Atuin의 답은 전역 저장소와 필터 모드다. 모든 세션의 명령이 하나의 DB에 시간순으로 들어가고, 세션별로 보고 싶을 때 `session` 모드로 좁힌다.
셸이 종료할 때 히스토리 파일을 덮어쓰는 전통적 모델과 근본적으로 다른 지점이다.

ssh로 접속한 원격 호스트의 명령은 기록되지 않는다.
sureglymop이 지적한 대로, 하루에 원격 호스트 다섯 곳을 오간다면 명령 대부분이 로컬에서 실행된 것이 아니므로 로컬 히스토리에 남지 않는다.[^sureglymop]
원격 호스트에도 Atuin을 설치하고 같은 계정으로 동기화하는 것이 현재의 답이고, 그러면 `host` 필터로 어느 기기에서 실행했는지가 구분된다.

`enter_accept`의 기본값이 즉시 실행이라는 점을 인지해야 한다.
퍼지 검색으로 좁힌 목록에서 엔터를 치면 편집 기회 없이 그대로 돌아간다. 파괴적인 명령이 히스토리에 있다면 이 기본값은 위험하다.

자기 서버를 쓸 계획이라면 `sync_address`를 등록보다 먼저 설정해야 한다.
순서가 바뀌면 공식 서버에 계정이 만들어진다.

## 확인하기

설치 후 실제로 기록되고 있는지 확인하는 최소 절차다.

```bash
# 1. 훅이 붙었는지 확인한다. 값이 비어 있으면 init이 실행되지 않은 것이다
echo $ATUIN_SESSION

# 2. 표시용 명령을 하나 실행하고 즉시 검색한다
echo atuin-smoke-test
atuin search atuin-smoke-test

# 3. 부가 맥락이 실제로 붙었는지 본다
atuin search --exit 0 --after "1 hour ago" atuin-smoke-test

# 4. 제외 규칙이 먹는지 본다. history_filter에 '^atuin-excluded' 를 넣은 뒤
atuin-excluded-command 2>/dev/null
atuin search atuin-excluded   # 결과가 없어야 정상이다

# 5. 데이터가 어디에 얼마나 쌓였는지 본다
ls -lh ~/.local/share/atuin/history.db
atuin stats today
```

동기화를 설정했다면 두 번째 기기에서 `atuin sync -f`를 돌린 뒤 1번 명령을 검색해 본다.
찾아지면 등록, 키, 서버 주소가 모두 맞는 것이다.

## 체크리스트

- `atuin init`을 셸 시작 파일에 넣었고, 그 파일이 실제로 source되는가
- 새 셸에서 `echo $ATUIN_SESSION`이 값을 출력하는가
- `atuin import auto`로 기존 히스토리를 가져왔는가
- `secrets_filter`를 끄지 않았는가
- `history_filter`와 `cwd_filter`를 정의했고, 정의한 뒤 `atuin history prune`을 한 번 돌렸는가
- `enter_accept`의 기본 동작이 즉시 실행이라는 것을 알고 있으며, 그대로 둘지 결정했는가
- 동기화를 쓴다면 `atuin key`의 값을 비밀번호 관리자에 넣었는가
- 자기 서버를 쓴다면 등록 전에 `sync_address`를 바꿨는가
- 자기 서버의 데이터베이스가 PostgreSQL 또는 SQLite인가(MySQL은 2티어)
- 자기 서버에 TLS를 붙였는가
- 원격 호스트의 히스토리가 필요하다면 그곳에도 설치했는가

## 비평

### 검색을 잘하게 만들었지만 무엇을 저장할지는 사용자에게 떠넘긴다

mrAssHat이 지적한 문제가 이 도구 범주 전체를 관통한다.
오래 두고 싶은 명령과 `cd`, `ls`, `cat` 같은 며칠 안에 지워도 좋은 쓰레기를 어떻게 구분할 것인가를 아무도 다루지 않는다는 것이다.[^mrAssHat]

Atuin의 답은 `history_filter` 정규식이다. 이것은 부분적인 답이다.
정규식은 형태를 거르지 실제 가치를 거르지 못한다. `^ls$`를 거르면 인자 없는 `ls`가 사라지지만, 한 번 쓰고 다시는 안 쓸 긴 `docker run` 한 줄은 그대로 남는다.

그리고 Atuin은 이 문제를 풀 재료를 이미 갖고 있다. 실행 횟수, 종료 코드, 소요 시간, 재실행 간격이 전부 DB에 있다.
자주 반복되면서 짧은 명령은 검색 대상으로서 가치가 낮고, 한 번 성공하고 오래 뒤에 다시 찾는 긴 명령이야말로 이 도구가 존재하는 이유다.
그 구분을 자동으로 학습할 수 있는 데이터가 있는데도, 사용자가 손으로 정규식을 관리하게 두는 것은 설계의 미완성이다.

agumonkey가 같은 방향을 다르게 짚었다.
히스토리를 파서나 LLM에 넣어 가장 자주 쓰는 관용구를 뽑아낼 수 있지 않겠느냐는 것이다. `ls | grep | less` 같은 형태를 인자와 분리해 파악하는 것이다.[^agumonkey]
이 제안이 흥미로운 이유는 검색과 다른 문제를 가리키기 때문이다. 찾기가 아니라 요약이고, 개별 명령이 아니라 패턴이다.

### 로컬 SQLite와 동기화 서비스는 다른 제품인데 하나로 묶여 있다

Atuin이 파는 것은 사실 두 가지다.
맥락 있는 로컬 히스토리 인덱스와, 종단 간 암호화된 기기 간 동기화 서비스다.

기술적으로는 분리되어 있다. 동기화를 켜지 않아도 완전히 동작하고, 문서도 오프라인 설정을 안내한다.
그런데 README의 빠른 시작이 먼저 보여 주는 것은 `atuin register`이고, 공식 서버 가입이 기본 경로로 제시된다.

이것이 프로젝트의 지속 가능성 문제와 직결되어 있어서 비난하기는 어렵다.
개발자는 전업으로 이 프로젝트를 하고 있고, 호스팅 서비스가 그 재원이다.

문제는 평가하는 사람이 두 결정을 한꺼번에 내리게 된다는 점이다.
로컬 인덱스는 순전히 로컬 도구이고 되돌리기 쉬운 선택이지만, 계정 등록과 암호화 키 관리는 다른 종류의 약속이다.
둘을 나눠 제시했다면 훨씬 많은 사람이 앞의 것만 먼저 시도했을 것이다.

xguru가 2021년 GN에 남긴 관찰도 초기의 같은 문제를 다른 각도에서 짚는다. BashHub 쪽 검색 UI가 조금 더 편해 보인다는 것이다.[^xguru]
Atuin이 지금 갖춘 필터 모드와 검색 모드의 조합은 그때보다 훨씬 강력해졌지만, 그 강력함이 첫 화면에서 드러나지 않는다는 성질은 남아 있다.

### 경쟁 도구가 여럿인데 선택 기준이 문서에 없다

HN 스레드에서만 대안이 네 개 나왔다.
IshKebab은 McFly를 썼고 훌륭하다고 하면서, 기본 검색 모드가 SQL 문자열이라 와일드카드에 `%`를 써야 하는 점이 유일한 불만이라고 했다. 둘 다 써 본 사람의 비교를 구했다.[^IshKebab]
user-와 v3ss0n은 RESH를 들었고, 후자는 SQLite가 필요 없어 더 단순하고 요점에 충실하다고 평했다.[^user-][^v3ss0n]
oftenwrong은 몇 년째 `zsh-histdb`를 쓰고 있다고 적었다.[^oftenwrong]
outcoldman은 2017년부터 자기 SQLite 히스토리를 써 왔고 10만 건 넘는 항목에 DB가 0.5GB 가까이 되었다면서, 터미널에서 오래 일하는 사람이라면 Atuin이든 비슷한 도구든 반드시 쓰라고 권했다.[^outcoldman]

이 목록이 알려 주는 것은 SQLite 기반 셸 히스토리가 이미 여러 번 독립적으로 발명된 아이디어라는 사실이다.
그렇다면 Atuin이 답해야 할 질문은 왜 SQLite인가가 아니라 왜 다른 SQLite 히스토리가 아니라 이것인가다.

실제 답은 있다. 종단 간 암호화 동기화, 여섯 개 셸 지원, 필터 모드와 검색 모드의 직교 설계, 그리고 에이전트 실행 명령 태깅이다.
그런데 문서 어디에도 그 비교가 없다.
0.5GB DB를 이미 굴리고 있는 사람에게 Atuin으로 옮길 이유를 설명하는 문단이 없고, 그것이 그대로 HN 스레드의 반복되는 질문으로 나타난다.

## 기억할 원칙

### 셸 히스토리는 기록이 아니라 인덱스다

전통적인 히스토리 파일이 하는 일은 기록이다. 명령을 순서대로 적고, 일정 개수가 넘으면 앞에서부터 버린다.
그래서 `ctrl-r`이 하는 일도 선형 탐색이고, 찾는 방식은 “언제쯤이었더라”를 거슬러 올라가는 것이다.

Atuin이 바꾼 전제는 히스토리가 인덱스라는 것이다.
인덱스에는 질의가 있고, 질의에는 조건이 있고, 조건은 기록된 속성 위에서만 성립한다.
그래서 종료 코드와 작업 디렉터리와 소요 시간을 기록하는 것이 부가 기능이 아니라 설계의 전부다. 그것들이 없으면 질의할 것이 없다.

이 관점의 전환이 주는 실무적 함의는 명확하다.
어떤 도구를 검색 가능하게 만들고 싶다면, 검색 UI를 붙이기 전에 무엇을 조건으로 쓸지를 먼저 정하고 그것을 기록하기 시작해야 한다.
데이터가 없으면 아무리 좋은 검색도 문자열 매칭에 머문다.

didip이 던진 질문이 이 원칙의 다른 표현이다. 왜 리눅스 도구들이 SQLite를 전면적으로 받아들이지 않았느냐는 것이다.[^didip]
tonymet도 같은 방향을 가리켰다. 셸 명령, 설정 파일, 코드 파일 모두 색인되어야 하며, 윈도우나 맥과 비교해 리눅스에 CLI와 GUI 전문 색인이 없는 것이 실질적인 후퇴라는 것이다.[^tonymet]
`apropos`와 `locatedb`와 Atuin이 각각 자기 영역에서 그 일을 하고 있지만, 전부 개별 해법이다.

### 기록의 가치는 맥락에서 나온다

명령 문자열만 보면 `make -j8`은 그냥 `make -j8`이다.
그것이 어느 프로젝트 디렉터리에서, 성공했는지 실패했는지, 4초 걸렸는지 40분 걸렸는지를 함께 알면 완전히 다른 정보가 된다.

ranting-moth가 자기가 찾던 기능이라고 콕 집은 것도 바로 그 한 줄이었다. 종료 코드, 작업 디렉터리, 호스트명, 세션, 소요 시간을 남긴다는 부분이다.[^ranting-moth]
명령 자체는 이미 갖고 있었고, 없던 것은 그 명령이 놓였던 자리였다.

이 원칙은 셸 히스토리 바깥으로 그대로 옮겨진다.
로그를 남길 때 메시지만 남기면 나중에 grep밖에 못 하고, 요청 ID와 소요 시간과 결과 코드를 함께 남기면 질의할 수 있다.
비용은 기록 시점에 지불되고 이득은 조회 시점에 돌아오므로, 기록하는 쪽은 언제나 그 비용이 아깝게 느껴진다.
그 비대칭을 알고 미리 기록해 두는 것이 이 도구가 가르치는 실천이다.

cjbprime이 한 걸음 더 나간 제안을 남겼다. 이왕 데이터베이스를 세운다면 stdout과 stderr도 테이블에 저장하는 프로젝트가 있는지 물었다.[^cjbprime]
출력으로 명령을 찾을 수 있고, 작업 전체에 대한 대화가 가능해진다는 것이다.
맥락을 어디까지 남길 것인가에 정답이 없다는 점, 그리고 남긴 만큼 질의할 수 있다는 점이 이 원칙의 양면이다.

---

[^Dowwie]: <https://news.ycombinator.com/item?id=35841027>

[^notresidenter]: <https://news.ycombinator.com/item?id=35841948>

[^maleldil]: <https://news.ycombinator.com/item?id=35842303>

[^earthboundkid]: <https://news.ycombinator.com/item?id=35847085>

[^IanCal]: <https://news.ycombinator.com/item?id=35839921>

[^Waterluvian]: <https://news.ycombinator.com/item?id=35846438>

[^sureglymop]: <https://news.ycombinator.com/item?id=35841374>

[^mrAssHat]: <https://news.ycombinator.com/item?id=35840540>

[^agumonkey]: <https://news.ycombinator.com/item?id=35842425>

[^IshKebab]: <https://news.ycombinator.com/item?id=35840629>

[^user-]: <https://news.ycombinator.com/item?id=35841475>

[^v3ss0n]: <https://news.ycombinator.com/item?id=35845056>

[^oftenwrong]: <https://news.ycombinator.com/item?id=35841252>

[^outcoldman]: <https://news.ycombinator.com/item?id=35840944>

[^didip]: <https://news.ycombinator.com/item?id=35844840>

[^tonymet]: <https://news.ycombinator.com/item?id=35842596>

[^ranting-moth]: <https://news.ycombinator.com/item?id=35839895>

[^cjbprime]: <https://news.ycombinator.com/item?id=35845363>

[^xguru]: <https://news.hada.io/topic?id=4276#cid5211>
