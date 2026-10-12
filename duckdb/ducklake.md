# DuckLake: 레이크하우스 메타데이터를 파일 대신 SQL 데이터베이스에 두는 형식

<https://ducklake.select/>

<https://github.com/duckdb/ducklake>

HN 토론: <https://news.ycombinator.com/item?id=44106934> (276점, 107개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=49996149> (233점, 35개 댓글)

GN 토론: <https://news.hada.io/topic?id=21168>

GN 토론: <https://news.hada.io/topic?id=35046>

## 소개

DuckLake는 데이터를 Parquet 파일로 두고,
어떤 파일이 어느 테이블의 어느 시점에 속하는지 같은 메타데이터 전부를
SQL 데이터베이스에 두는 레이크하우스 형식이다.
이 메타데이터 데이터베이스를 DuckLake는 카탈로그 데이터베이스라고 부른다.
공식 FAQ는 DuckLake라는 이름이 세 가지를 가리킨다고 정리한다.
카탈로그 데이터베이스와 Parquet 저장소로 데이터를 담는 형식 자체,
그 형식으로 저장된 데이터셋 하나,
그리고 그 형식을 읽고 쓰는 DuckDB 확장 `ducklake`다.
FAQ는 비교 대상으로 Unity Catalog를 붙인 Delta Lake와
Lakekeeper나 Polaris를 붙인 Iceberg를 든다.

GitHub 저장소 `duckdb/ducklake`는 이 가운데 세 번째, DuckDB 확장의 C++ 구현이다.
저장소 설명은 통합 데이터 레이크이자 카탈로그 형식이고,
명세와 확장 모두 MIT 라이선스다.
저장소는 2025년 3월에 만들어졌고 이 글을 쓰는 시점에 별 3,277개를 받았다.
명세 문서와 웹사이트 소스는 별도 저장소 `duckdb/ducklake-web`에 있다.
프로젝트는 비영리 DuckDB Foundation이 관리한다.

버전 이력은 다음과 같다.
2025년 5월 27일 v0.1이 Mark Raasveldt와 Hannes Mühleisen의 매니페스토와
함께 나왔고, 0.2, 0.3, 0.4를 거쳐 2026년 4월 13일 v1.0이 나왔다.
v1.0은 하위 호환을 보장하는 프로덕션용 릴리스이며 DuckDB v1.5.2에 들어 있다.
릴리스 캘린더는 다음 릴리스로
명세 1.1과 확장 2.0을 2026년 10월 21일에 잡아 두었는데,
날짜는 잠정이라고 밝힌다.
FAQ에는 같은 1.1이 2026년 9월 예정으로 남아 있어
일정이 한 번 밀린 것으로 보인다.

## 설계 배경

### 카탈로그가 이미 데이터베이스를 쓰고 있었다

매니페스토의 논지는
Iceberg와 Delta Lake가 데이터베이스 없이 동작하도록 설계됐지만
결국 데이터베이스를 들여왔다는 것이다.
두 형식은 테이블 상태를 객체 저장소의 파일로만 표현하려 했고,
Iceberg는 스키마, 스냅숏, 테이블에 속한 Parquet 파일 목록을
JSON과 Avro 파일의 미로로 정의한다.
그런데 객체 저장소에서는 최신 버전을 가리키는 포인터를 원자적으로 바꾸기 어렵고,
두 형식은 테이블 하나만 알기 때문에
여러 테이블을 다루려면 카탈로그 서비스가 필요했다.
그 카탈로그는 다시 데이터베이스와 이야기하며,
테이블마다 현재 버전 번호 한 줄만 담은 테이블을 관리한다.
매니페스토는 이것을 역사상 가장 슬픈 테이블이라고 부른다.

데이터베이스가 이미 스택에 들어왔는데도
나머지 설계는 파일만 쓴다는 제약을 그대로 지고 있다는 것이 비판의 핵심이다.
Iceberg의 루트 파일은 스키마를 포함한 모든 스냅숏을 담고,
변경마다 전체 이력을 담은 새 파일이 써진다.
작은 파일을 피하려고 매니페스트를 두 층으로 묶는 식의 타협도 여기서 나온다.
DuckLake는 이 지점에서 방향을 바꿔 메타데이터 전부를 SQL 테이블로 옮긴다.
매니페스토는 Google BigQuery가 Spanner를,
Snowflake가 FoundationDB를 메타데이터 저장소로 쓰는 것과 같은 설계이며,
다만 맨 아래 데이터를 개방형 형식으로 둔다는 점만 다르다고 설명한다.

### 형식이 곧 SQL 테이블과 트랜잭션이다

DuckLake 형식은 관계형 테이블의 집합과
그 위에서 도는 순수 SQL 트랜잭션으로 정의된다.
v1.0 명세는 메타데이터 저장과 데이터 인라이닝용으로 테이블 28개를 쓴다.
스냅숏(`ducklake_snapshot`, `ducklake_snapshot_changes`),
스키마(`ducklake_schema`, `ducklake_table`, `ducklake_view`, `ducklake_column`),
데이터 파일(`ducklake_data_file`, `ducklake_delete_file`), 통계, 파티션,
정렬 정보 테이블로 나뉜다.
카탈로그 데이터베이스의 조건은
SQL-92 표준의 트랜잭션과 기본 키 제약을 지원하는 것뿐이다.
명세는 처음 읽는 사람에게 테이블 목록보다 쿼리 페이지부터 보라고 권한다.
형식을 이해하는 가장 빠른 길이 어떤 SQL이 실행되는지 보는 것이라는 뜻이다.

## 동작 방식

### 쓰기 한 번은 카탈로그 트랜잭션 한 번이다

매니페스토는 빈 테이블에 `INSERT INTO demo VALUES (42), (43);`을
실행할 때 카탈로그에서 일어나는 일을 그대로 보여 준다.
Parquet 파일은 이보다 먼저 저장소에 써지고,
카탈로그에는 다음 트랜잭션 하나가 실행된다.

```sql
BEGIN TRANSACTION;
    -- 일부 메타데이터 읽기는 생략
    INSERT INTO ducklake_data_file
    VALUES (0, 1, 2, NULL, NULL, 'data_files/ducklake-8196...13a.parquet', 'parquet', 2, 279, 164, 0, NULL, NULL);
    INSERT INTO ducklake_table_stats
    VALUES (1, 2, 2, 279);
    INSERT INTO ducklake_table_column_stats
    VALUES (1, 1, false, NULL, '42', '43');
    INSERT INTO ducklake_file_column_statistics
    VALUES (0, 1, 1, NULL, 2, 0, 56, '42', '43', NULL)
    INSERT INTO ducklake_snapshot
    VALUES (2, now(), 1, 2, 1);
    INSERT INTO ducklake_snapshot_changes
    VALUES (2, 'inserted_into_table:1');
COMMIT;
```

새 파일 경로 등록, 테이블 통계와 열 통계 갱신, 파일별 최소·최댓값 기록,
새 스냅숏 생성, 변경 기록이 한 트랜잭션에 묶인다.
값을 몇 개 넣든 이 순서의 비용은 같다.
여러 테이블에 걸친 변경과 `CREATE TABLE`,
`ALTER TABLE` 같은 DDL도 같은 방식으로 한 트랜잭션에 들어가며,
커밋된 `BEGIN`-`COMMIT` 블록 하나가 스냅숏 하나가 된다.
스냅숏은 카탈로그에 몇 줄 더하는 것이라 미리 정리할 필요가 없고,
매니페스토는 수백만 개의 스냅숏도 다룰 수 있다고 주장한다.

### 읽기는 카탈로그 쿼리 한 번으로 파일 목록을 얻는다

테이블을 읽을 때는 카탈로그에 쿼리 하나를 보내고, 카탈로그가 스키마, 파티션,
통계 기반 가지치기를 해서 읽을 Parquet 파일 목록을 돌려준다.
Iceberg처럼 메타데이터 파일을 여러 번 차례로 HTTP로 가져와
상태를 재구성하는 과정이 없다.
매니페스토는 이 덕분에 S3 요청 제한, 실패한 요청, 재시도,
아직 일관되지 않은 저장소 뷰 같은 문제도 사라진다고 말한다.
Dowwie는 이 차이를 이렇게 요약했다.
Iceberg는 스키마와 파일 목록을
객체 저장소의 작은 메타데이터 파일 여러 개로 두지만,
DuckLake는 그것을 트랜잭션 SQL 데이터베이스에 넣고
쿼리 한 번으로 꺼낸다.[^Dowwie]

### 충돌은 스냅숏 번호의 기본 키 위반으로 감지한다

스냅숏 번호는 순서대로 하나씩 늘어나고
`ducklake_snapshot.snapshot_id`에는 기본 키가 걸려 있다.
두 연결이 동시에 쓰면 같은 스냅숏 번호를 쓰려다
한쪽이 기본 키 위반으로 커밋에 실패한다.
이때 확장은 `ducklake_snapshot_changes`를 읽어
그 사이 다른 스냅숏이 무엇을 바꿨는지 확인한다.
논리적 충돌이 없으면
데이터 파일을 다시 쓰지 않고 카탈로그 트랜잭션만 재시도하고,
있으면 트랜잭션을 중단한다.
문서가 꼽는 논리적 충돌은 같은 이름의 스키마나 테이블을 둘 다 만드는 경우,
다른 스냅숏이 삭제하거나 변경한 테이블에 쓰는 경우,
다른 스냅숏이 삭제나 압축을 한 테이블에서 지우는 경우 등이다.
같은 테이블에 두 쪽이 모두 추가만 하는 경우는 충돌이 아니다.

이 구조는 파일 기반 레이크에서 직접 동시 쓰기를 다뤄 본 사람에게
익숙한 고통을 겨냥한다.
wodenokoto는 deltalake-rs와 DuckDB로 Blob 저장소에 직접 꾸린 레이크에서
주기적으로 도는 수집 함수와 백필 작업이 겹칠 때마다
동시 쓰기 문제를 겪는다고 적었다.[^wodenokoto-2]

### 작은 변경은 카탈로그에 인라인으로 담는다

데이터 인라이닝은 정해진 행 수보다 작은 삽입, 삭제, 수정을
Parquet 파일 대신 카탈로그 데이터베이스의 테이블에 기록하는 기능이다.
v1.0부터 기본으로 켜져 있고 기본 문턱값은 10행이다.
인라인 데이터 테이블은
원래 열에 `row_id`, `begin_snapshot`, `end_snapshot`을 더해
시점 조회를 그대로 지원하고,
이미 Parquet에 있는 행을 지우면 파일을 다시 쓰지 않고
인라인 삭제 테이블에 파일 번호와 행 번호를 적는다.
쌓인 인라인 데이터는 `ducklake_flush_inlined_data`나 `CHECKPOINT`로
Parquet 파일 하나로 내보낸다.

인라이닝 소개 글은 PostgreSQL 16.10(Amazon RDS)을 카탈로그로,
같은 리전의 S3를 저장소로 두고 초당 100행을 10행씩 나눠 넣는 스트리밍 작업을
50분 분량(30만 행, 3만 배치) 돌린 결과를 실었다.

| 단계       | 인라이닝 없음 | 인라이닝 사용 | 차이   |
| ---------- | ------------- | ------------- | ------ |
| 삽입       | 1,964 s       | 375.0 s       | 5.2×   |
| 집계       | 1,574 s       | 1.7 s         | 925.9× |
| 체크포인트 | 30 s          | 2.1 s         | 14.5×  |

인라이닝이 없으면 집계 쿼리가 S3의 Parquet 파일 3만 개를 모두 열어야 하기 때문에
차이가 이렇게 벌어진다.
같은 글은 pyiceberg와 Apache Polaris 조합의 Iceberg가 50분 작업을 감당하지 못해
100초 분량(1만 행, 1,000 배치)으로 줄여 비교했고,
삽입 105배, 집계 923배, 체크포인트 189배 차이가 났다고 적었다.
글은 클라이언트 쪽 버퍼링이나 더 큰 배치로
작은 파일 문제를 줄일 수 있다는 점을 인정하면서,
그러면 ACID 보장과 다중 사용자 지원을 잃는다고 반박한다.
DuckLake 팀이 직접 설계하고 돌린 벤치마크라는 점은 감안해야 한다.

## 시작하기

### 카탈로그 데이터베이스 고르기

DuckDB에서는 확장을 설치하고 `ATTACH` 한 줄로 시작한다.
`DATA_PATH`는 Parquet 파일이 놓일 위치이며,
로컬 디렉터리, S3, GCS, Azure Blob, NFS 등
DuckDB가 지원하는 파일 시스템이면 된다.

```sql
INSTALL ducklake;

-- 단일 클라이언트: 카탈로그가 DuckDB 파일 하나
ATTACH 'ducklake:metadata.ducklake' AS my_ducklake (DATA_PATH 'data/');

-- 여러 로컬 클라이언트: SQLite 카탈로그
INSTALL sqlite;
ATTACH 'ducklake:sqlite:metadata.sqlite' AS lake_sqlite (DATA_PATH 'data/');

-- 원격 클라이언트를 포함한 다중 사용자: PostgreSQL 카탈로그
INSTALL postgres;
ATTACH 'ducklake:postgres:dbname=ducklake_catalog host=localhost'
    AS lake_pg (DATA_PATH 's3://my-bucket/lake/');

USE my_ducklake;
```

| 카탈로그   | 맞는 용도                            | 주의할 점                                       |
| ---------- | ------------------------------------ | ----------------------------------------------- |
| DuckDB     | 로컬 단일 클라이언트                 | 클라이언트 하나로 제한된다                      |
| SQLite     | 같은 기계의 여러 클라이언트          | 쿼리마다 붙었다 떨어지며 쓰기 잠금을 재시도한다 |
| PostgreSQL | 원격 클라이언트를 포함한 다중 사용자 | PostgreSQL 12 이상이 필요하다                   |
| MySQL      | 권장하지 않음                        | DuckDB MySQL 커넥터의 알려진 문제가 있다        |

FAQ는 DuckDB를 진입점과 카탈로그 양쪽에 모두 써도 이득이 있다고 말한다.
시점 조회와 파티셔닝을 쓸 수 있고,
아주 커질 수 있는 DuckDB 파일 하나 대신 여러 파일에 데이터를 나눠 둘 수 있다.
여러 DuckDB 인스턴스가 PostgreSQL 카탈로그를 거쳐
같은 데이터셋을 읽고 쓰는 구성을
FAQ는 기본 DuckDB가 지원하지 않는 멀티플레이어 DuckDB라고 부른다.

### 기본 기능

README의 예제를 이어 보면 테이블 생성과 수정, 시점 조회, 스키마 변경,
변경 데이터 피드가 모두 일반 SQL로 이뤄진다.

```sql
CREATE TABLE my_ducklake.my_table (id INTEGER, val VARCHAR);
INSERT INTO my_ducklake.my_table VALUES (1, 'Hello'), (2, 'World');
UPDATE my_ducklake.my_table SET val = 'DuckLake' WHERE id = 2;

-- 스냅숏 2 시점의 테이블
FROM my_ducklake.my_table AT (VERSION => 2);

-- 스냅숏 2에서 일어난 변경 내역
FROM my_ducklake.table_changes('my_table', 2, 2);

ALTER TABLE my_ducklake.my_table ADD COLUMN new_column VARCHAR;
```

공식 FAQ는 네덜란드 철도 데이터셋을 담은 공개 DuckLake도 제공한다.
카탈로그가 DuckDB 파일이고 객체 저장소에서 바로 서비스되므로
아무 설치 없이 붙어 볼 수 있다.

```sql
ATTACH 'https://blobs.duckdb.org/datalake/nl-railway.ducklake' AS nl_railway
    (TYPE ducklake);
USE nl_railway;
FROM services LIMIT 1;
```

### 유지 관리

DuckLake는 기존 파일을 고치거나 덧붙이지 않고,
시점 조회를 위해 오래된 데이터 파일도 지우지 않는다.
테이블을 삭제해도 파일은 남는다.
실제로 공간을 돌려받으려면 `ducklake_expire_snapshots`로 스냅숏을 만료시키고
`ducklake_cleanup_old_files`로 파일을 정리해야 한다.
인라이닝을 쓰지 않는 작은 쓰기는 `ducklake_merge_adjacent_files`로 합치고,
삭제가 많은 테이블은 `ducklake_rewrite_data_files`로 다시 쓴다.
`CHECKPOINT`는 플러시, 스냅숏 만료, 파일 병합, 정리를 차례로 실행한다.
카탈로그 쪽 유지 관리는 그 데이터베이스의 몫이라,
PostgreSQL이라면 가끔 `VACUUM`을 돌리면 된다고 문서는 말한다.

## v1.0과 주변 구현

### v1.0에서 더해진 기능

v1.0 발표 글은 2025년 말 이후 병합된 PR 108개를 부록으로 붙였고,
그중 68개가 신뢰성과 정확성, 12개가 내부 리팩터링,
12개가 성능 개선이라고 분류했다.
사용자에게 보이는 변화는 다음과 같다.

- 데이터 인라이닝 기본 활성화와 삭제·수정 인라이닝
- `SET SORTED BY`로 정렬 순서를 지정하는 정렬 테이블. 압축, 플러시, 삽입 때 정렬한다
- Iceberg와 같은 murmur3 해시를 쓰는 버킷 파티셔닝 `bucket(N, column)`
- 파일별 경계 상자 통계를 남기는 `GEOMETRY`와 문자열 대신 이진으로 저장하고 쪼개 둘 수 있는 `VARIANT` 타입
- Iceberg v3의 삭제 벡터를 Puffin 파일로 읽고 쓰는 실험 기능
- 파일 행 수 통계로 `COUNT(*)`에 답해 S3 테이블에서 8배에서 258배 빨라진 경로

새 확장 버전으로 붙어도 카탈로그를 자동으로 이전하지 않고
`AUTOMATIC_MIGRATION`으로 명시해야 하게 바뀐 것도 v1.0의 변화다.
v1.1에는 VARIANT 인라이닝과 여러 삭제 벡터를 담는 Puffin 파일이 잡혀 있고,
v2.0 후보로는 Git 같은 브랜치와 병합, 권한 기반 역할,
증분 구체화 뷰가 올라 있다.

### Frozen DuckLake

Madhive의 Mark Harrison이 쓴 게스트 글은
카탈로그 서버 없이 읽기 전용 DuckLake를 서비스하는 방법을 소개한다.
외부 프로그램이 만든 Parquet 파일을 `ducklake_add_data_files()`로
로컬 DuckDB 카탈로그에 등록하고,
그 카탈로그 파일을 객체 저장소나 HTTPS로 올리면
누구나 읽기 전용으로 붙을 수 있다.
등록은 Parquet 메타데이터만 읽으므로 빠르고,
갱신은 카탈로그 파일을 새로 만들어 바꿔 끼우는 식이다.
저장 비용 외에 추가 비용이 거의 없고
공개 버킷으로도 내놓을 수 있다는 것이 장점이다.

### DuckDB 밖의 구현

명세가 SQL 테이블과 쿼리로 정의돼 있어 DuckDB가 아닌 엔진도 구현할 수 있다.
v1.0 발표 시점에 Apache DataFusion(Hotdata), Apache Spark(MotherDuck),
Trino 두 갈래, Pandas 데이터프레임 클라이언트가 있었고,
MotherDuck은 카탈로그와 저장소를 함께 관리하는 호스팅 서비스를 낸다.
DuckLake 리드 개발자 pdet는 확장을 C++로 쓴 이유를
DuckDB 내부의 테이블 스캐너, 형 변환 함수와 긴밀하게 붙기 위해서라고 설명하고,
DuckLake 자체는 C++일 필요가 전혀 없다며
Rust, Scala, Kotlin 구현을 예로 들었다.[^pdet]

Hotdata는 AI 에이전트마다 격리된 데이터베이스를 밀리초 단위로 만들어 주는
서비스에 DataFusion용 DuckLake를 넣었다.
자체 메타데이터 계층과 Iceberg를 검토한 끝에,
관계형 카탈로그가 이해하고 구현하기 쉬워서 DuckLake를 골랐다고 한다.
TPC-H 22개 쿼리를 Parquet 직접 읽기와 비교한 결과
SF1에서 4,398 ms 대 4,461 ms로 메타데이터 오버헤드가 드러나지 않았다.
Hotdata의 eddietejeda는 HN에서 Iceberg가 저지연 작업에는 너무 무거웠고,
datafusion-ducklake가 직접 만든 어떤 전용 카탈로그만큼 빠르다고
적었다.[^eddietejeda]
smithclay는 DuckLake가 DuckDB를 요구하지 않는 명세라는 점이
잘 알려지지 않았다며,
쓸 곳을 찾는다면 에이전트 실행 추적을 전부 넣어 보라고 권했다.[^smithclay]

## 트레이드오프

### 카탈로그 데이터베이스가 새 의존점이 된다

메타데이터를 데이터베이스에 옮기면 객체 저장소 왕복은 사라지지만
그 데이터베이스가 레이크 전체의 단일 의존점이 된다.
Lucasoato는 Delta 로그에 해당하는 정보를
JSON이나 Parquet가 아닌 데이터베이스에 두면
훨씬 빠르지만 의존성이 하나 생긴다고 정리하고,
데이터베이스 기반 카탈로그를 쓰고 있었다면
어차피 생겼을 의존성이라고 덧붙였다.[^Lucasoato]
반대로 Iceberg를 파일 기반 카탈로그나 REST 카탈로그로 쓰던 조직에게는
운영할 데이터베이스가 하나 늘어난다.

규모가 커지면 무엇이 병목이 되는지도 달라진다.
buremba는 DuckLake가 연산 계층을 수평으로 늘려 쿼리 병렬성을 얻는 대신
메타데이터 계층의 확장성은 풀려 하지 않는다고 짚었다.
DuckDB 연산 노드가 많아지면 PostgreSQL은 따로 키워야 한다는 것이다.[^buremba]
매니페스토는 PostgreSQL 카탈로그로도
수백 TB와 수천 개 연산 노드까지 간다고 말하지만,
공식 로드맵의 자금 지원 대기 목록에는
PostgreSQL 왕복 횟수를 줄이고 큰 메타데이터를 최적화하는 작업이 올라 있다.
문서에는 DuckDB, SQLite, PostgreSQL 카탈로그별 백업과 복구 안내가 따로 있는데,
카탈로그를 잃으면 Parquet 파일만으로는 테이블 상태를 되살릴 수 없기 때문이다.

### 접근 제어는 버킷과 카탈로그 권한을 조합해야 한다

DuckLake에는 자체 권한 모델이 없다.
FAQ는 인증을 카탈로그 데이터베이스에 맡긴다고 하고,
접근 제어 안내서는 슈퍼유저, 쓰기, 읽기 역할이
DuckLake에 실제로 구현된 것이 아니라 안내용 구성이라고 밝힌다.
카탈로그에는 PostgreSQL의 `SELECT`, `INSERT` 같은 권한을 주고,
저장소에는 `/⟨schema⟩/⟨table⟩/⟨partition⟩/` 경로 규칙과 버킷 정책으로
스키마, 테이블, 파티션 단위 권한을 건다.

tomwphillips는 경쟁 제품보다 우아하고 뛰어난 설계라고 보면서도,
접근 제어가 버킷이 할 수 있는 범위에 갇혀 행·열 단위 제어와 열 마스킹이 없으므로
일반적인 기업 BI에는 나쁜 선택이라고 비판했다.[^tomwphillips]
efromvt는 버킷을 잠그고
Spark나 Presto 같은 엔진 계층에서 통제하면 된다고 답하면서,
그러면 엔진을 거치지 않는 접근이 막히고
레이크하우스의 접근 제어가 기업용 데이터베이스보다 덜 성숙하다는 점은
인정했다.[^efromvt]
DuckLake 팀도 권한 기반 역할을 v2.0 후보로 올려 두었다.
지금은 Postgres와 S3를 제대로 설정하면 가능하지만
DuckLake 안에서 관리하기 쉽게 만들고 싶다는 설명이다.

### 작은 변경과 동시 쓰기가 레이크의 일인가

매니페스토는 데이터 레이크의 가장 큰 성능 문제 두 가지로
작은 변경과 많은 동시 변경을 꼽고 DuckLake가 둘 다 개선한다고 말한다.
nxm은 이것이 애초에 데이터 레이크의 자연스러운 용도가 아니며,
한 테이블에 여러 작성자가 쓰는 설계라면 더 그렇다고 반박했다.[^nxm]
인라이닝은 이 반박에 대한 DuckLake의 답이다.
작은 쓰기를 레이크가 감당할 일이 아니라고 미루는 대신
카탈로그 데이터베이스가 받아 두었다가 모아서 내보낸다.

다만 이 답은 카탈로그에 실제 데이터를 쌓는다는 뜻이기도 하다.
인라인 데이터가 플러시되기 전까지 그 행은 PostgreSQL에 있고,
저장소 쪽 권한이나 백업 정책만으로는 그 행을 다룰 수 없다.
쓰기 빈도가 높은 워크로드라면 플러시 주기와 카탈로그 용량을 함께 정해야 한다.

### Iceberg와 경쟁하면서 데이터 수준에서는 맞춘다

DuckLake가 저장소에 쓰는 데이터 파일과 위치 기반 삭제 파일은 Iceberg와 호환되고,
그래서 메타데이터만 옮기는 이전이 가능하며
DuckLake에서 Iceberg로 복사할 수도 있다.
버킷 파티셔닝이 Iceberg와 같은 murmur3 해시를 쓰고
삭제 벡터를 Puffin 파일로 구현한 것도 같은 방향이다.
buremba는 발표 영상을 본 뒤 DuckLake를 경쟁자라기보다
Iceberg와 양방향으로 함께 쓸 수 있는 것으로 보았다.[^buremba-2]

georgewfraser는 데이터베이스가 있는데 왜 메타데이터를 파일에 두느냐는 비판이
정확하다고 보면서도,
DuckLake 자체는 DuckDB 밖으로 퍼지지 못하고,
대신 시간이 지나며 카탈로그가 메타데이터를 흡수해
원래 Iceberg 형식이 과도기의 형태로 사라질 것이라고 예측했다.[^georgewfraser]
spenczar5는 Iceberg가 이미 여러 대형 쿼리 엔진의 지원을 받고 있고,
DuckLake 형식의 메타데이터에서 큰 데이터셋에 필요한 쿼리 병렬성을
어떻게 얻을지 그리기 어렵다고 지적했다.[^spenczar5]
v1.0까지 Spark와 Trino 클라이언트가 나오고
그 뒤 DataFusion 구현이 운영에 들어간 것은 첫 번째 우려에 대한 부분적인 답이다.
반면 이들 클라이언트가 얼마나 성숙했는지는
DuckLake 쪽 자료만으로는 판단할 수 없다.

## 함정

### 명세 1.0과 소프트웨어 1.0은 다르다

engineeringwoke는 아직 꽤 알파 수준이라며,
v1.5.4에서 카탈로그에 필터를 건 개수 집계가 깨졌고
이를 피하려 main 브랜치로 옮기자
DuckDB v2의 SQL 파서가 10배 느려지는 문제를 만났다고 적었다.[^engineeringwoke]
jauco는 명세는 1.0이지만 소프트웨어는 1.0이 아니니
쓰기 전에 버그 목록을 훑어보라고 답했다.[^jauco]
v1.0 부록이 이를 뒷받침한다.
동시 커밋 재시도 때 인라인 삭제가 조용히 사라지던 문제(#846),
동시 upsert에서 중복 행이 조용히 생기던 문제(#906),
`delete_orphaned_files`가 데이터 경로 안에 있는 카탈로그 자체를
지울 수 있던 문제(#839)가 v1.0 직전에야 고쳐졌다.
모두 결과가 틀려도 오류가 나지 않는 종류다.

### 이름 때문에 DuckDB 전용으로 오해한다

wodenokoto는 카탈로그가 DuckDB 파일인 줄 알았다가
PostgreSQL에 둘 수 있다는 것을 보고,
그렇다면 DuckLake가 아니라 PostgresLake라고 농담했다.[^wodenokoto]
iampims는 표준을 노린다면
특정 소프트웨어의 이름을 붙인 것이 역효과라고 지적했다.[^iampims]
도입을 검토하는 사람에게 이 오해는 두 방향으로 비용이 된다.
DuckDB를 쓰지 않는 팀은 처음부터 후보에서 빼고,
DuckDB를 쓰는 팀은 DuckDB 파일 카탈로그로 시작했다가
클라이언트 하나 제한에 걸린다.

### 데이터베이스 기능이 모두 따라오지는 않는다

DuckLake는 SQL로 다루지만
DuckDB 자체 데이터베이스 파일과 같은 기능을 주지 않는다.
기본 키, 고유 제약, 외래 키, 인덱스, 시퀀스는
데이터 레이크에서 강제하기에 너무 비싸다는 이유로
앞으로도 지원할 가능성이 낮다.
upsert는 `MERGE INTO`로만 할 수 있다.
`ENUM`, 고정 길이 `ARRAY`, 사용자 정의 타입, `CHECK` 제약,
`now()` 같은 비리터럴 기본값, 생성 열은 아직 없다.
기존 DuckDB 데이터베이스를 옮길 때는 이 목록부터 확인해야 하며,
문서에 이를 위한 이전 스크립트가 있다.

### 그 밖에 놓치기 쉬운 것

- 오래된 파일은 지워지지 않는다. 스냅숏 만료와 파일 정리를 돌리지 않으면 저장소가 계속 커진다.
- `ducklake_add_data_files`로 등록한 파일이 경로 규칙을 따르지 않으면 경로 기반 저장소 권한이 적용되지 않는다.
- 새 확장으로 오래된 카탈로그에 붙으면 자동으로 이전되지 않는다. 이전은 카탈로그를 만든 슈퍼유저가 해야 한다.
- snthpy는 `table_stats`와 `column_stats` 테이블에 스냅숏 버전이 없어 시점 조회에 영향을 주지 않느냐고 물었지만 스레드에서 답을 얻지 못했다.[^snthpy]
- 회사 보안 장비가 공식 사이트 접속을 막았다는 보고가 있었고, 답글은 `.select` 최상위 도메인을 원인으로 추정했다.[^SystemOut]

## 기억할 원칙

### 데이터베이스를 이미 쓰고 있다면 나머지 상태도 거기 둔다

DuckLake의 설계 판단은 한 문장으로 줄일 수 있다.
원자적 갱신이 필요해 데이터베이스를 들여왔다면,
그 데이터베이스를 포인터 하나 바꾸는 데만 쓰지 말고 상태 전체를 맡기라는 것이다.
여러 객체에 걸친 변경을 파일만으로 원자적으로 만들려는 설계는
대개 매니페스트, 재시도, 정리 작업 같은 복잡도를 끌고 온다.
이 저장소의 `code-review/reviewing-is-a-skill.md`는
DuckLake 발표에서 얻은 다중 객체 트랜잭션의 부재라는 개념으로
CI의 tarball과 체크섬 사이드카 파일 사이의 실패 모드를 찾아낸 사례를 다룬다.
같은 원리가 데이터 레이크가 아닌 곳에서도 그대로 적용된다는 증거다.

### 형식의 명세와 그 구현의 성숙도는 따로 평가한다

DuckLake 명세는 짧고 SQL로 읽을 수 있어서
Hotdata 같은 팀이 직접 구현해 운영에 넣을 수 있었다.
명세가 단순하다는 것은 구현이 단순하다는 것과 다르다.
v1.0 직전까지 동시 쓰기와 삭제 경로에서 조용한 데이터 오류가 고쳐졌다는 사실은,
트랜잭션 의미론이 명세에서는 SQL 몇 줄이어도
구현에서는 재시도, 인라인 데이터, 파티션, 압축이 얽힌
상태 기계라는 것을 보여 준다.
도입을 판단할 때는 명세 버전이 아니라
쓰려는 엔진 구현의 이슈 목록과 쓰려는 카탈로그 백엔드의 성숙도를 본다.
DuckLake를 만드는 DuckLabs의 AWS 합류와 프로젝트 지속 계획은
`duckdb/ducklabs-aws.md`에,
엔진이 빨라질수록 파일 압축과 테이블 형식의 가치가 커진다는 관찰은
`duckdb/duckdb-2-performance.md`에 있다.

---

[^Dowwie]: <https://news.ycombinator.com/item?id=44114283>

[^wodenokoto-2]: <https://news.ycombinator.com/item?id=44108933>

[^pdet]: <https://news.ycombinator.com/item?id=50022427>

[^eddietejeda]: <https://news.ycombinator.com/item?id=50013044>

[^smithclay]: <https://news.ycombinator.com/item?id=50011324>

[^Lucasoato]: <https://news.ycombinator.com/item?id=50013413>

[^buremba]: <https://news.ycombinator.com/item?id=44108347>

[^tomwphillips]: <https://news.ycombinator.com/item?id=50016993>

[^efromvt]: <https://news.ycombinator.com/item?id=50020758>

[^nxm]: <https://news.ycombinator.com/item?id=44108599>

[^buremba-2]: <https://news.ycombinator.com/item?id=44108311>

[^georgewfraser]: <https://news.ycombinator.com/item?id=44112073>

[^spenczar5]: <https://news.ycombinator.com/item?id=44107493>

[^engineeringwoke]: <https://news.ycombinator.com/item?id=50011781>

[^jauco]: <https://news.ycombinator.com/item?id=50012289>

[^wodenokoto]: <https://news.ycombinator.com/item?id=50016091>

[^iampims]: <https://news.ycombinator.com/item?id=44107133>

[^snthpy]: <https://news.ycombinator.com/item?id=44111008>

[^SystemOut]: <https://news.ycombinator.com/item?id=44110253>
