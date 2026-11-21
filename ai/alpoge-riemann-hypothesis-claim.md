# Alpöge의 리만 가설 증명 발표

원문: [Levent Alpöge claims proof of the Generalized Riemann Hypothesis](https://alpo.ge/remark.pdf)

HN 토론: <https://news.ycombinator.com/item?id=50574968> (2419점, 1631개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann> (71점, 31개 댓글)

GN 토론: <https://news.hada.io/topic?id=37529>

## 요약

이 문서의 원문은 `alpo.ge/remark.pdf`로 공개된 4쪽짜리 발표문이다.
발표문에는 저자 이름과 소속이 적혀 있지 않고 제목도 없다.
HN 스레드의 제목은 Levent Alpöge가 일반화 리만 가설(Generalized Riemann
Hypothesis, GRH)의 증명을 주장한다고 소개하고,[^hn-title]
GeekNews 토픽의 제목은 Anthropic 수학자가 Claude와 리만 가설을 증명했다고
발표했다고 소개한다.[^gn-title]
이 문서는 PDF 전문을 내려받아 텍스트로 추출해 읽었다.
수식은 추출된 텍스트로만 읽었고 렌더링된 쪽을 확인하지 않았으므로 연표의 수식은
옮기지 않는다.
발표문이 가리키는 Lean 자료 14개 파일은 내려받지 않았고 증명을 검증하지도
못했다.
이 문서가 읽은 시점은 발표 다음 날이라 검증과 반응은 계속 바뀌고 있다.

일반화 리만 가설은 리만 제타 함수 외의 함수까지 같은 명제를 요구하고,
리만 가설을 특수한 경우로 포함한다.
이는 이 문서의 배경 설명이다.

### 발표문이 말하는 것

발표문은 1인칭으로 쓰인 글이고 크게 세 부분으로 나뉜다.
첫 쪽은 주장과 소회, 둘째 쪽은 공개 시점과 감사,
셋째와 넷째 쪽은 작업 경과의 연표이다.

- 증명 주장: 저자는 Claude와 함께 리만 가설의 증명을 발견했다고 믿는다고 쓴다. 같은 방법이 일반화 리만 가설도 해결하고, 시간이 더 있으면 확장 리만 가설(Extended Riemann Hypothesis)도 해결할 것으로 기대한다고 덧붙인다. 확장 리만 가설은 기대이고 주장이 아니다.
- 형식화: Claude와 함께 논증을 가정 없이 형식화했다고 쓴다. 첫 쪽의 각주는 `lean.tar.gz.part01`부터 `part14`까지 14개 분할 파일의 주소를 적는다. 발표문에는 어떤 검증기로 확인했는지나 증명된 명제가 무엇인지에 대한 서술이 없다.
- 읽을 수 있는 증명의 부재: 논증이 현재 매우 길다고 쓴다. 형식화는 끝났고, 충분히 상세하지만 읽을 수 없는 거대한 문서를 만드는 일은 기계적이라고 한다. 저자는 이 논증을 이해하고 설명하고 제대로 쓰는 일을 하려 한다고 밝힌다. 각주에는 재미 삼아 만들어 보니 25만 쪽이 넘었다고 적는다. 읽을 수 없는 문서를 올리는 것은 부적절하다고 보아 Lean만 공개하기로 했다고 한다.
- 한계 진술: 논증이 닿는 수학의 넓은 영역을 아직 숙달하지 못했고, 고차 군의 보형 형식에 대한 이해가 얕다고 쓴다. 이상하고 비최적인 선택이 많이 들어갔을 수 있으며 더 짧은 논증이 곧 나올 것으로 기대한다고도 쓴다.
- 분담: 저자는 서로 다른 두 아이디어를 단순한 모형에서 결합하고 이에 맞는 상황을 찾는 데까지 이끌었고, 결승선 근처에서는 Claude가 자신을 크게 앞섰다고 쓴다.

기술적 서술은 한 줄 예시와 연표뿐이다.
발표문은 함수체의 리만 가설을 푼 Stepanov 논증이 중복도(multiplicity)를 가진
인자(divisor)를 쓰는데, 정수에서는 중복도를 찾기 어렵다고 설명한다.
저자는 이를 정수를 미분하는 것에 비유한다.
단순한 모형의 푸리에 해석 아이디어는 보형적인 방식으로 세타 올림(theta lift)을
연쇄하는 방향으로 이어졌다고 한다.
길이 X인 폰 망골트(von Mangoldt) 합에서, 각 올림이 중복도를 흉내 내도록 연쇄의
길이를 √X로 하자고 제안한 것이 Claude였다고 쓴다.

셋째 쪽의 연표는 Claude가 철저한 검색 뒤에 만든 대략적인 목록이라고 소개되며
20개 항목이다.
첫 항목은 2026년 10월 6일의 Stepanov 행렬식이고,
마지막 항목은 11월 16일의 GRH이다.
항목에는 Guinand–Weil 부호, GGP 주기, Iwasawa 탑, Bost 기울기 부등식,
Vandiver 추측의 약화 같은 주제가 이어진다.
저자는 각주에서 Claude가 전문가인 부분은 자신이 요약을 풀어 쓴 것이라 말이 안 될
수 있으며, 명확히 하는 것은 Lean으로 충분하다고 적는다.

### 공개 방식과 시점

둘째 쪽은 발표 시점이 끔찍하다고 시작한다.
저자는 늦은 일요일 밤에 결과를 얻었고 Dario에게 공개 가능 여부를 물었으며,
지켜야 할 제약이 있었다고 쓴다.
상의한 몇몇 수학자와 저자 쪽 지도부가 비슷한 견해였고,
더 기다리면 살 수 없을 것 같다고 느낀 책임은 자신에게 있다고 한다.
시점에 대한 냉소적인 해석이 있음을 알지만 그것은 사실이 아니라고 쓴다.

그 뒤에는 감사하는 사람들의 이름이 이어지고 OpenAI의 수학 작업을 칭찬하는
대목이 있다.
저자는 OpenAI가 고른 Ehrhart 추측 문제를 더 풀어 보다가 Navier–Stokes 문제가
풀릴 것임을 곧바로 알았다고 쓴다.
이는 개인적 전망이며 이번 발표문이 그 문제의 해법을 제시하는 것은 아니다.


## 분석

### 증명의 무게가 읽을 수 있는 논증에서 형식화 자료로 옮겨 갔다

이 발표의 구조는 보통의 수학 발표와 순서가 반대이다.
사람이 읽을 수 있는 증명이 먼저 나오고 형식화가 뒤따르는 대신, Lean 형식화가 끝난 자료가 먼저 나오고 사람이 읽을 수 있는 설명은 나중으로 미뤄졌다.
발표자는 사람이 읽을 해설 없이 생성된 거대한 문서를 그대로 올리는 것은 부적절하다고 판단했다고 쓴다.

그 결과 독자가 확인할 수 있는 것은 두 가지로 좁아진다.
Lean으로 쓰인 명제가 리만 가설과 GRH를 정확히 표현하는지, 그리고 그 증명이 검증기를 통과하는지이다.
HN의 layer8은 확인할 것이 Lean 명제가 리만 가설을 제대로 표현하는지와 Lean 구현에 해당 결함이 없는지 두 가지라고 적었다.[^layer8]
Jweb_Guru는 OpenAI가 내놓은 수백 개의 Lean 증명 가운데 증명기의 버그를 악용한 것은 자기가 아는 한 없었고, 더 흔한 병리는 문제를 잘못 서술하거나 근거 없는 가정을 더하거나 종이 증명과 맞지 않는 경우라고 했다.[^Jweb_Guru]
그는 이번 건에서는 추가 가정이 없다고 다른 사람들이 보고했다는 점도 전했지만, 자신은 아직 Lean 증명을 검사하지 못했다고 밝혔다.[^Jweb_Guru]
zug_zug는 발표자가 증명을 완전히 이해하지 못한다고 했으니 Lean이 맞다고 하면 맞다고 추정하는 상황이라고 정리했고, 서로 다른 Lean 검증기가 같은 버그를 가질 가능성이 낮다는 점이 가장 설득력 있는 신뢰 근거라며 검증기별 결과 목록을 보고 싶다고 했다.[^zug_zug]

자료의 규모는 가늠이 된다.
djoldman은 공개된 파일을 풀면 1.3GB에 약 1,500만 줄이라고 적었다.[^djoldman]
이 수치는 댓글이 제시한 것이고, 이 문서가 재현하지는 못했다.

### 신뢰의 출처를 두고 저자의 이력과 형식 검증이 겹쳐 논의된다

HN의 가장 큰 가지는 저자의 신뢰도를 둘러싼 논쟁이었다.
xianshou는 Alpöge가 AI를 새로운 수학적 발견으로 이끄는 데 세계 최고 수준이고 그가 리만 가설을 가졌다고 하면 가진 것이라고 썼다.[^xianshou]
gus_massa는 이 사람이 무작위 Anthropic 직원이 아니라 올해 이미 검증된 흥미로운 결과 서너 개를 낸 사람이라고 보탰다.[^gus_massa]
반대편에서 auntienomen은 Alpöge가 똑똑하고 원칙 있는 사람이고 LLM으로 수학을 하게 하는 데 세계 최고일 수 있지만 이 분야의 전문가는 아니므로, 권위에 기댈 거라면 실제 권위자의 검토를 기다리자고 했다.[^auntienomen]
xyzzyz는 프린스턴 박사 학위와 대수기하 논문이 있으니 전문가가 아니라고 부르기 어렵다고 반박했다.[^xyzzyz]
hyperpape는 이 논쟁의 접점을 이렇게 정리했다. 검증은 수학자들이 하고, 이력은 이 주장이 진지하게 받아들여질 가치가 있다는 것을 보여 줄 뿐이며, Lean이 있다는 점이 모치즈키 논쟁과 다르다는 것이다.[^hyperpape]

Lobste.rs에서는 다른 비교가 나왔다.
WilhelmVonWeiner는 Lean 문화 덕분에 리만 가설에 관한 25만 쪽짜리 저작이 처음부터 배척당하지 않는다는 점이 흥미롭고, 우주 간 타이히뮐러 이론(IUTT)의 논쟁을 떠올렸다고 썼다.[^WilhelmVonWeiner]

### 같은 날 나온 또 하나의 GRH 증명안이 비교 대상이 되었다

발표 당일 다른 주장이 겹쳤다.
Math 216 블로그에 올라온 짧은 공지(작성자 표기 ravivakil)는 Alessandro Maria Masullo의 GRH 증명안을 소개한다.
Brian Conrad가 몇 달 동안 면밀히 검토하며 피드백을 주었고 지금까지는 괜찮아 보인다고 하며, 이 증명은 모두 사람이 썼고 AI는 쓰이지 않았다고 한다.
공지는 원래 Conrad가 1년쯤 더 다듬은 뒤 발표하려 했으나 지금 초안을 내는 편이 낫다고 판단했다고 설명한다.[^vakil]
공지에는 약 8시간 뒤의 추가 글도 있다. 여러 사람이 서로 다른 AI 모델의 도움으로 찾은 문제점들을 알려 왔고, 모든 문제가 해결되어야 이 증명이 참으로 받아들여지며 자신은 증명 전략의 정확성에 대해 어떤 주장도 하지 않는다는 내용이다.[^vakil]

댓글들은 이 쌍을 비교 대상으로 읽었다.
chorsestudios는 Alpöge에게는 Lean 증명은 있고 사람이 읽을 증명이 없는 반면 Masullo에게는 사람이 읽을 증명은 있고 Lean 증명이 없다는 점을 짚었다.[^chorsestudios]
분량은 댓글마다 다르다. lysace는 940쪽이라고 했고,[^lysace] Lobste.rs의 aardvark179는 900쪽,[^aardvark179] dzwdz는 1,000쪽이라고 적었다.[^dzwdz]
두 증명이 모두 맞는다면 서로 다른 경로로 같은 결론에 닿는 것이다.
이는 가정일 뿐이고 이 문서는 어느 쪽도 검증하지 못했다.

Alpöge는 앞서 나비에-스토크스 연구에서도 이름이 오른 수학자이다.
이 저장소의 [나비에-스토크스 발표 직전에 일어난 일](navier-stokes-authorship-dispute.md) 문서는 Buckmaster가 Alpöge와 함께한 유체 방정식 연구와 OpenAI와의 경위를 쓴 성명을 정리했다.

## 비평

### 발표문에는 독립 검증이 없고, 검증 상황은 지금도 갱신 중이다

형식화가 끝났다는 발표와 외부 검증은 다르다.
발표문에는 독립적인 검증 결과가 없고 Lean 자료의 주소만 있다.
Lobste.rs에서 bakkot은 LeanProver Zulip의 논의를 근거로 처음에는 다른 누구도 컴파일을 끝내지 못한 듯했으나 한 명이 컴파일을 마치고 비교기(comparator)를 돌리고 있다고 전했다.[^bakkot]
hwayne은 누군가 이 Lean 증명이 틀렸다고 주장한다고 알렸고,[^hwayne] bakkot은 그 사람이 과거에도 여러 주요 결과가 틀렸다고 주장해 온 인물이라며 신뢰하지 않았다.[^bakkot-crank]
이 문서는 Zulip 논의를 직접 읽지 못했고 두 주장의 근거를 확인하지 못했다.
따라서 이 시점의 정확한 진술은 증명이 맞다는 것도 틀렸다는 것도 아니고, 아직 확인 중이라는 것이다.

### 명제의 정합성과 검증기의 신뢰를 어떻게 확인했는지는 발표문 요약에 없다

Lean이 증명을 받아들였다는 사실은 증명된 명제가 리만 가설이라는 사실과 별개이다.
Jweb_Guru가 든 병리 가운데 문제의 오기술은 사람이 정의를 대조해야만 잡힌다.[^Jweb_Guru]
발표문은 형식화가 가정 없이 이루어졌다고만 쓰고,
증명된 명제가 무엇인지와 어떤 검증기로 확인했는지,
명제가 표준 라이브러리의 정의와 맞는지 누가 어떻게 확인했는지는 적지 않는다.
저자는 이를 Lean 자료가 설명해 줄 것으로 본다. 이 문서는 그 자료를 내려받지 않아
확인하지 못했다.

### 25만 쪽의 의미는 입장에 따라 갈린다

Lobste.rs의 orib은 25만 쪽이면 신탁에 답을 구하는 것과 다를 바 없다고 했다.[^orib]
hyperpape는 요약만 봐도 해당 분야 전문가가 접근법의 윤곽을 이해할 만큼 상세하고, 25만 쪽 결과물은 앞으로 몇 달간 사람과 AI의 노력으로 줄어들 것이라고 답했다.[^hyperpape-lobsters]
bitshift는 발표문의 세 번째 쪽을 인용해, 저자 스스로 이상하고 비최적인 선택이 많이 들어갔을 수 있고 짧은 논증이 빨리 나올 것으로 기대한다고 했다.[^bitshift]
marginalia는 AI 모델이 거의 모든 작업에서 장황해지는 경향의 부산물일 가능성이 높아 보인다고 했다.[^marginalia]
이 문서가 읽은 범위에서는 분량이 증명의 본질적 복잡성에서 오는지, 생성 방식에서 오는지를 가릴 근거가 나오지 않았다.

### 연표는 순서와 정확성에 대한 단서가 붙어 있다

연표의 날짜는 시간순으로 놓여 있지 않다.
항목 4와 11은 10월 6일, 항목 19는 10월 19일, 항목 8은 11월 15일로 적혀 있다.
저자는 이 목록을 Claude가 작업 기록을 검색해 만든 대략적인 재구성이라고
소개하고, 일부 설명은 성찰하며 고쳐야 할 것이라고 쓴다.
따라서 이 연표는 논증의 논리 순서도 확정된 작업 일지도 아니다.
증명을 이해하려는 사람이 의지할 것은 Lean 자료이고,
연표는 길잡이로 읽는 것이 맞다.

### 발표 시점에 대한 의문은 발표문의 답과 댓글의 설명이 함께 있다

Lobste.rs에서 nemin은 Anthropic의 상장 직후라는 시점이 조금 계산적으로 느껴진다고 했고,[^nemin] 이에 pja는 상장 전 조용한 기간에는 공개할 수 없었을 것이라고 답했다.[^pja]
rweir는 발표문이 이 문제를 에둘러 다루고 있고 더 오래 묵히는 쪽이 이상해 보인다고 썼다.[^rweir]
발표문은 시점에 관한 냉소적 해석이 사실이 아니라고 밝히고 책임이 자신에게 있다고
말한다.
이는 발표자의 진술이고, 이 문서는 시점의 동기를 확인할 수 없다.

## 인사이트

### 병목이 증명을 찾는 일에서 증명을 이해하고 명제를 대조하는 일로 옮겨 간다

이번 발표가 맞다고 가정하면 새로 드러나는 것은 결과보다 병목의 위치이다.
증명을 찾는 일은 모델과 연산이 맡았고, 사람에게 남은 일은 명제가 맞는지 대조하고 증명을 읽을 수 있게 줄이는 일이다.
발표자도 앞으로의 핵심 과제를 이해 가능한 설명과 단순화라고 적는다.
HN의 puff_pastry는 읽을 수 없는 증명이 쌓이면 실험을 읽고 재현하던 과학에서 믿음의 영역으로 돌아간다는 불안을 말했고,[^puff_pastry] BearOso는 그래도 수학자들은 이해되지 않는 증명에서는 배울 것이 없다고 여길 것이라고 보탰다.[^BearOso]
형식 검증은 틀릴 가능성을 크게 줄이지만 이해를 대신하지는 않는다는 점이 두 댓글의 공통 지점이다.
이는 댓글의 논의를 이 문서가 묶은 것이다.

### 접근의 비대칭이 발표의 공정성 논의로 번진다

qnleigh는 AI 회사와 손잡은 소수의 수학자가 모델이 공개되기도 전에 열린 문제의 정점을 가져가는 것이 불편하다고 썼다.[^qnleigh]
그는 이것이 경제적 효용이 거의 없는 순수수학에서도 자제되지 않는다면 다른 분야의 앞날이 낙관적이지 않다고 말했다.
같은 논의의 다른 쪽에는 수학 자체의 가치와 증명의 이해를 추구하는 수학자에게는 달라진 것이 없다는 반론이 있었다.
이 쟁점은 이번 증명이 맞는지와 별개이고, 결과가 맞든 틀리든 남는다.

### 확인할 관찰

이 발표의 평가를 가를 관찰은 다섯 가지이다.
Lean 증명이 서로 다른 검증기에서 모두 통과하는지,
Lean 명제가 표준 정의의 리만 가설과 GRH인지를 독립된 사람이 확인했는지,
전문가가 쓴 읽을 수 있는 해설이 나오는지,
Masullo의 증명안에서 보고된 문제가 해결되는지,
두 증명이 모두 성립한다면 증명 구조가 얼마나 다른지이다.
다섯 모두 이 문서가 확인하지 못했다.

---

[^hn-title]: Hacker News, [Levent Alpöge claims proof of the Generalized Riemann Hypothesis](https://news.ycombinator.com/item?id=50574968), 2026-11-20

[^gn-title]: GeekNews, [Anthropic 수학자, Claude와 리만 가설 및 일반화 리만 가설을 증명했다고 발표](https://news.hada.io/topic?id=37529), 2026-11-21

[^layer8]: <https://news.ycombinator.com/item?id=50576195>

[^Jweb_Guru]: <https://news.ycombinator.com/item?id=50576769>

[^zug_zug]: <https://news.ycombinator.com/item?id=50578785>

[^djoldman]: <https://news.ycombinator.com/item?id=50576609>

[^xianshou]: <https://news.ycombinator.com/item?id=50575281>

[^gus_massa]: <https://news.ycombinator.com/item?id=50575298>

[^auntienomen]: <https://news.ycombinator.com/item?id=50576368>

[^xyzzyz]: <https://news.ycombinator.com/item?id=50576841>

[^hyperpape]: <https://news.ycombinator.com/item?id=50579078>

[^WilhelmVonWeiner]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_umvm9v>

[^vakil]: Math 216: Foundations of Algebraic Geometry, [Hurried Announcement: Alessandro Masullo GRH](https://math216.wordpress.com/2026/11/20/hurried-announcement-alessandro-masullo-grh/), 2026-11-20

[^chorsestudios]: <https://news.ycombinator.com/item?id=50580850>

[^lysace]: <https://news.ycombinator.com/item?id=50579827>

[^aardvark179]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_mpvneb>

[^dzwdz]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_ae4dpg>

[^bakkot]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_paiozb>

[^hwayne]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_97mxzi>

[^bakkot-crank]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_8tns6f>

[^orib]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_dgmlan>

[^hyperpape-lobsters]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_mhzvj2>

[^bitshift]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_kjsffc>

[^marginalia]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_vpff1r>

[^nemin]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_hy1asw>

[^pja]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_q2zl8x>

[^rweir]: <https://lobste.rs/s/cmifpg/levent_alpoge_claims_proof_riemann#c_r5yynh>

[^puff_pastry]: <https://news.ycombinator.com/item?id=50575311>

[^BearOso]: <https://news.ycombinator.com/item?id=50575682>

[^qnleigh]: <https://news.ycombinator.com/item?id=50578671>
