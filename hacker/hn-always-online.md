# Hacker News가 늘 켜져 있는 이유: 서버 한 대와 파일, 그리고 변하지 않는 제품

Ask HN: [Ask HN: How does HN manage to be always online?](https://news.ycombinator.com/item?id=31821269)

GN 토론: <https://news.hada.io/topic?id=6877>

## 요약

2022년 6월 21일 hacsky가 Hacker News에 올린 질문이다.
본문은 제목과 같은 한 문장, HN은 어떻게 늘 온라인 상태를 유지하느냐뿐이다.
스레드는 127점과 188개의 댓글을 모았다.
같은 날 HN에는 Cloudflare의 부분 장애 소식이 올라와 있었고,
notlukesky는 그 글을 링크하며
HN은 Cloudflare를 쓰지 않나 보다고 적었다.[^notlukesky]
ignoramous는 news.ycombinator.com은 아닐지 몰라도 ycombinator.com과
startupschool.org는 Cloudflare 위에 있다고 덧붙였다.[^ignoramous]

가장 많이 인용된 답은 5id의 댓글이다.[^5id]
5id는 dang이 2021년에 가리킨 sctb의 2018년 설명을 옮겼다.
HN은 M5 Hosting에 마스터와 스탠바이 두 대를 두고 있고,
HN 전체는 특별할 것 없는 한 대의 장비에서 돈다는 내용이다.
CPU는 Intel Xeon E5-2637 v4 3.50GHz, 운영체제는 FreeBSD이며
2 패키지 × 4 코어 × 2 하드웨어 스레드 구성이다.
데이터는 미러링된 SSD에, 로그는 미러링된 자기 디스크에 UFS로 둔다.
sctb의 원래 댓글은 하루 약 400만 요청이라고 적었고,[^sctb]
dang은 2021년에 구성은 그대로이고 하루 요청이 600만에 가까워졌다고 했다.[^dang]

저장 방식에 대한 답도 나왔다.
krapp은 데이터가 Arc Lisp 테이블을 담은 평범한 텍스트 파일이나 RAM에 있고,
따로 데이터베이스는 없다고 설명했다.[^krapp]
petercooper는 공개된 HN 코드의 미러 저장소를 가리키며
모든 것이 파일과 디렉터리일 뿐이라고 적고,
지금도 관리되는 변형으로 Anarki의 news 앱을 소개했다.[^petercooper]

나머지 댓글은 크게 세 갈래로 흘렀다.
한 갈래는 단일 서버가 생각보다 빠르고 믿을 만하다는 주장과
그것이 Kubernetes와 마이크로서비스에 대한 반론으로 번진 논쟁이다.
두 번째는 HN이 실제로 늘 켜져 있지는 않다는 관찰이다.
세 번째는 HN이 거의 바뀌지 않기 때문에 장애가 적다는 설명이다.
운영자인 dang이나 다른 HN 직원은 이 스레드에 직접 답하지 않았다.

## 분석

### 답의 핵심은 장애 지점의 수를 줄이는 것이다

nik736은 베어메탈 서버 한 대가 사람들이 생각하는 것보다 믿을 만하며,
복잡성은 실패할 수 있는 층을 계속 쌓는다고 썼다.[^nik736]
jazzyjackson은 존재하는지도 몰랐던 컴퓨터의 장애가
내 컴퓨터를 못 쓰게 만드는 것이 분산 시스템이라는
Lamport의 말을 꺼냈다.[^jazzyjackson]
jmartens는 HN에 알려진 베어메탈 장비 말고는
의존성이 거의 없을 것이라고 짐작했다.[^jmartens]

이 논리는 가용성을 장비의 신뢰도가 아니라 의존성 사슬의 길이로 본다.
여러 서비스가 직렬로 연결되면 전체 가용성은 각 가용성의 곱이 된다.
구성 요소가 하나뿐이면 곱할 것이 없다.
HN의 구조는 웹 서버, 애플리케이션, 저장소가 한 프로세스 안에 있고
그 프로세스가 한 장비 위에 있는 형태다.
이 구조에서 네트워크 너머로 가는 내부 호출은 없다.

srer는 같은 이야기를 성능 쪽에서 했다.[^srer]
단일 서버에서는 마이크로초 단위였을 메서드 호출이
분산 클라우드에서는 수백 밀리초의 HTTP 요청이 될 수 있고,
단일 서버의 1000배 앞선 출발이 확장 문제를 오래 늦출 수 있다는 주장이다.
srer는 Frank McSherry의 COST 논문을
AWS 계정을 주기 전에 읽혀야 할 글로 추천했다.

GeekNews에서도 같은 지점에 놀라는 반응이 나왔다.
nicewook은 글로벌 사이트가 예비용 스탠바이 하나를 포함해
단 2대로 운영된다는 점이 신기하다고 적었다.[^gn-nicewook]
kwangyeol은 HN의 반응성에 부족함을 느낀 적이 없었는데
이런 간단한 구조였다며 Ad-hoc 파일시스템이 무엇인지 궁금해했다.[^gn-kwangyeol]
xguru는 DB 없이 운영된다는 점이 흥미롭다며
GeekNews는 AWS에서 EC2와 RDS로 운영 중이라고 밝혔다.[^gn-xguru]

### 저장소가 파일이라는 사실은 스탠바이 구성과 맞물린다

krapp과 petercooper의 설명대로라면 HN의 데이터는 Arc 객체를 직렬화한 파일이다.
justsomehnguy는 파일시스템이 저장소라면 Redis도 필요 없고
운영체제가 최근 파일을 알아서 캐시한다고 받았다.[^justsomehnguy]
koolba가 fsync는 하길 바란다고 하자,
somat은 뉴스 사이트의 댓글이라면 완전한 비동기 마운트로도 버틸 것이라고 했다.
koolba는 HN의 실제 쓰기량은 거의 없으니 fsync를 꺼야 성능이 나온다면
뭔가 크게 잘못된 것이라고 반박했다.[^somat][^koolba]

파일 기반 저장은 복제 방식도 단순하게 만든다.
petercooper는 HN이 어떻게 하는지는 모른다고 전제하면서도,
Syncthing이나 rsync 스크립트, 혹은 cron으로 돌리는 압축과 복사로도
충분할 수 있다고 추측했다.
이것은 추측이며, 스레드 안에서 실제 복제 방식을 확인한 사람은 없다.
atmosx는 FreeBSD의 CARP 같은 이중화를 쓰는지, 왜 ZFS가 아닌지를 물었고,
dsr_는 디스크 교체는 미러가,
나머지는 두 번째 장비가 해결한다고 답했다.[^atmosx][^dsr_]
용량이 더 필요하면 새 장비를 만들어 뒤에서 복사하고
몇 분의 중단으로 넘어가면 된다는 설명이다.

### 늘 켜져 있다는 전제부터 정확하지 않다

질문의 전제에 반대하는 댓글이 여럿이었다.
sokoloff는 짧은 장애가 꽤 자주 있다고 관찰했고,[^sokoloff]
jve는 장애를 알리는 hnstatus Twitter 계정을 가리켰다.[^jve]
theandrewbailey는 일주일에 한 번쯤
몇 분씩 내려가는 것을 본다고 했다.[^theandrewbailey]

가장 정리된 답은 jasode의 것이다.[^jasode]
jasode는 온라인의 뜻을 둘로 나눴다.
HN 서버가 무엇이든 응답한다는 뜻이라면 HN은 늘 켜져 있다.
정상적인 응답 시간이라는 뜻이라면 일주일이나 한 달에 한 번쯤 요청을 처리할 수
없다는 메시지가 뜨고, 아주 인기 있는 스레드는 불러오는 데 1분 이상 걸린다.
그럴 때 dang은 글을 쓰지 않을 사람은 로그아웃해 달라고 스레드에 적는다.
로그아웃한 사용자의 페이지는 개인별 투표, 숨긴 댓글 같은 정보를 조회할 필요가
없어서 서버 부하가 줄어든다.
jasode는 이것을 클라우드에 인스턴스를 더 띄우는 대신
공동체가 즉석에서 협력해 부하를 줄이는 방식이라고 불렀다.

EduardoBautista도 로그아웃하면 서버가 캐시에서 바로 응답할 수 있다는 요청을
몇 번 보았다고 적었다.[^EduardoBautista]
pshc는 가끔 요청이 너무 많다는 오류를 받고 투표가 사라지기도 한다고 했고,[^pshc]
danuker가 빠르게 투표하고 답글을 누르면 뜨는 메시지를 언급하자
kqr은 그것은 처리 능력 부족이 아니라 신중한 과부하 보호라고 보았다.[^kqr]

## 비평

### 가장 많이 인용된 답은 이미 낡은 자료였다

질문이 올라온 2022년에 스레드가 내놓은 하드웨어 정보는
2018년 sctb의 설명이었다.
dang의 2021년 댓글이 구성이 그대로라고 확인해 주었지만,
2022년 시점에서 다시 확인한 사람은 없었다.
운영자가 스레드에 답하지 않았으니 스레드 전체가 4년 전 자료와
공개된 오래된 코드를 바탕으로 한 추론 위에 서 있다.

이 추론의 일부는 틀렸을 가능성도 있다.
ericpauley는 HN이 이제 CDN 뒤에 있어서 로그인하지 않으면
문제를 못 느낄 것이라고 적었고,[^ericpauley]
jjice는 스레드 다른 곳에서 비로그인 사용자에게 Nginx 캐시를 쓴다는 글을
보았다며 CDN도 아닌 것 같다고 답했다.[^jjice]
이 문서를 쓰며 Firebase API로 읽은 스레드의 공개 댓글 188개에는
Nginx 캐시를 말한 댓글이 없다.
어느 쪽도 출처를 대지 않았고,
확인되지 않은 두 주장이 서로를 고치는 모양이 되었다.

### 단순함을 원인으로, 낮은 요구 수준을 결과로 혼동한다

highlytedious는 HN이 매우 단순한 애플리케이션이며,
단순한 앱의 많은 트래픽과 복잡한 앱의 확장은
전혀 다른 문제라고 지적했다.[^highlytedious]
globular-toast는 HN 같은 사이트에서 사용자를 붙잡는 데
여러 개의 9가 붙는 가용성은 필요 없다고 했다.[^globular-toast]
JonAtkinson은 몇 분 중단이 사용자에게 무슨 손해이며,
그것을 막으려 복잡성을 더할 이유가 무엇이냐고 물었다.[^JonAtkinson]

이 세 댓글을 합치면 질문 자체가 뒤집힌다.
HN이 늘 켜져 있는 것처럼 보이는 이유의 상당 부분은
몇 분의 중단이 아무에게도 비용이 되지 않는다는 데 있다.
jasode도 이것이 토론 포럼이고 누구의 매출도 여기에 걸려 있지 않으니
지금보다 높은 가용성이 필요 없다고 결론지었다.
그러면 단순한 구조가 높은 가용성을 만든 것이 아니라,
낮은 가용성 요구가 단순한 구조를 허락한 것에 가깝다.
스레드의 다수 의견은 이 인과의 방향을 거의 묻지 않았다.

### Kubernetes 논쟁은 질문과 다른 문제를 다퉜다

arnaudsm이 1024개의 Kubernetes 노드와 70MB짜리 React 번들,
200명의 엔지니어가 필요한 줄 알았다고 비꼰 댓글이
스레드의 분위기를 정했다.[^arnaudsm]
이후 aristofun의 단일 VPS 경험담과 halfstar91의 반론을 거쳐
Kubernetes가 필요한 규모에 대한 긴 논쟁이 이어졌다.[^aristofun][^halfstar91]

이 논쟁에서 가장 쓸모 있는 말은 petercooper의 구분이다.[^petercooper-2]
Kubernetes는 운영보다 조직의 복잡성을 다루는 도구에 가깝고,
기술적 규모는 장비 한두 대로도 감당할 수 있지만
작은 회사도 정책, 팀, 조직 문제 때문에 표준화 도구가 필요하다는 것이다.
이 문서의 해석으로는 HN은 운영 조직이 매우 작아 조직 복잡성이 거의 없다.
그러니 HN을 근거로 Kubernetes를 비판하는 것은
비교 대상의 조건이 다른 논증이다.

### 변하지 않는 제품이라는 설명은 반만 맞다

thdxr은 HN이 성숙한 제품이고 흔한 장애는 대부분 변경 배포에서 오는데
HN은 매일 배포하지 않는다고 했다.[^thdxr]
thatoneguytoo도 장애는 대개 변경이 있을 때 일어나는데 HN은 변경이 없다고
간단히 정리했다.[^thatoneguytoo]

krapp은 이 통념에 반대했다.[^krapp-2]
레이아웃이 바뀌지 않을 뿐 HN은 생각보다 자주 바뀌며,
차단된 사용자에 대한 보증, 스레드 접기, Show HN, 두 번째 기회 풀 공개,
past 페이지, API, 스팸 탐지와 성능 변경 등을 예로 들었다.
orf는 그 목록이 그리 많지 않다며
HN이 잘 안 바뀐다는 점은 그대로라고 받았다.[^orf]
둘 다 맞다.
HN은 사용자 눈에 보이는 표면은 거의 고정하고,
안쪽의 모더레이션과 성능 작업은 계속 바꾼다.
안정성은 변경이 없어서가 아니라
변경의 표면적이 좁아서 나온다고 보는 편이 정확하다.

## 인사이트

### 가용성의 일부는 사용자가 떠맡는다

jasode가 묘사한 로그아웃 요청은 흔치 않은 운영 기법이다.
부하가 몰리면 서버를 늘리는 대신 사용자에게 가벼운 경로를 쓰라고 부탁한다.
로그인 사용자를 위한 개인화가 비싼 부분이고,
비로그인 페이지는 캐시할 수 있으니 이 부탁은 실제로 효과가 있다.

이 기법이 통하는 조건은 공동체의 신뢰다.
운영자의 요청을 사용자가 따를 만큼 관계가 있어야 하고,
사용자가 잠시 불편을 감수할 만큼 사이트에 애착이 있어야 한다.
상업 서비스에서 고객에게 로그아웃을 부탁하는 일은 상상하기 어렵다.
HN의 가용성은 기술 구조와 공동체 구조가 함께 만든 결과이며,
기술 구조만 따라 해서는 같은 결과를 얻기 어렵다는 것이 이 문서의 해석이다.

### 이 스레드 이후 HN의 병목은 실제로 코어 수였다

이 스레드에서 단일 서버의 위력을 말한 사람들이 몰랐던 사실이 있다.
HN 프로세스는 한 장비뿐 아니라 사실상 한 코어 위에서 돌았다.
dang은 이 스레드 두 달 뒤인 2022년 8월에 SBCL 위의 Arc 구현이
훨씬 빠르고 HN을 여러 코어에서 돌릴 수 있게 해 준다고 적었고,
그 전환은 2024년 9월에 이루어졌다.
이 과정은 이 저장소의 `hacker/hn-on-common-lisp.md`가 다룬다.

이 사실은 스레드의 결론을 강화하는 동시에 한계도 보여 준다.
16스레드 장비에서 한 코어만 쓰고도 하루 수백만 요청을 처리했다면
단일 서버의 여유는 스레드가 말한 것보다 더 크다.
그러나 인기 스레드에서 1분씩 걸리고
긴 스레드를 페이지로 나눠야 했던 제약도 그 한 코어에서 왔을 것이라고
이 문서는 해석한다.
단일 서버 예찬은 그 서버를 얼마나 쓰고 있었는지를 함께 물어야 완성된다.

### 장애 대비는 비용과 중단 비용의 비교로 결정된다

iso1631은 HN의 가장 큰 위험이 단일 데이터센터라는 점이라고 지적했다.[^iso1631]
네임서버가 모두 AWS Route 53이고 DNS TTL이 2분처럼 보인다는 관찰도 덧붙였다.
다른 지역의 대기 서버와 두 업체에 나눈 네임서버를 두면
샌디에이고가 지진으로 무너져도 버틸 수 있겠지만
비용 대비 이익이 있는지는 다른 문제라고 스스로 답했다.

이 계산은 모든 서비스에 같은 형태로 적용된다.
중단 1분의 비용이 작으면 대비는 백업과 스탠바이로 충분하다.
중단 1분의 비용이 크면 지역 분산과 자동 장애 조치가 필요하고,
그만큼 복잡성과 새로운 장애 지점이 생긴다.
HN 사례가 주는 교훈은 단순함 자체가 아니라
중단 비용을 정직하게 추정했을 때 대부분의 서비스가 HN 쪽에 가깝다는 점이다.

### 공개된 오래된 코드가 추론의 기준점이 된다

스레드의 기술적 설명 대부분은 운영자의 답이 아니라
Paul Graham이 오래전 공개한 Arc 코드에서 나왔다.
petercooper와 krapp은 공개 코드를 근거로 HN의 저장 구조를 설명했고,
mobilio는 Arc 포럼 링크를 붙이며 화면이 낯익지 않으냐고 물었다.[^mobilio]
CobaltFire는 Arc로 쓰인 것은 사실상 HN뿐이고
나머지는 초기 HN의 포크라고 정리했다.[^CobaltFire]

이것은 공개 코드가 가진 의외의 효과다.
실제 서비스 코드는 어뷰징 방지 때문에 공개되지 않지만,
오래된 공개판이 구조를 짐작하는 기준점이 되어 외부 사람들이
HN의 작동 방식을 설명할 수 있게 해 준다.
그 대가로 설명이 실제와 어긋나도 확인할 방법이 없다.
그 공개판의 구조는 `hacker/hackernews-arc-source.md`에서 다룬다.

---

[^notlukesky]: <https://news.ycombinator.com/item?id=31821318>

[^ignoramous]: <https://news.ycombinator.com/item?id=31821941>

[^5id]: <https://news.ycombinator.com/item?id=31821904>

[^sctb]: <https://news.ycombinator.com/item?id=16076041>

[^dang]: <https://news.ycombinator.com/item?id=28479595>

[^krapp]: <https://news.ycombinator.com/item?id=31822366>

[^petercooper]: <https://news.ycombinator.com/item?id=31822376>

[^nik736]: <https://news.ycombinator.com/item?id=31821564>

[^jazzyjackson]: <https://news.ycombinator.com/item?id=31821872>

[^jmartens]: <https://news.ycombinator.com/item?id=31830687>

[^srer]: <https://news.ycombinator.com/item?id=31822005>

[^justsomehnguy]: <https://news.ycombinator.com/item?id=31831550>

[^somat]: <https://news.ycombinator.com/item?id=31822808>

[^koolba]: <https://news.ycombinator.com/item?id=31825965>

[^atmosx]: <https://news.ycombinator.com/item?id=31822432>

[^dsr_]: <https://news.ycombinator.com/item?id=31822916>

[^sokoloff]: <https://news.ycombinator.com/item?id=31821865>

[^jve]: <https://news.ycombinator.com/item?id=31822079>

[^theandrewbailey]: <https://news.ycombinator.com/item?id=31826043>

[^jasode]: <https://news.ycombinator.com/item?id=31822454>

[^EduardoBautista]: <https://news.ycombinator.com/item?id=31850990>

[^pshc]: <https://news.ycombinator.com/item?id=31822923>

[^kqr]: <https://news.ycombinator.com/item?id=31822248>

[^ericpauley]: <https://news.ycombinator.com/item?id=31823925>

[^jjice]: <https://news.ycombinator.com/item?id=31849439>

[^highlytedious]: <https://news.ycombinator.com/item?id=31825720>

[^globular-toast]: <https://news.ycombinator.com/item?id=31822002>

[^JonAtkinson]: <https://news.ycombinator.com/item?id=31833438>

[^arnaudsm]: <https://news.ycombinator.com/item?id=31822418>

[^aristofun]: <https://news.ycombinator.com/item?id=31822062>

[^halfstar91]: <https://news.ycombinator.com/item?id=31822312>

[^petercooper-2]: <https://news.ycombinator.com/item?id=31822435>

[^thdxr]: <https://news.ycombinator.com/item?id=31823648>

[^thatoneguytoo]: <https://news.ycombinator.com/item?id=31822241>

[^krapp-2]: <https://news.ycombinator.com/item?id=31828349>

[^orf]: <https://news.ycombinator.com/item?id=31828642>

[^iso1631]: <https://news.ycombinator.com/item?id=31822279>

[^mobilio]: <https://news.ycombinator.com/item?id=31822145>

[^CobaltFire]: <https://news.ycombinator.com/item?id=31828120>

[^gn-nicewook]: <https://news.hada.io/topic?id=6877#cid10958>

[^gn-kwangyeol]: <https://news.hada.io/topic?id=6877#cid10960>

[^gn-xguru]: <https://news.hada.io/topic?id=6877#cid10954>
