# Claude의 Advanced Tool Use

원문: [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use)

HN 토론: <https://news.ycombinator.com/item?id=46038047> (673점, 266개 댓글)

GN 토론: <https://news.hada.io/topic?id=24594>

## 요약

Anthropic 엔지니어링 팀이 2025년 11월 24일에 올린 글이다.
에이전트가 수백, 수천 개의 도구를 쓰려면 모든 도구 정의를 미리 컨텍스트에
올리지 않고 필요할 때 찾아 로드해야 한다는 전제에서, Claude Developer
Platform에 세 기능을 냈다고 밝힌다.

- Tool Search Tool: 도구를 검색해 필요한 정의만 컨텍스트에 들인다.
- Programmatic Tool Calling: 도구를 코드 실행 환경에서 호출해 중간 결과를
  컨텍스트에 넣지 않는다.
- Tool Use Examples: 도구 정의 안에 호출 예시를 넣는다.

### Tool Search Tool

글이 드는 문제는 MCP 도구 정의의 토큰 비용이다.
서버별 도구 수와 정의의 토큰은 다음과 같다.

| 서버    | 도구 수 | 토큰   |
| ------- | ------- | ------ |
| GitHub  | 35개    | 약 26K |
| Slack   | 11개    | 약 21K |
| Sentry  | 5개     | 약 3K  |
| Grafana | 5개     | 약 3K  |
| Splunk  | 2개     | 약 2K  |

이 58개 도구를 합치면 대화 시작 전에 약 55K 토큰을 쓴다고 한다.
Jira 하나만 약 17K 토큰이고, Anthropic 내부에서는 최적화 전에 도구 정의가
134K 토큰을 차지한 사례를 봤다고 한다.
토큰 비용만이 문제가 아니고, 이름이 비슷한 도구(예: `notification-send-user`와
`notification-send-channel`) 사이의 오선택과 잘못된 매개변수가 가장 흔한
실패라고 한다.

해법은 도구 정의에 `defer_loading: true`를 붙여 처음에는 컨텍스트에 올리지
않는 것이다.
Claude는 검색 도구와 `defer_loading: false`인 핵심 도구만 보다가, 필요한
기능이 생기면 검색해 해당 도구의 전체 정의만 불러온다.
글의 예에서 GitHub가 필요하면 “github”를 검색해 `github.createPullRequest`와
`github.listIssues`만 로드하고, 나머지 50개 이상은 로드하지 않는다.
지연된 도구는 첫 프롬프트에서 아예 빠지므로
프롬프트 캐싱이 깨지지 않는다고 적는다.
검색은 정규식 방식과 BM25 방식이 기본 제공되고 임베딩 등으로 만든 사용자
정의 검색도 쓸 수 있다.

글이 제시하는 수치는 다음과 같다.

| 조건                      | 전통 방식   | Tool Search Tool       |
| ------------------------- | ----------- | ---------------------- |
| 처음 올라오는 도구 정의   | 약 72K 토큰 | 검색 도구 약 500 토큰  |
| 작업 중 추가 로드         | 없음        | 3~5개 도구, 약 3K 토큰 |
| 작업 시작 전 총 소비      | 약 77K 토큰 | 약 8.7K 토큰           |
| MCP 평가 정확도(Opus 4)   | 49%         | 74%                    |
| MCP 평가 정확도(Opus 4.5) | 79.5%       | 88.1%                  |

글은 이를 토큰 사용 85% 감소로 요약한다.
쓰기 좋은 경우는 다음과 같다.

- 도구 정의가 10K 토큰을 넘을 때
- 도구 선택 정확도에 문제가 있을 때
- 여러 MCP 서버를 쓸 때
- 도구가 10개 이상일 때

효과가 작은 경우는 다음과 같다고 한다.

- 도구가 10개 미만일 때
- 모든 도구를 매 세션 자주 쓸 때
- 정의가 짧을 때

Anthropic 문서는 가장 자주 쓰는 도구 3~5개는 지연 로드하지 말라고 하고,
도구가 30~50개를 넘으면 Claude의 선택 정확도가 떨어진다고 적는다.[^ts]

### Programmatic Tool Calling

자연어 도구 호출은 호출마다 추론이 한 번 필요하고
중간 결과가 컨텍스트에 쌓인다.
Programmatic Tool Calling은 Claude가 도구 호출을 조율하는 Python 코드를
작성하고, 이 코드가 샌드박스 코드 실행 도구에서 돌며 도구 결과는 모델이
아니라 스크립트가 받게 한다.
글의 예에서 팀원 20명의 3분기 출장 경비 항목 2,000개 이상(50KB 이상)이
컨텍스트에 들어가는 대신 스크립트가 합산해 예산을 넘긴 두세 명만 돌려준다.
원시 경비 자료 200KB가 결과 1KB로 줄어든다고 한다.
글이 제시하는 측정값은 다음과 같다.

| 측정                                 | 이전   | 이후   |
| ------------------------------------ | ------ | ------ |
| 복잡한 조사 과제 평균 토큰(37% 감소) | 43,588 | 27,297 |
| 내부 지식 검색 정확도                | 25.6%  | 28.5%  |
| GIA 벤치마크                         | 46.5%  | 51.2%  |

쓰기 좋은 경우는 다음과 같다.

- 큰 자료의 집계
- 의존하는 도구 호출이 셋 이상인 흐름
- 결과를 걸러 내는 작업

단일 도구의 간단한 호출이나 Claude가 중간 결과를 직접 봐야 하는 작업에는
덜 맞는다.

### Tool Use Examples

JSON 스키마는 구조는 정의하지만 선택 매개변수를 언제 넣는지, 날짜 형식이
무엇인지, 식별자 규칙이 무엇인지는 표현하지 못한다.
도구 정의에 `input_examples`로 실제 호출 예시를 넣어 이 사용 패턴을
보여 주는 기능이다.

## 분석

### 점진적 공개로 읽기

Tool Search Tool은 도구 정의에 대한 점진적 공개(progressive disclosure)다.
Anthropic의 컨텍스트 엔지니어링 글은 같은 원리를 어휘로 쓴다.
식별자만 유지하다 필요할 때 도구로 데이터를 불러오는 방식으로 에이전트가
컨텍스트를 층층이 쌓게 하는 것이 점진적 공개를 가능하게 한다는 설명이다.[^ece]
스킬은 이름과 설명을 먼저, 본문과 참조 파일을 나중에 로드한다.
도구는 이름과 설명이 담긴 지연 목록을 먼저, 전체 정의를 나중에 로드한다.
첫 단계에 목록이 필요하고 다음 단계로 가는 검색 경로가 있다는 구조가 같다.

### 비용의 이동

글의 효과는 컨텍스트 소비를 줄이는 대신 검색 한 번의 추가 단계를 들이는
교환이다.
글은 이 교환을 스스로 인정해, 검색 단계가 있으므로 절감과 정확도 개선이
추가 지연보다 클 때 이득이라고 적는다.
Programmatic Tool Calling도 코드 실행 단계를 추가하므로 같은 구조의
조건부 이득이다.

## 비평

### 수치는 Anthropic 내부 시험이다

정확도 개선 수치(49%에서 74%, 79.5%에서 88.1%)는 내부 MCP 평가의 결과이며
평가의 구성이나 도구 수는 글에 없다.
글은 정확도 개선이 도구 수가 많은 라이브러리에서 나온 것이라고만 밝힌다.
토큰 절감 85%도 55K에서 8.7K 같은 한 가지 구성에서 계산된 값이다.

### 도구 검색이 필요 없다는 반론

HN에서 jmward01은 프로그램 호출은 당연한 다음 단계지만 도구 검색은 확신이
없다고 했다.
좋은 컨텍스트 엔지니어링이라면 필요한 도구만 미리 두므로, 전부 쓰게 될 도구에
검색을 더하면 오버헤드라는 것이다.[^jmward01]
이 의견은 글이 말하는 적용 조건과 겹친다.
글도 모든 도구를 자주 쓰는 경우는 효과가 작다고 하기 때문이다.

### 도구를 늘리는 방향이 맞는가

ra는 도구를 수백, 수천 개 쓰는 미래가 누구 말이냐고 물으며, 도구는 줄이고
그 도구를 쓰는 스킬이 나아지는 쪽으로 간다고 본다.
극단적으로는 셸 도구 하나로 충분하다는 것이다.[^ra]
dragonwriter는 셸을 중간에 두는 것도 도구 검색이나 코드에서의 도구 호출과
같은 종류의 간접화라서
실질적으로는 글의 뜻에 동의하는 셈이라고 답했다.[^dragonwriter]
post_below는 매 세션 모델이 셸 스크립트를 다시 만들면 응답이 컨텍스트에
쌓여 질이 떨어지고 비용이 늘며, 코드가 이미 있는 도구로 넘기는 편이 낫다고
반박했다.[^post_below]

도구를 아예 한 개로 줄이는 사례도 나왔다.
_pdp_의 에이전트 빌더는 `graphql` 도구 하나만 두고, 모르는 쿼리는 GraphQL
인트로스펙션(introspection)으로 알아내게 해서 50개 이상의 도구를 로드하지
않는다.[^_pdp_]
이에 대해 bravura는 인트로스펙션이 긴 정의 집합이거나 여러 번의 호출이
되어 토큰을 쓰지 않느냐고 물었다.[^bravura]
theknarf는 MCP 대신 `jira` 같은 CLI를 만들어 에이전트가 `--help`로 쓰는 법을
알게 하자고 했고,[^theknarf] arianvanp는 도구 검색이 매뉴얼 페이지를 찾는
`apropos`, `whatis`와 같다고 비유했다.[^arianvanp]

### 경쟁과 종속

jameslk는 같은 일을 하는 도구가 많아지면 도구 순위 검색 엔진이 필요하고 도구
제작자가 순위를 올리는 최적화(TEO)를 시도할 것이라고 했다.[^jameslk]
이 우려는 글이 다루지 않은 검색 결과의 편향 문제다.
michaelanckaert는 도구 검색 도구가 다른 모델과 공급자에도 쉽게 붙일 수 있는
추가 기능이라고 했고, 첫 호출에 검색 도구만 넘기고 둘째 호출에 검색된 도구를
넘기는 방식으로 직접 구현했다고 했다.[^michaelanckaert]
RobertDeNiro는 이를 Anthropic에 기대면
종속(lock-in)이 된다고 보았다.[^RobertDeNiro]
글도 사용자 정의 검색을 지원하지만 구현 방법은 다루지 않는다.

### 복잡성의 순환

tfirst는 에이전트 설계가 복잡함에서 단순함으로, 다시 복잡함으로 순환한다고
관찰했다.
거대한 스캐폴딩을 둔 에이전트에서 루프 속 단순한 LLM으로, MCP로 기능을 늘린
대가로 컨텍스트가 소비되는 단계로, 한 달 전부터는 `bash`와 파일시스템으로
갔다가 다시 복잡한 도구로 돌아왔다는 것이다.[^tfirst]
behnamoh는 도구 스키마를 미리 올린 것이 컨텍스트 낭비이며 3년 전에 이미
풀린 문제라고 말했다.[^behnamoh]

GeekNews의 kaydash는 이 기능이 Claude 모델에서는 잘 되지만 다른 모델에서는
어떨지 모르겠다는 의견을 남겼다.[^gn-kaydash]
글은 모델별 결과를 싣지 않았다.

## 인사이트

### 첫 단계의 노출 범위

첫 단계에 무엇을 보일지가 핵심 설계다.
도구는 항상 올릴 3~5개와 나머지로 나누고,
항상 올릴 것은 호출 기록으로 정한다.

### 도구와 스킬의 선택 근거

도구와 스킬은 같은 구조지만 선택의 근거가 다르다.
도구 검색은 이름, 설명, 인수 이름을 검색하고, 스킬은 시작 때 올라온
설명으로 모델이 판단한다.

### 토큰과 단계의 교환

줄어드는 것은 토큰이고 늘어나는 것은 단계다.
도구가 10개 미만이거나 전부 자주 쓰이면 이 기능을 끄는 것이 맞고,
Workday의 스킬 실험도 점진적 공개가 지연을 조금 늘린다고 보고한다.[^wd]

### 확인할 것

확인할 것은 검색 단계에서의 실패율이다.
글의 정확도 수치는 도구를 잘 고르는 쪽의 이득이며, 검색이 필요한 도구를
찾지 못하는 비율은 따로 재야 한다.

---

[^ts]: Anthropic, [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

[^ece]: Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 2025-09-29

[^wd]: Guilin Zhang 외, [Report: Progressive Disclosure of Agent Skills](https://arxiv.org/abs/2609.35692), 2026-09-28

[^jmward01]: <https://news.ycombinator.com/item?id=46039238>

[^ra]: <https://news.ycombinator.com/item?id=46040731>

[^dragonwriter]: <https://news.ycombinator.com/item?id=46041246>

[^post_below]: <https://news.ycombinator.com/item?id=46044189>

[^_pdp_]: <https://news.ycombinator.com/item?id=46039179>

[^bravura]: <https://news.ycombinator.com/item?id=46040511>

[^theknarf]: <https://news.ycombinator.com/item?id=46044438>

[^arianvanp]: <https://news.ycombinator.com/item?id=46038995>

[^jameslk]: <https://news.ycombinator.com/item?id=46038932>

[^michaelanckaert]: <https://news.ycombinator.com/item?id=46039171>

[^RobertDeNiro]: <https://news.ycombinator.com/item?id=46039306>

[^tfirst]: <https://news.ycombinator.com/item?id=46038439>

[^behnamoh]: <https://news.ycombinator.com/item?id=46038598>

[^gn-kaydash]: <https://news.hada.io/topic?id=24594#cid46836>
