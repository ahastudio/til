# git-memento: AI 코딩 세션을 커밋에 기록하는 Git 확장

<https://github.com/mandel-macaque/memento>

## 한 줄 요약

AI 코딩 도구(Codex, Claude Code 등)의 대화 세션을 `git notes`로 커밋에 첨부하는
Git 확장 도구.

## 왜 필요한가

AI 코딩 도구가 보편화되면서 새로운 문제가 등장했다. 커밋 메시지만으로는 "AI와
어떤 대화를 거쳐 이 코드가 나왔는지" 알 수 없다. `git blame`으로 누가
작성했는지는 추적할 수 있지만, AI가 개입한 맥락은 사라진다.

git-memento는 이 빈틈을 메운다. 커밋할 때 AI 세션 히스토리를 자동으로 가져와
`git notes`에 마크다운 형태로 저장한다. 기존 Git 워크플로우를 건드리지 않으면서
AI 협업의 추적성(traceability)을 확보하는 접근이다.

## File-based Planning Workflow와의 접점

AI 코딩 도구의 작업 관리에는 두 축이 있다.

**실시간 축 — File-based Planning Workflow.** `task_plan.md`, `progress.md` 같은
마크다운 파일을 디스크에 만들어 AI의 "작업 기억(working memory)"으로 쓴다.
컨텍스트 윈도우를 넘는 복잡한 작업에서 맥락 유실을 방지한다.

**사후 축 — git-memento.** 완료된 AI 세션 대화를 커밋에 첨부한다. "무엇을
계획했는가"가 아니라 "어떤 대화로 이 결과에 도달했는가"를 기록한다.

이 두 축은 상호 보완적이다.

```
[Planning]                    [Execution]
task_plan.md ──→ AI 세션 ──→ 코드 변경
     ↓                           ↓
progress.md              git memento commit
(실시간 상태)             (대화 아카이브)
```

File-based Planning이 "작전 지도"라면, git-memento는 "작전 일지"다. 지도만으로는
실제 전투에서 무슨 일이 있었는지 알 수 없고, 일지만으로는 전체 전략을 파악할 수
없다. 둘 다 있어야 AI 코딩의 전체 맥락이 보존된다.

### 계획 파일을 왜 노트에 넣지 않는가

`task_plan.md`도 커밋에 첨부하면 되지 않을까? git-memento는 의도적으로 이를 하지
않는다. 계획 파일은 작업 중간에 계속 변하는 가변 상태(mutable state)이고, 세션
대화는 작업 완료 후 확정되는 불변 기록(immutable log)이다.

가변 상태를 불변 저장소에 넣으면 혼란이 생긴다. "이 계획 파일의 어느 버전이 이
커밋에 해당하는가?" 커밋 시점의 세션 대화만 기록하면 이 문제가 없다. 세션이 곧
"이 커밋을 만들기 위해 실제로 일어난 일의 전부"이기 때문이다.

## 핵심 설계 결정

### git notes를 저장소로 선택한 이유

커밋 메시지 본문에 세션을 넣으면 로그가 오염된다. 별도 파일로 관리하면 저장소가
비대해진다. `git notes`는 커밋 객체에 메타데이터를 덧붙이되 커밋 해시를 변경하지
않는다. 기존 워크플로우와 충돌 없이 부가 정보를 관리할 수 있는 유일한 Git 내장
메커니즘이다.

단, `git notes`는 잘 알려지지 않은 기능이라 팀 도입 시 학습 비용이 있고,
`git push`로는 자동 전파되지 않아 별도 동기화가 필요하다. git-memento는
`share-notes`, `push`, `notes-sync` 명령으로 이 문제를 해결한다.

### 2단계 노트 아키텍처 (Summary + Full Audit)

`CommitWorkflow.fs`에서 가장 흥미로운 설계. 기본 `refs/notes/commits`에는
**요약**만 저장하고, 전체 대화는 별도 ref인 `refs/notes/memento-full-audit`에
보관한다.

```
refs/notes/commits           ← 요약 (일상 참조용)
refs/notes/memento-full-audit ← 전체 대화 (감사용)
```

이 분리의 배경: AI 세션 대화는 길다. `git log --notes`로 볼 때 수백 줄의 대화가
쏟아지면 로그가 못 쓰게 된다. 요약은 간결하게, 전체 기록은 필요할 때만.

File-based Planning에서 `progress.md`(요약)와 `findings.md`(상세)를 분리하는
패턴과 동일한 원리다. 정보의 계층화(information layering).

### SHA256 무결성 체인

요약 노트와 전체 노트는 해시로 연결된다:

```fsharp
let originalSessionLogHash (session: SessionData) =
    // Provider, SessionId, 모든 메시지를
    // 정규화된 형식으로 직렬화 후 SHA256
    sha256Hex (sb.ToString())
```

```
원본 세션 데이터
   ↓ SHA256
originalSessionLogHash ──→ 요약 노트에 기록
                       ──→ 전체 감사 노트에 기록
                                ↓
                          summaryHash도 기록
```

요약이 조작되었는지 전체 대화와 대조할 수 있다. "AI가 이렇게 말했다"는 주장을
암호학적으로 검증할 수 있는 것이다. 코드 거버넌스가 단순한 관례가 아니라 검증
가능한 시스템으로 격상된다.

### summarySkill: AI가 AI를 요약하는 메타 패턴

`CommitWorkflow`의 `summarySkill` 파라미터는 AI 도구를 호출해 세션 대화를
요약하게 한다. 사용자는 요약 결과를 확인하고, 불만족스러우면 프롬프트를 수정해
재생성할 수 있다:

```fsharp
let rec confirmSummaryAsync session userSkill
    userPrompt =
    task {
        let! summaryResult =
            provider.SummarizeSessionAsync(...)
        // 결과 표시 후 사용자에게 확인
        // "y" → 승인, 아니면 재생성 프롬프트 입력
        // 재귀 호출로 만족할 때까지 반복
    }
```

AI 코딩 세션을 AI가 요약하고, 인간이 검수하는 3자 구조. 이것은 File-based
Planning에서 AI가 계획을 세우고 인간이 승인하는 패턴의 변형이다. 차이점은 "사전
계획 승인"이 아니라 "사후 기록 승인"이라는 점이다.

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

AI 도구별 세션 조회 방식을 `IAiSessionProvider` 인터페이스로 추상화했다. 실제
구현체인 `CliJsonProvider`는 외부 CLI를 호출해 JSON을 파싱하는 단일 클래스로,
Codex든 Claude든 실행 파일명과 인자만 바꾸면 동작한다.

이 설계의 핵심 인사이트: AI 도구들의 세션 데이터 형식은 다르지만, "세션 ID로
대화를 가져온다"는 인터랙션 패턴은 동일하다. 이 공통 패턴을 인터페이스 경계로
잡은 것이 확장성의 기반이다.

### JSON 파싱의 방어적 설계

`SessionJson` 모듈의 파싱 전략이 독특하다:

```fsharp
let rec extractTextFromContent (element: JsonElement) =
    match element.ValueKind with
    | JsonValueKind.String → element.GetString()
    | JsonValueKind.Array →
        // 배열이면 각 요소를 재귀적으로 추출
    | JsonValueKind.Object →
        // "text" 또는 "content" 속성을 재귀 탐색
    | _ → String.Empty
```

`content` 필드가 문자열일 수도, 배열일 수도, 중첩 객체일 수도 있다고 가정한다.
Codex와 Claude의 JSON 구조가 다르고, 버전마다 변할 수 있기 때문에 가능한 모든
형태를 재귀적으로 탐색한다. 스키마를 강제하는 대신 데이터에 적응하는 전략.

이것은 외부 API에 의존하는 도구의 현실적 선택이다. AI 도구의 출력 포맷은 빠르게
변한다. 엄격한 스키마 검증은 새 버전이 나올 때마다 깨진다. 유연한 탐색이 더
실용적이다.

### F#과 Railway-Oriented Programming

코드베이스 전체가 F#의 `Result<'T, string>` 타입으로 에러를 전파한다. 커밋
워크플로우는 저장소 확인 → 커미터 조회 → 세션 가져오기 → 마크다운 렌더링 → git
commit → HEAD 해시 조회 → git notes add 순으로 7단계를 거친다.

각 단계가 `match ... with | Error → | Ok →`로 연쇄되어 있어, 어디서 실패하든
깔끔하게 에러 메시지를 반환한다. 예외(exception)를 쓰지 않고 타입 시스템으로
실패를 표현하는 함수형 패턴이 일관되게 적용되어 있다.

#### 피라미드의 극단: MementoConfig

```fsharp
// MementoConfig.fs - 6단계 중첩 match
match read $"{keyBase}.bin" defaults.Executable with
| Error err -> Error err
| Ok executable ->
    match read $"{keyBase}.getArgs" defaults.GetArgs with
    | Error err -> Error err
    | Ok getArgs ->
        match read $"{keyBase}.listArgs" defaults.ListArgs with
        | Error err -> Error err
        | Ok listArgs ->
            match read ... with  // 계속 깊어진다
```

5개 설정 값을 순서대로 읽는 것뿐인데 들여쓰기가 6단계까지 깊어진다. F#의
`result {}` CE를 쓰면:

```fsharp
result {
    let! executable = read ... defaults.Executable
    let! getArgs = read ... defaults.GetArgs
    let! listArgs = read ... defaults.ListArgs
    return { Provider = provider; ... }
}
```

이렇게 평탄화할 수 있다. 현재 코드가 CE를 의도적으로 피한 것인지(외부 의존
최소화), 아직 리팩터링 전인지는 흥미로운 지점이다. 전체 코드베이스에서 CE를 한
번도 쓰지 않는 것으로 보아 의도적 선택일 가능성이 높다.

## 주요 명령어 흐름

```
git memento init claude
git memento commit <id> -m "msg"
git memento amend <id>
git memento push
git memento notes-sync
git memento audit --range main..HEAD
git memento doctor
```

### amend 워크플로우: 노트 누적의 설계

`git commit --amend`는 커밋 해시를 변경한다. 기존 커밋에 붙어 있던 노트가 유실될
수 있다. git-memento의 amend 워크플로우는:

1. amend 전 HEAD의 기존 노트를 읽는다
2. `SessionNotes.parseEntries`로 개별 세션 파싱
3. 새 세션이 있으면 기존 목록에 추가
4. amend로 새 커밋을 생성
5. 새 HEAD에 병합된 노트를 첨부

하나의 커밋에 여러 AI 세션이 누적될 수 있다. 이것은 "하나의 커밋 = 하나의 AI
세션"이라는 단순한 가정을 넘어선다. 현실에서는 AI 도구를 여러 번 사용하고
amend로 하나의 커밋으로 합치는 경우가 흔하기 때문이다.

### notes-sync: 분산 환경의 노트 동기화

`NotesSyncWorkflow`는 이 프로젝트에서 가장 방어적으로 설계된 워크플로우다.

```
1. 리모트 노트를 임시 네임스페이스에 fetch
   refs/notes/remote/{remote}/*
2. 로컬 refs 각각에 대해:
   a. 타임스탬프 백업 생성
      refs/notes/memento-backups/20260302143022/commits
   b. 리모트 노트와 병합
3. 병합 성공 시 리모트에 push
```

**핵심: 직접 fetch하지 않는다.** 리모트 노트를 로컬 `refs/notes/commits`에 바로
가져오면 기존 로컬 노트를 덮어쓸 수 있다. 임시 네임스페이스에 먼저 격리한 후
의도적으로 병합한다.

병합 실패 시 에러 메시지에 복원 명령어까지 포함시킨다:

```fsharp
let recoveryHint =
    $"git update-ref {notesRef} " +
    $"$(git rev-parse {backupRef})"
```

사용자가 패닉하지 않도록 탈출구를 미리 안내하는 방어적 설계. File-based
Planning의 `progress.md`가 장애 복구 지점을 기록하는 것과 같은 발상이다.

### notes-carry: rebase에서 노트 보존

`git rebase`는 커밋을 재작성한다. 커밋 해시가 바뀌면 `git notes`는 고아가 된다.
`notes-carry`는 원본 범위의 노트를 읽어 대상 커밋에 다시 첨부한다.

`notes-rewrite-setup`은 Git의 내장 rewrite 설정을 구성한다:

```
notes.rewriteRef = refs/notes/*
notes.rewriteMode = concatenate
notes.rewrite.rebase = true
notes.rewrite.amend = true
```

이 설정이 없으면 rebase할 때마다 노트가 사라진다. `doctor` 명령으로 이 설정이
되어 있는지 확인할 수 있다.

### doctor: 자가 진단 시스템

`DoctorWorkflow`는 13가지 항목을 점검한다:

- 저장소 유효성
- Provider 설정 (`memento.provider`)
- CLI 바이너리 경로, 인자 설정
- Provider 런타임 테스트 (실제 세션 목록 조회)
- 로컬 노트 ref 존재 여부
- 리모트 fetch 설정
- 리모트 노트 ref 존재 여부
- 4가지 rewrite 설정

각 항목이 `Pass`, `Warn`, `Fail` 상태를 갖고 JSON 또는 텍스트로 출력된다. CI
파이프라인에서 `--format json`으로 호출하면 자동화된 상태 점검이 가능하다.

## 노트 포맷: 봉투(Envelope) 패턴

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

### 봉투의 설계 원리

HTML 주석을 구분자로 쓰면 마크다운 렌더러가 보이지 않게 처리한다. GitHub에서
노트를 보면 메타데이터 마커 없이 깔끔한 대화만 보인다. 동시에 프로그래밍적
파싱도 가능하다.

대화 내용에 구분자와 동일한 문자열이 있으면 백슬래시로 이스케이프한다:

```fsharp
let private escapeCollisionLine (line: string) =
    let trimmed = line.Trim()
    if trimmed = SessionStartMarker
       || trimmed = SessionEndMarker
       || trimmed = EnvelopeMarker
       || trimmed = NoteVersionHeader
    then
        line.Replace(trimmed, "\\" + trimmed)
    else line
```

버전 마커(`note-version:1`)가 있어 포맷 진화의 여지를 남겼다. 레거시 단일 세션
노트(봉투 없이 본문만 있는 형태)도 `parseEntries`에서 자동으로 인식한다.

### TextCleaning: 노이즈 제거

AI 도구의 세션 데이터에는 로그 레벨 접두사가 섞여 있을 수 있다:

```
[debug] Starting analysis...
[info] Found 3 issues
```

`TextCleaning.cleanLine`은 이런 접두사를 반복적으로 제거한다.
`[debug] [info] text`처럼 중첩된 경우도 while 루프로 모두 벗겨낸다. AI 세션이
"기록"으로 변환될 때 발생하는 데이터 정제(data cleansing) 과정이다.

## GitHub Actions 통합

두 가지 모드로 CI/CD에 통합된다:

| 모드    | 역할                             |
| ------- | -------------------------------- |
| comment | PR에 세션 히스토리를 댓글로 게시 |
| gate    | 노트 누락 시 빌드 실패           |

### gate 모드의 감사(Audit) 로직

`AuditCore.validateNote`는 노트 존재 여부만 보지 않는다. 내용의 구조까지
검증한다:

```fsharp
type AuditIssue =
    | MissingNote           // 노트 자체가 없음
    | MissingProviderMarker // "- Provider:" 없음
    | MissingSessionIdMarker // "- Session ID:" 없음
    | EmptyNote             // 노트가 비어있음
```

`--strict` 모드에서는 `MissingProviderMarker`나 `MissingSessionIdMarker`도
실패로 처리한다. 단순히 "뭔가 적혀 있으면 통과"가 아니라 "올바른 형식의 AI 세션
기록인가"를 검증한다.

이것은 File-based Planning에서 계획 파일의 형식을 검증하는 린터(linter)와 같은
역할이다. "계획이 있는가"가 아니라 "유효한 계획인가"를 묻는 것이다.

## 기술 스택 선택의 의미

**F# + NativeAOT**: 함수형 언어로 CLI 도구를 만들면서 NativeAOT로 단일
바이너리를 생성한다. .NET 런타임 없이 배포할 수 있어 `git-memento` 바이너리
하나만 PATH에 넣으면 `git memento`로 바로 쓸 수 있다. Git의 서브커맨드 탐색 규칙
(`git-<name>` → `git <name>`)을 활용한 것이다.

**TypeScript (GitHub Actions)**: 노트를 PR 댓글로 렌더링하는 부분만 TypeScript로
작성했다. GitHub Actions 런타임이 Node.js 기반이므로 합리적인 선택이다. 번들된
`dist/` 파일을 커밋에 포함해 Actions 소비자가 별도 빌드 없이 쓸 수 있게 했다.

### ProcessRunner의 이중 모드

```fsharp
type ICommandRunner =
    abstract member RunCaptureAsync:
        fileName: string * arguments: string list
        -> Task<ProcessResult>
    abstract member RunStreamingAsync:
        fileName: string * arguments: string list
        -> Task<int>
```

`RunCaptureAsync`는 stdout/stderr를 캡처하고, `RunStreamingAsync`는 콘솔에 직접
출력한다.

`-m` 플래그 없는 `git commit`은 편집기를 연다. 이때 `RunStreamingAsync`로
사용자에게 제어를 넘긴다. 자동화와 인터랙티브의 경계를 프로세스 실행 레벨에서
설계한 것이다.

### CommandLine.splitArgs: 쉘 모사

Provider CLI 인자가 git config에 단일 문자열로 저장된다:

```
memento.codex.getArgs = sessions get {id} --json
```

이것을 인자 배열로 분리해야 한다. `CommandLine.splitArgs`는 작은따옴표와
큰따옴표를 처리하는 미니 쉘 파서다. 쉘에 의존하지 않고 크로스 플랫폼으로
동작하기 위한 선택이다.

## 도메인 모델링: Discriminated Union의 힘

```fsharp
type Command =
    | Commit of sessionId: string
              * messages: string list
              * summarySkill: string option
    | Amend of sessionId: string option
             * messages: string list
             * summarySkill: string option
    | Audit of range: string option
             * strict: bool
             * outputFormat: string
    | Doctor of remote: string
              * outputFormat: string
    | ShareNotes of remote: string
    | Push of remote: string
    | NotesSync of remote: string * strategy: string
    | NotesRewriteSetup
    | NotesCarry of onto: string * fromRange: string
    | Init of provider: string option
    | Version
    | Help
```

CLI의 모든 명령어가 하나의 타입으로 표현된다. 각 변형(variant)이 필요한
파라미터만 정확히 가지고 있다. `Program.fs`의 진입점에서 `match command with`로
분기하면 컴파일러가 누락된 케이스를 잡아준다.

이 패턴의 인사이트: CLI 파싱과 실행이 타입으로 완전히 분리된다.
`CliArgs.parse`는 `string[] → Result<Command, string>`만 책임지고,
`Program.main`은 `Command → int`만 책임진다. 중간에 유효하지 않은 상태가 존재할
수 없다.

## 인사이트

### AI 코딩의 3계층 기록 모델

git-memento와 File-based Planning을 결합하면 AI 코딩의 기록이 3계층으로
구성된다:

| 계층     | 도구             | 기록 시점 |
| -------- | ---------------- | --------- |
| 계획     | task_plan.md     | 작업 전   |
| 실행     | AI 세션 대화     | 작업 중   |
| 아카이브 | git-memento 노트 | 커밋 시점 |

기존 소프트웨어 개발에서 요구사항 문서 → 코드 → 커밋 메시지라는 3계층이
있었다면, AI 코딩에서는 계획 파일 → 세션 대화 → 세션 노트가 그 역할을 대체한다.
차이점은 세 계층 모두 마크다운이라는 동일한 매체로 통일된다는 것이다.

### "맥락 보존"의 서로 다른 시간 스케일

File-based Planning은 **분~시간** 단위의 맥락 보존이다. 긴 작업 중 컨텍스트
윈도우를 넘어도 디스크의 파일이 기억을 유지한다.

git-memento는 **주~월** 단위의 맥락 보존이다. 3개월 후 "왜 이렇게 구현했지?"
싶을 때 커밋 노트에서 당시 AI와의 대화를 복원한다.

시간 스케일이 다르기에 저장 메커니즘도 다르다. 단기 기억은 파일 시스템, 장기
기억은 Git 객체 저장소. 각각의 용도에 맞는 인프라를 쓴다.

### 요약과 전체 기록의 분리가 주는 교훈

2단계 노트 아키텍처는 단순한 편의가 아니다. "모든 정보를 기록하되, 일상적으로는
요약만 보여주라"는 정보 관리의 핵심 원칙이다.

File-based Planning에서도 `progress.md`는 짧은 상태 요약이고, `findings.md`는
상세 발견 사항이다. 같은 원칙의 다른 적용이다.

이 원칙이 없으면 정보 과잉으로 도구가 못 쓰게 된다. AI 세션 대화를 `git log`에
전부 쏟아내면 아무도 보지 않는다. 요약이 있어야 보고, 의심스러울 때만 전체를
본다.

### 감사(Audit)의 자동화가 바꾸는 것

`git memento audit --strict`를 CI에 넣으면 "AI 도구를 쓰고 기록을 남기지 않은
커밋"이 머지되지 않는다. 이것은 단순한 기술적 제약을 넘어서 팀 문화를 형성한다:

- "AI 사용은 숨길 일이 아니다"
- "AI와의 대화는 코드의 일부다"
- "검증 가능한 AI 사용이 책임 있는 AI 사용이다"

### 방어적 설계의 일관성

코드베이스 전체에 "최악의 상황에 대비하라"는 태도가 일관되게 흐른다:

- JSON 파싱: 스키마를 강제하지 않고 적응
- notes-sync: 병합 전 백업, 실패 시 복원 안내
- amend: 기존 노트 보존 후 누적
- 봉투 포맷: 구분자 충돌 이스케이프
- doctor: 13가지 사전 점검

CLI 도구는 "한 번 설치하면 잊어버리는" 성격이 강하다. 문제가 생겼을 때 사용자가
소스 코드를 읽을 리 없다. 도구 자체가 자기 진단하고 복구 방법을 안내해야 한다.

### 함수형 CLI의 실용성

F#으로 작성된 이 프로젝트는 함수형 프로그래밍이 CLI 도구 개발에서 어떻게
빛나는지 보여준다. Discriminated Union으로 명령어를 모델링하고, Result 타입으로
에러를 전파하며, 패턴 매칭으로 분기를 처리한다. 타입 시스템이 "처리하지 않은
케이스"를 컴파일 타임에 잡아준다.

동시에 한계도 보인다. CE 없는 Result 체인은 중첩이 깊어질수록 읽기 어렵다.
`NotesSyncWorkflow`의 `mutable failure` 패턴은 함수형이 아니라 명령형에 가깝다.
순수 함수형의 이상과 실용적 타협의 경계를 보여주는 코드베이스다.

## 참고

- [GitHub 저장소](https://github.com/mandel-macaque/memento)
- [git notes 공식 문서](https://git-scm.com/docs/git-notes)
