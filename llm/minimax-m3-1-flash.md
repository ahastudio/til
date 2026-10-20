# MiniMax-M3.1-Flash: Vercel AI Gateway로 호출하는 100만 토큰 추론 모델

<https://vercel.com/ai-gateway/models/minimax-m3.1-flash>

HN 토론: <https://news.ycombinator.com/item?id=50154540> (316점, 132개 댓글)

GN 토론: <https://news.hada.io/topic?id=35657>

## 소개

Vercel AI Gateway의 모델 페이지는 MiniMax-M3.1-Flash를
에이전트 추론, 도구 호출, 코딩, 긴 컨텍스트 작업을 위한
M 시리즈 언어 모델로 소개한다.
컨텍스트 창은 100만 토큰이다.
M3와 비교해 항상 켜진 추론(always-on reasoning)과
조절 가능한 추론 강도(reasoning effort)가 추가되었다고 한다.
페이지의 출시일은 2026년 10월 19일이다.

이 페이지는 모델을 만든 쪽의 글이 아니라 중개 서비스의 호출 안내다.
그래서 벤치마크 점수, 가중치 공개 여부, `Flash`라는 이름의 의미는 페이지에 없다.
이 문서는 페이지에 있는 사양과 호출 방법만 정리하고,
없는 내용은 확인하지 못했다고 표시한다.
HN 토론은 MiniMax가 같은 모델을 발표한
글(`minimax.io/blog/minimax-m31f`)에 달린 것이다.
가중치가 아직 공개되지 않았다는 점은 terhechte가 짚었고,
penagwin은 MiniMax 웹사이트의 FAQ가
총 4,280억 개 파라미터에 활성 230억 개라고 한다며
요즘 Flash 모델이 작지도 빠르지도 않은 경우가
많다고 적었다.[^terhechte][^penagwin]
MiniMax의 발표 글도 가중치를 나중에 공개한다고 적는다.
사용에는 MiniMax의 이용 약관과 개인정보 처리방침이 적용된다고 페이지가 밝힌다.

## 사양

페이지의 제공자 표에서 읽은 값은 다음과 같다.
아래 수치는 모델이 나온 직후인 2026년 10월 19일에 게시된 페이지의 값이다.

| 항목          | 값                                      |
| ------------- | --------------------------------------- |
| 모델 ID       | `minimax/minimax-m3.1-flash`            |
| 제공자        | MiniMax                                 |
| 컨텍스트      | 100만 토큰                              |
| 최대 출력     | 524,288 토큰(표에는 524K로 표시)        |
| 지연(latency) | 1.4초                                   |
| 처리량        | 초당 52 토큰                            |
| 캐시 적중률   | 94%                                     |
| 가격          | 입력과 출력 모두 무료로 표시            |
| 입력 형식     | 텍스트, 이미지(URL, base64, Uint8Array) |

같은 페이지의 모델 목록에는 `minimax/minimax-m3`도 있다.
M3는 컨텍스트 100만 토큰, 지연 0.5초, 처리량 초당 178 토큰이고
입력은 100만 토큰당 $0.24부터, 출력은 $0.96부터이며 캐시 읽기는 $0.05이다.
출시일은 2026년 5월 31일이다.

두 모델의 숫자를 나란히 놓으면 눈에 띄는 점이 있다.
Flash라는 이름과 달리 이 표에서는
M3.1-Flash의 지연과 처리량이 M3보다 나쁘게 나온다.
다만 출시 하루 뒤의 측정이고 부하와 제공자 상태에 따라 달라지는 값이므로
이를 모델의 성질로 읽기는 이르다.
확인한 사실은 페이지에 그렇게 표시되어 있다는 점까지다.

페이지에 표시된 무료 가격을 그대로 믿으면 안 된다.
MiniMax의 발표 글은 100만 토큰당 입력 $0.15, 출력 $0.60,
캐시 입력 $0.015로 단일 요금을 적는다. minimaxir는 이를 M3의 $0.30, $1.20,
$0.06과 비교해 입력과 캐시 읽기가 절반으로 줄어 발표에서
밝힌 사용 비용 70% 절감이 그럴듯하다고 계산했다.[^minimaxir]

## 호출하기

AI SDK(`ai` 패키지)와 AI Gateway의 API 키만 있으면 된다.
페이지의 설명대로 설치하고 키를 환경 변수에 둔다.

```bash
pnpm add ai dotenv
echo 'AI_GATEWAY_API_KEY=여기에_키' > .env
```

가장 짧은 호출은 모델 ID만 넣는 형태다.
이 코드는 페이지의 예시이며
이 문서를 쓰는 동안 직접 실행해 보지 못했다(API 키가 없다).

```typescript
import { generateText } from 'ai';
import 'dotenv/config';

async function main() {
  const result = await generateText({
    model: 'minimax/minimax-m3.1-flash', // creator/model 형식
    prompt: 'Why is the sky blue?',
  });
  console.log(result.text);
}

main().catch(console.error);
```

AI SDK 외에도 OpenAI Chat Completions, OpenAI Responses,
Anthropic Messages API에서
기본 주소(base URL)만 바꿔 같은 모델을 부를 수 있다고 한다.
게이트웨이가 요청을 인증하고 사용 가능한 제공자로 보낸다.

## 추론 강도 정하기

`maxOutputTokens`는 생성 토큰의 상한이고
이 모델은 최대 524,288 토큰까지 지원한다.
추론 토큰도 이 상한에 포함된다는 점이 중요하다.
상한을 너무 낮게 잡으면 답이 나오기 전에 추론에서 토큰이 소진될 수 있다.
이는 페이지에 적힌 규칙에서 이 문서가 이끌어 낸 추론이다.

추론 강도는 API 형식마다 쓰는 자리가 다르고
게이트웨이가 이를 모델의 설정으로 바꿔 준다.

| 호출 방식                    | 추론을 지정하는 곳                   |
| ---------------------------- | ------------------------------------ |
| AI SDK 7 이상                | 최상위 `reasoning`                   |
| Chat Completions와 Responses | `reasoning.effort`                   |
| Anthropic Messages           | 토큰 예산을 쓰는 네이티브 `thinking` |

`reasoning`이 받는 값은 `provider-default`, `none`, `minimal`, `low`, `medium`,
`high`, `xhigh`다.
`providerOptions` 안의 추론 설정은 최상위 값보다 항상 우선하고
두 값을 합치지 않는다.
둘을 함께 넣으면 최상위 값은 무시된다는 뜻이다.

```typescript
const result = await generateText({
  model: 'minimax/minimax-m3.1-flash',
  prompt: 'Explain the Monty Hall problem step by step.',
  reasoning: 'high',
});
```

페이지는 어떤 작업에 어떤 강도를 쓰라는 기준을 주지 않는다.
이 모델이 항상 추론한다고 소개되므로 `none`이 추론을 정말 끄는지도
페이지만으로는 알 수 없다.
정하는 방법은 측정밖에 없다.
같은 질문 묶음을 `low`, `medium`, `high`로 돌려 정답률,
출력 토큰 수(추론 토큰 포함),
응답 시간을 비교해 작업별 기본값을 정한다. simonw는 이 모델의 추론 흔적이
“We need provide SVG code”처럼 줄여 쓴 영어라고 소개했는데,
추론 길이가 출력 토큰으로 얼마나 계산되는지는 직접 재 봐야 안다.[^simonw]

## 라우팅 옵션과 트레이드오프

게이트웨이 라우팅 옵션은 `providerOptions.gateway` 아래에 넣는다.

| 옵션                | 동작                                                 |
| ------------------- | ---------------------------------------------------- |
| `only`              | 제공자 슬러그 허용 목록. 목록 안에서만 장애 조치한다 |
| `order`             | 선호 순서. 목록에 없는 제공자도 대체 후보로 남는다   |
| `sort`              | `cost`, `ttft`, `tps` 중 하나로 후보를 정렬한다      |
| `zeroDataRetention` | 데이터 보존 없는 정책을 가진 제공자로만 라우팅한다   |

```typescript
const result = await generateText({
  model: 'minimax/minimax-m3.1-flash',
  prompt: 'Why is the sky blue?',
  providerOptions: { gateway: { only: ['minimax'] } },
});
```

### only는 가용성을 포기하고 통제를 얻는다

`only`는 허용 목록이어서 목록의 제공자를 모두 쓸 수 없으면 요청이 실패한다.
다른 제공자로 넘어가지 않는다.
이 페이지의 제공자 표에는 MiniMax 한 곳만 보이므로
이 모델에서는 `only: ['minimax']`가 라우팅 결과를 바꾸지 않는다.
얻는 것은 나중에 제공자가 늘어도 의도하지 않은 곳으로 가지 않는다는 보장이고,
잃는 것은 그때 장애 조치가 막힌다는 점이다.

### order는 선호를 표현하되 보장하지 않는다

`order`는 목록의 제공자를 먼저 시도하지만
나머지 제공자도 대체 후보로 두므로 요청이 선호하지 않은 곳으로 갈 수 있다.
데이터가 특정 제공자 밖으로 나가면 안 되는 요구에는
쓸 수 없고 `only`를 써야 한다.

### zeroDataRetention의 실패 방식은 문서에 없다

`zeroDataRetention`을 켜면 정책을 가진 제공자로만 라우팅한다.
페이지의 표에는 ZDR 열이 있지만
이 모델의 값은 텍스트에서 확실히 읽히지 않아 확인하지 못했다.
해당 제공자가 정책을 갖지 않았을 때 요청이 실패하는지는 페이지에 적혀 있지 않다.
의존하기 전에 작은 요청으로 직접 확인해야 한다.

## 이미지와 도구 호출

이미지는 메시지 부분(part)으로 보내고 입력 토큰으로 계산된다.
도구는 AI SDK의 `tool`과 Zod 스키마로 정의한다.

```typescript
import { generateText, tool } from 'ai';
import { z } from 'zod';
import 'dotenv/config';

const result = await generateText({
  model: 'minimax/minimax-m3.1-flash',
  prompt: 'What is the weather in San Francisco?',
  tools: {
    getWeather: tool({
      description: 'Get the current weather for a location',
      inputSchema: z.object({ location: z.string() }),
      execute: async ({ location }) => ({ location, temperatureC: 18 }),
    }),
  },
});
console.log(result.text);
```

## 함정

- 무료로 표시된 가격은 페이지 시점의 값이다.
  무료 기간의 조건이나 제한(속도, 크레딧)은 페이지 텍스트에 없다.
  fallingbananna는 모델 발표가 임시 가격과 토큰이 늘어나는 정도,
  실제 작업당 비용을 자주 빼놓는다고 지적했다.[^fallingbananna]
  운영 비용 계획에 넣기 전에 가격 항목을 다시 확인한다.
- 벤치마크 점수만 믿고 정하면 안 된다.
  이 모델은 “Space Bunny”라는 이름의 익명 모델로 먼저 쓰였는데,
  DCKing과 walrus01은 그때의 사용 후기가 발표된 점수만큼 좋지 않았다고 적었다.[^dcking][^walrus01]
  penagwin은 Space Bunny가 초기 체크포인트였으므로 이후 좋아졌을 수 있다고 덧붙였다.[^penagwin-checkpoint]
  어느 쪽이 맞는지는 확인하지 못했으므로 자신의 작업 묶음으로 재야 한다.
- 추론 토큰이 최대 출력에 들어가므로 짧은 상한에서는 답이 잘릴 수 있다.
- 추론 설정을 `providerOptions`와 최상위 `reasoning` 양쪽에 넣으면 앞의 것만 적용된다.
- 이미지는 입력 토큰으로 계산되므로 긴 컨텍스트에서 이미지를 많이 보내면 한도를 먼저 쓴다.
- 지연과 처리량은 제공자와 시점에 따라 변한다.
  페이지의 1.4초와 초당 52 토큰을 서비스 수준 목표로 쓰면 안 된다.
- `reasoning` 최상위 인자는 AI SDK 7 이상에서만 쓸 수 있다.
  낮은 버전에서는 이 인자에 기댈 수 없다.

## 확인하기

키가 있다면 아래 스크립트로 추론 강도별 출력 토큰 수와 응답 시간을 잴 수 있다.
이 스크립트도 이 문서를 쓰는 동안 실행하지 못했으므로
`usage` 필드 이름은 사용 중인 AI SDK 버전의 문서로 확인해야 한다.

```typescript
import { generateText } from 'ai';
import 'dotenv/config';

const levels = ['low', 'medium', 'high'] as const;

for (const reasoning of levels) {
  const start = Date.now();
  const result = await generateText({
    model: 'minimax/minimax-m3.1-flash',
    prompt: 'Explain the Monty Hall problem step by step.',
    reasoning,
  });
  console.log(reasoning, `${Date.now() - start}ms`, result.usage);
}
```

## 체크리스트

- 호출 코드의 모델 ID가 `creator/model` 형식(`minimax/minimax-m3.1-flash`)인가.
- `AI_GATEWAY_API_KEY`가 저장소에 들어가지 않고 환경 변수로만 전달되는가.
- `maxOutputTokens`가 추론 토큰을 포함해도 충분한가.
- 추론 설정을 한 곳에서만 지정했는가.
- 작업별 추론 강도를 정확도와 비용을 재서 정했는가.
- 데이터 위치 요구가 있다면 `order`가 아니라 `only`를 썼는가.
- 무료 가격의 조건을 사용 시점에 다시 확인했는가.

## 기억할 원칙

### 중개 서비스의 페이지는 모델의 평가가 아니라 호출 안내다

이 페이지에서 알 수 있는 것은 모델 ID, 한도, 호출 방법, 라우팅 규칙이다.
모델이 얼마나 정확한지나 어떤 일에 맞는지는 알 수 없다.
채택하기 전에는 자신의 작업 묶음으로 정확도와 비용, 지연을 직접 재야 하고,
페이지의 수치는 그 측정을 시작할 기준선으로만 쓴다. thefourthchime은 이 모델이
Pac-Man 과제를 푸는 데 30분이 걸렸다고 적었는데,
지연과 처리량이 수치로 볼 때보다 작업 완료 시간에서
더 크게 드러날 수 있다는 사례다.[^thefourthchime]

---

[^terhechte]: <https://news.ycombinator.com/item?id=50155686>

[^penagwin]: <https://news.ycombinator.com/item?id=50155897>

[^minimaxir]: <https://news.ycombinator.com/item?id=50156178>

[^fallingbananna]: <https://news.ycombinator.com/item?id=50156889>

[^dcking]: <https://news.ycombinator.com/item?id=50157109>

[^walrus01]: <https://news.ycombinator.com/item?id=50156022>

[^penagwin-checkpoint]: <https://news.ycombinator.com/item?id=50156234>

[^simonw]: <https://news.ycombinator.com/item?id=50157424>

[^thefourthchime]: <https://news.ycombinator.com/item?id=50157772>
