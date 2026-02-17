# go fix

Go 코드를 최신 관용구(idiom)와 API로 자동 변환해 주는
도구. Go 1.26에서 `go vet`과 같은 분석 프레임워크 기반으로
완전히 재작성되었다.

- <https://go.dev/blog/gofix>
- <https://go.dev/blog/introducing-gofix>

## 배경: 원래의 gofix (2011)

Russ Cox가 만든 원래의 `gofix`는 Go 릴리스마다
변경되는 API를 자동으로 마이그레이션해 주는 도구였다.
Go의 AST 파싱/출력 라이브러리 덕분에 `gofmt` 포맷을
유지하면서 기계적 변환이 가능했다.

```bash
# 원래 사용법
gofix .
```

## Go 1.26의 새로운 go fix

Go 1.26에서 `go fix`가 `go vet`과 동일한
분석(analysis) 프레임워크 위에 재구축되었다.
목적은 다르지만 인프라를 공유한다.

- `go vet`: 버그 가능성이 있는 코드 탐지
- `go fix`: 최신 언어/라이브러리 기능으로 현대화

```bash
# 모든 분석기 적용
go fix ./...

# 변경 사항을 diff로 미리 확인
go fix -diff ./...

# 특정 분석기만 실행
go fix -minmax -rangeint ./...

# 특정 분석기 제외
go fix -minmax=false ./...
```

## 주요 분석기 목록

| 분석기           | 설명                             |
|------------------|----------------------------------|
| minmax           | min/max 빌트인 함수 활용         |
| rangeint         | range over int 활용 (Go 1.22)    |
| slicescontains   | slices.Contains 활용             |
| slicessort       | slices.Sort 활용                 |
| stringscut       | strings.Cut 활용                 |
| stringsbuilder   | strings.Builder 활용             |
| fmtappendf       | fmt.Appendf 활용                 |
| forvar           | for 변수 캡처 수정 (Go 1.22)     |
| any              | interface{} → any 변환           |
| waitgroup        | sync.WaitGroup 패턴 개선         |
| inline           | //go:fix inline 지시어 처리      |

## //go:fix inline - 핵심 기능

라이브러리 관리자가 **자신의 API 마이그레이션을
자동화**할 수 있는 메커니즘. 함수나 상수에
`//go:fix inline` 주석을 달면 `go fix` 실행 시
호출부가 자동으로 인라인된다.

### 함수 마이그레이션 예시

```go
// Deprecated: Use Pow(x, 2) instead.
//
//go:fix inline
func Square(x int) int { return Pow(x, 2) }
```

사용자가 `go fix`를 실행하면:

```go
// Before
result := Square(n)

// After
result := Pow(n, 2)
```

### 패키지 이동 예시

```go
// Deprecated: Use pkg2.F instead.
//
//go:fix inline
func F() { pkg2.F(nil) }
```

```go
// Before
pkg.F()

// After
pkg2.F(nil)
```

### 상수 마이그레이션

```go
// Deprecated: Use MaxSize instead.
//
//go:fix inline
const OldMaxSize = MaxSize
```

인라이너는 인자 평가 순서 변경 등 동작 변화가
생길 수 있는 경우 안전하게 변환을 건너뛴다.

## LLM과의 관계

Go 팀이 `go fix`를 현대화한 동기 중 하나가
LLM 코딩 어시스턴트다.

> LLM은 학습 데이터에 있는 오래된 스타일의
> Go 코드를 생성하는 경향이 있고, "최신 관용구를
> 사용하라"고 지시해도 잘 따르지 않는다.

오픈소스 Go 코드 전체를 현대화하면 미래의 LLM
학습 데이터 품질이 개선되는 효과를 기대한다.

## gopls 연동

`go fix`의 분석기들은 gopls(언어 서버)에서도
실시간으로 동작한다.

- 에디터에서 타이핑할 때마다 현대화 제안 표시
- gopls의 MCP 서버를 통해 LLM 코딩 에이전트에도
  진단 정보 제공 ("가드레일" 역할)

## 활용 인사이트

### 1. CI에 go fix -diff 통합

```bash
# CI에서 현대화되지 않은 코드 감지
diff=$(go fix -diff ./...)
if [ -n "$diff" ]; then
  echo "Run 'go fix ./...' to modernize code"
  exit 1
fi
```

### 2. 라이브러리 메이저 버전 업그레이드 자동화

v1 → v2 마이그레이션 시 v1의 함수를 v2 래퍼로
만들고 `//go:fix inline`을 붙이면, 사용자가
`go fix`만 실행하면 된다. Breaking change의
부담을 크게 줄일 수 있다.

### 3. 조직 내 코딩 컨벤션 강제

Go 1.27부터는 staticcheck 분석기도 `go fix`에
포함될 예정이다. 향후에는 소스 트리에서 커스텀
분석기를 동적으로 로드하는 "셀프 서비스" 모델도
계획되어 있다.

### 4. 외부 분석기 사용

```bash
# 외부 분석기 설치 후 go fix에서 사용
go install golang.org/x/tools/go/analysis/passes/\
stringintconv/cmd/stringintconv@latest

go fix -fixtool=$(which stringintconv) ./...
```
