# Best value LLM: 토큰 단가와 지능 지수로 그린 가치 경계선

<https://bestmodelforyourbudget.terrydjony.com/>

<https://github.com/terryds/bestvaluemodel>

HN 토론: <https://news.ycombinator.com/item?id=49830866> (173점, 106개 댓글)

GN 토론: <https://news.hada.io/topic?id=34242>

## 소개

Best value LLM은 Artificial Analysis의 Intelligence Index에 오른 모든 모델을 혼합 API 가격과 함께 한 장의 그래프에 찍고, 그 가운데 “가치 경계선”에 있는 모델을 보여 주는 정적 페이지다.
가치 경계선은 자기보다 싸면서 더 똑똑한 모델이 하나도 없는 모델들의 집합이고, 경계선 밖의 모델은 가격과 점수 두 면에서 모두 경계선 위의 어떤 모델에 진다.
저장소 `terryds/bestvaluemodel`은 2026년 9월 24일에 만들어졌고, README는 수작업으로 관리되던 vps.sonnylab.com의 모델 가치 표에서 영감을 받아 데이터 기반으로 만들었다고 밝힌다.

페이지는 여섯 부분으로 이루어진다.
가격 대 성능 산점도, 예산 구간별로 가장 높은 점수의 모델과 차점자를 보여 주는 조회표, 가격을 무시한 순수 성능 순위, 하루 단위 변경 내역, 전체 수치 표, 읽는 법이다.
지표는 Intelligence, Coding, Math 셋 중에 고를 수 있고, 제작사로 거를 수 있으며, 기본값으로는 모델 이름마다 가장 점수가 높은 추론 설정 하나만 보여 주고 점수 30 미만은 숨긴다.

## 동작 방식

데이터는 Artificial Analysis의 무료 데이터 API에서 온다.
GitHub Actions가 매일 06:17 UTC에 `scripts/fetch-aa.mjs`를 돌려 API 응답을 정리하고, 이전 스냅숏과 비교해 추가, 제거, 재채점, 가격 변경을 `data/changelog.json`에 기록하며, 달라진 것이 있을 때만 커밋하고 Cloudflare Workers에 다시 배포한다.
페이지 자체는 빌드 단계 없는 순수 HTML, SVG, JavaScript이고, 실행할 때 `data/models.json`을 불러와 선택한 지표에 대해 경계선을 브라우저에서 계산한다.

경계선 계산은 단순하다.
가격 오름차순으로 정렬한 뒤, 자기보다 싼 모든 모델보다 점수가 높은 모델만 남긴다.
가격이 같으면 점수가 높은 쪽이, 점수가 같으면 싼 쪽이 이긴다.
가격은 입력과 출력을 3:1로 섞은 100만 토큰당 혼합 가격이며, 캐시 입력 할인, 배치 가격, 빠른 모드 가격은 넣지 않는다.
최소 점수 필터는 아주 오래되고 작은 모델이 바닥 가격으로 경계선의 출발점을 붙잡지 않게 하려는 장치다.

### 9월 24일 스냅숏의 경계선

9월 24일 13시 33분(UTC)에 받은 스냅숏에는 420개 항목이 들어 있다.
Intelligence Index 30 이상, 추론 설정별 변형을 모두 포함해 같은 규칙으로 경계선을 다시 계산하면 다음과 같다.

| 혼합 가격($/1M) | 지수 | 모델                         |
| --------------- | ---- | ---------------------------- |
| 0.200           | 37.3 | GPT-6 Luna (max)             |
| 0.230           | 39.8 | Qwen3.8-Flash-Next           |
| 0.237           | 41.8 | GLM 5.3 Flash                |
| 0.544           | 46.3 | MiMo-V2.6-Pro                |
| 2.000           | 48.1 | Muse Spark 1.3 (max)         |
| 8.000           | 57.6 | Claude Opus 5.5 (max effort) |

같은 스냅숏에서 GPT-6 Astra (max)는 지수 52.7에 혼합 가격 20달러로, 8달러에 57.6을 받는 Opus 5.5에 두 면에서 모두 져 경계선 밖에 있다.

## 분석

### 한 장의 그래프로 모델 선택을 줄이려는 도구다

모델이 수백 개로 늘어난 지금, 개발자가 부딪히는 질문은 “가장 좋은 모델이 무엇인가”보다 “이 예산으로 무엇을 써야 하는가”에 가깝다.
이 페이지는 그 질문을 파레토 경계선이라는 오래된 도구로 푼다.
경계선 밖의 모델은 고려할 이유가 없으므로, 수백 개의 선택지가 여섯 개 남짓으로 줄어든다.

Hacker News에서 newsy-combi는 코딩과 수학 그래프가 특히 흥미롭다며, 아주 싼 모델들이 상위권에 들어와 1위의 1% 가격으로 90%의 성능을 낸다고 적었다.[^newsy-combi]
verytrivial은 코딩 점수 50 이상에서 경계선 위의 모델이 Ling, Qwen, Gemini, Muse, Grok, GPT, Claude로 모두 다른 제작사라는 점을 흥미롭게 봤다.[^verytrivial]
가격 구간마다 강자가 다르다는 것은, 한 회사의 모델만 쓰는 습관이 대부분의 구간에서 손해라는 뜻이다.

### 데이터를 사람이 아니라 cron이 관리한다

영감을 준 원래 표는 사람이 손으로 관리했고, 이 페이지는 그것을 하루 한 번 도는 자동화로 바꿨다.
모델 출시 속도를 생각하면 이 선택은 합리적이다.
사람이 관리하는 표는 새 모델이 나올 때마다 뒤처지지만, API를 매일 받아 다시 계산하는 페이지는 적어도 원천 데이터만큼은 최신이다.

다만 그 “최신”은 원천의 최신이다.
Hacker News에서 jeremysalwen은 하루 전에 나온 Opus 5.5가 빠져 있다고 지적했지만,[^jeremysalwen] 9월 24일 스냅숏에는 들어 있어 원천이 갱신되자 페이지도 따라온 것으로 보인다.
real0mar와 israrkhan은 수학 지표의 최고가 여전히 GPT-5.2로 나오고 Astra나 Fable이 없다고 적었다.[^real0mar][^israrkhan]
Artificial Analysis가 새 모델의 수학 점수를 아직 채우지 않았다면, 페이지는 그 빈칸을 그대로 옮긴다.

## 비평

### 토큰당 가격은 작업당 비용을 대신하지 못한다

Hacker News에서 가장 많이 나온 비판은 가격 축에 대한 것이었다.
ford는 어떤 모델은 같은 수준의 결과를 내는 데 토큰을 2~3배 더 쓰기 때문에 이런 가격 추정은 순진하며, Artificial Analysis 자체의 작업당 비용이 더 공정한 추정이라고 지적했다.[^ford]
jwolfe도 필요한 것은 100만 토큰당 비용이 아니라 작업당 비용이라고 했고,[^jwolfe] arshxyz는 캐시 토큰 비용까지 빠져 있어, 토큰을 같은 양 쓰더라도 “싼” 모델이 실제로는 더 비쌀 수 있다고 덧붙였다.[^arshxyz]

이 비판은 경계선의 의미를 흔든다.
추론 모델은 설정에 따라 생각 토큰을 몇 배씩 더 쓰고, 같은 이름의 max와 low 설정은 토큰 단가가 같아도 작업당 비용이 크게 다르다.
그런데 이 페이지는 모델 이름마다 가장 점수가 높은 설정, 곧 대개 가장 많이 생각하는 설정을 고르고, 그 설정의 토큰 단가를 가격으로 쓴다.
점수는 가장 비싸게 돌린 결과에서 가져오고 가격은 가장 싸게 보이는 단위로 적는 셈이라, 경계선이 실제보다 싼 쪽으로 기운다.

### 대부분의 사용자는 API 가격표 위에 있지 않다

jrflo는 API 비용을 자기 주머니에서 내는 사람이 있기나 하냐며, 구독이 API보다 10배쯤 싸게 보조되고 있다고 적었다.[^jrflo]
Brendinooo는 다음 달 100달러를 쓴다면 무엇을 해야 하는지, 곧 Claude 구독인지 Grok인지 중국 모델인지를 알려 주는 구독 중심의 비교가 필요하다고 했고,[^Brendinooo] swingboy는 대부분이 Anthropic이나 OpenAI의 구독을 쓰는데 어떤 모델이 사용 한도를 가장 효율적으로 쓰는지 알려 주는 믿을 만한 자료가 없다고 했다.[^swingboy]
rmi_는 OpenCode Go의 사용 한도에 대해 Artificial Analysis 점수를 비교하는 비슷한 페이지를 직접 만들었다고 소개했다.[^rmi_]

이 반응은 도구의 대상이 좁다는 것을 보여 준다.
API를 직접 호출하는 제품 개발자에게는 토큰 단가가 의미가 있지만, 개인 사용자의 실제 선택은 구독 요금제와 사용 한도 위에서 이루어진다.
예산 조회표라는 이름은 개인의 한 달 예산을 떠올리게 하지만, 실제로 답하는 것은 API로 100만 토큰을 쓸 때의 선택이다.

### 한 개의 지수로 줄인 순위는 벤치마크의 불확실성을 감춘다

khalic은 이것이 벤치마크 소음을 더할 뿐이라며, 벤치마크는 이미 문제가 있고 여러 개를 모아 비용까지 얹으면 오차 막대가 더 커질 뿐이니, 자기 사용과 제약을 반영하는 비공개 평가 체계를 만들라고 적었다.[^khalic]
floppyd도 시간이 갈수록 모델의 능력을 숫자 한두 개로 구별하기 어려워진다며, 장황함, 쉽게 포기하는 정도, 앞을 내다보는 능력 같은 여러 축의 비교를 원했다.[^floppyd]

rdsubhas가 짚은 조회표의 모양도 같은 문제를 드러낸다.[^rdsubhas]
조회표에는 여섯 구간밖에 없는데, 그중 하나가 “0.23달러 이상 0.24달러 미만”이라는, 사실상 한 모델의 가격만을 위해 만들어진 구간이라는 것이다.
경계선의 계단을 그대로 표로 옮기면, 가격 차이가 1센트도 안 되는 모델들이 서로 다른 구간을 차지한다.
지수 차이 2점이 벤치마크 오차 안에 있을 수 있다는 점을 생각하면, 이 계단은 실제 차이보다 정밀해 보인다.

## 인사이트

### 가치 경계선은 가격 전략의 표적이 된다

ggcr은 연구소가 새 모델을 아주 싸게 내놓아 보기 좋은 파레토 그래프를 만들고 “비용의 새 경계선”이라는 문구를 붙인 뒤 가격을 다시 올리는 것을 무엇이 막느냐고 물었다.[^ggcr]
경계선 그래프가 널리 쓰일수록, 그 그래프에 오르는 것 자체가 마케팅 목표가 된다.
출시 직후의 할인 가격과 한정 기간 가격은 그래프를 움직이지만 장기 비용을 반영하지 않는다.

매일 갱신하고 변경 내역을 남기는 이 페이지의 설계는 그 문제에 대한 부분적 방어다.
가격이 오르면 다음 날 경계선에서 밀려나고, 그 변화가 기록에 남는다.
그러나 그 기록을 보는 사람은 그래프를 보는 사람보다 훨씬 적다.

### 로컬 모델이 빠진 경계선은 절반의 지도다

hsnewman, aslkalska, daft_pink는 로컬 모델이 훨씬 쌀 것이라거나, 자기 기기에서 돌릴 수 있는 최고의 모델을 보여 주는 사이트, 곧 가로축이 VRAM인 그래프를 원한다고 적었다.[^hsnewman][^aslkalska][^daft_pink]
Xeoncross는 24~64GB Mac이라면 밤에 Qwen3.8 27B를 로컬로 돌려 보라며, 느리지만 잠자는 동안이면 문제가 덜하고 GPT-5.3 Codex나 Claude Opus 4.6보다 순위가 높다고 했다.[^Xeoncross]
greggh는 M1 Max 32GB MacBook에서 Qwen3.8 27B 양자화 모델로 밤새 네이티브 Mac 앱의 문제를 고치게 하고 있다고 전했다.[^greggh]

이 반응들은 “가격”이 하나의 축이 아니라는 것을 보여 준다.
API 가격, 구독 한도, 로컬 하드웨어의 감가상각과 전기요금, 그리고 기다릴 수 있는 시간이 모두 비용이다.
시간을 비용에서 빼도 되는 밤 작업이라면, 느린 로컬 모델이 어떤 API 모델보다 싼 선택이 된다.
토큰 단가 경계선은 즉시 응답이 필요한 API 사용자에게는 좋은 지도이지만, 사용 방식이 다른 사람에게는 절반의 지도다.

---

[^newsy-combi]: <https://news.ycombinator.com/item?id=49831577>

[^verytrivial]: <https://news.ycombinator.com/item?id=49831584>

[^jeremysalwen]: <https://news.ycombinator.com/item?id=49831311>

[^real0mar]: <https://news.ycombinator.com/item?id=49832484>

[^israrkhan]: <https://news.ycombinator.com/item?id=49833449>

[^ford]: <https://news.ycombinator.com/item?id=49831494>

[^jwolfe]: <https://news.ycombinator.com/item?id=49831229>

[^arshxyz]: <https://news.ycombinator.com/item?id=49840209>

[^jrflo]: <https://news.ycombinator.com/item?id=49831411>

[^Brendinooo]: <https://news.ycombinator.com/item?id=49831818>

[^swingboy]: <https://news.ycombinator.com/item?id=49833130>

[^rmi_]: <https://news.ycombinator.com/item?id=49832170>

[^khalic]: <https://news.ycombinator.com/item?id=49832567>

[^floppyd]: <https://news.ycombinator.com/item?id=49831376>

[^rdsubhas]: <https://news.ycombinator.com/item?id=49833491>

[^ggcr]: <https://news.ycombinator.com/item?id=49832517>

[^hsnewman]: <https://news.ycombinator.com/item?id=49831245>

[^aslkalska]: <https://news.ycombinator.com/item?id=49831300>

[^daft_pink]: <https://news.ycombinator.com/item?id=49835693>

[^Xeoncross]: <https://news.ycombinator.com/item?id=49831556>

[^greggh]: <https://news.ycombinator.com/item?id=49832460>
