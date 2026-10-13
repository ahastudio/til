# Postgres가 느린 게 아니라 스토리지가 느리다

원문: [POSETTE Talk Recap - Postgres Isn't Slow. Your Storage Is | ClickHouse](https://clickhouse.com/blog/posette-talk-recap-postgres-isnt-slow-your-storage-is)

HN 토론: <https://news.ycombinator.com/item?id=50052163> (170점, 179개 댓글)

GN 토론: <https://news.hada.io/topic?id=35244>

## 요약

ClickHouse 블로그가 2026년 8월 20일에 올린 글로,
POSETTE 2026에서
Sai Srirampur가 발표한 “Postgres Isn't Slow. Your Storage Is.”를 정리했다.
발표는 PostgreSQL이 수백 GB에서
TB 규모로 커질 때 흔히 나타나는 다섯 가지 증상에서 출발한다.
UPDATE와 UPSERT가 많은 적재 작업이 몇 초에서 몇 분으로 늘어나고,
일부 쿼리만 느려져 P95 지연이 밀리초에서 초 단위로 튄다.
autovacuum이 밀려 테이블 팽창이 GB에서 TB로 쌓이고,
체크포인트가 클라이언트 작업과 I/O와 CPU를 다투며,
Kafka나 ClickHouse로 보내는 논리 복제가 지연된다.
글은 이 증상들의 원인이 늘 같지는 않지만,
간과하기 쉬운 공통 원인이 스토리지 성능일 수 있다고 주장한다.

연결 고리는 이렇다.
작업 집합이 PostgreSQL 메모리와 운영체제 페이지 캐시를 넘어서면
물리 I/O가 늘어나고,
느린 스토리지에서는 그 비용과 대기열이 평균 지연과 꼬리 지연을 함께 키운다.
힙과 인덱스 쓰기, WAL 동기화, 체크포인트, VACUUM, 논리 디코딩 스필은
모두 같은 대역폭, IOPS, 대기열을 나눠 쓴다.
스토리지가 한계에 닿으면 작업들이 서로를 늦추고,
겉보기에 무관한 여러 문제가 한 원인에서 생긴다.
로컬 NVMe가 I/O를 없애지는 않지만,
네트워크 스토리지에서
밀리초 걸리던 작업을 수십 마이크로초로 줄일 수 있다는 것이 글의 논지다.

벤치마크는 스토리지만 다르게 한 PostgreSQL 클러스터 여덟 개로 진행했다.
네 개는 인스턴스 스토어 NVMe, 네 개는 3,000 IOPS의 기본 gp3 EBS를 썼고,
모두 vCPU 16개, RAM 64GiB의 m6id.4xlarge에 `shared_buffers` 16GiB였다.
데이터는 33억 행, 482GiB의 `pgbench_accounts` 테이블이고,
클라이언트 64개와 워커 스레드 16개가 5분 동안 무작위 UPDATE를 실행했다.

```text
\set aid random(1, 3300000000)
UPDATE pgbench_accounts SET abalance = abalance + 1 WHERE aid = :aid;
```

결과는 NVMe 중앙값 16,030 TPS, EBS 1,734 TPS로 9.24배 차이였고,
트랜잭션 지연 중앙값은 36.9ms에서 4.0ms로 줄었다.
10GB 팽창에 대한 VACUUM은 NVMe 366초, EBS 964초가 걸렸고,
10GB 논리 복제 적체를 비우는 데는 139초와 238초가 걸렸다.
글은 이 결과가 이 작업 부하와 이 스토리지 구성에만 해당하며,
다른 EBS 설정이면 결과가 달라질 가능성이 크다고 단서를 단다.

EBS의 37ms 지연은 페이지 읽기 약 19ms(NVMe 0.3ms),
커밋 때 WAL `fsync` 11ms(NVMe 1.5ms),
락과 스케줄러 오버헤드 약 5ms(NVMe 0.2ms)로 나뉘었고,
CPU 작업 자체는 양쪽 모두 약 2ms였다.
실행 중간의 `pg_stat_activity` 스냅숏에서는 백엔드 64개 중
EBS 29개, NVMe 9개가 `IO:DataFileRead`를 기다리고 있었다.
약 240초의 프로파일링 동안 NVMe 호스트는 2,253 CPU초(코어 약 9.4개)를 썼지만
EBS 호스트는 251 CPU초(코어 약 1개)만 썼다.
EBS 쪽 프로세스는 CPU 밖에서 스토리지를 기다리는 시간이 훨씬 길었다는 뜻이다.

마지막으로 글은 인스턴스 스토어가 노드와 함께 사라진다는 반론에 답한다.
내구성을 개별 노드가 아니라 클러스터 수준에서 확보하면 된다는 것이다.
`ANY 1 (standby1, standby2)` 같은 쿼럼 동기 복제로
두 대기 서버 중 하나만 확인하면 커밋하고,
노드를 가용 영역에 나눠 둔다.
WAL-G 같은 도구로 베이스 백업과 WAL을 객체 스토리지에 계속 보내
초 단위 RPO와 시점 복구를 노리고, 백업은 별도 장애 영역과 다른 리전에도 둔다.
Instacart와 Datadog이 로컬 NVMe PostgreSQL을 쓰는 사례로 소개되며,
글은 ClickHouse Managed Postgres 가입 안내로 끝난다.

## 분석

### 글의 힘은 지연을 항목별로 나눈 회계에 있다

이 글이 다른 “클라우드 디스크는 느리다”는 주장과 다른 점은 숫자의 형태다.
TPS가 9배 차이 난다는 결과만 있었다면 설정 차이나 운 탓으로 넘길 수 있다.
그런데 글은 37ms를 페이지 읽기, WAL `fsync`, 락 대기, CPU로 쪼개고,
CPU 시간이 양쪽 모두 2ms로 같다는 점을 보여 준다.
PostgreSQL이 일을 더 한 것이 아니라 기다린 것이라는 결론이 숫자에서 바로 나온다.

CPU 프로파일은 이 주장을 뒤집어서 확인한다.
EBS 호스트는 코어 16개 중 하나 정도만 쓰고 있었다.
흔히 데이터베이스가 느리면 더 큰 인스턴스로 올리는데,
이 측정대로라면 그 돈은 기다리는 코어를 더 사는 데 쓰인다.
HN의 matthorse는 클라우드가 하드웨어 사양을 vCPU 개수로 줄이고
네트워크 스토리지를 기본값으로 만들면서,
그 지연을 Postgres의 지연으로 착각하게 되었다고 짚었다.[^matthorse]

### 내구성의 위치를 스토리지에서 클러스터로 옮기자는 제안이다

EBS가 기본값이 된 이유는 성능이 아니라 내구성과 이동성이다.
nik736이 정리했듯 로컬 스토리지는 호스트가 죽으면 VM도 함께 죽지만,
EBS는 여러 호스트에 복제되어 다른 호스트에서 다시 붙일 수 있다.[^nik736]
mightyham은 이것을 지연과 가용성의 교환이라고 부르며,
Kafka, Spanner, DynamoDB, CockroachDB처럼 복제와 합의를 내장한 데이터베이스는
사실상 모든 저장 요청에서
네트워크를 거치는 같은 선택을 한다고 덧붙였다.[^mightyham]

글의 제안은 이 교환을 다른 층에서 하자는 것이다.
블록 장치가 모든 쓰기를 원격으로 복제하는 대신,
PostgreSQL이 WAL을 스트리밍 복제로 보내고 백업은 객체 스토리지에 쌓는다.
dangoodmanUT는 이 구조가 유리한 이유를 정확히 짚었다.
네트워크 스토리지 위의 애플리케이션은 작은 I/O가 빠르고 로컬이라고 가정하므로
네트워크 지연이 상각되지 않지만,
애플리케이션 수준 복제는 커밋 같은 몇 단계에만 네트워크를 쓰게 만든다.
데이터베이스가 디스크보다
언제 네트워크를 건드려야 하는지 더 잘 안다는 것이다.[^dangoodmanUT]

### 이 글은 판매 문서이기도 하다

글을 실은 곳이 ClickHouse 블로그이고
마지막 문단이 ClickHouse Managed Postgres 가입 안내라는 점은
읽는 방식에 영향을 준다.
ClickHouse는 분석 데이터베이스 회사지만
이제 PostgreSQL 관리형 서비스를 팔고 있고,
“스토리지가 문제”라는 진단은
로컬 NVMe 기반 관리형 서비스라는 처방과 짝을 이룬다.
발표의 다섯 증상 가운데 하나가
Kafka나 ClickHouse로 가는 논리 복제 지연이라는 점도
같은 맥락에서 읽힌다.

판매 문서라고 해서 숫자가 틀린 것은 아니다.
다만 어떤 기준선을 골랐는지, 무엇을 측정하지 않았는지를 따져 볼 이유가 된다.
비평은 그 두 가지에서 시작한다.

HN에서는 발표자 Sai Srirampur 본인으로 보이는 saisrirampur 계정이 이 성격을 드러냈다.
CodesInChaos가 원자적 스냅숏과 비동기 복제 같은 부가 기능을 얹은 NVMe를
클라우드가 제공해 주면 좋겠다고 하자,[^CodesInChaos]
곧 자기들에게서 소식을 듣게 될 것이라고 답했다.[^saisrirampur]
벤치마크가 제기한 문제를 풀 상품이 준비되고 있다는 예고다.

## 비평

### 기준선이 가장 느린 EBS이고, 작업 부하는 캐시를 피하도록 짜였다

비교 대상은 3,000 IOPS로 프로비저닝한 기본 gp3다.
gp3의 기본 성능 그대로이고, 같은 EBS 안에서도 가장 싼 선택에 가깝다.
글도 다른 EBS 설정이면 결과가 달라질 것이라고 인정하지만,
제목은 “your storage”라는 일반론을 택했다.
HN의 d1l은 gp3에서 io2로 옮기자 지연이 줄고 내구성도 나아졌으며,
IOPS를 크게 프로비저닝하지 않아도 연쇄적으로 시스템이 안정되었다고 적었다.[^d1l]
같은 네트워크 스토리지 안에서도 등급에 따라 결과가 크게 달라진다는 반례다.

작업 부하도 극단적이다.
482GiB 테이블에 `shared_buffers`는 16GiB, RAM은 64GiB이고,
UPDATE 대상 행은 33억 개 중에서 균일하게 무작위로 고른다.
캐시가 거의 맞지 않도록 설계된 부하이며,
실제 서비스처럼 최근 데이터나 인기 행에 접근이 몰리는 경우와는 다르다.
glimshe가 비꼬듯 “데이터가 캐시에 없을 뿐”이라는 요약도 가능하고,[^glimshe]
traceroute66은 대부분의 경우 느린 원인은 스토리지가 아니라
스키마와 쿼리라고 반박했다.[^traceroute66]
boxed가 아무리 좋은 스키마도 멀리 있는 스토리지를 이기지 못한다고 하자
nijave가 아무리 좋은 스토리지도 나쁜 스키마를 구하지 못한다고 받아친 대화가
이 글이 빠뜨린 균형을 잘 보여 준다.[^boxed][^nijave]

### 벤치마크는 글이 권하는 운영 구조를 측정하지 않았다

9.24배라는 숫자는 단일 노드 클러스터끼리의 비교다.
그런데 글이 운영 환경에 권하는 구조는 가용 영역에 걸친 쿼럼 동기 복제다.
동기 복제에서는 커밋할 때마다
다른 가용 영역의 대기 서버가 WAL을 받았다고 답해야 한다.
NVMe에서 1.5ms였던 커밋 경로에 영역 간 네트워크 왕복이 다시 들어오는 셈이다.

물론 이 왕복은 EBS가 모든 페이지 읽기와 쓰기에 거는 네트워크 비용과는 다르다.
페이지 읽기는 여전히 로컬에서 끝나고 네트워크는 커밋 때만 쓰이므로,
dangoodmanUT가 말한 상각이 일어난다.
그래도 글이 독자에게 권하는 구조의 성능은 측정되지 않았고,
9배라는 숫자를 그 구조의 기대치로 읽으면 안 된다.
“durability를 클러스터 수준에서 제공하면 된다”는 짧은 답이
가장 비싼 부분을 측정 없이 넘긴다.

### 비용과 운영 부담은 한 줄도 계산하지 않았다

글은 성능만 비교하고 가격은 비교하지 않는다.
로컬 NVMe 구조는 노드 세 대(주 서버와 대기 서버 둘)가 필요하고,
저장 용량이 인스턴스 유형에 묶이므로
디스크가 부족하면 인스턴스 자체를 키워야 한다.
노드 하나를 잃으면 수백 GB를 네트워크로 다시 복제해 새 대기 서버를 채워야 하고,
그동안 클러스터는 대기 서버가 하나 줄어든 상태로 돈다.
EBS는 이 모든 일을 블록 계층에서 대신해 준다.

ngrilly는 로컬 NVMe를 쓰면 복제, 장애 조치, 백업을 직접 책임져야 하지만
복제된 블록 스토리지는 그 문제를 대부분 밖으로 넘길 수 있다고
정리했다.[^ngrilly]
vbezhenar는 네트워크 스토리지 덕분에 Kubernetes에서 데이터베이스가
노드 사이를 옮겨 다닐 수 있다며,
단순함이 그 값을 할 때가 있다고 했다.[^vbezhenar]
반대로 nasretdinov는 네트워크 블록 스토리지는 HDD 시대에나 의미가 있었고,
어차피 복제는 필요하니
로컬 NVMe와 복제가 더 단순하고 견고하다고 맞섰다.[^nasretdinov]
글이 이 논쟁에 답하려면
운영 인력과 장애 시나리오의 비용까지 숫자로 보여 줘야 했다.

dikei는 비용 쪽에서 반대 계산을 내놓았다.
대부분의 애플리케이션 데이터베이스는 SSD 한 장보다 훨씬 작아서,
여러 데이터베이스가 저장소를 나눠 쓰는
NAS나 SAN이 비용 효율적이라는 것이다.[^dikei-nas]
처음부터 비싼 NVMe 서버에 수천 달러를 쓰고도
애플리케이션이 그 1%도 쓰지 못한 채
폐기될 수 있다는 지적도 덧붙였다.[^dikei-tradeoff]

### Instacart와 Datadog 사례는 결론이 아니라 조건이다

글은 Instacart와 Datadog을 근거로 이 패턴이 이론이 아니라고 말한다.
그러나 두 회사는 데이터베이스 운영 전담 팀을 가진 조직이고,
글 스스로도 그들이 지연에 민감한 특정 작업이나
그런 성능이 필요한 작업에 NVMe를 쓴다고 표현한다.
즉 사례가 보여 주는 것은 “모두 NVMe로 가라”가 아니라
“측정으로 스토리지 병목이 확인된 작업만 옮겨라”다.

이 차이는 글의 마지막 단락과도 맞닿는다.
글은 제목보다 결론이 일부러 좁다고 스스로 말하며,
스토리지에 묶인 작업 부하에서 I/O 비용을 크게 줄이지만
운영 모델이 달라진다고 정리한다.
제목의 단언과 결론의 단서 사이 간격이 이 글의 가장 큰 약점이다.

## 인사이트

### 대기 이벤트와 놀고 있는 CPU가 가장 싼 진단 도구다

이 글에서 그대로 가져다 쓸 수 있는 것은 결론보다 진단 방법이다.
`pg_stat_activity`의 `wait_event`가 `IO:DataFileRead`인 백엔드 비율,
그리고 부하가 높은데 CPU가 놀고 있는지를 보면
스토리지 병목인지 쿼리 문제인지를 큰 비용 없이 가를 수 있다.
EBS 호스트에서 백엔드의 45%가 읽기를 기다리고
CPU는 코어 하나만 쓰고 있었다는 패턴은
인스턴스를 키워도 해결되지 않는 상황의 전형이다.

반대로 CPU가 꽉 차 있고 대기 이벤트가 적다면 문제는 스토리지가 아니다.
traceroute66이 말한 스키마와 쿼리, kebsup가 늦게 알았다는
인덱스 전용 스캔(index-only scan)과
커버링 인덱스 같은 문제일 가능성이 크다.[^kebsup]
같은 증상에 두 처방이 경쟁할 때,
이 두 지표가 어느 쪽 말을 들을지 정해 준다.

### 저장 계층은 HDD 이후 한 바퀴를 돌아 다시 로컬로 오고 있다

데이터베이스 저장 장치의 위치는 몇 번 오갔다.
디스크가 느리던 시절에는
SAN이 여러 서버의 디스크를 모아 성능과 관리를 함께 얻었고,
클라우드는 그 모델을 EBS 같은 네트워크 블록 스토리지로 되살렸다.
HDD가 수 밀리초 걸리던 때에는 네트워크 왕복이 상대적으로 작은 비용이었다.
NVMe가 수십 마이크로초로 내려오자 같은 왕복이 지연의 대부분이 되었다.

그래서 관리형 서비스도 방향을 바꾸고 있다.
HN의 iancarroll은 RDS 인스턴스를 r8g에서 로컬 NVMe가 붙은 r8gd로 옮기자
평균 I/O 지연이 1.0ms에서 0.1ms로 줄었다고 적었다.[^iancarroll]
CodesInChaos는 클라우드가 원자적 스냅숏과 비동기 복제를 얹은
NVMe를 팔았으면 좋겠다고 했다.[^CodesInChaos]
결국 시장이 원하는 것은 “로컬의 지연과 네트워크 스토리지의 편의”이고,
그 둘을 묶어 파는 회사가 다음 관리형 데이터베이스 경쟁의 축이 될 것이다.
ClickHouse가 이 발표를 블로그에 실은 이유도 거기에 있다.

### 로컬 NVMe는 계산과 저장을 다시 하나로 묶는다

네트워크 블록 스토리지의 숨은 장점은 계산과 저장을 따로 늘릴 수 있다는 점이다.
디스크가 부족하면 볼륨만 키우고, CPU가 부족하면 인스턴스만 바꾼다.
rtp4me가 말했듯 처음에는 얼마나 많은 공간과 성능이 필요한지 모르기 때문에
이 유연성이 비용 효율적인 선택을 돕는다.[^rtp4me]

로컬 NVMe로 가면 이 둘이 다시 묶인다.
저장 용량이 필요하면 CPU와 메모리까지 함께 사야 하고,
데이터가 자랄수록 인스턴스 유형 선택이 용량 계획이 된다.
하드웨어 가격도 변수다.
linsomniac은 4년 전 1만 4천 달러에 산 사내 데이터베이스 서버가
지금 같은 사양이면 9만 6천 달러라고 적었다.[^linsomniac]
성능만 보면 로컬 NVMe가 명백히 낫지만,
데이터 증가 속도가 빠르고 예측하기 어려운 서비스일수록
그 성능을 사는 대가로 용량 계획의 유연성을 내주게 된다.

Kubernetes 생태계는 이 재결합을 이미 받아들이고 있다.
smartbit은 CloudNativePG가 Kubernetes 로컬 영구 볼륨을 주요 기능으로 지원하며,
WAL과 테이블스페이스를 위한 별도 볼륨과
볼륨 재사용까지 다룬다고 소개했다.[^smartbit]
로컬 디스크에 묶인 데이터베이스를 운영하는 일은
스토리지 계층이 아니라 오퍼레이터와 복제 계층의 책임이 되고 있다.

### 단일 노드의 속도는 SQLite식 설계를 다시 매력적으로 만든다

이 글의 숫자는 PostgreSQL 이야기지만,
같은 논리를 끝까지 밀면
데이터베이스와 애플리케이션을 한 머신에 두는 설계가 나온다.
bob1029는 같은 머신의 웹 서버, SQLite, NVMe 조합에서
상태를 바꾸는 요청 전체를
수십에서 수백 마이크로초에 처리한다고 적었고,[^bob1029]
tilemarch는 게임 월드마다 SQLite 파일 하나를 두고
Litestream으로 WAL을 객체 스토리지에 보내 내구성을 확보했다고 했다.[^tilemarch]

이 구조는 글이 제안한 PostgreSQL 구조의 축소판이다.
빠른 로컬 저장과 객체 스토리지로의 연속 백업이라는 두 요소가 같다.
차이는 복제와 장애 조치를 얼마나 자동화하느냐다.
로컬 저장의 지연이 낮아질수록,
“어디까지를 한 머신에서 끝내고 어디부터 네트워크로 넘길 것인가”라는 질문이
데이터베이스 선택보다 먼저 와야 하는 설계 질문이 된다.

---

[^matthorse]: <https://news.ycombinator.com/item?id=50053926>

[^nik736]: <https://news.ycombinator.com/item?id=50053541>

[^mightyham]: <https://news.ycombinator.com/item?id=50055797>

[^dangoodmanUT]: <https://news.ycombinator.com/item?id=50055383>

[^d1l]: <https://news.ycombinator.com/item?id=50055297>

[^glimshe]: <https://news.ycombinator.com/item?id=50054322>

[^traceroute66]: <https://news.ycombinator.com/item?id=50053153>

[^boxed]: <https://news.ycombinator.com/item?id=50053581>

[^nijave]: <https://news.ycombinator.com/item?id=50054650>

[^ngrilly]: <https://news.ycombinator.com/item?id=50053244>

[^vbezhenar]: <https://news.ycombinator.com/item?id=50055313>

[^nasretdinov]: <https://news.ycombinator.com/item?id=50053028>

[^kebsup]: <https://news.ycombinator.com/item?id=50054825>

[^iancarroll]: <https://news.ycombinator.com/item?id=50053076>

[^CodesInChaos]: <https://news.ycombinator.com/item?id=50053274>

[^rtp4me]: <https://news.ycombinator.com/item?id=50054771>

[^linsomniac]: <https://news.ycombinator.com/item?id=50055377>

[^bob1029]: <https://news.ycombinator.com/item?id=50053374>

[^tilemarch]: <https://news.ycombinator.com/item?id=50056473>

[^saisrirampur]: <https://news.ycombinator.com/item?id=50059247>

[^dikei-nas]: <https://news.ycombinator.com/item?id=50053959>

[^dikei-tradeoff]: <https://news.ycombinator.com/item?id=50053889>

[^smartbit]: <https://news.ycombinator.com/item?id=50054900>
