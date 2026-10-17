# Torvalds: “X에 AI를 쓰지 말라”는 규칙은 어리석다

원문: [Re: \[PATCH\] docs: remove Assisted-by references - Linus Torvalds](https://lore.kernel.org/lkml/CAHk-=whTs09_ozN+e09GU68N1wPP56MUzDjrg9rnKxQUa0A_4Q@mail.gmail.com/)

HN 토론: <https://news.ycombinator.com/item?id=50113790> (18점, 7개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel> (85점, 149개 댓글)

GN 토론: <https://news.hada.io/topic?id=35504>

## 요약

2026년 10월 9일 Sasha Levin은 리눅스 커널 문서에서
`Assisted-by` 태그를 요구하는 내용을 지우는 패치를 올렸다.
메인테이너 서밋에서 이 태그를 폐기하기로 합의했다는 것이다.
패치는 `coding-assistants.rst`, `submitting-patches.rst`와 그 이탈리아어 번역,
`checkpatch.pl`에서 모두 51줄을 지운다.[^levin]
The Register에 따르면 이 태그는 패치를 만들 때 고급 코딩 도구를 썼다면
커밋 메시지에 밝히라는 요구로,
2025년 7월에 제안되어 2026년 1월 공식 문서에 들어갔다.[^register]
Greg Kroah-Hartman은 패치에 동의하면서도 정책 변경이니
논의와 합의를 변경 기록에 더 설명해야 한다고 했다.[^gregkh]

스레드에서 Laurent Pinchart는 태그를 지키자는 쪽이었다.
Kees Cook이 커밋 메시지를 손으로 쓰라는 요구도 `Assisted-by`만큼 강제할 수
없다고 하자,[^kees-unenforceable]
Pinchart는 Signed-off-by도 강제할 수 없고 커널의 요구 대부분이 그렇다며,
이것은 우리가 무엇을 원하고 원하지 않는지 기대를 정하는 문제라고 답했다.
속이는 사람은 늘 있었고 앞으로도 그들의 기여를 거부할 것이며,
100% 정확성을 목표로 한 적은 없다는 것이다.[^pinchart]

10월 13일 Linus Torvalds가 이 메일에 답했다.
그는 Pinchart가 말하는 것은 기대가 아니라 그의 집착이라고 받아치고,
“X에 AI를 쓰지 말라”는 개념 자체를 이해할 수 없다고 했다.
그리고 새 규칙을 제안했다.
커널 패치에 컴파일러를 쓰지 말 것.
어셈블리로 써서 기계가 실제로 무엇을 하는지 이해한다는 것을 보이지 못하면
기여를 보고 싶지 않다는 것이다.
커밋 메시지를 쓸 때 편집기도 쓰지 말 것.
백스페이스로 실수를 숨기기 쉬운 도구 없이 좋은 커밋 메시지를 쓸 수 있음을 보여야
한다는 것이다.
그는 이런 규칙이 얼마나 어리석은지 보이지 않느냐고 묻는다.

Torvalds가 밝힌 기대는 두 가지다.
사람들이 최선을 다하고, 자기가 무엇을 하는지 이해하는 것이다.
그리고 그 이해는 어떤 도구를 쓰는지와 거의 관계가 없다고 말한다.
그는 자기가 존경하고 똑똑하다고 여기는 사람들은
새롭고 흥미로운 도구를 피하는 사람들이 아니었다고 덧붙인다.

## 분석

### 쟁점은 공개 의무가 아니라 책임의 위치다

이 스레드의 실제 쟁점은 AI를 썼는지 밝히라는 의무가 무엇을 지켜 주느냐다.
Pinchart는 태그가 강제되지 않아도 기대를 표명하는 데 가치가 있다고 봤다.
Torvalds는 도구를 기준으로 기대를 세우는 것 자체가 틀렸다고 봤다.
그의 기준은 결과물에 대한 이해이고, 그 이해는 도구와 무관하다는 것이다.

Kees Cook은 다른 메일에서 이 차이를 더 정확히 짚었다.
Signed-off-by는 보낸 사람과 서명이 일치하는지 기계적으로 검증할 수 있고
기원 증명이라는 목적을 실제로 수행하지만,
LLM에 대해 우리가 원하는 것은 “이 변경을 이해하고 다른 사람들을 설득할 준비가
되었다”는 것이며,
`Assisted-by`는 그것을 한 번도 해내지 못했다고 썼다.
그는 그 일을 할 곳은 늘 커밋 메시지 본문이었다고 덧붙였다.[^kees-crux]
태그는 사용 사실을 알릴 뿐, 이해를 증명하지 않는다.

### 컴파일러 비유는 의도적으로 과장되었다

Torvalds의 비유는 공정하지 않다.
컴파일러는 결정론적이고 수십 년 검증된 도구이며,
같은 입력에 같은 출력을 낸다.
LLM은 그렇지 않고, 그럴듯하지만 틀린 코드를 만들 수 있다.
그러나 Torvalds가 겨냥한 것은 도구의 신뢰성이 아니라
규칙의 형태다.
“어떤 도구를 쓰지 말라”는 규칙은 결과물의 품질이 아니라 과정을 규제하고,
과정은 검증할 수 없다.

Lobste.rs에서 가장 많은 표를 받은 반응도 이 지점이었다.
elobommart는 결정론적 알고리즘과 확률적 과정을 비교하는 것은 어울리지 않으며
“AI도 도구일 뿐”이라는 주장은 오래전에 반박되지 않았느냐고 했다.[^elobommart]
stip은 결정론적 빌드를 만들어 본 경험으로 보면
운영 컴파일러도 기본 설정에서는 대체로만 결정론적이라고 답했지만,[^stip]
gunduzc는 좋은 컴파일러는 예측하기 어려울 수는 있어도 결정론적이며
예측 불가능과 확률적인 것은 다르다고 반박했다.[^gunduzc]
yshui가 Torvalds가 바이브 코딩을 컴파일러에 빗댔다고 읽은 반면,[^yshui]
creesch는 그가 분명히 이해를 보여야 한다고 말했다며 다르게 읽었다.[^creesch]

그래서 이 비유는 논증이라기보다 귀류법에 가깝다.
도구 사용을 기준으로 삼으면 결국 어디선가 선을 그어야 하는데,
그 선은 자의적일 수밖에 없다는 것을 보이려는 장치다.

HN의 ux266478은 Torvalds가 20년 전에 쓴 C++ 비판을
조금만 고치면 LLM과 바이브 코딩에 대한 아주 일관된 불만이 된다는 점이 흥미롭다고
했다.[^ux266478]
Zambyte는 Torvalds가 AI를 받아들이지 않을 사람으로 보였다며
최근의 더 나은 도구를 접한 결과가 아니냐고 물었지만,[^Zambyte]
efortis는 그가 생각을 바꾼 것이 아니라
이해가 도구와 무관하다는 같은 기준을 적용했을 뿐이라고 답했다.[^efortis]

### 태그를 없애는 데는 다른 이유도 있었다

The Register는 Jeff Layton이 이 태그가 사실상
독점 LLM 회사의 무료 광고 역할을 한다고 설명했다고 전한다.[^register]
태그에 도구 이름이 들어가면 커널 커밋 기록이 특정 상용 제품의 사용 목록이 된다.
태그의 폐기는 원칙의 문제이기도 하지만,
커널 기록이 무엇을 남겨야 하는가라는 실용적 판단이기도 하다.

## 비평

### “이해”는 확인할 수 없다는 점에서 태그와 같은 약점을 가진다

Torvalds는 도구 사용은 검증할 수 없으니 규칙으로 삼지 말자고 한다.
그러나 그가 대신 내세운 “자기가 무엇을 하는지 이해한다”는 기대도
리뷰어가 직접 확인할 방법이 마땅치 않다.
Pinchart의 반론, 즉 커널의 요구 대부분은 원래 강제할 수 없고
기대를 밝히는 것 자체에 가치가 있다는 말은
이해에 대한 기대에도 그대로 적용된다.

결국 두 사람의 차이는 강제 가능성이 아니라
어떤 기대를 문서에 적을 것인가다.
Torvalds의 메일은 그 차이를 날카롭게 만들었지만,
이해를 어떻게 드러내게 할지에 대해서는 말하지 않는다.
Kees Cook이 말한 커밋 메시지 본문이 그 답의 후보지만,
그 역시 LLM이 쓸 수 있다는 점에서 같은 문제를 다시 만난다.

### 리뷰어의 부담이라는 현실을 비켜 간다

Theodore Ts'o는 원하는 것은 높은 품질의 기여이고
품질이 높다면 AI가 만들었든 아니든 상관없다고 하면서도,
AI가 새 기여자를 크게 늘려 문제를 악화시킨다고 인정했다.[^tytso]
Kees Cook은 이전에 좋은 패치를 보내던 사람이
갑자기 나쁜 패치를 보내는 경우에 대한 신호가 태그의 의도였지만
제대로 작동하지 않았다고 정리했다.[^kees-crux]

Torvalds의 메일은 기여자의 태도에 대한 기대만 말하고,
늘어난 기여를 감당해야 하는 메인테이너의 부담은 다루지 않는다.
태그가 그 부담을 덜어 주지 못했다는 판단은 맞을 수 있지만,
태그를 없앤 자리를 무엇이 채울지는 비어 있다.

Lobste.rs의 orib은 Torvalds가 최근 인터뷰에서 병합하는 코드를
자세히 리뷰하지 않고 리뷰를 위임한 사람들을 믿는다고 말했다며,
LLM이 만든 코드를 리뷰하는 일이 그에게 떨어지지는 않는다고 짚었다.[^orib]
규칙을 정하는 사람과 그 규칙의 비용을 치르는 사람이 다르다는 지적이다.

### 효용 말고 다른 기준은 논의에서 빠졌다

Lobste.rs의 pralkarz는 Torvalds가 LLM의 효용만이 사용 여부를 정하는 유일한 요소라는
서사에 빠졌다며,
윤리와 환경과 사회적 영향은 고려하지 않았다고 비판했다.[^pralkarz]
flockofbirbs는 그가 원래 그런 문제에 관심이 없었다며
GPLv3로 옮기기를 거부한 일을 예로 들었다.[^flockofbirbs]
Torvalds의 메일은 의도적으로 기술적 기준에만 머문다.
그 선택이 커널 프로젝트의 관례에는 맞을 수 있지만,
윤리나 사회적 이유로 AI 사용을 반대하는 사람들의 주장에는
같은 층위에서 답하지 않는다.

## 인사이트

### 공개 의무는 도구가 보편화되면 의미를 잃는다

Kees Cook은 자기 커밋 로그가 코드처럼 자신과 LLM의 합작이 되었고,
동료의 장황한 커밋 로그를 LLM이 쓴 것으로 착각한 적도 있다며
사람과 기계를 구분하는 변곡점이 이미 왔거나 다가오고 있다고
했다.[^kees-unenforceable]
대부분의 사람이 어떤 형태로든 도구를 쓰게 되면,
“도구를 썼다”는 표시는 아무것도 구별하지 못한다.
컴파일러를 썼다는 태그가 없는 것과 같은 이유다.

이는 다른 공개 의무에도 적용된다.
AI 사용 공개를 요구하는 규칙은 도입 시점에는 의미가 있지만,
사용이 보편화될수록 정보량이 0에 가까워진다.
규칙을 만들 때 그 규칙이 언제 무의미해지는지도 함께 정해 두는 편이 낫다.

### 평판이 도구 공개를 대신한다

Kees Cook은 결국 각 기여자의 평판, 작업 영역, 실수를 고치는 책임감,
분야 밖 지식의 깊이, 소통 방식을 확장 가능하게 이해하는 방법을 찾고 있다고 했다.
그리고 이것은 메인테이너마다 기준이 달라 기계적으로 다루기 어려울 것이라고
봤다.[^kees-crux]
도구 공개가 무의미해지면 남는 신호는 사람에 대한 신뢰다.
이는 오픈소스가 원래 작동하던 방식으로의 회귀이기도 하다.

### 접근성이라는 관점은 금지 규칙의 숨은 비용을 드러낸다

Matthew Brost는 읽기와 쓰기에 관련된 학습 장애가 있어
오랫동안 코드를 설명하는 일이 가장 어려웠고,
LLM이 처음 나왔을 때는 문서와 커밋 메시지를 쓰는 데만 썼다고 밝혔다.[^brost]
“커밋 메시지는 손으로 써라” 같은 규칙은 중립적으로 보이지만,
특정 사람들에게는 기여 자체를 어렵게 만든다.
도구를 금지하는 규칙은 품질이 아니라 기여자의 조건을 걸러 내는
규칙이 될 수 있다.

---

[^levin]: Sasha Levin, [\[PATCH\] docs: remove Assisted-by references](https://lore.kernel.org/lkml/20261009083137.3-1-sashal@kernel.org/), 2026-10-09

[^register]: The Register, [Linux kernel devs drop obligatory confession of AI tool usage](https://www.theregister.com/ai-and-ml/2026/10/14/linux-kernel-devs-drop-obligatory-confession-of-ai-tool-usage/5303140), 2026-10-14

[^gregkh]: Greg Kroah-Hartman, [Re: \[PATCH\] docs: remove Assisted-by references](https://lore.kernel.org/lkml/2026100940-deceiving-lazily-9416@gregkh/), 2026-10-09

[^kees-unenforceable]: Kees Cook, [Re: \[PATCH\] docs: remove Assisted-by references](https://lore.kernel.org/lkml/202610131216.C841415F01@keescook/), 2026-10-13

[^pinchart]: Laurent Pinchart, [Re: \[PATCH\] docs: remove Assisted-by references](https://lore.kernel.org/lkml/20261013201628.GO4214@killaraus.ideasonboard.com/), 2026-10-13

[^kees-crux]: Kees Cook, [Re: \[PATCH\] docs: remove Assisted-by references](https://lore.kernel.org/lkml/202610140951.C3D6CBF73@keescook/), 2026-10-14

[^tytso]: Theodore Ts'o, [Re: \[PATCH\] docs: remove Assisted-by references](https://lore.kernel.org/lkml/as7uqZn9rQ52USwy@mit.edu/), 2026-10-14

[^brost]: Matthew Brost, [Re: \[PATCH\] docs: remove Assisted-by references](https://lore.kernel.org/lkml/atIyeGHCGDTCIvkx@gsse-cloud1.jf.intel.com/), 2026-10-16

[^ux266478]: <https://news.ycombinator.com/item?id=50126338>

[^Zambyte]: <https://news.ycombinator.com/item?id=50113991>

[^efortis]: <https://news.ycombinator.com/item?id=50114609>

[^elobommart]: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel#c_g7p3g6>

[^stip]: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel#c_uoxeae>

[^gunduzc]: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel#c_hm9tdo>

[^yshui]: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel#c_lqoemq>

[^creesch]: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel#c_l7sbtz>

[^orib]: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel#c_3g5ijd>

[^pralkarz]: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel#c_nct7jk>

[^flockofbirbs]: <https://lobste.rs/s/xiq59t/linus_torvalds_on_ai_assisted_kernel#c_lugcme>
