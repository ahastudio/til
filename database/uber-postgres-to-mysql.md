# Uber는 왜 Postgres에서 MySQL로 옮겼나

원문: [Why Uber Engineering Switched from Postgres to MySQL](https://www.uber.com/in/en/blog/postgres-to-mysql-migration/)

HN 토론: <https://news.ycombinator.com/item?id=12166585> (731점, 294개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/b4hbxr/why_uber_engineering_switched_from>

## 요약

Evan Klitzke가 2016년 7월 26일에 쓴 Uber 엔지니어링 블로그 글이다.
Uber의 초기 아키텍처는 Postgres를 영속 계층으로 쓰는
모놀리식 Python 백엔드였고,
마이크로서비스로 넘어가면서 Postgres가 담당하던 상당수 용례를
“Schemaless, a novel database sharding layer built on top of MySQL”로
옮겼다고 밝힌다.
글이 드는 Postgres의 문제는 다섯 가지다.
쓰기에 비효율적인 구조, 비효율적인 복제, 테이블 손상,
부실한 복제본 MVCC 지원, 그리고 새 릴리스로 올리기 어렵다는 점이다.
분석 대상은 주로 Postgres 9.2이며,
저자는 “the internal architecture that we discuss in this article has
not changed significantly in newer Postgres releases”라고 단서를 단다.

기술적 논지의 중심은 온디스크 형식이다.
Postgres는 불변 행 데이터인 튜플(tuple)을 쓰고,
각 튜플은 디스크 위치를 뜻하는 ctid로 식별된다.
인덱스는 인덱스 필드를 ctid에 직접 대응시킨다.
레코드를 갱신하면 제자리에서 고치지 않고 새 ctid를 가진 새 튜플을 만들며,
autovacuum이 옛 튜플을 걷어 갈 때까지 양쪽 모두 인덱스에 남는다.
그래서 필드 하나를 바꿔도 물리적 쓰기가 여러 번 일어난다.
새 행 튜플을 테이블스페이스에 쓰고,
기본 키 인덱스를 새 ctid로 갱신하고,
보조 인덱스 전부를 새 ctid로 갱신해야 한다.
“For tables with a large number of secondary indexes,
these superfluous steps can cause enormous inefficiencies”이며,
이 모든 쓰기가 WAL에도 기록되므로 문제가 겹친다.

쓰기 증폭은 그대로 복제 증폭이 된다.
Postgres 복제는 물리 수준에서 이루어지므로
작은 논리적 변경도 여러 WAL 항목으로 네트워크를 건너간다.
Uber에게 이것은 서부와 동부 데이터센터 사이의 복제 문제였다.
연쇄 복제(cascading replication)가
데이터센터 간 대역폭 요구를 줄여 주긴 하지만
프로토콜 자체의 장황함은 남았고,
피크 트래픽 때는 WAL 아카이브가 스토리지 서비스로 따라가지 못하는 일도
있었다.
마스터 승격 과정에서는 Postgres 9.2 버그로
복제본이 타임라인 전환을 잘못 따라가
일부 WAL 레코드가 잘못 적용됐고,
비활성으로 표시되어야 할 레코드가 활성으로 남아 질의가 중복 결과를 냈다.
손상 양상은 복제본마다 달랐고,
물리 복제이기 때문에 B-tree 인덱스 손상이 퍼질 가능성을 우려했다고 적는다.

복제본 MVCC와 업그레이드도 물리 복제의 결과다.
스트리밍 복제본이 WAL을 적용할 때
오래 도는 트랜잭션이 적용을 막을 수 있어,
Postgres는 일정 시간 이상 WAL 적용을 막는 트랜잭션을 죽인다.
ORM을 쓰다 보면
블로킹 I/O 중에 트랜잭션을 열어 둔 채로 두기 쉬운데,
그러면 애플리케이션이 깨진다.
업그레이드는 9.3 마스터가 9.2 복제본으로 복제할 수 없고 그 반대도 안 되기
때문에,
마스터를 내리고 `pg_upgrade`를 돌리고(대형 DB에서는 몇 시간)
새 스냅숏을 만들고 복제본을 전부 지웠다 복원하고 따라잡기를 기다려야
한다.
Uber는 9.1에서 9.2로 한 번 올린 뒤
다시는 그 과정을 감당할 수 없다고 판단했고,
그래서 레거시 인스턴스는 현재 릴리스가 9.5인 시점에도
9.2에 머물러 있다고 적는다.

MySQL 쪽 논지는 InnoDB의 간접 참조 구조다.
“while Postgres directly maps index records to on-disk locations,
InnoDB maintains a secondary structure” —
보조 인덱스가 디스크 위치가 아니라 기본 키 값을 가리킨다.
그래서 보조 인덱스 조회는 두 번 찾아야 하지만,
갱신은 대개 제자리에서 일어나고
옛 버전은 롤백 세그먼트로 복사되므로
실제로 바뀐 필드의 인덱스만 고치면 된다.
복제는 논리 수준이라 바이너리 로그가 WAL보다 훨씬 작고,
복제본에서 진짜 MVCC가 가능해 읽기 질의가 복제 스트림을 막지 않는다.
버전은 복제 형식이 바뀔 때만 올라가므로
복제본을 하나씩 올린 뒤 승격하는 방식으로
거의 무중단 업그레이드가 된다.
그 밖에 InnoDB가 사용자 공간에 자체 LRU 버퍼 풀을 두어
`lseek()`/`read()` 시스템 콜과 컨텍스트 전환을 피한다는 점,
그리고 연결 처리가 프로세스가 아니라 스레드 기반이라
동시 연결 1만 개도 가능하다는 점을 든다.
Uber는 “significant problems scaling Postgres past a few hundred active
connections”를 겪었고 pgbouncer가 필요했는데,
애플리케이션 버그로 유휴 연결이 과다해지면 그마저 무너졌다고 밝힌다.

## 십 년 뒤 재검토: 원문의 다섯 가지 주장은 지금 어떻게 됐나

이 글은 2016년 7월에 나왔고 Postgres 9.2를 분석했다.
지금은 2026년 9월이며 안정판은 18, 19가 베타다.
9.2는 2017년에 지원이 끝났다.
원문의 주장들이 어떤 상태인지 항목별로 확인해 둔다.
아래 인용은 모두 현행 공식 문서와 릴리스 노트의 문구다.

### 논리 복제 부재 — 해소됨, 그리고 그 이상으로 진행됨

원문의 다섯 불만 중 넷 —
복제 스트림의 크기, 버전 간 복제 불가, 물리적 손상의 전파,
복제본에서의 질의 취소 — 은
복제가 물리 수준이라는 한 가지 사실에서 나온다.
논리 복제는 2017년 10에서 코어에 들어왔다.
그 시점에 이 넷의 전제가 사라졌다.

그 뒤로도 계속 진행됐다.
16에서 스탠바이로부터의 논리 복제가 가능해졌고,
17에서는 세 가지가 한꺼번에 들어왔다.
`pg_upgrade`가 유효한 논리 슬롯과 구독 상태를 이관하게 됐고
(“This will allow upgrades to future major versions to continue
logical replication without requiring copy to resynchronize”),
물리 스탠바이를 논리 복제본으로 바꾸는 `pg_createsubscriber`가
추가됐으며,
논리 슬롯의 페일오버가 지원됐다.
마지막 항목은 원문이 겪은 것과 정확히 같은 상황 — 마스터 승격 — 에서
복제 설정이 깨지는 문제를 겨냥한다.

### 쓰기 증폭 — 구조는 그대로지만 실효 비용은 크게 줄었다

원문의 핵심 예시는
al-Khwārizmī의 출생 연도를 고치면
이름 인덱스까지 새 ctid로 갱신해야 한다는 것이었다.
그 구조 자체는 지금도 같다.
인덱스는 여전히 ctid를 가리키고,
인덱스 컬럼을 건드리는 갱신은 여전히 non-HOT이다.

바뀐 것은 그 결과로 쌓이는 비용이다.
13에서 B-tree 중복 제거(deduplication)가 기본 활성으로 들어왔고,
14에서 bottom-up index deletion이 들어왔다.
후자의 대상이 정확히 원문의 사례다.
공식 문서는 이 기제가
“indexes that are not logically modified by `UPDATE` statements”에서
작동한다고 설명하는데,
출생 연도를 고칠 때의 이름 인덱스가 바로 그 경우다.
문서는
“Changing the value of only one column covered by one index
during an `UPDATE` *always* necessitates a new set of index tuples —
one for *each and every* index on the table”라고
원문과 같은 사실을 적은 뒤, 그 결과에 대해 이렇게 쓴다.
“It's quite possible that the on-disk size of certain indexes
will never increase by even one single page/block despite
*constant* version churn from `UPDATE`s.”

14 릴리스 노트의 표현은 더 짧다.
“B-tree index updates are managed more efficiently,
reducing index bloat”이며,
해당 항목은
“particularly helpful for reducing index bloat on tables whose
indexed columns are frequently updated”라고 덧붙인다.
즉 쓰기 증폭이라는 현상은 남았지만,
그것이 인덱스 팽창과 VACUUM 부담으로 번지는 경로는 상당 부분 끊겼다.
원문이 “구조적이므로 고칠 수 없다”는 뉘앙스로 서술한 것이
실제로는 구조를 그대로 둔 채 개선됐다.

### 업그레이드 지옥 — 당시에도 과장이었고 지금은 다른 문제다

`pg_upgrade --link`는 2016년에도 있었고 공식 문서에 적혀 있었다.
HN에서 nierman이 지적한 그대로다.[^nierman]
그 뒤 객체 수가 많은 데이터베이스에서의 `pg_upgrade` 성능 문제가
여러 차례 개선됐고,
17부터는 업그레이드가 논리 복제 설정을 보존하므로
업그레이드가 복제 재구축을 강제하지 않는다.

지금 남은 업그레이드 부담은 원문이 서술한 것과 종류가 다르다.
물리 복제본을 전부 다시 만들어야 한다는 문제가 아니라,
확장(extension) 호환성과 통계 정보 이관 같은 문제다.
“9.2에 갇혀 있다”는 상태를 Postgres의 성질로 서술한
원문의 프레임은 지금 기준으로 성립하지 않는다.

### 연결 확장 — 병목의 위치가 바뀌었다

원문은 수백 개의 활성 연결에서 문제를 겪었고 프로세스 모델을 원인으로 지목했다.
프로세스 모델은 그대로다.
하지만 14에서 Andres Freund의 작업으로
“the speed of computing MVCC visibility snapshots on systems with
many CPUs and high session counts”가 개선됐고,
릴리스 노트는
“This also improves performance when there are many idle sessions”라고
덧붙인다.

이 단서가 원문의 서술과 맞물린다.
원문이 실제로 무너진 지점은 활성 연결이 아니라,
애플리케이션 버그로 늘어난 유휴 연결(특히 idle in transaction)이
pgbouncer를 넘어뜨린 경우였다.
유휴 세션이 많을 때의 비용을 줄인 개선이 바로 그 지점을 겨냥한다.
프로세스당 메모리라는 원가는 남아 있으므로
pgbouncer가 필요 없어진 것은 아니지만,
“수백 연결에서 무너진다”는 수치는 더 이상 현행 버전의 특성이 아니다.

### VACUUM — 원문이 거의 다루지 않은 축에서 가장 많이 바뀌었다

흥미롭게도 원문은
VACUUM을 쓰기 증폭의 부산물로만 언급하고 별도 불만으로 세지 않았다.
그런데 십 년간 가장 많은 개선이 쌓인 곳이 여기다.
17은 VACUUM의 메모리 관리 방식을 새로 만들어 소비를 줄였고,
`maintenance_work_mem`이 더 높아도 1GB로 조용히 제한되던 동작을
없앴으며,
튜플 제거와 동결을 더 효율적으로 바꾸면서
“WAL traffic caused by vacuum is also more compact”라고 적는다.
마지막 항목은 원문의 복제 대역폭 불만과 직접 이어진다.
원문이 문제 삼은 WAL 양의 일부가 VACUUM에서 나오고 있었기 때문이다.

### 플러그인 스토리지 — 유일하게 완결되지 않은 항목

원문의 논지 중 가장 근본적인 것 —
인덱스가 디스크 위치를 직접 가리킨다는 설계 자체 — 에 대한 답은
대체 스토리지 엔진이다.
테이블 접근 방법(table access method) API는 2019년 12에 들어왔다.
인터페이스는 열렸다.
그러나 그 위에 얹혀 코어에 들어온 대체 힙은 없다.
undo 기반의 zheap은 코어에 병합되지 않았고,
OrioleDB는 확장으로 남아 있다.
2026년에도 Postgres의 기본 스토리지는 append 기반 힙이며,
이 점에서만큼은 원문의 서술이 여전히 현행이다.

### Uber 쪽에서 일어난 일

Uber는 Schemaless를 Docstore로 발전시켰고, 2021년 2월에 그 설계를 공개했다.
Docstore는
“a general-purpose multi-model database that provides a strict
serializability consistency model on a partition level”이며,
여전히 “uses MySQL as the underlying database engine”이다.
복제 단위는 “a MySQL transaction”이고
그 위에 Raft 기반 복제 상태 기계가 올라간다.

즉 MySQL을 고른 선택은 십 년간 유지됐다.
그 점에서 원문의 판단은 자기 조직에 대해서는 옳았다.
동시에 그 선택의 진짜 내용도 드러난다.
Uber가 산 것은 MySQL이 아니라
“MySQL을 트랜잭션 단위로만 쓰는 분산 계층”이었고,
그 계층은 그 뒤로 계속 두꺼워졌다.
DB를 바꾼 것이 아니라 DB를 부품으로 강등시킨 것이며,
그 결정의 유지 비용은 원문에도 이후 글에도 정리되어 있지 않다.

## 분석

### 이 글의 모든 논점은 하나의 설계 선택에서 파생된다

다섯 개의 불만은 병렬 목록처럼 제시되지만 실제로는 계층 구조다.
뿌리는 인덱스가 디스크 위치를 직접 가리킨다는 한 가지 결정이고,
나머지는 전부 그 귀결이다.
행이 옮겨 다니므로 모든 인덱스를 갱신해야 하고(쓰기 증폭),
그 쓰기가 WAL에 실리므로 복제가 무거워지고,
복제가 물리 수준이므로 버전이 다르면 복제할 수 없고(업그레이드 지옥),
복제본이 WAL을 그대로 재생해야 하므로
읽기 트랜잭션과 충돌한다(복제본 MVCC).

이 구성은 글의 설득력이 어디서 오는지도 설명한다.
개별 불만을 나열했다면 “그건 튜닝하면 된다”는 반박에
하나씩 흩어졌을 텐데,
하나의 뿌리에서 뻗어 나온 가지로 배치하면 반박도 뿌리를 건드려야 한다.
그래서 이 글은 벤치마크 없이도 십 년을 살아남았다.
구조 논증은 수치 논증보다 반증 비용이 크다.

### 발표 시점이 논증의 성격을 결정한다

2016년 7월에 쓰인 글이 분석하는 것은 2012년에 나온 9.2다.
당시 최신은 2016년 1월에 나온 9.5였고,
저자도 자신들의 레거시가 9.2에 남아 있다고 인정한다.
즉 이 글은 최신 Postgres와 최신 InnoDB를 비교한 것이 아니라,
자기 조직이 올리지 못한 버전과
새로 도입할 수 있었던 엔진을 비교한 것이다.

그 비대칭을 덮는 장치가
“새 릴리스에서도 내부 구조가 크게 바뀌지 않았다”는 한 문장이다.
이 문장이 없었다면 글의 유효기간은 몇 년이었을 것이다.
이 문장이 있어서 독자는 버전 차이를 무시해도 된다고 허락받는다.
HN에서 quotemstr는 다른 층위의 정밀성 문제를 지적했다.
시스템 콜은 컨텍스트 전환이 아니며,
권한 수준 변경일 뿐 스케줄러 호출과 레지스터 저장·복원과
캐시 무효화를 수반하지 않는다는 것이다.[^quotemstr]
버퍼 풀 논지의 근거로 제시된 비용이 실제로는 그만큼 크지 않다는 뜻이다.

### 제목이 가리키는 것과 본문이 하는 일이 다르다

제목은 Postgres와 MySQL의 선택 문제로 읽히지만,
결론에서 Uber가 도착한 곳은 Schemaless다.
MySQL은 그 아래에 깔린 저장소이며,
Uber는 관계형 모델을 대체로 쓰지 않는다.
HN의 forgotpwtomain은
그래서 이 글이 Postgres 대 MySQL 선택에
일반적으로 적용될 만한 고려를 보여 주지 못한다고 짚었다.
Uber는 MySQL을 사실상 키-값 저장소로 쓰고 있다는 것이다.[^forgotpwtomain]
mace의 요약은 더 직설적이다.
“대규모 저장에 관계형 DB를 쓰는 방식을 다시 생각했고
지금은 MySQL을 멍청한 키-값 저장소로 쓴다”가
공정한 정리라는 것이다.[^mace]

여기서 아이러니가 하나 생긴다.
Illniyar는 Schemaless 소개 글의 첫 문단을 끌어와 대조했다.
데이터의 기본 단위인 셀(cell)은 불변이며 한 번 쓰면 덮어쓸 수 없고,
갱신은 같은 행 키와 컬럼 이름에
더 높은 ref 키를 가진 새 버전을 쓰는 것으로 이루어진다.[^Illniyar]
불변 행이 문제라서 떠났다고 말한 팀이,
그 위에 불변 셀을 쌓은 계층을 만든 셈이다.

### 이 글이 실제로 비교하는 것은 두 DB가 아니라 두 운영 모델이다

philpennock은 Lobste.rs에서 이 지점을 정확히 겨눴다.
Uber는 코드에서 MySQL을 직접 쓰지 않고
추상 계층을 통해 쓰기 때문에 MySQL의 문제 대부분을 피하고 있으며,
연결 풀링 불만이나 오래 열린 복제본 질의 불만도
Postgres에 같은 추상을 뒀다면 똑같이 해결됐을 것이라는 지적이다.[^philpennock]
jlarocco도 같은 방향에서 물었다.
추상 계층 안에 얼마나 많은 MySQL 문제가 숨겨져 있는지 궁금하며,
Postgres 문제도 같은 방식으로 숨기면서
Postgres의 이점을 유지할 수 있지 않았겠느냐는 것이다.[^jlarocco]

이 비판이 중요한 이유는 글의 인과를 뒤집기 때문이다.
글은 “Postgres의 한계 때문에 Schemaless를 만들었다”는 순서로
읽히지만,
실제 순서는
“샤딩 계층을 만들기로 했고 그 아래에 무엇을 둘지 골랐다”였을 수 있다.
샤딩 계층을 전제하면 관계형 기능 대부분이 쓰이지 않으므로,
남는 비교 축은 쓰기 비용과 복제 비용뿐이다.
그 축에서 InnoDB가 낫다는 것이 글의 결론이고,
그것은 처음부터 좁혀진 비교의 결과다.

## 비평

### 엔지니어링 글인데 수치가 거의 없다

이 글의 핵심 주장은 쓰기 증폭이 크다는 것인데, 얼마나 큰지는 어디에도 없다.
초당 몇 건의 갱신에서 WAL이 몇 바이트 늘었는지,
데이터센터 간 복제 대역폭이 실제로 얼마였는지,
MySQL로 옮긴 뒤 무엇이 몇 퍼센트 나아졌는지가 제시되지 않는다.
보조 인덱스가 많은 테이블이 문제라고 하면서
그 테이블에 인덱스가 몇 개였는지도 밝히지 않는다.

수치의 부재는 사소한 흠이 아니다.
이 글이 반박하기 어려운 이유가 바로 거기에 있기 때문이다.
구조 논증은 “그런 경우 비효율이 생긴다”까지만 말하고
“우리 워크로드에서 그 비효율이 지배적이었다”는 단계를 건너뛴다.
독자는 두 번째 단계가 참이라고 가정한 채
첫 번째 단계의 논리적 타당성만 검토하게 되고,
그 검토에서는 글이 항상 이긴다.

대조가 되는 사례가 있다.
`database/mvcc-bad.md`가 다루는 boringsql 글은
100만 행 테이블에서 인덱스 없는 쪽이 행당 약 3.0개,
인덱스가 많은 쪽이 7.1개의 WAL 레코드를 낸다는 식으로 측정값을 낸다.
같은 현상을 다루면서 한쪽은 재현 가능한 수치를 내고 한쪽은 내지 않는데,
널리 인용되는 쪽은 수치가 없는 쪽이다.
그 사실 자체가 이 장르의 독자가 무엇을 검증하지 않는지를 보여 준다.

### 버그를 구조의 증거로 쓴다

데이터 손상 절은 Postgres 9.2의 특정 버그를 서술한 뒤,
물리 복제이기 때문에 인덱스 손상이 퍼질 수 있어
걱정된다는 일반론으로 넘어간다.
그런데 그 버그는 특정 릴리스의 결함이고 이미 고쳐졌다.
2021년 HN 재게시에서 lumost가 짚은 것도 이 대목이다.
나열된 불만 대부분은
사실상 어떤 트랜잭션 RDBMS에도 해당할 수 있는 것들이라는 지적이다.[^lumost]

버그와 설계를 구분하지 않으면 어떤 시스템도 방어할 수 없다.
MySQL에도 복제 관련 버그의 역사가 길고,
특히 문장 기반 복제(statement-based replication)는
비결정적 함수에서 마스터와 복제본이 갈라지는 문제로 오래 시달렸다.
jedberg는 HN에서
Postgres도 서드파티 도구로 문장 기반 복제를 지원하며
10년 전 reddit에서 써 봤는데 문제가 많았다고,
그것을 MySQL의 장점으로 부르지는 않겠다고 적었다.[^jedberg]

논리 복제가 물리 복제보다 손상 전파에 강하다는 것은 맞지만,
대신 논리 복제는
마스터와 복제본이 조용히 갈라질 수 있다는 다른 종류의 위험을 진다.
물리 복제의 실패는 시끄럽고 논리 복제의 실패는 조용한데,
글은 시끄러운 실패만 비용으로 계산한다.

### 반대편 트레이드오프를 세지 않는다

InnoDB의 간접 참조가 쓰기에 유리하다는 서술은 정확하다.
문제는 그 대가가 한 문장으로 처리된다는 점이다.
solidsnack이 Lobste.rs에서 정리한 목록이 그 대가다.
질의가 (적어도 잠재적으로) 느려지고,
기본 키가 반드시 있어야 하고, 복합 기본 키일 때는 어떻게 되며,
기본 키 갱신의 영향은 무엇이냐는 것이다.[^solidsnack]
반대로 vanviegen은
글이 언급하지 않은 InnoDB의 이점 하나를 덧붙였다.
행 데이터가 기본 키 인덱스 안에 있으므로
기본 키 읽기는 추가 페이지 참조가 없어 더 빠르고,
특히 기본 키 범위 질의에서 유리하다는 것이다.[^vanviegen]
양쪽 다 글에 없다.
트레이드오프를 한 방향으로만 세었다는 뜻이다.

연결 처리 논지도 마찬가지다.
프로세스 기반이 스레드 기반보다 비싸다는 것은 사실이지만,
solidsnack은 Postgres가 그 방식을 택한 두 가지 실질적 이유를 든다.
크래시를 일으키는 확장이 있어도
해당 연결 프로세스만 죽고 마스터 프로세스는 무사하며,
OS가 연결을 여러 코어에 알아서 배치해 준다는 것이다.[^solidsnack-proc]
jamesjporter는 pgbouncer를 문제로 든 것 자체가 조금 불공정하다고 봤다.
pgbouncer는 훌륭한 소프트웨어이고
자신은 수천 클라이언트를 붙여 봤지만 문제가 없었다는 것이다.[^jamesjporter]

가장 날카로운 요약은 scotty79의 것이다.
글은
“우리에게 맞는 방식으로 X를 썼고,
X의 어떤 기술적 성질 때문에 문제가 생겼고,
그래서 Z로 옮겼다”인데,
상위 댓글들은
“X를 잘못 썼다”와
“문제를 일으킨 그 기술적 성질들은 사실 X의 우월한 기능이다”라고
답한다는 것이다.[^scotty79]
이 요약은 양쪽 모두를 겨냥한다.
글은 자기 사용 방식을 상수로 두었고,
반박자들은 자기 선호를 상수로 두었다.

### 업그레이드가 불가능하다는 주장은 그 시점에도 완전하지 않았다

업그레이드 절은
마스터를 내리고 `pg_upgrade`를 돌리고
복제본을 전부 재구축해야 한다고 서술한다.
nierman은 HN에서 `pg_upgrade`의 `--link` 옵션을 지적했다.
새 클러스터가 옛 클러스터의 파일을
하드 링크로 참조하므로 대형 DB에서도 매우 빠를 수 있고,
스탠바이도 `rsync --hard-links`로 전체 전송 없이 올릴 수 있으며,
이는 당시 공식 문서에 이미 적혀 있었다는 것이다.[^nierman]

이 반박이 결정적인 이유는
업그레이드 불가가 다른 모든 문제의 전제이기 때문이다.
9.2에 갇혀 있지 않았다면 그사이의 개선을 받을 수 있었고,
물리 복제의 여러 제약도 후속 버전에서 완화됐다.
글은 갇힌 상태를 Postgres의 성질로 서술하지만,
갇힌 상태의 일부는 사용 가능한 도구를 쓰지 않은 결과이기도 하다.

viraptor는 여기서 한 발 더 나갔다.
9.2에서 상위 버전으로 올리는 일이 너무 큰 작업이라면서
MySQL로 옮기는 일은 하겠다는 것이 이상하다는 지적이다.
MySQL 이관은 훨씬 큰 공수가 들고,
실시간에 가깝게 하려면
기존 데이터를 복사하면서 신규 쓰기를 양쪽으로 흘려야 하는데
WAL로는 그것을 할 수 없다는 것이다.[^viraptor]
같은 조직이 더 큰 마이그레이션은 감당하고
더 작은 업그레이드는 감당할 수 없다고 말할 때,
설명되지 않은 것은 기술이 아니라 의사결정이다.
denishpatel은
Uber가 2013년에 거의 같은 이유를 들어
MySQL에서 Postgres로 옮겼다는 발표 자료를 들어 이 점을 꼬집었다.[^denishpatel]

### 지금 이 글을 근거로 인용하는 것은 거의 언제나 오용이다

이 글은 여전히 “Postgres는 쓰기에 약하다”의 출처로 인용된다.
그런데 앞의 재검토를 항목별로 대응시켜 보면,
인용 가능한 부분이 거의 남지 않는다.
복제 관련 네 불만은 논리 복제가 코어에 들어오면서 전제가 사라졌고,
업그레이드 불만은 당시에도 `--link`로 반박됐으며,
연결 확장 수치는 14 이후의 스냅숏 개선을 반영하지 않고,
쓰기 증폭은 현상은 남았지만
그 비용의 주된 경로가 13·14의 인덱스 개선으로 끊겼다.
남는 것은 기본 힙이 여전히 append 기반이라는 사실 하나뿐이며,
그것은 원문이 든 다섯 불만 중 어느 것도 그대로 뒷받침하지 않는다.

문제는 이 글이 그런 오용을 유도하는 방식으로 쓰였다는 점이다.
“the internal architecture that we discuss in this article has not
changed significantly in newer Postgres releases”라는 한 문장이
독자에게 버전 확인을 면제해 준다.
2016년에 그 문장은 9.2와 9.5 사이를 가리켰고 대체로 맞았다.
2026년에 같은 문장을 읽는 독자는
9.2와 18 사이를 면제받는다고 이해하며, 그것은 전혀 맞지 않다.
문장에 유효 범위를 적지 않은 것이 십 년짜리 오독을 만들었다.

2021년 재게시 스레드에서 frankietaylr가
“9.2 이후 이 글이 말한 비효율에 관해
Postgres 구조가 바뀌었느냐”고 물어야 했다는 사실이
이 상태를 그대로 보여 준다.[^frankietaylr]
그 질문에 대한 답은 같은 스레드에 있었다.
Postgres 커미터 petergeoghegan이
자신이 커밋한 bottom-up index deletion이
바로 이 글의 쓰기 증폭을 완화하려고 설계됐다고 답했다.[^petergeoghegan]
질문과 답이 같은 스레드에 나란히 있어야 했다는 것 자체가,
원문이 자기 유효기간을 표시하지 않은 대가다.

## 인사이트

### 아키텍처 비판은 그 대상이 고쳐질수록 더 널리 인용된다

상식적으로는 반대여야 한다.
문제가 고쳐지면 그 문제를 지적한 글의 인용은 줄어야 한다.
실제로는 그렇지 않다.
고쳐지는 과정에서 그 문제가 유명해지고,
유명해진 문제는 해결된 뒤에도 이름으로 남는다.
“Postgres 쓰기 증폭”은 2016년보다 2026년에 더 널리 알려진 표현이며,
그 인지도의 상당 부분을 이 글 하나가 만들었다.

이 비대칭이 생기는 이유는 정보의 전파 속도가 층마다 다르기 때문이다.
문제 제기는 블로그와 뉴스 애그리게이터를 타고 며칠 만에 퍼지고,
해결은 릴리스 노트와 커밋 로그에 실려 그것을 읽는 소수에게만 닿는다.
14 릴리스 노트의
“B-tree index updates are managed more efficiently,
reducing index bloat”라는 한 줄이 도달한 독자 수와,
Uber 글이 도달한 독자 수는 자릿수가 다르다.
릴리스 노트는 무엇이 고쳐졌는지 적을 뿐 무엇에 대한 반박인지 적지 않으므로,
두 텍스트는 서로 연결되지 않은 채 각자 유통된다.

여기서 나오는 이차 효과가 기술 선택의 지연이다.
어떤 시스템에 대한 부정적 평판은 그 원인이 제거된 뒤에도 몇 년을 더 산다.
반증을 유통시킬 채널이 문제 제기를 유통시킨 채널보다 약하기 때문이다.
같은 구조가 언어와 프레임워크에서도 반복된다.
특정 버전의 성능 문제나 보안 사고로 붙은 평판이
몇 개 메이저 버전이 지나도록 검색 결과 상단에 남는다.

실무에서 쓸 수 있는 대응은 두 가지다.
읽는 쪽에서는 비판 글을 만났을 때
그 글의 날짜와 대상 버전을 먼저 확인하고,
해당 프로젝트의 그 이후 릴리스 노트를 그 키워드로 검색하는 습관이다.
쓰는 쪽에서는
개선을 발표할 때 무엇이 좋아졌는지가 아니라
어떤 알려진 비판에 대한 답인지를 함께 적는 것이다.
후자는 릴리스 노트의 관행이 아니지만,
평판을 되돌리는 유일하게 효율적인 방법이기도 하다.

### 구조 논증은 벤치마크보다 오래 살고, 그래서 더 위험하다

벤치마크에는 날짜가 붙는다.
“9.2에서 초당 3만 건” 같은 문장은
읽는 사람이 스스로 유효기간을 계산한다.
구조 논증에는 날짜가 붙지 않는다.
“인덱스가 디스크 위치를 직접 가리키므로
모든 인덱스를 갱신해야 한다”는 문장은
십 년 뒤에 읽어도 시제가 없다.
그래서 아키텍처를 논한 글은 측정을 제시한 글보다 훨씬 오래 인용되고,
그 인용의 상당수는 이미 사실이 아닌 시점에 일어난다.

이 글의 경우 반증은 실제로 존재한다.
Postgres 커미터 petergeoghegan은 2021년 HN 스레드에서
자신이 커밋한 “bottom-up index deletion”이
바로 이 글이 말하는 쓰기 증폭을 완화하려고 설계된 기제이며
여러 워크로드에서 매우 효과적임이 테스트로 확인됐다고 밝혔다.[^petergeoghegan]
그 기능은 Postgres 14에 들어갔고,
그사이 논리 복제는 10에서 내장으로 들어왔으며
지금은 18이 안정판이고 19가 베타다.
그럼에도 이 글은 여전히 인용된다.
같은 스레드에서 frankietaylr가
“9.2 이후 이 글이 말한 비효율에 관해
Postgres 구조가 바뀌었느냐”고 물어야 했다는 사실이
그 상태를 보여 준다.[^frankietaylr]

여기서 나오는 실무적 기준은 단순하다.
아키텍처 비교 글을 읽을 때 먼저 확인해야 할 것은
논리의 타당성이 아니라
그 논리가 참조하는 버전과 지금 버전 사이에 무엇이 들어왔는지다.
그리고 글을 쓰는 쪽에서는,
측정값을 넣는 것이 글의 수명을 줄이는 것처럼 보여도
실은 독자가 오용하는 것을 막는 장치다.

### 기업 엔지니어링 블로그는 기술 문서인 동시에 채용 문서다

2021년 재게시 스레드에서 Uber에서 1년 일했던 junon이 맥락을 하나 붙였다.
2016년은 Uber가 급격히 성장하던 해였고,
입사 6개월이면 사번이 중앙값에 온다는 말이 사내에 돌 정도였으며,
회사는 가능한 모든 사람을 채용하고 빼 오려 하고 있었다는 것이다.
그래서 이런 글은 실제 내부 기술에 비해 매우 반짝이게 쓰였다고 적는다.[^junon]

이 관찰은 글의 형식을 다시 보게 만든다.
왜 수치가 없고 구조 서술만 있는가,
왜 대안 검토(다른 버전으로의 업그레이드, 다른 샤딩 계층, 다른 DB)가
없는가,
왜 결론이 “우리는 MySQL에 대체로 만족한다”로 끝나는가.
내부 의사결정 문서라면 이 셋 다 있어야 한다.
채용과 브랜딩을 겸하는 공개 글이라면 셋 다 없는 편이 낫다.

같은 구조는 다른 회사의 유명한 마이그레이션 글에도 반복된다.
“우리는 X에서 Y로 옮겼고 이만큼 나아졌다”는 형식은
조직 안에서는 이미 끝난 결정을 사후 정당화하는 글이고,
조직 밖에서는 아직 결정하지 않은 사람에게 근거로 읽힌다.
두 독자의 필요가 다른데 글은 하나뿐이며,
대체로 안쪽 독자의 필요가 이긴다.
따라서 이런 글을 자기 결정의 근거로 쓸 때 필요한 보정은
“이 회사와 우리가 얼마나 비슷한가”가 아니라
“이 글이 답하지 않기로 한 질문이 무엇인가”다.

### 저장 엔진 선택은 그 위에 무엇을 얹느냐가 정해진 뒤에는 대체로 부차적이다

이 글에서 가장 덜 논의된 문장은 결론에 있다.
Uber는 Schemaless를 만들었고
특수한 경우에는 Cassandra 같은 NoSQL을 쓴다는 대목이다.
샤딩 계층을 만들기로 한 순간,
아래층 DB에 요구되는 것은
트랜잭션 격리도 아니고 조인도 아니고 제약 조건도 아니다.
빠른 쓰기와 싼 복제와 쉬운 업그레이드뿐이다.
그 좁은 요구 집합에서 두 DB를 비교하면
결과가 달라지는 것이 당연하다.

fusiongyro의 정리가 이 점을 짚는다.
글은 “Postgres는 분산 데이터베이스가 아니다”로 요약될 수 있으며,
MySQL도 아니지만 복제 도구가 더 친절할 뿐이라는 것이다.[^fusiongyro]
drob은 Heap에서 같은 종류의 한계를 겪었지만
다른 답을 골랐다고 밝혔다.
데이터 품질을 희생하는 대신 분산 계층을 만들었고,
읽기는 CitusDB, 쓰기와 분산 운영은 자체 시스템을 쓴다는 것이다.[^drob]
같은 문제에 같은 형태의 해법(분산 계층)을 쓰면서
아래층은 Postgres로 남긴 사례이며,
이것이 저장 엔진 교체가 필수가 아니었음을 보여 준다.

여기서 나오는 이차 효과는 조직 역량 쪽이다.
샤딩 계층을 자체 구축하면
아래층 DB의 특성이 팀에서 점점 덜 중요해지고,
대신 그 계층을 유지할 인력이 계속 필요해진다.
DB 선택은 한 번의 결정이지만 자체 계층은 영구적인 인건비이며,
이 글은 전자만 논한다.
십 년 뒤 관점에서 보면
Uber가 실제로 산 것은 MySQL의 쓰기 성능이 아니라
자기 데이터 계층에 대한 통제권이었고,
그 통제권의 가격은 이 글 어디에도 적혀 있지 않다.

### 논쟁의 승패보다 논쟁이 남긴 개선이 결과였다

이 글에 대한 반응은 반박문의 형태로 이어졌다.
2ndQuadrant의 Simon Riggs는
제기된 기술적 논점 대부분에 대한 전체 답변을 썼고
HN 스레드에 직접 링크를 남겼다.[^simon2Q]
Markus Winand는 “On Uber's Choice of Databases”를,
Oren Eini는 “Re: Why Uber Engineering Switched from Postgres to
MySQL”을 썼고,
두 글 다 Lobste.rs에 별도 스레드로 올라갔다.
lithp가 짚었듯
pgsql-hackers 메일링 리스트에도 꽤 정직한 자기 평가가 올라왔으며,
steveno는
그 스레드가 단점을 인정하는 데 그치지 않고
어떻게 고칠지를 파고들기 시작했다는 점을 높이 샀다.[^lithp][^steveno]

여기서 보이는 구조가 오픈소스 프로젝트에 대한 공개 비판의 전형적 경로다.
비판이 부정확하더라도 그 비판이 겨눈 지점에 개발 자원이 몰린다.
반박을 쓰려면 현황을 정리해야 하고,
현황을 정리하면 실제로 부족한 곳이 드러나기 때문이다.
Postgres에서 논리 복제와 인덱스 쓰기 최적화가
이후 몇 년간 눈에 띄게 진전한 것을
이 글 하나의 인과로 돌릴 수는 없지만,
그 방향에 대한 외부 압력이 이 시기에 최고조였던 것은 사실이다.

그래서 이런 논쟁의 실질적 결과를 평가할 때
“누가 옳았나”는 대체로 잘못된 질문이다.
Uber의 진단 중 일부는 자기 조직의 문제였고
일부는 진짜 구조적 비용이었으며,
십 년이 지난 지금 남은 것은 그 구분이 아니라
그 사이 무엇이 고쳐졌는지다.
그리고 고쳐진 것들의 목록을 최신 상태로 들고 있지 않은 독자에게는,
이 글이 여전히 2016년의 결론을 2026년의 조언처럼 건넨다.

---

[^quotemstr]: <https://news.ycombinator.com/item?id=12170826>

[^forgotpwtomain]: <https://news.ycombinator.com/item?id=12167292>

[^mace]: <https://news.ycombinator.com/item?id=12194434>

[^Illniyar]: <https://news.ycombinator.com/item?id=12167321>

[^jedberg]: <https://news.ycombinator.com/item?id=12167700>

[^scotty79]: <https://news.ycombinator.com/item?id=12168665>

[^nierman]: <https://news.ycombinator.com/item?id=12169862>

[^viraptor]: <https://news.ycombinator.com/item?id=12169443>

[^denishpatel]: <https://news.ycombinator.com/item?id=12173397>

[^simon2Q]: <https://news.ycombinator.com/item?id=12212408>

[^vanviegen]: <https://news.ycombinator.com/item?id=12169041>

[^fusiongyro]: <https://news.ycombinator.com/item?id=12167302>

[^drob]: <https://news.ycombinator.com/item?id=12168243>

[^lumost]: <https://news.ycombinator.com/item?id=26286042>

[^petergeoghegan]: <https://news.ycombinator.com/item?id=26285452>

[^junon]: <https://news.ycombinator.com/item?id=26285755>

[^frankietaylr]: <https://news.ycombinator.com/item?id=26284116>

[^philpennock]: <https://lobste.rs/s/b4hbxr/why_uber_engineering_switched_from#c_rof0il>

[^jlarocco]: <https://lobste.rs/s/b4hbxr/why_uber_engineering_switched_from#c_grbztl>

[^solidsnack]: <https://lobste.rs/s/b4hbxr/why_uber_engineering_switched_from#c_lsxghz>

[^solidsnack-proc]: <https://lobste.rs/s/b4hbxr/why_uber_engineering_switched_from#c_gubldz>

[^jamesjporter]: <https://lobste.rs/s/b4hbxr/why_uber_engineering_switched_from#c_n9b0uz>

[^lithp]: <https://lobste.rs/s/b4hbxr/why_uber_engineering_switched_from#c_s9ikof>

[^steveno]: <https://lobste.rs/s/b4hbxr/why_uber_engineering_switched_from#c_xrnzso>
