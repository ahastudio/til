# United 항공이 개인 AI 에이전트의 항공권 예약을 금지한다: 보안과 규정을 내세웠지만 쟁점은 중개 구조와 가격이다

원문: [United Airlines bans AI agents from booking flights on behalf of travelers](https://www.cbsnews.com/news/united-airlines-bans-ai-agents-booking-flights/)

HN 토론: <https://news.ycombinator.com/item?id=50458900> (391점, 378개 댓글)

GN 토론: <https://news.hada.io/topic?id=37014>

## 요약

CBS News의 MoneyWatch는 2026년 11월 11일, United 항공이 수요일에 AI 에이전트가
여행객을 대신해 항공편을 예약하는 것을 금지한다고 밝혔다고 보도한다.
이유로는 보안 위험과 연방 규정을 어길 가능성을 든다.

기사는 많은 소비자가 Meta의 Muse나 OpenAI의 dots 같은 AI 에이전트로 제품 조사,
특가 찾기, 구매까지 맡긴다고 설명한다.
항공권을 예약하려면 에이전트가 결제 정보 같은 자격 증명을 포함한 고객의 개인
정보에 접근해야 한다.
United는 계정 자격 증명을 개인용 제3자 AI 비서와 공유하면 민감한 정보가 노출될
수 있고, 이런 도구의 행동이 의도하지 않은 구매, 계정 변경, MileagePlus 마일
사용을 낳을 수 있다고 했다.
또 AI 에이전트로 체크인을 하는 것 같은 행동은, 여행객이 위험 물질이 짐에 없음을
직접 확인하도록 요구하는 규정을 포함한 연방 규정을 어길 수 있다고 했다.

United는 “디지털 플랫폼 안에서 직접, 그리고 여행사와 판매 대행업체를 통해
간접적으로 접근을 제한해 승인받지 않은 제3자 개인 AI 에이전트나 비서의 사용을
금지”하겠다고 밝혔고, 이를 반영해 예약과 발권 정책을 고치는 중이다.

항공 분석가 Henry Harteveldt(Atmosphere Research Group)는 이 정책이 United가
고객의 예약 과정을 통제하고 싶어 한다는 뜻이라고 해석했다.
그는 United가 Google 검색, 가격 비교 메타서치 사이트, 온라인 여행사에 더해 더
강력할 수도 있는 중개자를 하나 더 원하지 않는 것이며, 항공편 검색에는 항공사의
돈이 들기 때문에 AI 봇의 검색 급증에 따른 비용을 피하려 할 것이라고 말했다.
Southwest는 다른 길을 택해 ChatGPT 사용자가 자사 웹사이트에 접근해 항공편 재고를
볼 수 있게 했다.
Harteveldt는 United 항공권이 Kayak, Hopper, Google Flights 같은 통합
판매처에서는 계속 예약 가능하고 소비자가 좋은 요금을 찾는 것이 더 어려워지지는
않겠지만, AI 봇을 막는다고 United 요금을 찾기가 쉬워지지도 않는다고 덧붙였다.

## 분석

### 공식 이유와 분석가의 이유가 다르다

United가 직접 든 이유는 두 가지다.
하나는 자격 증명 공유의 보안 위험이고, 다른 하나는 체크인 같은 행위가 연방
규정을 어길 수 있다는 것이다.
기사에 인용된 분석가는 통제와 비용을 이유로 본다.
HN의 ProblemExplorer는 항공이 거의 상품에 가까운 사업이고 승객이 5달러 때문에
항공사를 바꾼다고 설명하며, 개인 AI 에이전트가 국지적 최적을 만들고 나머지
여행객의 가격을 올린다고 주장했다.[^ProblemExplorer]
이를 간결하게 설명한 댓글로 그가 가리킨 _diyar는, 지불 의사가 100달러인 Alice와
50달러인 Bob에게 각각 그 값을 받으면 평균 75달러를 거두는데, 에이전트가
Alice에게 싼 표를 찾아 주면 같은 평균을 위해 모두에게 75달러를 받아야 하고 Bob은
시장에서 빠진다고 예를 들었다.[^_diyar]
이는 가격 차별 구조가 에이전트로 흔들린다는 해석이며, United가 이를 이유로 말한
것은 아니다.

### 이미 열려 있는 경로와 막으려는 경로가 구분되어 있다

기사에 따르면 Kayak, Hopper, Google Flights 같은 판매처에서는 계속 예약된다.
막으려는 대상은 “승인받지 않은 제3자의 개인 AI 에이전트나 비서”다.
같은 판매처 안에 있어도 사용자가 그 위에서 에이전트를 돌리면 어디까지가
금지인지는 기사에 없다.
United가 금지하는 것은 에이전트 자체라기보다 승인 없이 계정 접근을 대행하는
경로로 읽을 수 있다.
“승인받지 않은”이라는 단서는 승인받은 경로가 있을 수 있다는 여지를 남기지만,
기사는 그런 경로가 있는지 말하지 않는다.

### 비용 주장은 규모를 알 수 없다

분석가는 항공편 검색에 돈이 들고 AI 봇이 검색을 폭증시킨다고 했다.
HN의 pavel_lishin은 얼마나 드는지, 비싸다면 결과를 캐시하는 중개자가 오히려 싸지
않은지 물었다.[^pavel_lishin]
rootsudo는 Sabre 같은 예약 시스템(GDS)을 거치면 예약과 과도한 조회에 건당 몇
센트의 수수료가 들 수 있고, 항공사에 따라 조회마다 소액이 든다고 설명하면서도
그렇다면 가격을 올리고 접근을 쉽게 하는 편이 낫다고 덧붙였다.[^rootsudo]
이 댓글은 한 사용자의 설명이며 United의 실제 구조는 기사에 없다.

## 비평

### 규정 위반이라는 이유는 예약 금지의 근거로는 약하다

기사가 인용한 규정 문제는 체크인 때 짐에 위험 물질이 없다는 직접 확인이다.
이는 예약이 아니라 체크인에 관한 이야기이고, 금지는 “예약”에 걸려 있다.
HN의 aucisson_masque는 이를 우스꽝스럽다고 보고 항공사가 요금표를 비교하기
어렵게 유지해 더 많이 받으려 한다고 썼다.[^aucisson_masque]
charles_f는 자격 증명 공유가 정보를 노출한다는 논거를 악의적이라고 보며, 이
조치가 고객에게 이로운 쪽에 해로워서 막은 것이라고 했다.[^charles_f]
이는 동기에 대한 추측이다.
반대로 figassis는 규제 산업에서 시스템을 만들어 본 경험으로, 사용자가
서비스약관에 동의했다는 것을 LLM이 대신 했다면 어떻게 증명하겠느냐며 자동화는
바라는 만큼 단순해지지 않는다고 썼다.[^figassis]
기사는 어떤 연방 규정이 정확히 무엇을 요구하는지 밝히지 않는다.

### 집행이 가능한지 기사가 다루지 않는다

doctoboggan은 Claude의 브라우저 확장 같은 컴퓨터 사용 에이전트를 쓰는 사람을
United가 어떻게 막겠느냐고 물었고 상점과의 관계가 적대적이 되어 간다고
했다.[^doctoboggan]
olouv는 일반 Safari를 사람처럼 조작하는 에이전트를 직접 만들어 봤는데 이를
어떻게 탐지하는지 모르겠다고 했다.[^olouv]
andix는 브라우저를 쓰면 막을 수 없고, 할 수 있는 것은 IP나 지문으로 속도를
제한하는 것이라고 했다.[^andix]
기사는 United가 에이전트를 어떻게 탐지하겠다는 기술적 수단을 말하지 않는다.
금지가 정책 문구인지 기술적 차단인지에 따라 효과가 크게 달라진다.

### 법적 결과는 댓글마다 정반대로 그린다

otterley는 막지 못해도 나중에 약관이나 운송 계약 위반을 이유로 항공편을 취소할
수 있다고 했다.[^otterley]
lovich는 분쟁이 커지면 Computer Fraud and Abuse Act를 어긴 것이 될 수 있어서
이는 기술이 아니라 법의 문제라고 썼다.[^lovich]
qurren은 키보드와 마우스를 흉내 내는 장치까지 막는다면 시각 장애인이나 반복 사용
장애가 있는 사람의 보조 도구를 차별하는 것이므로 ADA 위반이라고 주장하겠다고
했다.[^qurren]
이들은 모두 개인의 법적 견해이고 기사나 United가 말한 것이 아니다.
확인할 수 있는 것은 이 정책의 집행이 법적으로 시험될 가능성을 독자들이 이미
상정한다는 점이다.

### 에이전트가 항공권 예약에 맞는 일인지부터 의문이 있다

cmpolis는 항공권, 호텔, 공연 예매가 에이전트 자동화의 표준 예시가 된 것이
이상하다고 썼다.
이미 Google Flights로 2분이면 되고, 결과를 완전히 통제하고 싶으며, 큰 결제가
필요하고, 여행을 계획하는 것 자체가 즐거움이라는 이유다.[^cmpolis]
teliskr도 AI 시연에서 항공권 예약이 예시로 자주 쓰이는 것이 불편하며 대부분은
전용 UI가 낫다고 했다.[^teliskr]
이 반응이 맞다면 금지의 실제 영향은 기사가 말하는 것보다 작을 수 있다.
다만 이는 몇 사람의 선호이며 사용 규모의 자료는 없다.

## 인사이트

### 재예약 같은 “게으름의 세금”을 에이전트가 없앤다는 것이 진짜 쟁점일 수 있다

bz_bz_bz는 United에서 가격이 내려가면 재예약해서 차액을 여행 크레딧으로 받을 수
있고 (기본 이코노미 제외), 이 옵션은 예약 뒤 가격을 다시 확인하지 않는 여행객
때문에 저평가된 것으로 여겨진다고 했다.[^bz_bz_bz]
AI 에이전트는 이 “게으름의 세금”을 줄이고 다른 산업도 같은 걱정을 한다고 한다.
이 시각은 규정과 보안이 아니라 항공사의 수익 모델이 정책의 뿌리라는 가설로,
기사의 분석가 설명(통제와 비용)과 결이 다르다.
이는 댓글의 가설이며 확인된 바 없다.

### “승인받지 않은”이라는 단서가 정책의 방향을 정한다

Southwest가 ChatGPT 사용자에게 재고를 보여 주는 쪽을 택한 것과 비교하면 두
항공사는 에이전트를 막느냐 열느냐보다 누가 에이전트의 접근 조건을 정하느냐에서
갈린다.
HN의 andix는 항공권을 예약하려면 API나 MCP를 제공하는 믿을 만한 여행사를 쓰고
에이전트는 특가를 찾는 데만 쓰라고 했는데, mimischi는 그런 곳이 실제로 있느냐고
되물었다.[^mimischi]
siliconc0w는 에이전트에 자격 증명을 통째로 주지 않고 브라우저 쿠키를 범위가
제한된 작업에만 선택적으로 주입하는 방식을 만들고 있다고 썼다.[^siliconc0w]
United가 우려하는 보안 위험이 진짜라면 해법은 에이전트 금지가 아니라 승인과 권한
위임의 표준일 수 있다.
이는 이 문서의 해석이며, United가 승인받은 에이전트의 경로를 만들겠다고 말한
것은 기사에 없다.

### 결론을 바꿀 관찰

- United가 승인받은 제3자 에이전트에 공식 API나 인증 방식을 내놓는다면, 금지는
  차단이 아니라 라이선스 정책이라는 읽기가 맞게 된다.
- 항공사가 탐지와 차단의 기술 수단을 공개하거나 약관 위반으로 예약을 취소한
  사례가 나오면, 집행의 현실성에 대한 의문이 풀린다.
- 에이전트로 재예약한 가격 차이나 검색 비용에 대한 자료가 공개되면, 수익 모델이
  원인이라는 가설과 비용 주장 모두 검증된다.

---

[^ProblemExplorer]: <https://news.ycombinator.com/item?id=50459287>

[^_diyar]: <https://news.ycombinator.com/item?id=50459444>

[^pavel_lishin]: <https://news.ycombinator.com/item?id=50459145>

[^rootsudo]: <https://news.ycombinator.com/item?id=50459361>

[^aucisson_masque]: <https://news.ycombinator.com/item?id=50459483>

[^charles_f]: <https://news.ycombinator.com/item?id=50460319>

[^figassis]: <https://news.ycombinator.com/item?id=50460757>

[^doctoboggan]: <https://news.ycombinator.com/item?id=50459506>

[^olouv]: <https://news.ycombinator.com/item?id=50459468>

[^andix]: <https://news.ycombinator.com/item?id=50459448>

[^otterley]: <https://news.ycombinator.com/item?id=50459608>

[^lovich]: <https://news.ycombinator.com/item?id=50462164>

[^qurren]: <https://news.ycombinator.com/item?id=50459727>

[^cmpolis]: <https://news.ycombinator.com/item?id=50459719>

[^teliskr]: <https://news.ycombinator.com/item?id=50459845>

[^bz_bz_bz]: <https://news.ycombinator.com/item?id=50459841>

[^mimischi]: <https://news.ycombinator.com/item?id=50459547>

[^siliconc0w]: <https://news.ycombinator.com/item?id=50460035>
