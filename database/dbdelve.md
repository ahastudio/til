# DBDelve: Rust로 만든 데이터베이스 클라이언트

<https://dbdelve.github.io/>

<https://github.com/ShayanAbbas1/dbdelve>

Show HN: [Show HN: DBDelve – Open-Source DB Client Made with Rust and GPUI](https://news.ycombinator.com/item?id=50427934) (125점, 50개 댓글)

GN 토론: <https://news.hada.io/topic?id=37236>

## 소개

DBDelve는 여러 엔진을 지원하는 네이티브 크로스 플랫폼 데이터베이스 클라이언트이다.
Rust와 GPUI로 만들었고 Electron과 JVM이 없다고 밝힌다.
저장소는 2026년 8월 17일에 만들어졌고 GPL-3.0이며 Rust이다.
2026년 11월 16일에 읽은 값으로 별 1,474개, 포크 81개, 열린 이슈 35개이고 마지막 변경이 같은 날이다.
앱을 설치하거나 벤치마크를 재현하지는 않았다.

만든 사람은 README에서 성능이 좋고 현대적이며 램을 적게 쓰는 것을 원했고, 기존 DB 클라이언트는 Electron과 JVM으로 부풀었거나 유료라고 쓴다.
어떤 기능도 유료 벽 뒤로 가지 않고 시간이 지나면 기존 도구와 기능이 같아질 것이라고 한다.

저장소가 홈페이지로 등록한 주소는 dbdelve.github.io이다.
읽은 시점(2026년 11월 18일)에 열어
첫 화면 제목이 “DBDelve — a fast, native database client”임을 확인했다.
사이트 본문은 읽지 않았고, 사이트의 설명은 제작자의 주장이다.

## 주요 기능

README가 설명하는 기능은 다음과 같다.

- 지원 엔진: Postgres, MySQL, MariaDB, SQLite, Turso, DuckDB, Snowflake, SQL Server, MongoDB, Redis(와 Valkey, KeyDB, Dragonfly), ClickHouse. ODBC 드라이버가 있는 다른 데이터베이스(Oracle, IBM Db2, SAP HANA, BigQuery 등)는 내장 ODBC 브리지로 닿는다.
- 안전장치: 연결마다 격리하고 제목 표시줄 색을 정할 수 있으며 읽기 전용, 읽기와 쓰기, 전체 권한으로 실행한다. 파괴적인 작업은 확인을 묻고, 셀을 고치면 실행할 `UPDATE`를 먼저 보여 준다.
- 편집기: 스키마를 아는 자동 완성(테이블, 열, `JOIN` 뒤에는 외래 키가 시사하는 조건), 쿼리 계획을 따로 창에 보여 주고 행 수 추정이 크게 틀린 곳을 짚는다.
- 데이터: CSV와 TSV와 JSON에서 행 가져오기(실행 전에 모든 행과 문장을 검토), CSV와 Excel과 Parquet과 JSON 파일을 창에 끌어놓으면 DuckDB에서 메모리로 열어 SQL을 돌릴 수 있고, 열을 숨기거나 고정하며 배치는 재시작해도 남는다.
- 연결: DBeaver와 macOS의 TablePlus에서 저장된 연결(비밀번호와 SSH 설정 포함)을 가져오고, SSH 터널은 자체 구현이 아니라 시스템 `ssh`를 쓰며, AWS SSM 터널과 비밀번호 명령(짧은 수명 토큰, 예: Amazon RDS)을 지원한다.
- 외관과 조작: Catppuccin과 Tokyo Night와 Gruvbox와 Dracula 등 어두운/밝은/유리 테마, Zed와 VS Code 테마 가져오기, 단축키를 모두 다시 지정할 수 있는 키보드 우선 팔레트.
- 개인정보: 무료이고 오픈 소스이며 원격 측정이 없고 스스로 보내는 유일한 요청은 끌 수 있는 업데이트 확인이라고 한다. 진단 로그는 기기에 남고 어디로도 보내지 않는다.

설치는 macOS(Apple Silicon)와 Linux, Windows(x86_64)를 지원한다. macOS 앱은 공증되지 않아 Homebrew cask가 격리 플래그를 지운다고 밝힌다.

벤치마크는 DBDelve 0.3.6과 DBeaver 25.3.1을 같은 Postgres 테이블에서 각 5번 돌린 중앙값이다(2026-10-11, M1 Pro 32GB).

| 항목            | DBDelve | DBeaver |
| --------------- | ------- | ------- |
| 실행            | 1.1초   | 5.2초   |
| 유휴 메모리     | 133MB   | 606MB   |
| 1,000행 쿼리    | 0.21초  | 1.96초  |
| 100만 행 시간   | 56초    | 208초   |
| 100만 행 메모리 | 4.9GB   | 17GB    |

100만 행은 행 제한을 끄고 전체 테이블을 일부러 메모리에 끌어온 경우이다.

## 분석

### 중심 주장은 네이티브 렌더링이 큰 결과 표에서 이득이라는 것이다

README의 서사는 “큰 테이블을 스크롤하다 다른 클라이언트가 멈추거나 한도를 건다”는 문제이다.
GPUI는 Zed 편집기의 GPU 가속 UI 프레임워크이고, 같은 UI 코드로 세 플랫폼에서 네이티브로 도는 것이 선택의 이유이다.
HN의 한 댓글은 이점이 UI 체감 속도에 있는지 물었다. 대부분의 시간은 DB를 기다리는 데 쓰이니 성능이 판매 포인트로 약하다는 것이다.[^mbreese]
만든 사람은 다른 질문에 대한 답에서, 행 목록 속도가 중요하지 않더라도 큰 데이터 집합을 스크롤하고 불러오는 데서 차이가 난다고 보았다고 했다.[^shayan_abbas]
이 구분은 README의 벤치마크 항목(실행 시간, 1,000행, 100만 행)과 맞는다.

### 안전장치가 “운영 DB를 헷갈리지 않게”라는 요구에 맞춘다

연결별 색상과 읽기 전용 모드와 편집 전 `UPDATE` 미리 보기는 DB 클라이언트에서 실수를 줄이는 기능이다.
HN의 한 댓글은 행 목록 속도보다 클릭 한 번으로 할 수 있는가와 데이터를 파괴하지 않는가가 중요하다고 했고, 만든 사람은 파괴적 쿼리에 확인을 두고 편집 때 실행될 쿼리를 보여 준다고 답했다.[^d0100]

## 비평

### 벤치마크의 범위

비교는 한 기기(M1 Pro)와 한 테이블, 한 상대(DBeaver 25.3.1)이다.
상대의 기본 설정을 쓴 것인지, DBeaver의 메모리 설정을 조정했는지는 README 본문에 없다.
100만 행 메모리 4.9GB 대 17GB는 전체를 끌어오도록 한 조건이어서 일상 사용의 수치가 아니다.
GeekNews의 한 사용자는 직접 실행해 보니 거의 1초 만에 나타나고 DBeaver는 5초쯤 걸린다고 했다.[^eususu]
이는 README의 실행 시간(1.1초 대 5.2초)과 같은 방향의 개인 경험이다.
다만 이 사용자는 Oracle까지 지원하면 최고인데 아쉽다고 했고, README는 Oracle을 ODBC 브리지로 닿는다고 적는다.
브리지는 별도 드라이버 설치가 필요하다.

### 기능 격차를 만든 사람도 인정한다

한 댓글이 DBeaver와 기능을 비교해 묻자 만든 사람은 아직 동등하지 않다고 답했다.[^d0100]
또 다른 댓글은 개념 증명처럼 보인다고 했고 AI 쿼리 도우미를 원했으며,[^gmmachine]
답변은 계획에 있지만 핵심 작업 흐름이 먼저이고 매일 쓰는 사람들이 있다는 것이었다.[^shayan_abbas2]
DataGrip의 인텔리센스와 비교하는 질문에는 스키마를 아는 자동 완성이 있지만 DataGrip을 거의 써 보지 않아 정확히 비교할 수 없다는 답이 있었다.[^written-beyond]
README도 기존 도구와 완전한 기능 동등성이 “시간이 지나면” 이뤄진다고 쓴다.

### 생태계의 불확실성

GPUI는 Zed 팀의 크레이트 갱신이 1년 넘게 멈춰 있어 사람들이 각자 배포판(gpui-ce, gpui-pre, gpui-kit 등)을 낸다고 만든 사람이 답했고, 이에 한 댓글은 모두가 자기만의 GPUI 변종을 갖고 있어 “모래 위에 짓는” 느낌이라고 했다.[^edstarch]
이 저장소의 `rust/gpui.md`가 GPUI를 다룬다.
유지 비용에 대한 질문에는 만든 사람이 자발적 후원을 계획이라고 답했다.[^mikenikles]
한 댓글은 비슷한 GPUI 기반 오픈 소스 클라이언트(dbflux)가 이미 있다고 지적했다.[^waterTanuki]
다른 댓글은 dbx(Tauri 기반)와의 차이를 물었다.[^exaroth]

### 호환성 문제와 요청

한 사용자는 WSL 파일 시스템의 `.sqlite` 파일을 Windows에서 열지 못한다고 보고했고 DBeaver도 마찬가지라고 했다.[^olive-n]
다른 사용자는 Postgres 복합 타입 필터링과 편집을 요청했고, 만든 사람은 이미 된다고 했으나 사용자는 익명 타입 입력이 구현되지 않았다는 오류를 확인했다.[^mamcx]

### 코드 생성에 대한 의심

한 댓글은 “모든 것을 Rust로 다시 쓰는 AI 슬롭” 흐름에 지쳤다고 했고,[^edem]
답글들은 이 프로젝트는 슬롭처럼 보이지 않고 DB 클라이언트가 대체로 엉성했다고 했다.[^logdahl]
사이트에 LLM 말투가 가득하다는 지적도 있었다.[^natfan]

## 인사이트

### DB 클라이언트를 고르는 기준

스레드에서 선택 기준은 속도가 아니라 두 가지로 모였다.
지원할 DB(특히 Oracle, SQL Server)와 데이터를 망치지 않는 안전장치이다.
한 사용자는 Oracle과 SQL Server와 Postgres를 모두 쓸 수 있어야 DataGrip을 놓을 수 있다고 했고,[^mrgoldenbrown]
만든 사람은 SQL Server와 Postgres는 기본 지원, Oracle은 ODBC라고 답했다.
도입 전에 본인이 쓰는 엔진의 지원 방식(기본인지 ODBC인지)과 편집 확인 동작을 먼저 확인하는 것이 안전하다. 이는 이 문서의 제안이다.

### 무료 오픈 소스의 지속성 질문은 여전히 열려 있다

“어떤 기능도 유료 벽 뒤로 가지 않는다”는 약속은 후원에 기대고, GPL-3.0이라는 선택과 이전 코드가 MIT였다는 README의 안내가 있다.
한 사용자는 다른 클라이언트가 유료 업그레이드 안내로 성가셔졌다고 했다.[^mariushn]
스레드의 반응에서 이 점이 이 프로젝트의 매력이었음이 보인다. 만든 사람이 스스로 인정하듯 지속성은 앞으로 증명할 일이다.

### 확인할 관찰

이 프로젝트를 평가할 관찰은 세 가지이다.
독립적인 벤치마크가 DBeaver의 설정을 조정한 비교에서도 격차를 확인하는지,
GPUI 배포판 문제가 프로젝트의 유지에 영향을 주는지,
Oracle 같은 ODBC 경유 엔진의 사용성과 기능 동등성이 얼마나 진전되는지이다.

---

[^mbreese]: <https://news.ycombinator.com/item?id=50429820>

[^shayan_abbas]: <https://news.ycombinator.com/item?id=50441665>

[^d0100]: <https://news.ycombinator.com/item?id=50440837>

[^eususu]: <https://news.hada.io/topic?id=37236#cid69927>

[^gmmachine]: <https://news.ycombinator.com/item?id=50433220>

[^shayan_abbas2]: <https://news.ycombinator.com/item?id=50436253>

[^written-beyond]: <https://news.ycombinator.com/item?id=50432528>

[^edstarch]: <https://news.ycombinator.com/item?id=50429762>

[^mikenikles]: <https://news.ycombinator.com/item?id=50429760>

[^waterTanuki]: <https://news.ycombinator.com/item?id=50434278>

[^exaroth]: <https://news.ycombinator.com/item?id=50429547>

[^olive-n]: <https://news.ycombinator.com/item?id=50433026>

[^mamcx]: <https://news.ycombinator.com/item?id=50430837>

[^edem]: <https://news.ycombinator.com/item?id=50430055>

[^logdahl]: <https://news.ycombinator.com/item?id=50430649>

[^natfan]: <https://news.ycombinator.com/item?id=50440690>

[^mrgoldenbrown]: <https://news.ycombinator.com/item?id=50430454>

[^mariushn]: <https://news.ycombinator.com/item?id=50506723>
