# 에이전트 팀 만들기: 오케스트레이터, 전문가, 비평가를 Opus 5.5로 구성하는 법

트윗: [How to Build Your First Team of AI Agents Using Claude Opus 5.5](https://twitter.com/eng_khairallah1/status/2104868464770863565)

## 소개

Khairallah AL-Awady(@eng_khairallah1)가 2026년 9월 29일에 올린 Twitter
Article이다.
읽는 데 13분이 걸린다고 적혀 있고, Claude Agent SDK로 에이전트 팀을 처음부터
만드는 과정을 열한 단계로 안내한다.
글의 전제는 에이전트 여럿을 붙인 시스템이 대개 값비싼 혼돈이라는 것이다.
역할이 모호하고, 권한이 전부 열려 있고, 지출 한도가 없고,
덜 끝난 맥락을 서로 넘기다가 자신 있게 틀린 결과를 병렬로 내놓는다고 한다.
글의 처방은 계획하고 위임하는 오케스트레이터,
좁은 일과 더 좁은 권한을 가진 전문가, 약한 결과를 돌려보내는 비평가,
그리고 예산과 한도와 중단 조건이다.

이 문서는 글의 순서를 따르지 않고 팀을 만들 때 내려야 하는 결정을 기준으로
다시 정리했다.
글이 Anthropic의 문서를 근거로 든 부분은 공식 문서를 직접 열어 대조했고,
어긋나는 곳은 비평에서 다룬다.

## 팀이 필요한 경우

글은 먼저 대부분의 작업에는 팀이 필요 없다고 말한다.
일이 하나이고 검증 방법이 하나라면 잘 지시한 에이전트 하나가 팀보다 빠르고
싸다는 것이다.
팀은 조율 비용과 호출 수와 토큰과 실패 경로를 늘린다.

팀을 쓸 이유는 하위 에이전트(subagent)가 주는 네 가지 이점 가운데 하나가 실제로
일을 할 때뿐이다.
공식 문서도 같은 네 가지를 든다.
맥락 격리(context isolation)는 하위 에이전트가 자기 대화 안에서 중간 도구 호출과
결과를 처리하고 최종 메시지만 부모에게 돌려주는 것이다.[^subagents]
이 밖에 병렬 실행, 역할별 지시문, 도구 제한이 있다.
따라서 일이 서로 독립된 조각으로 나뉘거나,
한 단계가 메인 맥락을 쓸데없는 자료로 채우거나,
일부에만 다른 전문성이나 권한이 필요할 때 팀을 쓴다.

## 동작 방식

### 하위 에이전트는 부모의 대화를 보지 못한다

하위 에이전트의 맥락은 부모의 대화 이력이나 도구 결과 없이 새로 시작한다.
공식 문서는 부모가 하위 에이전트에게 넘기는 유일한 내용이 Agent 도구의 `prompt`
문자열이라고 설명하고, 파일 경로, 오류 메시지,
결정을 그 안에 직접 적으라고 한다.[^subagents]
그래서 오케스트레이터가 “이제 정리해 줘”라고만 위임하면 작성자(writer) 역할의
하위 에이전트는 무엇을 정리해야 하는지 모른다.
글은 오케스트레이터의 지시문에 위임할 때마다 완전한 브리프를 쓰고,
하위 에이전트가 대화를 전혀 보지 못했다고 가정하라는 문장을 넣으라고 권한다.

다만 이 규칙에는 예외가 있다. 포크(fork)는 대화를 처음부터 새로 시작하지 않고
지금까지의 대화를 복사하는 하위 에이전트다.[^subagents]
아래 구현은 포크가 아닌 일반 하위 에이전트를 전제로 한다.

### 하위 에이전트는 기본적으로 백그라운드에서 돈다

부모가 띄운 하위 에이전트는 기본적으로 백그라운드에서 실행되고,
Agent 도구 결과의 상태가 `async_launched`이며 보고는 나중 턴에
도착한다.[^subagents]
독립된 조사 세 개를 동시에 돌리는 구조가 가능한 이유다.
작성자 역할은 조사 보고 세 개가 모두 돌아온 뒤에야 시작할 수 있으므로,
오케스트레이터에게 어느 일이 함께 돌 수 있고 어느 일이 기다려야 하는지 지시문에
적어 두어야 한다.

### 오케스트레이터는 Agent 도구를 허용해야 한다

공식 문서에 따르면 Claude는 Agent 도구로 하위 에이전트를 호출한다.[^subagents]
글은 오케스트레이터의 `allowed_tools`에 `Agent`가 빠져 있으면 하위 에이전트를
부를 수 없다고 경고한다.

### 도구를 줄이는 것이 가장 깔끔한 안전 장치다

하위 에이전트에게 주는 도구 목록에서 빠진 도구는 그 세션에 아예 존재하지
않는다고 글은 말한다.
공식 문서에는 반대 방향의 함정이 있다. `tools`를 생략하면 하위 에이전트가 사용할
수 있는 모든 도구를 물려받는다.[^subagents]
도구를 줄이려면 목록을 반드시 적어야 하고, 적지 않은 것이 곧 전체 허용이다.

## 구현하기

아래는 조사, 작성, 비평 세 역할을 가진 팀의 최소 구성이다.
필드 이름은 공식 문서의 `AgentDefinition` 표를 기준으로 했다.[^subagents]
Python SDK는 v0.2.127 이상이어야 아래 한도 설정을 믿을 수 있다.[^subagents]

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, ResultMessage

ORCHESTRATOR = """You lead a research and writing team. You plan and delegate; you do not research or write yourself.
1. Split the brief into independent research questions and dispatch one researcher per question at once.
2. When every report is back, send the writer a complete brief: all findings and the output path.
   Assume the writer has seen nothing of this conversation.
3. Send every draft to the critic. On FAIL, return the critic's exact fix list to the writer.
   Stop after three rounds and report the outstanding objections.
You run unattended: a message with no tool call ends your turn. Never end a turn with a summary that announces
the next step, an offer to continue, a list of non-blocking decisions, or a milestone report."""

AGENTS = {
    "researcher": AgentDefinition(
        description="Gathers and verifies facts on one focused question. Use for every research subtask.",
        prompt="Research exactly one question. Give a source URL for every claim and mark unverifiable claims UNVERIFIED.",
        tools=["WebSearch", "WebFetch"],  # 생략하면 모든 도구를 물려받는다
        effort="low",
    ),
    "writer": AgentDefinition(
        description="Writes a draft strictly from supplied findings. Use only after research is complete.",
        prompt="Write using only the findings in your brief. Add no facts of your own.",
        tools=["Read", "Write"],
        effort="medium",
    ),
    "critic": AgentDefinition(
        description="Reviews a draft against its findings. Use after every draft, before anything is final.",
        prompt="Check every claim against the findings. Return PASS, or FAIL with a numbered fix list. Never edit.",
        tools=["Read"],  # 읽기 전용: 조용히 고치지 않고 보고만 한다
        effort="medium",
    ),
}

async def run_team(brief: str) -> None:
    async for message in query(
        prompt=brief,
        options=ClaudeAgentOptions(
            model="claude-opus-5-5",
            system_prompt=ORCHESTRATOR,
            agents=AGENTS,
            allowed_tools=["Agent", "Read", "Write", "WebSearch", "WebFetch"],
            permission_mode="acceptEdits",
            env={
                "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1",   # 전문가가 하위 에이전트를 또 만들지 못하게 한다
                "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS": "5",
            },
            max_budget_usd=5.0,                                 # 기본값은 한도 없음
        ),
    ):
        if isinstance(message, ResultMessage):
            print(message.subtype, message.total_cost_usd)

async def main() -> None:
    brief = "Compare the three most-discussed AI agent frameworks this month and save a one-page briefing to drafts/briefing.md."
    try:
        await asyncio.wait_for(run_team(brief), timeout=1200)   # 시간 예산은 권고일 뿐이므로 실제 중단은 직접 건다
    except asyncio.TimeoutError:
        print("hard stop: check drafts/ for partial output")

asyncio.run(main())
```

글은 이 구성을 짜기 전에 오케스트레이터 하나만 먼저 돌리라고 한다.
혼자 돌려 보고 어디서 막혔고 어느 부분이 서로 독립이었는지 기록하면 그것이 팀
설계가 된다는 것이다.
독립이었던 조각은 병렬 전문가가 되고, 품질이 흔들린 부분은 비평가의 일이 된다.

## 값 정하기

| 항목                  | 시작값                        | 근거와 측정할 것                                                                                                      |
| --------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 조사 역할 effort      | `low`                         | 공식 effort 표가 `low`의 대표 용도로 하위 에이전트를 든다[^effort]                                                    |
| 작성과 비평 effort    | `medium`                      | Opus 5.5의 기본값이 `medium`이다[^effort]                                                                             |
| 오케스트레이터 effort | `medium`에서 시작             | 계획 품질이 평가에서 오르면 `high`로 올린다. 올려야 하는지는 자기 평가로 잰다                                         |
| 중첩 깊이             | `1`                           | 기본값은 3층이다. 1이면 하위 에이전트가 자기 하위 에이전트를 만들지 못한다[^subagents]                                |
| 동시 실행 수          | `5`                           | 기본값은 20이다. 한도에 닿으면 새 하위 에이전트 생성을 거절한다[^subagents]                                           |
| 지출 한도             | `max_budget_usd=5.0`          | 기본값은 한도 없음이다. 한도에 닿으면 생성을 거절하고 백그라운드를 멈추고 `error_max_budget_usd`로 끝난다[^subagents] |
| 시간 예산             | 바라는 시간보다 조금 넉넉하게 | 모델은 예산 안에 끝내려 하고 보통 훨씬 일찍 끝낸다. 샘플로 조정한다[^prompting]                                       |
| 비평 반복             | 최대 3회                      | 글의 권고다. 이 횟수를 넘으면 남은 이의를 붙여 최선의 초안을 돌려준다                                                 |

effort는 `low`, `medium`, `high`, `xhigh`, `max` 다섯 단계다.[^effort]
공식 문서는 `xhigh`를 30분 넘게 걸리는 긴 에이전트 작업에 쓰라고 하고,
모델별 권장값이 위 표를 덮어쓰는 경우가 있다고 적는다.[^effort]
Opus 5.5에서는 기본값이 `high`가 아니라 `medium`이므로,
설정하지 않은 요청은 `medium`으로 돈다.[^effort]

## 트레이드오프

### 시간 예산은 속도를 사지만 검증을 얇게 만들 수 있다

Opus 5.5는 경과 시간 정보에 매우 민감하고(highly responsive to information about
elapsed time), 하위 에이전트에게 일을 맡기는 설정에서는 이것으로 병렬화를 끌어낼
수 있다고 공식 가이드는 설명한다.[^prompting]
하네스가 매 메시지 끝에 `elapsed 340s / 1200s` 같은 줄을 붙이면 모델이 예산 안에
끝내도록 속도를 맞춘다.[^prompting]
예산을 예측할 수 없으면 경과 시간만 보여 주고 시스템 프롬프트에 한 문장을
넣는다.[^prompting]

Anthropic의 소규모 에이전트 팀 평가에서 예산을 받은 팀은 답의 품질이 단일
에이전트와 비슷하면서 훨씬 일찍 끝났다.[^prompting]
그러나 같은 가이드는 시간이 모자란 조건에서 모델이 검색과 검증을 조금 덜 할 수
있으니 자기 작업으로 답의 품질을 확인하라고 덧붙인다.[^prompting]
빨라진 만큼 줄어드는 것이 어디인지는 작업마다 다르다. 비평가의 PASS 비율과
`UNVERIFIED` 표시의 수가 줄었는지 보면 알 수 있다.

### 예산은 권고이고 중단은 코드가 한다

시간 예산은 모델이 속도를 맞추는 신호일 뿐 한도에서 모델을 멈추는 장치가
아니다.[^prompting]
그래서 실제 한계는 위 코드의 `asyncio.wait_for` 같은 자체 시간 제한으로
걸어야 한다.
지출 한도는 반대로 SDK가 집행한다. 한도에 닿으면 새 하위 에이전트를 만들지 않고
백그라운드에서 돌던 것을 멈추며 질의를 `error_max_budget_usd`로
끝낸다.[^subagents]
이 한도는 하위 에이전트의 요청까지 합산한다.[^subagents]

### 권한을 줄일수록 오케스트레이터의 위임이 어려워진다

비평가에게 읽기 도구만 주면 조용히 고쳐 버리는 일이 없지만,
고치는 일은 작성자에게 돌아가는 왕복이 된다.
왕복 횟수를 3회로 제한하는 이유가 여기에 있다. 한도가 없으면 작성자와 비평가가
합의하지 못한 채 예산을 쓴다.
권한을 좁히는 것과 왕복을 줄이는 것은 서로 당기는 힘이어서 한쪽을 극단으로
가져가면 다른 쪽이 나빠진다.

## 함정

### 도구 목록을 빼먹으면 전부 허용이다

하위 에이전트 정의에서 `tools`를 생략하면 사용할 수 있는 모든 도구를
물려받는다.[^subagents]
비평가를 읽기 전용으로 만들 생각이었는데 목록을 적지 않았다면 비평가는 쓰기
도구까지 가진다.

### 일을 끝낸 줄 알고 멈춘다

Opus 5.5는 긴 작업 중에 사용자에게 상태를 알려 주는데,
그 알림 중 일부가 도구 호출 없이 텍스트로 턴을 끝낸다(`stop_reason:
“end_turn”`).[^prompting]
무인 실행 루프가 이를 작업의 끝으로 보면 거기서 멈춘다.[^prompting]
공식 가이드는 텍스트로만 끝난 턴을 완료의 증거가 아니라 보고로 보라고
권한다.[^prompting]
작업 목록을 체크리스트로 두고, 열린 항목이 남은 채 차단 사유 없이 끝나면 남은
항목을 이름 붙여 짧게 다시 지시하고, 자동으로 이어 가는 횟수는 두세 번에서
멈추라는 것이다.[^prompting]
시스템 프롬프트에는 피하고 싶은 조기 종료의 종류를 구체적으로 적는다. 길게
요약하면서 다음 단계를 예고만 하는 것, 사용자가 원치 않는 이어 가기 제안,
막지 않는 결정의 나열, 지금이 보고하기 좋은 지점이라는 판단이 가이드가 드는 네
가지다.[^prompting]
위 코드의 오케스트레이터 지시문 마지막 줄이 이 네 가지를 담은 것이다.

### 반대로, 사람이 지켜보는 앱에서는 이 지시를 넣지 않는다

가이드는 이 지시를 사람이 곁에 있는 앱에는 넣지 말라고 하고,
위험하거나 되돌릴 수 없는 일에는 자체 확인 단계를 두라고 한다.[^prompting]
이메일 초안을 쓰는 것은 위임이지만 보내는 것은 사람의 결정이다.

### 한도 설정은 SDK 버전에 달려 있다

중첩 깊이, 동시 실행 수, 지출 한도의 동작은 TypeScript SDK v0.3.219,
Python SDK v0.2.127 이후 버전에서 설명된 대로 돈다.[^subagents]
그보다 오래된 버전에서는 일부 한도가 없거나 기본값이 다르다.[^subagents]

## 확인하기

팀을 처음 돌릴 때는 아래 순서로 한다.

1. 오케스트레이터 하나만 돌려 같은 일을 맡기고, 어디서 막혔고 어느 부분이 독립이었는지 기록한다.
2. `max_budget_usd`를 아주 작게(예: 0.5) 두고 돌려서 `error_max_budget_usd`로 끝나고 하위 에이전트가 멈추는지 본다.
3. `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`에서 전문가가 또 하위 에이전트를 부르지 않는지 확인한다.
4. 비평가에게 일부러 틀린 초안을 주고 FAIL과 수정 목록이 돌아오는지 본다.
5. 타임아웃을 짧게 두고 부분 결과가 `drafts/`에 남는지 본다.

## 비평

### 글은 공식 문서의 문장을 따옴표로 옮기지만 표현이 다르다

글은 Anthropic의 프롬프트 가이드가 Opus 5.5에 대해 경과 시간 정보에 세심한
주의를 기울인다고(pays close attention) 말했다고 큰따옴표로 인용한다.
이 문서가 읽은 공식 가이드의 해당 문장은 그 표현이 아니라 경과 시간 정보에 매우
민감하다는 것이었다.[^prompting]
뜻은 가깝지만 따옴표 안의 문장은 문서와 글자가 일치하지 않는다. 문서가 그 뒤에
개정되었을 가능성도 있어서 어느 쪽이 맞는지는 이 문서로 판정하지 못한다.

더 중요한 것은 글이 가이드의 단서를 옮기지 않은 점이다.
글은 팀이 예산을 받으면 품질이 비슷하면서 훨씬 일찍 끝났다는 결과를 맨 위에
내세우고, 예산이 권고일 뿐이라는 점은 따로 적는다.
그러나 가이드가 그 결과를 소규모 에이전트 팀의 조사 작업 평가라고 한정한 점과,
시간이 모자란 조건에서 검색과 검증이 조금 줄 수 있다는 경고는 글에
없다.[^prompting]
글의 첫 문단이 이 결과를 모든 빌더에게 해당하는 일처럼 읽히게 만든다.

### 하위 에이전트의 맥락이 항상 새로 시작하는 것은 아니다

글은 하위 에이전트가 부모의 대화를 전혀 보지 못한다고 말한다.
공식 문서는 새로 시작한다는 규칙에 포크라는 예외를 둔다.[^subagents]
포크는 대화를 복사하므로 위임 메시지에 모든 것을 적어야 한다는 조언은 일반 하위
에이전트에만 맞다.
또 하위 에이전트의 맥락이 빈 것은 아니고,
자기 시스템 프롬프트와 Agent 도구의 프롬프트를 받는다고 문서는
적는다.[^subagents]
이 차이는 설계를 바꾼다. 부모의 긴 대화가 필요한 일에는 포크를,
격리가 필요한 일에는 일반 하위 에이전트를 고르면 된다.

### 글의 수치는 대부분 Khairallah의 주장으로 남는다

공식 모델 소개 페이지로 확인한 것은 Opus 5.5의 가격이 입력 백만 토큰당 4달러,
출력 백만 토큰당 20달러라는 점이다.[^overview]
Terminal-Bench 4.0에서 66.4%와 55.8%라는 점수,
일반 작업에서 Opus 5보다 약 40% 싸다는 주장,
68만 줄 마이그레이션을 하루 안에 끝낸 초기 시험자,
경계를 우회하려는 시도가 85% 줄었다는 수치는 이 문서가 열어 본 문서에서
찾지 못했다.
출처가 있을 수 있지만 글은 출처를 달지 않았으므로,
이 수치들은 Khairallah의 인용으로만 다루는 것이 맞다.

공식 문서와 맞아떨어지는 부분도 많다.
하위 에이전트의 네 가지 이점, 전달되는 것이 `prompt` 문자열뿐이라는 점,
깊이와 동시성과 지출 한도의 이름과 기본값(3층, 20개, 한도 없음),
조기 종료의 네 가지 유형, 예산이 권고라는 점은 모두 문서에
있다.[^subagents][^prompting]
글의 실무 뼈대는 신뢰할 만하고, 검증이 필요한 곳은 성능 수치와 인용 문장이다.

## 체크리스트

- 이 일이 하위 에이전트의 네 가지 이점 가운데 하나를 실제로 쓰는가. 아니라면 에이전트 하나로 만든다.
- 오케스트레이터의 `allowed_tools`에 `Agent`가 들어 있는가.
- 모든 하위 에이전트 정의에 `tools` 목록이 있는가. 비평가는 읽기 전용인가.
- 위임 메시지가 파일 경로, 결정, 제약을 모두 담은 완전한 브리프인가.
- 중첩 깊이, 동시 실행 수, `max_budget_usd`를 모두 설정했는가.
- 시간 예산과 별개로 자체 타임아웃이 있는가.
- 비평 반복에 상한이 있고 그 뒤의 동작이 정해져 있는가.
- 되돌릴 수 없는 행동(전송, 게시, 지출, 삭제)이 사람의 승인 뒤에 있는가.
- SDK 버전이 한도 설정을 지원하는 버전 이상인가.

## 기억할 원칙

### 에이전트를 늘리기 전에 오케스트레이터 하나를 먼저 낫게 만든다

글이 가장 오래 남을 조언은 팀을 설계하기 전에 한 에이전트로 일을 끝까지 해
보라는 것이다.
막힌 곳이 비평가의 일이 되고, 독립이었던 조각이 병렬 전문가가 된다.
역할은 미리 상상해서 나누는 것이 아니라 한 번 돌려 본 기록에서 나온다.

### 한도는 에이전트의 판단에 맡기지 않고 하네스가 집행한다

시간 예산은 모델이 지키려고 애쓰는 권고이고,
지출 한도와 깊이와 동시성은 SDK가 집행하는 한도다.
따라서 멈춰야 하는 것은 코드로 멈춘다.
모델에게는 속도와 방향을 맡기고, 끝내는 권한은 하네스에 둔다.

---

[^subagents]: Claude Code Docs, [Subagents in the SDK - Claude Code Docs](https://platform.claude.com/docs/en/agent-sdk/subagents), 2026-10-21

[^prompting]: Claude Platform Docs, [Prompting Claude Opus 5.5 - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)

[^effort]: Claude Platform Docs, [Effort - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/effort)

[^overview]: Claude Platform Docs, [Claude Opus 5.5 - Claude Platform Docs](https://platform.claude.com/docs/en/models/opus-5-5/overview)
