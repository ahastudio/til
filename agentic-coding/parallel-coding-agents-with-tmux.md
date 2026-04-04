# tmux와 마크다운 스펙으로 4~8개 병렬 코딩 에이전트 운영하기

Manuel Schipper가 공유한 병렬 코딩 에이전트 워크플로우.
오케스트레이터(Orchestrator)나 서브에이전트 프로파일 없이, tmux + 마크다운
파일 + bash alias + 슬래시 커맨드 6개만으로 구성한 경량(lightweight) 시스템이다.

## 핵심 개념: Feature Design (FD)

코드 작성의 대부분은 **완성된 스펙**에서 시작한다. 이 스펙을 **Feature
Design(FD)** 라 부르며, 실체는 마크다운 파일이다. 각 FD는 번호가
부여되고(FD-001, FD-002, ...), 인덱스에서 추적되며, 슬래시 커맨드로 전체
생명주기를 관리한다.

300개 이상의 스펙을 손으로 만들며 발전시킨 시스템을 `/fd-init` 슬래시 커맨드로
어떤 저장소에든 부트스트랩할 수 있도록 정리했다.

## 워크플로우: 3개 윈도우 체계

### PM 윈도우

- `/fd-status`로 활성·대기 중인 FD 확인
- `/fd-new`로 새 아이디어 등록 또는 백로그 정리

### Planner 윈도우 (새 에이전트 세션)

- `/fd-explore`로 프로젝트 컨텍스트 로딩
- FD를 설계하고, 막히면 `/fd-deep` 사용
- 설계 완료 시 FD 상태를 “Open”으로 전환

### Worker 윈도우 (새 에이전트 세션)

- `/fd-explore`로 컨텍스트를 새로 로딩
- “implement fd-14” 같은 지시 + **plan mode on**으로 Claude가 라인 수준 구현
  계획 수립
- 계획 확인 후 **accept edits on**으로 실행

## `/fd-deep` — 병렬 심층 탐색

복잡한 문제에서 `/fd-deep`은 **4개의 Opus 에이전트를 병렬로 실행**한다. GPT
Pro의 병렬 test-time compute에서 영감을 받았다. 각 에이전트는 서로 다른 각도로
탐색한다:

- **알고리즘적(Algorithmic)** 접근
- **구조적(Structural)** 접근
- **점진적(Incremental)** 접근
- **환경적(Environmental)** 접근

오케스트레이터가 각 출력을 검증하고 다음 단계를 추천한다.

## `/fd-verify` — 자기 검증

Claude는 자기가 작성한 코드의 버그를 **재점검할 때** 잘 찾는다는 관찰에서 나온
커맨드다:

1. 현재 상태를 커밋
2. 교정(Proofread) 패스 실행
3. 검증 계획(Verification Plan) 수행

## tmux 운영 팁

기본 tmux 네비게이션으로 충분하다:

| 키           | 동작                    |
| ------------ | ----------------------- |
| `Ctrl-b n/p` | 윈도우 순환             |
| `Ctrl-b ,`   | 윈도우 이름 변경        |
| `Ctrl-b c`   | 새 에이전트 윈도우 생성 |
| `Ctrl-b s`   | 세션 브라우징           |

에이전트가 **유휴(idle) 상태**가 되면 탭 색상이 바뀌도록 설정했다. 6개 이상
에이전트가 돌면 항상 입력을 기다리는 윈도우가 있다 — Planner의 설계 질문이나
Worker의 검증 대기.

## 스케일링의 한계

- **4~8개 에이전트**가 실용적 최대치
- 8개를 넘으면 각 에이전트의 상태를 추적하기 어렵고 설계 결정의 품질이 떨어진다
- 모든 것이 병렬화되지는 않는다 — 순차 의존성이 있는 피처는 worktree로 강제
  병렬화하면 머지 충돌과 혼란만 발생한다
- **원자적(atomic)이고 점진적(incremental)인 작업**을 유지하는 것이 핵심

## 테스팅 슬래시 커맨드

`/test-cli` 같은 전용 테스팅 커맨드도 만들었다. 에이전트가 실제 데이터로 라이브
쿼리·커맨드를 실행하고, 결과가 올바른지 추론한 뒤, 타임스탬프와 진단 노트가 담긴
마크다운 테이블을 작성한다. 문제 발견 시 즉석에서 조사까지 수행한다.

## 분석 및 인사이트

### 스펙이 병렬화의 전제 조건이다

병렬 에이전트의 병목은 컴퓨팅이 아니라 **명확한 작업 정의**다. FD 시스템은
에이전트에게 자율성을 부여하기 위해 인간이 먼저 명세를 완성해야 한다는 점을
정면으로 수용한다. “스펙 없이 에이전트를 풀어놓으면 결과도 없다”는 원칙이다.
이것은 [Spec-Driven Development](./spec-driven-development.md) 의 실전 구현이다.

### 인간이 오케스트레이터다

자동 오케스트레이터를 쓰지 않는다. 인간이 PM·Planner·Worker 역할을 tmux 윈도우
단위로 수동 전환하며 조율한다. 이 선택의 핵심은 **설계 결정의 품질 관리**다.
8개를 넘기면 인간의 인지 대역폭(cognitive bandwidth)이 포화되어 품질이
떨어진다는 경험적 관찰이 이를 뒷받침한다.

### `/fd-deep`의 설계: 다각도 병렬 탐색

하나의 문제를 4개 에이전트가 **서로 다른 렌즈**로 동시에 탐색하는 것은 일종의
**앙상블 추론(ensemble reasoning)** 이다. 알고리즘·구조·점진·환경이라는 네 축은
소프트웨어 설계의 트레이드오프 공간을 체계적으로 커버한다. 단일 에이전트의
편향을 상쇄하는 실용적 방법이다.

### 자기 검증의 가치

Claude는 “코드를 작성할 때”보다 “작성된 코드를 리뷰할 때” 버그를 더 잘 찾는다.
`/fd-verify`는 이 비대칭성을 시스템에 내장한다. 커밋 → 교정 → 검증이라는 3단계
파이프라인은 단순하지만, **생성과 평가를 분리**하는 것만으로도 에러율이 의미
있게 감소한다.

### 병렬화의 진짜 적은 머지 충돌이 아니라 설계 일관성이다

Worktree 기반 강제 병렬화가 위험한 이유는 머지 충돌 자체가 아니다. 서로 다른
에이전트가 **서로 다른 설계 가정** 하에 코드를 생성하면, 충돌이 없어도
아키텍처가 파편화된다. 원자적·점진적 작업 분할을 고수하는 것은 코드 통합의
문제가 아니라 **설계 통합의 문제**를 해결하는 전략이다.

### 에이전트 수의 경험적 상한: 인지 부하 이론과의 접점

4~8개라는 상한은 Miller의 매직 넘버(7±2)와 거의 일치한다. 각 에이전트의 상태가
인간 작업 기억의 한 슬롯을 차지한다면, 에이전트 수의 물리적 한계는 GPU가 아니라
**인간 인지의 채널 용량**이다. 자동 오케스트레이터가 이 병목을 해소할 수 있지만,
현재 수준에서는 설계 결정의 위임이 곧 품질 저하를 의미한다.

## File-based Planning Workflow와의 연계

FD 시스템과 [File-based Planning Workflow](./file-based-planning-workflow.md) 는
같은 직관에서 출발한다: **파일 시스템이 에이전트의 영구 메모리다.** 하지만 두
시스템은 서로 다른 문제를 풀며, 결합할 때 비로소 완전해진다.

### “무엇을”과 “어떻게”의 분리

FD(Feature Design)는 **“무엇을” 만들지** 정의하는 스펙이다. File-based
Planning의 3-File Pattern(`tasks.md`, `findings.md`, `progress.md`)은 **“어떻게”
진행되는지** 과정을 추적한다. 이 관계는 Spec-Driven Development와 File-based
Planning의 관계와 정확히 동형(isomorphic)이다:

| 관심사    | FD 시스템              | 3-File Pattern          |
| --------- | ---------------------- | ----------------------- |
| 방향      | Top-down (스펙 → 구현) | Bottom-up (탐색 → 기록) |
| 시점      | 작업 **전**에 완성     | 작업 **중**에 갱신      |
| 산출물    | FD-001.md (번호 스펙)  | tasks/findings/progress |
| 주요 질문 | “무엇을 만들 것인가?”  | “지금 어디까지 왔는가?” |

FD가 방향타라면, 3-File Pattern은 항해 일지다. FD 없이 3-File Pattern만 쓰면
방향 없는 탐색이 되고, 3-File Pattern 없이 FD만 쓰면 실행 과정의 학습이
휘발된다.

### 병렬 에이전트에서 3-File Pattern의 역할

Schipper의 시스템에서 각 Worker 에이전트는 **독립된 세션**으로 실행된다.
컨텍스트가 리셋되면 작업 내용을 잊어버리는 문제 — File-based Planning이 풀고자
했던 바로 그 문제 — 가 병렬 환경에서 N배로 증폭된다.

**단일 에이전트의 기억 문제:**

- 컨텍스트 리셋 → 작업 내용 망각
- 긴 작업 중 원래 목표 상실
- 실패한 시도가 추적되지 않아 같은 실수 반복

**병렬 에이전트의 기억 문제 (N배 증폭):**

- N개 에이전트가 **동시에** 컨텍스트를 잃을 수 있음
- 에이전트 간 발견사항이 공유되지 않으면 **같은 삽질을 N번 반복**
- 한 에이전트의 설계 결정이 다른 에이전트에 전파되지 않으면 아키텍처가 파편화

3-File Pattern을 FD 단위로 배치하면 이 문제를 완화할 수 있다. 각 FD-XXX
디렉토리에 자체 `findings.md`와 `progress.md`를 두면, Worker 에이전트가 세션을
재개할 때 해당 FD의 컨텍스트를 즉시 복구할 수 있다.

### FD 인덱스 = tasks.md의 프로젝트 수준 확장

3-File Pattern의 `tasks.md`는 **단일 프로젝트의 단계별 진행**을 추적한다. FD
시스템의 인덱스(FD-001~FD-300+)는 이것을 **프로젝트 수준의 작업 백로그**로
확장한 것이다. `/fd-status`는 사실상 프로젝트 전체의 `tasks.md`를 조회하는
명령이다.

| 스케일         | 추적 도구            | 관리 방식           |
| -------------- | -------------------- | ------------------- |
| 단일 작업 내부 | `progress.md`        | 세션마다 수동 갱신  |
| 피처 단위      | `tasks.md` (Phase별) | Phase 전환 시 갱신  |
| 프로젝트 전체  | FD 인덱스            | `/fd-status`로 조회 |

이 3단계 스케일링은 에이전트의 컨텍스트 윈도우 한계를 우회하는 전략이다.
에이전트가 한 번에 볼 수 있는 범위는 제한적이지만, 적절한 추상화 수준의 파일을
참조함으로써 필요한 깊이의 정보에만 접근한다.

### `/fd-deep`과 findings.md: 탐색 결과의 구조화

`/fd-deep`이 4개 에이전트의 병렬 탐색 결과를 수집하는 과정은, 3-File Pattern의
`findings.md`가 기술적 발견사항을 구조화하는 것과 본질적으로 같다. 차이점은
**탐색 주체의 수**뿐이다:

- 3-File Pattern: 1개 에이전트가 순차적으로 발견 → 기록
- `/fd-deep`: 4개 에이전트가 병렬로 발견 → 오케스트레이터가 통합 → 기록

`/fd-deep`의 출력을 `findings.md` 형식으로 정규화하면, 탐색 결과가 후속
에이전트의 컨텍스트로 자연스럽게 유입된다. 이것은
[컨텍스트 엔지니어링](./agent-skills-for-context-engineering.md) 에서 말하는
**Progressive Disclosure** — 필요한 정보를 필요한 시점에 제공하는 원칙 — 의 파일
기반 구현이다.

### 5-Question Reboot Check의 병렬 변형

File-based Planning의 `progress.md`에는 세션 재개 시 컨텍스트를 복구하는
**5-Question Reboot Check**가 있다:

1. 현재 어느 단계인가?
2. 다음에 할 일은?
3. 목표는?
4. 지금까지 배운 것?
5. 완료한 작업은?

병렬 에이전트 환경에서 이 질문은 **에이전트 단위**로 변형된다:

1. 이 에이전트는 어떤 FD를 작업 중인가?
2. 다른 에이전트와 겹치는 파일이 있는가?
3. 이 FD의 설계 제약은 무엇인가?
4. 이전 에이전트가 남긴 findings는 무엇인가?
5. 현재 FD의 검증 기준은 무엇인가?

`/fd-explore`가 프로젝트 컨텍스트를 로딩하는 것은 이 Reboot Check를 자동화한
것이다.

### Errors Encountered의 전략적 가치

3-File Pattern의 `tasks.md`에 포함된 **Errors Encountered** 테이블은 단일
에이전트에서도 유용하지만, 병렬 환경에서는 결정적이다. 에이전트 A가 겪은
`npm install 실패` 같은 문제를 에이전트 B가 반복하지 않으려면, 에러 기록이
**공유 파일 시스템**에 즉시 반영되어야 한다.

Schipper가 `/fd-verify`에서 “현재 상태를 커밋”하는 첫 단계를 두는 이유도 여기에
있다. 커밋은 에러 기록을 포함한 모든 상태를 **다른 에이전트가 참조 가능한
형태**로 고정하는 행위다.

## 관련 패턴과의 교차 분석

### “코드는 거의 공짜다”와의 접점

[에이전틱 엔지니어링 패턴 #1](./agentic-engineering-patterns-1-1-code-is-cheap.md)
은 코딩 에이전트로 인해 코드 작성 비용이 거의 0에 수렴한다고 주장한다. FD
시스템은 이 전제 위에서 작동한다. 코드 생성이 공짜라면, **가치의 원천은 “무엇을
만들지”를 정의하는 스펙**으로 이동한다. 300개 이상의 FD를 작성한 Schipper의
경험이 이를 증명한다 — 가장 많은 시간과 주의를 쏟는 곳은 코드가 아니라 마크다운
스펙이다.

개발자의 역할이 “코드 작성자”에서 “품질 판단자”로 전환되는 패러다임에서, FD
시스템은 그 판단의 매체를 코드 리뷰에서 **스펙 리뷰**로 앞당긴다. 코드가
생성되기 전에 설계를 검증하는 것이 생성된 코드를 검증하는 것보다 훨씬 비용
효율적이다.

### Red/Green TDD와 `/fd-verify`의 구조적 유사성

[에이전틱 엔지니어링 패턴 #2](./agentic-engineering-patterns-2-1-red-green-tdd.md)
의 Red/Green TDD는 “테스트 실패 확인 → 구현 → 테스트 통과 확인”의 3단계다.
`/fd-verify`의 “커밋 → 교정 → 검증”과 구조가 동형이다:

| 단계 | Red/Green TDD     | `/fd-verify`          |
| ---- | ----------------- | --------------------- |
| 1    | 테스트 작성 (Red) | 현재 상태 커밋 (고정) |
| 2    | 구현 (Green)      | 교정 패스 (Proofread) |
| 3    | 테스트 통과 확인  | 검증 계획 수행        |

둘 다 **“이것이 올바른가?”를 생성 과정과 분리된 단계에서 묻는다**는 점이
핵심이다. TDD가 코드 수준의 검증이라면, `/fd-verify`는 피처 수준의 검증이다.
양쪽을 결합하면 코드 수준과 피처 수준에서 이중으로 검증하는 체계가 된다.

### 골빈해커 프롬프팅 플로우의 “검토 12단계”와의 관계

[골빈해커의 프롬프팅 플로우](./golbin-agent-prompting-flow.md) 는 18단계 중
구현이 1단계, 검토가 12단계다. 이 극단적 비율은 `/fd-deep`과 `/fd-verify`의 설계
철학과 정확히 공명한다:

- `/fd-deep`: **구현 전** 4개 에이전트로 **다관점 탐색** (골빈 Phase 1의 계획
  검증에 대응)
- `/fd-verify`: **구현 후** 교정과 검증 수행 (골빈 Phase 3의 다층 검토에 대응)

골빈 플로우가 “검토 관점을 명시적으로 지정해야 AI가 해당 관점에 집중한다”고
말하는 것은, `/fd-deep`이 각 에이전트에 알고리즘·구조·점진·환경이라는 **명시적
렌즈**를 부여하는 것과 같은 원리다. “일반적으로 검토해줘”는 깊이 있게 보지
않지만, “구조적 관점에서 검토해줘”는 집중한다.

### 에이전틱 소프트웨어 레벨과의 위치

[에이전틱 소프트웨어의 5단계](./agentic-software-levels.md) 에서 FD 시스템은
어디에 위치하는가?

- **Level 1** (도구를 갖춘 에이전트): 각 Worker 윈도우
- **Level 2** (저장소와 지식): FD 파일 + 3-File Pattern이 “코드베이스 밖의
  중요한 컨텍스트”를 제공
- **Level 4** (멀티 에이전트 팀): PM·Planner·Worker 역할 분리

주목할 점은 **Level 3(메모리와 학습)을 의도적으로 건너뛴다**는 것이다. 자동 학습
대신 FD 파일에 수동으로 지식을 기록한다. 이것은 “Level 1에서 시작하라”는 원칙의
변형이다 — 단순한 방법이 동작하는 한, 복잡한 자동화를 도입하지 않는다. FD
시스템의 300개 스펙이 증명하듯, 마크다운 파일의 수동 관리는 놀라울 정도로 오래
버틴다.

### AI 코딩 에이전트 가이드라인과의 정합성

[AI 코딩 에이전트 가이드라인](./ai-coding-agent-guidelines.md) 의 핵심 원칙과 FD
시스템의 대응:

| 가이드라인 원칙       | FD 시스템의 구현        |
| --------------------- | ----------------------- |
| Smallest Blast Radius | 원자적·점진적 FD 분할   |
| Leverage Existing     | `/fd-explore` 컨텍스트  |
| Prove It Works        | `/fd-verify` 검증 루프  |
| Plan Mode Default     | Worker의 plan mode on   |
| Self-Improvement Loop | FD의 Errors Encountered |
| Stop-the-Line Rule    | 유휴 탭 색상 변경 알림  |

특히 **Stop-the-Line Rule**(예상치 못한 실패 시 즉시 중단하고 보존)과 tmux의
유휴 탭 색상 변경은 같은 문제를 서로 다른 층위에서 푸는 것이다. 하나는 에이전트
내부 규칙이고, 다른 하나는 인간에게 보내는 시각적 신호다.

### 컨텍스트 엔지니어링 관점에서 본 FD 시스템

[컨텍스트 엔지니어링](./agent-skills-for-context-engineering.md) 의 핵심 개념인
**주의 예산(Attention Budget)** 으로 FD 시스템을 분석하면:

**컨텍스트 절약 전략:**

- 각 에이전트 세션을 **새로 시작**한다. 긴 대화의 Lost-in-the-Middle 문제를 원천
  차단
- `/fd-explore`로 **필요한 컨텍스트만** 선택적 로딩. Attention Saturation 방지
- FD 단위로 작업을 분할하여 **하나의 에이전트가 하나의 관심사에만 집중**. 주의
  분산 최소화

**컨텍스트 낭비 요인:**

- 에이전트 간 정보 공유가 파일 시스템 경유라서 실시간성이 떨어짐
- `/fd-deep`의 4개 에이전트 출력을 통합하는 과정에서 오케스트레이터의 컨텍스트
  윈도우에 부하 발생

이것은 컨텍스트 엔지니어링의 **Platform Agnosticism** 원칙 — Claude Code, Cursor
등에 모두 적용 가능한 설계 — 의 실천이기도 하다. FD 시스템은 특정 IDE나 에이전트
프레임워크에 의존하지 않는다. 마크다운과 tmux만 있으면 된다.

## 종합: FD 시스템이 드러내는 설계 원칙

| 원칙                               | 근거                      |
| ---------------------------------- | ------------------------- |
| 스펙이 코드보다 먼저다             | SDD, FD                   |
| 파일 시스템이 기억이다             | 3-File Pattern, FD 인덱스 |
| 생성과 평가는 분리한다             | `/fd-verify`, TDD         |
| 검토 관점은 명시적으로 부여한다    | `/fd-deep`, 골빈 플로우   |
| 인간 인지가 병렬화의 상한이다      | Miller 7±2, 4~8 에이전트  |
| 단순한 방법이 실패할 때만 복잡하게 | Level 1 원칙, 마크다운    |
| 원자적 작업이 설계 일관성을 지킨다 | Smallest Blast Radius     |

## 참고 자료

- [How I run 4–8 parallel coding agents with tmux and Markdown specs — Manuel Schipper](https://schipper.ai/posts/parallel-coding-agents/)
- [Hacker News Discussion](https://news.ycombinator.com/item?id=47218318)
- [ComposioHQ/agent-orchestrator](https://github.com/ComposioHQ/agent-orchestrator)
  — 에이전트·런타임·트래커에 독립적인 오케스트레이터
- [andyrewlee/amux](https://github.com/andyrewlee/amux) — 병렬 코딩 에이전트를
  위한 TUI(tmux 세션 기반)

## 관련 문서

- [File-based Planning Workflow](./file-based-planning-workflow.md)
- [Spec-Driven Development](./spec-driven-development.md)
- [에이전틱 엔지니어링 패턴 #1: 코드는 거의 공짜다](./agentic-engineering-patterns-1-1-code-is-cheap.md)
- [에이전틱 엔지니어링 패턴 #2: Red/Green TDD](./agentic-engineering-patterns-2-1-red-green-tdd.md)
- [에이전틱 소프트웨어의 5단계](./agentic-software-levels.md)
- [골빈해커의 코딩 에이전트 프롬프팅 플로우](./golbin-agent-prompting-flow.md)
- [에이전트 스킬: 컨텍스트 엔지니어링](./agent-skills-for-context-engineering.md)
- [AI 코딩 에이전트 가이드라인](./ai-coding-agent-guidelines.md)
