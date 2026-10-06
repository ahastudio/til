# Claude Code mods 입문: 빈 폴더에서 첫 mod를 만들기까지

원문: [Getting started with Claude Code mods / claude.dev Blog](https://claude.dev/blog/getting-started-with-claude-code-mods/)

HN 토론: <https://news.ycombinator.com/item?id=49926243> (3점, 0개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49940121> (2점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=34796>

## 소개

Addy Osmani가 2026년 10월 1일 claude.dev 블로그의 튜토리얼 분류에 올린 글이다.
빈 폴더에서 mod 하나를 처음부터 만들고,
이어서 더 큰 mod 두 개를 둘러보며 API가 무엇을 할 수 있는지 보여 준다.

글이 정의하는 mod는 Claude Code 세션 안에서 돌아가는 작은 JavaScript 또는
TypeScript 파일이다.
세션에서 일어나는 일을 지켜보거나, Claude Code가 하는 일을 바꾸거나,
터미널이나 데스크톱 앱에 자체 UI를 그릴 수 있다.
설정, 권한 규칙, 슬래시 명령, 스킬, 상태 줄도 Claude Code의 동작을 바꾸지만,
mod는 Claude Code가 하는 일을 다시 쓰거나 대체하고 사용자 정의 UI를 그린다는
점에서 한 걸음 더 나간다.
내부적으로 mod는 플러그인 안에 담겨 배포되는 훅이며, 각 mod는 세션의 모든
이벤트를 일어나는 순간에 본다.

요구 사항은 Claude Code 2.1.287 이상이다.
mod는 기본으로 켜져 있어 따로 켤 것이 없다.
글은 API가 릴리스마다 바뀔 수 있다고 경고하며, Claude Code가 mod를 불러올
때마다 그 빌드의 타입 선언을 mod의 `.claude-plugin/types/` 폴더에 써 주므로 그
선언이 자기 버전의 기준이라고 말한다.

Claude Code의 일부 기능도 mod로 만들어져 있다.
글은 `AGENTS.md` 지원과 대화 옆의 `/diff` 창을 예로 들고, 그 소스와 테스트가
공개 저장소 `anthropics/claude-code`의 `mods/` 아래에 있다고 적는다.
`AGENTS.md` 지원 mod는 이 저장소의 `claude/claude-code-agents-md.md`에, mods로
이어진 설계 제안 이슈는 `claude/claude-mods-function-hooks.md`에 정리되어 있다.

나는 이 글의 코드와 명령을 직접 실행하지 않았다.
아래의 출력 예시와 동작 설명은 모두 원문이 보여 주는 것이다.

## 동작 방식

### 폴더 구조와 진입점

mod는 동작이 JavaScript 또는 TypeScript 모듈에 들어 있는
Claude Code 플러그인이다.
세 가지가 갖춰지면 된다.
폴더는 `.claude-plugin/plugin.json` 매니페스트를 가진 평범한 플러그인이고,
`hooks/hooks.json`이 `modules` 아래에 모듈 하나를 지정하며,
모듈은 `register(on, options)`를 내보낸다.
그 안에서 `on(event, matcher?, hook)`이 훅을 하나 더한다.

모든 훅은 같은 모양이다.

```javascript
on("tool.call", { tool: "Bash" }, async ($, e, next) => {
  // $    the mods API: ui, session, state, store, fs, process, clock, http, tool, command, model, ...
  // e    this event's input, as plain data
  // next passes e to the other plugins and then to Claude Code's own behavior
  return next(e);
});
```

### 미들웨어처럼 이어지는 훅 사슬

훅은 미들웨어처럼 사슬을 이룬다.
내 훅이 먼저 돌고, `next(e)`가 이벤트를 다음 플러그인에 넘기며, 맨 아래에서
Claude Code가 원래 하려던 일을 한다.
그래서 훅이 할 수 있는 일은 세 가지로 나뉜다.

| 동작      | 방법                                          | 예                                                  |
| --------- | --------------------------------------------- | --------------------------------------------------- |
| 관찰      | `const r = await next(e);` 뒤에 살펴보고 반환 | 모든 파일 편집을 기록한다. 매 턴 뒤에 수치를 잰다   |
| 다시 쓰기 | `return next({ ...e, command: safer })`       | 사슬의 나머지가 보는 내용을 바꾼다                  |
| 응답      | `next`를 부르지 않고 `return { deny: "…" }`   | 도구 호출을 거부한다. 명령이나 도구를 직접 제공한다 |

이벤트는 도구 호출, 제출된 프롬프트, 턴의 시작과 끝, 세션의 시작과 끝,
슬래시 명령, 그리고 화면이 그려질 때의 모든 조각인 `ui.render`를 다룬다.
모듈은 DOM도 Node도 없는 자체 샌드박스에서 돌기 때문에
바깥의 모든 것은 `$`를 거친다.

### 설정 훅과 다른 점

설정 훅은 이벤트마다 셸 명령을 실행하고 stdin과 stdout으로 JSON을 주고받는다.
mod는 한 번 불러오면 세션에 계속 남는다.
그래서 상태를 유지하고, 이벤트에 맞춰 갱신되는 UI를 그리고,
창을 열거나 프로세스를 실행하거나 슬래시 명령을 등록하거나 모델이 부를 수 있는
도구를 등록하는 식으로 Claude Code를 다시 호출할 수 있다.

## 지름길: Claude에게 만들게 하기

글은 여섯 단계를 건너뛰는 방법을 먼저 제시한다.
Claude Code는 mod 작성법을 알고 있으므로,
`claude`로 세션을 열고 원하는 mod를 설명하면 된다.
Token Weather를 만드는 프롬프트는 원문에 이렇게 실려 있다.

```text
Make me a Claude Code mod called token-weather: a live forecast of my context window, shown in the band above the prompt.

What it should show, on one line:
- A weather icon and word for how full the context window is: under 25% ☀ Clear (yellow), 25–49% ☁ Cloudy (cyan), 50–74% ☂ Showers (blue), 75–89% ☇ Storm (magenta), 90% and up ↯ Compact soon (red).
- The percentage used, then the tokens used out of the window, like "134.4k / 200k".
- A small chart of the last 12 turns, drawn with ▁▂▃▄▅▆▇█.
- How much the last turn added, like "▲ +98.3k last turn".

It should update after every turn.
```

Claude는 이 세션에서 핫 리로드를 켤지 한 번 묻는다.
허락하면 Claude의 턴이 끝날 때 프롬프트 위에 띠가 나타나고,
이후의 수정은 그 자리에서 다시 불러온다.
글은 이 프롬프트가 보고 싶은 것만 설명한다는 점을 짚는다.
상태를 어디에 두어야 리로드를 견디는지,
`claude plugin validate`로 어떻게 검사하는지,
어떤 이벤트에 훅을 걸지는 Claude Code에 내장된 mod 작성 안내가 맡는다.

주의할 점이 하나 있다.
이렇게 만든 mod는 그 세션에서만 불러오고 폴더는 나중에 정리된다.
계속 쓰려면 폴더를 밖으로 복사해 일반 플러그인처럼 설치해야 한다.

## 첫 mod 만들기: Token Weather

Token Weather는 매 턴 뒤에 컨텍스트 창이 얼마나 찼는지 읽고
프롬프트 위에 한 줄을 그린다.
날씨 아이콘, 사용 비율, 창 크기 대비 사용 토큰, 최근 턴의 작은 차트,
마지막 턴이 더한 양이 들어간다.
글에 따르면 전체가 약 80줄이다.

| 사용량   | 예보           |
| -------- | -------------- |
| 25% 미만 | ☀ Clear        |
| 25–49%   | ☁ Cloudy       |
| 50–74%   | ☂ Showers      |
| 75–89%   | ☇ Storm        |
| 90% 이상 | ↯ Compact soon |

### 1단계: 폴더 만들기

먼저 버전을 확인한다.

```bash
claude --version   # 2.1.287 or later
```

구조는 다음과 같다.
`.claude-plugin/types/`는 Claude Code가 mod를 불러올 때 직접 쓰는 폴더다.

```text
token-weather/
├── .claude-plugin/
│   ├── plugin.json
│   └── types/            (written by Claude Code when it loads the mod)
├── hooks/
│   ├── hooks.json
│   └── token-weather.mjs
├── types/
│   └── index.d.ts        (added in step 3)
└── tests/
    └── token-weather.test.ts   (added in step 5)
```

`.claude-plugin/plugin.json`은 표준 플러그인 매니페스트다.

```json
{
  "name": "token-weather",
  "version": "0.1.0",
  "description": "A live forecast of the context window, drawn above the prompt.",
  "author": { "name": "You" }
}
```

`hooks/hooks.json`은 모듈을 가리킨다.
mod는 모듈을 정확히 하나 가진다.

```json
{
  "modules": ["./token-weather.mjs"]
}
```

### 2단계: 무언가 그리기

프롬프트 바로 위의 띠는 `AbovePrompt`라는 컴포넌트다.
Claude Code가 그 자리에 아무것도 그리지 않으므로 첫 대상으로 알맞다.
그 컴포넌트의 `ui.render` 이벤트에 훅을 걸고 요소 트리를 돌려준다.

```javascript
// hooks/token-weather.mjs
export function register(on) {
  on("ui.render", { component: "AbovePrompt" }, ($, e, next) => {
    const { Box, Text } = $.ui.resolve(e);
    return Box({
      paddingX: 1,
      children: [Text({ color: "yellow", bold: true, children: "☀  Clear skies" })],
    });
  });
}
```

요소는 전역이 아니다.
`$.ui.resolve(e)`가 지금 그리는 표면의 생성자를 돌려주는데,
Claude Code가 그리는 표면마다 지원하는 요소 집합이 조금씩 다르기 때문이다.
`h`를 팩토리로 쓰면 JSX도 된다.

플러그인을 불러온 채 세션을 연다.

```bash
claude --plugin-dir ./token-weather
```

프롬프트 위에 “☀ Clear skies”가 나타난다.
폴더가 감시되므로 저장할 때마다 재시작 없이 모듈이 그 자리에서 다시 로드된다.

### 3단계: 실제 수치를 읽고 `$.state`에 두기

`$.session.usage()`는 상태 줄과 같은 수치를 돌려준다.
`context.tokens`는 마지막 응답이 처리한 입력, `context.window`는 모델의 창 크기,
`context.percent`는 그 비율이다.
글은 이 호출이 공짜라고 적는다.
세부 내역을 요청할 때만 토큰 수 세기 요청을 보낸다는 것이다.

세션이 시작될 때와 매 턴 뒤에 수치를 잰다.
두 훅 모두 `next(e)`를 먼저 부르고 나서 관찰하므로 일어나는 일을 바꾸지 않는다.
`e.agentId`가 있는 턴은 서브에이전트의 턴이므로 건너뛴다.

```javascript
on("session.start", async ($, e, next) => {
  const result = await next(e);
  await takeReading($);
  return result;
});

on("turn.complete", async ($, e, next) => {
  const result = await next(e);
  if (!e.agentId) {
    await takeReading($); // main-loop turns only, not subagents
  }
  return result;
});
```

수치를 어디에 둘지가 이 단계의 핵심 결정이다.
모듈 수준의 `let readings = []`가 당연해 보이지만,
핫 리로드는 새로 불러오는 것이라 `register`가 다시 돌고
`session.start`가 다시 발생하며 모듈 변수는 처음부터 시작한다.
그래서 기록은 `$.state`에 둔다.
`$.state`는 세션 내내 호스트가 이름 붙은 값을 들고 있으므로 리로드를 견딘다.

```javascript
// Held by the host, so the history survives a hot reload of this file.
const readings = { plugin: "token-weather", key: "readings" };

async function takeReading($) {
  const { context } = await $.session.usage();
  if (!context?.window) return;
  const tokens = context.tokens ?? 0;
  const percent = context.percent ?? Math.round((tokens / context.window) * 100);
  const { value: history = [] } = await $.state.get(readings);
  await $.state.set(readings, [...history, { tokens, window: context.window, percent }].slice(-HISTORY));
}
```

상태 값은 플러그인의 타입 계약에 선언해야 한다.
매니페스트가 가리키는 작은 `.d.ts` 파일이며, `types/index.d.ts`를 더한다.

```typescript
export type TokenWeatherReading = { tokens: number; window: number; percent: number };

declare module "claude-code" {
  interface PluginState {
    "token-weather": { readings: TokenWeatherReading[] };
  }
}
```

그리고 `plugin.json`에 `"types": "./types/index.d.ts"`를 더한다.
이 단계를 건너뛰면 `claude plugin validate`가 고칠 방법을 적은 오류로 막는다.
원문이 보여 주는 오류 문구는
`token-weather.readings is not declared: the manifest's types contract must name it in interface PluginState { … }`다.

선언의 대가로 다시 그리기가 자동으로 따라온다.
렌더 훅이 도는 동안 부른 `$.state.get`은 그 그리기를 구독하므로,
이후의 모든 `$.state.set`이 띠를 다시 그린다.
`$.ui.invalidate`를 부를 일이 없다.

### 4단계: 예보 그리기

원문에 실린 전체 모듈이다.

```javascript
// Token Weather: a live forecast of the context window, above the prompt.

const HISTORY = 12;
const BARS = "▁▂▃▄▅▆▇█";
const FORECAST = [
  { upTo: 25, icon: "☀", word: "Clear", color: "yellow" },
  { upTo: 50, icon: "☁", word: "Cloudy", color: "cyan" },
  { upTo: 75, icon: "☂", word: "Showers", color: "blue" },
  { upTo: 90, icon: "☇", word: "Storm", color: "magenta" },
  { upTo: Infinity, icon: "↯", word: "Compact soon", color: "red" },
];

// Held by the host, so the history survives a hot reload of this file.
const readings = { plugin: "token-weather", key: "readings" };

export function register(on) {
  on("session.start", async ($, e, next) => {
    const result = await next(e);
    await takeReading($);
    return result;
  });

  on("turn.complete", async ($, e, next) => {
    const result = await next(e);
    if (!e.agentId) {
      await takeReading($); // main-loop turns only, not subagents
    }
    return result;
  });

  on("ui.render", { component: "AbovePrompt" }, async ($, e, next) => {
    const { value: history = [] } = await $.state.get(readings);
    if (e.props.hasSurvey || history.length === 0) {
      return next(e);
    }
    const { Box, Text } = $.ui.resolve(e);
    return band(Box, Text, history, e.props.bodyColumns);
  });
}

async function takeReading($) {
  const { context } = await $.session.usage();
  if (!context?.window) return;
  const tokens = context.tokens ?? 0;
  const percent = context.percent ?? Math.round((tokens / context.window) * 100);
  const { value: history = [] } = await $.state.get(readings);
  await $.state.set(readings, [...history, { tokens, window: context.window, percent }].slice(-HISTORY));
}

function band(Box, Text, history, columns) {
  const now = history[history.length - 1];
  const f = FORECAST.find((b) => now.percent < b.upTo);
  const parts = [
    Text({ color: f.color, bold: true, children: `${f.icon}  ${f.word}` }),
    Text({ children: `  ${now.percent}% of context` }),
    Text({ dimColor: true, children: `  ${short(now.tokens)} / ${short(now.window)}` }),
  ];
  if (columns >= 60) {
    parts.push(Text({ dimColor: true, children: "   last turns " }));
    parts.push(Text({ color: f.color, children: sparkline(history) }));
    if (history.length > 1) {
      parts.push(Text({ dimColor: true, children: trend(history) }));
    }
  }
  return Box({ flexDirection: "row", paddingX: 1, children: parts });
}

function sparkline(history) {
  const top = Math.max(...history.map((r) => r.tokens), 1);
  return history.map((r) => BARS[Math.floor((r.tokens / top) * (BARS.length - 1))]).join("");
}

function trend(history) {
  const delta = history[history.length - 1].tokens - history[history.length - 2].tokens;
  if (delta === 0) return "  steady";
  return delta > 0 ? `  ▲ +${short(delta)} last turn` : `  ▼ ${short(-delta)} last turn`;
}

function short(n) {
  if (n >= 1_000_000) return `${+(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${+(n / 1_000).toFixed(1)}k`;
  return String(n);
}
```

글이 자기 mod에 옮겨 쓸 만하다고 꼽는 세부는 세 가지다.
첫째, 컴포넌트의 props는 `e.props`에 있다.
`hasSurvey`는 설문이 띠를 쓰려 한다는 뜻이라 훅이 `next(e)`로 양보하고,
`bodyColumns`는 띠의 실제 폭으로,
대화 기록 옆에 창이 붙어 있으면 터미널보다 좁다.
`e`의 최상위에는 `e.component`, `e.surface`, `e.requestId`, `e.viewport`만 있다.
둘째, 그릴 것이 없으면 `next(e)`를 돌려 띠를 Claude Code와 다른 mod에 넘긴다.
셋째, 이모지가 아니라 한 칸 폭의 기호를 쓴다.
☀ ☁ ☂ ☇ ↯는 어떤 터미널 글꼴에서도 줄이 맞는다.

## 검증하고 테스트하기

`claude plugin validate`는 Claude Code가 하는 것과 같은 방식으로 매니페스트와
모듈 소스를 읽고, 모듈이 무엇에 훅을 걸고 무엇을 부르는지 보고한다.
원문의 출력은 다음과 같다.

```text
$ claude plugin validate ./token-weather
  > types ./types/index.d.ts declares state: token-weather.readings
  > ./token-weather.mjs hooks: session.start, turn.complete, ui.render{component=AbovePrompt}
  > ./token-weather.mjs calls: $.session.usage (via takeReading), $.state.get, $.state.set (via takeReading), $.ui.resolve
  > ./token-weather.mjs state writes: token-weather.readings
  > ./token-weather.mjs state reads: token-weather.readings
√ Validation passed
```

`claude plugin test`는 플러그인의 `*.test.ts` 파일을 실제 Claude
Code 런타임에서 돌린다.
테스트가 `on`으로 등록한 훅은
사슬에서 mod 뒤에 돌면서 Claude Code가 답했을 내용을 대신하므로,
`$.session.usage()`가 무엇을 돌려줄지 테스트가 정확히 정할 수 있다.

```typescript
// tests/token-weather.test.ts
import { describe, expect, test } from "claude-code/testing";

describe("token-weather", () => {
  test("the band follows the context window", async ($, on) => {
    // Hooks registered here run after the mod and stub what Claude Code would answer.
    let tokens = 36_100;
    on("session.start", ($, e) => ({ cwd: e.cwd }));
    on("session.usage", () => ({
      value: { startedAt: 0, rateLimits: [], context: { tokens, window: 200_000, percent: Math.round(tokens / 2_000) } },
    }));
    on("turn.complete", () => ({ text: "" }));

    await $.session.start({ surface: "terminal", isInteractive: true, cwd: "/work" } as any);
    const ui = await $.ui.mount({
      plugin: "token-weather",
      surface: "terminal",
      component: "AbovePrompt",
      props: { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 120 },
    } as any);
    expect(await ui.find({ type: "Text", text: /Clear/ })).toBeDefined();

    tokens = 134_400;
    await $.turn.complete({ reason: "answer", answer: "ok", durationMs: 1 } as any);
    expect(await ui.find({ type: "Text", text: /Showers/ })).toBeDefined();
    expect(await ui.find({ type: "Text", text: /67% of context/ })).toBeDefined();
    expect(await ui.find({ type: "Text", text: /▲ \+98\.3k last turn/ })).toBeDefined();
    await ui.unmount();
  });
});
```

```text
$ claude plugin test ./token-weather
(pass) token-weather > the band follows the context window
 1 pass
 0 fail
```

테스트의 수치를 따라가면 동작이 보인다.
200,000 토큰 창에서 36,100 토큰은 18%라 Clear이고,
134,400 토큰으로 오르면 67%라 Showers가 되며 차이는 98.3k다.
이 테스트는 3단계의 다시 그리기 동작도 함께 확인한다.
mod가 다시 그려 달라고 요청한 적이 없는데도 `turn.complete` 뒤에 띠가 갱신된다.

## 배포하기

mod는 플러그인이므로 배포도 플러그인과 같다.
가장 단순한 마켓플레이스는 `.claude-plugin/marketplace.json`을 가진 폴더 하나다.

```json
{
  "name": "my-mods",
  "owner": { "name": "You" },
  "plugins": [{ "name": "token-weather", "source": "./token-weather" }]
}
```

```bash
claude plugin marketplace add ./my-mods
claude plugin install token-weather@my-mods --scope user
```

mod를 마켓플레이스 파일과 함께 GitHub 저장소에 두면 그 저장소가 마켓플레이스가
되고, 갱신은 평소처럼 푸시하면 된다.
Claude Code 안에서 설치하는 명령은 세 개다.

```text
/plugin marketplace add your-org/my-mods
/plugin install token-weather@my-mods
/reload-plugins
```

mod는 리로드할 때 시작하며,
나타나지 않으면 Claude Code를 재시작하라고 글은 안내한다.
Claude 디렉터리도 mod를 포함한 플러그인을 받으며,
`claude.ai/directory/manage`에서 제출할 수 있다.

## 더 큰 예제 두 개

Token Weather는 지켜보고 그리기만 한다.
나머지 두 mod는 이벤트에 개입하고, 창을 열고, 입력을 받는다.
원문은 두 mod의 전체 소스가 아니라 핵심 훅만 싣고 있으며, `classify`, `measure`,
`stepsFor`, `openReplay` 같은 보조 함수의 본문은 글에 없다.

### Blast Radius: 위험한 명령을 실행 전에 붙잡기

Claude가 `rm -rf`, `git reset --hard`, `git clean`, 강제 푸시,
데이터베이스 마이그레이션을 Bash로 부르면 Blast Radius가 호출을 붙잡는다.
명령이 무엇을 건드릴지 계산하고 Proceed와 Cancel이 있는 창을 연다.
2를 누르면 Claude는 이유가 담긴 거부를 받고, 1을 누르면 명령이 그대로 실행된다.
원문의 영상은 `rm -rf build`를 붙잡아
지워질 파일 9개(1.1 MB)를 보여 주는 장면이다.

훅은 셋이다.
Bash에 대한 `tool.call`, 그리고 `Pane`과 `AbovePrompt`에 대한 `ui.render`다.
핵심은 앞의 표에서 본 응답 동작이다.

```javascript
on("tool.call", { tool: "Bash" }, async ($, e, next) => {
  const risk = classify(String(e.command ?? ""));
  if (risk === null) return next(e);                 // everything else runs as normal

  const report = await measure($, risk, await $.session.cwd());  // git status, git clean -n, du, ...
  held = { command: e.command, risk, report, decision: null };
  const opened = await $.ui.open({ id: "blast-radius", title: "Blast Radius", focus: true });
  if (!opened.isPlaced) held.where = "band";         // too narrow for a pane: draw above the prompt

  while (held.decision === null && !next.signal.aborted) {
    await $.process.run(["sleep", "0.25"]);          // time inside $ calls doesn't count against the hook's time limit
  }
  if (held.decision === "proceed") return next(e);   // let it run
  return { deny: `Blast Radius held this command: the user pressed Cancel. It would have: ${report.summary}.` };
});
```

이 예제가 가르치는 것은 네 가지다.
보고서는 `$.process.run`으로 각 도구 자신의 명령을 돌려 얻는다.
`git status --porcelain`, `git clean -n`,
`git log HEAD..origin/main`, `showmigrations`이며,
인자를 argv 배열로 넘기므로 경로에 든 어떤 것도 셸 코드로 실행되지 않는다.
훅은 디스패치마다 자기 시간 10초를 받지만
`$` 호출 안에서 기다린 시간은 세지 않는다.
그래서 버튼의 `onPress`가 결정을 정할 때까지 짧은 `sleep` 프로세스로 기다리고,
Esc를 눌러 `next.signal`이 중단되면 포기한다.
`Button({ label: "Proceed", hotkey: "1", onPress })`는 클릭, Tab과 Enter,
숫자 키로 모두 동작한다.
터미널이 충분히 넓으면 대화 기록 옆에 창을 붙이고,
`$.ui.open`이 `isPlaced: false`로 답하면 같은 보고서를 프롬프트 위 띠에 그린다.

### Replay Theater: 마지막 턴의 편집을 한 단계씩 보기

Replay Theater는 턴이 도는 동안 모든 Edit와 Write 호출을 파일과
앞뒤 텍스트까지 기록한다.
턴이 끝나면 프롬프트 위에 힌트가 뜨고,
`r`을 누르거나 `/replay`를 입력하면 번호 붙은 단계 띠와 Prev, Next,
Close 버튼이 있는 창에서 편집을 diff 하나씩 넘겨 본다.
편집을 막거나 바꾸지 않고 관찰만 한다.

```javascript
on("tool.call", async ($, e, next) => {
  if (EDIT_TOOLS.has(e.tool)) state.pending.push(...(await stepsFor($, e)));  // old/new text → diff
  return next(e);                                                              // the edit runs untouched
});

on("turn.start", ($, e, next) => { if (!e.agentId) state.pending = []; return next(e); });

on("turn.complete", async ($, e, next) => {
  const r = await next(e);
  if (!e.agentId && state.pending.length) state.replay = state.pending;       // one replay per turn
  return r;
});

on("session.start", async ($, e, next) => {
  const r = await next(e);
  await $.command.register({ name: "replay", description: "Step through the last turn's file edits" });
  return r;
});
on("command.run", { command: "replay" }, async ($, e) => ({ text: (await openReplay($)) ? "Replaying" : "No edits" }));
```

`turn.start`와 `turn.complete`가 편집을 턴 하나의 재생으로 묶고,
`e.agentId`가 서브에이전트의 턴을 그 묶음에서 뺀다.
슬래시 명령은 `session.start`에서 `$.command.register`로 등록하고
`command.run`에서 답한다.
Write의 경우 `$.fs.read`가 쓰기 직전의 기존 내용을 읽으므로
diff가 실제 내용이 된다.
창의 위치는 표면이 정한다.
전체 화면에서는 오른쪽에 붙고, 80열에서는 프롬프트 위에 인라인으로 열리며,
mod는 어느 쪽이든 같은 트리를 그린다.

## 트레이드오프

### mod와 설정 훅 중 무엇을 고를지

설정 훅은 이벤트마다 셸 명령을 새로 띄우므로 상태가 없고,
언어에 묶이지 않으며, 한 번의 호출로 끝난다.
mod는 세션에 상주하며 상태와 UI, Claude Code로의 역호출을 얻지만,
대가로 API가 릴리스마다 바뀔 수 있다는 위험을 진다.
글이 타입 선언을 버전의 기준으로 삼으라고 거듭 말하는 것은
이 위험을 인정한 것이다.
여기서부터는 내 해석이다.
명령 하나를 막거나 기록을 남기는 정도라면 설정 훅이 더 오래 버티고,
턴을 넘나드는 상태나 화면이 필요할 때 비로소 mod의 유지 비용이 정당화된다.

### 핫 리로드의 편리함과 모듈 변수의 함정

저장할 때마다 다시 불러오는 피드백 고리는 글이 mod 작성의
재미 대부분이라고 말하는 부분이다.
그러나 같은 성질이 모듈 변수를 매번 초기화한다.
Token Weather는 `$.state`로 이를 피하지만, Blast Radius와
Replay Theater의 발췌는 `held`와 `state` 같은 모듈 수준 변수를
쓰는 것처럼 보인다.
발췌에 선언부가 없으므로 이 변수가 어떻게 정의되었는지는
원문으로 확인할 수 없다.
글의 습관 목록을 그대로 따르면,
리로드 뒤에도 남아야 하는 값은 `$.state`에 두어야 한다.

### 안전망과 권한 시스템은 다르다

글은 Blast Radius가 권한 시스템이 아니라 안전망이라고 분명히 적는다.
명령 텍스트를 읽기 때문에 `$(…)`, 별칭, `rm`을 부르는 스크립트는 빠져나가며,
확실한 차단에는 권한 규칙을 쓰라고 한다.
GN의 growuplove7은 여기서 한 걸음 더 나가,
공식 권한 문서에 따르면 `tool.check`를 처리하는 mod는
권한 규칙과 `PreToolUse` 훅이 판단한 뒤에 답하며,
그 답으로 ask 규칙의 확인 창이나 managed 설정이 아닌 훅의 차단을
승인으로 바꿀 수 있다고 적었다.[^gn-growuplove7]
managed 설정이나 Team, Enterprise 로그인이 없는 개인 환경에서는 deny 규칙보다
mod의 승인이 앞선다는 것이며,
그래서 꼭 막아야 할 명령은 명령 문자열에 기대지 않는 샌드박스 설정에 두는
편이 맞다고 보았다.
이 문서 내용은 원문에 없고 나는 공식 문서에서 따로 확인하지 않았지만, 사실이라면
mod는 권한을 보조하는 장치가 아니라 권한을 뒤집을 수도 있는 층이 된다.

## 함정

- 그릴 것이 없는데 트리를 돌려주면 띠를 Claude Code와 다른 mod에게서 빼앗는다. 이때는 `next(e)`를 돌려준다.
- props를 `e`에서 찾으면 없다. `hasSurvey`, `bodyColumns` 등은 `e.props`에 있다.
- 폭을 터미널 폭으로 가정하면 창이 붙었을 때 넘친다. `bodyColumns`에 맞춘다.
- 이모지는 터미널 글꼴마다 폭이 달라 줄이 어긋난다. 한 칸 폭 기호를 쓴다.
- 서브에이전트의 턴도 `turn.complete`를 일으킨다. 메인 루프만 셀 때는 `e.agentId`를 거른다.
- 상태 값을 `PluginState`에 선언하지 않으면 `claude plugin validate`가 실패한다.
- 지름길로 만든 mod는 그 세션에서만 불러오고 폴더가 나중에 정리된다. 남기려면 밖으로 복사한다.
- 그림이 나타나지 않으면 `claude --debug`로 실행하고 훅이 검증되지 않는 트리를 돌려줬다는 줄을 찾는다.
- mod는 내 컴퓨터에서 Claude Code와 같은 접근 권한으로 돌고 Anthropic이 아니라 게시자가 쓴 코드다. 글은 패키지를 설치하듯 저장소를 먼저 읽고 신뢰하는 사람의 것만 설치하라고 한다.

## 체크리스트

- `claude --version`이 2.1.287 이상인가?
- `hooks/hooks.json`의 `modules`가 모듈 하나를 가리키는가?
- 리로드 뒤에도 남아야 하는 값이 모두 `$.state`에 있는가?
- `$.state`에 쓰는 키가 `types/index.d.ts`의 `PluginState`에 선언되어 있고 `plugin.json`이 그 파일을 가리키는가?
- 렌더 훅이 그릴 것이 없을 때 `next(e)`를 돌려주는가?
- 렌더 트리가 `e.props.bodyColumns` 안에 들어가는가?
- `claude plugin validate`가 기대한 훅과 호출만 보고하는가?
- `claude plugin test`가 Claude Code의 응답을 대신하는 훅으로 주요 상태 전이를 확인하는가?
- 확실히 막아야 하는 명령을 mod가 아니라 권한 규칙이나 샌드박스에 두었는가?

## 기억할 원칙

### 전부 `next`를 거치는 사슬이라는 것

이 글의 모든 예제는 관찰, 다시 쓰기, 응답 세 가지 중 하나로 설명된다.
Token Weather와 Replay Theater는 `next(e)`를 먼저 부르고 결과를 보는 관찰이고,
Blast Radius는 `next`를 부르지 않고 `deny`를 돌려주는 응답이다.
mod를 설계할 때 먼저 정할 것은 무엇을 그릴지가 아니라 이 훅이 사슬에서
어느 동작을 맡는지다.
관찰만 하는 mod는 실패해도 원래 동작이 남지만,
응답하는 mod는 사슬의 아래를 통째로 대신한다.

### 상태는 호스트에, 기준은 생성된 타입에

핫 리로드와 릴리스 간 API 변경이라는 두 가지 불안정성에
글은 같은 방식으로 답한다.
변하는 쪽에 기대지 말고 호스트가 쥐고 있는 쪽에 기대라는 것이다.
값은 모듈 변수가 아니라 `$.state`에, API의 기준은 기억이나 블로그 글이 아니라
Claude Code가 빌드마다 `.claude-plugin/types/`에 써 주는 선언에 둔다.
이 원칙을 따르면 이 문서의 코드가 언젠가 맞지 않게 되더라도
무엇을 확인해야 할지는 남는다.

---

[^gn-growuplove7]: <https://news.hada.io/topic?id=34796#cid66944>
