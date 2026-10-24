# 모델이 그렇게 좋다면 OpenAI는 왜 회사 100개를 직접 세우지 않는가

Ask HN: [If the models are so good, why doesn't OpenAI just start 100 companies?](https://news.ycombinator.com/item?id=50200997)

GN 토론: <https://news.hada.io/topic?id=35862>

## 요약

ex-aws-dude가 2026년 10월 22일에 올린 Ask HN이다.
질문은 이렇다.
최전선 모델이 정말 그렇게 좋다면, 모델을 파는 것을 주 수익원으로 삼는 이유가
무엇인가.
OpenAI나 Anthropic이 모델을 이용하는 회사와 제품을 직접 만들면 더 많이 벌 수
있지 않은가.
제목이 과장이라고 스스로 밝히지만, 토큰 판매가 정말 최선의 전략이냐고 묻는다.
가격이 내려가고 상품화가 진행되면 돈이 모델 쪽(유틸리티)보다 애플리케이션 쪽에
있다는 신호가 아니냐는 것이다.

이 스레드는 이 문서를 읽은 시점에 약 600점을 받았고 댓글 수백 개가 달렸다.
이 문서는 하위 댓글 수가 많은 상위 댓글과 그 답글 위주로 읽었으며, 전체를 읽지는
않았다.
답변은 대체로 일곱 가지 방향으로 갈렸다.

첫째, 모델은 두뇌일 뿐 회사는 팔다리와 관계가 필요하다는 답이다.
둘째, 이미 하고 있다는 답이다.
셋째, 재무와 시간의 압박 때문에 지금 증명된 토큰 매출을 택한다는 답이다.
넷째, 금광 열풍에서는 곡괭이를 파는 것이 낫다는 답이다.
다섯째, 집중의 문제로, 모델 경쟁이 치열해서 하류에 쓸 관심이 없다는 답이다.
여섯째, 앱스토어와 플랫폼의 비유로, 모든 앱을 직접 만들지 않고 수수료를 받는
것이 위험 없는 돈이라는 답이다.
일곱째, 질문의 전제를 뒤집어 AI가 만드는 가치가 사라지니 수익이 붕괴한다는
답이다.

## 분석

### 가장 많은 지지를 받은 답: 두뇌는 회사가 아니다

가장 큰 하위 스레드를 만든 epsteingpt는 맥킨지가 컨설팅과 운영 지식에도 불구하고
포천 500대 기업을 장악하지 못한 것과 같은 이유라고 답했다.
AI는 두뇌이고 회사에는 팔다리와 관계가 필요하며, 직원 대부분이 창업가가 아니듯
컨설턴트도 마찬가지라는 것이다.
토큰 안에 수조 개의 회사 아이디어가 있지만 실현하려면 수년의 시간과 인내와
자본과 맞는 사람이 필요하다고 한다.[^epsteingpt]
moezd는 공장은 지어지겠지만 여전히 작업자와 프로젝트 엔지니어와 설계자가
필요하다고 덧붙였다.[^moezd]
paxy는 회사 하나를 운영하는 것이 100개를 운영하는 것보다 쉽고 성공에는 좋은
소프트웨어 이상이 필요하다고 했다.[^paxy]
이 답의 약점은 devin이 짚었다.
질문을 바꿔 모델이 그렇게 좋다면 왜 사업을 운영하지 못하느냐고 되물은
것이다.[^devin]

### 이미 하고 있고 제품 포트폴리오가 곧 그 시도라는 답

CoolestBeans는 네 가지를 들었다.
그들은 이미 시작했고(OpenAI의 제품 포트폴리오에 응용 시도가 많다), 장시간
에이전트로 토큰을 파는 것이 매출 성장으로 증명된 유일한 일이며, 매출이 시급하고
차입 금리가 오른 탓에 자본 접근이 예전 같지 않다.
또한 의사결정자 일부가 AI에 제본스 역설이 나타나 가격이 내려도 총 사용이 늘
것이라고 믿는다고 했다.[^coolestbeans]
fennecbutt는 이 셋째 이유(재무 압박)가 가장 크다고 보았다.
OpenAI는 기존 투자를 아직 상각하지 못했고 새 투자를 멈추지도 않았으므로 새로운
사업 1천 개는 더 많은 부채와 불확실성이라는 것이다.[^fennecbutt]
Unknown_Unknown은 SaaS 회사 하나에 시간과 자원, 마케팅과 법무를 들여 연매출
수백만 달러를 얻어도 시장과 투자자가 기대하는 규모에 못 미친다고
했다.[^unknown_unknown]
aristofun은 수백 개 회사가 이미 그들의 모델을 감싼 껍데기이고, 그들은 약간의
이익을 포기하는 대신 그 회사들이 떠안는 위험을 피하며 나중에 가장 수익성 좋고
위험이 낮은 회사를 사거나 없앨 것이라고 했다.[^aristofun]
이 주장은 스레드에서 직접 반박되지 않았고, 이 문서가 확인할 근거도 없다.

### 곡괭이와 플랫폼 비유는 서로 다른 논리다

adelekeabdulgan은 금광 열풍에서 가장 좋은 전략은 삽을 파는 것이며, 사용자가 다음
큰 것을 만들든 못 만들든 그들은 돈을 번다고 했다.[^adelekeabdulgan]
vanschelven은 삽을 손해를 보며 파는 것은 최선이 아니며 삽 종속 효과가 없다면
성립하지 않는다고 반박했다.[^vanschelven]
NormalGoat는 애플이 앱스토어의 모든 앱을 만들지 않은 이유와 같다며, 토큰 판매는
사업 위험 없이 앱마다 일정 몫을 받는 위험 없는 돈이라고 했다.[^normalgoat]
psadri는 이는 다른 논거라고 했는데, 애플은 크게 성공한 오래가는 앱을 실제로
베끼며 이를 업계에서 Sherlocked라고 부른다는 것이다.[^psadri]
janalsncm은 표준 비유는 햄버거가 아니라 삽이고, 질문은 도구를 파는 쪽이 만들어진
것을 직접 만들지 않느냐는 것이므로 정당하다고 했다.[^janalsncm]

### 질문의 전제를 뒤집는 답: 가치가 사라진다

throwyawayyyy는 OpenAI 에이전트가 쉽게 다시 만들 수 있는 회사의 이익은 0으로
수렴하는데, 다른 이의 에이전트도 쉽게 할 수 있기 때문이라고 했다.
OpenAI와 Anthropic의 경제가 이상한 이유는 수조 달러의 가치를 확보해야 하는데 그
수조 달러가 사라질 것이기 때문이라는 설명이다.[^throwyawayyyy]
LeFantome은 AI가 상품화한 영역의 경쟁이 이익을 끌어내리고 AI 자체도 상품이 되면
이익이 어디서 나올지 묻는다고 동의했다.[^lefantome]
vostrocity는 George Hotz가 비슷한 관점을 썼다며 링크를 달았지만 이 문서는 그
글을 열어 보지 않았다.[^vostrocity]
JeremyNT는 LLM이 사람들이 돈을 낼 유일한 소프트웨어가 될 것이라서 다른
소프트웨어 사업을 시작할 이유가 없다고 했다.[^jeremynt]

## 비평

### 곡괭이 비유는 질문에 답하지 않고 질문을 바꾼다

가장 흔한 답인 곡괭이 장수는 왜 광산을 하지 않는지의 이유를 말하지 않는다.
금광에서 곡괭이 장수가 광산을 하지 않는 이유는 광부들이 곡괭이를 계속 산다는
점과 광산 위험을 지지 않는다는 점이다.
이 비유가 성립하려면 곡괭이를 산 사람들이 모두 금을 찾지 못해도 곡괭이 가격이
유지돼야 하는데, 질문자는 바로 그 가격이 내려가고 있다고 전제했다.
simianwords는 곡괭이 비유가 생각을 멈추게 하는 상투어이고 AI가 사라지는 것을
전제한다고 비판했다.[^simianwords]
따라서 곡괭이 비유는 질문의 핵심(가격 하락)을 다루지 않고, 비유가 맞는지는
가격이 하락할 때 모델 판매 사업의 이익이 유지되는지에 달려 있다.

### 이미 업종을 죽였다는 주장은 근거 없이 단정된다

maxdo는 질문이 잘못 형성됐다며 이미 산업 전체를 죽였다고 했다.
소프트웨어 개발 도구와 모든 IDE, 개발 분석 도구가 죽었고, 투자를 받은 AI 터미널
스타트업은 존재 이유를 설명하기 어렵다는 식이다.[^maxdo]
saidnooneever는 죽은 업종의 목록과 근거를 요구했고,[^saidnooneever] ActionHank는
개발자들이 디버깅과 프로파일링과 코드 리뷰 없이 곧바로 프로덕션에 올린다는
뜻이냐며 반박했다.[^actionhank]
bityard는 약간 멋을 낸 터미널과 워크플로 편집기에 벤처 자금을 대는 일이 처음부터
위험한 선택이었을 것이라고 보았다.[^bityard]
이 주장은 업계의 현실이 아니라 한 사람의 인상이며, 스레드 안에서도 근거가
제시되지 않았다.

### 일화 하나가 일반 법칙처럼 쓰인다

aenis는 자기 회사에서 모델이 전부 만든 프로젝트(사람이 한 줄도 쓰거나 읽지
않음)가 가장 빠르게 성장하는 수익원이 됐고, 존재한 지 두 달 만에 마진 약 9%에
매출 8,900만 달러에 이르렀으며 개발 비용은 토큰 약 4만 달러였다고
적었다.[^aenis]
이는 한 회사의 서술이며 검증할 수 없고, 마진 9%라는 수치는 매출 규모에 비해 이
사업이 얼마나 많은 비용을 다른 곳에 쓰는지를 알려 주지 않는다.
saithound는 자문하는 대기업이 Figma에서 Anthropic Claude로 옮겼다고
했는데,[^saithound] jen729w는 출처를 요구했다.[^jen729w]
이런 일화는 질문에 답하지 못하고, 모델 회사가 직접 사업을 하는 일이 이미
일어나고 있다는 주장의 증거로 보기에는 약하다.

### 어떤 답도 숫자를 내놓지 않는다

스레드의 거의 모든 답은 정성적인 논리이고, 토큰 판매의 마진과 응용 사업의 기대
수익을 비교한 숫자는 보이지 않았다.
Unknown_Unknown이 인용한 손실 수치(Anthropic 6개월 800억, OpenAI 210억)는 이
문서가 확인하지 못했다.[^unknown_unknown]
어느 쪽이 더 많이 번다는 질문의 핵심은 숫자 없이는 답할 수 없고, 이 스레드는 그
숫자가 공개된 적이 없다는 사실을 보여 주는 것에 가깝다.

## 인사이트

### 모델 회사의 선택은 사업 전략이 아니라 시간의 문제로 읽힌다

가장 설득력 있는 답은 하나의 이유가 아니라 이유들의 곱이다.
수익이 지금 필요하고, 응용 사업은 느리고 개별 규모가 작고, 모델 경주에서 앞서는
것의 보상이 크다.
seizethecheese는 NVIDIA가 왜 최고의 모델을 만들지 않고 TSMC가 왜 칩 설계를 하지
않느냐고 되물으며, 모델 경쟁이 치열한 지금은 하류에 집중하는 것이 의미가 없다고
답했다.[^seizethecheese]
이는 시간이 지나 경주의 속도가 느려지거나 모델이 상품화되면 모델 회사의 선택도
바뀔 수 있다는 뜻이다.
dofm은 Alex Karp가 CNBC 인터뷰에서 코드가 그렇게 좋다면 왜 토큰 단위로 팔고
수익의 일부를 요구하지 않느냐고 물었다고 전하며, OpenAI가 결국 수명이 짧은
컨설팅과 SaaS 분사 회사들을 세울 것이라고 보았다.[^dofm]
이 문서는 그 인터뷰를 열어 보지 않았다.

### 가치 포획의 문제는 고객이 모델 회사의 경쟁자가 되는 것이다

vladimirralev는 모델 회사가 직접 사업을 하면 사람들이 지식 기반을 공유하기를
꺼리고 규제도 나설 것이라고 했다.
지식 기반을 모델에 계속 주는 한 영리한 선택은 기다리는 것이라는
설명이다.[^vladimirralev]
amelius는 공개적으로 하지 않아도 된다고 했고,[^amelius] PaulRobinson은 지식
기반을 공유한 사람은 없다고 반박했다.[^paulrobinson]
이 대화는 모델 회사와 고객 사이의 신뢰가 경쟁 구도의 일부임을 보여 준다.
모델 회사가 하류에 들어가면 고객은 기능을 쓰는 것이 아니라 경쟁자에게 입력하는
것이 되고, 이것이 직접 사업을 막는 비용이 될 수 있다.
다만 vladimirralev가 한 연구소의 내부 벤치마크가 인기 제품 20개 이상을 복제하는
것이라는 주장을 덧붙인 것은 이 문서가 확인하지 못했다.

### 이 스레드를 읽는 방법

질문의 전제(좋은 모델이면 사업도 잘한다)는 모델이 좋은 것과 사업을 하는 것이
같은 능력이라고 본다.
답들의 공통 분모는 둘이 다르다는 인식, 그리고 돈이 어디에 있는지는 시점에 따라
바뀐다는 인식이다.
이 스레드의 어떤 답이 맞는지를 가를 관찰은 두 가지다.
모델 회사의 응용 사업 매출이 모델 판매 매출에서 차지하는 비중이 커지는지, 모델
가격이 계속 내려갈 때 모델 판매의 총이익이 유지되는지다.
둘 다 공개되기 전에는 이 스레드는 의견의 모음으로 남는다.

---

[^epsteingpt]: <https://news.ycombinator.com/item?id=50207846>

[^moezd]: <https://news.ycombinator.com/item?id=50207970>

[^paxy]: <https://news.ycombinator.com/item?id=50201337>

[^devin]: <https://news.ycombinator.com/item?id=50201471>

[^coolestbeans]: <https://news.ycombinator.com/item?id=50201229>

[^fennecbutt]: <https://news.ycombinator.com/item?id=50202562>

[^unknown_unknown]: <https://news.ycombinator.com/item?id=50208411>

[^aristofun]: <https://news.ycombinator.com/item?id=50208662>

[^adelekeabdulgan]: <https://news.ycombinator.com/item?id=50207604>

[^vanschelven]: <https://news.ycombinator.com/item?id=50207799>

[^normalgoat]: <https://news.ycombinator.com/item?id=50201618>

[^psadri]: <https://news.ycombinator.com/item?id=50201878>

[^janalsncm]: <https://news.ycombinator.com/item?id=50201925>

[^throwyawayyyy]: <https://news.ycombinator.com/item?id=50213253>

[^lefantome]: <https://news.ycombinator.com/item?id=50213618>

[^vostrocity]: <https://news.ycombinator.com/item?id=50213995>

[^jeremynt]: <https://news.ycombinator.com/item?id=50208606>

[^simianwords]: <https://news.ycombinator.com/item?id=50206704>

[^maxdo]: <https://news.ycombinator.com/item?id=50207828>

[^saidnooneever]: <https://news.ycombinator.com/item?id=50208206>

[^actionhank]: <https://news.ycombinator.com/item?id=50208245>

[^bityard]: <https://news.ycombinator.com/item?id=50208359>

[^aenis]: <https://news.ycombinator.com/item?id=50206802>

[^saithound]: <https://news.ycombinator.com/item?id=50206091>

[^jen729w]: <https://news.ycombinator.com/item?id=50206289>

[^seizethecheese]: <https://news.ycombinator.com/item?id=50212522>

[^dofm]: <https://news.ycombinator.com/item?id=50201907>

[^vladimirralev]: <https://news.ycombinator.com/item?id=50205797>

[^amelius]: <https://news.ycombinator.com/item?id=50206021>

[^paulrobinson]: <https://news.ycombinator.com/item?id=50206891>
