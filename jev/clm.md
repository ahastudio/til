# CLM: 문장을 생성하지 않고 상태와 행동의 임베딩을 맞춰 다음 행동을 고르는 대조 언어 모델

<https://github.com/Contrastive-LM/CLM>

HN 토론: <https://news.ycombinator.com/item?id=49826221> (170점, 55개 댓글)

GN 토론: <https://news.hada.io/topic?id=34240>

## 소개

Contrastive Language Models(CLM)는 상태(state)와 행동(action)을 잇는 대조 학습(contrastive learning) 목표로 학습한 System One 모델이다.
저장소는 CLM-8B를 TypeSafe 호환 API 뒤에서 서빙하는 추론 패키지, 웹 플레이그라운드, 미세 조정 스크립트, T-Rex 예제를 담고 있다.
저자는 Jacky Kwok, Hangoo Kang, Tarun Suresh, Jon Saad-Falcon, Marco Pavone, Christopher Ré, Azalia Mirhoseini이고, 코드와 CLM-8B 가중치는 모두 Apache 2.0으로 공개됐다.
저장소는 2026년 9월 23일에 만들어졌고, 이틀 만에 별 1,200개를 넘겼다.

README가 내세우는 숫자는 세 가지다.
CLM-8B는 Nemotron Q&A 쌍 6천만 개로 사전 학습하고, 합성 하드 네거티브(hard negative) 3천만 개로 중간 학습하고, 에이전트 궤적 100만 개로 사후 학습했다.
컴퓨터 사용, 게임, 도구 호출 과제에서 Jev와 비슷한 성능을 내면서 지연 시간은 최대 9배 낮다고 한다.
가벼운 미세 조정을 거쳐 에이전트형 코딩 벤치마크의 검증자(verifier)로 쓰면 Terminal-Bench 2.1에서 87.6%, DeepSWE에서 81.6%로 새 최고 성적을 낸다고 주장한다.

## 동작 방식

CLM은 상태 인코더와 행동 인코더를 InfoNCE 목표로 학습한다.
각 상태를 실제로 취한 행동 쪽으로 끌어당기고 다른 모든 행동에서는 밀어내도록 학습하면, 두 인코더가 곧바로 제로샷 행동 분류기가 된다.
배포할 때는 현재 상태와 후보 행동 집합을 받아, 각 행동의 임베딩이 상태 임베딩과 얼마나 잘 맞는지로 점수를 매기고 가장 높은 행동을 고른다.

각 인코더는 얼린(frozen) LLM 백본 위에 학습 가능한 2천만 파라미터 투영 헤드를 얹은 구조다.
참조 헤드는 Qwen3-8B 백본과 마지막 토큰 풀링을 쓰며, 파일 크기는 75MB다.
그래서 추론은 새 텍스트마다 임베딩 한 번, 캐시된 후보마다 내적 한 번으로 끝난다.

```text
browser ──► clm-serve  (CPU, :8700)   GET / (playground)
client  ──►                          POST /v1/systemone · GET /v1/models · GET /health
               │       state head + action head (20M params, hot-reloaded), embedding cache
               ▼
          vLLM Qwen3-8B pooling server (GPU, :8090)   /v1/embeddings
```

상태와 행동을 따로 인코딩한다는 점이 속도의 핵심이다.
Super Mario처럼 상태는 계속 바뀌지만 행동 집합은 고정된 환경에서는 매 단계 상태 임베딩만 다시 계산하고 행동 임베딩은 재사용한다.
`clm-serve`는 vLLM이 KV 캐시를 잡듯 시작할 때 장치 메모리의 일부(기본 2%)를 벡터 캐시로 예약하고, 이 크기는 늘어나지 않아 오래 도는 서버가 메모리 부족으로 죽지 않게 한다.
RTX 4090에서 서버 측 p50은 매번 새 상태일 때 약 28ms이고, 이미 본 상태를 다시 물을 때는 0.6~0.7ms로, 상태를 반복하는 루프는 약 2.8배 빨라진다.

학습은 세 단계로 점점 어려워진다.
사전 학습은 약 6천만 개의 Nemotron DQA 질문-답 쌍으로 넓은 의미 표현을 배우고, 중간 학습은 Gemini 2.5 Flash-Lite로 만든 “그럴듯하지만 틀린 답” 3천만 개로 미세한 구분을 익힌다.
사후 학습은 Agent Data Protocol 데이터셋과 터미널 궤적에서 뽑은 약 100만 개의 에이전트 궤적을 쓰되, 그중 40%를 Nemotron DQA 재생(replay)으로 채운다.
재생을 섞으면 하드 네거티브 top-1 정확도가 69%에서 68.5%로만 내려가지만, 에이전트 데이터만 쓰면 56.2%로 떨어진다.

README는 처음부터 하드 네거티브로 학습하지 않은 이유도 실험으로 밝힌다.
하드 네거티브 10개씩을 붙인 약 10만 개 질문에서, 사전 학습만으로 52.1%, 짧은 중간 학습을 더하면 69.2%에 이른다.
처음부터 하드 네거티브로 학습하면 빠르게 오르다가 62.4%에서 과적합으로 꺾여, 같은 예산에서 두 단계 방식이 7점 앞선다.
테스트 InfoNCE 손실은 연산량, 데이터 크기, 헤드 크기, 인코더 크기에 대해 거듭제곱 법칙을 따르고, 최적 헤드 크기는 파라미터당 약 310 토큰에서 데이터에 거의 정비례한다고 한다.

## 사용법

인코더와 CLM API를 차례로 띄운다.

```bash
pip install contrastive-lm

# 1. 인코더: Qwen3-8B 임베딩을 vLLM 풀링 서버로 띄운다
vllm serve Qwen/Qwen3-8B --served-model-name qwen3-8b --runner pooling --max-model-len 2048 --port 8090 &

# 2. CLM API: 첫 실행 때 75MB 참조 헤드를 내려받는다
clm-serve
```

2048 토큰보다 긴 상태는 잘리므로, 더 긴 상태가 필요하면 `vllm serve`의 `--max-model-len`과 `clm-serve --max-tokens`를 함께 올려야 한다.

질문은 세 가지 타입으로 한다.
`Noul`은 참일 확률, `Choice`는 선택지별 확률, `Score`는 순서가 있는 등급의 기댓값을 돌려준다.

```python
from clm import CLMClient, Choice, Noul, Score

client = CLMClient()
r = client.system_one(
    state="Customer: my invoice was charged twice and nobody answers the phone!",
    questions={
        "urgency": Noul(instructions="Is this urgent?"),
        "department": Choice(instructions="Which team should handle this?",
                             criteria={"billing": "Charges, invoices, refunds",
                                       "technical": "Bugs and outages"}),
        "frustration": Score(instructions="How frustrated is the customer?",
                             criteria=["Calm", "Frustrated", "Very angry"]),
    },
)
print(r.answers["department"].probabilities)  # {'billing': 0.93878, 'technical': 0.06122}
```

TypeSafe용으로 쓴 요청은 `client.system_one(state, questions)`로 그대로 다시 보낼 수 있다.
자유 형식 후보를 순위 매길 때는 `Engine.rank`나 `POST /v1/rank`를 쓴다.
`clm-serve`는 `/`에서 상태와 질문을 넣고 답의 분포를 보는 플레이그라운드도 제공하며, 모든 요청을 JSON, `curl`, Python 형식으로 보여 준다.

## 분석

### Jev의 인터페이스를 가져오고, 안쪽은 CLIP의 방식으로 바꿨다

CLM은 Jev를 정면으로 겨냥한다.
README는 Jev를 비교 대상으로 삼고, API는 TypeSafe와 호환되며, 질문 타입의 이름까지 맞췄다.
그러나 안쪽의 원리는 다르다.

Hacker News에서 andy12_는 이것을 한마디로 “행동을 위한 CLIP”이라고 불렀다.[^andy12_]
CLIP이 이미지와 캡션을 한 임베딩 공간에 놓았듯, CLM은 상태와 행동을 한 공간에 놓는다.
amluto는 이 구조를 얼린 LLM 위에 작은 모델을 얹어, 입력을 처리한 뒤의 은닉 상태에서 답의 “확률”을 뽑는 방식으로 이해했다.[^amluto]
원래 LLM이라면 자기회귀 방식으로 여러 토큰을 생성해 답을 냈을 것이다.

amluto는 이 분리 자체에 의미를 뒀다.
프리필(prefill)은 자기회귀 출력보다 빠르고 싸며, 모델이 출력 토큰 하나마다 한 번씩 순전파를 돌아야 한다는 제약은 원래 그다지 합리적이지 않았다는 것이다.
입력과 출력이 같은 토큰 공간을 쓰는 주된 이유는 사전 학습 방식이 그렇기 때문일 뿐이라고 그는 적었다.

### 속도는 모델이 아니라 캐시에서 나온다

README의 캐시 표는 이 모델의 속도가 어디서 오는지를 정직하게 보여 준다.
매번 새 상태를 물으면 약 28ms가 들고, 캐시가 이 숫자를 거의 줄이지 못한다.
다시 본 상태를 물을 때만 1ms 아래로 떨어진다.

Hacker News의 사용자 실험도 같은 이야기를 한다.
sdan은 H100에서 돌려 보니 190ms가 나와 Jev의 170ms보다 오히려 느렸다고 적었고,[^sdan] kevmo314는 캐시가 낮은 지연 시간 수치에 크게 기여하는 것 같으며, 캐시 없이 요청 하나만 보내면 꽤 느려서 sdan의 관찰과 비슷하다고 답했다.[^kevmo314]
결국 “최대 9배 빠르다”는 WikiRacing처럼 후보 행동이 많거나 T-Rex처럼 행동이 상태 사이에서 재사용되는 환경의 숫자이고, README도 속도 향상이 그런 경우에 가장 크다고 밝힌다.

### 실패한 실험까지 적은 학습 레시피가 이 저장소의 가장 큰 기여다

Hacker News에서 mugul은 학습 과정에 대한 설명이 흥미롭다며, 왜 이 단계를 밟았는지, 무엇을 시도했고 무엇이 안 됐는지를 실험으로 정당화한 덕분에 덜 흑마술처럼 느껴진다고 적었다.[^mugul]
처음부터 하드 네거티브로 학습하면 62.4%에서 과적합으로 꺾인다는 결과, 재생 없이 에이전트 데이터만 쓰면 일반 능력이 69%에서 56.2%로 무너진다는 결과가 그런 예다.

peter_d_sherman은 블로그에서 Nemotron DQA 사전 학습 한 번이 RTX 4090 한 장에서 약 한 시간 걸린다는 대목을 짚었다.[^peter_d_sherman]
그는 소비자용 하드웨어에서 로컬 AI 학습과 추론의 마지막 한 사이클까지 짜내고 싶은 사람이라면 이 모델을 공부할 가치가 있다고 봤다.
얼린 백본 위에 2천만 파라미터 헤드만 학습하는 구조이기에 가능한 비용이다.

## 비평

### 에이전트 코딩 “최고 성적”은 CLM의 점수가 아니라 선택의 점수다

README의 가장 눈에 띄는 숫자는 DeepSWE 81.6%와 Terminal-Bench 2.1 87.6%다.
Hacker News에서 vessenes는 이 숫자를 믿지 않는다며, Astra x-high의 DeepSWE pass@1이 74% 안팎이라고 반박했다.[^vessenes]
kuukyo는 이들이 pass@1을 보고하지 않았고, Opus와 Fable에서 여러 해답을 뽑은 뒤 CLM이 제출할 하나를 고르기 때문에 80%를 넘는다고 설명했다.[^kuukyo]

vatsachak는 더 날카롭게, 이 모델은 DeepSWE에서 80% 넘게 득점하는 것이 아니라 매 단계 Opus 5의 가장 좋은 아이디어를 고를 뿐이라며 성능을 5% 정도 올리는 것이라고 지적했다.[^vatsachak]
aoeusnth1은 GitHub 첫 페이지가 이 점을 분명히 밝혀 훨씬 덜 오해를 부르는데, 왜 마케팅 페이지는 이 세부를 흐리는지 모르겠다며 그것이 저자들의 사고방식을 드러낸다고 답했다.[^aoeusnth1]

README를 다시 읽으면 실제로 그렇다.
평가는 DeepSWE 38개, Terminal-Bench 2.1 30개의 보류(held-out) 과제에서 했고, 81.6%는 38개 중 31개다.
표본이 이 정도로 작으면 한두 과제의 차이가 몇 %포인트를 움직이고, “새 최고 성적”이라는 표현이 담기에는 신뢰 구간이 넓다.

### 제로샷 비교는 이 구조가 가장 잘하는 과제만 골랐다

Hacker News에서 0x4139는 “Jev와 비슷하다”는 결과가 Mario, T-Rex, WikiRacing, 곧 후보가 많은 의미적 행동 매칭이라고 짚었다.[^0x4139]
그는 이것이 독립적으로 인코딩한 벡터 사이의 코사인이 옳은 귀납적 편향이 되는 영역이라며, 제로샷 평가가 날짜 계산, 부정의 연쇄, 정책 임계값 같은 타입 결정의 부하는 다루지 않는다고 적었다.

이 지적은 구조의 본질을 건드린다.
상태와 행동을 따로 인코딩하면, 두 텍스트 사이의 세밀한 논리적 상호작용은 두 벡터의 내적으로만 표현돼야 한다.
“환불 기한이 30일이고 오늘이 구매 후 31일째다”라는 상태에서 “환불 가능”과 “환불 불가”를 가르는 일은, 의미가 가까운 행동을 고르는 일과 종류가 다르다.
README의 고객 문의 예시에서 긴급도의 참일 확률이 0.41로 나오는 것도, 이 모델이 무엇을 잘하고 무엇에 약한지를 보여 주는 작은 신호일 수 있다.

### 지연 시간 비교의 두 쪽이 같은 조건이 아니다

Hacker News에서 eadwu는 지연 시간이 정말 중요하냐며, 로컬 GPU를 네트워크를 거치는 API와 비교하는 것 아니냐고 물었다.[^eadwu]
brookman64k는 TypeSafe의 Jev 플레이그라운드가 모델 지연과 네트워크 지연을 따로 보여 주며, 자신의 테스트에서는 모델 지연이 100~200ms였다고 답했다.[^brookman64k]
mugul도 Jev가 원격 서버에서 도니 지연 시간 논거는 큰 의미가 없고, 최근 나온 여러 오픈 Jev류 모델과 비교하는 편이 훨씬 흥미로울 것이라고 적었다.[^mugul]

README는 에이전트 벤치마크의 지연 시간을 H100에서 쟀다고 밝히지만, Jev 쪽의 측정 조건은 같은 수준으로 적혀 있지 않다.
로컬에서 캐시를 쓰는 모델과 네트워크 너머의 API를 비교한 “9배”는, 모델 구조의 차이와 배포 방식의 차이를 한 숫자에 섞는다.
공정한 비교라면 같은 하드웨어에서 도는 오픈 Jev류 구현과 나란히 세웠어야 한다.

## 인사이트

### System One이라는 이름은 이제 한 회사의 브랜드가 아니라 범주가 됐다

TypeSafe가 Jev를 내놓으며 쓴 “System One 모델”이라는 말을, CLM은 부제에 그대로 가져왔다.
Hacker News에서 fxwin은 System One이 단지 “빠르다”는 뜻의 새 유행어로 남지 않기를 바란다고 적었고,[^fxwin] khalic은 Kahneman조차 S1과 S2가 뇌의 작동을 이해하기 위한 틀일 뿐 독립된 시스템은 없다고 했다며 이 이름을 그만 쓰라고 했다.[^khalic]
반면 robrenaud는 뇌와의 연관을 빼면 꽤 적절한 설명이라며, 토큰 공간에서 여러 번 순전파로 생각하는 모델과 달리 이 모델들은 입력을 처리한 뒤 빠르게 결정을 내린다고 답했다.[^robrenaud]

이름을 둘러싼 논쟁과 별개로, 경쟁자가 같은 이름을 쓰기 시작했다는 사실이 더 중요하다.
한 회사의 제품 이름이던 말이 오픈소스 연구의 부제가 되면, 그것은 범주가 된다.
Jev를 둘러싼 이 저장소의 문서들에는 Jevlike, Jev Ultrafast, 25줄짜리 패러디가 이미 있고, CLM은 그 목록에 학계 연구진이 만든 다른 구조를 더한다.

### 생성 모델의 점수를 올리는 가장 싼 길은 더 나은 선택자다

CLM이 에이전트 코딩에서 보여 준 것은 엄밀히 말하면 선택 능력이다.
Opus 5나 Fable 5가 여러 해답을 만들고, CLM은 그중 하나를 고른다.
vatsachak의 말처럼 이것이 성능을 몇 %포인트 올리는 정도라 해도,[^vatsachak] 그 몇 포인트를 수백 밀리초와 작은 헤드 하나로 얻는다는 점은 가볍지 않다.

이 구조는 생성과 검증의 비용 비대칭을 이용한다.
좋은 해답을 만드는 일은 비싸지만, 여러 해답 중 좋은 것을 알아보는 일은 훨씬 쌀 수 있다.
best-of-N 샘플링과 빠른 검증자의 조합은, 더 큰 생성 모델을 기다리지 않고도 지금의 모델에서 더 많은 성능을 뽑는 길이 된다.

다만 amluto가 지적했듯, 스팸 판별처럼 정답이 있는 분류와 에이전트의 다음 한 수를 고르는 전략은 다르다.[^amluto]
정답이 없는 문제에서 “확률”은 보정된 확신이 아니라 학습 분포와의 유사도일 수 있고, noduerme는 이런 모델들이 과적합으로 겉보기만 확신에 찬 확률을 낸다고 의심했다.[^noduerme]
빠른 선택자를 에이전트 루프에 넣을수록, 그 확률이 무엇을 뜻하는지 검증할 책임도 함께 커진다.

### 상태와 행동을 분리하면 에이전트 설계가 “행동 목록”을 중심으로 바뀐다

CLM의 캐시는 행동 집합이 고정되거나 재사용될 때 가장 빛난다.
이것은 에이전트를 설계하는 쪽에 한 가지 압력을 준다.
자유 형식으로 다음 행동을 생성하게 하는 대신, 가능한 행동을 미리 목록으로 정의하고 그 안에서 고르게 만들수록 빠르고 싸진다.

이 방향은 이 저장소의 Jev Ultrafast 문서가 다룬 브라우저 에이전트, 곧 행동 공간을 매번 새로 만들어 한 번의 요청으로 고르는 설계와 통한다.
행동이 목록이 되면 에이전트는 예측 가능해지고, 허용되지 않은 행동은 애초에 후보에 오르지 않는다.
대신 목록에 없는 새로운 행동, 곧 설계자가 예상하지 못한 해법은 고를 수 없게 된다.
빠른 선택과 열린 생성 사이의 이 긴장은, 모델의 속도가 아니라 에이전트가 어떤 문제를 풀어야 하느냐로 결정될 것이다.

---

[^andy12_]: <https://news.ycombinator.com/item?id=49828036>

[^amluto]: <https://news.ycombinator.com/item?id=49828101>

[^sdan]: <https://news.ycombinator.com/item?id=49827766>

[^kevmo314]: <https://news.ycombinator.com/item?id=49831986>

[^mugul]: <https://news.ycombinator.com/item?id=49827073>

[^peter_d_sherman]: <https://news.ycombinator.com/item?id=49829113>

[^vessenes]: <https://news.ycombinator.com/item?id=49830745>

[^kuukyo]: <https://news.ycombinator.com/item?id=49831049>

[^vatsachak]: <https://news.ycombinator.com/item?id=49833632>

[^aoeusnth1]: <https://news.ycombinator.com/item?id=49834242>

[^0x4139]: <https://news.ycombinator.com/item?id=49827598>

[^eadwu]: <https://news.ycombinator.com/item?id=49826740>

[^brookman64k]: <https://news.ycombinator.com/item?id=49827283>

[^fxwin]: <https://news.ycombinator.com/item?id=49827631>

[^khalic]: <https://news.ycombinator.com/item?id=49829997>

[^robrenaud]: <https://news.ycombinator.com/item?id=49833404>

[^noduerme]: <https://news.ycombinator.com/item?id=49828394>
