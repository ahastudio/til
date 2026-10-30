# pstack: 에이전트를 병렬로 돌려도 품질을 지키려는 스킬 모음

<https://github.com/cursor/plugins/tree/main/pstack>

HN 토론: <https://news.ycombinator.com/item?id=49523858> (1점, 0개 댓글)

## 소개

pstack은 Cursor 플러그인 저장소 `cursor/plugins`의 `pstack/` 디렉터리에 들어
있는 스킬(skill) 묶음이다.
README 첫머리에서 작성자는 자신을 poteto라고 소개하고,
목표가 코드의 양을 늘리는 것이 아니라 더 적고 더 좋은 코드를 쓰게 하는 것이라고
밝힌다.
`plugin.json`의 작성자 항목은 Lauren Tan이다.
README는 이 스킬들이 작성자가 Cursor에서 매일 쓰는 것과 같다고 말한다.
이 주장은 제작자의 말이고, 이 글이 확인한 범위는 저장소의 코드와 문서가 서로
맞는지까지다.

2026년 10월 29일에 `main`의 커밋 `1ba91fc`(커밋 날짜 2026-10-28, 버전 0.15.36)를
받아 읽었다.
`pstack/` 아래 파일은 573개다.
스킬 디렉터리는 58개이며, 슬래시 명령으로 쓰는 스킬 34개와 원칙(principle) 스킬
24개로 나뉜다.
플레이북(playbook)은 23개, 서브에이전트(subagent) 정의는 2개다.
스킬 58개 가운데 57개가 `disable-model-invocation: true`이고 `setup-pstack`만
아니다.
이 설정은 모델이 스스로 스킬을 고르지 못하게 하므로,
스킬은 사용자가 이름을 입력하거나 다른 스킬이 파일을 읽을 때만 실행되는 구조다.

이 문서는 사용법 안내가 아니라 코드를 읽은 기록이다.
저장소에서 실제로 실행되는 코드는 TypeScript와 셸과 Node 스크립트 몇 묶음이고,
나머지 대부분은 에이전트가 읽는 마크다운 지시문이다.
이 비율이 pstack의 성격을 결정하므로 먼저 구성을 본다.

## 저장소 구성

| 위치                                | 내용                                                                                |
| ----------------------------------- | ----------------------------------------------------------------------------------- |
| `skills/poteto-mode/SKILL.md`       | 진입 스킬. 트리거 목록, 원칙 색인, 서브에이전트 규칙, 응답 작성 규칙, 플레이북 목록 |
| `skills/poteto-mode/playbooks/`     | 작업 종류별 절차 23개                                                               |
| `skills/principle-*/SKILL.md`       | 원칙 24개. 파일 하나에 규칙 하나                                                    |
| `skills/<그 밖의 명령>/`            | `how`, `why`, `arena`, `swarm`, `interrogate`, `tdd`, `unslop` 등 34개 명령         |
| `agents/`                           | `poteto-agent`, `comment-sicko`                                                     |
| `skills/poteto-mode/scripts/`       | `watch-pr`(TypeScript), `check-plan.mjs`, `worktree-audit.sh`                       |
| `skills/show-me-your-work/scripts/` | 결정 기록용 `log.sh`                                                                |
| `skills/statechart/scripts/`        | TLA+ 모델을 Mermaid 상태 차트로 바꾸는 TypeScript 파이프라인                        |
| `docs/guide/`, `docs/harness/`      | 가이드 10편, Claude Code 어댑터                                                     |
| `automations/benny/`                | Slack 버그 제보를 분류하고 고치는 휴면 상태의 자동화 묶음                           |

저장소 루트의 `scripts/`에는 pstack 문서를 검사하는 `check-pstack-docs.mjs`와
Claude Code용 복사본을 만드는 `generate-pstack-harness-trees.mjs`가 있다.
이 두 스크립트가 마크다운 스킬 묶음의 일관성을 코드로 지키는 장치다.

## 동작 방식

### 진입점과 플레이북

`/poteto-mode`는 사용자의 요청을 읽고 플레이북 23개 가운데 하나를 골라
그 절차를 할 일 목록(todo list)의 첫 항목으로 그대로 옮긴 뒤 실행한다.
플레이북은 조사(investigation), 버그 수정(bug fix), 성능(perf), 점진적 지표
개선(hillclimb),
기능(feature), 리팩터링(refactoring), 프로토타입(prototype), PR 감시(babysit),
병합(shipping), 자동 운영(autopilot-full, autopilot-stack) 같은 작업 단위다.
요청에 맞는 플레이북이 없으면 `figure-it-out` 스킬이 그 작업에 맞는 절차를 새로
설계한다.

`poteto-mode`의 “Non-negotiables” 절은 트리거를 조건과 행동의 쌍으로 적는다.
첫 메시지에서는 사용자의 목표와 문제와 예상하는 가장 작은 변경을 자기 말로 다시
설명해야 하고,
확인을 기다리지 않는다.
코드를 쓰기 전에는 데이터 모양(data shape)부터 이름 붙이고,
함수 경계를 넘는 코드는 `architect`로, 논쟁이 있는 설계는 `interrogate`로
보낸다.
“어느 방식이 좋을까” 같은 질문은 실행해 보면 관찰할 수 있는 사실인지 먼저
가르고,
관찰할 수 있으면 사람에게 묻지 않고 프로토타입으로 결정한다.
되돌릴 수 있는 작업은 묻지 않고 진행하며, 강제 푸시, 배포, 데이터 삭제 같은
되돌릴 수 없는 쓰기에서만 멈춘다.

### 서브에이전트 규칙

서브에이전트를 띄우는 규칙이 파일에서 가장 구체적이다.
모든 `Task` 호출은 `run_in_background: true`로, 에이전트 모드로, 파일 포인터만
넘기고,
역할마다 모델을 명시해서 띄운다.
기본 모델은 코드 위임에 `grok-4.7-xhigh-fast`, 어려운 변경과 글과 판단에
`claude-opus-5-5-xhigh`다.
새 작업은 기본적으로 새 서브에이전트에게 맡기고, 이어받기(resume)는
그 에이전트의 로컬 체크아웃이나 미커밋 변경, 아직 도는 프로세스가 꼭 필요할 때만
허용한다.
이유로 적힌 것은 연쇄적으로 이어받으면 지시가 조용히 빠진다는 점이다.

`poteto-agent`는 위임받은 서브에이전트의 래퍼(wrapper)로,
작업을 시작하기 전에 `poteto-mode/SKILL.md`를 처음부터 끝까지 읽도록 강제한다.
`generalPurpose`로 대체하면 이 읽기가 빠져 스타일이 흐트러진다고 정의 파일이
직접 경고한다.
`comment-sicko`는 읽기 전용 주석 검토 에이전트이고, 정의 파일은 주석 삭제를
집요하게 요구하는 캐릭터 대사로 쓰여 있다.
이 에이전트는 코드를 고치지 않고 주석 삭제 개수와 `MUST KILL` 표시만 보고한다.

### 병렬 스킬

`arena`는 같은 과제를 N개의 후보가 풀게 하고 기준표(rubric)로 기본안을
고른 다음,
진 후보에서 쓸 만한 부분만 접목(graft)한다.
교차 판정자는 부모 모델과 다른 계열에서 고르게 되어 있다.
`swarm`은 조각을 나누거나 같은 지시로 경주시키고, 결과를 `PASS`, `ISSUES`,
`BLOCKED` 중 하나로 받아 한 표로 모은다.
`interrogate`는 서로 다른 모델이 변경을 깨뜨리려 시도하고,
실행으로 증명된 결함만 남기며 수정은 하지 않고 보고만 한다.
그 증명은 실패하는 테스트나 재현 스크립트, 잘못된 동작을 보여 주는 명령
출력이어야 한다.

## 코드로 보는 watch-pr

`skills/poteto-mode/scripts/watch-pr/`는 PR 하나, 연결된 스택, 고정된 큐의
상태를 감시하는 TypeScript 도구다.
`babysit`과 `shipping` 플레이북이 이 도구를 `/loop` 아래에서 돌리라고 지시한다.
`github.ts`(726줄), `policy.ts`(842줄), `types.ts`(414줄), `cli.ts`(223줄),
`render.ts`(169줄)로 되어 있고,
GitHub와의 통신은 전부 `gh` 명령을 자식 프로세스로 호출해서 처리한다.
의존성은 `commander` 14.0.0 하나이고 개발 의존성은 `bun-types`와
`typescript`다(둘 다 `latest`).

### 막는 순서

`classifyPr`는 PR 한 건을 다음 순서로 검사해서 첫 번째로 걸린 것을 차단 사유로
돌려준다.
충돌(conflict), 해결되지 않은 리뷰 스레드(review thread), 실패한 CI, 병합
게이트(merge gate) 순이다.
넷 모두 아니고 CI가 진행 중이면 대기(waiting)이고, 모두 깨끗하면
준비됨(ready)이다.
리뷰 스레드는 작성자가 누구든 해결되지 않았으면 막는다.
Bugbot 여부는 `isBugbot`이 판별해 표시만 하고, 막는지는 판별과 무관하다.

병합 게이트는 PR이 닫힌 채 병합되지 않았거나, 초안(draft)이거나, 리뷰 결정이
`CHANGES_REQUESTED`일 때다.
단 초안이더라도 CI가 아직 진행 중이면 막지 않고 기다린다.
`--allow-draft`를 주면 초안은 게이트가 아니다.

스택에서는 같은 검사를 “층 우선(tier-major)”으로 적용한다.
`selectTierMajorStackDecision`은 모든 PR의 충돌을 먼저 보고, 그다음 모든 PR의
스레드를, 그다음 CI를 보고,
그 뒤에 게이트를 보고, 마지막으로 가장 아래의 진행 중인 PR을 기다린다.
그래서 윗 PR의 충돌이 아랫 PR의 CI 실패보다 먼저 보고된다.
`policy.test.ts`에는 윗 PR의 충돌이 맨 아래 PR의 CI보다 우선한다는 테스트가
있어서, 이 순서는 의도된 동작이다.

### 검사 결과 분류

체크는 먼저 `gh pr checks`의 `bucket` 값으로 읽고(빠른 경로),
쓸 수 없으면 GraphQL의 `statusCheckRollup`을 100개씩 페이지로 넘겨 읽는다.
GraphQL 경로는 `CheckRun`의 `status`와 `conclusion`, `StatusContext`의 `state`를
각각 풀어서
통과(passed), 건너뜀(skipped), 실패(failed), 진행 중(pending)으로 나눈다.
`ACTION_REQUIRED`는 실패로 본다.

이름이 정확히 `Code Review Gate`인 체크는 어느 쪽도 아닌 별도
종류(`code-review-gate`)로 뺀다.
코드 주석의 이유는 이렇다.
소유자 승인을 기다리는 게이트를 진행 중이나 실패로 세면 감시기가 사람을 기다리게
되기 때문이다.
이 이름은 코드에 문자열로 고정되어 있어서, 다른 저장소의 승인 체크에는 적용되지
않는다.

`assessGitHubMerge`는 GitHub이 병합을 거절한 상황을 CI 목록과 따로 판단한다.
`mergeStateStatus`가 `BLOCKED`이고 머리 커밋의 롤업 상태가 `ERROR`나
`FAILURE`이면 거절(refused)이고,
이때는 실패한 체크가 목록에 하나도 없어도 `ci-github-rejected`로 분류해 CI 차단
사유로 올린다.
`BLOCKED`이지만 롤업이 실패가 아니면 필수 리뷰 같은 다른 이유일 수 있으므로
거절로 세지 않는다.

### 재시도와 종료 코드

조회가 실패해도 곧바로 끝내지 않는다.
재시도할 수 있는 오류(`retryable`)는 연속 `--max-query-errors`(기본 5)번까지
지수 백오프로 다시 시도한다.
대기 시간은 `min(max(interval, 60) * 2^(n-1), 300)`초라서 간격을 10초로 줘도 60,
120, 240, 300초로 늘어난다.
PR URL을 해석하지 못하는 오류(`invalid-context-url`)는 재시도하지 않는다.

출력은 기본이 줄 단위 JSON(NDJSON)이고 이벤트마다 `schemaVersion`, `sequence`,
`observedAt`, `mode`가 붙는다.
종료 코드가 의미를 가진다.

| 종료 코드 | 이벤트                        | 뜻                                     |
| --------- | ----------------------------- | -------------------------------------- |
| 0         | `READY`, `COMPLETE`, `STATUS` | 준비됨, 큐의 모든 PR 병합, 상태만 출력 |
| 2         | `BLOCKER`                     | 병합 충돌                              |
| 3         | `BLOCKER`                     | 해결되지 않은 리뷰 스레드              |
| 4         | `BLOCKER`                     | 실패한 체크 또는 GitHub의 병합 거절    |
| 5         | `TIMEOUT`                     | `--timeout` 초과                       |
| 6         | `BLOCKER`                     | 병합 게이트                            |
| 7         | `BLOCKER`                     | 조회 실패 한도 초과                    |
| 64        | 없음                          | 인자 오류                              |

종료 코드를 에이전트가 읽는 계약으로 쓰는 설계다.
표에 `1`이 없다는 점만 코드에서 확인되고, 이유는 적혀 있지 않다.

### 스택과 큐

`--stack`은 열린 PR 목록에서 기준 PR의 아래쪽(부모)과 위쪽(자식)을 찾아 스택을
구성한다.
`orderStack`은 베이스 브랜치 이름과 같은 헤드 브랜치를 가진 PR을 부모로 보되,
포크에서 온 PR(`isCrossRepository`)은 부모 후보에서 뺀다.
이름이 같아도 포크의 브랜치는 이 저장소의 브랜치가 아니기 때문이다.

`--queued-stack --stack-prs 101,102,103`은 아래에서 위로 고정한 큐를 끝까지
감시한다.
상태는 두 종류의 읽기를 번갈아 한다.
가장 아래 미병합 PR(frontier)만 자주 읽는 `frontier-poll`과,
`--sweep-interval`(기본 300초)마다 큐 전체를 읽는 `whole-stack-sweep`이다.
앞쪽 PR이 병합되어 frontier가 바뀌면 `ADVANCE` 이벤트를 내고,
같은 대기 상태는 키(`pending:<번호>:<개수>`)가 바뀔 때만 다시 알린다.
그래서 긴 대기 중에도 이벤트 줄이 불어나지 않는다.
모든 PR이 병합되면 `COMPLETE`다.

### 직접 확인한 것

의존성을 `--ignore-scripts`로 설치하고 `bun test watch-pr
check-plan.test.ts`를 돌리니
4개 파일에서 61개 테스트가 통과하고 실패는 없었다.
`bun watch-pr/watch-pr --help`는 위 옵션 목록을 출력했고,
`--stack-prs`를 `--queued-stack` 없이 주면
`error: --stack-prs requires --queued-stack`을 내고 종료 코드 64로 끝났다.
`gh`로 실제 PR을 조회하는 경로는 실행하지 않았다.

## 기록과 정리 스크립트

### log.sh: 결정 기록을 TSV로 남기는 42줄

`show-me-your-work`의 `log.sh`는 `ts`, `phase`, `decision`, `why`, `evidence`,
`result` 여섯 열의 TSV에 행을 덧붙인다.
파일이 비어 있으면 머리글 행을 먼저 쓴다.
셀 안의 탭과 줄바꿈과 캐리지 리턴은 공백으로 바꾼다.
셀이 `=`, `+`, `-`, `@`로 시작하면 앞에 작은따옴표를 붙인다.
스크립트 주석이 밝히는 이유는, 이 기록을 스프레드시트로 열 때
PR 제목이나 파일 이름처럼 외부에서 온 증거 문자열이 수식으로 실행되지 않게
하려는 것이다.
머리글은 `>>`로만 쓰고 `>`로 덮어쓰지 않는데, 이유도 주석에 있다.
네트워크 마운트에서 존재하는 파일을 비어 있다고 오판하면 머리글이 한 줄 더 생길
뿐 행이 사라지지는 않는다.

`=HYPERLINK(1)`과 `-cmd`를 증거 칸에 넣어 실행하니 두 셀이 각각
`'=HYPERLINK(1)`, `'-cmd`로 기록되었고,
탭이 든 셀은 공백 하나로 바뀌었다.

### worktree-audit.sh: 읽기 전용 정리 후보 분류

`worktree-audit.sh`는 `git worktree`마다 크기, 나이, 병합 여부, 변경 여부, 원격
상태, PR 상태, 마지막 채팅 날짜를 표로 만든다.
스크립트 머리 주석이 삭제는 사람이 확인하는 단계로 남긴다고 적고, 코드에도 삭제
명령이 없다.
버킷(bucket) 규칙은 다음 순서다.

1. 추적 중인 파일에 변경이 있으면 `hold-wip`.
2. PR이 열려 있거나 초안이면 `hold-open-pr`.
3. 최근 4일 안에 그 워크트리에서 작업한 채팅 기록이 있으면 `verify-recent-chat`.
4. 베이스에 병합되었거나 PR이 하나라도 있으면 `safe`.
5. 그 밖에는 `review`.

스쿼시 병합은 헤드가 베이스의 조상이 되지 않으므로 병합
여부(`merge-base --is-ancestor`)만으로는 잡히지 않는다.
코드 주석이 이 점을 알고 PR 상태를 실제 신호로 쓴다고 설명한다.
채팅 기록은 `~/.cursor/projects/<경로를 바꾼 슬러그>/agent-transcripts`에서
`rg`로 찾는다.
이 경로는 Cursor에 묶여 있다.

이 스크립트는 실행하지 않았고, 아래 두 가지는 코드를 읽고 추론한 것이다.
첫째, 4번 조건의 “PR이 하나라도 있으면”은 닫혔지만 병합되지 않은 PR도 포함한다.
버킷 계산은 `remote` 열(원격보다 앞선 커밋 수)을 쓰지 않으므로,
닫힌 PR이 있고 추적 파일이 깨끗하며 원격보다 커밋이 앞선 워크트리도 `safe`가 될
수 있다.
둘째, 추적하지 않는 파일만 있는 상태는 “버려도 되는 임시 파일”(`scratch`)로 보고
`safe`를 막지 않는다.
이것은 코드에 적힌 의도지만, 삭제하면 그 파일은 사라진다.
이 스크립트에는 테스트도 없다.
`poteto-mode/scripts/`에서 테스트 파일이 있는 것은 `watch-pr`와
`check-plan.mjs`뿐이었다.

### check-plan.mjs: 계획 문서를 형식으로 검사

`multi-phase-plan` 플레이북의 6단계는
`node pstack/skills/poteto-mode/scripts/check-plan.mjs <plan.md>`를 실행해서
출력되는 줄을 모두 고치라고 지시한다.
이 검사기는 계획 문서가 정해진 뼈대를 갖췄는지 정규식으로 확인한다.

- H1과 10줄 미만의 도입부, 그리고 `## How to read this`, `## Program checklist`, `## Close the program` 절.
- PR 절마다 굵은 소제목 9개(`Depends on.`, `Files.`, `Build.`, `You see.`, `Verify, unit.`, `Verify, live.`, `Verify, perf.`, `Review gate.`, `Merge.`)가 이 순서로 있어야 한다.
- `Verify, live.`에는 “Ten lanes on `<모델>` at the PR head” 문구와 `Lane 1.`부터 `Lane 10.`까지의 상자(box)가 있어야 하고, 각 레인에는 ``Save `파일명` ``과 `Pass when`이 있어야 한다.
- `Verify, perf.`의 상자는 `Metric.`, `Probe.`, `Baseline.`, `Rule.` 순서다.
- 코드 블록 바깥에서 긴 줄표(en dash, em dash)와 둥근 따옴표와 문장 중간의 `: `를 금지한다.

펜스(fence) 안과 인라인 코드를 건너뛰는 파서를 직접 쓴 점이 눈에 띈다.
빈 계획 파일(`# t`와 본문 한 줄)을 넣으니 네 가지 문제를 출력하고 종료 코드 1로
끝났다.
이 검사기가 확인하는 것은 문구와 순서의 존재이지 내용의 타당성이 아니다.
레인에 `Pass when`이라는 문자열이 있는지는 보지만, 그 조건이 검증 가능한지는
보지 못한다.
또 6단계의 경로 `pstack/skills/...`는 `cursor/plugins` 저장소 안에서만 맞는 상대
경로이므로,
플러그인으로 설치된 곳에서는 그대로 실행되지 않을 것이다.
이 마지막 부분은 경로 문자열을 읽고 한 추정이다.

## 문서와 이식 검사

### check-pstack-docs.mjs

이 스크립트(152줄)는 README와 가이드가 트리와 어긋났는지 검사한다.
확인하는 항목은 다음과 같다.

- “the twenty-three playbooks” 같은 개수 주장이 실제 파일 수와 같은지(`all`, `the`, `has`, `of`, `ships`, `with` 중 하나로 시작하는 표현만 대상).
- 문서가 언급하는 모든 `/명령`이 `pstack` 스킬, `cursor-team-kit` 스킬, 허용 목록의 내장 명령 중 하나인지.
- 상대 링크와 `#앵커`가 실제 파일과 제목에 대응하는지.
- `subagent_type: "..."`가 `agents/`에 있는 이름인지.
- 문서에 적힌 모델 이름이 `setup-pstack`에 있는지.
- README가 모든 스킬과 플레이북과 에이전트를 나열하는지.

저장소를 받아 실행하니
`tree: 58 skills (34 commands, 24 principles), 23 playbooks, 2 agents`,
`358 slash mentions, 256 relative links`, `0 problems`가 나왔다.
문서의 개수와 이름과 링크가 코드로 검증되는 저장소라는 점이 확인된다.
`babysit`를 `autopilot`으로 이름이 바뀐 명령으로 따로 기록해 두고, 옛 이름이
남아 있으면 실패시키는 규칙도 있다.

### generate-pstack-harness-trees.mjs

Cursor는 `pstack/`를 그대로 쓰고, Claude Code는 `harness/pstack/claude-code/`에
생성된 복사본을 설치한다.
생성기(188줄)는 스킬이 Cursor 전용 이름을 쓰는지 정규식 22개로 분류한다.
`Task`, `AskQuestion`, `generalPurpose`, `run_in_background`, `grok-`,
`.cursor/rules/`, `agent-transcripts`, Bugbot 같은 것들이다.
Cursor 이름을 쓰는 스킬은 H1 바로 아래에
“Claude Code에서는 이 스킬을 따르기 전에 어댑터를 세션당 한 번 읽어라”는 줄을
삽입한다.
복사본에 없는 파일로 가는 상대 링크는 GitHub `main`의 주소로 바꿔 쓴다.
`--check` 옵션을 주면 디스크의 생성물과 새로 만든 결과를 바이트 단위로 비교해서
다르면 실패한다.
README는 CI가 생성물이 낡으면 실패한다고 설명한다.
나는 `--check`만 실행했고 `harness/pstack is up to date.`가 나왔다.

어댑터(`docs/harness/claude-code.md`)의 대응표에서 눈에 띄는 것은 다음이다.

- `Task`는 `Agent`로, `generalPurpose`는 `general-purpose`로 바뀐다.
- `readonly: true`는 `Explore`에 대응하지만, `Explore`가 `Bash`를 유지하므로 지시문에 “파일을 고치지 말라”를 넣고 끝난 뒤 `git status`로 확인하라고 적었다.
- `environment: "cloud"`는 `isolation: "worktree"`로 바뀐다.
- `model`은 `opus`, `sonnet`, `haiku`, `fable`만 받으므로 `claude-opus-5-5-xhigh`는 `opus`와 `effort: "xhigh"`가 된다.
- `grok-*`와 `gpt-*` 같은 Claude 이외의 슬러그는 `model`을 생략해서 세션 모델로 돌린다.
- Bugbot, Cursor 자동화(Automations), 클라우드 에이전트, 내장 PR 도구가 필요한 단계는 한 줄만 남기고 건너뛴다.
- 다른 pstack 스킬을 부를 때는 `Skill` 도구가 대부분 거부하므로 `SKILL.md`를 `Read`로 읽는다.

## statechart: 모델 검사를 차트로 바꾸는 파이프라인

`statechart`는 pstack에서 가장 큰 실행 코드다.
`scripts/` 아래 TypeScript가 `ir.ts`(547줄), `run.ts`(481줄),
`regions.ts`(295줄), `config.ts`(276줄), `label.ts`(269줄) 등으로 나뉘어 있고,
`test/corpus/`에는 `Counter`, `CounterDeadlock` 같은 TLA+ 예제와 기대
출력이 있다.
`SKILL.md`가 설명하는 흐름은 이렇다.

1. 에이전트가 TLA+ 명세(spec)와 설정(config)을 쓴다. 지켜야 하는 규칙은
불변식(INVARIANT)으로 쓴다.
2. 첫 실행 때 mise로 TLC와 Java를 내려받아 설치하므로 네트워크가 필요하다. TLC는
TLA+ 모델 검사기다.
3. `run.ts`가 TLC를 한 워커로 돌린다. 규칙이 깨지면 그 규칙을 설정에서 빼고 다시
돌려, 더 깨지는 규칙이 없을 때까지 반복한다. 처음 깨진 뒤의 실행은 서로 다른
상태 10만 개에서 멈춘다.
4. `pipeline.ts`의 `compile`이 상태 그래프를 걷고(`walk`) 규칙을 깬
경로(`bugs`)를 찾아 가장 짧은 경로 순으로 정렬한다.
5. 뷰(view) 모듈의 `state(vars)`, `step(action, from, to)`, `group(vars)`가 모델
상태와 단계에 사람이 읽는 이름을 붙인다.
6. 병렬 영역(regions)으로 그린 차트가 실제 동작을 왜곡하는지 `regionsLie`로
검사하고, 왜곡하면 부모-자식 상태 표현(`asParents`)으로 다시 그린다.
7. `chart.mmd`(Mermaid), `report.md`, `tlc.out`을 쓴다. 상태가 500개를 넘으면
규칙을 깬 경로만 그리고, 깬 규칙이 없으면 차트를 만들지 않는다.

설계 의도는 TLA+ 명세를 읽지 않는 사람이 상태 차트로 동작을 보고 맞는지 판단하게
하는 것이다.
`SKILL.md`는 버그 경로를 실제 코드에서 한 단계씩 재현해 보고,
재현되지 않으면 모델이 틀렸다고 먼저 의심하라고 적는다.
이 도구는 실행하지 않았다.
첫 실행이 Java와 TLC 내려받기를 요구하기 때문이며, 위 설명은 `SKILL.md`와
`pipeline.ts`를 읽은 결과다.

## 값 정하기

`setup-pstack`은
`~/.cursor/rules/pstack-models.mdc`(Claude Code에서는 `~/.claude/rules/pstack-models.md`)에
역할별 모델을 쓴다.
기본값이 곧 권장값인 구조라서, 지우면 기본값으로 돌아간다.

| 역할                                            | 기본 모델                                       | 근거                                   |
| ----------------------------------------------- | ----------------------------------------------- | -------------------------------------- |
| 기능, 리팩터링, 버그 수정, 성능, hillclimb 코드 | `grok-4.7-xhigh-fast`                           | 코드 위임은 빠른 모델                  |
| 판단과 글, 가장 어려운 변경                     | `claude-opus-5-5-xhigh`                         | 판단과 글은 가장 강한 모델             |
| `arena` 후보, `architect`, `interrogate` 검토자 | `claude-opus-5-5-xhigh`와 `grok-4.7-xhigh-fast` | 계열이 다른 두 모델을 섞어 결과를 대조 |
| `swarm` 워커와 검증                             | `grok-4.7-xhigh-fast`                           | 검증은 모델과 속도를 바꾸지 않는다     |

예산(budget)은 네 단계이고 모델의 추론 강도 토큰을 일괄로 바꾼다.

| 예산      | 추론 강도 |
| --------- | --------- |
| unlimited | `max`     |
| large     | `xhigh`   |
| medium    | `high`    |
| small     | `medium`  |

기본은 `large`다.
기본값의 근거는 README와 `SKILL.md`가 말하는 모델별 강점뿐이고, 비용이나 측정
결과는 저장소에 없다.
빠른(`-fast`) 변형은 CI나 트렁크가 깨졌거나 사람이 지금 기다릴 때만 쓰라고
`poteto-mode`가 정한다.

Claude Code에서는 어댑터가 `grok-4.7-xhigh-fast`를 `inherit-parent`로
대응시킨다.
코드는 빠른 모델에, 판단은 강한 모델에 나누는 기본 분업은
Claude Code에서 모든 역할이 세션 모델로 돌아가는 것으로 바뀐다는 뜻이다.
역할별 분업이 필요하면 `~/.claude/rules/pstack-models.md`에서 직접
`opus xhigh`처럼 지정해야 한다.

## 트레이드오프

### 지시문이 코드의 대부분이다

58개 스킬의 `SKILL.md`만 합쳐도 36,085단어다.
이 지시문이 얼마나 지켜지는지는 모델에 달려 있고, 저장소는 지켜졌는지 확인하는
코드를 일부에만 둔다.
확인 코드가 있는 곳은 `watch-pr`(PR 상태), `check-plan.mjs`(계획 모양),
`log.sh`(기록 형식),
`check-pstack-docs.mjs`와 생성기(문서와 복사본)다.
“증거 없이는 끝났다고 말하지 말라”는 핵심 규칙(`prove-it-works`)은 그 자체가
지시문이어서,
지켜졌는지는 검증 플레이북이 만든 서브에이전트의 보고와 사람의 검토가 확인한다.
이 구조는 `encode-lessons-in-structure`
원칙(같은 지시를 두 번 쓰게 되면 린트나 스크립트로 바꿔라)과 맞지만,
원칙이 적용된 범위는 위 목록에 한정된다.

### 계획을 믿지 않는다면서 계획 검사기를 둔다

README는 계획 스킬이 없는 이유로 가장 좋은 명세는 코드라고 말하고,
계획은 기본이 아니라고 한다.
같은 저장소에 205줄짜리 `check-plan.mjs`와 `multi-phase-plan` 플레이북이 있다.
두 가지는 모순이 아니라 범위의 차이로 읽는 것이 자연스럽다.
계획은 단계가 여럿이거나 PR이 쌓이는 큰 작업에만 쓰고, 그때는 형식을 엄격하게
요구한다는 해석이다.
이것은 코드에서 확인된 사실이 아니라 두 문서를 맞춘 나의 해석이다.
이 엄격함의 대가는 PR마다 10개의 라이브 검증 레인과 성능 상자 4개를 채워야 하는
무거운 계획이다.
검사기는 그 칸이 채워졌는지만 본다.

### 서브에이전트에 맡길수록 검증도 비싸진다

`autopilot-full`은 PR마다 소유 에이전트 하나를 두고, 병합 전에 코드를 쓰지 않은
검증 스웜(swarm)이 증명하게 한다.
플레이북은 작성자가 아닌 쪽의 평결만 인정한다고 명시한다.
작성자는 자신이 만들려던 것을 확인하기 때문이라는 이유다.
이 규칙은 자기 확인 편향을 막는다.
그 대신 PR이 늘수록 검증 에이전트와 CI 실행도 늘어난다고 추정되며, 저장소에는 비용 측정이 없다.
플레이북은 전체 스웜을 코드가 준비된 헤드에서 한 번만 돌리도록 제한한다.
리베이스나 충돌 해결이나 작은 수정에는 검증자 하나만, 문구만 바꾼 변경에는
검증을 생략한다.

## 함정

### watch-pr의 가정이 Cursor 저장소의 관례다

`Code Review Gate`라는 이름과 `bugbot`, `security review`,
`pr review automation` 같은 토큰은 코드에 고정되어 있다.
`isBugbot`은 작성자가 `bugbot`을 포함하거나,
작성자가 `cursor`이면서 본문에 `severity`, `description start` 같은 토큰이 있을
때 참이다.
본문 토큰에 의존하는 판별은 Bugbot의 출력 형식이 바뀌면 조용히 빗나간다.
판별이 빗나가도 스레드가 막는다는 사실은 바뀌지 않으므로 병합 판정은 안전하지만,
`bugbotReviewPasses` 같은 보조 정보는 어긋날 수 있다.
이 도구를 다른 팀의 저장소에 쓴다면 게이트 이름이 다른 경우 게이트가 일반 체크로
분류되어
소유자 승인을 기다리는 상태가 진행 중 체크로 세어질 수 있다.
이것은 코드를 읽고 한 추정이고 실제 저장소에서 확인하지 않았다.

### Cursor 경로가 곳곳에 있다

`skills`와 `agents` 아래에서 `.cursor/`를 언급하는 파일이 20개다.
`poteto-agent`는 경로를 받지 못하면 `~/.cursor/plugins/`에서
`skills/poteto-mode/SKILL.md`로 끝나는 파일을 찾는다.
Claude Code용 복사본은 어댑터가 경로를 번역하지만,
어댑터를 읽는 것도 모델이 세션당 한 번 지켜야 하는 지시다.
읽기 전용(`readonly`) 에이전트가 `Explore`로 바뀌면 `Bash` 때문에 강제력이
약해지고,
어댑터는 그 사실을 인정해 끝난 뒤 `git status`로 확인하라고 한다.

### 자동 병합 권한은 문서가 아니라 사용자의 요청에서 나온다

`poteto-mode`는 “going to bed”나 “run until done” 같은 요청을 완전 자율
권한(full-autonomy grant)으로 읽는다.
README의 예시
`/poteto-mode i'm going to bed. land the stack even if ci flakes.`는
CI가 불안정해도 병합하라는 요청이다.
`shipping` 플레이북은 이 경우에도 독립 평결 없이 병합하지 말라고 하므로 완전히
무방비는 아니다.
그러나 `poteto-mode`의 `Always pause` 목록은 강제 푸시와 배포와 데이터 삭제와
고객 대상 메시지로 한정되고,
병합은 그 목록에 없다.
무엇을 병합까지 허용하는지는 요청 문구가 정하므로, 문구를 쓰는 사람이
책임을 진다.

## 확인하기

아래는 이 글에서 실행해 확인한 명령이다.
설치는 `--ignore-scripts`로 하고, 받은 저장소는 임시 디렉터리에서만 다룬다.

```bash
D=$(mktemp -d) && cd "$D"
git clone --depth 1 https://github.com/cursor/plugins.git
cd plugins

# 문서와 트리가 어긋났는지 검사 (기대: 0 problems)
node scripts/check-pstack-docs.mjs

# Claude Code용 복사본이 최신인지 비교 (기대: harness/pstack is up to date.)
node scripts/generate-pstack-harness-trees.mjs --check

cd pstack/skills/poteto-mode/scripts
bun install --frozen-lockfile --ignore-scripts
bun test watch-pr check-plan.test.ts   # 기대: 61 pass, 0 fail
bun watch-pr/watch-pr --help

# 결정 기록의 수식 방어
cd ../../show-me-your-work/scripts
bash log.sh "$D/log.tsv" build '=HYPERLINK(1)' why '-cmd' ok
cat -vet "$D/log.tsv"   # 두 셀 앞에 작은따옴표가 붙는다
```

PR 하나를 실제로 감시하려면 `gh`가 로그인된 저장소에서 다음처럼 쓴다.

```bash
# 한 번만 상태를 보고 끝낸다
bun watch-pr/watch-pr --pr 123 --status-only --pretty

# 아래에서 위로 고정한 큐를 끝까지 감시하고 종료 코드로 분기한다
bun watch-pr/watch-pr --queued-stack --stack-prs 101,102,103 --timeout 3600
echo "exit=$?"   # 0 완료, 2 충돌, 3 스레드, 4 CI, 5 시간 초과, 6 게이트, 7 조회 실패
```

이 두 명령은 저장소 안의 `scripts` 디렉터리에서 실행한다고 가정한 것이며,
실제 PR에 대해서는 실행하지 않았다.

## 체크리스트

- 사용할 에이전트 환경이 Cursor인지 Claude Code인지 정했는가. Claude Code라면 `/pstack:` 접두사와 어댑터를 쓴다.
- `/setup-pstack`을 실행해 역할별 모델을 정했는가. Claude Code라면 역할마다 `opus xhigh` 같은 값을 직접 지정하는가.
- 자신의 저장소의 승인 게이트 체크 이름이 `Code Review Gate`인가. 아니면 `watch-pr`가 그 체크를 일반 체크로 센다.
- `watch-pr`의 종료 코드를 호출하는 쪽이 0, 2, 3, 4, 5, 6, 7로 분기하는가.
- 계획 문서를 `check-plan.mjs`에 통과시킬 때, 검사기가 보지 않는 `Pass when`의 내용을 사람이 읽었는가.
- `worktree-audit.sh`의 `safe`를 지우기 전에 `remote`와 `DIRTY` 열을 함께 보았는가.
- 자율 실행을 맡기는 요청 문구에 병합 범위가 들어 있는가.

## 기억할 원칙

### 지시문과 검사 코드를 한 묶음으로 배포한다

pstack에서 가장 배울 만한 부분은 지시문 자체보다
지시문이 어긋나지 않게 지키는 얇은 코드 층이다.
README의 개수와 링크, 모델 이름, 명령 이름, 복사본의 최신 여부를 스크립트가
검사하고,
계획의 모양과 기록의 형식과 PR의 병합 가능 여부는 그 상태 판정을 코드로 옮겨서
에이전트가 해석을 덜 하게 만든다.
에이전트에게 맡기는 판단을 줄이려면 문장을 늘리는 대신 종료 코드와 린트로
바꾸라는 것이다.

### 코드가 대신하는 판단은 그 코드의 가정과 함께 이식된다

`watch-pr`는 정교하지만 게이트 이름과 봇 판별과 경로에 한 조직의 관례가
들어 있다.
이런 도구를 가져다 쓸 때는 코드가 내리는 판정(`ready`, `blocker`)을 믿기 전에,
그 판정이 의존하는 문자열과 규칙이 자기 환경에 있는지 먼저 확인해야 한다.
