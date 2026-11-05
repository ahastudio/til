# Superpowers: 코딩 에이전트에 개발 방법론을 얹는 스킬 프레임워크

<https://claude.com/marketplace/plugins/superpowers>

<https://github.com/obra/superpowers>

HN 토론: <https://news.ycombinator.com/item?id=47341827> (4점, 1개 댓글)

## 이게 뭔가

코딩 에이전트(Claude Code, Cursor, Codex 등)에 얹는
워크플로우 프레임워크다. 조합 가능한 스킬 모음으로
브레인스토밍, 계획, 서브에이전트 구현, TDD,
코드 리뷰, 브랜치 관리까지 7단계를 제공한다.

설치하면 에이전트의 작업 방식 자체가 바뀐다.
“코드 짜줘”가 아니라 “설계하고, 승인받고, 계획 세우고,
구현하고, 테스트하고, 리뷰받고, 머지해라”가 된다.

## 설치

README는 harness마다 설치 방법이 다르다고 적는다.
두 개 이상의 harness를 쓰면 각각에 따로 설치해야 한다.
README가 나열하는 대상은 모두 열여섯 가지로,
Claude Code, Antigravity, Codex App, Codex CLI, Cursor, Devin CLI,
Factory Droid, Gemini CLI, GitHub Copilot CLI, Grok Build CLI,
Kimi Code, OpenCode, Pi, Qwen Code, Hermes Agent, Muse가 있다.

Claude Code는 Anthropic의 공식 마켓플레이스에서 설치한다.
README가 적은 명령은 다음과 같다.

```bash
/plugin install superpowers@claude-plugins-official
```

README는 Superpowers와 관련 플러그인을 함께 제공하는
별도 마켓플레이스도 소개한다.

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

업데이트는 coding agent마다 다르지만 대체로 자동이라고 README는 적는다.

## 7단계와 스킬 구성

README의 기본 워크플로는 일곱 단계다.
각 단계의 스킬은 자동으로 활성화된다.
README는 에이전트가 어떤 작업이든 시작하기 전에 관련 스킬이 있는지 확인하며,
이 워크플로는 제안이 아니라 필수라고 적는다.

| 순서 | 스킬                                             | README가 말하는 역할                                                                                                                                                                     |
| ---- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | brainstorming                                    | 만들기 전에 활성화된다. 질문으로 원하는 바를 끌어내고 이해한 내용을 되돌려 보여 준다. 작은 변경은 대화에서 합의하고, 프로젝트는 설계 문서를 쓴다.                                        |
| 2    | using-git-worktrees                              | 설계 승인 뒤에 활성화된다. 새 브랜치에 격리된 작업 공간을 만들고, 프로젝트 설정을 돌리고, 깨끗한 테스트 기준선을 확인한다.                                                               |
| 3    | writing-plans                                    | 작업을 2~5분짜리로 쪼갠다. 모든 작업에 정확한 파일 경로, 완전한 코드, 검증 단계가 들어간다.                                                                                              |
| 4    | subagent-driven-development 또는 executing-plans | 앞쪽은 작업마다 새 subagent를 보내고 작업이 끝날 때마다 리뷰하며 가장 철저하다. 뒤쪽은 현재 세션에서 모든 작업을 직접 구현하고 마지막에 브랜치 전체를 새로 한 번 리뷰하며 가장 저렴하다. |
| 5    | test-driven-development                          | RED-GREEN-REFACTOR를 강제한다. 실패하는 테스트를 쓰고, 실패를 확인하고, 최소한의 코드를 쓰고, 통과를 확인하고, 커밋한다. 테스트보다 먼저 쓴 코드는 삭제한다.                             |
| 6    | requesting-code-review                           | 작업 사이에 활성화된다. 계획과 대조해 리뷰하고 문제를 심각도별로 보고하며, critical 문제는 진행을 막는다.                                                                                |
| 7    | finishing-a-development-branch                   | 모든 작업이 끝나면 활성화된다. 테스트를 확인하고, merge, PR, 유지, 폐기 중에서 고르게 하고, worktree를 정리한다.                                                                         |

스킬 라이브러리는 Testing, Debugging, Collaboration, Meta의 네 갈래다.
Testing에는 `test-driven-development`가 있다.
Debugging에는 4단계로 근본 원인을 찾는 `systematic-debugging`,
고쳤다는 주장을 확인하게 하는 `verification-before-completion`,
세션에서 무엇이 잘못됐는지 증거와 함께 밝히는 `diagnosing-superpowers`가 있다.
Collaboration에는 위 워크플로의 스킬들에 더해
`dispatching-parallel-agents`와 `receiving-code-review`가 있다.
Meta에는 새 스킬을 만드는 `writing-skills`와
스킬 체계를 소개하는 `using-superpowers`가 있다.

세션이 이상하게 돌아가면 에이전트에게
이 세션에서 Superpowers에 무엇이 잘못됐는지 알아내라고 하면 된다.
그러면 `diagnosing-superpowers`가 세션 기록을 읽고
줄 단위 근거와 함께 무슨 일이 있었는지 보고하며,
원하면 개인정보를 지운 묶음을 버그 리포트용으로 만들어 준다고 README는 적는다.

README가 내세우는 철학은 네 가지다.
테스트를 먼저 쓴다(Test-Driven Development).
즉흥이 아니라 체계를 따른다(Systematic over ad-hoc).
복잡성을 줄이는 것을 첫째 목표로 삼는다(Complexity reduction).
성공했다는 주장이 아니라 증거를 본다(Evidence over claims).

## Claude 마켓플레이스의 소개

Claude 마켓플레이스에도 Superpowers 소개 페이지가 있다.
페이지에는 Anthropic verified 표시가 붙어 있고,
설명은 Claude Code용 핵심 스킬 라이브러리라고 되어 있다.
설치 수는 1,009,371건으로 표시되며,
페이지에 기준 날짜는 없다.
플러그인 출처 링크는 `obra/superpowers`를 가리킨다.

사용법을 설명하는 방식은 README와 다르다.
페이지는 `/brainstorming`과 `/execute-plan` 같은 슬래시 명령으로
스킬을 부르는 법을 안내하고,
`/execute-plan`을 검토 지점이 있는
배치 구현 계획 실행이라고 소개한다.
계획과 코딩 기준에 비춰 구현을 평가하는 code-reviewer 에이전트도 소개하고,
디버깅 방법에는 수정 시도가 세 번 실패하면
아키텍처 검토를 일으키는 안전장치가 있다고 적는다.
README는 스킬이 자동으로 활성화되므로 따로 할 일이 없다고 쓴다.
두 설명이 같은 판본을 가리키는지는 확인하지 못했다.

## 기여와 텔레메트리

Superpowers는 Jesse Vincent와 Prime Radiant가 만들며 라이선스는 MIT다.
README의 기여 안내는 새 스킬 기여를 대체로 받지 않는다고 밝힌다.
기존 스킬의 수정은 지원하는 모든 coding agent에서 동작해야 한다.
다른 사람이 올린 이슈를 고치는 에이전트 작성 PR도,
maintainer가 요청하지 않았다면 받지 않는다.
같은 문제를 겪었다면 기존 이슈에 제보를 더하라는 것이다.
PR 템플릿의 요약은 사람이 직접 쓰게 한다.

README는 brainstorming의 선택 기능인 visual companion이
Prime Radiant 웹사이트에서 로고를 불러오며,
이 요청에 Superpowers 버전이 들어간다고 적는다.
프로젝트, 프롬프트, coding agent에 관한 정보는 들어가지 않는다고 한다.
끄려면 환경 변수 `SUPERPOWERS_DISABLE_TELEMETRY`를 참 값으로 설정한다.
Claude Code의 `DISABLE_TELEMETRY`와
`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 설정도 따른다.
이는 README의 설명이며, 실제 요청 내용은 확인하지 않았다.

## 인사이트

### 에이전트의 가장 위험한 본능을 꺾는다

에이전트는 코드부터 짠다. 무조건.
질문 안 한다. 설계 안 한다. 확인 안 한다.
“간단해 보여서”라는 이유로 바로 구현에 돌입하고,
500줄을 쏟아낸 뒤에야 방향이 틀렸다는 걸 안다.

Superpowers의 brainstorming 스킬은
이 충동 앞에 게이트를 세운다.
스킬 본문의 `HARD-GATE`는
사용자가 설계 문서를 승인하기 전에는 아무것도 만들지 못하게 한다.
여기서 만든다는 것은 제품 코드 작성, 스캐폴딩, 의존성 설치,
프로젝트 생성, 구현 스킬 호출을 모두 포함하며,
읽기와 탐색은 허용된다.[^sp-brainstorming]
작은 변경은 짧은 설계 문서로,
프로젝트는 전체 설계 문서로 승인받는다.[^sp-brainstorming]

예외는 두 가지다.
사용자가 질문을 건너뛰기로 하면 스킬이 끝나면서 게이트도 사라진다.
사용자가 동의한 spike는 만들 수 있지만 버리는 용도라고 표시해야 하고,
그 결과를 계속 쓰려면 다시 게이트를 거쳐야 한다.[^sp-brainstorming]
요청에 중요한 내용이 이미 다 들어 있는 분명한 작업은
스킬이 바로 처리하고 한 일을 말하라고 한다.[^sp-brainstorming]

이 게이트는 코드가 막는 장치가 아니라 스킬 본문에 적힌 지시다.
명령형으로 쓰였고 예외가 둘로 한정되어 있다는 점에서
CLAUDE.md의 권고 한 줄보다 강한 문구이지만,
에이전트가 이 지시를 따를 때에만 작동한다.

### 기억이 오염되면 에이전트는 망가진다

에이전트 하나가 작업 5개를 연속으로 하면
세 번째쯤부터 이상해진다.
첫 번째 작업의 변수명을 네 번째에서 쓰고,
두 번째에서 삭제한 함수를 다섯 번째에서 호출한다.
컨텍스트가 서로 스며드는 것이다.

`subagent-driven-development`는 **작업마다 구현 subagent를 새로 보낸다.**
스킬은 이 방식의 이점을 한 context가 모든 작업을 하는 것과 달리
context 오염이 없다는 점으로 든다.
대신 작업마다, 리뷰마다 새 context를 쓰는 비용을 치른다.[^sp-sdd]

README가 가장 저렴하다고 소개하는 `executing-plans`는 이 이점을 포기한다.
현재 세션 하나가 모든 작업을 하고,
작업별 리뷰어도 없이 마지막에 브랜치 전체를 한 번 리뷰한다.
스킬은 작업 기록 장부를 에이전트의 기억 대신으로 삼고,
작업마다의 관문은 TDD가 맡는다고 설명한다.[^sp-exec]
오염을 피하는 장치는 실행 방식을 어느 쪽으로 고르느냐에 달려 있다.

구현 subagent가 시작 전이나 작업 도중에 질문하면,
스킬은 분명하고 빠짐없이 답하고,
구현으로 서둘러 들어가게 하지 말라고 한다.[^sp-sdd]

### 테스트를 “작성”하는 것과 “목격”하는 것은 다르다

대부분의 팀이 TDD를 한다고 말하면서
실제로는 코드를 먼저 쓰고 테스트를 나중에 붙인다.
나중에 붙인 테스트는 당연히 통과한다.
**하지만 그 테스트가 진짜 올바른 동작을 검증하는지는
아무도 모른다.**

Superpowers의 TDD 스킬은 테스트가 **실패하는 것을
직접 목격**하도록 강제한다.[^sp-tdd]
실패를 보지 못한 테스트는 테스트가 아니다.

여기서 끝이 아니다. 가장 엄격한 규칙이 있다.
**실패 테스트 없이 먼저 작성된 프로덕션 코드는
전부 삭제한다.**
참고용으로 남겨 두는 것도,
테스트를 쓰면서 고쳐 쓰는 것도 안 된다.
스킬은 삭제가 말 그대로 삭제를 뜻한다고 분명히 적는다.[^sp-tdd]
“아까우니까 살려두자”는 매몰 비용 오류다.
이 규칙은 그 오류를 지시문 차원에서 금지한다.

### 리뷰를 한 번에 하면 반드시 놓친다

코드 리뷰에서 “이거 잘 됐나?” 하고 한 번 보면
두 가지가 뒤섞인다.
요구사항을 충족하는가? 구현이 깨끗한가?
하나에 집중하면 다른 하나를 놓친다.
그래서 “동작하지만 더러운 코드”가 머지되고,
“깨끗하지만 스펙에서 벗어난 코드”가 머지된다.

Superpowers는 리뷰를 **두 단계로 분리**한다.
스펙 준수 리뷰가 먼저다. 요구사항만 본다.
코드 품질 리뷰가 다음이다. 구현만 본다.
한 번에 하나만 보니까 놓칠 수가 없다.

작업별 리뷰에는 두 판정이 모두 있어야 하고,
구현자의 자체 리뷰는 작업 리뷰를 대신하지 못한다고 스킬은 적는다.
작업별 리뷰와는 별개로,
브랜치 전체를 보는 리뷰가 마지막에 한 번 더 있다.[^sp-sdd]

### 자율 실행은 네 가지 경우에만 멈춘다

에이전트에게 작업 20개를 주고 돌아서면
10개째에서 방향이 틀어져 있어도 모른다.
20개가 끝나고 나서야 발견하면
그때는 이미 10개를 버려야 한다.

Superpowers는 이 문제를 사람의 확인 주기로 풀지 않는다.
README는 사용자가 go라고 한 뒤
에이전트가 계획에서 벗어나지 않고
몇 시간씩 자율적으로 일하는 일이 드물지 않다고 적는다.
`executing-plans` 스킬은 작업 사이에 사용자에게 확인하지 말고
계획의 모든 작업을 멈추지 않고 실행하라고 쓴다.[^sp-exec]

멈추는 경우는 네 가지뿐이다.
되돌릴 수 없거나 파괴적인 작업,
보안에 민감한 작업,
merge, 공유 브랜치로의 push, 배포처럼 작업 공간 밖에 영향을 주는 작업,
그리고 어느 길로 가도 추측이 될 만큼 망가진 계획이다.[^sp-exec]
`subagent-driven-development`도 같은 네 가지를 든다.[^sp-sdd]

그 밖의 충돌, 모호함, 계획의 결함은 멈추지 않고 에이전트가 직접 판단한다.
판단마다 `Ruling:` 형식으로 이유와 틀렸을 때의 비용을 장부(ledger)에 적고
계속 진행한다.[^sp-exec]
계획에서 벗어났는데 장부에 판단이 없으면
몰래 내린 결정이라는 것이 스킬의 기준이다.[^sp-exec]

이 구조에서 사람이 결정하는 자리는 구현 도중이 아니라
설계 승인과 실행 방식 선택에 모인다.
이것은 스킬 본문에서 읽어 낸 구조에 대한 해석이며,
스킬이 그렇게 설명하는 것은 아니다.

## 관련 문서

- [Spec-Driven Development](../agentic-coding/spec-driven-development.md)
- [File-based Planning Workflow](../ai/file-based-planning-workflow.md)
- [Karpathy's Claude Coding Notes](../claude/karpathy-claude-coding-notes.md)

---

[^sp-brainstorming]: GitHub obra/superpowers, [Brainstorming](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/brainstorming/SKILL.md)

[^sp-exec]: GitHub obra/superpowers, [Executing Plans](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/executing-plans/SKILL.md)

[^sp-sdd]: GitHub obra/superpowers, [Subagent-Driven Development](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/subagent-driven-development/SKILL.md)

[^sp-tdd]: GitHub obra/superpowers, [Test-Driven Development](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/test-driven-development/SKILL.md)
