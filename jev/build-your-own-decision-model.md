# 의사결정 모델 직접 만들기: 선택지 토큰만 남기고 온도로 보정하기

원문: [Build your own decision model](https://nishtahir.com/build-your-own-decision-model/)

HN 토론: <https://news.ycombinator.com/item?id=50037949> (465점, 104개 댓글)

GN 토론: <https://news.hada.io/topic?id=35145>

## 소개

Nish Tahir가 2026년 10월 10일에 쓴 글로,
Jev 같은 “System One” 의사결정 모델이 하는 일을 작은 오픈 모델로 직접 흉내 내는
방법을 보여 준다.
의사결정 모델은 허용된 답 각각에 보정된 확률을 붙여 내놓는 모델이다.
글은 이 정의를 두 단계로 나눈다.
첫째는 출력을 고정된 선택지 안으로 가두는 일이고,
둘째는 그렇게 얻은 확률을 실제 정답률과 맞추는 보정(calibration)이다.

글이 약속하는 범위는 분명하다.
출력을 선택지 토큰으로 제한하면 모델은 그 밖의 답을 낼 수 없지만,
그것이 답이 맞다는 보장은 아니다.
그리고 추가 학습 없이 읽은 토큰 확률은 “다음 토큰이 무엇일지”에 대한 확신이지
“이 답이 맞을 확률”이 아니다.
글의 나머지는 이 두 번째 간극을 온도 스케일링(temperature scaling)으로 좁히는
과정이다.
저자는 데이터셋 구성, 평가, 미세 조정, 보정을 단계별 스크립트로 묶은
`nishtahir/build-your-own-jev` 저장소도 함께 공개했다.

## 동작 방식

### 생성은 토큰마다 한 번, 결정은 한 번이다

구조화 출력으로 JSON을 받는 일반 언어 모델은
프롬프트를 한 번에 프리필(prefill)한 뒤에도
출력 토큰마다 한 번씩 순전파를 해야 한다.
글의 예시에서는 최종 JSON을 만들기까지 11번이 필요하다.
의사결정 모델은 선택지가 고정되어 있다고 가정하므로,
프리필이 끝난 마지막 위치에서 한 번만 다음 토큰 분포를 읽으면 된다.

순서대로 보면 이렇다.
질문과 선택지 A~E를 프롬프트로 만들고 채팅 템플릿을 씌운다.
모델에 한 번 통과시켜 마지막 위치의 로짓(logit)을 얻는다.
어휘 전체 중 `A`, `B`, `C`, `D`, `E` 다섯 토큰의 로짓만 남기고 나머지는
버린다.
남은 다섯 값에 소프트맥스를 씌우면 선택지별 확률이 되고,
가장 큰 값이 예측이다.

### 마스킹은 형식을 보장하고 정답은 보장하지 않는다

다섯 토큰 밖의 확률을 버리는 것은 생성 시 다른 토큰을 금지하는 마스킹과 같은
효과다.
그래서 모델은 거절, 엉뚱한 설명, 형식 오류를 낼 수 없다.
대신 원래 분포에서 모델이 다른 토큰을 더 원했다는 정보도 함께 사라진다.
다섯 선택지 모두 마음에 들지 않아도 그중 하나에 확률을 몰아주게 된다.

### 원시 확률은 과신한다

저자는 CommonsenseQA 홀드아웃에서 모델의 확신 구간별 정확도를 쟀다.
0.9~1.0 구간에 809개가 몰렸는데 실제 정확도는 0.70이었고,
0.8~0.9 구간은 정확도가 0.47에 그쳤다.
“박쥐를 가장 찾기 쉬운 곳”처럼 동굴, 야구장, 다락이 모두 말이 되는 질문에도
동굴에 0.998을 준다.

온도 스케일링은 모든 로짓을 하나의 값 T로 나눈 뒤 소프트맥스를 씌운다.
T가 1보다 크면 분포가 평평해지고, 예측 순위는 바뀌지 않는다.
저자가 맞춘 값은 T≈3.797이었고,
보정 후에는 0.9~1.0 구간의 확신 0.93에 정확도 0.95,
0.4~0.5 구간의 확신 0.45에 정확도 0.51처럼 확신과 정확도가 가까워졌다.

## 구현하기

### 선택지 확률 읽기

아래 스크립트는 글의 방식을 그대로 따르되,
보정을 따로 할 수 있도록 확률이 아니라 선택지 로짓을 저장한다.
CommonsenseQA의 `validation` 분할을 Hugging Face `datasets`로 받아서
문항마다 다섯 로짓과 정답을 JSONL로 남긴다.

```python
# score.py — pip install torch transformers datasets accelerate
import argparse
import json

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

OPTIONS = ["A", "B", "C", "D", "E"]

parser = argparse.ArgumentParser()
parser.add_argument("--model", default="Qwen/Qwen3-1.7B")
parser.add_argument("--out", default="scores.jsonl")
parser.add_argument("--limit", type=int, default=0)
args = parser.parse_args()

tok = AutoTokenizer.from_pretrained(args.model)
model = AutoModelForCausalLM.from_pretrained(
    args.model, torch_dtype="auto", device_map="auto"
)
model.eval()

# 선택지마다 토큰이 정확히 하나여야 한다. 둘 이상이면 첫 토큰만 비교하게 되어
# 서로 다른 선택지가 같은 첫 토큰을 공유할 수 있다.
option_ids = []
for opt in OPTIONS:
    ids = tok.encode(opt, add_special_tokens=False)
    assert len(ids) == 1, f"{opt!r} is {len(ids)} tokens"
    option_ids.append(ids[0])
assert len(set(option_ids)) == len(OPTIONS)


def build_prompt(question, choices):
    lines = [question]
    lines += [f"{label}. {text}" for label, text in zip(OPTIONS, choices)]
    lines.append("Answer with a single letter.")
    messages = [{"role": "user", "content": "\n".join(lines)}]
    # Qwen3의 사고 모드를 끈다. 켜 두면 첫 토큰이 <think>가 되어 선택지가 아니다.
    return tok.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )


data = load_dataset("tau/commonsense_qa", split="validation")
if args.limit:
    data = data.select(range(args.limit))

with open(args.out, "w") as out, torch.no_grad():
    for row in data:
        prompt = build_prompt(row["question"], row["choices"]["text"])
        inputs = tok(prompt, return_tensors="pt").to(model.device)
        last = model(**inputs).logits[0, -1]
        # 어휘 전체가 아니라 선택지 토큰의 로짓만 남긴다. 이것이 마스킹이다.
        logits = last[option_ids].float().tolist()
        label = OPTIONS.index(row["answerKey"])
        out.write(json.dumps({"logits": logits, "label": label}) + "\n")
```

### 보정하고 검증하기

보정은 로짓 파일만 있으면 모델 없이 할 수 있다.
아래 스크립트는 문항을 무작위로 반으로 나눠,
앞쪽 절반에서 T를 맞추고 뒤쪽 절반에서만 구간표와 ECE(expected calibration
error)를 보고한다.
T는 정확도 곡선이 아니라 음의 로그 우도(NLL)를 최소화해서 구한다.
온도 스케일링의 표준 방식이고, 목적 함수가 볼록이라 결과가 안정적이다.

```python
# calibrate.py — python calibrate.py scores.jsonl
import json
import sys

import torch

rows = [json.loads(line) for line in open(sys.argv[1])]
logits = torch.tensor([r["logits"] for r in rows])
labels = torch.tensor([r["label"] for r in rows])

# T를 맞추는 데 쓴 문항으로 보정 결과를 평가하면 테스트 셋에 과적합한 숫자가 된다.
gen = torch.Generator().manual_seed(0)
perm = torch.randperm(len(rows), generator=gen)
half = len(rows) // 2
fit_idx, test_idx = perm[:half], perm[half:]


def fit_temperature(z, y):
    # T > 0을 보장하려고 log T를 최적화한다.
    log_t = torch.zeros(1, requires_grad=True)
    opt = torch.optim.LBFGS([log_t], lr=0.1, max_iter=200)
    nll = torch.nn.CrossEntropyLoss()

    def closure():
        opt.zero_grad()
        loss = nll(z / log_t.exp(), y)
        loss.backward()
        return loss

    opt.step(closure)
    return log_t.exp().item()


def report(z, y, t, bins=10):
    probs = torch.softmax(z / t, dim=-1)
    conf, pred = probs.max(dim=-1)
    correct = (pred == y).float()
    ece = 0.0
    print(f"T={t:.3f} accuracy={correct.mean():.4f}")
    print("bin           count  confidence  accuracy")
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        mask = (conf > lo) & (conf <= hi)
        n = int(mask.sum())
        if n == 0:
            continue
        c, a = conf[mask].mean().item(), correct[mask].mean().item()
        ece += n / len(y) * abs(c - a)
        print(f"({lo:.1f}, {hi:.1f}]  {n:6d}  {c:10.4f}  {a:8.4f}")
    print(f"ECE={ece:.4f}\n")


t = fit_temperature(logits[fit_idx], labels[fit_idx])
report(logits[test_idx], labels[test_idx], 1.0)
report(logits[test_idx], labels[test_idx], t)
```

실행 순서는 두 줄이다.

```bash
python score.py --model Qwen/Qwen3-1.7B --out scores.jsonl
python calibrate.py scores.jsonl
```

`--limit 50`으로 먼저 돌려 선택지 토큰 단언문이 통과하는지,
예측이 한 글자에 쏠리지 않는지 확인한 다음 전체를 돌리는 편이 안전하다.

## 값 정하기

| 값          | 시작값               | 근거                                                      | 무엇을 재서 바꿀지                      |
| ----------- | -------------------- | --------------------------------------------------------- | --------------------------------------- |
| 기반 모델   | Qwen3-1.7B           | 원문이 쓴 크기, 노트북 GPU에서도 한 번 통과가 빠르다      | 같은 문항에서 정확도와 지연 시간        |
| 선택지 표기 | `A`~`E` 한 글자      | 대부분의 토크나이저에서 한 토큰이고 첫 토큰이 겹치지 않음 | 단언문 통과 여부, 위치별 예측 분포      |
| 보정 분할   | 문항의 절반          | T 하나만 맞추면 되므로 수백 문항이면 충분하다             | 분할 시드를 바꿨을 때 T의 흔들림        |
| 온도 T      | NLL 최소화로 구한 값 | 원문은 약 3.8, 모델과 프롬프트가 바뀌면 다시 맞춰야 함    | 테스트 분할의 ECE와 구간표              |
| 구간 수     | 10                   | 원문 표와 같은 해상도, 표본이 적으면 빈 구간이 생김       | 구간당 표본 수가 30개 아래로 떨어지는지 |

## 트레이드오프

### 한 번의 순전파는 생각할 시간을 버린 대가다

선택지 토큰 하나만 읽으면 지연 시간과 비용이 크게 줄지만,
모델이 답하기 전에 추론할 기회도 사라진다.
HN의 kombinatori는 토큰 마스킹이 비용을 줄이는 만큼 쓸 수 있는 연산량도 줄여
정확도를 제한한다고 지적했다.[^kombinatori]
글의 결과도 이를 보여 준다.
1.7B 모델은 CommonsenseQA에서 59.4%였고,
미세 조정 후에도 62.4%에 그쳤다.

그렇다고 사고 모드를 켜고 마지막에 선택지를 읽는 것은 해법이 아니다.
그러면 생성 비용이 돌아오고,
의사결정 모델을 쓰는 이유인 속도와 단순함이 사라진다.
결국 고를 수 있는 것은 같은 지연 시간 안에서 더 큰 모델을 쓰거나,
과제별 데이터로 미세 조정하는 쪽이다.

### 기존 LLM 위에 얹으면 출력 헤드를 새로 학습할 수 없다

이 글의 방법은 기존 언어 모델의 다음 토큰 분포를 빌린다.
2bitencryption은 Jev에서 영감을 받은 최근 의사결정 모델들이 기성 모델에 토큰
마스크를 씌운 것이 아니라 구조부터 다르다고 생각했다고 물었고,[^2bitencryption]
Tostino는 트랜스포머에 새 출력 헤드를 다는 정도는 연구소라면 당연히 할 줄
안다고 답했다.[^Tostino]
make3는 Laya가 ModernBERT-Large를 미세 조정한 것일 뿐이라며,
“의사결정 모델”이라는 신비주의 대신
양방향 언어 모델이라고 부르자고 했다.[^make3]

글의 방식은 어휘의 기존 토큰을 출력 클래스로 재활용하므로 학습 없이 바로 쓸
수 있다.
대신 선택지 수가 늘거나 선택지가 의미 있는 이름이 되면,
한 토큰짜리 표기로 바꾸는 과정에서 정보가 줄어든다.
전용 헤드를 붙이면 이 제약이 사라지지만,
그때부터는 학습 데이터와 학습 비용이 필요하다.

### 범용 영점(zero-shot) 결정과 전용 분류기 사이

nico는 과제가 고정되는 순간 전용 분류기가 더 효율적이라고 했다.
banking77에서 로컬 분류기로 94% 이상이 나오고,
이메일 분류기는 50~100통으로 정확도 95%에 이를 수 있다는 것이다.[^nico]
howunfortunate는 오랫동안 분류기를 팔지 못한 ML 엔지니어로서 Jev 열풍에 속으로
비명을 지른다고 했고,
LLM으로 학습·평가 데이터를 만들어 하루 만에 분류기를 증류할 수 있다고
주장했다.[^howunfortunate]
jrmg는 그것이 결코 “간단”하지 않으며,
질문을 쓰면 바로 답이 나오는 Jev 쪽이 한 자릿수 이상 간단하다고 반박했다.[^jrmg]

글의 방법은 그 중간에 있다.
학습 없이 시작할 수 있고,
나중에 같은 파이프라인에서 미세 조정과 보정으로 넘어갈 수 있다.
jofzar의 말처럼 일단 넣어 보고 효과가 있으면 그때 사업 근거를 만드는 흐름이
가능해진다.[^jofzar]
하지만 영점 결정이 편하다는 이유로 측정을 건너뛰면,
전용 분류기가 공짜로 주던 평가 습관까지 잃는다.

## 함정

### 같은 데이터로 T를 맞추고 보고하면 보정이 아니라 과적합이다

원문은 앞서 평가한 결과에 온도를 맞추고 같은 구간표를 보고한다.
demibabs는 특정 벤치마크에서 보정된 것처럼 보이게 사후에 온도를 바꾸는 것이
p-해킹 같다고 물었고,[^demibabs]
shawntan은 학습·검증·테스트 분할을 나누는 이유가 바로 이것이며,
보고하는 결과를 보면서 시스템의 어느 부분이라도 조정했다면 테스트 셋에 과적합한
것이라고 답했다.[^shawntan]
위 `calibrate.py`가 문항을 반으로 나눈 이유다.

분할을 나눠도 남는 문제가 있다.
CommonsenseQA로 맞춘 T는 CommonsenseQA와 비슷한 분포에서만 의미가 있다.
실제로 쓸 과제의 라벨 데이터로 다시 맞추지 않으면,
보정된 확률은 다른 시험에서 받은 점수를 옮겨 온 것에 가깝다.
shawntan이 Jev의 보정된 확률을 두고 “무엇에 대해 보정했느냐”고 물은 것도 같은
지점이다.

### 온도 하나로는 순위가 바뀌지 않는다

온도 스케일링은 확신의 크기만 고치고 정확도는 그대로 둔다.
보정 전후 정확도가 같은 것이 정상이고,
정확도를 올리고 싶다면 미세 조정이나 더 큰 모델이 필요하다.
nl이 3.797이라는 값의 직관을 물었을 때 roger_가 Platt 스케일링을 가리킨 것도
이 방법이 출력 위에 얹는 사후 변환이기 때문이다.[^nl][^roger_]
글은 “곡선 맞춤”이라고만 적어 무엇을 최소화했는지 밝히지 않으므로,
재현할 때는 NLL처럼 목적 함수를 명시하는 편이 낫다.

### 정답이 하나가 아닌 문항은 과신을 측정하기 어렵다

박쥐 문항에 대해 utbabya는 맥락 없이 물으면 보통 사람도 동굴이라고 답할 것이니
과신이 아니라고 했다.[^utbabya]
_superposition_은 도메인이 정해져야 정답이 생긴다며,
스포츠용품 서비스라면 야구 쪽 답을 원할 것이라고 답했다.[^_superposition_]
즉 보정은 “어떤 사용자의 정답”에 대한 것이고,
벤치마크의 정답 키가 그 사용자와 다르면 보정된 확률도 그만큼 어긋난다.

### 선택지 표기와 위치가 답을 움직인다

`A`~`E` 표기는 토크나이저마다 공백이 붙은 토큰(` A`)과 붙지 않은 토큰(`A`)이
따로 있을 수 있다.
채팅 템플릿이 어시스턴트 차례를 어떻게 여는지에 따라 모델이 실제로 내려던 첫
토큰이 다를 수 있으니,
몇 문항을 정상 생성으로 돌려 첫 토큰을 눈으로 확인해야 한다.
또 다지선다 문항에서 언어 모델은 특정 위치의 글자를 선호하는 경향이 있다.
원문의 첫 평가에서 A, B의 재현율이 0.72, 0.77이고 D, E가 0.39, 0.43인 것도
그런 쏠림을 의심하게 한다.
선택지 순서를 섞어 다시 재 보면 확인할 수 있다.

### 브라우저 데모는 기기 메모리에 막힌다

글의 인터랙티브 예시는 브라우저에서 모델을 내려받아 돌린다.
kekebo는 iOS 26의 여러 브라우저에서 모델 다운로드가 끝나는 순간 페이지가 새로
고쳐져 상태가 초기화된다고 했고,[^kekebo]
enjoyyourlife는 iOS Safari의 메모리 한도가 400MB 미만이라 그럴 것이라고
답했다.[^enjoyyourlife]
같은 방식을 제품에 넣을 때도 모델 크기는 정확도만이 아니라 실행 환경의 메모리로
정해진다.

## 확인하기

1. `python score.py --limit 50`을 돌려 단언문이 통과하는지 본다.
2. `scores.jsonl`에서 예측 글자 분포를 세어 한 글자에 쏠리지 않았는지 본다.
3. `python calibrate.py scores.jsonl`의 첫 표(T=1)에서 높은 구간의 정확도가
   확신보다 낮은지, 즉 원문처럼 과신하는지 확인한다.
4. 두 번째 표에서 ECE가 줄었는지, 정확도는 그대로인지 확인한다.
5. 시드를 바꿔 `calibrate.py`를 몇 번 돌리고 T가 크게 흔들리지 않는지 본다.
6. 실제로 쓸 과제의 라벨 데이터 수백 개로 같은 과정을 반복해 T를 다시 맞춘다.

## 비평

### 글은 의사결정 모델을 만드는 법이 아니라 읽는 법을 보여 준다

제목은 “직접 만들기”지만,
글에서 새로 만드는 것은 모델이 아니라 기존 모델의 출력을 읽는 방식이다.
HN에서 bellajbadr가 고정된 JSON 출력을 얻는 이야기냐고 묻자 yawnxyz는 텍스트를
생성하지 않고 확률만 낸다고 답했는데,[^bellajbadr][^yawnxyz]
이 짧은 문답이 글의 범위를 정확히 요약한다.
firasd는 GPT-3 논문에서도 다지선다 문항을 특정 이어쓰기의 토큰 확률을 비교해
풀었다고 짚었다.[^firasd]
기법 자체는 오래됐고,
새로운 것은 그것을 if 문이나 switch 문 같은 API로 포장했다는 점이다.

이것이 글의 결함이라는 뜻은 아니다.
softwaredoug는 Jev의 진짜 의미가 Jev라는 회사가 아니라 이런 글들,
즉 수많은 Jev가 피어나게 하는 데 있다고 했다.[^softwaredoug]
다만 글이 미세 조정에서 얻은 개선을 3%포인트로 보고하고 넘어가면서,
그 차이가 의사결정 모델 전용 학습과 범용 모델 재활용 사이의 간격이라는 점은
말하지 않는다.

### 보정의 결과가 보정의 방법보다 크게 보인다

가장 인상적인 표는 보정 후의 구간표인데,
그 표가 어떤 데이터에서 나왔는지가 글에서 가장 불분명하다.
홀드아웃에서 잰 과신 표를 보여 준 뒤 같은 평가에 T를 맞췄다고 읽히고,
별도의 테스트 분할은 언급되지 않는다.
보정 표에서 0.9~1.0 구간의 정확도가 확신보다 높은 0.95로 뒤집힌 것도,
T를 고르면서 그 구간까지 함께 본 결과일 수 있다.

beamy는 전통적인 분류기를 만드는 일의 대부분이 실제 결정 대상 데이터에서
성능을 재고 개선하는 데 있는데,
Jev에서는 그것을 모두 건너뛰고 AI니까 정확하다는 마법적 사고가 있다고
했다.[^beamy]
이 글은 그 습관을 되살리는 방향에 서 있다.
그래서 자기 보정 결과에도 같은 엄격함을 적용하지 않은 점이 아쉽다.

### 확률을 노출하는 것이 언제나 장점은 아니다

글은 보정된 확률을 의사결정 모델의 정의로 삼는다.
bob1029는 정확한 확률이 필요 없다면 단순한 도구 호출 구성으로도 같은 이점을
얻을 수 있고,
행동 공간을 튜링 완전한 셸에서 다지선다로 줄이는 것이 핵심이라고 했다.
그리고 구체적인 확률을 아는 것 자체가 큰 정보 위험이라고 봤다.[^bob1029]
MisterMunchkin은 의사결정 모델이 유연한 이유가 무엇에든 답을 지어낼 수 있기
때문이라고 했고,
mbil은 그래도 얼마나 확신하는지는 말해 준다고 받았다.[^MisterMunchkin][^mbil]

이 두 견해 사이에서 글은 확률이 언제 도움이 되고 언제 오해를 낳는지 다루지
않는다.
보정된 0.8이 의미 있는 것은 그 확률로 임계값을 정하고 사람에게 넘길지 결정할
때다.
그렇지 않다면 확률은 정답처럼 보이는 숫자 하나를 더할 뿐이다.

## 기억할 원칙

### 확률을 내놓는 모델의 값은 보정 데이터에서 나온다

선택지 토큰만 남기는 데는 코드 몇 줄이면 충분하다.
그 확률을 믿을 수 있게 만드는 데는 실제 과제의 라벨 데이터와,
그 데이터를 맞추는 쪽과 보고하는 쪽으로 나누는 규율이 필요하다.
보정은 모델의 성질이 아니라 모델과 데이터 분포의 짝에 붙는 성질이다.

### 의사결정 모델은 측정을 생략할 핑계가 아니라 측정을 싸게 만드는 도구다

HN에서 소개된 사례들,
이메일을 폴더로 나누고(jrmg),
Claude Code 훅에서 위험한 명령을 거르고(UltraSane),
퀴즈 게임용 문단을 골라 토큰 사용을 10배 줄이는(xavortm) 일은 모두 빠르고 싼
판단이 필요한 자리다.[^jrmg][^UltraSane][^xavortm]
e12e가 jrmg에게 이메일 내용을 전부 외부 서비스에 보내는 것이냐고
물은 것처럼,[^e12e]
호스팅 모델을 쓸 때는 데이터가 어디로 가는지도 결정의 일부다.
이 글의 방법이 주는 가장 실용적인 이점은 그 판단을 로컬에서 돌리면서,
같은 파이프라인으로 정확도와 보정을 직접 잴 수 있다는 점이다.

---

[^kombinatori]: <https://news.ycombinator.com/item?id=50040438>

[^2bitencryption]: <https://news.ycombinator.com/item?id=50040363>

[^Tostino]: <https://news.ycombinator.com/item?id=50041226>

[^make3]: <https://news.ycombinator.com/item?id=50040121>

[^nico]: <https://news.ycombinator.com/item?id=50039100>

[^howunfortunate]: <https://news.ycombinator.com/item?id=50038233>

[^jrmg]: <https://news.ycombinator.com/item?id=50047615>

[^jofzar]: <https://news.ycombinator.com/item?id=50039098>

[^demibabs]: <https://news.ycombinator.com/item?id=50038450>

[^shawntan]: <https://news.ycombinator.com/item?id=50040410>

[^nl]: <https://news.ycombinator.com/item?id=50041818>

[^roger_]: <https://news.ycombinator.com/item?id=50042047>

[^utbabya]: <https://news.ycombinator.com/item?id=50042432>

[^_superposition_]: <https://news.ycombinator.com/item?id=50043915>

[^kekebo]: <https://news.ycombinator.com/item?id=50040215>

[^enjoyyourlife]: <https://news.ycombinator.com/item?id=50040226>

[^bellajbadr]: <https://news.ycombinator.com/item?id=50038144>

[^yawnxyz]: <https://news.ycombinator.com/item?id=50040171>

[^firasd]: <https://news.ycombinator.com/item?id=50038347>

[^softwaredoug]: <https://news.ycombinator.com/item?id=50043731>

[^beamy]: <https://news.ycombinator.com/item?id=50042243>

[^bob1029]: <https://news.ycombinator.com/item?id=50044064>

[^MisterMunchkin]: <https://news.ycombinator.com/item?id=50040795>

[^mbil]: <https://news.ycombinator.com/item?id=50041850>

[^UltraSane]: <https://news.ycombinator.com/item?id=50039223>

[^xavortm]: <https://news.ycombinator.com/item?id=50040366>

[^e12e]: <https://news.ycombinator.com/item?id=50056168>
