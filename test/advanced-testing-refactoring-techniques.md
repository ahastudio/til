# Advanced Testing and Refactoring Techniques

Emily Bache (2018-11-20, Eficode):
<https://www.eficode.com/blog/advanced-testing-refactoring-techniques>

어려운 레거시 코드를 상속받으면 생산적이 되기까지
수 주가 걸린다. 올바른 도구와 사용법을 알면
상황이 크게 달라진다. Emily Bache가 Gilded Rose
Kata를 소재로 제작한 3부작 스크린캐스트 시리즈.
Llewellyn Falco에게 배운 접근법을 크레딧한다.

3부작 구성:

1. Approval Testing, Coverage, Mutation Testing
2. Lift-Up Conditional
3. Replace Conditional with Polymorphism

## 요약

### 배경: Gilded Rose Kata

Terry Hughes가 원래 설계하고
Emily Bache가 코드를 다듬어 더 좋은 연습 문제로
만든 리팩터링 카타(kata)다.
여러 프로그래밍 언어로 시작 코드를 번역하여
GitHub에 공개했다. 5년 만에 50명 이상의
기여자와 800개 이상의 포크를 기록했다.

Gilded Rose 여관이 취급하는 마법 아이템의
품질(quality)을 관리하는 코드를 다룬다.
새 기능은 "Conjured" 아이템 지원이다.
복잡하게 얽힌 조건문으로 이루어진 레거시 코드에
테스트를 추가하고, 정리한 뒤, 새 기능을 구현하는
현실적 시나리오를 연습한다.

> 이 연습의 매력은 엉뚱한 시나리오와
> 처음 코드의 극도로 끔찍한 상태에서 온다.
> 리팩터링을 잘 해내면 실제로 깔끔해지는데,
> 그게 아주 만족스럽다.

핵심 제약: 코드가 무엇을 하는지 모르는 상태에서
시작한다. 이것이 현실의 레거시 코드와 동일하다.

### Llewellyn Falco의 세 가지 기법

Falco는 레거시 코드를 "읽거나 이해하지 않고도"
다룰 수 있는 세 가지 기법을 제시한다.
이 세 기법은 단독으로도 유용하지만,
조합했을 때 "불가능한 작업을 사소하게" 만든다.

#### 1. Combination Testing(조합 테스팅)

100% 테스트 커버리지를 빠르게 달성하는 기법.

**핵심 원리:**
코드가 무엇을 하는지 모르므로 기대값을 미리
정의할 수 없다. 대신 코드를 실행하고, 현재
동작을 "올바른 것"으로 승인(approve)한 뒤,
코드의 모든 분기를 실행하는 시나리오를 만든다.

**Approval Testing(승인 테스팅) 워크플로우:**

1. 코드를 블랙박스로 취급하고 실행한다
2. 출력을 캡처하여 "승인된 결과"로 저장한다
3. 코드 커버리지를 확인하여 미실행 분기를 찾는다
4. 입력 조합을 추가하여 미실행 분기를 커버한다
5. 100% 커버리지에 도달할 때까지 반복한다

**CombinationApprovals:**
ApprovalTests 라이브러리의 핵심 기능.
입력 파라미터의 모든 조합을 자동 생성하여,
한 번의 테스트로 수백 개의 케이스를 커버한다.

```
verify_all_combinations(
    update_quality,
    [names],      # 아이템 이름 배열
    [sell_ins],   # 판매 기한 배열
    [qualities]   # 품질 값 배열
)
```

적은 노력으로 240개 이상의 테스트 케이스를
한 번에 생성할 수 있다.

#### 2. Code Coverage as Guidance(커버리지 가이드)

커버리지를 "목표"가 아닌 "안내자"로 사용한다.

**두 가지 활용법:**

- **입력 결정**: 어떤 입력 조합이 미실행 분기를
  커버하는지 커버리지 리포트가 알려준다
- **삭제 결정**: 어떤 조합으로도 실행되지 않는
  코드는 죽은 코드(dead code)일 가능성이 높다

**Mutation Testing(변이 테스팅)으로 검증:**
100% 커버리지가 진정한 테스트를 보장하지 않는다.
변이 테스팅은 코드의 각 줄을 의도적으로 변경하여
테스트가 실패하는지 확인한다.

- 테스트가 실패하면: 해당 줄이 제대로 테스트됨
- 테스트가 통과하면: 입력 조합이 부족하므로 추가

#### 3. Provable Refactorings(증명 가능한 리팩터링)

테스트 없이도 안전하다고 증명할 수 있는
코드 변환 기법.

**증명 방법:**

- **자동화된 도구 리팩터링**: IDE의 리팩터링
  기능을 사용하여 도구가 안전성을 보장
- **스크립트화된 수동 리팩터링**: 컴파일러를
  활용하여 각 단계의 안전성을 검증

**Arlo의 커밋 표기법과 연결:**

| 접두사 | 의미                         |
|--------|------------------------------|
| `r`    | Provable Refactor (증명됨)   |
| `!!`   | 증명 불가능한 리팩터링       |
| `a`    | Automated (자동화 도구 사용) |
| `t`    | Test only (테스트만 변경)    |
| `F`    | Feature (기능 추가)          |
| `B`    | Bug (버그 수정)              |

각 커밋의 위험 수준을 명시적으로 표현하여,
리뷰어가 주의를 기울여야 할 지점을 안내한다.

### Emily Bache의 리팩터링 시연

Falco의 세 기법으로 테스트를 확보한 뒤,
Emily Bache가 두 가지 리팩터링을 시연한다.

#### Lift-Up Conditional(조건문 끌어올리기)

Emily Bache가 명명하고 Falco에게 배운 기법.
Fowler의 "Remove Flag Argument"와 관련된다.

**핵심 원리:**
코드 전체에 흩어진 중복 조건을 찾아
최상위로 "끌어올려" 각 조건이 한 곳에서만
존재하도록 만든다.

**단계별 절차:**

1. 테스트가 모두 통과하는 상태에서 시작
2. 중복 조건이 포함된 코드 블록 전체를 복사
3. `if/else`로 감싸고, 끌어올릴 조건을 설정
4. `if` 분기에서 해당 조건을 `true`로 치환
5. `else` 분기에서 해당 조건을 `false`로 치환
6. 테스트 통과 확인
7. `if(true)`와 `if(false)`를 단순화
8. 테스트 통과 확인
9. 결과가 더 단순해졌는지 평가 (아니면 되돌림)

**변환 예시:**

```
// Before: 조건 b가 두 곳에 중복
if (a) {
    if (b) { a_true_b_true(); }
    else   { a_true_b_false(); }
} else {
    if (b) { a_false_b_true(); }
    else   { a_false_b_false(); }
}

// After: 조건 b를 최상위로 끌어올림
if (b) {
    if (a) { a_true_b_true(); }
    else   { a_false_b_true(); }
} else {
    if (a) { a_true_b_false(); }
    else   { a_false_b_false(); }
}
```

#### Replace Conditional with Polymorphism

Martin Fowler의 *Refactoring*에서 소개된 고전적
기법. Lift-Up Conditional로 조건문을 정리한 뒤,
각 조건 분기를 서브클래스로 추출한다.

**단계별 절차:**

1. 조건문이 독립된 메서드에 있는지 확인
2. 각 분기에 대응하는 서브클래스 계층 구조 생성
3. 부모 클래스에 추상 메서드 정의
4. 각 분기의 로직을 해당 서브클래스로 이동
5. 조건문을 다형성 메서드 호출로 대체

**효과:**

- 새 타입 추가 시 기존 코드 수정 불필요
  (Open/Closed Principle)
- 각 타입의 로직이 한 클래스에 응집
- 조건문의 복잡도가 클래스 구조로 분산

### 전체 워크플로우

Falco와 Bache가 제시하는 레거시 코드 정복 순서:

```
1. Test    → Combination + Approval Testing
             으로 100% 커버리지 달성
2. Verify  → Mutation Testing으로
             테스트 품질 검증
3. Lift    → Lift-Up Conditional로
             조건문 정리
4. Split   → Replace Conditional with
             Polymorphism으로 클래스 분리
5. Add     → 새 기능을 쉽게 추가
```

### Mob Programming과 Learning Hour

이 기법들은 Eficode에서 실천하는
모브 프로그래밍(Mob Programming) 환경에서
전파되었다. Learning Hour는 매일 한 시간씩
새로운 기법을 학습하는 세션으로,
Falco나 Bache 같은 코치가 이끈다.

Samman Technical Coaching이라 불리는 이 방법은
두 가지 활동으로 구성된다:

- **Learning Hour**: 기법 시연 후 짝 프로그래밍으로
  직접 연습
- **Ensemble Working**: 실제 프로덕션 코드에
  기법 적용

---

## 분석

### "읽지 않고 리팩터링한다"는 역설

전통적 접근: 코드를 읽고 → 이해하고 →
테스트를 작성하고 → 리팩터링한다.

Falco의 접근: 코드를 실행하고 → 동작을 포획하고
→ 리팩터링하고 → 그제서야 이해한다.

이것은 단순한 순서 변경이 아니다.
"이해"를 전제 조건에서 결과물로 전환한 것이다.

코드를 읽어서 이해하는 것은 인간의 인지 능력에
의존한다. 복잡한 레거시 코드에서 이 능력은
급격히 떨어진다. 반면 "실행하고 관찰"하는 것은
기계적이고 확장 가능하다.

### Approval Testing의 인식론적 전환

전통적 테스트: "코드가 이것을 해야 한다"
(당위, specification)

Approval Testing: "코드가 이것을 한다"
(사실, characterization)

이 전환이 강력한 이유는 레거시 코드에서
"당위"를 아는 사람이 없는 경우가 대부분이기
때문이다. 원래 작성자는 떠났고, 문서는 낡았고,
요구사항은 변했다.

Approval Testing은 이 인식론적 공백을 우회한다.
"올바름"을 정의하는 대신,
"현재 동작의 변경"을 감지하는 데 집중한다.

이것은 Michael Feathers의 레거시 코드 정의와
정확히 일치한다:

> 레거시 코드란 테스트가 없는 코드다.

Approval Testing은 이 정의를 실용적으로 해결한다.

### Provable Refactoring과 신뢰의 계층

코드 변경의 신뢰 수준을 계층화하면:

| 신뢰 수준 | 방법                       |
|-----------|----------------------------|
| 최고      | 자동화 도구 리팩터링       |
| 높음      | 컴파일러 검증 수동 단계    |
| 중간      | 테스트로 검증된 변경       |
| 낮음      | 사람의 판단에 의존한 변경  |

Falco는 가능한 한 높은 신뢰 수준에서
작업할 것을 권장한다. "테스트가 통과하니까
안전하다"보다 "이 변환은 수학적으로
동치(equivalent)다"가 더 강력하다.

### Lift-Up Conditional의 기계적 아름다움

이 기법의 핵심 강점은 판단이 필요 없다는 것이다.

1. 복사한다
2. `true`/`false`로 치환한다
3. 단순화한다
4. 테스트를 돌린다

각 단계가 기계적이므로 실수할 여지가 작다.
그리고 각 단계 사이에 테스트를 실행하므로,
실수하더라도 즉시 감지된다.

이것은 "작은 단계로, 항상 테스트 통과 상태를
유지하며" 리팩터링하라는 원칙의 구체적 실현이다.

### 세 기법의 시너지 구조

```
Combination Testing ─── 안전망 구축
        │
        ├── Code Coverage ── 방향 제시
        │
        └── Mutation Testing ── 안전망 검증
                │
Provable Refactoring ── 안전한 변환
        │
        ├── Lift-Up Conditional ── 구조 정리
        │
        └── Replace Conditional ── 설계 개선
                    with Polymorphism
```

이 구조에서 각 기법은 다음 기법의 전제 조건을
충족시킨다. Combination Testing 없이
Lift-Up Conditional은 위험하고,
Lift-Up Conditional 없이
Replace Conditional with Polymorphism은
적용할 수 없다.

---

## 인사이트

### "코드를 읽지 마라"는 반직관적 지혜

프로그래머의 첫 번째 본능은 코드를 읽는 것이다.
그러나 복잡한 레거시 코드를 읽는 행위 자체가
위험하다. 잘못된 이해를 형성하고,
그 이해에 기반한 변경이 버그를 만든다.

Falco의 접근은 이 본능을 뒤집는다:
"이해하기 전에 안전망을 치고,
리팩터링 과정에서 이해가 자연스럽게 형성되게
하라."

이것은 TDD의 "Red-Green-Refactor"와
구조적으로 동일하다.
테스트가 먼저, 이해가 나중이다.

### 레거시 코드 리팩터링의 경제학

전통적 접근의 비용 구조:

- 코드 이해: 높음 (불확실)
- 테스트 작성: 높음 (사양서 필요)
- 리팩터링: 중간
- 합계: 매우 높음 → "그냥 두자"

Falco/Bache 접근의 비용 구조:

- Combination Testing: 낮음 (기계적)
- 커버리지 확인 + 변이 테스팅: 낮음 (도구 지원)
- Provable Refactoring: 낮음 (기계적)
- 합계: 낮음 → "지금 하자"

이 비용 차이가 레거시 코드를 "방치의 대상"에서
"점진적 개선의 대상"으로 전환시킨다.

### AI 시대에 이 기법들의 가치가 올라간다

AI 코딩 도구는 Combination Testing의
입력 조합 생성, Approval Testing의 출력 검증,
커버리지 분석을 자동화할 수 있다.

그러나 핵심 판단은 여전히 인간의 몫이다:

- 어떤 조건을 끌어올릴 것인가
- 어떤 클래스 계층이 적절한가
- 리팩터링의 방향은 무엇인가

기법을 아는 인간 + 실행을 돕는 AI의 조합이
레거시 코드 리팩터링의 비용을 한 차원 더 낮출
것이다.

### Kata의 교육적 가치

Gilded Rose 같은 카타가 효과적인 이유:

1. **현실적 제약**: 코드를 모르는 상태에서 시작
2. **안전한 실패**: 프로덕션이 아니므로
   실수해도 괜찮다
3. **반복 가능**: 같은 카타를 다른 언어,
   다른 접근으로 반복 연습
4. **점진적 복잡도**: 기법을 하나씩 적용하며
   효과를 체감

Learning Hour에서 매일 한 시간씩 연습하는
Samman 방식은 이 카타의 가치를 극대화한다.
기법은 "아는 것"이 아니라 "손에 익는 것"이다.

### 테스트와 리팩터링의 공진화

이 글의 가장 깊은 통찰:
테스트와 리팩터링은 별개의 활동이 아니라
상호 강화하는 순환이다.

```
테스트 → 리팩터링을 안전하게 만듦
  ↑                            ↓
  └── 리팩터링 → 더 나은 테스트 가능
```

Approval Testing으로 시작한 조잡한 테스트가
리팩터링 후에는 각 클래스의 단위 테스트로
진화한다. 리팩터링이 코드를 명확하게 만들면,
비로소 "코드가 무엇을 해야 하는지" 이해하게 되고,
Approval Test를 진정한 Specification Test로
대체할 수 있다.

---

## 관련 문서

- [Tests Are The New Moat](
  ./tests-are-the-new-moat.md)
- [Test Pyramid](./test-pyramid.md)

## 참고

- [Advanced Testing and Refactoring Techniques
  - Eficode Blog](
  https://www.eficode.com/blog/advanced-testing-refactoring-techniques)
- [Lift Up Conditional - Samman Coaching](
  https://sammancoaching.org/refactorings/lift_up_conditional.html)
- [Gilded Rose Refactoring Kata - GitHub](
  https://github.com/emilybache/GildedRose-Refactoring-Kata)
- [Arlo's Commit Notation - GitHub](
  https://github.com/RefactoringCombos/ArlosCommitNotation)
- [Cutting Code Quickly - Llewellyn Falco](
  https://www.classcentral.com/course/youtube-cutting-code-quickly-from-0-to-cleanly-refactored-100-tested-code-llewellyn-falco-132984)
- [Approval Testing on Legacy Code
  - Nicolas Carlo](
  https://www.nicoespeon.com/en/2019/01/approval-testing-on-legacy-code/)
- [Replace Conditional with Polymorphism
  - Refactoring Guru](
  https://refactoring.guru/replace-conditional-with-polymorphism)
