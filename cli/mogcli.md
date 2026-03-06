# mogcli: Microsoft 365 비공식 CLI

> Microsoft Graph API를 통해 메일, 캘린더, 연락처 등을
> 커맨드라인에서 다루는 비공식 Microsoft 365 CLI.
> 에이전트 친화적으로 설계되어 스크립팅에 최적화.

<https://github.com/jaredpalmer/mogcli>

## 설치

```bash
# Homebrew (macOS/Linux)
brew tap jaredpalmer/tap && brew install jaredpalmer/tap/mogcli

# Go로 직접 설치
go install github.com/jaredpalmer/mogcli/cmd/mog@latest

# 소스 빌드
git clone https://github.com/jaredpalmer/mogcli.git
cd mogcli && go build -o bin/mog ./cmd/mog
```

## 인증

```bash
# 대화형 인증 설정
mog auth
```

Microsoft Entra 앱 등록이 선행되어야 한다.
Delegated 모드는 공개 클라이언트 흐름 + Graph 권한 설정,
App-only 모드는 애플리케이션 권한 + 관리자 동의 + 클라이언트
시크릿이 필요하다.

## 지원 워크로드

| 워크로드    | Delegated | App-Only       |
|-------------|-----------|----------------|
| 메일        | ✓         | ✓ (엔터프라이즈) |
| 캘린더      | ✓         | ✗              |
| 연락처      | ✓         | ✓ (엔터프라이즈) |
| Groups      | 엔터프라이즈만 | 엔터프라이즈만 |
| Tasks       | ✓         | ✗              |
| OneDrive    | ✓         | ✓ (엔터프라이즈) |

## 주요 명령어

```bash
# 메일
mog mail list --max 50 --query "from:alerts@example.com"
mog mail send --to user@contoso.com --subject "주제" --body "내용"

# 캘린더
mog calendar list --from 2026-03-01 --to 2026-03-31
mog calendar create --subject "회의" --start "2026-03-10T10:00:00+09:00"

# 연락처
mog contacts list --max 100
mog contacts create --display-name "홍길동" --email "hong@example.com"

# OneDrive
mog onedrive ls --path /
mog onedrive put ./report.pdf --path /Documents/report.pdf
```

## 출력 형식

```bash
# JSON 출력 (파이프라인/스크립팅용)
mog mail list --json

# 일반 텍스트 출력
mog mail list --plain
```

## 코드 분석

### 패키지 구조

`cmd/mog/main.go`는 극도로 얇은 진입점이다.
실질적인 로직은 모두 `internal/` 패키지에 위임된다.

```
cmd/mog/main.go          # 진입점: cmd.Execute(os.Args[1:])
internal/cmd/root.go     # kong 기반 CLI 파싱 및 서브커맨드 등록
internal/services/       # 워크로드별 비즈니스 로직
internal/graph/          # Graph API 클라이언트 (재시도, 서킷브레이커)
internal/auth/           # 인증 흐름 (Delegated, App-Only)
internal/secrets/        # 시스템 키체인 기반 자격증명 저장
```

### `internal/graph/client.go`

Graph API 요청을 처리하는 핵심 HTTP 클라이언트.

- **`TokenProvider` 함수 타입**: OAuth 토큰을 요청마다 동적으로
  획득한다. 토큰 주입 방식을 추상화해 Delegated/App-Only 모드 모두
  동일한 클라이언트로 처리한다.
- **`Do()` / `DoJSON()`**: 재시도와 서킷브레이커를 거쳐 요청을
  실행하는 공개 메서드. `DoJSON()`은 응답 본문을 구조체로
  역직렬화하는 편의 래퍼다.
- **재시도 분기**: 응답 코드에 따라 두 경로로 나뉜다.
  429는 `Retry-After` 헤더 값을 읽어 정확한 대기 시간을 지킨다.
  5xx는 별도 카운터로 지수 백오프를 적용한다.
- **`parseAPIError()`**: Graph API 오류 응답에서 `error.code`와
  `error.message`를 추출한다. 파싱 실패 시 HTTP 상태 텍스트로
  폴백한다.
- **`Paginate()`**: 콜백 함수를 받아 `@odata.nextLink`가 없을 때까지
  페이지를 순회한다. 호출자는 페이지 처리 로직에만 집중할 수 있다.
- **`resolveURL()`**: 상대경로는 BaseURL에 붙이고, 절대 URL은 그대로
  사용한다. OData 쿼리 파라미터를 병합해 최종 URL을 구성한다.

### `internal/graph/circuitbreaker.go`

상태 머신으로 구현된 서킷브레이커.

- 상태: `Closed`(정상) → `Open`(차단) → `HalfOpen`(탐침) → `Closed`
- `sync.Mutex`로 상태 전이를 보호한다. 동시 요청이 몰릴 때
  중복 복구 시도를 차단한다.
- `Open` 상태에서 30초가 지나면 자동으로 `HalfOpen`으로 전환해
  단일 탐침 요청을 허용한다.
- 연속 실패 임계값(`threshold`)과 복구 대기 시간(`timeout`)은
  생성 시 주입받아 테스트 가능성을 높인다.

### `internal/auth/scopes.go`

사용자 입력을 OAuth 스코프로 변환하는 파이프라인.

```
CSV 문자열
  → ParseScopeWorkloadsCSV()   # 쉼표 분리, 공백 제거
  → NormalizeScopeWorkloads()  # 유효성 검증, 중복 제거
  → DelegatedScopesForWorkloads()  # 워크로드 → 스코프 매핑
  → normalizeScopes()          # 기본 스코프 우선 정렬
```

`scopeStringCoversRequiredScopes()`는 이미 부여된 스코프 집합에
필요한 스코프가 모두 포함되는지 대소문자 무관하게 확인한다.
이 함수가 `false`를 반환할 때만 재인증을 요청하는 구조다.

### `internal/auth/manager.go`

인증 생명주기 전반을 관리하는 모듈.

- 토큰 캐시 조회 전 계정 ID를 검증한다. 동일 프로필에 다른 계정이
  로그인된 경우 캐시 히트를 거부해 크로스 테넌트 오용을 차단한다.
- `secureZero([]byte)`: 사용이 끝난 민감 데이터를 0으로 덮어쓴다.
  GC 전에 메모리 덤프가 발생해도 평문 자격증명이 노출되지 않는다.
- OS 키체인(`internal/secrets`)에 리프레시 토큰을 저장한다.
  프로세스 재시작 후에도 재인증 없이 토큰을 재사용한다.

### `internal/cmd/root.go`

CLI 진입점이자 전역 플래그 정의 파일.

- `kong` 라이브러리로 서브커맨드 트리를 구성한다. 플래그 정의가
  구조체 태그에 선언되어 파서와 도움말이 동기화된다.
- panic을 catch해 exit code를 Go 에러값으로 변환한다. 서브프로세스나
  에이전트로 실행될 때 프로세스 종료 없이 오류를 전달할 수 있다.
- `--dry-run` 플래그는 컨텍스트에 주입되어 서비스 계층에서 읽는다.
  쓰기 명령이 실제 변경 없이 수행될 내용을 출력만 한다.

---

## 인사이트

### "에이전트 친화적"이 실제로 의미하는 것

mogcli가 스스로를 "agent-friendly"라 부르는 근거는 세 가지다.

첫째, **안정적인 출력 형식**이다. `--json`은 항상 동일한 스키마를
유지하고, `--plain`은 파싱 가능한 구분자를 보장한다. 에이전트가
자연어 파싱 없이 출력을 소비할 수 있다.

둘째, **프로세스 종료 없는 오류 반환**이다. panic-recovery가 exit code를
Go 에러로 변환하기 때문에 서브프로세스로 실행한 에이전트가 실패 원인을
구조적으로 받아볼 수 있다.

셋째, **`--dry-run`으로 부작용 격리**가 가능하다. 에이전트가 메일 발송
전 내용을 미리 확인하거나, 파일 업로드 전 경로를 검증하는 단계를
명시적으로 분리할 수 있다.

### 재시도 전략의 두 가지 경로 분리

429와 5xx를 같은 재시도 루프로 묶는 구현이 흔하다. mogcli는 이를
의도적으로 분리한다.

429는 서버가 명시한 `Retry-After` 시간을 지켜야 한다. 더 빨리
재시도하면 오히려 차단이 길어진다. 반면 5xx는 서버 측 일시 장애이므로
지수 백오프로 부하를 줄이는 것이 목적이 다르다.

두 경로를 분리하면 각각의 카운터와 전략을 독립적으로 튜닝할 수 있다.
같은 요청이 Rate Limit에 걸린 뒤 서버 오류까지 만나도 카운터가 섞이지
않는다.

### 서킷브레이커가 CLI에서 필요한 이유

서킷브레이커는 보통 서버 사이드 패턴으로 인식된다. CLI에서 쓰는 이유는
자동화 스크립트와 에이전트 루프 때문이다.

사람이 직접 실행하면 서비스 장애 시 몇 번 재시도하다 포기한다.
에이전트 루프는 멈추지 않는다. Graph API가 다운된 상태에서 수백 개의
명령이 연속으로 실패하면 Microsoft가 해당 클라이언트 ID를 차단할 수 있다.
서킷브레이커는 이 상황에서 "스스로 멈추는" 안전장치다.

### Progressive Consent의 UX 함의

전통적인 OAuth 앱은 처음 로그인 시 모든 권한을 한꺼번에 요청한다.
사용자는 어떤 기능이 왜 이 권한을 필요로 하는지 알 수 없다.

`scopes.go`의 파이프라인은 각 명령이 자신에게 필요한 스코프를
선언하고, 현재 토큰이 그 스코프를 이미 포함하는지 확인한 뒤
부족한 경우에만 재인증을 요청한다. `mog mail list`를 처음 실행하면
메일 읽기 권한만 요청한다. 나중에 `mog mail send`를 실행하면 추가로
쓰기 권한을 요청한다.

이 패턴은 최소 권한 원칙을 사용자 경험 수준에서 구현한다.

### `secureZero()`가 방어하는 위협 모델

Go의 GC는 객체가 참조되지 않아도 즉시 해제하지 않는다. 메모리에
평문 자격증명이 잠시 남아있는 창이 존재한다. 이 창에서 다음이
가능하다.

- `/proc/[pid]/mem` 읽기 (Linux, root 권한)
- 코어 덤프 파일 분석
- 메모리 포렌식

`secureZero()`는 사용이 끝난 직후 해당 슬라이스를 0으로 덮어써
이 창을 최소화한다. 완벽한 방어는 아니지만(CPU 레지스터, 스택
복사본은 제어 불가) 가장 오래 남는 힙 객체를 대상으로 한다는 점에서
합리적인 트레이드오프다.
