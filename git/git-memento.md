# git-memento: AI 코딩 세션을 커밋에 기록하는 Git 확장

<https://github.com/mandel-macaque/memento>

## 한 줄 요약

AI 코딩 도구(Codex, Claude Code 등)의 대화 세션을
`git notes`로 커밋에 첨부하는 Git 확장 도구.

## 왜 필요한가

AI 코딩 도구가 보편화되면서 새로운 문제가 등장했다.
커밋 메시지만으로는 "AI와 어떤 대화를 거쳐 이 코드가
나왔는지" 알 수 없다. `git blame`으로 누가 작성했는지는
추적할 수 있지만, AI가 개입한 맥락은 사라진다.

git-memento는 이 빈틈을 메운다. 커밋할 때 AI 세션
히스토리를 자동으로 가져와 `git notes`에 마크다운
형태로 저장한다. 기존 Git 워크플로우를 건드리지 않으면서
AI 협업의 추적성(traceability)을 확보하는 접근이다.

## 핵심 설계 결정

### git notes를 저장소로 선택한 이유

커밋 메시지 본문에 세션을 넣으면 로그가 오염된다.
별도 파일로 관리하면 저장소가 비대해진다.
`git notes`는 커밋 객체에 메타데이터를 덧붙이되
커밋 해시를 변경하지 않는다. 기존 워크플로우와
충돌 없이 부가 정보를 관리할 수 있는 유일한 Git
내장 메커니즘이다.

단, `git notes`는 잘 알려지지 않은 기능이라
팀 도입 시 학습 비용이 있고, `git push`로는
자동 전파되지 않아 별도 동기화가 필요하다.
git-memento는 `share-notes`, `push`,
`notes-sync` 명령으로 이 문제를 해결한다.

### Provider 추상화 아키텍처

```fsharp
type IAiSessionProvider =
    abstract member Name: string
    abstract member GetSessionAsync:
        sessionId: string
        -> Task<Result<SessionData, string>>
    abstract member ListSessionsAsync:
        unit
        -> Task<Result<SessionRef list, string>>
```

AI 도구별 세션 조회 방식을 `IAiSessionProvider`
인터페이스로 추상화했다. 실제 구현체인
`CliJsonProvider`는 외부 CLI를 호출해 JSON을
파싱하는 단일 클래스로, Codex든 Claude든
실행 파일명과 인자만 바꾸면 동작한다.

이 설계의 핵심 인사이트: AI 도구들의 세션 데이터
형식은 다르지만, "세션 ID로 대화를 가져온다"는
인터랙션 패턴은 동일하다. 이 공통 패턴을 인터페이스
경계로 잡은 것이 확장성의 기반이다.

### F#과 Railway-Oriented Programming

코드베이스 전체가 F#의 `Result<'T, string>`
타입으로 에러를 전파한다. 예를 들어 커밋
워크플로우는 다음 단계를 거친다:

1. 저장소 확인 → 실패 시 즉시 반환
2. 커미터 별칭 조회
3. AI 세션 가져오기 → 실패 시 세션 목록 표시
4. 마크다운 렌더링
5. `git commit` 실행
6. HEAD 해시 조회
7. `git notes add` 실행

각 단계가 `match ... with | Error → | Ok →`로
연쇄되어 있어, 어디서 실패하든 깔끔하게 에러
메시지를 반환한다. 예외(exception)를 쓰지 않고
타입 시스템으로 실패를 표현하는 함수형 패턴이
일관되게 적용되어 있다.

다만 중첩 match가 7-8단계까지 깊어지면서
코드가 "스텝 피라미드(pyramid of doom)"
형태가 되는데, F#의 `result {}` CE(Computation
Expression)를 쓰면 상당히 평탄화할 수 있다.
의도적인 선택인지 향후 리팩터링 대상인지는
흥미로운 지점이다.

## 주요 명령어 흐름

```
git memento init claude     # .git/config에 설정 저장
git memento commit <id> -m "msg"  # 커밋 + 세션 노트 첨부
git memento amend <id>      # 기존 노트 보존하며 amend
git memento push            # 브랜치 + 노트 동시 push
git memento notes-sync      # 리모트 노트 병합 (백업 자동 생성)
git memento audit --range main..HEAD  # 노트 누락 검사
git memento doctor          # 설정/동기화 상태 진단
```

### amend 워크플로우의 설계

`git commit --amend`는 커밋 해시를 변경한다.
기존 커밋에 붙어 있던 노트가 유실될 수 있다.
git-memento의 amend 워크플로우는:

1. amend 전 HEAD의 기존 노트를 읽는다
2. 새 세션이 있으면 기존 노트 목록에 추가한다
3. amend로 새 커밋을 만든다
4. 새 HEAD에 병합된 노트를 첨부한다

이렇게 하면 amend를 반복해도 세션 기록이
누적된다. 하나의 커밋에 여러 AI 세션이 기록될
수 있는 것이다.

### notes-sync의 안전장치

노트 동기화 시 충돌이 발생할 수 있다.
git-memento는 동기화 전에 항상 타임스탬프
기반 백업 ref를 생성한다:

```
refs/notes/memento-backups/20260302143022
```

병합이 실패해도 백업에서 복원할 수 있다.
기본 병합 전략은 `cat_sort_uniq`로,
중복 없이 노트를 합친다.

## 노트 포맷 분석

```markdown
<!-- git-memento-sessions:v1 -->
<!-- git-memento-note-version:1 -->
<!-- git-memento-session:start -->
# Git Memento Session

- Provider: Claude
- Session ID: abc123
- Committer: developer
- Captured At (UTC): 2026-03-02T14:30:22Z

## Conversation

### developer

코드 리뷰 부탁합니다.

### Claude

네, 살펴보겠습니다.
<!-- git-memento-session:end -->
```

HTML 주석을 구분자로 사용해 기계 파싱이 가능하면서도
사람이 읽을 수 있는 마크다운을 유지한다.
레거시 단일 세션 노트도 자동으로 새 포맷으로
업그레이드된다.

대화 내용에 구분자와 동일한 문자열이 있으면
백슬래시로 이스케이프하고, 파싱 시 역이스케이프한다.
단순하지만 견고한 충돌 방지 메커니즘이다.

## GitHub Actions 통합

두 가지 모드로 CI/CD에 통합된다:

| 모드      | 역할                              |
|-----------|-----------------------------------|
| comment   | PR에 세션 히스토리를 댓글로 게시  |
| gate      | 노트 누락 시 빌드 실패 (감사 모드)|

gate 모드의 `--strict` 옵션은 Provider, Session
ID 마커가 없는 노트도 실패로 처리한다.
"AI 도구를 썼다면 반드시 기록을 남겨라"를
CI 레벨에서 강제할 수 있다.

## 기술 스택 선택의 의미

**F# + NativeAOT**: 함수형 언어로 CLI 도구를
만들면서 NativeAOT로 단일 바이너리를 생성한다.
.NET 런타임 없이 배포할 수 있어 `git-memento`
바이너리 하나만 PATH에 넣으면 `git memento`로
바로 쓸 수 있다. Git의 서브커맨드 탐색 규칙
(`git-<name>` → `git <name>`)을 활용한 것이다.

**TypeScript (GitHub Actions)**: 노트를 PR
댓글로 렌더링하는 부분만 TypeScript로 작성했다.
GitHub Actions 런타임이 Node.js 기반이므로
합리적인 선택이다. 번들된 `dist/` 파일을
커밋에 포함해 Actions 소비자가 별도 빌드 없이
쓸 수 있게 했다.

## 인사이트

### AI 코딩의 감사 추적 문제

코드 리뷰에서 "이 코드를 왜 이렇게 짰는가?"라는
질문은 항상 있었다. AI 코딩 도구가 보편화되면
"AI에게 뭐라고 요청했는가?"가 추가된다.
git-memento는 이 질문에 대한 답을 커밋 수준에서
제공한다. 단순한 편의 도구가 아니라, AI 시대의
코드 거버넌스 인프라로 볼 수 있다.

### "세션 = 의도의 기록"이라는 관점

커밋 메시지가 "무엇을 했는가"를 기록한다면,
AI 세션은 "어떤 의도로, 어떤 시행착오를 거쳐
이 결과에 도달했는가"를 기록한다. 프롬프트
엔지니어링의 과정 자체가 코드의 맥락이 되는
셈이다. 이것은 전통적인 코드 리뷰에서
커버하지 못하던 영역이다.

### git notes의 재발견

`git notes`는 2010년 Git 1.6.6에서 추가된
이후 거의 사용되지 않았다. git-memento는
이 잊혀진 기능에 완벽한 용도를 찾아준 사례다.
커밋을 오염시키지 않으면서 메타데이터를 붙일
수 있는 `git notes`의 특성이 AI 세션 기록이라는
새로운 요구사항과 정확히 맞아떨어진다.

### 함수형 CLI의 실용성

F#으로 작성된 이 프로젝트는 함수형 프로그래밍이
CLI 도구 개발에서 어떻게 빛나는지 보여준다.
Discriminated Union으로 명령어를 모델링하고,
Result 타입으로 에러를 전파하며, 패턴 매칭으로
분기를 처리한다. 타입 시스템이 "처리하지 않은
케이스"를 컴파일 타임에 잡아준다.
안정적인 CLI 도구의 조건과 함수형 언어의 강점이
잘 맞는 조합이다.

## 참고

- [GitHub 저장소](https://github.com/mandel-macaque/memento)
- [git notes 공식 문서](https://git-scm.com/docs/git-notes)
