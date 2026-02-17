# go fix

<https://go.dev/blog/gofix>

Go 1.26에서 `go fix`가 완전히 재작성되었다.
핵심은 **코드 현대화 자동화**와
**라이브러리 마이그레이션 셀프 서비스**.

## 왜 지금 다시 만들었나

LLM이 오래된 Go 관용구로 코드를 생성하고,
"최신 스타일 써라"고 해도 안 고친다.
Go 팀의 해법: **코드 자체를 고쳐서 학습 데이터를
바꾸자.** `go fix`는 그 도구다.

## //go:fix inline이 게임 체인저인 이유

라이브러리 관리자가 Breaking change 없이
API를 마이그레이션할 수 있다.

```go
// Deprecated: Use Pow(x, 2) instead.
//
//go:fix inline
func Square(x int) int { return Pow(x, 2) }
```

사용자는 `go fix ./...`만 실행하면
`Square(n)` → `Pow(n, 2)`로 자동 변환된다.
인자 평가 순서 같은 동작 변화가 생기는 경우는
안전하게 건너뛴다. 패키지 이동, 상수 교체도
같은 패턴으로 처리한다.

**이것이 중요한 이유:**
v1 → v2 마이그레이션 시 v1 함수를 v2 래퍼로
만들고 `//go:fix inline`만 붙이면 된다.
Breaking change의 고통을 구조적으로 제거한다.

## gopls와 결합하면 실시간 가드레일

`go fix` 분석기들이 gopls에서도 동작한다.
에디터에서 코드 작성 중 현대화 제안이 뜨고,
gopls MCP 서버를 통해 LLM 에이전트에도
진단 정보가 흘러간다.

`go fix` + gopls + LLM 에이전트.
이 조합이 Go 코드 품질의 바닥을 끌어올린다.

## CI에 넣어라

```bash
diff=$(go fix -diff ./...)
if [ -n "$diff" ]; then
  echo "Run 'go fix ./...' to modernize"
  exit 1
fi
```

이것 하나로 팀 전체의 코드가 최신 관용구를
유지하게 된다. `go vet`처럼 CI 필수 단계로
넣어야 한다.

## 정리

| 관점               | 핵심                           |
|--------------------|--------------------------------|
| 코드 작성자        | `go fix ./...`로 최신화        |
| 라이브러리 관리자  | `//go:fix inline`으로          |
|                    | 마이그레이션 자동화            |
| 팀 리더            | CI에 `go fix -diff` 통합       |
| LLM 시대           | 학습 데이터 품질을             |
|                    | 도구로 강제 개선               |
