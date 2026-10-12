# Neon: 스토리지를 떼어 내 브랜치하고 잠드는 Postgres

<https://neon.com/>

<https://github.com/neondatabase/neon>

HN 토론: <https://news.ycombinator.com/item?id=31536827> (667점, 330개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=41184952> (101점, 50개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/2sxjo2/neon_serverless_fault_tolerant> (4점, 4개 댓글)

GN 토론: <https://news.hada.io/topic?id=6658>

## 소개

Neon은 Postgres의 스토리지 계층을 새로 써서 컴퓨트와 스토리지를 분리한 서버리스
Postgres 서비스다.
2021년 Nikita Shamgunov, Heikki Linnakangas, Stas Kelvich가 창업했고,
2022년 공개 서비스를 시작했다.
공동 창업자 블로그 글은 AWS Aurora와 Microsoft Socrates 논문에서
아이디어를 가져오고 S3 연동과 브랜치를 더했다고 설명한다.
블로그 글은 Heikki Linnakangas를 초기 Postgres 커미터 중 한 명으로 소개하며,
그가 업스트림 Postgres와 스토리지 엔진의 통합을 맡았다고 쓴다.

2025년 5월 14일 Databricks가 Neon 인수 의사를 발표했다.
Databricks 보도자료는 인수 이유로 에이전트 워크로드를 들면서,
내부 원격 측정에서 Neon에 프로비저닝된 데이터베이스의 80% 이상을 사람이 아니라
AI 에이전트가 만들었다고 밝혔다.
같은 보도자료는 Neon이 격리된 Postgres 인스턴스를 500밀리초 이내에 띄운다고
적었다.
인수 금액은 공식 발표에 나오지 않는다.
홈페이지는 지금 Neon이 2025년 5월부터 Databricks 플랫폼의 일부라고 적고,
문서는 2025년에 Neon이 Databricks에 합류했다고 쓴다.
2026년 8월에는 PGlite와 Electric 동기화 엔진을 만든 Electric 팀이 Databricks
안의 Neon 팀으로 들어왔다.

그사이 제품의 정체성도 바뀌었다.
홈페이지 제목은 이제 앱과 에이전트를 위한 Postgres 백엔드이고,
데이터베이스 이름은 Lakebase Postgres다.
Neon과 Databricks는 같은 인프라 위에서 같은 Lakebase Postgres를 돌리며,
Neon 쪽은 개발자와 스타트업, 에이전트 플랫폼을,
Databricks 쪽은 Unity Catalog와 레이크하우스에 통합된 기업 고객을 맡는다.
Neon은 2026년 9월 18일 Postgres 주위에 Managed Better Auth, Data API, Functions,
Object Storage, AI Gateway를 묶은 백엔드를 정식 출시했고,
이 서비스들도 Postgres처럼 브랜치를 따라 갈라진다.
도메인은 `neon.tech`에서 `neon.com`으로 옮겼고 `neon.tech`는 리다이렉트된다.
이 저장소의 `postgresql/README.md`에 모아 둔 Neon 링크는 옛 주소를 가리킨다.

이 노트는 그중 데이터베이스, 즉 Lakebase Postgres를 다룬다.
인수 소식은 `database/databases-in-2025-review.md`에서,
Neon 블로그 글은 `llm/castform-neon-post-training.md`에서,
관리형 Postgres의 PgBouncer 제공 여부는
`postgresql/postgres-without-pgbouncer.md`에서 언급된다.

## 동작 방식

### 컴퓨트는 소모품이고 스토리지가 진실이다

Neon은 Postgres를 하나의 VM과 파일 시스템에 묶인 상태 있는 시스템으로 돌리지
않는다.
컴퓨트 계층에서는 표준 Postgres가 SQL 파싱, 실행 계획, MVCC, 잠금,
인덱스를 그대로 처리한다.
달라지는 것은 내구성의 책임이다.
컴퓨트 노드는 RAM과 로컬 NVMe를 캐시로만 쓰고 영속 상태를 갖지 않으므로,
언제 멈추거나 교체되어도 데이터가 사라지지 않는다.
Neon이 `fsync`를 `off`로 설정해 두는 것도 이 때문이다.

스토리지 계층은 세 부분으로 나뉜다.

| 구성 요소       | 하는 일                                                | 핫 경로 여부                        |
| --------------- | ------------------------------------------------------ | ----------------------------------- |
| Safekeeper      | 컴퓨트가 보낸 WAL을 여러 노드에 복제하고 정족수로 확정 | 커밋이 여기서 끝난다                |
| Pageserver      | WAL을 재생해 특정 LSN 시점의 페이지를 만들어 돌려줌    | 컴퓨트 캐시가 빗나갈 때만           |
| 오브젝트 저장소 | 만들어진 페이지 버전과 긴 이력을 불변으로 보관         | 쿼리 경로에 없음, Pageserver만 읽음 |

GitHub 저장소의 README도 같은 구조를 설명한다.
컴퓨트는 상태 없는 PostgreSQL 노드이고, Safekeeper는 WAL을 받아 Pageserver가
처리하고 클라우드 저장소에 올릴 때까지 보관한다.
코드는 Rust로 쓰였다.
2022년 HN 출시 스레드에서 공동 창업자 kelvich는 Postgres 노드가 데이터를
저장하지 않아 시작, 중지, 재배치가 쉽다고 설명하며,
가장 가까운 비교 대상은 RDS가 아니라 Aurora나 AlloyDB라고 했다.[^kelvich]

### 쓰기 경로: 커밋은 네트워크 정족수다

트랜잭션 하나가 커밋되는 순서는 다음과 같다.

1. Postgres가 공유 버퍼에서 행과 인덱스를 바꾸고 평소처럼 WAL 레코드를 만든다.
2. 컴퓨트는 WAL을 로컬 디스크에 플러시하는 대신 네트워크로 여러 Safekeeper에 보낸다.
3. Safekeeper 정족수가 Paxos 방식으로 WAL을 확인하면 커밋이 성립하고 클라이언트가 성공을 받는다.
4. 페이지 재구성과 오브젝트 저장소 업로드는 그 뒤에 비동기로 일어난다.

문서는 커밋 지연이 주로 정족수와 네트워크에 묶이며,
Safekeeper가 WAL 플러시를 묶어서 처리한다고 쓴다.
로컬 `fsync` 한 번이 아니라 네트워크 왕복이 커밋 비용이라는 뜻이다.

### 읽기 경로: 오브젝트 저장소는 쿼리 경로에 없다

컴퓨트는 페이지를 공유 버퍼, 로컬 NVMe 캐시 순서로 찾는다.
둘 다 없을 때만 Pageserver에 페이지 식별자와 LSN을 보내고,
Pageserver는 이미 만들어 둔 버전이 없으면 오브젝트 저장소에서 기준 페이지를 읽어
WAL을 그 LSN까지 재생한 뒤 돌려준다.
문서는 오브젝트 저장소 읽기가 수백 밀리초 걸릴 수 있지만 그 일은 Pageserver
안에서만 일어난다고 강조한다.
반대로 말하면 캐시가 빈 컴퓨트, 예를 들어 막 깨어난 컴퓨트의 첫 쿼리들은
Pageserver 왕복을 거친다.

2026년 9월부터 18 CU 이상 고정 크기 컴퓨트에서는
공유 버퍼가 가용 메모리의 최대 75%까지 늘었고,
변경 이력은 캐시 중심 워크로드에서 처리량이 최대 2배까지 오를 수 있다고 적었다.

### 브랜치와 history window

브랜치는 특정 시점의 이력을 가리키는 copy-on-write 복제본이다.
파일이나 페이지를 복사하지 않으므로
만드는 데 걸리는 시간이 데이터 크기와 무관하고,
부모 브랜치에 부하를 주지 않으며, 새로 쓰거나 바꾼 데이터만 저장 공간을 쓴다.
현재 시점뿐 아니라 과거 시점에서도 브랜치를 만들 수 있고,
스키마만 복제하는 브랜치도 있다.
브랜치마다 자체 컴퓨트를 붙이므로 병렬 테스트가 서로 간섭하지 않는다.
2022년 출시 스레드에서 Nikita Shamgunov는
PlanetScale의 브랜치가 스키마만 복제한다는 질문에,
Neon은 스키마와 데이터를 모두 copy-on-write로 복제한다고 답했다.[^nikita-branch]

과거로 돌아가는 기능은 모두 history window에 묶인다.
즉시 복원, Time Travel 쿼리, 과거 시점 브랜치, 스냅숏이 그렇다.
기본값은 Free 6시간, 유료 1일이며, Launch는 7일, Scale은 30일까지 늘릴 수 있다.
창을 넓히면 보관하는 변경 이력이 늘어 비용도 오른다.

### Scale to zero와 오토스케일링

컴퓨트는 5분 동안 활동이 없으면 멈추고, 다음 연결이 오면 다시 켜진다.
문서는 다시 켜지는 데 보통 수백 밀리초가 걸린다고 쓴다.
2022년 출시 당시 Nikita Shamgunov는
프로비저닝과 콜드 스타트가 모두 2초라고 답했었다.[^nikita]
Free 플랜은 이 설정을 끌 수 없고, Launch는 끌 수 있으며,
Scale은 1분부터 상시 가동까지 조정할 수 있다.
16 CU를 넘는 컴퓨트는 scale to zero 대상이 아니라 항상 켜져 있다.

오토스케일링은 컴퓨트마다 최소와 최대 CU 범위를 정하면 재시작 없이 그 안에서
크기를 바꾼다.
1 CU는 약 4GB RAM이다.
범위의 폭, 즉 최대와 최소의 차이는 8 CU를 넘을 수 없다.
홈페이지는 데이터베이스 부하를 초당 10번 감시한다고 적는다.

### 연결 풀링

Neon은 컴퓨트 앞에 PgBouncer를 트랜잭션 모드로 둔다.
호스트 이름에 `-pooler`를 붙인 연결 문자열이 풀러로 가고,
붙이지 않으면 Postgres에 바로 붙는다.
설정은 사용자가 바꿀 수 없다.

| 한도                | 값                          | 넘으면                                      |
| ------------------- | --------------------------- | ------------------------------------------- |
| `max_client_conn`   | 10,000                      | `no more connections allowed`               |
| `default_pool_size` | `max_connections`의 90%     | 큐에서 기다리다 2분 뒤 `query_wait_timeout` |
| `max_connections`   | 컴퓨트 크기에 따라 104~4000 | `remaining connection slots are reserved`   |

풀은 사용자와 데이터베이스 조합마다 따로 생긴다.
1 CU 컴퓨트라면 `max_connections`가 419이고 풀 하나가 377개까지 쓰지만,
모든 풀이 같은 419개를 나눠 쓴다.
10,000은 동시에 돌아가는 쿼리 수가 아니라
PgBouncer가 받아 주는 클라이언트 연결 수다.

`max_connections` 공식에는 함정이 하나 있다.
문서의 공식은 `min(최대 크기, 8 × 최소 크기)`를 유효 크기로 삼아
CU당 약 419.66을 곱하고 100~4000으로 자른다.
그래서 0.25~4 CU로 오토스케일링하면
최대가 4 CU여도 연결 한도는 2 CU 기준인 839다.

## 시작하기

아래 명령은 Neon CLI 문서에서 옮긴 것이고 직접 실행하지는 않았다.
CLI의 이름은 이제 `neon`이고 `neonctl`은 별칭으로 남아 있으며,
Node.js 20.19.0 이상이 필요하다.

```bash
# 설치와 로그인 (Homebrew 포뮬러 이름은 여전히 neonctl)
npm i -g neon@latest
neon login                      # 브라우저 인증. CI에서는 NEON_API_KEY 환경 변수를 쓴다

# 프로젝트 생성. 지역은 앱 서버와 같은 곳으로 고른다
neon projects create --name demo --region-id aws-ap-southeast-1

# 현재 디렉터리를 프로젝트에 연결하면 .neon 파일이 생기고 .gitignore에 추가된다
neon link

# 기본 브랜치에 psql로 접속. 로컬 psql이 없으면 내장 TypeScript 구현을 쓴다
neon psql -- -c "SELECT version()"

# 브랜치를 만들고 오토스케일링 범위와 만료 시각을 함께 정한다
neon branches create --name feature/add-index --cu 0.25-2 --expires-at 2026-10-17T00:00:00Z

# 앱에는 풀링 연결 문자열을, 마이그레이션과 pg_dump에는 직접 연결 문자열을 쓴다
neon connection-string feature/add-index --pooled
neon connection-string feature/add-index

# 브랜치에서 마이그레이션을 돌린 뒤 부모와 스키마를 비교한다
neon branches schema-diff feature/add-index ^parent

# 어제 시점에서 복구용 브랜치를 만든다 (history window 안이어야 한다)
neon branches create --name recover --parent 2026-10-09T00:00:00Z

# 다 쓴 브랜치는 지운다. 추가 브랜치는 브랜치-월 단위로 과금된다
neon branches delete feature/add-index
```

`neon branches create`는 기본으로 읽기-쓰기 컴퓨트를 붙여 만들고,
결과에 연결 문자열을 출력한다.
CI 로그에 비밀번호가 남지 않게 하려면 `--no-secrets`를 붙인다(CLI 4.9.0 이상).
CLI나 API로 만든 프로젝트의 기본 브랜치는 `main`이고 Console에서 만든 프로젝트는
`production`이다.

계정 없이 먼저 써 볼 수도 있다.
`neon claim create`는 인증 없이 임시 프로젝트를 만들어 `DATABASE_URL`을
`.env.local`에 쓰고,
사람이 나중에 `neon claim accept`로 자기 계정에 가져간다.
에이전트가 먼저 백엔드를 만들고 사람이 소유권을 넘겨받는 흐름을 위한 기능이다.

서버리스나 엣지 런타임에서는 TCP 대신 HTTP나 WebSocket으로 쿼리하는
`@neondatabase/serverless` 드라이버를 쓴다.
기본은 HTTP의 `neon()` 함수이고, 대화형 트랜잭션이나 세션이 필요할 때만
WebSocket 위의 `Pool`과 `Client`를 쓴다.

## 요금과 제한

2026년 10월 가격 페이지 기준이다.
유료 플랜은 월 최소 금액 없이 시간 단위로 계량하고 월말에 청구한다.

| 항목                 | Free                         | Launch                          | Scale                            |
| -------------------- | ---------------------------- | ------------------------------- | -------------------------------- |
| 컴퓨트               | 프로젝트당 월 100 CU-시간    | $0.106/CU-시간                  | $0.222/CU-시간                   |
| 오토스케일링         | 2 CU까지                     | 16 CU까지                       | 16 CU까지, 고정 크기는 56 CU까지 |
| Scale to zero        | 5분, 끌 수 없음              | 5분, 끌 수 있음                 | 1분부터 상시 가동까지            |
| Postgres 스토리지    | 프로젝트당 1GB, 계정 총 20GB | $0.35/GB-월, 상한 없음          | $0.35/GB-월, 상한 없음           |
| 즉시 복원 이력       | 없음                         | $0.20/GB-월                     | $0.20/GB-월                      |
| History window       | 6시간(1GB 한도)              | 7일까지                         | 30일까지                         |
| 프로젝트             | 100                          | 100                             | 1,000                            |
| 브랜치(포함분)       | 프로젝트당 10                | 10, 추가 $1.50/브랜치-월        | 25, 추가 $1.50/브랜치-월         |
| 공용 네트워크 전송   | 프로젝트당 5GB               | 프로젝트당 500GB, 이후 $0.10/GB | 프로젝트당 500GB, 이후 $0.10/GB  |
| IP 허용, 사설망, SLA | 없음                         | 없음                            | 있음                             |

Free의 Postgres 스토리지는 2026년 10월 2일 0.5GB에서 1GB로 늘었다.
Free 한도에 걸렸을 때의 동작은 항목마다 다르다.
CU-시간이나 5GB 전송량을 다 쓰면 다음 청구 주기까지 컴퓨트가 멈추고,
스토리지 한도를 넘으면 쓰기가 막히며,
브랜치 10개에 이르면 브랜치를 더 만들 수 없다.
어느 경우에도 데이터는 지우지 않는다고 가격 페이지는 밝힌다.

자식 브랜치의 스토리지는 copy-on-write라
0에서 시작해 그 브랜치에서 쓴 만큼만 늘고,
루트 브랜치는 전체 데이터 크기로 과금된다.
읽기 복제본은 별도 컴퓨트라 CU-시간에 들어간다.

지역은 AWS 8곳이다.
미국 동부 두 곳과 서부 한 곳, 프랑크푸르트, 런던, 싱가포르, 시드니,
상파울루가 있고 서울과 도쿄는 없다.
Azure 지역은 2026년 4월 7일부로 지원 중단(deprecated) 상태가 되어
이미 Azure를 쓰던 조직이 아니면 새 프로젝트를 만들 수 없고,
GCP는 지원하지 않는다.
Object Storage, Functions, AI Gateway는 그중 4개 지역에서만 돈다.

## 트레이드오프

### Scale to zero는 비용을 콜드 스타트와 바꾼다

scale to zero는 이 서비스의 경제성을 떠받친다.
멈춘 컴퓨트는 CU-시간이 0이므로,
개발과 미리보기 브랜치가 수십 개여도 실제로 쿼리가 오는 시간만 낸다.
Neon은 Free 플랜 확대를 알리며 새 프로젝트가 초당 하나 넘게 만들어진다고 밝혔다.
이런 규모의 무료 프로젝트는 잠든 컴퓨트가 공짜라는 전제 없이는
감당하기 어렵다는 것이 이 노트의 해석이다.

대가는 깨어나는 첫 연결이다.
문서는 수백 밀리초라고 하지만,
그 숫자에는 앱과 데이터베이스 사이의 물리적 거리와
중간에 낀 다른 서비스의 시작 시간이 빠져 있다고 스스로 단서를 단다.
게다가 깨어난 컴퓨트는 캐시가 비어 있어서 첫 쿼리들이 Pageserver를 거친다.
누적 통계도 컴퓨트가 멈추면 사라지므로, 자주 잠드는 데이터베이스에서는
`pg_stat_*` 뷰로 장기 추세를 보기 어렵다.

끄면 끝나는 문제도 아니다.
scale to zero를 끄면 상시 가동 비용을 내야 하고,
Free 플랜에서는 아예 끌 수 없다.
그리고 한 번도 잠들지 않는 컴퓨트는
Neon의 주간 컴퓨트 이미지 업데이트를 받지 못하므로,
문서는 매주 직접 재시작하라고 권한다.
결국 사용자는 비용, 첫 요청 지연, 유지 보수 재시작 중
무엇을 감수할지 고르게 된다.
문서가 제시하는 중간값은 정지 대기 시간을 1시간처럼 늘리고
오토스케일링 최솟값을 낮게 잡는 것이다.

### 커밋과 캐시 미스가 네트워크를 건넌다

로컬 디스크 대신 Safekeeper 정족수가 커밋을 확정하므로,
쓰기 지연의 하한은 디스크가 아니라
컴퓨트와 Safekeeper 사이의 네트워크 왕복이 정한다.
그 대신 컴퓨트가 죽어도 커밋된 데이터는 남고,
새 컴퓨트가 같은 이력에 바로 붙는다.
이것이 Aurora 계열 구조가 공통으로 고른 교환이다.

앱 서버와 데이터베이스 사이의 거리는 이와 별개로 더해진다.
문서가 지연을 줄이는 방법으로 가장 먼저 꼽는 것도 같은 지역에 두기다.
한국에서 서비스한다면 가장 가까운 Neon 지역이 싱가포르나 시드니라는 점은
지역 목록에서 바로 보이는 제약이다.
서울 리전의 애플리케이션 서버와 짝지으면
쿼리마다 국가 간 왕복이 붙는다는 것은 이 노트의 추론이다.

### 풀링은 연결 수를 얻고 세션을 잃는다

트랜잭션 모드 PgBouncer 덕분에 서버리스 함수가 요청마다 연결을 열어도
`max_connections`에 바로 부딪히지 않는다.
대신 풀링 연결에서는 `SET`과 `RESET`, `LISTEN`/`NOTIFY`, `WITH HOLD` 커서,
SQL 수준 `PREPARE`, 세션 수준 advisory lock, `LOAD`를 쓸 수 없다.
프로토콜 수준 prepared statement는 PgBouncer 1.22.0부터 지원되어
연결당 1,000개까지 쓸 수 있다.

그래서 연결 문자열이 둘이 된다.
앱은 풀링 연결을, 마이그레이션 도구와 `pg_dump`, 논리 복제,
긴 분석 쿼리는 직접 연결을 쓴다.
직접 연결은 다시 `max_connections`에 묶이므로,
작은 컴퓨트에서 마이그레이션 도구가 연결을 많이 열면 막힌다.
풀 크기를 키우려면 컴퓨트를 키우거나 데이터베이스 사용자를 나누는 수밖에 없다.

### 오픈소스지만 자체 호스팅은 사실상 다른 제품이다

`neondatabase/neon` 저장소는 Apache 2.0 라이선스이고
2026년 10월 기준 별 23,000개가 넘는다.
README는 `cargo neon init`부터 `cargo neon endpoint start`까지
Pageserver, Safekeeper, 컴퓨트를 로컬에서 띄우고
`cargo neon timeline branch`로 브랜치를 만드는 과정을 보여 준다.
2024년 HN 저장소 스레드에서 hadlock은
공식 Helm 차트가 있지만 문서가 빈약하다고 적었고,[^hadlock]
ok_dad는 스토리지 가격이 비싸다고 지적하면서도
Apache 2.0이라 직접 돌릴 수 있다는 점을 높이 샀다.[^ok_dad]
2022년 출시 스레드에서 Nikita Shamgunov는
자체 호스팅에 Kubernetes와 S3 호환 오브젝트 저장소가 필요하며,
운영 측면을 다지기 전에는 온프레미스 운영 설치를
문서화하거나 지원하지 않겠다고 답했다.[^nikita-selfhost]

그 문서는 끝내 나오지 않았고 저장소의 흐름도 바뀌었다.
마지막 태그 릴리스는 2025년 7월이고, 2025년 10월 이후 기본 브랜치의 커밋은
README 수정, GCS 관련 수정, 프록시 수정, 오타 수정 등 여섯 건뿐이다.
2025년 12월 저장소 이슈 #12843에는 프로젝트가 버려졌느냐는 질문이 올라왔고,
한 외부 사용자가 Neon Discord의 답이라며 지금은 저장소에서 활발히 작업하지
않지만 외부 기여 PR은 검토한다는 문장을 옮겼다.
이것은 공식 공지가 아니라 Discord 발언의 전언이다.
그사이 서비스는 Lakebase라는 이름을 달고 Databricks의 두 제품에 함께 들어갔다.

따라서 이 오픈소스는 탈출구라기보다 설계를 읽을 수 있는 참고 구현에 가깝다.
관리형 서비스를 이루는 컨트롤 플레인과 플릿 운영은 README의 로컬 실행 경로에
들어 있지 않다.
Neon도 2026년 9월 블로그 글에서 수백만 데이터베이스 규모에서는 장애가 일상이고,
데이터베이스 문제로 시작한 일이 전 세계 운영 문제가 되었다고 썼다.
저장소 코드만으로 이 운영을 다시 만드는 일은
별개의 과제라는 것이 이 노트의 판단이다.
반면 데이터 자체에 대한 종속은 약하다.
컴퓨트는 표준 Postgres이므로 `pg_dump`와 `pg_restore`,
논리 복제로 다른 Postgres에 옮길 수 있다.
종속은 데이터가 아니라
브랜치 기반 개발 흐름과 scale to zero에 맞춘 비용 구조에 생긴다.
떠나는 순간 다른 관리형 Postgres에서는 이 둘을 다시 만들어야 한다.

### 고가용성은 아직 Databricks 쪽에만 있다

Neon 문서의 Neon과 Lakebase 비교표에서 고가용성은 Neon에서 곧 제공 예정이고,
Databricks에서는 제공된다.
교차 클라우드 재해 복구도 Neon에는 없고 Databricks에는 비공개 프리뷰로 있다.
스토리지는 모든 플랜에서 다중 AZ이고,
컴퓨트가 죽으면 새 컴퓨트가 같은 이력에 붙는다.
다만 고가용성이 아직 없다는 것은 컴퓨트 장애 때 미리 준비된 대기 컴퓨트로
넘어가는 구성이 Neon 쪽에는 없다는 뜻으로 읽힌다.
같은 데이터베이스 엔진이라도
어느 회사 콘솔에서 쓰느냐에 따라 운영 보장이 다르다.

Neon은 2026년 9월 블로그 글에서 그해 초 한 주에 두 번,
외부 의존성 장애가 자기 강화 루프를 일으켜 컨트롤 플레인을 무너뜨렸고,
이후 석 달 동안 30건 넘는 후속 수정을 했다고 밝혔다.
컨트롤 플레인이 멈추면 데이터베이스 생성뿐 아니라 잠든 컴퓨트를 깨우는 일도
실패할 수 있다고 같은 글은 설명한다.
scale to zero를 쓰는 데이터베이스는
매번 깨어날 때 컨트롤 플레인에 기대는 셈이다.

## 함정

- Unlogged 테이블은 WAL을 쓰지 않으므로 컴퓨트 로컬 저장소에만 있고, 재시작이나 scale to zero 때 사라진다.
  일반 Postgres에서는 비정상 종료 때만 비워지는 것과 다르다.
- 임시 테이블, 세션 파라미터, prepared statement, advisory lock, `LISTEN` 등록은 유휴 연결이 닫히면 함께 사라진다.
- 풀링 연결에서 `SET search_path`를 쓰면 다음 트랜잭션에서 다른 서버 연결로 넘어가 `relation does not exist`가 난다.
  스키마를 명시하거나 `ALTER ROLE ... SET search_path`로 역할 수준에 둔다.
- `pg_dump`는 `SET`을 쓰므로 풀링 연결로 돌리면 안 된다.
- Neon에서 논리 복제의 발행자가 되면 구독자가 연결된 동안 컴퓨트가 잠들지 않아 비용이 계속 나간다.
- 오토스케일링 범위를 0.25~4 CU로 잡아도 `max_connections`는 2 CU 기준이다. 최솟값이 연결 한도를 정한다.
- 스토리지가 copy-on-write여도 VACUUM은 여전히 필요하다.
  공동 창업자 hlinnaka는 VACUUM 일부를 스토리지 계층으로 내리려면 Postgres 코드를 깊게 고쳐야 해서 피한다고 답했다.[^hlinnaka]
- 슈퍼유저가 없고 `neon_superuser` 역할만 있다. SQL로 만든 역할은 이 역할의 구성원이 아니므로 권한을 따로 줘야 한다.
- 테이블스페이스와 `track_commit_timestamp`는 지원하지 않는다. 인스턴스 수준 파라미터는 바꿀 수 없다.
- 보호 브랜치에서 자식 브랜치를 만들면 자식의 역할 비밀번호가 바뀐다. 부모 비밀번호를 그대로 쓰는 스크립트는 실패한다.
- Postgres 로그는 Scale 플랜의 Datadog이나 OpenTelemetry 연동으로만 받는다.
  2024년 HN 스레드에서 Neon의 tristan957은 Neon이 호스팅이 아닌 관리형 서비스라 로그를 노출하지 않으며 나중에 하고 싶다고 답했다.[^tristan957]
- Free 플랜은 전송량 5GB를 넘기면 컴퓨트가 멈춘다. 데이터는 그대로지만 앱은 다음 청구 주기까지 연결하지 못한다.
- Vercel-Managed Integration으로 가입한 계정은 `neon login`을 쓸 수 없고 API 키로 인증해야 한다.

## 확인하기

아래 절차도 문서를 바탕으로 구성했고 직접 실행하지는 않았다.
`PROJECT_ID`는 프로젝트 설정 화면이나 `neon projects list`에서,
`ENDPOINT_ID`는 Console의 브랜치 페이지에서 확인한다.
`$URL`에는 이미 쿼리 파라미터가 붙어 있으므로 2번은 `&`로 파라미터를 덧붙인다.

```bash
# 1. 콜드 스타트 측정: 컴퓨트를 강제로 재운 뒤 첫 쿼리 시간을 잰다
curl -s -X POST \
  -H "Authorization: Bearer $NEON_API_KEY" \
  "https://console.neon.tech/api/v2/projects/$PROJECT_ID/endpoints/$ENDPOINT_ID/suspend"
URL=$(neon connection-string)
time psql "$URL" -c "SELECT 1"    # 잠든 상태에서 첫 연결
time psql "$URL" -c "SELECT 1"    # 깨어난 뒤 비교값

# 2. PostgreSQL 17 이상 클라이언트라면 SSL 협상 왕복을 줄여 다시 잰다
time psql "$URL&sslnegotiation=direct" -c "SELECT 1"

# 3. 연결 한도 확인: 오토스케일링 범위가 연결 수를 어떻게 정했는지 본다
psql "$URL" -c "SHOW max_connections"

# 4. 풀링과 세션 상태: 두 번째 SELECT가 실패하면 트랜잭션 모드 제약이 재현된 것이다
POOLED=$(neon connection-string --pooled)
psql "$POOLED" -c "CREATE SCHEMA IF NOT EXISTS s; CREATE TABLE IF NOT EXISTS s.t(x int)"
psql "$POOLED" <<'SQL'
SET search_path TO s;
SELECT * FROM t;
SQL

# 5. 브랜치 격리: 브랜치에서 쓴 행이 부모에 보이지 않아야 한다
neon branches create --name iso-test
neon psql iso-test -- -c "INSERT INTO s.t VALUES (1)"
neon psql -- -c "SELECT count(*) FROM s.t"    # 0이어야 한다
neon branches delete iso-test
```

4번의 heredoc은 `psql`이 한 연결에서 문장을 차례로 보내므로 성공할 수도 있다.
제약을 확실히 보려면 애플리케이션 드라이버의 풀에서 `SET`과 쿼리를 다른
트랜잭션으로 나눠 보내 본다.

측정할 값은 세 가지다.
잠든 상태의 첫 연결 시간과 깨어난 뒤 시간의 차이가 콜드 스타트이고,
깨어난 뒤 시간 자체는 지역 간 거리와 TLS 협상 비용이며,
첫 몇 번의 무거운 쿼리가 이후보다 느리다면
캐시가 빈 컴퓨트가 Pageserver를 거치는 비용이다.
Lobste.rs의 cmcaine은 서버리스라는 말을 SQLite 같은 임베디드 데이터베이스로
읽었다가 또 하나의 DBaaS였다고 적었는데,[^cmcaine]
이 측정은 그 서버리스가 무엇을 뜻하는지,
즉 연결 너머에서 컴퓨트가 켜지고 꺼지는 데 드는 시간을 숫자로 보여 준다.

---

[^kelvich]: <https://news.ycombinator.com/item?id=31538825>

[^nikita-branch]: <https://news.ycombinator.com/item?id=31538221>

[^nikita]: <https://news.ycombinator.com/item?id=31538133>

[^hadlock]: <https://news.ycombinator.com/item?id=41185522>

[^ok_dad]: <https://news.ycombinator.com/item?id=41185487>

[^nikita-selfhost]: <https://news.ycombinator.com/item?id=31538408>

[^hlinnaka]: <https://news.ycombinator.com/item?id=31538542>

[^tristan957]: <https://news.ycombinator.com/item?id=41185596>

[^cmcaine]: <https://lobste.rs/s/2sxjo2/neon_serverless_fault_tolerant#c_atxs0e>
