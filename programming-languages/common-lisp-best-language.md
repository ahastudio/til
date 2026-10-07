# LLM 시대에 Common Lisp가 최고의 언어라는 주장

원문: [Why Common Lisp Is Now the Best Programming Language](https://www.vivienhenz.com/common-lisp)

HN 토론: <https://news.ycombinator.com/item?id=49973598> (278점, 377개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/dxqp7h/why_common_lisp_is_now_best_programming> (-1점, 4개 댓글)

GN 토론: <https://news.hada.io/topic?id=34876>

## 요약

Vivien Henz가 2026년 10월에 쓴 짧은 글이다.
글은 어떤 프로그래밍 언어가 다른 언어보다 낫다는 데 동의한다면 그중 하나는
최고여야 하며, 그것은 LLM이 코드를 쓰는 지금 특히 Common Lisp라는 문장으로
시작한다.

첫 번째 근거는 피드백 루프다.
LLM은 코드를 매우 빨리 쓰므로, 예전에는 느린 부분이던 코드 작성이 더 이상 병목이
아니고, 이제 느린 부분은 프로그램이 실제로 동작하는지 확인하는 일이다.
확인하려면 다시 빌드해야 하고 그것이 몇 분씩 걸릴 수 있으므로,
피드백 루프의 길이가 개발 속도를 정한다는 것이다.
저자는 Paul Graham의 What Made Lisp Different를 인용해 Common Lisp에는 읽기
시점, 컴파일 시점, 실행 시점의 구분이 사실상 없다고 말한다.
Common Lisp는 이미지 기반이라 프로그램이 메모리 안의 살아 있는 이미지이고,
함수의 새 버전이 아무것도 재시작하지 않고 바로 이전 버전을 대체한다.

두 번째 근거는 오류 처리다.
대부분의 언어에서는 오류가 나면 프로그램이 죽고,
LLM은 크래시 로그를 읽고 고친 뒤 프로그램을 다시 실행해야 한다.
Common Lisp에서는 프로그램이 죽지 않고 멈춘 채 전체 스택과 모든 변수를 담은
디버거를 연다.
LLM에게 그 디버거를 가리키면 고친 뒤 프로그램을 이어서 실행할 수 있다고 저자는
말하며, 자신이 아는 한 이 모든 것을 하는 주류 언어는 Common Lisp뿐이라고 적는다.

세 번째 근거는 매크로와 도메인 언어다.
Lisp에서는 `(+ 1 2)` 같은 코드가 곧 기호와 숫자로 된 리스트이고,
데이터를 다루는 도구가 그대로 코드를 다룬다.
매크로는 코드를 받아 새 코드를 돌려주는 함수이므로 언어 자체에 새 구문을 더할 수
있고, 그래서 Lisp에서는 문제 영역의 언어를 먼저 만들고 그 언어로 프로그램을
쓴다.
저자는 프로그램의 가치가 그 뒤에 있는 의견(opinion)에 있으며,
LLM 덕분에 사용자가 제품을 직접 고치는 세상이 오고 있다고 본다.
회사가 의견이 담긴 도메인 언어를 잘 만들어 두면 사용자가 그 위에 만드는 것도
회사의 의견에서 출발하므로 더 좋아진다는 것이다.
ERP를 예로 들어, 회사마다 조금씩 달라 결국 고쳐야 하는데 ERP가 자체 도메인
언어로 쓰여 있으면 LLM에게 그 언어로 변경을 요청하면 되고,
변경이 도메인 언어의 의견을 따르므로 제품을 깨지 않는다고 설명한다.

네 번째 근거는 간결함이다.
매크로로 반복되는 패턴을 언어의 일부로 만들 수 있으므로 프로그램이 클수록 차이가
커진다.
저자는 자신이 Common Lisp로 만든 앱이 Python 판보다 대략 6~7배 짧았다고 말한다.
코드가 짧으면 토큰이 줄어 개발비가 줄고,
프로그램의 더 많은 부분이 LLM의 컨텍스트 창에 들어간다.
LLM 버그의 상당수는 나머지를 보지 못한 채 한 부분만 바꾸는 데서 오므로,
전체를 볼 수 있으면 의도를 더 잘 파악한다는 것이다.

마지막으로 예상되는 반론에 답한다.
Common Lisp는 ANSI 표준이고 1994년 이후 바뀌지 않았는데,
저자는 이것을 장점으로 본다.
사용자가 제품을 고치는 ERP 같은 경우 밑의 언어가 움직이지 않으니 그 위에 만든
것이 깨지지 않는다는 것이다.
라이브러리가 부족하다는 반론에는, 주 패키지 관리자 Quicklisp에는 수천 개
프로젝트밖에 없고 npm에는 수백만 개가 있지만,
요즘 프로그램은 계속 침해당하는 패키지의 수백만 줄 코드에 기대고 있으며 LLM으로
필요한 부분을 직접 쓰거나 라이브러리를 통째로 옮기면 된다고 답한다.
개발자를 구하기 어렵다는 반론에는, 새로운 것을 잘 배우는 사람을 뽑으면 되니 코딩
면접에서 Common Lisp를 배우게 해 보라고 답한다.
글은 다음에 프로그램을 쓸 때는 Common Lisp를 쓰라는 문장으로 끝난다.

## 분석

### 글의 축은 피드백 루프와 의견, 두 개다

alexjurkiewicz는 글의 절반은 예외에서 재개할 수 있어서 Common Lisp가 좋다는
이야기이고, 나머지 절반은 DSL이 좋다는 이야기라고 정리했다[^alexjurkiewicz].
이 정리가 글의 구조를 정확히 짚는다.
첫 번째 축은 LLM이 코드를 빨리 쓰니 확인 루프가 병목이라는 주장이고,
두 번째 축은 LLM이 무엇이든 쓸 수 있으니 무엇을 쓸지 정하는 의견이 가치라는
주장이다.
두 축은 서로 다른 논거이며, Common Lisp가 둘 다에 답할 수 있다는 것이 글의 연결
고리다.

### 이미지와 조건 시스템이라는 오래된 특징을 다시 읽는다

글이 내세우는 이미지 기반 개발과 디버거 재개는 새로운 기능이 아니라 Lisp가 수십
년 동안 가져온 특징이다.
글은 이것을 사람의 생산성 도구가 아니라 에이전트의 루프를 짧게 만드는 장치로
다시 해석한다.
HN에서 clx75는 Clojure에서 비슷한 경험을 했다며, 에이전트 하네스 Pi의 확장으로 nREPL이 열린 JVM을 띄우고 에이전트가 아무 Clojure 폼이나 평가하게 했더니, 테스트 코드를 고치고 영향받은 네임스페이스만 다시 불러 테스트를 돌리는 흐름이 매우 빨라졌다고 적었다[^clx75].
varjag는 실제 운영 프로젝트 일부에서 Codex와 MCP로 Common Lisp 에이전트 개발을
하고 있으며, REPL 기반 개발이 더 빠르게 느껴지지만 측정해 본 적은 없다고
했다[^varjag].
REPL에 에이전트를 붙이는 흐름 자체는 실제로 쓰이고 있다.

### 언어 선택의 근거가 사람에서 에이전트로 옮겨 간다

글이 드는 근거는 모두 에이전트를 기준으로 한다.
토큰 비용, 컨텍스트 창, 크래시 로그를 읽는 횟수 같은 지표는 사람에게는 중요하지
않던 것들이다.
이 저장소의 `frontend/frameworks-still-matter.md`가 다룬 프레임워크 논쟁처럼,
언어 논쟁도 에이전트에게 무엇이 유리한가라는 질문으로 다시 열리고 있다.

## 비평

### 모든 언어의 팬이 같은 논리를 쓸 수 있다

kelnos는 누구나 자기가 좋아하는 언어가 LLM 덕분에 최고가 된 이유를 찾는다고
지적했다[^kelnos].
JavaScript와 Python은 학습 코드가 많아서,
Rust는 강한 타입 덕분에 컴파일러 피드백이 좋아서,
Go는 단순해서 최고라고 말할 수 있다는 것이다.
rspeele도 자기 주변에서는 예전에 좋아하던 언어가 에이전트 시대에도 완벽한
언어라고 합리화하기가 매우 쉽다는 것을 봤다고 적었다[^rspeele].
nickm12는 이 글이 어떤 언어가 정말 에이전트에 좋은지 평가한 사람의 글이 아니라,
Common Lisp가 좋은 이유를 찾는 팬의 글로 읽힌다고 했다[^nickm12].

글의 첫 문장도 이 문제를 드러낸다.
gorgoiler는 어떤 언어가 다른 언어보다 낫다고 해서 최고의 언어가 존재한다는
결론은 나오지 않으며, 부분 순서에는 최대 원소가 보장되지 않는다고
반박했다[^gorgoiler].
글을 올리고 토론에 응한 misterchocolat은 이 지적에 맞는 말이라며
인정했다[^misterchocolat].

### 측정 없이 결론으로 간다

Rochus는 글의 결론이 논거와 증거로 뒷받침되지 않으며,
빠른 재정의는 빠른 검증이 아니고, 디버거에 들어간다고 회복이 보장되지 않으며,
생성된 코드가 검증된 라이브러리가 되는 것도 아니라고 지적했다[^Rochus].
같은 논리라면 Smalltalk(특히 Pharo), Racket, Julia, Elixir,
심지어 Forth도 최고의 언어 후보가 될 수 있다는 것이다.
soltanov는 같은 에이전트에게 Common Lisp, Rust, Go, Python,
TypeScript로 같은 작업을 주고 토큰, 재시도, 실패, 동작하는 해법까지의 시간,
사람의 수정 횟수를 재 보라고 제안했다[^soltanov].

글이 내놓는 수치는 저자 자신의 앱이 Python 판보다 6~7배 짧았다는 경험
하나뿐이다.
짧은 코드가 토큰을 줄인다는 주장에도 onion2k는 반론을 냈다.
필요한 것은 LLM이 가장 적은 토큰으로 변경할 만큼 맥락을 이해하는 것이지,
코드 전체가 짧은 것이 아니라는 것이다[^onion2k].

### LLM이 Lisp를 잘 다룬다는 전제가 흔들린다

글은 LLM이 Common Lisp 코드를 잘 쓴다고 전제한다.
그러나 사용자 경험은 엇갈린다.
peri-cl은 매크로를 쓰는 매크로 수준에서 LLM이 크게 망가지는 것을 봤으며,
최신 모델이 단순한 매크로 하나에 혼란을 일으켜 `(let (((`처럼 있을 수 없는 괄호
수로 펼쳐지는 코드를 만들었다고 적었다[^peri-cl].
Lobste.rs에서 xjix는 LLM이 괄호 균형에서 막히는 일이 잦아 괄호 균형과 parinfer 도구를 직접 만들어야 했고, 그래도 Lisp에 대한 기억이 약해 매번 문서를 다시 읽는다고 했다[^xjix].
반대로 Clojure 사용자 jwr는 최근 모델은 덜 쓰이는 언어도 잘 다룬다고
답했고[^jwr], icey는 LLM에게 매크로는 쓰게 하지 않는다며 자신이 추론하기 어려울
만큼 불투명해지기 때문이라고 했다[^icey].
글이 장점으로 내세우는 매크로가 바로 LLM과 사람 모두에게 가장 다루기 어려운
부분이라는 점은 글이 다루지 않는다.

### 디버거 재개와 이미지는 다른 언어에도 있거나 오히려 위험하다

alexjurkiewicz는 Python과 Node도 핵심 도구로 스택을 풀지 않고 예외 지점에서 멈출
수 있다고 지적했다[^alexjurkiewicz].
baq는 대부분의 언어에 없는 것은 진짜 네이티브 핫 리로드이며,
Python은 동적인 언어인데도 그것을 하지 못한다고 답했다[^baq].
marviter는 Common Lisp가 개발 도구 없이도 조건 시스템과 평가·컴파일 규칙으로 이
기능을 언어 차원에서 제공한다고 덧붙였다[^marviter].
즉 디버거 재개는 Common Lisp만의 기능은 아니지만,
언어에 내장되어 있다는 점은 실제 차이다.

이미지 기반 개발에는 다른 걱정도 있다.
maxiepoo는 이미지에 코드에 드러나지 않는 암묵적 상태가 많이 쌓이므로,
프로그램 텍스트로 시스템 상태를 재현하기 어렵다는 점이 LLM과 일할 때 큰
단점이라고 봤다[^maxiepoo].
pfdietz는 Common Lisp가 꼭 이미지 기반은 아니며,
보통은 파일의 코드를 실행 중인 이미지에 컴파일해 올리고 파일을 고쳐 다시
컴파일한다고 반박했다[^pfdietz].
글이 Common Lisp를 이미지 기반이라고 단정한 것은 실제 사용 방식보다 단순화된
설명인 셈이다.

### 글 자체의 출처가 의심받았다

HN과 Lobste.rs 모두에서 이 글이 Claude로 쓰였다는 지적이 나왔다.
davexunit은 저자 저장소의 커밋 기록을 근거로 이 글이 Claude가 쓴 글이라고
했고[^davexunit], Lobste.rs의 flockofbirbs도 같은 커밋 기록을 근거로 슬롭이라고
했다[^flockofbirbs].
crocidb는 커밋 기록상 Claude로 작성된 것은 맞지만 AI 탐지기 Pangram 4.0은 100%
사람이 쓴 글로 판정했다며, 저자가 직접 쓴 글을 Claude로 Markdown 파일로 만들었을
수도 있다고 조심스럽게 봤다[^crocidb].
글의 저자가 누구인지는 이 문서에서 확인할 수 없지만,
LLM이 쓴 코드를 다루는 언어 선택을 주장하는 글이 LLM으로 쓰였다는 의심을 받은
것은 이 논쟁의 분위기를 보여 준다.

## 인사이트

### 언어보다 루프 설계가 에이전트의 속도를 정한다

글의 첫 번째 축에서 가장 쓸모 있는 부분은 Common Lisp가 아니라 피드백 루프라는
관점이다.
clx75의 Clojure nREPL 사례처럼, 에이전트가 실행 중인 프로세스에 코드를 평가하고
영향받은 부분만 다시 불러 테스트하게 만드는 일은 언어보다 하네스의 설계에 달려
있다.
같은 구조는 Python의 IPython 커널, Elixir의 IEx,
Smalltalk 이미지에도 만들 수 있다.
에이전트 개발 환경을 고를 때 물어야 할 질문은 어떤 언어인가보다,
수정에서 확인까지 몇 초가 걸리고 상태를 얼마나 쉽게 재현할 수 있는가다.
그리고 maxiepoo가 지적한 대로, 루프가 빠를수록 실행 중인 상태와 파일의 상태가
어긋날 위험도 커진다.

### 도메인 언어는 사용자 커스터마이즈 시대의 해자가 될 수 있다

글의 두 번째 축, 즉 의견을 담은 도메인 언어가 가치라는 주장은 언어 논쟁과 떼어
놓아도 성립한다.
LLM으로 사용자가 제품을 직접 고치는 시대가 온다면,
제품 회사가 지켜야 할 것은 코드 자체보다 그 코드가 따라야 할 규칙과 어휘다.
이는 과거 Emacs Lisp, AutoLISP, Excel의 수식처럼 제품이 사용자에게 작은 언어를
내주었을 때 생태계가 커졌던 역사와 같은 구조다.
misterchocolat이 HN에서 LLM이 DSL 없이도 일할 수 있다는 지적에 동의하면서도,
DSL은 제품을 만든 사람의 의견을 담는다고 답한 대목이 이 주장의
핵심이다[^misterchocolat-dsl].
다만 WalterBright가 지적했듯 매크로로 만든 언어는 쉽게 각자의 문서 없는 언어가
되므로[^WalterBright], 의견을 담은 언어를 만드는 일은 그 언어를 문서화하고
안정적으로 유지하는 비용과 함께 온다.

### 동결된 표준은 에이전트 시대에 새로운 가치를 얻는다

Lobste.rs의 k749gtnc9l3w는 수십 년 동안 업데이트 없이 코드가 동작할 만큼 언어가 굳어 있다는 점을 글 중간의 곁가지가 아니라 첫 번째 장점으로 올렸어야 한다고 평가했다[^k749gtnc9l3w].
LLM이 학습한 지식은 특정 시점에 고정되고,
빠르게 바뀌는 언어와 라이브러리일수록 모델의 지식이 낡는다.
1994년 이후 바뀌지 않은 표준은 모델이 배운 것이 지금도 맞다는 것을 보장한다.
이 관점에서는 생태계가 작다는 약점과 표준이 멈춰 있다는 특징이 서로를 보완한다.
에이전트가 코드를 쓰는 시대에는 언어의 혁신 속도보다 모델의 지식과 현실이
어긋나지 않는 안정성이 더 중요한 품질이 될 수 있다.

---

[^alexjurkiewicz]: <https://news.ycombinator.com/item?id=49974354>

[^clx75]: <https://news.ycombinator.com/item?id=49974701>

[^varjag]: <https://news.ycombinator.com/item?id=49974822>

[^kelnos]: <https://news.ycombinator.com/item?id=49974799>

[^rspeele]: <https://news.ycombinator.com/item?id=49974402>

[^nickm12]: <https://news.ycombinator.com/item?id=49974481>

[^gorgoiler]: <https://news.ycombinator.com/item?id=49974248>

[^misterchocolat]: <https://news.ycombinator.com/item?id=49974300>

[^Rochus]: <https://news.ycombinator.com/item?id=49977371>

[^soltanov]: <https://news.ycombinator.com/item?id=49975625>

[^onion2k]: <https://news.ycombinator.com/item?id=49974564>

[^peri-cl]: <https://news.ycombinator.com/item?id=49974907>

[^xjix]: <https://lobste.rs/s/dxqp7h/why_common_lisp_is_now_best_programming#c_kckvxb>

[^jwr]: <https://news.ycombinator.com/item?id=49975913>

[^icey]: <https://news.ycombinator.com/item?id=49979760>

[^baq]: <https://news.ycombinator.com/item?id=49974510>

[^marviter]: <https://news.ycombinator.com/item?id=49974438>

[^maxiepoo]: <https://news.ycombinator.com/item?id=49978055>

[^pfdietz]: <https://news.ycombinator.com/item?id=49978444>

[^davexunit]: <https://news.ycombinator.com/item?id=49978174>

[^flockofbirbs]: <https://lobste.rs/s/dxqp7h/why_common_lisp_is_now_best_programming#c_pbvj9r>

[^crocidb]: <https://lobste.rs/s/dxqp7h/why_common_lisp_is_now_best_programming#c_hhlpwo>

[^misterchocolat-dsl]: <https://news.ycombinator.com/item?id=49974137>

[^WalterBright]: <https://news.ycombinator.com/item?id=49974858>

[^k749gtnc9l3w]: <https://lobste.rs/s/dxqp7h/why_common_lisp_is_now_best_programming#c_yhdpiw>
