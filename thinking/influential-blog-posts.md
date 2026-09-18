# 사고에 가장 큰 영향을 준 블로그 글은 무엇인가

원문: [What blog posts influenced your thinking the most? | Lobsters](https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking)

GN 토론: <https://news.hada.io/topic?id=33714>

## 소개

Lobste.rs 사용자 mt가 올린 질문 스레드다.
자기 사고에 가장 큰 영향을 준 블로그 글이 무엇이냐는 물음이며, 이런 질문에서 늘 많이 배운다는 말로 시작한다.
질문자는 자신에게는 Parse, Don't Validate와 초기 Joel on Software 글이라고 밝힌다.
스레드는 105점에 댓글 61개가 모였다.

답변의 성격이 두 갈래로 갈린다.
하나는 글 한 편을 지목하는 것이고, 다른 하나는 자기가 관리하는 읽기 목록 전체를 내미는 것이다.
그리고 가장 높은 점수를 받은 답변이 후자였다.

## 가장 많이 꼽힌 글

| 점수 | 추천인         | 글                                                |
| ---- | -------------- | ------------------------------------------------- |
| 41   | koala          | 본인이 3년째 관리하는 읽을거리 목록               |
| 28   | ThePaulMcBride | grugbrain.dev                                     |
| 27   | landon         | Caleb Hearth, Don't Get Distracted                |
| 26   | Relax          | Ben Kuhn, You Don't Need to Work on Hard Problems |
| 24   | voutilad       | Alexis King, Parse, Don't Validate                |
| 22   | nick4          | Sandi Metz, The Wrong Abstraction                 |
| 15   | cole-k         | aphyr, Typing the Technical Interview             |
| 13   | simonw         | Joel Spolsky, The Law of Leaky Abstractions       |
| 12   | ahelwer        | Sean Goedecke, How to Ship                        |
| 11   | dvogel         | Bob Nystrom, Magpie 연재                          |
| 7    | inactive-user  | Tony Hoare, The Emperor's Old Clothes             |
| 6    | dallen         | Richard Gabriel, The Rise of Worse is Better      |
| 6    | scraps         | Taco Bell Programming                             |
| 5    | cceckman       | Reality Has a Surprising Amount of Detail         |
| 5    | jackdk         | 본인의 Haskell 자료 목록과 여러 논문·글           |

Hoare의 글은 추천자가 The Emperor's New Clothes라고 적었지만, 그가 건 링크의 실제 제목은 The Emperor's Old Clothes다.
1980년 튜링상 수상 강연이며, 추천자가 최고의 문장으로 꼽은 대목은 기술적으로 부실한 그 프로젝트가 무너지기를 처음에는 바랐지만 곧 성공할 운명임을 깨달았다는 구절이다.[^sayyadirfanali]

그 아래로도 목록은 길게 이어진다.
ruuda는 메시지 루프와 순수 함수 코어에 부수 효과를 함께 돌려주는 패턴의 출처로 Moron Lab의 글을 들었고, zem은 완벽한 코드베이스보다 완성품을 내놓는 일의 가치를 상기시키는 Slumming with Basic Programmers를 꼽았다.
angelixd는 Moxie Marlinspike의 커리어 조언에서 우리는 우리가 하는 일 그 자체이며 그렇지 않다고 말하는 것은 자기기만이라는 대목을 짚었고, carlana는 노력의 함수로서 의존성의 이득을 다룬 Eli Bendersky의 글을 들었다.
amw-zero는 Marc Brooker의 Formal Methods Only Solve Half My Problems를 최근 몇 년간 1순위로 꼽았고, thiht는 What Color Is Your Function이 자신을 더 나은 개발자로 만들었다고 확언할 수 있는 유일한 글이라고 적었다.
Sietsebb는 Railway-Oriented Programming을 통해 Result 타입을 처음 접했고, 오류를 예외로 던지는 대신 값으로 파이프라인에 흘려보낸다는 발상이 사고를 넓혔다고 밝혔다.

## 목록을 관리하는 사람들

koala의 최고점 답변이 스레드의 성격을 결정했다.
그는 자기 목록을 따로 관리한다고 밝히며, 이미 꽤 여러 편을 잃어버린 것에 지쳐서 3년쯤 전에 시작했다고 적었다.[^koala]

matklad가 곧바로 화답했다. 덕분에 당분간 읽을 목록이 생겼다며 자기 목록도 공개하고, 단순성에 관해서는 Why C++ Sails When The Vasa Sank도 좋았다고 덧붙였다.[^matklad]
tclancy는 자기 pinboard 태그 목록을 내놓으며, 관통하는 흐름을 찾아 달라고 Claude에 물어본 적이 있다고 적었다.
그의 Spolsky 글은 유니코드에 관한 것이었고, 2005년쯤 마이크로소프트 웹 스택으로 여러 언어를 다루려 할 때 요긴했다고 회고한다.[^tclancy]

jackdk는 Haskell 자료 목록을 공유하면서 질문의 범위를 조금 넓혀 아직 목록에 넣지 못한 브라우저 탭들도 꺼냈다. The Best Refactoring You've Never Heard Of, LANGSEC, Armstrong의 박사 논문 등이다.[^jackdk]
sjamaan이 LANGSEC에 동의하면서 자기 사고에 가장 큰 영향을 준 것일 수 있다고 적되, 학회 자료가 파서 기술에만 머무는 것이 아쉽다고 했다.
그에게 LANGSEC의 핵심은 직렬화와 주입 버그를 구성 단계에서 없애는 데까지 뻗어 있다.[^sjamaan]

mtlynch는 이 주제로 이미 긴 글을 썼다며 The Software Essays that Shaped Me를 링크하고 목록을 나열했다.
Joel Spolsky의 The Joel Test는 소프트웨어 개발자가 회사에 가져다주는 가치를 알게 해 주었고, Alexis King의 Parse, Don't Validate는 자신이 프로그래밍 언어 이론에 밝지 않은데도 타입 시스템의 가치를 알아보게 했다는 것이다.[^mtlynch]

## 분석

### 이 스레드의 가치는 개별 글이 아니라 합의된 정전(canon)에 있다

이 질문이 흥미로운 이유는 개인의 추천이 모여 프로그래밍 사고의 비공식 정전을 드러내기 때문이다.
Parse, Don't Validate, The Wrong Abstraction, The Law of Leaky Abstractions는 서로 다른 사람이 독립적으로 꼽았다.
같은 글이 반복 등장한다는 것은 그것이 개인 취향을 넘어 공동체의 공유 어휘가 되었음을 뜻한다.

이 정전이 중요한 이유는 분야의 암묵적 합의를 가시화하기 때문이다.
소프트웨어 공학에는 공식 교과서만큼이나 이런 블로그 글들이 사고의 토대를 이룬다.
Parse, Don't Validate는 타입으로 불변식을 강제하라는, The Wrong Abstraction은 성급한 추상을 경계하라는 원칙을 각인시켰다.
이 글들이 반복 인용된다는 것은 공동체가 그 원칙을 공통 전제로 받아들였다는 증거다.

### 최고점 답변이 글이 아니라 목록이었다는 사실

질문은 글 한 편을 물었는데 41점으로 1위를 한 답변은 링크 모음이었다.
2위권에도 목록형 답변이 섞여 있고, 그 아래에서 답변자들이 서로의 목록을 교환한다.

이것은 질문에 대한 회피가 아니라 질문의 전제에 대한 수정으로 읽힌다.
어떤 글 한 편이 사고를 바꿨다는 서술은 사후적으로 구성된 이야기이고, 실제로 일어난 일은 수십 편이 몇 년에 걸쳐 조금씩 쌓인 것에 가깝다.
koala가 목록을 시작한 이유도 그 축적을 잃어버리는 것이 아까워서였지 한 편을 기억하기 위해서가 아니었다.

여기서 스레드가 실제로 생산한 가치도 드러난다.
개별 추천 하나하나보다, 서로 다른 사람이 오래 관리해 온 목록 네댓 개가 한자리에 모였다는 것이 더 큰 수확이다.
matklad의 반응이 그 점을 정확히 말한다. 한 편을 얻은 것이 아니라 당분간의 읽을거리를 통째로 얻었다는 것이다.

### 상위권은 기술이 아니라 태도에 관한 글이다

목록 답변을 빼고 개별 글만 보면 상위 다섯 편의 성격이 한쪽으로 쏠린다.
grugbrain.dev는 복잡도 앞에서의 겸손을 다루고, Don't Get Distracted는 집중을 다루며, You Don't Need to Work on Hard Problems는 어려운 문제에 대한 집착을 다루고, The Wrong Abstraction은 잘못된 추상이 없는 추상보다 위험하다는 판단을 다룬다.
순수하게 기술적인 것은 Parse, Don't Validate 하나뿐이고, Typing the Technical Interview는 기술 글이되 추천 이유가 재미였다.

cole-k가 그 이유를 솔직하게 적었다. 기대한 답은 아니겠지만 그 글은 프로그래밍에 대한 글쓰기가 얼마나 재미있을 수 있는지를 보여 줬고 지금도 영감으로 남아 있다는 것이다.
공감 가는 기술 글은 많지만 이만큼 또렷하게 기억나는 것은 없다고 덧붙인다.[^cole-k]

그렇다면 이 목록이 측정하는 것은 기술적 유용성이 아니라 직업관의 형성이다.
특정 기술의 사용법이 아니라 추상, 검증, 단순성, 집중 같은 판단에 관한 글이 살아남았다. 기술은 낡지만 판단은 오래간다.
Relax의 답변이 그 성격을 잘 보여 준다. 그 글이 자기가 경력 7~8년차에 느끼기 시작한 것을 말로 옮겨 주었다는 것이고, 많은 사람이 그 글에서 득을 볼 것이라는 추천이다.[^Relax]
후속 대화에서 그는 당시 스타트업에서 어려운 문제를 다루면서도 행복하지 않았고, 행복했던 다른 직장들을 돌아보니 정말 중요한 것은 실제로 쓰이는 무언가를 만드는 것과 함께 일하는 사람이었다고 밝힌다.[^Relax-followup]

### 정전이 대체로 오래된 글로 채워져 있다

연도를 붙여 보면 편향이 분명해진다.
Hoare의 튜링상 수상 강연은 1980년, Worse is Better는 1991년, Joel의 글들은 2000년과 2002년, Taco Bell Programming은 2010년, Parse, Don't Validate는 2019년이다.
최근 몇 년의 글은 Sean Goedecke의 How to Ship 정도가 눈에 띈다.

이것을 오래된 글이 더 좋다는 증거로 읽기는 어렵다.
영향을 확인하려면 시간이 필요하고, 사고가 바뀌었다고 말하려면 바뀌기 전의 자신을 기억할 만큼 시간이 지나 있어야 한다.
즉 이 목록은 좋은 글의 순위가 아니라 충분히 오래되어 영향이 관측된 글의 목록이며, 최근 글은 구조적으로 들어올 수 없다.

ahelwer의 추천이 그 예외 자리에 있어 흥미롭다.
그는 Sean Goedecke가 이곳에서 미움을 좀 받는다고 전제하면서도, 어떤 블로거에 대해 사람들이 의견을 갖는다는 것 자체가 주목할 만한 일이라고 적는다.
그가 꼽은 대목은 대기업 안에서 실제로 아무것도 내보내지 않고도 성공적인 커리어를 쌓는 것이 충분히 가능하다는 지적이고, 완벽주의자의 함정에 빠지기 쉬운 자신에게 그것이 유효했다는 것이다.[^ahelwer]

### 읽기와 쓰기의 관계에 대한 두 관점이 드러난다

marginalia의 답변, 곧 글을 읽기보다 쓰면서 더 영향받는다는 말은 이 스레드의 전제를 살짝 비튼다.
질문은 어떤 글이 당신에게 영향을 줬느냐를 묻지만, marginalia는 영향의 원천이 소비가 아니라 생산이라고 답한다. 쓰는 행위가 곧 사고 과정이라는 것이다.[^marginalia]

이 관점이 중요한 이유는 사고의 형성 방식에 대한 두 모델을 대비시키기 때문이다.
하나는 좋은 글을 읽어 사고가 형성된다는 소비 모델이고, 다른 하나는 직접 써 보며 사고가 벼려진다는 생산 모델이다.
스레드의 대다수는 소비 모델로 답하지만, marginalia와 aphyr를 언급한 cole-k는 생산 쪽을 가리킨다.

후속 질문을 받고 marginalia가 덧붙인 답이 이 대비를 더 날카롭게 만든다.
사고를 실질적으로 바꾼 블로그 글을 떠올릴 수 없고, 읽기가 뚜렷한 전후를 남긴 유일한 사례는 플라톤과 에픽테토스 정도라는 것이다.
그러면서 그냥 좋은 글을 원한다면 How Developers Stop Learning: Rise of the Expert Beginner를 좋아한다고 덧붙인다.[^marginalia-followup]

두 모델은 배타적이지 않고 순환한다.
좋은 글을 읽으면 쓰고 싶어지고, 쓰면서 읽은 것을 자기 것으로 만든다.
koala와 matklad가 읽기 목록을 관리하고 공유하는 것은 소비와 생산 사이의 이 순환을 제도화한 행위다.
읽은 것을 목록으로 남기고 남과 나누는 것 자체가 수동적 소비를 능동적 정리로 바꾼다.

이 해석을 받아들이면 목록의 용도가 하나 더 생긴다.
읽을 것을 고르는 참고 자료가 아니라 쓸 것을 고르는 참고 자료가 되는 것이다.
목록의 각 항목은 누군가 충분히 오래 붙들고 있어서 한 편으로 정리해 낸 주제이고, 그것은 곧 이 분야에서 정리할 가치가 있는 주제의 목록이기도 하다.
가장 적극적으로 답한 사람들이 대체로 쓰는 사람이라는 사실이 그 해석을 뒷받침한다. mtlynch는 아예 같은 질문에 대한 자기 글을 링크했다.

## 비평

### 영향과 기억이 구분되지 않는다

질문은 사고에 영향을 준 글을 물었지만 답변 상당수는 기억에 남은 글을 답한다.
voutilad의 답변이 이 문제를 스스로 드러낸다. Parse, Don't Validate가 이름으로 떠올릴 수 있는 유일한 글이며, 어쩌면 제목이 완벽해서 기억에 들러붙은 것일지도 모른다는 것이다.[^voutilad]

이 자기 관찰은 목록 전체의 신뢰도를 흔든다.
제목이 기억에 잘 남는 글과 사고를 실제로 바꾼 글은 겹칠 수도 있고 아닐 수도 있는데, 회상으로 만든 목록은 둘을 구분할 방법이 없다.
그리고 상위권의 제목들을 보면 이 편향이 실재한다는 심증이 강해진다. Parse, Don't Validate, The Wrong Abstraction, Don't Get Distracted, You Don't Need to Work on Hard Problems는 전부 명령문이거나 부정문이며 한 문장으로 요약된 주장이다.

이 구별이 중요한 이유는 영향력과 밈성을 혼동하게 하기 때문이다.
이런 제목은 대화에서 쉽게 소환되고, 소환될수록 더 자주 추천되어 정전에 굳어진다.
그러나 소환하기 쉬운 것과 사고를 가장 깊이 바꾼 것이 같지는 않다. 제목이 밋밋하지만 깊은 글은 이런 스레드에서 이름이 떠오르지 않아 과소 대표된다.

이것은 앞선 aligned-to-whom에서 본, 짧고 강한 프레이밍이 반박에 취약하되 인상은 강한 것과 같은 현상이다.
기억에 남는 형식이 영향력의 대리 지표가 되면, 잘 포장된 아이디어가 잘 논증된 아이디어를 이긴다.
이 스레드의 목록도 부분적으로는 가장 영향력 있는 글이 아니라 가장 회자하기 좋은 글의 목록일 수 있다.

### 한 커뮤니티의 정전을 일반적 정전으로 읽기 쉽다

목록을 훑으면 특정 방향의 쏠림이 눈에 띈다.
Parse, Don't Validate, Railway-Oriented Programming, jackdk의 Haskell 목록, Bob Nystrom의 Magpie 연재, What Color Is Your Function, Why I Still Lisp, LANGSEC까지 함수형 프로그래밍과 언어 이론 계열이 두텁다.
반대 관점, 곧 동적 타입의 유연함이나 빠른 반복의 가치를 옹호하는 글은 드물다.

이것은 Lobste.rs라는 장소의 성격이지 프로그래밍 일반의 성격이 아니다.
같은 질문을 다른 커뮤니티에 던지면 목록이 상당히 달라지리라고 보는 편이 안전하며, 실제로 이 목록에는 프런트엔드, 모바일, 데이터, 게임, 임베디드 쪽 글이 거의 없다.
ahelwer가 Sean Goedecke를 추천하며 그가 여기서 미움받는다고 단서를 단 것은, 이 공동체에 이미 선호와 배척의 기류가 있음을 드러낸다.
정전은 무엇이 좋은지를 보여 주는 만큼 그 공동체가 무엇을 밀어내는지도 보여 준다.

이 스레드가 GeekNews로 넘어온 뒤 달린 한국어 댓글들이 그 편향을 우연히 실증한다.
winterjung은 The Configuration Complexity Clock이 유독 기억에 남는다고 적었고[^winterjung], aucun은 늘 그만두기에 관한 글을 꼽는다고 했다.[^aucun]
onixboox의 답변이 특히 그렇다. 델마당에 양병규가 늦은 나이에 프로그래밍에 입문한 사람을 위해 쓴 글을 들며, 델마당이 사라져 원본은 찾지 못하고 다른 사이트에서만 볼 수 있다고 덧붙였다.[^onixboox]

원본 스레드의 어느 답변에도 이런 종류의 글은 없다. 언어권이 다르면 정전도 다르고, 심지어 그 정전이 놓인 플랫폼의 수명도 다르다.
델마당처럼 커뮤니티가 사라지면 그 정전은 링크째 소실된다는 사실은 앞서 본 목록 관리 습관이 왜 중요한지를 다른 각도에서 보여 준다.
영어권 목록의 오래된 항목들이 아직 살아 있는 것은 글이 더 좋아서가 아니라 호스팅이 더 오래 버텼기 때문이기도 하다.

따라서 이런 목록을 절대적 필독서로 받아들이면 위험하다.
그것은 특정 시대, 특정 공동체의 취향을 반영한 스냅숏이다.
목록을 옮길 때 어느 커뮤니티에서 모인 것인지를 함께 옮기는 것이 최소한의 정직이다.

### 추천 이유가 글의 내용보다 추천자의 시기를 말한다

답변들을 자세히 읽으면 같은 패턴이 반복된다. 그 글을 언제 읽었는지가 왜 영향을 받았는지를 설명한다는 것이다.

simonw는 커리어 초반에 The Law of Leaky Abstractions를 읽었고, 그것이 자기가 일하는 층 아래를 늘 더 이해하려 애쓰게 만들었다고 적는다. 추상이 새는 순간을 대비해서다.
그가 함께 꼽은 2018년의 Migrations: the sole scalable fix to tech debt는 경력의 다른 시점에서 온 것이며, 마이그레이션이 기술 부채를 확장 가능하게 해결하는 유일한 수단이라는 발상을 사랑한다고 밝힌다.[^simonw]

Relax의 7~8년차, mtlynch의 초년, ahelwer의 완벽주의 성향처럼, 추천의 근거는 대체로 글이 아니라 독자의 당시 상태다.
이것이 뜻하는 바는 실용적이다. 남의 인생을 바꾼 글이 내 인생을 바꿀 확률은 우리가 비슷한 시기에 비슷한 문제를 겪고 있을 때만 높아진다.
목록을 위에서부터 차례로 읽는 방식이 별로 효과가 없는 이유이며, 지금 내가 걸려 있는 문제의 이름으로 목록을 검색하는 편이 낫다.

## 인사이트

### 영향력 있는 글은 이미 알던 것에 이름을 붙여 준 글이다

상위권 글들의 공통점을 다시 보면 새로운 지식을 전달하는 글이 거의 없다.
어려운 문제에 매달릴 필요가 없다는 것, 잘못된 추상이 중복보다 나쁘다는 것, 추상은 샌다는 것, 산만해지지 말라는 것은 전부 경험 있는 개발자가 이미 어렴풋이 알고 있는 것들이다.

Relax가 쓴 표현이 이 구조를 정확히 말한다. 그 글이 자기가 느끼기 시작한 것을 말로 옮겨 주었다는 것이다.
wolfadex의 답변도 같다. 블로그 글은 아니지만 미치 헤드버그의 테니스 농담을 꼽으며, 이미 느끼고 있었지만 그것을 표현할 말이 없던 것이라고 적었다.[^wolfadex]

그렇다면 영향력의 메커니즘은 정보 전달이 아니라 명명이다.
이름이 붙는 순간 그것은 대화에서 가리킬 수 있는 대상이 되고, 코드 리뷰에서 근거로 쓸 수 있게 되며, 스스로도 그 상황을 알아보게 된다.
Parse, Don't Validate가 기술 글 중 유일하게 상위권에 오른 이유도 새 기법을 알려 줘서가 아니라, 여러 언어에 흩어져 있던 실천에 하나의 이름을 준 데 있을 것이다.

글을 쓰는 쪽에서 이 관찰은 곧바로 실천으로 바뀐다.
독자가 모르는 것을 가르치려 하기보다, 독자가 이미 겪고 있는데 부를 이름이 없는 것을 찾아 이름을 붙이는 편이 훨씬 멀리 간다.
그리고 그 이름은 짧은 명령문일수록 오래 남는다. voutilad가 제목 때문에 기억한다고 한 것이 농담이 아니다.

### 블로그 글이 소프트웨어 공학의 실질적 교과서 역할을 한다

이 스레드가 드러내는 가장 이전 가능한 통찰은 소프트웨어 공학의 사고가 교과서가 아니라 블로그 글로 전수된다는 점이다.
Parse, Don't Validate나 The Wrong Abstraction은 학술 논문도 교과서도 아니지만, 현장 개발자의 사고를 논문보다 더 깊이 형성한다.

이 현상이 중요한 이유는 지식 전수의 매체가 이동했음을 보여 주기 때문이다.
소프트웨어는 빠르게 변해 교과서가 따라잡지 못한다.
반면 블로그 글은 즉각적이고, 현장 경험에서 나오며, 공동체가 인용과 추천으로 검증한다.
이 검증은 동료 심사와 다르지만 나름의 엄정함을 갖는다. 수년에 걸쳐 반복 인용되는 글만이 정전에 남기 때문이다.

두 번째 차수의 효과는 이것이 좋은 글쓰기의 가치를 높인다는 점이다.
자기 통찰을 기억에 남는 형식으로 쓸 수 있는 개발자는 그 통찰을 공동체의 어휘로 만든다.
한 사람의 명료한 글이 수많은 개발자의 사고를 바꾸며, 코드를 잘 짜는 것만큼이나 사고를 잘 전달하는 글쓰기가 영향력의 통화가 되었다.

다만 이 통찰에는 앞의 비평이 단서로 붙는다.
정전에 남는 조건이 내용의 깊이만이 아니라 제목의 소환 가능성이기도 하다면, 이 통화는 논증의 질이 아니라 포장의 질을 보상하는 쪽으로도 기운다.
그리고 블로그는 교과서와 달리 호스팅이 끊기면 사라진다. 델마당의 사례가 그 취약함을 보여 준다.

### 희소해진 것은 글이 아니라 큐레이션이다

이 스레드에서 가장 높은 점수를 받은 것이 링크 목록이었다는 사실은 시대의 지표로 읽을 만하다.
좋은 기술 글은 20년 전보다 압도적으로 많고, 요약은 이제 기계가 무료로 해 준다. 부족한 것은 텍스트가 아니라 무엇을 읽을지에 대한 판단이다.

koala의 목록이 값을 하는 이유는 큐레이터가 누구인지 알 수 있기 때문이다.
3년 동안 한 사람이 자기 기준으로 모았고, 그 사람의 다른 발언을 통해 그 기준을 가늠할 수 있다. 알고리즘 추천이나 모델 요약에는 없는 성질이다.
tclancy가 Claude에게 자기 목록의 관통하는 흐름을 찾아 달라고 했다는 일화가 그 보완 관계를 보여 준다. 수집은 사람이 하고 패턴 발견은 기계에 맡긴 것이다.

여기서 나오는 2차 효과가 있다.
LLM이 어떤 글이든 요약해 줄 수 있게 되면 요약의 가치는 0에 수렴하고, 남는 것은 무엇을 요약할지 고른 사람의 판단이다.
fde-organizational-capability에서 본, 지식 접근이 평등해질수록 판단이 희소해진다는 통찰이 여기서도 반복된다.
그리고 그 판단은 공개된 목록의 형태로만 관측 가능하다. 읽은 것을 기록하지 않는 사람은 그 자산을 가질 수 없다.

실천적으로는 목록을 갖는 것 자체가 권할 만한 일이 된다.
koala가 시작한 계기가 잃어버린 것이 아까워서였다는 점도 중요하다. 남에게 보여 주려고 시작한 것이 아니라 자기 기억의 외부 저장소였고, 공개된 것은 그다음이다.
이 순서가 지속 가능한 목록과 금방 방치되는 목록을 가른다.

### 정전은 사람에게 전달되도록 만들어졌고, 에이전트에는 그 경로가 없다

이 스레드에서 가장 멀리 가는 발언은 landon이 The Wrong Abstraction에 단 답글이다.
그는 에이전트의 시대가 열린 뒤로 이 글을 다시 읽지 않았는데 지금은 느낌이 꽤 다르다고 적는다. 에이전트가 앞선 사람들이 남긴 바퀴 자국을 사람보다도 훨씬 더 고집스럽게 따라간다는 것이다.
사람에게는 이 글을 링크로 보내고 오지 않을 미래를 위한 편의 기능을 만들지 말라고 말하면 되고, 몇 번 상기시켜야 할 때도 있지만 결국 알아듣는다. 에이전트에는 그 경로가 없다.[^landon]

이 관찰이 중요한 이유는 이 목록 전체의 전달 방식을 겨냥하기 때문이다.
여기 모인 글들은 설득의 형식으로 쓰였다. 사례를 들고 반례를 놓고 독자가 스스로 판단을 바꾸도록 유도한다.
그 형식이 작동하려면 읽고 납득하고 다음에 비슷한 상황에서 그것을 떠올리는 주체가 있어야 하는데, 에이전트는 매 세션 그 기억을 갖지 않는다.

그래서 이 정전을 코드에 반영하려면 번역이 필요하다.
에세이가 아니라 규칙으로, 설득이 아니라 제약으로 옮겨야 하며, 실제로 여러 팀이 그 작업을 하고 있다. 규약 문서, 린트 규칙, 스킬 파일이 그 형태다.
문제는 번역 과정에서 잃는 것이다. The Wrong Abstraction의 핵심은 언제 중복을 허용할지에 대한 판단이고, 판단은 규칙으로 옮기는 순간 대체로 한쪽으로 고정된다.

그리고 여기에 세대 문제가 붙는다.
사람에게 이 글들이 영향을 준 방식은 커리어의 특정 시점에 우연히 읽는 것이었고, 그 우연을 만들어 준 것이 이런 스레드와 목록이었다.
에이전트가 코드의 상당 부분을 쓰는 환경에서 다음 세대가 이 우연을 겪을 기회가 얼마나 남을지는 별개의 질문이며, 이 스레드의 답변들이 대체로 10년 이상 된 글이라는 사실이 그 질문을 조금 불편하게 만든다.

---

[^koala]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_kdrw5b>

[^matklad]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_zvwh0o>

[^tclancy]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_b5bama>

[^jackdk]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_bb1ujz>

[^sjamaan]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_tfx9t1>

[^mtlynch]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_uxoaba>

[^cole-k]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_it7mgq>

[^Relax]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_kuj3tq>

[^Relax-followup]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_jqadcu>

[^ahelwer]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_hwtfzy>

[^voutilad]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_fssgte>

[^marginalia]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_8z8oop>

[^marginalia-followup]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_c5q5ds>

[^simonw]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_4fxnwn>

[^wolfadex]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_pixtgv>

[^landon]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_y1gumm>

[^sayyadirfanali]: <https://lobste.rs/s/lbavmm/what_blog_posts_influenced_your_thinking#c_zbfbez>

[^winterjung]: <https://news.hada.io/topic?id=33714#cid65547>

[^aucun]: <https://news.hada.io/topic?id=33714#cid65721>

[^onixboox]: <https://news.hada.io/topic?id=33714#cid65569>
