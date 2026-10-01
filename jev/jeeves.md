# Jeeves: 결정하기 전에 생각하게 만든 9B Jev 계열 모델과 그 대가

<https://github.com/PostHog/jeeves>

HN 토론: <https://news.ycombinator.com/item?id=49891290> (241점, 94개 댓글)

GN 토론: <https://news.hada.io/topic?id=34496>

## 소개

Jeeves는 PostHog 저장소에 공개된 추론형 Jev 스타일 분류기다.
Qwen3.5-9B에 LoRA와 포인터 헤드를 붙이고, SFT와 CISPO로 학습해 결정 전에 추론 사슬을 굴리게 했다.
추론을 빠르게 하려고 블록 4 확산 드래프터를 함께 제공한다.
저장소는 2026년 9월 29일에 만들어졌고, MIT 라이선스이며, 2026년 10월 1일 기준 GitHub 별 336개, 포크 16개다.
README의 인용 항목에 적힌 저자는 Nicholas P. Waltz다.

README는 [Kev](kev.md)에서 영감을 받았다고 밝히고, 설계의 출발점으로 [Jev의 구조를 되짚은 글](architecture-unmasked.md)을 참고 문헌 첫 줄에 둔다.
문제 정의는 한 문장이다.
Jev 계열 모델은 보정된 결정 확률을 주지만 정확도가 낮아서, 많은 파이프라인이 추론 모델을 대체 경로로 둔다는 것이다.
Jeeves는 그 대체 경로를 모델 안으로 넣어, 같은 모델이 필요할 때 생각한 뒤 결정하게 한다.

README가 앞세우는 결과는 두 가지다.
학습에 쓰지 않은 테스트 데이터에서 Kev-9B 0.822, Jev 0.857에 대해 0.889를 냈고, JevBench 공개 등급에서 Jev 0.866에 대해 0.935를 냈다는 것이다.
요청 형식은 Jev와 호환되고, `sdk/`는 Jev의 Python SDK를 그대로 대체한다.

## 동작 방식

### 생각한 뒤 질문을 다시 읽고 가리킨다

질문, 상태, 선택지는 Qwen 채팅 템플릿에 다음 모양으로 들어간다.

```text
<state> …state…
<q> instructions <opt> option 1 </opt> <opt> option 2 </opt> …
<think>
```

모델이 추론 사슬을 펼친 뒤 `</think>`가 나오면, 질문과 선택지를 한 번 더 붙이고 `<decide>` 토큰을 둔다.

```text
</think>

<q> instructions <opt> option 1 </opt> <opt> option 2 </opt> …
<decide>
```

포인터 헤드는 `<decide>` 위치 은닉 상태의 query 투영과, 각 선택지 `</opt>` 위치 은닉 상태의 key 투영 사이의 스케일된 내적으로 선택지 점수를 낸다.
최종 확률은 그 점수의 softmax를 개발 세트에서 맞춘 온도로 나눈 값이다.
특수 토큰에는 Qwen 토크나이저에서 거의 쓰이지 않는 `<|fim_prefix|>`, `<|fim_middle|>`, `<|box_start|>`, `<|box_end|>`, `<|fim_suffix|>`를 빌려 쓴다.
README의 절제 실험에 따르면 이 자리에 State 같은 평범한 글자를 쓰거나, 추론 뒤에 질문을 반복하지 않으면 성능이 떨어진다.

생성된 텍스트를 파싱하지 않는다는 점은 Jev와 같다.
추론 사슬은 생성하지만, 답은 여전히 포인터 헤드가 선택지 위의 확률 분포로 낸다.

### 학습은 세 단계다

| 단계  | 내용                                                                                                                              |
| ----- | --------------------------------------------------------------------------------------------------------------------------------- |
| SFT   | 2에폭, GPU 8장에서 596스텝, LoRA r=16, 12개 공개 데이터셋과 합성 정책 데이터 1만 9,126문항, 절반에 기반 모델이 샘플링한 추론 사슬 |
| CISPO | 624스텝 일정 중 402스텝에서 멈춤, RL 문항 9,992개, 온도 1로 8번씩 롤아웃, 사고 토큰 상한 2,560                                    |
| 보정  | 개발 세트에서 온도 하나를 맞춰 체크포인트에 저장                                                                                  |

402스텝에서 멈춘 이유는 보정과 개발 점수가 그때 가장 좋고, 그 뒤로는 포화된 RL 풀에서 헤드가 지나치게 날카로워지기 때문이라고 한다.
CISPO는 MiniMax-M1 논문이 소개한 강화학습 방식이다.

### 확산 드래프터로 사슬을 빨리 뽑는다

드래프터는 고정된 모델을 확산 방식으로 본 것으로, Orthrus에서 영감을 받았다.
Orthrus는 어텐션만 있는 모델을 지원하지만, Jeeves는 마스크 토큰이 Qwen3.5의 Gated DeltaNet 층의 합성곱 이후 key와 value를 교차 어텐션하게 해서 그 층까지 지원한다.

| 방식                    | 사슬 토큰/초 |
| ----------------------- | ------------ |
| 일반 탐욕 디코딩, 1문항 | 109          |
| 블록 4, 1문항           | 176(1.6배)   |
| 블록 8, 1문항           | 193(1.76배)  |
| 블록 4, 8문항 배치      | 합계 약 960  |

여러 문항을 배치해도 싸게 유지된다는 이유로 블록 4가 기본값이다.

## 빠르게 돌려 보기

Python 3.12와 CUDA GPU가 필요하고, 추론은 48GB 이상의 Apple Silicon Mac에서도 된다.

```bash
pip install -r requirements.txt
hf download PostHog/jeeves --local-dir jeeves-weights
python -m inference.serve --model jeeves-weights \
  --drafter jeeves-weights/drafter_k4.safetensors --port 8009
```

Mac에서는 가중치가 bf16으로 21GB이고 기본 캐시(`--max-rows 8 --max-len 8192`)가 28GB를 더 쓰므로, 48GB Mac은 스왑을 시작한다.
캐시를 줄여서 띄운다.

```bash
# 48GB Mac: 캐시를 줄여 스왑을 피한다
python -m inference.serve --model jeeves-weights \
  --drafter jeeves-weights/drafter_k4.safetensors \
  --max-rows 4 --max-len 4096 --port 8009
```

`--precision fp8`을 주면 선형 층을 양자화해 가중치가 11.5GB로 줄고, M4 Pro에서 사고 속도가 초당 약 20토큰에서 약 31토큰으로 오른다.
출력은 조금 달라지지만 개발 문항에서 정확도와 NLL의 차이는 측정되지 않았다고 한다.
CUDA에서는 연산 능력 8.9 이상의 GPU에서 쓸 수 있다.

요청은 Jev 형식에 선택적인 `options`를 더한다.

```bash
curl -s localhost:8009/v1/systemone -H 'content-type: application/json' -d '{
  "state": "Shoes arrived two weeks late and in the wrong size. Also I see two charges on my card.",
  "questions": {
    "department":  {"type": "choice", "instructions": "Which team should handle this?",
                    "criteria": {"returns": "Exchanges, refunds, wrong or damaged items",
                                 "shipping": "Delivery status, delays, lost packages",
                                 "billing": "Charges, invoices, payment problems"}},
    "escalate":    {"type": "noul", "instructions": "Does this need urgent human attention?"},
    "frustration": {"type": "score", "instructions": "How frustrated is the customer?",
                    "criteria": ["Calm", "Frustrated", "Very angry"]}
  },
  "options": {"max_think": 512}}'
```

## 값 정하기

`options`는 Jev 클라이언트가 보내지 않으면 무시된다.
서버 전체 기본값은 같은 이름의 `serve` 플래그로 정한다.

| 옵션                | 기본값  | 효과                                                       |
| ------------------- | ------- | ---------------------------------------------------------- |
| `think`             | `true`  | `false`면 프롬프트만 보고 답한다(약 0.3초)                 |
| `max_think`         | 2560    | 추론 사슬을 이 토큰 수에서 자르고 답한다                   |
| `nothink_threshold` | `null`  | 생각하지 않은 답의 신뢰도가 이 값 이상이면 생각을 건너뛴다 |
| `return_reasoning`  | `false` | 질문마다 추론 텍스트를 응답에 붙인다                       |

README가 H100 한 장, `--precision fp8`로 개발 문항 325개에서 잰 값이다.

| 설정                                     | 정확도 | 평균 추론 토큰 | 중앙값 / p90 지연 |
| ---------------------------------------- | ------ | -------------- | ----------------- |
| 전체 사고                                | 0.825  | 1,138          | 3.3초 / 17.1초    |
| `max_think` 768, `nothink_threshold` 0.9 | 0.806  | 344            | 2.0초 / 5.6초     |
| 사고 없음                                | 0.775  | 0              | 약 0.3초          |

시작점은 가운데 줄이다.
전체 사고 대비 정확도 1.9점을 내주고 p90 지연을 17.1초에서 5.6초로 줄인다.
`nothink_threshold`는 쉬운 문항에서 사고를 건너뛰게 해 평균 비용을 낮추므로, 쉬운 문항이 많은 과제일수록 효과가 크다.
정할 때 볼 것은 자기 과제에서 사고 없음과 전체 사고의 정확도 차이다.
차이가 작다면 사고를 끄는 편이 Jev 계열 모델을 쓰는 원래 이유에 맞는다.

## 결과 읽기

README 표의 Kev-9B와 Jev 열은 Kev가 공개한 숫자를 가져온 것이다.

| 벤치마크                                          | Kev-9B | Jev   | Jeeves |
| ------------------------------------------------- | ------ | ----- | ------ |
| 테스트 전체                                       | 0.822  | 0.857 | 0.889  |
| 전이 전체(MMLU-Pro, 묻힌 상태)                    | 0.579  | 0.800 | 0.746  |
| JevBench 전체(공개 231문항)                       | 0.715  | 0.866 | 0.935  |
| MMLU                                              | 0.738  | 0.900 | 0.793  |
| MMLU-Pro(10지선다)                                | 0.515  | 0.840 | 0.739  |
| JevBench hard(공개 111문항)                       | 0.451  | 0.730 | 0.865  |
| 답할 수 없는 문항에 p ≥ 0.9로 답함(낮을수록 좋음) | 0.000  | 0.090 | 0.055  |
| JevBench ECE                                      |        | 0.049 | 0.037  |

JevBench의 Kev 숫자는 Kev-9B가 아니라 Kev-8B(Qwen3) 결과다.
JevBench 숫자는 봉인된 judge 등급을 뺀 공개 등급 231문항에서만 냈다.
README의 한계 항목은 JevBench 밖의 Kev와 Jev 비교가 같은 출처의 다른 문항에서 나왔다고 적는다.

지식 문항에서는 Jev에 뒤진다.
MMLU 0.793 대 0.900, MMLU-Pro 0.739 대 0.840이다.
추론이 규칙 적용이나 정책 판정에는 도움이 되지만, 모델이 모르는 지식을 만들어 주지는 않는다는 뜻이다.

## 트레이드오프

### 생각하면 Jev 계열을 쓰는 이유가 사라진다

HN에서 가장 먼저 나온 반응은 p90 17초라면 무슨 의미가 있느냐, 차라리 LLM을 쓰겠다는 것이었다[^sharih].
itzikkatz도 p90 지연 17초가 빠르고 싼 Jev급 모델이라는 취지를 무너뜨리고, MMLU에서 10점을 잃은 것도 도움이 안 된다고 했다[^itzikkatz].
hjun1052는 결정 전에 자기회귀 추론을 하면 한 번의 순전파와 값싼 보정 확률이라는 Jev 스타일의 이점 대부분을 포기하는 것 아니냐며, 요점이 타입 있는 출력과 확률 인터페이스를 유지한 채 어려운 문항의 정확도를 올리는 데 있느냐고 물었다[^hjun1052].

마지막 질문이 이 모델의 자리를 정확히 짚는다.
Jeeves는 Jev를 대체하는 모델이 아니라, Jev 계열 파이프라인에서 추론 모델로 넘기던 어려운 문항의 대체 경로를 같은 인터페이스로 흡수하는 모델이다.
그렇게 보면 비교 대상은 Jev가 아니라 추론 LLM에 구조화 출력을 거는 기존 대체 경로다.
그런데 README는 그 비교를 하지 않는다.
druskacik이 일반 9B LLM에 구조화 출력을 건 것과 정확도와 속도를 비교하면 어떠냐고 물은 것도 같은 공백이다[^druskacik].

### 생각을 자르면 정확도가 줄고, 자르지 않으면 꼬리가 길다

`max_think`로 사슬을 자르는 것이 README의 지연 해법이다.
teravor는 이런 방식의 사후 학습 자체가 필요 없다며, LLM이 생각하게 한 뒤 사고가 끝난 자리에 특정 JSON을 강제하는 프리필을 쓰면 된다고 했다[^teravor].
betenoire가 Jev는 LLM으로는 짜증 날 만큼 느리고 불필요하게 비싼 곳에 흩뿌릴 수 있을 만큼 싸고 빠르다는 점이 요점이라고 반박하자[^betenoire], teravor는 그래서 Jev에 사고가 없는 것이라며 LLM의 사고를 이렇게 자르는 방식은 잘 통하지 않고 사고 자체도 효율적이지 않다고 답했다[^teravor-reply].

표의 숫자는 teravor의 경고와 README의 해법이 모두 부분적으로 맞다는 것을 보여 준다.
사슬을 768토큰으로 자르고 쉬운 문항을 건너뛰면 정확도는 0.825에서 0.806으로 조금만 떨어진다.
하지만 그래도 p90은 5.6초로, 사고 없음의 0.3초와 한 자릿수 이상 차이가 난다.
결정마다 수백 ms 안에 답해야 하는 루프에서는 어느 설정도 들어갈 자리가 없다.

### 로컬에서 돌린다는 약속은 하드웨어에 달려 있다

TN1ck은 독일 축구 트윗의 반어 탐지 벤치마크를 M5 Pro 48GB에서 돌렸는데, 트윗 100개를 결정하는 데 30분이 넘게 걸렸고 Jev 79개 대 Jeeves 68개를 맞췄지만 다른 공개 결정 모델보다는 나았다고 보고했다[^TN1ck].
이후 394개 데이터로 한 콘텐츠 모더레이션은 약 2시간이 걸렸고, Jev만큼은 아니지만 아주 가까웠다며 모더레이션의 엄격함을 조절할 수 있다는 점이 좋다고 덧붙였다[^TN1ck-update].
작성자의 동료 robbie-c는 M5 Pro 성능을 꽤 올려 줄 MPS 이식 작업을 진행 중이라고 답했다[^robbie-c].

문항당 18초는 README의 H100 중앙값 3.3초와 거리가 멀다.
48GB Mac은 README가 스스로 경계선이라고 적은 사양이고, 캐시를 줄이면 동시 문항 수도 준다.
로컬 추론이 가능하다는 것과 로컬에서 쓸 만하다는 것은 다른 문제다.

## 함정

### 예시 응답이 보여 주는 두 가지 문제

README의 예시 응답은 H100 한 장, `--precision fp8`에서 세 질문을 병렬로 생각해 `latency_ms` 8141.6을 기록했다.
`max_think`를 512로 줬는데도 추론 토큰은 1,536개였다.
README는 `max_think`가 추론 사슬 각각을 자른다고 설명하므로, 질문 셋이 각각 512토큰씩 쓴 결과로 맞아떨어진다.
즉 `max_think`는 요청 전체가 아니라 질문마다 적용된다.
질문 수가 늘면 비용도 그만큼 늘어난다.

같은 예시에서 `department`는 billing을 0.46, returns를 0.40으로 골랐고 `confidence`는 0.19다.
상태에는 늦은 배송, 잘못된 사이즈, 이중 청구가 함께 들어 있으니 셋 중 하나만 고르라는 질문 자체가 모호하다.
`choice`는 하나만 고르게 하므로, 여러 부서가 얽힌 상태라면 부서마다 `noul`을 따로 묻는 편이 낫다.
낮은 `confidence`는 모델의 약점이 아니라 질문 설계의 신호로 읽어야 한다.

### 두 개의 테스트 숫자가 서로 다르다

결과표의 테스트 전체는 0.889인데, 본문은 같은 체크포인트가 테스트 분할 2,962문항에서 사고 없이 0.804, 사고와 함께 0.840이라고 적는다.
표의 행은 분포 밖과 보류 문항을 문항 수로 가중한 값이라고 되어 있으니 집계 대상이 다른 것으로 보이지만, README는 둘의 관계를 설명하지 않는다.
Jev와 비교할 때는 어느 숫자를 쓰는지 확인해야 한다.

### 추론 사슬은 읽을 수 있다고 가정하면 안 된다

README는 언어 일관성 보상을 넣지 않았기 때문에 사고 사슬을 잘 해석할 수 없다고 한계에 적는다.
`return_reasoning`으로 사슬을 받아 사람에게 보여 주거나 감사 기록으로 남길 계획이라면, 그 텍스트가 결정의 근거를 충실하게 반영한다고 믿으면 안 된다.

## 비평

### 문제 정의의 전제가 검증되지 않았다

README는 Jev 계열 모델이 보정된 확률을 주지만 정확도가 낮다는 문장으로 시작한다.
esafak은 이 문장을 인용해, 그렇다면 왜 둘 다를 보여 주지 않았느냐고 물었다[^esafak].
실제로 결과표에서 Jev는 테스트 전체 0.857, JevBench 0.866이고, 지식 문항에서는 Jeeves보다 높다.
정확도가 낮다는 전제는 README의 표로는 성립하지 않는다.

더 중요한 것은 전제가 겨냥하는 대상이다.
Jev 계열 파이프라인이 추론 모델로 넘기는 문항이 무엇이고 얼마나 되는지, 그 문항에서 Jeeves가 추론 모델보다 나은지가 이 모델의 존재 이유를 증명할 숫자다.
README는 Jev와 Kev를 이기는 숫자를 보여 주지만, 정작 대체하겠다는 대상과의 비교는 없다.

### 보정이 좋아졌다는 주장은 한 숫자에 기대고 있다

JevBench ECE 0.037 대 Jev 0.049가 보정 쪽의 유일한 비교이고, 공개 231문항에서만 쟀다.
finding_alfred는 Jev가 실제로 보정되어 있다는 데이터가 있느냐고 물었다[^finding_alfred].
LudwigNagasena는 `noul`이 돌려주는 값이 베이즈 통계에서 credence라 부르는 것인데 굳이 새 용어를 만들었다고 지적했다[^LudwigNagasena].

Jev 계열 모델의 약속은 확률이 실제 정답률과 맞는다는 것이고, 추론 사슬이 그 확률을 어떻게 바꾸는지는 이 모델에서 가장 궁금한 질문이다.
생각을 한 뒤의 확률이 더 날카로워지는지, 틀린 사슬이 틀린 답에 높은 확률을 주는지는 문항 수준의 보정 곡선으로만 알 수 있다.
README가 CISPO를 402스텝에서 멈춘 이유로 헤드의 과도한 날카로움을 든 것을 보면, 저자도 이 위험을 알고 있다.
그렇다면 사고 유무에 따른 보정 곡선을 함께 공개했어야 한다.

### 환각이 없다는 주장의 무게가 사용자에게 옮겨 간다

k__는 환각이 없다는 전제 전체가 결국 사용자에게 마지막 결정을 떠넘기는 데서 나온다고 지적했다[^k__].
doginasuit는 그것이 결코 틀리지 않는 모델이 아닌 이상 환각을 없애는 유일한 방법이라고 답했다[^doginasuit].

Jeeves는 이 논쟁에 새 변수를 더한다.
답은 여전히 선택지 위의 분포라 형식상 환각할 수 없지만, 그 앞에 생성된 사슬이 있다.
사슬 안에서 사실을 지어내고 그 위에서 선택지를 고르면, 출력은 타입이 맞는 채로 틀린다.
타입 안전성은 출력의 모양을 보장할 뿐 판단의 근거를 보장하지 않으며, 사고를 더한 모델에서는 그 간격이 더 넓어진다.

## 체크리스트

- 자기 과제에서 사고 없음(`think: false`)과 전체 사고의 정확도 차이를 쟀는가?
- 결정 루프의 지연 예산이 p90 5.6초 이상을 견디는가?
- `max_think`가 질문마다 적용된다는 점을 비용 계산에 넣었는가?
- 여러 주제가 섞인 상태에 `choice` 대신 주제별 `noul`을 썼는가?
- 48GB Mac이라면 캐시를 줄이거나 `--precision fp8`을 썼는가?
- 추론 LLM에 구조화 출력을 건 기존 대체 경로와 직접 비교했는가?
- `return_reasoning`의 사슬을 결정 근거로 사람에게 보여 주려 하지 않는가?

## 기억할 원칙

### 대체 경로를 흡수하는 모델은 그 대체 경로와 비교해야 한다

Jeeves의 설계는 영리하다.
빠른 결정 모델과 느린 추론 모델로 나뉘던 두 경로를 하나의 인터페이스와 두 개의 손잡이, `think`와 `nothink_threshold`로 합쳤다.
하지만 합친 모델의 가치는 빠른 쪽을 이기는 숫자가 아니라, 느린 쪽을 대체할 만큼 정확하고 그보다 싸다는 숫자로 증명된다.
무엇을 대체하려는지 정했으면 비교표의 열도 그 대상으로 채워야 한다.

### 지연의 꼬리가 모델의 쓰임새를 정한다

중앙값 3.3초와 p90 17.1초는 같은 모델의 두 얼굴이다.
실시간 루프, 사용자 대기, 배치 처리 중 어디에 넣을지는 평균이 아니라 꼬리가 정한다.
사고하는 결정 모델은 배치 모더레이션처럼 기다릴 수 있는 곳에서 가장 먼저 자리를 찾을 것이고, TN1ck의 모더레이션 실험이 바로 그 경우였다.

---

[^sharih]: <https://news.ycombinator.com/item?id=49892563>

[^itzikkatz]: <https://news.ycombinator.com/item?id=49896483>

[^hjun1052]: <https://news.ycombinator.com/item?id=49891626>

[^druskacik]: <https://news.ycombinator.com/item?id=49894747>

[^teravor]: <https://news.ycombinator.com/item?id=49894284>

[^betenoire]: <https://news.ycombinator.com/item?id=49894390>

[^teravor-reply]: <https://news.ycombinator.com/item?id=49894433>

[^TN1ck]: <https://news.ycombinator.com/item?id=49893066>

[^TN1ck-update]: <https://news.ycombinator.com/item?id=49897575>

[^robbie-c]: <https://news.ycombinator.com/item?id=49906269>

[^esafak]: <https://news.ycombinator.com/item?id=49892837>

[^finding_alfred]: <https://news.ycombinator.com/item?id=49898873>

[^LudwigNagasena]: <https://news.ycombinator.com/item?id=49892782>

[^k__]: <https://news.ycombinator.com/item?id=49892039>

[^doginasuit]: <https://news.ycombinator.com/item?id=49892195>
