# Kimi K3.1 Pro: 가중치는 공개됐지만 2.8T 규모와 라이선스가 쓸 수 있는 곳을 좁힌다

<https://huggingface.co/moonshotai/Kimi-K3.1-Pro>

HN 토론: <https://news.ycombinator.com/item?id=50366999> (401점, 109개 댓글)

GN 토론: <https://news.hada.io/topic?id=36595>

## 소개

Kimi K3.1 Pro는 Moonshot AI가 Hugging Face에 올린 오픈 웨이트(open weights)
모델이다.
모델 카드는 이 모델을 네이티브 멀티모달 에이전트 모델이며 지금까지 만든 3T급
모델 가운데 가장 강하다고 소개한다.
Kimi K3를 후처리 학습(post-training)해 만들었고,
수백 개 하위 영역에 걸친 대규모 공동 강화학습을 거쳤다고 한다.
K3.1 시리즈의 첫 모델이며, 컨텍스트 길이는 100만 토큰(1048576)이다.
Moonshot은 코딩, 3D 제작, 금융 리서치, 사실 정확도에서 크게 나아졌다고 주장한다.

같은 모델의 기술 블로그는 [별도 문서](kimi-k3-1-pro.md)에서 다뤘다.
이 문서는 가중치 저장소 쪽, 곧 사양과 평가표와 배포 방법과 라이선스를 읽는다.
카드에 적힌 수치는 모두 Moonshot이 자기 모델에 대해 말한 내용이므로 제조사의
주장으로 다룬다.

## 사양

사양표는 카드의 Model Summary를 옮긴 것이다.
전문가 혼합(Mixture-of-Experts, MoE) 구조이고,
전체 파라미터 2.8T 가운데 토큰마다 쓰이는 활성 파라미터(activated
parameters)는 104B다.
활성 비율은 약 3.7%다.
이 비율은 카드의 두 수치로 계산한 값이며 카드가 직접 적은 수치는 아니다.

| 항목                                         | 값                                                         |
| -------------------------------------------- | ---------------------------------------------------------- |
| 구조(Architecture)                           | Mixture-of-Experts (MoE)                                   |
| 전체 파라미터(Total Parameters)              | 2.8T                                                       |
| 활성 파라미터(Activated Parameters)          | 104B                                                       |
| 레이어 수(Number of Layers)                  | 93 (dense 레이어 1개)                                      |
| 어텐션 구성(Attention-Layer Composition)     | 69 KDA + 24 Gated DSA                                      |
| 어텐션 은닉 차원(Attention Hidden Dimension) | 7168                                                       |
| 어텐션 헤드 수(Number of Attention Heads)    | 96                                                         |
| 전문가 수(Number of Experts)                 | 896개 중 토큰당 16개 선택, 공유 전문가(shared experts) 2개 |
| 전문가별 MoE 은닉 차원                       | 3072                                                       |
| 어휘 크기(Vocabulary Size)                   | 160K                                                       |
| 컨텍스트 길이(Context Length)                | 1048576                                                    |
| 비전 인코더(Vision Encoder)                  | MoonViT-V2 (401M)                                          |
| 양자화(Quantization)                         | MXFP4 weights / MXFP8 activations (양자화 인지 학습)       |
| 입력 모달리티(Modality)                      | Text, Image                                                |

카드는 K3와 달리 전체 어텐션 방식의 Gated MLA 레이어를 Gated DeepSeek Sparse
Attention(Gated DSA) 레이어로 바꿨다고 적는다.
이유로는 긴 컨텍스트를 더 효율적으로 다루기 위해서라고 밝힌다.
DSA 인덱스의 헤드 차원은 128, 헤드 수는 32, Top-K는 2048이다.

Hugging Face의 모델 메타데이터는 이 저장소가 2026년 11월 2일에 만들어졌고,
가중치가 96개의 safetensors 파일로 나뉘어 있다고 보여 준다.[^hf-api]
같은 메타데이터에서 BF16으로 저장된 파라미터는 약 57.4B이고,
사용 중인 저장 용량(`usedStorage`)은 약 1.56TB다.[^hf-api]
양자화 설정의 제외 목록(`ignore`)에는 `self_attn`, `shared_experts`, `lm_head`,
`vision_tower`, `mm_projector`에 해당하는 패턴이 들어 있다.[^hf-api]
BF16 57.4B를 파라미터당 2바이트로 계산하면 약 115GB다.
이 계산은 문서 작성자의 산수이고, 4비트로 줄지 않은 부분의 크기를
가늠하는 용도다.

## 평가 결과

카드는 별도 표에서 K3.1 Pro를 Claude Fable 5.1, GPT-6 Astra, Claude Opus 5.5,
DeepSeek-V4.1-Flash-1017, GLM-5.3과 비교한다.
별도 언급이 없으면 K3.1 Pro는 추론 강도(reasoning effort) `max`,
`temperature = 1.0`, `top-p = 0.95`로 측정했다고 한다.
아래는 표 47개 행 가운데 이 문서의 논의에 쓰는 행만 옮긴 것이다.
점수의 단위와 방향은 행마다 다르며, 대시(—)는 해당 출처가 점수를 보고하지
않았다는 뜻이다.

| 벤치마크                                             | Kimi K3.1 Pro | Claude Fable 5.1 | GPT-6 Astra | Claude Opus 5.5 | DeepSeek-V4.1-Flash-1017 | GLM-5.3 |
| ---------------------------------------------------- | ------------- | ---------------- | ----------- | --------------- | ------------------------ | ------- |
| Terminal-Bench 4.0                                   | 65.7          | 57.9             | 58.2        | 66.4            | 42.3                     | 41.8    |
| SWE Marathon v1.1                                    | 51.7          | 45.6             | 42.5        | 46.3            | 40.0                     | 42.5    |
| Program Bench                                        | 31.5          | 53.5             | 50.0        | 65.0            | 29.1                     | 19.0    |
| DeepSWE v1.1                                         | 75.5          | 67.4             | 74.1        | 74.2            | 77.0                     | 66.9    |
| Kimi Code Bench 2.0 (내부)                           | 77.1          | —                | —           | —               | 76.1                     | 61.7    |
| BrowseComp                                           | 92.1          | —                | 91.5        | 90.8            | —                        | —       |
| HLE-Diamond                                          | 39.4          | 55.1             | 65.8        | 60.9            | 21.6                     | 25.1*   |
| Design Bench (내부, Elo)                             | 957           | —                | 1076        | 927             | 863                      | 718     |
| DECK-Arena (내부, Elo)                               | 1456          | —                | 1423        | 1253            | 1231                     | 1119    |
| Kimi Hallu Bench Hard w/ tools (내부, 낮을수록 좋음) | 8.3           | 23.3             | 5.5         | 15.0            | 23.3                     | 22.6    |
| ExploitBench                                         | 74.7          | 83.0             | 100         | 91.0            | —                        | 54.4    |
| ExploitGym                                           | 20.7          | 30.4             | 42.4        | 34.5            | —                        | 15.0    |
| xdev-bench-hard (내부)                               | 81.0          | —                | —           | —               | 85.7                     | 57.1    |

표 전체 47개 행에서 K3.1 Pro가 보고된 점수 가운데 가장 높은 행은 16개다.
이 가운데 내부 벤치마크가 3개(Kimi Code Bench 2.0, Business Operation,
DECK-Arena)다.
이 집계는 문서 작성자가 카드의 표를 세어 얻은 값이다.
쌍으로 비교하면 Claude Opus 5.5와는 둘 다 보고된 행 중 21승 21패이고,
DeepSeek-V4.1-Flash-1017과는 41승 3패다.

## 배포와 사용

Moonshot은 `platform.kimi.ai`에서 모델 이름 `kimi-k3.1-pro`를 고르면 API를 쓸 수
있고, OpenAI와 Anthropic 호환 API를 제공한다고 안내한다.
직접 서빙할 때 권장하는 추론 엔진(inference engine)은 vLLM, SGLang,
TokenSpeed 세 가지이며 각각 레시피나 쿡북 링크가 걸려 있다.

사고 강도는 요청의 최상위 필드 `reasoning_effort`로 정한다.
값은 `"low"`, `"high"`, `"max"`이고 기본값은 `"max"`다.
여러 턴의 대화나 도구 호출에서는 API가 돌려준 어시스턴트 메시지를
`reasoning_content`와 `tool_calls`까지 포함해 그대로 `messages`에 되돌려 보내야
한다고 카드는 요구한다.
카드의 예제는 이전 턴의 추론 내용에 있던 숫자 두 개를 다음 턴에서 모델이
기억하는지로 이 동작을 보여 준다.

```python
response = client.chat.completions.create(
    model=model_name,
    messages=messages,  # reasoning_content를 포함한 이전 어시스턴트 메시지
    stream=False,
    max_tokens=4096,
    reasoning_effort="max",
)
```

비전 입력, 구조화된 출력, 도구 선택, 컨텍스트 캐싱 같은 나머지 사용법은 카드가
API 퀵스타트 문서로 넘긴다.
카드는 최소 메모리나 GPU 구성을 어디에도 적지 않는다.

## 라이선스

라이선스는 Hugging Face 메타데이터에서 `other`로 분류된 Moonshot 자체 약관
(Kimi K3.1-Pro License)이다.
저작권 표시를 유지하면 사용, 복제, 수정, 배포, 파인튜닝,
파생물 제작을 제한 없이 허용한다고 시작한다.[^license]

예외는 두 가지다.
첫째, 본인이나 계열사가 서비스형 모델(Model as a Service) 사업을 하고 연속
12개월 동안 매출 합계가 2천만 달러를 넘으면,
상업적 사용 전에 Moonshot과 별도 계약을 맺어야 한다.[^license]
서비스형 모델은 제3자가 입력, 파라미터,
학습 데이터에 의미 있는 통제력을 가지도록 모델 추론이나 파인튜닝 접근을 주는
것으로 정의되고, 기능 일부로만 모델이 들어간 최종 사용자 제품과 남이 호스팅하는
모델로 요청을 중계하는 일은 제외된다.[^license]
둘째, 월간 활성 사용자가 1억 명을 넘거나 월 매출이 2천만 달러를 넘는 상용 제품은
사용자 화면에 “Kimi K3.1-Pro”를 눈에 띄게 표시해야 한다.[^license]

두 의무는 내부 사용과 Moonshot의 공식 제품 또는 인증받은 추론 파트너
(certified inference partners)를 통한 사용에는 적용되지 않는다.[^license]

## 분석

### 활성 파라미터가 3.7%라서 연산량과 메모리 요구가 따로 움직인다

카드의 사양은 896개 전문가 가운데 토큰마다 16개와 공유 전문가 2개만 쓰는 구조를
보여 준다.
매 토큰의 연산은 104B 규모지만, 어떤 전문가가 뽑힐지 미리 알 수 없으므로 2.8T
전체가 어딘가에 올라 있어야 한다.
그래서 이 모델의 서빙 비용은 연산이 아니라 가중치를 어디에 얼마나
두느냐로 갈린다.
카드가 권장하는 vLLM, SGLang, TokenSpeed는 모두 여러 GPU에 가중치를 나눠 두는
서버용 엔진이다.

Hacker News에서 zozbot234는 이 희소성을 이용해 SSD에서 전문가를 필요할 때만
읽으면 192GB 램 정도로도 돌릴 수 있다고 주장했다.[^zozbot234-ssd]
같은 사용자는 128GB M5 MacBook Pro에서 이 방식을 시연한 사례가 있고,
토큰마다 SSD에서 약 25GB를 읽어 초당 0.3토큰 안팎에 그쳤다고
적었다.[^zozbot234-demo]
둘 다 댓글 작성자의 주장이고 이 문서가 재현한 값은 아니다.

다만 두 숫자는 카드의 수치와 맞물린다.
활성 104B에서 BF16으로 남는 약 57.4B를 빼면 매 토큰 읽는 전문가 파라미터는 대략
47B이고, 4비트면 약 23GB다.
이 계산은 BF16 부분이 매 토큰 전부 쓰인다는 가정 위의 어림값이다.
그 가정이 맞다면 zozbot234가 말한 25GB와 가깝다.

### 라이선스는 사용을 막지 않고 서비스로 되파는 사업만 가른다

라이선스의 의무는 모두 서비스형 모델 사업자와 대형 상용 제품에만 걸린다.
내부 사용은 두 조건에서 모두 빠진다.
Hacker News에서 bityard는 이런 크기의 모델이 취미 사용자가 아니라 연구자,
추론 제공 업체, 온프레미스를 택한 기업을 겨냥한다고 적었다.[^bityard]
이 라이선스를 읽으면 그 사용자층이 곧 의무가 걸리는 층이기도 하다.

한 가지 오해는 댓글에서 바로잡혔다.
월 매출 2천만 달러라는 문구를 보고 기준이 낮다고 한 댓글에 zozbot234는,
서비스형 모델 조항은 12개월 합계 2천만 달러이고 월 매출 기준은 이름 표시 의무에
해당한다고 답했다.[^zozbot234-maas]
라이선스 원문과 일치하는 설명이다.

### 점수표는 행마다 측정 조건이 다르다

표의 각주를 읽으면 비교가 같은 조건에서 이뤄지지 않았음을 알 수 있다.
Terminal-Bench 4.0에서 K3.1 Pro는 Claude Code 하니스로 직접 측정했고,
나머지 모델은 블로그나 공식 리더보드에 보고된 최댓값을 쓴다고 카드는 적는다.
ExploitBench는 K3.1 Pro가 다섯 시드 중 최선을 점수로 삼은 pass@5이고 비교 점수는
각 업체 보고서에서 가져왔다.
BioMysteryBench의 채점자는 Kimi K3다.
내부 벤치마크 3개에서는 K3.1 Pro가 가장 높지만,
내부 벤치마크는 외부가 같은 조건으로 돌릴 수 없다.

공개 리더보드 행에서는 그림이 다르다.
Program Bench는 K3.1 Pro 31.5, Claude Opus 5.5 65.0이고,
ExploitBench는 74.7 대 91.0이다.
승수 집계(16/47)가 K3.1 Pro 쪽에 유리하게 보이는 것은 내부 벤치마크와 에이전트
업무 벤치마크의 비중 덕분이기도 하다.
이 마지막 문장은 문서 작성자의 추론이다.

### 기본값 max와 추론 내용 반환 요구가 토큰 사용량을 결정한다

`reasoning_effort`의 기본값이 `max`이고,
다음 턴에 `reasoning_content`를 되돌려 보내야 한다.
추론 토큰이 매 턴 요청에 다시 실리므로 긴 에이전트 세션의 입력 토큰은 누적된다.
이 때문에 캐시 적중 여부가 비용을 좌우한다.
카드는 컨텍스트 캐싱을 퀵스타트 문서로 넘겼으므로 비용 구조는 카드만으로 알
수 없다.

## 비평

### 가장 큰 행이 오염 의혹을 받는데 카드는 그 조건을 말하지 않는다

Hacker News에서 NitpickLawyer는 R40 Research의 감사 보고서를 근거로 K3.1이
벤치마크 과제에 직접 학습했을 가능성을 제기했다.[^NitpickLawyer]
보고서는 K3.1이 과제에 없는 지시를 추론에서 인용하는 경우가 시도의 23%이고,
숨은 규칙과 모순되도록 과제 파일을 고치면 네 과제 중 세 과제에서 수정을 무시하고
실패한다고 적는다.[^r40-audit]
보고서는 이 행동이 훈련 오염과 맞는다고 해석하지만 증명할 수는 없다고 스스로
한계를 밝힌다.[^r40-audit]

카드의 Terminal-Bench 4.0 행(65.7)은 이 주장과 직접 닿는다.
카드는 점수가 Claude Code 하니스에서 나왔다는 것까지만 말하고 오염 점검 여부는
언급하지 않는다.
이 의혹이 결론을 바꾸려면, 새로 만든 과제에서 K3.1 Pro가 같은 순위를 유지하는지
독립 측정이 필요하다.
유지된다면 의혹은 약해지고, 무너지면 해당 행은 카드 점수로 쓸 수 없다.

### 사람 선호 평가와 에이전트 평가가 서로 다른 말을 한다

reissbaker는 매일 써 보면 K3.1이 DeepSeek-V4.1-Flash보다 훨씬 강하다고 느껴지고,
Design Arena에서 오래 상위였던 것은 사람 선호라 조작하기 어렵다고
반박했다.[^reissbaker]
반면 seizethecheese는 자신들의 agentduel 리더보드에서 두 모델이 사실상 비겼고
K3.1이 더 느리고 비싸다고 했다.[^seizethecheese]
이 댓글은 조기 투표를 허용하는 방식의 영향도 인정한다.

카드 안에서도 신호가 갈린다.
DECK-Arena(1456)에서는 K3.1 Pro가 가장 높지만 Design Bench(957)에서는 GPT-6
Astra(1076)가 앞선다.
두 벤치마크 모두 Moonshot 내부 평가라 어느 쪽이 대표적인지 외부에서 가릴
수 없다.

### 모델 카드가 하드웨어 요구량도 서빙 비용도 말하지 않는다

카드는 최소 메모리를 한 줄도 적지 않는다.
저장소의 `usedStorage`가 약 1.56TB라는 사실이 가장 구체적인 단서다.[^hf-api]
FuriouslyAdrift는 AMD MI300A 4장짜리 단일 서버(약 11만 달러)에서 이전 세대 Kimi
모델을 돌려 30~40명이 쓰고 있으며 이전 Claude 지출을 약 2주 만에 회수한다고
적었다.[^FuriouslyAdrift]
이 보고는 K3.1 Pro가 아니고, 검증할 수 없으며,
비교 기준이 늘어나던 월 청구서라는 전제가 붙는다.
1.56TB 저장소가 이 서버에 들어가는지는 확인된 바 없다.

### 사이버 보안 행은 카드에서 가장 낮고 설명이 없다

ExploitBench에서 K3.1 Pro는 74.7로 Claude Fable 5.1(83.0),
Claude Opus 5.5(91.0), GPT-6 Astra(100)보다 낮다.
ExploitGym도 20.7로 세 모델(30.4, 34.5, 42.4) 아래다.
Moonshot이 사이버 능력을 학습 데이터에서 덜어 냈다고 한 기술 블로그의 주장은
[관련 문서](kimi-k3-1-pro.md)에 정리했다.
카드에는 그 설명이 없고 점수만 나열된다.
그래서 낮은 점수가 의도된 결과인지 능력 부족인지 카드만으로는 구분되지 않는다.

## 인사이트

### 오픈 웨이트의 경쟁은 같은 가중치를 호스팅하는 다른 사업자와 벌어진다

minimaxir는 공개 직후 OpenRouter에 제3자 추론 제공 업체가 올라왔고,
Together가 Moonshot 엔드포인트의 두 배 처리량을 같은 가격에 낸다고
적었다.[^minimaxir]
가중치가 공개되면 모델 품질은 같아지고 차이는 처리량과 가격으로 옮겨 간다.
서비스형 모델 조항은 그 경쟁이 일정 규모를 넘을 때 Moonshot과의 계약을
거치게 만든다.

penagwin은 이 조항 때문에 제3자 가격이 Moonshot보다 낮아지기 어렵다고
추정했다.[^penagwin]
라이선스는 가격을 정하지 않으므로 이것은 추정이다.
다만 별도 계약의 조건이 공개되지 않았다는 점은 사실이어서,
조항은 사실상 Moonshot이 호스팅 시장의 출입을 조절하는 수단이다.
이는 클라우드 사업자에게 되팔림을 막으려는 소스 공개 라이선스들과 구조가
비슷하다.
인증 파트너가 Moonshot보다 낮은 가격을 공개하면 이 해석은 약해진다.

### MoE 희소성은 서빙 문제를 메모리 계층 문제로 바꾼다

활성 파라미터가 3.7%이면 대부분의 가중치는 한 토큰 동안 놀고 있다.
그 가중치를 램이 아니라 SSD에 두면 속도는 SSD 읽기 대역폭을 토큰당 읽는 양으로
나눈 값에 가까워진다.
토큰당 약 25GB를 읽고 SSD가 초당 7GB를 읽는다고 가정하면 초당 0.28토큰이다.
이 가정은 문서 작성자의 것이지만 zozbot234가 전한 0.3 토큰과 겹친다.

여기서 자주 쓰는 전문가를 램에 캐시하는 효과가 커진다.
같은 과제가 같은 전문가를 반복해서 쓰므로 작은 캐시도 도움이 된다는 것이 댓글
작성자들의 주장이다.
카드의 권장 엔진 세 가지는 이 경로를 다루지 않는다.
개인 사용자의 길은 공식 지원 밖의 도구에 달려 있어,
속도를 정하는 것은 모델이 아니라 저장장치다.

### 추론 내용이 공개되는 모델은 훈련 오염을 행동으로 드러낸다

카드는 API가 `reasoning_content`를 돌려주며 이를 보관하라고 요구한다.
R40 보고서가 K3.1의 추론에서 과제에 없는 지시를 읽어 낸 근거도 추론 텍스트다.
카드와 보고서를 잇는 이 연결은 추론이다. 보고서가 어떤 경로로 추론을 얻었는지는
초록만 읽은 이 문서가 확인하지 못했다.

추론이 보이면 점수만으로는 알 수 없는 질문을 던질 수 있다.
모델이 문제에 없는 규칙을 인용하는지, 규칙을 뒤집으면 따르는지를 물을 수 있다.
채택 판단의 규칙은 단순하다.
카드의 점수는 가설로 보고, 쓰려는 과제 몇 개로 추론 내용을 읽으며 직접 확인한다.
숨은 규칙을 인용하는 일이 반복되면 점수는 쓸 수 없다.

---

[^hf-api]: Hugging Face, [moonshotai/Kimi-K3.1-Pro](https://huggingface.co/api/models/moonshotai/Kimi-K3.1-Pro), 2026-11-02

[^license]: Moonshot AI, [Kimi K3.1-Pro License](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/main/LICENSE)

[^r40-audit]: R40 Research, [Kimi K3.1 Pro Recalls and Enforces Hidden Test Rules](https://r40.org/papers/kimi_k31_benchmark_audit.pdf), 2026-11-03

[^zozbot234-ssd]: <https://news.ycombinator.com/item?id=50368319>

[^zozbot234-demo]: <https://news.ycombinator.com/item?id=50369725>

[^bityard]: <https://news.ycombinator.com/item?id=50368811>

[^zozbot234-maas]: <https://news.ycombinator.com/item?id=50370047>

[^NitpickLawyer]: <https://news.ycombinator.com/item?id=50369625>

[^reissbaker]: <https://news.ycombinator.com/item?id=50368806>

[^seizethecheese]: <https://news.ycombinator.com/item?id=50369514>

[^FuriouslyAdrift]: <https://news.ycombinator.com/item?id=50370951>

[^minimaxir]: <https://news.ycombinator.com/item?id=50369602>

[^penagwin]: <https://news.ycombinator.com/item?id=50369658>
