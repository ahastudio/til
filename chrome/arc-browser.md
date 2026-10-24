# Arc 브라우저가 2026년 12월 22일에 종료되고 Dia로 이어진다

> A farewell to Arc

<https://arc.net/>

HN 토론: <https://news.ycombinator.com/item?id=50197601> (274점, 235개 댓글)

GN 토론: <https://news.hada.io/topic?id=35834>

## 요약

Arc 개발팀이 2026년 12월 22일에 Arc를 종료한다고 알린 공지다.
공지의 이유는 하나다.
브라우저를 안전하게 유지하는 일에는 꾸준하고 전담적인 작업이 필요하고, 그 필요는
AI 시대에 커지고 있으므로 엔지니어링팀과 보안팀을 새 브라우저 Dia에 모으겠다는
것이다.
Dia는 오늘의 보안 기준에 맞춰 처음부터 만든 브라우저라고 소개한다.

이전 방법으로 공지는 네 가지를 약속한다.
비밀번호, 북마크, 확장 프로그램, 방문 기록이 Dia로 넘어온다.
Spaces, Folders, Tab Groups는 데이터를 유지한 채 가져온다.
Dia가 안정성, 속도, 보안에서 Arc의 벤치마크를 넘어섰다고 한다.
Arc에서 쓰던 브라우저 기능은 Dia에서 무료이고 AI는 선택 사항이다.
공지는 Arc를 만든 팀이 Dia를 만든 팀과 같다고 강조하며 끝난다.

종료 일정의 세부는 GeekNews가 정리한 Arc 안내에 있다.
2026년 10월 22일부터 새 Arc 계정을 만들 수 없고, 11월 23일부터 모바일 Arc
Search의 AI 기능과 로그인, 탭 동기화가 꺼진다.
12월 22일에 macOS와 Windows용 Arc가 작동을 멈추고 모든 계정이 비활성화되며, 계정
관련 개인 데이터는 이후 30일 이내 삭제된다.
Android 버전은 그날 완전히 종료되고, iOS에서는 AI와 로그인과 동기화가 없는
가벼운 브라우저로 남는다.[^gn-summary]

## 분석

### 글의 중심 주장: 종료의 이유를 보안 인력의 집중으로 설명한다

공지는 종료를 시장 사정이나 사용자 수로 설명하지 않는다.
이유로 내세운 것은 보안 유지에 드는 인력이 AI 시대에 늘어난다는 점이고, 그래서
한 제품에 인력을 모아야 한다는 논리다.
이 설명은 결정을 기술적 필연처럼 보이게 한다.
브라우저 보안을 두 제품에서 따로 하기 어렵다는 말은 일리가 있지만, 왜 남기는
제품이 Dia여야 하는지는 설명하지 않는다.
그 선택의 이유는 공지 안에서 Dia가 오늘의 보안 기준으로 처음부터 만들어졌다는 한
문장뿐이다.

### 전환 비용을 낮추는 문장이 공지의 절반을 차지한다

공지의 약 절반은 이전이 쉽다는 이야기다.
가져올 수 있는 항목을 나열하고, 기능은 무료이며 AI는 선택이라고 분명히 한다.
이는 떠나는 사용자가 가장 먼저 걱정할 것(데이터 손실, 가격, 강제 AI 기능)을 먼저
막으려는 구성이다.
같은 팀이 만들었다는 마지막 문장은 신뢰를 이어 붙이려는 장치다.

### 종료가 한 번의 결정이 아니라 1년 반의 과정이었다는 맥락

HN에서 jerlam은 Arc의 개발 중단이 2025년 5월에, Atlassian의 인수가 2025년 9월에
있었다고 짚었다.[^jerlam]
allenleee는 2025년 5월 CEO 공개 서한에서 활발한 기능 개발은 끝나지만 Arc는 계속
유지된다고 안심시켰다고 전했다.[^allenleee]
이 서술을 따르면 이번 종료는 유지 약속에서 종료까지의 마지막 단계다.
다만 이 문서는 서한과 기사를 직접 열어 보지 않았고, 두 사람의 설명으로만 전한다.

## 비평

### 안전 때문이라는 설명은 선택의 근거가 되지 못한다

AI 시대에 보안 작업이 늘어난다는 문장은 일반론이다.
impure는 이 문장을 두고 AI가 오히려 작업을 줄여 줘야 하는 것 아니냐고
되물었다.[^impure]
공지는 어떤 위협이 늘었는지, Arc의 어떤 구조가 보안 유지를 어렵게 하는지 밝히지
않는다.
검증 가능한 정보가 없는 이유는 결정을 설명하는 이유가 아니라 결정의 포장으로
읽힐 수 있다.
이 문서가 확인한 범위에서 공지에는 보안 사고나 유지 비용에 관한 수치가 없다.

### 같은 팀이라는 말이 신뢰 문제를 풀지 못한다

공지가 신뢰의 근거로 내세운 같은 팀이라는 점이 오히려 불신의 이유가 됐다.
jdgoesmarching은 유지를 약속한 뒤 브라우저를 접은 사람들이 만든 브라우저로 옮길
이유가 없고, 인수한 Atlassian의 기록도 좋지 않다고 썼다.[^jdgoesmarching]
asadotzler는 지난번 제품에서 사용자를 저버린 곳에 다시 돌아가 같은 일이 없을
것이라 믿느냐고 물었다.[^asadotzler]
GeekNews의 colus001도 Arc를 버렸는데 Dia를 쓸 이유가 있느냐고 같은 취지로
적었다.[^colus001]
공지에는 이 질문에 대한 답, 예를 들어 Dia에 대한 유지 기간 약속이 없다.

### 이전이 쉽다는 주장과 실제로 옮긴 사람들의 평가가 다르다

공지는 Dia가 Arc의 기능을 갖췄다고 하지만 써 본 사람들은 빠진 기능을 짚는다.
jhaile는 Arc에서 Peek, Air Traffic Control, 중첩 폴더가 아쉽다고 했고,[^jhaile]
simjnd는 요청서를 내고 설문에 답했는데도 강력한 기능이 Dia로 오지 않아 Arc로
돌아왔다고 했다.[^simjnd]
반면 falloon은 한 해 식힌 뒤 Dia를 써 봤더니 AI 기능을 끌 수 있고 잘 설계된
브라우저라 만족한다고 했다.[^falloon]
평가는 갈리고, 같은 기능 이전이 사용자 습관에 따라 다르게 느껴진다는 점만
확인된다.

### Dia의 가격과 AI 중심 방향은 공지에서 가려진다

공지는 기능이 무료이고 AI는 선택이라고 말한다.
kvam은 Dia의 요금제 페이지에 월 100달러 요금과 AI 아침 브리핑 같은 핵심 기능이
있어 옮기지 않겠다고 썼다.[^kvam]
다른 사용자 artdigital은 업그레이드 항목이 사라져 인수 후 모두에게 무료가 된 줄
알았다며, 실제 화면에서 확인한 바를 적었다.[^artdigital]
두 증언이 어긋나므로 Dia의 현재 요금 구조는 이 문서가 확인하지 못했다.

## 인사이트

### 사용자가 낸 신뢰의 값은 제품이 아니라 약속에 걸려 있었다

HN의 불만은 대부분 기능이 아니라 약속에 모인다.
유지하겠다던 약속이 깨진 뒤에는 이전 도구가 아무리 쉬워도 새 제품을 같은 신뢰로
쓰기 어렵다.
이는 유료나 VC 투자 제품에서 반복되는 구조다.
an0malous는 VC 투자를 받은 제품은 믿지 말고 보조금이 붙은 가격을 누리되 대비책을
두라고 했고,[^an0malous]
colesantiago는 VC 없이는 거의 모든 스타트업이 생존하지 못한다고
반박했다.[^colesantiago]
둘의 대립에서 남는 실무 기준은 하나다.
핵심 작업 흐름이 닫힌 클라이언트 앱에 걸려 있다면, 종료에 대비해 데이터를
내보내는 경로가 있는지부터 확인해야 한다.

### 오픈소스 공개 요구는 종료 때마다 반복되지만 조건이 다르다

slipwalker는 Arc를 오픈소스로 공개하면 신뢰한 사용자의 뒷맛이 나아질 것이라
했다.[^slipwalker]
hbn은 Dia에서 계속 쓰는 독자 프레임워크가 있어 공개를 원하지 않을 것이라는
이야기를 들은 적이 있다고 했고,[^hbn]
DrammBA는 클라이언트 앱이라 다른 사람이 대신 공개할 수 있다고 했다.[^drammba]
공지는 소스 공개에 대해 아무 말도 하지 않는다.
종료 후 공개가 일어나려면 코드가 Dia와 얼마나 얽혀 있는지, 소유 회사가 이를
원하는지가 조건이며, 공지의 침묵은 둘 중 어느 쪽도 확인해 주지 않는다.

### 대안이 정리되는 방식이 시장의 빈자리를 보여 준다

종료 소식에 사용자들이 가장 많이 언급한 이름은 Zen, Helium, Crest였다.
jamie_ca는 Dia로 방향이 바뀔 때부터 Zen으로 옮겼고 사이드바 탭, 고정 탭, 전역
북마크, 작업 공간 같은 Arc의 요소를 가져왔다고 썼다.[^jamie_ca]
silvertab은 Crest가 Chrome과 Safari 엔진을 모두 쓸 수 있고 Arc의 기능을 재현하는
것이 목표지만 아직 미숙하다고 했다.[^silvertab]
mostlysimilar는 Firefox에 이미 있는 기능이 아니냐고 물었고,[^mostlysimilar]
SomeonesAccount는 Arc의 UX가 Chrome이나 Firefox보다 훨씬 낫다고
반박했다.[^someonesaccount]
여기서 드러나는 사실은 사용자가 좋아한 것이 엔진이나 AI가 아니라 사이드바 중심의
탭 UX였고, 그 UX를 이어받겠다는 후보가 여럿 나선다는 점이다.
이를 가를 관찰은 Arc가 멈춘 뒤 이 후보들 중 어느 쪽이 Arc 사용자를 실제로
흡수하는지다.

### 이 글을 읽는 방법

Arc 사용자라면 12월 22일 전에 두 가지를 해야 한다.
Arc 설정의 Export Data로 데이터를 내보내거나 Dia로 가져오는 일, 그리고 다른
브라우저로 옮길 탭을 링크 목록으로 저장하는 일이다.
Arc를 한동안 쓰지 않았어도 종료 전에 다시 설치해 앱 안에서 내보낼 수 있다고
안내돼 있다.[^gn-summary]
이 공지의 주장을 가를 관찰은 두 가지다.
Dia가 종료 이후에도 몇 년간 같은 형태로 유지되는지, 그리고 Dia의 요금 구조가
무료 기능 약속과 맞는지다.
둘 다 확인되기 전까지는 Dia로 옮기는 것도 하나의 선택일 뿐 안전한 종착지가
아니다.

---

[^gn-summary]: GeekNews, [Arc 브라우저와의 작별, 12월 22일 서비스 종료](https://news.hada.io/topic?id=35834), 2026-10-23

[^jerlam]: <https://news.ycombinator.com/item?id=50199270>

[^allenleee]: <https://news.ycombinator.com/item?id=50198258>

[^impure]: <https://news.ycombinator.com/item?id=50198184>

[^jdgoesmarching]: <https://news.ycombinator.com/item?id=50198480>

[^asadotzler]: <https://news.ycombinator.com/item?id=50200684>

[^colus001]: <https://news.hada.io/topic?id=35834#cid68293>

[^jhaile]: <https://news.ycombinator.com/item?id=50199454>

[^simjnd]: <https://news.ycombinator.com/item?id=50198502>

[^falloon]: <https://news.ycombinator.com/item?id=50198096>

[^kvam]: <https://news.ycombinator.com/item?id=50199291>

[^artdigital]: <https://news.ycombinator.com/item?id=50202880>

[^an0malous]: <https://news.ycombinator.com/item?id=50197878>

[^colesantiago]: <https://news.ycombinator.com/item?id=50198125>

[^slipwalker]: <https://news.ycombinator.com/item?id=50197925>

[^hbn]: <https://news.ycombinator.com/item?id=50200225>

[^drammba]: <https://news.ycombinator.com/item?id=50201276>

[^jamie_ca]: <https://news.ycombinator.com/item?id=50197962>

[^silvertab]: <https://news.ycombinator.com/item?id=50200698>

[^mostlysimilar]: <https://news.ycombinator.com/item?id=50198635>

[^someonesaccount]: <https://news.ycombinator.com/item?id=50198906>
