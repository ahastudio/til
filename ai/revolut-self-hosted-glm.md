# Revolut의 자체 호스팅 GLM 전환: 비용 90% 절감과 생산성 70% 개선의 근거

트윗: [BREAKING: Revolut moved ~2,000 engineers onto self-hosted GLM for coding and pushed Claude Code and Codex to the exception list.](https://twitter.com/guilleflorvs/status/2117379073785696395)

HN 토론: <https://news.ycombinator.com/item?id=50350004> (189점, 159개 댓글)

GN 토론: <https://news.hada.io/topic?id=36534>

## 요약

Twitter 사용자 Guillermo Flor(guilleflorvs)는 2026년 11월 3일에
Revolut이 엔지니어 약 2,000명의 코딩 도구를 자체 호스팅 GLM으로 바꾸고
Claude Code와 Codex를 예외 목록(exception list)으로 옮겼다고 적었다.
그가 전한 숫자는 Nvidia B200 56대, 백만 토큰당 평균 30센트,
Anthropic과 OpenAI에 내던 비용의 약 10분의 1, 엔지니어링 리드 타임(lead time) 70% 개선이다.
그는 이 개선이 토큰을 아끼지 않게 된 뒤에 나타났다고 보고,
엔지니어들이 AI를 어려운 티켓에만 쓰지 않고 모든 일에 쓰기 시작했다고 해석했다.
결론으로는 프런티어(frontier) 모델이 예외가 되고 오픈 웨이트(open weights)가 기본값이 되며,
이것이 IPO를 앞둔 모든 연구소에 가격 문제라고 적었다.
Revolut의 AI 운영 책임자 David Abitbol의 발언이 출처라고 밝혔고,
조회수는 열람한 시점에 904.5K였다.

이 숫자들의 출처는 Abitbol이 2026년 10월 13일 AI Engineer NYC 본무대에서 한
“Shipping like a startup, regulated like a bank” 발표다.
행사 페이지는 발표 요약에서 같은 숫자를 싣고 있다.[^talk]
GLM 5.3을 B200 56대로 약 2,000명에게 서비스하고,
평균 비용이 백만 토큰당 약 0.30달러이며
청구액이 이전 Anthropic과 OpenAI 지출의 약 10분의 1이라는 내용이다.[^talk]
같은 페이지는 코딩 시간이 약 60%, 리드 타임이 약 70% 좋아졌다고 적으면서,
이 내부 비교가 모델 교체의 효과를 따로 떼어 내지는 못한다고 밝힌다.[^talk]
리드 타임은 기능을 맡은 때부터 병합 가능한 상태가 될 때까지의 시간이다.[^talk]

발표 영상에서 Abitbol은 2026년 4월 26일 무렵 GLM 5.1로 자체 호스팅을 시작했고
그 무렵 코딩 시간 60%, 리드 타임 70% 개선을 보았다고 말한다.[^video]
백만 토큰당 30센트와 청구액 10분의 1, B200 56대, GLM 5.3이라는 숫자도 영상에서 직접 확인된다.[^video]

The Register는 이 발표를 2026년 11월 3일에 보도하며,
추론 비용이 1년이 안 되어 약 90% 줄었다는 Revolut의 말을 전했다.[^register]
엔지니어들이 처음에는 월 1,000달러에서 1만 달러를 쓰면서도 성과가 크지 않았다는 Abitbol의 말도 실었다.[^register]
기사는 GLM이 GPT나 Claude를 완전히 대체한 것은 아니며
프런티어는 예외라는 Abitbol의 표현을 전한다.[^register]

## 분석

### 숫자의 출처는 한 사람의 발표이고 기사들은 그것을 되풀이한다

트윗과 이후 보도의 숫자는 모두 한 번의 컨퍼런스 발표에서 나왔다.
Dealroom은 수치가 Revolut 자체 집계이고
회사의 비교가 모델 교체를 다른 원인과 분리하지 않는다고 적었다.[^dealroom]
AI Weekly는 The Register를 원출처로 밝히면서,
60%와 70% 개선의 기준 기간과 측정 방법이 기사에 없다고 지적한다.[^aiweekly]
따라서 지금 확인된 것은 Revolut이 이런 숫자를 발표했다는 사실이고,
독립적으로 검증된 결과는 없다.

### 세 숫자는 서로 다른 것을 잰다

백만 토큰당 0.30달러는 서버 쪽 단가다.
행사 페이지는 이 비용이 Revolut의 배치와 사용률을 반영한 값이지
다른 조직에 그대로 옮길 수 있는 가격은 아니라고 적었다.[^talk]
청구액이 이전의 10분의 1이라는 것은 지출 총액의 비교다.
Dealroom은 이 90% 절감에 클라우드, 인력, 모니터링 비용이 빠져 있다고 전한다.[^dealroom]
리드 타임 70% 개선은 비용이 아니라 사람의 일하는 속도를 잰 숫자다.

단가의 정의도 열려 있다.
발표 영상에서 Abitbol은 평균 토큰 비용이 백만 토큰당 30센트라고 말한다.[^video]
Hacker News의 corford가 이 평균이 입력과 출력 중 무엇을 가리키는지 묻자,[^corford]
NortySpock은 둘을 평균한 값이라고 보았고 입력과 출력의 비율은 짐작할 수밖에 없다고 적었다.[^NortySpock]

세 숫자를 한 문장으로 묶으면 비용이 10분의 1이 되고 속도도 올랐다는 이야기가 된다.
그러나 단가, 총지출, 리드 타임은 서로 다른 대상을 서로 다른 방법으로 재고 있어서,
어느 하나가 다른 하나의 원인이라고 읽을 수 없다.

### 효과의 원인으로 지목된 것은 모델이 아니라 토큰 제한 해제다

Abitbol은 처음 Claude Code를 도입했을 때 비용 대비 효과가 분명하지 않아
엔지니어별 토큰 한도를 두었다고 말했다.[^talk]
The Register에 따르면 가장 큰 개선은 코드 작성이 아니라
디버깅과 Jira, Confluence 티켓 처리에서 나왔고,
Abitbol은 토큰이 무제한이면 그렇게 쓸 자유가 생긴다고 말했다.[^register]
Startup Fortune은 리드 타임이 코딩 속도보다 더 크게 좋아졌다는 점에서
이득이 주변 업무의 자동화에서 왔다고 추론했다.[^startupfortune]
Guillermo Flor의 해석, 곧 토큰을 아끼지 않게 된 뒤에 효과가 나타났다는 것과 같은 방향이다.

Abitbol은 발표 영상에서 같은 흐름을 더 구체적으로 말한다.
영상의 자동 자막에 따르면 Gemini는 리드 타임을 10%, 코딩 시간을 20% 개선했고,
그 뒤에 도입한 Claude Code는 당시 영향이 크지 않았다고 한다.[^video]
리드 타임이 코딩 시간보다 더 크게 좋아졌다는 점을 들어,
엔지니어링의 병목이 반드시 코딩은 아니라고 설명한다.[^video]
받은 편지함을 뒤지거나 Jira와 Confluence를 만지는 시간을 줄일 수 있고,
토큰이 무제한이면 그렇게 쓸 자유가 생긴다는 것이다.[^video]

다만 이 방향은 추론이다.
출처 어디에도 같은 한도 해제를 프런티어 모델에서 한 경우와의 비교는 없다.

### 운영 세부는 보도마다 다르게 적혔다

모델 버전부터 일치하지 않는다.
행사 페이지는 60%와 70% 개선이 GLM 5.1으로 바꾼 시기와 겹쳤고
현재 서비스 중인 것은 GLM 5.3이라고 적는다.[^talk]
The Register는 처음 GLM-5.1을 쓰다가 GLM-5.3으로 옮겼다고 전하면서도
기사 앞부분에서는 0.30달러 가격을 GLM 5.1에 붙였다.[^register]
어느 버전에서 이 비용과 개선이 나왔는지는 기사에서 가를 수 없다.

운영 방식은 비교적 일관된다.
GLM은 텍스트 전용이어서 이미지 질의는 Gemini 같은 다른 모델로 보내는 라우터를 둔다.[^register]
컨텍스트는 최대 100만 토큰을 지원하지만 25만 6천 토큰이면 충분하다고 Abitbol이 말했다.[^register]
같은 하드웨어에서 튜닝만으로 초당 요청 수가 76% 늘고
첫 토큰까지의 시간이 14.26초에서 1.68초로 88% 줄었다고 행사 페이지는 적는다.[^talk]

## 비평

### 90% 절감은 운영 비용을 뺀 비교로 읽어야 한다

Dealroom이 전하듯 90% 절감에는 클라우드, 인력, 모니터링 비용이 들어 있지 않다.[^dealroom]
B200 56대를 운영하려면 서빙 전문 인력이 필요하다.
Twitter 사용자 NashBriggsy는 B200 56대를 건강하게 유지하는 데 몇 명이 필요한지가
다음에 알고 싶은 숫자이고, 절감분이 대개 거기서 줄어든다고 적었다.[^NashBriggsy]
행사 페이지가 비용이 이식 가능한 가격이 아니라고 밝힌 것도 같은 맥락이다.[^talk]

Hacker News에서는 이 비용이 구매인지 임대인지가 먼저 논란이 되었다.
gosen은 B200 56대를 샀다면 하드웨어에 250만~300만 달러, 여기에 운영비가 든다고 어림했고,[^gosen]
mongrelion은 구매가 아니라 임대일 수 있다고 짚었다.[^mongrelion]
yolo3000은 영상에서 Together.ai에서 돌린다고 했다고 적었다.[^yolo3000]
그러나 영상의 자동 자막에서는 Together.ai라는 이름을 찾지 못했으므로 이 전언은 확인되지 않았다.
gosen은 Together.ai의 공개 가격으로 어림한 임대료가 월 25만~30만 달러라고 적었다.[^gosen-rent]
구매인지 임대인지에 따라 10분의 1이라는 비교의 내용이 달라진다.

여기서 지적하려는 것은 숫자가 틀렸다는 것이 아니다.
토큰 단가는 하드웨어 사용률이 높을수록 낮아지는 값이고,
Revolut은 엔지니어 2,000명이라는 사용량을 갖고 있다.
같은 비교를 수십 명 규모 팀에 적용할 수 있는지는 이 출처들로 알 수 없다.

### 생산성 개선에는 비교군이 없다

행사 페이지는 내부 비교가 모델 교체의 효과를 분리하지 못한다고 스스로 밝힌다.[^talk]
이 개선은 모델 교체, 토큰 한도 해제, 추론 튜닝,
Gemini에서 Claude Code를 거쳐 GLM으로 이어진 도구 변화가 겹친 시기에 측정되었다.
AI Weekly는 기준 기간과 측정 방법이 기사에 없다고 적었다.[^aiweekly]

Twitter 사용자 400_yen은 숙련된 엔지니어에게는 GLM과 Claude의 차이가 미미하고
벤치마크 몇 점 차이는 문제가 되지 않는다고 적었다.[^400_yen]
이는 경험에서 나온 의견이고 근거 수치는 없다.
이 주장이 사실이라면 70% 개선의 원인으로 모델 능력 차이를 제외할 수 있지만,
출처 어디에도 이를 확인하는 비교는 없다.

반대 경험도 같은 스레드에 올라왔다.
user43928은 Opus 5.5용 월 500달러 예산을 빼앗고 GLM-5.3 무제한으로 바꾼다면 큰 후퇴라고 적었다.[^user43928]
iLoveOncall은 Amazon 전사에 토큰이 무제한이지만 그 결과가 엄청난 양의 쓸모없는 산출물과
생산성의 착각뿐이라고 적었다.[^iLoveOncall]
두 의견 모두 경험담이어서 측정값은 아니지만,
토큰 한도 해제가 생산성을 올린다는 해석에 반례가 있다는 것은 보여 준다.

### 프런티어 모델이 예외가 되었다는 말은 보도마다 범위가 다르다

Startup Fortune은 Claude Code와 Codex가 예외 목록에 올랐다고 적고,
자체 모델이 못 하는 일에만 쓴다고 전한다.[^startupfortune]
RuntimeWire는 둘이 예외 역할로 옮겨졌다고 쓰고,[^runtimewire]
Dealroom은 가장 어려운 작업에는 계속 쓸 수 있다고 쓴다.[^dealroom]
반면 The Register는 엔지니어에게 두 도구의 접근 권한이 남아 있는지 분명히 밝히지 않았다.[^register]

따라서 예외 목록이 구체적으로 무엇이고 누가 쓸 수 있는지는 확인되지 않았다.
프런티어 모델이 이 조직에서 얼마나 쓰이는지에 대한 수치도 없다.
Guillermo Flor가 이를 근거로 모든 연구소에 가격 문제라고 결론 내린 것은 그의 추론이다.
Revolut의 사례 하나에서 다른 조직의 구매 결정을 읽어 내는 근거는 출처에 없다.

## 인사이트

### 바뀐 것은 모델이 아니라 과금 방식일 수 있다

Abitbol은 청구가 고정이어서 월말에 놀랄 일이 없고 프런티어가 예외라고 말했다.[^aiweekly]
토큰당 과금에서는 엔지니어가 어려운 일에만 AI를 쓰도록 스스로 줄인다.
고정 비용에서는 한계 비용이 거의 사라져서 티켓 정리와 문서 작업까지 쓰임이 번진다.
The Register가 전한 대로 큰 개선이 디버깅과 티켓 처리에서 나왔다는 점이 이를 뒷받침한다.[^register]

Hacker News의 littlecranky67도 이 효과가 토큰당 비용의 전후 비교로는 계산되지 않는다고 짚었다.[^littlecranky67]

이는 정액제가 사용 방식을 바꾼 오래된 사례와 구조가 같다.
통신 요금이 종량제에서 정액제로 바뀌면 사용량의 성격이 달라진다.
같은 구조라면 모델이 프런티어였더라도 한도를 풀면 비슷한 개선이 나왔을 수 있다.
이 가설은 확인되지 않았고, 확인하는 방법은 아래에서 제안한다.

### 길게 쓸 수 있는 능력과 길게 쓸 필요는 다르다

Abitbol은 긴 컨텍스트는 사기이니 조심해야 한다고 말했고,
100만 토큰을 서빙할 수 있어도 필요한 것은 25만 6천 토큰이라고 덧붙였다.[^register]
행사 페이지는 최대 컨텍스트를 위해 공간을 잡아 두면 KV-cache 용량이 낭비되므로
컨텍스트 창을 실제 작업에 맞추라고 권한다.[^talk]
자체 호스팅의 단가는 GPU 수보다 이런 설정에 크게 좌우된다.

kgeist는 GLM을 평가하는 중인데 vLLM에서 긴 컨텍스트일 때 정확성 문제가 많았다며
Revolut의 설정이 궁금하다고 적었다.[^kgeist]
행사 페이지가 컨텍스트 길이를 작업에 맞추라고 권하는 이유 가운데
하나일 수 있지만, 출처에서 확인되지는 않는다.

그래서 다른 조직이 같은 비용을 기대하려면 Revolut의 단가가 아니라 자기 사용량부터 봐야 한다.
같은 모델이라도 사용률이 낮으면 토큰당 비용은 오히려 올라간다.
첫 토큰까지 3초 미만을 목표로 한다는 Abitbol의 기준도 서비스 품질 비용으로 따라온다.[^talk]

### 도입 전에 던질 질문과 결론을 바꿀 관찰

이 사례를 자기 조직에 적용할지 정하려면 세 가지를 먼저 잰다.
엔지니어별 토큰 지출의 분포,
한도 때문에 AI를 쓰지 않던 업무의 비중,
한도를 풀기 전후의 리드 타임과 함께 같은 기간 한도를 유지한 대조 팀의 리드 타임이다.

결론을 바꿀 관찰도 분명하다.
프런티어 API를 쓰는 팀이 한도를 풀고도 비슷한 리드 타임 개선을 얻는다면,
Revolut의 효과는 모델 교체가 아니라 한도 해제에서 나온 것이다.
반대로 같은 한도 조건에서 GLM 팀만 개선이 크다면 모델과 서빙 구성이 효과를 만든다.
지금의 공개 자료로는 어느 쪽인지 알 수 없고, 이 질문에 답하는 자료는 아직 없다.

### 규제 산업에서는 비용보다 통제가 먼저 설명이 된다

행사 페이지는 자체 호스팅이 가중치를 회사가 고른 인프라에서 돌린다는 뜻이라고 설명하고,
샌드박스와 승인 규칙이 제한된 작업에 사람의 개입을 요구하며
텔레메트리가 사고 조사에 쓰인다고 적었다.[^talk]
The Register는 중국의 오픈 웨이트 모델이 중국 밖의 API로 접근할 때 개인정보와 보안 우려가 있고,
온프레미스나 지역 클라우드 배치는 그 우려가 덜하다고 전한다.[^register]

torginus는 일부 금융 규제가 서명한 계약과 무관하게 제3자에게 데이터를 넘기는 것을 막는다고 적었다.[^torginus]

이 맥락에서 오픈 웨이트의 자체 호스팅은 비용 절감 수단이기 전에
데이터가 나가는 경로를 통제하는 방법이다.
그 대가로 모델 공급과 버전 관리가 운영 업무가 된다.
Revolut이 GLM 5.1에서 5.3으로 옮긴 것도 업그레이드를 직접 맡는다는 뜻이다.[^register]
출처는 이 업무에 드는 인력과 비용을 밝히지 않는다.

---

[^talk]: AI Engineer, [Shipping like a startup, regulated like a bank](https://www.ai.engineer/nyc/2026/talks/revolut)

[^register]: The Register, [British fintech Revolut slashes AI coding costs 10x by cutting out Claude and going self-hosted](https://www.theregister.com/ai-and-ml/2026/11/03/british-fintech-revolut-slashes-ai-coding-costs-10x-by-cutting-out-claude-and-going-self-hosted/5307345), 2026-11-03

[^dealroom]: Dealroom News, [Revolut swaps Claude Code for a Chinese open-weight model, cutting its AI coding bill by 90%](https://dealroom.co/news/169124-revolut-moves-2-000-engineers-onto-self-hosted-ai-cutting-coding-costs-9/), 2026-11-03

[^startupfortune]: Startup Fortune, [Revolut Shows Cheap Unlimited Tokens, Not Smarter AI, Is What Speeds Up Coding](https://startupfortune.com/revolut-shows-cheap-unlimited-tokens-not-smarter-ai-is-what-speeds-up-coding/), 2026-11-03

[^runtimewire]: RuntimeWire, [Revolut says self-hosted GLM cut its AI coding costs by 90% for 2,000 engineers](https://runtimewire.com/article/revolut-self-hosted-glm-coding-costs), 2026-11-03

[^aiweekly]: AI Weekly, [Revolut Cuts AI Coding Costs ~90% With Self-Hosted GLM on 56 B200s](https://aiweekly.co/alerts/revolut-cuts-ai-coding-costs-90-with-self-hosted-glm-on-56-b200s), 2026-11-03

[^400_yen]: Twitter, [And to be honest the difference is negligible for seasoned engineers.](https://twitter.com/400_yen/status/2117552991595377024)

[^NashBriggsy]: Twitter, [30 cents per million is wild.](https://twitter.com/NashBriggsy/status/2117388169901707487), 2026-11-03

[^video]: YouTube, [How Revolut Cut AI Coding Costs 90% With Self-Hosted Open Models - David Abitbol, Revolut AI Engineer](https://www.youtube.com/watch?v=Ok6QdZHCcI8), 2026-10-29

[^corford]: <https://news.ycombinator.com/item?id=50351162>

[^NortySpock]: <https://news.ycombinator.com/item?id=50351437>

[^gosen]: <https://news.ycombinator.com/item?id=50350214>

[^mongrelion]: <https://news.ycombinator.com/item?id=50350398>

[^yolo3000]: <https://news.ycombinator.com/item?id=50350458>

[^gosen-rent]: <https://news.ycombinator.com/item?id=50351318>

[^user43928]: <https://news.ycombinator.com/item?id=50350618>

[^iLoveOncall]: <https://news.ycombinator.com/item?id=50351254>

[^littlecranky67]: <https://news.ycombinator.com/item?id=50351978>

[^kgeist]: <https://news.ycombinator.com/item?id=50352859>

[^torginus]: <https://news.ycombinator.com/item?id=50350375>
