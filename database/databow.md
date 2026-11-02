# databow: ADBC로 데이터베이스를 조회하는 CLI 도구

<https://docs.columnar.tech/databow>

<https://github.com/columnar-tech/databow>

GN 토론: <https://news.hada.io/topic?id=31069>

## 소개

databow는 ADBC(Apache Arrow Database Connectivity)를 통해 여러 데이터베이스에
SQL을 실행하는 Rust 기반 CLI 도구다.
README는 호환되는 ADBC 드라이버가 있는 데이터베이스라면 무엇이든 연결할 수
있다고 적고,
문서 사이트의 Databases 페이지는 45종을 예시와 함께 나열한다.
DuckDB, PostgreSQL, MySQL, SQLite, BigQuery, Snowflake, Databricks, ClickHouse,
Redshift, Trino 등을
단일 인터페이스로 다룰 수 있다.

인터랙티브 셸과 비대화형 실행 모드를 모두 지원하며,
SQL 구문 강조, 자동 열 너비 조정 테이블 출력,
쿼리 히스토리 탐색 기능을 제공한다.
결과는 터미널 테이블 외에 JSON, JSON lines, CSV, Arrow IPC,
Parquet 파일로 내보낼 수 있다.
`--output`의 파일 확장자로 형식이 정해진다(`.json`, `.jsonl`, `.csv`,
`.arrow`와 `.ipc`, `.arrows`, `.parquet`).
`.arrow`와 `.ipc`는 Arrow IPC 파일이고 `.arrows`는 Arrow IPC 스트림이다.

ADBC 드라이버는 별도의 도구인 `dbc`로 관리한다.
`dbc install duckdb` 같은 명령으로 드라이버를 설치한 뒤,
`--driver` 플래그로 연결할 데이터베이스를 지정하는 방식이다.
일부 드라이버는 아직 프리릴리스(`--pre`) 상태다.

저장소는 Columnar Technologies가 2026년 1월 30일에 만들었고,
가장 최근 릴리스는 2026년 10월 14일의 v0.2.0이다.
기록 시점에 스타는 300개, 포크는 20개, 열린 이슈는 9개였고, 주 언어는 Rust,
라이선스는 Apache-2.0이다.[^api]

## 지원 데이터베이스

문서 사이트의 Databases 페이지에는 45종의 데이터베이스가 올라 있다.
전용 드라이버가 있는 경우도 있고, 기존 드라이버를 재활용하는 경우도 있다.
`postgresql` 드라이버는 11종, `mysql` 드라이버는 7종,
`flightsql` 드라이버는 6종을 맡고, 나머지는 데이터베이스마다 전용
드라이버를 쓴다.
프리릴리스(`dbc install --pre`)로 표시된 것은 Apache Cassandra, Apache Druid,
Apache Spark, Presto 네 종이다.

| 드라이버                                | 지원 데이터베이스                                                                                                                                                                            |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `postgresql`                            | PostgreSQL, CedarDB, Citus, CockroachDB, CrateDB, Materialize, Neon, ParadeDB, TimescaleDB, Yellowbrick, YugabyteDB                                                                          |
| `mysql`                                 | MySQL, MariaDB, TiDB, Vitess, GreptimeDB, SingleStore, OceanBase Database                                                                                                                    |
| `flightsql`                             | Apache Doris, Dremio, InfluxDB, Sail, StarRocks, XTDB (Arrow Flight SQL)                                                                                                                     |
| `duckdb`                                | DuckDB, MotherDuck                                                                                                                                                                           |
| `cassandra`, `druid`, `spark`, `presto` | Apache Cassandra, Apache Druid, Apache Spark, Presto (모두 프리릴리스)                                                                                                                       |
| 전용 드라이버                           | Amazon Redshift, Apache DataFusion, BigQuery, chDB, ClickHouse, Databricks, DuckDB Quack server, Exasol, Firebolt, Microsoft SQL Server, Oracle Database, Snowflake, SQLite, Teradata, Trino |

`CockroachDB`, `CrateDB`, `Materialize`는 `postgresql` 드라이버를 쓰되
`use_copy=false` 문(statement) 옵션이 필요하다고 문서는 적는다.

## CLI

```console
$ databow --help
Query databases via ADBC

Usage: databow [OPTIONS]

Options:
      --profile <profile>             Connection profile name or path
      --driver <driver>               Driver name (inferred from --uri scheme or profile if not specified)
      --uri <uri>                     Database uniform resource identifier
      --username <username>           Database user username
      --password <password>           Database user password
      --option <key=value>            Driver-specific database option
      --statement-option <key=value>  Driver-specific statement option
      --mode <mode>                   Table display style [default: utf8-compact]
      --query <query>                 Execute query and exit
      --file <file>                   Read and execute file and exit
      --output <file>                 Write result to file
  -h, --help                          Print help
  -V, --version                       Print version
```

`--driver`는 `--uri`의 스킴이나 프로필에서 추론할 수 있으면 생략할 수 있다.
`--statement-option`은 실행하는 모든 문에 적용되는 드라이버별 옵션이다(예:
`adbc.postgresql.use_copy=false`).

`uv tool install databow`, `cargo install databow`,
`brew install columnar-tech/tap/databow` 가운데 하나로 설치한다.

## 연결 프로필과 대화형 셸

연결 정보는 TOML 프로필 파일에 담을 수 있다.
튜토리얼의 예시는 `~/.config/adbc/profiles/warehouse.toml`에 `profile_version =
1`, `driver = “duckdb”`, `[Options]` 아래 `uri`를 적고,
표준 검색 위치에 있으면 `databow --profile warehouse`처럼 이름으로,
아니면 `--profile path/to/warehouse.toml`처럼 경로로 부른다.

대화형 셸은 쿼리를 세미콜론으로 끝내고,
줄 하나로 끝나는 점(`.`) 명령을 제공한다.
`.help`, `.last`(마지막 결과를 자르지 않고 보기),
`.maxrows`(터미널에서 기본 40행), `.maxwidth`(기본은 터미널 너비), `.mode`,
`.pager`, `.quit`(별칭 `.exit`)이 있다.
`--query`, `--file`, 표준 입력으로 실행한 결과는 행을 자르지 않는다.
`.pager`는 `.pager` 인자, 환경 변수 `DATABOW_PAGER`,
`PAGER` 순으로 명령을 고르고 기본은 `less -SRX`이다.
표 스타일은 `--mode`와 `.mode`로 바꾸며 `utf8-compact`가 기본이고,
`ascii-markdown`, `utf8-full`, `nothing` 같은 값이 있다.

## 분석

### ADBC가 해결하려는 문제: 데이터베이스 인터페이스의 세 번째 시도

데이터베이스 접근 표준은 역사적으로 두 세대를 거쳤다.
1990년대 ODBC는 C 기반으로 드라이버와 애플리케이션을 분리했고,
2000년대 JDBC는 동일한 개념을 JVM 위에서 재구현했다.
두 표준 모두 데이터를 행 단위로 전송한다는 전제에서 벗어나지 못했다.

ADBC는 그 전제를 교체한다.
Apache Arrow를 와이어 포맷으로 사용함으로써 드라이버와 클라이언트 사이에
직렬화/역직렬화 없이
컬럼형 데이터를 그대로 전달한다.
이는 분석 쿼리처럼 대량의 컬럼 데이터를 읽는 상황에서 특히 유리하다.

databow는 이 인터페이스 위에 셸 경험을 얹은 도구다.
ADBC 자체가 드라이버-불가지론적(driver-agnostic)이기 때문에,
도구 하나로 전혀 다른 아키텍처의 데이터베이스들을 같은 방식으로 다룰 수 있다.

ADBC는 분석용 데이터 접근에서 ODBC와 비슷한 위치를 차지한다고 볼 수 있다.
ODBC가 OLTP 중심의 행 지향 접근을 추상화했다면,
ADBC는 분석 중심의 컬럼형 데이터 접근을 같은 방식으로 추상화한다.

### Arrow IPC 출력이 만드는 데이터 연결 지점

쿼리 결과를 Arrow IPC 파일로 저장한다는 기능은 겉보기보다 중요하다.
Arrow IPC는 특정 언어나 프레임워크에 묶이지 않은 메모리 레이아웃
표준이기 때문에,
같은 파일을 Python pandas, Polars, DuckDB,
R의 `arrow` 패키지 등이 복사 없이 읽을 수 있다.

즉 databow는 쿼리 결과를 Arrow 생태계 전체로 전달하는 출구 역할을 한다.
데이터베이스 → databow → Arrow IPC → 분석 도구라는 흐름이 셸 파이프라인 수준의
단순함으로 구성된다.
이 출력 형식은 단순한 편의 기능이 아니라 도구의 포지셔닝 그 자체다.

### `uv`로 배포하는 Rust 바이너리의 의미

`uv tool install databow`는 얼핏 기이한 선택처럼 보인다.
Rust로 쓴 바이너리를 Python 패키지 관리자로 배포하는 것이기 때문이다.
그러나 데이터 도구 생태계에서 `uv`는 이미 언어 경계를 넘은 범용 도구 관리자로
자리를 잡아가고 있다.

데이터 엔지니어와 분석가 대부분은 Python 환경을 기본으로 쓴다.
그들에게는 `pip install`이나 `uv tool install`이 `cargo install`보다
훨씬 자연스럽다.
사용자 기반의 언어 습관을 따른 배포 결정은 기술적 순수성보다 실용적 도달 범위를
택한 것이다.

## 비평

### 드라이버 생태계의 성숙도가 도구의 실제 가용성을 결정한다

문서에 나열된 45종의 데이터베이스 목록은 인상적이지만,
드라이버 하나하나의 성숙도는 천차만별이다.
Cassandra, Druid, Spark, Presto 드라이버가 여전히 프리릴리스 상태라는 점이 이를
단적으로 보여준다.
또 45종 가운데 26종은 `postgresql`, `mysql`, `flightsql`,
`duckdb` 네 드라이버를 공유한다.
이들은 호환 프로토콜을 쓰는 서로 다른 제품이어서,
드라이버가 같아도 제품마다 달라지는 옵션(예: `use_copy=false`)이 생긴다.

ADBC 드라이버 생태계는 JDBC에 비해 아직 얇다.
JDBC는 수십 년간 누적된 드라이버 구현이 있지만,
ADBC는 JDBC보다 훨씬 늦게 나온 규격이다.
드라이버 품질의 편차, 미지원 SQL 방언, 연결 옵션 불일치 같은 문제는
통합 인터페이스라는 약속을 산발적으로 깨뜨린다.
목록이 길다는 것과 쓸 수 있다는 것은 다른 이야기다.

Go로 작성된 유사 도구 `usql`이 선례다.
`usql`은 수십 개 데이터베이스를 단일 인터페이스로 다루겠다는 같은
목표를 앞세웠다.
드라이버를 광범위하게 지원할수록 공격 표면도 함께 넓어진다.

### 인터랙티브 셸 경험은 기존 도구와의 비교를 피할 수 없다

데이터베이스별 전용 CLI(`psql`, `mysql`, `sqlite3`,
`duckdb`)는 수십 년의 사용자 피드백을 반영한 도구들이다.
자동 완성, 메타데이터 조회, 트랜잭션 제어,
에러 메시지 품질 면에서 이들을 단기간에 따라잡기 어렵다.

databow가 SQL 구문 강조와 정렬된 테이블 출력을 제공한다는 것은 알 수 있지만,
실제 인터랙티브 사용 경험에서 어떤 한계가 드러나는지는 문서만으로
가늠하기 어렵다.
멀티 데이터베이스 지원을 위해 개별 데이터베이스에 특화된 경험을 얼마나
포기했는지가
실사용자에게 가장 민감한 부분일 것이다.

이 비교에서 대표적인 경쟁자는 DuckDB다.
이미 DuckDB를 쓰는 사용자가 databow를 써야 할 이유가 무엇인지가
넘어야 할 문턱이다.

### 연결 프로필 기능의 보안 모델이 명확하지 않다

`--profile` 플래그로 연결 정보를 파일에서 불러오는 기능은 튜토리얼이 TOML 형식과
`~/.config/adbc/profiles/` 위치까지 보여 준다.
그러나 문서 사이트의 Reference 페이지는 프로필의 검색 경로와 비밀을 어떻게
다루는지를 적지 않고,
비밀번호는 `--password my_pwd`처럼 명령줄에 직접 쓰는 예시만 있다.
튜토리얼에는 비밀번호 예시와 보안 안내가 없다.
명령줄에 쓴 비밀번호는 셸 히스토리와 프로세스 목록에 남을 수 있다.

데이터베이스 CLI 도구에서 자격증명 관리는 보안상 가장 취약하기 쉬운 지점이다.
`psql`이 `.pgpass`를 통해 이 문제를 다루듯,
databow도 명확한 자격증명 관리 방식을 앞세워야 엔터프라이즈 환경에서 신뢰를
얻을 수 있다.

## 인사이트

### ADBC가 실제로 성공하려면 드라이버가 아니라 규격이 먼저 안정돼야 한다

JDBC가 성공한 핵심 이유는 규격의 안정성 때문이었다.
드라이버를 만드는 벤더들이 십수 년의 시간 동안 같은 인터페이스를 믿고
구현할 수 있었다.
ADBC는 아직 그 신뢰를 쌓는 과정에 있다.

databow 같은 도구가 많이 등장할수록 ADBC에 대한 드라이버 수요가 늘고,
드라이버가 늘수록 규격이 실전에서 검증돼 안정화된다.
이 선순환이 돌아가기 시작하는 임계점이 어디인지가 ADBC 생태계의 실질적 승부처다.
databow는 그 임계점을 앞당기는 수요 측 자극제 역할을 한다.

### Arrow IPC 출력은 “데이터베이스와 노트북 사이의 복사”를 없앤다

지금까지 분석가들은 데이터베이스 결과를 CSV로 내려받아 pandas에 올리고,
필요하면 다시 다른 도구로 변환하는 과정을 반복했다.
각 단계마다 메모리 복사가 일어나고, 형식 변환에서 타입 손실이 발생한다.

Arrow IPC는 이 경로를 단일 포맷으로 끊어낸다.
databow가 Arrow IPC를 출력하면 DuckDB, Polars,
PyArrow가 그 파일을 제로 복사로 읽는다.
쿼리 결과가 한 생태계 안에서 형식 손실 없이 이동한다는 것은,
데이터 파이프라인 설계 방식 자체를 바꾸는 힘을 가진다.
이 패턴이 정착되면 CSV는 인간이 읽기 위한 용도로만 남게 될 것이다.

### 단일 CLI로 수십 개 데이터베이스를 다루는 전략의 진짜 수혜자

databow 같은 멀티 데이터베이스 CLI의 일반적인 사용자 상은
“모든 데이터베이스를 쓰는 사람”으로 그려지기 쉽다.
그러나 실제 가장 큰 수혜자는 데이터 플랫폼 팀이나 DBA처럼
환경을 자주 바꾸거나 여러 클라이언트의 데이터베이스를 동시에 관리하는 사람이다.

전용 CLI를 열 개 외우는 대신 하나의 패턴으로 환경을 바꿀 수 있다는 것은
인지 부하를 낮추는 효과가 크다.
이 관점에서 보면 databow는 “더 좋은 psql”이 아니라
“데이터베이스 종류를 추상화하는 운영 도구”에 가깝다.
포지셔닝을 이쪽으로 잡을수록 비교 우위가 선명해진다.

### Rust 기반 데이터 도구 확산의 배경

databow가 Rust로 작성됐다는 점은 최근 데이터 도구 분야의 더 넓은 흐름과
맞닿아 있다.
Polars, DataFusion, Delta Lake의 핵심 엔진,
그리고 각종 CLI 도구들이 Rust로 구현되고 있다.

이 흐름의 공통 동기는 Python의 GIL 한계와 C/C++ 의존성 지옥을 동시에
피하는 것이다.
Rust는 네이티브 성능을 내면서 Python에서 바인딩하기도 쉽고,
단일 정적 바이너리를 배포하기도 편리하다.
databow가 `uv`로 배포 가능한 것도 결국 Rust 바이너리의 이식성 덕분이다.
데이터 도구의 구현 언어 선택이 배포 전략과 생태계 통합 방식 전체를 규정하는
시대가 됐다.

---

[^api]: GitHub, [REST API: columnar-tech/databow](https://api.github.com/repos/columnar-tech/databow)
