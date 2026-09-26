# Cloudflare Workers AI: Cloudflare 네트워크의 서버리스 GPU에서 공개 모델을 부르는 추론 서비스

<https://developers.cloudflare.com/workers-ai/>

## 소개

Workers AI는 Cloudflare 네트워크의 서버리스 GPU에서 머신러닝 모델을 돌리는 서비스다.
공식 문서 첫 페이지는 확장, 유지보수, 쓰지 않는 인프라 비용을 걱정하지 않고 AI 모델을 서버리스로 돌릴 수 있으며, Workers와 Pages의 코드에서, 또는 Cloudflare API로 어디서든 부를 수 있다고 소개한다.
Workers Free와 Workers Paid 플랜 모두에서 쓸 수 있고, 정식 출시(GA) 상태다.

문서가 내세우는 것은 세 가지다.
모델 카탈로그의 50개가 넘는 공개 모델, 쓴 만큼 내는 서버리스 가격, 그리고 AI Gateway, Vectorize, Workers, R2, D1, Durable Objects, KV를 포함한 개발자 플랫폼과의 통합이다.
비공개 맞춤 모델이나 더 높은 한도가 필요하면 별도 양식으로 요청하라고 안내한다.
문서 전체는 `llms.txt`로 목록이 제공되고, 모든 페이지를 Markdown으로 받을 수 있다.

## 주요 기능

문서의 기능 절은 추론 호출 자체를 넘어 운영에 필요한 여러 장치를 다룬다.

| 기능                   | 하는 일                                                                     |
| ---------------------- | --------------------------------------------------------------------------- |
| 모델 카탈로그          | 텍스트 생성, 임베딩, 이미지 생성, 음성 인식과 합성, 번역, 분류 모델         |
| OpenAI 호환 엔드포인트 | `/v1/chat/completions`와 `/v1/embeddings`, GPT-OSS 모델에만 `/v1/responses` |
| 함수 호출              | 표준 방식의 도구 정의와, 추론과 함께 함수 코드를 실행하는 내장 방식         |
| JSON 모드              | `response_format`이나 JSON 스키마로 올바른 JSON 출력을 강제                 |
| 프롬프트 캐싱          | 같은 접두부의 입력 텐서를 재사용해 첫 토큰 시간과 비용을 줄임               |
| 비동기 배치 API        | 요청 묶음을 큐에 넣고 나중에 결과를 가져옴                                  |
| LoRA 미세 조정         | LoRA 어댑터로 미세 조정된 추론, 오픈 베타 동안 무료                         |
| Markdown 변환          | 여러 형식의 문서를 `toMarkdown`으로 Markdown으로 바꿈                       |
| 혼잡 시 거절           | 용량이 없으면 대기하지 않고 요청을 실패시킴                                 |

## 호출하기

### 세 가지 진입점

가장 기본적인 방법은 Worker 안의 AI 바인딩이다.
`wrangler.toml`에 바인딩을 선언하면 Worker 코드에서 `env.AI.run()`으로 모델을 부른다.

```toml
# wrangler.toml
[ai]
binding = "AI"
```

```javascript
export default {
  async fetch(request, env) {
    const answer = await env.AI.run("@cf/meta/llama-3.1-8b-instruct-fp8", {
      messages: [{ role: "user", content: "What is a capacity queue?" }],
      max_tokens: 256,
    });
    return Response.json(answer);
  },
};
```

Worker 밖에서는 REST API `/client/v4/accounts/{account_id}/ai/run/{model}`을 쓰거나, OpenAI SDK의 `baseURL`을 `https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1`로 바꿔 쓴다.
OpenAI 호환 엔드포인트 덕분에 기존 OpenAI SDK 코드를 모델 이름과 기본 URL만 바꿔 옮길 수 있다.

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.CLOUDFLARE_API_TOKEN,
  baseURL: `https://api.cloudflare.com/client/v4/accounts/${process.env.CLOUDFLARE_ACCOUNT_ID}/ai/v1`,
});

const completion = await openai.chat.completions.create({
  model: "@cf/meta/llama-3.1-8b-instruct-fp8",
  messages: [{ role: "user", content: "Make some robot noises" }],
});
console.log(completion.choices[0].message.content);
```

### 프롬프트 캐싱과 세션 고정

일부 모델은 접두부 캐싱이 기본으로 켜져 있다.
LLM은 입력을 처리하는 prefill 단계와 출력을 만드는 단계를 거치는데, 접두부 캐싱은 prefill에서 계산한 입력 텐서를 저장해 두었다가, 같은 접두부를 가진 다음 요청에서 그 부분의 prefill을 건너뛴다.
코딩 에이전트처럼 매 요청에 이전 대화와 도구 정의를 다시 보내는 작업에서 효과가 크다.
캐시된 입력 토큰은 일반 입력보다 할인된 단가로 과금된다.

캐시는 요청이 캐시를 가진 같은 모델 인스턴스로 갈 때만 맞는다.
그래서 세션이나 에이전트마다 고유한 값을 `x-session-affinity` 헤더로 보내, 같은 식별자의 요청이 같은 인스턴스로 가도록 해야 한다.

### 배치와 혼잡 시 거절

사람이 기다리지 않는 대량 작업, 곧 요약이나 임베딩 일괄 처리에는 비동기 배치 API를 쓴다.
요청 묶음을 보내면 곧바로 `queued` 상태와 `request_id`를 돌려주고, 나중에 그 ID로 결과를 가져온다.
문서는 배치 API가 Cloudflare에 당장 용량이 없을 때 오류를 내는 대신 요청이 결국 처리되도록 보장한다고 설명하며, 전체 페이로드는 10MB 미만이어야 한다.

반대로 동기 요청이 용량 대기열에서 기다리는 것을 원하지 않는다면 `rejectIfBusy`를 켠다.
REST API에서는 요청 본문의 `options` 객체에, 바인딩에서는 `env.AI.run()`의 세 번째 인자에 넣는다.

```javascript
const response = await env.AI.run(
  "@cf/google/gemma-4-26b-a4b-it",
  { messages: [{ role: "user", content: "Explain what a capacity queue is." }] },
  { rejectIfBusy: true }, // 용량이 없으면 기다리지 않고 실패
);
```

## 가격과 한도

과금 단위는 뉴런이고, 1,000 뉴런당 0.011달러이며, 두 플랜 모두 하루 10,000 뉴런을 무료로 쓴다.
가격표는 모델마다 토큰 단위 가격과 뉴런 단위 가격을 함께 보여 주며, Kimi, GLM, DeepSeek V4 같은 일부 최신 대형 모델은 Workers Paid나 선불 AI Gateway 크레딧이 있어야 쓸 수 있다.
하루 10,000 뉴런으로 모델별로 몇 번을 부를 수 있는지는 [[workers-ai-free-tier]]에서 공식 단가로 계산했다.

요청 속도는 작업 종류별로 제한된다.
텍스트 생성은 분당 300회이며, 유료 결제가 필요한 모델은 표준 결제로 분당 20회, 선불 AI Gateway 크레딧으로 분당 50회다.
임베딩과 이미지 분류는 분당 3,000회, 음성 인식과 이미지 생성과 번역은 분당 720회다.

## 데이터 사용

데이터 사용 문서는 몇 가지를 분명히 한다.
Cloudflare는 Workers AI의 모델을 만들거나 학습시키지 않으며, 모델은 제3자 서비스로서 각 모델의 라이선스 조건이 사용자와 모델 제공자 사이에 적용될 수 있다.
입력, 출력, 임베딩, 학습 데이터는 고객 콘텐츠이고, Cloudflare는 이것을 다른 고객에게 보여 주지 않으며, 명시적 동의 없이 모델 학습이나 서비스 개선에 쓰지 않는다.
고객 콘텐츠는 사용자가 R2, KV, Durable Objects, Vectorize 같은 저장소를 함께 쓸 때만 저장된다.

## 트레이드오프

### 카탈로그에 묶인 모델 선택

Workers AI의 장점은 GPU를 운영하지 않고 모델을 부를 수 있다는 것이지만, 그 대가로 쓸 수 있는 모델은 Cloudflare 카탈로그로 정해진다.
LoRA 어댑터로 일부 기본 모델을 맞출 수는 있지만, 전체 가중치를 올리거나 카탈로그에 없는 모델을 돌리려면 맞춤 요구 양식으로 따로 요청해야 한다.
카탈로그는 바뀌므로, 특정 모델 변형에 의존하는 코드는 그 모델이 카탈로그에서 빠지거나 단가가 바뀔 때를 대비해야 한다.

### 서버리스의 편리함과 용량의 불확실성

서버리스는 쓰지 않을 때 돈을 내지 않게 해 주지만, 필요할 때 용량이 있다는 보장도 약해진다.
문서가 용량 대기열, `rejectIfBusy`, “용량이 부족하면 오류를 내는 대신” 처리를 보장하는 배치 API를 따로 설명한다는 것 자체가, 동기 요청이 용량 부족에 부딪힐 수 있다는 뜻이다.
응답 시간이 중요한 요청은 `rejectIfBusy`로 빨리 실패시키고 다른 공급자로 넘기는 폴백을 두며, 기다려도 되는 작업은 배치 API로 보내는 식으로 요청의 성격에 따라 경로를 나눠야 한다.

### 캐싱 효과와 라우팅 고정의 긴장

`x-session-affinity`는 캐시 적중률을 올리지만, 같은 세션의 요청을 같은 인스턴스에 고정한다.
한 세션이 아주 많은 요청을 보내면 그 부하가 한 인스턴스에 몰리고, 그 인스턴스가 바쁘면 캐시의 이득보다 대기 시간이 커질 수 있다.
세션 식별자의 단위를 사용자 전체가 아니라 대화나 에이전트 실행 하나로 잡는 것이 무난하다.

## 함정

- 가격표에 있다고 모델 카탈로그에 페이지가 있는 것은 아니다. 예컨대 `@cf/meta/llama-3.1-8b-instruct`는 가격표와 OpenAI 호환 문서의 예제에는 나오지만, 9월 26일 기준 모델 카탈로그에는 페이지가 없다.
- 같은 모델도 정밀도와 양자화 변형에 따라 단가가 세 배 넘게 다르다. 변형 이름까지 확인해야 한다.
- 무료 할당은 00:00 UTC에 초기화되며, Workers Free에서는 한도를 넘기면 요청이 실패한다.
- 텍스트, 이미지, 음성, 임베딩이 모두 같은 뉴런 예산을 나눠 쓴다.
- 배치 API의 페이로드는 10MB 미만이어야 한다.
- 모델 라이선스는 Cloudflare가 아니라 모델 제공자와의 관계에서 적용될 수 있다.

## 체크리스트

- 쓸 모델이 현재 모델 카탈로그에 있고, 그 변형의 단가를 가격표에서 확인했는가?
- 유료 결제가 필요한 모델을 쓴다면 Workers Paid나 선불 AI Gateway 크레딧을 설정했는가?
- 반복되는 긴 접두부를 가진 요청에 `x-session-affinity`를 보내는가?
- 사람이 기다리지 않는 대량 작업을 배치 API로 보내는가?
- 지연 시간이 중요한 요청에 `rejectIfBusy`와 폴백 경로를 두었는가?
- 출력 길이에 `max_tokens` 상한을 두었는가?
- 쓰는 모델의 라이선스 조건을 확인했는가?

## 기억할 원칙

### 서버리스 추론은 요청의 성격에 따라 경로를 나눌 때 가장 싸고 안정적이다

Workers AI의 기능 목록은 하나의 원칙으로 모인다.
사람이 기다리는 요청은 동기로 보내되 캐시를 살리고 혼잡하면 빨리 실패시키며, 사람이 기다리지 않는 작업은 배치로 보내 용량이 날 때 처리한다.
같은 모델을 부르더라도 요청의 성격에 맞는 경로를 고르는 것이, 서버리스 GPU의 비용과 용량 제약을 동시에 다루는 방법이다.

[[ai-platform]]이 다룬 Cloudflare의 추론 계층 구상도 같은 방향을 가리킨다.
여러 모델과 여러 공급자를 AI Gateway 뒤에 두고, 요청마다 모델과 경로를 고르게 하는 것이다.
Workers AI는 그 계층에서 Cloudflare가 직접 GPU를 돌리는 한 공급자이고, 다른 공급자와 섞어 쓸 때 가장 쓸모가 커진다.
