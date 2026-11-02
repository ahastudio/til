# Cisco가 27세 엔지니어에게 토큰 무제한을 주고 레거시 코드 98%의 리팩터링을 맡겼다

원문: [Cisco is letting a 27-year-old refactor 98% of its legacy code with unlimited AI tokens: ‘Go nuts’](https://fortune.com/2026/10/30/cisco-president-jeetu-patel-gen-z-27-year-old-unlimited-ai-tokens-rewrite-legacy-code-entry-level-jobs/)

HN 토론: <https://news.ycombinator.com/item?id=50304122> (311점, 382개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=50303001> (5점, 5개 댓글)

GN 토론: <https://news.hada.io/topic?id=36324>

## 요약

Fortune은 2026년 10월 30일에 Cisco의 사장 겸 최고제품책임자 Jeetu Patel이 한
일을 전했다.
Patel은 조직도에서 자신보다 다섯 단계 아래에 있던 27세 엔지니어 Padmanabhan
Krishnamurthy(Paddy)에게 회사의 가장 큰 일 가운데 하나를 맡겼다.
Krishnamurthy는 실시간 번역 스타트업 EzDubs를 2023년에 공동 창업했고,
Cisco가 이 회사를 인수한 2025년에 입사했다.
Patel은 그가 조직 안에서 전략과 무관한 일을 하며 묻혀 있었다고 말했다.

Patel이 샌프란시스코 사무실에 들렀을 때 둘은 이야기를 나눴고,
Krishnamurthy는 두 사람 팀으로 Cisco의 레거시 코드를 다시 쓸 수 있다고 말했다.
Patel은 자기 팀의 가장 AI에 앞선 사람들도 그렇게 생각하지 못했다고 한다.
Patel은 스스로에게 4주를 주어 이를 증명하겠다고 했고,
최종 목표는 24개월 안에 레거시 코드의 98%를 리팩터링하는 것이다.
Patel은 코드를 리팩터링할 것이므로 토큰을 무제한으로 줬다며 마음껏 하라고
말했다고 기사는 전한다.

기사의 나머지는 Gen Z 채용에 관한 것이다.
Patel은 경험이 없는 사람만이 던질 수 있는 질문이 있다고 보고,
인턴을 역방향 멘토로 대하며, 그 때문에 생기는 긴장도 좋다고 말했다.
Stanford 장학생 Baya가 매달 AI에 대해 배운 것을 메일로 보내라는 시험을 빠짐없이
통과해 Cisco 인턴이 되었고, 경험 많은 직원들이 풀지 못한 무언가를 다시
설계했다는 일화도 있다.
Thrive Capital의 Josh Kushner, Tastewise의 Alon Chen,
will.i.am도 경험이 적은 젊은 인재를 찾는다고 말했다.
Patel은 자기 팀의 3분의 1은 Cisco 엔진을 아는 숙련 운영자,
3분의 1은 외부 시각을 가진 시스템 사고자,
나머지는 AI 네이티브인 창업자와 엔지니어로 구성한다고 밝혔다.

## 분석

### 기사의 주제는 코드 이식이 아니라 채용 철학이다

제목은 코드 98%의 리팩터링을 내세우지만 기사의 무게는 다른 곳에 있다.
코드 이야기는 앞부분에 있고, 이후는 젊은 인재가 왜 자산인지에 대한 Patel과
투자자들의 진술이다.
기사는 첫 문단에서 신입 일자리가 사라지고 있으며 관리자 약 40%가 AI가 더 싸게
일을 하므로 졸업생을 덜 뽑을 계획이라고 말한 점을 짚는다.
이 배경 속에서 Cisco의 사례는 반대 방향의 선택으로 소개된다.

그래서 이 글에서 Cisco의 코드는 주인공이 아니라 증거의 역할을 한다.
Patel의 논리는 경험이 적은 사람에게 큰 일을 맡기면 기존 방식의 가정을 흔들 수
있고, 그 사람에게 AI 토큰을 제한 없이 주면 그 효과가 증명된다는 것이다.
이 논리에서 4주와 24개월, 98%라는 숫자는 성과를 재는 기준이 아니라 도전의 크기를
보여 주는 장치로 쓰인다.

### 경험 있는 사람과 없는 사람을 섞는다는 구조가 실제 주장이다

Patel은 자기 팀을 세 부류로 구성한다고 말한다.
회사의 엔진을 아는 숙련 운영자, 외부 시각의 시스템 사고자,
창업 경험이 있는 AI 네이티브가 함께 일할 때 각각 따로일 때보다 훨씬
강하다는 것이다.
이 구조에서 Krishnamurthy는 세 번째 부류의 사례다.

여기서 눈여겨볼 점은 Patel이 경험을 낮추지 않는다는 것이다.
그는 숙련된 직원도 새로운 아이디어를 낼 수 있지만 경험이 없는 사람만 물을 수
있는 질문이 있다고 말한다.
즉 주장의 핵심은 젊음의 우월이 아니라 서로 다른 시야의 조합이다.
다만 기사는 이 조합이 이번 레거시 코드 프로젝트에서 어떻게 작동하는지,
첫 번째 부류의 사람들이 어떤 역할을 맡는지는 설명하지 않는다.

### 무제한 토큰은 자원이 아니라 신뢰의 표시로 쓰였다

Patel의 표현에서 토큰 무제한은 예산 항목이 아니라 신뢰의 신호다.
일반적인 회사에서는 이 규모의 프로젝트에 수십 년 경력이 있는 사람만 믿고
맡긴다는 것이 그의 진단이다.
그런 관행을 깨는 가장 눈에 띄는 방법이 토큰에 상한을 두지 않는 것이었다.

HN에서 fwlr은 이 결정이 코드가 아닌 다른 것들에 관한 것이라고 읽었다.
한 사람이 일을 맡는 한 회사의 비용은 거의 들지 않으며,
한 사람의 개인적인 처리 능력으로는 무제한이라는 말이 실제로 의미를 갖게 쓸 수
없을 것이라는 해석이다.[^fwlr]
이에 rogerrogerr는 자기 동료들이 병렬 워크플로를 광적으로 쓴다며 그 전제가
틀렸다고 답했고, sneak도 비슷하게 반박했다.[^rogerrogerr][^sneak]
토큰 무제한이 실제로 얼마나 쓰이는지는 기사에 나오지 않는다.

## 비평

### 98%라는 숫자는 분모를 알 수 없고 목적도 없다

HN에서 가장 먼저 나온 반응은 목표가 무엇이냐는 것이었다.
williadc는 기사에 98%의 코드를 다시 써야 하는 이유가 없다고 지적했다.[^williadc]
raincom은 “회사의 레거시 코드 98%”가 모호하다며,
코드베이스가 몇 개이고 지원되는 제품과 어떻게 연결되며 총 몇 KLOC인지
물었다.[^raincom]
blobbers는 새 C++ 코드로 다시 쓰는 것인지, 더 새로운 Linux로 옮기는 것인지,
Catalyst와 Meraki 스위치의 코드베이스를 통합하는 것인지 알 수 없다고
적었다.[^blobbers]

기사에는 이 질문들에 대한 답이 없다.
리팩터링의 대상이 펌웨어인지 내부 도구인지,
성공의 기준이 코드 줄 수인지 결함 수인지도 나오지 않는다.
따라서 98%라는 숫자는 분자도 분모도 정해지지 않은 목표이며,
4주 뒤에 무엇을 증명한 것으로 칠지도 열려 있다.

### 레거시 코드의 문서에 없는 요구사항이 기사에서 빠져 있다

HarHarVeryFunny는 코드를 다시 쓰는 일이 보통 피해야 할 일이라고 했다.
오래된 운영 코드는 버그 수정, 성능 조정, 특수 사례,
추가 요구사항이 쌓여 있고 문서와 테스트가 항상 따라가지는 않으므로 다시 쓴
코드가 처음에는 깔끔해 보여도 그 요구사항을 잃기 쉽다는
설명이다.[^HarHarVeryFunny]
Taikonerd는 이 엔지니어가 옛 코드가 왜 그렇게 쓰였는지,
고참들이 지금 다시 시작한다면 무엇을 다르게 했을지 아는 도메인 지식이 있는지
물었다.[^Taikonerd]
cromka는 시간이 지나면서 일부 버그가 사용자가 모르는 사이에 기능이 되었다고
지적했다.[^cromka]

이 우려에 반대하는 의견도 있었다.
rustyhancock은 레거시 코드가 흔히 유지되지 않고 아무도 어떻게 동작하는지 모르는
오래된 코드를 에둘러 말하는 표현이라며,
작동하는 코드의 재작성을 피하다 보니 2026년에 COBOL 프로그래머보다 COBOL 코드가
더 많아졌다고 썼다.[^rustyhancock]
btown은 LLM이 버그나 단순화 대상으로 보지만 실제로는 독특한 사용 사례를 지탱하던
것을 어떻게 가려낼지가 핵심 질문이라고 하면서,
한 회사의 코드 전체를 24개월에 다시 쓰면 점진적 배포에 쓸 시간이 거의 없다고
짚었다.[^btown]
어느 쪽이든 기사는 이 쟁점을 다루지 않는다.

### 인용된 사례는 모두 말하는 사람의 이해관계 안에 있다

기사의 주요 진술은 Patel 본인이 한 것이다.
HN의 simonw는 Fortune의 출처가 Patel 본인이며 그가 작은 라운드테이블 저녁
식사에서 말한 것이라고 짚었다.[^simonw]
piker는 이 글이 개인을 홍보하는 글처럼 읽힌다며,
보통이라면 회사나 결정 자체를 다룰 글에서 한 사람이 부각되는 것이 이상하다고
적었다.[^piker]

기사가 같이 인용한 Kushner, Chen, will.i.am도 자기 투자나 채용 전략을
말한 사람들이다.
이들의 발언은 젊은 인재를 찾는 이유에 대한 증언이지만,
그 전략이 성과를 낸다는 증거는 아니다.
기사에서 성과의 증거는 Kushner의 초기 투자 성과와 Baya의 일화 정도이고,
Cisco 프로젝트의 중간 결과는 아직 없다.

## 인사이트

### 재작성의 성패는 코드를 쓰는 속도가 아니라 동작이 같은지 확인하는 방법에 달려 있다

HN의 낙관적 경험담과 신중한 경험담은 같은 지점에서 갈린다.
balderdash는 20년 동안 개발된 임베디드 시스템의 코드베이스가 두 개발자의 은퇴 뒤
약 3개월, 토큰 약 2만 달러로 다시 쓰이고 문서화되었다고 했다.[^balderdash]
raizer88은 회사에서 이런 일이 있을 때마다 비즈니스 로직이 두 버전에서 같은지
누가 코드를 봤느냐고 묻는데, 답은 자동화된 테스트가 있다는 것이고 이어서 그
테스트를 누가 읽었느냐고 물으면 침묵이 흐르고 재작성은 보류된다고
썼다.[^raizer88]

micw는 AI가 기존 코드의 기능과 동작을 탐색하고,
모든 것에 대한 E2E 테스트를 먼저 쓰고, 사람이 기능 목록과 테스트 케이스를 검토한
뒤에 구현하고 테스트로 검증하는 순서를 제안했다.[^micw]
rstuart4133은 포괄적인 테스트 세트가 없다면 누군가 스스로를 속이는 것이라는
경험을 적었다.[^rstuart4133]
이 의견들을 합치면 재작성의 성공 조건은 구현 속도가 아니라,
기존 동작을 어떻게 기록하고 어떻게 비교하느냐다.
AI가 코드를 쓰는 비용이 낮아질수록 이 검증 쪽 비용의 비중이 커진다.

### 네트워크 장비는 같은 재작성이라도 검증 기준이 외부에 있다

Cyph0n은 IOS-XR 팀에서 일했다며 이 일이 생각보다 훨씬 복잡하고 현실과 동떨어진
곳에서 나온 허영 프로젝트처럼 들린다고 썼다.[^Cyph0n]
petra는 Cisco 코드가 정해진 명세를 따르고 속도와 지연 같은 측정 가능한 목표가
있으니 AI의 좋은 사례라고 했지만, pphysch는 실제 네트워크의 상호 의존적인 동작을
어떻게 시뮬레이션하느냐고 반문했다.[^petra][^pphysch]
mkjs는 현재 쓰이는 네트워크 프로토콜 다수가 수십 년 되었고 호환성을 유지하며
진화했으며, 벤더마다 표준을 조금씩 다르게 구현한다고 설명했다.[^mkjs]

이 맥락에서는 정답의 기준이 코드 안이 아니라 다른 벤더 장비와의 상호
동작에 있다.
테스트 세트를 만들 때도 표준 문서가 아니라 현장의 구현 편차를 담아야 한다.
기사의 98% 중에 이런 코드가 얼마나 있는지는 알 수 없고,
사내 도구와 펌웨어 중 어느 쪽이 큰지에 따라 같은 4주가 전혀 다른 의미가 된다.

### 젊은 인재를 쓰라는 주장은 따로, 재작성 프로젝트의 성패는 따로 판단해야 한다

기사는 두 이야기를 하나의 서사로 엮는다.
경험이 없는 사람이 새로운 질문을 한다는 주장과,
한 사람이 AI로 회사의 레거시 코드를 다시 쓸 수 있다는 주장이다.
그러나 두 주장은 독립적이다. 앞의 주장이 맞아도 뒤의 프로젝트는 실패할 수 있고,
반대의 경우도 가능하다.

jonathanlydall은 이 엔지니어가 인수된 회사의 창업자라는 점에서 같은 나이의 다른
사람보다 뛰어나고 성숙했을 가능성이 있지만 27세는 여전히 젊고 과신할 수 있다고
썼다.[^jonathanlydall]
GN에서 botplaysdice는 혁신이 이루어지는 과정은 늘 고통스럽겠지만 그 회사 시니어
엔지니어들이 느낄 기분은 이해된다고 적었다.[^botplaysdice]
skageektp는 말이 안 되는 일은 아닌 것 같다는 짧은 의견을 남겼다.[^skageektp]
GN의 두 반응은 모두 결과를 평가한 것이 아니라 일에 대한 느낌을 적은 것이어서,
4주 뒤의 결과를 판단할 근거는 아니다.
이 프로젝트를 평가할 수 있는 기준은 4주 뒤에 Patel이 무엇을 성공으로
공개하느냐이고, 그 기준은 아직 공개되지 않았다.

---

[^fwlr]: <https://news.ycombinator.com/item?id=50313176>

[^rogerrogerr]: <https://news.ycombinator.com/item?id=50313341>

[^sneak]: <https://news.ycombinator.com/item?id=50313458>

[^williadc]: <https://news.ycombinator.com/item?id=50304827>

[^raincom]: <https://news.ycombinator.com/item?id=50305339>

[^blobbers]: <https://news.ycombinator.com/item?id=50305293>

[^HarHarVeryFunny]: <https://news.ycombinator.com/item?id=50304948>

[^Taikonerd]: <https://news.ycombinator.com/item?id=50305003>

[^cromka]: <https://news.ycombinator.com/item?id=50314785>

[^rustyhancock]: <https://news.ycombinator.com/item?id=50304955>

[^btown]: <https://news.ycombinator.com/item?id=50317691>

[^simonw]: <https://news.ycombinator.com/item?id=50305417>

[^piker]: <https://news.ycombinator.com/item?id=50305010>

[^balderdash]: <https://news.ycombinator.com/item?id=50305103>

[^raizer88]: <https://news.ycombinator.com/item?id=50313867>

[^micw]: <https://news.ycombinator.com/item?id=50314881>

[^rstuart4133]: <https://news.ycombinator.com/item?id=50321679>

[^Cyph0n]: <https://news.ycombinator.com/item?id=50305963>

[^petra]: <https://news.ycombinator.com/item?id=50305351>

[^pphysch]: <https://news.ycombinator.com/item?id=50305402>

[^mkjs]: <https://news.ycombinator.com/item?id=50305585>

[^jonathanlydall]: <https://news.ycombinator.com/item?id=50315519>

[^botplaysdice]: <https://news.hada.io/topic?id=36324#cid68911>

[^skageektp]: <https://news.hada.io/topic?id=36324#cid68933>
