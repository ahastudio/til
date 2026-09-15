# 사고에 가장 큰 영향을 준 블로그 글은 무엇인가

원문: [What blog posts influenced your thinking the most? | Lobsters](https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking)

## 소개

Lobste.rs에 올라온 질문 스레드다.
자기 사고에 가장 큰 영향을 준 블로그 글이 무엇이냐는 물음에
47점과 33개의 댓글이 모였다.
질문자는 자신에게는 Parse, Don't Validate와
초기 Joel on Software 글이라고 밝히며 시작한다.

답변으로 모인 글들은 프로그래밍 사고의 고전 목록을 이룬다.
Sandi Metz의 The Wrong Abstraction,
곧 잘못된 추상이 추상 없음보다 위험하다는 글,[^nick4]
Ben Kuhn의 You Don't Need to Work on Hard Problems,[^Relax]
Sean Goedecke의 how-to-ship,[^ahelwer]
Caleb Hearth의 Don't Get Distracted,[^landon]
grugbrain.dev,[^ThePaulMcBride]
Tony Hoare의 튜링상 수상 연설 The Emperor's New Clothes,[^sayyadirfanali]
Joel Spolsky의 The Law of Leaky Abstractions,[^simonw]
aphyr의 Typing the Technical Interview가 거론됐다.[^cole-k]

Parse, Don't Validate는 제목만으로도 기억에 남는다는 평이 여럿이었고,[^voutilad]
여러 참가자가 자기 읽기 목록 페이지를 공유했다.
koala는 잃어버리는 글이 많아 3년 전부터 목록을 관리한다고 했고,[^koala]
matklad는 뜻밖의 선물이라며 앞으로 읽을 목록을 얻었다고 했다.[^matklad]
marginalia는 글을 읽기보다 쓰면서 더 영향받으며
그것이 자기 사고 과정 전체라고 답했다.[^marginalia]

## 분석

### 이 스레드의 가치는 개별 글이 아니라 합의된 정전(canon)에 있다

이 질문이 흥미로운 이유는 개인의 추천이 모여
프로그래밍 사고의 비공식 정전을 드러내기 때문이다.
Parse, Don't Validate, The Wrong Abstraction, The Law of Leaky Abstractions는
서로 다른 사람이 독립적으로 꼽았다.
같은 글이 반복 등장한다는 것은
그것이 개인 취향을 넘어 공동체의 공유 어휘가 되었음을 뜻한다.

이 정전이 중요한 이유는 분야의 암묵적 합의를 가시화하기 때문이다.
소프트웨어 공학에는 공식 교과서만큼이나
이런 블로그 글들이 사고의 토대를 이룬다.
Parse, Don't Validate는 타입으로 불변식을 강제하라는,
The Wrong Abstraction은 성급한 추상을 경계하라는 원칙을 각인시켰다.
이 글들이 반복 인용된다는 것은
공동체가 그 원칙을 공통 전제로 받아들였다는 증거다.

주목할 만한 것은 이 정전이 대부분 원칙에 관한 글이라는 점이다.
특정 기술의 사용법이 아니라
추상, 검증, 단순성, 집중 같은 사고 방식에 관한 글이 살아남았다.
기술은 낡지만 사고 방식은 오래간다.
grugbrain.dev가 단순함을,
Don't Get Distracted가 집중을,
You Don't Need to Work on Hard Problems가 문제 선택을 다루듯,
정전에 오른 글들은 코드가 아니라 판단을 가르친다.

### 읽기와 쓰기의 관계에 대한 두 관점이 드러난다

marginalia의 답변, 곧 글을 읽기보다 쓰면서 더 영향받는다는 말은
이 스레드의 전제를 살짝 비튼다.
질문은 어떤 글이 당신에게 영향을 줬느냐를 묻지만,
marginalia는 영향의 원천이 소비가 아니라 생산이라고 답한다.
쓰는 행위가 곧 사고 과정이라는 것이다.

이 관점이 중요한 이유는 사고의 형성 방식에 대한 두 모델을 대비시키기 때문이다.
하나는 좋은 글을 읽어 사고가 형성된다는 소비 모델이고,
다른 하나는 직접 써 보며 사고가 벼려진다는 생산 모델이다.
스레드의 대다수는 소비 모델로 답하지만,
marginalia와 aphyr를 언급한 cole-k는 생산 쪽을 가리킨다.
aphyr의 Typing the Technical Interview가
프로그래밍에 관한 글쓰기가 얼마나 재미있을 수 있는지를 보여 줘
글을 쓰고 싶게 만든 영감이었다는 것이다.

두 모델은 배타적이지 않고 순환한다.
좋은 글을 읽으면 쓰고 싶어지고,
쓰면서 읽은 것을 자기 것으로 만든다.
koala와 matklad가 읽기 목록을 관리하고 공유하는 것은
소비와 생산 사이의 이 순환을 제도화한 행위다.
읽은 것을 목록으로 남기고 남과 나누는 것 자체가
수동적 소비를 능동적 정리로 바꾼다.

## 비평

### 정전의 반복은 반향실 효과일 수도 있다

같은 글이 반복 추천되는 것을 공동체의 지혜로만 읽을 수는 없다.
Lobste.rs라는 특정 커뮤니티,
곧 함수형·타입 중심 사고에 우호적인 집단이 모인 곳에서는
Parse, Don't Validate 같은 글이 과대 대표될 수 있다.
같은 취향의 사람들이 같은 글을 꼽는 것은
지혜의 수렴이 아니라 반향실일 수 있다.

이 편향이 중요한 이유는 정전이 배제하는 것을 가리기 때문이다.
이 목록에는 특정 관점의 글이 두드러지고,
반대 관점, 곧 동적 타입의 유연함이나
빠른 반복의 가치를 옹호하는 글은 드물다.
ahelwer가 Sean Goedecke를 추천하며
그가 여기서 미움받는다고 단서를 단 것은,[^ahelwer]
이 공동체에 이미 선호와 배척의 기류가 있음을 드러낸다.
정전은 무엇이 좋은지를 보여 주는 만큼
그 공동체가 무엇을 밀어내는지도 보여 준다.

따라서 이런 목록을 절대적 필독서로 받아들이면 위험하다.
그것은 특정 시대, 특정 공동체의 취향을 반영한 스냅숏이다.
Joel on Software가 초기 웹 시대의 감수성을 담듯,
지금의 정전은 지금 이 커뮤니티의 감수성을 담는다.
목록의 가치는 정답이어서가 아니라
어떤 집단이 무엇을 중요하게 여기는지의 창이라는 데 있다.

### 제목이 좋아서 기억되는 것과 내용이 깊어서 기억되는 것은 다르다

voutilad가 Parse, Don't Validate를 이름으로 기억할 수 있는 유일한 글이라며
제목이 완벽해서 기억에 새겨진 것 같다고 한 것은[^voutilad]
정전 형성의 숨은 메커니즘을 드러낸다.
어떤 글이 반복 인용되는 데는
내용의 깊이만큼이나 제목의 기억성이 작용한다.

이 구별이 중요한 이유는 영향력과 밈성을 혼동하게 하기 때문이다.
Parse, Don't Validate, The Wrong Abstraction, grugbrain은
모두 짧고 강렬한 제목을 가졌다.
이런 제목은 대화에서 쉽게 소환되고,
소환될수록 더 자주 추천되어 정전에 굳어진다.
그러나 소환하기 쉬운 것과 사고를 가장 깊이 바꾼 것이 같지는 않다.
제목이 밋밋하지만 깊은 글은
이런 스레드에서 이름이 떠오르지 않아 과소 대표된다.

이것은 앞선 aligned-to-whom에서 본,
짧고 강한 프레이밍이 반박에 취약하되 인상은 강한 것과 같은 현상이다.
기억에 남는 형식이 영향력의 대리 지표가 되면,
잘 포장된 아이디어가 잘 논증된 아이디어를 이긴다.
이 스레드의 목록도 부분적으로는
가장 영향력 있는 글이 아니라
가장 회자하기 좋은 글의 목록일 수 있다.

## 인사이트

### 블로그 글이 소프트웨어 공학의 실질적 교과서 역할을 한다

이 스레드가 드러내는 가장 이전 가능한 통찰은
소프트웨어 공학의 사고가 교과서가 아니라
블로그 글로 전수된다는 점이다.
Parse, Don't Validate나 The Wrong Abstraction은
학술 논문도 교과서도 아니지만,
현장 개발자의 사고를 논문보다 더 깊이 형성한다.

이 현상이 중요한 이유는 지식 전수의 매체가 이동했음을 보여 주기 때문이다.
소프트웨어는 빠르게 변해 교과서가 따라잡지 못한다.
반면 블로그 글은 즉각적이고, 현장 경험에서 나오며,
공동체가 인용과 추천으로 검증한다.
이 검증은 동료 심사와 다르지만 나름의 엄정함을 갖는다.
수년에 걸쳐 반복 인용되는 글만이 정전에 남기 때문이다.

두 번째 차수의 효과는 이것이 좋은 글쓰기의 가치를 높인다는 점이다.
자기 통찰을 기억에 남는 형식으로 쓸 수 있는 개발자는
그 통찰을 공동체의 어휘로 만든다.
gitbybit의 창작자나 Refactoring.Guru가 그랬듯,
한 사람의 명료한 글이 수많은 개발자의 사고를 바꾼다.
코드를 잘 짜는 것만큼이나
사고를 잘 전달하는 글쓰기가 영향력의 통화가 되었다.

### 잃어버리지 않으려 목록을 관리하는 행위가 큐레이션의 부상을 보여 준다

koala가 3년 전부터 목록을 관리하고 matklad가 링크 페이지를 유지하는 것,
그리고 이 스레드 자체가
개인의 큐레이션이 집단의 자산이 되는 흐름을 보여 준다.
좋은 글이 넘쳐 나는 시대에는
그것을 찾는 것보다 잃지 않고 정리하는 것이 어렵다.

이 통찰이 새로운 프레임을 주는 이유는
정보 과잉 시대의 진짜 희소재를 드러내기 때문이다.
글은 무한히 많지만,
무엇이 오래 가치 있는지를 가려내는 판단은 희소하다.
koala가 잃어버리는 것이 싫어 목록을 시작했다는 것은,
개인이 자기만의 정전을 능동적으로 구축하는 행위다.
그리고 그 개인 목록들이 이 스레드처럼 모이면
집단의 정전이 된다.

세 번째 차수의 효과는 이것이 AI 시대에 더 중요해진다는 점이다.
LLM이 모든 글을 요약해 줄 수 있는 시대에도,
무엇을 읽을 가치가 있는지의 판단은 여전히 사람의 몫이다.
fde-organizational-capability에서 본,
지식 접근이 평등해질수록 판단이 희소해진다는 통찰이 여기서도 반복된다.
어떤 글이 사고를 바꿀 만한지를 아는 것,
그것을 잃지 않게 정리하는 것,
그리고 남과 나누는 것은
정보가 흔할수록 오히려 값진 능력이 된다.
이 스레드의 진짜 산출물은 목록이 아니라,
그 목록을 만드는 큐레이션이라는 행위의 가치에 대한 확인이다.

---

[^koala]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_kdrw5b>

[^nick4]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_bks1x0>

[^voutilad]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_fssgte>

[^Relax]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_kuj3tq>

[^ahelwer]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_hwtfzy>

[^landon]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_vsyty2>

[^cole-k]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_it7mgq>

[^ThePaulMcBride]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_989euw>

[^sayyadirfanali]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_zbfbez>

[^marginalia]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_8z8oop>

[^simonw]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_4fxnwn>

[^matklad]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_zvwh0o>
