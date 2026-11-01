# AI 시대에 정말 지쳤는가: 병렬 작업과 검증 부담이 만든 피로

Ask HN: [Ask HN: Are you tired too in this AI era?](https://news.ycombinator.com/item?id=50301479)

GN 토론: <https://news.hada.io/topic?id=36335>

## 요약

2026-10-30에 Hacker News에 올라온 이 질문은 148점, 141개 댓글을 받았다.
질문자는 AI 덕분에 훨씬 많은 일을 할 수 있게 되었지만 예전보다 훨씬
피곤하다고 적었다.
병렬로 벌어지는 여러 일을 추적해야 하고, 생성된 방대한 글을 읽어야 하며,
끊임없는 감시와 결정과 맥락 전환이 짓누른다는 것이다.
질문자는 정신적 과부하를 늘리지 않고 AI를 쓰는 방법이 있는지 묻고,
상사에게 해고당하지 않을 만큼 경쟁력도 유지하고 싶다고 덧붙였다.

답글은 크게 세 갈래로 갈린다.
첫째는 질문에 동의하는 쪽이다.
이들은 병렬 작업의 맥락 전환, 끝없는 검토,
직접 코드를 짜며 얻던 보람의 상실을 피로의 원인으로 든다.
둘째는 오히려 에너지가 늘었다는 쪽이다.
이들은 스스로 속도를 정하는 개인 프로젝트, 경험에서 나온 판단 기준,
만드는 일 자체에 대한 애정을 이유로 든다.
셋째는 피로의 원인이 AI가 아니라 직장의 압박, 과장된 홍보,
경제 상황이라고 보는 쪽이다.

대처법은 병렬 작업 수를 줄이기, 쉬는 시간 계획하기,
작업 상태를 기록해 두는 도구 만들기, 코드의 일부를 직접 맡기,
자동 완성 중심으로 쓰기, 에이전트 말투 바꾸기처럼 구체적이다.
다만 대부분은 한 사람의 경험이며 효과가 검증된 것은 아니다.

## 분석

### 질문이 가리킨 피로는 생산이 아니라 관리에서 온다

질문자가 든 원인은 모두 만드는 일이 아니라 지켜보는 일에 속한다.
병렬 추적, 생성물 읽기, 감시, 결정, 맥락 전환(context switching)이 그것이다.
답글은 이 목록이 개인의 푸념이 아니라 반복해서 확인되는 패턴임을 보여 준다.

martypitt는 작업 흐름 4~5개를 동시에 돌리며 검토를 얼마나 해야 하는지,
테스트 커버리지가 높으면 바로 병합해도 되는지를 계속 불안해한다고
적었다.[^martypitt]
justforfunhere는 Claude Code 할당량을 다 쓰려고 프로젝트 네댓 개를 동시에
돌렸다가 처음의 흥분이 가라앉은 뒤 몹시 괴로웠고,
한 번에 하나로 돌아가서 정신을 되찾았다고 말했다.[^justforfunhere]
FailMore는 초기에 Claude 세션을 여덟 개까지 돌렸지만 지금은 두세 개로 줄였고,
그래도 AI 이전보다 열 배쯤 생산적이라고 적었다.[^failmore]
victorbuilds는 한 가지를 제대로 하는 편이 에이전트 다섯 개를 돌보는 것보다
낫다고 했다.[^victorbuilds]

반대 방향의 증언도 있다.
PippaSedai는 세션 관리가 힘들어서 알림과 색 구분이 있는 창 관리자를 AI로
만들었고, 지금은 작업 트리를 나눠 8~12개 세션을 편하게 돌린다고
적었다.[^pippasedai]
philipp-gayret는 에이전트를 더 오래 자율적으로 돌려 중단을 줄이는 방식을 택했고,
이를 위해서는 먼저 자동화 체계를 직접 만들어야 한다고 했다.[^philipp-gayret]
두 증언은 병렬 작업 자체보다 작업을 이어받는 비용이 피로를 가른다고 읽을
수 있게 한다.

### 검토 부담은 개인에서 팀으로 번진다

피로의 두 번째 축은 읽어야 하는 생성물의 양이다.
fabioborellini는 길고 질 낮은 글을 읽다 보면 퇴근할 때 읽고 쓰는 능력이
떨어지고, 평소에 하지 않던 오타를 낸다고 적었다.[^fabioborellini]
Retr0id는 남이 만든 생성물은 아예 읽지 않고,
자기 쪽 생성물은 통독하는 대신 질문하며 파악한다고 했다.[^retr0id]

팀에서는 이 부담이 연쇄로 이어진다.
Gigachad는 관리자가 Claude로 티켓을 만들고,
개발자가 그것을 통째로 Claude에 넣어 PR을 올리면,
검토자는 4,000줄을 볼 시간이 없어 아무도 이해하지 못한 채 배포된다고
설명했다.[^gigachad-chain]
yulaow는 동료가 전부 AI로 만든 PR을 올리고 문제를 고치는 어려운 일을 검토자에게
떠넘기는 상황이 가장 지친다고 했다.[^yulaow]
orwin은 테스트를 일일이 검토할 여력이 없어 일주일에 한 번 AI에게 테스트를
리팩터링시킨다고 적었다.[^orwin]

테스트를 검토하느냐는 질문(hasley)에 대한 답은 갈렸다.[^hasley]
KptMarchewa는 검토하지 않으며 몇 달 동안 AI가 테스트를 조작하는 것을 본 적이
없다고 답했다.[^kptmarchewa-tests]
40PT는 사람들이 통합 테스트와 종단 간 테스트만 쓰게 해서 그대로 커밋하며,
단위 테스트는 모델이 올바른 코드를 만들도록 돕는 용도일 뿐이라고 적었다.[^40pt]
nehal3m은 리뷰와 운영 모두 놓치는 것이 있다는 점을 인정하면서,
실패할 수 없는 테스트는 변이 테스트(mutation testing)로 찾을 수 있다고
했다.[^nehal3m-mutation]

### 일의 의미와 기술 전수가 따로 무너진다

세 번째 축은 피로와는 구분되는 상실감이다.
prathje는 평생 코드로 문제를 풀며 의미를 찾았는데,
AI와 함께하면 더 많이 만들고도 보람이 줄었다고 적었다.[^prathje]
ryandvm은 직접 깊은 기술 문제를 푸는 일이 좋아서 이 분야에 들어왔는데,
이제는 흔들리지 않는 자신감과 형편없는 장기 기억을 가진 중급 엔지니어 여럿을
관리하는 사람이 되었다고 했다.[^ryandvm]
thunfischtoast는 코드를 더 읽지 않고, 동료와 어려운 문제를 두고 머리를 맞대는
일도 사라졌으며, 뇌가 퇴화하는 느낌이라고 적었다.[^thunfischtoast]

zuInnp도 비슷한 이야기를 하면서 쉬는 시간을 계획하고,
직접 해 본 뒤 AI로 규모를 키우는 순서를 지키라는 구체적인 팁을 남겼다.[^zuinnp]
boogieknite는 아예 간호학 학위를 시작해,
열정을 안고 다니지 않아도 되는 안정적인 직업으로 옮기고 있다고
적었다.[^boogieknite]

### 피로의 원인을 AI에 돌리는 데 이의가 따른다

일부 답글은 질문의 틀 자체를 겨냥한다.
dude250711은 병렬로 많은 일을 추적해야 하는 것은 AI 시대가 아니라 질문자의 직장
문제라고 했다.[^dude250711]
podgorniy는 해고당할까 두려운 마음이 핵심이고 AI가 아니라고 짧게
적었다.[^podgorniy]
hypfer는 같은 시간에 성과를 몇 배로 늘리지 못했다는 이유로,
보수는 그대로인 채 직원을 해고하려는 고용주는 직원을 더 쥐어짜려는 것이고,
비정상적인 요구의 도덕적 책임은 요구한 쪽에 있다고 적었다.[^hypfer]

보수를 받지 않는 생산성 증가에 대한 반응도 있다.
qs1ykyusPlate는 생산성 증가에 대한 보상이 없으니 AI로 일을 덜 한다고 적었고,
하루에 티켓 하나만 처리하고 나머지는 남의 PR 검토와 메일 답장에 쓴다고
했다.[^qs1ykyusplate]
MotoriX는 AI가 더 자유롭고 부유하게 해 줄 줄 알았지만 지금은 더 빠르게 더 많이,
대개 더 적은 돈으로 일한다고 적었다.[^motorix]
rhedak은 주간 사용 한도를 90%까지 쓰지 않으면 돈과 토큰을 낭비하는 것 같은
압박이 유령처럼 쫓아온다고 했다.[^rhedak]

## 비평

### 표본은 이미 피곤한 사람에게 기운다

질문은 “대부분 같은 경험을 하고 있을 것”이라는 확신을 전제로 시작한다.
HN에서 이런 질문에 답하는 사람은 피로를 느끼는 사람이거나,
그 전제에 반박하고 싶은 사람이다.
어느 쪽도 개발자 전체의 분포를 대표하지 않으므로,
141개 댓글에서 피로의 비율이나 원인의 비중을 읽을 수는 없다.

스레드 안에도 이 한계가 드러난다.
victorbuilds는 나이가 마흔이 넘고 반대 경험을 하고 있으며 경험이 그 이유일
것이라고 했다.[^victorbuilds]
sammy2255는 어느 때보다 힘이 난다고 하면서도 소진될 수 있다고
덧붙였다.[^sammy2255]
이 스레드에서 확실히 말할 수 있는 것은 피로의 유형이 몇 가지로 나뉜다는
것까지이며, 얼마나 흔한지는 말할 수 없다.

### 지치지 않았다는 증언은 검토 비용을 내가 지지 않는 일에서 많이 나온다

이것은 스레드의 증언을 읽고 세운 가설이며 검증된 것은 아니다.
지치지 않았다고 쓴 사람들의 상황을 보면 스스로 속도를 정하는 개인 프로젝트,
퇴직 후의 취미 작업, 직장을 그만두고 시작한 일이 눈에 띈다.
victorbuilds는 자기 프로젝트에서 AI를 쓰므로 속도를 스스로 정해 재미있다고 했고,
alentodorov는 직장을 그만둔 뒤 AI로 만드는 일이 즐겁지만 직장에서 쓰라고
강요받던 때는 싫었다고 적었다.[^victorbuilds][^alentodorov]
JKCalhoun은 퇴직자로서 Claude와 한 시간 남짓 작업해 6502 개발 환경을 만들었지만,
애플에 있는 친구는 동료가 올린 Claude 생성 PR을 검토하느라 시달린다고
전했다.[^jkcalhoun]

반례도 있다.
martypitt는 투자자와 경쟁사의 속도 압박에 불안하다고 적었고,
ghoshbishakh는 자기 사업을 운영하면서도 매일 경쟁사 소식에 지친다고
했다.[^martypitt][^ghoshbishakh]
따라서 스스로 정하는 자율성만으로는 피로를 막지 못하며,
자신이 만든 결과를 직접 책임져야 하는 정도와 외부에서 오는 속도 압박의 정도가
함께 작용하는 것으로 보인다.
이 가설을 확인하려면 같은 사람이 개인 프로젝트와 팀 업무를 오가며 느끼는 피로를
비교해야 한다.

### 대처법 목록은 검증되지 않았고, 일부는 자기 도구를 홍보한다

제안된 대처법은 다양하지만 효과를 측정한 것은 하나도 없다.
FailMore는 자신이 만든 문서 도구 smalldocs를, imron은 코드 검토 도구를,
sadilek은 캔버스형 작업 공간 obeya를 소개했다.[^failmore][^imron][^sadilek]
도구를 직접 만드는 해결책 자체는 흥미롭지만,
이들 모두 자기 경험을 증거로 삼고 있으며 다른 사람에게 같은 효과가
있는지는 알 수 없다.

더 근본적인 점은 대처법이 피로의 원인 중 하나만 다룬다는 것이다.
쉬는 시간과 작업 수 줄이기는 맥락 전환에는 효과가 있을 수 있지만,
직접 짜는 보람이 사라진 문제나 속도 규범이 바뀐 문제에는 효과가 없다.
boogieknite의 선택이 보여 주듯 일부는 대처 대신 이탈을 택한다.[^boogieknite]

## 인사이트

### 비용이 내려간 것은 만들기이고, 확인은 여전히 사람 몫이다

생성 비용이 내려가자 확인 비용이 눈에 띄게 남았다.
jorisboris는 대시보드를 만드는 일은 쉬워졌지만,
고객의 입장에서 한 시간 동안 화면을 훑으며 숫자가 맞는지 따지는 일은 AI 이전에도
어려웠고 지금은 더 어려워졌다고 적었다.[^jorisboris]
GaryNumanVevo는 AI 열기가 만드는 쪽(sell side)에 쏠려 있다며,
자신은 사고 쪽(buy side)에서 워크플로 단계마다 평가 틀을 만들어 에이전트 출력을
측정한다고 했다.[^garynumanvevo]

Gigachad의 연쇄 사례는 이 확인 비용이 조직 안에서 어디로 모이는지 보여
준다.[^gigachad-chain]
관리자, 개발자, 검토자 중 누구도 시간을 들여 이해하지 않으면 코드는 아무도
이해하지 못한 채 배포된다.
검사 공정이 조립 라인의 끝에 몰려 있는 공장과 비슷한 구조이며,
앞 공정의 속도를 올릴수록 마지막 검사자가 먼저 한계에 닿는다.

이 구조에서 의미 있는 질문은 AI를 얼마나 쓰느냐가 아니라 확인의 책임을 누가 어떤
도구로 나눠 지느냐이다.
KptMarchewa는 의도와 설계를 에이전트와 먼저 맞추고,
에이전트가 스스로 검증할 수단과 운영 지표를 주며,
핵심 부분만 직접 읽는 방식을 적었다.[^kptmarchewa-context]
이것은 확인을 없애는 것이 아니라 확인이 일어나는 위치를 앞으로 당기는 시도이다.

### 병렬 작업의 적정 수는 다시 이어받는 비용이 정한다

스레드의 증언은 사람마다 감당하는 병렬 수가 2~3개에서 12개까지 크게
다르다고 알려 준다.
이 차이를 능력 차이로 읽기는 어렵다.
FailMore는 여덟 개에서 두세 개로 줄였고,
PippaSedai는 도구를 만들어 8~12개를 감당한다고 했다.[^failmore][^pippasedai]

달라진 것은 작업을 놓았다가 다시 잡을 때의 비용이다.
piqufoh는 슬랙, 캘린더, 메일에서 하루 작업을 모아 저녁에 Notion 일지로 써 주는
스킬을 만들어 다음 날 아침 맥락을 복원한다고 했다.[^piqufoh]
ccapndave는 대기, 진행, 검토 열로 나뉜 칸반 보드에 에이전트가 요약을 남기게
하고, 작업을 열어 훑은 뒤 그 작업을 맥락으로 에이전트를 이어 가는 방식을 쓴다고
했다.[^ccapndave]
frumiousirc는 어제 한 일이 기억나지 않는 것이 가장 큰 문제라고
적었다.[^frumiousirc]

적정 병렬 수는 이어받는 비용이 낮아지는 만큼 늘어난다고 볼 수 있다.
반대로 비용을 줄이지 않고 병렬 수만 늘리면 rhedak이 말한 유령처럼 한도를 채우는
것이 목적이 되어 버린다.[^rhedak]
사용량이라는 지표가 가치와 상관없이 목표가 되면 일이 지표를 따라가게 되며,
이는 지표가 목표가 되면 좋은 지표가 아니게 된다는 굿하트의 법칙(Goodhart's
law)과 같은 구조이다.

### 보람이 사라지는 문제는 휴식으로 풀리지 않는다

ryandvm은 피곤할 뿐 아니라 불행하다고 했고,
생산성을 높이는 것은 자기 삶의 목표가 아니라고 적었다.[^ryandvm]
이것은 맥락 전환이나 검토 부담과는 다른 종류의 문제이다.
쉬는 시간을 늘려도 해결되지 않기 때문에,
이 유형의 답글은 대처법이 아니라 이탈이나 체념으로 끝나는 경우가 많다.

thunfischtoast의 증언은 이 문제가 개인을 넘어 팀의 학습 구조와 연결됨을 보여
준다.[^thunfischtoast]
어려운 문제가 사라지면 함께 머리를 맞대는 코딩 세션도 사라지고,
서로에게서 배우는 일도 줄어든다.
sys_64738은 AI와 함께 자란 세대가 AI가 알려 주는 답 말고는 퍼즐을 푸는 법을
모르게 될 것이라고 우려했다.[^sys_64738]
반론으로 tstrimple은 새 게임이 길 안내선을 준다고 사람들이 어려운 게임을 안 하게
된다는 식의 주장이라며 비꼬는 비유를 들었다.[^tstrimple-games]

이 긴장은 규모가 커질수록 문제가 된다.
개인에게는 보람의 상실이 선택의 문제일 수 있다.
그러나 어려운 문제를 함께 푸는 경험이 신입이 숙련자로 크는 경로였다면,
그 경로가 줄어든 조직은 몇 년 뒤 확인을 맡길 사람이 부족해질 수 있다.
앞의 첫 번째 인사이트와 이어 보면, 확인이 사람 몫으로 남는 동안 확인할 수 있는
사람을 키우는 경로는 약해지고 있다는 모순이 드러난다.

### 속도 규범은 오르는데 이득의 분배는 정해지지 않았다

많은 증언에서 생산성 이득이 직원에게 돌아가지 않는다.
MotoriX와 qs1ykyusPlate는 같은 진단을 다른 대응으로 보여 준다.
한 사람은 더 빨리 더 많이 일하고, 다른 사람은 이득이 없으니 AI로 일을 덜
한다.[^motorix][^qs1ykyusplate]
sourcecodeplz는 주 4~5일 대신 강도 높은 하루나 이틀만 일하고 나머지는 생각하는
데 쓴다고 적었다.[^sourcecodeplz]
GeekNews의 kirinonakar는 AI의 속도에 맞춰 일하면 힘들어질 수밖에 없고, 반대로 원래 자기
페이스를 지키면 생산성이 떨어진다고 적었다.
그렇다고 모두 AI에 맡기는 데는 거부감과 불안을 느끼는 사람도 많으므로 이것은
과도기의 딜레마라는 것이다.[^kirinonakar]

hypfer의 지적처럼 분배 문제를 개인의 효율 문제로 바꾸면 요구하는 쪽의 책임이
사라진다.[^hypfer]
질문자가 말한 해고 걱정이 정당한지는 이 스레드로 알 수 없다.
다만 속도 규범이 올라가는 동안 보상과 노동시간이 함께 조정되었다는 증언은 이
스레드에서 찾지 못했고, 반대 방향의 증언이 여럿이라는 점은 분명하다.

---

[^martypitt]: <https://news.ycombinator.com/item?id=50301583>

[^justforfunhere]: <https://news.ycombinator.com/item?id=50301832>

[^failmore]: <https://news.ycombinator.com/item?id=50301820>

[^victorbuilds]: <https://news.ycombinator.com/item?id=50301585>

[^pippasedai]: <https://news.ycombinator.com/item?id=50301737>

[^philipp-gayret]: <https://news.ycombinator.com/item?id=50301661>

[^fabioborellini]: <https://news.ycombinator.com/item?id=50301575>

[^retr0id]: <https://news.ycombinator.com/item?id=50301662>

[^gigachad-chain]: <https://news.ycombinator.com/item?id=50302102>

[^yulaow]: <https://news.ycombinator.com/item?id=50301771>

[^orwin]: <https://news.ycombinator.com/item?id=50302184>

[^hasley]: <https://news.ycombinator.com/item?id=50301651>

[^kptmarchewa-tests]: <https://news.ycombinator.com/item?id=50301707>

[^40pt]: <https://news.ycombinator.com/item?id=50304472>

[^nehal3m-mutation]: <https://news.ycombinator.com/item?id=50304433>

[^prathje]: <https://news.ycombinator.com/item?id=50301660>

[^ryandvm]: <https://news.ycombinator.com/item?id=50303602>

[^thunfischtoast]: <https://news.ycombinator.com/item?id=50301807>

[^zuinnp]: <https://news.ycombinator.com/item?id=50301863>

[^boogieknite]: <https://news.ycombinator.com/item?id=50307473>

[^dude250711]: <https://news.ycombinator.com/item?id=50301540>

[^podgorniy]: <https://news.ycombinator.com/item?id=50301766>

[^hypfer]: <https://news.ycombinator.com/item?id=50301724>

[^qs1ykyusplate]: <https://news.ycombinator.com/item?id=50303841>

[^motorix]: <https://news.ycombinator.com/item?id=50302238>

[^rhedak]: <https://news.ycombinator.com/item?id=50304864>

[^sammy2255]: <https://news.ycombinator.com/item?id=50301732>

[^alentodorov]: <https://news.ycombinator.com/item?id=50301859>

[^jkcalhoun]: <https://news.ycombinator.com/item?id=50302206>

[^ghoshbishakh]: <https://news.ycombinator.com/item?id=50301672>

[^imron]: <https://news.ycombinator.com/item?id=50301940>

[^sadilek]: <https://news.ycombinator.com/item?id=50304018>

[^jorisboris]: <https://news.ycombinator.com/item?id=50301690>

[^garynumanvevo]: <https://news.ycombinator.com/item?id=50301937>

[^kptmarchewa-context]: <https://news.ycombinator.com/item?id=50301697>

[^piqufoh]: <https://news.ycombinator.com/item?id=50301855>

[^ccapndave]: <https://news.ycombinator.com/item?id=50301626>

[^frumiousirc]: <https://news.ycombinator.com/item?id=50301905>

[^sys_64738]: <https://news.ycombinator.com/item?id=50303629>

[^tstrimple-games]: <https://news.ycombinator.com/item?id=50312575>

[^sourcecodeplz]: <https://news.ycombinator.com/item?id=50301747>

[^kirinonakar]: <https://news.hada.io/topic?id=36335#cid68914>
