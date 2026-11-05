# Claude Code 클라우드 환경은 네트워크 접근, 환경 변수, 시크릿, 설정 스크립트를 세션 밖에서 정한다

원문: [Configure cloud environments - Claude Code Docs](https://code.claude.com/docs/en/cloud-environments)

HN 토론: <https://news.ycombinator.com/item?id=50351334> (1점, 2개 댓글)

## 소개

Anthropic의 Claude Code 문서 중 클라우드 세션(cloud session)이 실행되는
환경(environment)을 설정하는 페이지입니다.
환경에서 정하는 것은 네트워크 접근 수준, 환경 변수,
세션이 값을 보지 못한 채 쓰는 네트워크 시크릿(network secrets),
Claude가 일하기 전에 도는 설정 스크립트(setup script)입니다.
같은 환경이 데스크톱 앱, 모바일 앱, `claude.ai/code`, 터미널의 `claude --cloud`,
클라우드 예약 작업, Claude Tag에서 모두 쓰입니다.
문서는 이 환경들이 자체 호스팅 환경(self-hosted environment)으로도 연결될 수
있다고 밝힙니다.
Remote Control 세션은 내 컴퓨터의 네트워크와 파일을 쓰므로 클라우드 환경을 쓰지
않습니다.

클라우드 세션은 Pro, Max, Ultra, Team 요금제와 Enterprise의 일부 좌석에서 쓸 수
있다고 합니다.
예약 작업 쪽 설명은 [claude-code-routines.md](claude-code-routines.md)에 따로
정리했습니다.

## 환경 구성하기

### 기본 환경

환경이 없으면 온보딩이 Default 환경을 만듭니다.
Default는 Trusted 네트워크 접근만 가지며 환경 변수와 설정 스크립트가 없습니다.
환경이 하나뿐이면 모든 세션이 그것을 쓰고,
둘 이상이면 표면마다 고르는 방법이 다릅니다.

- 데스크톱 앱, 모바일 앱, `claude.ai/code`: 선택기에 보이는 환경을 씁니다. 고르지 않았다면 Owner가 정한 조직 기본값이 채워집니다. 프로젝트의 스레드는 프로젝트 설정의 환경을 씁니다.
- CLI: `/remote-env`로 고른 환경을 쓰고, 고르지 않았다면 Anthropic 호스팅 환경, 그것도 없으면 목록의 첫 번째 환경입니다. 단 Remote Control이 등록하는 브리지 환경은 제외합니다. `/remote-env`는 기본값을 `remote.defaultEnvironmentId`에 저장할 뿐 세션을 시작하거나 환경을 추가·수정하지는 않습니다.

### 추가, 수정, 보관

환경은 `claude.ai/code`의 새 세션 화면에서 메시지 상자 아래 선택기로 추가, 수정,
보관(archive)합니다.
내가 만든 환경은 개인 소유이며, Owner가 만든 공유 환경은 선택기에 함께 나옵니다.
실행 중인 세션의 환경은 세션 제목 옆 캐럿에서 `Edit cloud environment`로 고칠 수
있습니다.

보관은 새 세션에만 영향을 줍니다.

- 실행 중인 세션은 계속 동작하고 그 세션의 네트워크 시크릿도 붙어 있으므로, 원치 않는 시크릿은 보관하기 전에 지웁니다.
- 선택기와 `/remote-env`에서 사라지고, 예약 작업처럼 환경을 명시한 설정은 새 세션을 시작할 수 없으므로 다른 환경으로 돌려야 합니다.
- Anthropic 호스팅 환경은 삭제 기능이 없고 보관만 됩니다.

### 조직 공유 환경

Team과 Enterprise에서는 Owner가 모든 구성원에게 공유되는 환경을 만들 수
있습니다.
공유 환경은 선택기의 `Organization` 아래에 나오고 구성원에게는 읽기 전용입니다.
Owner는 관리자 설정의 `Cloud environments` 페이지에서 만들거나,
자기 개인 환경을 `Who can use it` 행에서 공유할 수 있습니다.
공유한 환경은 ID를 유지하므로 이미 쓰던 세션과 예약 작업에 영향이 없습니다.
조직 기본 환경은 `claude.ai/admin-settings/claude-code`에서 따로 정합니다.
공유 환경의 변수는 모든 구성원의 세션이 읽으므로 시크릿을 넣지 말고 네트워크
시크릿을 쓰라고 합니다.

## 네트워크 접근

환경마다 아웃바운드 연결을 제어하는 접근 수준 하나를 정합니다.

| 수준    | 아웃바운드 연결                                             |
| ------- | ----------------------------------------------------------- |
| None    | 세션 네트워크를 통한 외부 접근 없음                         |
| Trusted | 허용 목록 도메인만: 패키지 레지스트리, GitHub, 클라우드 SDK |
| Full    | 모든 도메인                                                 |
| Custom  | 직접 만든 허용 목록, 기본 목록을 함께 넣을 수도 있음        |

어느 수준이든 다음은 세션 네트워크 허용 목록을 거치지 않으므로 계속 닿습니다.

- GitHub: 별도의 프록시를 거칩니다.
- 켜 둔 MCP 커넥터: 트래픽이 Anthropic 서버를 거칩니다.
- 환경의 네트워크 시크릿에 적은 호스트: 단 시크릿이 붙지 않는 호스트는 제외합니다.
- Claude Code 자신의 Anthropic API 요청: None에서도 가능합니다.

수준을 바꾸면 Anthropic 호스팅 환경의 기존 세션도 약 1분 안에 새 설정을
따릅니다.
Custom에서는 한 줄에 도메인 하나를 쓰고 앞의 `*.`는 모든 하위 도메인에
일치합니다.

```text
api.example.com
*.internal.example.com
registry.example.com
```

기본 허용 목록을 함께 쓰려면
`Also include default list of common package managers`를 체크합니다.
환경마다 허용 목록이 따로이며, 조직 전체에 밀어 넣는 허용 목록이나 서버 관리
설정은 없습니다.
팀의 표준 목록이 필요하면 Owner가 Custom 접근을 가진 공유 환경을
만들라고 합니다.

Trusted의 기본 허용 목록은 Anthropic 서비스, 버전 관리(GitHub, GitLab,
Bitbucket), 컨테이너 레지스트리, 클라우드 플랫폼, 여러 언어의 패키지 관리자,
리눅스 배포판, 개발 도구, 클라우드 서비스와 모니터링, 콘텐츠 전송과 미러,
스키마와 설정, MCP 도메인으로 묶여 있습니다.
전체 목록은 원문의 `Default allowed domains` 절에 있습니다.

### GitHub 프록시

Anthropic 호스팅 환경에서는 모든 GitHub 작업이 전용 프록시를 거치며,
실제 GitHub 자격 증명은 세션 VM 밖에 둡니다.

- 세션 안의 git 클라이언트는 범위가 제한된 자격 증명을 쓰고, 프록시가 확인한 뒤 실제 토큰으로 바꿉니다.
- 브랜치 삭제와 브랜치가 아닌 대상(태그 등)의 push는 거부합니다. 어느 브랜치를 갱신할 수 있는지는 제한하지 않으므로 GitHub의 브랜치 보호 규칙이나 룰셋을 씁니다.
- 세션에 붙인 저장소의 API 요청만 처리하고, 다른 저장소 요청은 `is not enabled for this session`으로 시작하는 메시지의 403을 받습니다. 붙이지 않은 저장소의 소스 아카이브도 공개 저장소를 포함해 같은 403입니다.
- GraphQL 엔드포인트 요청은 403입니다. 그래서 GraphQL을 쓰는 `gh pr`, `gh issue` 같은 하위 명령이 실패하고, 직접 설정한 `GH_TOKEN`도 같은 403을 받습니다. REST로는 `gh api repos/{owner}/{repo}/...`를 쓰라고 합니다.
- `GH_TOKEN`과 `GITHUB_TOKEN`을 직접 설정하지 않고 프록시가 인증하면 두 변수는 `proxy-injected`라는 자리표시 문자열로 읽힙니다. 그 변수를 직접 읽는 스크립트는 쓸 수 있는 토큰을 얻지 못합니다.

## 환경 변수와 시크릿

### 환경 변수

환경 변수는 한 줄에 `KEY=value` 하나인 `.env` 형식입니다.
따옴표로 감싼 값의 따옴표는 값에 포함되지 않고,
여러 줄 값이나 `#`가 든 값은 따옴표로 감싸야 합니다.
따옴표 없는 값에서 `#`는 주석을 시작하고 그 줄의 나머지는 버려집니다.

```text
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

Claude가 실행하는 어떤 명령도 이 값을 읽을 수 있습니다.
예외는 `OTEL_*` 변수로, Claude Code가 자체 텔레메트리에 쓰며 명령에는 넘기지
않습니다.
세션이 시작할 때 설정하는 `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`는 환경에 넣어도
세션의 값이 이깁니다.

Anthropic 호스팅 환경의 세션은 생성할 때와,
Claude Code가 VM에서 다시 시작할 때마다 값을 읽습니다.
다시 시작하는 경우는 두 가지입니다.

- 몇 분 동안 활동이 없어 일시 중지된 VM이 다음 메시지로 복원될 때
- 일시 중지된 VM이 회수되어 새 VM으로 다시 만들어질 때

그래서 변수를 고쳐도 기존 세션은 VM이 복원되거나 재생성될 때까지 이전 값을
유지합니다.
VM을 직접 일시 중지할 수는 없고, 바로 쓰려면 Claude에게 명령에 직접 지정하게
하거나 새 세션을 시작합니다.
환경 변수는 그 환경을 쓰는 누구나 읽을 수 있습니다.

### 네트워크 시크릿

네트워크 시크릿은 환경에 저장한 API 키나 토큰으로,
Claude가 값을 보지 못한 채 그 API를 호출하게 합니다.
Anthropic의 에이전트 프록시가 요청이 세션 VM을 떠난 뒤 목록에 적은 호스트로 가는
요청에 키를 붙이므로 키가 VM 안에 들어오지 않습니다.
Anthropic 호스팅 환경에만 있고, 자체 호스팅 환경과 고객 관리 암호화 키를 쓰는
조직에서는 저장할 수 없습니다.

시크릿은 하나씩 추가하며 호스트나 값을 바꾸려면 지우고 다시 추가합니다.

| 항목             | 설정                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Secret type      | 기본 Bearer, 헤더로 가는 키용                                                                                             |
| Name             | 라벨                                                                                                                      |
| Allowed websites | API 호스트, 앞의 `*.`는 모든 하위 도메인                                                                                  |
| Custom headers   | 키를 싣는 헤더. 기본은 `Authorization`과 접두사 `Bearer`, `X-Api-Key`처럼 맨 값만 받는 헤더는 이름을 바꾸고 접두사를 지움 |

Team과 Enterprise에서 조직 관리자 역할이 없으면 한 호스트에 시크릿 하나만 받는
짧은 양식이 열리며 `*.` 와일드카드를 받지 않습니다.
공유 환경의 시크릿은 Owner가 관리자 설정에서 추가하고 지웁니다.

시크릿이 붙는 요청에는 세션의 네트워크 접근 수준이 허용하지 않는 호스트도
포함됩니다.
시크릿은 환경을 쓰는 모든 세션에 시작한 사람과 상관없이 지울 때까지 적용됩니다.
저장한 뒤에는 값을 다시 볼 수 없으며, 확인하려면 세션에서 `curl`로 API를
호출시키면 됩니다.
목록에 `Not sent`로 표시되면 아래의 설명을 따르고,
호스트가 겹치지만 완전히 같지 않은 두 시크릿은 표시 없이 하나만 전송됩니다.

시크릿이 절대 붙지 않는 요청은 다음과 같습니다.

- GitHub: GitHub 프록시가 따로 인증합니다.
- `api.anthropic.com`과 공개 패키지 레지스트리: `registry.npmjs.org`, `jsr.io`, `npm.jsr.io`, `pypi.org`, `files.pythonhosted.org`, `index.crates.io`, `proxy.golang.org`
- 설정 스크립트의 요청: Claude Code가 에이전트 프록시에 연결하는 시점은 스크립트가 끝난 뒤입니다.
- Claude Code의 텔레메트리 내보내기

프록시가 붙일 수 없는 키는 환경 변수로 남아야 합니다.

## 세션에서 쓸 수 있는 것

Anthropic 호스팅 환경의 세션은 세션마다 새 VM(Ubuntu 24.04,
x86_64)에서 시작하고 저장소를 새로 clone합니다.
Apple Silicon 같은 로컬 아키텍처와 상관없이 x86_64 리눅스 빌드를 써야 합니다.

### 내 설정 중 따라오는 것

| 항목                                                                   | 클라우드 세션에서          | 이유                                  |
| ---------------------------------------------------------------------- | -------------------------- | ------------------------------------- |
| 저장소의 `CLAUDE.md`, `.claude/rules/`, `skills`, `agents`, `commands` | 있음                       | clone에 포함됨                        |
| 저장소의 `.claude/settings.json` 훅과 권한 규칙, `.mcp.json`           | 저장소가 하나일 때 있음    | clone에 포함됨                        |
| 저장소가 켠 플러그인과 마켓플레이스                                    | 없음                       | `enabledPlugins`를 설치하지 않음      |
| 조직의 서버 관리 설정                                                  | 있음, Claude Tag 세션 제외 | 세션 시작 때 서버에서 가져옴          |
| 사용자 `~/.claude/CLAUDE.md`, `skills`, `agents`, `commands`           | 없음                       | 내 컴퓨터에만 있음                    |
| `claude mcp add`의 로컬·사용자 범위 서버                               | 없음                       | 내 컴퓨터의 `~/.claude.json`에 기록됨 |
| 서비스용 API 키                                                        | 네트워크 시크릿으로        | 프록시가 붙임                         |
| AWS SSO 같은 대화형 인증                                               | 불가                       | 브라우저 로그인이 필요함              |

내 구성을 클라우드에서 쓰려면 저장소에 커밋하라고 합니다.
MCP 서버는 `claude mcp add --scope project`로 `.mcp.json`에 기록해 커밋하면
저장소가 하나인 세션에서 불러옵니다.
저장소 `.claude/settings.json`의 `env` 블록에 있는 `NODE_EXTRA_CA_CERTS`나 mTLS
인증서 변수 같은 전송 변수는 무시되며 디버그 로그에 기록됩니다.

개인 선호를 커밋하고 싶지 않으면 설정 스크립트가 `~/.claude/CLAUDE.md`를 쓰게 할
수 있습니다.
공유 환경이 아닌 내 환경에 두라고 합니다.

```bash
#!/bin/bash
mkdir -p ~/.claude
cat > ~/.claude/CLAUDE.md <<'EOF'
Use conventional commit messages.
EOF
```

다음 세션에서 `/context`를 실행해 `/root/.claude/CLAUDE.md`가 Memory files에
나오는지 확인합니다.

### 설치된 도구

공통 런타임이 미리 설치되어 있습니다.

| 범주         | 포함                                                                      |
| ------------ | ------------------------------------------------------------------------- |
| Python       | pip, poetry, uv, black, mypy, pytest, ruff                                |
| Node.js      | 20, 21, 22(기본 22), npm, yarn, pnpm, bun, eslint, prettier, chromedriver |
| Ruby, PHP    | Ruby 3.1~3.3, PHP 8.3과 Composer                                          |
| JVM          | OpenJDK 21, Maven, Gradle                                                 |
| 그 외 언어   | Go, Rust, C/C++(GCC, Clang, cmake, ninja, conan)                          |
| Docker       | docker, dockerd, docker compose                                           |
| 데이터베이스 | PostgreSQL 16, Redis 7.0                                                  |
| 브라우저     | `/usr/bin/google-chrome`, `CHROME_PATH` 설정됨                            |
| 유틸리티     | git, gh, jq, yq, ripgrep, tmux, vim, nano                                 |

도구 버전은 Claude에게 `check-tools`를 실행하게 해 확인합니다.
.NET SDK처럼 목록에 없는 도구는 레지스트리가 허용 목록에 있어도 미리 설치되어
있지 않으므로 설정 스크립트로 설치합니다.
Bun은 설치되어 있지만 프록시 호환 문제가 알려져 있습니다.
PostgreSQL과 Redis는 설치되어 있지만 실행 중이지 않으며,
Claude에게 `service postgresql start`나 `service redis-server start`를 시킵니다.
VM에 셸로 직접 들어갈 수는 없고 모든 명령은 Claude가 실행합니다.

### 자원과 시간 한도

자원 상한은 대략 4 vCPU, 16GB RAM, 30GB 디스크이며 바뀔 수 있습니다.
큰 빌드나 메모리를 많이 쓰는 테스트는 VM이 중단시킬 수 있다고 합니다.
이를 넘는 작업은 Remote Control이나 자체 호스팅 환경을 쓰라고 합니다.

- 명령: 환경이 따로 타임아웃을 정하지 않으므로 Bash 도구 기본값이 적용됩니다. 포그라운드 명령은 기본 2분, 최대 10분을 기다립니다. 타임아웃에 이르면 `sleep`으로 시작하지 않는 한 백그라운드로 옮기고 30분 더 실행될 수 있습니다. 환경 변수 `BASH_DEFAULT_TIMEOUT_MS`와 `BASH_MAX_TIMEOUT_MS`(밀리초)로 올립니다.
- SessionStart 훅: `timeout`을 지정하지 않으면 600초 뒤 취소됩니다. `async: true`인 훅은 적용되지 않습니다.
- 설정 스크립트: 대략 5분을 넘으면 캐시되지 않습니다.
- 유휴 세션: 몇 분 활동이 없으면 VM이 파일을 저장한 채 일시 중지되고 나중에 회수될 수 있습니다.

### 세션을 추적 가능하게 만들기

Claude가 클라우드 세션에서 만든 커밋에는 `Claude-Session: <url>` git 트레일러가
붙고, PR 본문에는 세션 URL이 한 줄로 들어갑니다.
`attribution.sessionUrl`을 `false`로 하면 둘 다 빠집니다.
다른 곳에 링크를 넣으려면 `CLAUDE_CODE_REMOTE_SESSION_ID`의 `cse_` 접두사를
`session_`로 바꿔 URL을 만듭니다.

```bash
echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/#cse_/session_}"
```

## 설정 스크립트와 환경 캐시

### 설정 스크립트

설정 스크립트는 새 클라우드 세션이 시작될 때 Claude Code가 뜨기 전에 도는 Bash
스크립트입니다.
root로 Ubuntu 24.04에서 실행되므로 `apt install`과 대부분의 언어 패키지 관리자가
동작합니다.
환경 대화상자의 `Setup script` 행에 입력하거나 64KB까지의 텍스트 파일을
불러옵니다.

```bash
#!/bin/bash
apt update && apt install -y shellcheck
```

작성 시 지킬 제약은 네 가지입니다.

- **0으로 종료**: 비정상 종료하면 세션이 시작되지 않습니다. 중요하지 않은 명령에는 `|| true`를 붙입니다.
- **5분 안에 끝내기**: 넘으면 캐시가 만들어지지 않습니다. 독립적인 설치는 `&`와 `wait`로 병렬화하고, 안 맞는 큰 다운로드는 SessionStart 훅에서 백그라운드로 띄웁니다.
- **설치에는 네트워크 필요**: Trusted 수준은 npm, PyPI, RubyGems, crates.io를 포함하지만 None에서는 설치가 실패합니다.
- **환경 변수가 아직 없음**: 스크립트는 환경 변수가 설정되기 전에 돌므로 필요한 값은 스크립트 안에 둡니다.

### 환경 캐시

설정 스크립트가 5분 안에 끝나면 Anthropic이 파일 시스템 스냅샷을 만들어 이후
세션의 시작점으로 씁니다.
캐시는 디스크에 쓴 것만 보존합니다.
설치한 패키지, 받은 Docker 이미지, 쓴 파일은 남고,
스크립트가 띄운 데이터베이스나 `docker compose up` 스택 같은 실행 중 프로세스는
남지 않습니다.
스크립트나 허용 호스트를 바꿀 때, 그리고 캐시가 약 7일 뒤 만료될 때 다시
빌드합니다.
유휴 후 복원된 VM에서는 스크립트가 다시 돌지 않으므로,
스크립트 수정은 VM이 재생성될 때에야 기존 세션에 닿습니다.
바로 적용하려면 세션에서 명령을 직접 실행하거나 새 세션을 시작합니다.
캐시는 켜거나 관리할 필요가 없습니다.

### 설정 스크립트와 SessionStart 훅

|           | 설정 스크립트                                               | SessionStart 훅                               |
| --------- | ----------------------------------------------------------- | --------------------------------------------- |
| 설정 위치 | `claude.ai/code`의 환경 대화상자, 공유 환경은 관리자 페이지 | 저장소 `.claude/settings.json` 같은 설정 파일 |
| 실행 시점 | Claude Code가 뜨기 전, 캐시가 있으면 건너뜀                 | Claude Code가 뜬 뒤, 재개된 세션 포함 매 세션 |
| 실행 장소 | 클라우드 세션만                                             | 로컬과 클라우드                               |

VM 자체에 필요한 도구는 설정 스크립트로,
로컬과 클라우드 모두에서 돌아야 하는 `npm install` 같은 프로젝트 준비는
훅으로 합니다.
사용자 수준 `~/.claude/settings.json`의 훅은 클라우드에서 돌지 않습니다.

훅으로 의존성을 설치하는 예에서 문서는 저장소 `.claude/settings.json`에 훅을
등록합니다.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

스크립트는 `CLAUDE_CODE_REMOTE`가 `true`가 아니면 곧바로 끝나므로 로컬에서는
아무것도 설치하지 않습니다.
`package.json`, `package-lock.json`, 스크립트 자체의 해시가 바뀌지 않았으면
`npm install`을 건너뛰고, 설치가 실패하면 해시를 지워 다음에 다시 시도합니다.

```bash
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR" || exit 1
hashes=node_modules/.install_pkgs.sha256

if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  # Delete the old hashes first, so a failed install runs again next time
  rm -f "$hashes"
  if npm install; then
    sha256sum scripts/install_pkgs.sh package.json package-lock.json > "$hashes" || rm -f "$hashes"
  fi
fi

# pip skips requirements that are already satisfied
pip install -r requirements.txt
exit 0
```

`npm install`이 워크스페이스의 `package.json`이나 `.npmrc`처럼 다른 파일을
읽으면 해시 명령에 그 파일도 넣어야 합니다.

## 함정

- **저장소가 둘 이상이면 훅이 안 돈다**: Anthropic 호스팅 환경에서 여러 저장소를 붙인 세션은 어느 저장소의 `.claude/settings.json` 훅도 불러오지 않습니다. 프로젝트의 클라우드 스레드는 저장소 수와 상관없이 같습니다. 이 경우 설정 스크립트로 의존성을 설치합니다.
- **None 네트워크에서는 설치가 실패한다**: 설정 스크립트와 설치 훅 모두 레지스트리 접근이 필요합니다.
- **캐시되지 않는 5분 초과**: 스크립트가 오래 걸리면 매 세션이 느려지는데, 알림 없이 캐시가 생기지 않습니다.
- **고친 변수와 스크립트가 기존 세션에 안 닿는다**: VM이 복원되거나 재생성될 때까지 이전 값입니다.
- **시크릿을 변수에 두면 읽힌다**: 환경 변수와 설정 스크립트는 그 환경을 쓰는 누구나 읽습니다. 공유 환경이면 모든 구성원입니다.
- **GraphQL은 막혀 있다**: `gh pr`, `gh issue`가 실패하고 Projects v2처럼 GraphQL에만 있는 API는 프록시로 닿지 않습니다.
- **자체 호스팅에는 네트워크 시크릿이 없다**: 시크릿은 Anthropic 호스팅 환경 기능입니다.
- **플러그인은 따라오지 않는다**: 저장소가 `enabledPlugins`로 켠 플러그인도 클라우드 세션은 설치하지 않습니다.
- **보관은 소급되지 않는다**: 이미 도는 세션과 그 시크릿은 남습니다.

HN에서 이 페이지가 올라온 스레드는 댓글이 둘뿐이고 실질적인 논의는 없었습니다.
`for security?`라는 한 줄[^gosen]과 올린 사람의 답글이 전부이고,
올린 사람의 다른 댓글 하나는 dead 상태입니다.

## 기억할 원칙

- 환경은 세션 밖의 설정입니다. 내 컴퓨터에 있는 것은 따라오지 않으므로 필요한 것은 저장소에 커밋하거나 환경에 넣습니다.
- 키는 환경 변수가 아니라 네트워크 시크릿에 두고, 프록시가 붙일 수 없는 호스트와 설정 스크립트에서 쓸 키만 환경 변수로 남깁니다.
- 네트워크는 필요한 만큼만 엽니다. GitHub, 커넥터, 시크릿 호스트는 수준과 상관없이 열려 있다는 점을 전제로 정합니다.
- 설정 스크립트는 5분 안에 0으로 끝나게 쓰고, 실행 중인 프로세스는 캐시되지 않으므로 세션마다 시작합니다.
- 설정을 바꾼 뒤 기존 세션에서 확인하려면 새 세션을 시작합니다.

---

[^gosen]: <https://news.ycombinator.com/item?id=50351349>
