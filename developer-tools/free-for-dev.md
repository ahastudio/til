# free-for.dev: 무료 티어의 자격을 정해 두고 1,300여 개를 모은 개발자용 목록

<https://free-for.dev/>

HN 토론: <https://news.ycombinator.com/item?id=26239711> (967점, 197개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/e7ss02/list_services_offering_free_tiers> (18점, 4개 댓글)

GN 토론: <https://news.hada.io/topic?id=759>

## 소개

free-for.dev는 무료 개발자 티어(free tier)를 제공하는 서비스를 모은 목록이다.
페이지는 docsify로 만든 얇은 껍데기이고,
본문은 실행 시점에 저장소 `ripienaar/free-for-dev`의 README를 불러와 보여준다.
이 문서는 그 README 전문을 읽고 썼다.

목록의 범위는 시스템 관리자와 DevOps 실무자 같은 인프라 개발자가 쓸 만한
서비스로 한정된다.
운영자는 이 범위가 의견이 섞인 선택이라고 직접 밝히고,
기여가 거절되어도 서운해하지 말라고 적었다.
이 목록은 1,600명 넘는 사람의 풀 리퀘스트(Pull Request), 리뷰,
아이디어로 만들어졌다고 README는 말한다.

등재 조건은 네 가지다.
첫째, 서비스형(as-a-Service) 제품만 받고
직접 설치해 쓰는 소프트웨어는 받지 않는다.
둘째, 무료 체험판(trial)이 아니라 무료 티어여야 한다.
셋째, 기간으로 끊어 주는 무료 티어라면 최소 1년이어야 한다.
넷째, 보안 관점에서 TLS를 유료 티어에만 허용하는 서비스는 받지 않는다. SSO는
괜찮다고 적혀 있다.

### 구성

목차는 57개 섹션이다.
내가 정규식으로 센 값으로는 링크가 달린 최상위 항목이 1,306개다.
Google Cloud, AWS, Azure, Oracle Cloud, IBM Cloud,
Cloudflare 여섯 곳은 `Major Cloud Providers` 아래에서
하위 항목으로 서비스별 한도를 따로 적는다.
항목이 가장 많은 섹션은 `APIs, Data, and ML` 148개, `Email` 85개,
`Tools for Teams and Collaboration` 84개, `Monitoring` 67개,
`Issue Tracking and Project Management` 61개,
`Storage and Media Processing` 51개 순이다.

한 항목은 서비스 이름, 링크, 한 줄 설명으로 이루어지고
설명에는 한도 숫자가 들어간다.
예를 들어 Google Cloud의 Cloud Run은 월 200만 요청, 월 360,000 GB-초의 메모리,
180,000 vCPU-초를 무료로 쓸 수 있다고 적혀 있다.
AWS SES는 월 3,000건이고 뒤에 `(6mo)`가 붙는다.

### 저장소의 현황

저장소의 별은 142,350개, 포크는 15,297개이고 2015-03-18에 만들어졌다.[^repo]
커밋은 7,619개이고, 기여자는 익명 포함 2,386명이다.[^commits][^contributors]
2015년 3월부터 2026-11-09까지를 일수로 나누면
하루 약 1.8개꼴로 커밋이 쌓인 셈이다. 이 계산은 내가 했다.
가장 최근 커밋은 2026-11-09에 올라온 DNSvivo 추가와 Hyperserve 무료 티어 한도
갱신이다.[^recent]

## 분석

### 이 목록의 가치는 거절 기준에 있다

1,306개를 한곳에 모은 것은 검색으로도 어느 정도 흉내 낼 수 있다.
다른 곳에서 얻기 어려운 것은 무엇을 받지 않을지에 대한 규칙이다.
체험판을 빼고, 1년 미만의 기간제 무료 티어를 빼고,
TLS를 유료로 묶은 서비스를 뺀다는 세 규칙은 무료라는 단어에 붙는 느슨한 정의를
하나의 기준으로 고정한다.

이 기준은 개발자 쪽의 불안을 겨냥한다.
체험판은 끝나면 이전 비용이 생기고,
1년 미만의 무료 기간은 프로젝트가 자리 잡기 전에 끝나며,
TLS를 유료로 묶은 서비스는 무료 티어로 만든 첫 서비스를 안전하지 않은 채로
내놓게 만든다.
규칙의 모양이 곧 목록의 독자가 누구인지 말해 준다.
작은 팀과 개인 프로젝트가 청구서를 받기 전에 한 번 더 따져 보게 하려는 목록이다.

### 가장 큰 칸은 인프라가 아니라 API와 협업 도구다

운영자는 범위를 인프라 개발자용으로 좁혔다고 말하지만, 항목 수만 보면
가장 큰 섹션은 `APIs, Data, and ML`이고 그다음이 `Email`과 팀 협업 도구다.
순수한 인프라에 가까운 `Cloud management solutions`는 7개, `IaaS`는 5개,
`Docker Related`는 5개뿐이다.

이 분포가 무엇을 뜻하는지는 단정하기 어렵다.
무료 티어를 내놓는 쪽이 많은 영역이 이런 영역이라서일 수도 있고,
큰 클라우드는 한 항목에 한도를 모아 적기 때문에 개수가 적게 보이는 것일 수도
있다.
확실한 것은 항목 수가 서비스의 중요도가 아니라 등재 단위의 수라는 점이다.

### 유지 방식은 풀 리퀘스트에 기댄다

README는 서비스 추가뿐 아니라 제공 조건이 바뀌었거나 서비스가 종료된 항목을
지우는 기여도 받는다고 말한다.
가장 최근 커밋 두 개가 항목 추가와 한도 갱신이라는 점은 이 두 방향의 수정이
실제로 일어난다는 것을 보여준다.

## 비평

### 링크가 살아 있어도 무료 티어가 살아 있다는 뜻은 아니다

이 목록이 시간이 지나 썩었을 것이라는 의심을 검증하려고
항목 링크를 전부 확인했다.
2026-11-10에 1,306개 링크에 브라우저 User-Agent로 HEAD 요청을 보내고 실패하면
GET으로 다시 요청했으며, 제한 시간은 12초로 두었다.
1,278개(97.9%)가 200으로 응답했다.

응답하지 않은 28개 가운데 19개는 403, 429, 406, 451,
418처럼 접근을 거절하거나 요청이 많다고 알리는 코드라서,
스크립트로는 서비스가 죽은 것과 구분되지 않는다.
실패로 읽을 만한 것은 9개다.
Quidlo Timesheets 경로는 404였고, Compare JSON, MDB GO,
localhost.run은 연결 오류였으며, Engage와 Abby는 시간이 초과되었다.
TestTLS.com은 502, nTask는 504,
Wikifactory는 500이었다. 일시적인 오류일 수도 있다.

따라서 링크 부패에 관한 가장 강한 주장,
곧 이 목록이 방치되어 죽은 링크로 가득하다는 주장은 이 측정으로 반박된다.
다만 이 측정이 보여주는 것은 사이트가 응답한다는 사실까지다.
무료 티어가 남아 있는지, 한도가 README에 적힌 숫자와 같은지는 확인하지 않았다.
그것을 확인하려면 항목마다 요금 페이지를 읽어야 하고,
이 측정은 그 일을 하지 않았다.

200으로 끝난 링크 가운데 71개는 적힌 주소와 다른 호스트로 넘어갔다.
이 중에는 `fibery.io`에서 `fibery.com`으로 가는 것처럼 같은 제품의 도메인 변경도
있지만, Revolt.chat은 `stoat.chat`으로, RequestBin.com은 `pipedream.com`으로,
Weights & Biases는 `forge.coreweave.com/wandb`로,
Terrateam은 `stategraph.com`으로 넘어갔다.
이름이나 주인이 바뀐 서비스의 무료 티어가 그대로인지는 이 목록에서 알 수 없다.

2021년 2월 Hacker News 스레드에서도 같은 구분이 나왔다.
justin_oaks는 이런 목록이 금방 낡는다고 했고,[^justin_oaks]
jldugger는 이 목록은 커뮤니티 기여로 잘 유지된다고 답했다.[^jldugger]
anamexis는 봇이 링크가 죽지 않았는지는 확인해도
인용한 정보가 아직 맞는지는 확인하지 못한다고 짚었다.[^anamexis]
이 측정은 앞의 두 의견 가운데 링크에 관한 부분에서는 jldugger 쪽을 지지하고,
anamexis가 말한 한계는 그대로 남는다.

### 항목에는 확인한 날짜가 없다

README에서 연도 숫자가 들어간 줄은 세 줄뿐이고, 그 가운데
항목의 시점을 말하는 것은 PhantomJsCloud의 2017년부터 무료라는 표기 정도다.
나머지 항목은 한도가 언제 확인된 것인지 알려주지 않는다.
무료 티어는 요금제 개편 한 번으로 달라지는 정보인데,
항목 옆에 마지막 확인 날짜가 없으면
독자는 숫자를 얼마나 믿어야 할지 가늠할 수 없다.

최근 커밋 중 Hyperserve 한도 갱신이 보여주듯 갱신은 일어난다.
하지만 갱신된 항목과 그렇지 않은 항목이 겉으로는 구별되지 않는다.

이 문제는 2021년 HN 스레드에서 이미 지적되었다.
kencausey는 바뀔 수 있는 정보를 모은 목록이라면
정보를 마지막으로 확인한 날짜를 공개해야 한다고 적었다.[^kencausey]
remram은 Wikipedia처럼 외부 링크에 접근 날짜를 붙이고,
GitHub Actions로 6개월 넘게 확인하지 않은 항목의 목록을 뽑아
사람이 확인하게 하자고 제안했다.[^remram]
내가 지금의 README를 확인한 결과 항목 옆에 확인 날짜를 붙이는 방식은 아직 쓰이지
않는다.
rapfaria는 한 걸음 더 나가 한도 축소를 미리 알려 주는 뉴스레터를
원했다.[^rapfaria]
fomine3도 항목에 무료 티어의 기간이 적혀 있기를 바랐다.[^fomine3]

### 목록이 자기 규칙을 항목에서 지키는지 알 수 없다

README는 기간으로 끊어 주는 무료 티어는 최소 1년이어야 한다고 적는다.
그런데 AWS SES 항목은 월 3,000건 뒤에 `(6mo)`를 붙였다.
이 표기를 6개월로 읽으면 자기 규칙과 어긋난다.
큰 클라우드의 한 서비스에 대한 예외일 수도 있지만
README에는 예외라는 설명이 없다.

카드 요구 여부도 비슷하다.
신용카드를 언급하는 줄은 52줄이고 그중 47줄이 카드가 필요 없다는 내용이다.
나머지 대부분의 항목은 카드가 필요한지를 적지 않았다.
무료 티어를 고를 때 가장 먼저 묻는 질문에 대해 목록이 답을 주는 항목은 소수다.
dvfjsdhgfv도 같은 스레드에서 항목마다 카드 정보를 요구하는지 작은 기호로
표시하자고 제안했다.[^dvfjsdhgfv]
BossingAround는 무료 서비스가 카드를 요구하고,
HN 상위권에 올라 트래픽이 폭증하면
그때부터 비용을 내야 하는 구조를 문제로 꼽았다.[^BossingAround]

### 항목 문장은 등재를 요청한 쪽의 어조를 닮았다

Keywords AI 항목은 자사를 최고의 LLM 모니터링 플랫폼이라고 소개하고,
Langfuse 항목은 평생 무료 플랜을 말한다.
이런 문장은 제3자의 평가가 아니라 서비스 제공자의 소개 문구에 가깝다.
항목 문장을 누가 썼는지는 이 README만으로는 알 수 없고, 어조에서 나온 추정이다.
다만 어조가 그렇다면 목록은 비교표가 아니라 업체들의 소개 문구 모음이 되고,
숫자는 업체가 가장 좋아 보이는 방식으로 고른 값일 수 있다.

## 인사이트

### 무료 티어 목록이 실제로 다루는 단위는 서비스가 아니라 한도와 날짜의 쌍이다

목록은 서비스를 하나의 항목으로 적지만
독자가 의존하는 것은 월 200만 요청이나 5GB 같은 한도다.
한도는 서비스보다 훨씬 자주 바뀐다.
이름이 같아도 한도가 바뀌면 다른 항목이 된다.
그래서 목록에서 찾은 숫자를 프로젝트 문서로 옮길 때는 숫자와 함께 확인한 날짜를
적고, 요금 페이지의 주소를 같이 남기는 편이 안전하다.
이 목록이 날짜를 적지 않기 때문에 독자가 그 일을 대신해야 한다.

### 가장 위험한 정보는 한도를 넘었을 때의 동작인데 목록에 없다

항목은 한도의 크기를 적지만, 한도를 넘으면
서비스가 멈추는지 과금되는지는 적지 않는다.
작은 팀이 청구서를 받는 순간은 한도가 모자랄 때가 아니라 한도를 넘었을 때의
동작을 몰랐을 때다.
무료 티어 하나를 도입하기 전에 확인할 목록은 네 칸으로 줄일 수 있다.
한도, 넘었을 때의 동작, 확인한 날짜, 다른 곳으로 옮길 때의 비용이다.
이 목록은 첫 칸만 채워 주고, 나머지 세 칸은 독자가 채워야 한다.

HN 스레드의 사례가 이 구분을 뒷받침한다.
glaucon은 DynamoDB의 25GB라는 숫자가 실제로 걸리는 제약이 아니고,
읽기와 쓰기 단위가 데이터 구조에 따라 먼저 한도에 닿을 수 있다고
적었다.[^glaucon]
deathanatos는 Azure Kubernetes Service의 클러스터 관리가 무료라는 항목이
문장 그대로는 맞지만 노드의 VM과 디스크는 요금이 붙고,
무료 관리형 API 서버에서 요청 시간 초과를 겪었다고 말했다.[^deathanatos]
tetraodonpuffer는 한도를 넘으면 서비스를 끊되 다른 요금은 청구하지 않겠다고
보장하는 요금제를 원했다.[^tetraodonpuffer]
반대로 jillesvangurp는 Cloud Run과 Firestore로 스타트업의 개발과 초기 트래픽을
거의 0달러로 운영한다고 보고했고, 큰 데이터를 가져올 때 한도를 1달러도 안 되게
넘긴 적이 있었다고 덧붙였다.[^jillesvangurp]
한도 안에서 쓰면 실제로 무료이고, 한도 밖의 동작이 비용을 가른다는 뜻이다.

이것은 목록의 결함이라기보다 목록이라는 형식의 한계다.
한 줄에 담을 수 있는 것은 숫자 하나이고, 위험은 숫자 밖에 있다.

### 자격 규칙은 목록이 업체에 거는 압력일 수 있다

142,350개의 별을 가진 목록에 오르는 것은 업체에 유입 경로가 된다.
그렇다면 1년 이상, 체험판 불가,
TLS 무료 제공 같은 규칙은 독자를 보호하는 규칙인 동시에 업체가 요금제를 설계할
때 맞춰야 하는 조건이 된다.
이것은 내가 세운 가설이고, 이 README와 저장소 통계만으로는 입증되지 않는다.
검증하려면 등재를 위해 요금제를 바꾼 업체의 사례가 필요하다.

무료 제공의 동기에 관해서는 Lobste.rs의 david_chisnall이 다른 방향의 근거를
냈다.
그는 Microsoft가 오픈소스 개발자에게 Visual Studio 구독을 무료로 주고,
거기에 월 150달러의 Azure 크레딧이 딸려 있다고 적었다.
그리고 이 제도의 목적은 개발자의 소프트웨어가 Azure에서 잘 돌게 만들어
사용자가 Azure에 배포하기 쉽게 하려는 것이라고 설명했다.[^david_chisnall]
이 말대로라면 무료 티어는 요금제의 한 칸이기 전에 생태계를 자기 쪽에 맞추는
수단이고,
한도와 조건은 그 목적에 따라 바뀔 수 있다.

---

[^repo]: GitHub API, [Repository ripienaar/free-for-dev](https://api.github.com/repos/ripienaar/free-for-dev)

[^commits]: GitHub API, [Commits of ripienaar/free-for-dev](https://api.github.com/repos/ripienaar/free-for-dev/commits?per_page=1)

[^contributors]: GitHub API, [Contributors of ripienaar/free-for-dev](https://api.github.com/repos/ripienaar/free-for-dev/contributors?per_page=1&anon=true)

[^recent]: GitHub API, [Recent commits of ripienaar/free-for-dev](https://api.github.com/repos/ripienaar/free-for-dev/commits?per_page=5)

[^justin_oaks]: <https://news.ycombinator.com/item?id=26242649>

[^jldugger]: <https://news.ycombinator.com/item?id=26244497>

[^anamexis]: <https://news.ycombinator.com/item?id=26244711>

[^kencausey]: <https://news.ycombinator.com/item?id=26242284>

[^remram]: <https://news.ycombinator.com/item?id=26243183>

[^rapfaria]: <https://news.ycombinator.com/item?id=26243162>

[^fomine3]: <https://news.ycombinator.com/item?id=26246505>

[^dvfjsdhgfv]: <https://news.ycombinator.com/item?id=26240743>

[^BossingAround]: <https://news.ycombinator.com/item?id=26241313>

[^glaucon]: <https://news.ycombinator.com/item?id=26247366>

[^deathanatos]: <https://news.ycombinator.com/item?id=26243444>

[^tetraodonpuffer]: <https://news.ycombinator.com/item?id=26242578>

[^jillesvangurp]: <https://news.ycombinator.com/item?id=26249095>

[^david_chisnall]: <https://lobste.rs/s/e7ss02/list_services_offering_free_tiers#c_tnnvan>
