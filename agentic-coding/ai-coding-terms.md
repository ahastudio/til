# AI 시대 코딩 용어 비교

## 한눈에 보기

먼저 결론을 적는다.
2025년에 나온 이름들은 사람이 코드를 얼마나 읽고 책임지느냐를 두고 갈렸다.
2026년에 나온 이름들은 사람이 무엇을 설계하느냐를 두고 갈린다.
설계 대상이 prompt에서 context로, harness로,
loop로, 마지막에는 factory로 올라갔다.
이 결론은 어느 출처 하나가 말한 것이 아니다.
아래 출처를 겹쳐 읽고 이 문서가 세운 틀이다.

용어를 마주치면 질문 두 개를 던지면 된다.
사람이 코드를 읽는가, 그리고 사람이 계속 관리하는 산출물이 무엇인가.
이 두 질문에 답하면 이름이 달라도 같은 말인지 다른 말인지 가려진다.

이 틀이 틀릴 수 있는 지점도 먼저 적어 둔다.
loop와 factory는 아직 통제된 연구로 검증되지 않았다.
loop engineering의 도입을 저장소 데이터로 처음 잰 연구가 있지만
탐색 단계다.[^loop-survey]
생산성 측정 자체도 흔들리고 있다.[^metr26]
그래서 이 문서의 분류는 현재의 어휘 지도이지 효과의 순위가 아니다.

### 이전 판에서 바로잡은 것

이 문서의 이전 판은 출처를 다시 읽어 보니 다음 네 곳이 틀렸거나 흐렸다.

- 완전 위임이 0~20%라는 수치는 개발자 일반의 통계가 아니다. 보고서는
이를 Anthropic 내부 연구의 결과로 서술하고,
본문에 인용된 사례도 자사 엔지니어의 말이다.[^trends]
- Addy Osmani의 70%는 AI와 사람의 분담 비율이 아니다. 바이브 코딩이 앱의
70%까지 빨리 가게 해 주지만 나머지 30%가 어렵다는 70% 문제다.[^addy]
- Kent Beck의 흡입과 호흡 비유는 “Beyond the Vibes” 글이 아니라
그보다 한 달 앞선 “Augmented Coding & Design”에 있다.[^beck2]
- 바이브 코딩 트윗은 페이지에 2025년 2월 3일로 표시된다. 트윗 ID에 담긴 시각으로
계산하면 UTC로는 2월 2일이다. Simon Willison의 글은 2월 6일이라고
적었지만 트윗 자체의 표시와 어긋난다.[^vibe-tweet][^notall]

## 연표

| 시점       | 사건                                                                                                                                                 |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2021-06-29 | GitHub이 Copilot을 AI pair programmer로 소개한다[^copilot]                                                                                           |
| 2023-04-21 | Centaur Programmer 개념을 제안하는 논문이 arXiv에 올라온다[^centaur]                                                                                 |
| 2024-06-24 | Steve Yegge가 Chat Oriented Programming(CHOP)을 처음 이름 붙인다[^yegge]                                                                             |
| 2025-02-03 | Karpathy가 vibe coding을 트윗한다(ID 계산으로는 UTC 2월 2일)[^vibe-tweet]                                                                            |
| 2025-05-03 | Kent Beck이 augmented coding을 쓰기 시작한다[^beck2]                                                                                                 |
| 2025-06-23 | LangChain이 context engineering을 정의한다[^lc-ce]                                                                                                   |
| 2025-07-14 | Geoffrey Huntley가 Ralph(bash loop 한 줄)를 소개한다[^ralph]                                                                                         |
| 2025-10-07 | Simon Willison이 vibe engineering을 제안한다[^vibeeng]                                                                                               |
| 2025-10-15 | Birgitta Böckeler가 spec-driven development의 세 단계를 정리한다[^bock-sdd]                                                                          |
| 2025-11-06 | Collins Dictionary가 vibe coding을 올해의 단어로 고른다[^collins]                                                                                    |
| 2026-01-23 | Dan Shapiro가 자동화 5단계를 제시하고 마지막을 dark factory라 부른다[^shapiro]                                                                       |
| 2026-02-05 | Karpathy가 agentic engineering을 가장 좋아하는 이름으로 고른다[^karp26]; 같은 날 Mitchell Hashimoto가 harness engineering이라는 말을 쓴다[^mitchell] |
| 2026-02-07 | StrongDM이 software factory의 원칙을 공개한다[^willison-sf]                                                                                          |
| 2026-02-11 | OpenAI가 harness engineering 사례를 발표한다[^openai]                                                                                                |
| 2026-02-23 | Simon Willison이 agentic engineering이 이긴 것 같다고 갱신하고 패턴 연재를 시작한다[^vibeeng][^aep]                                                  |
| 2026-04-02 | Böckeler가 coding agent 사용자용 harness engineering을 정리한다[^bock-harness]                                                                       |
| 2026-04-28 | Thoughtworks가 Structured-Prompt-Driven Development를 발표한다[^spdd]                                                                                |
| 2026-06-08 | Addy Osmani가 loop engineering을 쓴다[^addy-loop]                                                                                                    |
| 2026-08-22 | loop engineering의 도입을 저장소 데이터로 잰 논문이 올라온다[^loop-survey]                                                                           |

## 용어 15개 한눈에 비교

| 용어                           | 제안                         | 정의의 핵심(출처 기준)                                                                |
| ------------------------------ | ---------------------------- | ------------------------------------------------------------------------------------- |
| AI Pair Programming            | GitHub, 2021                 | 코드를 쓰는 동안 곁에서 제안하는 AI[^copilot]                                         |
| Centaur Programming            | Alves, Cipriano, 2023        | 인간과 AI의 협업이 AI 단독보다 낫다는 전제[^centaur]                                  |
| CHOP                           | Steve Yegge, 2024            | 반복적인 prompt 다듬기로 코딩한다[^yegge]                                             |
| Vibe Coding                    | Karpathy, 2025               | 코드의 존재를 잊고 diff도 읽지 않는다[^vibe-tweet]                                    |
| Augmented Coding               | Kent Beck, 2025              | 코드와 복잡도와 테스트를 계속 신경 쓴다[^beck1]                                       |
| AI-Assisted Engineering        | Addy Osmani, 2025            | vibe coding의 창의성에 엔지니어링의 엄밀함을 합친다[^addy]                            |
| Vibe Engineering               | Simon Willison, 2025         | 숙련자가 책임을 지며 LLM으로 속도를 낸다[^vibeeng]                                    |
| Agentic Engineering            | Karpathy, 2026               | 코드를 직접 쓰지 않고 agent를 지휘하며 감독한다[^karp26]                              |
| Agentic Coding                 | Anthropic 등                 | 코드를 생성하고 실행하며 스스로 반복하는 환경[^ccdocs]                                |
| Spec-Driven Development        | 업계, Thoughtworks 정리 2025 | 명세를 먼저 쓰고 agent가 코드를 만든다[^bock-sdd]                                     |
| Prompt-Driven Development      | 여러 곳, SPDD 2026           | prompt를 버전 관리되는 산출물로 다룬다[^spdd]                                         |
| Context Engineering            | 2025년 6월 무렵              | 모델이 볼 token 전체를 설계한다[^anth-ce]                                             |
| Harness Engineering            | Hashimoto, 2026              | agent가 같은 실수를 반복하지 못하게 환경을 고친다[^mitchell]                          |
| Loop Engineering               | Osmani 등, 2026              | agent를 prompt하는 시스템을 설계한다[^addy-loop]                                      |
| Software Factory, Dark Factory | Shapiro, StrongDM, 2026      | 사람이 코드를 쓰지도 읽지도 않고 명세와 시나리오로 수렴시킨다[^shapiro][^willison-sf] |

## 용어별 상세

### AI Pair Programming (2021)

GitHub은 2021년 6월 29일 Copilot의 기술 미리보기를 알리며
새로운 AI pair programmer라고 소개했다.[^copilot]
이 말은 지금도 가장 넓은 우산 용어로 쓰인다.
방법론을 특정하지 않아서
vibe coding도 augmented coding도 이 안에 들어간다는 것이 이 문서의 해석이다.
Dan Shapiro의 틀에서는 tab으로 제안을 받는 자동완성이 레벨 0이고,
Copilot은 레벨 1에서 쓸 수 있는 도구의 예로 언급된다.[^shapiro]

### Centaur Programming (2023)

Pedro Alves와 Bruno Cipriano는 2023년 4월 논문에서
Centaur Programmer라는 개념을 제안했다.
인간과 AI의 협업이 AI 단독보다 효과적이라는 전제이고,
근거는 인간과 컴퓨터의 혼성 팀이 컴퓨터 단독을 이긴 centaur chess 대회다.
논문은 guidance model, sketch model,
inverted control model 세 협업 모델을 제시한다.[^centaur]

이 비유의 한계를 짚는 글도 있다.
Richard Marmorstein은 체스에서
centaur 시대가 끝난 것은 엔진이 너무 강해져 대국자가 방해만 되기 때문이고,
소프트웨어는 아직 centaur 시대에 들어서지도 못했다고 쓴다.[^centera]
그가 드는 근거는 agent가 사람의 지휘 없이는 장기 프로젝트에서
곧 궤도를 벗어난다는 것이다.[^centera]
이 이름은 방법이라기보다 사람의 몫이 남아 있다는 논지에 가깝다는 것이
이 문서의 판단이다.

### CHOP, Chat Oriented Programming (2024)

Steve Yegge는 2024년 6월 24일 Sourcegraph 블로그 글에서
chat 기반 프로그래밍에 CHOP라는 이름을 미리 붙인다고 썼다.[^yegge]
그는 CHOP를 반복적인 prompt 다듬기를 통한 코딩으로 정의하고,
사용자가 LLM의 코드를 승인하는 일은 늘고
직접 쓰는 일은 줄어든다고 설명한다.[^yegge]
이 글은 현재 모델이 이전에는 4~5회 만에 막히던 반복을 수렴시킨다는 관찰에서
출발한다.[^yegge]
CHOP는 바이브 코딩보다 앞섰고 chat 인터페이스에 초점이 있다는 점에서
이후 agent 중심 용어와 구분된다.

### Vibe Coding (2025)

Andrej Karpathy는 2025년 2월의 트윗에서 vibe coding을 새로운 코딩이라 부르며,
분위기에 몸을 맡기고 코드의 존재를 잊는 방식이라고 설명했다.[^vibe-tweet]
트윗은 매번 Accept All을 누르고 diff를 읽지 않으며,
오류 메시지는 설명 없이 붙여 넣고,
해결되지 않는 버그는 무작위 변경을 요청해 없앤다고 적는다.[^vibe-tweet]
그는 이것이 일회성 주말 프로젝트에는 나쁘지 않다고 덧붙였다.[^vibe-tweet]
Collins Dictionary는 2025년 11월 6일 이 말을 올해의 단어로 소개했다.
정의는 자연어로 prompt한 AI로 코드를 쓰는 것이다.[^collins]

이 정의는 곧 넓어졌다.
Simon Willison은 2025년 3월 AI의 도움을 받아 쓴 모든 코드에 이 말이 붙는 것을
우려하며, 자신이 말하는 vibe coding은 LLM이 쓴 코드를 검토하지 않고
소프트웨어를 만드는 것이라고 분명히 했다.[^notall]
그의 기준은 커밋하는 코드를 다른 사람에게 정확히 설명할 수 없으면
커밋하지 않는다는 것이다.[^notall]
LLM이 쓴 코드를 검토하고 테스트하고 설명할 수 있다면
그것은 vibe coding이 아니라 소프트웨어 개발이라고도 쓴다.[^notall]

Karpathy 자신도 1년 뒤 이를 되돌아봤다.
당시에는 LLM 능력이 낮아서 대체로 재미 삼은 일회성 프로젝트에만 썼고,
지금은 전문가의 기본 작업 방식이 더 많은 감독과 검증을
동반하는 agent 프로그래밍이 되고 있다고 썼다.[^karp26]

### Augmented Coding (2025)

Kent Beck은 augmented coding을 vibe coding과 구분한다.
vibe coding에서는 시스템의 동작만 신경 쓰고 오류가 나면 AI에게 다시 넘기지만,
augmented coding에서는
코드와 복잡도와 테스트와 커버리지를 신경 쓴다고 그는 설명한다.[^beck1]
가치 체계는 손으로 코딩할 때와 같아서 정돈되고 동작하는 코드를 원하고,
다만 그 코드를 거의 타이핑하지 않는다는 것이다.[^beck1]

그가 B+ Tree 라이브러리를 AI와 약 4주 만든 기록에는 감독의 구체적인 방식이 있다.
AI가 TDD를 따르게 하려고 plan.md와 system prompt를 쓰고,
중간 결과를 자세히 지켜보며 개입했다.[^beck1]
그가 꼽은 이상 징후는 세 가지다. 같은 일의 반복,
요청하지 않은 기능, 테스트를 끄거나 지우는 속임수다.[^beck1]

이 용어가 오래 남는 이유는 AI의 비대칭 때문이다.
Beck은 개발이 기능을 더하며 복잡도를 들이마시고
구조를 개선하며 내쉬는 호흡이라고 설명한다.[^beck2]
그런데 현재의 AI는 들이마시기만 한다. 이미 큰 함수에 20줄을 더하고,
복잡도를 줄일 필요가 없다고 가정하며,
그 가정은 틀릴 때까지만 맞는다는 것이다.[^beck2]
기능이 복잡도를 늘리고 복잡도가 개발을 늦추는 순환이 AI의 한계를 넘으면
AI가 몇 시간을 헛돌게 되고,
그때는 처음부터 다시 하거나 사람이 설계를 고쳐야 한다고 한다.[^beck2]
그의 시험 중인 대응은 AI에게 다음 단계에 필요한 것만 알려 주는 것이다.[^beck2]
이는 뒤에 나오는 context engineering과 같은 방향이다.

### AI-Assisted Engineering (2025)

Addy Osmani의 Beyond Vibe Coding은 AI 지원 코딩이 스펙트럼이라고 설명한다.
한쪽 끝은 vibe coding이고
다른 쪽 끝은 명세와 엄밀함을 갖춘 AI-assisted engineering이며,
상황에 맞게 옮겨 다니라는 것이다.[^addy]
그는 70% 문제를 든다. vibe coding으로 기능하는 앱의 70%까지는 빨리 가지만
나머지 30%는 깊은 엔지니어링 지식 없이는 극도로 어렵다는 것이다.[^addy]
같은 글은 vibe coding이 모든 AI 지원 코딩을 가리키려던 것이 아니라
AI가 쓴 코드를 읽지 않고 실행하는 특정 방식이라고 밝힌다.[^addy]

### Vibe Engineering (2025)

Simon Willison은 2025년 10월 7일 vibe coding의 반대쪽 끝을 가리킬 이름이 없다며
vibe engineering을 제안했다.
숙련된 전문가가 LLM으로 속도를 내면서
만든 소프트웨어에 책임을 지는 방식이다.[^vibeeng]
그는 agent가 기존의 상위 엔지니어링 관행을 보상한다고 쓰며 자동화된 테스트,
사전 계획, 문서화, 버전 관리 습관, 자동화, 코드 리뷰 문화를 든다.[^vibeeng]
테스트가 없으면 agent가 실제로 시험하지 않고
동작한다고 주장할 수 있다는 경고도 있다.[^vibeeng]

이 이름은 오래 가지 않았다.
Willison은 2026년 2월 23일 이 글에 갱신을 달아
agentic engineering이 이 자리를 차지하는 것 같다고 적었다.[^vibeeng]
제안하고 다섯 달이 채 안 된 때다.
제안자 스스로 이름을 바꾼 사례여서 어휘가 얼마나 빨리 수렴하는지 보여 준다.

### Agentic Engineering (2026)

Karpathy는 2026년 2월의 글에서
vibe coding과 구분되는 더 나은 이름을 찾는 사람이 많다며
자신이 가장 좋아하는 이름으로 agentic engineering을 골랐다.
agentic은 코드의 99%를 직접 쓰지 않고 agent를 지휘하며
감독하는 것이 새로운 기본이어서이고, engineering은 거기에
예술과 과학과 전문성이 있고 배워서
나아질 수 있다는 점을 강조하려는 것이다.[^karp26]
목표는 소프트웨어 품질을 조금도 양보하지 않으면서
agent의 레버리지를 얻는 것이다.[^karp26]

Willison도 같은 이름으로 정리했다.
그는 agentic engineering을 코드를 생성하고
실행해 사람의 매 차례 안내 없이도 테스트하고
반복할 수 있는 coding agent로 소프트웨어를 만드는 일이라고 정의한다.[^aep]
vibe coding은 원래 정의대로 코드에 전혀 주의를 기울이지 않는 것이고,
agentic engineering은 전문 엔지니어가 기존 전문성을 증폭하는 반대쪽 끝이라고
한다.[^aep]

### Agentic Coding

Claude Code 문서는 Claude Code를 agentic coding 환경이라 부른다.
질문에 답하고 기다리는 chatbot과 달리 파일을 읽고 명령을 실행하며 변경하고,
사용자가 지켜보거나 방향을 바꾸거나 자리를 비워도
스스로 문제를 풀어 간다는 설명이다.[^ccdocs]
이 이름이 가리키는 것은 특정 방법론보다 도구가 갖는 자율성의 범주라고
이 문서는 읽는다.

Anthropic의 2026년 보고서는 이 이름의 한계를 수치로 보여 준다.
개발자가 업무의 약 60%에서 AI를 쓰지만 작업의 0~20%만 완전히 위임할 수 있다고
응답했고, 이는 Anthropic 내부 연구의 결과다.[^trends]
보고서는 위임하는 일이 검증하기 쉽거나 위험이 낮은 것에 몰린다고 설명하며,
개념적으로 어렵고 설계에 의존하는 일일수록 사람이 직접 하거나 AI와 함께 한다고
덧붙인다.[^trends]

### Spec-Driven Development (2025)

Birgitta Böckeler는 2025년 10월 spec-driven development(SDD)가 AI 코딩의 최신
유행어 중 하나라며, 이름을 붙인 도구 셋(Kiro, spec-kit,
Tessl)을 직접 써 보고 의미를 정리했다.[^bock-sdd]
그가 본 구현 수준은 셋이다.
spec-first는 잘 생각한 명세를 먼저 쓰고 작업에 쓰는 것이고,
spec-anchored는 작업이 끝나도 명세를 유지해 기능을 발전시키고
유지보수하는 것이며, spec-as-source는 명세가 시간이 지나도 주 원본이고
사람이 코드를 건드리지 않는 것이다.[^bock-sdd]
그가 찾은 SDD 접근은 모두 spec-first이고
모두가 나머지 둘을 지향하는 것은 아니며,
명세를 시간이 지나며 어떻게 유지할지는 흔히 모호하다고 한다.[^bock-sdd]

Thoughtworks의 Liu Shangqi는 2025년 12월 SDD를 잘 쓴 요구사항 명세를 prompt로
삼아 AI agent가 실행 가능한 코드를 만드는 개발 패러다임이라고
이해한다고 썼다.[^tw-sdd]
명세를 단일 진실 원천으로 보고 코드를 부산물로 보는 급진적인 쪽과,
명세는 코드 생성을 이끄는 요소일 뿐이고
실행 가능한 코드가 계속 유지할 진실 원천이라는 쪽이 갈린다고 정리한다.[^tw-sdd]
그는 waterfall로 돌아가는 것이냐는 질문에 이번에는 다르다고 답하면서도,
비결정성과 spec drift와 환각을 피하기 어려워서
결정적인 CI/CD가 여전히 필요하다고 경고한다.[^tw-sdd]

Böckeler의 회의는 구체적이다.
spec-as-source는 model-driven development(MDD)와 닮았다. MDD는 업무용
애플리케이션에서 자리 잡지 못했고,
지나친 부담과 제약 때문이었다고 그는 설명한다.[^bock-sdd]
LLM이 그 부담의 일부를 덜어 주지만 비결정성이라는 값을 치르므로,
spec-as-source가 MDD의 경직성과 LLM의 비결정성이라는
두 단점을 함께 가질 수 있다고 우려한다.[^bock-sdd]
작은 단계의 반복이 통제의 열쇠였는데
상세한 명세를 먼저 쓰는 접근은 이와 어긋난다고도 쓴다.[^bock-sdd]

### Prompt-Driven Development와 SPDD

Prompt-Driven Development는 느슨하게 쓰이는 이름이다.
가장 엄밀한 형태는 Thoughtworks 내부 IT 조직이
만든 Structured-Prompt-Driven Development(SPDD)다.
2026년 4월 28일 martinfowler.com에 실린 글은 이를 prompt를
일급 산출물로 다루는 공학 방법이라고 소개한다.[^spdd]
prompt가 버전 관리되고, 리뷰되고, 재사용되고,
시간이 지나며 개선되는 자산이 된다는 뜻이다.[^spdd]
핵심 구성은 요구사항, 도메인 모델, 해법, 구조, 작업 분해, 규범,
안전장치를 담는 REASONS Canvas와 prompt를 코드와
같은 규율로 다루는 workflow 두 가지다.[^spdd]

이 글은 SPDD를 SDD와 이어서 설명한다.
둘 다 코드 전에 명세를 만들지만 SPDD는 그 명세를 어떻게 만들고
리뷰하고 코드와 동기화하는지를 더한다.[^spdd]
prompt를 한 번 만들고 버리지 않고
정해진 workflow를 거쳐 의도의 기록으로 유지한다는 점이 차이다.[^spdd]
현실이 어긋나면 코드보다 prompt를 먼저 고치고
그다음 코드를 고친다는 것이 workflow의 단순한 규칙이다.[^spdd]
글은 이 방법이 Böckeler가 말하는 spec-anchored 접근에 속한다고 분류한다.[^spdd]
이 분류는 글 속의 서술이고 이 문서가 독립적으로 확인한 것은 아니다.

### Context Engineering (2025)

Willison은 2025년 6월 27일 글에서
context engineering이 prompt engineering의 더 나은 대안으로 힘을 얻고
있다고 썼다.
Shopify의 Tobi Lutke가 핵심 기술을 더 잘 설명하는 말이라고
쓴 것을 Karpathy가 지지했다는 설명이다.[^willison-ce]
Willison은 이 말이 오래갈 것 같다고 평하며,
prompt engineering은 챗봇에 입력하는 우스꽝스러운 말로 추론되어 버렸지만
context engineering의 추론된 정의는 의도된 의미에 더 가깝다고
설명한다.[^willison-ce]
LangChain의 Harrison Chase는 같은 달 이를 LLM이 과업을 그럴듯하게 해내도록
올바른 정보와 도구를 올바른 형식으로 주는 동적 시스템을 만드는 일이라고
정의했다.[^lc-ce]
Anthropic은 2025년 9월 이를 prompt engineering의 자연스러운 진화로 보며,
추론 중 token의 최적 집합을 큐레이션하고 유지하는 전략이라고 설명한다.[^anth-ce]

Thoughtworks의 시각은 구체적이다.
prompt engineering은 사람과 LLM의 상호작용을 최적화하고,
context engineering은 agent와 LLM의 상호작용을 최적화한다는 구분이다.[^tw-sdd]
SDD에서 요구사항 분석과 계획을 구현에서
떼어 내는 것은 context를 명세로 압축하는 일이라고도 쓴다.[^tw-sdd]

### Harness Engineering (2026)

Mitchell Hashimoto는 2026년 2월 5일 글에서
agent가 실수를 발견할 때마다 같은 실수를 하지 않도록 해법을
설계하는 일을 harness engineering이라 부르게 됐다고 썼다.
그는 업계에 널리 받아들여진 말이 있는지 모르겠고
있다면 따르겠다고 덧붙인다.[^mitchell]
그가 꼽은 두 형태는 AGENTS.md 같은 더 나은 암묵적 prompt와 스크린샷이나
필터링된 테스트를 돌리는 스크립트 같은 실제로 프로그램된 도구다.[^mitchell]

OpenAI는 엿새 뒤 이 이름으로 사례를 발표했다.
Ryan Lopopolo가 쓴 글은 5개월 동안 손으로 쓴 코드
0줄로 내부 베타 제품을 만들었다고 밝힌다.[^openai]
약 백만 줄의 코드와 약 1,500개의 PR을 엔지니어 3명에서 7명이 몰았고,
사람은 시스템과 거의 prompt로만 상호작용했다.[^openai]
엔지니어의 주된 일은 agent가 유용한 일을 하도록 환경을 갖추는 것이 되었고,
실패했을 때의 해법은 거의 늘 더 열심히 하라가
아니라 어떤 능력이 빠졌는지 묻는 것이었다.[^openai]

그들의 구체적인 교훈 몇 가지가 이 분야의 윤곽을 보여 준다.

- 거대한 AGENTS.md는 context를 차지하고, 모든 것이 중요하면
아무것도 중요하지 않으며, 금세 낡고, 검증하기 어려워서
실패했다. 약 100줄의 AGENTS.md를 목차로 쓰고
구조화된 docs/ 디렉터리를 기록 체계로 삼았다.[^openai]
- agent가 접근할 수 없는 지식은 존재하지 않는 것과 같아서
Slack 토론 같은 암묵지를 저장소 안으로 옮겨야 했다.[^openai]
- 아키텍처 규칙은 문서가 아니라 맞춤 linter와 구조 테스트로 강제하고,
오류 메시지에 수정 지시를 넣어 agent의 context로 주입했다.[^openai]
- agent는 저장소의 나쁜 패턴도 복제하므로 금요일마다 AI slop을 청소하던 것을,
원칙을 저장소에 넣고 주기적인 정리 agent를 돌리는 방식으로 바꿨다.[^openai]

글은 스스로 한계를 적는다.
완전한 자율성은 이 저장소의 구조와 도구에 크게 의존하므로
비슷한 투자 없이는 일반화하지 말라고 한다.[^openai]
수년에 걸쳐 완전히 agent가 만든 시스템에서
아키텍처 일관성이 어떻게 변할지는 아직 모른다고도 적는다.[^openai]

Böckeler는 2026년 4월 이를 coding agent 사용자의 관점으로 좁혔다.
harness는 agent에서 모델을 뺀 전부를 가리키는 말로 퍼졌고
Agent = Model + Harness로 표현되며,
그는 coding agent 사용자가 만드는 바깥 harness로 범위를 한정한다.[^bock-harness]
그는 harness 요소를 행동 전에 유도하는 guides(feedforward)와 행동 뒤에 관찰해
스스로 고치게 하는 sensors(feedback)로 나누고,
실행 방식을 결정적인 computational(테스트, linter,
타입 검사)과 비결정적인 inferential(AI 리뷰,
LLM-as-judge)로 가른다.[^bock-harness]
feedback만 있으면 같은 실수를 반복하고 feedforward만 있으면
규칙이 통했는지 모른다는 점이 둘을 함께 요구하는 이유다.[^bock-harness]

### Loop Engineering (2026)

loop의 원형은 Geoffrey Huntley의 Ralph다.
2025년 7월 그는 Ralph가 가장 순수한 형태에서는 bash loop라고 설명했다.[^ralph]
그는 이 기법이 비결정적인 세계에서
결정적으로 나쁘다는 점이 오히려 장점이라고 썼다.[^ralph]

Addy Osmani는 2026년 6월 8일 이를 loop engineering으로 정리했다.
agent에게 prompt하는 사람의 자리를 대체하고
그 일을 하는 시스템을 설계하는 일이다.[^addy-loop]
그가 꼽은 다섯 구성 요소는 일정에 따라 발견과 분류를 하는 automations,
병렬 agent가 부딪히지 않게 하는 worktrees, 프로젝트 지식을 적는 skills,
도구에 연결하는 plugins와 connectors,
한 agent가 낸 아이디어를 다른 agent가 검사하는 sub-agents다.[^addy-loop]
여기에 대화 밖에서
완료와 다음 할 일을 담는 기억(마크다운
파일이나 보드)이 하나 더 있다.[^addy-loop]
그는 loop가 harness보다 한 층 위에 있다고 쓰면서,
아직 이르고 자신은 회의적이며
token 비용에 조심해야 한다고 단서를 단다.[^addy-loop]

LangChain은 이를 쌓이는 loop로 설명한다.
첫째는 모델이 도구를 호출하며 일을 끝내는 agent loop,
둘째는 grader가 출력을 검사하고 부족하면 피드백을 보내는 verification loop,
셋째는 이벤트가 agent를 깨우는 event-driven loop다.[^lc-loop]
verification은 지연과 비용을 늘리지만
품질이 속도보다 중요한 대부분의 운영 환경에서
값어치가 있다고 설명한다.[^lc-loop]

이 이름의 도입을 처음으로 잰 연구가 2026년 8월에 나왔다.
논문은 지난 몇 달 사이 개발자가 agent를 지시하는 방식이 prompt를 쓰는 데서
context를 설계하는 데로, 다시 모델 주변의 harness를 구성하는 데로 올라갔다고
정리하고,
2026년 6월에 loop engineering이라는 한 층이 더 나타났다고 쓴다.[^loop-survey]
회색 문헌은 잘 설계된 loop의 구성에 대체로 동의한다. 기계로 검사하는 종료 조건이
있는 촉발형 agent 실행, 지속되는 상태 파일, 검증용 sub-agent,
token 예산, 사람에게 올리는 지점이다.[^loop-survey]
36,710개 저장소를 훑은 탐색 연구에서 휴리스틱에 걸린 256개 중 217개에서
자율 agent loop의 동작을 확인했다.[^loop-survey]
그러나 loop의 설정은 커밋하면서도 담론이 처방하는 상태 파일은 거의
커밋하지 않았고, loop의 런타임 상태는 버전 관리 밖에 있다.[^loop-survey]
말과 실제 관행 사이의 이 틈이 현재 이 용어의 성숙도를 가장 잘 보여 준다고
이 문서는 읽는다.

### Software Factory와 Dark Factory (2026)

Dan Shapiro는 2026년 1월 23일 AI 코딩 자동화를 자율
주행의 단계에 빗대 다섯 단계로 나눴다.[^shapiro]
레벨 0은 코드가 분명히 내 것인 수동 작업이고,
레벨 1은 단위 테스트 작성처럼 개별 작업을 AI 인턴에게 넘기는 단계다.[^shapiro]
레벨 2는 AI와 colleague처럼 짝으로 일하는 단계이고
Shapiro는 AI-native 개발자의 90%가 여기 산다고 쓴다.[^shapiro]
레벨 3은 사람이 안전 운전자가 되어 하루 종일 diff를 리뷰하는 단계이고
대부분이 여기서 멈춘다고 한다.[^shapiro]
레벨 4는 사람이 명세를 쓰고 agent와 논쟁하고 skill을 만들며
12시간 뒤에 테스트가 통과했는지 확인하는 단계다.[^shapiro]
레벨 5는 명세를 소프트웨어로 바꾸는 블랙박스이고
이름의 dark는 사람이 필요하지도 환영받지도 않는 무인 공장에서 따왔다.[^shapiro]

그가 말한 레벨 5의 실천을 구체적으로 공개한 곳이 StrongDM이다.
StrongDM은 명세와 시나리오가 agent를 이끌어 사람의 리뷰 없이 수렴하는 비대화형
개발을 software factory라 부르고, 코드는 사람이 쓰면 안 되고
사람이 리뷰하면 안 된다는 규칙을 내세운다.[^strongdm]
Willison은 이를 가장 야심 찬 형태로 보고,
구현도 테스트도 agent가 쓸 때 소프트웨어가 동작한다는 것을 어떻게
증명하느냐가 지금 가장 중요한 질문이라고 쓴다.[^willison-sf]
StrongDM의 답은 테스트가 쉽게 다시 쓰이고 보상 해킹될 수 있어서
코드 저장소 밖에 둔 시나리오(훈련의 holdout set과 비슷한 것)와 외부 서비스를
행동까지 복제한 Digital Twin Universe로
검증하는 것이다.[^strongdm][^willison-sf]
성공은 테스트가 초록색인가가 아니라 시나리오를 거친 궤적
중 사용자를 만족시킬 비율(satisfaction)로 잰다.[^strongdm]

## 두 개의 축으로 보기

이 절은 위의 출처를 바탕으로 이 문서가 세운 틀이다.
출처가 이 틀 자체를 말하지는 않는다.

### 축 A: 사람이 코드를 얼마나 읽는가

Shapiro의 단계는 이 축의 좋은 눈금이다.[^shapiro]
용어를 그 눈금에 놓으면 다음과 같다.

| 눈금(Shapiro) | 사람의 일                               | 이 눈금에 놓이는 용어                                    |
| ------------- | --------------------------------------- | -------------------------------------------------------- |
| 레벨 0~2      | 코드를 직접 쓰고 AI가 곁에서 거든다     | AI Pair Programming, CHOP, Centaur Programming           |
| 레벨 3        | 대부분을 AI가 쓰고 사람이 전부 리뷰한다 | Augmented Coding, AI-Assisted Engineering                |
| 레벨 3~4      | 사람이 지휘하고 감독한다                | Agentic Engineering, Vibe Engineering, Agentic Coding    |
| 레벨 4        | 명세와 계획을 쓰고 결과를 확인한다      | Spec-Driven Development, Prompt-Driven Development(SPDD) |
| 레벨 5        | 코드를 쓰지도 읽지도 않는다             | Software Factory, Dark Factory                           |
| 눈금 밖       | 의도적으로 읽지 않는다                  | Vibe Coding                                              |

Vibe coding은 자율성이 높아서 눈금 밖에 있는 것이 아니다.
읽지 않기로 선택한다는 점이 정의이기 때문이다.
Willison이 원래 정의를 지켜야 한다고 주장한 이유가 이것이다.[^notall]
책임 없이 읽지 않는 것과,
읽지 않아도 증명할 장치를 만든 것(레벨 5)은 다른 일이라는 것이
이 문서의 판단이다.

### 축 B: 사람이 무엇을 설계하는가

2026년 용어는 이 축에서 갈린다.

| 층      | 설계 대상                               | 대표 용어           |
| ------- | --------------------------------------- | ------------------- |
| prompt  | 한 번의 지시                            | Prompt Engineering  |
| context | 모델이 볼 정보와 도구의 구성            | Context Engineering |
| harness | agent 한 번의 실행을 둘러싼 환경과 검증 | Harness Engineering |
| loop    | harness를 반복 실행하는 시스템          | Loop Engineering    |
| factory | 명세와 시나리오로 수렴시키는 전체 공정  | Software Factory    |

층이 올라간다는 서술은 loop 논문의 요약과
Addy의 글에 있다.[^loop-survey][^addy-loop]
Thoughtworks는 context engineering이 agent와 LLM의 상호작용을 다룬다고 구분하고,
Böckeler는 coding agent 사용자가 만드는 harness가
context engineering의 한 특수한 형태라고 쓴다.[^tw-sdd][^bock-harness]
즉 아래 층이 위 층의 재료가 된다. 층을 오를수록 사람이
개입하는 단위가 한 번의 대화에서 시스템으로 커진다.

### 두 축을 함께 놓으면

| 용어                    | 축 A(읽는 정도)         | 축 B(설계 대상)         |
| ----------------------- | ----------------------- | ----------------------- |
| Vibe Coding             | 읽지 않음               | prompt                  |
| Augmented Coding        | 전부 읽음               | prompt, 테스트와 설계   |
| Agentic Engineering     | 감독하며 읽음           | context에서 harness까지 |
| Spec-Driven Development | 명세를 읽고 결과는 확인 | 명세(context의 압축)    |
| Harness Engineering     | 필요한 곳만 읽음        | harness                 |
| Loop Engineering        | 종료 조건을 읽음        | loop                    |
| Dark Factory            | 읽지 않고 증명          | 시나리오와 검증 환경    |

이 표의 칸은 이 문서의 해석이고 출처의 직접 서술이 아니다.

## 용어가 흐려지는 곳

### 같은 말이 다른 범위를 가리킨다

Vibe coding은 AI가 쓴 코드를 전부 일컫는 말로 번졌고
Willison은 이를 두고 원래 의도를 벗어난다고 쓴다.[^notall]
Harness는 agent에서 모델을 뺀 전부라는 넓은 정의에서 시작해,
Böckeler가 coding agent 사용자의 바깥 harness로 좁혔다.[^bock-harness]
Böckeler는 harness 안에 harness를 두는 은유의 어색함(개의
안쪽에 harness를 달 수 있는가)도 인정한다.[^bock-harness]
Spec이라는 말도 정해진 정의가 없고
PRD와의 비교가 가장 일관된 정의라고 그는 쓴다.[^bock-sdd]

### 이름이 사람 따라 바뀐다

Willison은 vibe engineering을 제안했다가
넉 달 만에 agentic engineering이 우세하다고 갱신했다.[^vibeeng]
Hashimoto는 harness engineering을 쓰면서
널리 받아들여진 말이 따로 있으면 따르겠다고 했다.[^mitchell]
이런 태도는 어휘가 아직 굳지 않았다는 신호이고,
오늘의 용어 지도가 반년 뒤에도 같을 것이라고 기대하면 안 된다.

## 증거는 어디까지 말하는가

용어 대부분은 사람의 감독이 필요하다는 주장을 깔고
있으므로 감독의 효과를 측정한 자료를 짚어 둔다.

METR은 2025년 7월 숙련된 오픈소스 개발자 16명을 대상으로 한 무작위 대조 실험에서
AI 도구를 허용하자 작업이 19% 더 오래 걸렸다고 발표했다.
이 실험의 문제 246건에는 개발자의 자기 저장소의 실제 이슈가 쓰였고,
주 도구는 Cursor Pro와 Claude 3.5와 3.7 Sonnet이었다.[^metr25]
METR은 이 결과가 2025년 초 AI의 스냅샷이고
현재의 효과를 반영하지 않는다고 페이지에 경고를 단다.[^metr25]

2026년 2월 METR은 후속 실험의 설계를 바꾼다고 밝혔다.
새 실험의 자료가 신뢰하기 어려운 이유는 개발자들이 AI 없이는 일하기 싫어 참여를
거부하는 일이 늘었기 때문이고,
이는 AI가 준 속도 향상의 추정을 낮게 편향시킬 가능성이 높다.[^metr26]
작업 시간의 변화로 쓰면,
원래 개발자 중 후속에 참여한 부분집합의 추정은 -18%(18% 단축,
신뢰구간 -38%에서 +9%)이고 새로 모집한 개발자는 -4%(신뢰구간 -15%에서 +9%)다.
두 구간 모두 +9%, 곧 시간이 늘어나는 경우를 포함한다.[^metr26]
METR은 개발자들이 지금은 2025년 초보다 더 빨라졌을 가능성이 높다고
보지만 자료는 그 크기에 약한 증거만 준다고 적는다.[^metr26]

이 두 자료가 합쳐 말하는 바는 이렇다.
감독 수준이 다른 방식들의 실제 생산성과 품질
차이를 보여 주는 통제된 증거는 아직 없다.
그래서 이 용어 지도는 어느 방식이 낫다는 순위를 주지 않고,
각 방식이 사람에게 요구하는 것이 무엇인지만 보여 준다.

## 선택 가이드

이 절은 이 문서의 판단이다.

| 상황                                     | 가까운 용어와 방식    | 이유                                                                                    |
| ---------------------------------------- | --------------------- | --------------------------------------------------------------------------------------- |
| 버릴 수 있는 프로토타입, 주말 프로젝트   | Vibe Coding           | 원래 정의가 일회성 프로젝트를 전제한다[^vibe-tweet][^notall]                            |
| 유지해야 하는 코드베이스를 직접 만진다   | Augmented Coding      | 복잡도와 테스트를 사람이 계속 관리한다[^beck1]                                          |
| 전문가가 agent를 매일 쓴다               | Agentic Engineering   | 숙련자의 감독이 전제이고 어휘가 수렴하는 중이다[^aep][^karp26]                          |
| 요구사항이 복잡하고 여러 사람이 참여한다 | Spec-Driven, SPDD     | 의도를 산출물로 남긴다. 단 spec drift와 과도한 선행 설계를 경계한다[^bock-sdd][^tw-sdd] |
| agent가 같은 실수를 되풀이한다           | Harness Engineering   | 실수마다 환경을 고쳐 재발을 막는다[^mitchell]                                           |
| agent를 밤새 돌리고 싶다                 | Loop Engineering      | 종료 조건, 상태 파일, 예산, 사람에게 올리는 지점이 필요하다[^loop-survey]               |
| 사람이 코드를 보지 않는 공정을 시도한다  | Factory, Dark Factory | 시나리오와 시뮬레이션 같은 증명 장치를 먼저 만든다[^willison-sf]                        |

### 이름이 바뀌어도 변하지 않는 것

출처마다 다른 이름을 쓰지만 공통으로 요구하는 것이 있다.

- 자동 피드백이 있어야 한다. Willison은 테스트가 없으면
agent가 동작한다고 거짓으로 주장할 수 있다고 쓴다.[^vibeeng]
  Hashimoto는 agent에게 틀렸음을 빠르게 알려 주는 도구를 주라고 한다.[^mitchell]
  Beck은 AI가 테스트를 끄거나 지우는 속임수를 이상 징후로 꼽는다.[^beck1]
  StrongDM은 테스트가 보상 해킹될 수 있어
시나리오를 저장소 밖에 둔다.[^strongdm]
- 의도가 저장소 안의 산출물로 있어야 한다. OpenAI는 agent가
접근할 수 없는 지식은 존재하지 않는 것과 같다고 쓴다.[^openai]
  SDD는 명세로, SPDD는 prompt로,
loop는 상태 파일로 같은 일을 한다.[^bock-sdd][^spdd][^addy-loop]
- 사람의 주의는 한정된 자원이다. OpenAI의 병목은 사람의 QA 시간이었고
Addy는 loop 설계에서 token 비용을 경고한다.[^openai][^addy-loop]

## 이 틀을 뒤집을 관찰

- 리뷰 없는 공정(레벨 5)이 보안과 신뢰성이 필요한 제품에서 오래 유지되고,
그 품질을 독립된 감사가 확인하면
축 A를 읽는 정도로 나눈 이 문서의 분류가 약해진다.
  StrongDM과 Shapiro의 서술은 아직 일부 팀의 보고다.[^shapiro][^willison-sf]
- loop engineering을 쓰는 저장소가 상태 파일을 커밋하고
종료 조건을 지킨다는 측정이 나오면
말과 관행의 틈이라는 이 문서의 해석이 약해진다.[^loop-survey]
- 감독 수준을 달리한 통제 실험이 나오면
이 문서가 순위를 주지 않는다는 한계가 풀린다. METR이
설계를 바꾸는 이유가 그 실험의 어려움이다.[^metr26]

## 관련 문서

- `agentic-coding/vibe-coding.md`,
`agentic-coding/augmented-coding.md`: 개별 용어의 원문 분석.
- `agentic-coding/spec-driven-development.md`: SDD 상세.
- `agentic-coding/prompt-to-loop-engineering.md`: prompt에서
loop까지 층이 올라가는 과정.
- `agentic-coding/harness-engineering.md`,
`agentic-coding/loop-engineering.md`: harness와 loop의 개별 분석.

---

[^copilot]: GitHub Blog, [Introducing GitHub Copilot: your AI pair programmer](https://github.blog/news-insights/product-news/introducing-github-copilot-ai-pair-programmer/), 2021-06-29

[^centaur]: arXiv, [The centaur programmer -- How Kasparov's Advanced Chess spans over to the software development of the future](https://arxiv.org/abs/2304.11172), 2023-04-21

[^centera]: Richard Marmorstein, [Software's Centaur Era](https://twitchard.github.io/posts/2026-05-18-softwares-centaur-era.html), 2026-05-18

[^yegge]: Sourcegraph Blog, [The death of the junior developer](https://sourcegraph.com/blog/the-death-of-the-junior-developer), 2024-06-24

[^vibe-tweet]: Twitter, [Andrej Karpathy on X: “There's a new kind of coding I call ”vibe coding“, where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. ...”](https://twitter.com/karpathy/status/1886192184808149383), 2025-02-03

[^karp26]: Twitter, [Andrej Karpathy on X: “A lot of people quote tweeted this as 1 year anniversary of vibe coding. Some retrospective - ...”](https://twitter.com/karpathy/status/2019137879310836075), 2026-02-05

[^collins]: Collins Dictionary Language Blog, [Collins' Word of the Year 2025: AI meets authenticity as society shifts](https://blog.collinsdictionary.com/language-lovers/collins-word-of-the-year-2025-ai-meets-authenticity-as-society-shifts/), 2025-11-06

[^notall]: Simon Willison's Weblog, [Not all AI-assisted programming is vibe coding (but vibe coding rocks)](https://simonwillison.net/2025/Mar/19/vibe-coding/), 2025-03-19

[^beck2]: Tidy First?, [Augmented Coding & Design](https://tidyfirst.substack.com/p/augmented-coding-and-design), 2025-05-03

[^beck1]: Tidy First?, [Augmented Coding: Beyond the Vibes](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes), 2025-06-25

[^addy]: Addy Osmani, [Beyond Vibe Coding - A Guide To AI-Assisted Development](https://beyond.addy.ie/)

[^vibeeng]: Simon Willison's Weblog, [Vibe engineering](https://simonwillison.net/2025/Oct/7/vibe-engineering/), 2025-10-07

[^aep]: Simon Willison's Weblog, [Writing about Agentic Engineering Patterns](https://simonwillison.net/2026/Feb/23/agentic-engineering-patterns/), 2026-02-23

[^ccdocs]: Claude Code Docs, [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices)

[^trends]: Anthropic, [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf), 2026-01-22(PDF 메타데이터의 생성일, 본문에 게시일 없음)

[^bock-sdd]: martinfowler.com, [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), 2025-10-15

[^tw-sdd]: Thoughtworks, [Spec-driven development: Unpacking one of 2025's key new AI-assisted engineering practices](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices), 2025-12-04

[^spdd]: martinfowler.com, [Structured-Prompt-Driven Development (SPDD)](https://martinfowler.com/articles/structured-prompt-driven/), 2026-04-28

[^willison-ce]: Simon Willison's Weblog, [Context engineering](https://simonwillison.net/2025/Jun/27/context-engineering/), 2025-06-27

[^lc-ce]: LangChain Blog, [The rise of “context engineering”](https://blog.langchain.com/the-rise-of-context-engineering/), 2025-06-23

[^anth-ce]: Anthropic Engineering, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025-09-29

[^mitchell]: Mitchell Hashimoto, [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey), 2026-02-05

[^openai]: OpenAI, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), 2026-02-11

[^bock-harness]: martinfowler.com, [Harness engineering for coding agent users](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html), 2026-04-02

[^ralph]: Geoffrey Huntley, [Ralph Wiggum as a “software engineer”](https://ghuntley.com/ralph/), 2025-07-14

[^addy-loop]: Addy Osmani(Substack), [Loop Engineering](https://addyo.substack.com/p/loop-engineering), 2026-06-08

[^lc-loop]: LangChain Blog, [The Art of Loop Engineering](https://www.langchain.com/blog/the-art-of-loop-engineering), 2026-06-16

[^loop-survey]: arXiv, [Loop Engineering: Building Blocks, Adoption, and Impact](https://arxiv.org/abs/2608.21884), 2026-08-22

[^shapiro]: Dan Shapiro's Blog, [The Five Levels: from Spicy Autocomplete to the Dark Factory](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/), 2026-01-23

[^strongdm]: StrongDM, [StrongDM Software Factory](https://factory.strongdm.ai)

[^willison-sf]: Simon Willison's Weblog, [How StrongDM's AI team build serious software without even looking at the code](https://simonwillison.net/2026/Feb/7/software-factory/), 2026-02-07

[^metr25]: METR, [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), 2025-07-10

[^metr26]: METR, [We are Changing our Developer Productivity Experiment Design](https://metr.org/blog/2026-02-24-uplift-update/), 2026-02-24
