# TorchTPU: PyTorch 코드를 `device="tpu"` 한 줄로 TPU에 올리는 Google과 Meta의 네이티브 백엔드

<https://github.com/google-pytorch/torch_tpu>

HN 토론: <https://news.ycombinator.com/item?id=50169053> (273점, 64개 댓글)

GN 토론: <https://news.hada.io/topic?id=35728>

## 소개

TorchTPU는 Google Cloud TPU를 위한 오픈소스 PyTorch 백엔드다.
README는 PyTorch 모델과 연산을 TPU 장치에서 돌리게 해 주며
커스텀 ATen 커널, 컴파일 캐시, 분산 학습과 추론 예제를 포함한다고 설명한다.
문서 사이트는 이를 Google과 Meta의 PyTorch 팀이 협업해 만든 것이라고
소개한다.[^intro]
라이선스 파일은 Apache 2.0 전문이고 README도 같은 라이선스를 밝힌다.
GitHub의 라이선스 자동 감지는 이 파일의 앞머리에
붙은 한 줄 때문에 라이선스를 식별하지 못했다.
저장소는 2026년 3월 9일에 만들어졌고 이 글을 쓴 시점에 별은 346개, 언어는 C++다.

기존에는 PyTorch를 TPU에서 쓰려면 PyTorch/XLA 같은 다리를 거쳤다.
문서의 FAQ는 PyTorch/XLA가 JAX 런타임 구성 요소에 크게 의존한 다리였고
TorchTPU는 JAX 런타임 의존이 없는 네이티브 백엔드이며,
PyTorch/XLA는 폐기되고 TorchTPU로 대체된다고 적는다.
TorchAX(torch_xla2)는 파이썬 수준에서 연산을 가로채 XLA로 내리는 구현이며
TorchTPU가 새로운 공식 표준이라고 한다.
JAX를 대체하는 것은 아니고 기존 PyTorch 코드베이스가 다시 쓰지 않고
TPU로 오는 입구라는 설명이다.[^faq]

## 동작 방식

### 세 가지 즉시 실행 모드와 그래프 컴파일

문서에 따르면 TorchTPU는 PyTorch의 한 프로세스당 한 장치 실행 모델을 따르고
`torch.compile`을 Dynamo로 지원한다.
즉시 실행(eager)에는 세 모드가 있다.
기본인 Strict는 ATen 연산을 하나씩 비동기로 TPU에 보낸다.
Debug(`TORCH_TPU_LAUNCH_BLOCKING=1`)는 연산마다 동기로 실행하고
런타임 경계 검사를 켠다.
DeferAndFuse(`TORCH_TPU_DEFER_AND_FUSE=1`)는 `.cpu()`나 `.item()`
같은 구체화 지점까지 연산을 미루고 묶어서 HBM 트래픽을 줄인다.
그래프 모드는 `torch.compile(model)`이 “tpu” Dynamo 백엔드를 등록해
FX 그래프 전체를 StableHLO로 내리고 OpenXLA 컴파일러로 컴파일한다.[^intro]

### 컴파일 비용을 줄이는 캐시와 분산 프리미티브

반복되는 XLA 컴파일을 줄이려고 세 단계의 캐시를 둔다.
1단계는 프로세스 안의 메모리 캐시이고 항상 켜져 있다.
2단계는 다중 장치 작업에서 프로세스끼리 쓰는 호스트 로컬 공유 메모리이고,
3단계는 Cloud Storage 같은 지속적 원격 캐시로
호스트와 작업 재시작을 넘어 재사용한다.
분산은 `backend="tpu_dist"`로 `torch.distributed`의
프로세스 그룹에 TPU 집합 연산을 구현했고,
DDP, FSDP2와 SimpleFSDP, DTensor를 지원한다고 한다.
커스텀 커널은 Pallas, 실험적 Helion DSL, 미리 만든 Tokamax 커널로 쓴다.[^intro]

## 사용하기

TPU VM(예: v6e)에서 파이썬 3.12 환경을 만들고 패키지를 설치한다.
문서는 설치 순서가 PyTorch 디스패처와 TPU 드라이버를 맞추는 데 중요하다고
쓴다.[^vm]
README의 설치 예는 CPU용 torch를 받도록 추가 인덱스를 지정한다.
추가 인덱스를 빼면 CUDA 빌드의 torch가 설치된다는 경고가 붙어 있다.

```bash
python3.12 -m venv env
source env/bin/activate
pip install torch_tpu==0.2.0 --extra-index-url https://download.pytorch.org/whl/cpu
```

가장 작은 예는 문서의 소개 페이지에 있다.
장치 문자열만 `"tpu"`로 바꾸면 기존 연산이 그대로 돈다.

```python
import torch

device = torch.device("tpu")  # cuda 에서 tpu 로 바꾸는 한 줄
x = torch.randn((4, 4), device=device)
y = torch.ones((4, 4), device=device)
result = torch.matmul(x, y).cpu()  # TPU 결과를 CPU 로 가져온다
print(f"Executed on device: {x.device}")
print(f"Result shape on CPU: {result.shape}, sum: {result.sum():.4f}")
```

문서의 설명대로 GPU에서 옮기는 일은 `device="cuda"`를 `device="tpu"`로,
`backend="nccl"`을 `backend="tpu_dist"`로 바꾸는 데서 시작한다.[^intro]
즉시 실행 속도를 높이려면 환경 변수 `TORCH_TPU_DEFER_AND_FUSE=1`을 주고,
그래프 컴파일은 `torch.compile(model)`을 쓴다.
문서의 권고는 즉시 실행의 워밍업 시간과 컴파일 시간이
길 때 지속적 컴파일 캐시를 켜라는 것이다.[^intro]

## 지원 범위와 알려진 한계

문서가 구분한 검증 단계(Validated)와 실험 단계(Experimental)를 정리하면
이렇다.[^features]

| 영역     | 검증됨                                                      | 실험적                                             |
| -------- | ----------------------------------------------------------- | -------------------------------------------------- |
| TPU 세대 | v5e, v5p, v6e, v7                                           | 향후 v8i, v8t                                      |
| 모델     | Qwen, Llama, Muse Glimmer, Gemma, WAN, FLUX                 | CNN, Mamba, LSTM/GRU, DLRM, GLM, Kimi, DeepSeek 등 |
| 커널     | Pallas, Tokamax                                             | Helion                                             |
| 양자화   | 전체 텐서 FP8/FP4, 채널별 FP8                               | 블록 단위 FP8/FP4(향후)                            |
| 분산     | 최적 메시, SimpleFSDP, 체크포인트, 최대 8K 칩 다중 슬라이스 | FSDPv2와 MPMD(낮은 성능)                           |
| 통합     | Hugging Face, Ray, vLLM, SGLang, TorchTitan, TorchRec       | VeRL(향후)                                         |

연산 범위는 핵심 ATen 연산 450개(순전파와 역전파)이고
LLM, 비전, 오디오,
확산 파이프라인에 걸친 5,000개의 인기 Hugging Face 모델로 지속 검증한다고
한다.[^intro]
동적 형상은 아직 한계다.
`torch.compile`의 `dynamic`은 기본이 False이고,
문서의 예로 Hugging Face LLM의 디코드 단계는
경계가 있는 동적성(bounded dynamism)을 켜지 않으면
단계마다 재컴파일이 일어난다고 한다.
FlexAttention은 네이티브로 지원되지 않고,
현재 세대 TPU는 fp32보다 낮은 정밀도의 행렬곱 누적을 지원하지 않으며,
하나의 TPU 장치에는 한 프로세스만 접근할 수 있어서
같은 장치를 공유하는 RL 구성이 제한된다.
PyTorch의 기본 채널 우선 CNN 배치는 TPU에서
매우 비효율적이라는 항목도 있다.[^intro]

## 비평

### 한 줄이면 옮겨진다는 약속은 조건이 붙는다

소개 문구는 최소한의 코드 변경으로 기존 PyTorch 워크로드를 돌린다고 말한다.
같은 페이지가 이어서 적은 한계는 그 약속이 어디까지인지를 말해 준다.
돌아가는 것과 빠르게 돌아가는 것은 다르다.
동적 형상 때문에 디코드 단계마다 재컴파일이 일어나고,
FSDPv2와 MPMD는 기능은 되지만 성능이 낮으며,
CNN의 기본 배치는 TPU에서 비효율적이다.
이 문서가 읽은 소개와 기능 목록에는 GPU 대비 성능 수치가 없고
일반적인 가격 대비 성능 주장만 있다.
사례 연구(FLUX 최적화,
Muse Glimmer 30B 추론과 학습)가 문서에 있지만 이 문서는 열어 보지 않았다.
따라서 옮기는 비용이 코드 수정에서
끝나는지 성능 공학까지 이어지는지는 워크로드마다 직접 재야 한다.

### 접근성은 여전히 Google Cloud의 TPU에 묶인다

HN의 Lucasoato는 TPU를 Google Cloud 밖에서 쓸 수 있느냐고 물었고,
sschueller는 Coral USB와 M.2 장치가 TPU라고 답했다.[^Lucasoato][^sschueller]
boulos는 Google이 큰 고객에게 TPU를 현장 설치용으로 팔고
있다고 설명했다.[^boulos]
이 백엔드는 문서상 Google Cloud TPU를 대상으로 하며
최신 하드웨어를 쓰려면 GKE가 필요하다고 안내한다.[^vm]
코드가 오픈소스여도 실행할 하드웨어는 한 사업자의 클라우드에 있다.
PyTorch/XLA가 폐기되고
대체된다는 FAQ의 문장은 기존 XLA 사용자에게 이전 비용도 의미한다.[^faq]

### 로드맵은 약속이 아니라고 문서가 말한다

기능 문서는 앞으로의 작업이 커밋된 출시 일정이 아니며
커뮤니티의 피드백에 따라 특징과 일정과 구조가 바뀔 수 있다고 적는다.[^features]
다음 단계 목록에는 스트림, 그래프 캡처,
빠른 시작의 즉시 실행, 동적 연산의 재컴파일 제거,
FSDPv2와 MPMD의 성능, 8K 칩을 넘는 학습, RL과 사전학습 솔루션이 있다.
이 항목들은 현재 한계의 목록과 거의 겹친다.
따라서 도입 판단은 로드맵이 아니라 현재 검증 단계의 표에 근거해야 한다.

## 인사이트

### 하드웨어가 프레임워크의 문을 열어야 하는 시대가 되었다

PyTorch가 사용자의 기본 도구가 된 뒤 가속기는 PyTorch를 지원하지 않으면
선택지가 되기 어렵다.
HN의 fancyfredbot은 XLA가 inductor보다 더 나은
컴파일러 기반일 수 있어 모든 하드웨어의 성능을 높일 것이고
이것이 TensorFlow의 마지막 못이라고 썼다.[^fancyfredbot]
ismailmaj은 하드웨어 특이성이 커널 층(Pallas나 CUDA)에 있으니
이제 JAX와 PyTorch는 취향의 문제가 아닌가 하고 추측했다.[^ismailmaj]
Tanjreeve는 이것이 TPU를 Google 밖에 팔려는 노력으로
사람들이 TPU에 익숙해지게 하는 수라고 읽었다.[^Tanjreeve]
23agt는 Google이 클라우드 서비스와 일부 파트너에게의 직접 판매로 TPU 삽을 판다고
비유했고,[^23agt]
nelaggy는 해자가 모델도 추론 계층도 아니라면 하드웨어냐고 물었다.[^nelaggy]
이 반응들이 공통으로 짚는 구도는 해자가 소프트웨어
호환 계층을 얼마나 낮추느냐로 옮겨 간다는 것이다.
TorchTPU의 450개 ATen 연산 지원은 이 계층의 구체적인 크기를 보여 주는 숫자다.
이는 이 문서의 해석이다.

### 한 줄로 도는 것과 비용 효율적으로 도는 것 사이에 성능 공학이 남는다

`device="tpu"`로 즉시 돌아가는 것이 이식의 시작일 뿐이라는 점은 문서
자체의 표가 말해 준다.
동적 형상의 재컴파일, 컴파일 시간, 즉시 실행의 워밍업,
뷰 연산의 비용은 모두 TPU와 XLA의 메모리 모델에서 나온다.
문서가 권하는 처방은 지속적 컴파일 캐시와 경계가 있는 동적성,
SimpleFSDP와 `torch.compile`의 조합이다.
이는 GPU에서 쌓은 직관이 그대로 통하지 않는 영역이 있다는 뜻이다.
그러므로 이식을 시작하기 전에 자기 워크로드의 형상이 얼마나 가변적인지,
디코드 단계가 얼마나 많은지,
배치와 레이아웃이 TPU에 맞는지를 먼저 보는 것이 순서다.
이는 이 문서가 문서의 한계 목록을 읽고
세운 점검 순서이며 실제로 옮겨 본 결과가 아니다.

### 다른 가속기도 같은 문을 노린다

pcmoritz는 Tenstorrent 가속기를 위한 오픈소스
libtpu 구현을 사이드 프로젝트로 만들고 있으며
TorchTPU의 대부분을 이미 돌릴 수 있다고 소개했다.[^pcmoritz]
npalli는 Amazon이 AWS Trainium에 대해 같은 일을 하고
있다고 링크를 달았다.[^npalli]
이 두 댓글은 TorchTPU가 TPU만의 이야기가 아니라 PyTorch
위에 올라타는 가속기들의 공통된 패턴을 보여 준다.
이 문서는 두 댓글이 링크한 프로젝트를 열어 확인하지 않았다.
같은 날 DeepSeek의 추론 프레임워크 공개와
맞물린 시점이라는 추측도 스레드에 있었는데,
AnotherGoodName은 PyTorch 컨퍼런스가 그날 열려 시점이 겹쳤다고
설명했고,[^AnotherGoodName]
bitpush는 큰 회사가 그런 뉴스에 반응하지 않고
미리 정해진 일정이었을 것이라고 했다.[^bitpush]
시점의 이유는 이 문서가 확인하지 못했다.

---

[^intro]: TorchTPU Documentation, [Introduction to TorchTPU](https://torchtpu.readthedocs.io/en/latest/intro_to_torchtpu/)

[^faq]: TorchTPU Documentation, [TorchTPU FAQ](https://torchtpu.readthedocs.io/en/latest/faq/)

[^vm]: TorchTPU Documentation, [Get started with TorchTPU on a TPU VM](https://torchtpu.readthedocs.io/en/latest/get_started_on_a_vm/)

[^features]: TorchTPU Documentation, [TorchTPU supported feature set and future work](https://torchtpu.readthedocs.io/en/latest/feature_set/)

[^Lucasoato]: <https://news.ycombinator.com/item?id=50169173>

[^sschueller]: <https://news.ycombinator.com/item?id=50169268>

[^boulos]: <https://news.ycombinator.com/item?id=50169474>

[^fancyfredbot]: <https://news.ycombinator.com/item?id=50170486>

[^ismailmaj]: <https://news.ycombinator.com/item?id=50171330>

[^Tanjreeve]: <https://news.ycombinator.com/item?id=50169637>

[^23agt]: <https://news.ycombinator.com/item?id=50169752>

[^nelaggy]: <https://news.ycombinator.com/item?id=50170052>

[^pcmoritz]: <https://news.ycombinator.com/item?id=50170447>

[^npalli]: <https://news.ycombinator.com/item?id=50169215>

[^AnotherGoodName]: <https://news.ycombinator.com/item?id=50170870>

[^bitpush]: <https://news.ycombinator.com/item?id=50169570>
