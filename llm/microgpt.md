# MicroGPT

Andrej Karpathy의 MicroGPT 분석.

- 블로그: <http://karpathy.github.io/2026/02/12/microgpt/>
- 소스코드: <https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95>
- 트윗: <https://twitter.com/karpathy/status/2021694437152157847>

## 개요

순수 Python만으로 GPT를 훈련하고 추론하는 243줄짜리 단일 파일 프로젝트. 외부
의존성(PyTorch, NumPy 등)이 전혀 없다.

> This file is the complete algorithm. Everything else is just efficiency. I
> cannot simplify this any further.

Karpathy의 이전 프로젝트들(micrograd, makemore, nanoGPT 등)을 하나로 응축한
결과물이다. LLM을 본질까지 단순화하려는 10년간의 집착이 담겨 있다.

## 구성 요소

243줄 안에 다음이 모두 들어 있다:

| 구성 요소       | 설명                       |
| --------------- | -------------------------- |
| 데이터셋 로딩   | names.txt 다운로드 및 파싱 |
| 토크나이저      | 문자 단위, BOS 토큰 포함   |
| Autograd 엔진   | Value 클래스 기반 역전파   |
| 신경망 아키텍처 | GPT-2 유사 Transformer     |
| Adam 옵티마이저 | 모멘텀 + 적응적 학습률     |
| 훈련 루프       | 1000 스텝, 토큰 단위 처리  |
| 추론 루프       | temperature 샘플링         |

## 아키텍처 상세

```python
n_layer    = 1      # Transformer 레이어 수
n_embd     = 16     # 임베딩 차원
block_size = 16     # 최대 시퀀스 길이
n_head     = 4      # 어텐션 헤드 수
head_dim   = 4      # 헤드당 차원 (n_embd / n_head)
```

총 파라미터 수: **4,192개**. GPT-4급 모델이 수천억 개인 것과 비교하면 구조는
같되 규모만 극단적으로 작다.

### 모델 구조

```txt
입력 토큰
  → 토큰 임베딩 + 위치 임베딩
  → RMSNorm
  → Multi-Head Attention (QKV + Output projection)
  → Residual Connection
  → RMSNorm
  → MLP (FC1 → ReLU → FC2)
  → Residual Connection
  → lm_head (로짓 출력)
```

프로덕션 GPT와 동일한 뼈대다. LayerNorm 대신 RMSNorm을 사용한 점이 눈에 띈다.
이는 LLaMA 계열에서 채택한 방식이기도 하다.

## Autograd 엔진

`Value` 클래스 하나로 자동 미분을 구현한다.

```python
class Value:
    __slots__ = (
        'data', 'grad', '_children', '_local_grads'
    )
```

지원 연산: `+`, `*`, `**`, `exp`, `log`, `relu`. `backward()` 메서드가 위상
정렬(topological sort)로 계산 그래프를 역순 순회하며 그래디언트를 전파한다.

PyTorch의 `torch.autograd`가 하는 일을 50줄 남짓으로 재현한 것이다.

## KV 캐시: 핵심 인사이트

MicroGPT의 가장 흥미로운 설계 결정은 **훈련 중에도 KV 캐시를 사용**하는 것이다.

보통 KV 캐시는 추론 최적화 기법으로만 알려져 있다. 하지만 개념적으로 KV 캐시는
항상 존재한다. 프로덕션 구현에서는 고도로 벡터화된 어텐션 연산 내부에 숨겨져
있을 뿐이다.

MicroGPT는 토큰을 한 번에 하나씩 처리하므로 KV 캐시를 명시적으로 구축한다.
일반적인 추론과 다른 점은 캐시된 Key/Value가 계산 그래프의 살아있는 `Value`
노드라는 것이다. 따라서 역전파가 캐시를 통해서도 진행된다.

```python
keys[li].append(k)    # 계산 그래프에 연결된 상태
values[li].append(v)  # backward()가 여기도 통과
```

이 설계 덕분에 배치 차원이나 병렬 시간 스텝 없이도 정확한 그래디언트를 계산할 수
있다.

## 프로덕션 GPT와의 차이

| 항목        | MicroGPT    | 프로덕션 GPT     |
| ----------- | ----------- | ---------------- |
| 파라미터    | 4,192       | 수천억           |
| 임베딩 차원 | 16          | 10,000+          |
| 레이어 수   | 1           | 100+             |
| 토크나이저  | 문자 단위   | BPE (수만 토큰)  |
| Autograd    | 순수 Python | CUDA 커널        |
| 배치 크기   | 1           | 수천             |
| 데이터      | names.txt   | 수조 토큰        |
| 정규화      | 없음        | Dropout 등       |
| 의존성      | 없음        | PyTorch, CUDA 등 |

차이는 전부 **효율성**에 관한 것이다. 알고리즘 자체는 동일하다.

## 인사이트

### 1. 복잡성의 본질은 규모이지 구조가 아니다

243줄로 GPT의 전체 알고리즘을 표현할 수 있다는 것은 LLM의 핵심 아이디어가
놀랍도록 간결하다는 뜻이다. 수십만 줄의 프로덕션 코드는 대부분 효율성을 위한
것이다. CUDA 커널, 분산 훈련, 메모리 최적화, 데이터 파이프라인. 알고리즘 자체는
단순하다.

### 2. KV 캐시는 추론 트릭이 아니라 본질이다

KV 캐시를 훈련에서도 사용한다는 설계는 "추론 최적화 기법"이라는 통념을 깨뜨린다.
어텐션 메커니즘에서 이전 토큰의 Key/Value를 재사용하는 것은 알고리즘의 본질적
구조다. 프로덕션 코드에서는 행렬 연산으로 한 번에 처리해서 캐시가 명시적으로
드러나지 않을 뿐이다.

### 3. 교육적 가치: "읽을 수 있는" Transformer

PyTorch나 JAX로 작성된 Transformer는 프레임워크의 추상화 뒤에 핵심이 숨겨져
있다. `nn.MultiheadAttention`이 실제로 무엇을 하는지 코드만 봐서는 알기 어렵다.
MicroGPT는 모든 연산이 스칼라 수준으로 풀어져 있어 어텐션이 정확히 어떤 계산인지
한눈에 보인다.

### 4. 단순화의 힘: "더 이상 줄일 수 없다"

> I cannot simplify this any further.

이 선언은 강력하다. 복잡한 시스템의 본질을 찾아내는 능력은 그 시스템을 깊이
이해하고 있다는 증거다. micrograd → makemore → nanoGPT → MicroGPT로 이어지는
단순화의 여정 자체가 하나의 교훈이다.

### 5. Autograd는 생각보다 간단하다

딥러닝 프레임워크의 핵심인 자동 미분이 `Value` 클래스 50줄로 구현된다는 사실은
이 개념의 수학적 우아함을 보여준다. 연쇄 법칙(chain rule)과 위상 정렬만 있으면
된다.

## 커뮤니티 반응

GitHub Gist에 4,800+ 스타, 1,000+ 포크. Common Lisp, C#, JavaScript(브라우저),
Rust 등 다양한 언어로 포팅되었다.

## 관련 문서

- [GPT](./gpt.md)
