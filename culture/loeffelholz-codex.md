# Löffelholz Codex: 1505년 뉘른베르크 기사의 공구 책을 AI와 함께 읽는 프로젝트

<https://loeffelholz-codex.org/en/>

HN 토론: <https://news.ycombinator.com/item?id=50230917> (134점, 69개 댓글)

GN 토론: <https://news.hada.io/topic?id=35980>

## 소개

Löffelholz Codex는 1505년에 뉘른베르크의 귀족이자 기사인 Martin Löffelholz가
쓰기 시작한 책이다.
일기도 가문 연대기도 아니고 공구 책이다.
교체할 수 있는 날을 끼우는 드릴, 나사와 그것을 깎는 도구, 바이스가 달린 작업대,
바퀴 달린 회전의자, 치워 둘 수 있는 나선 계단, 부품 단위로 분해해 그린 석궁,
수은을 채운 흔들 요람이 그려져 있다.
원본은 크라쿠프에 있고, 전체가 디지털화돼 퍼블릭 도메인으로 공개돼 있다.
사이트는 이 책이 500년 넘게 처음부터 끝까지 읽힌 적이 없다고 하며, 전사본도
편집본도 번역본도 없다고 한다.

사이트는 2026년에 Dirk Schornstein이 시작한 비영리 취미 프로젝트다.
그는 스스로를 공학 학위를 가진 엔지니어(Diplom-Ingenieur)이자 기술 애호가라고
소개한다.
책은 154쪽이고 그중 127쪽을 검토했고 27쪽은 아직 하지 않았다고 한다.
텍스트는 CC BY-SA 4.0이고, 원본 이미지는 야기엘론스카 도서관(Biblioteka
Jagiellońska)의 것이다.

## 페이지 구성과 검증 상태

154쪽마다 별도 페이지가 있고, 진행 정도에 따라 다음이 들어 있다.
가장 해상도가 좋은 복제 이미지, 무엇이 그려졌는지를 알리는 제목, 원래 철자를
그대로 둔 전사, 현대 영어 번역, 그 물건이 무엇이고 어떻게 작동하는지에 대한 해석
제안이 있다.
오늘날 눈으로 보면 놀라운 점, 열린 질문, 장인에게 던지는 질문도 있다.

신뢰도는 페이지마다 다르게 표시된다.
특별한 표시가 없는 페이지는 편집 검토를 거쳤고, 원본 그림과 이미 출판된 연구,
전사, AI가 낸 설명 제안을 대조해 다시 썼다고 한다.
맨 위에 raw transcription이라는 표시가 있는 페이지는 초안이다.
AI가 전사와 해석을 만들었고, 저자는 읽어 봤지만 줄 단위로 확인하고 고치지는
않았다고 한다.
불확실하게 읽은 곳은 색으로 표시되고, 판독하지 못한 곳은 빈칸으로 남는다.

검토 전 페이지의 예로 76r이 있다.
이 페이지는 편집 검토를 거치지 않았고, 전사와 해석을 기계가 만들었으며 읽기가
틀렸을 수 있다고 밝힌다.[^f076r]
연구자가 읽고 고칠 수 있도록 공개하되, 사람이 내용을 확인할 때까지 검색 엔진
색인에서는 제외한다고 한다.[^f076r]

반면 3v 페이지는 검토를 거친 쪽이다.
Pia Rudolph가 쓴 목록의 설명(KdiH 49a.4.1)을 인용하고, 전사에서 불확실한 글자를
대괄호로 표시하며, 번역과 해석 제안을 붙인다.[^f003v]
이 페이지는 그림이 위아래가 뒤집혀 그려진 손 드릴(brace)이며, 한 손잡이에 날 세
개가 맞는 구조라고 해석한다.[^f003v]
AI가 그린 시각화는 역사적 출처가 아니라는 표시와 함께 붙는다.[^f003v]

AI 시각화 모음은 기기 48개를 다룬다.
모든 이미지는 AI가 생성했고 사진도 역사적 출처도 아니며, 해석 제안이라는 도장이
이미지가 페이지 밖으로 나가도 보이게 남는다고 한다.[^aivis]

## 비평

### 검증 표시가 있어도 읽는 사람에게 거르는 부담이 남는다

HN에서 가장 많은 반응을 모은 것은 AI 사용에 대한 불신이었다.
BlackRabbit1은 사이트 전체가 LLM이 쓰고 분석한 것처럼 보이고, 그래서 모든 줄의
정확성과 출처를 확인해야 하므로 학술적 가치가 크게 떨어진다고
했다.[^BlackRabbit1]
kreyenborgi는 AI 이미지와 글 때문에 신뢰가 줄어든다고 했다.[^kreyenborgi]

사이트는 이에 대한 장치를 이미 갖고 있다.
검토 전 페이지는 표시하고 검색 색인에서 뺀다.
katzenq는 이 경고를 높이 평가하면서도 기본적으로는 믿을 수 없는 스팸이라고
했다.[^katzenq]
moffers는 저자가 소개글에서 일부만 검증됐다고 밝혔고, LLM을 썼다는 것만으로
가치가 낮아지지는 않는다고 반박했다.[^moffers]
amelung는 사이트가 출처 목록에서 KdiH 목록(kdih.badw.de)을 많이 끌어다 쓴다는
점에서 진짜 같다고 했다.[^amelung]

이 논쟁에서 눈여겨볼 지점은 검증 표시의 방향이다.
사이트는 검토 전 페이지에만 표시를 붙이고, 표시가 없는 페이지는 검토했다는
뜻이라고 한다.
독자는 표시가 없다는 사실을 근거로 검토를 믿어야 하고, 이 문서가 연 페이지에서는
무엇을 어떻게 고쳤는지 확인할 수 없었다.
HN의 peri-cl이 76r을 보고 이것은 지금까지 들어 본 가장 비효율적인 부호이며
사실상 일진법이라고 농담한 것은, 마침 사이트가 검토 전이라고 밝힌 바로 그
페이지였다.[^peri-cl]
농담은 맞을 수 있지만, 근거가 된 해석이 기계가 만든 것이라는 점은 이 문서가 읽은
범위의 댓글에서 언급되지 않았다.

### AI 시각화는 원본의 모호함을 확정된 모습으로 바꾼다

kornork는 AI 이미지가 이 용도에서는 오히려 역효과이고 오해를 부른다고
했다.[^kornork]
원본 그림은 원근과 비율이 어긋나고 세부에 의문이 많은데, AI는 그 의심스러운
세부를 그대로 실제인 것처럼 그려 내기 때문이라는 것이다.[^kornork]
현존하는 실제 유물이 있다면 그 이미지를 찾아 쓰는 편이 낫다고도 했다.[^kornork]
mcbishop은 자신이 본 도구 페이지 하나에는 실제 유물이 있었다고
알렸다.[^mcbishop]

사이트는 이 위험을 알고 있는 것으로 보인다.
시각화 모음은 모든 이미지가 AI 생성물이고 사진이 아니라고 밝히며, 불확실하면
이미지 옆에 그렇게 적는다고 한다.[^aivis]
다만 그 표시는 이미지가 놓인 자리에서 효과가 있고, 표시를 읽지 않고 이미지만
가져가는 독자에게는 소용이 없다.
도장이 이미지에 남는다는 설계는 이를 막으려는 것이다.
이 도장이 실제 확산 경로에서 얼마나 보이는지는 이 문서가 확인하지 못했다.

### 아무도 읽지 않았다는 이야기와 출처 목록 사이의 간격

홈페이지는 500년 넘게 아무도 이 책을 끝까지 읽지 않았다고 말한다.
같은 사이트의 출처 페이지는 Pia Rudolph의 폴리오별 설명을 표준 설명이라고 부르며
이것이 없으면 페이지 단위 연구가 거의 불가능했을 것이라고 적는다.[^sources]
그 밖에 1933년의 Feldhaus와 Reicke 논문, 2021년 Hohrath 논문, f.73v의 영어
번역(Lost Art Press, 2018)도 목록에 있다.[^sources]
독일어 위키백과 문서는 자세하고 출처가 꼼꼼하다고 소개한다.[^sources]
FAQ의 표현은 더 조심스러워서, 모든 쪽을 읽고 해석한 출판본은 알려진 바 없다고만
한다.

jacquesm은 한 사람이 AI 없이는 이 규모의 일을 할 수 없다는 저자의 말이 맞지
않는다고 했다.[^jacquesm-claim]
자신의 삼촌이 이런 일을 했고 보통 한두 해가 걸려 훨씬 낫게 해냈다는
것이다.[^jacquesm-claim]
AI는 며칠로 줄여 주지만 거의 쓸모없게 만들고, 이 프로젝트의 가장 큰 기여는 덜
알려진 책을 알리는 일이라고 했다.[^jacquesm-claim]
Planktonne은 책을 쓴 기사가 AI도 컴퓨터도 없이 더 큰 프로젝트를 해냈다고
짚었다.[^Planktonne]
반면 scrollop은 저자가 책을 발견하는 일이 열정이고 남에게 보이는 페이지를 만드는
일은 지루하니, 시간을 아끼도록 AI를 쓰는 것을 지지했다.[^scrollop]

이 논쟁은 속도의 문제로 보이지만 실제로는 책임의 문제다.
아무도 읽지 않았다는 서사는 프로젝트의 의미를 키우고, 그 서사가 사실에서
멀어질수록 AI가 만든 초안을 검증하는 부담도 독자에게 넘어간다.

## 인사이트

### 해석을 공개할 때는 페이지마다 신뢰 수준을 보이게 한다

이 프로젝트에서 배울 점은 AI를 썼다는 사실보다 쓴 방식이다.
검토 전 페이지를 눈에 띄게 표시하고, 검색 색인에서 빼고, 시각화에는 출처가
아니라는 표시를 붙이는 것은 AI가 만든 초안을 공개하는 프로젝트가 갖춰야 할
최소한의 장치다.
HN의 논쟁은 이 장치가 있어도 독자가 불신을 거두지 않을 수 있음을 보여 준다.

실용적인 결정 규칙은 읽는 순서다.
복제 이미지와 전사를 먼저 보고, 해석은 그다음에 읽고, 검토 표시가 없는
페이지에서도 중요한 주장은 Pia Rudolph의 목록 같은 독립된 자료로 확인한다.
출처 페이지가 목록과 문헌을 공개하고 있으므로 확인 경로는 열려 있다.[^sources]

### 옛 책이 지금의 질문과 만나는 방식

peri-cl의 일진법 농담과 함께 다른 반응도 있었다.
WillAdams는 CNC 기계로 만든 캘리퍼스 프로젝트를 떠올리며 각 물건을 재현할 디지털
파일을 만드는 일이 흥미롭겠다고 했다.[^WillAdams]
jimmySixDOF는 당시 기사치고는 3차원 원근 묘사가 꽤 괜찮다고 했다.[^jimmySixDOF]
이런 반응은 사이트의 재현 코너나 장인에게 던지는 질문과 닿아 있다.
AI 논쟁 때문에 가려졌지만, 프로젝트가 목표로 하는 것은 물건이 실제로 어떻게
작동하는지를 사람이 확인하는 일이다.

### 이 글을 읽는 방법

이 사이트는 프로젝트가 자신을 소개하는 글이므로, 페이지 수와 검토 수는 사이트의
주장으로 읽어야 한다.
HN의 비판도 사이트가 AI를 쓴 방식에 대한 인상이며, 개별 페이지의 오류를 세어 본
것이 아니다.
이 문서도 76r과 3v 두 페이지만 열어 보았다.

이 판단을 가를 관찰은 두 가지다.
첫째, 검토를 마쳤다는 페이지 열 쪽 안팎의 전사를 복제 이미지와 Pia Rudolph의
목록 설명에 맞대어 오류율을 세는 것이다.
둘째, AI 시각화 몇 장에서 원본 그림에 없는 세부를 찾아 표시하는 것이다.
첫째는 검토를 거쳤다는 표시를 믿어도 되는지를, 둘째는 kornork의 우려가 실제로
일어나는지를 가른다.

---

[^f076r]: Löffelholz-Codex.org, [Folio 76r: The Code - Löffelholz Codex](https://loeffelholz-codex.org/en/codex/f076r.html)

[^f003v]: Löffelholz-Codex.org, [Folio 3v: The Brace with Interchangeable Bits - Drawn Upside Down - Löffelholz Codex](https://loeffelholz-codex.org/en/codex/f003v.html)

[^aivis]: Löffelholz-Codex.org, [AI Visualizations - Löffelholz Codex](https://loeffelholz-codex.org/en/explore/ai-visualizations.html)

[^sources]: Löffelholz-Codex.org, [Sources - Löffelholz Codex](https://loeffelholz-codex.org/en/history/sources.html)

[^BlackRabbit1]: <https://news.ycombinator.com/item?id=50231701>

[^kreyenborgi]: <https://news.ycombinator.com/item?id=50231476>

[^katzenq]: <https://news.ycombinator.com/item?id=50231826>

[^moffers]: <https://news.ycombinator.com/item?id=50231858>

[^amelung]: <https://news.ycombinator.com/item?id=50231999>

[^peri-cl]: <https://news.ycombinator.com/item?id=50231699>

[^kornork]: <https://news.ycombinator.com/item?id=50232515>

[^mcbishop]: <https://news.ycombinator.com/item?id=50232626>

[^jacquesm-claim]: <https://news.ycombinator.com/item?id=50232717>

[^Planktonne]: <https://news.ycombinator.com/item?id=50232998>

[^scrollop]: <https://news.ycombinator.com/item?id=50232662>

[^WillAdams]: <https://news.ycombinator.com/item?id=50231625>

[^jimmySixDOF]: <https://news.ycombinator.com/item?id=50232074>
