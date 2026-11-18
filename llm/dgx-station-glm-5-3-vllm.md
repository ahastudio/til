# DGX Station 두 대로 GLM-5.3 서빙하기

원문: [When One GPU Isn't Enough: Serving GLM-5.3 Across Two NVIDIA DGX Stations with vLLM](https://developer.nvidia.com/blog/when-one-gpu-isnt-enough-serving-glm-5-3-across-two-nvidia-dgx-stations-with-vllm/)

HN 토론: <https://news.ycombinator.com/item?id=50497155> (149점, 72개 댓글)

GN 토론: <https://news.hada.io/topic?id=37221>

## 요약

2026년 11월 13일 NVIDIA 기술 블로그에 기술 마케팅 엔지니어 Fatima Fall이 쓴 튜토리얼이다. GB300 GPU가 든 DGX Station 두 대를 ConnectX-8 RDMA로 이어 vLLM으로 NVIDIA의 GLM-5.3 NVFP4 모델 하나를 서빙하는 과정을 단계별로 안내한다.
이 문서는 글 전문을 읽었다. 직접 따라 하지는 않았고 함께 올라온 영상, 링크된 모델 카드와 플레이북, AIPerf와 vLLM 문서는 열지 못했다. 글에는 NVIDIA가 만든 AI 요약 블록이 붙어 있고 불완전할 수 있다고 표시되어 있다.

전제와 구성은 다음과 같다.

- 모델: Z.ai의 MoE 모델을 양자화한 `nvidia/GLM-5.3-NVFP4`로 총 7,530억 매개변수에 토큰당 활성 400억이다. 체크포인트는 약 464GB로 GB300 한 장의 HBM3e 252GB를 넘어서 CPU 가중치 오프로딩은 끄고 두 대의 GPU 메모리에 나눠 올린다.
- 병렬화: 텐서 병렬(TP) 2로 두 Station이 모든 요청을 함께 계산한다. Station A가 랭크 0으로 API를 서빙하고 Station B는 헤드리스 워커이다. 파이프라인 병렬이나 전문가 병렬 플래그는 없다.
- 준비물: GB300 DGX Station 두 대(Linux, 「Connect Two DGX Stations」 플레이북으로 연결, 두 레일의 GPU 메모리 RDMA 시험), 양쪽 같은 사용자 이름과 SSH와 sudo, Docker와 NVIDIA Container Toolkit, 각 Station에 464GB 이상의 여유 디스크, 모델 라이선스 수락, Hugging Face 읽기 토큰과 게이트된 데이터셋 `cais/hle` 접근이다.

## 따라 하는 순서

### 1. 두 Station 준비

`~/glm53.env`에 `RANK`, `HEAD_IP`, `WORKER_IP`, `RAIL_IFACE`(예 `cx8r1`), `RAIL_HCA`(예 `mlx5_1`), 이미지 `vllm/vllm-openai:v0.30.0-aarch64`(sha256 다이제스트로 고정), `MODEL_REPO`, `MODEL_REV`, `MODEL_HOST`, `CONTAINER`, `PORT=8000`을 둔다. 예시 IP는 A가 `192.168.101.1`, B가 `192.168.101.2`이다.
점검은 `ethtool`(링크 400,000Mb/s), MTU 9000, 점보 프레임 ping(`-M do -s 8972`), `timedatectl`(시간 동기), `nvidia-smi`(GB300에 계산 프로세스 없음)이다.

### 2. 모델 내려받기와 복사

양쪽에서 고정된 이미지를 받고 A에서 컨테이너 안으로 `hf download`한다(1Gb/s에서 약 1시간, 10Gb/s에서 약 6분). B로는 `rsync -aH`로 SSH 너머 복사하며 A에서 B로 비밀번호 없는 SSH가 필요하다. 재양자화는 하지 않고 두 디스크가 전체 체크포인트를 가지며 vLLM이 로드 때 샤딩한다. 검증은 파일 목록과 크기 비교, `model-*-of-00050.safetensors` 50개, 아키텍처 `GlmMoeDsaForCausalLM`, 양자화 `MIXED_PRECISION` 확인 뒤 `MODEL_READY`를 출력한다.

### 3. 분산 서비스 실행

`~/launch-glm53.sh`를 B 먼저 A 나중에 실행한다. 글이 강조하는 설정은 `--max-model-len 98304`(입력과 출력 합)와 `--gpu-memory-utilization 0.93`이다. 주요 플래그는 다음과 같다.

| 구분        | 설정                                                                                                                                                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 병렬        | `--nnodes 2`, `--node-rank`, `--master-port 29501`, `--tensor-parallel-size 2`(B는 `--headless`)                                                                                                                          |
| 추측 디코딩 | MTP, `num_speculative_tokens` 4                                                                                                                                                                                           |
| 커널        | `moe_backend` `flashinfer_cutlass`, `enable_flashinfer_autotune` 끔                                                                                                                                                       |
| 컴파일      | `cudagraph_mode` `FULL_DECODE_ONLY`, 캡처 크기 5, 10, 20, 40, 80                                                                                                                                                          |
| 기타        | `--max-num-batched-tokens 8192`, `--block-size 128`, `--max-num-seqs 16`, `--kv-cache-dtype fp8`, `--enable-prefix-caching`, `--distributed-timeout-seconds 1800`, `--tool-call-parser glm47`, `--reasoning-parser glm47` |

Docker는 `--network host`, `--ipc host`, `--shm-size 32g`, `--device /dev/infiniband`, `IPC_LOCK` 권한을 쓴다. NCCL 환경 변수로 `NCCL_IB_TIMEOUT=22`, `NCCL_IB_RETRY_CNT=7`, `NCCL_NET_GDR_LEVEL=5` 등을 두고 이미지의 NCCL 2.30.7을 쓴다. 글은 더 오래된 NCCL이 RoCE 위의 노드 간 CUDA 그래프 재생에서 교착될 수 있다(vLLM 이슈 52504)고 적는다.
MTP는 단계마다 토큰 4개를 초안으로 만들고 전체 모델이 검증하며 이득은 수용률에 달려 있다. FP8 KV 캐시는 캐시 메모리를 절반으로 줄이고 접두사 캐싱은 반복되는 프롬프트 앞부분의 재처리를 피한다. 준비는 로그의 `Application startup complete`로 확인한다.

### 4. 서비스 확인과 요청

`/health`가 `HEALTH_OK`를 내는지, NCCL 로그에 `NET/IB`와 `GPU Direct RDMA Enabled`가 있고 `NET/Socket`, `NCCL WARN`, `NCCL ERROR`가 없는지(`RDMA_CHECK_OK`), `nvidia-smi`에 A에서 `VLLM::Worker_TP0`, B에서 `VLLM::Worker_TP1`이 보이는지 본다. GPU당 가중치는 약 218GiB이고 요청이 없을 때 사용 메모리는 A 231.35GiB, B 231.34GiB(가중치와 KV 캐시와 버퍼 포함)이다.
예시 요청은 온도 0, `max_tokens` 4096, `reasoning_effort` `low`이고 분기별 판매량으로 Q1에서 Q2의 변화율 50%를 구하게 한다. `reasoning_effort`는 low, high, max를 받으며 높을수록 추론이 길고 지연이 늘며 도구 호출은 OpenAI 도구 API로 된다.

### 5. 동시성 시험과 자원 해제

AIPerf 0.12.0을 별도 가상 환경에 설치하고 SPEED-Bench Coding(대화 80개, 턴 89개)을 NeMo Skills `prepare.py`로 준비한다. 동시성 1, 8, 16, 32에서 워밍업 3×C, 측정 10×C 요청, 출력 상한 8,192, 기본 `reasoning_effort` `max`로 잰다. 정리는 A 다음 B 순서로 `docker stop --timeout 60`이다.

| 동시성 | 전체 처리량(tok/s) | 평균 지연 | 평균 첫 토큰 시간 | 토큰 간 지연 |
| ------ | ------------------ | --------- | ----------------- | ------------ |
| 1      | 107.4              | 49.84초   | 479.75ms          | 8.78ms       |
| 8      | 386.0              | 114.17초  | 433.79ms          | 19.01ms      |
| 16     | 607.8              | 136.46초  | 482.90ms          | 23.77ms      |
| 32     | 385.0              | 453.54초  | 899.36ms          | 77.90ms      |

사용자별 평균 처리량은 동시성 1에서 115.3, 8에서 53.0, 16에서 42.4, 32에서 13.0 tok/s이다. 처리량에는 추론 토큰이 포함되고 접두사 캐싱을 켠 결과이다. 전체 처리량은 16에서 최고이고 32에서 떨어진다. 표를 재현하려면 `--max-num-seqs`를 16이나 32로 바꾸고 컨테이너를 다시 만들어야 한다.

## 글이 적은 주의 사항

- 서버가 `--host 0.0.0.0`과 `--network host`로 인증 없이 A의 모든 인터페이스에 노출되므로 더 넓게 쓰기 전에 방화벽, 인증, TLS를 더해야 한다.
- 어느 GPU도 전체 모델을 갖지 못해 단독으로 답할 수 없고 토큰마다 두 랭크가 RoCE로 통신한다.
- KV 캐시는 모든 진행 중 요청이 나누므로 길거나 많으면 메모리가 부족할 수 있다. 줄이려면 `--max-model-len`을 낮추거나 요청을 줄인다.
- 벤치마크는 접두사 캐싱을 켠 SPEED-Bench Coding 조건이고 끄면 성능이 다를 수 있다. 자기 프롬프트로 AIPerf를 다시 돌려 보라고 한다. 전체 스윕은 몇 시간이 걸린다.

## 비평

### 헤드라인 수치는 총처리량이다

제목급 수치 607.8 tok/s는 동시성 16에서의 전체 처리량이다. HN에서 한 사용자가 헤드라인이 단일 사용자 수치인지 묻자, 다른 사용자는 단일 사용자는 107 tok/s이고 607은 16명의 합계라 사용자당 35에서 40 tok/s 정도라고 답했다.[^k0morebi][^osamagirl69]
글 본문의 그림은 동시성 16에서 사용자별 42.4 tok/s를 보여 준다.

### 경제성에 대한 회의가 크다

HN에서 한 사용자는 DGX를 10만 달러, 출력 100만 토큰당 1.4달러로 가정하면 최대 가동에서도 투자 회수에 약 7년이 걸려 개인정보 같은 목적이 아니면 경제성이 없다고 계산했다.[^hkalbasi] 다른 사용자는 출력이 4.4달러이고 입력과 캐시 입력 단가가 따로 있다고 가격표를 바로잡으며 다시 계산했다.[^liuliu]
이에 어떤 사용자는 상용 API 승인에 수년이 걸리는 통제된 환경(은행, 의료, 기밀)에서는 쓸모가 있다고 했다.[^lumost] 소음과 전력(각 1.6kW)이 가정이나 소규모 사업에는 과하다는 지적도 있었고,[^anothergoodname] 반대로 1.6kW는 유도 가열 조리기 정도라는 반응도 있었다.[^killingtime74]
이는 모두 개인의 계산이며 글 자체는 경제성을 다루지 않는다.

### 하드웨어 대안과의 비교가 없다

한 사용자는 4비트 모델을 RTX PRO 6000 8장으로 절반 가격에 서빙한 사례가 처리량이 60% 높다고 링크했다.[^jbellis] 글은 다른 구성과 비교하지 않는다. 이 문서는 해당 링크를 열지 못했다.

### 한계가 글의 전제에 있다

NVFP4 양자화된 NVIDIA 체크포인트, 특정 이미지 다이제스트, 특정 NCCL 버전, 게이트된 데이터셋에 의존한다. 사용자가 다른 모델이나 하드웨어로 옮길 때 어느 설정이 일반적인지 글은 구분하지 않는다. 글의 첫 문장의 문법을 지적하는 댓글도 있었다.

### 외부 반응

HN 글 제목은 「Serving GLM-5.3 at 607.8 tok/s across two Nvidia DGX stations with vLLM」이다.
Lobste.rs의 `developer.nvidia.com` 도메인에는 이 글이 없었고 `GLM` 검색에도 이 글이 없었다.
GeekNews 토픽에는 HN 의견을 옮긴 GN⁺ 블록만 있고 이용자가 쓴 댓글은 없었다.

## 기억할 원칙

- 한 GPU에 모델이 들어가지 않으면 텐서 병렬로 두 장비를 한 엔드포인트로 묶고, 이때 모든 토큰이 노드 간 통신을 거친다는 점을 지연의 기준에 둔다.
- 처리량 수치를 볼 때는 동시성, 사용자별 값, 추론 토큰 포함 여부, 접두사 캐시 여부를 같이 확인한다.
- 설정을 바꿀 때는 한 번에 하나씩 바꾸고 다시 시험한다. 이미지와 모델 리비전을 고정한다.
- 인증 없는 `0.0.0.0` 서버는 방화벽과 인증과 TLS를 갖추기 전에 열지 않는다.
- 경제성은 자기 사용량과 상용 API 단가, 전력과 운영 비용으로 따로 계산한다.

---

[^k0morebi]: <https://news.ycombinator.com/item?id=50498596>

[^osamagirl69]: <https://news.ycombinator.com/item?id=50498800>

[^hkalbasi]: <https://news.ycombinator.com/item?id=50497485>

[^liuliu]: <https://news.ycombinator.com/item?id=50499366>

[^lumost]: <https://news.ycombinator.com/item?id=50497577>

[^anothergoodname]: <https://news.ycombinator.com/item?id=50497941>

[^killingtime74]: <https://news.ycombinator.com/item?id=50505723>

[^jbellis]: <https://news.ycombinator.com/item?id=50497443>
