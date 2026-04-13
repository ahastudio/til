# pgmicro - SQLite 기반 인-프로세스 PostgreSQL

원문: <https://github.com/glommer/pgmicro>

## 요약

pgmicro는 PostgreSQL SQL을 SQLite 바이트코드로 직접 컴파일하는 임베디드 데이터베이스다.
Turso(Rust로 재작성된 SQLite 구현체)를 엔진으로 사용하면서,
PostgreSQL의 실제 파서(`libpg_query`)를 채택해 100% 구문 호환성을 확보한다.

처리 파이프라인은 다음과 같다:

1. PostgreSQL 파서(`libpg_query`)로 SQL 구문 분석
2. 번역기(`parser_pg/`)가 PostgreSQL 파스 트리를 Turso 내부 AST로 변환
3. Turso 엔진이 AST를 VDBE 바이트코드로 컴파일
4. 표준 SQLite B-tree 포맷과 WAL을 사용해 저장

데이터 파일은 표준 SQLite 3.x `.db` 포맷이므로 기존 SQLite 도구로도 읽을 수 있고,
단일 연결에서 PostgreSQL과 SQLite 구문을 동적으로 전환할 수 있다.
PostgreSQL 와이어 프로토콜 서버를 포함해 `psql` 등 표준 클라이언트 접속도 지원한다.

## 분석

### WebAssembly가 아닌 바이트코드 번역이라는 아키텍처

pgmicro의 핵심 전략은 "PostgreSQL을 임베드하거나 WebAssembly로 컴파일하지 않고,
PostgreSQL 구문을 SQLite 바이트코드로 직접 번역한다"는 것이다.
이는 PGlite 같은 WebAssembly 기반 접근과 근본적으로 다른 아키텍처다.

### Turso 위에 구축한 이유

Turso는 이미 SQLite의 완전한 Rust 재구현체이므로,
커스텀 타입 시스템이나 바이트코드 확장을 엔진 수준에서 지원할 수 있다.
PostgreSQL 타입(`SERIAL`, `::` 캐스팅 등)을 해킹이 아닌 네이티브 기능으로 구현할 수 있는 것이다.

### AI 에이전트 환경이라는 주요 타겟

에이전트가 임시로 사용하는 단명(短命) 데이터베이스,
사용자별 샌드박스, 세션 스토어 등에서
PostgreSQL 구문 호환성과 SQLite의 가벼움을 동시에 얻을 수 있다.

## 비평

### 파싱과 실행의 간극

실험적 프로젝트라는 점이 가장 큰 한계다.
PostgreSQL 구문의 100% 파싱은 가능하지만,
모든 PostgreSQL 기능(윈도우 함수, CTE 고급 활용, 트리거 등)이
SQLite 바이트코드로 완벽히 번역되는지는 별개의 문제다.

### Turso 코어 의존성의 양면성

Turso 코어 변경을 최소화한다는 설계 원칙은
장기적 유지보수에는 유리하지만, 성능 최적화나 고급 기능 구현에 제약이 될 수 있다.
Turso가 활발히 개발 중이므로 머지 충돌 관리도 지속적인 비용이다.

### 와이어 프로토콜의 미완성

와이어 프로토콜 구현도 아직 단순한 수준이라
프로덕션 PostgreSQL 드라이버의 모든 기능(프리페어드 스테이트먼트 캐싱, COPY 프로토콜 등)을
기대하기는 어렵다.

## 인사이트

### 데이터베이스에 적용되는 "파서와 엔진의 분리"

pgmicro는 프론트엔드(파서)와 백엔드(실행 엔진)를 완전히 분리한 컴파일러 아키텍처다.
이는 DuckDB가 다양한 파일 포맷을 읽으면서 자체 실행 엔진을 쓰는 것,
DataFusion이 SQL 파서와 Arrow 기반 실행을 분리한 것과 같은 맥락이다.
데이터베이스가 "모놀리식 시스템"에서 "조합 가능한 컴파일러 파이프라인"으로 진화하고 있다.

### AI 에이전트 시대가 요구하는 데이터베이스의 새로운 폼팩터

기존 데이터베이스는 장수(長壽)하는 서버 프로세스를 전제로 설계되었다.
그러나 AI 에이전트가 작업마다 임시 DB를 생성하고 폐기하는 패턴에서는
기동 시간, 메모리 오버헤드, 배포 복잡성이 핵심 제약이 된다.
pgmicro의 "인-프로세스 + 단일 파일 + PostgreSQL 호환"이라는 조합은
이 새로운 수요에 정확히 대응한다.
GeekNews 댓글에서도 "AI 시대에 만들 생각을 못했다"는 반응이 나온 것이 이 지점이다.

### SQLite의 "만능 기판(基板)" 역할 강화

Turso, Cloudflare D1, LiteFS, Litestream, 그리고 이제 pgmicro까지,
SQLite의 저장 포맷과 실행 엔진 위에 전혀 다른 인터페이스를 올리는 프로젝트가 급증하고 있다.
SQLite가 사실상 "범용 로컬 데이터 엔진"으로서
리눅스 커널이나 LLVM 같은 인프라 레이어의 지위를 얻어가고 있다.
