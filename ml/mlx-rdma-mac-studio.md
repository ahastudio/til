# Mac Studio 네 대로 816B 모델을 돌린다: MLX와 Thunderbolt RDMA

원문: [Local and Distributed Large LLM Inference with MLX and RDMA on Mac Studio](https://machinelearning.apple.com/research/mlx-distributed-inference)

HN 토론: <https://news.ycombinator.com/item?id=50118320> (284점, 130개 댓글)

GN 토론: <https://news.hada.io/topic?id=35483>

## 요약

Apple 머신러닝 리서치는 2026년 10월 15일,
같은 날 공개한 최신 MLX로 1조 개에 가까운 파라미터를 가진
Muse Spark Open을 책상 위에서 돌리는 방법을 소개했다.
M5 Ultra Mac Studio 네 대 클러스터에서 Muse Spark Open은
초당 36토큰 넘게 생성했고,
Apple은 이것이 사람의 평균 읽기 속도를 훨씬 웃돈다고 말한다.

### 평가 대상

| 모델               | 전체 파라미터 | 활성 파라미터 | 평가 정밀도 |
| ------------------ | ------------- | ------------- | ----------- |
| Muse Spark Open    | 816B          | 42B           | NVFP4       |
| Mistral Medium 3.5 | 128B          | 128B          | FP8         |
| Qwen 3.8           | 27B           | 27B           | BF16        |

Muse Spark Open은 전문가 혼합(MoE) 모델로
원래 BF16이지만 4비트 NVFP4로 평가했고,
나머지 둘은 밀집 모델로 원래 정밀도 그대로 평가했다.
측정은 `mlx_lm.benchmark`로 했고,
첫 토큰까지 걸린 시간(TTFT), 생성 속도, 최대 전력을
8,192토큰과 65,536토큰 컨텍스트에서 쟀다.
에이전트 코딩처럼 긴 컨텍스트가 필요한 용도를 염두에 둔 설정이다.

### 단일 Mac Studio

Qwen 3.8과 Mistral Medium 3.5는 512GB Mac Studio 한 대에 넉넉히 들어가며,
65,536토큰에서 각각 최대 68GB와 158GB를 쓴다.
TTFT는 연산 성능에 좌우되는데,
M5 Ultra GPU의 뉴럴 가속기가 행렬 곱셈을 전담하면서
M3 Ultra보다 최대 4.6배 빨라졌다.
생성 속도는 메모리 대역폭에 좌우되는데,
M5 Ultra의 1.2TB/s 대역폭(M3 Ultra는 819GB/s) 덕에 1.6배 빨라졌다.
최대 전력은 M3 Ultra가 약 200W, M5 Ultra가 약 300W로,
Apple은 이것이 흔한 토스터보다 적어
집이나 사무실 어디에나 둘 수 있다고 강조한다.

Muse Spark Open은 BF16으로는 파라미터만 1.6TB가 넘고,
NVFP4로 줄여도 약 493GB라 추론 중 계산 메모리를 더하면 한 대에 들어가지 않는다.

### 파이프라인 병렬화

모델의 앞쪽 절반 층은 한 대에, 뒤쪽 절반은 다른 한 대에 두고
출력을 넘겨 주는 방식이다.
구현이 아주 간단해 코드 변경이 거의 필요 없다.
macOS 26.2가 Thunderbolt 5 위의 저지연 RDMA 드라이버를 도입했고,
MLX 0.30.1 이상은 그 위에서 동작하는 jaccl이라는 집합 통신 백엔드를 제공한다.
Apple은 대역폭을 두 배로 하려고 두 대를 Thunderbolt 케이블 두 개로 연결했다.

```bash
mlx.launch --hostfile hostfile.json --backend jaccl --env MLX_METAL_FAST_SYNCH=1 -- \
  mlx_lm.benchmark --model mistralai/Mistral-Medium-3.5-128B \
  -p 8192 -g 128 -b 1 --prefill-step-size 8192 --pipeline
```

`MLX_METAL_FAST_SYNCH=1`은 Thunderbolt 통신을 시작하는 CPU와
연산하는 GPU 사이의 동기화를 빠르게 하는 실험 기능이다.
층은 여전히 순서대로 계산되므로
파이프라인 병렬화의 생성 속도는 한 대와 거의 같다.
다만 65,536토큰처럼 긴 컨텍스트에서는 MLX가 프리필을 8,192토큰 단위로 나눠
두 기계가 서로 다른 조각을 겹쳐 처리하므로, 프리필이 최대 약 1.8배 빨라진다.

### 텐서 병렬화

텐서 병렬화는 모델의 너비를 나눠 각 기계가 모든 층의 일부를 갖는다.
층마다 계산이 병렬화되어 빨라지지만,
토큰마다, 층마다 입력을 나눠 보내고 출력을 모으는 작은 통신이 많아서
Thunderbolt RDMA 같은 아주 낮은 지연의 통신이 있어야 효과가 난다.
Mac Studio들은 각 쌍이 케이블 두 개로 직접 연결된 Thunderbolt 메시로 묶였다.

8,192토큰 컨텍스트의 결과는 다음과 같다.

| 모델               | 지표     | M3 Ultra | M5 Ultra | M5 2대 파이프라인 | M5 2대 텐서 | M5 4대 텐서 |
| ------------------ | -------- | -------- | -------- | ----------------- | ----------- | ----------- |
| Muse Spark Open    | TTFT(초) | —        | —        | 8.4               | 8.2         | 4.8         |
| Muse Spark Open    | 토큰/초  | —        | —        | 15.74             | 24.99       | 36.73       |
| Mistral Medium 3.5 | TTFT(초) | 95.9     | 24.6     | 24.5              | 14.4        | 7.5         |
| Mistral Medium 3.5 | 토큰/초  | 4.95     | 7.70     | 7.70              | 13.69       | 23.37       |
| Qwen 3.8           | TTFT(초) | 18.2     | 4.1      | 4.1               | 3.1         | 1.7         |
| Qwen 3.8           | 토큰/초  | 12.46    | 19.69    | 19.44             | 33.27       | 50.89       |

기계 수를 늘렸을 때 속도가 더 잘 오르는 쪽은 밀집 모델이다.
Muse Spark Open은 전문가 출력의 정규화가 프리필 통신을 늘려서,
65,536토큰에서는 2대 텐서 병렬화가 2대 파이프라인보다 느렸다.
그러나 생성 속도에는 영향이 없고 4대가 되면 텐서 병렬화가 효과를 낸다.
4대 M5 Ultra에서 65,536토큰의 Muse Spark Open TTFT는
케이블 한 개일 때 약 50.5초, 두 개일 때 40.6초였다.

### 로컬 에이전트

`mlx_lm.server`로 OpenAI 호환 서버를 띄우고,
`mlx.launch`를 앞에 붙이면 여러 대의 Mac Studio로 나눠 서빙한다.
Apple은 OpenCode의 설정에서 이 로컬 서버를 공급자로 지정하는 예를 보여 준다.

```bash
mlx.launch --hostfile hostfile.json --backend jaccl --env MLX_METAL_FAST_SYNCH=1 -- \
  mlx_lm.server --model meta-models/Muse-Spark-Open-816B-A42B-NVFP4 --port 8080
```

Apple은 지난 1년 동안 M5 GPU 뉴럴 가속기 지원, Thunderbolt RDMA 통신,
MoE 같은 최신 구조의 효율적 구현을 MLX에 더해 왔고,
이것들이 최신 하드웨어와 결합해
800B가 넘는 모델을 로컬에서 실행할 수 있게 되었다고 정리한다.

## 분석

### 연산과 대역폭을 나눠 보는 것이 이 글의 핵심 틀이다

Apple은 성능을 두 축으로 나눠 설명한다.
TTFT는 연산 성능에, 생성 속도는 메모리 대역폭에 좌우된다는 구분이다.
M5 Ultra의 TTFT가 최대 4.6배, 생성 속도가 1.6배 빨라진 차이가
바로 이 구분에서 나온다.
뉴럴 가속기는 프리필의 행렬 곱셈을 크게 줄였지만,
생성은 대역폭이 819GB/s에서 1.2TB/s로 늘어난 만큼만 빨라졌다.

이 틀은 로컬 LLM 하드웨어를 고르는 사람에게 실용적인 기준이 된다.
긴 문서나 큰 코드베이스를 컨텍스트로 넣는 에이전트 작업은
TTFT가 체감 속도를 좌우하고,
짧은 질문에 긴 답을 받는 대화는 생성 속도가 좌우한다.
Apple이 에이전트 코딩을 이유로 65,536토큰을 함께 잰 것도
M5의 강점이 드러나는 쪽을 보여 주려는 선택이다.

### 병렬화 방식의 선택은 모델 구조와 컨텍스트 길이에 달려 있다

파이프라인 병렬화는 메모리를 늘려 줄 뿐 생성 속도를 올리지 않는다.
텐서 병렬화는 속도를 올리지만 통신이 많아 저지연 연결이 필수다.
그리고 MoE 모델은 전문가 출력 정규화 때문에 통신이 더 늘어,
두 대에서는 긴 컨텍스트 프리필이 오히려 파이프라인보다 느렸다.

결국 몇 대를 어떻게 묶을지는 모델 하나로 정해지지 않는다.
모델이 한 대에 들어가는지, 밀집인지 MoE인지, 컨텍스트가 얼마나 긴지에 따라
최선의 구성이 달라진다.
Apple의 표는 이 선택을 위한 측정값이지만,
글 자체는 선택 기준을 정리해 주지 않으므로 독자가 표에서 읽어 내야 한다.

### 데이터센터의 기술을 데스크톱 케이블로 옮겼다

RDMA는 원래 InfiniBand나 RoCE처럼 데이터센터 네트워크에서
분산 학습과 추론을 받치던 기술이다.
Apple은 이것을 Thunderbolt 5 케이블에 올렸고,
케이블 두 개로 대역폭을 늘리고 기계끼리 직접 메시로 엮었다.
스위치 없이 케이블만으로 네 대를 묶는 구성이라
네트워크 장비를 따로 살 필요가 없다.

이는 Apple이 소비자용 포트와 운영체제 드라이버만으로
작은 클러스터를 만들 수 있게 했다는 뜻이다.
케이블 수가 기계 수에 따라 빠르게 늘어나는 메시 구조라
네 대 정도가 현실적인 상한이라는 점도 함께 읽어야 한다.

## 비평

### 비용을 말하지 않는 벤치마크는 절반의 정보다

글은 성능과 전력은 자세히 적지만 가격은 한 번도 언급하지 않는다.
512GB M5 Ultra Mac Studio 네 대와 Thunderbolt 케이블 메시의 비용은
같은 돈으로 쓸 수 있는 API 사용량이나 GPU 서버 임대료와 비교해야
“책상 위에서 돌린다”는 말의 의미가 분명해진다.
초당 36토큰은 사람이 읽기에는 충분하지만,
에이전트가 수십 번 도구를 부르며 긴 출력을 만드는 작업에는 느릴 수 있다.

전력 비교도 같은 문제를 안고 있다.
300W가 토스터보다 적다는 비교는 한 대 기준이고,
네 대 클러스터는 약 1.2kW다.
여전히 데이터센터 GPU보다는 적지만,
“어느 집이나 사무실에나 둘 수 있다”는 문장은 한 대에 대한 것이다.
HN의 throwworhtthrow는 토스터 비교를 짚었고,[^throwworhtthrow]
porridgeraisin은 자기도 토스터를 몇 시간씩 돌린다고 비꼬았다.[^porridgeraisin]
토스터는 몇 분 켜는 기기이고 추론 서버는 하루 종일 켜 두는 기기다.
순간 최대 전력을 비교하는 것은 누적 전력 소비를 가린다.

### 배치 1 측정은 서빙 시나리오를 대표하지 않는다

모든 측정은 `-b 1`, 즉 요청 하나를 처리하는 조건이다.
개인이 혼자 쓰는 경우에는 맞는 설정이지만,
팀이 함께 쓰는 로컬 서버나 여러 에이전트를 동시에 돌리는 경우에는
동시 요청에서의 처리량이 더 중요하다.
GPU 서버는 배치를 키워 처리량을 크게 늘리는데,
Mac Studio 클러스터가 같은 방식으로 확장되는지는 이 글에서 알 수 없다.

또 생성 속도는 컨텍스트 뒤에 128토큰을 만드는 동안만 쟀다.
에이전트 코딩처럼 수천 토큰을 생성하는 작업에서는
컨텍스트가 늘어나며 속도가 떨어지는 정도가 중요하지만,
이 측정은 그 부분을 보여 주지 않는다.
HN의 mrboatshoepants도 첫 그래프의 초당 15~36토큰이 8,192토큰 컨텍스트 기준이며,
요즘 쓰기에는 턱없이 짧다고 지적했다.[^mrboatshoepants]

### 정밀도 차이가 비교를 흐린다

Muse Spark Open은 원래 BF16인 모델을 4비트 NVFP4로 평가했다.
나머지 두 모델은 원래 정밀도 그대로다.
4비트 양자화는 메모리와 속도를 크게 줄이지만 품질에도 영향을 줄 수 있다.
글은 Muse Spark Open의 품질이
원래 정밀도와 비교해 얼마나 유지되는지 말하지 않는다.
“최첨단 모델을 책상 위에서”라는 주장에는
양자화한 버전을 실행한다는 단서를 조금 더 앞에 두었어야 했다.
HN의 peri-cl은 Muse Spark Open은 4비트로, Qwen은 BF16으로만 비교한 것이
Qwen을 깎아내리는 구성이고, 대부분의 사용자가 고를 양자화도 아니라고 했다.
그러면서 512GB M5가 있다면
Muse Spark Open은 고려할 상위 10개 모델에도 들지 않는다고 덧붙였다.[^peri-cl]
comandillos도 800B 모델이 다른 300B 모델보다 성능이 훨씬 나쁘다고 했다.[^comandillos]
글이 이 모델을 고른 이유가 성능이 아니라 크기의 상징성에 있었다면,
그 선택은 벤치마크라기보다 시연에 가깝다.

## 인사이트

### 로컬 LLM 하드웨어 경쟁의 축은 메모리 용량으로 옮겨 갔다

Muse Spark Open이 한 대에 들어가지 않는 이유는 연산이 아니라 메모리다.
4비트로 줄여도 493GB가 필요하고, 그래서 512GB 기계도 두 대가 필요하다.
모델이 커질수록 로컬에서 돌릴 수 있는지 여부는
GPU 성능보다 통합 메모리 용량과 기계를 묶는 통신으로 정해진다.

Apple의 통합 메모리 구조는 이 지점에서 유리하다.
소비자용 GPU는 VRAM 용량이 작아 대형 모델을 올리려면 여러 장이 필요하고,
그 사이의 통신이 또 병목이 된다.
HN의 GeekyBear는 같은 모델을 돌리려면 16GB짜리 5080을 몇 장 사야 하느냐고 되물었다.[^GeekyBear]
반대로 liuliu는 256GiB M5 Ultra 한 대로 DeepSeek 4.1 Flash를
프리필 초당 약 3,200토큰, 생성 초당 약 45토큰으로 무리 없이 실행하며,
품질 벤치마크로 공식 수치와 같은 품질이 나오는지도 확인했다고 했다.[^liuliu]
가장 큰 모델이 아니라 한 대에 들어가는 좋은 모델을 고르는 편이
실제 로컬 사용에서는 더 현실적이라는 경험담이다.
Apple이 RDMA를 Thunderbolt에 올린 것은
메모리 용량에서 생긴 우위를 여러 대로 넓히려는 포석이다.

### 오픈 가중치 모델의 크기가 로컬 하드웨어의 수요를 정한다

Apple은 새로 나온 816B 규모의 오픈 가중치 모델 Muse Spark Open을
네 대의 Mac Studio로 돌리는 방법을 MLX 새 버전과 함께 발표했다.
오픈 가중치 모델이 커질수록 그것을 돌릴 하드웨어 수요가 생기고,
하드웨어 회사는 그 모델을 기준 작업으로 삼아 제품을 홍보한다.

이 관계는 앞으로 오픈 가중치 모델의 크기와 구조가
하드웨어 업체의 마케팅 일정과 맞물리게 될 수 있음을 뜻한다.
MoE 모델이 늘어나면 활성 파라미터는 작아도 전체 파라미터가 커서,
메모리 용량을 많이 파는 쪽이 유리해진다.
HN의 ks2048은 Meta가 수십억 달러를 들여 오픈 가중치 모델을 만들면
사람들은 그것을 실행하려고 Apple에 2만 달러를 보낸다며
Apple에는 좋은 거래라고 했다.[^ks2048]
giancarlostoro는 그래도 같은 성능의 NVIDIA GPU 구성보다는 싸다고 했고,[^giancarlostoro]
loeg는 로컬 LLM 시장이 대당 2만 달러짜리 기계를 팔 만큼 크냐고 의문을 제기했다.[^loeg]
macinjosh는 많은 사람이 Apple이 프런티어 연구소와 경쟁해야 한다고 생각했지만
Apple은 스스로를 NVIDIA의 경쟁자로 본다고 정리했다.[^macinjosh]

### 로컬 에이전트의 진짜 시험대는 긴 세션이다

Apple은 OpenCode 설정까지 보여 주며 로컬 에이전트 코딩을 강조했다.
그러나 에이전트 세션은 컨텍스트가 계속 쌓이고, 도구 호출마다 프리필이 반복된다.
65,536토큰에서 4대 클러스터의 Muse Spark Open TTFT가 40.6초라는 것은,
긴 세션 후반부에 도구 호출 한 번마다 그만큼 기다릴 수 있다는 뜻이다.
프롬프트 캐시가 이를 얼마나 줄이는지가
로컬 에이전트가 클라우드 에이전트를 대체할 수 있는지를 가를 것이다.

---

[^throwworhtthrow]: <https://news.ycombinator.com/item?id=50121167>

[^porridgeraisin]: <https://news.ycombinator.com/item?id=50121278>

[^mrboatshoepants]: <https://news.ycombinator.com/item?id=50121823>

[^peri-cl]: <https://news.ycombinator.com/item?id=50119761>

[^comandillos]: <https://news.ycombinator.com/item?id=50120210>

[^GeekyBear]: <https://news.ycombinator.com/item?id=50120128>

[^liuliu]: <https://news.ycombinator.com/item?id=50120882>

[^ks2048]: <https://news.ycombinator.com/item?id=50119897>

[^giancarlostoro]: <https://news.ycombinator.com/item?id=50126910>

[^loeg]: <https://news.ycombinator.com/item?id=50120608>

[^macinjosh]: <https://news.ycombinator.com/item?id=50127734>
