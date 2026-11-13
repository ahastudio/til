# 복잡성이라는 단 하나의 적을 두고 모든 조언을 짠 풍자 에세이 Grug Brained Developer는 단순함을 개발자의 한계에 맞춘 규율로 만든다

원문: [The Grug Brained Developer](https://grugbrain.dev/)

HN 토론: <https://news.ycombinator.com/item?id=44303542> (1087점, 578개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/ifaar4/grug_brained_developer>

## 요약

htmx를 만든 Carson Gross가 쓴 에세이이다.
페이지에는 날짜가 없고, HN에는 2022년 6월 22일에 처음 올라왔다.
글쓴이는 스스로를 머리 작은 개발자(grug brain developer)라고 부르며 오래 프로그램을
짜며 배운 것을 짧고 우스운 글로 모았다고 소개한다.
문체는 일부러 원시인 말투이고, 똑똑하다고 자처하는 개발자들이 눈살을 찌푸릴 것을 알면서도
쓴다고 밝힌다.
저자는 HN 스레드에 직접 나타나 같은 내용에 색인을 더한 종이책이 있다고 알렸다.[^author-book]

중심 주장은 단순하다.
개발자의 천적은 복잡성이고, 코드베이스에 복잡성이 들어오는 순간 하나를 고치면 관계없는
다른 것이 깨지는 상태가 된다고 한다.
복잡성은 눈에 보이지 않고 존재만 느껴진다는 것이 비유의 요지이다.
이 하나의 적을 두고 글은 주제별로 대응책을 늘어놓는다.

- 아니오라고 말하기: 가장 좋은 무기는 기능이나 추상화를 만들지 않겠다고 말하는 것이다.
  이것은 좋은 엔지니어링 조언이지만 출세에는 나쁜 조언이라고 스스로 인정한다.
- 어쩔 수 없을 때 좋다고 말하기: 요구의 80%를 20%의 코드로 푸는 방안을 찾는다.
  PM에게 굳이 알리지 않고 그렇게 하는 편이 나을 때가 있다고까지 쓴다.
- 코드 나누기(factoring): 프로젝트 초기에는 모양이 물처럼 흐릿하므로 서둘러 나누지 않고,
  시스템의 모양이 잡히면 좁은 인터페이스를 가진 절단점이 드러난다.
  절단점은 복잡성의 악령을 수정에 가둔 것처럼 안에 가둔다.
  초기에 추상화를 쏟아내는 큰 머리의 개발자는 UML 그림이나 내일까지의 동작하는 데모로
  현실에 붙들어 둔다.
- 테스트: 코드가 굳어 가는 프로토타입 뒤에 쓴다.
  먼저 쓰는 테스트는 싫어한다.
  단위 테스트는 구현이 바뀌면 깨지고, 종단간(E2E) 테스트는 깨졌을 때 이유를 알기
  어려워 결국 무시당한다.
  가장 좋은 지점은 중간의 통합 테스트이고, 잘 가꾼 소수의 E2E를 곁들이며,
  목(mock)은 거의 안 쓴다.
  예외는 버그를 찾았을 때이다.
  그때는 재현하는 회귀 테스트를 먼저 쓰고 고친다.
- 애자일은 나쁘지 않지만 애자일 샤먼이 위험하다.
  실패하면 제대로 안 했다고 말하는 것이 편리하기 때문이다.
- 리팩터링: 클수록 실패하므로 작게, 시스템이 계속 돌아가는 상태로 한다.
  J2EE와 OSGi가 추상화를 늘려 오히려 복잡성을 키운 사례로 나온다.
- 체스터턴의 울타리(Chesterton's fence): 왜 있는지 모르는 울타리는 치우지 않는다.
  테스트가 이 울타리의 이유를 알려 주는 힌트가 되곤 한다.
- 마이크로서비스: 가장 어려운 문제인 시스템 분할에 네트워크 호출까지 더하는 것이 이해되지
  않는다고 한다.
- 도구: 좋은 디버거를 가장 값진 도구로 꼽고 새 프로그래머가 깊이 배울 것을 권한다.
  IDE 코드 완성은 API를 외우지 않게 해 준다.
- 타입 시스템: 점을 찍으면 쓸 수 있는 것이 뜨는 것이 가치의 90% 이상이고,
  정합성은 부수적이다.
  제네릭은 컨테이너 정도로 한정하고, 타입 위주의 추상은 위험하다.
- 표현식 복잡도: 한 줄로 줄이는 대신 의미 있는 이름의 중간 변수를 두면 디버깅이 쉽다.
- DRY: 균형이 필요하며 단순하고 뻔한 반복은 복잡한 콜백이나 객체 모델보다 낫기도 하다.
- 관심사 분리(SoC)와 locality of behavior(LoB): 일을 하는 그 자리에 코드를 둔다.
- 클로저, 로깅, 동시성, 최적화, API: 클로저는 소금처럼 쓴다.
  로깅은 분기마다 남기고, 요청 ID를 모든 로그에 붙이고, 로그 수준을 동적으로 바꾸고,
  가능하면 사용자별로 조절한다.
  동시성은 상태 없는 웹 요청 처리기나 서로 의존하지 않는 작업 큐 같은 단순한 모델에 기댄다.
  최적화는 구체적인 프로파일을 본 뒤에 하고 네트워크가 CPU보다 흔한 병목이라고 한다.
  API는 단순한 경우를 단순하게, 복잡한 경우도 가능하게 층을 나눈다.
- 파싱은 재귀 하향이 가장 재미있고 실제 프로덕션 파서의 거의 전부라고 하며,
  Bob Nystrom의 Crafting Interpreters를 추천한다.
  방문자(visitor) 패턴에는 나쁘다는 한 줄만 쓴다.
- 프런트엔드: SPA와 GraphQL JSON API로 나누면 복잡성의 소굴이 둘이 된다고 보고,
  htmx와 hyperscript를 만든 이유로 든다.
  React는 일자리에는 낫지만 복잡성의 신도가 된다고 덧붙인다.
- 유행은 소금 한 줌으로 받아들인다.
- 바보처럼 보일까 하는 두려움(FOLD)과 사기꾼 증후군: 시니어가 공개적으로 이것은 나에게 너무
  복잡하다고 말하면 주니어가 따라 말할 수 있다.
  모두가 사기꾼이면 아무도 사기꾼이 아니다.

## 분석

### 중심 주장은 복잡성이 단 하나의 적이고 나머지 조언은 그 예산 관리라는 것이다

가장 강하게 말하면 이 에세이의 모든 항목은 같은 질문을 다른 자리에서 묻는다.
이 변경이 복잡성을 늘리는가.
아니오라고 말하기, 80/20, 늦은 분할, 작은 리팩터링, 반복 허용, 중간 변수, 단순한 동시성 모델은
모두 복잡성을 들이지 않는 방법이고,
테스트, 로깅, 디버거, 코드 완성은 이미 들어온 복잡성 속에서 길을 잃지 않는 방법이다.
이 구조 덕분에 흩어진 조언이 한 원리로 묶인다.
HN의 GMoromisato는 복잡성을 도입하는 가장 흔한 이유가 나중에 시간을 아껴 줄 것이라는
믿음이라고 했고 DRY가 성급한 추상화로 이어지는 경우를 들었다.[^gmoromisato]
저자 본인도 스레드에서 같은 점을 말했다.
복잡성은 엔지니어가 정당화하기 쉬운 것이어서, 필요한 복잡성도 기능을 거절하면 줄일 수
있다는 것이다.[^author-complexity]

### 단순함의 기준은 개발자의 한계이다

원시인 문체는 장난만이 아니라 논거이다.
머리가 작다는 설정이 곧 인간의 작업 기억이 제한되어 있다는 전제이고, 그래서 점을 찍으면
목록이 뜨는 것, 이름 붙은 중간 변수, 한 군데에 모인 동작 같은 것이 가치가 된다.
디버깅이 쉬운가, 한눈에 읽히는가가 판단 기준이다.
HN에서 PaulHoule은 지능을 한정된 자원으로 여기면 도구와 절차와 설계에 낭비하지 않게 된다고
요약했고, dgb23은 이 글이 더 정교한 것을 할 수 있는 사람이 경험에 따라 그러지 않기로 한
것이라서 가치가 있다고 했다.[^paulhoule][^dgb23]
ahartmetz는 추상화가 정당한 때를 특별한 강의 없이도 코드가 더 쉬워질 때라고 표현했다.[^ahartmetz]

### 조언은 측정이 아니라 경험담이고 문체가 설득을 맡는다

글의 근거는 저자의 오랜 경험이다.
J2EE와 OSGi의 실패, 단위 테스트에 대한 인상, 리팩터링이 클수록 실패한다는 관찰은 모두
수치나 표본 없이 제시된다.
글쓴이 스스로 왜 어떤 리팩터링은 성공하고 어떤 것은 실패하는지 잘 모르겠다고 적는다.
이 글이 힘을 갖는 것은 증명이 아니라 유머와 반복이다.
FOLD를 다루는 절은 이 점을 드러낸다.
공개적으로 너무 복잡하다고 말해도 된다는 허락이 글의 가장 실용적인 처방이고,
그 처방은 증거가 아니라 문화에 관한 것이다.

## 비평

### 복잡성의 정의가 없어서 어떤 것이든 복잡성이라고 부를 수 있다

HN에서 가장 되풀이된 반론은 정의 문제이다.
osigurdson은 복잡성이 무엇인지에 대한 공통 이해가 없어서 나쁨의 동의어로 정신적 방화벽을
통과한다고 했고, 프로젝트에 파일이 여러 개인 것이 복잡한 것이냐고 물었다.[^osigurdson]
0xbadcafebee는 복잡성은 고려할 것이 많다는 뜻일 뿐이고 쓸모 있고 필요하면 나쁘지 않으니
복잡성이 나쁘다는 신화를 퍼뜨리지 말라고 했다.[^badcafebee]
Jean-Papoulos는 복잡성은 좋고 복잡한 것(complicated)이 나쁘다고 했고,
저자는 필요한 복잡성과 아닌 것의 구분이 개발자 대부분에게(어쩌면 당신에게도) 매우
어렵다고 답했다.[^jean-papoulos][^author-diff]
sesm은 Rich Hickey가 말한 complect(얽음)를 가져와, 복잡성이 나쁘다고는 동의하지 않고
필요한 것들은 서로 엮여야 문제가 풀린다고 했다.[^sesm]
저자는 0xbadcafebee에게 좋은 지적이지만 복잡성은 나쁘다고만 답했다.[^author-bad]
이 답은 농담이지만 정의 없이 규율로 쓰이는 약점을 드러낸다.
저자가 필요한 복잡성과 불필요한 복잡성을 구분하기 어렵다고 인정한 것이 구체적인 답에
가깝다.
Lobste.rs에서도 adam_d_ruppe가 이 글이 복잡성이라는 단어의 정의가 있으면 크게 나아질 것이라고
했다.[^adam-d-ruppe]
이 문서는 이 구분을 돕는 기준을 아래 인사이트에 제안한다.

### 디버거 찬양이 모든 환경에 맞지는 않는다

글은 좋은 디버거를 가장 값진 도구로 꼽는다.
titanomachy는 작은 스타트업과 대형 기술 회사에서 일했지만 팀에서 디버거를 쓰는 사람은
자신뿐이었고 모두 출력문 디버깅을 하더라고 했다.[^titanomachy]
roncesvalles는 마이크로서비스 메시 구조에서는 로컬에서 아무것도 돌릴 수 없어 디버거가
선택지가 아니었다고 했고, demosthanos는 Kernighan과 Pike가 디버거를 스택 추적과 값 확인
이상으로는 쓰지 않는다고 했다는 오래된 논의를 가리켰다.[^roncesvalles][^demosthanos]
r-bryan은 둘 중 하나가 아니라 둘 다 가치 있다고 했고, 저자는 글이 디버거와 로깅을 모두
중요한 도구로 다룬다고 답했다.[^r-bryan][^author-debug]
글의 주장과 환경의 현실 사이의 간격은 디버거가 맞고 틀리고의 문제가 아니라, 글이 가정하는
개발 환경(로컬에서 돌아가는 시스템)이 모두에게 주어지지 않는다는 점에 있다.

### 프런트엔드 조언에는 저자의 이해관계가 걸려 있다

글은 SPA와 GraphQL을 복잡성의 소굴로 보고 htmx와 hyperscript를 만든 이유로 든다.
저자는 이 점을 숨기지 않는다.
htmx를 만들었다고 직접 쓰고 일자리 공고는 없다고 덧붙인다.
그래도 평가는 갈렸다.
toastercat는 글이 현대 프런트엔드에 편향되어 있고 htmx도 한 형태의 복잡성을 다른 형태로
바꿀 뿐이라고 했다.[^toastercat]
brushfoot는 부트스트랩 B2B SaaS에서 상호작용이 필요한 섬에만 htmx를 뿌려 잘 맞았다고
했다.[^brushfoot]
저자는 deadbabe의 htmx가 밈 아니냐는 물음에 htmx sucks라는 htmx 공식 에세이 링크로
답했다.[^deadbabe][^author-htmx]
이 문서는 이 에세이의 프런트엔드 부분을 저자가 만든 도구를 변호하는 글로 읽는 것이
안전하다고 본다.

### 개인의 두뇌 차이와 조직의 지식 문제를 비켜 간다

magarnicle는 자신이 그루그형 두뇌가 아니라 세부를 잘 기억하므로 복잡성이 앱에 더 많은
기능을 주면 감수하겠다고 했다.[^magarnicle]
pixelatedindex는 미래에 어떻게 돌아가는지를 아는 것은 주석이나 문서로 해결해야 하고,
큰 조직에서는 구전 지식이 보이지 않는 티렉스라고 답했다.[^pixelatedindex]
이 대화는 글의 전제(내 기억은 믿을 수 없다)가 팀 단위에서는 더 강하게 작동한다는 점을
보여 준다.
글이 자기 한계를 인정하는 데서 출발하지만 그 한계를 조직의 문서화 규율로 옮기는 부분은
얇다.

### 80/20을 알리지 않고 하라는 조언은 신뢰를 갉는다

글은 PM에게 굳이 말하지 않고 80/20 방식으로 짜는 편이 나을 때가 있다고 쓴다.
농담의 어조이지만 조직에서 그대로 따르면 요구와 구현의 불일치가 늦게 드러난다.
복잡성을 줄이는 목표는 옳아도 방법은 투명성과 충돌한다.
이 문서는 이 조언을 줄여서 따르려면 무엇을 덜어 냈는지 PR이나 설계 메모에 적는 것을 권한다.

### 문체는 설득이자 진입 장벽이다

ChrisArchitect는 좋은 점이 있을 수 있지만 읽기가 너무 어렵다고 했고,
_shantaram은 번역 페이지를 가리켰다.[^chrisarchitect][^shantaram]
anthomtb는 문법이 틀리지만 간결한 문장이 큰 머리를 물러나게 하고 작은 머리가 단어를
천천히 흡수하게 한다고 했고, idlewords는 문체가 에세이의 가장 매력적인 부분이라고
했다.[^anthomtb][^idlewords]
chuckadams는 말장난이 너무 길게 이어져 지친다고 했고 저자는 환불해 주겠다고 답했다.[^chuckadams][^author-refund]
hmartin은 Claude에게 읽기 쉬운 영어로 다시 쓰게 하고 다른 관점의 링크를 붙였다.[^hmartin]
문체가 기억에 남게 하는 대가로 읽기 비용을 올린다는 균형은 이 글이 의식적으로 택한 것이다.

### 반론: 타입 시스템과 작게 쪼개기가 복잡성을 줄이기도 한다

Lobste.rs에서는 타입 절에 대한 반론이 나왔다.
inactive-user는 복잡성의 위험을 길게 말하면서 타입 시스템 절이 타입이 코드를 크게 단순하게
만드는 방식을 무시한다고 했다.[^inactive-user]
Loup-Vaillant는 이 글이 거의 이해한 것이 타입 시스템의 큰 이득이 피드백 고리를 조이는
것이라는 점이며, 자동 완성은 이름을 생각하기도 전에 맞게 쓰게 하고 정적 타입은 테스트보다
앞서 컴파일 시점에 오류를 잡고 합 타입은 잘못된 상태를 표현할 수 없게 한다고 했다.[^loup-types]
FeepingCreature는 불변 도메인 타입과 순수 함수가 이 글에서 덜 강조된 힘이라고 했다.[^feepingcreature]
글은 타입의 가치를 점을 찍을 때 뜨는 목록에 거의 한정하고 제네릭은 경계하는데,
이 반론들은 타입이 복잡성을 줄이는 도구이기도 하다고 본다.

쪼개기에 대해서도 다른 시각이 있었다.
lproven은 이 글이 널리 오해되고 있다고 하면서 작은 프로그램이 많은 편이 낫다고 했고,
sjamaan은 지나치게 작은 프로그램을 합치면 복잡성이 접착제(glue)로 옮겨 가서 디버깅이
더 어려울 수 있다고 했다.[^lproven][^sjamaan]
duncan_bayne는 복잡한 문제일수록 단순한 사고로 접근해야 하고 유닉스 파이프 조합이 그
예라고 했다.[^duncan-pipes]
글의 마이크로서비스 한 줄과 체스터턴의 울타리 절이 바로 이어지는 것을 quad는 아이러니라고
느꼈다.[^quad]
Loup-Vaillant는 Casey Muratori가 말한 의미 압축(semantic compression)과 글의 늦은 분할이
같은 이야기라고 했다.
시작은 어리석게, 패턴이 보일 때만 나눈다는 것이다.[^loup-factor]

### 반응: 프런트엔드와 FOLD

badtuple은 프런트엔드 개발이 유행을 좇는다는 비판이 정확하지만 기술 부족이나 수치의
문제가 아니라고 했다.
브라우저와 기기와 해상도 호환성은 단순히 해결하기에는 복잡하고 문제가 아직 풀리지 않아서
변화가 많다는 것이다.
그는 htmx를 선호하고 두 프로젝트에서 쓰지만 같은 정도로 유효한 접근이 여럿이라고 했다.[^badtuple]
thev는 시니어가 공개적으로 너무 복잡하다고 말하는 것이 좋다는 글을 읽고 이것을 더 자주
말하는 연습을 하겠다고 했고, icefox는 첫 줄에서 싫었다가 다섯 줄 뒤에 사랑하게 되어
신입 필독서로 만들겠다고 했다.[^thev][^icefox]

## 인사이트

### 팀의 어휘로 쓰려면 리뷰 질문으로 바꾼다

이 에세이는 어휘가 힘이다.
이 문서의 제안은 PR 리뷰에 그루그형 질문 다섯 개를 두는 것이다.
이 변경이 새 추상화를 만드는가, 만든다면 인터페이스가 좁은가(좁은 절단점).
지금 나누는 것이 너무 이른가.
동작하는 데모나 재현 테스트가 있는가.
내가 이해하지 못하는 부분이 있는가(FOLD를 허용하는 질문).
무엇을 덜어 냈는가(80/20을 알리는 질문).
이 다섯 개는 에세이의 항목을 바꾼 이 문서의 제안이고 에세이가 정한 체크리스트는 아니다.

### 필요한 복잡성과 불필요한 복잡성을 가르는 기준을 둔다

정의 문제의 실용적 해법으로 이 문서는 세 가지 질문을 제안한다.
이 복잡성을 없애면 사용자가 보는 동작이 달라지는가.
없애면 어떤 요구가 깨지는지를 한 문장으로 말할 수 있는가.
이 복잡성이 한 곳에 갇혀 있는가, 아니면 여러 모듈에 번지는가.
앞의 두 질문에 답하지 못하면 불필요한 복잡성일 가능성이 높고,
세 번째는 에세이의 좁은 인터페이스 기준이다.
이 기준은 이 문서의 제안이다.

### 에이전트 시대에는 복잡성을 들이는 비용이 더 낮아진다

tartoran는 이 글이 LLM 시대에 맞게 개정되어야 한다고 했다.[^tartoran]
tptacek는 경험상 LLM 에이전트는 상당히 그루그 두뇌적이라고 했고,
ethan_smith는 LLM이 단순하고 일관된 패턴에서 가장 잘 일하며 사람을 혼란스럽게 하는 복잡성
악령에 같이 시달린다고 했다.[^tptacek][^ethan-smith]
dgb23은 일관되고 평범한 코드에서 AI 보조가 더 효과적이라고 했다.[^dgb23]
mcqueenjordan은 이 에세이를 LLM에게 먹이고 그루그 개발자 페르소나로 현재 문제에 의견을
내게 하는데 스트레스 해소가 된다고 했다.[^mcqueenjordan]
이 문서의 제안은 에이전트 지침 파일에 이 에세이의 규칙 몇 개를 바꿔 넣는 것이다.
새 추상화를 도입하지 말고 필요한 위치에 반복을 허용하고, 리팩터링은 작게 하고 시스템이
계속 돌아가게 하고, 버그에는 재현 테스트를 먼저 쓰고, 큰 변경은 이유를 적게 하는 것이다.
이 문구는 이 문서의 제안이고 에세이나 댓글이 제시한 것이 아니다.

### 글의 주장을 확인할 관찰

에세이의 가장 검증 가능한 주장은 리팩터링이 클수록 실패한다는 것이다.
팀의 저장소에서 리팩터링 PR의 크기(변경 줄 수나 파일 수)와 되돌림 또는 후속 결함의 비율을
함께 보면 이 관찰을 확인할 수 있다.
크기가 커질수록 실패가 늘면 글의 직관이 지지되고, 크기와 무관하면 실패의 원인은 다른 곳에
있다는 뜻이다.
이 비교는 이 문서의 제안이고 글이 제시한 것이 아니다.

---

[^author-book]: <https://news.ycombinator.com/item?id=44304928>

[^gmoromisato]: <https://news.ycombinator.com/item?id=44304940>

[^author-complexity]: <https://news.ycombinator.com/item?id=44309892>

[^paulhoule]: <https://news.ycombinator.com/item?id=44303560>

[^dgb23]: <https://news.ycombinator.com/item?id=44304509>

[^ahartmetz]: <https://news.ycombinator.com/item?id=44304924>

[^osigurdson]: <https://news.ycombinator.com/item?id=44309840>

[^badcafebee]: <https://news.ycombinator.com/item?id=44310148>

[^jean-papoulos]: <https://news.ycombinator.com/item?id=44307538>

[^author-diff]: <https://news.ycombinator.com/item?id=44309999>

[^sesm]: <https://news.ycombinator.com/item?id=44312989>

[^author-bad]: <https://news.ycombinator.com/item?id=44311205>

[^titanomachy]: <https://news.ycombinator.com/item?id=44305194>

[^roncesvalles]: <https://news.ycombinator.com/item?id=44305375>

[^demosthanos]: <https://news.ycombinator.com/item?id=44305400>

[^r-bryan]: <https://news.ycombinator.com/item?id=44306848>

[^author-debug]: <https://news.ycombinator.com/item?id=44310010>

[^toastercat]: <https://news.ycombinator.com/item?id=44312665>

[^brushfoot]: <https://news.ycombinator.com/item?id=44304200>

[^deadbabe]: <https://news.ycombinator.com/item?id=44304044>

[^author-htmx]: <https://news.ycombinator.com/item?id=44304068>

[^magarnicle]: <https://news.ycombinator.com/item?id=44304941>

[^pixelatedindex]: <https://news.ycombinator.com/item?id=44305082>

[^chrisarchitect]: <https://news.ycombinator.com/item?id=44303809>

[^shantaram]: <https://news.ycombinator.com/item?id=44303896>

[^anthomtb]: <https://news.ycombinator.com/item?id=44303966>

[^idlewords]: <https://news.ycombinator.com/item?id=44303999>

[^chuckadams]: <https://news.ycombinator.com/item?id=44306819>

[^author-refund]: <https://news.ycombinator.com/item?id=44310008>

[^hmartin]: <https://news.ycombinator.com/item?id=44311681>

[^tartoran]: <https://news.ycombinator.com/item?id=44304307>

[^tptacek]: <https://news.ycombinator.com/item?id=44304357>

[^ethan-smith]: <https://news.ycombinator.com/item?id=44305892>

[^mcqueenjordan]: <https://news.ycombinator.com/item?id=44306070>

[^adam-d-ruppe]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_s3gcnd>

[^inactive-user]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_z22tmh>

[^loup-types]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_zsjxnx>

[^feepingcreature]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_2oaiel>

[^lproven]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_jxv0ln>

[^sjamaan]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_tguwub>

[^duncan-pipes]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_vi7ory>

[^loup-factor]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_itugdl>

[^badtuple]: <https://lobste.rs/s/ifaar4/grug_brained_developer#c_rpybgl>

[^quad]: <https://lobste.rs/s/pmpc9v/grug_brained_developer#c_voq4pz>

[^thev]: <https://lobste.rs/s/pmpc9v/grug_brained_developer#c_uvn3i4>

[^icefox]: <https://lobste.rs/s/pmpc9v/grug_brained_developer#c_xvdmpt>
