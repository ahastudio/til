# Conductor, Meta에 합류하며 신규 가입을 닫고 클라우드를 16일 안에 끝낸다

원문: [Conductor is joining Meta](https://www.conductor.build/announcement)

HN 토론: <https://news.ycombinator.com/item?id=50369503> (191점, 203개 댓글)

GN 토론: <https://news.hada.io/topic?id=36639>

## 요약

Conductor는 여러 코딩 에이전트를 작업 공간(workspace)별로 나누어 돌리는
macOS 앱이다.
공동 창업자 Charlie가 쓴 이 공지는 Conductor가 Meta에 합류한다고 알린다.
Conductor는 2025년 7월에 출시되었고, 글은 그때를 에이전트로 코드 대부분을 쓰는
일이 터무니없게 느껴지던 아주 먼 과거라고 표현한다.
글은 다음 인터페이스에 대한 큰 계획이 있고 내년 초에 쓸 수 있는 새것을
내놓겠다고 말하지만, 그것이 무엇인지는 밝히지 않는다.
FAQ도 지금 공유할 수 있는 것이 많지 않다고만 답한다.

일정표는 네 단계다.
11월 4일에 신규 가입과 앱 내려받기가 막히고,
기존 무료 사용자는 프로 요금제로 올릴 수 없으며,
프로 사용자는 프로 기능을 무료로 계속 쓴다.
11월 13일에 Conductor Cloud 작업 공간이 읽기 전용으로 바뀐다.
이때부터는 지난 대화를 읽고 데이터를 내보낼 수 있지만 새 메시지는 보낼 수 없고,
구독 중인 사용자는 환불받는다.
11월 20일에 Conductor Cloud가 종료되고 사용자 데이터 삭제가 시작된다.

로컬 Conductor는 2027년 초까지 새 모델 지원과 치명적 버그 수정을 받으며,
그 뒤 종료 준비에 들어간다고 한다.
클라우드 작업 공간은 앱에서 우클릭해 Transfer to local을 고르면 Mac으로 옮길 수
있고, 전체 데이터는 Settings, Account, Export data에서 내려받는다.
회사는 Conductor 사용자 데이터를 팔거나 학습에 쓴 적이 없고 앞으로도 그러지
않겠다고 하며, 앱이 종료되는 2027년 초에 모든 사용자 데이터를 삭제한다고 적었다.
인수 조건, Meta에서 맡을 역할, 앱의 장기 운명은 공지에 없다.
페이지 하단에는 Conductor from Meta라는 표기와 2026년 Meta 저작권 표시가 있다.

## 분석

### 공지가 약속하는 것과 일정표가 말하는 것

공지 본문은 2027년 초까지 Conductor가 평소처럼 돌아간다고 먼저 말하고,
Conductor Cloud가 몇 주 안에 닫힌다는 사실을 그 뒤에 붙인다.
일정표를 날짜로 계산하면 신규 가입 차단(11월 4일)부터 클라우드 종료(11월
20일)까지 16일이다.
읽기 전용 전환(11월 13일)부터 삭제 시작(11월 20일)까지는 7일뿐이다.
이 간격은 사용자가 대화와 데이터를 내보낼 수 있는 기간이 일주일이라는 뜻이다.
글이 환불, 이전 기능, 내보내기 경로를 먼저 마련해 둔 것은 이 짧은 기간이 문제가
되리라는 점을 알고 있다는 신호로 읽을 수 있다.

HN에서 markerz는 종료가 몇 달에 걸친다고 하지만 일정표에는 새 사용자 차단과 읽기
전용 전환이 앞에 있다고 짚었다.[^markerz]
fn-mote는 몇 달이 아니라 몇 주라고 바로잡았다.[^fn-mote]
Raed667은 종료 일정이 서둘러 정해진 것 같다고 했고,
dgritsko는 Discord 서버에서도 같은 반응이라고 전했다.[^Raed667][^dgritsko]

### 클라우드와 로컬이 다르게 취급되는 이유

공지는 로컬 앱은 2027년 초까지 유지하고 클라우드만 먼저 닫는다.
HN에서 dregitsky는 Conductor Cloud가 작업 공간마다 개발 환경이 미리 설치된 별도
VM을 주어 git worktree가 필요 없게 했다고 설명했다.[^dregitsky]
VM을 운영하는 클라우드는 서버 비용이 계속 들고,
로컬 앱은 사용자 기기에서 돌기 때문에 유지 비용이 거의 없다.
이 차이가 종료 순서를 정했다는 해석은 이 문서의 추론이며,
공지는 이유를 설명하지 않는다.

### 인수 이유에 대한 해석은 댓글에서 갈린다

공지는 인수 이유를 말하지 않으므로 해석은 모두 독자의 추측이다.
adam-eclse는 코딩 하네스(harness) 시장이 매우 경쟁적이고,
Anthropic이나 OpenAI가 구독 요금제로 쓰는 하네스를 API 과금으로 돌리면 사업이
사실상 끝난다는 두려움 속에서 운영했을 것이라고 보았다.[^adam-eclse]
potamic은 제품을 종료하므로 제품이나 사용자 기반이 목적일 수 없다고 했고,
chrisgarand는 Meta가 아직 없는 데스크톱 앱을 몇 주 만에 시작하는 발판으로 쓸 수
있다고 반박했다.[^potamic][^chrisgarand]
어느 쪽이든 공지가 확인해 주는 것은 합류와 종료 일정뿐이다.

## 비평

### 사용자에게 가는 비용은 글 끝에 있고 어조는 앞에 있다

공지는 지금까지 믿고 따라와 준 데 감사하고,
다음에 올 것을 좋아하게 될 것이라고 말한다.
같은 글이 사용자 데이터 삭제를 11월 20일에 시작한다고 쓴다.
stevage는 이 대비를 직접 인용하며 어색함을 짚었다.[^stevage]
habosa는 변경 기록(changelog)에서 클라우드 종료 안내와 맞닿은 줄에 알림음 추가
기능이 적혀 있는 점을 꼬집었다.[^habosa]
roskoes는 먼 과거라는 표현이 오만하게 읽힌다고 했다.[^roskoes]
이런 반응은 취향의 문제일 수 있으나, 어조와 실제 조치의 격차가 신뢰를 깎는다는
점은 공통이다.

### 폐쇄 소스 인수의 위험이 다시 확인되었다

phildenhoff는 이런 경우 회사가 데스크톱 소프트웨어의 한 버전을 오픈소스로
공개했으면 한다고 썼다.[^phildenhoff]
chrisvalleybay는 Conductor가 폐쇄 소스 제품을 인수 후 인력 확보(acquihire)로
흡수하는 사례여서 사용자가 떠날 수밖에 없었다고 했고,
인수합병이 빠른 환경에서는 소스가 필요하다고 주장했다.[^chrisvalleybay]
이 주장이 옳더라도 공지가 소스 공개를 거절했다는 증거는 없다.
공개가 논의되었는지조차 글에서는 알 수 없다.

jahala는 Conductor를 좋아한다면서도 Meta 제품을 쓰지 않겠다며 Claude에게
역공학시키겠다고 했고, 이어 실제로 Conducted라는 MIT 라이선스 프로젝트를
올렸다.[^jahala]
BowBun은 같은 날 팀이 프로젝트를 포크하고 역공학했다고 썼다.[^BowBun]
BowBun의 보고는 에이전트 덕분에 이탈 비용이 낮아졌다는 증거가 된다.
다만 이는 한 팀의 주장이며, 포크가 원본의 기능 전체를 대체하는지는
확인되지 않았다.

### 대안이 많다는 사실이 대체 가능성을 증명하지는 않는다

스레드는 대안 홍보로 채워졌다.
Orca, Paseo, T3 Code, Superset(현 Paradev), boxes.dev, Herdr 등이 올라왔고,
그중 상당수는 만든 사람이 직접 소개했다.[^nwparker][^davecyen]
mattmaroon은 이 경향이 시장 상황을 보여 주는 증거라고 했고,
markush_는 이 정도면 확실한 방어벽(moat)이 없다고
읽었다.[^mattmaroon][^markush_]
inshard는 Claude Desktop이 같은 일을 하지 않느냐고 물었다.[^inshard]

그러나 사용자의 필요가 같다고 단정하기는 어렵다.
dregitsky가 지적했듯 T3 Code는 클라우드를 호스팅하지 않고 사용자가 자기 서버에서
돌려야 하므로, 클라우드 작업 공간이 필요한 사용자에게는 Conductor Cloud의 완전한
대체가 아니다.[^dregitsky]
대안의 수는 지원 범위와 별개이며, 소개한 사람이 이해관계자라는 점도
고려해야 한다.

## 인사이트

### 도구를 고르는 기준에 소스 공개 여부와 종료 조건이 들어간다

freedomben은 새 도구를 워크플로에 들이는 데 극도로 보수적이 되었다고 했고,
paaloeye는 지금 18개월 미만 도구를 쓰는 것은 무책임하다고
했다.[^freedomben][^paaloeye]
gdulli는 기술 스택에 더하는 모든 것은 부채라고 했다.[^gdulli]
이 반응은 과장이 섞였으나, 에이전트 도구 시장에서 제품 수명이 1년 남짓일 수
있다는 점은 Conductor가 2025년 7월 출시 후 1년 4개월 만에 신규 가입을 닫은
사실로 뒷받침된다.

따라서 도입 평가에는 기능 외에 두 항목이 들어가야 한다.
데이터를 내보낼 수 있는 형식이 있는가, 그리고 제품이 종료되어도 로컬에서 계속
돌릴 수 있는가이다.
Conductor는 둘 다 일정 수준 제공했고, 로컬 우선 도구는 이 위험을 줄인다.
mksadoughi는 별도 도구 없이 Claude Code만으로 세션마다 git worktree를 하나씩
쓰고 조율 세션 하나가 일을 나눠 주는 방식으로 다중 에이전트를 돌린다고
했다.[^mksadoughi]
이는 종료될 제품이 없는 가장 단순한 대안이다.

### 에이전트 도구는 만드는 비용이 떨어져 인수가 제품이 아니라 팀을 사는 일이 된다

sksum은 회사가 인력, 사용량이 늘어나는 제품,
경쟁에서 시간을 벌어 주는 제품을 사며, 이 순서로 실질 가치가 줄고 자기기만이
는다고 썼다.[^sksum]
brainless는 LLM 때문에 한 사람이 월 구독료 몇 개로 앱을 만드는 시대라서 사용자
이탈이 자연스럽다고 보았다.[^brainless]
cgio는 제품 설계는 코드 작성과 다르고 그 기술이 Meta에는 가치가 있다고
반박했다.[^cgio]

공지가 제품을 닫는다는 사실은 sksum의 순서에서 첫 번째 항목,
즉 인력 확보에 무게가 실린다는 읽기와 맞는다.
이것은 추론이며 Meta가 밝힌 바는 없다.
확인 방법은 Charlie의 말대로 내년 초에 나올 새 제품이 Conductor의 설계와 얼마나
이어지는지 보는 것이다.
이어지지 않으면 인력 확보였다는 읽기가 강해지고,
이어지면 제품을 사서 다시 쓴 것이 된다.

### 공동 창업자가 스레드에 남긴 글은 인사 하나뿐이다

Charlieholtz는 스레드에서 공동 창업자라고 밝히며 팀이 질문에 답하기 위해 있다고
말했고 개인 이메일도 남겼다.[^Charlieholtz]
doublerabbit가 왜 회사를 팔았느냐고 물었을 때 답한 사람은 다른 댓글러였고,
signatoremo는 사용자가 위험을 알고 선택했다고 했다.[^doublerabbit][^signatoremo]
이 스레드에서 Charlieholtz가 쓴 댓글은 이 하나뿐이어서,
인수 이유나 일정이 서둘러진 이유에 대한 설명은 스레드에 없다.
이 부재는 공지가 비워 둔 항목(인수 조건,
계획의 구체 내용)이 이 자리에서도 채워지지 않았다는 뜻이다.
독자가 알 수 있는 것은 이메일로 도움을 받을 수 있다는 점뿐이다.

---

[^markerz]: <https://news.ycombinator.com/item?id=50369878>

[^fn-mote]: <https://news.ycombinator.com/item?id=50373981>

[^Raed667]: <https://news.ycombinator.com/item?id=50372065>

[^dgritsko]: <https://news.ycombinator.com/item?id=50372104>

[^dregitsky]: <https://news.ycombinator.com/item?id=50374117>

[^adam-eclse]: <https://news.ycombinator.com/item?id=50370712>

[^potamic]: <https://news.ycombinator.com/item?id=50374949>

[^chrisgarand]: <https://news.ycombinator.com/item?id=50375735>

[^stevage]: <https://news.ycombinator.com/item?id=50372749>

[^habosa]: <https://news.ycombinator.com/item?id=50374789>

[^roskoes]: <https://news.ycombinator.com/item?id=50374164>

[^phildenhoff]: <https://news.ycombinator.com/item?id=50369888>

[^chrisvalleybay]: <https://news.ycombinator.com/item?id=50376199>

[^jahala]: <https://news.ycombinator.com/item?id=50370152>

[^BowBun]: <https://news.ycombinator.com/item?id=50374304>

[^mattmaroon]: <https://news.ycombinator.com/item?id=50377383>

[^markush_]: <https://news.ycombinator.com/item?id=50374681>

[^inshard]: <https://news.ycombinator.com/item?id=50371521>

[^freedomben]: <https://news.ycombinator.com/item?id=50370073>

[^paaloeye]: <https://news.ycombinator.com/item?id=50370133>

[^gdulli]: <https://news.ycombinator.com/item?id=50370065>

[^mksadoughi]: <https://news.ycombinator.com/item?id=50373638>

[^nwparker]: <https://news.ycombinator.com/item?id=50372338>

[^davecyen]: <https://news.ycombinator.com/item?id=50372547>

[^sksum]: <https://news.ycombinator.com/item?id=50374654>

[^brainless]: <https://news.ycombinator.com/item?id=50374788>

[^cgio]: <https://news.ycombinator.com/item?id=50377213>

[^Charlieholtz]: <https://news.ycombinator.com/item?id=50370169>

[^doublerabbit]: <https://news.ycombinator.com/item?id=50370403>

[^signatoremo]: <https://news.ycombinator.com/item?id=50372780>
