# Tao의 AI 수학 결과 세 건 소개

원문: [Unforced Euler singularity, unforced Navier-Stokes singularity, and the Generalized Riemann Hypothesis](https://terrytao.wordpress.com/2026/11/20/unforced-euler-singularity-unforced-navier-stokes-singularity-and-the-generalized-riemann-hypothesis/)

HN 토론: <https://news.ycombinator.com/item?id=50578358> (487점, 210개 댓글)

GN 토론: <https://news.hada.io/topic?id=37546>

## 요약

Terence Tao가 2026년 11월 20일 자기 블로그에 올린 짧은 글이다.
글은 곧 여러 매체가 보도할 결과들이라며,
결과가 얼마나 소화(digested)되었는지를 기준으로 내림차순으로 세 가지를 적는다.

1. Levent Alpöge, Tristan Buckmaster, Matei Coiculescu가
   AI의 큰 도움으로 3차원 비압축성 Euler 방정식(외력 없음)의
   유한 시간 폭발(finite time blowup)에 대한 사람이 읽을 수 있는 증명을 썼고,
   Lean으로 형식화되어 있다.
2. Alpöge와 Buckmaster가 역시 AI를 많이 써서
   3차원 비압축성 Navier-Stokes 방정식(외력 없음)의 유한 시간 폭발 증명을 만들었고
   Lean 형식화가 딸려 있다.
   논문은 기술적으로 사람이 읽을 수 있고 증명 전략도 대체로 분명하다.
   전략은 이산 자기유사(discretely self-similar) 근사 해를 수치로 만든 다음
   엄밀한 섭동 이론으로 정확한 해로 바꾸는 것이고,
   이 결과에 대한 기대 경로 가운데 하나라고 한다.
   다만 제대로 전문적으로 쓴 증명을 만들려면 더 많은 작업이 필요하다고 한다.
3. Alpöge가 내부 AI 모델로 일반화 리만 가설(Generalized Riemann Hypothesis, GRH)의
   방대한 Lean 전용 증명을 생성했다.
   글은 이 증명을 검증하고 전략을 추출하는 노력을 따라가기에는
   Lean Zulip 스레드가 가장 좋다고 소개한다.
   아주 초기 분석으로는 Langlands 프로그램과 산술기하학의 현대적 성과를
   최대한 활용하는 것으로 보인다고 적는다.
   이후 Zulip 중재자들이 토론을 Lean 관련 사항으로 한정하고 있다는 추가 글이 있다.
   소화에 시간이 걸리겠지만 이 경우에는 소통할 수 있는 사람 저자가 있다고 덧붙인다.

끝에는 앞의 두 결과에 대한 Buckmaster의 Mastodon 글을 참고하라는 링크가 있다.

## 분석

### 글의 구조가 곧 주장이다

글은 결과의 의미나 중요성을 말하지 않고 소화 정도의 순서만 정한다.
첫째 결과는 읽을 수 있는 증명과 Lean이 모두 있고,
둘째는 읽을 수 있지만 전문적 정리가 더 필요하며,
셋째는 Lean만 있다.
이 순서는 검증 경로의 차이를 그대로 보여 준다.
셋째 결과를 두고 사람이 읽는 길이 아직 없다는 점을 먼저 짚는 것이다.

HN에서 maplet은 Tao가 틀릴 수 있는 결과를 홍보하고 싶지 않은 것은 이해하지만
리만 가설 관련 결과를 올리면서 그 의미를 언급하지 않는 글은 상상하기 어렵다고 썼다.[^maplet]
글이 의미 부여를 피한 것은 이 순서 매기기와 같은 선택으로 읽힌다.

### Lean 증명이 맞는 명제를 증명하는지의 문제

swingboy는 1,500만 줄에 가까운 Lean 코드에서 빌드가 통과했을 때
정말 의도한 것을 검증하는지, 1+1=2 같은 것이 통과시키지는 않았는지 물었다.[^swingboy]
raincole은 Lean이 검사하는 것은 타입이고 비즈니스 로직이 아니라고 답했고,[^raincole]
black_knight는 타입 이론에서는 명제를 타입으로 표현하므로 타입 검사기가 논리를 검증한다고 이었다.[^black_knight]
kaashif는 이 비유의 핵심이 프로그램이 컴파일되어도 명세를 구현했다는 보장이 없는 것처럼
수학 형식화에서도 다른 명제를 증명했을 수 있다는 점이라고 정리했다.[^kaashif]
chunky1994는 Lean Zulip에서 독립된 두 커널이 결과를 받아들였다고 전했고
이는 커널 버그를 이용한 증명일 가능성이 낮다는 뜻이라고 썼다.[^chunky1994]
커널이 받아들이는 것과 명제가 표준 GRH와 같은 것은 별개의 문제이다.

## 비평

### 글은 세 결과의 근거를 제시하지 않는다

이 글은 발표문이 아니라 소개글이다.
각 결과의 주장은 링크된 논문과 Lean 코드, 저자들의 글에 있고,
글 안에는 증명의 내용이 거의 없다.
GRH에 대해서는 Zulip 스레드의 초기 분석에서 보이는 인상이라는 단서가 붙어 있다.

### 새 추상화는 누가 만드는가

softwaredoug는 지금의 진전이 기존 추상화와 개념 위에서 언어를 대량으로 생성하고
증명을 검증하는 힘에 기대고 있다고 보고,
Langlands 프로그램 같은 새 추상화는 어떻게 만들어지는지,
공동체의 합의가 필요한지, 그 사회적 과정이 없으면 수학이 정체할지 물었다.[^softwaredoug]
QuesnayJr는 수학이 정체할 수 있다는 가능성은 많이 나오지만 진실은 아무도 모르며,
Langlands는 가장 추측적인 영역인데 특수한 경우만 증명해도
Fermat의 마지막 정리가 나올 만큼 강력했다고 답했다.[^QuesnayJr]
chunky1994는 이론물리와 실험물리의 상호작용에 빗대어
AI가 더 포괄적인 이론을 만들 수 있으리라 보았지만 수학이라는 학문에
어떻게 들어맞을지는 실시간으로 알아 가는 중이라고 썼다.[^chunky1994-theory]
이 질문은 글이 던지지 않았지만 글이 다룬 결과들이 던지게 만든 것이다.

### 검증이 쉬운 분야라는 한계

sega_sai는 AI가 사실상 인간 지능을 넘어섰다고 느끼며 무섭다고 썼다.[^sega_sai]
nomadpenguin은 수학 결과에서 즉시 검증 가능한 보상으로 하는 강화학습이 얼마나 중요한지가
덜 논의되며 즉시 검증이 안 되는 분야에서 같은 성과가 나올지 확신하지 못한다고 답했다.[^nomadpenguin]
justanotherjoe는 수학이 추상 공간에서만 사는 학문이어서 AI에 특별히 유리하다고 보았다.[^justanotherjoe]
Lean이 있는 분야의 성과를 모든 분야의 능력으로 일반화할 수 있는지는
이 글과 댓글만으로는 알 수 없다.

## 인사이트

### 소화 순서가 곧 신뢰의 순서이다

세 결과를 같은 날 받았을 때 독자가 할 일은
결과의 크기를 비교하는 것이 아니라 각각의 검증 경로가 어디까지 열렸는지 보는 것이다.
읽을 수 있는 증명과 Lean이 모두 있으면 전문가가 며칠 안에 판단할 수 있고,
Lean만 있으면 명제의 정확성과 전략의 이해가 서로 다른 시간표로 풀린다.
Tao가 순서를 매긴 방식은 그 구분을 요구하는 것이다.

같은 날 GRH에 대한 다른 주장도 공개되었다.
Masullo가 사람이 쓴 증명안 초안을 올렸고,
이 글은 그 주장을 언급하지 않는다.

### 확인할 관찰

이 결과들의 평가를 가를 관찰은 다음과 같다.

1. Euler와 Navier-Stokes 결과에 대해 독립된 전문가가 읽을 수 있는 증명을
   검토한 뒤 어떤 결론에 이르는지.
2. Lean의 GRH 명제가 표준 정의의 GRH와 같다는 것을
   독립된 사람이 확인하는지.
3. GRH 증명에서 사람이 읽을 수 있는 전략이 추출되는지,
   추출되면 Tao의 초기 인상(Langlands와 산술기하학)과 맞는지.
4. Navier-Stokes 결과의 전문적인 정리본이 나오는지.

---

[^maplet]: <https://news.ycombinator.com/item?id=50579814>

[^swingboy]: <https://news.ycombinator.com/item?id=50583510>

[^raincole]: <https://news.ycombinator.com/item?id=50586443>

[^black_knight]: <https://news.ycombinator.com/item?id=50587469>

[^kaashif]: <https://news.ycombinator.com/item?id=50589401>

[^chunky1994]: <https://news.ycombinator.com/item?id=50581818>

[^softwaredoug]: <https://news.ycombinator.com/item?id=50580358>

[^QuesnayJr]: <https://news.ycombinator.com/item?id=50580662>

[^chunky1994-theory]: <https://news.ycombinator.com/item?id=50580744>

[^sega_sai]: <https://news.ycombinator.com/item?id=50583654>

[^nomadpenguin]: <https://news.ycombinator.com/item?id=50585482>

[^justanotherjoe]: <https://news.ycombinator.com/item?id=50588022>
