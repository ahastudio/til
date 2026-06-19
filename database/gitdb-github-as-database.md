# GitDB: GitHub 저장소를 서버리스 RDB처럼 사용하기

<https://github.com/3x-haust/gitdb>

Show GN: [GitHub 저장소를 서버리스 RDB처럼 쓰는 GitDB를 만들었습니다 | GeekNews](https://news.hada.io/topic?id=30608)

## 소개

GitDB는 GitHub 저장소를 백엔드로 사용하는 TypeScript 라이브러리다.
데이터베이스 서버 없이 GitHub 저장소 하나만으로
데이터를 저장하고 관리할 수 있다.
브라우저 확장 프로그램, 정적 앱, AI 에이전트, 서버리스 도구처럼
저빈도 쓰기 작업에 단순한 영구 저장소가 필요한 경우를 겨냥한다.

## 아키텍처

데이터는 GitHub 저장소에 세 계층으로 저장된다.

- **매니페스트(manifest)**: 어느 로그 세그먼트까지 재생할지를 기록하는 경계
- **뮤테이션 로그(mutation log)**: 모든 변경 사항을 순서대로 기록한 JSON 또는 암호화 파일
- **스냅샷(snapshot, 선택)**: 빠른 조회를 위한 평문 스냅샷

평문 모드에서의 저장소 구조는 아래와 같다.

```text
gitdb/v1/
  manifest.json
  log/
    00000000000000000001.json
    00000000000000000002.json
```

암호화 모드에서는 `.json` 대신 `.enc` 파일로 저장된다.

## 사용법

```javascript
import { defineTable, GitDb, GitHubFetchPlaintextStore } from "@3xhaust/gitdb/browser"
import { z } from "zod"

const TodoRow = z.object({
  id: z.string(),
  title: z.string(),
  done: z.boolean(),
})

const Todo = defineTable({
  columns: { done: "BOOLEAN", id: "STRING", title: "STRING" },
  indexes: [{ columns: ["done"], name: "todos_done_idx" }],
  name: "todos",
  primaryKey: "id",
  row: TodoRow,
})

const db = await GitDb.open({
  store: new GitHubFetchPlaintextStore({
    branch: "main",
    owner: "your-github-user",
    prefix: "gitdb/v1",
    repo: "my-extension-db",
    token: userProvidedGithubToken,
  }),
  syncSchema: true,
  tables: [Todo],
})

await todos.upsert({ done: false, id: "t1", title: "Ship extension sync" })
const openTodos = await todos.select({ done: false })
```

암호화 모드는 `GitHubFetchEncryptedStore`와 `createWebAesGcmCipher`를 사용하며
AES-GCM 방식으로 파일을 저장한다.

## 주요 기능

- **테이블 API**: `insert`, `upsert`, `select`, `deleteWhere`
- **SQL 엔진**: `SELECT`, `JOIN`, `GROUP BY`, 집계 함수
- **인덱스 기반 검색**
- **트랜잭션 처리**
- **단일 작성자 동시성 모델** — 브랜치 충돌 시 자동 재시도
- **로컬 개발용 `LocalPlaintextStore`** — GitHub 없이 로컬 파일로 테스트 가능

## CLI

```bash
gitdb keygen                        # 암호화 키 생성
gitdb check                         # 저장소 설정 검증
gitdb query "SELECT * FROM todos"   # SQL 실행
```

## 분석

### Git 커밋을 내구성 있는 로그로 쓰는 설계의 논리

GitDB의 핵심 아이디어는 Git의 불변 커밋 이력을 뮤테이션 로그로 재활용한다는 것이다.
기존 데이터베이스가 WAL(Write-Ahead Log)로 복구 가능성을 보장하듯,
GitDB는 GitHub 커밋을 WAL처럼 쓴다.
매니페스트가 "어디까지 재생했는가"를 기록함으로써
로그 파일이 고아 상태가 되더라도 데이터 일관성을 유지할 수 있다.

이 설계는 GitHub의 비강제 ref 업데이트(non-force ref update)를 충돌 방지 메커니즘으로 활용한다.
자체 분산 합의 알고리즘 없이 GitHub의 낙관적 동시성 제어를 빌려온 셈이다.

### 평문 저장의 운영 이점

기본 모드가 암호화가 아닌 평문이라는 점은 의도적 선택이다.
코드 리뷰 도구로 데이터 변경 이력을 검토할 수 있고,
Git blame으로 특정 레코드가 언제 어떻게 바뀌었는지 추적할 수 있다.
"데이터베이스 변경 이력이 PR에 포함되는" 워크플로가 가능해진다.

## 비평

### 단일 작성자 모델이 실제 사용 가능 범위를 크게 좁힌다

GitDB는 단일 작성자 인스턴스를 전제한다.
여러 사용자가 동시에 쓰는 멀티 라이터 환경은 지원하지 않는다.
GitHub API의 요청 제한과 레이턴시도 근본적인 제약이다.
공식 문서 역시 고처리량 OLTP, 실시간 멀티 유저 환경, 저지연이 필요한 경우는
명시적으로 부적합하다고 밝힌다.

이 제약들은 곧 사용 가능한 실제 시나리오를 상당히 좁힌다.
"브라우저 확장 프로그램의 사용자별 설정 동기화"처럼 정말 단일 사용자·저빈도인 경우에만 합리적이다.
팀 단위 도구나 공유 데이터를 다루는 앱에는 적합하지 않다.

### 토큰 관리가 사용자에게 전가된다

브라우저 환경에서 동작하려면 GitHub Personal Access Token이 필요하다.
클라이언트 측에서 토큰을 어떻게 안전하게 보관할지는 사용자 책임이다.
확장 프로그램이 토큰을 잘못 저장하면 저장소 전체에 대한 쓰기 권한이 노출된다.
문서는 이 보안 고려사항을 상세히 다루지 않는다.

## 인사이트

### "GitHub을 인프라로 쓴다"는 발상이 만드는 가능성과 한계

GitDB는 GitHub을 무료 호스팅 인프라로 사용한다는 점에서
GitHub Pages, GitHub Actions를 정적 서버로 활용하는 패턴과 같은 계보다.
백엔드 없이 지속 가능한 데이터 저장소를 원하는 개발자에게
GitHub는 이미 세계 최대의 무료 분산 스토리지다.

이 패턴의 천장은 GitHub의 정책과 요청 제한이다.
GitHub이 이런 용도를 명시적으로 금지하거나 요금을 부과하면
GitDB 위에 구축된 모든 것이 흔들린다.
"GitHub을 DB로 쓴다"는 발상은 영리하지만,
그 영리함의 기반이 타사 플랫폼의 암묵적 허용 위에 있다는 것이 구조적 약점이다.

### AI 에이전트의 경량 영구 저장소로서의 가능성

GitDB가 명시적으로 언급한 사용 사례 중 "AI 에이전트의 관계형 데이터"는 흥미롭다.
에이전트가 실행 결과, 메모리, 태스크 상태를 저장할 때
별도 데이터베이스 서버 없이 GitHub 저장소에 커밋하는 방식은
설정이 단순하고 이력이 자동으로 남는다는 이점이 있다.
에이전트 실행의 감사 추적(audit trail)이 Git 이력과 동일해지는 것은 운영 편의성 측면에서 가치가 있다.
