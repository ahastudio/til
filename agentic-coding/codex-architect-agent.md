# Codex 설정 팁: Astra는 매 턴이 아니라 세 지점에서만 부르는 설계자로 둔다

트윗: [Codex tip: once GPT-6.1 Sol is your main model, stop running Astra on every turn](https://twitter.com/thedelost/status/2105398038026195279)

## 소개

delost가 2026년 10월 1일 올린 트윗은 Codex 설정 한 가지를 제안한다.
GPT-6.1 Sol을 주 모델로 쓴다면 Astra를 매 턴 돌리지 말고,
필요할 때만 부르는 설계자(architect) 에이전트로 두라는 것이다.
코드는 계속 Sol이 쓰고, Astra는 세 지점에서만 호출한다.

첫째는 계획을 세우기 전이다. 이 접근이 맞는지 묻는다.
둘째는 같은 오류가 다시 나왔을 때다. 엉뚱한 곳을 파고 있는지 묻는다.
셋째는 끝났다고 말하기 전이다. 놓친 것이 무엇인지 묻는다.
트윗은 이를 “Astra는 검토하고 Sol은 출시한다”고 요약한다.

트윗은 이어서 Jev 엔지니어링을 같은 발상을 한 층 아래에
적용한 것이라고 소개한다.
어느 파일을 볼지, 어느 도구를 쓸지,
재시도할지 멈출지처럼 생각이 필요 없는 분기는 0.5초 안에 Jev가 처리하고, 큰
모델은 실제로 갈리는 분기만 본다는 설명이다.
이 저장소의 Jev 문서는 `jev/jev.md`에 있다.

끝에는 Codex에 붙여 넣을 프롬프트가 있다.
이 프롬프트는 설정 전체를 아래 트리로 다시 짜게 한다.

## 구성

| 역할       | 모델        | 추론 강도 | 하는 일                               |
| ---------- | ----------- | --------- | ------------------------------------- |
| 메인 세션  | GPT-6.1 Sol | high      | 계획하고 코드를 쓴다                  |
| explorer   | gpt-6-luna  | medium    | 코드를 읽고 조사한다                  |
| worker     | gpt-6.1-sol | medium    | 편집하고 테스트를 돌린다              |
| researcher | gpt-6-luna  | medium    | 문서를 찾아 읽는다                    |
| architect  | gpt-6-astra | high      | 계획, 반복 오류, 완료 직전을 검토한다 |
| 승인 검토  | auto_review | -         | 승인 요청을 검토한다                  |

표는 트윗의 트리를 정리한 것이다.
`gpt-6-astra`라는 모델 이름은 트윗에만 나오고,
공식 서브에이전트 문서의 예시에서는 확인하지 못했다.

## 동작 방식

### 서브에이전트는 이렇게 정해진다

Codex 공식 문서에 따르면 내장 에이전트는 `default`, `worker`,
`explorer` 세 가지다.
직접 만든 에이전트는 개인용이면 `~/.codex/agents/`에,
프로젝트용이면 `.codex/agents/`에 TOML 파일 하나씩 둔다.
파일에는 `name`, `description`, `developer_instructions`가 필수이고,
`model`과 `model_reasoning_effort`도 같은 파일에 쓸 수 있다.
이름이 내장 에이전트와 같으면 직접 만든 쪽이 우선한다.

모델과 추론 강도는 이렇게 결정된다.
명시적인 호출 값이 가장 앞서고, 그다음이 `[agents]` 기본값이며,
그다음이 부모 에이전트의 값이다.
다만 에이전트 파일이 `model`이나 `model_reasoning_effort`를 직접 지정하면
파일의 값이 우선한다.
아무것도 설정하지 않으면 서브에이전트는 부모의 모델과 추론 강도를 그대로 쓴다.

### 승인 검토는 별개의 장치다

트윗의 2번 항목에 있는 `approvals_reviewer = "auto_review"`는 공식
문서에도 있는 설정이다.
문서는 이것이 이미 승인이 필요한 요청, 예를 들어 샌드박스 확장이나 차단된
네트워크 접근을 검토자 에이전트가 먼저 평가하게 하는 기능이라고 설명한다.
승인이 대화형일 때, 곧 `approval_policy = "on-request"` 같은
설정에서 의미가 있다.

## 설정하기

트윗의 프롬프트가 만들려는 결과를 공식 문서의 형식에 맞춰 쓰면 아래와 같다.
architect 파일과 `config.toml`의 해당 부분이다.
`developer_instructions`의 문구는 트윗의 설명을 바탕으로 내가 쓴 예시이고,
모델 이름은 트윗 그대로다.

```toml
# .codex/agents/architect.toml
name = "architect"
description = "Reviews plans, repeated errors and finished work. Never writes code."
model = "gpt-6-astra"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
You are called at only three points.
1. Before a large plan: say if the approach is right and name a safer one if not.
2. When the same error comes back: say if the work is in the wrong place.
3. Before the task is called done: list what was missed.
Do not edit files. Answer in a short list.
"""
```

```toml
# ~/.codex/config.toml (relevant lines)
model = "gpt-6.1-sol"
model_reasoning_effort = "high"
approval_policy = "on-request"
approvals_reviewer = "auto_review"
```

`approval_policy = "on-request"` 줄은 트윗에 없고,
공식 문서가 `auto_review`의 전제로 설명한 조건이라 내가 덧붙였다.
트윗의 프롬프트는 여기에 `AGENTS.md` 규칙 한 줄도 더하게 한다.
큰 계획 전, 오류가 반복될 때, 긴 작업을 끝났다고 부르기 전에 architect를
호출하라는 규칙이다.

### 프롬프트가 지키는 안전장치

트윗의 프롬프트는 먼저 기존 설정을 확인하게 한다.
이미 맞는 에이전트가 있으면 새로 만들지 않고,
다른 모델을 고정한 파일은 건너뛰고 목록으로 보고하게 한다.
`agents.default_subagent_model`처럼 설정을 덮어쓸 수 있는 것은 찾아서 보고만
하고 고치지 않게 한다.
모든 변경은 diff로 먼저 보여 주고, 승인 전에는 편집하지 않게 한다.
설정 변경을 맡기는 프롬프트로서 이 순서는 합리적이다.

## 트레이드오프

### 비싼 모델을 줄이는 대신 호출 시점의 판단을 얻는다

Astra를 매 턴 쓰면 가장 높은 품질을 항상 얻지만 비용이 가장 크다.
세 지점에만 부르면 호출 수가 크게 줄지만 그 세 지점이 정말 위험한
지점인지는 보장되지 않는다.
계획 전, 오류 반복, 완료 직전은 오류 비용이 큰 곳이어서 고른 것으로 읽히지만
트윗은 근거 데이터를 보이지 않는다.

### 규칙은 부탁이지 강제가 아니다

`AGENTS.md`에 적은 규칙은 모델이 따르는 지침이다.
호출 시점을 시스템이 감지해서 자동으로 부르는 것이 아니다.
공식 문서도 서브에이전트는 요청할 때 만들어진다고 설명하므로, 주 모델이 규칙을
잊으면 architect는 한 번도 불리지 않는다.
세 지점 가운데 오류 반복은 모델이 스스로 알아차려야 하는
조건이라 특히 빠뜨리기 쉽다.

### 검토가 늘면 지연도 는다

architect를 부를 때마다 메인 작업이 멈추고 높은 추론 강도의 응답을 기다린다.
계획 전과 완료 직전은 호출 횟수가 적어 부담이 작지만,
반복 오류 지점은 이미 막힌 상황에서 지연이 더해진다.
트윗은 지연이나 비용을 얼마나 줄이는지 숫자로 말하지 않는다.

## 함정

- **승인 검토의 범위를 과대하게 읽는다.** 트리에는 `auto_review checks every approval`이라고 적혔지만, 공식 문서는 검토자가 이미 승인이 필요한 행동만 평가한다고 쓴다. 승인이 필요 없는 행동은 거치지 않는다.
- **모델 이름이 계정마다 다를 수 있다.** 공식 문서는 접근 권한이 있을 때 GPT-6.1 Sol을 쓰고 아니면 쓸 수 있는 모델을 고르라고 안내한다. 이름이 맞지 않으면 에이전트 파일이 동작하지 않는다.
- **이미 설정이 덮어쓰고 있을 수 있다.** 프로필, 셸 별칭의 플래그, `agents.default_subagent_model`이 새 설정을 가린다. 트윗의 프롬프트가 3번 항목에서 이를 찾게 한 이유다.
- **architect가 코드를 고치기 시작한다.** `developer_instructions`와 `sandbox_mode`로 읽기 전용에 가깝게 묶어 두지 않으면 검토자가 작성자가 된다.

## 확인하기

이 문서는 설정을 실제 Codex에서 실행해 보지 않았다.
아래 순서로 직접 확인할 수 있다.

1. 프롬프트가 보여 주는 diff를 읽고, 모델 이름과 `config.toml` 키가 설치한 Codex에서 유효한지 확인한다.
2. 작은 저장소에서 일부러 같은 테스트 실패를 두 번 만들고, architect가 두 번째 실패 뒤에 불리는지 본다.
3. 호출 기록으로 architect가 하루에 몇 번 불렸는지 센다. 0이면 규칙이 지켜지지 않은 것이다.
4. 한 주 정도 지난 뒤, 계획이 바뀐 호출과 아무것도 바꾸지 못한 호출의 비율을 비교한다.

## 비평

### 비용 절감은 주장이고 측정은 없다

트윗의 전제는 Astra를 매 턴 쓰는 것이 낭비라는 것이다.
그러나 Sol이 Astra에 가까운 지능을 훨씬 싼 값에 제공한다는 이 저장소의
`openai/gpt-6-1-sol.md` 정리는 가격 비교 자체가 작업 비용과
다르다는 점을 이미 다룬다.
같은 논리로 이 설정이 비용을 얼마나 줄이는지는 호출 횟수, 재시도 횟수,
결과 품질을 함께 재야 알 수 있다.

### 세 지점이 최선이라는 근거가 없다

계획, 반복 오류, 완료 직전은 직관적이지만 다른 지점도 후보다.
예를 들어 범위가 큰 삭제나 마이그레이션 직전은 오류 비용이 더 클 수 있다.
트윗은 세 지점을 사례로 든 것이지 최적이라고 주장하지는 않으므로,
각자의 작업에 맞게 지점을 추가해야 한다.

## 기억할 원칙

### 비싼 판단은 갈림길에서만 쓴다

이 트윗의 두 번째 단락과 첫 단락은 같은 구조다.
판단이 필요 없는 분기는 가장 싼 수단으로 처리하고,
실제로 갈리는 지점에만 비싼 모델을 쓴다.
Astra를 부르는 세 지점은 계획이 틀렸을 때, 같은 방향에서 계속 실패할 때,
놓친 것이 있을 때로 모두 방향 전환이 필요한 순간이다.
어떤 지점이 방향 전환의 순간인지를 먼저 정하는 것이 이 설계의 핵심이고,
모델 이름은 그다음 문제다.
