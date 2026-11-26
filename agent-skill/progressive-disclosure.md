# Progressive Disclosure

## 개념

점진적 공개(progressive disclosure)는 처음에는 이름과 설명 같은 최소한의
정보만 보여 주고, 본문과 세부 자료는 필요해진 시점에 불러오는 방식이다.[^1]
UI 설계에서 먼저 쓰인 원칙이다.
Jakob Nielsen은 2006년 글에서 고급 기능이나 드물게 쓰는 기능을 보조
화면으로 미뤄 애플리케이션을 배우기 쉽고 실수하기 어렵게 만드는 방식이라고
정의했다.[^nng]
자세한 정리는
[Jakob Nielsen의 Progressive Disclosure](../ux/progressive-disclosure-nielsen.md)에 있다.
에이전트 설계에서는 같은 원칙을 컨텍스트 윈도우(context window) 관리에
옮긴 것이다.
Anthropic은 스킬의 메타데이터를 점진적 공개의 첫 단계로 설명한다.[^eng]
정보를 한꺼번에 쏟아붓는 것은 사용자에게 복잡한 화면을 내미는 것과
같다는 설명이 이를 잘 보여 준다.[^2]

같은 원리를 가리키는 말이 여럿이다.
지연 로딩(lazy loading)은 쓰기 직전에 전체 정의를 불러온다는 뜻으로
쓰인다.[^3]
라우터(router)로서의 진입 파일은 진입 파일이 백과사전이 아니라 필요한
문서를 가리키는 길잡이여야 한다는 원칙이다.[^4]
단계적 공개는 영어 용어를 이렇게 옮긴 문서도 있다.[^5]

## 스킬의 3단계 로딩

스킬(skill)이 점진적 공개를 가장 뚜렷하게 구현한 사례다.
세 단계로 나뉜다.

| 단계                    | 컨텍스트에 올라오는 것 | 시점               |
| ----------------------- | ---------------------- | ------------------ |
| 메타데이터(frontmatter) | `name`과 `description` | 항상               |
| `SKILL.md` 본문         | 전체 지시문            | 스킬이 활성화될 때 |
| 참조 파일               | 번들된 스크립트와 문서 | 작업이 요구할 때   |

구글의 `google/skills`는 이 세 단계를 Discovery, Activation, Execution이라
부른다.[^6]
Vercel Eve는 시스템 프롬프트에 스킬의 이름과 설명만 올린다.
요청이 설명과 맞으면 모델이 도구를 호출해 본문을 불러오고, 스킬이 많으면
목록에서 빼고 검색으로 찾게 할 수도 있다.[^7]

### 비용 수치

공개 표준인 Agent Skills 명세는 단계별 크기를 다음과 같이 적는다.[^spec]

| 단계                  | 명세의 수치                       |
| --------------------- | --------------------------------- |
| 메타데이터            | 약 100토큰, 시작할 때 모든 스킬   |
| `SKILL.md` 본문       | 5,000토큰 미만을 권장, 500줄 아래 |
| 참조 파일(scripts 등) | 필요할 때만 로드                  |

명세는 파일 참조를 `SKILL.md`에서 한 단계 깊이로 두고 깊게 중첩된 참조
사슬을 피하라고 한다.[^spec]
Claude의 작성 모범 사례 문서도 같은 한도를 적는다.
중첩된 참조는 `head -100` 같은 명령으로 일부만 미리 읽혀 불완전한 정보가
될 수 있기 때문이다.[^bp]
다른 정리는 계층별 비용을 수십, 수백, 수천 토큰으로 적는데,[^9]
이는 명세의 수치와 맞지 않는 2차 설명이다.
명세의 수치는 권장값이며 실제 측정값이 아니다.

## 적용 범위

스킬 밖에서도 같은 구조가 반복된다.

| 대상                       | 먼저 보이는 것                | 나중에 펼치는 것              | 근거  |
| -------------------------- | ----------------------------- | ----------------------------- | ----- |
| 도구 정의(tool definition) | 이름과 설명, 지연 로딩 목록   | 쓰기 직전에 검색한 전체 정의  | [^3]  |
| `CLAUDE.md`, `AGENTS.md`   | 80줄 안팎의 라우팅 파일       | 주제별 문서                   | [^4]  |
| MCP 서버의 스킬            | 서버가 게시한 스킬 목록       | 필요할 때 읽는 스킬 본문      | [^10] |
| 에이전트 메모리            | 검색 결과의 요약              | 필요한 기록의 원문            | [^11] |
| 긴 도구 출력               | 앞뒤 일정 토큰                | 파일시스템으로 옮긴 전문      | [^12] |
| 저장소 수백 개의 지도      | 사업 영역마다 파일 하나       | 그 영역의 저장소 목록         | [^13] |
| 다이어그램 설명            | 순서대로 그려지는 노드와 엣지 | 전체 구조                     | [^14] |
| 저작 도구 Twine            | 코드 없이 만드는 화면         | 변수, 조건문, CSS, JavaScript | [^5]  |

### 서브에이전트와의 관계

서브에이전트(subagent)로 쪼개던 주된 이유는 컨텍스트 부풀림이었다.
점진적 공개가 이를 막으면 하나의 에이전트 루프에 합치는 편이
공유된 컨텍스트를 유지할 수 있어 낫다는 논지가 있다.[^15]

### 도구 검색의 수치

Anthropic의 Advanced Tool Use 글은 GitHub, Slack, Sentry, Grafana, Splunk를
합친 58개 도구가 대화 시작 전에 약 55K 토큰을 쓴다고 한다.
도구 검색(Tool Search Tool)은 지연된 정의를 필요할 때만 로드해 이를 85%
줄이고, 내부 MCP 평가에서 Opus 4의 정확도가 49%에서 74%로, Opus 4.5가
79.5%에서 88.1%로 올랐다고 보고한다.
이 수치는 Anthropic 내부 시험이다.
정리는 [Claude의 Advanced Tool Use](../claude/advanced-tool-use.md)에 있다.
Anthropic 문서는 도구가 30~50개를 넘으면 선택 정확도가 떨어지고, 가장
자주 쓰는 3~5개는 지연 로드하지 말라고 한다.[^ts]

### 컨텍스트 엔지니어링과의 관계

Anthropic의 컨텍스트 엔지니어링 글은 에이전트가 식별자(파일 경로, 저장된
쿼리, 링크)만 유지하다 필요할 때 도구로 불러오는 '필요한 순간' 방식을
설명하고, 이것이 점진적 공개를 가능하게 한다고 말한다.[^ece]
Claude Code가 이 방식과 미리 올리는 방식을 섞는다는 설명도 있다.
`CLAUDE.md`는 처음에 컨텍스트에 올리고, `glob`과 `grep`으로는 파일을 그때그때
가져온다는 것이다.[^ece]

### MCP와의 관계

MCP가 도구 목록을 선언적으로 전부 내려보내는 설계는 목록이 커질수록
컨텍스트 비용이 된다.
한 사용자의 다섯 도구 패턴은 이를 손으로 구현한 점진적 공개로 풀이된다.[^16]

## 측정된 효과

Workday AI Research의 보고서는 스킬 라이브러리 크기 N을 5, 20, 50, 100으로
바꿔 즉시 로딩과 점진적 공개를 비교했다.
자세한 표는
[Agent Skills 점진적 공개 보고서](../ai/progressive-disclosure-of-agent-skills.md)에
있다.

토큰은 점진적 공개가 N이 클수록 더 줄이며 최대 81.7% 절감했다.
N=100에서 즉시 로딩은 모든 실행에서 컨텍스트 한도를 넘어 충돌했다.[^wd]

검색 품질은 평균적으로 점진적 공개가 낫다.
Qwen3-14B의 즉시 로딩 성공률은 N=5의 1.00에서 N=50의 0.125로 떨어졌다.
다만 Qwen3-8B, N=20에서는 즉시 로딩 0.68이 점진적 공개 0.38보다 높았다.[^wd]

지연은 스킬을 고르는 모델 호출이 늘어 Qwen3-8B, N=50에서 1.75초가
2.01초로 15% 늘었다.[^wd]
이 결과의 조건은 7B~14B 규모의 Qwen 모델 세 가지, 32k 컨텍스트, 과제 24개의
합성 실험이다.[^wd]

## 왜 컨텍스트 창이 커져도 필요한가

컨텍스트 창이 커졌으니 전부 넣으면 되지 않느냐는 반론이 있다.
답은 용량이 아니라 주의(attention)에 있다.
지침 100개 중 3개만 이번 작업에 관련되면, 나머지 97개는 비용일 뿐 아니라
모델의 주의를 분산시키는 잡음이다.
용량이 남아도 이 잡음은 줄지 않는다.[^17]
그래서 목표를 토큰 절약으로 이해하면 잘못된 최적화가 된다.
목표는 이번 턴에 필요한 것만 컨텍스트에 두는 것이다.[^17]

같은 이유로 성능 최적화가 아니라 정확도 최적화라는 표현도 쓰인다.
LLM에서는 컨텍스트에 넣는 모든 토큰이 비용이기 때문이다.[^18]
Claude 5 세대 컨텍스트 엔지니어링의 여섯 가지 전환 중 점진적 공개는
모델이 좋아져도 유효한 항목으로 분류된다.
규칙에서 판단으로, 예시에서 인터페이스 설계로, 반복에서 단일 진술로의
전환은 모델 세대에 종속된 조언이다.[^19]

### 비유

컨텍스트를 RAM에, 불필요한 정보를 미리 올리는 것을 캐시 오염에 견주는
설명이 있다.[^20]
모든 지식을 한꺼번에 넣을 수 없으니 색인을 두고 필요할 때만 본문을
펼치는 구조를 운영체제의 가상 메모리 페이징에 견주는 설명도 있다.[^21]
다만 이런 비유는 직관을 줄 뿐 설계 결정의 근거가 될 수 없다는 지적이
있다.[^22]

## 설계 지침

출처들이 공통으로 제시하는 실천은 여섯 가지다.

첫째, 진입 파일은 라우터로 만든다.
한 강의는 600줄짜리 단일 `AGENTS.md`를 80줄 라우팅 파일과 주제 문서
4개로 쪼갠 뒤 작업 성공률이 45%에서 72%로 올랐다고 보고한다.
이 수치는 강의의 보고이며 재현하지 않았다.[^4]

둘째, 스킬은 폴더로 설계한다.
상세 함수 시그니처는 `references/api.md`로, 출력 템플릿은 `assets/`로
나누고, 어떤 파일이 있는지 알려 주면 Claude가 적절한 시점에 읽는다.[^23]

셋째, 여러 워크플로를 가진 스킬은 루트 문서를 최소한의 라우터로 만들고
보조 문서와 스크립트를 가리키게 한다.
스킬을 읽는 것 자체가 컨텍스트를 쓰고, 지금 작업과 무관한 안내까지
끌어들이기 때문이다.[^24]

넷째, `description`은 짧게 쓰되 언제 써야 하는지 밝힌다.
로드 여부를 정하는 근거가 이 한 줄이기 때문이다.[^24][^25]

다섯째, 규모가 커지면 한 단계를 더 둔다.
저장소가 수백 개면 저장소마다 포인터를 두는 대신 사업 영역마다 파일 하나를
두고, 그 파일이 영역의 저장소를 나열한다.[^13]

여섯째, 압축보다 요약과 원본의 짝을 먼저 고려한다.
요약을 먼저 주고 필요할 때 원본을 펼치는 방식이 정답에 가깝다는 견해가
있다.[^26]

## 한계

### 지연과 단계 수

지연은 선택 단계가 모델 호출을 늘려서 생긴다.
Workday 실험에서 지연이 15% 늘었고, 도구 검색에 대해서도 Anthropic은
검색 단계가 있으므로 절감이 지연보다 클 때 이득이라고 쓴다.[^wd][^atu]
단계 수에 대해서는 Nielsen이 공개 단계가 둘을 넘으면 사용자가 길을 잃어
사용성이 떨어지는 경우가 많다고 본다.
스킬의 로딩은 세 단계이며, 모델에게도 같은 문제가 생기는지는 이 글로는 알
수 없다.[^nng]
도구 검색에는 반론도 있다.
HN에서는 전부 쓰게 될 도구에 검색을 더하면 오버헤드라는 의견과, 도구를
늘리기보다 셸 하나와 스킬로 가야 한다는 의견이 나왔다.
[Claude의 Advanced Tool Use](../claude/advanced-tool-use.md)에 정리했다.

### 신뢰와 매칭

신뢰 문제는 사용자가 평소 보는 것이 `description`뿐인데 실제로 실행되는
것은 활성화 후 펼쳐지는 본문 전체라는 데서 생긴다.
설명은 무해한데 본문이 위험한 명령을 담는 경우를 미리 알아채기
어렵다.[^21]
매칭 신뢰성도 같은 곳에 걸린다.
어떤 스킬을 불러올지가 `description` 하나로 결정되므로 그 문장의 품질이
로드 여부를 좌우한다.[^25]

### 비용과 근거의 한계

되풀이되는 비용도 있다.
직접 API 호출은 점진적 공개로 컨텍스트를 아낄 수 있지만 쓸 때마다 API를
다시 이해해야 한다.
MCP는 목록을 선불로 주고 직접 호출은 사용할 때마다 명세를 다시 읽는다.
둘은 컨텍스트 비용을 어디에 두느냐가 다를 뿐이다.[^16][^27]
경계값도 없다.
서브에이전트를 합칠 때 한 컨텍스트에 쌓이는 중간 결과가 어디서 이득에서
손해로 바뀌는지 수치가 없다.[^28]
끝으로 이해관계가 있다.
스킬 지침을 다룬 원문은 자사 제품의 최신 동작을 정당화하는 문서이기도
하다.[^24]

## 정리

구조는 항상 보이는 작은 색인과, 필요할 때만 읽는 큰 본문의 분리다.
목표는 토큰 절약이 아니라 이번 작업에 관련된 정보만 남기는 것이다.
쟁점은 다음 세 가지다.

- 비용 수치
- 모델 세대와의 무관 여부
- 신뢰와 보안을 어디서 보장하느냐

1차 자료로 직접 읽은 것은 다음과 같다.

- Nielsen의 글
- Anthropic의 스킬 글
- Anthropic의 Advanced Tool Use 글
- 컨텍스트 엔지니어링 글
- Agent Skills 명세
- 작성 모범 사례 문서
- 도구 검색 문서
- Workday 보고서

나머지 인용은 저장소의 TIL 문서가 보고한 내용을 옮겼고 원문과 대조하지
않았다.

## 관련 문서

- [Jakob Nielsen의 Progressive Disclosure](../ux/progressive-disclosure-nielsen.md)
- [Anthropic의 Agent Skills 소개 글](equipping-agents-with-agent-skills.md)
- [Claude의 Advanced Tool Use](../claude/advanced-tool-use.md)
- [Agent Skills 점진적 공개 보고서](../ai/progressive-disclosure-of-agent-skills.md)

---

[^nng]: Jakob Nielsen, [Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/), 2006-12-03

[^eng]: Anthropic, [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), 2025-10-16

[^spec]: Agent Skills, [Specification](https://agentskills.io/specification)

[^bp]: Anthropic, [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

[^ts]: Anthropic, [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

[^atu]: Anthropic, [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use), 2025-11-24

[^ece]: Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025-09-29

[^wd]: Guilin Zhang 외, [Report: Progressive Disclosure of Agent Skills](https://arxiv.org/abs/2609.35692), 2026-09-28

[^1]: [Claude Code Skills](../claude/skills.md)의 「Skill의 동작 원리: 점진적 공개」, [하네스 엔지니어링 백과사전](../agentic-coding/harness-engineering-encyclopedia.md)의 용어표.

[^2]: [Agent Skills for Context Engineering](agent-skills-for-context-engineering.md)의 「Progressive Disclosure는 UX 원칙의 재발견」.

[^3]: [Claude 5 세대 모델을 위한 컨텍스트 엔지니어링의 새 규칙](../claude/new-rules-of-context-engineering-for-claude-5.md)의 「선행 로딩에서 점진적 공개로」.

[^4]: [결정론적 강제와 텍스트 지침의 경계](../_wiki/harness-engineering/deterministic-vs-prompted.md), [Learn Harness Engineering 강의 전편](../agentic-coding/learn-harness-engineering-lectures.md).

[^5]: [Twine — 인터랙티브 논리니어 스토리 저작 도구](../game/twine.md).

[^6]: [google/skills: 구글의 Agent Skills 저장소](../google/google-skills.md)의 「명세와 동작」.

[^7]: [Eve: 디렉터리 하나로 에이전트를 정의하고 운영하는 Vercel 프레임워크](../ai-tool/vercel-eve.md).

[^9]: [Claude Skills 2.0 완전 분석](../claude/claude-skills-2.0.md)의 「토큰 효율성 구조」.

[^10]: [Claude의 MCP 확장 지원 발표](../mcp/skills-over-mcp.md).

[^11]: [claude-mem](claude-mem.md)의 구성 요소 표.

[^12]: [Harness Engineering: AI 에이전트를 실제로 움직이게 하는 인프라 설계](../agentic-coding/agent-harness-engineering.md).

[^13]: [Home Repo 패턴](../agentic-coding/home-repo-pattern.md)의 「규모에 따라 포인터 방식이 한계에 이른다」.

[^14]: [OpenFlowKit](../ai-tool/openflowkit.md).

[^15]: [서브에이전트를 메인 에이전트 루프에 합칠 때](../agentic-coding/fold-subagents-into-agent-loop.md).

[^16]: [MCP를 프로덕션에서 쓰는 사람들이 실제로 답한 것](../mcp/mcp-in-production.md).

[^17]: [Claude 5 세대 모델을 위한 컨텍스트 엔지니어링의 새 규칙](../claude/new-rules-of-context-engineering-for-claude-5.md)의 「점진적 공개는 컨텍스트 창이 커져도 유효하다」.

[^18]: [Lessons from Building Claude Code: How We Use Skills](../claude/lessons-from-building-claude-code-skills.md)의 「점진적 공개의 일관성」.

[^19]: [모델이 좋아져도 하네스가 사라지지 않는 이유](../_wiki/harness-engineering/why-harness-persists.md).

[^20]: [Claude Skills 2.0 완전 분석](../claude/claude-skills-2.0.md)의 「Progressive Disclosure는 올바른 아키텍처 패턴」.

[^21]: [google/skills: 구글의 Agent Skills 저장소](../google/google-skills.md)의 분석과 비평 부분.

[^22]: [하네스 엔지니어링 커리큘럼 — 핵심 개념 정리](../ai/harness-engineering-curriculum.md)의 「LLM OS 비유가 포착하는 것과 놓치는 것」.

[^23]: [Lessons from Building Claude Code: How We Use Skills](../claude/lessons-from-building-claude-code-skills.md)의 「파일 시스템 & 점진적 공개를 활용하라」.

[^24]: [GPT-6 Astra 시대에는 스킬과 지침을 다시 써야 한다](../agentic-coding/gpt-6-astra-skills-and-prompts.md).

[^25]: [Claude Skills 2.0 완전 분석](../claude/claude-skills-2.0.md)의 「약점 및 한계」, [Claude Skills 제작 완전 가이드](../claude/claude-skills-guide.md)의 「description이 Skill의 성패를 결정한다」.

[^26]: [RTK — Rust Token Killer](../ai-tool/rtk.md).

[^27]: [MCP는 처음부터 잘못된 아이디어였다](../mcp/why-mcp-was-always-a-bad-idea.md).

[^28]: [서브에이전트를 메인 에이전트 루프에 합칠 때](../agentic-coding/fold-subagents-into-agent-loop.md)의 「합친 뒤에 컨텍스트가 늘어나는 비용은 짧게만 다룬다」.
