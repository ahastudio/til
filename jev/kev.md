# Kev: Qwen3.5 위에 직접 학습하고 돌리는 Jev 계열 의사결정 모델

<https://github.com/jaredpalmer/kev>

HN 토론: <https://news.ycombinator.com/item?id=49783999> (427점, 192개 댓글)

GN 토론: <https://news.hada.io/topic?id=34065>

## 소개

Qwen3.5 위에 올린 작은 의사결정 모델 계열이다.
[Jev](jev.md)의 구조를 다룬 [Jev's Architecture Unmasked](architecture-unmasked.md)에 서술된 설계를 바탕으로 하며,
API는 TypeSafe의 System One과 맞춰져 있어 그쪽 Python SDK를 로컬 서버로 향하게 할 수 있다.
2026년 9월 17일에 만들어졌고 Apache 2.0 라이선스이며 Python으로 쓰였다.

같은 문제를 겨냥한 다른 오픈 시도들과의 차이가 분명하다.
[Jevlike](jevlike.md)가 입출력 모양만 가져온 시작점 모델이라고 스스로를 규정하는 데 비해,
Kev는 0.8B와 4B와 9B 세 크기의 사전 학습된 가중치와 학습 코드와 평가 데이터를 함께 내놓고
Jev와의 수치 비교를 표로 제시한다.
그 비교가 통제된 비교가 아니라는 단서도 함께 붙인다.

한 요청 안에서 세 가지 질문 유형을 섞을 수 있다.
예 또는 아니오를 묻는 `noul`, 선택지에서 고르는 `choice`, 등급을 매기는 `score`다.
질문들은 입력 텍스트를 공유하지만 서로를 읽지 못한다.
이 격리가 이 프로젝트의 기술적 중심이고, 아래 아키텍처 절에서 다시 다룬다.

CUDA와 ROCm과 Apple Silicon에서 돌아간다.
4B와 9B는 bf16으로 32GB Mac에 들어가지만, 속도에는 단서가 붙는다.
서빙 성능 절에서 다룬다.

## 빠르게 돌려 보기

Python 3.12 이상과 `uv`가 필요하다.

```bash
git clone https://github.com/jaredpalmer/kev.git && cd kev
uv sync --extra serve
KEV_DTYPE=bf16 uv run --extra serve python -m kev.serve --run jaredpalmer/kev-4b --port 8009
```

첫 실행에서 어댑터와 기반 모델을 내려받는다.
`--run`에는 로컬 체크포인트 디렉터리나 Hub 리비전도 넘길 수 있으며,
`jaredpalmer/kev-4b@qwen3`처럼 쓰면 이전 세대를 부른다.

다른 터미널에서 고객 문의 하나를 보낸다.

```bash
curl -s localhost:8009/v1/systemone -H 'content-type: application/json' -d '{
  "state": "Shoes arrived two weeks late and in the wrong size. Also I see two charges on my card.",
  "model": "kev-latest",
  "questions": {
    "department":  {"type": "choice", "instructions": "Which team should handle this?",
                    "criteria": {"returns": "Exchanges, refunds, wrong or damaged items",
                                 "shipping": "Delivery status, delays, lost packages",
                                 "billing": "Charges, invoices, payment problems"}},
    "escalate":    {"type": "noul",  "instructions": "Does this need urgent human attention?"},
    "frustration": {"type": "score", "instructions": "How frustrated is the customer?",
                    "criteria": ["Calm", "Frustrated", "Very angry"]}
  }}'
```

Apple M5에서 bf16으로 돌린 Kev-4B의 응답은 이렇다.

```json
{
  "model": "kev-latest",
  "answers": {
    "department":  { "type": "choice", "choice": "returns", "confidence": 0.21,
                     "probabilities": { "returns": 0.47, "shipping": 0.28, "billing": 0.25 } },
    "escalate":    { "type": "noul", "noul": 0.93 },
    "frustration": { "type": "score", "score": 1.44, "confidence": 0.78,
                     "legend": { "0": "Calm", "1": "Frustrated", "2": "Very angry" },
                     "probabilities": { "0": 0.00, "1": 0.56, "2": 0.44 } }
  },
  "usage": { "input_tokens": 101, "output_tokens": 161 },
  "latency_ms": 495
}
```

이 예시가 README에 실린 이유는 부서 확률 분포에 있다.
이 문의는 반품과 배송 지연과 결제 문제를 모두 언급하고 있고, 확률이 그것을 그대로 말한다.
레이블 하나가 아니라 확률을 돌려받는 이유가 이것이라는 것이다.
`confidence` 0.21은 세 선택지에 대해 최댓값 0.47이 거의 균등에 가깝다는 뜻이며, 뒤에 나오는 공식으로 계산된다.

TypeSafe SDK는 `uv sync --extra serve`에 포함되어 있다.

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient(
    api_key="local",
    base_url="http://127.0.0.1:8009",
    model="kev-latest",
)
response = client.system_one(
    state="I was charged twice. Please fix this ASAP.",
    questions={
        "billing": Noul(instructions="Is this ticket about billing?"),
        "tone": Choice(
            instructions="What is the customer's tone?",
            criteria={"calm": None, "frustrated": None, "angry": None},
        ),
        "urgency": Score(
            instructions="How urgent is this ticket?",
            criteria=["can wait", "this week", "today"],
        ),
    },
)
print(response.nouls["billing"].noul)
print(response.choices["tone"].choice)
print(response.scores["urgency"].score)
```

Node 20.9 이상이 있으면 웹 놀이터도 띄울 수 있다.

```bash
cd playground
npm install
npm run dev -- -p 3001
```

프리셋 중 두 개가 진단 도구로 쓸 만하다.
모든 질문을 한 번에 묻는 것과 하나씩 묻는 것을 비교하는 것, 그리고 `choice` 질문을 여섯 가지 선택지 순서로 돌려 보는 것이다.
질문 격리와 가짜 구분자 토큰을 시험하는 프리셋도 있다.
체스 데모도 있는데, 판이 입력이고 합법 수가 `choice` 선택지이며 `score` 질문이 국면을 평가한다.

## 모델 고르기

세 모델 모두 같은 학습 데이터와 설정으로 Qwen3.5 기반 위에 만들어졌다.

| 모델     | 기반              | 학습 출처 정확도 | 새 출처 정확도 | 새 출처 Brier |
| -------- | ----------------- | ---------------- | -------------- | ------------- |
| Kev-0.8B | Qwen3.5-0.8B-Base | 0.825 / 0.834    | 0.652 / 0.684  | 0.499 / 0.460 |
| Kev-4B   | Qwen3.5-4B-Base   | 0.872 / 0.871    | 0.797 / 0.837  | 0.299 / 0.255 |
| Kev-9B   | Qwen3.5-9B-Base   | 0.872 / 0.874    | 0.822 / 0.852  | 0.286 / 0.237 |
| Jev      | 호스팅            | 0.845 / –        | 0.857 / –      | 0.211 / –     |

각 칸은 개발 세트와 테스트 세트의 값이다.
학습 출처는 Kev 학습에 쓴 데이터셋에서 떼어 둔 예제이고, 새 출처는 학습하지 않은 데이터셋과 정책 규칙 유형이다.
테스트 세트는 릴리스된 체크포인트마다 모델 선택이 끝난 뒤 한 번만 읽었다.
Brier는 낮을수록 좋다.

README가 이 표를 해석하는 방식이 이 저장소의 성격을 잘 보여 준다.
Kev-9B가 새 출처 개발 세트에서 Jev에 3.5점 뒤진다고 먼저 적고,
테스트 세트에서 0.852를 얻었지만 Jev는 그 세트에서 돌려 본 적이 없다고 덧붙이고,
Jev가 어떤 데이터셋으로 학습했는지 모르므로 두 아키텍처의 통제된 비교가 아니라고 분명히 밝힌다.
숫자를 내놓으면서 그 숫자가 무엇을 말할 수 없는지를 같은 문단에서 말한다.

실무 지침은 단순하다.
Kev-4B에서 시작하고, 정확도와 보정이 메모리보다 중요하면 Kev-9B를 쓰고, 가장 작은 것이 필요하면 Kev-0.8B를 쓴다.

세대 교체에 대한 서술도 방법론이 드러나는 대목이다.
이전 세대는 Qwen3 기반에 같은 데이터와 설정을 썼으므로 기반만 바뀐 통제된 비교가 된다.
개발 세트에서는 정확도 향상이 잡음 범위 안이었고, 테스트 세트에서 Kev-9B가 Kev-8B보다 7.3점 앞섰다.
95% 신뢰구간이 +2.8에서 +11.7이고 Brier는 0.08 낮다.
Kev-4B는 전 세대보다 2.9점 앞섰는데 구간이 −0.9에서 +6.4로 0을 포함한다.
즉 개선이 확인된 것은 가장 큰 모델뿐이며, README는 그것을 숨기지 않고 구간째 적어 둔다.

2026년 9월 21일에 세 모델 모두 생성 예제에 대한 짧은 2차 학습을 받았다.
명시적인 일수가 들어간 정책 사례와, 판단 근거가 제거된 사례를 균등한 답 쪽으로 학습시킨 것이다.
테스트 세트에서 Kev-9B가 0.837에서 0.852로 올라갔고 구간은 +0.8에서 +2.9다.
이전 가중치는 `v7-base` 리비전에 남아 있다.

## 아키텍처: 질문 격리를 두 방식으로 구현한다

이 저장소에서 가장 배울 것이 많은 부분이다.
각 체크포인트는 Qwen 기반 위의 랭크 16 LoRA 어댑터와 작은 포인터 헤드다.

어텐션만 쓰는 기반, 즉 Qwen3에서는 상태와 질문들이 한 토큰 열에 들어간다.

```text
<state> …state…
<q> instructions <opt> option 1 </opt> <opt> option 2 </opt> … <decide>
<q> instructions <opt> option 1 </opt> <opt> option 2 </opt> … <decide>
```

어텐션 마스크가 각 토큰이 상태와 자기 질문은 읽되 다른 질문과 미래 토큰은 읽지 못하게 한다.
그리고 각 질문의 위치 ID가 상태 바로 다음에서 다시 시작한다.
이 두 장치 덕분에 상태를 한 번만 처리하고 각 질문에 독립적으로 답할 수 있다.

Qwen3.5는 어텐션 층과 Gated DeltaNet 층을 섞는데, 후자는 순환형이라 어텐션 마스크를 무시한다.
그래서 이 기반에서는 각 질문이 자기 행으로 돌아간다.
상태 다음에 그 질문 하나가 오는 형태이고 위치는 위와 같다.
행들이 독립적이므로 격리가 정확하며, 서버는 상태를 한 번 계산해 그 캐시를 모든 행에 재사용한다.
어텐션만 쓰는 모델에서는 두 형태가 동일한 확률을 내며 그것이 테스트로 확인되어 있다.

같은 보장을 아키텍처가 바뀌자 다른 방법으로 다시 구현했다는 점이 중요하다.
마스크로 격리를 얻던 것을 행 분리로 바꾸면서, 비용은 상태 캐시 재사용으로 상쇄했다.
추상의 계약을 유지하면서 구현을 갈아 끼운 사례이고, 계약이 문서와 테스트로 표현되어 있어 확인이 가능하다.

포인터 헤드는 각 선택지의 `</opt>` 은닉 상태를 질문의 `<decide>` 은닉 상태에 대해 점수화하고 softmax로 확률을 만든다.
`<decide>`가 마지막에 오므로 선택지 목록 전체를 볼 수 있다.
학습은 정답에 대한 교차 엔트로피를 쓰며 어댑터와 헤드를 함께 학습하고 나머지 기반 가중치는 고정한다.
학습 예제와 API 요청이 같은 텍스트 형식을 쓴다.
그리고 Jev의 출력은 학습에 쓰이지 않았다고 명시한다.

주의할 구분이 하나 있다.
질문을 함께 묻든 따로 묻든 fp32 테스트에서 확률 차이가 `4e-6` 이내다.
그러나 이것이 선택지 순서가 무관하다는 뜻은 아니다.
한 질문 안의 선택지들은 여전히 서로에게 영향을 줄 수 있다.
놀이터의 순열 프리셋과 `/v1/systemone/permute` 엔드포인트가 그 영향을 직접 재 보라고 있는 것이다.

## 신뢰도와 보정

`confidence`는 정확도가 아니다.
README가 그 점을 명시하고 계산식을 공개한다.

선택지가 `K`개인 `choice`에서 신뢰도는 `(p_max − 1/K) / (1 − 1/K)`다.
선택지가 하나면 신뢰도는 1이다.
`score`의 신뢰도는 분포가 가장 그럴듯한 등급에 얼마나 가까운지를 재며,
TypeSafe의 공개되지 않은 공식에 대한 근사라고 적혀 있다.

확률은 기본적으로 보정되어 있다.
각 체크포인트가 분포 내 개발 세트에서 맞춘 온도를 저장하고 있고 값은 대략 2.1에서 2.4이며, 모델을 적재할 때 포인터 헤드가 그것을 적용한다.
답을 바꾸지는 않는다.
새 출처에서 Kev-9B의 보정 오차가 0.106에서 0.042로, 확신에 찬 오답, 즉 확률 0.9 이상인 틀린 답의 비율이 8.7%에서 4.0%로 내려간다.
Jev의 3.7%와 비슷한 수준이고 정확도는 동일하다.
원시 로짓을 보려면 `KEV_TEMPERATURE=1.0`으로 두면 되고, 표의 Brier 수치는 원시 로짓 기준이다.

선택적 설정이 하나 있다.
`KEV_DATE_FACTS=1`은 상태에서 찾은 두 절대 날짜 사이의 일수를 덧붙인다.
Kev는 날짜를 안정적으로 빼지 못하지만 명시된 일수는 쓸 수 있어서,
기한 정책 질문에서 Kev-9B가 0.80에서 0.90으로 올라간다.
Jev는 0.93이다.
위의 표는 이 설정을 쓰지 않은 값이다.

이 항목은 모델의 한계를 우회 설계로 메운 좋은 예다.
산술을 학습으로 해결하려 하지 않고, 산술 결과를 입력에 넣어 주는 전처리로 옮겼다.

## 서빙 성능과 하드웨어

CUDA와 ROCm에서는 Qwen3.5 모델용으로 `flash-linear-attention`을 설치하면
질문 다섯 개짜리 요청이 H100과 MI300X에서 수십 밀리초에 끝난다.

Apple Silicon에는 DeltaNet 층을 위한 빠른 커널이 없어 PyTorch가 참조 구현을 돌린다.
M5에서 bf16으로 약 230토큰 상태에 선택지 세 개짜리 질문 다섯 개를 보낸 중앙값이다.

| 모델     | 시간   | 같은 요청에 대한 이전 세대                        |
| -------- | ------ | ------------------------------------------------- |
| Kev-0.8B | 329ms  | Kev-0.6B (Qwen3): 123ms                           |
| Kev-4B   | 779ms  | Kev-4B (Qwen3), `jaredpalmer/kev-4b@qwen3`: 174ms |
| Kev-9B   | 약 2초 | Kev-8B (Qwen3): 약 300ms                          |

세대가 올라가면서 Mac에서의 지연이 네 배에서 일곱 배로 늘었다.
Mac에서 서빙하면서 낮은 지연이 필요하면 당분간 Qwen3 모델을 쓰라고 README가 직접 권한다.
Qwen3.5 모델용 MLX 백엔드가 다음 계획이다.

어텐션만 쓰는 모델에는 서버 쪽 최적화가 여럿 들어가 있다.
캐스팅 전에 LoRA 가중치를 fp32로 병합하고, Apple GPU에서 SDPA 어텐션을 쓰고,
MPS 입력을 64토큰 단위로 패딩하고, 반복되는 요청을 위해 상태 접두부를 캐시한다.
기본값은 384토큰 이상인 상태 네 개다.
772토큰 상태를 반복하면 Kev-4B (Qwen3)가 861ms 대신 242ms에 답한다.

각각 `KEV_MERGE=0`, `KEV_ATTN=eager`, `KEV_SHAPE_BUCKET=1`, `KEV_PREFIX_CACHE=0`으로 끌 수 있다.
새 출처 24건에서 bf16 확률이 fp32와 최대 0.017 달랐고 최고 확률 답은 바뀌지 않았다.
README는 이것이 작은 확인이지 모든 입력에 대한 보장이 아니라고 적는다.

## 자기 데이터로 파인튜닝하기

이 절이 이 저장소를 실제로 쓸 이유에 가장 가깝다.
질문이 릴리스된 모델의 학습 데이터와 다르게 생겼다면,
즉 자기만의 라우팅 범주나 에스컬레이션 규칙이나 다른 언어라면,
수백 개의 레이블 예제로 짧게 파인튜닝하는 것이 어떤 프롬프트 변경보다 대개 낫다는 것이 README의 주장이다.

예제는 JSONL 한 줄에 요청 하나씩 넣고, API 요청과 같은 모양에 질문마다 `label`을 더한다.

```jsonl
{"state": {"subject": "Charged twice", "body": "I see two charges for order #4411. Please refund one."},
 "questions": {
   "team":     {"type": "choice", "instructions": "Which team should handle this ticket?",
                "criteria": {"billing": "Payments and refunds", "shipping": "Delivery problems", "access": "Login and account access"}, "label": "billing"},
   "angry":    {"type": "noul",   "instructions": "Is the customer angry?", "label": false},
   "priority": {"type": "score",  "instructions": "How urgent is this ticket?", "criteria": ["low", "normal", "high"], "label": 1}}}
```

`choice`의 레이블은 선택지 이름, `noul`은 참 또는 거짓, `score`는 0부터 세는 등급 위치다.
파일의 10~20%는 평가용으로 떼어 둔다.

그다음 릴리스된 체크포인트에서 시작한다.

```bash
uv run python -m kev.train --data train.jsonl --base Qwen/Qwen3.5-4B-Base --init_from jaredpalmer/kev-4b \
    --epochs 2 --lr 2e-5 --batch 1 --accum 8 --dtype bf16 --checkpointing 1 --device cuda --out runs/mine

uv run python -m kev.benchmark --run runs/mine --data heldout.jsonl --out runs/mine-eval
KEV_DTYPE=bf16 uv run --extra serve python -m kev.serve --run runs/mine --port 8009
```

`--init_from`이 핵심이고, 그 효과가 숫자로 제시되어 있다.
한 사용자가 지원 도구 관련 결정 836건으로 시험한 결과,
기반 모델에서 처음부터 파인튜닝한 것은 Kev 자체 평가 세트에서 0.33을 얻었고 릴리스된 모델은 0.84였다.
같은 데이터를 `--init_from`으로 학습하자 그 평가 세트에서 0.83을 유지하면서 새 영역에서 0.88에 도달했다.
기반에서 시작하는 것은 Kev가 이미 아는 것을 버리는 일이라는 뜻이다.

학습률은 처음부터 학습할 때보다 낮춰야 하고 `2e-5`가 좋은 출발점이다.
`--base`는 시작하는 체크포인트에 맞춰야 하며, 학습기가 기반과 리비전과 LoRA 랭크와 헤드 크기가 맞는지 적재 전에 확인한다.
`--batch 1 --accum 8`을 bf16으로 쓰면 0.8B 모델이 4GB GPU에 들어간다.
벤치마크가 질문 유형별로 정확도와 Brier와 보정을 보고하므로 어떤 질문에서 파인튜닝이 도움이 되었는지 볼 수 있다.

코딩 에이전트와 함께 일한다면 저장소에 포함된 `kev-finetune` 스킬이 이 과정을 Modal 위에서 대신 해 준다.
질문을 인터뷰하고, 코드가 이미 Jev나 TypeSafe에 던지는 질문을 찾아내고,
가진 레이블을 변환하거나 개선을 잴 만큼을 다른 LLM으로 생성하고,
릴리스된 체크포인트에서 파인튜닝하고, 떼어 둔 조각에서 온도를 맞추고,
기준선과 비교해 점수를 내고, System One 엔드포인트를 배포하고, 전부 정리한다.

## 평가

`evals/` 아래의 평가 데이터는 동결되어 있다.
데이터셋 판본과 파일 체크섬이 각 매니페스트에 기록되어 있고,
큰 학습 파일은 Hub 미러에서 내려받아 그 해시와 대조한다.

```bash
uv run python -m kev.benchmark --run jaredpalmer/kev-4b --suite evals/v4/transfer-v4 --out runs/my-eval
uv run python -m kev.benchmark --run jaredpalmer/kev-4b --suite evals/v9/transfer-v9 --out runs/my-eval-v9
uv run python -m kev.benchmark --run jaredpalmer/kev-4b --suite evals/v7/decision-v7 --out runs/my-eval-id
uv run python -m kev.benchmark --remote http://127.0.0.1:8009 --suite evals/v4/transfer-v4 --out runs/my-remote
```

마지막 명령이 보여 주듯 어떤 System One 엔드포인트에도 같은 평가를 돌릴 수 있다.

이 명령들은 개발 데이터를 쓰며 테스트 데이터에는 `--allow-test`가 필요하다.
Modal에서 연구를 돌릴 때도 같은 규율이 명령으로 강제된다.

```bash
uv run modal run modal_app.py::locked_test --trial my-study/00-trial-0 --name my-candidate   # 평생 한 번
```

벤치마크가 보고하는 항목이 이 프로젝트의 관점을 드러낸다.
정확도와 Brier와 보정 오차에 더해, 5% 오류 예산에서 자동화할 수 있는 결정의 비율,
선택지 순서에 따른 변화, 그리고 질문 격리를 함께 보고한다.
`transfer-v9`는 10지선다 MMLU-Pro와, 무관한 텍스트 사이에 묻힌 기록과,
판단 근거가 제거된 알 수 없는 기록을 더한다.
마지막 항목에 대해서는 모델이 그래도 0.9 이상의 확신으로 답하는 비율을 보고하는데
Kev-9B가 5%, Jev가 9%, Kev-8B가 26%다.
공개된 정확도 수치는 bf16 서빙 경로가 아니라 fp32 평가를 쓴다.

`evals/external/`에는 다른 두 프로젝트의 테스트 세트가 이 형식으로 변환되어 들어 있고,
그들이 공개한 실제 Jev 결과가 함께 있다.
[SemIf](semif.md)의 직접 작성한 결정 144건에서 Kev-9B 0.917에 Jev 0.965,
scienthoon의 지원 티켓 900건에서 라우팅은 Kev-9B 0.952에 Jev 0.897, 어조는 0.911에 0.914다.
두 세트 중 하나에서는 Kev가 앞서고 다른 하나에서는 뒤진다는 것을 그대로 싣는다.

## 값 정하기

| 결정할 것       | 무엇에 따라 정하는가                                                      |
| --------------- | ------------------------------------------------------------------------- |
| 모델 크기       | 4B에서 시작. 보정이 중요하면 9B, 메모리가 한계면 0.8B                     |
| 기반 세대       | 서버가 CUDA/ROCm이면 Qwen3.5. Mac에서 서빙하고 지연이 중요하면 Qwen3      |
| 온도            | 기본 보정값 유지. 원시 확률이 필요한 분석에만 `KEV_TEMPERATURE=1.0`       |
| 파인튜닝 시작점 | 거의 항상 `--init_from`. 기반에서 시작하는 것은 도메인이 완전히 다를 때만 |
| 파인튜닝 학습률 | `2e-5`에서 시작. 처음부터 학습할 때의 `5e-5`보다 낮게                     |
| 자동화 임계값   | 벤치마크의 오류 예산별 자동화 비율. 신뢰도 값 자체가 아니라               |
| 날짜 전처리     | 기한 규칙이 있으면 `KEV_DATE_FACTS=1`. 없으면 입력만 길어진다             |

## 함정

신뢰도를 정확도로 읽는 것이 가장 흔한 오해다.
README가 두 필드 모두 측정된 정확률이 아니라고 명시한다.
`choice` 신뢰도는 최댓값이 균등분포에서 얼마나 떨어져 있는지를 정규화한 값이고, 모델이 옳을 확률이 아니다.
자동화 임계값을 정할 때는 벤치마크가 주는 오류 예산별 자동화 비율을 봐야 한다.

질문을 함께 물어도 확률이 같다는 것을 선택지 순서도 무관하다는 뜻으로 읽으면 안 된다.
격리는 질문 사이에만 보장되고, 한 질문 안의 선택지들은 서로 영향을 준다.
그래서 `permute` 엔드포인트가 따로 있다.

서버는 `127.0.0.1`에 바인딩되고 인증이 없다.
인증을 직접 붙이지 않는 한 로컬 밖으로 내보내면 안 된다.

Mac에서 세대를 올리면 느려진다.
이전 세대가 더 빠르다는 사실이 표에 있는데, 최신 가중치를 쓰는 것이 당연히 낫다고 가정하면 지연이 네 배 이상 늘 수 있다.

`usage.output_tokens`는 직렬화된 답의 토큰 수이고 생성된 토큰 수가 아니다.
비용 모형을 이 값으로 세우면 어긋난다.

테스트 세트를 여러 번 읽는 것이 방법론적 함정이다.
이 저장소는 그것을 명령 이름과 플래그로 막아 두었지만, 자기 데이터로 같은 절차를 세울 때는 스스로 지켜야 한다.

그리고 Jev와의 비교표를 통제된 비교로 읽으면 안 된다.
Jev의 학습 데이터가 무엇인지 모르므로, 새 출처라는 구분이 Jev에게도 새 출처였는지 알 수 없다.
README가 그 단서를 붙여 두었다.

## 비평

### 아키텍처를 재현해도 학습 데이터를 재현한 것은 아니다

HN 논의에서 가장 날카로운 반론은 이 계열 프로젝트 전체를 겨눈다.
andy12_는 보통의 LLM 위에 Jev 모양의 API만 씌우는 사람들이 요점을 놓치고 있다고 적었다.[^andy12_]
Jev를 특별하게 만드는 것은 학습 데이터이고 학습 방식이며, 아키텍처는 아마 특별할 것이 없다는 것이다.
텍스트 인코더에 병렬 예측 가지를 붙인 것뿐이고,
자신이 여러 오픈소스 Jev 유사 모델을 언어 과제에 써 보았는데 Jev에 비해 형편없었다고 말한다.

Kev는 이 반론에 대해 다른 프로젝트들보다 나은 위치에 있다.
API만 씌운 것이 아니라 포인터 헤드와 마스크 설계를 구현했고,
학습 데이터의 구성과 출처를 공개했고, 두 외부 프로젝트의 평가 세트에서 Jev와 나란히 수치를 냈다.
그리고 새 출처 개발 세트에서 여전히 3.5점 뒤진다는 것을 스스로 표에 적었다.
즉 반론이 지목한 격차가 실재한다는 것을 저장소 자신이 확인해 준다.

hbarka의 물음도 같은 방향이다.
Jev가 근본적으로 한 방식으로 학습되었는데 다른 방식으로 학습된 Qwen 모델 위에 만든다면,
그 결과를 Jev 계열이라 부를 수 있느냐는 것이다.[^hbarka]
이 물음이 가리키는 것은 계열이라는 말의 뜻이다.
입출력 모양이 같으면 계열인지, 내부 구조가 같아야 계열인지, 성능 분포가 비슷해야 계열인지가 정해져 있지 않다.
Kev는 첫 번째와 두 번째를 충족하고 세 번째는 부분적으로만 충족한다.

그렇다면 이 프로젝트의 값어치를 어디서 찾아야 하는지가 남는다.
가장 설득력 있는 답은 성능이 아니라 운영 조건 쪽에서 나온다.
prodigycorp는 Jev 이야기에 이미 지쳤다면서도 핵심을 짚는다.[^prodigycorp]
Jev의 장점은 제품을 좋게 만들고 유지하는 데 전념하는 회사가 있다는 것이고,
이 Jev 모양의 프로젝트들은 기회주의적으로 보여 아직 올라타지 않았다는 것이다.
그런데 Jev에 대한 자기 열의가 데이터 정책에서 벽에 부딪힌다고 말한다.
넣은 것을 전부 보관하는 정책이 지나치며,
데이터를 보관하지 않는 제품을 내놓지 않으면 그 플랫폼은 시작부터 끝난 것이고,
열린 Jev 모양 모델은 그 이유 하나만으로 이길 것이라는 주장이다.

이 관점에서 보면 Kev가 비교해야 할 대상은 Jev의 정확도가 아니다.
데이터를 밖으로 내보내지 않고 얻을 수 있는 최선의 정확도다.
그리고 README의 파인튜닝 수치가 바로 그 계산을 위한 것이다.
릴리스 모델 0.84에서 자기 도메인 0.88로 가는 경로가 있다면, 개발 세트의 3.5점 격차는 다른 무게를 갖는다.
README가 이 논거를 명시적으로 세우지 않은 것이 아쉽다.
숫자는 다 있는데 그것이 무엇에 대한 답인지가 정리되어 있지 않다.

### 더 단순한 방법과의 비교가 빠져 있다

이 저장소에는 Jev와의 비교와 이전 세대와의 비교가 있지만, 더 아래쪽 기준선과의 비교가 없다.
그리고 HN에서 가장 많이 읽힌 반응이 정확히 그 기준선을 제시한다.

nico는 분류만 필요하고 학습 데이터를 조금 준비할 수 있다면
코딩 에이전트에게 임베딩과 로지스틱 분류기를 만들어 달라고 하면 된다고 적었다.[^nico]
이메일에서는 학습 예제 50~100개만으로 정확도 95%를 얻었고 CPU 학습이 5분 미만이라는 것이다.
그 방식의 이점도 함께 든다.
일반적인 이상적 분류가 아니라 자기 선호를 학습하고,
거의 모든 모바일 기기에서 돌며 기기 안에서 온라인 재학습이 가능하고,
구축 과정에서 에이전트에 전달하는 내용을 빼면 학습과 추론이 전부 로컬이다.
더 일반적인 검증으로 Banking77 분류기도 만들었는데 10MB 미만 모델이 CPU에서 30초 안에 학습되고 94.5%를 얻었다고 덧붙인다.

이 기준선이 중요한 이유는 Kev가 겨냥하는 사용 사례의 상당 부분과 겹치기 때문이다.
고정된 범주로 티켓을 분류하는 일이라면 임베딩 분류기가 더 작고 더 싸고 더 빠르다.
Kev가 의미를 갖는 것은 그 조건이 깨질 때다.
선택지 목록이 요청마다 바뀔 때, 선택지에 설명을 붙여야 할 때,
한 입력에 대해 서로 다른 유형의 질문 여럿을 동시에 물을 때,
그리고 레이블이 거의 없을 때다.
README의 첫 예시가 마침 그 조건을 모두 담고 있는데, 그것이 분류기로는 안 되는 이유는 설명하지 않는다.

이 비교가 없으면 도입 판단이 어려워진다.
9B 모델을 Mac에서 2초에 돌리는 것과 10MB 분류기를 30초 만에 학습해 밀리초에 돌리는 것 사이에는
정확도 몇 점으로 정리되지 않는 차이가 있다.
어떤 문제 모양에서 이 모델이 필요한지를 문서가 먼저 말해 주어야,
읽는 사람이 자기 문제가 그 모양인지 판단할 수 있다.

성숙도에 대한 회의도 함께 기록해 둘 만하다.
khazhoux는 이 모든 Jev 프로젝트가 좋지만 Jev가 나온 지 일주일밖에 되지 않았으므로
들어간 노력의 상한이 일주일이고, 그래서 필요하면 직접 만드는 것 대비 이들을 도입할 값어치를 모르겠다고 적었다.[^khazhoux]
이 회의는 Kev의 실험 기록과 동결된 평가 세트와 사전에 정한 기준을 보면 일부 누그러진다.
다만 시간이 걸러 낼 수 있는 것, 즉 판본 간 호환성과 유지 의사는 아직 확인할 방법이 없다.
raahelb가 짚은 도구 호출이 없어 지식 시점이 문제가 될 수 있다는 지적도 같은 계열이다.[^raahelb]
로컬에서 돌리면 계속 학습하거나, 폐쇄형을 쓰면 새 판본으로 옮겨 다녀야 한다는 것이다.

## 기억할 원칙

### 수치를 공개할 때는 그 수치가 답할 수 없는 질문을 같은 자리에 적는다

이 저장소가 다른 벤치마크 표와 다른 점은 숫자 자체가 아니라 숫자에 붙은 단서다.
Jev와의 비교가 통제된 비교가 아니라는 것, Jev가 그 테스트 세트에서 돌려진 적이 없다는 것,
신뢰구간이 0을 포함하는 개선이 어느 것인지, 표의 수치가 어느 정밀도로 평가되었는지,
그리고 bf16 확인이 24건짜리 작은 점검이지 보장이 아니라는 것이 모두 본문에 있다.

이 습관의 값어치는 신뢰가 아니라 재사용성에 있다.
단서가 없는 표는 읽는 사람이 자기 상황에 옮길 때 어디까지 옮겨도 되는지를 알 수 없으므로,
결국 가장 큰 숫자 하나만 인용되고 나머지는 버려진다.
단서가 붙은 표는 조건이 다른 사람이 그 조건 차이를 계산에 넣을 수 있다.

같은 원칙이 사내 벤치마크와 성능 보고서에도 적용된다.
무엇을 쟀는지만 적고 무엇을 재지 못했는지를 적지 않으면, 그 문서는 나중에 잘못 인용되기 위해 쓰인 것이 된다.

### 보장은 구현이 아니라 계약으로 유지한다

질문 격리라는 같은 보장을 이 프로젝트는 두 번 구현했다.
어텐션 기반에서는 마스크와 위치 재시작으로, 순환 층이 섞인 기반에서는 행 분리와 상태 캐시 재사용으로 얻는다.
기반 아키텍처가 바뀌어 첫 번째 방법이 성립하지 않게 되었을 때 보장을 포기하지 않고 구현을 바꿨다.

이것이 가능했던 이유는 보장이 구현 세부가 아니라 확인 가능한 계약으로 표현되어 있었기 때문이다.
질문들은 입력을 공유하지만 서로를 읽지 못한다는 문장이 있고,
두 형태가 같은 확률을 낸다는 것을 확인하는 테스트가 있고,
격리 자체를 재는 벤치마크 항목과 놀이터 프리셋이 있다.
계약과 측정이 함께 있으면 구현은 갈아 끼울 수 있는 것이 된다.

반대로 계약이 코드에만 있으면, 기반이 바뀔 때 무엇을 지켜야 하는지가 아무에게도 남아 있지 않다.
지켜야 할 성질이 있다면 문장으로 적고, 그 문장을 검사하는 테스트를 같이 두는 것이 순서다.

---

[^andy12_]: <https://news.ycombinator.com/item?id=49785339>

[^hbarka]: <https://news.ycombinator.com/item?id=49784983>

[^prodigycorp]: <https://news.ycombinator.com/item?id=49788533>

[^nico]: <https://news.ycombinator.com/item?id=49789123>

[^khazhoux]: <https://news.ycombinator.com/item?id=49790462>

[^raahelb]: <https://news.ycombinator.com/item?id=49784439>
