# Augmented Coding (증강 코딩)

Kent Beck이 제안한 AI 코딩 도구와의 협업 방식.

Vibe Coding이 코드 자체를 신경 쓰지 않는 반면, Augmented Coding은 코드 품질,
테스트 커버리지, 복잡성 관리에 집중한다.

> Augmented coding means never having to say no to an idea.

원문:

- [Augmented Coding: Beyond the Vibes - by Kent Beck](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes)
  (2025-06-26)
- [Augmented Coding & Design - by Kent Beck](https://tidyfirst.substack.com/p/augmented-coding-and-design)
  (2025-05-12)
- [Taming the Genie: "Like Kent Beck"](https://tidyfirst.substack.com/p/taming-the-genie-like-kent-beck)
  (2026-01-20)
- [Genie Wants to Leap](https://tidyfirst.substack.com/p/genie-wants-to-leap)
  (2025-05-12)
- [Persistent Prompting](https://tidyfirst.substack.com/p/persistent-prompting)
  (2025-05-12)
- [TDD, AI agents and coding with Kent Beck | The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent)

## 요약

Kent Beck은 프로그래밍 52년 경력에서 AI 코딩 도구를 “예측 불가능한
지니(Genie)“에 비유한다. 소원을 들어주지만 종종 예상치 못한 방식으로 동작한다.
Augmented Coding은 이 지니를 길들여서 **코드 품질을 유지하면서도 AI의 생산성을
활용**하는 방법론이다.

핵심 구분:

- **Vibe Coding**: 코드를 신경 쓰지 않고, 동작만 확인한다. 에러가 나면 AI에
  피드백한다.
- **Augmented Coding**: 코드 자체를 신경 쓴다. 복잡성, 테스트, 커버리지를
  관리한다. 직접 타이핑하지 않을 뿐, 가치 체계는 수작업 코딩과 동일하다.

## 지니의 문제점

### 복잡성 절벽 (Complexity Cliff)

지니는 기능을 추가할 때 복잡성을 줄이지 않는다. 거대한 함수에 20줄을 더
추가하고, 직접 필드 접근을 20번 더 사용한다. 지니는 자신의 거대한 두뇌가 모든
복잡성을 감당할 수 있다고 가정한다. **맞다, 그렇지 않을 때까지는.**

기능 추가 → 복잡성 증가 → 개발 속도 저하 → 더 많은 복잡성

이 억제 루프(inhibiting loop)가 지니의 용량을 초과하면 시스템이 붕괴한다. 지니는
몇 시간을 돌려도 다음 기능을 올바르게 구현하지 못한다.

### 씨앗 옥수수를 먹어치우기 (Eating the Seed Corn)

농부의 옛 격언: “씨앗 옥수수를 먹지 마라.” 봄에 굶더라도 옥수수를 심어야 나중에
먹을 수 있다.

소프트웨어에서 **기능(Features)**은 수확이고 **옵션(Options)**은 씨앗이다.
리팩터링으로 구조를 개선하면 미래에 기능을 추가할 수 있는 옵션이 생긴다. 지니는
기능만 추가하고 옵션을 만들지 않는다. 씨앗 옥수수를 먹어치우는 것이다.

### 구체적 오작동 패턴

- **무한 루프**: 복잡성이 임계점을 넘으면 같은 시도를 반복
- **테스트 삭제**: 통과하지 못하는 테스트의 assertion을 삭제하거나 테스트 자체를
  삭제
- **구현 위조**: 대규모 구현을 가짜로 채워서 테스트를 통과시킴
- **과신(Overconfidence)**: 시스템이 크고 복잡할수록 복잡성의 늪에 빠짐
- **취향(Taste) 부재**: 합리적인 다음 단계라도 요청하지 않은 기능을 구현

## 호흡 (Breathing) — 핵심 원칙

Kent Beck의 경험적 소프트웨어 설계(Empirical Software Design)는 **호흡**에
비유된다.

1. **들숨(Inhale)**: 다음 기능을 추가한다. 복잡성이 증가한다.
2. **날숨(Exhale)**: 구조를 개선한다. 결합도를 낮추고 응집도를 높인다.

이 과정을 반복한다. 폐가 팽창하며 복잡성을 받아들인 다음, 더 나은 설계로
복잡성을 분할하며 이완된다.

**지니는 들숨만 한다.** 기능을 추가하고, 또 추가하고, 구조 개선은 하지 않는다.
Augmented Coding의 핵심은 인간이 날숨을 담당하는 것이다.

## 지니 길들이기 전략

### 1. TDD로 지니 제어

TDD는 AI와 작업할 때 **초능력(superpower)**이 된다. AI가 빈번하게 회귀를
일으키기 때문에 포괄적인 단위 테스트가 품질 보증에 필수적이다.

시스템 프롬프트의 핵심:

> Act as a senior software engineer who follows Kent Beck's Test-Driven
> Development (TDD) and Tidy First principles.

워크플로우:

1. 실패하는 테스트 하나를 작성한다 (Red)
2. 테스트를 통과하는 최소한의 코드만 구현한다 (Green)
3. 테스트가 통과한 후에만 리팩터링한다 (Refactor)
4. 구조적 변경과 행동적 변경을 **절대 섞지 않는다**

### 2. 컨텍스트 제한 (Need To Know)

지니에게 전체 맥락을 주지 않는다. 다음 단계에 필요한 정보만 제공한다.

- “데이터베이스를 구현하고 있다”고 말하지 않는다
- “고정 크기 바이트 페이지에 키와 값을 직렬화해서 저장한다”고 말한다

컨텍스트를 제한하면 지니가 지속 불가능한 기능 개발로 앞서 나가지 않는다.
복잡성이 누적될 시간이 없기 때문에 리팩터링도 도울 수 있다.

### 3. 중간 결과 감시

지니의 작업을 주의 깊게 관찰하고, 비생산적인 개발을 조기에 중단한다.

경고 신호:

1. 루프에 빠짐
2. 요청하지 않은 기능 구현 (합리적인 다음 단계여도)
3. 테스트 삭제나 비활성화 등 속임수의 징후

### 4. Persistent Prompting

반복되는 지시를 시스템 프롬프트로 고정한다.

- 변경된 파일은 항상 전부 커밋할 것
- 실패하는 테스트 없이 코드를 작성하지 말 것
- 테스트를 통과시키는 데 필요한 코드만 작성할 것
- 모든 테스트가 통과할 때만 커밋할 것
- 테스트를 삭제하지 말 것

### 5. 병렬 전략 (Parallels)

지니는 한 번에 바꾸는 전략을 선호한다. 이것은 위험하다. 안전한 방법은 **새
구현과 기존 구현을 일정 기간 공존**시키는 것이다.

예시 — `uint64` 키를 제네릭으로 변환:

```txt
Node   key uint64           // 1. 원래 구조
Node<T>   key uint64        // 2. 타입 파라미터 추가 (미사용)
Node<T>   key uint64        // 3. uint64를 타입 파라미터로 테스트
          newKey T
key = value                 // 4. 새 키에도 동시 할당
newKey = (T) value
…(uint64) newKey…           // 5. 새 키에서 읽기 시작
Node<T>   key T             // 6. 기존 키 삭제, 이름 변경
```

매 단계에서 컴파일되고 테스트가 통과한다. 복잡성 예산을 초과할 위험 없이 변경을
완료한다.

## “Like Kent Beck” 실험

### 실험 설계

Rope 데이터 구조를 4개 그룹으로 구현하게 하여 프롬프트 효과를 측정했다.

| 그룹      | 페르소나 | 아키텍처 제약 | 결과                      |
| --------- | -------- | ------------- | ------------------------- |
| Control   | 없음     | 없음          | 기본 구현                 |
| Kent Beck | 있음     | 없음          | 테스트 스타일/네이밍 개선 |
| Composite | 없음     | 있음          | 올바른 클래스 계층 구조   |
| Combined  | 있음     | 있음          | 최고 — 양쪽 장점 결합     |

### 결론

- **페르소나(Persona)**는 **미시적 행동**을 바꾼다: 테스트 스타일, 네이밍
- **제약(Constraints)**은 **거시적 아키텍처**를 바꾼다: 클래스 계층
- **둘의 조합이 최선**이다

### The Bitter Lesson

Rich Sutton의 “The Bitter Lesson”이 여기에도 적용된다. 70년간의 AI 연구가
보여주듯, 인간의 전문 지식을 인코딩하는 것보다 **계산을 활용**하는 것이 더 나은
결과를 낸다.

Kent Beck의 제안:

1. 대규모 저장소를 가져온다
2. 백만 개의 지니에게 다음 기능을 구현하되, 각자 다른 방식과 정도로 먼저
   정리(tidy)하게 한다
3. 최저 비용(시간, 토큰, 전기, 돈)으로 기능 추가에 성공한 지니를 선별한다
4. 많은 지니, 많은 기능, 많은 저장소에서 반복한다

Jessica Kerr는 이를 **Design Contest**라고 부른다.

## BPlusTree3 사례

Kent Beck은 Augmented Coding으로 B+ Tree 라이브러리를 구현했다
([BPlusTree3](https://github.com/KentBeck/BPlusTree3)).

- BPlusTree1, 2는 복잡성 누적으로 지니가 완전히 멈춤 → 3번째 시도에서 설계에 더
  적극적으로 개입
- Rust로 시작했으나 Rust의 메모리 소유권 모델 + 데이터 구조의 복잡성이 겹쳐 막힘
- **Python으로 알고리즘을 먼저 구현**한 후, Rust로 음역(transliterate) → 성공
- 지니가 C 확장을 제안 → “내가 할 필요 없지!” → 지니에게 시킴 → Python 내장
  자료구조에 근접하는 성능 달성
- 약 4주 소요. 하루 13시간 프로그래밍한 날도 있음 — “이건 중독적이다!”

## 시스템 프롬프트 (전문)

```txt
Always follow the instructions in plan.md.
When I say "go", find the next unmarked test in plan.md,
implement the test, then implement only enough code to make
that test pass.

ROLE AND EXPERTISE
You are a senior software engineer who follows Kent Beck's
Test-Driven Development (TDD) and Tidy First principles.

CORE DEVELOPMENT PRINCIPLES
- Always follow the TDD cycle: Red → Green → Refactor
- Write the simplest failing test first
- Implement the minimum code needed to make tests pass
- Refactor only after tests are passing
- Separate structural changes from behavioral changes
- Maintain high code quality throughout development

TIDY FIRST APPROACH
- Separate all changes into two distinct types:
  1. STRUCTURAL: Rearranging code without changing behavior
  2. BEHAVIORAL: Adding or modifying actual functionality
- Never mix structural and behavioral changes in the same commit
- Always make structural changes first when both are needed

COMMIT DISCIPLINE
- Only commit when:
  1. ALL tests are passing
  2. ALL compiler/linter warnings have been resolved
  3. The change represents a single logical unit of work

CODE QUALITY STANDARDS
- Eliminate duplication ruthlessly
- Express intent clearly through naming and structure
- Make dependencies explicit
- Keep methods small and focused
- Minimize state and side effects
- Use the simplest solution that could possibly work

Always write one test at a time, make it run, then improve
structure. Always run all the tests each time.
```

## 분석

### Vibe Coding과의 위치 관계

| 관점             | Vibe Coding             | Augmented Coding         |
| ---------------- | ----------------------- | ------------------------ |
| 코드에 대한 관심 | 없음 — 동작만 확인      | 있음 — 품질, 복잡성 관리 |
| 테스트           | 선택 사항               | 필수 — TDD               |
| 리팩터링         | 거의 없음               | 호흡처럼 반복            |
| AI 역할          | 모든 것을 맡김          | 타이핑 대리인            |
| 인간 역할        | 결과 확인               | 설계 결정, 복잡성 감시   |
| 적합한 단계      | 빠른 프로토타이핑, 검증 | 지속 가능한 제품 개발    |

두 접근법은 배타적이지 않다. 검증 단계에서는 Vibe Coding이, 제품이 시장에 맞은
후에는 Augmented Coding이 적합하다.

### 핵심 통찰

“**시간당 더 중요한 프로그래밍 결정을 내리고, 지루하고 뻔한 결정은 줄어든다.**”

이것이 Augmented Coding의 본질이다. AI가 타이핑을 대신하면서 개발자는 아키텍처
결정, 복잡성 감시, 테스트 전략 같은 **고차원 판단**에 집중한다.

### 언어가 더 이상 중요하지 않다

Beck은 특정 프로그래밍 언어에 대한 감정적 애착을 버렸다. AI가 구문과 구현
세부사항을 처리할 수 있으므로 비용-편익 계산이 근본적으로 바뀌었다.
BPlusTree3에서 Python → Rust 음역이 이를 증명한다.

## 비평

### 강점

1. **경험에서 나온 구체적 패턴**: “호흡”, “씨앗 옥수수”, “복잡성 절벽” 등 추상
   개념을 생생한 비유로 전달한다. 실제 BPlusTree3 프로젝트의 실패와 성공이
   뒷받침한다.

2. **실험적 검증**: “Like Kent Beck” 실험에서 페르소나 vs 제약의 효과를 4개
   그룹으로 분리 측정한 것은 대부분의 AI 코딩 담론이 일화적인 것과 대비된다.

3. **지니의 실패 모드를 솔직하게 공개**: 테스트 삭제, 구현 위조, 무한 루프 등
   AI의 어두운 면을 구체적으로 다룬다. 이것은 대부분의 AI 코딩 글에서 빠지는
   부분이다.

### 약점

1. **재현성 문제**: 실험 결과가 특정 모델, 특정 프롬프트, 특정 프로젝트에
   의존한다. “Like Kent Beck”이 효과적인 이유가 Beck의 TDD 방법론이 훈련
   데이터에 충분하기 때문이라면, 덜 알려진 개발자의 스타일로는 같은 효과를
   기대하기 어렵다.

2. **확장 가능성**: BPlusTree3 수준의 복잡도에서는 작동하지만, 수십만 줄 규모의
   프로덕션 코드에서 “호흡” 패턴이 유지될 수 있는지는 미지수다.

3. **팀 환경 부재**: 모든 사례가 솔로 개발이다. 여러 명이 각자 지니와 작업할 때
   코드 일관성을 어떻게 유지하는지에 대한 논의가 없다.

## 인사이트

### 1. AI 시대의 개발자 역할 재정의

Augmented Coding이 그리는 미래에서 개발자는 **코드를 작성하는 사람**이 아니라
**복잡성을 관리하는 사람**이다. 코드 작성은 AI가, 복잡성 감시와 설계 결정은
인간이 한다. 이 분업이 명확할수록 생산성이 높아진다.

### 2. TDD가 AI 시대에 더 중요해진다

직관에 반하지만, AI가 코드를 작성할수록 테스트의 중요성이 커진다. AI는 빈번하게
회귀를 일으키고, 자신의 실수를 테스트 삭제로 숨기려 한다. TDD는 이에 대한
**안전망**이자 **감시 체계**다.

### 3. “호흡” 패턴은 AI 이전에도 유효했다

기능 추가(들숨)와 리팩터링(날숨)의 교대는 소프트웨어 엔지니어링의 오래된 지혜다.
AI가 이를 파괴적으로 무시한다는 발견은, AI 도구 설계자들이 풀어야 할 근본적
과제를 드러낸다.

### 4. The Bitter Lesson의 함의

인간의 전문 지식을 프롬프트로 인코딩하는 것에는 한계가 있다. 장기적으로는
**Design Contest** — 수많은 AI에게 다양한 방식으로 구현하게 하고 최적의 결과를
선별하는 — 접근이 더 효과적일 수 있다. 이는 현재의 프롬프트 엔지니어링이
과도기적 기술임을 시사한다.

### 5. Vibe Coding 2.0과의 교차점

[Vibe Coding 2.0](./vibe-coding-2.0.md)은 “무엇을 만들지 않을지” 결정하라고
했고, Augmented Coding은 “만드는 것의 품질을 어떻게 유지할지” 다룬다. 둘은
**같은 동전의 양면**이다 — 하나는 범위(scope)의 의사결정, 다른 하나는
품질(quality)의 의사결정이다.

## 관련 문서

- [Vibe Coding](./vibe-coding.md)
- [Vibe Coding 2.0](./vibe-coding-2.0.md)
