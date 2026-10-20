# 이해하지 못하는 AI 코드를 출시하는 불편함에 대한 답은 설계를 사람이 쥐는 것과 이해를 검증으로 바꾸는 것으로 갈린다

원문: [Ask HN: How to deal with shipping AI-written code you don't understand?](https://news.ycombinator.com/item?id=50151036)

GN 토론: <https://news.hada.io/topic?id=35662>

## 요약

2026년 10월 19일 Hacker News에 rzk가 올린 이 질문은
Meta 엔지니어의 LinkedIn 글에 공감했다는 말로 시작한다.
질문이 인용한 글의 요지는 이렇다.
AI로 출시하는 새 표준이 너무 빨라서 모든 줄을 확인하려면 영원히 걸리고,
그래서 자기가 만든 시스템인데
모든 코드가 어떻게 동작하는지 진정으로 이해하지 못하게 된다.
높은 수준은 이해하지만 모든 세부는 아니다.
이것이 새 표준이 되고 있을지도 모르고
이는 소프트웨어 엔지니어의 모든 본능에 반한다.
무엇을 만드는지 이해하던 사람이 이제는 얼마나 이해해야 안심하고
나아갈 수 있는지를 알아내려 한다는 것이다.
질문은 다른 엔지니어들도 이렇게 느끼는지, 어떻게 대처하는지를 묻는다.

이 스레드에서 답은 크게 일곱 갈래로 나뉜다.
설계는 사람이 하고 구현만 맡기는 방식, 테스트와 검증을 늘리는 방식,
역할이 프로젝트 관리자나 수석 엔지니어로 바뀐 것이라는 해석,
이해하지 못한 코드는 출시하지 않는다는 거부,
코드의 위험도에 따라 이해의 깊이를 달리하는 방식,
형식 검증으로 이해를 대체하자는 제안,
그리고 이전의 추상화 도약과 같은 일이라는 역사적 해석이다.

## 분석

### 같은 불편함에 대한 답은 이해의 단위를 어디에 두느냐로 갈린다

스레드의 답을 이해의 단위로 정리하면 다섯 가지 위치가 보인다.
설계 수준을 이해하겠다는 쪽은 각 단위의 책임과 상호작용만 알면 된다고 보고,
시스템 수준에서 이해하겠다는 쪽은 테스트가 통과하면 된다고 본다.
역할을 바꾸자는 쪽은 이해가 개발자의 일이 아니라고 보고,
거부하는 쪽은 이해가 개발자의 의무라고 본다.
형식 검증을 말하는 쪽은 이해를 증명으로 대체하자고 한다.

이 다섯 갈래는 서로 반박하기보다 서로 다른 전제에서 출발한다.
이해를 어디에 두느냐는 책임을 어디에 두느냐와 같은 질문이기 때문이다.

### 설계를 사람이 쥐는 방식이 가장 많이 지지받는다

가장 많은 하위 댓글을 받은 bitwizeshift는 LLM이 코드를 설계하게 하지 않고
자신이 만든 설계를 구현하게 한다고 했다.
추상화와 행위자의 계층 전체를 UML 수준에서 직접 정하고
LLM에게 빈틈을 구현하게 하므로,
각 단위가 어떻게 구현되었는지는 몰라도 단위의 책임과 상호작용은 안다는 것이다.
그는 LLM이 좋은 추상화를 쓰는 데는 끔찍하다고
했다.[^bitwizeshift] fasterik는 이것이 기본적인 소프트웨어 설계 원칙인데
말해야 한다는 것이 놀랍다며 그렇지 않은 사람은 주로 주니어일 것이라고
했다.[^fasterik] threethirtytwo는 LLM이 사람보다 뛰어난 설계를 내놓을 때가
많아서 내가 설계한 코드로 제한하면
AI 능력의 큰 부분을 잘라 내는 것이라고 반박했다.[^threethirtytwo]

이 교환의 쟁점은 LLM이 설계에도 쓸 만한가다. bitwizeshift는 추상화는 사람의
몫이라는 경험칙을, threethirtytwo는 변화 속도가 빠르니
그 경험칙이 곧 낡는다는 판단을 내놓는다.
스레드에서는 어느 쪽도 증거를 내놓지 않는다.

### 수석 엔지니어의 일과 닮았다는 유비가 가장 많이 반복된다

jedberg는 오래 수석 엔지니어(PE)였기 때문에
이것이 자신의 일하는 방식과 같다고 했다.
PE는 설계하고 주니어가 세부를 구현하거나, 이미 주니어가 설계하고
지은 프로젝트에 떨어져 가능한 한 많은 세부를 빠르게 이해해야 하며,
AI로 모두가 PE처럼 행동하게 되었다는 것이다.
세부를 전부 이해하지 못해도 주요 아이디어와 세부를 물을 곳을 알면 된다고
했다.[^jedberg] solatic도 PE는 여러 엔지니어의 일을 감독하지만
모든 코드를 직접 검토할 수 없고 사람의 코드 리뷰가 버그의 수와 심각도를 줄이지만
없애지는 않는다는 점을 이해한다고 했다.[^solatic]
SftwareRenderer는 주니어에게 세부를 물을 곳을 아는 기술을 기르기
위해 개인 프로젝트를 손으로 만들어 보라고 권했다.[^SftwareRenderer]

반면 akomtu는 이 유비가 성립하려면
시스템의 일부를 아는 엔지니어가 있거나 사람이 사람을 위해 만든
이해 가능한 시스템이어야 하는데 AI가 이 가정을 깬다고 했다.
지금은 아무도 어떻게 동작하는지 이해하지 못하고
이해할 수도 없다는 것이다.[^akomtu]
Silhouette는 solatic의 지금까지는 잘 되고
있다는 말에 객관적 증거가 놀랄 만큼 적다며, 코드는 많이 쓰이지만
실제 가치를 더하는 양은 별개의 질문이라고 했다.[^Silhouette]

## 비평

### 테스트로 이해를 대신하자는 답에는 같은 AI가 둘을 쓴다는 구멍이 있다

ChrisMarshallNY는 아주 많이 테스트한다고 했다.
LLM으로 코딩에 쓰는 시간이 줄어 테스트에 쓰는 시간이 늘었고
코딩 오류는 못 찾지만 구현 오류는 찾으며, 자신이 완벽하다고
믿던 성숙한 코드를 LLM에 돌렸더니 문제를 여럿 찾았다고
했다.[^ChrisMarshallNY] g-b-r는 코드를 검토하지 않으면 검증이 아니며
테스트 스위트가 모든 코드 경로를 시험해도 LLM이 추가했을지 모르는
의도치 않은 동작을 대부분 잡아내지 못한다고 반박했다.[^g-b-r]
SimianSci는 그렇다면 만드는 데는 시간과 돈을 아꼈지만
검증과 테스트의 새 일이 늘었을 뿐 설계 루프에서
시간과 노력이 쓰이는 곳만 바뀐 것 아니냐고 물었다.[^SimianSci]

edwin0는 AI가 코드와 테스트를 모두 쓸 때 둘이 서로 동의하면서
같은 것을 놓칠 수 있어 불안하다고
했고,[^edwin0] fractallyte는 두세 개의 다른 LLM을 쓰라고 했다.
Claude가 코딩하고 Codex가 적대적 리뷰를 하게 하면
허용할 만큼 올바른 버전으로 수렴할 때까지 오갈 수 있다는 것이다.[^fractallyte]
ch_sm은 AI 이전에도 코드의 작성자가 테스트를 썼고
그 테스트가 여전히 도움이 되었다고
했다.[^ch_sm] cadamsdotcom은 테스트 주도 개발로 에이전트가 테스트를 쓰고
그 테스트가 실패하는 것을 직접 확인한 뒤 통과시키는 일을 시작하면
큰 확신이 생긴다고
했고,[^cadamsdotcom] SimianSci는 슬롭 코드는 슬롭 테스트를 더해도 슬롭이며
코드를 생성하는 속도로 테스트를 생성하게 되는 지점에 이른다고
답했다.[^SimianSci-tests]

이 교환에서 확인되듯 테스트가 이해를 대신하려면 테스트의 독립성이 필요하다.
같은 모델이 같은 맥락에서 쓴 코드와 테스트는 같은 오해를 공유할 수 있고
모델을 바꾸는 것은 그 독립성을 부분적으로 얻는 방법이다.
스레드는 독립성이 얼마나 필요한지에 대한 측정은 내놓지 않는다.

### 위험도에 따라 이해의 깊이를 달리하는 답은 위험도를 판정하는 기준을 말하지 않는다

bob1029는 코드가 사용자의 눈에 가까울수록 특정한 것에 신경을 덜 쓴다고 했다.
HTML과 JS와 CSS는 사실상 전부 바이브 코딩이고
4,000줄짜리 `ui.js`를 재구성하려 하지 않으며
새 프롬프트로 몇 분 만에 다시 할 수 있지만
SQL 스키마는 여전히 전부 손으로 한다는 것이다.
스키마를 잘못하면
결과가 훨씬 치명적이기 때문이다.[^bob1029] w29UiIm2Xz는 어떤 사업에서는
고객이 눈에 보이는 것으로 가장 많이 판단한다고 반박했다.[^w29UiIm2Xz]

spacedcowboy는 자동 벡터화 컴파일러를 만드는데
AI에게 엄청난 수의 테스트를 쓰게 하고 실제의 비자명한 프로그램을 컴파일하게 하며
출시 전 5개 아키텍처에서 몇 시간 걸리는 관문을 돌린다고 했다.
오래 계획하고 코너 케이스와 테스트 케이스를 설계하는 데 공을 들이면
밤새 일하게 두기가 쉽다는 것이다.[^spacedcowboy] yulaow는 블라인드에서
읽은 바로는 Meta에서는 긴 계획 세션이나 구현 계획의 세부에 시간을 쓰지 않고
병렬로 관리해야 하는 PR이 많아서 그럴 수도 없다고
했다.[^yulaow] chrisjj는 작동하면
괜찮다는 말을 망치로 쳤을 때 콘크리트가 부서지지 않았다는 말과 같다며
공정의 품질이 필수라고 했다.[^chrisjj]

이 교환에서는 위험도에 따른 이해가 합리적이라는 데에 모두 동의하지만
위험도를 누가 어떻게 가르는지에는 답하지 않는다. bob1029의 스키마와 UI의 구분이
가장 구체적인 기준이지만 w29UiIm2Xz의 반박처럼 이 구분은 사업에 따라 달라진다.

### 책임을 누가 지는지 말할 때 유비가 깨진다

skeledrew는 이것이 기술적으로 역할의 변화이고 프로젝트 관리자 같은 것이 되었으며
관리자의 일은 코드를 이해하는 것이 아니라 해야 할 일을 하고
하지 말아야 할 일을 하지 않는지 보장하는 것이라고
했다.[^skeledrew] bsoles는 그러면 코드를 이해하는 것은 이제 누구의 역할이냐고
물었다.[^bsoles] 4ndrewl은 제품 관리자가 날마다 느끼는 감정이라고 했고
i_love_retros는 제품 관리자가 낸 것이 망가지면
코드를 제출한 소프트웨어 엔지니어가 비난받으며
엔지니어는 이제 Claude의 코드에도 책임져야 한다고
반박했다.[^4ndrewl][^i_love_retros] mikeocool는 제품 관리자는 올바른 제품을 내는
것에,
엔지니어링 팀은 성능과 장애와 보안 같은 자기 코드가 낳은 문제에 책임을 지는데
LLM에게는 무엇에도 책임을 묻기 어렵다고 했다.[^mikeocool]

이 교환을 보면 이해의 의무는 책임의 구조에 묶여 있다.
역할을 바꾸는 유비는 이해를 다른 사람에게 위임하는 구조를 가정하는데,
AI는 책임을 질 수 없으므로 위임의 끝이 결국 사람에게 돌아온다.

## 인사이트

### 형식 검증이 이해의 대체물이 되려면 명세를 쓰는 사람이 이해해야 한다

gavinray는 IDE의 다음 편집 예측 AI에서
Codex와 Claude CLI 중심으로 옮겨 가던 무렵부터
자신이 일하는 시스템을 설명하는 능력을 잃었다고 했다.
구현 세부에서 멀어질수록 의미가 흐려졌고
4~5년 동안 밑바닥부터 만든 시스템을 좋은 신념으로 이해한다고
말할 수 없게 되었다는 것이다.
해법은 구현 세부 검토로 돌아가는 것이 아니라 프로그램이 형식적으로 검증
가능하도록 코드와 언어를 바꾸는 것이라고
했다.[^gavinray] oblio는 gavinray가 말한 시점을 의심하며
2021년이나 2022년에는 LLM으로 프로그래밍하지 않았을 것이라고 반박했다.[^oblio]

이 문서의 읽기로는 형식 검증은 이해를 없애지 않는다.
이해의 위치를 코드에서 명세로 옮길 뿐이다.
증명이 명세를 만족함을 보여 줄 때 명세가 올바른지는 여전히 사람이 판단해야 한다.
이 읽기가 틀렸다면 명세를 AI가 쓰고
사람이 검증하는 데 필요한 이해가 훨씬 작다는 점이 보일 것이다.

### 이전의 추상화 도약과 이번을 가르는 것은 확정성이다

hahn-kev는 기계어를 손으로 쓰다가 컴파일러로 옮겨 간 일을 떠올리며,
당시 사람들도 컴파일러가 쓰는 기계어를 이해하지
못해 비슷하게 느꼈는지 물었다.[^hahn-kev]
Tadpole9181는 추상화가 한 단계 올라갈 때마다 받아들이는 마법의 수준에 불편해한
사람들이 있었고, 70~80년대에는 C도 너무 높은 수준이라는 전통주의자가 있었다고
답했다.[^Tadpole9181] netburst는 그것이 역사와 맞지 않는다며
고수준 언어는 복잡성 관리와 지루함 감소를 주었고
일반적인 불만은 컴파일러가 덜 효율적인 코드를 낸다는 것이었다고
반박했다.[^netburst] webarchitect는 MVC와 의존성 주입과 ORM이 자리 잡던 때도
코드가 너무 커서 일부만 다루게 되는 일이 있었다고
했고,[^webarchitect] combyn8tor는 사람들이 인터넷의 누군가가 쓴 수백,
수천 개 의존성을 기꺼이 가져오다가
이제야 자기가 출시하는 코드를 이해하지 못하는 것을 걱정한다고
꼬집었다.[^combyn8tor]

이 교환은 비교가 성립하는 부분과 아닌 부분을 가른다.
컴파일러는 같은 입력에 같은 출력을 내므로 이해를 한 번 믿으면
계속 믿을 수 있지만 LLM은 같은 요청에도 다른 코드를 내므로
믿음을 재사용할 수 없다.
이 문서의 읽기로는 이전의 도약과 이번의 차이는
추상화의 높이가 아니라 추상화가 결정적인가에 있다.
이 읽기가 틀렸다면
LLM의 출력이 충분히 안정되어 검증된 패턴처럼 쓰이는 사례가 늘어날 것이다.

### 이해하지 못한 코드를 출시하는 일은 작성자의 신뢰와 별개의 책임으로 남는다

HN의 internet2000은 Stack Overflow에서
복사해 붙인 코드를 이해하지 못한 채 출시한 적이 있으며 작동하면 된다고
했고,[^internet2000] platevoltage는 배우던 시절의 일이지 전문가가 하는 일이냐고
되물었다.[^platevoltage] ryandrake는 이 스레드에서 작동한다는 말을 검색해 보면
LLM 코딩 논의마다 같은 결과가 나오며,
그것은 창작물이 받아들여질 수 있는 가장 낮은 품질의 기준이라고
했다.[^ryandrake] tcdent는 전문가로서 일에 대한 의무는 그 직무에 자격이 있고
자신이 지지하는 일을 출시하는 것이므로 완전한 이해가 필요하지만
개인 부업과 도구에서는 마음껏 해도 된다고 구분했다.[^tcdent]

이 논의가 도달하는 구분은 책임이다.
개인 프로젝트에서는 이해하지 못한 코드의 책임이 자신에게만 돌아오고
직업에서는 다른 사람에게도 돌아온다.
이 저장소의 Sphinx 문서가 다룬 푸시 전 이해
확인도 이 책임의 구조를 도구로 옮긴 시도다.

---

[^bitwizeshift]: <https://news.ycombinator.com/item?id=50157475>

[^fasterik]: <https://news.ycombinator.com/item?id=50157790>

[^threethirtytwo]: <https://news.ycombinator.com/item?id=50159048>

[^jedberg]: <https://news.ycombinator.com/item?id=50158909>

[^solatic]: <https://news.ycombinator.com/item?id=50156513>

[^SftwareRenderer]: <https://news.ycombinator.com/item?id=50159502>

[^akomtu]: <https://news.ycombinator.com/item?id=50157068>

[^Silhouette]: <https://news.ycombinator.com/item?id=50157803>

[^ChrisMarshallNY]: <https://news.ycombinator.com/item?id=50156740>

[^g-b-r]: <https://news.ycombinator.com/item?id=50157437>

[^SimianSci]: <https://news.ycombinator.com/item?id=50156885>

[^edwin0]: <https://news.ycombinator.com/item?id=50151648>

[^fractallyte]: <https://news.ycombinator.com/item?id=50154810>

[^ch_sm]: <https://news.ycombinator.com/item?id=50153438>

[^cadamsdotcom]: <https://news.ycombinator.com/item?id=50157171>

[^SimianSci-tests]: <https://news.ycombinator.com/item?id=50157301>

[^bob1029]: <https://news.ycombinator.com/item?id=50158780>

[^w29UiIm2Xz]: <https://news.ycombinator.com/item?id=50159705>

[^spacedcowboy]: <https://news.ycombinator.com/item?id=50151160>

[^yulaow]: <https://news.ycombinator.com/item?id=50151337>

[^chrisjj]: <https://news.ycombinator.com/item?id=50156437>

[^skeledrew]: <https://news.ycombinator.com/item?id=50157164>

[^bsoles]: <https://news.ycombinator.com/item?id=50157273>

[^4ndrewl]: <https://news.ycombinator.com/item?id=50156430>

[^i_love_retros]: <https://news.ycombinator.com/item?id=50156773>

[^mikeocool]: <https://news.ycombinator.com/item?id=50156507>

[^gavinray]: <https://news.ycombinator.com/item?id=50156532>

[^oblio]: <https://news.ycombinator.com/item?id=50156697>

[^hahn-kev]: <https://news.ycombinator.com/item?id=50157745>

[^Tadpole9181]: <https://news.ycombinator.com/item?id=50158054>

[^netburst]: <https://news.ycombinator.com/item?id=50158216>

[^webarchitect]: <https://news.ycombinator.com/item?id=50154869>

[^combyn8tor]: <https://news.ycombinator.com/item?id=50157468>

[^internet2000]: <https://news.ycombinator.com/item?id=50156651>

[^platevoltage]: <https://news.ycombinator.com/item?id=50157703>

[^ryandrake]: <https://news.ycombinator.com/item?id=50158056>

[^tcdent]: <https://news.ycombinator.com/item?id=50156804>
