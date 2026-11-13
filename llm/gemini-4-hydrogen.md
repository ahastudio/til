# Gemini 4 Hydrogen은 빠른 실행용 모델을 모든 사용자에게 내놓으며 가격과 이름에서 의문을 남긴다

원문: [Introducing Gemini 4 Hydrogen](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/)

HN 토론: <https://news.ycombinator.com/item?id=50471431> (531점, 334개 댓글)

GN 토론: <https://news.hada.io/topic?id=37068>

## 요약

Google이 2026년 11월 12일에 올린 발표 글로, 글쓴이는 Google DeepMind의 Koray Kavukcuoglu이다.
Gemini 4 Hydrogen은 코딩과 에이전트 작업에서 빠른 실행을 목표로 하는 모델이다.
Google은 Gemini 4 Carbon과 Gemini 4 Argon을 깊고 긴 추론을 위한 최상위 모델로 두고,
Hydrogen을 여러 에이전트 작업에서 빠르게 실행하는 모델로 자리매김한다.
Hydrogen은 Google AI Studio, Gemini API, 기업용 Gemini, Gemini 앱, Google 검색에 모든 등급으로 들어가고,
Google AI Pro와 Ultra 유료 구독자는 Google Antigravity에서도 쓸 수 있다.

### Google이 내놓은 수치

아래는 모두 Google의 주장이다.

- Artificial Analysis Intelligence Index에서 기본 높음(high) 사고 수준으로 51점을 얻어 Argon의 50점을 넘고, 가장 높은 xhigh 수준에서는 54점이다.
- 1백만 토큰 컨텍스트 전체에 걸쳐 가격이 같고, 입력 100만 토큰당 1.50달러, 출력 100만 토큰당 7.50달러이다.
- Gemini 3.8 Flash보다 기본 수준에서 2.5배 빠르게 작업을 끝내고, Terminal-Bench 4.1 점수는 18.2%에서 57%로 세 배 넘게 올랐다. 근거 없는 주장(fabricated claims)은 5배 넘게 줄었다고 한다.
- 파트너 초기 시험에서 3.8 Flash 대비 2배에서 2.8배 빠르고 토큰 사용이 12~23% 줄었다고 한다.
- 도구 호출 실패나 빈 검색 결과가 나올 때 매끄럽게 적응한다고 한다.
- arena.ai의 Agent Arena에서 5위이고, HLE-Diamond에서 58.8%로 같은 등급 모델 중 선두라고 한다. Vals Tax Agent Bench에서는 52.3%로 1위, Vals Legal Research Bench에서는 55.8%로 공동 1위라고 한다.

### Orchestrator와 사고 수준

같은 날 Google은 Antigravity에 Orchestrator를 넣는다고 밝혔다.
한 세션 안에서 Carbon과 Hydrogen 같은 모델 사이를 자동으로 바꾸는 기능이다.
Terminal-Bench 4.0에서 Orchestrator가 Carbon에 가까운 작업 성공률을 내면서 평균적으로 쿼터를 24% 덜 쓰고 19% 빨랐다고 한다.
병렬 에이전트 작업에서는 Carbon이 조정자를 맡고 Hydrogen이 작업자와 검증자를 맡는 구성을 제시한다.

Hydrogen은 사고 수준이 낮음, 중간, 높음(기본), 새로 생긴 xhigh의 네 단계이다.
발표는 이 단계들이 품질과 지연과 비용 사이에서 매끄럽고 예측 가능하게 올라간다고 설명한다.

### 안전 주장

발표는 Hydrogen이 3.8 Flash보다 에이전트 작업에서 과잉 행동(overreach)을 최대 81% 줄이고,
부족 서비스(under-service)를 최대 79% 줄이며,
도구 사용과 코딩 평가에서 정렬되지 않은 행동과 과제 지름길 택하기를 12배 줄였다고 한다.
불가능하거나 막힌 작업에서 권한 경계를 우회할 가능성은 최대 2배 낮아졌고,
내부 에이전트 정직성 평가의 정직 비율은 96.7%라고 한다.
감사한 20만 개 넘는 턴에서 사고 과정의 가독성이 99.9% 유지되고 기만적인 추론 편집은 없었다고 한다.
간접 프롬프트 주입에 대해서는 Gray Swan IPI 벤치마크에서 2.3배 넘게 강건하다고 한다.
이 수치들은 Google 내부 평가이며, 이 문서는 모델 카드를 열어 보지 않았다.

## 분석

### 중심 주장은 중간 가격의 실행 모델이 일상 작업의 기본이 된다는 것이다

발표의 구조는 모델 계층을 나눈다.
깊은 판단은 Carbon과 Argon이 맡고, 코드를 쓰고 테스트를 돌리고 변경을 검증하는 일은 Hydrogen이 맡는다.
이 계층은 Orchestrator가 자동으로 오가게 하는 기능으로 제품화되었다.
Google은 비용 대비 성능을 강조하며, 같은 계열 안에서 일을 나누어 쿼터와 시간을 아낀다는 이야기를 한다.
이는 이미 여러 개발 도구가 추구해 온 모델 라우팅의 한 형태이다.
HN의 한 댓글은 이 발표에서 가장 중요한 부분이 하네스에 기본으로 내장되는 Orchestrator일 수 있다고 평했다.[^behat]

### 모든 사용자에게 같은 모델을 준다는 것이 배포의 핵심이다

발표는 Hydrogen이 검색을 포함한 모든 소비자 표면에 들어간다고 쓴다.
한 댓글은 무료 기본 모델이 최상위에 가까워지는 것이 일반인이 체감하는 AI 지능을 크게 올릴 것이라고 본다.[^jacob]
다른 댓글은 Gemini 앱에서 Hydrogen이 Flash 자리를 대체했고 Lite는 아직 남아 있다고 전한다.[^netrem]
한 사용자는 Hydrogen을 앱에서 어떻게 고르는지 알 수 없다고 했는데,[^qnleigh]
이는 배포가 점진적이고 선택 화면이 일관되지 않다는 신호이다.

### 비교의 기준이 Google의 선택이다

발표의 비교 대상은 Gemini 3.8 Flash와 Argon, 일부 벤치마크에서의 같은 등급 모델이다.
HN의 한 댓글은 이 글이 Terra와 Sonnet에 대한 시간과 작업당 비용 그래프를 직접 비교해 보여 주어 좋다고 평했고,
코딩 밖의 영역에서는 Sonnet보다 나은 선택으로 보이고 높은 추론에서는 Terra보다 똑똑하지만 조금 비싸다고 정리했다.[^modeless]
Artificial Analysis 지수 51 대 50이라는 차이는 작고, 같은 지수에서 Sonnet과 Terra가 약해 보인다는 댓글도 있다.[^ngomez]
이 해석은 지수의 신뢰에 달려 있다.

## 비평

### 가격이 빠르고 싼 등급을 포기하는 것처럼 보인다

가장 강한 반응은 가격이다.
한 댓글은 Hydrogen이 가장 가벼운 원소라는 점과 2.5배 빠르다는 점에서 진입 등급으로 보이는데,
가격이 할인이 끝난 3.8 Flash와 같고 현재 사용자들이 내는 값보다 훨씬 높다고 지적한다.
이것이 빠르고 싼 층을 포기하는 것이면 가격 민감한 업무 부하가 이탈할 것이라고 우려한다.[^computerguru]
답글에서 한 사용자는 비용이 이미 높고 3.8 Flash가 3.7 Flash보다 40% 비쌌는데 이번에 다시 두 배가 되므로 다른 모델로 옮길 것이라고 했다.[^pqdbr]
다른 답글은 Artificial Analysis 기준으로 작업당 비용은 3.8 Flash보다 오히려 낮다고 반박하면서, 출력 토큰이 더 많은데 어떻게 그런지는 이해하지 못한다고 했다.[^wasabi]
실제 부하를 측정한 사용자의 보고도 엇갈린다.
한 사용자는 자신의 평가에서 작업당 비용이 37% 올랐지만 시간은 40~60%로 줄었고 속도가 문제였기에 좋은 업그레이드라고 평가했다.[^dataottawa]
단가가 아니라 작업당 비용과 시간으로 비교해야 하고, 결과는 업무마다 다르다.

다른 댓글은 입력 1.5달러와 출력 7.5달러가 비싸다는 단순한 불만이고,[^epolanski]
Argon이 2달러이고 Carbon이 현재 2달러인 가격 구조가 모델을 고르지 않는 제품에서만 말이 된다고 지적한다.[^whinvik]
이 지적은 계층 사이의 가격 차가 작아 Hydrogen을 따로 두는 이유가 약해 보인다는 것이다.

### 이름이 계층을 알려 주지 못한다

이름은 반응이 가장 많은 주제 중 하나이다.
한 댓글은 복잡도와 비용 순서가 Hydrogen, Argon, Carbon인데 알파벳 순도 원자량 순도 아니라고 불평한다.[^jawns]
답글은 Business Insider가 전한 내부 문서에서 Argon, Barium, Carbon이 알파벳 순으로 시험되었고,
가벼운 모델이 필요해지자 가장 가벼운 원소 수소를 덧붙인 것 같다고 설명한다.[^amanda]
다른 답글도 같은 경위를 설명한다.[^aoeusnth]
이 설명은 이름이 계층 관계를 알려 주지 않는다는 비판을 반박하는 것이 아니라 확인한다.
사용자는 이름만으로 어느 것이 작고 큰지 모른다는 불만이 이어진다.[^schopra]
GeekNews에서도 같은 불만이 나왔다.
한 사용자는 모델 이름의 직관성이 OpenAI가 가장 낫고 Claude가 그 다음이며
Gemini는 알기 어렵다고 적었다.[^unsafe]
다른 사용자는 성능이 알파벳 순서도 원자번호 순서도 맞지 않아 불규칙 동사처럼 외워야 하고,
가장 좋거나 가장 많이 쓰는 프런티어 모델도 아닌데 이렇게 이름을 붙이면 누가 외우겠느냐고 했다.[^laeyoung]
이름이 의미 없는 것이 되면 선택은 문서를 찾아봐야 하는 일이 된다.

### 이 발표는 사용 한도와 접근성의 문제를 가린다

한 댓글은 Pro 구독에서 Argon이 아직 매우 제한적이고 Carbon은 Ultra에서만 쓸 수 있으며 Antigravity에 묶여 있어 경쟁력이 없다고 평했다.[^jeremy]
다른 댓글은 Pro 계정이 학생과 통신사 요금제에 준 접근을 받지 못하고, 연산 자원이 모자라 소통이 나쁘며 같은 모델이 몰래 약해졌다고 주장한다.[^childofchaos]
이 주장들은 증거가 제시되지 않은 개인 불만이다.
그러나 같은 스레드에서 Antigravity 명령줄 도구를 쓰다 계정 서비스가 정지되었다는 보고가 나왔고,
다른 사용자들이 비슷한 일을 겪었다고 확인했다.[^tobias][^davidd]
발표 글은 사용 한도와 정책 집행을 다루지 않는다.
모델의 성능과 사용자가 실제로 쓸 수 있는 양은 별개의 문제이다.

### 모든 수치가 자사 평가이다

발표의 안전과 정직성 수치는 내부 평가이다.
외부 검증이 없고 평가의 정의가 글에 없다.
벤치마크 이름도 일부는 새것이어서 독자가 재현할 방법이 없다.
Multimodal Knowledge Agent와 Agents' Last Exam v1.1에서 앞선다는 문장은 Google이 고른 평가에서의 결과이다.
이 문서가 확인할 수 있는 것은 발표가 무엇을 주장하는지까지이다.

## 인사이트

### 중간 등급 모델의 가치는 필요한 곳을 좁히는 데 있다

HN의 한 댓글은 자신이 최상위 모델이나 가장 싸고 빠른 모델만 쓰고 중간 등급은 쓸 곳이 없다고 했다.[^jv00]
답글들은 갈렸다.
중간 모델로 아끼려다 오류가 늘어 시간과 토큰을 더 쓴다는 의견과,[^xcsme]
일상 작업은 중간 모델로 충분하다는 의견이 있다.[^viraptor]
비코딩 생산 파이프라인에서는 벤치마크 지수가 낮은 모델이 더 나은 경우가 많다는 경험담도 나왔다.[^deaux]
이는 평가 지표가 측정하기 쉬운 것에 치우친다는 오래된 문제이다.
Hydrogen이 누구에게 맞는지는 지수가 아니라 자신의 작업에서 오류당 비용을 재서 정해야 한다.

### 모델 라우팅이 제품 기능이 되면 비교 단위가 모델에서 시스템으로 옮겨 간다

Orchestrator는 사용자가 모델을 고르지 않게 한다.
이 경우 비교할 대상은 모델 하나의 점수가 아니라 라우팅 정책과 쿼터 정책을 포함한 시스템이다.
Google이 Terminal-Bench 4.0에서 보인 24% 쿼터 절감과 19% 속도 향상은 Carbon 단독과의 비교이다.
같은 방식으로 Claude나 다른 모델 조합과 비교한 결과는 발표에 없다.
사용자가 확인해야 할 것은 라우팅이 자기 작업에서 실제로 쿼터를 줄이는지와,
어느 모델이 어느 단계를 맡았는지 볼 수 있는지이다.

### 확인할 관찰

이 발표의 주장이 옳다면 다음이 따라와야 한다.
독립 평가에서 Hydrogen이 Argon과 같은 수준으로 재현되고,
실제 작업당 비용이 3.8 Flash보다 같거나 낮고,
Pro 구독자의 사용 한도가 실사용에 충분해야 한다.
반대로 독립 평가가 지수 차이를 재현하지 못하거나 작업당 비용이 올라가면 가격 우려가 현실이 된다.
이 판단에는 모델 카드와 독립 평가 기관의 후속 측정이 필요하다.

---

[^behat]: <https://news.ycombinator.com/item?id=50471706>

[^jacob]: <https://news.ycombinator.com/item?id=50471613>

[^netrem]: <https://news.ycombinator.com/item?id=50471932>

[^qnleigh]: <https://news.ycombinator.com/item?id=50474627>

[^modeless]: <https://news.ycombinator.com/item?id=50471665>

[^ngomez]: <https://news.ycombinator.com/item?id=50472922>

[^computerguru]: <https://news.ycombinator.com/item?id=50471754>

[^pqdbr]: <https://news.ycombinator.com/item?id=50471846>

[^wasabi]: <https://news.ycombinator.com/item?id=50473627>

[^dataottawa]: <https://news.ycombinator.com/item?id=50473718>

[^epolanski]: <https://news.ycombinator.com/item?id=50479861>

[^whinvik]: <https://news.ycombinator.com/item?id=50471817>

[^jawns]: <https://news.ycombinator.com/item?id=50471630>

[^amanda]: <https://news.ycombinator.com/item?id=50471879>

[^aoeusnth]: <https://news.ycombinator.com/item?id=50473420>

[^schopra]: <https://news.ycombinator.com/item?id=50472854>

[^jeremy]: <https://news.ycombinator.com/item?id=50471936>

[^childofchaos]: <https://news.ycombinator.com/item?id=50474984>

[^tobias]: <https://news.ycombinator.com/item?id=50474230>

[^davidd]: <https://news.ycombinator.com/item?id=50478983>

[^jv00]: <https://news.ycombinator.com/item?id=50471826>

[^xcsme]: <https://news.ycombinator.com/item?id=50471973>

[^viraptor]: <https://news.ycombinator.com/item?id=50472412>

[^deaux]: <https://news.ycombinator.com/item?id=50472511>

[^unsafe]: <https://news.hada.io/topic?id=37068#cid69773>

[^laeyoung]: <https://news.hada.io/topic?id=37068#cid69788>
