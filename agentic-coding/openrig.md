# OpenRig: Claude Code와 Codex 세션을 YAML로 선언한 팀으로 묶는 로컬 제어면

<https://openrig.dev/>

<https://github.com/mvschwarz/openrig>

Show HN: [OpenRig – agent harness that runs Claude Code and Codex as one system](https://news.ycombinator.com/item?id=47772935) (8점, 5개 댓글)

Show HN: [OpenRig – a control plane for multi-agent coding topologies](https://news.ycombinator.com/item?id=48241066) (6점, 8개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49872623> (2점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=34854>

## 소개

OpenRig는 Claude Code, Codex, Pi 같은 코딩 에이전트를 역할과 주소를 가진
지속적인 팀으로 운영하는 오픈소스 도구다.
README의 첫 문장은 하네스가 모델을 감싸고, 리그(rig)가 하네스를 감싼다는 것이다.
에이전트 팀을 YAML로 정의하고 명령 하나로 띄우며,
Claude Code와 Codex를 한 리그 안에서 하나의 시스템으로 관리한다.
사용자는 리드 에이전트와만 대화하고,
리드가 전문 에이전트들을 조율해
결과와 사람이 내려야 할 결정을 가져온다는 구도다.

만든 사람은 Esoteric Labs의 Mike Schwarz다.
2026년 4월 8일 블로그 글 Why I Built OpenRig에서 그는 ChatGPT 출시 이후 AI와
함께 최소 8,000시간 코드를 썼다고 밝힌다.
출발점은 재부팅이었다.
tmux로 여러 에이전트를 서로 대화하게 엮어 며칠씩 키워 둔 오케스트레이터,
PR을 40개 넘게 리뷰한 리뷰어, 조사 에이전트가 있는데,
재부팅하면 어느 세션이 어느 역할이었는지, 작업 디렉터리가 어디였는지,
서로 어떻게 연결되어 있었는지를 다시 맞추는 데 30분 넘게 걸렸다는 것이다.
그래서 전체를 스냅숏으로 저장하고 재부팅한 뒤 복원하는 도구를 원했고,
그것이 OpenRig의 시작이었다고 설명한다.

저장소는 2026년 3월 23일 첫 커밋 이후 3,704개 커밋이 쌓였고,
9월 1일 이후에만 1,035개다.
태그는 4월 19일 v0.1.12에서 시작해 9월 28일 v0.6.0,
10월 9일 공개된 v0.6.8까지 이어지며,
main은 이미 0.6.9 개발 버전이다.
v0.6.0의 릴리스 제목은 works for strangers로,
만든 사람 밖의 사용자에게도 동작하게 만드는 것을 목표로 한 판이다.
라이선스는 Apache 2.0이고 언어는 TypeScript이며,
이 글을 쓰는 시점의 GitHub 별은 6,273개다.

`CONTRIBUTING.md`는 OpenRig가 자기 자신,
즉 코딩 에이전트 리그와 소수의 사람이 만든다고 적는다.
커밋 작성자 목록 맨 위가 `v-openrig-build`라는 빌드용 신원이고,
홈페이지 하단에도 Made with OpenRig라는 문구가 있다.
홈페이지는 2026년 9월 30일 기준 Mac mini 한 대에 좌석 109개를 정의해 41개가 실행
중이고 13개가 활동 중인 저자의 명단을 보여 주며,
에이전트를 필요할 때 띄워 그대로 두고, 그 부분을 이미 아는 에이전트에게 나중에
일을 보낸다고 설명한다.

이 저장소의 `sandbox.md` 트렌드 항목도 GitHub Trending에서 하루 734개 별을 얻은
프로젝트로 OpenRig를 짧게 다룬다.

## 동작 방식

### 구성 요소

OpenRig는 tmux 위에서 도는 로컬 데몬, CLI, TUI, MCP 서버로 이루어진다.
`ARCHITECTURE.md`에 따르면 데몬은 Hono HTTP 서버이고 기본 포트는 7433이며,
상태는 `~/.openrig`의 SQLite 데이터베이스에 둔다.
CLI, TUI, MCP 서버는 모두 같은 로컬 HTTP로 데몬과 통신한다.

| 패키지                 | 역할                                                              |
| ---------------------- | ----------------------------------------------------------------- |
| `packages/daemon`      | HTTP 라우트, 도메인 서비스, SQLite 마이그레이션, 런타임 어댑터    |
| `packages/cli`         | `rig` 명령과 MCP 서버, 유일하게 npm에 배포되는 `@openrig/cli`     |
| `packages/tui`         | 터미널 UI, CLI 패키지에 함께 들어감                               |
| `packages/ui`          | React 웹 UI, 유지보수 모드로 새 기능 개발 없음                    |
| `packages/test-system` | 스텁 에이전트 시나리오, CI 시나리오 하네스, 실제 모델 평가 케이스 |

에이전트 자체는 손대지 않는다.
각 에이전트는 tmux 세션 안에서 도는 평범한 Claude Code나 Codex 프로세스이고,
OpenRig가 더하는 것은 그 주변의 조율이다.
띄우고 복원하기, 메시지 전달, 작업 큐, 스킬과 문맥 주입이 여기에 속한다.
런타임 어댑터는 `claude-code`, `codex`, `pi`, `omp`, `terminal`,
`stub` 여섯 가지다.
아키텍처 문서가 확인한 시점 기준으로 최상위 `rig` 명령은 87개,
MCP 도구는 18개다.
4월 블로그 글이 36개 명령과 17개 MCP 도구를 내세웠던 것과 비교하면 반년 만에
명령이 두 배 넘게 늘었다.

### 개념

| 개념      | 뜻                                                                                     |
| --------- | -------------------------------------------------------------------------------------- |
| RigSpec   | 팀 전체를 정의하는 YAML, 팟, 멤버, 엣지, 연속성 정책, 문화 파일을 담는다               |
| AgentSpec | 스킬, 지침, 훅, 프로필, 시작 계약을 묶은 재사용 가능한 에이전트 설계도                 |
| 좌석      | `dev-build@starter`처럼 리그 안의 고정된 역할과 주소, 그 자리를 차지한 대화는 바뀐다   |
| 팟        | 지침과 문맥을 공유하는 좌석 묶음, 컨텍스트 창은 에이전트마다 따로다                    |
| 엣지      | 좌석 사이의 관계, `delegates_to`, `spawned_by`, `can_observe` 등 다섯 종류             |
| Culture   | 리그의 `CULTURE.md`, OpenRig 기본 문화 위에 그 팀의 협업 규범을 더한다                 |
| RigBundle | AgentSpec을 함께 넣고 SHA-256 무결성을 붙인 휴대용 아카이브, GitHub 폴더 링크도 받는다 |

좌석이라는 개념이 이 도구의 중심이다.
컨텍스트가 차서 세션을 새로 열어도 `dev-build@starter`라는 주소와 그 역할에 딸린
문맥은 그대로 남는다.
사용자와 다른 에이전트는 세션이 아니라 이 주소에 말을 건다.

### 기본 제공 팀

`starter` 리그의 YAML은 다음과 같다.
Claude Code 빌더 하나와 Codex 리뷰어 하나가 한 팟에 있고,
빌더가 리뷰어에게 일을 넘기는 `delegates_to` 엣지가 하나 있다.

```yaml
version: "0.2"
name: starter
culture_file: CULTURE.md

pods:
  - id: dev
    label: Project
    members:
      - id: build
        agent_ref: "local:../../../agents/development/implementer"
        runtime: claude-code
        profile: default
        cwd: "."
        startup:
          files:
            - path: guidance/lead-first-move.md
              delivery_hint: send_text
              required: true
      - id: review
        agent_ref: "local:../../../agents/development/qa"
        runtime: codex
        profile: default
        cwd: "."
    edges:
      - kind: delegates_to
        from: build
        to: review

edges: []
```

실제 파일에는 `summary`와 Codex 모델 지정이 더 있지만 구조는 이것이 전부다.
좌석 이름은 `{팟}-{멤버}@{리그}` 규칙을 따르므로 빌더의 주소는
`dev-build@starter`가 된다.

| 팀         | 말을 거는 좌석       | 구성                                                                   |
| ---------- | -------------------- | ---------------------------------------------------------------------- |
| `starter`  | `dev-build@starter`  | Claude Code 빌더와 Codex 리뷰어, 범위가 정해진 변경 하나               |
| `workshop` | `orch-lead@workshop` | 리드, 빌더, QA, 리뷰어, 한 저장소의 지속적인 작업, 번들로 설치         |
| `factory`  | `orch-lead@factory`  | 리드, 어드바이저, 빌드, QA, 디자인, 독립 리뷰어 둘, 모두 일곱 에이전트 |

`factory`에서 독립 리뷰어 둘은 하나가 Claude Code, 하나가 Codex다.
리드는 다섯 좌석에 `delegates_to` 엣지를 갖고,
리뷰어는 빌드와 디자인, QA 좌석에 `can_observe` 엣지를 갖는다.
이 밖에 `code-review`, `research`, `pm` 같은 특화 팀과,
HashiCorp Vault 인스턴스를 전문 에이전트가 운영하는 `secrets-manager`가 함께
들어 있다.

설치하면 `kernel`이라는 리그가 먼저 자동으로 뜬다.
사용자 의도를 해석하는 어드바이저, OpenRig 자체를 운영하는 운영자 에이전트,
사람과 에이전트가 같이 쓰는 터미널 좌석으로 이루어지며,
운영자가 무엇을 만들고 싶은지 묻고 위 세 팀 중 하나를 추천해 띄운다.
설치를 맡은 에이전트가 사용자를 운영자와의 대화로 넘겨주는 순간이 설치 완료로
정의되어 있다.

### 메시지와 큐

에이전트 사이의 대화는 tmux가 실어 나른다.
`rig send`는 대상 좌석의 tmux 창에 텍스트를 붙여 넣고,
`rig capture`는 그 창의 출력을 읽는다.
소스의 `tmux.ts`를 보면 `load-buffer`, `paste-buffer`,
`send-keys`로 구현되어 있다.
저자는 첫 Show HN에서 tmux가 여전히 아래에서 대화를 맡고 있고 더 화려한 메시징
계층을 얹지 않았다고 썼다.

다만 채팅 텍스트를 작업 기록으로 쓰지는 않는다.
`starter`의 `CULTURE.md`는 빌더가 큐 항목을 만들고 소유권을 주장한 뒤 일하고,
`rig queue handoff`로 저장소 경로, 후보 커밋이나 diff, 실행한 검사,
한계를 넘기라고 지시한다.
리뷰어는 그 정확한 후보에 대해 관찰을 기록하고,
빌더가 지적을 해결해 최종 결과를 큐에 남긴다.
README도 메시지를 보낸다고 큐 항목이 생기지 않으며 빌더가 직접 작업을 기록한다고
적는다.
응답이 없는 큐 항목은 `delegates_to` 엣지의 출발점,
즉 그 좌석의 오케스트레이터에게 올라간다.

### 스냅숏과 복원

`rig down --snapshot`은 토폴로지 상태를 저장하고 `rig up <이름>`은 최신
스냅숏에서 되살린다.
복원 결과는 좌석마다 `resumed`, `fresh-primed`, `awaiting-decision`,
`attention_required`, `failed` 중 하나로 보고된다.
원래 대화를 이어 갈 수 없으면 `--fresh`로 새로 시작할지 사람이 정해야 한다.
`rig discover`는 이미 tmux에서 돌고 있는 Claude Code와 Codex 세션의 프로세스
트리와 작업 디렉터리를 살펴 지문을 만들고,
`rig adopt`가 그 세션들을 관리 대상 리그로 편입한다.

## 사용하기

요구 사항은 Node.js 22 또는 24와 tmux, macOS나 Linux다.
Apple silicon Mac에서는 Node.js 22를 권하고,
Windows는 WSL2로만 지원하며 WSL2에서는 자동 테스트를 돌리지 않는다.
Claude Code와 Codex 중 이미 가진 계정 하나만 있어도 되고,
두 번째 구독은 필요 없다.
`starter`는 기본으로 둘 다 쓰므로, 하나만 있으면 커널 운영자에게 그 제공자에
맞게 고친 사본을 만들어 달라고 한다.

README가 안내하는 수동 경로는 다음과 같다.
나는 이 명령들을 직접 실행하지 않았다.

```bash
# 설치 후 실제로 무엇을 바꿀지 먼저 본다
npm install -g @openrig/cli
rig setup --dry-run

# 저장소에서 starter 팀의 구성과 실행 계획을 확인한 뒤 띄운다
cd /path/to/your/repository
rig specs preview starter --kind rig
rig up starter --cwd . --plan
rig up starter --cwd .

# 좌석이 인증, 신뢰, 권한 프롬프트에 걸려 있지 않은지 확인한다
rig ps --nodes --rig starter

# 빌더에게 범위가 정해진 결과 하나를 맡기고, 큐에 기록된 작업을 본다
rig send dev-build@starter 'Implement <one useful change>. Track the task in the queue and return its ID.'
rig queue list --destination dev-build@starter --limit 1000
```

팀과 터미널을 함께 보려면 `rig terminal open saved:kernel --window`를 쓰고,
herdr이 있으면 `rig terminal open starter --provider herdr`로 한 리그의 좌석을
한 작업 공간에 펼친다.
herdr에서는 탭 하나에 좌석 16개까지 들어간다.
사람이 직접 타이핑하는 좌석에는
`rig seat set-typing-guard <seat> --enabled true --reason <text>`로 자동 메시지
입력을 막을 수 있다.
막힌 메시지는 보관함에 남고, 가드를 꺼도 다시 재생되지 않는다.

README의 다른 경로인 설치 스크립트는 `npm install -g`로 최신 `@openrig/cli`를
설치하고 `rig setup --dry-run`과 `rig setup`까지 한 번에 돈다.
`rig setup`은 없는 Claude Code나 Codex를 설치하고,
`~/.tmux.conf`에 OpenRig 블록을 쓰며,
`--no-herdr`로 거절하지 않는 한 herdr도 설치한다.

## 권한과 기계에 남는 변경

README는 OpenRig가 신뢰 설정과 실행 가능한 훅을 쓴다고 굵게 경고하고,
처음 쓰기 전에 관련 파일을 백업하라고 권한다.
문서가 밝힌 변경을 정리하면 다음과 같다.

| 시점             | 바뀌는 것                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------ |
| 데몬 시작        | `~/.openrig` 상태와 데이터베이스, `~/.claude/skills`와 `~/.agents/skills`에 스킬 세 개, Codex 훅과 신뢰 기록 |
| 좌석 실행        | tmux 세션 생성, 작업 공간 사전 신뢰, `.claude/settings.local.json`에 상태 줄 명령과 활동 훅                  |
| Codex 설정       | `~/.codex/config.toml`에 훅 활성화, 활동 중계 명령, 그 명령의 신뢰 해시, 작업 공간 `trusted`                 |
| Claude 공유 설정 | `permissions.defaultMode`를 `acceptEdits`로 두고 Exa와 Context7 MCP 항목을 켠다                              |
| Git 저장소       | 새로 만든 `.codex/plugins/` 아래 파일을 `info/exclude`에 추가, 새 `AGENTS.md`와 `CLAUDE.md`는 경고만 한다    |

활동 중계는 이벤트 종류, 좌석과 런타임 신원, 시각,
세션 식별자를 로컬 데몬으로 보내고,
프롬프트 텍스트와 도구 인자는 보내지 않는다고 적혀 있다.
`OPENRIG_HOME`만 바꿔서는 제공자 설정이 격리되지 않는다는 점도 문서가 직접
경고한다.

권한은 층이 여럿이다.
정책도, 좌석별 선택도, Codex 프로필도 없는 팀 좌석은 실행할 때마다 팀 기본값을
받는다.
Claude는 `acceptEdits` 위에 평범한 `rig` 명령과 프로젝트 읽기,
흔한 테스트 명령을 묻지 않고 허용받고,
`rig up`과 `rig down` 같은 수명 주기 명령은 세션 한정 `PreToolUse` 훅이 묻는다.
Codex는 `workspace-write` 샌드박스에 OpenRig 작업 공간과 팟의 상태 디렉터리를
쓰기 가능한 디렉터리로 더 받는다.
문서는 이 훅이 편의 정책일 뿐 격리 경계가 아니라고 적고,
Codex의 수명 주기 명령에는 새 승인 규칙이 생기지 않는다고 밝힌다.

`kernel` 리그의 좌석은 예외다.
따로 정책이 없으면 Codex 좌석은 `-s danger-full-access -a never`로 뜬다.
Codex에 로그인한 상태라면 기본 커널의 운영자 에이전트가 Codex 좌석이므로,
설치하자마자 떠 있는 에이전트 하나가 샌드박스도 승인도 없이 도는 셈이다.

내장 권한 정책은 다섯 개다.

| 정책               | 묻지 않고 실행                              | 사람에게 묻는 것                         |
| ------------------ | ------------------------------------------- | ---------------------------------------- |
| `builtin:locked`   | 툴체인, `rig_up`, `rig_down`만, 나머지 거부 | 없음                                     |
| `builtin:standard` | 목록에 없는 모든 것, 원격 push 포함         | PR 생성, 패키지 배포, 병합, 강제 push 등 |
| `builtin:open`     | PR, 배포, 병합, 강제 push까지 전부          | 파괴적 작업 분류만                       |
| `builtin:yolo`     | 전부, 실행 시 권한 프롬프트를 우회          | 없음                                     |
| `builtin:auto`     | Claude는 자동 모드가 판단                   | Codex와 Pi는 기본 수준과 같다            |

여기서 문서가 숨기지 않는 사실이 하나 있다.
설정 면 정책인 `locked`, `standard`, `open`은
기록만 되고 실행 시점에 적용되지 않는다.
좌석은 여전히 기본 수준으로 뜨고, 허용과 거부 규칙은
`applying-a-permission-policy` 스킬이 각 런타임의 네이티브 설정으로 옮겨야
효력이 생긴다.
문서는 Claude의 접두어 규칙이 `git push --force`와 `git push`를 안정적으로
구분하지 못한다는 예도 든다.
또 사람에게 묻는 규칙은 자율 좌석을 멈추게 하므로,
정책 파일 스스로 자율 팀에는 Open이나 YOLO를 권한다.

## 트레이드오프

### tmux를 전송 계층으로 쓰면 투명하지만 전달을 증명하기 어렵다

tmux를 쓰는 이유는 분명하다.
모든 에이전트가 사람이 붙어서 읽고 타이핑할 수 있는 실제 터미널이고,
에이전트끼리 말하는 방식도 사람이 말하는 방식과 같다.
저자는 HN 답글에서 두 에이전트가 `rig send`와 `rig capture`로 서로의 터미널에
타이핑하고 화면을 보며,
사용자가 명령을 치는 것과 똑같이 동작한다고 설명했다[^mschwarz-pair].
API 이벤트 스트림으로 돌리는 Claude Managed Agents와 OpenRig를 가르는 지점도
여기다.

대가는 전달의 불확실성이다.
붙여 넣은 텍스트가 실제로 화면에 그려졌는지,
그 에이전트가 그 내용을 읽고 처리했는지는 별개의 문제다.
`docs/as-built/arteries.md`는 메시지 전달을 작은 변경이 큰 회귀를 부르는
영역으로 꼽고,
빈 셸에 타이핑하는 문제를 막은 수정이
권한 모드를 지정해 띄운 Claude 좌석을 모두 거부하게 만들었고,
그 회귀가 0.6.2에 그대로 실렸다고 기록한다.
같은 문서는 스텁 런타임에 입력 동작이 없어 이 회귀 부류를 테스트할 수 없고,
어떤 시나리오도 좌석이 메시지를 소비했다는 것을 증명하지 못한다고 적는다.
0.6.9 릴리스 노트가 다른 호스트로 보낸 메시지를
실패 대신 전달 미확인으로 보고하고,
재전송 전에 `rig capture`로 먼저 확인하라고 하는 것도 같은 문제의 다른 얼굴이다.
큐를 따로 두는 설계는 이 불확실성 위에서 일의 기록만큼은 확실히 남기려는
선택으로 읽힌다.

### 모두가 같은 기계를 공유하면 마찰도 경계도 없다

HN에서 NBenkovich는 tmux를 쓰면 모든 에이전트가
같은 네트워크와 파일 시스템을 공유하지 않느냐고 물었다[^NBenkovich].
저자는 OpenRig가 아직 그 문제를 풀려 하지 않으며,
사용자가 통제하는 호스트에서 에이전트들이 마찰 없이 함께 일하도록 같은
네트워크와 파일 시스템을 쓰기를 원한다고 가정한다고 답했다[^mschwarz-isolation].

이 가정은 협업에는 맞지만 피해 반경을 키운다.
한 좌석이 잘못된 명령을 실행하면 다른 좌석의 작업 디렉터리와 `.git`도 같은
사용자 권한 아래에 있다.
Codex 좌석이 작업 공간의 `.git`과 팟의 공유 큐 상태 디렉터리에 쓰기 권한을 받는
것도 그 예다.
엣지 문서는 엣지가 권한을 통제하지 않는다고 명시하므로,
`can_observe`로 선언한 리뷰어도 기술적으로는 무엇이든 할 수 있다.
격리가 필요하면 OpenRig 바깥에서, 예를 들어 VM이나 별도 사용자 계정으로 해결해야
한다.

### 오래 사는 좌석은 문맥을 쌓지만 잘못된 판단도 쌓는다

저자의 핵심 주장은 좁은 역할에 오래 머문 에이전트가 하루 사이에도 눈에 띄게
나아진다는 것이다.
HN에서 그는 에이전트 10개가 각각 100만 토큰 컨텍스트를 가지면
리그 전체를 1,000만 토큰 컨텍스트처럼 다룰 수 있다고까지
말했다[^mschwarz-context].

반대 경험도 같은 스레드에 있다.
unsaved159는 오픈소스 프로젝트 유지보수에 에이전트 무리를 써 보니 80% 정도는
자율로 해냈지만,
PR마다 직접 검토하고 다시 에이전트와 고쳐야 해서 결국 혼자 하는 것과 시간이
비슷했다고 적었다[^unsaved159].
그는 에이전트가 한 번 실수하면 그 위에 쌓이는 작업 때문에 아키텍처가 눈덩이처럼
혼돈으로 굴러간다고 했다.
저자도 그 눈덩이에 공감한다고 답하며, Claude는 의도를 잘 이해하지만 실수가 많고
Codex는 실수가 적지만 과하게 설계한다면서
Codex가 Claude를 리뷰하게 하고 TDD로 변경마다 관문을 두는 짝 구성을
권했다[^mschwarz-pair].
토큰 수를 더하는 계산은 문맥이 서로 맞물린다는 가정에서만 성립한다.
열 개의 컨텍스트 창은 하나의 큰 창이 아니라
서로 다른 판단을 가진 열 개의 기억이고,
그 사이를 잇는 것은 tmux 메시지와 큐 기록이다.

### 사람의 주의는 좌석 수만큼 늘지 않는다

저자는 첫 Show HN 답글에서 에이전트 4~5개를 넘으면 흐름을 놓친 느낌이 든다고
인정했다[^mschwarz-ha].
그래서 오케스트레이터 둘을 고가용성 쌍으로 두고 리드 하나와만 대화하며,
짝은 리드의 머릿속 모델을 실시간으로 흡수했다가 리드의 컨텍스트가 바닥나면
넘겨받는다고 설명했다.
가장 오래 연속으로 돌린 리그는 약 4일이었고,
아침에 데모 영상을 보고 PR을 표본 검사하는 방식으로 일한다고 했다.

이 구조는 사람의 검토를 없애지 않고 위치를 옮긴다.
사람은 코드 한 줄 한 줄이 아니라 스펙에서 벗어나는지,
이상한 예외가 생기는지를 본다.
홈페이지의 109좌석 명단은 이 방식이 얼마나 커질 수 있는지 보여 주지만,
같은 명단에서 활동 중인 좌석은 13개였다는 점도 함께 읽어야 한다.

## 비평

### 블로그가 출시했다고 말한 연속성 기능은 현재 문서상 아무 일도 하지 않는다

4월 블로그 글은 팟 구성원이 상태를 공유 메모리에 꺼내 두고,
한 에이전트가 컴팩션되면 나머지가 그것을 복원한다는 머릿속 모델 고가용성을
내세웠다.
재개할 수 없는 에이전트는 공유 메모리와 파일 시스템 산출물로 재구성한다고 했고,
연속성 정책을 가진 팟을 Managed Agents에 없는 이미 출시된 기능으로 꼽았다.

그런데 현재 `docs/reference/rig-spec.md`는 `continuity_policy`가 검증되고 팟에
저장되며 내보낼 때 다시 쓰이지만,
이 버전에서는 `sync_triggers`, `artifacts`,
`restore_protocol` 중 어느 것에도 반응하는 코드가 없다고 적는다.
YAML에 `restore_protocol.peer_driven: true`를 써도 동료가 복원을 이끄는 일은
일어나지 않는다는 뜻이다.
블로그 글도 성숙도는 제각각이라고 단서를 달았지만,
기능 목록과 실제 동작 사이의 거리를 사용자가 직접 문서에서 찾아야 한다.
저자가 첫 Show HN에서 자기 설정은 저장소와 npm 패키지보다 앞선 설정 계층으로
기능을 시제품화한다고 밝힌 것과 겹쳐 보면,
저자가 경험한 OpenRig와 사용자가 설치하는 OpenRig가 다를 수 있다.

### 선언형 토폴로지는 의도를 적을 뿐 강제하지 않는다

RigSpec은 인프라를 코드로 정의하듯 에이전트 토폴로지를 정의한다고 소개된다.
하지만 엣지 문서에 따르면 다섯 엣지 중 런타임에 영향을 주는 것은
`delegates_to`와 `spawned_by` 둘뿐이고,
그것도 실행 순서와 큐 에스컬레이션에 한정된다.
엣지는 메시지를 라우팅하지 않고, 위임을 강제하지 않고, 권한을 통제하지 않는다.
문서는 이것을 의도적으로 런타임보다 풍부한 어휘라고 설명한다.

Terraform 비유가 성립하려면 선언한 상태와 실제 상태의 차이를 도구가 맞춰 줘야
한다.
OpenRig에서 그 일을 하는 것은 대부분 에이전트가 읽는 문장이다.
`CULTURE.md`, 좌석 지침, `rig whoami --json`이 보여 주는 엣지 정보를 에이전트가
해석해 따르는 것이고,
그래서 토폴로지의 품질은 YAML보다 그 안의 문장과 모델의 순종에 달려 있다.
권한 정책도 같은 구조다.
설정 면 정책은 기록만 되고, 실제 효력은 에이전트가 스킬을 따라 네이티브 설정을
고쳐야 생긴다.

### 비교 실험을 약속하지만 측정 장치는 아직 없다

블로그 글은 어떤 프레임워크든 RigSpec으로 재현할 수 있다면 같은 과제,
같은 기계에서 정면 비교할 수 있고,
지금은 모두 감으로 판단한다고 말한다.
이 약속은 OpenRig를 하나의 패턴이 아닌 원시 요소로 보게 만드는 근거다.

그러나 저장소에서 확인할 수 있는 근거는 저자의 경험담이다.
`packages/test-system`에는 실제 모델 평가 케이스가 있지만,
그것은 OpenRig 자체의 동작을 검사하는 용도이고 토폴로지끼리의 산출물을 비교한
결과는 공개되어 있지 않다.
Claude와 Codex를 짝지으면 상당히 더 정확해진다는 주장도 저자의 관찰로만
제시된다.
HN의 jonnyasmar가 토폴로지가 새로운 문제 해결 방식을 열었는지,
주로 정리용 장식인지 물은 것도 이 지점이었다[^jonnyasmar].

### 문서 대부분이 에이전트를 독자로 쓰여 사람이 판단하기 어렵다

README는 설치를 맡은 에이전트에게 따로 지시하는 단락을 두고,
변경 노트는 방금 업그레이드된 설치의 에이전트를 위한 문서라고 스스로 밝힌다.
블로그 글도 에이전트에게 문서를 가리키고 만들고 싶은 것을 말하면 나머지는
에이전트가 알아낸다고 권한다.
에이전트가 쓰기 좋은 CLI와 문서라는 방향 자체는 설득력이 있다.

문제는 그 문서가 바로 사람이 결정을 내려야 하는 곳이라는 점이다.
README의 권한 단락은 팀 기본값, 커널 기본값, 다섯 정책, 좌석별 모드,
레거시 환경 변수, 비중단 모드가 한 덩어리로 얽혀 있다.
설치 과정 대부분을 에이전트에게 맡기면 그 에이전트가 사용자의 홈 디렉터리 설정과
신뢰 기록을 바꾸는 동안,
사람은 무엇이 바뀌었는지 직접 읽지 않게 된다.
README가 백업을 권하는 것은 정직하지만, 모든 변경에 대화형 미리 보기가 있지는
않고 `rig setup --dry-run`이 이후 시작 시점의 효과를 모두 보여 주지는 않는다는
문장도 같은 README에 있다.

## 함정

- `rig setup --dry-run`은 설정 단계의 계획만 보여 준다. 데몬 시작과 좌석 실행 때 쓰이는 훅, 신뢰 기록, 스킬은 미리 보기에 다 나오지 않는다.
- 데몬은 시작만 해도 `~/.claude/skills`와 `~/.agents/skills`에 스킬을 넣고, 기본 설정에서는 리그를 띄우기 전에도 Codex 훅과 신뢰 기록을 쓴다.
- 기존 Claude 상태 줄 명령과 신뢰 항목은 교체될 수 있다. README는 이것이 완전한 보존이나 롤백 보장이 아니라고 적는다.
- `kernel`의 Codex 좌석은 정책이 없으면 샌드박스와 승인 없이 돈다.
- `builtin:standard`는 이름과 달리 원격 push를 묻지 않고 허용한다. 묻는 것은 PR, 배포, 병합, 강제 push, 파괴적 작업이다.
- `rig seat set-permissions`는 다음 실행부터의 선택을 기록할 뿐 지금 도는 프로세스를 바꾸지 않는다. `rig seat status`의 값도 네이티브 강제를 증명하지 않는다.
- `continuity_policy`는 검증되고 저장되지만 현재 아무 동작도 하지 않는다.
- 호스트를 재부팅하면 tmux 세션이 사라진다. 커널 리그의 설명에 따르면 그때는 운영자 팟이 에이전트 재시작을 맡는다.
- 재개할 수 없는 좌석은 `awaiting-decision`으로 멈추고, 새로 시작할지는 사람이 `--fresh`로 정해야 한다.
- 다른 호스트로 보낸 메시지가 시간 초과로 끝나도 실제로는 도착했을 수 있다. 재전송 전에 `rig capture`로 대상 화면을 먼저 본다.
- 엣지는 메시지 라우팅도 권한도 통제하지 않는다. 리뷰어를 `can_observe`로 선언해도 쓰기를 막지 못한다.
- 0.x 버전이며 릴리스가 거의 매일 나온다. 업그레이드 중에 `rig down`은 업그레이드 단계가 아니라고 문서가 경고한다.

## 기억할 원칙

### 에이전트를 세션이 아니라 주소로 다룬다

OpenRig에서 가장 오래 쓸 만한 생각은 좌석이다.
대화 세션은 컨텍스트가 차면 끝나고 재부팅하면 흩어지지만,
`dev-build@starter`라는 주소와 그 주소에 딸린 역할, 지침, 큐 기록은 남는다.
사용자와 다른 에이전트가 세션 대신 주소에 말을 걸면,
세션이 바뀌어도 일의 연속성이 주소 쪽에 쌓인다.
OpenRig를 쓰지 않더라도 여러 에이전트를 돌린다면 이름 붙인 역할,
고정된 작업 디렉터리, 채팅과 분리된 작업 기록부터 갖추는 것이 같은 효과를 낸다.

### 선언과 강제를 구분해서 읽는다

YAML에 적힌 엣지와 정책은 의도의 기록이고,
실제로 무엇이 강제되는지는 별도로 확인해야 한다.
OpenRig 문서는 이 구분을 정직하게 적어 두었다.
엣지는 실행 순서만, 설정 면 정책은 기록만, 연속성 정책은 저장만 한다.
에이전트 팀의 안전은 결국 런타임의 네이티브 권한, 샌드박스,
호스트 경계에서 나오며,
토폴로지 선언이 그 경계를 대신해 주지 않는다.

---

[^mschwarz-pair]: <https://news.ycombinator.com/item?id=47787508>

[^NBenkovich]: <https://news.ycombinator.com/item?id=48308790>

[^mschwarz-isolation]: <https://news.ycombinator.com/item?id=48313131>

[^mschwarz-context]: <https://news.ycombinator.com/item?id=48299190>

[^unsaved159]: <https://news.ycombinator.com/item?id=47787185>

[^mschwarz-ha]: <https://news.ycombinator.com/item?id=47782107>

[^jonnyasmar]: <https://news.ycombinator.com/item?id=48245221>
