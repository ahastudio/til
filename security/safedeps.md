# safedeps: AI 에이전트 의존성 설치 보안 게이트

<https://www.npmjs.com/package/@aldegad/safedeps>

<https://github.com/aldegad/safedeps>

## 소개

safedeps는 Claude Code와 Codex CLI 에이전트가 실행하는 의존성 설치 명령을
검사하는 로컬 도구다.
README는 취약하거나 승인되지 않은 의존성을 에이전트가 설치하지 못하게 하고,
새어 들어온 것은 되돌린다고 소개한다.
설치 전에는 패키지와 그 전이 의존성 전체를 OSV, CISA KEV, GitHub Advisory로
확인해
승인 원장에 기록하고,
설치 후에는 실제로 lockfile에 들어온 폐쇄(closure)를 다시 확인해서
어긋나면 마지막으로 확인된 스냅샷으로 되돌린다.
외부 서비스에 맡기는 부분 없이 로컬에서 돌고 런타임 의존성이 없다는 것이
README의 설명이다.

2026년 11월 25일 기준 GitHub API 값은 다음과 같다.
언어는 Shell로 분류되고 별은 29개, 포크는 4개, 열린 이슈는 0개다.
저장소는 2026년 4월 1일에 만들어졌고 마지막 갱신은 2026년 11월 23일이다.
토픽은 `ai-agents`, `claude-code`, `codex-cli`, `dependency-security`,
`developer-tools`, `hooks`, `npm`, `osv`, `security-tools`,
`supply-chain-security`다.
npm 레지스트리에는 `@aldegad/safedeps`의 최신 버전 2.25.0과 29개 버전이 올라
있고,
첫 게시는 2026년 5월 18일이다.[^npm]
같은 소유자의 sprite-gen 저장소가 `SECURITY.md`에서 이 도구로 의존성을
확인하라고 안내한다.

저장소의 홈페이지 필드는 npm 패키지
페이지(`https://www.npmjs.com/package/@aldegad/safedeps`)다.
이 페이지는 열지 못했다.
브라우저로 열어도 Cloudflare의 보안 확인 화면(Just a moment)에서 멈췄고
이 확인을 대신 통과하지 않았다.
그래서 패키지 정보는 npm 레지스트리의 JSON으로 읽었고,
페이지에만 있을 수 있는 내용(예: 주간 내려받기 수)은 확인하지 못했다.

라이선스는 PolyForm Noncommercial 1.0.0이다.
`package.json`과 레지스트리가 그렇게 적고 `LICENSE`도 그 본문이다.
GitHub API는 같은 저장소의 라이선스를 `NOASSERTION`으로 돌려준다.
README는 v2.19.0부터 이 라이선스이고 v2.18.1까지는 Apache-2.0이었다고 적는다.
상업적 사용은 이 라이선스가 허용하는 범위 밖이라고 README가 밝히고,
상업적 사용의 허가는 저작권자에게 문의하라고 안내한다.

이 문서는 README, `SKILL.md`, `AGENTS.md`의 앞부분, `SECURITY.md`, `LICENSE`,
`CHANGELOG.md`, `package.json`과 Rust, Shell, Node 소스를 읽어 정리했다.
소스는 Rust 코어와 Shell/Node 쪽으로 나누어 읽었고, 읽은 범위가 좁았던 곳은
본문에 적었다.
어떤 코드도 실행하지 않았고 빌드하지 않았으며 시험도 돌리지 않았다.
따라서 훅이 실제 Claude Code나 Codex에서 어떻게 보이는지는 확인하지 못했다.

## 설치와 시작

README의 빠른 시작은 세 줄이다.

```bash
npm install -g @aldegad/safedeps
cd "$(npm root -g)/@aldegad/safedeps" && node scripts/install/install-safedeps-hooks.mjs
# 이후 에이전트가 실행하는 모든 의존성 설치가 게이트를 거친다
```

패키지 이름은 `@aldegad/`가 붙은 스코프 패키지이고
스코프 없는 `safedeps`는 무관한 다른 패키지라고 README가 따로 적는다.
npm 패키지는 `safedeps` 명령을 설치할 뿐이고
Claude Code나 Codex가 스킬을 알아서 찾지는 않으므로 훅 등록기를 한 번 돌려야
한다.
스킬 전체(`SKILL.md`, 훅 진입, Rust 코어의 소스, 공급자와 원장 라이브러리)를
얻으려면
저장소를 체크아웃하고, 이 경우 코어는 cargo로 빌드된다.
npm 패키지에는 macOS(Apple silicon, Intel)와 Linux x64용 빌드가 들어 있다고
한다.

훅 등록기(`scripts/install/install-safedeps-hooks.mjs`)가 하는 일은 코드에서
확인했다.
Claude Code는 `~/.claude/settings.json`, Codex CLI는 `~/.codex/hooks.json`을
읽고 쓴다.
엔진 디렉터리가 없으면 그 엔진은 건너뛴다.
`~/.<엔진>/skills/safedeps`를 저장소 루트로 가리키는 심볼릭 링크를 만들고,
등록하는 명령은 `safedeps-hook-entry.sh pre|post`이며 매처는 `Bash`다.
`PreToolUse`와 `PostToolUse`는 둘 다 30초로 등록하고,
Claude Code에만 `PostToolUseFailure`에도 사후 훅을 건다(Codex에는 이 이벤트가
없다).
옵트인으로 `SessionStart` 알림(10초)을 더할 수 있다.
같은 명령이 이미 있으면 타임아웃만 맞추고 바뀐 것이 없으면 아무것도 쓰지 않는다.
쓰기 전에 `<경로>.bak`으로 복사하고 임시 파일에 쓴 뒤 `rename`한다.
`.bak`은 매번 덮어써서 직전 상태 하나만 남는다.
코어 바이너리가 빌드되어 있고 진입 셸이 판정하지 않는 호출에 출력 없이 0으로
답하는지 확인하지 못하면
아무것도 등록하지 않는다.

## 동작 방식

### 구성

실행의 중심은 Rust 프로그램 `safedeps-core`이고 나머지는 Shell과 Node가 감싼다.
README는 이 코어가 이전 버전에서 등록하던 두 Bash 스크립트를 대체했다고
설명한다.

| 위치               | 내용                                                    | 규모               |
| ------------------ | ------------------------------------------------------- | ------------------ |
| `rust/src/`        | 훅 코어(PreToolUse 판정, PostToolUse 효과 검증과 롤백)  | 73개 파일 30,323줄 |
| `bin/safedeps`     | 사용자용 CLI(`check`, `revoke`, `re-check`, `watch` 등) | 2,067줄            |
| `lib/`             | 공급자 어댑터, 승인 원장, npm 폐쇄 해석, 저장소 게이트  | Shell              |
| `scripts/install/` | 훅 등록기, 재점검 에이전트 설치기, 상태 이전기          | Node `.mjs` 3개    |
| `scripts/test/`    | 시험 69개 파일, `run-all.sh`가 묶는 배터리 24개         | Shell, Python      |
| `scripts/measure/` | 문서가 인용하는 측정 141개 파일                         | 대부분 Python      |

`bin`, `lib`, `scripts`의 `.sh`와 `.mjs`는 105개 파일 41,621줄이고
이 중 시험이 28,557줄, 측정이 3,946줄이며 제품 쪽은 9,118줄이다.
코어가 Rust에 있으므로 줄 수만으로 Shell이 코드의 대부분이라고 읽으면 틀린다.
Rust에서 가장 큰 파일은 셸 렉서 `lex.rs`(3,868줄)이고
승인 저장소 `approvals.rs`(2,062줄), 판정 코어 `core.rs`(1,544줄),
매니저 단어 판독 `manager.rs`(1,432줄), `--ignore-scripts` 재작성
`inert.rs`(989줄)가 뒤를 잇는다.

코어의 진입은 `main.rs`가 서브커맨드로 나눈다.
`pre`와 `post`가 훅이고 `lex`, `facts`, `inert`, `ledger` 같은 나머지는 측정과
질의용이다.
설계된 경로는 모두 종료 코드 0으로 끝나고 결정은 표준 출력의 JSON에 담긴다.
차단은 `permissionDecision: "deny"`와 이유, 허용과 명령 교체는 `updatedInput`,
사후 메시지는 `systemMessage`다.
진입 셸 `safedeps-hook-entry.sh`는 `bin/native/<os>-<arch>/safedeps-core`를 골라
실행하고,
바이너리가 없거나 실행할 수 없거나 비정상 종료하면 이유를 적은 종료 코드 2로
바꾼다.
대체 판정기는 없다.
릴리스 빌드는 `panic = "abort"`라서 패닉은 진입 셸이 코드 134로 받아 설명과 함께
2로 바꾼다.

### 1단계: 사전 승인(`safedeps check`)

에이전트가 먼저 `safedeps check <생태계> <pkg>@<버전>`을 부른다.
이 명령의 흐름은 다음과 같다.

1. 범위는 정확한 버전으로 바꾼다. npm은 `npm view <pkg>@<범위> version --json`의
마지막 값을 쓰고,
   npm 이외 생태계의 범위는 구현되어 있지 않아 실패한다.
2. 원장에 이미 승인이 있고 승인 저장소가 그 승인을 보증하면 단축 경로로 끝난다.
3. npm이면 `npm install --package-lock-only --ignore-scripts`로 스크립트 없는
임시 lockfile을 만들어
   전이 의존성까지 폐쇄를 뽑고 OSV `/v1/querybatch`에 한꺼번에 묻는다.
4. 결과는 `hard_block`(KEV 등재), `vulnerable`, `clean` 중 하나이고
종료 코드는 0 승인, 2 패치 없는 취약점, 3 KEV 하드 블록, 4 입력과 공급자
오류(판정 불가)다.

공급자 호출은 모두 `curl`이고 Node의 `fetch`는 쓰지 않는다.
OSV 질의는 기본 `--max-time 15`, 배치는 20초이고,
배치는 취약점의 `id`와 `modified`만 주므로 `GET /v1/vulns/<id>`로 레코드를 다시
읽는다.
KEV는 CISA의 JSON 카탈로그를 받아 `cveID`로 맞춘다.
GitHub Advisory는 보강용이며 `GITHUB_TOKEN`이 있고 호스트가 `api.github.com`일
때만 토큰을 붙인다.
공급자 캐시의 TTL은 86,400초이지만 OSV는 2.21.0부터 매번 새로 묻고 이전 답을
읽지 않는다고 한다.

취약한 직접 패키지는 좁히기를 시도한다.
OSV의 `fixed` 값 중 현재보다 높은 것을 `sort -V`로 정렬해 최대 20개 후보를
만들고
앞에서부터 하나씩 다시 조회해 `clean`인 첫 버전을 승인한다.
없으면 종료 코드 2다.

승인 원장은 `~/.safedeps/approved-specs/`의 JSON 파일들이다.
파일 이름은 `sha256-<hex>.json`이고 키는
`sha256(생태계 \n 패키지 \n 버전 [\n 맥락 해시])`다.
기본 만료는 30일(`SAFEDEPS_LEDGER_DEFAULT_TTL_DAYS`)이다.
npm 승인은 `transitive_specs`로 폐쇄 전체를 함께 기록한다.
맥락 해시는 승인이 프로젝트에 묶이게 한다.
Yarn Berry는 프로젝트 디렉터리, `resolutions`, `yarn.lock`, 입력 파일 묶음을
접고,
npm `overrides`는 프로젝트 루트와 정렬한 `overrides`를 접는다.
그래서 한 저장소가 취약한 전이 의존성을 `overrides`로 고쳐 얻은 승인이
고치지 않은 다른 저장소에서는 통하지 않는다.
Yarn에서 아직 `yarn.lock`에 없는 후보는 프로젝트의 해석 입력만 복사한 비공개
미러에서
`yarn install --mode=update-lockfile --no-immutable`로 해석한다.
이 모드는 링크 단계가 없어 후보의 설치 스크립트가 돌지 않고 프로젝트 트리에는
쓰지 않는다.
입력의 해시를 실행 전후에 다시 계산해 바뀌었으면 승인을 무효로 한다.

### 2단계: 사전 훅(PreToolUse)

설치 명령이 나오면 `safedeps-core pre`가 명령을 읽는다.
이 단계는 README가 스스로 휴리스틱이고 격리 환경(sandbox)이 아니라고 말하는 빠른
안내층이다.

렉서(`lex.rs`)는 awk로 짠 이전 Bash 가드의 함수를 하나씩 옮긴 것이다.
따옴표, 치환, heredoc, 주석, 리다이렉션, 앞선 변수 대입을 한 번에 읽고
닫히지 않는 명령은 `unterm`으로 표시한다.
읽기는 bash, zsh, dash 세 가지(`Reading::{Bash, Zsh, Dash}`)이고
명령 시작점을 읽기마다 따로 계산한다.
세 읽기가 한 곳이라도 다르게 읽으면 `DIVERGE`가 서고,
그때는 세 읽기 모두로 설치를 다시 판정한다.
설치 여부는 읽기들의 합집합이다.
README의 “각 셸이 읽는 대로 읽는다”는 서술의 구조는 코드에서 확인했지만,
읽기별 규칙 차이의 전체 목록은 렉서 본문을 읽지 않아 적지 못한다.

설치 동사 표는 `grammar.rs`에 있다.
실행 파일은 `npm`, `npx`, `pnpm`, `yarn`, `bun`, `pip`, `python`, `poetry`,
`uv`, `pipx`,
`cargo`, `go`, `gem`, `bundle`, `mvn`, `dotnet` 등이고
npm은 약어와 오타 변형(`i`, `isntall`)과 `exec`, `create`, `link`까지 포함한다.
옵션 정의는 npm 11.19.0 기준이고 차이 표는 10.8.2다.

판정은 다음 순서다.
설치 대상 증거, 원장 검사, 읽기별 효과, 스냅샷, 호출 기록.
다음 경우 명령을 설치 전에 막는다.
오타를 노린 이름(`lod_sh`, `reacct`, `axois` 등), `--registry`로 공용이 아닌
레지스트리를 지정한 경우,
`curl ... | bash` 같은 원격 실행 파이프, `npm config set ignore-scripts false`,
원장에 없는 `pkg@version`이다.
차단 사유에는 에이전트가 이어서 돌릴 `safedeps check ...` 명령이 들어간다.

Claude Code에서는 npm 설치에 `--ignore-scripts`를 덧붙여 다시
쓴다(`updatedInput`).
Codex는 이 기능이 없어서 재작성하지 않고, 그 경우 설치 스크립트가 롤백 전에 한
번 돌 수 있다고 README가 적는다.
재작성은 `inert.rs`가 맡는다.
플래그를 npm이 참으로 읽는 자리에 놓으려고 마지막 인자 뒤에 먼저 놓아 보고,
`--cache`처럼 다음 단어를 값으로 먹는 옵션 뒤에서는 문장 앞쪽에 놓고,
어느 자리도 맞지 않으면 재작성하지 않고 `UNDECIDED`로 막는다.
세 읽기가 서로 다른 재작성을 만들어도 `UNDECIDED`다.

`UNDECIDED, not unsafe`는 판정을 끝내지 못했다는 뜻의 차단이다.
스캔이 실패했는데 설치처럼 읽히는 경우,
시간 예산 안에 판정이 끝나지 않은 경우,
읽기들이 갈린 경우가 그렇다.
이 문구를 쓰는 이유는 시간 초과를 취약점 발견으로 읽지 않게 하려는 것이라고
README가 설명한다.

시간 예산은 상수로 있다(`pre.rs`).
런타임이 훅에 주는 시간 `RUNTIME_BUDGET_SECONDS = 30`,
가드의 자체 예산 기본 20초와 상한 25초,
예산을 걸기 시작하는 명령 길이 기본 1,024바이트(상한 4,096).
명령이 이 길이 이상이면 부모가 `safedeps-core pre --budget-child`를 자식
프로세스로 띄워
자기 프로세스 그룹에서 판정하게 하고,
20ms 간격으로 지켜보다가 마감이 지나면 SIGTERM, 50ms 뒤 그룹 전체 SIGKILL로
끝내고 차단 JSON을 낸다.
README가 이 구조를 두는 이유는, 런타임이 시간 초과 훅을 죽이면 도구 호출이
그대로 진행되어
게이트가 사라지기 때문이다.
명령을 길게 부풀려 판정 시간을 넘기는 우회를 막는 장치이기도 하다.
상태 디렉터리의 `state.lock`은 `mkdir` 잠금이고 시도 100회, 100ms 간격,
60초가 넘은 잠금은 낡았다고 보고 지운다(`state.rs`, 직접 확인).

판정 중에는 설치 전 스냅샷을 만든다.
`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `package.json`과
`node_modules`의 패키지와 `.bin` 목록을 `~/.safedeps/snapshots/`에 복사하고
`parent_snapshot_id`로 직전의 확인된 스냅샷에 잇는다.

### 3단계: 사후 훅(PostToolUse)과 효과 게이트

README는 npm에서 권위가 사후 효과 게이트에 있다고 말한다.
명령 모양이 아니라 실제로 설치된 결과를 보기 때문에,
감싼 명령이나 난독화된 명령이 사전 검사를 통과해도 사후에서 잡힌다는 설명이다.

`post/run.rs`의 `judge`가 다음 순서로 판정한다.
`package-lock.json`과 npm의 숨은 `node_modules/.package-lock.json`에서 폐쇄를
읽고,
원장 색인(직접 항목과 `transitive_specs`, 폐기되지 않고 만료되지 않고
프로젝트 맥락이 맞는 것)과 대조하고,
OSV 배치와 KEV로 다시 확인한다.
원장에 없는 패키지가 하나라도 있으면 미승인으로 롤백 사유가 된다.
`--no-save`나 `npm -C sub install`처럼 `package-lock.json`을 건드리지 않는
설치도
숨은 lockfile과 `cd`를 따라가 읽는다.

설치가 흔적을 남긴 곳에서만 판정한다는 원칙이 있다.
설치 직전에 시각과 두 lockfile의 상태를 기록하고, 설치 뒤 둘 중 하나라도 다시
쓰였는지 본다.
흔적이 없으면 `UNGATED`로 `advisory.log`에 기록하고 아무것도 되돌리거나 확인하지
않는다.
명령 텍스트에서 디렉터리를 고르는 방식이 세 번의 검토에서 모두 조용한 통과를
만들어서
텍스트는 어디를 볼지만 정하게 바꿨다고 README는 설명한다.

원장 외에 다음 검사가 있다.

| 검사            | 내용                                                                                                                               |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 설치 스크립트   | `preinstall`, `install`, `postinstall`에서 네트워크, 동적 실행, 민감 경로, 난독화 패턴을 정규식으로 찾는다                         |
| 소스와 프로토콜 | 공용 레지스트리 밖의 resolved URL, `http://`와 `git://`, 새 항목 50개 초과 증가를 본다                                             |
| 바이너리        | 새 `.bin` 항목 최대 20개의 헤더를 읽어 ELF, Mach-O, PE 네이티브 실행 파일인지 판별한다. 파일당 64KiB, 합계 20×64KiB, 검사 시간 1초 |

바이너리 검사는 실행하지 않고 읽기만 하며,
검사가 끝나지 않으면(입출력, 마감, 예산 초과) 확인하지 않고 롤백 쪽으로 간다.
이 검사는 별도 감독 자식 프로세스에서 돈다.
OSV 질의는 한 번의 사후 실행 마감 25초 안에서만 하고,
배치 한 페이지는 20초, 레코드 하나는 15초, KEV는 15초 한도다.
OSV 페이지는 최대 20쪽이고 답이 안 오거나 개수가 어긋나면 모두
실패(`fail-closed`)로 처리해 롤백한다.
KEV는 질의 항목이 있을 때만 배치당 한 번 읽고 캐시가 신선하면 그것을 쓴다.
KEV 갱신이 실패하면 오래된 로컬 카탈로그로 대신하고 경고를 남기며,
카탈로그가 전혀 없을 때만 실패로 본다.

### 롤백(reorg)과 확인된 스냅샷

모든 검사를 통과하면 설치 결과의 lockfile과 매니페스트가 새 스냅샷으로 기록되고
`~/.safedeps/confirmed_<디렉터리 해시>`가 그것을 가리킨다.
README는 예전 기준이 설치 이전 스냅샷이어서 한 설치 뒤처졌다고 적고,
승인된 `a`를 설치한 뒤 미승인 `b`를 설치하면 `a`까지 사라지던 것을 지금은 `b`만
지운다고 설명한다.
기준이 되는 것은 파일이지 `node_modules`가 아니다.

검사가 하나라도 실패하면 롤백한다.
확인된 스냅샷이 없는 프로젝트는 명령 직전 스냅샷으로 돌아가고,
그 상태가 검증된 것은 아니라는 사실을 메시지와 로그에 같이 적는다.
`node_modules`는 설치 전에 있었으면 두고 명령이 추가한 항목만 지우며,
명령이 만들었으면 통째로 지운다.
심볼릭 링크는 따라가지 않는다.
`node_modules`, `package.json`, lockfile이 링크이면 그 단계를 거부하고
`REORG REFUSED`로 가리키는 곳을 기록한다.
복원은 패키지 매니저를 돌리지 않으므로 롤백 중에는 설치 스크립트가 돌지 않는다.
제자리에서 바뀐 패키지, 곧 명령이 교체하거나 업그레이드한 패키지는 되돌릴 수
없어서
다음 설치가 게이트를 거칠 때까지 디스크에 남는다고 README가 밝힌다.

롤백이 도중에 끊기는 경우를 위해 시작 전에 저널을 쓴다.
`~/.safedeps/rollback-journal/<id>.json`에 프로젝트, 스냅샷, 이유, 단계, 시각,
pid가 들어가고
롤백이 끝나 보고서를 만든 뒤에만 지운다.
다음 사후 실행이 남은 저널을 훑어 소유 프로세스가 죽었거나 멈췄으면
`rollback-incidents/`로 옮기고 `reorg.log`에 `REORG INTERRUPTED`(멈춘 경우
`REORG STOPPED`)를 쓰며
사용자에게 한 번 알린다.
런타임이 사후 훅 자체를 죽이면 `judging/<pid>-<시각>.json` 표식이 남고
다음 실행이 `NOT JUDGED`를 로그에 쓴다.
다만 사후 판정은 별도 프로세스에서 돌지 않으므로
25초 한도는 대기하는 요청만 끊고, 확인된 설치 뒤의 `npm rebuild`는 마감 없이
기다린다.

확인이 끝난 Claude Code 설치는 그 자리에서 `npm rebuild`를 돌려 그때서야
스크립트를 실행한다.
재빌드는 프로젝트 위치(`--global=false --location=project`)에서만 돌고,
공용 레지스트리가 아닌 출처의 패키지나 `file:` 디렉터리 의존성이 트리에 있으면
통째로 건너뛴다.

### 위험 수용(`SAFEDEPS_ACCEPT_RISK`)

2026년 10월 14일에 639개의 미승인 패키지와 수정본이 없는 OSV 권고 4건을 가진 큰
프로젝트의 설치가
롤백된 일이 이 기능의 계기라고 README는 적는다.
프로젝트가 그 권고들을 도달 불가능으로 직접 판단해 기록해 두었으나 safedeps는
알지 못했다.
명령 앞에 `SAFEDEPS_ACCEPT_RISK='<누가 왜 결정했는지>' npm ci`처럼 대입을 붙이면
사후 게이트가 그 설치를 유지한다.

조건은 코드에서 확인했다.
모든 npm 설치 문장이 같은 값의 대입을 앞에 가져야 하고,
값에 `$`, 백틱, 치환이 없고 비어 있지 않아야 하며,
명령에 설치 외에는 `cd`, `echo`, `export` 같은 닫힌 목록의 셸 내장 명령만 있어야
한다.
환경 변수나 앞선 `export`로 정한 값은 인정하지 않고,
safedeps는 자기 환경 변수에서 이 값을 읽지 않는다.
유지는 문제의 종류가 미승인 또는 취약뿐일 때만 되고,
CISA KEV 항목, 읽지 못한 폐쇄, 의심스러운 설치 스크립트, 비표준 출처, 대량 증가,
네이티브 바이너리는
언제나 롤백한다.
유지할 때는 `~/.safedeps/accepted-risk.jsonl`에 시각, 호출 id, 프로젝트, 명령,
이유,
스냅샷, 문제, 패키지를 한 줄로 쓰고,
쓰지 못하면 유지하지 않고 롤백한다.
`npm rebuild`는 돌리지 않고 확인된 기준 스냅샷은 움직이지 않는다.
Codex에서는 이름을 지정한 패키지의 원장 검사를 풀지 않는다.

### 저장소 잠금과 재점검

설치 시점 게이트와 별개로 저장소 단위 점검이 있다.
`safedeps doctor`는 저장소의 `.gitleaks` 정책, `.githooks`의 사전 점검 훅,
활성 `core.hooksPath`, 스캐너 유무를 진단하고 `--fix`로 시작 정책을 만들어
활성화한다.
`safedeps scan secrets`는 gitleaks를 부르고,
`safedeps audit`은 락파일로 생태계를 정해 `npm audit --json`, `pnpm audit
--json`,
`yarn npm audit --all --recursive --json`(Berry) 또는 `yarn audit
--json`(Classic),
`bun audit --json`을 실행한다.
기본 심각도는 `moderate`이고 알 수 없는 심각도는 critical로 센다.
광고 DB에 닿지 못하면 종료 코드 2(판정 불가)를 돌려주는데,
저장소의 훅 템플릿은 이 경우만 경고를 출력하고 통과시킨다.
실제 발견은 막고 오프라인은 통과시키는 구조다.

설치된 것의 사후 재점검은 `safedeps watch scan`과 `re-check`가 맡는다.
승인 원장의 항목마다 공급자에 다시 묻고 새로 나온 CVE나 KEV 등재를 자동으로
해지하며,
등록된 프로젝트 루트의 lockfile을 다시 읽는다.
설치기(`install-safedeps-recheck-agent.mjs`)가 만드는 것은 macOS launchd 사용자
에이전트 하나이고
기본 시각은 09:00와 21:00다.
README는 Linux의 systemd 타이머와 cron, Windows 작업 스케줄러 방법도 적지만
이는 사용자가 셸에서 직접 실행하는 명령 예시이고 설치기 코드는 launchd만 다룬다.
launchd 외의 호스트용으로는 런타임 복사본만 만드는 `--runtime-only`가 있다.

### 상태, 의존성, 시험

상태는 `~/.safedeps/`에 있다.
`approved-specs/`, `snapshots/`, `confirmed_<해시>`, `reorg.log`,
`advisory.log`,
`approvals.jsonl`(추가 전용 승인 저장소), `accepted-risk.jsonl`,
`rollback-journal/`,
`rollback-incidents/`, `watch/`가 그 구성이다.
`advisory.log`는 64MB를 넘으면 복사, gzip, 제자리 다시 쓰기 순으로 돌리고
보관 아카이브 5개, 합계 512MB 한도다.
README는 낡은 잠금을 60초에 지운다고 적는데,
셸 쪽에서는 이를 찾지 못했지만 Rust 코어의 `state.lock`에 60초 규칙이 있다.
워치 잠금은 `flock`이라 낡았다는 판정이 없고,
`advisory.log` 회전 잠금의 낡은 기준은 300초다.

크레이트 의존성은 0개다.
`Cargo.toml`의 `[dependencies]`가 비어 있고 `Cargo.lock`에는 `safedeps-core`
하나만 있다.
다만 런타임에 외부 프로그램을 부른다.
HTTP 클라이언트를 직접 만들지 않고 `curl`에 맡기고, `npm`과 `gzip`을 실행하며,
CLI는 `jq`가 없으면 종료 코드 4로 끝난다.
libc는 `extern "C"`로 직접 선언하고 `unsafe`는 코드로 30곳(시험 제외 17곳)이며
모두 `newlocale`, `flock`, `waitid`, `kill` 같은 libc 호출이다.
SHA-256, MD5, JSON, POSIX 정규식(`ere.rs`)도 코어 안에 직접 구현되어 있다.
`build.rs`는 `src`, `Cargo.toml`, `Cargo.lock`, `build.rs`를 해시해 바이너리에
도장을 넣고,
실행할 때 체크아웃 바이너리가 자기 소스를 다시 해시해 달라졌으면 판정하지
않는다.
릴리스 프로파일은 `opt-level=3`, `lto`, `codegen-units=1`, `panic="abort"`,
`strip`이다.

시험은 두 층이다.
Rust 안의 `#[test]`가 164개이고 `rust/tests`는 없다.
`scripts/test/`는 69개 파일이고 `npm test`는 `run-all.sh`의 배터리 24개 중
22개를,
`npm run test:release`는 24개 전부를 돌린다.
대표 시험은 다음과 같다.
`e2e.sh`(5,391줄)는 훅 응답과 보고서를 종단으로 검증하고,
`consumer-forms.sh`(3,896줄)는 설치로 인식하는 구문의 닫힌 목록의 경계를
양쪽에서 고정하고,
`check-fail-closed.sh`(3,072줄)는 공급자가 답하지 못할 때 `check`가 종료 코드
4를 내는지 보고,
`self-budget.sh`(772줄)는 시간 초과 시 차단으로 답하는지를 본다.
Rust 시험 중에는 셸 CLI의 상수와 코어의 상수가 어긋나지 않는지 `/bin/bash`로
대조하는 것이 있다.

### 저장소 운영

`.github` 디렉터리가 없다.
`AGENTS.md`와 README는 GitHub Actions가 시험을 돌리지 않고
시험은 소유자의 macOS 기계에서 돌며(`scripts/ci/run-on-hosts.sh`가 여러 대에
나눈다),
Windows는 WSL1에서 네 배터리만 돌리고 Linux는 시험하지 않는다고 적는다.
릴리스 점검 `scripts/ci/release-checks.sh`는 ShellCheck, 고정 버전 gitleaks
8.30.1로 전체 이력의 비밀 검사,
`npm pack` 내용 확인을 한다.
이 단계들은 예전에 워크플로에 있었고 2026년 10월 6일 소유자 결정으로 자체
호스트로 옮겼다는 주석이 있다.
`CHANGELOG.md`는 76줄이고 버전은 2.21.0부터 2.25.0까지 5개뿐이다.
`SECURITY.md`는 지원 버전을 2.x의 최신 마이너로 정하고 제보는 GitHub 비공개
권고나 이메일로 받는다.

## 분석

### 명령을 읽는 것이 아니라 결과를 읽는다

설계의 무게는 사후 효과 게이트에 있다.
README는 사전 훅을 빠른 안내이자 휴리스틱으로 낮추고,
npm에서는 lockfile에 실제로 들어온 폐쇄를 권위로 삼는다.
이유는 셸 명령의 모든 철자를 읽는 일이 끝나지 않기 때문이다.
README가 직접 적는 비가시 형식만 해도 herestring, 스크립트 파일, `xargs`,
`sudo`와 `timeout` 같은
인자 전달 래퍼, 셸이 런타임에 조립하는 단어가 있다.
코어가 `bash`, `zsh`, `dash` 세 읽기를 따로 돌리고 어긋나면 모두 판정하는 것은
같은 문자열을 셸마다 다르게 해석하는 문제를 설치 판정에 끌어들이지 않으려는
방어다.
하지만 렉서가 3,868줄에 이르는 것은 사전 층을 완벽하게 만들려는 시도의 크기를
보여 준다.
그 위에 사후 층이 있어서 사전 층의 구멍이 치명적이지 않다는 것이 이 설계의
논리다.

### 결정하지 못함이라는 제3의 결과

허용과 차단만 있으면 시간 초과가 곧 허용이 된다.
에이전트 런타임은 훅이 시간을 넘기면 죽이고 호출을 진행시키므로
명령을 부풀려 판정 비용을 늘리는 것만으로 게이트가 사라질 수 있다.
safedeps는 자체 예산을 런타임보다 짧게 잡고 넘기면 `UNDECIDED, not unsafe`로
막는다.
이 문구는 발견과 미결정을 구분해서 사람이 시간 초과를 취약점으로 오해하지 않게
한다.
판정 자체를 자식 프로세스 그룹에서 돌려 마감 시 그룹째 종료하는 구조도 같은
이유에서 나왔다.
미결정을 별도의 결과로 세운 것이 이 도구에서 가장 일반화하기 쉬운 부분이다.

### 승인을 맥락에 묶는 원장

원장 키가 `생태계, 패키지, 버전`에 프로젝트 맥락 해시를 더하는 구조는
승인이 패키지의 속성이 아니라 패키지와 그것이 놓이는 해석 환경의 속성이라는
판단이다.
같은 `foo@1.2.3`이라도 `overrides`가 다른 프로젝트에서는 전이 의존성이 달라진다.
그래서 `overrides`나 `resolutions`로 취약한 전이 의존성을 고친 저장소의 승인이
다른 저장소로 새지 않고, 고치기 전 상태가 승인되는 일도 없다.
승인에 만료(기본 30일)와 해지가 있고 재점검이 새 권고로 자동 해지하는 것도
승인을 한 번의 사실이 아니라 시간에 따라 낡는 기록으로 다루는 선택이다.

## 비평

### 이 게이트가 보는 범위는 npm이다

README의 마지막 경계 목록이 이를 직접 인정한다.
효과 우선 검증은 npm에서만 되고,
`pip`, `cargo`, `go`, `gem`, `maven`, `nuget`은 명령 게이트와 롤백 모델에
머문다.
`pip install evil`처럼 버전을 고정하지 않은 설치는 원장 검사가 돌지 않고
`UNGATED`로 기록만 된다.
pnpm, yarn, bun, `.npmrc`가 기록에서 빼는 설치, `npm link`, `npx` 같은 실행기도
같다.
기록만 하고 막지 않는 이유는 모든 비고정 설치를 거부하면
`cargo add x` 같은 평범한 작업이 깨지므로 저장소 소유자의 정책 결정으로 남긴다는
것이다.
도구의 이름과 소개문은 의존성 설치 전반을 말하지만 강제력은 npm에 치우쳐 있다.
README의 첫 인상과 이 경계 목록 사이의 거리를 독자가 직접 메워야 한다.

### Codex에서는 탐지 후 롤백이다

Claude Code의 훅 기능(`updatedInput`)을 쓰는 `--ignore-scripts` 덧붙임이
Codex에는 없다.
README는 Codex에서 악성 설치 스크립트가 롤백 전에 한 번 돌 수 있다고 적는다.
이 도구의 제목은 Claude Code와 Codex를 함께 말하지만
스크립트 실행을 막는 보증은 두 엔진에서 다르다.
또 Claude Code에서도 README는 플래그가 실제로 npm에 전달되는지는 셸 상태에 달려
있어서
safedeps가 보증하는 것은 플래그를 덧붙였다는 사실뿐이라고 거듭 적는다.

### 시간 예산의 구멍이 문서에 있는 만큼 코드에도 있다

사후 훅의 한도 25초는 OSV와 KEV 같은 요청과 네이티브 검사만 끊는다.
lockfile과 `node_modules` 순회, 롤백의 파일 작업,
확인된 설치 뒤의 `npm rebuild`는 끊지 못하고, 코드에서 `rebuild`의
`child.wait()`에는 마감이 없다.
런타임이 30초에 훅을 죽이면 설치는 판정 없이 남고,
다음 실행이 `NOT JUDGED`를 로그에 쓴다.
README의 측정은 이 한계를 숫자로 보여 준다.
Apple M1, macOS 15.6.1, 2026년 10월 7일의 합성 폐쇄에서
64,000개가 12.77초에서 29.60초, 128,000개가 33.55초에서 72.92초 걸렸고
그 사이는 재지 않았다.
실제 OSV와 CISA 네트워크, 롤백, 실제 `node_modules`는 이 측정에 들어 있지 않다.
매우 큰 lockfile에서는 게이트가 판정하기 전에 죽는다는 것을 문서가 스스로
말한다.
또 KEV는 갱신에 실패하면 오래된 로컬 카탈로그로 대체한다.
OSV 실패는 롤백인데 KEV 실패는 통과라는 비대칭은 문서의 fail-closed 서술에서
눈에 띄지 않는다.

### 문서와 라이선스의 확인되지 않는 부분

README가 146KB, `ARCHITECTURE.md`가 396KB, `ROADMAP.md`가 332KB이고
한국어판이 각각 따로 있다.
그 안에 한계와 예외가 잇달아 들어가 있어서 독자가 한 문장씩 코드와 대조하기는
어렵다.

라이선스는 확인되지 않는 점이 있다.
README는 v2.18.1까지 Apache-2.0이었다고 하는데 `CHANGELOG.md`에는 `apache`,
`polyform`, `license`가 한 번도 나오지 않고
버전 항목도 2.21.0 이후 5개뿐이어서 v2.18.1과 v2.19.0 항목이 없다.
`LICENSE`에도 Apache 본문은 없다.
GitHub이 `NOASSERTION`을 주는 원인은 이 클론으로는 알 수 없다.
`LICENSE`의 첫 줄에 `Required Notice:`가 표준 본문보다 앞에 붙어 있는 것이
감지를 막았을 수 있다는 것은 추측이다.
또 라이선스가 비상업용으로 바뀐 도구를 팀이나 회사의 에이전트 환경에 쓰는 경우
허용 범위를 사용자가 `LICENSE`에서 직접 확인해야 한다.

### 시험은 많지만 외부에서 재현할 수 없는 구조다

코어의 시험은 Rust 164개와 Shell 배터리 24개이고 릴리스 시험은 소유자의 macOS
기계에서만 돈다.
README가 Linux는 시험하지 않는다고 적는데 npm 패키지에는 Linux x64 바이너리가
들어 있다.
외부 사용자는 어느 환경에서 시험이 통과했는지 확인할 수 없고,
2026년 4월에 시작한 단일 소유자 저장소가 6개월 동안 29개 버전을 냈다는 속도는
기능이 빠르게 늘고 있음을 보여 주지만, 보안 도구가 믿음을 얻는 데 필요한 외부
검토와는 다른 지표다.

### 같은 사용자의 권한이라는 경계

`~/.safedeps`에 쓸 수 있는 같은 사용자의 공격자는 원장을 고칠 수 있다.
README가 이를 신뢰 경계 밖으로 둔다고 직접 적는다.
에이전트가 같은 사용자 권한으로 돌므로
에이전트가 원장 파일을 직접 쓰는 경로를 이 도구가 막는지는 문서에서 확인하지
못했다.
사전 훅이 `Bash` 도구 호출만 매처로 삼으므로
에이전트가 다른 도구(파일 쓰기)로 `~/.safedeps`를 바꾸는 경우는 훅의 대상이
아니다.
이는 코드에서 확인한 사실이 아니고 훅 등록 매처에서 이어 붙인 추론이다.

## 인사이트

### 에이전트 가드레일의 단위는 명령이 아니라 상태 변화다

에이전트에게 도구를 쥐여 주면 명령은 무한히 다양해지고 결과는 몇 가지로 모인다.
safedeps는 설치 명령이라는 열린 집합을 읽는 대신 lockfile이라는 닫힌 구조를 읽는
쪽에 권위를 둔다.
같은 원리는 다른 에이전트 안전 장치에도 옮겨진다.
파일을 지우는 명령을 막기보다 지워진 결과를 스냅샷과 비교해 되돌리고,
네트워크 호출을 막기보다 열린 소켓을 본다.
이 접근은 되돌릴 수 있는 결과에만 통한다는 한계가 있다.
safedeps도 제자리에서 바뀐 패키지는 되돌리지 못한다고 적는다.

### 확인된 기준선을 쌓는 방식은 롤백의 기준을 바꾼다

README가 블록체인의 재조직(reorg)에 비유하는 이유는 롤백 지점이 직전이 아니라
검증된 마지막이라는 데 있다.
기준을 설치 직전으로 두면 한 설치씩 뒤처져서 승인된 설치까지 지워지고,
검증을 통과한 결과를 새 기준으로 올리면 롤백은 미승인만 지운다.
이 구조는 확인 시점과 사용 시점 사이에 파일이 바뀌는 문제도 같이 다룬다.
파일을 먼저 복사하고 검사가 끝났을 때 같은 바이트일 때만 기준을 옮기며,
다른 설치가 그 사이 파일을 바꾸었으면 옮기지 않고 이유를 알린다.
검증과 되돌림이 있는 시스템에서 기준선을 언제 옮기는가가 가장 쉽게 틀리는
지점이다.

### 보안 도구의 정직함이 문서의 양으로 돌아온다

이 저장소의 README는 자기 한계를 길게 적는다.
측정 범위와 샘플 수까지 적고, 의도적으로 두는 구멍을 이름 붙여 나열한다.
이 태도는 보안 도구에서 드문 장점이다.
다만 한계를 적을수록 문서가 길어져서 독자가 핵심 보증이 무엇인지 찾기 어려워지는
비용이 따른다.
이 문서는 그 비용을 줄이려고 보증이 어디까지인지를 비평 앞부분에 모았지만,
원 문서 쪽에는 한눈에 보이는 보증 표가 있으면 읽기가 쉬워질 것이다.
이는 README의 내용에 대한 평가가 아니라 구성에 대한 제안이다.

---

[^npm]: npm registry, [@aldegad/safedeps](https://registry.npmjs.org/@aldegad%2fsafedeps), 2026-11-25
