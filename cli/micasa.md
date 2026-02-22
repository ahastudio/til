# micasa

> Your house is quietly plotting to break while you sleep

홈 유지보수·프로젝트·가전제품을 관리하는 터미널 TUI 앱.

- 사이트: <https://micasa.dev/>
- 저장소: <https://github.com/cpcloud/micasa>

---

## 개요

SQLite 단일 파일에 모든 데이터를 저장하는 로컬 퍼스트(local-first) 홈 관리 도구다.
클라우드, 계정, 구독 없이 `cp` 명령 하나로 전체 백업이 가능하다.

**관리 대상**

| 영역 | 기능 |
|------|------|
| 유지보수 | 자동 계산 만기일, 서비스 이력 |
| 프로젝트 | 계획→완료 전 단계 추적, 예산/실제 비용 |
| 가전제품 | 구매일, 보증 만료, 유지보수 일정 |
| 업체 관리 | 연락처, 견적 이력, 작업 기록 |
| 사건(Incident) | 누수 등 문제 심각도·상태 기록 |
| 파일 첨부 | 매뉴얼·영수증·사진을 DB BLOB으로 직접 저장 |

---

## 기술 스택

```
Pure Go (1.25+) + zero CGO
Charmbracelet (Bubble Tea, Lip Gloss, Bubbles)
GORM + SQLite
Nix (개발 환경 재현)
```

CGO를 전혀 사용하지 않아 Linux / macOS / Windows, amd64 / arm64에서
단일 바이너리로 배포된다.

---

## 아키텍처 인사이트

### 1. 단일 SQLite 파일 모델

모든 애플리케이션 데이터—관계형 레코드, 파일 첨부(BLOB), 설정—를
SQLite 파일 하나에 넣는다.

```go
// store.go - SQLite PRAGMA 설정
db, err := gorm.Open(
    sqlite.Open(path,
        "PRAGMA foreign_keys = ON",   // 참조 무결성 강제
        "PRAGMA journal_mode = WAL",  // WAL 모드로 읽기 동시성 확보
        "PRAGMA synchronous = NORMAL",
        "PRAGMA busy_timeout = 5000",
    ),
    &gorm.Config{Logger: logger.Default.LogMode(logger.Silent)},
)
```

- `WAL` 모드: 읽기가 쓰기를 차단하지 않아 TUI 반응성 유지
- `busy_timeout = 5000`: 잠금 충돌 시 5초 대기 후 오류
- `foreign_keys = ON`: GORM 레벨이 아닌 DB 레벨에서 무결성 보장

### 2. 소프트 삭제 + Undo 패턴

삭제된 레코드를 `DeletionRecord` 감사 테이블에 기록하고,
Unscoped 프리로드로 삭제된 부모를 함께 조회해 UI에 표시한다.

```go
// 삭제된 부모 엔티티도 함께 조회
Preload("Vendor", func(q *gorm.DB) *gorm.DB {
    return q.Unscoped()
})
```

이 방식으로 `undo` 기능을 구현한다. 복원 시 엔티티와 삭제 로그를 트랜잭션으로 원자적 업데이트.

### 3. 다형성(Polymorphic) 문서 첨부

`Document` 모델이 `(entity_kind, entity_id)` 복합 키로 어느 엔티티에든 연결된다.

```
Document
├── entity_kind: "Project" | "Appliance" | "Vendor" | ...
├── entity_id:   uint
└── data:        []byte (BLOB)
```

이 패턴 덕분에 별도 첨부 테이블 없이 모든 도메인 객체에 파일을 붙일 수 있다.

---

## 로컬 LLM 통합 — 2단계 파이프라인

`@` 키를 눌러 자연어로 데이터를 질문하면 Ollama(또는 OpenAI 호환 API)와 통신한다.
쿼리 실행과 결과 요약이 모두 로컬 머신에서 이루어진다.

```
사용자 자연어 입력
       │
       ▼
[Stage 1] NL → SQL 생성 (BuildSQLPrompt)
  - 스키마·테이블 구조를 컨텍스트로 제공
  - SELECT 전용, 소프트 삭제 레코드 필터 규칙 명시
  - 금액 컬럼은 센트 단위임을 안내
       │
       ▼
SQL 실행 (GORM Raw Query)
       │
       ▼
[Stage 2] 결과 → 자연어 요약 (BuildSummaryPrompt)
  - 파이프 구분 텍스트 테이블을 컨텍스트로 제공
  - 결과를 사람이 읽기 좋은 문장으로 변환
       │
       ▼
스트리밍 응답 → 채팅 뷰포트 렌더링
```

**슬래시 커맨드**: `/models`, `/model <name>`, `/sql`, `/help`
`/sql`은 마지막으로 생성된 SQL 쿼리를 채팅창에 표시하는 디버그 용도.

### LLM 클라이언트 설계

```go
type Client struct {
    baseURL   string  // OpenAI 호환 엔드포인트
    model     string
    timeout   time.Duration
    http      *http.Client
}
```

Ollama 네이티브 API 엔드포인트는 OpenAI 호환 URL에서 `/v1`을 제거해 파생한다.
스트리밍은 SSE(Server-Sent Events) 파싱으로 처리하고, 컨텍스트 취소를 지원한다.

---

## SQL 포매터 (자체 구현)

LLM이 생성한 SQL을 사람이 읽기 좋게 포맷하는 코드를 직접 작성했다.
외부 라이브러리 없이 3단계 파이프라인으로 구현:

```
토큰화 → 절(clause) 감지 및 계층 구성 → 레이아웃 엔진
```

- `SELECT`, `FROM`, `WHERE` 등 최상위 절은 컬럼 0에서 시작
- `AND`, `OR` 등 연속 토큰은 추가 들여쓰기
- `ORDER BY`, `LEFT JOIN` 같은 복합 키워드를 단일 단위로 처리
- `maxWidth` 초과 시 공백 경계에서 소프트 랩

---

## 모달 TUI 인터페이스

VisiData에서 영감을 받아 Vim 스타일 모달 내비게이션을 구현했다.

| 모드 | 설명 |
|------|------|
| `nav` | 테이블 탐색, 컬럼 정렬, 퍼지 검색 |
| `edit` | 레코드 추가·수정 (인라인 폼) |

**폼 검증**은 DB 레이어가 아닌 TUI 레이어에서 실시간으로 수행되어
잘못된 입력을 즉시 피드백한다.

---

## 색상 시스템 — 색맹 접근성

[Wong 컬러 팔레트](https://www.nature.com/articles/nmeth.1618)를 채택해
색맹 사용자도 구분할 수 있는 색상 체계를 사용한다.

```go
// 다크/라이트 터미널 모두 대응
var Primary = lipgloss.AdaptiveColor{
    Dark:  "#56B4E9",  // Sky Blue
    Light: "#0072B2",
}
var Success = lipgloss.AdaptiveColor{
    Dark:  "#009E73",  // Bluish Green
    Light: "#007A5A",
}
var Warning = lipgloss.AdaptiveColor{
    Dark:  "#F0E442",  // Yellow
    Light: "#B8860B",
}
var Error = lipgloss.AdaptiveColor{
    Dark:  "#D55E00",  // Vermillion
    Light: "#CC3311",
}
```

`lipgloss.AdaptiveColor`로 다크/라이트 터미널 배경에 자동 대응한다.

---

## 도메인 모델 설계

홈 관리 도메인을 Go 구조체로 표현한 방식이 깔끔하다.

```go
// 금액은 모두 센트 단위 정수로 저장 (부동소수점 오류 방지)
type Project struct {
    Title      string
    Status     ProjectStatus  // ideating | planned | quoted | underway | delayed | completed | abandoned
    Budget     int64          // cents
    ActualCost int64          // cents
}

// 유지보수 일정: 마지막 서비스일 + 주기(월)로 다음 만기일 자동 계산
type MaintenanceItem struct {
    LastServiced  time.Time
    IntervalMonths int
}

// 사건 심각도
type Severity string
const (
    Urgent   Severity = "urgent"    // 즉시 조치 필요
    Soon     Severity = "soon"      // 조만간 처리
    Whenever Severity = "whenever"  // 여유 있을 때
)
```

**금액을 센트 정수로 저장**하는 패턴은 부동소수점 정밀도 문제를 원천 차단한다.

---

## 개발 방식 — AI 에이전트로 개발한 앱

micasa는 **Claude Code로 개발한 프로젝트**임을 명시한다.
`AGENTS.md`에서 코딩 에이전트 운용 철학을 확인할 수 있다.

- 에이전트가 자율 스태프 엔지니어처럼 컨텍스트를 스스로 수집해 작업 완료
- `/resume-work` 슬래시 커맨드로 세션 간 컨텍스트 인계
- `golangci-lint` + `staticcheck` + `golines` 통과 후 커밋 (--no-verify 금지)
- 회귀 테스트는 수정 없이 실행하면 반드시 실패해야 함

이 프로젝트 자체가 "AI 에이전트가 실제 업무용 도구를 어느 수준까지 만들 수 있는가"의 증거다.

---

## 참고

- [Charmbracelet / Bubble Tea](https://github.com/charmbracelet/bubbletea) — Go TUI 프레임워크
- [VisiData](https://www.visidata.org/) — 모달 TUI 인터페이스 영감
- [Wong Color Palette](https://www.nature.com/articles/nmeth.1618) — 색맹 접근성 색상 체계
- [GORM](https://gorm.io/) — Go ORM
