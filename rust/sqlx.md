# SQLx: DSL 없이 컴파일 시점에 SQL을 검증하는 Rust 비동기 SQL 크레이트

<https://docs.rs/sqlx>

<https://github.com/transact-rs/sqlx>

HN 토론: <https://news.ycombinator.com/item?id=44690914> (180점, 97개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/djucxi/sqlx_typesafe_pure_sql_on_rust> (18점, 8개 댓글)

GN 토론: <https://news.hada.io/topic?id=22323>

GN 토론: <https://news.hada.io/topic?id=2160>

## 소개

SQLx는 async/await로 처음부터 만든 비동기 Rust SQL 크레이트다.
README는 쿼리 빌더 같은 DSL(domain-specific language) 없이 컴파일 시점에
검사되는 쿼리를 제공하는 것을 특징으로 내세운다.
PostgreSQL, MySQL, MariaDB, SQLite를 지원하고, 런타임은 `async-std`, `tokio`,
`actix`, TLS 백엔드는 `native-tls`와 `rustls`를 고를 수 있다.
README는 Postgres와 MySQL/MariaDB 드라이버가 `unsafe` 코드 없이 순수 Rust로
쓰였고, SQLite는 C 라이브러리 `libsqlite3`를 호출하므로 `unsafe`가
필요하다고 밝힌다.

저장소는 2019년 12월 28일에 만들어졌고 마지막 푸시는 2026년 10월 31일이다.
기록 시점에 스타는 17,618개, 포크는 1,769개, 열린 이슈는 776개였다.[^api]
저장소 주소는 `launchbadge/sqlx`에서 `transact-rs/sqlx`로 옮겨졌다.
옛 주소로 접속하면 새 주소로 연결되지만,
README와 crates.io의 저장소 필드는 아직 옛 주소를
가리킨다.[^crates]
crates.io에 올라 있는 최신 버전은 2026년 5월 21일에 나온 0.9.0이고,
누적 내려받기는 178,760,333회, 최근 내려받기는 53,025,089회다.[^crates]

HN 토론에서 운영 경험을 적은 사용자들의 보고는 대체로 긍정적이다.
echelon은 MySQL과 SQLx로 월간 활성 사용자 600만의 Actix-Web 사이트를 피크 때
초당 10만 쿼리로 돌렸고 안정적이었다고 적었다.[^echelon]
bitbasher는 Go 서버를 SQLx와 Postgres 기반의 Rust로 옮겼더니 코드 줄 수가 약 40%
줄고 메모리 사용이 줄었다고 적었다.[^bitbasher]
둘 다 사용자 본인의 보고이고, 이 문서가 재현하지는 않았다.

## 설치하기

README의 설치 안내는 의존성에 `runtime` 기능과 `tls` 기능을 함께 골라야
한다는 것이다.
둘을 합친 이전 형태의 기능 이름도 호환성 때문에 남아 있지만,
앞으로 없어질 수 있으니 따로 고르라고 README는 권한다.

```toml
# Cargo.toml
[dependencies]
sqlx = { version = "0.9", features = [ "runtime-tokio", "tls-rustls-aws-lc-rs" ] }
```

데이터베이스 드라이버도 기능으로 켠다.
`postgres`, `mysql`, `sqlite`가 있고, `sqlite-unbundled`는 번들된 SQLite 대신
시스템의 SQLite를 연결한다.
쿼리 매크로는 `macros`, 마이그레이션은 `migrate`,
`FromRow`와 `Type`과 `Encode`와 `Decode` 파생 매크로는 `derive` 기능이 필요하다.
`mysql-rsa`는 TLS 없이 RSA 비밀번호 암호화가 필요한 서버에 접속할 때만 켜라고
하며, README는 TLS를 쓰라고 권한다.
시간 타입은 `chrono`와 `time` 중에서 고르고,
둘 다 켜면 `query!` 매크로는 `chrono`를 우선한다고 한다.

## 쿼리하기

SQLx에서 `&str`은 준비되지 않은(unprepared) 단순 쿼리이고,
`Query`나 `QueryAs`는 준비된(prepared) 쿼리다.
준비된 쿼리는 실행 계획이 캐시되고 바이너리 모드로 통신하며 매개변수로 SQL
인젝션을 피한다.
README는 `PRAGMA`나 `SET`, `BEGIN`처럼 준비된 문장이 안 되는 명령에만 단순
쿼리를 쓰라고 한다.

```rust
sqlx::query("DELETE FROM table").execute(&pool).await?;

#[derive(sqlx::FromRow)]
struct User { name: String, id: i64 }

let mut stream = sqlx::query_as::<_, User>("SELECT * FROM users WHERE email = ? OR name = ?")
    .bind("user@example.com")
    .bind("example_username")
    .fetch(&mut conn);
```

`execute`는 영향받은 행 수를 돌려주고 결과를 버린다.
`fetch`는 행을 스트림으로 돌려주고, `fetch_one`, `fetch_optional`,
`fetch_all`은 결과를 한꺼번에 받는다.
`Row`는 연결의 불변 대여를 유지하므로 한 번에 하나만 존재할 수 있다.
README는 연결 풀(`sqlx::Pool`), 행 스트리밍, 연결별 문장 준비와 캐시,
중첩 트랜잭션(세이브포인트), Postgres의 `LISTEN`과 `NOTIFY`,
런타임에 드라이버를 바꾸는 `Any` 드라이버도 기능으로 든다.

## 컴파일 시점 검증

`sqlx::query!` 매크로는 SQL 문자열을 받아 문법과 의미를 컴파일 시점에 검증하고,
각 열을 필드로 가진 익명 레코드를 돌려준다.
README는 이 방식이 SQL을 직접 파싱하는 것이 아니라고 설명한다.
빌드할 때 개발용 데이터베이스에 접속해서 데이터베이스 자신이 쿼리를 검증하고
정보를 돌려주게 하는 방식이다.
그래서 개발 DB가 받아들이는 문법이면 확장 기능까지 쓸 수 있고,
검증의 깊이는 데이터베이스가 쿼리에 대해 알려 주는 정보의 양에 따라 달라진다.

빌드 시점에 `DATABASE_URL` 환경 변수가 있어야 한다.
데이터는 없어도 되지만, 실행 시점에 접속할 데이터베이스와 같은 종류이고 같은
스키마여야 한다.
개발 DB 없이 컴파일하려면 `sqlx` 명령줄 도구로 쿼리 분석 결과를 캐시하는
오프라인 모드를 쓴다.
README는 오프라인 모드가 이제 항상 켜져 있다고 적는다.

HN 토론에서 이 지점이 가장 크게 갈렸다.
tmpfs는 컴파일할 때 Postgres가 떠 있어야 해서 Docker로 묶기가 번거로웠고,
결국 SQLx를 접고 다른 드라이버로 옮겼다고 적었다.[^tmpfs]
vegizombie는 쿼리가 바뀔 때마다 데이터베이스에 다시 접속해야 하지만
데이터베이스를 대신하는 산출물을 만드는 옵션이 있고,
컴파일 시점 검사 자체가 선택이라고 답했다.[^vegizombie]
belak도 오프라인 모드로 데이터베이스 없이 Docker 빌드를 할 수 있다고
덧붙였다.[^belak]
jchw는 README가 여전히 환경 변수를 먼저 안내하고 오프라인 모드는 기본이 아니라는
점을 짚으며, 컴파일 중 데이터베이스에 접속하는 방식 자체를 없애는 편이 낫다고
주장했다.[^jchw]
maxbond는 새 사용자가 처음 만날 오류는 파일이 없다는 오류보다 데이터베이스에
연결하지 못했다는 오류여야 하고, 스키마가 계속 바뀌는 초기에는 캐시가 소용없다고
반박했다.[^maxbond]
sqlc 유지보수자라고 밝힌 conroy는 PostgreSQL 내부를 직접 재구현하는 일은 긴
꼬리의 기능까지 맞추기가 어려워서, SQLx처럼 실행 중인 데이터베이스와 대화하는
방식으로 바꾸는 것을 고려하고 있다고 적었다.[^conroy]
익명 레코드는 이름을 붙일 수 없으므로 출력 타입에 이름을 주려면
`query_as!`를 쓴다.
또 검증된 쿼리는 컴파일 시점에 일을 많이 하므로,
증분 `cargo check`와 `cargo build`를 빠르게 하려고 `sqlx-macros` 패키지를
최적화하는 설정을 소개한다.

```toml
[profile.dev.package.sqlx-macros]
opt-level = 3
```

selfmodruntime는 SQLx가 `syn`을 끌어오는데 `syn`은 컴파일이 느리다고
지적했다.[^selfmodruntime]

## 비평

### README의 예제와 목록이 서로 어긋나는 곳이 있다

README는 맨 위에서 MSSQL이 0.7 이전에 지원되었다가 드라이버 재작성을 기다리며
제거되었다고 적는다.
그런데 아래 기능 목록에는 `mssql`이 “MSSQL 데이터베이스 서버 지원 추가”로
그대로 남아 있다.
의존성 예시에 쓰인 `tls-rustls-ring-webpki`와 `tls-rustls-ring-native-roots`는
기능 목록에 없고, 목록에는 `tls-rustls`와 `tls-rustls-aws-lc-rs`만 있다.
`query!` 예시의 SQL은 `GROUP BY` 뒤에 `WHERE`를 두는데,
이 순서는 SQL 문법이 허용하지 않는다.
이 문서는 컴파일해 보지 않았으므로 이 예시가 실제로 거부되는지는
확인하지 못했다.
따라서 기능 이름은 README의 목록이 아니라 docs.rs의 기능 페이지에서 다시
확인하는 편이 안전하다.

### 컴파일 시점 검증은 빌드 환경에 데이터베이스를 요구한다

`query!`의 검증은 컴파일 시점에 실제 데이터베이스에 접속해서 이루어진다.
그래서 `DATABASE_URL`이 가리키는 스키마가 운영 스키마와 어긋나면,
컴파일이 통과해도 실행 시점에 오류가 날 수 있다.
README가 오프라인 모드로 이 의존을 줄이는 길을 열어 두었지만,
캐시한 분석 결과가 현재 스키마와 맞는지는 사용자가 따로 확인해야 한다.
README에는 캐시가 낡았는지 확인하는 방법이 적혀 있지 않다.
이 문서는 `sqlx-cli`의 README를 열어 보지 않았다.

### 검증의 범위는 데이터베이스마다 다르다

README는 쿼리 매크로가 주는 SQL 검증의 정도가 데이터베이스가 쿼리에 대해 알려
주는 정보에 달려 있다고 말한다.
세 데이터베이스에서 어떤 검증이 되고 안 되는지의 구체적 목록은 README에 없다.
특정 데이터베이스에서 기대한 검증이 안 되는 경우를 사전에 알 수 없다.

### 컴파일 시점 검증이 놓치는 곳이 있다

lovasoa는 SQL 값을 잘못된 Rust 타입으로 디코딩할 때 런타임 오류가 나고,
더 나쁘게는 쓰레기 값으로 디코딩되는 것이 가장 큰 불만이라고 적었다.[^lovasoa]
rellfy는 `LEFT JOIN`의 열을 쿼리에서 nullable로 표시해야 하고,
그러지 않으면 SQLx가 `NOT NULL`로 기대한다고 적었다.[^rellfy]
README가 검증의 깊이는 데이터베이스가 알려 주는 정보에 달려 있다고 말한 것과
같은 맥락이다.

### 동적 쿼리는 SQLx의 범위 밖이고 컴파일 시점 검사도 따라가지 못한다

banashark는 조건이 선택적으로 붙는 쿼리를 SQL 중심 방식에서 어떻게 다루는지
물었다.[^banashark]
dathinab은 SQLx가 동적 쿼리 구성을 의도적으로 다루지 않으며,
컴파일 시점 검사는 플레이스홀더만 쓰는 정적 쿼리에만 적용된다고 답했다.
동적 쿼리를 검사하려면 만들 수 있는 모든 쿼리를 만들어 검사해야 하므로 사실상
통합 테스트의 영역이고, 그런 프로젝트에는 `sea-query`나 `sea-orm` 같은
라이브러리가 맞다고 했다.[^dathinab]
fstephany는 매개변수를 전부 `Option`으로 받아 `$2 IS NULL OR ...` 형태로 조건을
건너뛰는 방법을 제안했다.[^fstephany]
williamdclt는 그 방식이 데이터베이스 엔진에 많이 의존하며,
조건이 복잡해지면 MySQL이 실행 계획을 잘못 고르는 일을 겪어서 `OR`을 `UNION`으로
쪼개야 했다고 적었다.[^williamdclt]

### 2019년 Lobste.rs 반응은 ORM인가를 두고 갈렸다

옛 주소 `launchbadge/sqlx`로 제출된 2019년의 Lobste.rs 스레드가 있다.
inactive-user는 이 방식이 오래 상상해 온 이상적인 ORM에 가깝다며
Clojure의 hugsql과 Python의 PugSQL을 비슷한 라이브러리로 들었다.[^inactive-user]
같은 사용자는 곧 자신은 쿼리를 감추는 ORM을 싫어하며,
이 라이브러리를 ORM이라고 부르지는 않겠다고 정정했다.[^inactive-user-orm]
README 예제가 문자열 보간처럼 보여 보기에 낯설다는 불만도
덧붙였다.[^inactive-user-interpolation]
roshan은 SQLx가 문장을 준비하고 변수를 바인딩해 실행하는 익숙한 절차를 따르므로
문자열 보간이 필요 없다고 답했다.[^roshan]
이스케이프는 라이브러리가 아니라 DBMS가 맡는다고 설명하면서,
자신도 확실하지는 않다는 단서를 달았다.[^roshan-prepare]
pstef도 Postgres의 매개변수화된 쿼리를 이해하는 것으로 보인다고 했다.[^pstef]
ane는 실행 중인 데이터베이스로 쿼리를 컴파일 시점에 검증하는 발상이 매우 멋지며,
전에는 Quill에서만 봤다고 썼다.[^ane]
hugsql과 PugSQL은 SQL 파일에서 코드를 생성하는 다른 방향이라고 구분했다.

이 오해는 README가 지금 DSL 없이 컴파일 시점에 검사된 쿼리를 내세우는 이유를
보여 준다.
다만 이 스레드는 초기 버전에 대한 반응이며,
이 문서는 당시 버전을 확인하지 않았다.

### SQLite 지원은 따로 확인해야 한다

README는 SQLite 드라이버가 C 라이브러리를 호출하는 유일한 예외라고 밝힌다.
HN에서는 SQLite 쪽 불만이 반복되었다.
thesuperbigfrog는 SQLite에서 동시 세션 부하가 걸리면 연결 풀 문제로
데이터베이스가 예기치 않게 사라졌고, 풀 매개변수를 바꿔도 해결되지 않아 데이터
계층을 NoSQL 방식으로 바꿨다고 적었다.[^thesuperbigfrog]
zbentley는 인메모리 SQLite를 풀 뒤에서 동시에 쓰면 풀이 데이터베이스가 프로세스
밖에 있다고 가정하기 때문에 문제가 생길 수 있다고 짚었다.[^zbentley]
cortesi는 SQLite 지원의 문제 목록이 길어서 SQLite 전용 라이브러리로 포크했고,
저수준 바인딩의 사소한 부정확함을 수십 개 고쳤다고 적었다.[^cortesi]
이 문서는 이 보고들이 0.9.0에서도 재현되는지 확인하지 않았다.

### 비동기 인터페이스에는 비용이 있다는 보고가 있다

moggers123은 SQLx에서 `rusqlite`로 바꿨더니 지연이 20배 줄었고,
원인은 비동기 장치로 보인다고 적었다.[^moggers123]
pie_flavor는 I/O에 묶인 작업에서 비동기가 20배 느려질 수는 없고 뮤텍스나 WAL
설정 문제 같다고 반박했다.[^pie_flavor]
moggers123은 작은 합성 벤치마크로 다시 재 보니 20배가 아니라 약 3배(릴리스
빌드에서는 5배) 느렸다고 정정했다.[^moggers123-rerun]
이 문서는 그 벤치마크를 열어 보거나 재현하지 않았다.

### GN에서는 0.7에 머문 사용자와 sqlc 선호가 나왔다

2025년 8월 4일의 GN 스레드에서 mokaa는 `_bin` collation 필드를 `String`으로
직렬화하지 못하는 문제가 1년 넘게 고쳐지지 않았다고 적었다.
회귀 이슈라서 많은 사용자와 라이브러리가 0.7 버전에 머물러 있고,
그래서 프로덕션에는 무리라는 판단이다.[^mokaa]
secret3056은 고쳐진 것 같지만 거의 1년이 걸렸다고 답했고,[^secret3056-fix]
yshrust는 해당 이슈로 `launchbadge/sqlx` 이슈 3387을 들었다.[^yshrust]
이 문서는 그 이슈를 열어 보지 않았고, 수정이 0.9.0에 들어 있는지도
확인하지 않았다.

secret3056은 네이티브 쿼리를 쓰고 코드를 생성하는 Go의 sqlc 방식을 좋아한다고
적었다.[^secret3056]
이는 앞서 sqlc 유지보수자 conroy가 실행 중인 데이터베이스와 대화하는 방식을
고려한다고 한 것과 방향이 겹친다.
GN 운영자 xguru는 5년 전 소개 이후의 변화로
컴파일 시점의 실제 DB 연동 검증, tokio·async-std·actix 호환,
커넥션 풀, 중첩 트랜잭션, AnyPool을 꼽았다.[^xguru]
그런데 2019년 Lobste.rs 스레드의 ane는 이미 실행 중인 데이터베이스로 검증하는
방식을 언급했으므로, xguru가 말한 변화의 시점은 이 문서가 확인하지 못했다.

### 릴리스 이후의 변경은 crates.io 버전에 들어 있지 않다

crates.io의 최신 버전 0.9.0은 2026년 5월 21일에 나왔고,
저장소의 마지막 푸시는 2026년 10월 31일이다.[^api][^crates]
그 사이 `main`에 들어간 변경은 0.9.0에 없으므로,
GitHub에서 읽은 문서와 `main`의 동작이 `cargo add`로 받은 버전과 다를 수 있다.
이 문서는 `main`과 0.9.0 사이의 차이를 열어 보지 않았다.
README에 쓰인 `version = "0.9"`와 기능 이름이 받은 버전과 맞는지 확인하려면
docs.rs의 해당 버전 페이지를 기준으로 삼는다.

## 체크리스트

- [ ] `runtime-*` 기능 하나와 `tls-*` 기능 하나를 각각 골랐는가
- [ ] 쓰는 데이터베이스의 드라이버 기능(`postgres`, `mysql`, `sqlite`)을 켰는가
- [ ] `query!`를 쓸 CI와 개발 환경에 `DATABASE_URL`이 가리키는 데이터베이스가 있는가
- [ ] 그 데이터베이스의 스키마가 운영 스키마와 같은가
- [ ] 개발 DB 없이 빌드해야 한다면 오프라인 모드의 캐시를 만들었는가
- [ ] `mysql-rsa`를 켜기 전에 TLS를 쓸 수 없는지 확인했는가
- [ ] `sqlite`를 쓴다면 번들 SQLite와 시스템 SQLite 중 무엇을 연결할지 정했는가
- [ ] 의존성에 `launchbadge/sqlx`와 `transact-rs/sqlx` 중 어느 주소를 적었는지 알고 있는가

---

[^api]: GitHub, [REST API: transact-rs/sqlx](https://api.github.com/repos/transact-rs/sqlx)

[^crates]: crates.io, [sqlx](https://crates.io/api/v1/crates/sqlx)

[^tmpfs]: <https://news.ycombinator.com/item?id=44692758>

[^vegizombie]: <https://news.ycombinator.com/item?id=44692919>

[^belak]: <https://news.ycombinator.com/item?id=44715431>

[^jchw]: <https://news.ycombinator.com/item?id=44718896>

[^maxbond]: <https://news.ycombinator.com/item?id=44719861>

[^conroy]: <https://news.ycombinator.com/item?id=44729344>

[^selfmodruntime]: <https://news.ycombinator.com/item?id=44720844>

[^echelon]: <https://news.ycombinator.com/item?id=44717849>

[^bitbasher]: <https://news.ycombinator.com/item?id=44715579>

[^lovasoa]: <https://news.ycombinator.com/item?id=44720908>

[^rellfy]: <https://news.ycombinator.com/item?id=44718910>

[^banashark]: <https://news.ycombinator.com/item?id=44719299>

[^dathinab]: <https://news.ycombinator.com/item?id=44721735>

[^fstephany]: <https://news.ycombinator.com/item?id=44720886>

[^williamdclt]: <https://news.ycombinator.com/item?id=44723048>

[^thesuperbigfrog]: <https://news.ycombinator.com/item?id=44715527>

[^zbentley]: <https://news.ycombinator.com/item?id=44715745>

[^cortesi]: <https://news.ycombinator.com/item?id=44718720>

[^moggers123]: <https://news.ycombinator.com/item?id=44718220>

[^pie_flavor]: <https://news.ycombinator.com/item?id=44722440>

[^moggers123-rerun]: <https://news.ycombinator.com/item?id=44773302>

[^inactive-user]: <https://lobste.rs/s/djucxi/sqlx_typesafe_pure_sql_on_rust#c_w8jbem>

[^inactive-user-orm]: <https://lobste.rs/s/djucxi/sqlx_typesafe_pure_sql_on_rust#c_tcj0c4>

[^inactive-user-interpolation]: <https://lobste.rs/s/djucxi/sqlx_typesafe_pure_sql_on_rust#c_sfbo10>

[^roshan]: <https://lobste.rs/s/djucxi/sqlx_typesafe_pure_sql_on_rust#c_j8zhjr>

[^roshan-prepare]: <https://lobste.rs/s/djucxi/sqlx_typesafe_pure_sql_on_rust#c_irjyv5>

[^pstef]: <https://lobste.rs/s/djucxi/sqlx_typesafe_pure_sql_on_rust#c_fedyat>

[^ane]: <https://lobste.rs/s/djucxi/sqlx_typesafe_pure_sql_on_rust#c_pjlirn>

[^mokaa]: <https://news.hada.io/topic?id=22323#cid42082>

[^secret3056-fix]: <https://news.hada.io/topic?id=22323#cid42104>

[^yshrust]: <https://news.hada.io/topic?id=22323#cid42100>

[^secret3056]: <https://news.hada.io/topic?id=22323#cid42103>

[^xguru]: <https://news.hada.io/topic?id=22323#cid42071>
