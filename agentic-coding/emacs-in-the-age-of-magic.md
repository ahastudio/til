# 편집 속도와 Lisp의 표현력이라는 Emacs의 우위가 AI 앞에서 사라졌고 재구현이 공짜가 되어 낭비의 개념이 무너졌다는 Emacs 사용자의 글

원문: [Emacs In the Age Of Magic](https://commandlinesystems.com/magic.txt)

HN 토론: <https://news.ycombinator.com/item?id=50458208> (305점, 156개 댓글)

## 요약

일반 텍스트 파일로 올라온 에세이이다.
글에는 저자 이름과 날짜가 없고, HN에는 2026년 11월 11일에 올라왔다.
부제는 로마는 하루에 지어지지 않았다, 오히려 10분에 가깝다이다.
글쓴이는 2025년 9월에 Claude Code를 쓰기 시작해 한동안 아침마다 전날 본 것이 사실인지
꼬집어 확인했고, 지금은 그때보다 한 자릿수 크기 이상 유능하다고 쓴다.

글의 줄기는 다섯 단계이다.
첫째, 디지털 시대의 신뢰가 같은 입력이면 같은 출력을 내는 트랜지스터의 결정성에서 온다고 말하고,
오래된 전문가 시스템 연구자들이 규칙 기반으로 인공지능을 만들려 했을 때 프로그래머들이
비웃었다는 이야기를 한다.
둘째, Lisp이 규칙 기반 AI의 도구로 쓰였고 C보다 느린 대신 표현이 경제적이었다는 역사를
짧게 훑는다.
셋째, 그래서 Emacs 사용자가 자랑하던 것, 곧 편집 속도, 사용자 정의, Lisp의 표현력이
AI에게 원하는 것을 말하는 순간 모두 사라졌다고 주장한다.
예로 magit의 커밋을 든다.
Emacs 사용자는 `C-x g`, `S`, `c c`, 커밋 메시지, `C-c C-c`로 으스댔지만 Claude Code는
변경 덩어리가 끝나면 회색으로 커밋을 제안하고 Tab과 Return만 누르면 된다.
넷째, 저자가 웃기다고 한 두 사례연구를 든다.
다섯째, 이것이 재구현의 비용이 토큰뿐인 세계이고 낭비의 전통적 개념이 의미를 잃는다고
결론짓고, 소프트웨어의 자유가 뒤집혔다고 맺는다.

### 사례연구 둘

첫 사례는 `excali-mode.el`이다.
Emacs에 새 캔버스 위젯 API가 생기자 누군가(글은 고등학생을 상상한다) Qwen에게 Excalidraw를 그
API로 만들라고 시켰고, Qwen은 Excalidraw의 전체 스택을 한 층씩 대응시켜 다시 만들었다.
글은 이를 표로 정리한다.
브라우저는 Emacs, JavaScript는 Elisp, rough.js와 렌더 코드는 C 모듈, Canvas 2D API는 Cairo와
Pango, `<canvas>` 요소는 Emacs 32의 canvas 이미지이다.
글은 이전의 어떤 개발자도 장난감 목적으로 이런 포팅을 시도하지 않았을 것이고 지금은 토큰만
든다고 말한다.

둘째 사례는 `cooked.el`이다.
r/emacs에서 comint의 편의를 보존하면서 일반 텍스트 버퍼처럼 보이는 터미널 에뮬레이션 모드를
이야기했고, 한 응답자가 그런 출력을 cooked라고 불렀다.
며칠 뒤 한 고등학생(이라고 글이 추정하는 사람)이 `cooked.el`을 올렸고, AI 사용을 사과하면서도
직접 강하게 설계했다는 점으로 공을 주장했다고 한다.
글이 이상하게 여기는 것은 이것이 Rust로 쓴 독립적인 터미널 에뮬레이터를 통째로 갖고 있다는
점이다.
예전이라면 기성 부품을 썼을 텐데 이 사람은 억만장자가 5년 동안 매달린 것을 커피 시간에
복제했다고 한다.
저자는 그 설계가 깔끔하고 합리적으로 보이지만 Claude가 그렇게 설명해 줬을 뿐이고 코드도
Claude가 썼다고 덧붙인다.

글은 Elisp를 Guile Scheme으로 바꾸거나 Lisp 스레드를 선점형으로 만드는 일처럼 전면 재구현이
정당한 프로젝트도 있다고 하며, 월 100달러 요금제와 긴 주말이 있는 충분히 관심 있는 개발자라면
괜찮은 초안을 만들 수 있다고 본다.
아직 아무도 안 한 것이 사실은 아무도 그것을 원하지 않았고 말하기만 좋아했다는 증거라고
쓴다.
이어 HN에 올라왔던 *The Emacsification of Software*를 소개한다.
이 글은 AI로 자기 취향의 마크다운 뷰어를 만든 이야기이고, r/emacs의 기질을 Product Hunt
0%와 보여 주기(show and tell) 100%로 요약했다.[^emacsification]
이 글이 말하는 흐름은 모든 소프트웨어가 Emacs처럼 개인화된다는 것이다.
글은 AI 모델이 Dario가 말한 사랑 어린 은총의 기계가 된다면 언젠가 하드웨어에 직접
쓰게 맡길 것이라고 상상하고, 마지막으로 이것이 Stallman의 소프트웨어 자유를 뒤집어 놓았다고 쓴다.
컴퓨터가 상상하는 대로 해 주는 것이 진짜 자유이지만 어떻게 돌아가는지는 아무도 모른다는
것이다.

## 분석

### 중심 주장은 도구의 효율이라는 해자가 증발했다는 것이다

가장 강하게 말하면 글은 Emacs 사용자의 정체성이 효율에 있었다고 가정하고, 그 효율이 AI 앞에서
의미를 잃었다고 쓴다.
키 입력으로 하던 일(스테이징, 커밋)을 AI가 대신 제안하므로 가장 빨리 누르는 사람이 이기는
경쟁이 사라진다는 것이다.
글의 문장으로는 칼싸움에 총을 들고 와 안심했는데 이제 모두가 드론을 보낸다는 비유이다.
HN의 danielvaughn은 이 문장이 완벽하다며 Vim에서 영감을 받은 키보드 중심 디자인 도구를
만들던 자신의 의욕이 LLM에 꺾였다고 했고, adamddev1은 AI가 만든 앱은 효율적이고 결정적인
소프트웨어라는 산 위에 얹힌 얇은 혹일 뿐이라고 답했다.[^danielvaughn][^adamddev1]

### 재구현이 공짜가 되자 낭비의 기준이 바뀐다

두 사례연구의 요점은 질적으로 새로운 소프트웨어가 아니라 비용 구조의 변화이다.
Excalidraw 전체를 Elisp와 C로 옮기는 일이나 터미널 에뮬레이터를 새로 쓰는 일은 예전에는
고용된 사람이 그만둘 일이었다.
이제는 토큰 값만 든다.
HN의 piker는 글의 Rust 터미널 에뮬레이터 대목에 대해 모델이 좋아진 지금 Ghostty 같은 것이
레거시가 된 것이냐고 물었다.[^piker]
이 문서는 이 물음에 답하지 못한다.
글이 이 사례들에서 끌어내는 것은 재구현이 현실적 선택이 되었으니 기성품에 기대는 판단의
무게가 달라졌다는 것이다.

### 자유와 이해가 분리된다는 마지막 대목이 가장 긴 파장을 갖는다

글은 상상하는 것을 컴퓨터가 해 주는 것이 진짜 자유라고 하면서 대가로 이해를 든다.
HN의 russfink가 이 문장을 인용했고, whartung은 Stallman이나 다른 누구가 어떻게 일하는지도
아무도 모르지만 Emacs를 그 저자들과 따로 해독할 수 있다고 반박했다.[^russfink][^whartung]
demo4567은 이제 폐쇄된 AI 벤더에 의존하게 되었으니 진짜 소프트웨어 자유는 코드를 쓰는 봇을
분해할 수 있는 것이라고 했고, merelydev는 Stallman이 퍼뜨린 자유 소프트웨어에서 LLM이
훈련되었으니 Stallman이 없었다면 바이브 코딩도 없었을 것이라고 했다.[^demo4567][^merelydev]
brabel은 글처럼 AI가 Stallman의 세계(누구나 쓰는 소프트웨어를 마음대로 바꾸는 세계)를
현실로 만드는 것이라 아이러니가 아니라고 했다.[^brabel]
글이 말하는 뒤집힘은 소프트웨어 자유의 네 가지 자유 가운데 수정할 자유가 쉬워졌지만 이해하고
공유할 수 있는 구조가 약해졌다는 것으로 풀 수 있다.
이것은 이 문서의 해석이다.

## 비평

### 인용한 수치와 사례를 확인하니 몇 곳이 맞지 않는다

글은 OpenAI의 최신 모델이 세 시간 만에 8,000개의 연구 문제를 융단 폭격해 372개의 유력한 적중을
냈다고 쓴다.
이 숫자의 출처인 Scott Aaronson의 글 *The Mathocalypse*를 열어 보니 Aaronson 자신이 글을
고쳤다.
처음 글에 8,000개 문제와 약 5% 성공률이라고 썼지만 독자들이 정정해서 약 4,000개 문제와
약 10%로 바로잡았다고 적혀 있다.
세 시간은 문제 전체가 아니라 결과 하나에 쓴 평균 ChatGPT Pro 사고 계산량이라는 설명이 댓글에서
OpenAI의 저장소 문구와 함께 나온다.[^aaronson]
Timothy Chow는 같은 댓글란에서 8,000이라는 숫자의 출처를 찾지 못했고 OpenAI 저장소에는
대략 4,000개 문제라고 적혀 있다고 했다.[^aaronson]
글의 문장은 정정되기 전의 숫자와 세 시간을 합쳐 썼다.
핵심 주장(AI가 어려운 문제를 푼다)에는 영향이 작지만, 인용의 정확성은 글의 약점이다.

### 사례연구는 확인 가능한 부분과 글의 상상이 섞여 있다

두 프로젝트의 저장소는 실제로 있다.
`yibie/excali-mode`는 2026년 9월 28일에 만들어졌고 README는 Emacs 32(마스터)의 새 `canvas`
이미지 타입에 Cairo와 Pango로 직접 그리는 작은 C 모듈과 Elisp의 장면 관리로 구성된다고
적는다.
공식 Excalidraw의 비공식 포트이고 브라우저나 웹뷰는 없다.[^excali-readme]
이 부분은 글의 표와 맞다.
그러나 글이 등장시킨 Qwen과의 대화는 저자가 쉽게 상상할 수 있다고 말한 가상의 대화이고,
글이 말한 프로젝트 작성자가 고등학생이라는 점은 근거가 없다.
`vodik/cooked`의 README는 이와 다른 사람을 보여 준다.
작성자는 터미널 에뮬레이터를 만들고 일해 본 경험이 있어서 LLM을 써도 성능 병목을 더 잘 찾고
진단할 수 있었다고 쓰고, 거의 100% 바이브 코딩이라 취향이 아니지만 시간이 부족해 설계를 시험하려고
썼으며 앞으로는 더 손으로 유지할 것이라고 적는다.[^cooked-readme]
Rust 구성 요소가 pts와 프로세스 통신을 맡고 Elisp 쪽이 더 느린 고정 프레임률로 갱신하도록
나눈 설계도 README에 있다.[^cooked-readme]
커피 시간에 복제했다는 표현도 저장소가 2026년 8월에 만들어졌고 9월에 마지막 푸시가 있었다는
사실과는 거리가 있다.
이 문서는 이 날짜들이 개발 기간의 증거라고 주장하지는 않는다.

### 아무도 원하지 않았다는 추론은 증거가 없다

글은 선점형 스레드나 Guile 전환이 아직 없는 것을 사람들이 원한 것이 아니라 말하고 싶었던
것의 증거로 읽는다.
이 해석은 개발 비용이 장벽이었다는 대안(이제 싸졌으니 곧 나온다)과도 양립하고,
논의가 설계 합의를 쌓는 과정이라는 시각과도 양립한다.
HN의 vhantz는 이 문장 뒤의 자전거 창고 논쟁(bikeshedding)이 없어지는 것이 큰 손실이라고
했고, 모든 과학자가 이미 쓰인 책만 참고하고 닫힌 연구실에서 연구하는 상황에 비유했다.[^vhantz]
jnpnj는 즉시 소통이 균질화를 낳고 느리고 제한된 소통이 나눌 시간과 동기를 만들었다고
말했다.[^jnpnj]
이 문서는 새 기능이 실제로 나오는지 보는 것으로만 확인할 수 있다고 본다.

### 결정성에 대한 전제는 하드웨어 현실과 다르다

글은 트랜지스터가 같은 입력에 같은 출력을 낸다는 것이 컴퓨터에 고삐를 맡기는 이유라고
한다.
HN의 everybodyknows는 ECC 메모리 업계를 모르느냐고 물었고, atrus는 컴퓨터가 결정적인 것은
현실과 사용자 사이에 오류 정정 층이 수십 겹 있기 때문이라고 했다.[^everybodyknows][^atrus]
이 지적은 글의 결론을 바꾸지는 않지만 서두의 논거가 단순화라는 점을 보여 준다.

### 속도가 Emacs를 쓰는 이유라는 전제를 의문시하는 반응

skydhash는 속도 경쟁을 위해 vim과 emacs를 배운 것이 아니라 좌절을 줄이기 위해 배웠다고
했고, rgoulter는 속도보다 노력이나 흐름(flow)으로 틀을 짜는 것이 낫다고 보았다.
키보드만으로 하던 일 중간에 마우스를 쓰면 흐름이 끊긴다는 것이다.[^skydhash][^rgoulter]
글의 전제가 효율 경쟁이라면 이 반응은 AI가 흐름 문제도 지우는지를 묻게 한다.

### AI 정신병 같다는 비난과 LLM 없는 Emacs 선언

vkgcr는 이 글이 원샷 프로토타입을 만들다가 AI 정신병에 걸린 사람처럼 읽힌다고 했다.[^vkgcr]
이는 근거를 대지 않은 단정이고, 글이 사례 두 개와 일부 부정확한 수치로 큰 결론에 이르는
방식에 대한 불만의 거친 표현으로 읽는 것이 안전하다.
jefurii는 GNU가 정하는 정책과 관계없이 LLM이 만든 기여가 없는 Emacs를 쓰고 개발하겠다는
human-emacs.org의 선언을 인용했고, brabel은 기술을 사랑한다던 사람들이 자기 기예를 대체할 새
기술에 가장 격렬하게 반대하는 집단이 되었다고 했다.[^jefurii][^brabel2]
이 갈등은 글 밖의 배경이다.

## 인사이트

### 효율의 해자를 잃은 도구가 남길 것은 결정성과 투명성이다

글의 진단이 맞다면 편집기가 팔 수 있는 것은 입력 속도가 아니라 결정적 동작, 조합 가능성,
검사 가능성이다.
HN에서 johanvts는 Claude Code를 Emacs 안에서 돌리며 elisp를 배우지 않고도 이득을 얻으니
LLM이 Emacs의 새 황금기를 열 것이라고 했고, iLemming은 코드 작성보다 읽기에서 Emacs를 더 많이
쓴다고 했고, mark_l_watson은 40년 넘게 쓴 Emacs 설정이 AI 덕에 최고가 되었다고 했다.[^johanvts][^ilemming][^mark-l-watson]
이 사례들은 글의 비관과 반대 방향의 경험담이다.
이 문서의 해석은 AI가 Emacs의 효율 우위를 없앴다는 글의 주장이 코드 작성에는 맞더라도
Emacs가 하는 읽기와 조합과 사용자 정의에는 맞지 않을 수 있다는 것이다.

### 재구현을 할 때 이유를 말할 수 있는지 먼저 묻는다

토큰만 들면 재구현이 쉬워지지만 비용은 사라지지 않고 검증과 유지보수로 옮겨 간다.
HN의 Animats는 AI가 만든 덩어리를 격리하도록 명확한 API로 모듈성을 생각해야 한다고
했다.[^animats]
이 문서의 제안은 재구현하기 전에 기성품이 주지 못하는 불변 조건 하나를 문장으로 쓰는 것이다.
쓰지 못하면 기성품을 쓰고, 쓸 수 있으면 그 조건을 시험으로 고정한다.
`cooked`의 README가 터미널 에뮬레이션을 Rust와 Elisp로 나눈 이유(성능과 갱신 속도)를 구체적으로
적은 것은 이 형식의 좋은 예이다.[^cooked-readme]
이 제안은 이 문서의 것이다.

### 글의 수치와 주장은 원문 확인을 거쳐서 인용한다

이 글의 사례는 AI 시대 글쓰기의 전형적인 위험을 보여 준다.
정정된 숫자가 남아 있고, 확인할 수 있는 저장소가 글의 서술과 다르다.
이 문서의 제안은 AI 관련 글에서 수치와 인물 서술을 인용할 때 원자료(여기서는 Aaronson의
글과 OpenAI 저장소, 두 프로젝트의 README)를 한 번 열어 보는 것이다.

### 글의 주장을 확인할 관찰

글의 핵심 예측은 모든 소프트웨어가 개인화되고 일회용 재구현이 늘어난다는 것이다.
이를 확인하려면 비슷한 프로젝트의 수와 수명을 보면 된다.
저장소가 만들어진 뒤 몇 달 안에 유지가 끊기는 비율이 높으면 일회용 소프트웨어라는 예측이
맞는 것이고, 유지가 계속되거나 공유 프로젝트로 합쳐지면 글의 예측보다 지속성이 높다는
뜻이다.
이 관찰은 이 문서의 제안이다.

---

[^aaronson]: Scott Aaronson, [The Mathocalypse](https://scottaaronson.blog/?p=10169)

[^emacsification]: Thomas Ptacek, [The Emacsification of Software](https://sockpuppet.org/blog/2026/05/12/emacsification/), 2026-05-12

[^excali-readme]: yibie, [excali-mode: Excalidraw inside Emacs](https://github.com/yibie/excali-mode)

[^cooked-readme]: vodik, [cooked](https://github.com/vodik/cooked)

[^danielvaughn]: <https://news.ycombinator.com/item?id=50459123>

[^adamddev1]: <https://news.ycombinator.com/item?id=50459353>

[^piker]: <https://news.ycombinator.com/item?id=50459019>

[^russfink]: <https://news.ycombinator.com/item?id=50459133>

[^whartung]: <https://news.ycombinator.com/item?id=50462980>

[^demo4567]: <https://news.ycombinator.com/item?id=50460162>

[^merelydev]: <https://news.ycombinator.com/item?id=50463996>

[^brabel]: <https://news.ycombinator.com/item?id=50464087>

[^vhantz]: <https://news.ycombinator.com/item?id=50460104>

[^jnpnj]: <https://news.ycombinator.com/item?id=50460512>

[^everybodyknows]: <https://news.ycombinator.com/item?id=50459423>

[^atrus]: <https://news.ycombinator.com/item?id=50460718>

[^skydhash]: <https://news.ycombinator.com/item?id=50460403>

[^rgoulter]: <https://news.ycombinator.com/item?id=50462168>

[^vkgcr]: <https://news.ycombinator.com/item?id=50464674>

[^jefurii]: <https://news.ycombinator.com/item?id=50460233>

[^brabel2]: <https://news.ycombinator.com/item?id=50469567>

[^johanvts]: <https://news.ycombinator.com/item?id=50460414>

[^ilemming]: <https://news.ycombinator.com/item?id=50470610>

[^mark-l-watson]: <https://news.ycombinator.com/item?id=50465063>

[^animats]: <https://news.ycombinator.com/item?id=50458865>
