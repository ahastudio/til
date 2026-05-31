# tiny-vllm - C++/CUDA로 직접 만드는 LLM 추론 엔진

<https://github.com/jmaczan/tiny-vllm>

## 소개

tiny-vllm은 jmaczan(Jędrzej Maczan)이 운영하는 GitHub 저장소로,
vLLM의 축소판을 C++17과 CUDA로 처음부터 구현하는 동시에 그 과정을
한 권의 강의로 함께 제공한다. 저자는 “고성능 LLM 추론 엔진을 직접
만들면서 아이디어와 수식을 처음부터 유도해 본다”는 학습 철학을 명시한다.
저장소 README가 곧 강의 본문이며, 두 가지 형태로 동시에 사용된다 —
실행 가능한 추론 서버의 전체 소스 코드, 그리고 그 코드를 한 줄씩
설명하는 교재.

추론 엔진이 구현하는 기능 목록은 다음과 같다. Safetensors에서 실제
LLM(Llama 3.2 1B Instruct) 가중치 로드, prefill + decode 전체 forward
pass, 모든 연산을 CUDA 커널로 작성, KV 캐시, static batching, continuous
batching, online softmax(FlashAttention 유사), PagedAttention. 외부
의존성은 단일 헤더 JSON 파서 `nlohmann/json` 하나뿐이다. 개발 환경은
Linux + CUDA Toolkit 13.1 + GCC 15.2.1 + RTX 5090.

## 강의 구성

목차는 LLM 추론 엔진의 모든 레이어를 빠짐없이 훑는다. Safetensors
형식 파싱, bfloat16의 비트 레이아웃, GPU vs CPU 메모리, 토크나이저,
임베딩, RMSNorm과 CUDA의 parallel reduction, RoPE, residual connection,
`cublasGemmEx`, column-major↔row-major 전치 트릭, prefill vs decode,
KV 캐시의 존재 이유, attention, GQA(Grouped Query Attention), SiLU,
softmax, causal mask, argmax, feed forward network, buffer 재사용,
static batching, continuous batching, online softmax, PagedAttention과
paged KV cache, PagedAttention CUDA 커널.

저자는 다른 학습 자원과의 경계를 명시적으로 그어준다. 학습 단계는
다루지 않으며 Karpathy의 nanoGPT, llm.c, micrograd를 가리킨다. 텐서
라이브러리 내부 구현은 tinygrad를 권한다. GPU 커널 학습 커뮤니티로는
Mark Saroufim의 GPU MODE Discord를 추천한다. 즉 학습/텐서 라이브러리/
추론을 세 영역으로 분리하고, 자신은 추론에만 집중한다.

## 명세

### 대상 모델 - Llama 3.2 1B Instruct

저자는 일부러 단일 모델을 골랐다. 모델 일반화를 처음부터 추구하지 않고
Llama 3.2 1B Instruct에 맞춰 코딩한 뒤 필요하면 일반화하라고 권한다.
모델 구조는 `LlamaForCausalLM` 덤프로 노출된다. 임베딩 vocab 128,256,
hidden size 2048, 16개 디코더 레이어, q_proj 2048×2048, k_proj/v_proj
2048×512(GQA로 key/value 차원 축소), MLP의 gate/up/down projection은
2048↔8192, RMSNorm eps 1e-5, RoPE 사용. 가중치는 BF16.

### 연산 순서

저자는 Sebastian Raschka의 LLM 아키텍처 갤러리 그림을 인용하면서
Llama 3.2 1B의 연산 순서를 글로 풀어 쓴다. 텍스트 → 토큰화 → 임베딩
조회 → 16개 트랜스포머 블록(RMSNorm → residual → masked GQA(Q/K/V
projection, RoPE, attention score, causal mask, softmax, V projection
곱) → O projection → residual → RMSNorm → FFN(gate/up projection, SiLU,
down projection, residual)) → 최종 RMSNorm → linear output → argmax.

### 메모리·배칭 전략의 점진적 도입

강의는 가장 단순한 단일 토큰 추론에서 시작해 KV 캐시, static batching,
continuous batching, online softmax, PagedAttention 순으로 누적한다.
각 단계는 직전 단계의 한계를 동기로 도입된다. 이 순서가 곧 vLLM
혁신의 시계열 순서와 일치한다 — KV 캐시 → continuous batching →
FlashAttention → PagedAttention.

## 분석

### “이해를 위한 재구현(reimplementation for understanding)” 장르의
한 사례

tiny-vllm은 Karpathy의 nanoGPT, llm.c, micrograd, George Hotz의 tinygrad가
대표하는 “이해를 위한 재구현” 장르에 속한다. 핵심은 “라이브러리 사용자에서
멈추지 말고 그 라이브러리를 직접 만들어보라”는 학습 철학이다. 저자도
이 계보를 본문에서 명시적으로 인용한다. tiny-vllm의 기여는 이 장르를
학습(training)에서 추론(inference)으로 옮긴 데 있다. 학습은 nanoGPT·llm.c가
이미 채웠지만, 추론 엔진의 내부는 산업용 도구(vLLM, TensorRT-LLM,
TGI)의 형태로만 존재해 학습 자료가 부족했다.

### vLLM 혁신의 학습 친화적 재배열

vLLM의 핵심 혁신인 PagedAttention(2023, SOSP), continuous batching,
KV 캐시 관리는 산업 논문 형태로는 접근성이 떨어진다. tiny-vllm은 이
혁신들을 “단순한 것 → 복잡한 것” 순서로 재배열하면서 각 단계가
이전 단계의 어떤 비효율을 푸는지 동기 부여한다. 이는 [[recent-llm-architectures]],
[[vllm-recipes]]가 다룬 vLLM 흐름의 학습 가능한 재해석이다.

### 단일 GPU·단일 모델·단일 의존성이라는 의도적 좁힘

저장소가 외부 의존성을 `nlohmann/json` 단 하나로 좁히고, 모델을 Llama
3.2 1B로 고정하고, GPU를 NVIDIA(CUDA)로 한정한 결정은 학습 자원으로서의
응집성을 극단까지 끌어올린다. PyTorch, ONNX, ROCm, MLX, 멀티 GPU 같은
변수를 모두 닫음으로써 “이 한 가지를 끝까지 한다”라는 학습 경로가
가능해진다. 이는 [[bijou64]] 글에서 본 “정규성을 포맷에 내장하라”와
같은 정신을 학습 설계에 적용한 사례다. 변수를 닫으면 학습이 단순해진다.

### CUDA·C++의 선택이 가르치는 두 번째 교훈

저자는 C++/CUDA 선택의 이유를 “하드웨어 효율을 최대로 짜내기 위해서”라고
설명한다. 그러나 학습 도구로서의 의미는 더 크다. Python + PyTorch는
모든 디테일을 추상화하므로 학습자가 “왜 빠른가”를 이해하지 못한다.
CUDA 커널을 직접 짜면 분기 발산(warp divergence), 메모리 합치기
(coalescing), 공유 메모리(shared memory)의 의미를 몸으로 배운다.
즉 “느린 추론을 만든 뒤 빠르게 만드는 과정”이 학습의 1차 컨텐츠가
된다. 이는 [[kog-inference-engine]]이 다룬 “마이크로초 회계”와 같은
근육을 기른다.

## 비평

### 강점 - 학습용 코드와 강의 본문이 같은 저장소에 통합되어 있다

저장소가 코드와 교재를 분리하지 않고 README에 통합한 점은 유지 보수
관점에서 강력하다. 코드가 갱신될 때 교재가 같은 PR로 갱신될 가능성이
높다. 보통의 책-코드 쌍은 책이 정적이고 코드가 빠르게 진화해 둘이
어긋난다. tiny-vllm은 이 어긋남을 구조적으로 줄인다.

### 약점 - NVIDIA 락인

CUDA를 1차 타깃으로 잡은 결정은 학습 응집성을 위해서는 합리적이지만,
AMD ROCm, Apple Metal, Intel oneAPI를 함께 다루지 않는다는 한계가 있다.
2026년 시점 GPU 시장은 NVIDIA 외 옵션이 의미 있게 늘어났는데
([[kog-inference-engine]]의 MI300X 사례), 학습 자원이 NVIDIA만 다루면
독자의 직장 환경과의 거리가 생길 수 있다.

### 약점 - 모델 일반화의 회피

Llama 3.2 1B 단일 모델 고정은 학습 응집성에는 좋지만, 실제 추론 엔진의
가장 큰 난제 — 다양한 모델 아키텍처(MoE, Mamba, hybrid attention)를
일반화하는 설계 — 는 다루지 않는다. 저자도 이를 인정하지만, 학습자가
이 한계를 의식하지 않으면 “나는 추론 엔진을 안다”라는 잘못된 자신감을
얻을 위험이 있다.

### 약점 - 평가·벤치마크의 부재

엔진이 “고성능”을 표방하지만 throughput, latency, tokens/s, MBU 같은
정량 지표가 README에 명시되지 않는다. 학습 자료로서는 “구현 정확성”이
1차 목표라 합리적이지만, “high performance”를 표방하는 이상 vLLM/
TensorRT-LLM 대비 어디에 있는지 비교가 있어야 학습자가 자기 구현의
위치를 알 수 있다.

### 약점 - 동시성·서버 측 도전 과제의 가벼움

continuous batching까지는 다루지만, 추론 서버의 산업적 도전 과제 —
요청 큐잉, 우선순위, 멀티 GPU 토폴로지, 캐시 정책, 장애 복구, 멀티
테넌시 — 는 표면적이다. vLLM은 단순한 PagedAttention 라이브러리가
아니라 거대한 서빙 시스템이다. tiny-vllm은 그 “엔진” 부분만 다루며,
이 경계가 더 명확히 표시되면 좋다.

## 인사이트

### 학습 자원의 새 1급 형식은 “저장소 = 교재”다

전통적인 컴퓨터 과학 학습 자원은 책과 코드를 분리했다. Tanenbaum의
Modern Operating Systems와 MINIX, Knuth의 TAOCP와 MIX 가상 머신처럼
책이 1차 자료, 코드는 부록이다. 2010년대 GitHub의 부상은 이 비율을
바꿨고, 2020년대 Karpathy의 nanoGPT가 결정적으로 뒤집었다. 이제 코드
저장소 자체가 1차 학습 자료이고, README가 교재 본문이다. tiny-vllm은
이 흐름의 한 데이터 포인트다.

이 형식은 세 가지 이유로 강하다. 첫째, 코드와 설명이 같은 커밋 히스토리에
묶여 버전 드리프트가 줄어든다. 둘째, 학습자가 코드를 fork·clone·실행할
때 별도 설치 단계가 없다. 셋째, 학습자가 자기 변경을 PR로 보낼 수
있어 교재 자체가 협력적으로 발전한다. 책으로는 불가능한 “학습자 →
저자” 피드백 루프가 자연스럽게 작동한다.

여기서 도출되는 함의는 학술 출판의 미래에 대한 것이다. 책의 1차 가치였던
“정제된 글”은 LLM이 자동으로 생성·요약하는 시대에 상대적 가치가 줄어든다.
반면 “실행 가능한 코드 + 그 코드에 정합한 설명”은 LLM이 자동 합성하기
훨씬 어렵다. 코드는 컴파일·실행·테스트라는 검증 가능한 기반을 가지므로
저자의 신뢰가 그 위에 직접 쌓인다. 미래의 학습 자원은 점점 더 저장소
중심이 될 것이다.

세 번째 함의는 평가의 변화다. “이 저자는 신뢰할 만한가?”의 답이 “이 저자의
저장소가 동작하는가?”로 환원된다. 학위·소속·논문 인용수 대신 “스타 수,
PR 수, 빌드 통과 여부”가 평가 척도가 된다. 이는 학습 자원 생태계의
탈권위화를 의미한다. Karpathy 같은 개인이 대학을 우회해 수십만 명의
학습자를 직접 가르치는 경로가 표준이 된다.

### 추론 엔진은 새 운영체제다

tiny-vllm의 목차를 보면 단순한 “수학 구현”이 아니라 운영체제 교과서와
같은 주제들이 등장한다. 메모리 관리(KV 캐시, paged attention),
스케줄링(continuous batching), I/O(safetensors 파싱), 동시성(CUDA
parallel reduction), 자원 관리(buffer reuse). 즉 LLM 추론 엔진은
“커스텀 운영체제”에 가깝다. 단지 그 운영체제가 관리하는 자원이 프로세스가
아니라 토큰이고, 코어가 아니라 SM(Streaming Multiprocessor)이라는 차이만
있다.

이 관찰은 산업 인프라의 진화 방향을 시사한다. 1990년대 운영체제(Linux)가
인프라의 1차 추상화였다면, 2010년대는 컨테이너 오케스트레이션(Kubernetes)이,
2026년대는 추론 엔진(vLLM, TensorRT-LLM, KIE)이 그 자리를 차지하고 있다.
각 시대의 “OS”는 그 시대의 1차 자원을 관리한다. 60년대 메인프레임의
OS는 CPU 시간을, Linux는 멀티프로세스를, Kubernetes는 컨테이너를,
vLLM은 토큰 생성 슬롯을 관리한다.

여기서 도출되는 두 번째 함의는 추론 엔진 엔지니어가 새 운영체제
엔지니어의 위상을 가진다는 것이다. 1990년대 Linus Torvalds, 2010년대
Kubernetes 코어 컨트리뷰터들이 했던 일을 2026년에는 vLLM/SGLang/TGI
코어 메인테이너들이 한다. 이 직무가 시장에서 희소한 이유는 “시스템
프로그래밍 + ML 수학 + GPU 아키텍처”라는 세 영역의 교차에 있기 때문이다.
tiny-vllm 같은 학습 자원이 이 교차 영역의 신규 엔지니어 공급을 늘리는
구조적 역할을 한다.

세 번째 함의는 추론 엔진 표준화의 부재가 곧 다음 큰 표준화 기회라는
점이다. POSIX가 1980년대에 운영체제를 표준화했고, OCI/CNCF가 2010년대
컨테이너를 표준화했다. 2026년 추론 엔진에는 그런 표준이 없다. 모델 포맷
(GGUF, Safetensors), 양자화 포맷(MXFP4, INT4, INT8), 추론 인터페이스
(OpenAI-compatible, gRPC, vLLM-native)가 모두 파편화되어 있다. 누가
이 표준화를 끌고 갈지가 향후 5년의 핵심 인프라 정치다.

### “단순한 것을 끝까지 만들어보기”가 가장 일반화 가능한 학습 패턴이다

tiny-vllm·nanoGPT·tinygrad가 공유하는 학습 철학은 “하나의 단순한 모델을
처음부터 끝까지 직접 만든다”이다. 이 패턴이 효과적인 이유는 여러
층위로 작동한다. 첫째, 끝까지 만들면 “블랙박스”가 사라진다. 학습자는
중간에 “이건 그냥 받아들이자”라고 넘어가는 부분이 없어진다. 둘째,
처음부터 만들면 추상화의 비용이 보인다. PyTorch가 무엇을 숨겼는지,
vLLM이 어떤 결정을 했는지가 자신의 구현 선택과 대조되어 드러난다.
셋째, 단순한 것을 끝까지 만들면 일반화의 어려움이 보인다. Llama 3.2 1B
하나를 끝까지 만들고 나서야 “이걸 다른 모델로 일반화하는 게 왜 어려운가”를
실감할 수 있다.

이 패턴은 일반적인 학습 이론에도 부합한다. Bloom의 분류에서 “창조하기”가
인지의 최상위 단계이고, Papert의 구성주의(constructionism)는 “만들면서
배운다”를 핵심으로 한다. tiny-vllm은 이 이론들을 LLM 추론이라는 영역에
적용한다. 단지 만드는 것이 “레고”나 “Logo turtle”이 아니라 “산업급
인프라 도구의 미니어처”라는 차이만 있다.

여기서 두 번째 함의는 직업 학습의 미래에 대한 것이다. 대학·부트캠프의
전통적 교육은 “개념 강의 + 과제”의 분리 모델이다. tiny-vllm 형식은
이 분리를 무너뜨린다. 강의가 곧 과제이고, 과제가 곧 강의다. AI 어시스턴트가
보편화되는 시대에 이 통합은 더 강력하다. 학습자가 막힌 지점에서 LLM에
질문하면, LLM은 자기 학습 데이터에 포함된 tiny-vllm 코드를 직접 참조해
답할 수 있다. 즉 “학습 자원이 LLM 학습 데이터에 들어가는 것”이 학습
효과의 새 변수다.

세 번째 함의는 다음 “tiny-X” 자원이 무엇이 될 것인가다. tiny-torch
(텐서 라이브러리), tiny-kubernetes(컨테이너 오케스트레이터),
tiny-postgres(RDBMS), tiny-llvm(컴파일러 백엔드)이 모두 가능한 후보다.
산업에 매우 영향력이 큰 도구일수록, 그 미니어처가 학습 자원으로서의
가치가 크다. 또한 LLM의 코드 생성 능력이 발전하면 이 “tiny-X”를 만드는
초기 비용이 급격히 낮아져, 향후 5년 안에 이 형식의 학습 자원이 폭발적으로
늘어날 가능성이 높다.

### 추론 엔진 학습은 “하드웨어 친화 사고”라는 일반 근육을 기른다

tiny-vllm 같은 자원이 가르치는 가장 큰 일반 가치는 “하드웨어 친화 사고”
라는 메타 스킬이다. 학습자는 CUDA 커널을 짜면서 메모리 합치기, 분기
발산, 공유 메모리, occupancy 같은 개념을 몸으로 익힌다. 이 개념들은
GPU에 한정되지 않는다. CPU의 캐시 라인, 분기 예측, SIMD도 같은 형태의
사고를 요구한다.

이 사고법이 일반화되면 어떤 영역에서도 “데이터 레이아웃이 성능을 결정
한다”라는 본능이 작동한다. 데이터베이스 인덱스 설계, 네트워크 패킷
크기, 직렬화 포맷 선택, 캐시 키 설계 — 모두 같은 근육을 쓴다.
[[bijou64]]의 정규 인코딩 설계가 “현대 CPU의 빅엔디안 연속 영역 친화성”을
의식적으로 활용한 사례, [[kog-inference-engine]]의 monokernel이
“커널 경계 제거”로 GPU를 더 잘 쓴 사례 모두 이 근육의 결과다.

여기서 도출되는 함의는 LLM 시대에 “하드웨어 사고”의 가치가 오히려
올라간다는 역설이다. AI가 코드를 생성하기 시작하면 평균 코드 품질은
평준화되지만, “하드웨어에 맞춰 코드를 다시 짜는” 능력은 평준화되기
어렵다. AI는 평균 패턴을 재생산하므로 “이 워크로드에 맞춰 메모리
레이아웃을 다시 설계”하는 일은 인간 엔지니어의 영역으로 남는다. 즉
tiny-vllm 같은 자원으로 길러진 학습자는 AI 코드 생성기와 보완 관계에
선다.

세 번째 함의는 채용 시장의 신호 변화다. “Python으로 ML 모델을 학습할
수 있는 사람”의 시장 공급이 충분해진 반면, “CUDA로 추론 엔진을 디버깅할
수 있는 사람”의 공급은 부족하다. tiny-vllm 같은 학습 자원을 끝까지
완주한 사람은 이 부족한 시장에 자기를 위치시킬 수 있다. 학습 자원의
사회적 기능은 단순한 지식 전달이 아니라 “시장 가치가 높은 스킬로의
경로 제공”이다. 이는 [[ai-frontend-lost-decade]]에서 본 “디스킬링 시대의
리스킬링 경로”라는 더 큰 흐름의 구체 사례다.
