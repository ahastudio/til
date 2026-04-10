# Claude Code의 기억 시스템 - CLAUDE.md와 Auto Memory

> 원문: <https://code.claude.com/docs/en/memory>

## 요약

### 두 개의 기억 메커니즘

Claude Code 공식 문서의 “How Claude remembers your project” 페이지다. Claude
Code는 매 세션이 빈 컨텍스트 윈도우로 시작되며, 지식을 세션 간에 전달
하는 두 가지 메커니즘이 존재한다. 하나는 사용자가 직접 쓰는 `CLAUDE.md`
파일이고, 다른 하나는 Claude 스스로 쌓아가는 auto memory다. 둘 다 매
대화 시작 시점에 로드되지만, 강제적 설정이 아니라 “컨텍스트”로 취급된다.
지시가 구체적이고 간결할수록 Claude가 더 일관되게 따른다.

### CLAUDE.md의 위치 계층

CLAUDE.md 파일은 네 가지 스코프에 놓일 수 있다. 좁은 스코프가 넓은 스코프
보다 우선한다. Managed policy(IT 관리자가 배포하는 조직 전체 정책, macOS의
경우 `/Library/Application Support/ClaudeCode/CLAUDE.md`), Project
instructions(`./CLAUDE.md` 또는 `./.claude/CLAUDE.md`, 팀 공유), User
instructions(`~/.claude/CLAUDE.md`, 개인 전역), Local instructions
(`./CLAUDE.local.md`, 개인 프로젝트별, `.gitignore`에 추가해야 함)가 그
네 가지다. 파일들은 오버라이드되지 않고 모두 연결(concatenate)되어
컨텍스트에 들어간다.

### 디렉토리 탐색 규칙

Claude Code는 현재 작업 디렉토리에서 상위로 올라가며 각 디렉토리마다
`CLAUDE.md`와 `CLAUDE.local.md`를 찾는다. `foo/bar/`에서 실행하면
`foo/bar/CLAUDE.md`, `foo/CLAUDE.md` 등 모두 로드된다. 작업 디렉토리
아래의 서브디렉토리에 있는 `CLAUDE.md`는 시작 시점이 아니라 해당
디렉토리의 파일을 실제로 읽을 때 on-demand로 포함된다. 블록 수준 HTML
주석(`<!-- ... -->`)은 컨텍스트에 주입되기 전에 제거되므로 사용자
유지관리 메모를 토큰 소비 없이 남길 수 있다.

### 효과적인 지시 작성법

문서는 CLAUDE.md 작성의 몇 가지 원칙을 제시한다. 크기는 파일당 200줄
이하를 목표로 한다(길어질수록 컨텍스트 소모가 늘고 준수율이 떨어진다).
구조는 마크다운 헤더와 불릿으로 그룹화한다. 구체성은 “Format code
properly” 대신 “Use 2-space indentation”, “Test your changes” 대신
“`npm test` before committing”, “Keep files organized” 대신 “API
handlers live in `src/api/handlers/`”처럼 검증 가능한 수준까지 내려간다.
일관성 측면에서, 두 규칙이 충돌하면 Claude가 임의로 하나를 선택할 수
있으므로 주기적으로 정리해야 한다.

### 임포트와 AGENTS.md 호환

CLAUDE.md는 `@path/to/import` 문법으로 다른 파일을 임포트할 수 있고,
최대 5단계까지 재귀 가능하다. `@README`, `@package.json`,
`@docs/git-instructions.md` 같은 형태로 사용한다. 중요한 실용 정보는
“Claude Code는 `AGENTS.md`를 직접 읽지 않는다”는 점이다. 이미 `AGENTS.md`
를 쓰는 저장소라면 `CLAUDE.md`에 `@AGENTS.md`를 임포트하고 그 아래에
Claude 전용 지시를 추가하면 된다.

### `.claude/rules/` 디렉토리

큰 프로젝트는 지시를 여러 파일로 분리해 `.claude/rules/` 디렉토리에
배치할 수 있다. 모든 `.md` 파일이 재귀적으로 발견되고, 서브디렉토리
(`frontend/`, `backend/`)로 조직 가능하다. Frontmatter에 `paths` 필드로
glob 패턴을 지정하면 특정 파일과 작업할 때만 로드되는 scoped rule이 된다.
`paths`가 없는 rule은 `.claude/CLAUDE.md`와 동일한 우선순위로 시작 시점에
무조건 로드된다. `~/.claude/rules/`는 모든 프로젝트에 적용되는 사용자
수준 rule이며, 프로젝트 rule보다 먼저 로드되어 프로젝트 rule이 더 높은
우선순위를 갖는다.

### 대규모 팀을 위한 관리

IT/DevOps가 배포하는 managed policy CLAUDE.md는 개별 사용자 설정으로
제외할 수 없다. `claudeMdExcludes` 설정은 거대 monorepo에서 다른 팀의
CLAUDE.md를 글로브 패턴으로 스킵할 수 있게 해준다. 문서는 managed
settings와 managed CLAUDE.md의 역할을 명확히 구분한다. 기술적 강제
(permissions.deny, sandbox.enabled, env, forceLoginMethod)는 settings에,
행동 지침(코드 스타일, 데이터 처리, 행동 지시)은 CLAUDE.md에 둔다.
“Settings rules are enforced by the client regardless of what Claude
decides to do. CLAUDE.md instructions shape Claude's behavior but are
not a hard enforcement layer.”

### Auto Memory 시스템

Auto memory는 사용자가 아무것도 쓰지 않아도 Claude가 세션을 넘나들며
지식을 쌓게 해주는 기능이다. Claude는 빌드 명령어, 디버깅 통찰, 아키텍처
노트, 코드 스타일 선호, 워크플로 습관을 스스로 기록한다. “매 세션마다
무언가를 저장하지는 않는다. 미래의 대화에 유용할지 여부를 기준으로 저장할
가치가 있는 것을 결정한다.” v2.1.59 이상이 필요하며 기본 활성화되어
있다. `/memory` 명령어로 토글하거나 `autoMemoryEnabled: false`로 비활성화
할 수 있고, 환경 변수 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`로도 꺼진다.

### Auto Memory 저장 구조

각 프로젝트는 `~/.claude/projects/<project>/memory/`에 독립된 메모리
디렉토리를 갖는다. `<project>` 경로는 git 저장소에서 파생되어, 같은
저장소의 모든 worktree와 서브디렉토리가 하나의 디렉토리를 공유한다.
디렉토리에는 `MEMORY.md` 엔트리포인트와 선택적 토픽 파일들(예:
`debugging.md`, `api-conventions.md`)이 들어간다. `MEMORY.md`는 매 세션
시작 시점에 처음 200줄 또는 25KB까지만 로드되며, 상세한 내용은 별도
토픽 파일로 분리되어 필요할 때 Claude가 직접 읽는다. auto memory는
machine-local이며 머신이나 클라우드 환경을 건너 공유되지 않는다.

### 트러블슈팅

문서는 주요 문제의 해결 방법을 정리한다. Claude가 CLAUDE.md를 따르지
않을 때: `/memory`로 파일이 로드되었는지 확인, 위치 재점검, 지시를 더
구체적으로 작성, 충돌하는 지시 제거, 필요 시 `--append-system-prompt`
사용. 파일이 너무 클 때: `@path` 임포트로 분리하거나 `.claude/rules/`로
분할. `/compact` 이후 지시가 사라진 것처럼 보일 때: CLAUDE.md는 compaction
이후 재로드되므로, 사라졌다면 대화에서만 준 지시이지 파일에 없던 것이다.

## 분석

### 문서의 메타-입장: “강제가 아니라 컨텍스트”

이 문서의 가장 중요한 한 문장은 “Both are loaded at the start of every
conversation. Claude treats them as context, not enforced configuration”
이다. 이 선언은 Claude Code의 기억 시스템에 대한 사용자의 기대치를 명확히
재설정한다. 많은 개발자는 CLAUDE.md를 “설정 파일”처럼 생각해 “여기에
쓰면 반드시 지켜진다”고 가정하지만, 문서는 이를 명시적으로 부정한다.

이 차이는 심대하다. 설정 파일은 결정론적이다. “2-space indentation”이라고
쓰면 도구가 무조건 2칸 들여쓰기를 적용한다. 컨텍스트는 확률적이다. 같은
지시를 써도 LLM이 일관되게 따를 가능성이 높아질 뿐, 보장되지 않는다.
이 불확실성을 줄이는 것이 “구체성, 간결성, 구조화”라는 문서의 세 가지
원칙이다. 이는 프롬프트 엔지니어링 원칙과 정확히 일치한다. CLAUDE.md는
본질적으로 “지속적으로 로드되는 프롬프트”이며, 프롬프트 엔지니어링의
모든 원칙이 그대로 적용된다.

### 네 가지 스코프의 설계 논리

Managed policy → Project → User → Local의 4단 스코프는 전통적인 Unix
설정 파일의 계층 구조를 연상시킨다. 시스템 설정, 사이트 설정, 사용자
설정, 프로세스별 설정이라는 고전적 4층을 Claude Code가 그대로 옮긴 것이다.
흥미로운 차이는 “오버라이드”가 아니라 “연결(concatenate)”이라는 점이다.

전통적 설정 파일에서는 좁은 스코프가 넓은 스코프를 덮어쓰지만(override),
Claude Code에서는 모든 스코프가 하나의 긴 컨텍스트로 합쳐진다. 이는
“Claude가 읽을 수 있는 텍스트가 많을수록 좋다”는 LLM 전제의 결과다.
다만 이 설계는 충돌 해결을 어렵게 만든다. Project CLAUDE.md가 “tabs”를
요구하고 User CLAUDE.md가 “spaces”를 요구하면 어느 쪽도 오버라이드되지
않고, 두 지시가 동시에 Claude에게 전달된다. 문서는 이 경우 “Claude가
임의로 선택할 수 있다”고 솔직히 인정한다.

### CLAUDE.md vs .claude/rules/ vs Skills

문서는 세 개의 로딩 메커니즘을 명확히 구분한다. CLAUDE.md와 unconditional
rules는 매 세션마다 전체 로드된다. Path-scoped rules는 매칭되는 파일을
읽을 때 로드된다. Skills는 사용자가 invoke하거나 Claude가 관련성을 판단할
때만 로드된다. 이 3단 구분은 컨텍스트 윈도우 관리의 설계 결정이다.

로딩 시점에 전체 로드되는 것은 비용이 크지만 확실한 영향을 준다. 조건부
로드되는 것은 비용이 싸지만 놓칠 가능성이 있다. 필요할 때만 로드되는
것은 가장 효율적이지만 발견 가능성에 의존한다. 개발자는 각 지시가 어떤
유형인지에 따라 위치를 선택해야 한다. “코드 스타일 같은 기본 규칙 → 전체
로드”, “특정 디렉토리의 규칙 → scoped rules”, “일회성 작업 워크플로 →
skills”라는 가이드라인이 자연스럽게 도출된다.

### Auto Memory의 철학적 전환

Auto memory는 CLAUDE.md의 “사용자가 쓴다” 모델과 정반대의 “Claude가 쓴다”
모델을 도입한다. 이는 단순한 기능 추가가 아니라 철학적 전환이다. 전통적
도구 설정은 사용자가 선언하고 도구가 따른다. Auto memory는 도구가 학습
하고 사용자가 감사(audit)한다. 이 역할 역전은 소프트웨어 도구 역사에서
드물다. Vim이 자기 설정을 스스로 바꾸거나, Git이 자기 hook을 스스로 추가
하는 것과 비교할 수 있다.

이 전환이 가능한 이유는 LLM의 능력이다. 전통적 도구는 “무엇이 기록할
가치가 있는가”를 판단할 수 없었지만, LLM은 가능하다. 문서가 명시한 원칙
― “Claude doesn't save something every session. It decides what's worth
remembering based on whether the information would be useful in a future
conversation” ― 은 LLM의 판단력을 전제로 한 설계다. 이 판단력이 잘못되면
메모리가 쓰레기로 채워지고, 잘 작동하면 사용자가 반복 지시할 필요가
없어진다. 후자가 이번 업데이트의 목표다.

## 비평

### 강점

#### 문서로서의 구조적 완결성

이 페이지는 단순한 기능 소개가 아니라 완전한 참조 문서다. 개념 설명, 설정
방법, 위치 규칙, 로딩 순서, 임포트 문법, 대안(AGENTS.md 호환), 대규모 팀
관리, 트러블슈팅까지 모든 필수 섹션을 포함한다. 사용자가 “어떻게 시작
하는가”부터 “문제가 생겼을 때 무엇을 봐야 하는가”까지 한 페이지에서 해결
할 수 있다.

#### 구체적 예시의 일관성

모든 추상적 개념이 즉시 코드 예시로 뒷받침된다. `.claude/rules/`의 디렉
토리 트리, YAML frontmatter의 paths 필드, `@AGENTS.md` 임포트 문법,
symlink 명령어, 환경 변수 이름까지 모두 실제로 복사해 쓸 수 있는 형태로
제공된다. 이는 “문서를 읽고도 시작하지 못하는” 흔한 문제를 회피한다.

#### LLM의 확률적 본성에 대한 솔직함

“no guarantee of strict compliance, especially for vague or conflicting
instructions”라는 문장은 드물게 솔직하다. 대부분의 AI 도구 문서는 “이
기능을 활성화하면 반드시 이렇게 작동합니다”처럼 결정론적으로 기술하지만,
이 문서는 LLM의 본질적 비결정성을 인정하고 그에 맞는 사용법을 권고한다.
이는 장기적으로 사용자 신뢰를 쌓는 정직한 선택이다.

#### Managed settings vs CLAUDE.md의 명확한 구분

대규모 팀 섹션의 표는 특히 유용하다. “settings는 기술적 강제, CLAUDE.md는
행동 지침”이라는 이분법은 조직 배포 시 가장 자주 혼란스러운 지점을
깔끔하게 정리한다. “Block specific tools → settings”, “Code style →
CLAUDE.md”처럼 구체적 매핑을 제공한 것은 의사결정 프레임워크로서 즉시
쓸 수 있다.

### 약점

#### 토큰 비용에 대한 정량적 가이드 부족

“200줄 이하를 목표로 하라”는 가이드는 있지만, 실제로 CLAUDE.md 전체가
컨텍스트 윈도우에서 몇 퍼센트를 차지하는지, 그것이 실제 성능에 어떤
영향을 미치는지에 대한 정량적 데이터는 없다. 사용자는 “길수록 나쁘다”는
방향만 알 뿐, “1000줄짜리 CLAUDE.md가 얼마나 나쁜가”는 알 수 없다.

#### 충돌 해결의 블랙박스

“두 규칙이 충돌하면 Claude가 임의로 하나를 선택할 수 있다”는 설명은
솔직하지만 불충분하다. 사용자 입장에서는 “어떤 조건에서 어느 쪽이 선택
되는가”를 알고 싶다. 최근 로드된 파일이 이기는가? 마지막으로 쓰여진
파일이 이기는가? 더 구체적인 지시가 이기는가? 이런 메커니즘을 명시
하지 않으면 충돌 해결이 운에 맡겨진다.

#### Auto memory의 실패 모드 미언급

“Claude가 기록할 가치가 있는 것을 결정한다”는 설명은 작동하는 경우의
이상적 묘사다. 그러나 LLM의 판단이 실패하는 경우 ― 잘못된 정보를 저장,
민감한 정보를 저장, 편향된 관찰을 일반화 ― 는 다루지 않는다. 특히 auto
memory에 저장된 내용이 자체 프롬프트에 재주입되면 편향이 강화되는
피드백 루프가 발생할 수 있는데, 이 위험은 언급되지 않는다.

#### `.claude/rules/`의 실제 로딩 동작 불명확

“Rules load into context every session or when matching files are
opened”라는 설명은 모호하다. unconditional rules는 세션 시작에 로드
되고 path-scoped rules는 파일을 읽을 때 로드된다는 것은 분명하지만,
“파일을 읽는다”의 정의가 불명확하다. Grep이 그 파일을 매칭하면 로드
되는가? Glob이 나열하면 로드되는가? Edit이 타겟으로 지정하면 로드되는가?
이 세부사항이 scoped rules의 실효성을 결정한다.

#### 버전 의존성의 함정

Auto memory가 v2.1.59 이상을 요구한다고 명시했지만, 이것은 사용자에게
도구 버전 관리의 부담을 준다. “이 기능이 왜 안 되지?”의 원인이 버전
차이일 수 있다는 점을 문서 맨 앞에서 더 크게 경고했어야 한다. 또한
“MEMORY.md의 200줄/25KB 제한”이 어느 버전부터 적용되는지도 명시되지
않았다.

## 인사이트

### 1. CLAUDE.md는 “지속적 프롬프트”라는 새로운 아티팩트 카테고리를 만든다

소프트웨어 엔지니어링 역사에는 몇 개의 표준화된 설정 아티팩트가 있다.
`.gitignore`, `package.json`, `tsconfig.json`, `.editorconfig`, `Dockerfile`
같은 파일들이 그 목록이다. 각각은 특정 도구의 설정을 담지만, 결정론적
규칙으로 해석된다. `CLAUDE.md`는 이 계보에 속하면서도 결정적으로 다른
성격을 갖는다. 그것은 “실행되는 설정”이 아니라 “읽히는 컨텍스트”다.

이 차이는 CLAUDE.md를 관리하는 방법에 즉각 영향을 미친다. 결정론적 설정은
오타가 있으면 즉시 에러가 나지만, CLAUDE.md는 오타가 있어도 Claude가 대충
이해하고 넘어간다. 결정론적 설정은 “최소한으로 유지”가 미덕이지만,
CLAUDE.md는 “너무 작아도 맥락 부족, 너무 커도 주의력 분산”이라는 미묘한
균형이 필요하다. 결정론적 설정은 A/B 테스트가 의미 없지만, CLAUDE.md는
“어떤 지시가 더 효과적인가”를 A/B 테스트해야 할 수 있다.

이 새로운 카테고리가 소프트웨어 엔지니어링에 가져올 변화는 깊다. 앞으로
모든 AI 코딩 도구가 비슷한 “지속적 프롬프트 파일”을 요구할 것이고, 이들의
유지보수는 새로운 전문 영역이 될 것이다. “CLAUDE.md 엔지니어”라는 역할이
이미 일부 큰 조직에서 비공식적으로 등장하고 있다. 그들의 일은 조직의
코드베이스를 AI 친화적으로 만들기 위해 CLAUDE.md와 rules 파일을 체계적
으로 설계하고 유지하는 것이다. 이는 2010년대의 “DevOps 엔지니어” 등장과
유사한 직업 진화의 징후다.

또한 이 카테고리는 버전 관리에도 새로운 질문을 던진다. CLAUDE.md가 결정
론적이지 않다면, 그 변경이 실제로 Claude의 행동을 어떻게 바꾸는지 어떻게
검증할 수 있는가? 현재는 검증 메커니즘이 없다. “eval suite for
CLAUDE.md”라는 새로운 도구 카테고리가 필요하며, 이는 미래의 성장 영역
이다. 주어진 CLAUDE.md로 Claude가 특정 작업을 정확히 수행하는지 자동
으로 확인하는 테스트 프레임워크 ― 이것이 없이는 CLAUDE.md 유지보수는
곧 기도에 가까워진다.

### 2. Auto memory는 “사용자 설정의 종말”의 시작이다

Auto memory가 도입한 “도구가 스스로 학습하고 사용자는 감사한다”는 모델은
지난 50년간의 소프트웨어 설정 패러다임을 거꾸로 뒤집는다. 역사적으로 소프트
웨어는 “기본값 + 사용자 설정”의 이원 구조로 작동했다. 개발자는 합리적
기본값을 제공하고, 사용자는 자기 취향에 맞게 오버라이드한다. 이 모델의
한계는 “사용자가 설정하지 않으면 개인화되지 않는다”는 것이다. 대부분의
사용자는 설정을 탐색하지 않고 기본값 그대로 사용한다.

Auto memory는 이 한계를 돌파한다. “사용자가 설정하지 않아도 도구가 학습
한다.” 이는 단지 Claude Code만의 혁신이 아니라 소프트웨어 전반의 방향성
이다. Apple의 Spotlight가 사용자의 검색 패턴을 학습하고, Google의 Gmail이
이메일 분류를 학습하고, Spotify가 음악 취향을 학습하는 모든 사례가 같은
흐름에 속한다. 그러나 이 모든 이전 사례는 “서비스 내부에서 숨겨진 학습”
이었다. 사용자는 학습된 내용을 볼 수 없고, 수정할 수 없었다.

Claude Code의 auto memory는 다르다. 학습된 내용이 `~/.claude/projects/
<project>/memory/`의 일반 마크다운 파일로 저장되고, 사용자는 언제든지
읽고 편집하고 삭제할 수 있다. 이는 “블랙박스 학습”에서 “투명한 학습”으로의
전환이다. 사용자는 도구가 무엇을 배웠는지 정확히 알고, 잘못된 학습은
교정할 수 있다.

이 투명성은 미래 소프트웨어 디자인의 새로운 표준이 될 수 있다. 사용자가
도구의 학습 결과를 직접 볼 수 있어야 한다는 요구는 GDPR의 “explainability”
요구와 맞닿아 있고, AI 안전 담론의 “interpretability” 요구와도 일치한다.
향후 모든 AI 기반 제품이 “학습된 내용을 사용자가 볼 수 있어야 한다”는
규제 또는 사회적 압력을 받을 가능성이 높다. Claude Code의 `/memory`
명령어와 MEMORY.md 파일은 이 표준의 초기 구현이며, 다른 AI 제품들이 이
패턴을 벤치마킹할 것이다.

### 3. 컨텍스트 윈도우가 늘어나도 “선택적 로딩”은 사라지지 않는다

2024-2026년 사이 LLM의 컨텍스트 윈도우는 기하급수적으로 늘어났다. 32k →
100k → 200k → 1M → 2M 토큰으로 증가했고, 일부 모델은 거의 무제한에
가까워지고 있다. 이 흐름에서 많은 사람이 “컨텍스트가 충분하면 모든 문서를
한꺼번에 로드하면 된다”고 생각한다. 그러나 Claude Code의 기억 시스템
설계는 정반대의 방향을 보여준다.

CLAUDE.md는 “200줄 이하 목표”, `.claude/rules/`의 path-scoped rules는
“매칭되는 파일 작업 시만 로드”, skills는 “invoke하거나 관련성 판단 시만
로드”, auto memory의 MEMORY.md도 “첫 200줄/25KB만 로드”. 모든 메커니즘이
“로드되는 양을 줄이는” 방향으로 설계되어 있다. 왜인가?

이유는 두 가지다. 첫째, 컨텍스트가 커도 LLM의 주의 집중(attention)이
모든 토큰에 균등하게 분배되지 않는다. 긴 컨텍스트 안에서 중요한 정보가
“길 중간에 묻히는” 문제(“lost in the middle”)가 여전히 존재한다. 컨텍스트
가 커질수록 LLM이 초반과 말미의 토큰에 더 주의를 기울이고, 중간 부분은
상대적으로 덜 주목하는 경향이 보고되었다. 이 문제는 컨텍스트 크기 증가
로 해결되지 않고, 오히려 악화될 수 있다.

둘째, 비용 문제다. 컨텍스트에 넣는 토큰은 매 요청마다 비용이 발생한다.
200k 토큰 전체를 매번 로드하면 비용이 수 배 증가한다. Anthropic의 prompt
caching은 이 비용을 완화하지만, 완전히 제거하지는 못한다. “필요한 것만
로드”는 단지 성능 문제가 아니라 경제 문제다.

이 두 이유 때문에 “선택적 로딩”은 컨텍스트 크기와 무관하게 지속적으로
중요한 기술로 남을 것이다. 향후 5년 내 등장할 모든 AI 코딩 도구는 어떤
형태로든 “무엇을 로드할지 결정하는” 메커니즘을 가질 것이다. Claude
Code의 4단계 로딩(CLAUDE.md → rules → scoped rules → skills)은 이 방향
의 초기 표준안이며, 다른 도구들이 유사한 계층을 만들 것이다. 컨텍스트
윈도우가 아무리 커져도, “무엇을 넣을지 결정하는 작업”은 사라지지 않고
오히려 더 정교해진다.

### 4. `.claude/rules/`의 glob 패턴은 “코드가 컨텍스트를 결정”하는 패러다임

`.claude/rules/`의 path-scoped rules는 기술적으로 단순한 기능이지만,
철학적으로 중요한 의미를 갖는다. 그것은 “Claude가 어떤 지시를 따라야
하는가”를 “Claude가 지금 만지는 파일이 무엇인가”로 결정한다는 것이다.
이는 “컨텍스트가 코드를 결정한다”가 아니라 “코드가 컨텍스트를 결정한다”
는 역전이다.

이 패턴의 실무적 함의는 크다. 전통적으로 코딩 가이드라인은 “프로젝트
전역”이나 “팀 전역”으로 설정되었다. “이 회사에서는 2-space indentation”
같은 규칙이다. 그러나 실제 코드베이스는 훨씬 더 미세한 구분을 필요로
한다. “notebooks은 탐색적 코드, src는 프로덕션 코드, tests는 명확성
우선, docs는 간결성 우선” 같은 차별화된 규칙이 필요하다. 이 차별화를
사람이 매번 기억하고 적용하기는 어렵다.

path-scoped rules는 이 문제의 해결책이다. 규칙을 파일에 박아두고 Claude가
자동으로 적용하게 만든다. 이는 코드베이스 자체가 “규칙의 위치”를 결정
하는 구조다. `src/models/churn/` 안에 들어가면 자동으로 “프로덕션 ML
규칙”이 활성화되고, `notebooks/` 안에 들어가면 “실험적 노트북 규칙”이
활성화된다. 사용자는 이를 의식할 필요가 없다.

더 깊은 함의는, 이 패턴이 “리포지토리가 자기 사용 방법을 설명한다”는
새로운 자기 문서화(self-documentation) 형태를 만든다는 점이다. 전통적
인 self-documenting code는 “함수 이름과 주석으로 의도를 표현한다”는
의미였다. path-scoped rules는 여기서 한 걸음 더 나아가 “코드 위치 자체가
AI 협력자의 행동 규칙을 활성화한다”는 차원을 추가한다. 향후 오픈소스
프로젝트들은 자신의 `.claude/rules/`를 리포지토리의 일부로 유지관리
할 것이고, 이는 README.md와 비슷한 공적 자료가 될 것이다. “이 프로젝트
에서 Claude를 어떻게 써야 하는가”가 리포지토리 수준에서 답변되는
시대가 오고 있다.

### 5. 기업 배포가 가능한 AI 도구의 조건: “managed policy”

문서의 대규모 팀 섹션은 쉽게 지나칠 수 있지만 가장 전략적으로 중요한
부분이다. Managed policy CLAUDE.md ― macOS의 `/Library/Application
Support/ClaudeCode/CLAUDE.md`, Linux의 `/etc/claude-code/CLAUDE.md`,
Windows의 `C:\Program Files\ClaudeCode\CLAUDE.md` ― 는 IT 관리자가 MDM,
Group Policy, Ansible로 배포할 수 있는 조직 전역 설정이다. 이 파일은
개별 사용자 설정으로 제외할 수 없다.

이 기능이 있다는 것과 없다는 것의 차이는 엔터프라이즈 시장에서 결정적
이다. 보안 민감 조직(금융, 의료, 법률, 정부)은 “모든 직원이 동일한
코딩 표준을 따라야 한다”는 요구를 갖는다. 이 요구는 도구가 사용자 개입
없이 정책을 강제할 수 있을 때만 충족된다. 개별 사용자가 자기 CLAUDE.md를
수정해 조직 정책을 우회할 수 있다면, 컴플라이언스 팀은 그 도구를 승인할
수 없다.

더 흥미로운 점은 Claude Code가 “managed settings”와 “managed CLAUDE.md”를
분리한 것이다. Settings는 기술적 강제(permissions.deny, sandbox.enabled)를
담당하고, CLAUDE.md는 행동 지침을 담당한다. 이 분리는 “하드 룰 vs 소프트
룰”의 전통적 구분을 재현한다. 방화벽 규칙처럼 절대 양보 불가한 것은
settings에 두고, 코드 스타일처럼 지침 수준인 것은 CLAUDE.md에 둔다.

이 설계는 다른 AI 도구들이 엔터프라이즈 시장에 진입할 때 따라야 할
템플릿이 될 것이다. “managed policy 지원 없이는 Fortune 500 고객을
얻을 수 없다”는 규칙이 이미 SaaS 업계에서 자리잡았고, AI 코딩 도구에도
같은 규칙이 적용되고 있다. Cursor, Windsurf, GitHub Copilot 등 경쟁
제품들이 managed policy 기능을 얼마나 잘 구현했는지는 그들의 엔터프
라이즈 시장 점유율을 직접 결정할 것이다. Claude Code가 이 기능을 명확히
문서화하고 공식적으로 지원하는 것은 엔터프라이즈 확산을 위한 전략적
투자의 명백한 증거다.
