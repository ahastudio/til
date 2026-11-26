# Ternary Bonsai 2.5 27B

원문: [Introducing Ternary Bonsai 2.5 27B: Powering Agentic Coding and Private Knowledge Work](https://prismml.com/news/bonsai-2-5-27b)

HN 토론: <https://news.ycombinator.com/item?id=50633922> (477점, 148개 댓글)

GN 토론: <https://news.hada.io/topic?id=37796>

## 요약

PrismML이 2026년 11월 24일에 낸 발표 글이다.
Ternary Bonsai 2 27B의 후속으로, Qwen3.8 27B를 기반으로 하며
에이전트형 코딩, 여러 턴에 걸친 도구 사용, 다단계 작업 실행을 강화했다고 한다.
모델 크기는 이전과 같은 5.9GB다.
글은 같은 메모리 크기의 모델 가운데 에이전트 작업에서 가장 강하다고 주장한다.

글이 짚는 개선의 방향은 세 가지다.

- 도구 호출의 결과를 해석하고, 단계가 실패하면 조정하고,
  상호작용 내내 작업의 목표를 유지하는 능력
- 이전 모델의 과도한 사고와 반복 루프를 줄이는 것
- 이전 모델보다 적은 턴과 토큰으로 더 빠르고 정확하게 끝내는 것

글은 작은 오류가 연속된 도구 호출에서 누적되어 작업 전체를 망치기 때문에
에이전트 작업이 모델 열화에 특히 민감하다고 설명한다.
그래서 풀 정밀도 기반 모델과의 성능 차이를 줄인 것이 이번 릴리스의
의미라고 한다.

### 벤치마크 표

글의 표는 Qwen3.8 27B 풀 정밀도, Bonsai 2 27B, Bonsai 2.5 27B를 비교한다.

| 벤치마크                      | Qwen3.8 27B | Bonsai 2 27B | Bonsai 2.5 27B |
| ----------------------------- | ----------- | ------------ | -------------- |
| SWE-bench Verified            | 80.6        | 60.8         | 75.6           |
| DeepSWE v1.1 (mini-swe-agent) | 30.1        | 0            | 27             |
| Terminal-Bench 2.1            | 70.8        | 52.8         | 60.1           |
| AppWorld                      | 93.2        | 51.2         | 90.5           |
| τ³-Bench                      | 72.8        | 69.1         | 73.9           |
| BigCodeBench                  | 61.5        | 57.2         | 60.3           |
| LiveCodeBench v6              | 87.6        | 83.8         | 83.0           |

### 속도와 배포

글에 따르면 NVIDIA H100 한 장에서 MTP(multi-token prediction)를 켜면
초당 291토큰을 생성하고, 2,000토큰 프롬프트를 초당 3,200토큰으로 처리한다.
소비자용 RTX 4090에서는 MTP로 초당 204토큰, 프롬프트 처리는 초당 약
3,060토큰이다.
NVIDIA와 Intel GPU에서는 llama.cpp로, Mac, iPhone, iPad에서는 MLX로 돌아가고
가중치는 Apache 2.0으로 공개된다.
글은 사설 저장소에서 이슈를 푸는 코딩 보조, 검토용 요약을 만드는 문서 앱,
반복 분석을 맡는 데스크톱 비서 같은 제품 용도를 예로 들고,
회사가 팀과 함께 도메인 데이터 후처리 학습과 추론 최적화를 해 준다고 안내한다.
PrismML은 Caltech 연구자들에서 시작했고
Khosla Ventures, Cerberus, Google의 지원과 Samsung의 후속 지원을 받는다고
소개한다.

### 백서가 더하는 내용

발표 글은 평가의 자세한 내용을 백서에 맡긴다.
백서에 따르면 이 모델은 가중치당 1.76비트, 5.93GB이고 FP16 모델은 53.8GB다.
도구 호출 벤치마크 다섯 개(τ²-Bench, τ³-Bench, BFCL v3, BFCL v4,
AppWorld)의 평균은
77.2로 FP16의 77.7과 비슷하고,
코딩 벤치마크 세 개(Terminal-Bench 2.1, SWE-bench Verified, DeepSWE)에서는
FP16 점수의 90%를 유지해 Bonsai 2의 63%에서 올랐다.[^wp]
비교 대상은 같은 기반 모델의 저비트 GGUF 빌드인 GSQ-RCO(IQ3_XXS, IQ2_S,
IQ2_XS)와
Unsloth Dynamic(UD-IQ2_XS)이다.
백서는 10GB 미만의 모든 빌드 가운데 도구 호출과 에이전트 코딩에서 앞선다고
주장한다.[^wp]

## 분석

### 압축에서 에이전트 작업으로 초점이 옮겨졌다

이 저장소의 [Bonsai 2 27B](bonsai-2-27b.md) 문서가 다룬 이전 발표는
크기 대비 점수 유지율을 중심에 두었다.
이번 글은 유지율이 아니라 에이전트 작업이 끝까지 이어지는지를 말한다.
Bonsai 2는 DeepSWE에서 한 건도 풀지 못했는데 2.5는 27.0점으로 풀 정밀도 30.1의
90%까지 올랐다.[^wp]
백서가 압축이 에이전트 코딩을 가장 크게 해친다고 설명하는 근거는
나쁜 행동 하나가 긴 에피소드 전체를 망친다는 점이다.[^wp]
표에서 점수가 가장 크게 뛴 항목이 DeepSWE(0에서 27), AppWorld(51.2에서 90.5),
SWE-bench Verified(60.8에서 75.6)인 것은 이 방향 전환과 맞는다.

### 비교 대상이 크기 기준이다

백서의 기준선은 같은 모델을 2비트 안팎으로 줄인 GGUF 빌드다.
이들은 2.27~3.0비트라서 Bonsai 2.5보다 비트가 많고 크기도 7.6~10.1GB로 더
크다.[^wp]
그래서 같은 메모리 예산 안에서 가장 낫다는 주장은 이 후보군 안에서의 비교다.
백서는 AppWorld에서 어떤 빌드가 점수가 낮은 이유를 구체적으로 든다.
IQ2_XS 빌드는 다섯 건에 한 건꼴로 모든 API 호출을 추측하는 긴 스크립트를 쓰고
출력을 보기도 전에 작업을 완료로 표시한다는 것이다.[^wp]
같은 빌드가 τ²-Bench에서는 79.5점이라 한 벤치마크의 점수가 다른 벤치마크의
실패를 알려 주지 않는다.

### 속도는 런타임 작업의 결과이기도 하다

백서는 속도 향상을 모델이 아니라 런타임으로 설명한다.
MTP 초안 헤드가 NVIDIA GPU에서 디코딩을 1.5~1.8배 높이고,
시험 중인 커널이 더해진다.
Bonsai 2 발표 당일과 비교하면 NVIDIA GPU 일곱 개 중 여섯 개에서 디코딩이
2.3~3.0배 빨라졌다.[^wp]
MTP 헤드가 프롬프트를 따로 읽기 때문에 NVIDIA GPU에서 프롬프트 처리는 9~23%
느려진다고도 적는다.[^wp]
최고 수치는 H200과 B200에서 초당 약 300토큰이다.
이는 발표 글이 H100과 RTX 4090 수치를 헤드라인으로 삼은 것과 같은 계열의 최고
환경 수치다.

## 비평

### 점수의 크기보다 비교의 틀이 좁다

HN의 hatthew는 같은 크기급의 작은 모델, 예를 들어 Qwen3.8의 인기 있는 Q1이나 Q2 양자화
또는 1B~10B급 최신 모델과의 직접 비교를 보고 싶다고 했다.[^hatthew]
백서의 비교 대상은 풀 정밀도와 2~3비트 빌드뿐이다.
NoidFonsense는 이미 Qwen3.8 27B를 4비트로 돌릴 수 있다면 이 모델은 맞지 않는
거래라고 했다.[^NoidFonsense]
tompagenet2는 표의 점수가 Qwen보다 낮아 보인다고 묻고,
trvz와 mahdi7d1은 풀 정밀도 모델이 50GB를 넘는 데 비해 이 모델은 6GB 미만이라는
답을 달았다.[^tompagenet2][^trvz][^mahdi7d1]
발표 글의 표에 크기 열이 없어서 이런 오독이 생기기 쉽다.

### 백서의 본문과 표가 어긋난다

백서 본문은 다섯 범주 평균이 FP16 84.4에 Bonsai 2.5 82.3이고
IQ3_XXS와 Bonsai 2가 둘 다 81.9라고 적는다.
같은 백서의 표 4는 평균을 84.32, 82.12, IQ3_XXS 81.72, Bonsai 2 81.55로
싣는다.[^wp]
차이는 0.2~0.35점이라 결론을 바꾸지는 않지만, 평균을 어떻게 냈는지 설명이
일관되지 않다.
또 τ²-Bench와 τ³-Bench는 사용자 시뮬레이터를 사고 모드의
deepseek-v4-flash로 바꿨고
BFCL v3는 기본 도구 호출 방식을 쓰기 때문에
Bonsai 2 보고서의 수치와 직접 비교할 수 없다고 백서가 스스로 적는다.[^wp]
표에 있는 Bonsai 2 열이 새 설정으로 다시 잰 값인지는 발표 글이 밝히지 않는다.

### 벤치마크 수치와 사용 경험

nik_s는 SWE-bench Verified 점수가 2026년 2월에 나온 Opus 4.6과 같다는 점을 두고
벤치마크에 맞춘 결과인지, 기준이 움직인 것인지,
작은 모델이 6개월 늦게 프런티어 수준에 닿는 것인지 궁금하다고 했다.[^nik_s]
dofm은 같은 점수가 실사용 경험과 같다는 뜻이 아니라고 반박했다.[^dofm]
백서의 평가는 모델마다 한 번씩만 시도하는 pass@1이고 제공사가 직접 돌린 것이어서
독립적인 확인은 아니다.

사용자들의 보고도 갈렸다.
syntaxing은 Unsloth Studio로 돌려 보니 이전 2보다 쓸 만하고
에이전트 호출이 안정적이었다고 했다.[^syntaxing]
thepoet은 자신의 장기 작업 벤치마크에서 Opus 5.5가 8건 모두 통과하는 동안
Bonsai 2와 2.5는 둘 다 5건을 통과했지만,
2.5가 단계 수는 17%, 시간은 29% 줄었다고 보고했다.[^thepoet]
ycui7은 처음으로 256K 컨텍스트에서 2,048개 바늘의 밀집 검색 시험을 통과했다고
했다.[^ycui7]
PaulKeeble은 V2가 루프에 빠지고 출력이 나빴다고 했고,
veemjeem은 많은 런타임이 온도 0을 기본으로 삼아 루프가 생길 수 있다고
답했다.[^PaulKeeble][^veemjeem]
이 문서는 이 보고들을 재현하지 못했다.

### 보고된 속도의 환경

발표 글의 초당 291토큰은 H100에서 MTP를 켠 수치다.
ariwilson은 Mac Mini M5 Pro 24GB에서 Q2 GGUF로 초당 22~25토큰이 나왔고
128k 컨텍스트가 메모리에 들어간다고 보고했다.[^ariwilson]
백서의 Apple M5 Pro 일반 디코딩 수치는 초당 30.2토큰으로 사용자 보고보다 높고,
측정 조건이 다르다.[^wp]
sleight42는 벤치마크를 올릴 때 양자화, 파일 형식, 엔진을 밝히지 않는 일이 많다고
비판했다.[^sleight42]
백서는 이를 밝히고 있다. 다만 일반 llama.cpp에서 Q2_0 파일이 도는 속도(H200에서
초당 109토큰)는
PrismML 포크(초당 150토큰)보다 낮다고 스스로 적는다.[^wp]

### 모호한 표현

글은 지능 밀도(intelligence density)라는 말을 쓴다.
andai가 그 뜻을 묻자 dofm은 어떤 단위당 지능을 말하는 듯하지만 모호하다고
답했다.[^andai][^dofm-density]
Lramseyer는 삼진 가중치를 가속하는 하드웨어가 FPGA 말고 있는지 물었고,
Foobar8568는 FPGA 보드가 비싸고 대역폭도 맞지 않는다고
답했다.[^Lramseyer][^Foobar8568]
백서의 런타임 설명으로 미루어 이 모델의 속도는 소프트웨어 커널 최적화에 크게
기댄다고 읽힌다.
이는 이 문서의 해석이다.

## 인사이트

### 크기 제약이 정하는 쓸모

이 모델이 쓸 만한지는 크기 제약이 있을 때 정해진다.
이미 4비트 Qwen3.8 27B를 돌릴 수 있는 환경이면 이 거래는 맞지 않는다는
지적이 있다.
6GB 안팎에 에이전트 작업을 넣어야 하는 환경에서만 비교 대상이 된다.

### 실패의 모양

벤치마크 합계보다 실패의 모양을 본다.
백서는 낮은 비트 빌드가 한 벤치마크에서는 좋고 다른 곳에서는 무너지는
사례를 든다.
자기 작업에서 한두 개 짧은 시험이 이 점을 가장 빨리 드러낸다.

### 공개된 설정

설정은 공개된 값에 맞춘다.
백서의 권장 샘플링은 사고 모드에서 온도 1.0, top-p 0.95, top-k 20이고
많은 런타임의 기본값 0과 다르다.

### 이전 세대 문서

이 저장소의 [Bonsai 2 27B](bonsai-2-27b.md)와
[Bonsai 27B](bonsai-27b-phone-model.md)를 같이 읽을 수 있다.
그러면 세 세대의 주장이 어떻게 바뀌었는지 볼 수 있다.

### 확인할 것

확인할 것은 두 가지다.
장시간 다중 컨텍스트 작업(MLE-bench 같은 것)에서도 이 수준이 유지되는지,
그리고 독립적인 평가가 제공사의 수치를 재현하는지다.

---

[^wp]: PrismML, [Ternary Bonsai 2.5 27B](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-5-27b-whitepaper.pdf), 2026-11

[^hatthew]: <https://news.ycombinator.com/item?id=50635809>

[^NoidFonsense]: <https://news.ycombinator.com/item?id=50634638>

[^tompagenet2]: <https://news.ycombinator.com/item?id=50634686>

[^trvz]: <https://news.ycombinator.com/item?id=50634725>

[^mahdi7d1]: <https://news.ycombinator.com/item?id=50634740>

[^nik_s]: <https://news.ycombinator.com/item?id=50634586>

[^dofm]: <https://news.ycombinator.com/item?id=50634804>

[^syntaxing]: <https://news.ycombinator.com/item?id=50635553>

[^thepoet]: <https://news.ycombinator.com/item?id=50636582>

[^ycui7]: <https://news.ycombinator.com/item?id=50636808>

[^PaulKeeble]: <https://news.ycombinator.com/item?id=50635095>

[^veemjeem]: <https://news.ycombinator.com/item?id=50635253>

[^ariwilson]: <https://news.ycombinator.com/item?id=50635106>

[^sleight42]: <https://news.ycombinator.com/item?id=50636371>

[^andai]: <https://news.ycombinator.com/item?id=50636509>

[^dofm-density]: <https://news.ycombinator.com/item?id=50636687>

[^Lramseyer]: <https://news.ycombinator.com/item?id=50634850>

[^Foobar8568]: <https://news.ycombinator.com/item?id=50634883>
