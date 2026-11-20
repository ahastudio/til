# Bun: SQL 우선 Go ORM

<https://bun.uptrace.dev/>

<https://github.com/uptrace/bun>

HN 토론: <https://news.ycombinator.com/item?id=31760990> (4점, 0개 댓글)

## 소개

Bun은 Uptrace가 만드는 Go ORM이다.
README는 SQL을 감추지 않고 끌어안는 현대적 ORM이라고 소개하고, 사이트는 마법
없이 Go와 SQL만 쓴다고 말한다.
Go의 정적 타입으로 복잡한 질의를 쓰고, 구조체와 맵과 스칼라와 슬라이스로 결과를
읽는 것이 핵심이다.

GitHub API로 2026년 11월 20일에 읽은 저장소 정보는 다음과 같다.

| 항목        | 값                        |
| ----------- | ------------------------- |
| 라이선스    | BSD-2-Clause              |
| 언어        | Go                        |
| 별과 포크   | 별 5,001개, 포크 323개    |
| 열린 이슈   | 38개                      |
| 저장소 생성 | 2021년 5월 3일            |
| 마지막 푸시 | 2026년 11월 19일          |
| 최신 릴리스 | v1.3.0 (2026년 10월 3일)  |
| 홈페이지    | `https://bun.uptrace.dev` |

프로젝트 사이트의 첫 화면과 안내 문서를 읽었다.
사이트가 링크한 문서 가운데 질의 작성,[^bun-queries] 관계,[^bun-relations] 모델
정의,[^bun-models] 마이그레이션,[^bun-migrations] go-pg에서
옮기기,[^bun-pg-migration] 입문 안내를[^bun-golang-orm] 열어 읽었다.
README는 Bun이 APM 도구 Uptrace의 후원으로 만들어졌다고 밝히며 OpenTelemetry
예제를 제공한다.
이 문서는 설치하거나 코드를 실행해 보지 않았다.

## 구성

README가 내세우는 특징은 다음과 같다.

- SQL 우선: SQL처럼 읽히는 질의를 쓴다.
- 여러 데이터베이스: PostgreSQL, MySQL과 MariaDB, MSSQL, SQLite, Oracle을
지원한다.
- 타입 안전과 유연한 스캔: 구조체, 맵, 스칼라, 슬라이스로 결과를 읽는다.
- 성능: `database/sql` 위에 만들어 부담이 적다고 한다.
- 관계: 구조체 태그로 테이블 관계를 정의한다.
- 운영 기능: 마이그레이션, 픽스처, 소프트 삭제, OpenTelemetry를 갖춘다.

사이트 첫 화면은 PostgreSQL, MySQL 5.7+, MSSQL, SQLite를 나열하고 연결 풀, 질의
훅, 픽스처, 테스트 도구를 언급한다.
README의 드라이버 표는 PostgreSQL용 `pgdriver`, SQLite용 `sqliteshim`을 제공하고
나머지는 `go-sql-driver/mysql`, `go-mssqldb`, `go-ora` 같은 외부 드라이버를
쓴다.

### 질의 작성

공식 문서가 밝히는 설계 목표는 관용적인 SQL을 쓰도록 돕는 것이지 어색한 구문
뒤에 감추는 것이 아니다.[^bun-queries]
문서는 psql 같은 CLI에서 질의를 먼저 써 보고 Bun의 질의 빌더로 다시 구성하라고
권한다.[^bun-queries]
질의 빌더의 주된 일은 긴 질의를 논리적 블록으로 나누고, `bun.Ident`와
`bun.Safe`로 자리 표시자를 안전하게 치환하며, 구조체 모델에서 열 목록과 일부
조인을 만드는 것이다.[^bun-queries]
질의는 `bun.DB`, `bun.Tx`, `bun.Conn`에서 `NewSelect`, `NewInsert`, `NewUpdate`,
`NewDelete`, `NewCreateTable`로 만들고 `Exec`나 `Scan`으로
실행한다.[^bun-queries]
결과는 구조체, `map[string]interface{}`, 스칼라, 그 슬라이스로 읽고, `bun.IDB`
인터페이스로 `DB`와 `Tx`와 `Conn`을 함께 받는 함수를 쓸 수 있다.[^bun-queries]

### 모델과 관계

모델은 테이블을 나타내는 Go 구조체이고 `bun.BaseModel` 필드로 테이블 이름과
별칭을 지정한다.[^bun-models]
문서는 이 필드가 일관된 인터페이스, 소프트 삭제 같은 기능, 더 나은 오류 정보를
준다고 설명한다.[^bun-models]
관계는 `has-one`, `belongs-to`, `has-many`, 다형 `has-many`, `many-to-many`를
지원하며 `Relation("Author")`로 조인한다.[^bun-relations]
관계 문서는 선택할 열을 줄이는 `Column`, 조인만 하고 선택하지 않는
`Exclude("*")`, LEFT JOIN을 INNER JOIN처럼 쓰는 조건 같은 예를
든다.[^bun-relations]

### 마이그레이션

마이그레이션은 Go 함수이거나 SQL 문이 든 텍스트 파일이다.[^bun-migrations]
파일 이름은 고유한 이름과 설명으로 이루어지며 예는
`20210505110026_add_foo_column.go`이다.[^bun-migrations]
완료된 이름은 `bun_migrations` 테이블에 저장되고, 실패한 마이그레이션도 적용된
것으로 표시해서 부분 적용을 되돌릴 수 있게 한다.[^bun-migrations]
여러 마이그레이션은 한 그룹으로 실행되고 되돌릴 때는 마지막 그룹 전체를
되돌린다.[^bun-migrations]
한 개만 되돌리려면 마지막 그룹을 되돌리고 건너뛸 것을 지운 뒤 다시 실행하거나,
필요한 변경을 새 마이그레이션으로 추가한다.[^bun-migrations]
SQL 마이그레이션은 `.up.sql` 파일이며 `--bun:split` 줄로 여러 문장을
나눈다.[^bun-migrations]

### go-pg에서의 이전

Bun은 go-pg를 다시 쓴 것이다.[^bun-pg-migration]
go-pg의 README는 자신이 유지보수 모드에 있고 중요한 문제만 고치며 새 개발은
Bun에서 이루어진다고 쓴다.[^go-pg-readme]
Bun의 이전 안내는 질의 빌더가 go-pg와 호환되도록 노력했고 거의 안 쓰는 일부
API(예: `WhereOrNotGroup`)만 지웠다고 설명한다.[^bun-pg-migration]
문서는 용어에 익숙해지면 8만에서 10만 줄의 go-pg 앱을 하루 안에 옮길 수 있다고
주장한다.[^bun-pg-migration]
Go 영값을 SQL NULL로 보내던 go-pg의 기본 동작은 바뀌어서, 옛 동작은 `nullzero`
태그로 얻는다.[^bun-pg-migration]
go-pg가 `has-one`과 `belongs-to`의 이름을 잘못 썼다고 하며 두 이름을 서로 바꿔야
한다고 안내한다.[^bun-pg-migration]

## 사용법

README의 기본 예제는 SQLite 메모리 데이터베이스로 시작한다.
`sql.Open`으로 연결을 열고 `bun.NewDB(sqldb, sqlitedialect.New())`로 감싼다.
모델은 `bun:",pk,autoincrement"` 같은 태그를 단 구조체이다.
`db.NewCreateTable().Model((*User)(nil)).Exec(ctx)`로 테이블을 만들고,
`NewInsert`와 `NewSelect().Model(user).Where("id = ?", user.ID).Scan(ctx)`로
읽고 쓴다.

복잡한 질의는 `With`로 공통 테이블 식(CTE)을 이어 붙인다.
README와 사이트는 지역별 매출 예제를 보이고, 사이트는 생성된 SQL이 손으로 쓴
것과 같다고 쓴다.
개발 중에는 `bundebug`의 질의 훅으로 실행되는 SQL을 출력하고, 운영에서는
`bunotel` 훅으로 분산 추적을 붙인다.
README는 마이그레이션에 `migrate.NewMigrations()`와 `MustRegister`로 올리기와
내리기 함수를 등록하는 방식을 보인다.

## 분석

### 설계의 중심은 SQL을 대체하지 않는 것이다

Bun의 문서는 반복해서 SQL을 먼저 쓰라고 안내한다.[^bun-queries]
이 구조에서 ORM이 하는 일은 SQL 생성이 아니라 안전한 치환, 구조체 매핑, 관계
조인 같은 보조이다.
Reddit에서 krkrkrneki는 요즘 순수 SQL을 쓰고 Bun은 구조체로 옮기는 데만 쓴다고
적었는데,[^krkrkrneki] 이는 문서가 의도한 사용 방식과 가깝다.
이는 이 문서의 해석이다.

### 쓸 수 있는 영역이 질의 빌더와 ORM 사이에 걸친다

Reddit의 Trk-5000은 Bun이 본격 ORM보다 질의 빌더에 가깝고 동적 SQL을 쓸 때만
쓰겠다고 했다.[^trk-5000]
같은 글에서 RBZ31은 기본 질의를 넘으면 ORM과 싸우게 되어 자신은 SQL을 선호한다고
적었다.[^rbz31]
문서의 관계 기능과 마이그레이션, 소프트 삭제까지 보면 Bun은 질의 빌더 이상을
제공하지만, 이 둘의 경계를 어떻게 읽느냐가 사용자마다 다르다.

### go-pg의 후속이라는 계보가 문서의 큰 부분을 차지한다

Bun 문서에는 go-pg에서 옮기는 전용 안내가 있고, go-pg README는 새 개발이 Bun에서
이루어진다고 적는다.[^bun-pg-migration][^go-pg-readme]
Reddit에서 krkrkrneki는 두 라이브러리가 같은 사람들이 만들었고 go-pg로 시작한
프로젝트를 쉽게 Bun으로 올렸다고 적었다.[^krkrkrneki]
RBZ31은 go-pg가 유지보수 모드라서 새 프로젝트라면 Bun을 고르겠다고 썼다.[^rbz31]
Bun은 새 프로젝트이기보다 기존 사용자가 이어 가는 길이 먼저 마련된 도구로
읽힌다.

### 질의 API가 쪼개진 이유가 성능 서술에도 쓰인다

go-pg의 `*pg.Query` 하나가 `SelectQuery`, `InsertQuery`, `UpdateQuery`,
`DeleteQuery` 같은 작은 구조체로 나뉘었다.[^bun-pg-migration]
문서는 이것이 Bun이 go-pg보다 빨리 삽입하고 갱신하는 이유의 하나라고
쓴다.[^bun-pg-migration]
같은 변화가 Reddit 글쓴이 Jakal7이 아쉬워한 지점이기도 하다.
그는 go-pg의 `db.Model(&book).Where(...).Select` 대신 Bun이
`db.NewSelect().Model(book).Where(...).Scan(ctx)`를 요구해서 문법이 덜 친절하게
느껴진다고 적었다.[^reddit-thread]
문서가 성능의 이유로 든 구조 변화가 사용자에게는 호출 길이로 보이는 셈이다.

## 비평

### 성능과 속도의 주장은 근거가 글에 없다

사이트는 제로 오버헤드와 원시 SQL의 속도를 내세우고 README는 최소한의
오버헤드라고 쓴다.
두 문구가 다르고, 둘 다 측정 자료를 내놓지 않는다.
이 문서가 읽은 입문 문서에는 성능 팁(필요한 열만 선택하기, `LIMIT`, 배치 삽입)이
있으나 다른 라이브러리와의 비교는 없다.[^bun-golang-orm]
go-pg보다 빨리 삽입한다는 이전 문서의 서술도 수치 없이 구조 변화를 이유로만
든다.[^bun-pg-migration]

### 지원 범위를 설명하는 문서끼리 어긋난다

README는 PostgreSQL, MySQL과 MariaDB, MSSQL, SQLite, Oracle을 지원한다고 쓴다.
사이트 첫 화면은 Oracle 없이 네 가지를 나열하고 MySQL은 5.7 이상이라고 쓴다.
입문 문서의 제목은 PostgreSQL과 MySQL용 Go ORM이고,[^bun-golang-orm]
마이그레이션 문서의 제목 옆에는 PostgreSQL과 MySQL 표시만 있다.[^bun-migrations]
어느 기능이 어느 데이터베이스에서 검증되었는지는 이 문서가 확인하지 못했다.

### 마이그레이션의 규약이 사용자의 불편으로 이어진다

Jakal7은 go-pg에서 `001_migration.up.sql` 같은 이름을 쓸 수 있었는데 Bun에서는
타임스탬프 이름을 써야 해서 불편하다고 적었다.[^reddit-thread]
Bun 문서는 마이그레이션 이름을 고유 이름과 설명의 조합으로 설명하고 예로 14자리
숫자를 든다.[^bun-migrations]
이 글은 2022년 것이어서 지금의 동작과 같은지는 확인하지 못했다.
한편 1.3.0 변경 기록에는 서로 다른 파일 이름이 같은 ID를 가지면
`Migrations.Discover`가 이제 오류를 낸다는 항목이 있다.
이름 규약의 엄격함이 오히려 늘었다는 뜻으로 읽을 수 있지만 이는 이 문서의
해석이다.

### 대안 도구와의 비교가 문서에는 없다

Bun 문서는 다른 Go 도구와의 비교를 다루지 않는다.
Reddit에서는 sqlc가 원시 SQL에서 타입과 함수를 만들어 주므로 새 문법을 배울
필요가 없다는 의견이 나왔다.[^arcbjorn]
sqlc가 99%의 경우에 최선이라는 평도 있었고,[^trk-5000] sqlx를 다음에 써 보겠다는
글과,[^krkrkrneki] sqlboiler를 봤느냐는 질문도 있었다.[^guettli]
2025년의 한 답글은 sqlboiler도 이제 유지보수 모드이고 데이터베이스별 기능 지원이
빠졌다고 적었다.[^dear-tension]
이 의견들은 개인 경험이며 이 문서가 검증하지 못했다.

### 변경 기록에서 보이는 위험

1.3.0 변경 기록은 호환을 깨는 변경 네 가지를 밝힌다.
`Count`와 `Limit`과 `Offset`이 `int64`를 쓰고, `pgdriver`가
`WithInsecure(false)`일 때 서버 인증서를 검증하며, 중복 마이그레이션 ID를
거부하고, NUL을 포함한 문자열을 거부한다.
보안 항목에는 음수에서의 줄 주석 SQL 인젝션 방지(CVE-2024-44906 계열)와 NUL
문자열 차단이 있다.
투명하게 밝힌 점은 장점이지만, 인증서 검증처럼 기본 동작이 바뀐 부분은
업그레이드 때 연결이 갑자기 실패할 수 있어서 호환 영향이 있는 변경이다.
이 문서는 변경 기록의 전체 항목과 각 이슈를 열어 보지 못했다.

### 근거로 삼은 자료의 한계

Reddit 글은 2022년 11월 12일에 올라온, 댓글이 몇 개 안 되는 작은
토론이다.[^reddit-thread]
이 문서는 Reddit을 직접 열 수 없어 공개 아카이브의 사본으로 읽었고, 점수와 댓글
수는 아카이브 시점의 값이다.

## 인사이트

### 후속 라이브러리의 첫 시험은 이전 비용이다

Bun은 go-pg 사용자를 위한 이전 안내를 공식 문서로 두었다.
Reddit의 Jakal7이 겪은 마찰은 기능 부족이 아니라 익숙한 호출 방식과 이름 규약의
차이였다.
사용자는 더 나은 기능이 있어도 덜 생산적이라고 느낄 수 있다는 점이 그의 글에서
드러난다.[^reddit-thread]
이는 이 문서의 해석이다.

### SQL 우선을 내세우는 ORM은 사용자가 어디까지 SQL을 쓰는지를 묻는다

문서는 SQL을 먼저 쓰라고 하지만 결과는 구조체로 받기를 권한다.
krkrkrneki처럼 SQL은 직접 쓰고 Bun은 매핑만 쓰는 방식도 가능하고, RBZ31처럼 아예
ORM을 피하는 방식도 있다.[^krkrkrneki][^rbz31]
어느 지점에서 질의 빌더를 접고 순수 SQL로 넘어가는지에 대한 기준이 팀마다
필요하다.
이는 이 문서의 제안이다.

### 기본값이 바뀌는 업그레이드를 점검 목록으로 만든다

go-pg에서 Bun으로 옮길 때 영값이 NULL로 바뀌지 않는다는 변화와 `has-one`과
`belongs-to`의 이름 교환은 조용히 의미를 바꾸는 항목이다.[^bun-pg-migration]
1.3.0에서는 인증서 검증과 `int64` 변경이 비슷한 성격을 가진다.
이런 변화는 컴파일 오류가 아닌 동작 변화로 나타날 수 있어서, 업그레이드 때 변경
기록의 호환 항목을 먼저 읽는 절차가 필요하다.
이는 이 문서의 제안이다.

### 확인할 관찰

이 문서의 해석을 가를 관찰은 세 가지이다.
같은 질의를 Bun과 sqlc, sqlx, 원시 `database/sql`로 쓸 때의 성능과 코드 길이,
데이터베이스별로 실제 검증된 기능 범위,
1.3.0 업그레이드에서 실제로 깨지는 코드의 비율이다.
세 가지 모두 이 문서가 확인하지 못했다.

---

[^bun-queries]: Bun 문서, [Writing Queries](https://bun.uptrace.dev/guide/queries.html), 2026-11-20 열람

[^bun-relations]: Bun 문서, [ORM: Table relationships](https://bun.uptrace.dev/guide/relations.html), 2026-11-20 열람

[^bun-models]: Bun 문서, [Defining models](https://bun.uptrace.dev/guide/models.html), 2026-11-20 열람

[^bun-migrations]: Bun 문서, [Migrations](https://bun.uptrace.dev/guide/migrations.html), 2026-11-20 열람

[^bun-pg-migration]: Bun 문서, [Migrating from go-pg](https://bun.uptrace.dev/guide/pg-migration.html), 2026-11-20 열람

[^bun-golang-orm]: Bun 문서, [Golang ORM for PostgreSQL and MySQL](https://bun.uptrace.dev/guide/golang-orm.html), 2026-11-20 열람

[^go-pg-readme]: GitHub go-pg/pg, [PostgreSQL client and ORM for Golang](https://github.com/go-pg/pg), 2026-11-20 열람

[^reddit-thread]: Reddit r/golang, [Go-pg vs Bun Developer experience](https://www.reddit.com/r/golang/comments/ytktq9/gopg_vs_bun_developer_experience/), 2022-11-12


[^rbz31]: <https://www.reddit.com/r/golang/comments/ytktq9/gopg_vs_bun_developer_experience/iw5j0fr/>

[^trk-5000]: <https://www.reddit.com/r/golang/comments/ytktq9/gopg_vs_bun_developer_experience/iw6udud/>

[^krkrkrneki]: <https://www.reddit.com/r/golang/comments/ytktq9/gopg_vs_bun_developer_experience/iw8orkd/>

[^arcbjorn]: <https://www.reddit.com/r/golang/comments/ytktq9/gopg_vs_bun_developer_experience/iw8wqy8/>

[^guettli]: <https://www.reddit.com/r/golang/comments/ytktq9/gopg_vs_bun_developer_experience/iw788kf/>

[^dear-tension]: <https://www.reddit.com/r/golang/comments/ytktq9/gopg_vs_bun_developer_experience/mxsek0j/>
