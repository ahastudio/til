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

## 코드 분석 인사이트

### 아키텍처

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

### Graph API 클라이언트 설계

`internal/graph/client.go`는 프로덕션급 HTTP 클라이언트 패턴을
구현한다.

- **재시도 로직 분리**: 429(Rate Limit)와 5xx(서버 오류)를 별도로
  처리하여 백오프 전략을 각각 적용한다.
- **서킷브레이커 통합**: 5번 연속 실패 시 회로를 열고 30초 후
  자동 복구를 시도한다. `circuitbreaker.go`에서 뮤텍스로 보호되는
  상태 머신으로 구현된다.
- **페이지네이션 추상화**: `Paginate()` 메서드로 `@odata.nextLink`
  기반 페이지 탐색을 투명하게 처리한다.

### 인증 보안 설계

`internal/auth/manager.go`에서 주목할 만한 패턴:

- **`secureZero()`**: 민감한 바이트 슬라이스를 사용 후 즉시 덮어써
  메모리 덤프를 통한 자격증명 유출을 방지한다.
- **계정 검증**: 캐시된 토큰 사용 전 계정 ID 일치 여부를 확인하여
  크로스 테넌트 토큰 오용을 차단한다.
- **시스템 키체인 저장**: OS 네이티브 시크릿 저장소를 활용한다.

### 스코프 관리

`internal/auth/scopes.go`는 사용자 입력 → OAuth 스코프의 파이프라인:

1. CSV 파싱 → 워크로드명 정규화 → 중복 제거
2. 워크로드 → OAuth 스코프 매핑
3. 기본 스코프 우선, 추가 스코프는 알파벳 정렬

Progressive Consent 구현에 핵심적인 모듈로, 명령별로 필요한 스코프만
요청하는 구조를 가능하게 한다.

### CLI 파싱: kong 라이브러리

`root.go`는 `kong` 라이브러리로 CLI를 구성한다.
panic-recovery 메커니즘으로 프로세스 강제 종료 없이 exit code를
Go 에러값으로 변환한다. 에이전트 환경에서 안전한 오류 처리를
가능하게 하는 설계다.
