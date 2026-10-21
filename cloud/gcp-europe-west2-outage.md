# 유럽 은행 대부분이 멈췄다는 보도의 실제는 런던 리전 한 영역의 전원 사고였다

원문: [Google cloud outage takes down HSBC, Revolut, Bank of Scotland, Lloyds, Equifax, more - Neowin](https://www.neowin.net/news/google-cloud-outage-takes-down-hsbc-revolut-bank-of-scotland-llyods-equifax-more/)

HN 토론: <https://news.ycombinator.com/item?id=50163961> (347점, 173개 댓글)

GN 토론: <https://news.hada.io/topic?id=35714>

## 요약

Neowin의 Sayan Sen은 2026년 10월 20일 기사에서 Google Cloud 장애로
유럽의 은행 업무 대부분이 영향을 받는다고 전했다.
HSBC, Revolut, Bank of Scotland, Lloyds, Royal Mail,
Geopost의 DPD 등의 인프라가 영향을 받았고,
문제는 Google Cloud 장애와 관련된 것으로 보인다는 서술이다.
제목에는 Equifax도 들어 있다.

기사는 Google이 확인한 영향 서비스 목록을 그대로 옮긴다.
AlloyDB, BigQuery, Cloud Run, Cloud Spanner,
Cloud SQL, Cloud Storage, Compute Engine,
GKE, Pub/Sub, Persistent Disk, VPC, Cloud Load Balancing 등 수십 개다.
Revolut은 가입, 로그인, 결제와 송금, 충전,
ATM 인출, 주식 거래, 암호화폐를 포함한
모든 업무가 멈췄다고 확인했다고 한다.
Google은 영향을 받은 고객에게 가능하면
워크로드를 다른 위치(영역이나 리전)로 옮겨 보라고 권했다.
기사는 자세한 내용이 나오면 갱신하겠다고 적고 끝난다.

## 분석

### 기사가 쓴 때는 원인이 알려지기 전이었다

기사는 장애가 일어난 지 몇 시간 되지 않은 시점의 속보다.
이 문서가 확인한 Google Cloud 서비스 상태 페이지에 따르면
장애는 europe-west2 리전에서 2026년 10월 19일 23시 8분(태평양 시간)에 시작했다.
세계 협정시로는 20일 6시 8분이다.
Google은 처음에 여러 서비스의 오류율 상승과 간헐적 네트워크 실패라고만 적었다가
나중에 전원 사고(power event)로 europe-west2-b 영역이 멈췄다고 밝혔다.[^status]
복구는 태평양 시간 5시 10분께 대부분의 워크로드에서 시작되었고,
Google은 기존 워크로드의 복구를 우선하느라 고객이
아직 새 워크로드를 만들지 못할 수 있다고 안내했다.
협정시 14시 3분에 사건은 해소로 표시되었고, 소수의 고객은 여전히 영향을 받으며
분석 보고서는 내부 조사가 끝난 뒤 게시한다고 했다.[^status]
시작에서 해소 표시까지 약 8시간이다.

기사에는 이 원인이 없다.
기사가 쓰인 때 원인이 공개되지 않았고,
그래서 이 보도로는 사고가 한 영역의 전원 문제라는 사실을 알 수 없다.

### 영향 범위는 영역이고 리전이며 영국이었다

기사 제목은 유럽의 은행 대부분이라고 말하지만,
사건은 런던 리전으로 알려진 europe-west2 한 곳이다.
상태 페이지는 europe-west2-b 영역이 멈췄고
리전의 일부 서비스에도 오류와 간헐적 네트워크 문제가 있었다고 적는다.[^status]
HN의 samkone은 스위스에서 GCP 위에 만든 은행 서비스를 쓰는데
하루 종일 끊김이 없었다고 썼고,[^samkone]
HSBC 고객이라는 bcvvvy는 모든 것이 정상이었고
Downdetector는 사용자 신고를 모은 것이라 나쁜 출처라고 했다.[^bcvvvy]
이 두 댓글은 개인의 관찰이지만,
영향이 영국의 해당 리전에 의존하는 곳에 집중되었다는 해석과 맞는다.
HSBC가 자기 홈페이지에 다른 조직에도 영향을 주는 상황이라고
알렸다는 댓글도 있다.[^4ndrewl]

## 비평

### 은행마다의 원인은 기사에서 확인되지 않는다

기사는 각 회사의 장애가 Google Cloud 때문일 가능성이 높다고 쓴다.
확인된 것은 Revolut의 발표뿐이다.
나머지 은행과 Royal Mail, DPD,
Equifax가 이 사건 때문에 멈췄는지는 각 회사의 확인이 없다.
Downdetector 같은 신고 집계에 기댄 판단일 수 있고,
그 정확성을 두고 HN에서도 의견이 갈렸다.
m11a는 큰 폭의 신고 급증이 문제와 잘 맞는 경우가 많고
사용자가 못 쓰면 실제로 멈춘 것이라고 했고,[^m11a]
rurp는 공식 상태 페이지가 틀리는 경우가 더 많다고 했다.[^rurp]
Johnny555는 상태 페이지가 확인된 큰 장애만 올리므로
서비스에 영향이 있어도 나타나지 않을 수 있다며
신고 집계를 더 낫다고 평가했다.[^Johnny555]
두 출처는 서로 다른 오류를 낸다. 하나는 거짓 양성을,
다른 하나는 거짓 음성을 낸다.

### 기사가 지운 구분이 가장 중요한 질문이다

HN의 nickcw는 이것이 한 영역의 전원 장애이고
그것이 클라우드 사업자가 영역을 여럿 두는 이유라며,
보도된 큰 회사들이 여러 영역을 쓰지 않았다는 사실에 놀랐다고 했다.
그는 상태 페이지가 태평양 시간으로만 쓰여 영국과
유럽 사용자에게 불친절하다고도 지적했다.[^nickcw]
그러나 상태 페이지는 영역 하나의 문제만이 아니라
리전의 네트워크 문제와 오류도 적었다.[^status]
다중 영역 설계가 이 사건에서 어디까지 막았는지는 기사에도 상태 페이지에도 없다.
Arbortheus는 이 사건의 영향을 받은 곳은 데이터 주권 요건 때문에 영국의 한 리전에
사업 전체를 둔 회사일 가능성이 높다고 추정했다.[^Arbortheus]
이 추정은 댓글의 것이고 확인된 것은 아니다.

### 인과에 대한 해설이 사건보다 빨랐다

스레드에는 사건을 구조적 취약성이나 전쟁 시나리오로 확대하는 댓글이 많았다.
josefritzishere는 전력 하나가 은행 다섯 곳 이상을 멈춘다면
그 자체로 가치 있는 표적이라는 뜻이라며
우크라이나가 러시아 데이터 센터를 공격한 사례와 연결했다.[^josefritzishere]
이 해석은 이 사건이 의도된 공격이 아니라 전원 사고라는
상태 페이지의 서술과 다른 이야기를 하고 있다.
집중 위험을 짚는 지적으로는 타당하지만, 이번 사건의 원인으로 제시된 것은 아니다.

## 인사이트

### 복구는 기존 워크로드부터이고 새 워크로드는 나중이라서 장애 중의 확장 계획은 작동하지 않는다

상태 페이지는 기존 워크로드의 복구를 우선하느라 새
워크로드를 만들지 못할 수 있다고 안내했다.[^status]
Google이 같은 시점에 제안한 대안은 워크로드를
다른 영역이나 리전으로 옮기는 것이었다.
이 둘은 서로 부딪친다.
장애가 난 영역에서 빠져나가는 일은 대체로 새 자원을 만드는 일이기 때문이다.
자동 확장이나 장애 조치가 장애 시점에 새 인스턴스를 만들어야 하는 설계라면,
필요한 때 가장 못 쓰는 설계가 된다.

그러므로
중요한 서비스는 장애 조치 대상을 평상시에 미리 띄워 두어야 한다는 결론이 나온다.
이 문서는 이를 자원을 장애 시점에 만들지 않고
미리 만들어 둔다는 설계 원칙으로 읽는다.
비용이 두 배가 될 수 있다는 점에서 모든 서비스에 쓸 수는 없고,
서비스의 중요도에 비례해 정할 일이다.
이는 이 문서의 해석이며 이번 사건의 사후 분석이 이를 확인한 것은 아니다.

### 규제가 요구하는 데이터 위치가 집중 위험을 만든다

Arbortheus의 추정이 맞다면 데이터 주권 요건이 사업을 한 리전에 묶고
그 리전의 사고가 업계 전체의 사고가 된다.[^Arbortheus]
gentlerain은 국가들이 AI 주권을 말하면서
컴퓨트 주권은 잊었다고 썼고,[^gentlerain]
otar는 EU가 AWS와 Google Cloud의 유럽판 대안을 우선해 만들어야 한다고
썼다.[^otar]
그러나 주권과 복원력은 같은 방향이 아니다.
한 나라 안에 두라는 요건은 선택지를 줄이고, 선택지가 줄면 같은 곳에 몰린다.
bobbiechen은 금융기관에 클라우드 사업자가 핵심 제3자 ICT 공급자인 경우
디지털 운영 복원력법(DORA)의 준수가 어떻게 영향을 받는지 물었다.[^bobbiechen]
이 질문의 답은 스레드에도 없다. 규제가 집중 위험을
줄이는 쪽으로 쓰일지는 규제당국의 해석에 달려 있다.

### 고객 접점의 복원력은 인프라의 복원력과 별개다

paweladamczuk은 Revolut의 주 계좌에 접근할 수 없었고 앱이 안 되며
전화 번호도 없어서 말할 사람이 없었다고 썼다.[^paweladamczuk]
rpozarickij는 가게에서 Revolut으로 결제하지 못했지만
다른 은행의 카드를 Apple Pay에 추가해 해결했다고 했다.[^rpozarickij]
Arbortheus는 Monzo가 별도 코드베이스와 별도 클라우드 사업자를 쓰는 대기 시스템이
있어서 예전 장애에서 기능에 거의 영향이 없었다고 소개했다.[^Arbortheus-monzo]
이 세 증언은 같은 사건이 사용자에게 얼마나 다르게 닿는지를 보여 준다.
인프라가 하나의 지점에 의존해도,
사용자가 다른 결제 수단과 사람 상담이라는 두 번째 경로를 갖고
있으면 사고가 불편으로 끝난다.
인프라 쪽 복원력과 서비스 쪽 복원력은 따로 설계해야 한다는 뜻이다.
Monzo의 사례는 댓글의 소개이고 이 문서가 해당 블로그를 열어 확인하지는 않았다.

---

[^status]: Google Cloud Service Health, [Multiple services are experiencing issues in the europe-west2 region (Incident Xs2XTHzAVC9YnafnPyzj)](https://status.cloud.google.com/incidents/Xs2XTHzAVC9YnafnPyzj), 2026-10-20

[^samkone]: <https://news.ycombinator.com/item?id=50170733>

[^bcvvvy]: <https://news.ycombinator.com/item?id=50164600>

[^4ndrewl]: <https://news.ycombinator.com/item?id=50164970>

[^m11a]: <https://news.ycombinator.com/item?id=50164819>

[^rurp]: <https://news.ycombinator.com/item?id=50167407>

[^Johnny555]: <https://news.ycombinator.com/item?id=50167649>

[^nickcw]: <https://news.ycombinator.com/item?id=50164718>

[^Arbortheus]: <https://news.ycombinator.com/item?id=50164405>

[^josefritzishere]: <https://news.ycombinator.com/item?id=50165582>

[^gentlerain]: <https://news.ycombinator.com/item?id=50164328>

[^otar]: <https://news.ycombinator.com/item?id=50171802>

[^bobbiechen]: <https://news.ycombinator.com/item?id=50169267>

[^paweladamczuk]: <https://news.ycombinator.com/item?id=50163962>

[^rpozarickij]: <https://news.ycombinator.com/item?id=50166668>

[^Arbortheus-monzo]: <https://news.ycombinator.com/item?id=50164305>
