# Ent: Go용 엔티티 프레임워크

<https://entgo.io/>

<https://github.com/ent/ent>

HN 토론: <https://news.ycombinator.com/item?id=33398806> (173점, 66개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=26008521> (39점, 9개 댓글)

## 소개

Ent는 Go로 쓴 엔티티 프레임워크이자 ORM이다.
데이터 모델이 큰 애플리케이션을 쉽게 만들고 유지하게 한다는 것이 README의
설명이다.
스키마를 Go 코드로 정의하고 코드 생성으로 정적 타입이 붙은 API를 만든다.

PoEAA의 이름으로 읽으면 Ent가 만드는 것은 Table Data Gateway이다.
스키마 하나마다 그 테이블의 모든 행을 다루는 클라이언트와 질의 빌더와 엔티티
구조체가 생성되고,[^fowler-tdg] 이는 J2EE의 Data Access Object를 생성하는 도구와
같은 자리에 선다.[^core-j2ee-dao]
아래 분석은 이 분류에서 출발한다.

GitHub API로 2026년 11월 20일에 읽은 저장소 정보는 다음과 같다.

| 항목        | 값                        |
| ----------- | ------------------------- |
| 라이선스    | Apache-2.0                |
| 언어        | Go                        |
| 별과 포크   | 별 17,241개, 포크 1,024개 |
| 열린 이슈   | 635개                     |
| 저장소 생성 | 2019년 6월 12일           |
| 마지막 푸시 | 2026년 10월 14일          |
| 최신 릴리스 | v0.14.6 (2026년 3월 23일) |
| 홈페이지    | `https://entgo.io`        |

README는 Meta(Facebook) 내부에서 쓰던 Ent에서 영감을 받았고 Facebook
Connectivity 팀의 a8m과 alexsn이 만들었다고 밝힌다.
지금은 Atlas 팀이 개발과 유지를 맡고 후원한다고 쓴다.
프로젝트 사이트 entgo.io는 첫 화면과 문서의 시작하기, 코드 생성, 마이그레이션
페이지를 읽었다.
첫 화면은 세 가지를 내세운다. 스키마를 Go 객체로 모델링하는 Schema As Code, 어떤
그래프든 쉽게 순회하는 기능, 코드 생성으로 얻는 100% 정적 타입의 명시적 API이다.
README는 여기에 여러 저장소 드라이버와 Go 템플릿으로 확장하는 방식을 더하며,
드라이버는 MySQL, MariaDB, TiDB, PostgreSQL, CockroachDB, SQLite, Gremlin이다.

저장소 예제의 생성 코드와 FAQ, 훅, 개인 접근 정책(privacy), 외부 템플릿 문서는
읽었고, 스키마 모서리(edge)와 GraphQL, gRPC 통합 문서는 읽지 못했다.

## 사용법

시작하기 문서가 안내하는 흐름은 다음과 같다.

1. Go 모듈을 만든다(`go mod init`).
2. `go run -mod=mod entgo.io/ent/cmd/ent new User`로 `ent/schema/user.go`를
만든다.
3. 스키마의 `Fields()`에 `field.Int("age").Positive()`,
`field.String("name").Default("unknown")` 같은 필드를 적는다.
4. `go generate ./ent`로 코드를 만든다. 클라이언트, 트랜잭션, 엔티티별 생성과
조회와 갱신과 삭제 빌더, 조건(predicate) 패키지가 생성된다.
5. `ent.Open("sqlite3", ...)`로 클라이언트를 열고 `client.Schema.Create(ctx)`로
자동 마이그레이션을 돌린다.
6. `client.User.Query().Where(user.Name("a8m")).Only(ctx)`처럼 타입이 붙은
질의를 쓴다.

관계는 `Edges()`에 `edge.To("cars", Car.Type)`처럼 적는다.

코드 생성 문서는 `ent` CLI와 프로젝트의 ent 버전을 같게 맞추라고 안내한다.
방법은 `ent/generate.go`에 `go:generate go run -mod=mod entgo.io/ent/cmd/ent
generate ./schema`를 두는 것이다.
옵션으로 `--feature`, `--template`, `--storage`, `--target`, `--header`가 있다.
외부 Go 템플릿을 넣으면 같은 이름의 기본 템플릿을 덮어쓰거나 새 파일을 만든다.
`entc`를 패키지로 쓰는 방법으로 `entc.Generate("./schema", &gen.Config{})`를
호출하는 파일을 둘 수도 있다.

마이그레이션 문서는 자동 마이그레이션이 기본적으로 덧붙이기만 하는(append-only)
방식이라고 설명한다.
새 테이블과 인덱스를 만들고 열을 추가하며 열 유형을 넓히는 일만 하고, 열이나
인덱스를 지우려면 `WithDropColumn`과 `WithDropIndex` 옵션을 켜야 한다.
`client.Schema.WriteTo`로 변경 SQL을 파일이나 표준 출력에 쓰는 오프라인 모드가
있고, 기본 외래 키는 `WithForeignKeys`로 끌 수 있다.

## 분석

### 설계의 중심은 스키마를 코드로 쓰고 나머지를 생성하는 것이다

Ent의 구조에서 사람이 쓰는 것은 스키마 파일 하나이다.
클라이언트, 빌더, 조건, 마이그레이션 정의는 모두 생성물이다.
README와 사이트가 100% 정적 타입을 내세우는 근거가 이 생성이다.
이는 문서를 이 문서가 정리한 것이다.

HN의 jitl은 이 접근이 새 질의 언어를 배우지 않으면서 저장소에 종속되지 않고 내장
언어로 그래프 모델을 다루게 한다는 점을 높이 샀다.[^jitl]
그가 꼽은 교훈은 코드 생성이 형식 수준의 마법 더미보다 이해하기 쉬울 수 있다는
것과, 좋은 ORM은 권한과 변경의 합성을 깊이 내장해야 한다는 것이다.
이것은 jitl이 Ent를 쓰지 않고 설계를 평한 의견이다.

### 도입 후기는 마이그레이션과 생성기에 모인다

HN의 ivanvanderbyl은 2년 사용 뒤 가장 잘한 기술 선택의 하나라며 Ent와 Atlas의
자동 마이그레이션, 스키마에서의 GraphQL API 생성, Protobuf 정의 생성, 여러
모서리를 잇는 복잡한 조인, GraphQL 페이지네이션의 WINDOW 절 최적화를
꼽았다.[^ivanvanderbyl]
syvolt는 스키마를 Go로 쓰는 것과 `enttest` 패키지로 테스트하기 쉬운 점을
들었다.[^syvolt]
이 후기는 Ent가 ORM을 넘어 GraphQL과 gRPC 같은 인접 계층을 같은 스키마에서
만든다는 점이 실사용의 이유임을 보여 준다.
이는 이 문서의 해석이다.

2021년 스레드에서도 bmo-at는 gorm에서 Ent로 바꿔 즐겁게 쓴다고 했다.[^bmo-at]
같은 글에서 `ent/schema` 폴더가 있는 위치에 생성 코드가 쌓여 폴더가 부푼다는
점을 아쉬움으로 적었다.

### 마이그레이션 엔진은 Atlas로 옮겨 갔다고 서술된다

HN에서 a8m은 마이그레이션이 Atlas 위에 만들어졌다고 답했다.[^a8m]
README는 현재 Atlas 팀이 프로젝트를 개발하고 후원한다고 쓴다.

### PoEAA 분류는 Table Data Gateway이다

PoEAA(Patterns of Enterprise Application Architecture)에서 Table Data Gateway는
데이터베이스 테이블 하나로 가는 관문 역할을 하는 객체이고, 인스턴스 하나가 그
테이블의 모든 행을 다룬다.[^fowler-tdg]
이 객체가 한 테이블이나 뷰에 대한 SELECT, INSERT, UPDATE, DELETE를 모두 가지며,
다른 코드는 데이터베이스와 오가는 모든 일을 이 객체의 메서드로
한다.[^fowler-tdg]
Ent는 이 설명에 그대로 맞는다.
스키마 하나마다 `UserClient` 같은 클라이언트 타입이 생성되고, `Create`,
`CreateBulk`, `Update`, `UpdateOne`, `Delete`, `DeleteOne`, `Query`, `Get`이
모두 이 타입에 있다.[^ent-client-go]
이 객체는 행 하나가 아니라 사용자 테이블 전체를 대표하며, `client.User`라는
인스턴스 하나가 모든 사용자를 다룬다.[^ent-crud]
사용하는 쪽 코드는 SQL을 쓰지 않고 이 객체의 메서드만 부른다.

Ent가 생성하는 것을 PoEAA와 J2EE의 이름으로 옮기면 다음과 같다.

| Ent의 생성물                        | PoEAA                   | Core J2EE Patterns    |
| ----------------------------------- | ----------------------- | --------------------- |
| `UserClient` (`client.User`)        | Table Data Gateway      | DataAccessObject      |
| `UserQuery`와 조건 패키지           | Query Object            | DAO의 질의 인터페이스 |
| `*ent.User`                         | 행 하나를 나르는 데이터 | TransferObject        |
| 스키마 파일                         | 해당 없음               | DAO 생성의 서술 파일  |
| 드라이버(MySQL, SQLite, Gremlin 등) | 데이터베이스            | DataSource            |
| 핸들러와 서비스 코드                | 게이트웨이를 부르는 쪽  | BusinessObject        |

오른쪽 열의 이름은 Core J2EE Patterns가 DAO 패턴의 참여자로 든
것이다.[^core-j2ee-dao]
왼쪽의 대응은 생성 코드를 읽어 이 문서가 맞춘 것이며 두 카탈로그가 Ent를
언급하는 것은 아니다.

Ent는 스스로를 ORM이라고 부르지만, 이 구성은 PoEAA의 Data Mapper와 다르다.
Data Mapper는 객체 스키마와 관계형 스키마가 달라질 수 있다는 전제에서, 둘이
서로를 모르게 하고 그 사이의 데이터 이동을 맡는 계층이다.[^fowler-data-mapper]
Ent의 엔티티 구조체는 스키마에서 그대로 생성되어 테이블과 일대일이므로 매퍼가
사이에서 해소할 차이가 처음부터 없다.
이는 이 문서의 해석이다.

### 엔티티의 메서드는 게이트웨이로 가는 지름길이다

생성된 `User`에는 `Update()`와 `QueryCars()`가 있어서 Active Record처럼
보인다.[^ent-user-go]
Active Record는 행 하나를 감싼 객체가 데이터베이스 접근을 캡슐화하고 그 데이터에
도메인 로직까지 더하는 패턴이다.[^fowler-active-record]
그러나 `Update()`의 본문은 엔티티가 가진 설정으로 클라이언트를 만들어
`UpdateOne(_m)`에 넘기는 한 줄이다.[^ent-user-go]
접근 로직은 엔티티가 아니라 게이트웨이에 있고, 엔티티는 그곳으로 가는 지름길만
갖는다.
엔티티가 설정(드라이버 포함)을 품는 것도 이 지름길을 쓰게 하고, 트랜잭션이 끝난
뒤 드라이버를 되돌리는 `Unwrap()`을 위한 것이다.[^ent-user-go]
도메인 로직은 엔티티에 없다.
그래서 이 구조를 Active Record로 부르면 데이터 접근을 엔티티가 한다는 오해가
생긴다.
이는 생성 코드를 정의에 대조한 이 문서의 해석이다.

### 질의는 Query Object가 맡는다

`client.User.Query().Where(user.Name("a8m")).Only(ctx)`는 테이블과 열이 아니라
생성된 타입과 필드로 질의를 만든다.[^ent-crud]
Query Object는 SQL로 스스로를 바꾸는 객체 구조를 클래스와 필드로 조립하게 해서,
질의를 쓰는 사람이 스키마와 무관하게 쓰고 스키마 변경을 한곳에 가두게
한다.[^fowler-query-object]
Ent의 빌더와 조건 패키지가 이 자리에 있다.
README와 사이트가 100% 정적 타입을 내세우는 것은 이 질의 객체가 생성물이기
때문이다.

### J2EE의 DAO와 같은 자리에 선다

Core J2EE Patterns의 DAO는 데이터 소스에 대한 모든 접근을 추상화하고 캡슐화하며,
업무 컴포넌트가 더 단순한 DAO 인터페이스만 쓰게 하고 데이터 소스의 구현 세부를
가린다.[^core-j2ee-dao]
Ent의 클라이언트가 같은 역할이다.
사용자 코드는 클라이언트 메서드만 부르고, 그 아래 드라이버는 MySQL, PostgreSQL,
SQLite, Gremlin 등으로 바뀐다.
DAO 패턴이 꼽은 결과(데이터 소스 투명성, 쉬운 이전, 업무 객체의 코드 단순화,
데이터 접근 계층의 한곳 집중)도 Ent 도입의 이유와 겹친다.[^core-j2ee-dao]

DAO 문서의 코드 자동 생성 전략은 더 직접적이다.
업무 객체와 DAO와 테이블 사이의 대응이 정해지면 서술 파일이나 데이터베이스
조사로 모든 DAO 코드를 만드는 도구를 쓸 수 있다고 쓴다.[^core-j2ee-dao]
Ent의 스키마 파일과 `go generate`가 이 전략을 제품으로 만든 것이다.
Ent의 새로움은 DAO의 모양이 아니라 모서리(edge)를 가진 그래프 모델과 정적 타입
API로 이를 생성한다는 점이다.
이는 이 문서의 해석이다.

### 도메인 로직은 게이트웨이 바깥에 둔다

Table Data Gateway는 SQL을 한곳에 모으는 관문이며 도메인 로직이 사는 곳이
아니다.[^fowler-tdg]
Ent의 생성 파일은 직접 고치지 말라는 `DO NOT EDIT` 머리말을 달고
있고,[^ent-user-go] FAQ가 안내하는 모델 확장은 사용자 정의 템플릿으로
`model/fields/additional`을 덮는 방법이다.[^ent-faq]

대신 Ent는 가로지르는 규칙을 게이트웨이 층에 넣게 한다.
훅은 데이터베이스 트리거와 달리 애플리케이션 수준에서 변경 작업의 앞뒤에 로직을
넣고,[^ent-hooks] 개인 접근 정책은 스키마에 한 번 쓰면 코드 어디에서 질의하든
항상 평가된다.[^ent-privacy]
스키마 패키지가 생성된 `ent`를 가져오면 순환 참조 오류가 난다고 훅 문서가
경고하는 점도 이 규칙들이 엔티티 타입 바깥의 층에서 작동함을 보여
준다.[^ent-hooks]
권한과 감사 같은 규칙은 게이트웨이에서 우회할 수 없게 하고, 업무 규칙은 그 위
층의 몫으로 남기는 구조이다.
이는 이 문서의 해석이다.

## 비평

### 게이트웨이 위에 도메인 모델을 따로 쌓아야 한다

Ent가 만드는 것은 도메인 모델을 담는 틀이 아니라 테이블과 일대일인 게이트웨이와
데이터 객체이다.
불변식과 행동을 가진 도메인 객체를 영속성과 분리해 두려면 Ent 엔티티와 별개의
도메인 타입을 만들고 둘 사이를 직접 변환해야 한다.
Data Mapper가 풀려는 문제가 정확히 이것이다.
객체가 데이터베이스 구조를 알면 한쪽의 변경이 다른 쪽으로 번진다는
것이다.[^fowler-data-mapper]
Ent 엔티티는 스키마의 모양을 그대로 가지므로, 서비스 경계에서 감싸지 않으면 컬럼
하나의 변경이 엔티티를 쓰는 모든 코드에 닿는다.
업무 규칙이 복잡한 애플리케이션에서는 큰 한계이고, 데이터 중심의 CRUD에서는
부담이 작을 것이다.
이는 이 문서의 해석이며, 실제 프로젝트에서 변환 비용이 얼마나 드는지는 확인하지
못했다.

### ORM이라는 호칭이 기대를 어긋나게 한다

Ent의 소개 문구는 ORM이고 이름은 엔티티 프레임워크이다.
객체와 관계형 모델을 잇는다는 ORM의 기대는 Data Mapper의 일이지만, 위에서 본
대로 Ent가 하는 일은 게이트웨이를 생성하는 것이다.
도메인 모델까지 해결해 줄 것으로 기대하고 도입하면 그 부분이 비어 있음을 뒤늦게
만난다.
이는 이 문서의 해석이다.

### 코드 생성에는 비용이 따른다

HN의 valenterry는 언어가 생성 없이 해낼 수 있어야 하고 생성물은 검사하고
유지하기 귀찮고 편법이 필요하다고 적었다.[^valenterry]
kbumsik은 Go에서는 IDE의 자동 완성과 검색이 생성 코드에서 완벽히 동작해 생산성이
높고, 단점은 코드 리뷰에 생성물이 섞이는 것이라고 답했다.[^kbumsik]
ibraheemdev도 변경할 때마다 큰 코드를 생성해야 하는 점이 어색하지 않느냐고
물었다.[^ibraheemdev]
시작하기 문서가 보여 주는 생성 결과는 엔티티마다 파일 여러 개(`user_create.go`,
`user_query.go`, `user_update.go`, `user_delete.go` 등)이다.
저장소에 생성물을 포함하는지, 리뷰를 어떻게 다루는지는 문서가 정하지 않고
사용자가 정한다.

### 마이그레이션의 기본은 덧붙이기뿐이다

자동 마이그레이션의 기본이 열과 인덱스를 지우지 않는다는 점은 안전하지만 스키마
정의와 실제 데이터베이스가 어긋날 수 있다는 뜻이다.
삭제하려면 옵션을 켜야 하고, 켜면 데이터가 지워질 수 있다.
문서는 이 위험과 버전 관리 마이그레이션의 사용법을 이 페이지에서 다루지 않는다.

### 사이트와 문서의 모든 주장은 만든 쪽의 서술이다

100% 정적 타입, 쉬운 그래프 순회, 확장성은 README와 사이트의 문구이다.
HN의 ThinkBeat는 .NET Entity Framework의 경험에서 코드를 스키마로 두는 방식이
델타 관리와 비효율적인 질의를 낳았다고 적었다.[^ThinkBeat]
이는 이름이 비슷한 다른 도구에 대한 경험이며 Ent에 그대로 적용되지 않는다.

### 프로젝트 상태 정보는 한 시점의 값이다

열린 이슈는 635개이고 최신 릴리스는 2026년 3월, 마지막 푸시는 10월이다.
최근 커밋에는 Go 1.27 지원과 blob 저장 지원, MySQL의 갱신 행 잠금 수정이 보인다.

### 외부 반응

HN 반응은 대체로 긍정적이었다.
vvern은 Go에서 늘 원하던 ORM의 모습이라고 했고,[^vvern] ivanvanderbyl은 gqlgen과
잘 동작하고 권한을 다루며 즉시 적재(eager loading)를 한다고
했다.[^ivanvanderbyl-2021]
Humphrey는 Django 대체가 되느냐고 물었고, kbumsik은 Ent가 완전한 웹 프레임워크가
아니라서 서버와 세션은 따로 구현해야 한다고 답했다.[^Humphrey][^kbumsik-django]

## 인사이트

### Ent는 데이터 접근 계층을 생성하는 도구로 도입하면 기대가 맞는다

Table Data Gateway와 DAO로 읽으면 도입의 방법이 분명해진다.
클라이언트와 엔티티는 데이터 접근 계층의 안쪽 구성원으로 두고, 업무 규칙은 그
위의 서비스 함수가 맡는다.
API의 경계나 도메인 로직이 `*ent.User`를 직접 주고받기 시작하면 스키마 변경이
번지는 지점이 늘어난다.
엔티티를 서비스 밖으로 내보낼지, 도메인 타입으로 바꿔서 내보낼지를 처음에 정해
두면 마찰이 줄 수 있다.
이는 이 문서의 제안이다.

### 규칙을 게이트웨이에 두는 선택은 고전적인 게이트웨이와 다르다

고전적인 Table Data Gateway는 SQL만 모은다.
Ent는 훅과 개인 접근 정책을 이 층에 넣어서 권한과 변경의 규칙이 우회되지 않게
한다.
HN의 jitl이 좋은 ORM은 권한과 변경의 합성을 깊이 내장해야 한다고 꼽은 것이 이
선택과 닿는다.[^jitl]
얻는 것은 어디서 접근하든 같은 규칙이 적용된다는 보장이고, 치르는 것은 업무
규칙이 데이터 접근 층 안에 흩어져 읽는 사람이 찾기 어려워질 가능성이다.
이는 이 문서의 해석이며, 실제 코드베이스에서의 가독성은 확인하지 못했다.

### 스키마 하나에서 여러 계층이 나오는 구조가 도입의 이유가 된다

후기에서 ORM 자체보다 GraphQL, Protobuf, 마이그레이션이 같은 스키마에서 나온다는
점이 반복해 언급된다.
스키마가 단일 진실 원천이 되면 계층 사이의 어긋남이 줄지만, 스키마 표현력의
한계가 모든 계층의 한계가 된다.
이는 이 문서의 해석이다.

### 생성 코드의 위치와 리뷰 방식은 팀이 정해야 하는 비용이다

bmo-at의 폴더 구조 불만과 kbumsik의 리뷰 소음 지적은 같은 문제의 두 면이다.
생성물을 저장소에 둘지, CI에서 만들지, 리뷰에서 접을지는 도구가 정해 주지
않는다.
도입 전에 이 규칙을 정해 두면 이후 마찰이 줄 수 있다.
이는 이 문서의 제안이다.

### ORM의 이름은 기대를 끌고 온다

Entity Framework라는 이름은 .NET 사용자에게 특정한 기억을 불러온다.
HN의 ThinkBeat와 bottlepalm의 상반된 반응은 같은 이름이 경험에 따라 기대와
경계를 함께 낳는다는 점을 보여 준다.[^bottlepalm]
Ent는 이 이름을 이어받은 Meta 내부 도구에서 왔다고 README가 쓰며, .NET 도구와의
관계는 문서에서 확인되지 않는다.

### 확인할 관찰

이 문서의 해석을 가를 관찰은 다섯 가지이다.
손으로 쓴 비즈니스 메서드를 엔티티 패키지에 두었을 때 재생성 뒤에도 남는지,
실제 프로젝트에서 스키마 변경을 운영 데이터베이스에 적용하는 흐름(자동과 버전
관리 마이그레이션),
큰 스키마에서의 생성 시간과 질의 성능,
최근 1년 이슈의 처리 속도와 릴리스 주기,
엔티티를 서비스 경계에서 도메인 타입으로 바꿀 때의 변환 코드 규모이다.

---

[^fowler-tdg]: Martin Fowler, [Table Data Gateway](https://martinfowler.com/eaaCatalog/tableDataGateway.html), 2003-03-05

[^fowler-query-object]: Martin Fowler, [Query Object](https://martinfowler.com/eaaCatalog/queryObject.html), 2003-03-05

[^core-j2ee-dao]: Oracle, [Core J2EE Patterns - Data Access Object](https://www.oracle.com/java/technologies/dataaccessobject.html), 2026-11-20 열람

[^ent-client-go]: GitHub ent/ent, [examples/start/ent/client.go](https://github.com/ent/ent/blob/master/examples/start/ent/client.go), 2026-11-20 열람

[^fowler-active-record]: Martin Fowler, [Active Record](https://martinfowler.com/eaaCatalog/activeRecord.html), 2003-03-05

[^fowler-data-mapper]: Martin Fowler, [Data Mapper](https://martinfowler.com/eaaCatalog/dataMapper.html), 2003-03-05

[^ent-crud]: Ent 문서, [CRUD API](https://entgo.io/docs/crud), 2026-11-20 열람

[^ent-user-go]: GitHub ent/ent, [examples/start/ent/user.go](https://github.com/ent/ent/blob/master/examples/start/ent/user.go), 2026-11-20 열람

[^ent-faq]: Ent 문서, [FAQ](https://entgo.io/docs/faq), 2026-11-20 열람

[^ent-hooks]: Ent 문서, [Hooks](https://entgo.io/docs/hooks), 2026-11-20 열람

[^ent-privacy]: Ent 문서, [Privacy](https://entgo.io/docs/privacy), 2026-11-20 열람

[^jitl]: <https://news.ycombinator.com/item?id=33399443>

[^ivanvanderbyl]: <https://news.ycombinator.com/item?id=33400587>

[^syvolt]: <https://news.ycombinator.com/item?id=33400658>

[^bmo-at]: <https://news.ycombinator.com/item?id=26012172>

[^a8m]: <https://news.ycombinator.com/item?id=33402533>

[^valenterry]: <https://news.ycombinator.com/item?id=33400044>

[^kbumsik]: <https://news.ycombinator.com/item?id=33402182>

[^ibraheemdev]: <https://news.ycombinator.com/item?id=26013849>

[^ThinkBeat]: <https://news.ycombinator.com/item?id=33403534>

[^vvern]: <https://news.ycombinator.com/item?id=26010666>

[^ivanvanderbyl-2021]: <https://news.ycombinator.com/item?id=26010896>

[^Humphrey]: <https://news.ycombinator.com/item?id=33402091>

[^kbumsik-django]: <https://news.ycombinator.com/item?id=33402156>

[^bottlepalm]: <https://news.ycombinator.com/item?id=33401215>
