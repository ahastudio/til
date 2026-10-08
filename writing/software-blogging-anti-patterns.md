# 개발 블로그는 독자에게 떠날 이유를 주지 말아야 한다

원문: [Anti-Patterns in Software Blogging · Refactoring English](https://refactoringenglish.com/blog/anti-patterns-software-blogging/)

HN 토론: <https://news.ycombinator.com/item?id=49992257> (242점, 129개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging> (78점, 37개 댓글)

GN 토론: <https://news.hada.io/topic?id=34962>

## 요약

Michael Lynch가 2026년 10월 7일 자신의 책 사이트인
Refactoring English 블로그에 올린 글이다.
그는 소프트웨어 개발에서 나쁜 결과로 이어지는 공통 특징을
안티패턴으로 모으듯,
초보 블로거에게서 가장 자주 보는 실수를 같은 방식으로 정리했다고
첫 문단에서 밝힌다.
목록은 장황한 도입, 서문, 독자의 배경지식에 대한 가정, 링크 의존,
후속편 전제, 과도한 격식으로 이어지고,
HTML 렌더링의 기본기(모바일 화면 넘침, 읽기 어려운 글꼴)로 끝난다.
각 항목에는 나쁜 예와 좋은 예가 나란히 붙어 있다.

### 도입과 서문

저자는 소프트웨어 블로그에서 단연 가장 흔한 실수가 장황함이라고 말한다.
개발자는 구체성을 좋아해서 배경 이야기와 역사적 맥락으로 글을 시작하지만,
독자에게는 읽을 수 있는 다른 글이 수없이 많다.
얻을 것이 있다는 기대 없이는 20분을 들여 끝까지 읽지 않는다.
글을 펼친 개발자는 이 글이 나 같은 사람을 위해 쓰였는지,
읽으면 무엇을 얻는지 두 질문에 가능한 한 빨리 답하려 한다.
그래서 저자는 제목과 첫 세 문장 안에 두 답을 모두 주라고 권한다.
좋은 예로는 자기 글
if got, want: A Simple Way to Write Better Go Tests의 도입을 든다.
잘 알려지지 않은 Go 테스트 패턴을 30초 안에 가르쳐 주겠다는 두 문장이다.
도입을 잘 써 놓고도 부제, 자기소개, 이미지, 유명한 인용문을 앞에 늘어놓으면,
이것들도 독자가 계속 읽도록 설득하는 예산을 깎아 먹는다고 덧붙인다.

### 독자가 아는 것과 링크, 후속편

두 번째 안티패턴의 이름은
독자가 이 한 가지만 빼고 내가 아는 모든 것을 안다는 가정이다.
Docker 입문 글에서 Docker를 Linux cgroups의 프런트엔드,
또는 *BSD jails의 Linux판이라고만 설명하면
그 용어를 모르는 독자를 놓친다.
저자는 실제로 아는 친구나 동료 한 명을 기준 독자로 정하라고 권한다.
그 사람이 알 용어와 모를 용어의 목록을 만든 뒤,
초안을 그 사람의 눈으로 다시 읽으라는 것이다.
그가 편집을 도운 Tyler Cipriani가
이 목록과 초안의 가정을 비교해 보는 일이 꽤 놀라웠다고 한 말도 인용한다.

링크 의존은 모르는 용어에 링크만 걸고 설명을 떠넘기는 습관이다.
방화벽이라는 단어에 FreeBSD 핸드북의 방화벽 장을 걸면,
약 2만 단어짜리 문서를 읽는 일을 독자에게 넘기게 된다.
대신 이해에 필요한 최소한의 설명을 본문에 쓰고,
링크는 필수 조건이 아닌 덤으로 두라고 한다.
기준 독자가 링크를 하나도 누르지 않고 처음부터 끝까지 읽을 수 있어야 한다.
저자가 sequel injection bug라고 이름 붙인 후속편 전제도 같은 문제다.
대부분의 독자는 1편을 읽지 않았으므로,
이전 글을 도입부터 내세우지 말고 필요한 부분만 요약하라고 한다.
후속편 대부분은 3% 정도만 더 애쓰면 독립된 글이 될 수 있다고 본다.

### 격식과 렌더링

저자는 초보 블로거가 진지하게 받아들여지려면 딱딱하게 써야 한다는
집단적 착각에 빠져 있다고 말한다.
나쁜 예는 다음 문장이다.
“Several static analysis tools were utilized by my teammates and myself
throughout the duration of this project's lifetime.”
좋은 예는 “We tried a few static analyzers on this project.”다.
독자는 아마 잠옷 차림으로 키보드 옆에서 시리얼을 먹고 있으니,
법률 문서처럼 말할 필요가 없다는 것이다.
그는 많은 개발자가 글쓰기를 AI에 맡기면서
소프트웨어 블로그가 밋밋하고 획일적으로 변하고 있고,
독자는 개성 있는 글에 굶주려 있다고 덧붙인다.
역대 최고의 소프트웨어 블로거로 꼽는 Joel Spolsky의
The Perils of JavaSchools 한 대목을 예로 들고,
Kathy Sierra, Terence Eden, Raymond Chen도 같은 문체를 쓴다고 말한다.

마지막 묶음은 글쓰기에서 가장 쉬워야 할 부분,
곧 웹 페이지를 제대로 만드는 일이다.
저자는 데스크톱 크기를 고집하는 이미지나 코드 조각 때문에
모바일에서 본문이 화면을 넘치는 것을 가장 나쁜 실수로 꼽는다.
게시 전에 Firefox와 Chrome의 모바일 미리보기로 확인하라는 것이다.
그의 통계로는 이 글을 휴대폰으로 읽는 독자가 25%,
개인 블로그에서는 35%다.
밝은 회색 바탕에 짙은 회색 글자 같은 낮은 대비는
브라우저의 접근성 도구로 찾을 수 있다.
글꼴을 고르기 어렵다면
Braille Institute의 무료 글꼴 Atkinson Hyperlegible을 쓰라고 권한다.
글은 항목별 요약으로 끝나고,
그 아래에 2026년 10월 11일까지 30% 할인 중인 책 Refactoring English의
안내가 붙는다.

## 분석

### 모든 항목은 독자의 집중력을 예산으로 보는 한 가지 모델에서 나온다

여덟 개의 항목은 따로 떨어진 요령처럼 보이지만,
저자가 서문 항목에서 쓴 표현 하나로 거의 다 설명된다.
독자의 길에 놓인 모든 것은 유한한 집중력을 깎아 먹는 추가 작업이라는 것이다.
링크 항목에서는 2만 단어짜리 문서가 독자에게 떠넘긴 막대한 작업이 되고,
후속편 항목에서는 읽기를 시작하기도 전에 생긴 추가 과제가 된다.
모바일 화면 넘침도 좌우로 스크롤하는 추가 노동이다.
목록 전체가 독자가 글을 떠날 이유를 하나씩 지우는 작업이라는 점에서,
이 글은 문체 지침이라기보다 독자 이탈 지점의 목록에 가깝다.

이 모델에서 독자는 언제든 떠날 수 있는 소비자다.
저자가 도입 항목에서 수없이 많은 다른 글을 언급하는 것도 같은 전제다.
그래서 처방은 늘 독자가 들일 비용을 줄이는 쪽으로 향한다.
글쓴이가 들일 비용, 곧 설명을 직접 쓰고 이전 글을 요약하는 수고는
당연히 감수할 몫으로 계산된다.
3% 더 애쓰면 된다는 후속편 항목의 숫자가 이 계산을 그대로 보여 준다.

HN의 janalsncm은 이 항목들이 모두 공감으로 귀결된다고 정리하고,
처음 10초 안에 관심을 끌면 30초를 더 번다고 적었다[^janalsncm].
Lobste.rs의 facundoolano는 첫 문단을 통째로 지워도 글이 읽히면
지운 쪽이 대개 낫고, 그다음 이를 반복하라는 요령을 보탰다[^facundoolano].
둘 다 같은 예산 모델을 다른 말로 옮긴 것이다.

### 개발자의 말로 글쓰기 실수를 부른다

이 글은 글쓰기 조언을 개발자의 어휘로 포장한다.
제목부터 안티패턴이고,
후속편 전제는 SQL injection을 빗댄 말장난인 sequel injection bug이며,
렌더링 실수는 HTML 렌더링의 기본기를 그르친다는 말로 묶인다.
이 장치는 새 개념을 독자에게 익숙한 것에 견주어 설명하라는 원칙을
글 자신에게 적용한 것으로 읽힌다(해석이다).
저자가 Jellyfin을 Netflix 같은 스트리밍 서비스이되
오픈소스이고 사적인 것이라고 설명한 예와 같은 구조다.

이 포장은 대상 독자를 좁히는 효과도 있다.
글쓰기를 소프트 스킬로 미뤄 두는 개발자에게,
이것도 코드 리뷰처럼 패턴으로 다룰 수 있다는 신호를 준다.
같은 사이트의 How to Write an Effective Software Design Document를 다룬
`documentation/effective-design-doc.md`도
설계 문서를 엔지니어링 산출물로 다루는 같은 태도를 보여 준다.
저자는 Refactoring English라는 책 제목부터 이 틀을 쓰고 있다.

HN의 ram1500natrluvr는 장황한 도입이 가장 흔한 실수일지는 몰라도,
가장 해로운 실수는 주제를 독자가 아는 것과 연결하지 못하는
두 번째 항목이라고 주장했다[^ram1500natrluvr].
그는 새 도구, 설계 패턴, 라이브러리, 모델, 하네스 모두에 대해
그것이 없는 프로젝트가 어떤 모습인지 먼저 보여 주라고 요구했다.
저자가 첫 항목으로 꼽은 것과 독자가 가장 아프게 느끼는 것이
다를 수 있다는 지적이다.

### 격식 항목은 AI 시대의 문체 문제로 넘어간다

격식 항목만은 집중력 예산 모델로 깔끔하게 설명되지 않는다.
딱딱한 문장도 끝까지 읽을 수는 있기 때문이다.
저자는 여기서 근거를 바꿔,
AI에 글을 맡기는 개발자가 늘수록 블로그가 획일적으로 변하고
독자는 개성을 원한다고 말한다.
이 항목에서 목록의 관심사는 독자의 비용에서 글쓴이의 목소리로 옮겨 간다.

반응도 이 지점에 몰렸다.
Lobste.rs의 simonw는 격식을 버리고 평소처럼 쓰라는 말에 전적으로 동의하며,
LLM이 바로 그 목소리를 없애고 사람들이 그것을 알아챈다고 적었다[^simonw-2].
HN의 jrochkind1은 어떤 주에는 보이는 소프트웨어 블로그 대부분이
LLM으로 쓴 글 같고 대체로 형편없다며,
이 안티패턴을 LLM에게 알려 주면 나아지겠느냐고 물었다[^jrochkind1].
janalsncm은 이 글을 온라인에 올린 것만으로
이미 그렇게 한 셈이라고 답했다[^janalsncm-2].

Lobste.rs의 dutc는 한발 더 나아가,
이런 말을 들어야 하는 사람이라면 어떤 식으로든 LLM을 글쓰기에 쓰지
말아야 한다는 것이 가장 현대적인 조언이라고 적었다[^dutc].
이 글의 목록이 2026년의 독자에게는
사람이 쓴 글을 가려내는 신호의 목록으로도 읽힌다는 뜻이다.

### 저자의 이력과 책이 목록의 무게를 정한다

저자는 HN 첫 페이지에 자주 오르는 블로거이고,
이 글은 책 출간 주간 할인 안내로 끝난다.
Lobste.rs에는 저자가 직접 올렸다.
목록의 근거는 통계가 아니라 그가 편집하며 본 초보 블로거들의 원고이며,
Tyler Cipriani 인용과 자기 글의 도입을 좋은 예로 쓰는 방식이 이를 드러낸다.

이는 약점이기도 하고 강점이기도 하다.
수치로 검증된 규칙은 아니지만,
실제 원고를 고쳐 본 사람의 반복 관찰이라는 점에서 구체적이다.
저자 자신도 댓글에서 이 지점을 분명히 했다.
Lobste.rs에서 그는 이것이 모두가 엄격히 따라야 할 규칙이 아니라,
글에 관심을 가질 사람을 찾기 어려운 블로거를 돕는 경험칙이라고
답했다[^mtlynch-lobsters-3].

## 비평

### 장황한 도입 규칙은 독자가 어디서 왔는지를 숨긴다

제목과 첫 세 문장 안에 답하라는 규칙은
목적을 가지고 검색해서 들어온 독자를 전제한다.
그런데 저자 자신이 HN 댓글에서 이 전제와 맞지 않는 사례를 인정했다.
Paul Graham과 Joel Spolsky의 글은 곧장 본론으로 들어가지 않고
서론, 본론, 결론 구조도 잘 따르지 않는다는 것이다.
방향이 불분명한 이야기로 시작하거나,
가치가 당장 드러나지 않는 곁가지를 길게 넣기도 한다[^mtlynch].
그는 오랫동안 이 모순으로 고민하다가,
두 사람의 글은 문장 자체의 완성도가
결론을 몰라도 계속 읽게 만드는 가치라고 결론지었다고 했다.

braiamp가 독자의 마음 상태에 따라 형식이 달라져야 한다고
반박하자[^braiamp],
저자는 Spolsky의 Things You Should Never Do를
아무도 검색해서 찾지 않는다고 답했다.
HN이나 RSS로 특별한 목적 없이 들어온 독자에게는
글쓴이가 시간을 들일 여지가 더 있다는 것이다[^mtlynch-2].
dustfinger도 요리책이나 튜토리얼이라면 동의하지만,
블로그에서는 글쓴이의 개성과 재미를 기대하고
서두르고 싶지 않다고 썼다[^dustfinger].
cyndunlop은 버그 추적 글은 탐정 이야기처럼 쓰고
벤치마크 글은 이야기 없이 쓰듯,
목적에 따라 접근이 다르다고 정리했다[^cyndunlop].

정작 중요한 이 구분, 곧 독자가 검색으로 왔는지 피드로 왔는지가
본문에는 없다.
본문은 모든 독자를 다른 글로 언제든 떠날 수 있는 사람으로 그리고,
그 예외는 댓글에서 저자 본인의 입으로만 나온다.
제목과 첫 세 문장이라는 숫자로 규칙의 범위를 정해 두면서,
그 범위가 성립하는 조건은 빼 버린 셈이다.

### 배경지식 최소화와 링크 금지는 깊이와 부딪친다

Lobste.rs의 amw-zero는 배경지식에 대한 가정을 최소화하라는 말보다
독자와 그 배경지식을 파악하라는 말이 낫다고 했다.
독자를 늘 완전한 초보로 가정하는 것도 좋은 글이 아니라는 것이다[^amw-zero].
purplesyringa는 Linux를 모르는 사람에게 Docker 내부를,
타입 이론을 모르는 사람에게 새 Rust 기능 제안을 설명할
좋은 방법은 없다고 썼다.
그래서 이 규칙은 가장 낮은 수준에 맞추라는 뜻이 아니라
대상 독자를 의도적으로 고르라는 뜻이어야 한다고 보았다[^purplesyringa].

dutc의 반론은 더 날카롭다.
장황한 도입은 대개 시각적으로 구분되어 스크롤 한 번으로 건너뛸 수 있지만,
기본 지식을 다시 설명하라는 요구는 모든 문단에 섞여 들어가
건너뛰기가 훨씬 어렵다는 것이다[^dutc].
그는 저자의 Docker 예시에 눈속임이 있다고 보았다.
권장된 쪽이 오히려 밋밋하고 이 경우 오해의 소지도 있으며,
금지된 쪽이 더 흥미로울 수 있다는 것이다.
실제로 좋은 예의 Docker 설명은 컨테이너와 격리라는 핵심을 빼고
재현 가능한 환경과 텍스트 파일만 말한다.
배경지식 가정을 줄이려다 개념의 정확성을 내준 사례가
이 규칙의 대표 예시로 쓰인 셈이다.

링크 항목도 본문과 저자의 실천 사이에 간격이 있다.
simonw는 링크 걸기를 무척 좋아한다며 이 항목이 슬프다고 했다.
저자는 자신도 링크를 많이 걸며,
기준은 링크를 누르지 않아도 글이 이해되느냐일 뿐이라고
답했다[^mtlynch-lobsters].
그러나 본문의 마지막 요약은
링크를 클릭하거나 툴팁 위에 마우스를 올리지 않고도 읽을 수 있어야 한다고
더 강하게 적는다.
HN의 kkapelon처럼 글을 스택처럼 읽으며
A 중간에 B로 갔다 돌아오는 것을 전혀 불편해하지 않는 독자도
있다[^kkapelon].
링크 항목이 실제로 겨냥하는 것은 링크가 아니라 설명의 생략인데,
제목은 링크를 문제 삼는다.

### 격식의 예시는 격식이 아니라 수동태와 군더더기를 보여 준다

나쁜 예로 든 문장의 문제는
utilized, throughout the duration of 같은 장황한 표현과 수동태다.
이것을 격식이라고 부르면 격식과 군더더기가 한데 묶인다.
HN의 dieselgate는 저자의 예문이 전혀 격식 있게 느껴지지 않는다고 했다.
그는 말하듯 쓰라는 조언이 좋은 목표이긴 하지만,
더 넓은 독자를 위해 혹은 업무상 영어로 쓰는 비원어민에게는
무턱대고 적용하기 어렵다고 지적했다[^dieselgate].
그에게는 상투어를 피하고 단어를 본뜻대로 쓰는 일이 더 중요했다.

반대쪽 취향도 분명히 있다.
HN의 layer8은 기술 글이 너무 가벼우면 산만하고
글쓴이는 자기 친구가 아니라고 했다.
그는 지나친 격식도 아닌 중립적이고 담백한 문체,
예컨대 Dijkstra의 문체를 좋아한다고 밝혔다[^layer8].
Lobste.rs의 marginalia는 누구에게나 같은 방식으로 말하지는 않는다며,
격식 있는 언어에도 목소리가 있을 수 있지만
그 문체에 익숙해야 드러난다고 적었다[^marginalia].
말하듯 쓰라는 처방은 영어 원어민이자 말을 잘하는 사람에게 유리하다.
그리고 글은 말보다 다듬을 기회가 많다는 장점을 스스로 내려놓게 할 수도 있다.

### 렌더링 항목은 대비와 화면 넘침에서 멈춘다

렌더링 기본기를 그르친다는 묶음에는 두 항목만 있다.
그런데 두 커뮤니티에서 가장 많이 나온 추가 안티패턴은 글의 작성일이었다.
Lobste.rs에서 가장 높은 점수를 받은 legoktm의 댓글은
작성일을 글 맨 위에 두지 않는 것과,
선택 자료여야 할 각주를 사실상 필수로 읽게 만드는 것을 더했다[^legoktm].
simonw는 아예 날짜가 없어서 소스 보기로 메타데이터를 뒤지고
Internet Archive까지 찾는 일이 너무 잦다고 했다.
언제 쓰였는지는 글쓴이의 관점을 이해하는 데 필수인 맥락이라는 것이다[^simonw].
HN에서도 mexicocitinluez가 같은 항목을 더했다[^mexicocitinluez].
저자의 글 자체는 맨 위에 날짜를 두고 있어서,
실천은 하지만 목록에는 넣지 않았다.

각주에 대해서는 fanf가,
독자는 각주가 읽을 가치가 있는지 미리 알 수 없으므로
각주는 언제나 흐름을 끊는다고 썼다.
웹에서는 종이 각주를 흉내 내기보다
본문 옆 보충 설명으로 배치하는 편이 낫다는 것이다[^fanf].
toastal은 JavaScript가 있어야 읽히는 블로그는 기술 독자를 놓친다며,
적어도 무엇을 놓치는지 알려 주는 `<noscript>`라도 두라고 요구했다[^toastal].
이 글의 페이지도 댓글 영역에 JavaScript를 켜라는 문구를 띄우고,
본문 삽화들은 HTML에서 대체 텍스트가 비어 있다.
대비를 접근성 도구로 확인하라고 권하는 글이
같은 접근성의 다른 기본기는 다루지 않는 것이다.

## 인사이트

### 블로그 규칙 목록은 다음 세대 LLM 글의 표준 형식이 된다

janalsncm의 농담처럼, 이런 목록은 공개되는 순간 LLM이 배울 자료가 된다.
제목과 첫 세 문장 안에 대상과 이득을 밝히고, 용어마다 짧은 설명을 붙이고,
구어체로 쓰라는 규칙은 모두 기계가 흉내 내기 쉬운 표면 형식이다.
그렇게 되면 이 형식은 좋은 글의 신호에서 흔한 글의 신호로 바뀐다(해석이다).
저자가 개성 있는 글을 원하는 독자의 갈증을 근거로 든 바로 그 지점에서,
규칙 목록은 획일화를 더 밀어붙일 수 있다.

이 순환은 이미 블로그 생태계 쪽에서 비용으로 나타나고 있다.
HN의 ogou는 2015년부터 2025년까지 신시사이저 제작 같은 긴 설명 글을 쓰며
Google 첫 페이지 트래픽을 꾸준히 얻었다.
그러나 이제 트래픽은 증발했고 99%가 LLM 학습용 수집으로 보이는 봇이라
블로그를 그만뒀다고 적었다[^ogou].
사람 독자를 붙잡는 요령을 다듬는 사이,
글을 끝까지 읽는 주체가 사람이 아니게 되는 셈이다.

그래서 이 목록의 수명은 각 규칙보다 그 밑의 질문에 달려 있다.
이 글은 누구를 위한 것이며 무엇을 주는가라는 질문은
기계가 흉내 낼 수 없는 구체성을 요구한다.
글쓴이가 실제로 겪은 일과 실제 기준 독자다.
규칙만 남고 질문이 빠지면,
저자가 경계한 밋밋한 글이 규칙을 지킨 채로 늘어날 것이다.

### 요리 블로그의 레시피 바로가기는 장황한 도입의 원인이 하나가 아님을 보여 준다

HN의 linsomniac은 지난주 HN 링크를 따라가다가,
기술 블로그에도 요리 블로그를 장악한 Jump to Recipe 링크가
필요해지고 있다고 느꼈다고 했다[^linsomniac].
요리 블로그의 긴 서두는 독자가 원해서가 아니라
검색 노출과 광고 체류 시간 같은 바깥의 유인에서 자랐고,
결국 글이 아니라 페이지 위의 버튼으로 우회됐다
(일반적인 인식에 기댄 해석이다).
저자가 진단한 기술 블로그의 장황함은 그와 달리 쓰는 사람이 즐거워서 생긴다.
원인이 다르면 처방도 달라야 한다.

LLM 시대의 기술 블로그는 두 원인을 동시에 갖는다.
phreack은 MCP가 무엇인지 몇 마디로 설명할 수 있는데,
검색하면 전화번호부만 한 글들이 끝내 요점에 이르지 않는다며
LLM이 이 문제를 훨씬 악화시켰다고 지적했다[^phreack].
기계로 부풀린 글은 요리 블로그의 서두처럼 바깥 유인에서 나오고,
사람이 쓴 장황한 글은 자기 표현에서 나온다.
도입을 줄이라는 저자의 처방은 앞쪽에는 거의 효과가 없고 뒤쪽에만 닿는다.

신문의 역피라미드는 이 문제를 구조로 다룬 오래된 사례다.
simonw는 많은 사람이 첫 문단을 넘기지 않는다고 가정하고
거기에 핵심을 담으라며 역피라미드를 권했다[^simonw-2].
marginalia는 이것이 자신의 기술 글 대부분의 틀이며
거의 실패하지 않는다고 답했다[^marginalia].
DonaldPShimoda가 지도교수에게서 들었다는,
논문과 발표는 살인 미스터리가 아니라는 말도 같은 원리다[^DonaldPShimoda].
목표는 자신이 겪은 깨달음을 재현하는 것이 아니라
독자를 결론에 데려가는 것이라는 뜻이다.
규칙 여덟 개보다 이 한 가지 구조가 더 오래 쓸 수 있는 도구일 수 있다.

### 규칙 목록은 초보자를 위한 비계이고, 그 사실이 드러나야 제 몫을 한다

목록에 대한 가장 근본적인 반론은 블로그가 제품이 아니라는 것이었다.
HN의 0x20cowboy는 블로그는 쓰는 사람이 원하는 것을 적는 일지라서
안티패턴이 없다고 했다[^0x20cowboy].
layer8은 그 말이 누구나 원하는 대로 쓸 수 있으니
나쁜 글이란 없다는 말과 같다고 받아쳤다[^layer8-2].
Lobste.rs의 nsfmc는 Sandi Metz가 초보에게 DRY를 가르치는 이유를 인용하며
규칙을 처방하는 태도에 반대했다[^nsfmc].
저자는 그에게 이것은 경험칙이며,
발행 뒤에 일어나는 일에 관심이 없다면 이 글은 쓸모가 없다고
답했다[^mtlynch-lobsters-3].
다만 그가 만난 블로거 대부분은 유명해지고 싶지는 않아도
누가 읽는지에는 관심이 있었다고 덧붙였다.

이 대답은 목록이 비계라는 사실을 인정한다.
비계는 건물이 서면 치운다.
문제는 본문이 이 사실을 말하지 않고 안티패턴이라는 보편 규칙의 말투를
쓴다는 점이다.
초보는 이 목록을 법칙으로 받아들이고,
경험자는 법칙의 말투에 반발해 쓸 만한 경험칙까지 버린다.
HN과 Lobste.rs의 반론 다수가 규칙의 내용보다 말투를 향했다는 점이
이를 보여 준다.

저자가 HN에서 덧붙인 말은 이 비계가 무엇을 위해 있는지 보여 준다.
한 번 해 본 일을 전문가처럼 가르치는 글이 거슬린다는 mcphage의 불만에[^mcphage],
그는 그것이 과도한 격식과 같은 뿌리에서 나온다고 답했다.
초보일 때 쓰는 글도 초보임을 밝히기만 하면
충분히 가치 있다는 것이다[^mtlynch-3].
그 예로 Julia Evans의 Some notes on using nix를 들었다.
아직 이해하지 못한 것을 쓰라는 `writing/blog-to-learn.md`의 주장과
같은 방향이다.
격식은 권위를 흉내 내려는 시도이고,
이 목록이 벗겨 내려는 것도 결국 그 흉내다.

### 기준 독자 목록은 블로그 밖에서 더 쓸모가 있다

글에서 가장 옮겨 쓰기 좋은 도구는 기준 독자가 알 용어와 모를 용어의 목록이다.
저자는 Lobste.rs에서 그 목록을 만드는 요령을 묻는 amycodes에게[^amycodes],
주제를 배우기 전의 자신을 떠올리고
독자가 알 것과 모를 것을 명시적으로 적으라고 답했다[^mtlynch-lobsters-2].
독자가 git을 모른다고 가정하면서 dig를 쓰라고 하면 dig도 설명해야 한다는
식으로, 기준선이 다른 용어의 판단을 돕는다는 것이다.
그는 경력 2~3년의 웹 개발자를 위한 글이라는 블로거에게
초보도 읽으려면 무엇을 바꿔야 하느냐고 물으면,
용어 두 개를 설명하는 두 문장이면 된다는 답이 자주 나온다고 했다.

이 목록은 블로그보다 README와 설계 문서에서 더 큰 효과를 낸다(해석이다).
ram1500natrluvr가 블로그와 함께 README를 지목했듯이,
그런 문서의 독자는 떠나지 못하고 대신 잘못 이해한 채 일을 진행하기 때문이다.
`documentation/effective-design-doc.md`가 다룬 설계 문서에서
기준 독자를 잘못 잡으면,
리뷰어는 글을 떠나는 대신 엉뚱한 부분에 의견을 단다.
블로그의 안티패턴은 조회수를 잃지만,
업무 문서의 같은 안티패턴은 결정을 잃는다.

목록을 만드는 일의 진짜 효과는 대상 독자를 다시 고르게 만든다는 데 있다.
저자의 두 문장 사례처럼,
목록을 적어 보면 독자를 넓히는 비용이
생각보다 작다는 것을 알게 되는 경우가 많다.
반대로 목록이 너무 길어지면 이 글이 그 독자에게 맞지 않는다는 신호다.
purplesyringa가 말한 대상 독자의 의도적 선택은
이 목록 없이 머릿속에서만 하기 어렵다.

---

[^janalsncm]: <https://news.ycombinator.com/item?id=49999267>

[^facundoolano]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_jwnjtx>

[^ram1500natrluvr]: <https://news.ycombinator.com/item?id=49995004>

[^simonw-2]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_sl6lod>

[^jrochkind1]: <https://news.ycombinator.com/item?id=49996473>

[^janalsncm-2]: <https://news.ycombinator.com/item?id=49999018>

[^dutc]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_iebiw4>

[^mtlynch-lobsters-3]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_3bfbyq>

[^mtlynch]: <https://news.ycombinator.com/item?id=49995689>

[^mtlynch-2]: <https://news.ycombinator.com/item?id=49998168>

[^dustfinger]: <https://news.ycombinator.com/item?id=49997303>

[^cyndunlop]: <https://news.ycombinator.com/item?id=49999012>

[^amw-zero]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_dsjrj8>

[^purplesyringa]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_d29ow6>

[^mtlynch-lobsters]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_qdhhsd>

[^kkapelon]: <https://news.ycombinator.com/item?id=49996262>

[^dieselgate]: <https://news.ycombinator.com/item?id=50000591>

[^layer8]: <https://news.ycombinator.com/item?id=49996737>

[^marginalia]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_g0jc4p>

[^legoktm]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_j0v9yt>

[^simonw]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_i2jmqx>

[^mexicocitinluez]: <https://news.ycombinator.com/item?id=49997005>

[^fanf]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_nxebu9>

[^toastal]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_5wcfr6>

[^ogou]: <https://news.ycombinator.com/item?id=50002051>

[^linsomniac]: <https://news.ycombinator.com/item?id=49995834>

[^phreack]: <https://news.ycombinator.com/item?id=49995310>

[^DonaldPShimoda]: <https://news.ycombinator.com/item?id=49995680>

[^layer8-2]: <https://news.ycombinator.com/item?id=49996554>

[^mtlynch-3]: <https://news.ycombinator.com/item?id=49995775>

[^mtlynch-lobsters-2]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_wppbgw>

[^braiamp]: <https://news.ycombinator.com/item?id=49997992>

[^0x20cowboy]: <https://news.ycombinator.com/item?id=49996510>

[^nsfmc]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_s6yrc3>

[^mcphage]: <https://news.ycombinator.com/item?id=49995043>

[^amycodes]: <https://lobste.rs/s/rwdufq/anti_patterns_software_blogging#c_1awz0n>
