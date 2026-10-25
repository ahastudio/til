# 분산 SQLite 12년: rqlite 저자가 2014년부터 다시 쓴 계보

원문: [Twelve years of distributed SQLite – Philip O'Toole](https://philipotoole.com/twelve-years-of-distributed-sqlite/)

HN 토론: <https://news.ycombinator.com/item?id=50217500> (370점, 63개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/rqefcw/twelve_years_distributed_sqlite> (16점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=35911>

## 요약

rqlite를 만든 Philip O'Toole가 2026년 10월 23일에 쓴 회고다.
2014년 9월에 SQLite 앞에 Raft 로그를 두고 모든 쓰기를 클러스터에 복제하는
rqlite를 공개했고, 그 주말에 소스를 GitHub에 올렸다고 한다.
저자가 아는 한 Raft와 SQLite를 결합한 최초의 오픈소스 시스템이며, 몇 년 동안
아무도 따라 하지 않았다.
지금은 분산 SQLite가 열두 개쯤의 프로젝트가 있는 분야가 됐고, 일부는 벤처 투자를
받았고 둘은 인수됐다.
이 분야를 쓰는 사람들이 이야기를 2021년쯤에서 시작하는 경향이 있어서
2014년부터의 이야기를 남기려 한다는 것이 글을 쓴 이유다.

글은 연도별로 이어진다.
2014년의 rqlite는 jut.io에서 일하던 시스템이 작은 관계형 저장소를 필요로 했던
구체적인 문제에서 나왔고, 합의 프로토콜로 SQLite를 복제하는 것이 답이었다고
한다.
저자는 그 일을 회사에서는 다른 방식으로 해결했지만 문제가 일반적이고 해법이
작아서 rqlite를 계속 만들었다.
처음에는 goraft를 쓰다가 2016년 초에 HashiCorp의 Raft 구현으로 바꿔 지금까지
쓰고 있다.
가장 중요한 설계 결정은 그때 내려졌고 바뀐 적이 없다.
rqlite는 CP 시스템이어서 쓰기는 리더를 거쳐야 하고 과반이 확인해야 하며 갈라진
소수 쪽은 쓰기를 거부한다.

저자는 정직을 위해 앞선 사례를 둘 든다.
Expensify는 자체 인프라에서 Paxos 계열 프로토콜로 SQLite를 복제해 왔고 2016년에
Bedrock으로 공개했다.
Erlang으로 만든 ActorDB는 행위자마다 Raft로 복제되는 SQLite를 주었고 rqlite와
비슷한 시기에 나왔다.
둘 다 출신 환경 밖에서는 널리 쓰이지 않았지만 아이디어가 이미 공기 중에 있었다는
증거라고 한다.

2017년에는 Canonical이 LXD와 MicroK8s에 etcd 없이 내장형 복제 저장소를 주려고
dqlite를 만들었다.
저자는 Mark Shuttleworth와 한 번 통화해 rqlite를 맞춰 볼 수 있을지 이야기했지만
맞지 않았다고 한다.
dqlite는 Go로 시작해 C로 다시 쓰였고, 의도는 rqlite와 가장 비슷하며 차이는 포장
방식이다.
dqlite는 내장하는 라이브러리이고 rqlite는 따로 띄우는 서버다.

2021년 Ben Johnson의 Litestream은 합의 없이 SQLite WAL을 감시해 S3로 흘려 단일
노드 SQLite의 재해 복구를 거의 공짜로 준다.
Litestream은 기계가 죽으면 어떻게 하느냐를, rqlite는 기계가 죽었는데 복원을
기다릴 수 없으면 어떻게 하느냐를 묻는다고 저자는 구분한다.
Fly.io가 2022년에 Ben을 고용해 파일시스템 수준에서 복제하는 LiteFS를 냈고,
Litestream은 rqlite 8.0의 WAL 처리 방식에 영감을 주었다고 한다.
2022년에는 cr-sqlite가 확장으로 CRDT를 더해 리더 없이 여러 작성자가 갈라졌다
합치게 했고, libSQL은 SQLite 자체를 포크했다.
libSQL 위에 에지 복제본을 둔 호스팅 서비스를 만든 Turso는 투자를 받았고 2026년에
Supabase가 인수했다고 한다.
Cloudflare의 D1과 Durable Objects 안의 SQLite 저장소처럼 이 분야는 직접 운영하는
것에서 사 쓰는 것으로 바뀌었다고 저자는 쓴다.

저자가 12년에서 읽은 것은 셋이다.
SQLite를 저장 엔진으로 두고 복제를 바깥에 더하는 핵심이 적어도 여덟 팀에 의해
서로 다른 필요와 프로토콜로 재발명됐다.
설계 공간에는 합의(rqlite, dqlite), 스트리밍(Litestream), 병합(cr-sqlite)의 세
모퉁이가 순서대로 나타났고, 논쟁의 대부분은 사용자들이 어느 질문이 맞는
질문인지를 두고 다투는 것이다.
그리고 투자와 인수는 서비스로 만든 플랫폼에 갔고, 아이디어는 누군가 팔기 전까지
8년 동안 오픈소스였다.
rqlite는 여전히 직접 운영하고 속을 알 수 있고 돈을 내지 않아도 되는 내결함
관계형 데이터베이스로 남는다.

## 분석

### 계보 서술은 설계 질문 세 개로 정리된다

글의 가장 쓸모 있는 부분은 연대기가 아니라 분류다.
합의는 하나의 리더에 강한 일관성과 클러스터를, 스트리밍은 하나의 작성자에 값싼
복구를, 병합은 여러 작성자에 결과적 일관성을 준다.
각각이 서로 다른 질문, 곧 기계가 죽었을 때 데이터를 잃지 않을 것인지, 죽은 뒤
복원을 기다릴 수 있는지, 여러 곳에서 동시에 쓸 수 있는지에 답한다.
이 분류 덕에 프로젝트 간 비교가 우열이 아니라 어떤 질문을 하는 사람이냐의 문제가
된다.
rqlite가 CP를 택했고 이후 바뀌지 않았다는 서술도 같은 틀 안에 있다.

### 2014년부터라는 시작점이 글의 주장이다

저자가 직접 말하듯 이 글은 이야기를 2021년에 시작하는 설명에 대한 응답이다.
시작 시점을 앞당기면 rqlite가 처음이고 이후 것들은 같은 아이디어의 다른 구현이
된다.
저자는 Bedrock과 ActorDB를 먼저 거론해 최초 주장을 방어한다.
이는 최초 주장의 범위를 좁히는 방식이다.
어떤 식으로든 먼저였다는 말이 아니라 독립된 범용 오픈소스로는 먼저였다는 말이
된다.

### 돈이 어디로 갔는지에 대한 서술이 글의 결론이다

저자는 오픈소스인 rqlite, dqlite, Litestream은 무료이고 투자를 받았거나 인수된
것은 이를 청구서가 있는 서비스로 만든 쪽이라고 한다.
이는 인프라 아이디어의 흔한 운명이라며 개의치 않는다고 한다.
다만 아이디어가 누군가 팔기 8년 전부터 오픈소스였다는 점은 기록할 가치가 있다고
쓴다.
이 결론은 기술적 주장이 아니라 공로를 누구에게 돌릴지에 대한 주장이다.

## 비평

### 이 글은 당사자의 계보여서 자기 프로젝트에 유리한 질문으로 틀을 짠다

저자는 rqlite를 만든 사람이고, 글의 마지막은 rqlite가 여전히 선택해야 할
것이라는 결론이다.
설계 공간의 세 모퉁이를 나눈 틀은 유용하지만, 그 틀에서 rqlite의 자리(내결함,
직접 운영, 무료)는 기준이 정해진 뒤에 정해진다.
HN에서 AgentME는 글이 D1을 갑자기 냉소적이고 무관심하게 다루고, 마지막 부분은
어색하게 방어적이고 패배적으로 느껴진다고 했다.[^AgentME]
brooksbp는 끝에서 청사진을 그린 사람이 누구인지 역사에 남기려는 의도가 눈에 띄어
읽는 재미가 가셨다고 했다.[^brooksbp]
반면 pbowyer는 벤처 지원을 받은 SQLite 서비스들이 마치 자기들이 아이디어를
냈다는 듯이 떠들어 왔으니 이런 균형이 공정하다고 했다.[^pbowyer]
이 반응들은 같은 글의 같은 의도를 다르게 읽은 것이다.
이 문서는 이 의도 자체를 판단하지 않고, 당사자가 쓴 글이라는 점만 짚는다.

### 비교에 빠진 축이 있다

gregsadetsky는 이 엔진들을 외부 의존성, 단일 리더인지 임의 노드 쓰기인지, 내장
라이브러리인지 서버인지로 비교한 표가 필요하다고 했다.[^gregsadetsky]
특히 트랜잭션 지원이 중요한 경계선이어서, 어떤 엔진은 SQLite의 전체 트랜잭션을
지원하고 rqlite는 공식적으로 BEGIN과 COMMIT을 지원하지 않는다고 했다.
이는 댓글의 주장이고 이 문서는 rqlite의 FAQ를 열어 보지 못했다.
Kinrany는 임베드 가능, 클러스터, 독립 노드, S3 백업, 선택적 AP를 한꺼번에 주는
프로젝트가 있는지 물었다.[^Kinrany]
글은 이런 축으로 비교하지 않고 각 프로젝트가 어떤 질문에 답하는지를 서술한다.
따라서 이 분야에서 무엇을 고를지 판단하려는 독자는 글만으로는 부족하다.

### 성능과 신뢰성 근거가 없다

글에는 처리량이나 지연, 장애 시나리오의 수치가 없다.
HN에서 a3nz3g는 벤치마크가 있는지, 어떤 사용 사례에서 이점이 있는지
물었다.[^a3nz3g]
jwr은 Jepsen 시험을 받았는지, 받지 않았다면 문제가 숨어 있을 것이라고
했다.[^jwr]
이에 tmsln은 저자의 블로그 글인 읽기 일관성 시험 글을 링크했다.[^tmsln]
이 문서는 그 글을 열어 보지 못했으므로 그 시험의 범위가 Jepsen 수준인지 판단하지
않는다.
gizzlon은 SQLite와 Litestream이면 충분히 안전했고, rqlite는 여러 곳에 저장된다는
보장을 주지만 단일 노드 데이터베이스보다 훨씬 느리다고 이해한다고
했다.[^gizzlon]
이 이해는 댓글의 것이다.

### 글쓴이가 누구인지에 대한 논쟁이 내용 논의를 가렸다

HN에서 가장 길게 이어진 답글 사슬 하나는 글이 AI로 쓰였는지에 관한 것이었다.
klamann은 자기 경험을 자기 목소리로 쓰는 데서 기쁨을 얻지 못하면 왜 쓰느냐고
했고,[^klamann] senderista는 자기 프로젝트의 이야기를 자기 말로 하지 못한다는
점이 실망스럽다고 했다.[^senderista]
phrotoma는 이 글에서 LLM의 느낌이 전혀 들지 않는다고 했는데,[^phrotoma]
AgentME는 자기 눈에는 가득하며 Pangram도 글 전체를 AI 생성으로 표시한다고
답했다.[^AgentME-pangram]
Lobste.rs에서도 antonz가 rqlite는 훌륭한 제품이고 Philip이 오랫동안 잘 관리해 왔다고 하면서, 글에 쓴 문장 몇 개를 인용해 이것이 본인인지 Claude인지 물었다.[^antonz]
이 문서는 글의 작성 방식을 판정할 수 없고 판정하지 않는다.
다만 이 논쟁이 글의 연표가 맞는지 같은 내용 논의를 밀어냈다는 점은 스레드에서
확인할 수 있다.

## 인사이트

### 오픈소스가 먼저여도 서사의 주도권은 서비스를 파는 쪽이 가져간다

저자의 불만은 이 분야 이야기를 쓰는 사람들이 2021년쯤에서 시작한다는 것이다.
이는 설명의 출처가 투자와 마케팅을 가진 쪽에 있다는 뜻이다.
서비스를 파는 회사는 소개 글과 컨퍼런스 발표와 문서로 서사를 만들고, 무료
오픈소스 유지관리자는 이를 만들 자원이 적다.
그래서 먼저 한 일의 기록은 오히려 뒤늦게 당사자가 직접 쓰게 된다.
pbowyer가 데이터베이스 분야의 많은 것이 20년 전까지 거슬러 올라가니 더 멀리
추적한 글이 더 있었으면 한다고 한 것도 같은 문제의식이다.[^pbowyer]
이 관찰은 이 문서의 해석이다.

### 운영 부담을 피하려는 이동은 SQLite가 아니라 서버 쪽으로도 간다

mmnfrdmcx는 에이전트와 일하면서 Postgres 관리가 매우 쉬워졌고 SQLite는 SQL
기능이 제한적이니, 원격 SQLite를 고려한다면 데이터베이스 서버를 쓰기 좋은 때라고
했다.[^mmnfrdmcx]
smellf는 같은 경험을 했고 내장되거나 호스팅 서버가 없는 경우에만 SQLite를
고른다고 답했다.[^smellf]
rapind는 문제가 원격 SQLite이며 한 대의 큰 서버에서 프로세스 안의 SQLite와
Litestream 백업이면 90%가 넘는 애플리케이션에 낫다고 했다.[^rapind]
이 세 의견은 서로 반대 방향이다.
분산 SQLite라는 분야 자체가 SQLite의 단순함과 서버 데이터베이스의 기능 사이에서
어디에 서느냐의 문제를 가리키고 있다.
글은 이 갈림길을 다루지 않고 SQLite를 유지하는 쪽의 선택지만 나열한다.

### 관리형 서비스의 신뢰도는 사용자 경험에서 드러난다

piterrro는 프로덕션에서 D1을 써 보니 신뢰할 만하지 않았다며, D1이 사실상 Durable
Object 위의 래퍼라는 D1 개발자의 댓글을 인용했다.[^piterrro]
unconscionable도 D1이 매우 불안정했다고 했다.[^unconscionable]
ruther4d는 D1이 읽기 복제와 시점 복구를 주지만 Durable Object처럼 동적으로 만들
수 없어 멀티테넌시가 어렵다고 했다.[^ruther4d]
글은 D1에 대해 한두 문장뿐이어서, 이 대화는 글이 건너뛴 부분을 사용자 경험으로
채운다.
다만 이는 댓글의 증언이고 이 문서는 확인하지 못했다.

### 이 글을 읽는 방법

이 글은 rqlite의 저자가 쓴 연표이며, 어느 프로젝트를 고를지의 근거로 쓰기에는
비교 축과 수치가 부족하다.
오늘 할 일은 글이 나눈 세 질문(기계가 죽을 때 잃어도 되는 데이터의 양, 복원을
기다릴 수 있는 시간, 동시에 쓰는 곳의 수)에 자기 서비스의 답을 먼저 적는 것이다.
그 답이 정해지면 후보를 합의, 스트리밍, 병합 세 갈래 중에서 고를 수 있다.
이 글의 주장을 가를 관찰은 두 가지다.
rqlite가 Raft와 SQLite를 결합한 최초의 독립 범용 오픈소스라는 주장이 Bedrock과
ActorDB를 포함한 목록에서 다른 기록과 맞는지, 그리고 rqlite의 쓰기 지연과
트랜잭션 지원이 같은 조건의 다른 엔진과 비교해 어떤지다.
둘 다 이 글에는 없다.

---

[^AgentME]: <https://news.ycombinator.com/item?id=50219960>

[^brooksbp]: <https://news.ycombinator.com/item?id=50218493>

[^pbowyer]: <https://news.ycombinator.com/item?id=50219132>

[^gregsadetsky]: <https://news.ycombinator.com/item?id=50225066>

[^Kinrany]: <https://news.ycombinator.com/item?id=50218636>

[^a3nz3g]: <https://news.ycombinator.com/item?id=50218267>

[^jwr]: <https://news.ycombinator.com/item?id=50219701>

[^tmsln]: <https://news.ycombinator.com/item?id=50220822>

[^gizzlon]: <https://news.ycombinator.com/item?id=50219277>

[^klamann]: <https://news.ycombinator.com/item?id=50219224>

[^senderista]: <https://news.ycombinator.com/item?id=50223570>

[^phrotoma]: <https://news.ycombinator.com/item?id=50220045>

[^AgentME-pangram]: <https://news.ycombinator.com/item?id=50220436>

[^mmnfrdmcx]: <https://news.ycombinator.com/item?id=50219987>

[^smellf]: <https://news.ycombinator.com/item?id=50223112>

[^rapind]: <https://news.ycombinator.com/item?id=50225312>

[^piterrro]: <https://news.ycombinator.com/item?id=50218626>

[^unconscionable]: <https://news.ycombinator.com/item?id=50219202>

[^ruther4d]: <https://news.ycombinator.com/item?id=50220205>

[^antonz]: <https://lobste.rs/s/rqefcw/twelve_years_distributed_sqlite#c_avi4ib>
