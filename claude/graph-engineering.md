# Graph engineering: 직렬 에이전트를 노드와 간선으로 다시 그리는 14단계

트윗: [GRAPH ENGINEERING CON OPUS 5](https://twitter.com/angeldot_/status/2081061068516798931)

## 소개

angel(@angeldot_)이 2026년 7월 26일에 올린 스페인어 Twitter Article이다.
읽는 데 16분이 걸린다고 적혀 있고, 부제는 프롬프트에서 출발해 나를 위해 일하는
에이전트 함대를 움직이기까지의 14단계 로드맵이다.
글의 전제는 이렇다.
여러 단계를 거치는 에이전트를 만들면 대개 일직선이 되고, 그 단계의 절반은 앞 단계를
기다릴 이유가 없었다는 것이다.
글은 그 일직선을 노드(node)와 간선(edge)으로 이루어진 그래프로 다시 그리라고
가르친다.

14단계는 네 블록이다.
01~04는 이미 가진 그래프를 보는 일, 05~08은 함대를 움직이는 일,
09~11은 나온 결과를 믿을 수 있게 만드는 일, 12~14는 비용이 터지지 않게 하는 일이다.
글은 도구로 Claude Code의 동적 워크플로(dynamic workflow)를 쓴다.
Claude가 JavaScript 오케스트레이션 스크립트를 쓰고 하위 에이전트 함대가 그것을
실행하는 방식이며, 조정 자체는 코드라서 모델 토큰이 들지 않는다고 말한다.

이 문서는 글을 따라 해 볼 수 있는 노트로 다시 쓴 것이다.
글의 코드는 조각이라 그대로 돌릴 수 없어서, 정의가 빠진 변수를 채워 완결된 예제로
고쳤다.
글의 주장 가운데 Claude Code 공식 문서로 확인할 수 있는 것은 확인했고,
확인하지 못한 것은 그렇게 표시했다.
예제는 이 문서를 쓰는 동안 실행해 보지 않았다.

## 동작 방식

### 노드는 일이고 간선은 데이터다

글이 가장 먼저 세우는 구분은 두 가지다.
노드는 입력과 출력이 있는 한정된 일 하나, 곧 에이전트 하나다.
간선은 한 노드의 출력이 다른 노드의 입력이 된다는 의존성이고, 그 이상이 아니다.
글은 그리고 나서 같은 말을 일상의 문장 하나로 바꾼다.
이 파일을 요약하고 그다음에 날씨를 알려 달라는 요청에서 날씨는 요약을 쓰지 않으므로,
두 일 사이에는 간선이 없다.
순서를 나타내는 그리고 나서를 간선으로 착각하는 것이 가장 흔한 실수라는 것이다.

글이 주는 판별법은 단순하다.
호출 하나를 상자로, 한 호출의 반환값이 다른 호출의 프롬프트로 들어가는 변수를
화살표로 그린다.
화살표로 그릴 변수가 없으면 두 상자는 독립이고, 독립인 상자는 동시에 돌릴 수 있다.

### 선형 스크립트는 퇴화한 그래프다

A, B, C, D를 차례로 하는 에이전트는 가지 없는 사슬이다.
글은 사슬이 느리고 약하다고 말한다.
C가 막히면 D가 영영 돌지 않고, A가 한 일은 갈 곳 없이 위쪽에 갇힌다는 것이다.
데이터가 건너가지 않는 간선이 두세 개씩 있는 경우가 많고,
그것을 지우면 사슬이 폭이 넓은 형태로 접힌다.
독립인 노드 몇 개가 동시에 돌고, 그 결과를 모두 필요로 하는 노드 하나로 모인다.

### 노드와 간선은 계약이다

글은 노드마다 계약을 주라고 한다.
입력은 공유된 컨텍스트 창에서 짐작하지 않고 명시적으로 넘기고,
출력은 다음 노드가 추측 없이 소비할 수 있게 정해진 형태로 받는다.
워크플로에서는 `agent()` 호출에 JSON 스키마를 넘겨서 이 계약을 강제한다.
공식 문서도 `schema`를 넘기면 하위 에이전트가 산문 대신 그 모양의 JSON을 돌려준다고
적는다.[^docs]
출력이 검증에 다섯 번 실패하면 호출이 오류로 끝난다는 내용도 문서에 있다.[^docs]

간선도 계약이다.
글은 간선을 순서가 아니라 건너가는 데이터의 이름으로 부르라고 말한다.
그러면 간선이 진짜인지 바로 보이고, 모양만 유지되면 양 끝의 노드를 갈아 끼워도
그래프가 깨지지 않는다.
이 관점의 가장 실용적인 결론은 간선은 코드라는 점이다.
펼치고, 중복을 걸러내고, 거르는 감축 단계는 에이전트가 필요 없는 평범한
JavaScript다.
글은 결과를 합치는 데 에이전트를 부르고 싶은 유혹을 이겨 내라고 하면서,
`flatMap`과 `Set`이면 결정적이고 즉각적이며 토큰이 들지 않는다고 말한다.

### 병렬은 장벽이고 파이프라인은 장벽이 없다

N개의 독립 노드는 `parallel()`로 한꺼번에 연다.
공식 문서는 `parallel()`이 일련의 에이전트 작업을 동시에 돌리고 전부 끝나기를
기다린다고 설명한다.[^docs]
글은 이를 장벽(barrier)이라고 부르고, 한 단계가 끝나야 다음 단계가 시작되는 지점이라고
말한다.
반면 `pipeline()`은 항목마다 하위 에이전트를 하나씩 돌린다고 문서에 나와 있다.[^docs]
글은 `pipeline()`에서는 항목 A가 3단계에 있을 때 B가 아직 1단계에 있을 수 있어서,
빠른 항목이 느린 항목 뒤에서 서 있지 않아도 된다고 설명한다.
글의 결론은 파이프라인을 기본으로 하고, 장벽은 한 단계가 모든 앞선 결과를 한꺼번에
필요로 할 때만 쓰라는 것이다.

### 실패는 null이 된다

글은 `parallel()` 안에서 예외를 던진 작업이 배치 전체를 무너뜨리는 대신 null이 된다고
쓴다.
공식 문서의 서술은 조금 다르다.
`agent()` 호출은 중간에 멈췄거나 복구할 수 없는 API 오류를 만나면 null이 되고,
`parallel()`이나 `pipeline()` 안에서는 그 null이 결과 배열에 남은 채 실행이 계속된다고
적혀 있다.[^docs]
스크립트 코드가 던진 예외까지 null이 되는지는 문서에 없다.
어느 쪽이든 결과를 쓰기 전에 `.filter(Boolean)`으로 null을 걸러야 한다는 점은
글과 문서가 같다.[^docs]

## 구현하기

### 갈래 펼치기, 감축, 합성

글의 7단계가 말하는 기본 위상은 다이아몬드다.
한 노드가 일을 나누고, 여러 노드가 병렬로 일하고, 한 노드가 합친다.
갈래를 펼쳐 폭을 얻고, 평범한 코드로 줄이고, 마지막 에이전트가 답을 쓴다.

글의 코드는 두 군데에서 서로 맞지 않는다.
3단계의 스키마는 항목 하나(`titulo`, `url`, `impacto`)를 돌려주는데,
6단계는 `c.items`를 펼친다.
그리고 4단계는 중복 제거를 `flatMap`과 `Set`에 맡기라고 해 놓고,
6단계의 예제는 중복 제거와 정렬을 에이전트에게 시킨다.
아래 예제는 둘 다 고쳤다.
스키마는 `items` 배열을 돌려주고, 중복 제거와 정렬은 코드가 하고,
에이전트는 합성에만 쓴다.

```javascript
export const meta = {
  name: 'ecosystem-scan',
  description: 'Fan out source research, reduce in plain JS, synthesize once',
  phases: [{ title: 'Research' }, { title: 'Synthesize' }],
}

// 입력: 저장된 워크플로라면 args로 받는다. 없으면 기본 목록을 쓴다.
const SOURCES = args?.sources ?? [
  { key: 'releases', prompt: 'List notable Claude Code releases this month.' },
  { key: 'blogs', prompt: 'List notable posts about agent orchestration this month.' },
  { key: 'forums', prompt: 'List notable forum threads about Claude Code workflows this month.' },
]

// 노드의 출력 계약: 항목 하나가 아니라 항목 배열을 돌려준다.
const ITEM = {
  type: 'object',
  additionalProperties: false,
  properties: {
    title: { type: 'string' },
    url: { type: 'string' },
    impact: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
  required: ['title', 'url', 'impact'],
}
const RESULT = {
  type: 'object',
  additionalProperties: false,
  properties: { items: { type: 'array', items: ITEM } },
  required: ['items'],
}

phase('Research')
const raw = await parallel(
  SOURCES.map((s) => () =>
    agent(s.prompt, { label: `research:${s.key}`, phase: 'Research', schema: RESULT }),
  ),
)

// 간선: 코드만 쓴다. null(실패한 노드)은 버린다.
const collected = raw.filter(Boolean)
log(`sources ok: ${collected.length}/${SOURCES.length}`)

const byUrl = new Map()
for (const item of collected.flatMap((c) => c.items)) {
  if (!byUrl.has(item.url)) byUrl.set(item.url, item) // URL이 같으면 같은 항목
}
const rank = { high: 0, medium: 1, low: 2 }
const curated = [...byUrl.values()].sort((a, b) => rank[a.impact] - rank[b.impact])

// 판단이 필요한 마지막 노드만 에이전트다.
phase('Synthesize')
const summary = await agent(
  `Write a short briefing from these items, most impactful first:\n${JSON.stringify(curated)}`,
  { label: 'synthesize', phase: 'Synthesize' },
)

return { count: curated.length, summary }
```

공식 문서가 요구하는 모양에 맞추었다.
스크립트는 `export const meta`로 시작하고, `meta`는 값만 담은 객체 리터럴이어야 하며,
`phases`의 제목은 `phase()`에 넘기는 제목과 정확히 같아야 한다.[^docs]
`log()`로 진행 메시지를 보이고 `args`로 입력을 받는 방식도 문서에 있다.[^docs]

### 라우터: 모델이 분류하고 코드가 갈래를 고른다

글의 8단계는 실행 중에 간선을 고르는 라우터를 보여 준다.
에이전트는 무엇인지를 분류하고, `if`가 무엇을 할지를 정한다.
같은 분류에는 언제나 같은 갈래가 선택되므로, 에이전트가 감사를 건너뛰기로 했다는
식의 돌발은 그래프에 쓰여 있지 않은 한 생기지 않는다는 것이 글의 논리다.

```javascript
export const meta = {
  name: 'diff-review',
  description: 'Classify a diff, then pick a quick review or a parallel audit',
}

const DIFF = args?.diff ?? ''
const FILES = args?.files ?? []

const { severity } = await agent(`Classify the risk of this diff:\n${DIFF}`, {
  label: 'route',
  schema: {
    type: 'object',
    additionalProperties: false,
    properties: { severity: { type: 'string', enum: ['low', 'high'] } },
    required: ['severity'],
  },
})

let review
if (severity === 'high') {
  // 위험이 높으면 파일마다 하나씩 병렬로 감사한다.
  review = (await parallel(FILES.map((f) => () => agent(`Audit ${f} for defects.`, { label: f }))))
    .filter(Boolean)
} else {
  review = await agent(`Quick review of this diff:\n${DIFF}`, { label: 'quick-review' })
}

return { severity, review }
```

### 끝나지 않는 탐색: 마를 때까지 돌되 수렴하게 한다

크기를 모르는 탐색에는 고리가 필요하다.
글의 11단계는 연속 K라운드 동안 새것이 나오지 않으면 멈추는 방식을 권한다.
이 방식이 성공하는 지점은 무엇에 대해 중복을 거르느냐다.
글은 확인된 것이 아니라 본 것 전체에 대해 걸러야 한다고 말한다.
확인된 것에 대해서만 걸러 내면 기각된 발견이 라운드마다 다시 나타나서,
고리가 영영 마르지 않는다는 것이다.

글의 코드에는 상한이 없다.
같은 글이 모든 고리에는 라운드 상한이 있어야 한다고 말하는데,
예제의 `while`은 건조한 라운드가 두 번 이어질 때만 멈춘다.
아래 예제는 상한을 더했다.

```javascript
export const meta = {
  name: 'bug-sweep',
  description: 'Search in rounds, verify new findings with 3 lenses, stop when dry',
}

const SEARCHERS = args?.searchers ?? [
  { key: 'auth', prompt: 'Find bugs related to authentication in src/.' },
  { key: 'io', prompt: 'Find bugs related to file and network I/O in src/.' },
]
const LENSES = ['correctness', 'security', 'reproducibility']
const DRY_ROUNDS = 2 // 연속으로 새것이 없는 라운드 수
const MAX_ROUNDS = 5 // 수렴하지 않아도 여기서 끝낸다

const BUGS = {
  type: 'object',
  additionalProperties: false,
  properties: {
    bugs: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        properties: { file: { type: 'string' }, desc: { type: 'string' } },
        required: ['file', 'desc'],
      },
    },
  },
  required: ['bugs'],
}
const VERDICT = {
  type: 'object',
  additionalProperties: false,
  properties: { real: { type: 'boolean' } },
  required: ['real'],
}

const key = (b) => `${b.file}::${b.desc}`
const seen = new Set() // 확인된 것이 아니라 본 것 전체
const confirmed = []
let dry = 0

for (let round = 1; round <= MAX_ROUNDS && dry < DRY_ROUNDS; round++) {
  const found = (
    await parallel(SEARCHERS.map((s) => () => agent(s.prompt, { label: `search:${s.key}`, schema: BUGS })))
  )
    .filter(Boolean)
    .flatMap((r) => r.bugs)

  const fresh = found.filter((b) => !seen.has(key(b)))
  if (fresh.length === 0) { dry++; continue }
  dry = 0
  fresh.forEach((b) => seen.add(key(b)))

  // 발견마다 서로 다른 관점의 검증자 셋. 둘 이상이 진짜라고 하면 통과.
  const judged = await parallel(
    fresh.map((b) => async () => {
      const votes = (
        await parallel(
          LENSES.map((lens) => () =>
            agent(`Judge from the ${lens} angle: is this a real bug? ${b.desc} (${b.file})`, {
              label: `verify:${lens}`,
              schema: VERDICT,
            }),
          ),
        )
      ).filter(Boolean)
      return { bug: b, real: votes.filter((v) => v.real).length >= 2 }
    }),
  )
  confirmed.push(...judged.filter(Boolean).filter((j) => j.real).map((j) => j.bug))
}

return confirmed
```

## 값 정하기

| 값                                  | 시작값                                            | 근거                                                                                                                     | 무엇을 재서 고치는가                                                          |
| ----------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| 발견당 검증자 수                    | 서로 다른 관점 3명, 2명 이상이 진짜라고 하면 통과 | 글의 9단계가 같은 질문을 하는 검증자 둘을 두지 말라고 하고, 글의 11단계 예제가 3관점 2표를 쓴다                          | 통과한 발견 중 사람이 보기에 가짜인 비율, 발견당 추가되는 에이전트 3개의 비용 |
| 연속 건조 라운드                    | 2                                                 | 글과 공식 문서의 예시 프롬프트가 모두 연속 두 라운드를 말한다[^docs]                                                     | 라운드마다 새로 나온 발견 수, 마지막 새 발견이 몇 번째 라운드였는지           |
| 최대 라운드                         | 5                                                 | 필자의 제안이다. 수렴하지 않아도 끝나게 하는 안전장치다                                                                  | 라운드당 에이전트 수 × 5가 실행당 상한과 비용 경고선 안에 드는지              |
| 병렬 동시성                         | 기본값 그대로                                     | 기본은 동시 16개이고 CPU가 적으면 더 적다. 환경 변수로 1~256까지 조정한다[^docs]                                         | 대기열이 길어져 한 단계가 얼마나 늦어지는지                                   |
| 한 호출의 항목 수와 실행당 에이전트 | 4,096개와 1,000개 이내                            | 문서에 나온 상한이다. 4,096개를 넘기면 실행이 오류를 내고, 한 실행에서 에이전트는 1,000개까지다[^docs]                   | 고리가 있는 설계에서 누적 에이전트 수                                         |
| 규모 가이드                         | 기본 medium(에이전트 10개 미만)                   | 문서의 기본값이다. 글이 말하는 수십~수백 개는 이 기본값을 넘으므로 large나 unrestricted가 필요하다[^docs]                | `/workflows`의 에이전트별 토큰 사용량                                         |
| 모델                                | 반복 노드는 작은 모델, 합성 노드는 세션 모델      | 글의 12단계. 문서는 스크립트가 단계에 지정한 모델이 호출별 모델로 취급되고, 지정이 없으면 세션 모델로 돈다고 한다[^docs] | 작은 모델로 낮춘 뒤 출력 품질의 변화                                          |

## 트레이드오프

### 장벽을 둘지 파이프라인으로 흘릴지

장벽은 이해하기 쉽다.
모든 결과가 모인 뒤에 다음 단계가 시작되므로, 중복 제거나 전체 순위 매기기처럼 전체가
필요한 일을 한 지점에서 처리할 수 있다.
비용은 가장 느린 노드를 모두가 기다린다는 점이다.
파이프라인은 항목마다 독립적으로 흘러서 빠른 항목이 먼저 끝난다.
대신 단계 사이에 전체를 보는 일을 넣을 수 없다.
글은 단계가 분리된 느낌이 든다거나 더 깔끔하다는 이유로는 장벽을 정당화하지 못하며,
장벽의 지연은 측정할 수 있는 낭비라고 말한다.
그 말이 맞는지는 같은 입력으로 두 방식의 소요 시간을 재 보아야 안다.

### 검증자가 늘수록 믿음은 커지고 비용도 같이 커진다

발견마다 검증자 셋을 두면 한 번에 지나가는 오류가 줄지만 에이전트 수가 발견 수의
세 배로 는다.
검증을 줄이면 비용은 줄고, 검증된 척하는 발견이 섞인다.
글은 같은 에이전트가 자기 결과를 검증하면 자기 오류의 대부분을 놓친다고 말한다.
그래서 검증자는 반드시 다른 에이전트이고, 서로 다른 질문을 해야 한다.
그러나 관점을 다양하게 한다고 검증자의 오류가 독립이 되지는 않는다.
같은 모델이 만든 검증자는 같은 종류의 맹점을 공유할 수 있다.
이는 글에 없는 필자의 경고다.

### 그래프를 쓰지 않는 선택

글은 7단계와 8단계 사이에 반대 규칙을 따로 둔다.
그래프는 폭을 사지, 더 나은 판단을 사지 않는다는 것이다.
모든 단계가 앞 단계의 전체 그림을 필요로 한다면 일을 나누어도 더 좋은 답은 나오지
않고, 같은 답이 더 비싸고 더 늦게 나온다.
일이 서로의 결과를 읽지 않는 몫으로 갈라지는 순간에야 그래프가 값을 한다.
글은 갈라지지 않으면 에이전트 하나로 두고 남은 6단계를 건너뛰라고까지 말한다.

### 간선에 에이전트를 쓰지 않는 선택

결과를 합치는 일에 에이전트를 부르지 않으면 토큰이 들지 않고 결과가 결정적이다.
대신 코드가 이해할 수 있는 기준, 곧 같은 URL이나 같은 키로만 중복을 판단할 수 있다.
뜻이 같은데 표현이 다른 항목은 코드가 알아보지 못한다.
의미 기준의 중복 제거가 필요하다면 그 지점은 간선이 아니라 판단이 필요한 노드이고,
에이전트를 쓰는 것이 맞다.
글이 4단계에서 6단계로 넘어가며 이 경계를 모호하게 쓴 이유도 여기에 있어 보인다.
이는 필자의 해석이다.

## 함정

- 스키마가 호출 사이에 어긋나는 경우다.
  한 노드는 항목 하나를 돌려주는데 다음 코드는 `.items`를 펼치면, 오류 없이
  `undefined`가 흘러간다.
  노드 출력의 스키마와 그것을 읽는 코드를 한 화면에서 맞대어 확인해야 한다.
- 실패한 노드를 조용히 버리는 경우다.
  `.filter(Boolean)`은 실행이 끝까지 가게 하지만, 실패한 소스는 결과에서 그냥
  사라진다.
  예제의 `log()`처럼 성공한 개수를 남겨서 빠진 소스를 알 수 있어야 한다.
- 고리에 상한이 없는 경우다.
  건조한 라운드만 종료 조건이면 수렴하지 않는 탐색이 에이전트를 계속 만든다.
  라운드 상한과 한 실행의 에이전트 상한(1,000개)이 안전장치다.[^docs]
- 재개하면 일이 다시 도는 경우다.
  문서에 따르면 실패한 에이전트가 있으면 그 뒤에 시작된 에이전트가 이미 끝났어도 다시
  돈다.
  A, B, C, D 순으로 시작했는데 B가 실패하면 재개 시 A는 저장된 결과를 쓰고
  B, C, D가 다시 돈다.[^docs]
- 시각과 난수를 쓰는 경우다.
  문서에 따르면 스크립트 안에서 `Date.now()`와 `Math.random()`과 인자 없는
  `new Date()`는 예외를 던진다.
  재개한 실행이 같은 `agent()` 호출을 되풀이하도록 하기 위해서이고, 시각이 필요하면
  `args`로 넘겨야 한다.[^docs]
- 스크립트에서 `import()`를 쓰는 경우다.
  모듈을 불러오는 스크립트는 실행이 시작되기 전에 실패한다.
  라이브러리가 필요한 일은 에이전트의 작업으로 넘겨야 한다.[^docs]
- 병렬 쓰기가 같은 파일을 건드리는 경우다.
  글은 한 파일에 쓰는 노드는 하나여야 하고, 병렬로 쓰는 노드는 각자의 git
  worktree에서 일해야 한다고 말한다.
  문서도 많은 파일을 옮기는 예시에서 파일마다 격리된 사본에서 작업하게 한다.[^docs]
- 비용이 예상보다 큰 경우다.
  문서는 워크플로 한 번이 같은 일을 대화로 할 때보다 의미 있게 많은 토큰을 쓸 수
  있다고 경고한다.[^docs]
  에이전트가 25개를 넘거나 예상 토큰이 150만을 넘으면 진행 줄에 큰 워크플로 경고가
  뜬다.[^docs]
  글의 세 번째 블록이 비용을 낮추는 방법을 말하지만, 줄어든다는 수치는 없다.

## 확인하기

1. 지금 쓰는 직렬 에이전트의 단계를 상자로, 한 단계의 반환값이 다음 단계의
   프롬프트에 들어가는 곳을 화살표로 종이에 그린다.
   화살표가 없는 연결의 수를 센다.
   글은 그 수가 두세 개일 때가 많고, 그것을 지우는 일이 비용 없이 대기를 가장 많이
   줄인다고 말한다.
2. 작은 조각으로 먼저 실행한다.
   문서는 큰 일을 하기 전에 한 디렉터리나 좁은 질문으로 시험해 비용을 가늠하라고
   권한다.[^docs]
   Claude Code에서는 `use a workflow to ...`라고 요청하면 Claude가 스크립트를 쓴다.[^docs]
3. `/workflows`를 열어 단계마다 에이전트 수와 토큰 사용량을 본다.
   멈추고 싶으면 거기서 중단할 수 있다.[^docs]
4. 같은 입력으로 장벽을 둔 `parallel()` 두 단계와 `pipeline()`을 각각 돌려
   전체 소요 시간을 비교한다.
5. 결과가 마음에 들면 `/workflows`에서 실행을 선택해 `s`로 저장한다.
   `.claude/workflows/`에 저장하면 저장소를 받은 사람이 `/<이름>`으로 실행할 수
   있다.[^docs]

## 체크리스트

- 데이터가 건너가지 않는 간선을 모두 지웠는가?
- 일이 실제로 서로의 결과를 읽지 않는 몫으로 갈라지는가?
- 모든 노드에 한정된 입력, 정해진 형태의 출력, 하나의 일이 있는가?
- 노드의 출력 스키마와 그것을 읽는 코드의 필드 이름이 일치하는가?
- `flatMap`과 `Set`으로 되는 일에 에이전트를 쓰지 않았는가?
- 모든 결과가 모일 필요가 없는 곳에 장벽이 있지 않은가?
- 검증을 거치지 않고 결과에 닿는 발견이 없는가?
- 두 검증자가 같은 질문을 하지는 않는가?
- 모든 고리에 라운드 상한이 있고, 중복은 확인된 것이 아니라 본 것 전체에 대해
  거르는가?
- 같은 파일에 쓰는 노드가 둘 이상이지 않은가?
- 반복 노드가 비싼 모델로 돌고 있지 않은가?

글은 이 중 셋 넘게 어긋나면 그래프가 아니라 단계만 많은 사슬이라고 말한다.

## 비평

### 글의 코드는 서로 맞지 않고 그대로 돌릴 수 없다

글의 코드는 조각이라 `FUENTES`, `CURADO`, `BUGS`, `VEREDICTO`, `clave` 같은 이름이
정의되어 있지 않다.
거기에 더해 앞에서 짚은 어긋남이 있다.
스키마는 항목 하나인데 코드는 `items`를 펼친다.
간선에는 에이전트를 쓰지 말라는 본문과 달리 예제는 중복 제거에 에이전트를 쓴다.
고리에 상한이 있어야 한다는 규칙과 달리 예제에는 상한이 없다.
따라서 글은 개념을 가르치는 데는 쓸 만하지만, 코드를 복사해 쓰기에는 믿기 어렵다.

### 효과의 크기는 숫자로 뒷받침되지 않는다

글은 파이프라인이 지연을 줄이고, 모델 단계화가 품질을 건드리지 않고 비용을 낮추며,
거짓 간선을 지우는 일이 어떤 도구보다 많은 대기를 없앤다고 말한다.
그러나 어떤 측정도 보여 주지 않는다.
공식 문서는 오히려 워크플로가 같은 일을 대화로 하는 것보다 의미 있게 많은 토큰을 쓸 수
있다고 경고한다.[^docs]
글의 약속은 구조가 바르면 비용이 줄어든다는 쪽이고, 문서의 경고는 규모가 커지면
비용이 는다는 쪽이다.
두 말은 모순이 아니지만, 글이 둘 중 어느 쪽에 얼마나 해당하는지는 독자가 재어
보아야 한다.

### 일부 서술은 공식 문서와 다르거나 문서에서 확인되지 않는다

null이 되는 조건이 앞서 본 대로 다르다.
글은 예외를 던진 작업이 null이 된다고 쓰고, 문서는 멈췄거나 복구할 수 없는 API 오류를
만난 에이전트 호출이 null이 된다고 쓴다.[^docs]
글이 쓰는 `agentType: 'general-purpose'` 옵션은 필자가 읽은 문서 페이지에서
찾지 못했다.
글의 병렬 한도 서술은 코어 수에 대략 맞춘다는 정도인데, 문서는 기본 16개이고
환경 변수로 바꾼다고 구체적으로 적는다.[^docs]
글이 말하지 않는 상한, 곧 호출당 4,096개와 실행당 1,000개도 설계에 영향을 준다.[^docs]

### 예시 출력의 성격을 밝히지 않는다

14단계에는 `/workflows` 화면처럼 보이는 출력이 실려 있다.
단계별 개수와 토큰과 시간이 적혀 있고, 검증이 11/18 진행 중이라고 보인다.
이것이 실제 실행에서 나온 출력인지 설명을 위한 구성인지 글은 밝히지 않는다.
문서가 설명하는 `/workflows`의 진행 화면은 단계마다 에이전트 수를 보여 준다는
정도이므로, 화면 모양은 맞아 보여도 숫자의 출처는 확인할 수 없다.[^docs]

## 기억할 원칙

### 에이전트는 판단에 쓰고 배관은 코드에 맡긴다

노드가 해야 하는 일은 판단이다.
분류하고, 평가하고, 글을 쓰는 일이 그렇다.
펼치고, 거르고, 정렬하고, 갈래를 고르는 일은 코드가 더 싸고 정확하다.
이 구분은 비용 문제이면서 신뢰 문제다.
에이전트가 갈래를 고르면 같은 입력에 다른 길이 나올 수 있지만, 코드의 `if`는
그렇지 않다.

### 갈라지지 않는 일에는 그래프가 필요 없다

그래프가 사는 것은 폭이다.
모든 단계가 앞 단계의 전체를 필요로 하는 일이라면 에이전트 하나가 같은 답을 더 싸게
낸다.
그래프를 그리기 전에 물을 것은 일이 어디서 갈라지는가 하나다.
갈라지는 곳이 없으면 거기서 멈추는 것이 이 로드맵이 스스로 내놓는 결론이다.

---

[^docs]: Claude Code Docs, [Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
