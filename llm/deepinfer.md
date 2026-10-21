# DeepInfer: DeepSeek이 프로덕션 추론 엔진의 반쪽을 공개했다

<https://github.com/deepseek-ai/DeepInfer>

HN 토론: <https://news.ycombinator.com/item?id=50163277> (2142점, 835개 댓글)

GN 토론: <https://news.hada.io/topic?id=35703>

## 소개

DeepInfer는 DeepSeek이 대규모 프로덕션 서비스를 돌리는 추론 프레임워크라고
소개하는 저장소다.
2026년 10월 16일에 만들어졌고 Apache-2.0이며,
이 문서를 쓴 시점에 별이 약 1만 3천 개다.
커밋은 3개뿐이라서 개발 이력이 아니라 한 시점의 스냅샷을 올린 것으로 보인다.
이 판단은 이 문서의 추측이다.

공개된 범위는 좁다.
지원 모델은 DeepSeek-V4.1-Flash 하나이고
하드웨어는 NVIDIA SM100 GPU와 Huawei Ascend 950 NPU다.
README는 완전한 추론 서비스에 필요하지만 이번에 포함하지 않은 것을 직접 적는다.
KV cache 시스템,
VE/Prefill/Decode 분리 배치(필요한 엔진 기능은 대부분 구현되어 있다고 한다),
그리고 prefill과 decode 양쪽의 데이터 병렬 복제본 사이 부하 분산이다.
그래서 이 저장소로 되는 것은 오프라인 추론이고, 온라인 서빙 스택은 아니다.

저장소와 함께 `doc/inference_deployment_qa.md`가 공개됐다.
이 문서는
DeepSeek V4.1 Flash 추론 시스템의 전체 구조를 질문과 답 형식으로 설명하고,
저장소에 없는 KV cache와 부하 분산 부분의 설계를 글로 보충한다.[^qa]

## 공개된 기능

| 기능                      | 설명                                                                |
| ------------------------- | ------------------------------------------------------------------- |
| 최적화된 커널             | FlashMLA, DeepGEMM, DeepEP, TileKernels, DeepSelect와 TileLang 커널 |
| 병렬화                    | Attention DP와 균형 CP, MoE EP와 EPLB                               |
| DSpark와 신뢰도 기반 검증 | draft token의 검증량을 신뢰도 추정으로 스케줄링                     |
| SWA bounded replay        | prefill에서 SWA 창의 일부만 다시 계산                               |
| 비동기 스케줄링           | CPU의 배치 스케줄링을 장치 실행과 겹침                              |
| batch-invariant 추론      | 배치 구성이 달라도 결과가 같음(NVIDIA만)                            |
| 결정적 샘플링             | 같은 입력 token과 매개변수면 같은 출력(NVIDIA만)                    |
| 구조화 출력               | 정규식, JSON 스키마, EBNF 문법으로 생성을 제한                      |

설정은 대부분 환경 변수다.
DSpark의 가변 길이 검증은 `DEEPINFER_ENABLE_MTP_VARLEN=1`로 켜고,
draft의 최대 길이는 `DEEPINFER_USE_NEXTN_DECODE`가 정하며 기본값은 5다.
decoder SWA bounded replay는 `DEEPINFER_YOCO_PREFILL_TRUNCATION_MODE=compact`와
`DEEPINFER_YOCO_PREFILL_KEEP_TOKENS=140`이 V4.1의 기본 설정이다.
batch-invariant 추론은 `DEEPINFER_BATCH_INVARIANT=1`이고,
결정적 샘플링은 여기에
`DEEPINFER_ENABLE_MTP_VARLEN=0`과 고정된 `seq_seed`를 더한다.

## 실행하기

사전 조건은 Linux, GCC 13 이상, Python 3.12이고,
NVIDIA는 CUDA 13, Ascend는 CANN 9.2가 필요하다.
빌드는 빈 Python 3.12 환경에서 하며,
가속기 종류를 환경 변수로 정하고 `build.sh`를 돌린다.
저장소는 DeepEP, DeepGEMM, FlashMLA,
DeepSelect와 Ascend용 두 개를 서브모듈로 가져온다.
의존성은 정확한 버전으로 고정되어 있다. NVIDIA는 torch 2.13.0+cu132,
flash-attn-4 4.0.0b34, tilelang 0.1.15, xgrammar 0.2.2 등이다.

```bash
# NVIDIA에서 빌드하고 오프라인 추론을 돌린다. Ascend는 ascend로 바꾼다.
export DEEPINFER_ACCELERATOR=nvidia   # 실행하는 환경에서도 계속 export해 둔다
./build.sh

# 기본 체크포인트(deepseek-ai/DeepSeek-V4.1-Flash-1017)를 처음 실행할 때 받는다
python examples/offline_inference.py

# 병렬 구성 예
python examples/offline_inference.py --ep 8
python examples/offline_inference.py --ep 2 --dp 8
python examples/offline_inference.py --ep 2 --cp 8
```

로컬 사본이 있으면 `DEEPINFER_HF_MODEL_DIR`로 지정한다.
`--check_structured_output`을 주면 같은 인스턴스로 정규식, JSON,
EBNF 구조화 출력 검사와 정상 종료 검사를 이어서 돈다.[^examples]
정밀도 기준선(PPL)은 `tests/models/offline_decode_ppl.json`에
플랫폼과 작업 부하별로 저장되어 있고,
검증은 샘플 단위로 정확히 비교한다.[^examples]

## 성능 수치를 읽는 법

README의 성능 그림은 두 장이다.
둘 다 그림 안에 조건이 적혀 있어서 그것을 같이 읽어야 한다.

| 그림    | 조건                                                                  | 읽은 값(그림에서 눈으로 읽은 근사)                                                                                     |
| ------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| prefill | EP4DP4, 전문가 384+32, 문맥 131,072, decoder bounded replay 140 token | 배치 4,096 token이면 GPU당 약 6만 token/s에 약 68ms, 65,536이면 약 8만 9천 token/s에 약 730ms                          |
| decode  | EP64DP64, 전문가 384+64, 문맥 131,072, nextn 3, token당 수락률 75%    | 랭크당 요청 64개면 GPU당 약 1만 5천 7백 token/s에 사용자당 약 246 token/s, 256개면 약 2만 6천 token/s에 약 103 token/s |

여기서 알아 둘 것이 세 가지다.
첫째, decode 그림은 수락률 75%(평균 수락 길이 3.25)를 가정해 곡선을 그린 것이다.
예제 문서도 `run_sweep.sh decode`가 수락률을 인자로 받아 그림을 그린다고
설명하고,
`benchmark.py`의 decode throughput은 요청이 매 단계 1 + nextn개를 받는다고
가정한 계산이라고 밝힌다.[^examples]
그러므로 이 숫자는 실제 서비스의 수락률로 잰 값이 아니라 가정이 들어간 환산이다.

둘째, 그림의 점은 모두 한 확장 도메인(scale-up domain) 안에서
prefill 4개, decode 64개 GPU로 잰 것이다.
셋째, 그림의 숫자는 이 문서가 눈으로 읽은 근사이고
정확한 값은 `results.jsonl`을 직접 돌려 얻어야 한다.
README는 재현 스크립트로 `examples/sweep/run_sweep.sh`를 가리킨다.

## 배포 Q&A가 알려 주는 운영 구조

저장소의 코드는 오프라인 추론이지만 Q&A 문서는
DeepSeek이 이 엔진을 어떻게 돌리는지 설명한다.
핵심 수치를 옮기면 이렇다.[^qa]

| 항목           | 문서가 밝힌 내용                                                                                                |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| 목표           | 여러 벤더의 가속기, 범용 하드웨어 위의 prefill과 decode 분리, 72시간 넘는 KV cache 보존                         |
| 규모           | 한 클러스터가 하루 155조 token을 처리하고 카드당 시간당 매출 38달러(한가한 시간대 요금 기준)                    |
| prefill        | 8-GPU 일반 서버, EP2~8 / DP2~8, HBM이 허용하는 가장 작은 값                                                     |
| decode         | 64~128 GPU 슈퍼노드, EP64~128 / DP64~128(Wide-EP)                                                               |
| 최소 배포 단위 | prefill 64 GPU와 decode 64 GPU. P와 D의 GPU 비율은 대략 1대 1                                                   |
| KV cache 저장  | 전용 3FS 스토리지 클러스터, 서버당 30.73TB SSD 20개, GPU당 논리 용량 약 14.4TB, TTL은 agent 3일, 챗봇 7일       |
| EPLB 설정      | prefill은 GPU당 중복 전문가 4개에서 시작해 `moe_lb`(가장 느린 랭크 / 평균) 1.074, decode는 1개에서 시작해 1.090 |
| 저정밀도       | main KV는 FP4(per-16, e4m3), indexer KV와 MoE 전문가 가중치는 MXFP4                                             |

구조화 출력은 컴파일과 추론을 분리한다.
문법 자동자를 전용 머신에서 비동기로 컴파일하고,
요청은 엔진에 들어가기 전에 컴파일 결과를 받는다.
각 decode 단계에서는
자동자를 진행시켜 허용되는 token의 마스크를 만들어 샘플링에 적용한다.[^qa]

비동기 스케줄링은 한 단계의 schedule과 post-process
동안 GPU가 노는 시간을 없애려는 것이다.
GPU가 `forward(N)`과 `sample(N)`을 도는 동안 CPU가 `schedule(N+1)`을 하고
`post-process(N-1)`을 이어서 한다.
DSpark와 같이 쓸 때는 신뢰도가 아직 돌아오기 전에 `schedule(N+1)`이 돌아서,
CPU는 전체 예산만 정하고 요청별 길이는 GPU의 TileLang 커널이 다시 계산한다.[^qa]

## 평가 결과

`eval/`은 AIME 2026, HLE, GPQA Diamond의 오프라인 배치 평가를 제공한다.
생성과 채점을 분리해서 채점만 다른 judge로 다시 돌릴 수 있다.
지표는 Pass@1이고 AIME는 문제 30개에 32회,
GPQA Diamond는 198개에 8회, HLE는 2,500개에 1회 표집한다.

README가 밝힌 기준 결과는 AIME 2026 99.9%,
GPQA Diamond 93.4%, HLE-Full 42.6%다.[^eval]
채점의 기본은 LLM judge이고 `deepseek-v4-flash`를 판정 모델로 쓴다.
AIME와 GPQA는 규칙 기반 채점도 되며,
AIME 2026에서는 두 방식이 960개 전부에서 일치했다고 한다.
HLE는 정답의 절반 넘게 자유 서술이라 규칙 채점을 거부한다.[^eval]
이 수치는 문서 스스로 근사치이고
배포가 제대로 설정됐는지 확인하는 용도라고 밝힌다.[^eval]

## 비평

### 공개한 것은 성능의 원인 가운데 일부다

README가 말하는 요소 중 이 저장소만으로 되는 것은 커널과 엔진과 샘플러다.
Q&A가 설명하는 성능의 큰 부분, 곧 72시간 넘는 KV cache 보존,
3FS 전용 스토리지, 네 종류의 부하 분산기는 코드가 없다.[^qa]
HN의 `_aavaa_`는 KV cache 시스템이 빠졌다고 짚었고,[^aavaa]
rektlessness는 H100 열두 장을 가진 사람이 복제해
프로덕션 서비스를 띄울 수 있게 되기 전까지는
Anthropic과 OpenAI가 잘 지낼 것이라고 했다.[^rektlessness]
반면 cmrdporcupine은 누구나 vLLM으로 이미 이 모델을 서빙하고 있고,
이 저장소의 가치는 vLLM과 SGLang 기여자에게 DeepSeek이 고생해서
얻은 서빙 기법의 참조 구현을 주는 데 있다고 답했다.[^cmrdporcupine]
swiftcoder는 제공자마다 자체 추론 엔진을 만들었으므로
이 공개가 공통 최적화를 채택하게 도울 것이라고 했다.[^swiftcoder]

두 읽기는 모순되지 않는다.
복제 가능한 서비스를 기대하면 부족하고, 참조 구현으로 보면 가치가 있다.
Q&A도 KV cache와 부하 분산이 내부 인프라와 강하게 묶여 있어서
아직 전부 공개하지 못한다고 밝힌다.[^qa]

### 공개된 커널이 내부 버전과 같지 않다고 스스로 적었다

Q&A는 내부의 kernel 라이브러리가 공개판과 대체로 같지만
indexer와 mega 계열은 조금 다르다고 한다.
FlashMLA에는 손으로 튜닝한 SASS 최적화
하나가 빠져 있어 decode 커널이 5~10% 느리고,
종단 간 성능은 최대 5% 차이라고 한다.
draft 모델도 내부 것이 조금 더 새롭지만 성능 차이는 작다고 한다.[^qa]
README의 숫자를 프로덕션 숫자와 같다고 읽으면 안 된다는 단서다.
차이가 작다는 말 자체도 내부 측정이어서 독립적으로 확인할 수 없다.

### 하루 155조 token과 카드당 38달러는 정의가 없다

가장 많이 인용된 수치가 Q&A의 첫머리에 나온다.
한 클러스터가 하루 155조 token을 처리하고
매출이 카드당 시간당 38달러(한가한 시간대 요금)라는 것이다.[^qa]
HN의 schneehertz는 이를 핵폭탄이라고 불렀고,[^schneehertz]
abound는 GPU 데이터센터의 감가상각을 포함한 소유
비용이 카드당 시간당 38달러보다 훨씬 낮을 것이므로
적자 사업이라는 논쟁이 줄기를 바랐다.[^abound]

그러나 이 수치는 해석에 필요한 것이 빠져 있다.
이 문서가 계산하면 하루 155조는 초당 약 18억 token이다.
decode 그림의 GPU당 약 1만 5천 token/s를 그대로 곱하면
출력 token만으로 11만 개가 넘는 GPU가 필요해서,
한 클러스터라는 말과 맞지 않는다.
그러니
155조에는 입력과 캐시 적중 token이 많이 섞여
있을 가능성이 크다. 이는 이 문서의 추정이다.
HN의 carstonh도 OpenRouter가 지난주 플랫폼
전체 사용량을 164조 token으로 보고하는데
한 클러스터가 그것을 하루에 소화할 수 있겠느냐며
단위가 다른 것 아니냐고 물었다.[^carstonh]
매출 38달러도 xrisk가 H100 대여가 시간당 약 2.75달러라고
비교했듯 비교 대상이 불분명하다.
어떤 카드인지, 입력과 출력 token을 어떻게 세는지,
가동률은 얼마인지는 문서에 없다.[^xrisk]
38달러는 순이익이 아니라 매출이다.

### 기술 보고가 아니라 한 기업의 운영 자료다

Q&A의 표는 DSpark의 가변 길이 검증이 고정 5개보다 4~7% 낫다고 쓴다.
이 문서가 표를 다시 계산해 보니
랭크당 동시 요청이 60개일 때 +5.4%, 72개일 때 +6.7%로 맞다.
그런데 같은 표에서 16개일 때는 −1.5%이고 96개일 때는 +11.0%다.
4~7%는 운영 지점의 값이고, 부하가 낮으면 오히려 손해다.
검증 길이가 평균 5에서 3.2~4.4로 줄고
평균 수락 길이는 거의 같다는 설명도 표와 맞지만,
수락 길이는 3.29에서 3.20으로 조금 줄었다.[^qa]
데이터는 EP64/DP64 벤치마크이고 제3자 재현은 아직 없다.

## 인사이트

### 추론 엔진의 해자는 코드가 아니라 그 옆의 인프라다

저장소에 없는 것의 목록이 DeepSeek이 어디에 가치를 두는지 말해 준다.
KV cache를 72시간 넘게 두는 전용 스토리지,
모든 prefill 서버가 어떤 접두어든 적중시키게 하는 구조,
4단계로 나눈 길이 구간별 prefill 부하 분산,
요청 수와 KV 길이를 동시에 맞추는 decode 분산이 그것이다.[^qa]
이것들은 엔진 코드가 아니라 클러스터 설계이고,
코드로 공개해도 데이터센터와 SSD 수십 PB가 없으면 쓸 수 없다.

이 때문에 오픈소스가 곧 복제 가능성이 아닌 구도가 된다.
HN의 draxen은 OpenRouter에서
Together.ai와 Baseten 같은 제공자가 DeepSeek 자신의 서비스보다
처리량과 지연이 더 좋다고 지적했다.[^draxen]
이 비교에는 반론이 있다. 사용자 쏠림 때문이라는
설명과 더 좋은 칩 때문이라는 설명이 나왔다.
어느 쪽이든 모델을 가진 쪽이 추론 성능에서
이기는 것이 자동은 아니라는 점은 같다.
모델 가중치와 엔진이 모두 열렸을 때 남는 차별화는 운영 규모와 캐시 적중률이다.

### 추론 비용의 중심이 계산에서 재사용으로 옮겨 간다

Q&A의 설계는 계산을 줄이는 것보다 이미 한 계산을 다시 쓰는 데 많은 부분을 쓴다.
72시간 이상의 보존, 적중 길이를 블록 KV cache가 정하고
SWA가 없으면 한 블록 물러나 다시 계산하는 규칙,
SWA bounded replay로 재계산을 문맥 길이와 무관한 상수로 줄이는 것이 그렇다.[^qa]
decoder 쪽 replay는 prefill 계산을 거의 절반으로 줄인다고 한다.

이 구도에서 비용은 GPU 시간이 아니라 저장 용량과 적중률에 걸린다.
Q&A는 챗봇 트래픽에서 TTL을 3일로 줄이면 적중률이 0.5~1% 떨어진다고 적는다.[^qa]
저장 비용과 계산 비용 사이의 이 교환은
에이전트 같은 긴 문맥 반복 호출에 특히 유리하다.
다만 Q&A는 이 교환이 손익분기를 넘는 조건을 숫자로 주지 않는다.

### 하드웨어 이식성이 수사가 아니라 코드 구조에 들어 있다

저장소에는 `vendor/`에 Ascend용 DeepEP와 DeepGEMM이 있고,
`requirements-ascend.txt`가 따로 있으며,
`deepinfer/npu_ops/`와 `csrc/asc_utils.cpp`가 있다.
README는 batch-invariant 추론과 결정적 샘플링이 NVIDIA 전용이라고 적어
Ascend에서 되는 것과 안 되는 것을 구분한다.
HN의 yaoke259는 이것이 하드웨어 시장에 큰 의미라고 했고,[^yaoke259]
seamossfet은 사람들이 화웨이 하드웨어를 쓰지 않는 주된 이유는 규제이므로
NVIDIA의 지위는 바뀌지 않는다고 했다.[^seamossfet]

이 둘의 차이를 가르는 것은 성능이 아니라 접근성이다.
코드가 있어도 칩을 살 수 없으면 쓸 수 없다.
이 저장소가 시험해 줄 첫 질문은 Ascend 경로가
NVIDIA 경로와 같은 수준으로 유지되느냐이고,
기능 표에서 두 하드웨어가 이미 갈라진 점이 그 답을 일부 알려 준다.

### 재현 가능성은 결정적 샘플링과 배치 불변성에서 시작된다

배치 구성이 달라져도 결과가 같고 같은 입력과 시드면
출력이 같다는 두 기능은 눈에 띄지 않지만
이 저장소에서 가장 검증 가능한 부분이다.
`tests/models/offline_decode_ppl.json`의 PPL 기준선을 샘플
단위로 정확히 비교하는 검증이 이를 뒷받침한다.[^examples]
서비스의 성능을 외부에서 재현하기 어려워도,
같은 입력이면 같은 출력이라는 성질은 외부에서 확인할 수 있다.
다른 엔진과 비교하거나 수치 변경을 추적할 때 이 성질이 기준점이 된다.
단 NVIDIA에서만 지원되고, 가변 길이 검증을 꺼야 한다는 조건이 붙는다.

---

[^qa]: GitHub, [DeepSeek V4.1 Flash Inference Deployment Q&A](https://github.com/deepseek-ai/DeepInfer/blob/main/doc/inference_deployment_qa.md)

[^examples]: GitHub, [DeepInfer examples](https://github.com/deepseek-ai/DeepInfer/blob/main/examples/README.md)

[^eval]: GitHub, [DeepInfer Benchmark evaluation](https://github.com/deepseek-ai/DeepInfer/blob/main/eval/README.md)

[^schneehertz]: <https://news.ycombinator.com/item?id=50163494>

[^abound]: <https://news.ycombinator.com/item?id=50163753>

[^carstonh]: <https://news.ycombinator.com/item?id=50170781>

[^xrisk]: <https://news.ycombinator.com/item?id=50164052>

[^aavaa]: <https://news.ycombinator.com/item?id=50163850>

[^rektlessness]: <https://news.ycombinator.com/item?id=50164217>

[^cmrdporcupine]: <https://news.ycombinator.com/item?id=50168151>

[^swiftcoder]: <https://news.ycombinator.com/item?id=50164223>

[^draxen]: <https://news.ycombinator.com/item?id=50165101>

[^seamossfet]: <https://news.ycombinator.com/item?id=50166097>

[^yaoke259]: <https://news.ycombinator.com/item?id=50164502>
