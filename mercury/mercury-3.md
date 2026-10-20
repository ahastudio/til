# Mercury 3는 확산 방식 언어 모형이 커져도 빠르다는 주장이고 그 근거는 맞춘 추론 강도에서의 비교다

원문: [Diffusion at Scale: Introducing Mercury 3 – Inception](https://www.inceptionlabs.ai/blog/introducing-mercury-3)

HN 토론: <https://news.ycombinator.com/item?id=50155245> (226점, 85개 댓글)

GN 토론: <https://news.hada.io/topic?id=35658>

## 요약

Inception은 2026년 10월 19일 Mercury 3를 지금까지
공개된 가장 유능한 확산 기반 LLM으로 소개한다.
여러 벤치마크에서 GPT-6 Luna와 Claude Haiku 5.5를 앞서면서
1,000토큰/초 이상으로 4~8배 빠르게 돈다는 주장이다.
이 글은 Mercury 1보다 40배 넘게 크면서
훨씬 똑똑하지만 속도는 같다는 점을 요점으로 내세운다.

한눈에 보는 사양은 이렇다.

| 항목      | 내용                                                                          |
| --------- | ----------------------------------------------------------------------------- |
| 품질      | GPT-6 Luna와 Claude Haiku 5.5 같은 속도 최적화 모델과 대등하거나 더 낫다      |
| 속도      | NVIDIA GPU에서 초당 1,068토큰                                                 |
| 컨텍스트  | 100만 토큰, Mercury 2.5의 26만 토큰에서 늘어남                                |
| 가격      | 입력 100만 토큰당 0.20달러, 출력 0.70달러                                     |
| 출시 할인 | 50% 할인으로 입력 0.10달러, 출력 0.35달러, 캐시된 토큰은 입력 가격의 90% 할인 |

글의 논지는 확산이 규모에 따라 커진다는 것이다.
Mercury 1이 확산 LLM을 상업 용도로 만들 수 있다는 첫 증거였고,
열린 질문은 복잡한 용도에서
자기회귀 모델과 경쟁할 만큼 확산 LLM이 커질 수 있느냐였다고 한다.
Inception은 총 파라미터를 40배 넘게 키웠고
표준 벤치마크 전반의 지능이 Mercury 1(mini)에서 Mercury 3까지 3배가 되었으며
자기회귀 모델의 진보를 이끈 스케일링 법칙이 확산에도 적용된다고 쓴다.

현장 사례로 글은 브라우저 에이전트, 교육,
실시간 검색 에이전트, 고객 지원을 든다.
TinyFish AI의 Shuhao Zhang은 Mind2Web 내비게이션 작업 50개를 자사 웹 에이전트
하네스에서 돌려 Mercury 3가 50%를 끝냈고
이는 GPT-6.1-Sol보다 크게 많았다고 말한다.
그는 프런티어 모델과 같은 토큰 양과 같은 에이전트
단계 수로 토큰당 비용은 훨씬 낮았다고 덧붙인다.
RevisionDojo의 Michael Tong은 힌트와 채점과 정의가 약 1초 만에 돌아오고
품질은 이전에 쓰던 모델과 같거나 낫고 기존 스택에 바로 교체되었다고 한다.
Octen AI의 Kuan Zou는 스마트 안경에서 5초 걸리는 답은 망가진 것처럼 느껴지고,
Mercury 3의 중앙 생성 시간이 0.9초이고 중앙 종단 응답 시간이 2.2초였다고 말한다.
Lorikeet의 Michael Gribben은 초기 시험에서
지연뿐 아니라 평가와 프로덕션에서도 다른 모델을 앞섰다고 한다.

함께 소개된 제품은 두 가지다.
Mercury Voice는 첫 답 토큰까지의 시간(TTFAT)을 최소화하도록 맞춘 음성용
모델이고,
Mercury Decide는 대량 분류를 위한 결정 모델로 JevBench와
LegalBench 같은 벤치마크에서 Jev를 앞선다고 한다.
Mercury 3는 Inception API 플랫폼과 OpenRouter와 Baseten과 Vercel에서 쓸 수 있고
OpenAI API와 호환되며,
엔터프라이즈는 전용 용량과 오토스케일링과
규정 준수 통제와 데이터 보존 설정을 지원한다.

## 분석

### 글의 중심 주장은 확산에도 스케일링 법칙이 통한다는 것이다

글의 제목과 마지막 문장은 똑같이 확산이 규모에서도 통한다고 말한다.
이 주장은 확산 LLM이 작은 모델이나 틈새
용도에만 맞는다는 의문에 대한 답으로 쓰인다.
근거는 Mercury 1에서 3까지 파라미터를 40배 넘게 키웠을 때 지능이 3배가 되고
속도가 유지되었다는 한 줄이다.

HN에서
Inception의 공동 창업자이자 수석 과학자 Volodymyr는 확산이 토큰을 하나씩이
아니라 반복적인 노이즈 제거로 병렬 생성하므로,
추론 모델이 답마다 더 오래 생각할수록 같은 크기의 자기회귀
모델에 대한 속도 이점이 커진다고 설명했다.[^volodia]
이는 글에는 없는 설명이며 추론 시대에 확산의 위치를 설명하는 논리다.

### 비교의 단위는 같은 추론 강도다

Volodymyr의 댓글은 품질 주장에 맞춘 추론 강도라는 단서를 붙여,
같은 추론 강도에서 GPT-6 Luna와 Claude Haiku 5.5를 앞선다고 말한다.
이 단서는 글이 어떤 비교를 하는지 가장 정확하게 보여 준다.
속도는 확산의 구조에서 오는 이점이고, 품질은 같은 강도에서 맞서는 것이다.

글의 현장 사례도 같은 구조를 따른다.
TinyFish의 비교는 같은 토큰 양과 같은 에이전트 단계 수에서
토큰당 비용이 훨씬 낮다는 것이고, 속도와 가격을 품질과 함께 내세운다.

### 사례의 공통점은 사람이나 에이전트가 모델을 기다리는 일이다

네 사례는 모두 대기 시간이 쌓이는 일이다.
에이전트는 모든 단계에서 모델을 기다리고, 학생은 피드백을 기다리고,
검색 사용자는 몇 초만 지나도 느리다고 느끼며,
고객 지원은 대화 속도로 답해야 한다.
이 글은 속도를 부가 기능이 아니라 용도를 정하는 속성으로 놓는다.

이 저장소의 Mercury 2.5 문서도 같은 구조를 짚었다.
확산 방식 모형을 지연 시간 시장에 파는 전략이라는 읽기다.
이번 발표는 그 전략을 더 큰 모델로 확장하고
컨텍스트를 100만 토큰으로 늘린 것이다.

## 비평

### 모든 비교가 자사 선택의 벤치마크와 중간 추론 강도에서 나왔다

글은 어떤 벤치마크에서 얼마나 앞서는지 숫자를 주지 않고
여러 벤치마크라고만 쓴다.
HN에서 himata4113은 왜 벤치마크를 중간(medium)에서 했느냐고 물으며,
값싼 모델은 보통 xhigh나 max로 쓰는데 낮음에서
최대까지의 성능 곡선도 과제 완료 시간도 없다고
했다.[^himata4113] vorticalbox는 중간에서의 펠리컨이 높음의 펠리컨보다 나아서
추론이 중간 이후에 출력에 부정적일 수도 있다고 추측했다.[^vorticalbox]

이 질문은 글의 핵심 비교를 건드린다.
추론 강도를 맞춘다는 것이 가장 유리한 강도에서
맞춘다는 뜻인지가 글에서 확인되지 않는다.
글은 DeepSWE 성적을 말하지 않지만 ttul이 지적한 대로 Mercury 3는 DeepSWE에서
46%로 Haiku의 52%보다 낮다고 한다.[^ttul]
이 수치는 글에 없고 댓글이 전하는 것이어서 이 문서는 확인하지 못했다.

### 속도 주장이 실사용에서 지켜지는지 글이 보여 주지 않는다

글의 속도는 NVIDIA GPU에서 1,068토큰/초다.
HN의 Escapado는 Oh My Pi 하네스로 SwiftUI 앱을 만들었는데
45분의 프롬프트와 시험과 수정에 2,600만 토큰(캐시되지 않은 것 130만)을 약
160TPS로 썼다고
했다.[^Escapado] bigmadshoe는 왜 블로그가 말한 1,000TPS 이상이 아니라 160TPS만
나왔는지 물으며
능력이 프런티어보다 뒤처지는 지금은 속도가 이 모델의 유일한 매력이라고
했다.[^bigmadshoe]

글은 이 차이의 이유를 말하지 않는다.
블랙웰 급 GPU나 낮은 동시 요청 같은 조건이 달랐을 수 있지만
이는 이 문서의 추측이다.
HN에서 LarsDu88는 Google의 Gemini Diffusion 예비 논문이 작은 배치 크기에서는
잘 돌았지만 대부분의 프로덕션 배포는 여러 사용자를 서비스하는 큰 배치 크기라고
지적했다.[^LarsDu88]
같은 맥락에서
글은 배치가 클 때 확산의 속도 이점이 어떻게 달라지는지 다루지 않는다.

### 가중치가 열려 있지 않다

HN의 jacquesm은 가중치를 공개할 것이냐고
물었고,[^jacquesm] SillyUsername은 이런 오픈 웨이트 모델을 기다렸는데
아직 아니라고 아쉬워했다.[^SillyUsername]
이 문서가 읽은 발표문은 Inception API와 OpenRouter와 Baseten과
Vercel을 통한 제공만 말하고 가중치 공개는 말하지 않는다.
이 저장소의 Mercury 2.5 문서도 열린 가중치가 아닌 점을 가장 큰 실망으로 꼽았다.

### 출시 할인이 가격 주장의 의미를 흐린다

가격은 입력 0.20달러와 출력 0.70달러로 쓰고,
출시 때는 50% 할인으로 0.10달러와 0.35달러다.
HN의 moecables는 속도가 필요한 일에 Haiku나 GPT-Luna 대신 이것을 쓰기
시작하겠지만 할인이 끝나도 쓸모가 있을지 궁금하다고
했다.[^moecables] cubefox는 속도를 필요로 하는 일이 떠오르지 않으며
보통의 거래는 가격과 품질과 신뢰성 사이라고 했다.[^cubefox]
글이 내세운 가격 우위가 할인된 값인지 정가인지에 따라 인상이 달라진다.

## 인사이트

### 속도가 용도를 정한다는 주장은 속도가 필요한 일이 무엇인지에 대한 합의를 요구한다

cubefox는 속도를 필요로 하는 일이 정말 있느냐고 물었고,
이 질문은 이 글의 시장 전체를 겨냥한다.
글은 브라우저 에이전트와 교육과 검색과 지원을 답으로 든다. bpavuk는 빠른 LLM이
가능하게 할 UX를 상상하기 어렵다며 자신이 JetBrains IDE에서
활동을 추적하는 프로토타입을 만들었다고
했다.[^bpavuk] davedx는 결정 모델에는 최대 처리량이 필요하니
이 속도가 얼마나 경쟁력이 있을지 궁금해했고,
moonu는 Inception에 별도의 결정 모델 Mercury Decide가 있다고
답했다.[^davedx][^moonu]

이 교환들을 보면 속도의 가치는 용도에 따라 갈린다.
대화나 에이전트의 상호작용에서는 지연이 사용 경험을 정하고,
일괄 작업에서는 처리량이 정한다.
이 문서의 읽기로는 Mercury 3의 시장은 속도가 품질의 일부가 되는 곳이며
그런 곳이 얼마나 큰지가 이 모델의 사업 규모를 정한다.
이 읽기가 틀렸다면
속도가 필요 없는 일에서도 가격 때문에 이 모델이 선택될 것이다.

### 대형 연구소가 확산을 접었는지에 대한 해석이 갈린다

simonw는 Google이 작년의 Gemini Diffusion 시연으로 사실상 아무것도 하지 않은
이유를 이해하지 못한다고 했고, Diffusion Gemma가 몇 달 전 공개되었지만
큰 반향이 없다고
적었다.[^simonw] dumberquestions는 주요 연구소가 확산 실험을 하지 않을 리 없고
하더라도 연산 능력이 훨씬 많은 그들보다 다른 회사가 앞서 있다면 놀라운 일이라고
했다.[^dumberquestions] willy_k는 Google이 이 범주를 사실상 열었으나
요청을 묶어 처리하는 배치 방식의 경제성에서
트랜스포머만큼 확장되지 않는 것 같아 접은 것으로 보인다고 했다.[^willy_k]

이 해석이 맞다면 Inception의 도전은 배치 경제성에서
확산이 자기회귀를 이기는 지점을 찾는 일이다.
이 문서의 읽기로는 이 지점이 낮은 지연이 중요한 소규모 배치와 추론 모델처럼
길게 생성하는 일이고 글이 이 두 가지를 모두 내세우는 것은 우연이 아니다.
글은 대규모 배치에서 경제성이 어떤지는 말하지 않는다.

### 확산이 다중 모달리티와 도구 사용으로 확장되는지가 다음 시험이다

HN의 moonu는 이것이 다중 모달이었으면 좋겠다고 했다.[^moonu-multimodal]
글의 사례는 대부분 텍스트이고
브라우저 에이전트의 Mind2Web은 DOM이나 텍스트 관찰일 가능성이 있지만
글에서 확인되지 않는다.
이 저장소의 Mercury 2.5 문서는
도구 사용과 에이전트 코딩이 안 된다는 실측 보고를 비평에서 다뤘는데,
이번 글은 에이전트 하네스에서
같은 단계 수로 프런티어와 비교했다는 점이 그 비평에 대한 응답으로 읽힌다.

이 읽기는 이 문서의 것이다.
다음 확인은 같은 하네스에서 모델을 바꿔 가며
도구 호출의 정확도와 단계 수를 재는 독립 평가다.
글은 그런 독립 평가를 제시하지 않는다.

---

[^volodia]: <https://news.ycombinator.com/item?id=50155371>

[^himata4113]: <https://news.ycombinator.com/item?id=50155512>

[^vorticalbox]: <https://news.ycombinator.com/item?id=50156089>

[^ttul]: <https://news.ycombinator.com/item?id=50155574>

[^Escapado]: <https://news.ycombinator.com/item?id=50157244>

[^bigmadshoe]: <https://news.ycombinator.com/item?id=50158434>

[^LarsDu88]: <https://news.ycombinator.com/item?id=50155675>

[^jacquesm]: <https://news.ycombinator.com/item?id=50155573>

[^SillyUsername]: <https://news.ycombinator.com/item?id=50155451>

[^moecables]: <https://news.ycombinator.com/item?id=50156073>

[^cubefox]: <https://news.ycombinator.com/item?id=50156140>

[^bpavuk]: <https://news.ycombinator.com/item?id=50157817>

[^davedx]: <https://news.ycombinator.com/item?id=50155688>

[^moonu]: <https://news.ycombinator.com/item?id=50155721>

[^simonw]: <https://news.ycombinator.com/item?id=50155594>

[^dumberquestions]: <https://news.ycombinator.com/item?id=50155664>

[^willy_k]: <https://news.ycombinator.com/item?id=50155941>

[^moonu-multimodal]: <https://news.ycombinator.com/item?id=50155391>
