# TorchTPU: PyTorch 코드를 `device="tpu"` 한 줄로 TPU에 올리는 Google과 Meta의 네이티브 백엔드

<https://github.com/google-pytorch/torch_tpu>

HN 토론: <https://news.ycombinator.com/item?id=50169053> (342점, 73개 댓글)

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
저장소는 2026년 3월 9일에 만들어졌고 언어는 C++다.
이 문서를 처음 썼을 때 별은 346개였고 2026년 10월 21일에 다시 읽은 값은 467개다.
PyPI에 올라 있는 버전은 0.0.0과 0.2.0뿐이고
README의 설치 예도 0.2.0을 가리킨다.[^pypi]
그런데 `main`의 공개 API 문서에는 0.2.1에서 폐기된 항목이 이미 적혀 있어서
`main`은 PyPI의 최신 휠(0.2.0)보다 앞서 있다.[^apis]
README는 지원 파이썬을 3.11 이상이라고 쓰고,
정책 문서는 3.11부터 3.14까지이며
자유 스레드 3.14t를 포함한다고 적는다.[^pypolicy]

기존에는 PyTorch를 TPU에서 쓰려면 PyTorch/XLA 같은 다리를 거쳤다.
문서의 FAQ는 PyTorch/XLA가 JAX 런타임 구성 요소에 크게 의존한 다리였고
TorchTPU는 JAX 런타임 의존이 없는 네이티브 백엔드이며,
PyTorch/XLA는 폐기되고 TorchTPU로 대체된다고 적는다.
TorchAX(torch_xla2)는 파이썬 수준에서 연산을 가로채 XLA로 내리는 구현이며
TorchTPU가 새로운 공식 표준이라고 한다.
JAX를 대체하는 것은 아니고 기존 PyTorch 코드베이스가 다시 쓰지 않고
TPU로 오는 입구라는 설명이다.[^faq]
HN의 mathisfun123도 이것이 pytorch/xla를 대체하는 것이라고
짧게 답했다.[^mathisfun123]

## 목차

- [동작 방식](#동작-방식)
  - [세 가지 즉시 실행 모드와 그래프 컴파일](#세-가지-즉시-실행-모드와-그래프-컴파일)
  - [컴파일 비용을 줄이는 캐시와 분산 프리미티브](#컴파일-비용을-줄이는-캐시와-분산-프리미티브)
  - [지연 연산이 실행되기까지](#지연-연산이-실행되기까지)
  - [텐서 메모리 모델: 복사는 싸고 뷰는 비싸다](#텐서-메모리-모델-복사는-싸고-뷰는-비싸다)
  - [분산 실행: tpu_dist와 SPMD라는 가정](#분산-실행-tpu_dist와-spmd라는-가정)
  - [동적 형상: 경계가 있는 동적성](#동적-형상-경계가-있는-동적성)
  - [수치 정밀도: bfloat16 입력과 float32 누적](#수치-정밀도-bfloat16-입력과-float32-누적)
- [사용하기](#사용하기)
  - [소스에서 빌드하기](#소스에서-빌드하기)
  - [노트북으로 따라 하기](#노트북으로-따라-하기)
  - [컴파일 캐시 켜기](#컴파일-캐시-켜기)
  - [커스텀 커널: Tokamax, Pallas, Helion](#커스텀-커널-tokamax-pallas-helion)
  - [프로파일 찍기](#프로파일-찍기)
  - [GKE에서 돌리기](#gke에서-돌리기)
- [지원 범위와 알려진 한계](#지원-범위와-알려진-한계)
  - [공개 API의 안정성 단계](#공개-api의-안정성-단계)
- [사례 연구가 보여 주는 수치](#사례-연구가-보여-주는-수치)
  - [FLUX: 같은 블록을 1.46배 빠르게](#flux-같은-블록을-146배-빠르게)
  - [FSDP: SimpleFSDP를 기본으로](#fsdp-simplefsdp를-기본으로)
  - [Muse Glimmer 30B 추론: 정적 캐시와 동적 캐시](#muse-glimmer-30b-추론-정적-캐시와-동적-캐시)
  - [Muse Glimmer 30B 학습: 순수 PyTorch로 얼마나 나오나](#muse-glimmer-30b-학습-순수-pytorch로-얼마나-나오나)
- [비평](#비평)
  - [한 줄이면 옮겨진다는 약속은 조건이 붙는다](#한-줄이면-옮겨진다는-약속은-조건이-붙는다)
  - [접근성은 여전히 Google Cloud의 TPU에 묶인다](#접근성은-여전히-google-cloud의-tpu에-묶인다)
  - [열린 이슈는 문서의 한계 목록보다 넓다](#열린-이슈는-문서의-한계-목록보다-넓다)
  - [로드맵은 약속이 아니라고 문서가 말한다](#로드맵은-약속이-아니라고-문서가-말한다)
- [인사이트](#인사이트)
  - [하드웨어가 프레임워크의 문을 열어야 하는 시대가 되었다](#하드웨어가-프레임워크의-문을-열어야-하는-시대가-되었다)
  - [한 줄로 도는 것과 비용 효율적으로 도는 것 사이에 성능 공학이 남는다](#한-줄로-도는-것과-비용-효율적으로-도는-것-사이에-성능-공학이-남는다)
  - [다른 가속기도 같은 문을 노린다](#다른-가속기도-같은-문을-노린다)
  - [번역해야 하는 것은 연산이 아니라 PyTorch의 암묵적 가정이다](#번역해야-하는-것은-연산이-아니라-pytorch의-암묵적-가정이다)

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

### 지연 연산이 실행되기까지

TorchTPU에서 연산을 부르면 TPU가 바로 일하지 않는다.
연산의 입력과 논리 단계, 출력의 모양과 타입이
CPU 쪽 메모리 객체인 deferred op로 먼저 포장된다.
deferred op는 현재 스트림의 대기열에 들어가고,
호출한 스레드는 여기서 끝난다.
launch-blocking 모드를 빼면 이후는 모두 백그라운드에서 비동기로 진행된다.[^exec]

백그라운드 스레드는 스트림에 쌓인 일을 묶어서 분석한다.
몇 개의 실행으로 나눌지, 실행마다 입력과 출력이 무엇인지,
최적화 수준을 어디에 맞출지, 전에 본 계산인지,
TensorCore와 SparseCore 중 어디서 돌릴지를 함께 정한다.
그다음 컴파일 캐시에서 실행 파일을 찾고,
없으면 StableHLO로 바꿔 컴파일 스레드풀에 넘기며,
준비된 실행 파일은 XLA 런타임 PjRt에 실행 작업으로 올라간다.
결과가 필요하면 `torch.Event`를 기록해 `query`로 확인하거나
`synchronize`로 파이썬을 멈춰서 기다린다.[^exec]

세 가지 즉시 실행 모드는 이 파이프라인을 어디서 끊느냐의 차이다.
Strict는 연산마다 실행을 시작하고,
단일 연산 그래프는 최적화 여지가 적어서 낮은 `-O1` 수준으로 빨리 컴파일한다.
컴파일이 연산마다 따로 일어나 스레드풀에서 병렬로 돌고 재사용률이 높아서
캐시를 데우는 비용이 작다는 것이 문서의 설명이다.
`torch.compile`은 전체 FX 그래프를 한 번 받아 더 높은 `-O2`로 컴파일하고,
호출할 때는 deferred op와 그래프 분석을 거치지 않고
실행 파일을 곧장 PjRt에 올린다.
DeferAndFuse는 연산을 파이썬 호출 사이에도 대기열에 두다가
디바이스에서 호스트로의 전송이 시작되거나 명시적 동기화가 일어날 때,
또는 같은 연산열이 반복되어 루프로 판단될 때 한 번에 컴파일한다.
그 시점에 이미 버려지거나 덮어쓴 텐서는 건너뛰어 다른 연산에 융합하거나 없앤다.
다만 분산 collective는 TPU 사이의 교착을 피하려고 이 제거를 하지 않는다.
문서는 DeferAndFuse가 모델 코드를 바꾸지 않고
기본 즉시 실행보다 최대 50% 빨라질 수 있다고 쓴다.[^exec]
이 수치는 문서의 주장이며 이 문서가 재 본 것은 아니다.

문서가 짚는 성능 함정은 네 가지다.
첫째, `if my_tensor.all()`처럼 텐서 값으로 파이썬 분기를 하면
조용히 동기화와 호스트 복사가 일어난다.
기본 즉시 실행에서는 파이프라인이 비워질 뿐이지만
DeferAndFuse와 컴파일 모드에서는 graph break가 되어 최적화 경계가 생긴다.
`torch.masked_select`처럼 출력 모양이 값에 따라 정해지는 연산도 같다.
둘째, Strict에서 작은 텐서로 연산을 잘게 보내면 PjRt에 올리는 데
드는 50마이크로초 안팎의 시간을 실행 시간이 가리지 못해서
TPU가 일감을 기다리는 작은 틈이 자주 생긴다.
셋째, 컴파일된 함수의 입력이 연속적이고 오프셋이 0인 텐서가 아니면
TorchTPU가 임시 복사를 만든다.
넷째, DeferAndFuse에서 쓸모없는 중간 텐서를 쥐고 있으면
그 텐서가 필요한 출력으로 오인되어 구체화되므로
다 쓴 텐서는 빨리 놓아야 한다.[^exec]

### 텐서 메모리 모델: 복사는 싸고 뷰는 비싸다

PyTorch의 `UntypedStorage`는 메모리 주소와 바이트 크기에 가깝다.
TPU의 버퍼는 타입과 다차원 모양을 가지며
메모리가 2차원 레지스터 정렬 타일로 배치되기 때문에
바이트 배열만으로는 실행에 필요한 정보가 모자란다.
문서가 TorchTPU 동작의 핵심이라고 말하는 장치는
TPU에서 `data_ptr`가 TPU 메모리가 아니라
TPU 버퍼의 메타데이터를 담은 CPU 메모리 위치를 가리키게 한 것이다.
이 한 겹이 CUDA 같은 PyTorch 인터페이스와
XLA의 함수형 설계를 이어 준다.[^memory]

stride로 표현된 뷰는 TPU에서 그대로 쓸 수 없어서
TorchTPU는 stride 패턴을 StableHLO의 slice, reshape, transpose,
broadcast 같은 논리 연산열로 해석하는 view decomposition을 한다.
문서는 논리적으로 같다는 것이 성능이 같다는 뜻은 아니라고 분명히 적는다.
reshape나 transpose가 한 레이아웃에서 다른 레이아웃으로 옮기려고
전체 복사를 요구할 수 있어서, CUDA와 달리 뷰는 공짜가 아니다.[^memory]

StableHLO는 값을 새로 만들기만 하는 SSA 언어라서
`add_`나 `out=` 같은 제자리 변경은 자동으로 functionalization된다.
갱신을 새 버퍼를 만드는 연산으로 기술하고
메타데이터 객체 안의 버퍼를 바꿔 끼우는 방식이다.
이 변환에는 view decomposition을 거꾸로 돌리는 view inversion이 필요하고
겹치는 뷰에서는 불가능하다.
브로드캐스트로 만든 텐서에 쓰면 CUDA에서는 정의되지 않은 동작이지만
TorchTPU는 항상 명시적으로 실패시킨다.
제자리 변경이 새 버퍼를 요구하면 최대 메모리가 두 배가 되므로
TorchTPU는 마지막 참조가 사라질 때 입력을 넘겨주는 buffer donation을 시도한다.
안전하다고 증명하지 못하면 out-of-place 갱신으로 돌아가고,
이때 큰 버퍼의 작은 일부를 쓰면 쓴 부분이 아니라
기반 스토리지 전체가 복사된다.[^memory]
반대로 `clone()`은 참조만 만드는 copy-on-write로 처리되어
실제 복사는 제자리 갱신이 일어날 때까지 미뤄진다.[^memory]

문서가 실무 지침으로 정리한 것은 다음과 같다.
같은 PyTorch 코드는 CUDA와 TPU에서 논리적으로 같은 결과를 내지만
성능은 같지 않을 수 있다.
복사는 싸고 뷰는 비싸므로 연속 텐서를 선호한다.
연속 텐서를 통째로 덮어쓰는 것은 보통 donation으로 메모리 효율이 좋다.
부분 쓰기는 비쌀 수 있어서 큰 텐서의 슬라이스보다
작은 텐서 여러 개가 낫다.[^memory]

### 분산 실행: tpu_dist와 SPMD라는 가정

`tpu_dist`는 `c10d::Backend`, 곧 ProcessGroup 수준에서 collective를 가로챈다.
NCCL 같은 별도 통신 라이브러리를 거치지 않고
`all_reduce`, `all_gather`, `reduce_scatter`, `all_to_all`을
StableHLO collective로 낮춰 XLA가 실행 파일 안에 컴파일한다.
GPU와 달라지는 점은 문서가 세 가지로 꼽는다.[^dist]

첫째, 각 프로세스가 한 TPU 장치에 묶여서
`init_process_group` 전에 슬라이스의 물리적 모양(`TORCH_TPU_TOPOLOGY`)과
칩 사이 연결을 만드는 주소(`TORCH_TPU_SLICEBUILDER_ADDRESSES`),
장치 총수(`WORLD_SIZE`)가 환경에 있어야 한다.
둘째, `stablehlo.all_reduce`는 호출한 rank가 속하지 않은 서브그룹까지
모든 `replica_groups`를 요구하므로
`tpu_dist`가 서브그룹 구성을 모든 rank와 교환해 조립한다.
셋째, XLA와 TPU 통신은 모든 rank가 같은 모듈을 컴파일하는
SPMD를 전제하는데, PyTorch 프로그램은 `if rank == 0:` 분기나
균등하게 나뉘지 않는 샤딩 때문에 MPMD가 되기 쉽다.
rank마다 다른 모듈에 collective가 들어 있으면
동기화 플래그나 버퍼 오프셋이 어긋나
교착이나 메모리 손상이 일어날 수 있다.[^dist]

그래서 collective는 기본적으로 앞뒤에 graph break를 넣어
각각 독립된 skinny collective 모듈로 컴파일된다.
안전한 대신 XLA가 계산과 통신을 겹치지 못한다.
겹치기를 켜는 방법은 둘이고 서로 독립이다.

| 방식                  | 설정                                                                            | 동작                                                                      |
| --------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| skinny (기본)         | 항상 켜져 있음                                                                  | collective마다 별도 StableHLO 모듈, 주위에 graph break                    |
| `@spmd_safe`          | `@torch.tpu.distributed.spmd_safe`                                              | 데코레이트한 함수 안의 graph break를 없애 하나의 모듈로 융합              |
| Compilation Handshake | `TORCH_TPU_SPMD_HANDSHAKE_STAGE=COMPILE_STAGE` 또는 `DISPATCH_STAGE` (기본 OFF) | 모든 rank의 FX 그래프가 같은지 확인해 같으면 융합, 다르면 skinny로 되돌림 |

`@spmd_safe`는 모든 rank가 같은 텐서 연산과 collective 순서를
실행한다고 사용자가 보장해야 쓸 수 있는 방법이고,
MPMD 코드에 붙이면 교착이 날 수 있다고 문서가 경고한다.
`COMPILE_STAGE`는 rank마다 따로 재컴파일되는 상황에서
한 rank만 핸드셰이크를 시작해 시간 초과가 날 수 있고,
그런 작업에는 디스패치 시점에 합의를 확인하는 `DISPATCH_STAGE`가 필요하지만
오버헤드가 더 크다고 한다.[^dist]

실행은 환경 변수를 채우는 도우미를 거쳐 `torchrun`으로 시작한다.
아래는 문서의 흐름을 줄여 옮긴 것이다.
TPU가 없어서 이 문서가 실행한 것은 아니다.

```bash
# TORCH_TPU_TOPOLOGY, TORCH_TPU_SLICEBUILDER_ADDRESSES, WORLD_SIZE 등을 내보낸다
# 이미 설정한 값은 그대로 두므로 일부만 직접 덮어쓸 수 있다
eval $(python3 -m torch.tpu.distributed | sed 's/^/export /')
# 호스트의 TPU 장치마다 워커 프로세스를 하나씩 띄운다
torchrun --nproc_per_node=$WORLD_SIZE train.py
```

```python
import torch
import torch.distributed as dist

def worker_main():
  # 백엔드 이름만 nccl 에서 tpu_dist 로 바뀐다
  dist.init_process_group(backend="tpu_dist")
  rank = dist.get_rank()
  device = torch.device("tpu")

  x = torch.ones(4, 4, device=device) * (rank + 1)
  dist.all_reduce(x, op=dist.ReduceOp.SUM)
  print(f"[Rank {rank}] Reduced sum: {x[0, 0].item()}")
  dist.destroy_process_group()

if __name__ == "__main__":
  worker_main()
```

병렬화 차원은 통신이 잦은 것부터 안쪽에 두라는 것이 문서의 메시 지침이다.
텐서 병렬은 레이어마다 collective가 있어서 가장 빠른 칩 사이 링크(ICI)에,
복제 데이터 병렬은 스텝마다 그래디언트만 합치므로 바깥 축이나
슬라이스 사이의 데이터 센터 네트워크(DCN)에 둔다.
`torch.tpu.distributed.topology_aware_mesh()`가 물리적 ICI 링에 맞춘
rank 배치를 계산하고, 여러 슬라이스면
바깥 차원을 DCN에 자동으로 매핑한다.[^dist]
커스텀 Pallas 커널로 ICI 위에서 호스트 CPU 없이
원격 DMA를 하는 통신 커널(Ring Attention 등)도 등록할 수 있다.[^dist]

### 동적 형상: 경계가 있는 동적성

XLA는 텐서 모양이 컴파일 때 정해져 있다고 가정하고 HBM 버퍼 배치와
연산 융합, 행렬곱 타일링을 짠다.
`torch.compile`에서 입력 모양이 호출마다 달라지면
Dynamo의 모양 guard가 깨지고 XLA 전체 재컴파일이 일어난다.
TorchTPU의 대응은 동적 차원의 상한은 컴파일 때 고정하고
실제 크기는 실행 때 XLA가 추적하게 하는 bounded dynamism이다.[^dyn]

작동 방식은 이렇다.
Dynamo가 변하는 차원을 `SymInt`로 표현한 FX 그래프를 주면
TorchTPU가 `[하한, 상한]` 구간을 `bucket_size`(기본 128,
TPU의 128 레인 타일에 맞춘 값)
배수 경계의 버킷들로 나눈다.
버킷 수 `num_dynamic_buckets`의 기본은 1이고 최대는 8이다.
버킷마다 동적 차원을 그 버킷의 상한 U로 바꾸고,
실제 크기를 입력으로 받는 StableHLO로 낮춰 XLA가 컴파일한다.
실행하면 XLA가 입력을 U까지 채우고 채운 영역을 연산에 영향이 없는
항등값으로 덮으며, 동적인 출력은 패딩을 끝에 둔 채
모양 메타데이터만 갱신해서 PyTorch로 돌려준다.[^dyn]

대표 사례는 `torch.cat`으로 KV 캐시가 한 토큰씩 자라는 자기회귀 디코딩이다.
`dynamic=False`에서는 토큰마다 guard가 깨져 매번 재컴파일이 일어난다.
문서가 실은 샘플 출력에서 `dynamic=False`는 열 단계 내내 약 38에서 50밀리초였고,
`dynamic=None`은 처음 세 단계에만 컴파일 비용이 있고
네 번째 단계부터 약 0.4밀리초였다.
세 번 컴파일되는 이유도 적혀 있다.
둘째 단계에서 Dynamo가 그 차원을 동적으로 표시하고,
셋째 단계에서는
XLA가 만든 패딩 출력의 레이아웃에 맞춰 같은 버킷을 한 번 더 컴파일한다.
달라질 차원을 미리 안다면
`mark_dynamic`으로 첫 정적 컴파일을 건너뛸 수 있다.[^dyn]

```python
import time
import torch

device = torch.device("tpu")

def decode_step(kv_cache, new_token):
  return torch.cat([kv_cache, new_token], dim=2)

kv_cache = torch.ones((1, 8, 16, 128), dtype=torch.bfloat16, device=device)
new_token = torch.ones((1, 8, 1, 128), dtype=torch.bfloat16, device=device)

# 달라질 차원(2)과 범위를 미리 알려 첫 정적 컴파일을 건너뛴다
torch._dynamo.mark_dynamic(kv_cache, 2, min=16, max=128)
# dynamic=None 이 bounded dynamism 을 켜는 설정이다
step = torch.compile(decode_step, backend="tpu", dynamic=None)

for i in range(10):
  start = time.perf_counter()
  kv_cache = step(kv_cache, new_token)
  torch.accelerator.synchronize()
  ms = (time.perf_counter() - start) * 1000
  print(f"step {i + 1} (seq_len={kv_cache.shape[2]}): {ms:.2f} ms")
```

위 코드는 문서의 예를 줄이고
`mark_dynamic`을 더한 것이며 이 문서가 실행하지는 않았다.
같은 문서가 적은 한계가 적용 범위를 정한다.
버킷은 트레이스당 최대 8개이고 가장 큰 버킷의 상한을 넘으면 재컴파일이 일어난다.
실행이 상한 U까지 채워진 버퍼에서 돌기 때문에
실제 크기가 U보다 한참 작아도 HBM과 FLOPs는 U 기준으로 낸다.
XLA 물리 레이아웃이 바뀌면 같은 버킷 안에서도 재컴파일된다.
컴파일 결과가 `AOTAutogradCache`에 저장되지 않아
프로세스를 새로 시작할 때마다 다시 컴파일한다.
`torch.nonzero`처럼 출력 크기가 값에 달린 연산, Pallas 커스텀 커널,
`dynamic=True`는 지원하지 않는다.
문서는 이 기능이 자기회귀 KV 캐시를 위해 다듬어진 상태라고 쓴다.[^dyn]
소개 페이지는 한 걸음 더 나아가 기본값이 `dynamic=False`이고
`dynamic=None`과 `dynamic=True`는 아직 프로덕션 지원이 아니라고 적는다.[^intro]
이 둘은 같은 저장소 문서의 서로 다른 페이지이며
이 문서는 어느 쪽이 더 최신인지 확인하지 못했다.

### 수치 정밀도: bfloat16 입력과 float32 누적

TPU는 부동소수점 연산을 두 유닛에 나눈다.
행렬곱 유닛(MXU)은 `matmul`, `mm`, `bmm`, 합성곱 같은 수축 연산을
bfloat16 입력과 float32 누적으로 실행하고,
벡터 유닛(VPU)은 원소별 연산과 활성화,
정규화, softmax를 완전한 float32로 실행한다.
그래서 float32 행렬곱의 기본 동작이 GPU와 다르다.
CUDA의 기본은 `"highest"`(순수 float32)이지만
TorchTPU의 기본은 `"medium"`(`Precision.DEFAULT`)이고
float32 입력을 bfloat16으로 반올림해서 한 번에 곱한다.
`"high"`는 입력을 bfloat16 둘로 쪼개 세 번,
`"highest"`는 셋으로 쪼개 여섯 번 곱해서
MXU 계산량이 대략 3배, 6배가 된다고 문서가 쓴다.[^prec]

정밀도는 `torch.set_float32_matmul_precision`으로 프로세스 전체에,
`with torch.tpu.precision(mode):`로 민감한 층에만 지정한다.
범위 지정 컨텍스트는 들어가고
나올 때 `torch.compile` graph break를 만들기 때문에
`fullgraph=True`라면 컴파일된 함수 밖에서 지정해야 한다.
`"high"`와 `"highest"`는 한 번 경고를 낸다.
문서는 대부분의 학습과 추론에 기본값이 충분하다고 권하고,
큰 수축 차원을 가진 현대 모델에서는 누적 잡음이 저차 항의 기여보다 커서
1-pass로 족하다고 주장한다.
메모리 대역폭이 병목인 옛 float32 모델은 놀고 있던 MXU 주기를 쓰기 때문에
3배나 6배까지 느려지지는 않는다고도 한다.[^prec]

또 하나의 스위치는 `torch.tpu.allow_excess_precision`이다.
행렬곱 결과를 bfloat16으로 내리지 않고 float32로 둔 채 다음 연산에 융합하면
컴파일 결과가 즉시 실행의 반올림과 달라질 수 있다.
기본값은 `False`라서 즉시 실행과 같은 반올림을 유지한다.
XLA가 첫 컴파일 때 이 값을 잠그므로 스크립트 맨 앞에서 정해야 하고,
나중에 바꾸면 `RuntimeError`가 난다.
bfloat16 `mm`이나 `bmm`의 float32 누적기를 그대로 받으려면
`out_dtype=torch.float32`를 준다.[^prec]

GPU 코드를 옮길 때 문서가 권하는 확인 방법은
같은 dtype끼리 CPU와 TPU 결과를 `torch.testing.assert_close`로 비교하는 것이다.
bfloat16 대 float32 비교는 하드웨어 차이가 아니라 양자화 오차를 재기 때문이다.
활성화뿐 아니라 그래디언트도 같은 방식으로 비교하라고 한다.
문서가 보여 주는 `nn.Linear(10, 10)` bfloat16 예에서도
최대 절대 차이가 0.006596으로 기본 허용치를 넘었다.
문서는 작은 절대 차이가 여러 요소에서 보이면 보통 융합과 누적 순서에서 나온
반올림 차이이지 논리 버그가 아니라고 설명한다.[^prec]

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

### 소스에서 빌드하기

릴리스 휠 대신 소스에서 빌드하려면 Bazel이 필요하고,
README는 Bazelisk를 설치해 `PATH`에 두라고 안내한다.
README의 빌드 명령과 주의점은 다음과 같다.
이 문서가 실행해 본 것은 아니다.

```bash
# --config=wheel_common 이 없으면 빌드가 실패한다
bazel build --config=wheel_common //ci/wheel:torch_tpu_wheel

# RBE(원격 빌드 실행) 자격이 없으면 no_rbe 를 wheel_common 뒤에 붙인다
# 나중에 오는 config 가 원격 캐시와 원격 실행 플래그를 이기기 때문이다
bazel build --config=wheel_common //ci/wheel:torch_tpu_wheel --config=no_rbe

# 만들어진 휠은 CPU 용 torch 를 받도록 추가 인덱스를 주고 설치한다
pip install ../bazel-bin/ci/wheel/*.whl \
  --extra-index-url https://download.pytorch.org/whl/cpu
```

README는 `wheel_common` 없이 만든 휠이 `import torch`에서
정적 등록 중복으로 중단된다고 설명한다.
최적화 없는 빌드(`-c dbg` 등)는 휠 빌드에 쓰지 않으며,
C++를 디버깅하려고 일부러 만들 때만
`--//:allow_unoptimized_wheel=True`를 준다.

### 노트북으로 따라 하기

사용자 가이드는 `docs` 폴더의 대화형 노트북을 정적으로 옮긴 것이다.
노트북은 Jupyter와 비슷한 Marimo이고
`marimo edit file.py`로 열어 브라우저에서 쓴다.
TPU VM에서 실행해야 하며 v6e GCE 인스턴스가 가장 쉽다고 README가 적는다.
저장소의 `examples` 디렉터리에는 `simple_pytorch`, `tensor_parallel`, `fsdp`,
`FLUX_optimization`, `muse_glimmer_30b`가 있다.
README의 기능 목록은 Llama, Qwen, ResNet, DLRM, minGPT, UNet 예제를 든다.

### 컴파일 캐시 켜기

컴파일이 길거나 즉시 실행의 워밍업이 길면 문서는 지속적 캐시를 권한다.
2단계 캐시는 `/dev/shm/torch_tpu_cache/<이름>`에 만들어지고
환경 변수에는 경로가 아니라 디렉터리 이름만 넣는다.
3단계는 `gs://` 버킷이나 공유 파일 시스템 경로를 쓴다.
아래는 API 레퍼런스의 예를 줄인 것이다.[^api]

```python
import os

tier2_name = "tpu_tier2_cache"
os.makedirs(os.path.join("/dev/shm/torch_tpu_cache", tier2_name), exist_ok=True)

# 이름만 넣는다 (경로 전체가 아니다)
os.environ["TORCH_TPU_TIER2_COMPILATION_CACHE"] = tier2_name
# 호스트와 작업 재시작을 넘어 재사용하려면 지속적 경로를 준다
os.environ["TORCH_TPU_TIER3_COMPILATION_CACHE_ROOT"] = "/tmp/tpu_tier3_cache"

import torch  # 환경 변수는 TPU 연산을 처음 쓰기 전에 정한다

device = torch.device("tpu")
a = torch.randn(1024, 1024, device=device)
_ = (a @ a).to("cpu")
```

### 커스텀 커널: Tokamax, Pallas, Helion

기본 연산이 부족하면 커널을 직접 끼우는 방법이 세 가지 있다.[^kernels]

| 방식                               | 상태     | 쓰는 경우                                                  |
| ---------------------------------- | -------- | ---------------------------------------------------------- |
| Tokamax                            | 프로덕션 | 커널 코드를 쓰지 않고 흔한 LLM과 MoE 블록을 가속           |
| Pallas (`torch.tpu.pallas.jax_op`) | 프로덕션 | JAX/Pallas로 맞춤형 최고 성능 커널을 써서 PyTorch에서 호출 |
| Helion                             | 실험     | PyTorch 네이티브 DSL로 GPU와 TPU 모두에 쓸 수 있는 커널    |

Tokamax는 MoE의 grouped matmul과 토큰 gather와 scatter,
paged attention, Gated DeltaNet, Kimi Delta Attention, MLA,
`TopK` 같은 블록을 이미 갖춘 JAX/Pallas 커널 라이브러리다.
Pallas 커널은 입출력 `Ref`로 정의하고 `pl.pallas_call`로 감싼 JAX 함수를
`torch.tpu.pallas.jax_op`로 등록하는 세 단계로 쓴다.
아래는 문서의 예다.
이 문서가 실행한 것은 아니다.

```python
import jax
from jax.experimental import pallas as pl
import torch

# 1. Pallas 커널을 입출력 Ref 로 정의한다
def add_vectors_pallas_kernel(x_ref, y_ref, o_ref):
  x, y = x_ref[...], y_ref[...]
  o_ref[...] = x + y

# 2. pallas_call 로 감싸 출력 모양과 dtype 을 지정한다
def add_vectors_jax(x: jax.Array, y: jax.Array) -> jax.Array:
  return pl.pallas_call(
      add_vectors_pallas_kernel,
      out_shape=jax.ShapeDtypeStruct(x.shape, x.dtype),
  )(x, y)

# 3. PyTorch 연산으로 등록한다
add_vectors_fn = torch.tpu.pallas.jax_op("pallas::add_vectors", add_vectors_jax)

x = torch.tensor([1.0, 2.0, 3.0], device="tpu")
y = torch.tensor([4.0, 5.0, 6.0], device="tpu")
z = add_vectors_fn(x, y)
```

문서는 `jax_op`가 JAX를 트레이스할 때 한 번만 쓰며,
학습과 추론 때는 커널이 `torch.Tensor`의 TPU 버퍼에서
바로 돈다고 설명한다.[^flux]
Helion 지원은 실험 단계이고
프로덕션에는 Tokamax나 `jax_op`를 쓰라고 한다.[^kernels]

### 프로파일 찍기

네이티브 `torch.profiler`가 TPU 실행을 기록하려면 PyTorch 2.12 이상이 필요하다.
TensorBoard가 `pkg_resources`에 기대므로 `setuptools<81`을 먼저 깔고
`xprof`와 `tensorboard`를 설치하라고 문서가 경고한다.[^xprof]

```python
import torch
from torch.tpu.profiler import TpuProfilerConfig

device = torch.device("tpu")
model = torch.nn.Sequential(
    torch.nn.Linear(128, 64), torch.nn.ReLU(), torch.nn.Linear(64, 10)
).to(device).to(torch.bfloat16)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
data = torch.randn(32, 128, device=device, dtype=torch.bfloat16)

config = TpuProfilerConfig(host_tracer_level=2, device_tracer_level=1)

# 프로파일러는 오버헤드가 있으므로 대표적인 100~1000 스텝만 감싼다
with torch.profiler.profile(
    activities=[
        torch.profiler.ProfilerActivity.CPU,
        torch.profiler.ProfilerActivity.TPU,
    ],
    experimental_config=config,
    on_trace_ready=torch.profiler.tensorboard_trace_handler("/tmp/profiler_output"),
) as prof:
  for step in range(100):
    optimizer.zero_grad()
    loss = model(data).sum()
    loss.backward()
    optimizer.step()
    torch.accelerator.synchronize()
    prof.step()
```

문서가 트레이스에서 읽으라고 하는 신호는 세 가지다.
TPU 연산 사이에 큰 틈이 있으면 호스트 쪽 병목이고,
짧은 TPU 실행이 자주 끊기면 graph break로 인한 잦은 재컴파일이며
`.item()`과 `.cpu()`를 줄이고 `torch.compile`을 쓰라고 한다.
MXU 사용률이 낮으면 텐서
차원이 타일 크기 128에 맞지 않은 것이므로 128의 배수로 채운다.
좋은 프로파일은 긴 연속 계산 블록과 60%를 넘는 MXU 사용률이라고
문서가 말한다.[^xprof]

### GKE에서 돌리기

문서의 GKE 가이드는 `tpu7x` 노드 풀을 가진 GKE Standard 클러스터를 전제하고,
예제 스크립트가 미리 들어 있는 공개 컨테이너 이미지로 Kubernetes `Job`이나
`JobSet`을 제출하는 흐름을 보여 준다.
단일 장치 예제, 4칩 한 호스트의 분산 예제,
16개 호스트에 걸친 64칩 슬라이스 예제,
업스트림 PyTorch의 MNIST를 올리는 예제가 순서대로 나온다.[^gke]

## 지원 범위와 알려진 한계

문서가 구분한 검증 단계(Validated)와 실험 단계(Experimental)를 정리하면
이렇다.[^features]

| 영역           | 검증됨                                                                                    | 실험적                                                 |
| -------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| TPU 세대       | v5e, v5p, v6e, v7                                                                         | 향후 v8i, v8t                                          |
| 기본 기능      | 쉬운 이식, 즉시 실행과 컴파일 혼용, 순전파와 역전파, `torch.profile`, 동적 연산(재컴파일) | SymInt, jagged tensor                                  |
| 모델           | Transformer(Dense, MoE): Qwen, Llama, Muse Glimmer, Gemma / 확산: WAN, FLUX / CNN         | GLM, Kimi, DeepSeek, GPT OSS 등, Mamba, LSTM/GRU, DLRM |
| 커널           | Pallas, Tokamax                                                                           | Helion                                                 |
| 양자화         | 전체 텐서 FP8/FP4, 채널별 FP8                                                             | 블록 단위 FP8/FP4(향후)                                |
| 분산           | 최적 메시, SimpleFSDP, 체크포인트, 활성화 오프로딩, 최대 8K 칩 다중 슬라이스              | FSDPv2와 MPMD(낮은 성능), TorchComm                    |
| 통합           | Hugging Face, Ray, vLLM, SGLang, TorchTitan, TorchRec                                     | VeRL(향후)                                             |
| 제품 수준 해법 | 추론(멀티 호스트, prefill/decode 분리), 파인튜닝(최대 약 8K 칩)                           | 향후 RL, 탐색 단계의 사전학습                          |

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

### 공개 API의 안정성 단계

공개 API 문서는 먼저 경고한다.
나열된 것 말고 다른 TorchTPU API를 쓰는 것은 정의되지 않은 동작이고
지원하지 않는다.
나열된 API는 네 단계로 나뉜다.[^apis]

| 단계         | 약속                                                        | 들어 있는 것                                                                                      |
| ------------ | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Stable       | 장기 지원, 하위 호환을 깨거나 없애려면 폐기 절차를 거침     | `torch.accelerator.*` 대부분, `torch.tpu.ops.max_pool1d/2d/3d`와 역전파, `TPU_VISIBLE_DEVICES` 등 |
| Experimental | 폐기 절차 없이 언제든 바뀌거나 삭제됨, 쓰면 경고를 한 번 냄 | `EagerMode`, `Stream`, `Event`, `Precision`, 옵티마이저, 희소 연산, `pallas.jax_op`, `spmd_safe`  |
| Deprecated   | 폐기를 도입한 버전 이후 최소 2개 마이너 릴리스 뒤에 제거    | `torch.tpu.get_device_name`(0.2.1에서 폐기), `torch.tpu.topology_aware_mesh`(0.2.0에서 폐기)      |
| Internal     | PyTorch가 부르기 위한 것, 직접 부르면 오류                  | `torch.tpu.current_device`, `torch.tpu.set_device` 등(대체: `torch.accelerator.*`)                |

이 표에서 눈에 띄는 점은 이 문서가 앞에서
소개한 기능 대부분이 Experimental이라는 것이다.
즉시 실행 모드 선택(`torch.tpu.EagerMode`와 `eager_mode`),
`torch.tpu.precision`과 `allow_excess_precision`,
`torch.tpu.distributed.spmd_safe`와 `topology_aware_mesh`,
`torch.tpu.pallas.jax_op`,
`torch.tpu.optimizers`의 AdamW, Muon, Sgd와 `SingleTraceTrainer`,
`splash_sdpa`와 `ragged_dot`,
`sparse_dense_matmul` 같은 연산이 모두 여기에 있다.
`TORCH_TPU_DEFER_AND_FUSE`와 `TORCH_TPU_LAUNCH_BLOCKING`,
컴파일 캐시 변수도 같은 단계다.[^apis]
문서가 기능 목록에서 검증됨으로 분류한 것과
API 약속 단계가 같은 말이 아니라는 점은 이 문서의 해석이며,
검증된 기능을 쓰는 코드라도 그 진입점이 바뀔 수 있다는 뜻으로 읽었다.

## 사례 연구가 보여 주는 수치

문서에는 네 편의 사례 연구가 있고 그중 세 편이 숫자를 싣는다.
다만 비교 대상은 같은 코드의 이전 버전이고 GPU가 아니다.
이 문서가 읽은 소개, 기능 목록, 사례 연구 어디에도 GPU와의 성능 비교는 없었다.
아래 수치는 문서 저자의 측정이고 이 문서가 재현한 것은 없다.

### FLUX: 같은 블록을 1.46배 빠르게

FLUX 확산 트랜스포머의 `DoubleStreamBlock` 한 개를
TPU v6e 칩 하나(HBM 32GiB)에서 시퀀스 길이 32,768,
bfloat16으로 학습시킨 스텝 시간이다.
측정 환경은 파이썬 3.14, PyTorch 2.15 사전 릴리스,
소스에서 빌드한 TorchTPU다.[^flux]

| 구성                                                            | 평균 스텝 시간 | 기준 대비 |
| --------------------------------------------------------------- | -------------- | --------- |
| 기준(즉시 실행)                                                 | 178.61 ms      | 1.00x     |
| Pallas SplashAttention만(즉시 실행)                             | 149.81 ms      | 1.19x     |
| zero-copy views만(즉시 실행)                                    | 178.30 ms      | 1.00x     |
| `torch.compile`만                                               | 159.33 ms      | 1.12x     |
| zero-copy views + RoPE 융합 + `torch.compile`                   | 153.60 ms      | 1.16x     |
| zero-copy views + RoPE 융합 + SplashAttention + `torch.compile` | 122.51 ms      | 1.46x     |

표에서 눈에 띄는 것은 최적화의 효과가 단순히 더해지지 않는다는 점이다.
뷰를 복사 없이 만드는 변경은 단독으로는 거의 효과가 없었고(178.61에서 178.30),
RoPE 융합은 `torch.compile` 안에서만 이득이 났다(159.08에서 153.60, 3.4%).
SplashAttention은 기본 512토큰 블록에서는 컴파일 상태의 표준 SDPA보다
약 10% 느렸고, 블록을 2048로 맞추고 bfloat16으로 돌렸을 때 이득이 났다.
문서도 블록 크기를 몇 가지 재 보고
프로파일한 뒤에 커스텀 커널을 쓰라고 권한다.[^flux]
이 사례 연구는 첫머리에서 1.48배라고 쓰고 표에서는 1.46배를 보여 준다.
이 문서는 표의 값을 따랐고 불일치의 이유는 확인하지 못했다.

### FSDP: SimpleFSDP를 기본으로

FSDP 가이드의 결론은 TPU에서 성능이 학습 스텝 전체를
`torch.compile(backend="tpu")`로 하나의 XLA 프로그램에 담는 데서
나온다는 것이다.
XLA가 순전파, 역전파, collective를 한꺼번에 봐야 계산과 통신을 겹치기 때문이다.
SimpleFSDP는 파라미터를 샤딩된 `DTensor`로 두고 접근할 때 all-gather를 일으켜
런타임 훅이 없고 그래프가 끊기지 않으며
`data_parallel(...)` 한 번으로 모델 전체를 샤딩한다.
PyTorch FSDPv2의 `fully_shard`는 파이썬 훅이 스텝을 여러 그래프로 쪼개서
SparseCore 오프로드가 나오기 전에는 경쟁력 있는 성능을 내기 어렵다고
한다.[^fsdp]

공통 모범 사례로 문서가 든 것은 일곱 가지다.
스텝 전체를 컴파일하고, 샤딩한 층마다 activation checkpointing을 하고,
샤딩 차원이 메시 크기로 나누어떨어지게 하고,
샤딩된 가중치를 초기화할 때 rank마다 시드를 다르게 하고,
rank별 분기 안에서 `.item()`처럼 구체화를 일으키는 연산을 피하고,
전체 샤딩이 확장되지 않으면 HSDP를 쓰고,
확장하기 전에 메모리와 수치를 기준과 비교하는 것이다.
여러 슬라이스에서는 느린 DCN으로는 복제하고
슬라이스 안에서 샤딩하는 것이 거의 항상 낫다고 한다.[^fsdp]

### Muse Glimmer 30B 추론: 정적 캐시와 동적 캐시

52층 모델의 전체 가중치는 TPU HBM에서 약 55.7GB이고,
노트북의 기본값은 처음 4층(약 9.3GB)만 올리는 것이라서 생성 문장은 의미가 없다.
단일 TPU v7x 칩에서 컴파일 캐시를 비운 상태로 잰 결과는 다음과 같다.[^infer]

| 항목                     | `StaticCache`(`dynamic=False`) | `DynamicCache`(`dynamic=None`) |
| ------------------------ | ------------------------------ | ------------------------------ |
| prefill                  | 약 21.0초                      | 약 18.3초                      |
| 디코드 1단계             | 약 19.8초                      | 약 20.0초                      |
| 디코드 2단계             | 24.66 ms                       | 약 22.0초                      |
| 디코드 3단계             | 24.29 ms                       | 약 4.9초                       |
| 토큰당 평균(워밍업 제외) | 23.58 ms(2~20단계)             | 24.17 ms(4~20단계)             |

체크포인트 627개 텐서를 올리는 데 약 100초에서 420초가 걸렸다고 한다.
정적 캐시는 컴파일이 둘뿐이고 동적 캐시는 워밍업 단계가 두 개 더 있지만
워밍업 뒤의 토큰당 시간은 거의 같았다.
같은 가이드는 `AOTAutogradCache`가 컴파일 결과를 디스크에 저장해서
모델 코드가 같으면 재실행 때 prefill과 첫 디코드가 캐시에서
올라온다고 쓴다.[^infer]

### Muse Glimmer 30B 학습: 순수 PyTorch로 얼마나 나오나

Ironwood TPU 4개가 있는 호스트 한 대에서 FSDP로 전체 모델을 학습하는
단순한 루프이며 커스텀 커널이 없다.
시퀀스 길이 5120에서 rank당 2,400에서 2,800 TPS,
전체 1만 9천에서 2만 2천 TPS가 나온다고 한다.
문서는 현실적인 사전학습 규모가 아니라
직접 돌려 보고 읽을 수 있는 예제라는 점을 분명히 한다.[^train]

## 비평

### 한 줄이면 옮겨진다는 약속은 조건이 붙는다

소개 문구는 최소한의 코드 변경으로 기존 PyTorch 워크로드를 돌린다고 말한다.
같은 페이지가 이어서 적은 한계는 그 약속이 어디까지인지를 말해 준다.
돌아가는 것과 빠르게 돌아가는 것은 다르다.
동적 형상 때문에 디코드 단계마다 재컴파일이 일어나고,
FSDPv2와 MPMD는 기능은 되지만 성능이 낮으며,
CNN의 기본 배치는 TPU에서 비효율적이다.
이 문서가 읽은 소개와 기능 목록, 사례 연구에는 GPU 대비 성능 수치가 없고
일반적인 가격 대비 성능 주장만 있다.
사례 연구에는 숫자가 있지만 비교 대상은 같은 코드의 이전 버전이다.
FLUX 사례는 최적화를 쌓아서 1.46배를 얻는 데
Pallas 커널과 뷰 변경, 연산 융합이라는 코드 수정이 필요했다.
따라서 옮기는 비용이 코드 수정에서
끝나는지 성능 공학까지 이어지는지는 워크로드마다 직접 재야 한다.
HN의 coredog64는 가능하다고들 하지만 세부에 늘 문제가 있고,
모델 구조의 특이점 하나가 내보내기 과정이 깔고 있는 암묵적 가정을
깨뜨리는 것을 알게 되면 낭패라고 적었다.[^coredog64]

### 접근성은 여전히 Google Cloud의 TPU에 묶인다

HN의 Lucasoato는 TPU를 Google Cloud 밖에서 쓸 수 있느냐고 물었고,
sschueller는 Coral USB와 M.2 장치가 TPU라고 답했지만,
boulos는 마케팅 이름만 같을 뿐 서로 관련이 없다고
바로잡았다.[^Lucasoato][^sschueller][^boulos-coral]
Dr4kn은 Coral이 2019년에 나온 뒤 하드웨어 개정이 없어
대부분의 작업에 뒤처졌다고 덧붙였다.[^Dr4kn]
boulos는 Google이 큰 고객에게 TPU를 현장 설치용으로 팔고
있다고 설명했다.[^boulos]
atty는 대형 GCP 고객으로서 온프레미스 TPU를 평가했지만
Nvidia에 한 세대 더 머물기로 했다고 썼다.[^atty]
jacquesm은 TPU를 구하기 어렵다고 보고
Google의 노력은 고맙지만 자신에게 쓸모가 있지는 않다고 적었다.[^jacquesm]
이 백엔드는 문서상 Google Cloud TPU를 대상으로 하며
최신 하드웨어를 쓰려면 GKE가 필요하다고 안내한다.[^vm]
코드가 오픈소스여도 실행할 하드웨어는 한 사업자의 클라우드에 있다.
PyTorch/XLA가 폐기되고
대체된다는 FAQ의 문장은 기존 XLA 사용자에게 이전 비용도 의미한다.[^faq]

### 열린 이슈는 문서의 한계 목록보다 넓다

문서의 한계 항목은 동적 형상, 뷰 연산, MPMD,
FlexAttention, 정밀도, 프로세스 접근이다.
2026년 10월 21일에 저장소의 열린 이슈를 읽어 보니
이 목록에 없는 종류의 문제가 있었다.
모두 사용자가 올린 보고이고 이 문서가 재현한 것은 없으며,
보고마다 쓴 버전이 달라서 지금의 `main`에서도 같은지는 확인하지 못했다.

가장 눈에 띄는 것은 스케일링 보고다.
ViT 기반 기상 예측 모델(2,560만 파라미터)을 v6e-8로 옮기던 사용자는
학습 스텝 전체가 한 칩에서는 그래프 하나(32.9 ms/step)로 컴파일되는데,
`DistributedDataParallel`로 감싸면
그래프 셋과 스텝당 약 1,550개의 실행 파일로 쪼개져
8칩에서 102.7 ms/step, 스케일링 효율 32%가 되었다고 적었다.
같은 스텝을 DDP 없이 컴파일된 스텝 안의 함수형 all-reduce 한 번으로 평균하면
8칩에서 93%였다고 한다.[^issue-4411]
이것은 문서가 SimpleFSDP와 `torch.compile` 조합을 권하면서
FSDPv2를 낮은 성능으로 분류한 것과 같은 방향의 이야기이지만,
DDP도 같은 함정에 걸린다는 점은 문서의 한계 목록에 없다.

정확성 보고도 있다.
학습 모드의 BatchNorm이 `running_mean`과 `running_var`를 갱신하지 않아서
`model.eval()`이 평균 0, 분산 1로 정규화한다는 보고가 올라와 있고,
재현 코드의 결과는 CPU가 `[0.4964, 0.4978, 0.4965]`, TPU가 `[0., 0., 0.]`이었다.
즉시 실행과 `torch.compile` 양쪽에서 같다고 한다.[^issue-5667]
`module.to("tpu")`가 공유 가중치를 풀어서
Qwen3-0.6B의 텐서가 310개가 아니라 311개가 되었고,
학습기와 생성기가 조용히 어긋났다는 보고도 있다.[^issue-4897]
`nonzero`가 새 입력 길이마다 약 1.2초씩 컴파일되고
Whisper의 타임스탬프 처리기에서 호출마다 약 1.6초가 걸렸다는 보고는
문서가 말한 데이터 의존 모양의 비용을 숫자로 보여 준다.[^issue-5085]

이 보고들이 문서의 450개 ATen 연산 지원이나
5,000개 모델 지속 검증이라는 주장을 반박하지는 않는다.
다만 지원 연산의 수가 학습 모드의 상태 갱신이나 장치 이동 때의 객체 동일성 같은
의미론까지 보증하지 않는다는 것은 보여 준다.
도입을 검토하는 쪽은 문서의 한계 표와 함께 열린
이슈를 자기 워크로드의 연산과 대조해야 한다.

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
AnotherGoodName은 많은 사람이 CUDA를 해자라고 믿었지만
이제 소프트웨어 쪽에서 동등한 스택으로 옮겨 가는 것은 꽤 쉬워졌다고
썼고,[^AnotherGoodName-cuda]
jacquesm은 이런 공개가 나올 때마다 CUDA의 우위가 조금씩 깎이지만
하드웨어를 구하기 어려운 것은 여전하다고 보았다.[^jacquesm]
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

### 번역해야 하는 것은 연산이 아니라 PyTorch의 암묵적 가정이다

메모리 모델 문서가 그리는 구도는 이렇다.
PyTorch는 바이트 배열과 포인터, stride, 제자리 쓰기를 전제로 자랐고
XLA는 타입과 모양이 있는 불변 값을 전제로 한다.
TorchTPU는 그 사이에 TPU 버퍼의 메타데이터를 담은 한 겹을 끼워
view decomposition과 functionalization,
buffer donation으로 둘을 잇는다.[^memory]
이 층은 비용과 위험이 모이는 곳이기도 하다.
문서가 성능 지침으로 든 것은 모두 이 층에서 나오고
(뷰는 비싸다, 큰 텐서의 슬라이스에 쓰면 전체가 복사될 수 있다),
이슈 목록에서도 같은 지점이 눈에 띈다.
`view_decomposition`을 제목에 단 열린 이슈가 같은 날 셋 올라왔는데,
0차원 뷰와 오프셋, 끝이 크기 1인 stride 뷰,
Dynamo의 동적 재컴파일 때 생기는 입력 뷰를 다루며
세 건 모두 속성 기반 테스트로 찾았다고 적고
있다.[^issue-5671][^issue-5672][^issue-5674]

그렇다면 이식의 어려움은 연산 하나하나의 구현보다
PyTorch가 당연하게 여기는 별칭, 변경,
모양의 규칙을 불변 값의 세계로 옮기는 데서 나온다.
연산 커버리지가 450개라는 숫자는 앞의 것을 재고
성능 격차와 정확성 보고는 뒤의 것에서 나온다.
이 문서의 비유로는 객체와 관계형 데이터베이스를 잇는 ORM과 닮았다.
시작은 쉽고 대부분이 그대로 돌지만,
두 모델이 어긋나는 이음매에서 비용과 버그가 몰린다.
이는 해석이며 두 시스템의 구조를 엄밀히 대응시킨 것은 아니다.

따라서 “한 줄이면 옮겨진다”는 약속과 문서의 지침 사이에는 긴장이 있다.
큰 텐서의 슬라이스 대신 작은 텐서 여러 개를 쓰고, 연속 텐서를 선호하고,
컴파일 함수의 입력을 연속으로 유지하라는 권고는
결국 TPU의 방언으로 PyTorch를 쓰라는 요구이기 때문이다.
이식을 평가할 때 연산 목록이 아니라 자기 코드가 뷰, 제자리 변경, 가변 모양을
얼마나 쓰는지부터 세어 보는 것이 이 구도에서 나오는 점검이다.
이 점검 순서는 이 문서의 제안이고 실제로 옮겨 본 결과로 검증한 것이 아니다.

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

[^pypi]: PyPI, [torch-tpu](https://pypi.org/project/torch-tpu/)

[^apis]: GitHub, [TorchTPU Public APIs](https://github.com/google-pytorch/torch_tpu/blob/main/docs/public_apis.md)

[^pypolicy]: GitHub, [TorchTPU Python Version Support Policy](https://github.com/google-pytorch/torch_tpu/blob/main/docs/developers/python_support_policy.md)

[^exec]: TorchTPU Documentation, [TorchTPU execution model](https://torchtpu.readthedocs.io/en/latest/torchtpu_execution_model/)

[^memory]: TorchTPU Documentation, [TorchTPU and the TPU memory model](https://torchtpu.readthedocs.io/en/latest/torchtpu_memory_model/)

[^dist]: TorchTPU Documentation, [TorchTPU distributed support](https://torchtpu.readthedocs.io/en/latest/distributed_support/)

[^dyn]: TorchTPU Documentation, [Dynamic shapes](https://torchtpu.readthedocs.io/en/latest/dynamic_shapes/)

[^prec]: TorchTPU Documentation, [Manage numerical precision in TorchTPU](https://torchtpu.readthedocs.io/en/latest/numerical_precision/)

[^api]: TorchTPU Documentation, [TorchTPU API Reference](https://torchtpu.readthedocs.io/en/latest/api_reference/)

[^kernels]: TorchTPU Documentation, [TorchTPU custom kernels](https://torchtpu.readthedocs.io/en/latest/custom_kernels/)

[^xprof]: TorchTPU Documentation, [Performance profiling with XProf](https://torchtpu.readthedocs.io/en/latest/performance_profiling_with_xprof/)

[^gke]: TorchTPU Documentation, [Get started with TorchTPU on GKE](https://torchtpu.readthedocs.io/en/latest/get_started_on_gke/)

[^flux]: TorchTPU Documentation, [FLUX optimization](https://torchtpu.readthedocs.io/en/latest/case_studies_flux/)

[^fsdp]: TorchTPU Documentation, [FSDP best practices](https://torchtpu.readthedocs.io/en/latest/case_studies_fsdp/)

[^infer]: TorchTPU Documentation, [Muse Glimmer 30B: autoregressive decoding](https://torchtpu.readthedocs.io/en/latest/case_studies_muse_glimmer_30b_inference/)

[^train]: TorchTPU Documentation, [Muse Glimmer 30B: training](https://torchtpu.readthedocs.io/en/latest/case_studies_muse_glimmer_30b_training/)

[^issue-4411]: GitHub, [DDP + `torch.compile`: graph breaks leave most of the step eager (32% scaling efficiency on 8 chips; a functional all-reduce reaches 93%)](https://github.com/google-pytorch/torch_tpu/issues/4411), 2026-09-29

[^issue-5667]: GitHub, [BatchNorm never updates running_mean/running_var in training mode, in eager and with torch.compile](https://github.com/google-pytorch/torch_tpu/issues/5667), 2026-10-20

[^issue-4897]: GitHub, [`module.to("tpu")` unties tied parameters (each module gets its own `Parameter`)](https://github.com/google-pytorch/torch_tpu/issues/4897), 2026-10-07

[^issue-5085]: GitHub, [`nonzero` takes ~1.2 s to compile for every new input length, and again for every new number of nonzeros](https://github.com/google-pytorch/torch_tpu/issues/5085), 2026-10-09

[^issue-5671]: GitHub, [view_decomposition: IndexError for 0-d view with non-zero storage offset](https://github.com/google-pytorch/torch_tpu/issues/5671), 2026-10-21

[^issue-5672]: GitHub, [view_decomposition: strided view with trailing size-1 dim gets a base larger than its storage](https://github.com/google-pytorch/torch_tpu/issues/5672), 2026-10-21

[^issue-5674]: GitHub, [view_decomposition: NotImplementedError for input views on Dynamo dynamic recompile (independent storage-offset symbol)](https://github.com/google-pytorch/torch_tpu/issues/5674), 2026-10-21

[^mathisfun123]: <https://news.ycombinator.com/item?id=50170003>

[^coredog64]: <https://news.ycombinator.com/item?id=50171812>

[^boulos-coral]: <https://news.ycombinator.com/item?id=50169459>

[^Dr4kn]: <https://news.ycombinator.com/item?id=50176742>

[^atty]: <https://news.ycombinator.com/item?id=50175919>

[^jacquesm]: <https://news.ycombinator.com/item?id=50171463>

[^AnotherGoodName-cuda]: <https://news.ycombinator.com/item?id=50171275>
