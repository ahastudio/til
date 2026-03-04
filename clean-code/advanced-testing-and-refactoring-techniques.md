# Advanced Testing and Refactoring Techniques

Emily Bache (2018-11-20, updated 2025-05-26, Eficode):
<https://www.eficode.com/blog/advanced-testing-refactoring-techniques>

어려운 레거시 코드를 상속받으면 생산적이 되기까지 수 주가 걸린다. 올바른 도구와
사용법을 알면 상황이 크게 달라진다. Emily Bache가 Gilded Rose Kata를 소재로
제작한 3부작 스크린캐스트 시리즈. Llewellyn Falco에게 배운 접근법을 크레딧한다.

3부작 구성:

1. Approval Testing, Coverage, Mutation Testing
2. Lift-Up Conditional
3. Replace Conditional with Polymorphism

## 요약

### 배경: Gilded Rose Kata

Terry Hughes가 원래 설계하고 Emily Bache가 코드를 다듬어 더 좋은 연습 문제로
만든 리팩터링 카타(kata)다. 여러 프로그래밍 언어로 시작 코드를 번역하여 GitHub에
공개했다. 5년 만에 50명 이상의 기여자와 800개 이상의 포크를 기록했다.

Gilded Rose 여관이 취급하는 마법 아이템의 품질(quality)을 관리하는 코드를
다룬다. 새 기능은 "Conjured" 아이템 지원이다. 복잡하게 얽힌 조건문으로 이루어진
레거시 코드에 테스트를 추가하고, 정리한 뒤, 새 기능을 구현하는 현실적 시나리오를
연습한다.

> 이 연습의 매력은 엉뚱한 시나리오와 처음 코드의 극도로 끔찍한 상태에서 온다.
> 리팩터링을 잘 해내면 실제로 깔끔해지는데, 그게 아주 만족스럽다.

핵심 제약: 코드가 무엇을 하는지 모르는 상태에서 시작한다. 이것이 현실의 레거시
코드와 동일하다.

### Llewellyn Falco의 세 가지 기법

Falco는 레거시 코드를 "읽거나 이해하지 않고도" 다룰 수 있는 세 가지 기법을
제시한다. 이 세 기법은 단독으로도 유용하지만, 조합했을 때 "불가능한 작업을
사소하게" 만든다.

#### 1. Combination Testing(조합 테스팅)

100% 테스트 커버리지를 빠르게 달성하는 기법.

**핵심 원리:** 코드가 무엇을 하는지 모르므로 기대값을 미리 정의할 수 없다. 대신
코드를 실행하고, 현재 동작을 "올바른 것"으로 승인(approve)한 뒤, 코드의 모든
분기를 실행하는 시나리오를 만든다.

**Approval Testing(승인 테스팅) 워크플로우:**

1. 코드를 블랙박스로 취급하고 실행한다
2. 출력을 캡처하여 "승인된 결과"로 저장한다
3. 코드 커버리지를 확인하여 미실행 분기를 찾는다
4. 입력 조합을 추가하여 미실행 분기를 커버한다
5. 100% 커버리지에 도달할 때까지 반복한다

**CombinationApprovals:** ApprovalTests 라이브러리의 핵심 기능. 입력 파라미터의
모든 조합을 자동 생성하여, 한 번의 테스트로 수백 개의 케이스를 커버한다.

```python
verify_all_combinations(
    update_quality,
    [names],      # 아이템 이름 배열
    [sell_ins],   # 판매 기한 배열
    [qualities]   # 품질 값 배열
)
```

적은 노력으로 240개 이상의 테스트 케이스를 한 번에 생성할 수 있다.

#### 2. Code Coverage as Guidance(커버리지 가이드)

커버리지를 "목표"가 아닌 "안내자"로 사용한다.

**두 가지 활용법:**

- **입력 결정**: 어떤 입력 조합이 미실행 분기를 커버하는지 커버리지 리포트가
  알려준다
- **삭제 결정**: 어떤 조합으로도 실행되지 않는 코드는 죽은 코드(dead code)일
  가능성이 높다

**Mutation Testing(변이 테스팅)으로 검증:** 100% 커버리지가 진정한 테스트를
보장하지 않는다. 변이 테스팅은 코드의 각 줄을 의도적으로 변경하여 테스트가
실패하는지 확인한다.

- 테스트가 실패하면: 해당 줄이 제대로 테스트됨
- 테스트가 통과하면: 입력 조합이 부족하므로 추가

#### 3. Provable Refactorings(증명 가능한 리팩터링)

테스트 없이도 안전하다고 증명할 수 있는 코드 변환 기법.

**증명 방법:**

- **자동화된 도구 리팩터링**: IDE의 리팩터링 기능을 사용하여 도구가 안전성을
  보장
- **스크립트화된 수동 리팩터링**: 컴파일러를 활용하여 각 단계의 안전성을 검증

**Arlo의 커밋 표기법과 연결:**

| 접두사 | 의미                         |
| ------ | ---------------------------- |
| `r`    | Provable Refactor (증명됨)   |
| `!!`   | 증명 불가능한 리팩터링       |
| `a`    | Automated (자동화 도구 사용) |
| `t`    | Test only (테스트만 변경)    |
| `F`    | Feature (기능 추가)          |
| `B`    | Bug (버그 수정)              |

각 커밋의 위험 수준을 명시적으로 표현하여, 리뷰어가 주의를 기울여야 할 지점을
안내한다.

### Emily Bache의 리팩터링 시연

Falco의 세 기법으로 테스트를 확보한 뒤, Emily Bache가 두 가지 리팩터링을
시연한다.

#### Lift-Up Conditional(조건문 끌어올리기)

Emily Bache가 명명하고 Falco에게 배운 기법. Fowler의 "Remove Flag Argument"와
관련된다.

**핵심 원리:** 코드 전체에 흩어진 중복 조건을 찾아 최상위로 "끌어올려" 각 조건이
한 곳에서만 존재하도록 만든다.

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

```javascript
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

Martin Fowler의 *Refactoring*에서 소개된 고전적 기법. Lift-Up Conditional로
조건문을 정리한 뒤, 각 조건 분기를 서브클래스로 추출한다.

**단계별 절차:**

1. 조건문이 독립된 메서드에 있는지 확인
2. 각 분기에 대응하는 서브클래스 계층 구조 생성
3. 부모 클래스에 추상 메서드 정의
4. 각 분기의 로직을 해당 서브클래스로 이동
5. 조건문을 다형성 메서드 호출로 대체

**효과:**

- 새 타입 추가 시 기존 코드 수정 불필요 (Open/Closed Principle)
- 각 타입의 로직이 한 클래스에 응집
- 조건문의 복잡도가 클래스 구조로 분산

### 전체 워크플로우

Falco와 Bache가 제시하는 레거시 코드 정복 순서:

```text
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

이 기법들은 Eficode에서 실천하는 모브 프로그래밍(Mob Programming) 환경에서
전파되었다. Learning Hour는 매일 한 시간씩 새로운 기법을 학습하는 세션으로,
Falco나 Bache 같은 코치가 이끈다.

Samman Technical Coaching이라 불리는 이 방법은 두 가지 활동으로 구성된다:

- **Learning Hour**: 기법 시연 후 짝 프로그래밍으로 직접 연습
- **Ensemble Working**: 실제 프로덕션 코드에 기법 적용

---

## 분석

### "읽지 않고 리팩터링한다"는 역설

전통적 접근: 코드를 읽고 → 이해하고 → 테스트를 작성하고 → 리팩터링한다.

Falco의 접근: 코드를 실행하고 → 동작을 포획하고 → 리팩터링하고 → 그제서야
이해한다.

이것은 단순한 순서 변경이 아니다. "이해"를 전제 조건에서 결과물로 전환한 것이다.

코드를 읽어서 이해하는 것은 인간의 인지 능력에 의존한다. 복잡한 레거시 코드에서
이 능력은 급격히 떨어진다. 반면 "실행하고 관찰"하는 것은 기계적이고 확장
가능하다.

### Approval Testing의 인식론적 전환

전통적 테스트: "코드가 이것을 해야 한다" (당위, specification)

Approval Testing: "코드가 이것을 한다" (사실, characterization)

이 전환이 강력한 이유는 레거시 코드에서 "당위"를 아는 사람이 없는 경우가
대부분이기 때문이다. 원래 작성자는 떠났고, 문서는 낡았고, 요구사항은 변했다.

Approval Testing은 이 인식론적 공백을 우회한다. "올바름"을 정의하는 대신, "현재
동작의 변경"을 감지하는 데 집중한다.

이것은 Michael Feathers의 레거시 코드 정의와 정확히 일치한다:

> 레거시 코드란 테스트가 없는 코드다.

Approval Testing은 이 정의를 실용적으로 해결한다.

### Provable Refactoring과 신뢰의 계층

코드 변경의 신뢰 수준을 계층화하면:

| 신뢰 수준 | 방법                      |
| --------- | ------------------------- |
| 최고      | 자동화 도구 리팩터링      |
| 높음      | 컴파일러 검증 수동 단계   |
| 중간      | 테스트로 검증된 변경      |
| 낮음      | 사람의 판단에 의존한 변경 |

Falco는 가능한 한 높은 신뢰 수준에서 작업할 것을 권장한다. "테스트가 통과하니까
안전하다"보다 "이 변환은 수학적으로 동치(equivalent)다"가 더 강력하다.

### Lift-Up Conditional의 기계적 아름다움

이 기법의 핵심 강점은 판단이 필요 없다는 것이다.

1. 복사한다
2. `true`/`false`로 치환한다
3. 단순화한다
4. 테스트를 돌린다

각 단계가 기계적이므로 실수할 여지가 작다. 그리고 각 단계 사이에 테스트를
실행하므로, 실수하더라도 즉시 감지된다.

이것은 "작은 단계로, 항상 테스트 통과 상태를 유지하며" 리팩터링하라는 원칙의
구체적 실현이다.

### 세 기법의 시너지 구조

```text
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

이 구조에서 각 기법은 다음 기법의 전제 조건을 충족시킨다. Combination Testing
없이 Lift-Up Conditional은 위험하고, Lift-Up Conditional 없이 Replace
Conditional with Polymorphism은 적용할 수 없다.

---

## 인사이트

### "코드를 읽지 마라"는 반직관적 지혜

프로그래머의 첫 번째 본능은 코드를 읽는 것이다. 그러나 복잡한 레거시 코드를 읽는
행위 자체가 위험하다. 잘못된 이해를 형성하고, 그 이해에 기반한 변경이 버그를
만든다.

Falco의 접근은 이 본능을 뒤집는다: "이해하기 전에 안전망을 치고, 리팩터링
과정에서 이해가 자연스럽게 형성되게 하라."

이것은 TDD의 "Red-Green-Refactor"와 구조적으로 동일하다. 테스트가 먼저, 이해가
나중이다.

더 넓게 보면 이것은 인지심리학에서 말하는 "확증 편향(confirmation bias)"의
문제다. 코드를 읽고 "이해했다"고 느끼는 순간, 그 이해에 부합하는 증거만 보게
된다. Approval Testing은 이 편향을 원천 차단한다. 인간의 이해가 아닌 기계의
관찰로 시작하기 때문이다.

George Lakoff의 프레임 이론과도 연결된다. 코드를 읽는 행위는 프레임을 형성하고,
그 프레임이 이후의 모든 판단을 왜곡한다. "읽지 않는 것"은 프레임 없이 시작하는
것이다.

### Approval Testing: 귀납과 관찰의 인식론

전통적 테스트: "코드가 이것을 해야 한다" (당위, specification)

Approval Testing: "코드가 이것을 한다" (사실, characterization)

이 전환이 강력한 이유는 레거시 코드에서 "당위"를 아는 사람이 없는 경우가
대부분이기 때문이다. 원래 작성자는 떠났고, 문서는 낡았고, 요구사항은 변했다.

Approval Testing은 이 인식론적 공백을 우회한다. "올바름"을 정의하는 대신, "현재
동작의 변경"을 감지하는 데 집중한다.

이것은 Michael Feathers의 레거시 코드 정의와 정확히 일치한다:

> 레거시 코드란 테스트가 없는 코드다.

Approval Testing은 이 정의를 실용적으로 해결한다.

더 깊이 들어가면 이것은 과학철학의 "관찰 적재(theory-ladenness of observation)"
문제와 닮았다. 전통적 테스트는 이론(사양)이 관찰(테스트)을 결정한다. Approval
Testing은 이론 없이 관찰부터 시작하여 이론을 역으로 구성한다. 귀납적 접근이다.

프로덕션에서 동작하는 코드는 그 자체로 "사실상의 사양(de facto
specification)"이다. 사용자가 기대하는 동작은 코드가 실제로 하는 동작이다.
문서에 적힌 것이 아니다. 이 현실을 인정하는 것이 Approval Testing의 철학적
출발점이다.

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

이 비용 차이가 레거시 코드를 "방치의 대상"에서 "점진적 개선의 대상"으로
전환시킨다.

경제학적으로 이것은 "거래 비용" 감소의 효과다. Ronald Coase가 기업의 존재를 거래
비용으로 설명한 것처럼, 레거시 코드의 방치는 "리팩터링의 거래 비용"이 너무 높기
때문이다. Falco/Bache 기법은 이 거래 비용을 극적으로 낮춘다. 거래 비용이
내려가면 거래가 발생한다. 즉, 리팩터링이 일어난다.

"기술 부채(technical debt)"라는 은유도 재해석된다. 기술 부채의 진짜 비용은
코드가 나쁜 것이 아니라, 코드를 개선하는 비용이 높은 것이다. Falco/Bache 접근은
부채의 원금이 아닌 이자율을 낮추는 것이다. 이자율이 충분히 낮아지면 부채 상환이
합리적 선택이 된다.

### "이해"의 단계적 출현

전통적 접근에서 "이해"는 이산적(discrete)이다. 이해하거나 이해하지 못하거나.
Falco/Bache 접근에서 "이해"는 연속적(continuous)이다.

```text
Approval Test    → 동작을 안다 (what)
Mutation Test    → 경계를 안다 (where)
Lift-Up          → 구조를 안다 (how)
Polymorphism     → 의도를 안다 (why)
```

각 단계를 거칠 때마다 이해의 깊이가 증가한다. "무엇을 하는지" → "어디가
경계인지" → "어떻게 구성되어 있는지" → "왜 이렇게 되어 있는지"

이것은 Bloom의 인지 분류 체계(taxonomy)와 대응한다: 기억 → 이해 → 적용 → 분석 →
평가. 기법이 인지 단계를 자연스럽게 안내하는 것이다.

### 두려움의 제거: 심리적 안전망

레거시 코드 앞에서 개발자가 느끼는 감정은 두려움이다. "건드리면 뭔가 깨질
것이다." 이 두려움이 합리적인 이유는 실제로 깨지기 때문이다.

Falco/Bache 접근의 심리적 효과:

- **Approval Testing**: "현재 동작이 포획되었다. 변경이 감지된다." → 두려움 감소
- **Mutation Testing**: "테스트가 실제로 작동한다는 증거가 있다." → 신뢰 증가
- **Provable Refactoring**: "이 변환은 수학적으로 안전하다." → 확신

Amy Edmondson의 "심리적 안전(psychological safety)" 개념이 코드 수준에서
실현된다. 팀원에 대한 신뢰가 아닌, 도구와 기법에 대한 신뢰가 안전을 만든다.

이것은 등반의 비유로 설명된다. 자유 등반(free solo)은 영웅적이지만 위험하다.
로프와 안전 장비가 있으면 같은 벽을 더 빠르고 더 과감하게 오른다. 테스트는 안전
장비다. 안전 장비가 있으면 더 대담한 리팩터링이 가능해진다.

### Provable Refactoring: 테스트를 넘어서는 확신

코드 변경의 신뢰 수준을 계층화하면:

| 신뢰 수준 | 방법                      |
| --------- | ------------------------- |
| 최고      | 자동화 도구 리팩터링      |
| 높음      | 컴파일러 검증 수동 단계   |
| 중간      | 테스트로 검증된 변경      |
| 낮음      | 사람의 판단에 의존한 변경 |

Falco는 가능한 한 높은 신뢰 수준에서 작업할 것을 권장한다. "테스트가 통과하니까
안전하다"보다 "이 변환은 수학적으로 동치(equivalent)다"가 더 강력하다.

이것은 형식 검증(formal verification)의 실용적 변형이다. 전체 프로그램을
형식적으로 증명하는 것은 비현실적이지만, 개별 리팩터링 단계를 형식적으로
증명하는 것은 가능하고 실용적이다.

"Rename Variable"이 왜 안전한가? 이름은 의미론에 영향을 주지 않기 때문이다.
"Extract Method"가 왜 안전한가? 동일한 코드를 다른 위치에서 호출하는 것이 실행
순서를 바꾸지 않기 때문이다.

이런 추론이 가능한 리팩터링과 불가능한 리팩터링을 구분하는 것 자체가 가치 있다.
Arlo의 커밋 표기법은 이 구분을 커밋 메시지에 인코딩하여 코드 리뷰의 효율을
높인다.

`r` 접두사가 붙은 커밋은 빠르게 훑어도 된다. `!!` 접두사가 붙은 커밋은 주의 깊게
봐야 한다. 이것은 리뷰어의 인지 예산(cognitive budget)을 효율적으로 배분하는
전략이다.

### Lift-Up Conditional: 구성적 증명과 되돌림의 자유

이 기법의 핵심 강점은 판단이 필요 없다는 것이다.

1. 복사한다
2. `true`/`false`로 치환한다
3. 단순화한다
4. 테스트를 돌린다

각 단계가 기계적이므로 실수할 여지가 작다. 그리고 각 단계 사이에 테스트를
실행하므로, 실수하더라도 즉시 감지된다.

이것은 "작은 단계로, 항상 테스트 통과 상태를 유지하며" 리팩터링하라는 원칙의
구체적 실현이다.

수학에서 "구성적 증명(constructive proof)"과 유사하다. 존재를 주장하는 것이
아니라 실제로 구성하여 보여주는 것이다. "이 코드는 더 깔끔해질 수 있다"가 아니라
"이 단계를 따르면 깔끔해진다"를 보여준다.

주목할 점은 이 기법이 "항상 성공하지 않는다"는 것이다. 조건을 끌어올렸는데 다른
조건이 중복되면 의미가 없다. 이때 "되돌림"이 핵심이다. 이것은 체스에서 수를
시도하고 되돌리는 것과 같다. 되돌릴 수 있기 때문에 시도할 수 있다. 되돌릴 수
없으면 시도 자체를 하지 못한다.

### 세 기법의 시너지와 파이프라인 사고

```text
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

이 구조에서 각 기법은 다음 기법의 전제 조건을 충족시킨다. Combination Testing
없이 Lift-Up Conditional은 위험하고, Lift-Up Conditional 없이 Replace
Conditional with Polymorphism은 적용할 수 없다.

이것은 Unix 파이프라인 철학과 동일하다. "한 가지 일을 잘 하는 도구를 조합하라."
각 기법은 단순하다. 조합이 복잡한 문제를 푼다.

더 중요한 것은 이 파이프라인이 "되돌림 가능" 하다는 점이다. 어느 단계에서든
문제가 발생하면 이전 단계로 돌아갈 수 있다. 이것은 Agile의 "빠른 실패(fail
fast)"와 같은 원리다. 되돌림 비용이 낮으면 실험이 자유로워진다.

### 테스트와 리팩터링의 공진화

이 글의 가장 깊은 통찰: 테스트와 리팩터링은 별개의 활동이 아니라 상호 강화하는
순환이다.

```text
테스트 → 리팩터링을 안전하게 만듦
  ↑                            ↓
  └── 리팩터링 → 더 나은 테스트 가능
```

Approval Testing으로 시작한 조잡한 테스트가 리팩터링 후에는 각 클래스의 단위
테스트로 진화한다. 리팩터링이 코드를 명확하게 만들면, 비로소 "코드가 무엇을 해야
하는지" 이해하게 되고, Approval Test를 진정한 Specification Test로 대체할 수
있다.

테스트의 생애주기가 존재하는 것이다:

```text
1. Characterization Test (코드가 뭘 하는지 포획)
        ↓ 리팩터링
2. Unit Test (각 클래스의 동작을 검증)
        ↓ 이해 심화
3. Specification Test (의도를 명시적으로 표현)
        ↓ 기능 추가
4. Regression Test (새 기능이 기존을 깨지 않음)
```

테스트는 태어나고, 성숙하고, 역할이 변한다. "테스트를 작성한다"가 아니라
"테스트를 키운다(grow)"가 더 정확한 표현이다.

### Kata의 교육적 가치: 의도적 수련

Gilded Rose 같은 카타가 효과적인 이유:

1. **현실적 제약**: 코드를 모르는 상태에서 시작
2. **안전한 실패**: 프로덕션이 아니므로 실수해도 괜찮다
3. **반복 가능**: 같은 카타를 다른 언어, 다른 접근으로 반복 연습
4. **점진적 복잡도**: 기법을 하나씩 적용하며 효과를 체감

Learning Hour에서 매일 한 시간씩 연습하는 Samman 방식은 이 카타의 가치를
극대화한다. 기법은 "아는 것"이 아니라 "손에 익는 것"이다.

Anders Ericsson의 "의도적 수련(deliberate practice)" 이론과 정확히 일치한다.
전문성은 반복이 아니라 "피드백 있는 반복"에서 온다. 카타의 테스트는 즉각적
피드백을 제공한다.

Bache가 말하는 "리팩터링을 잘 해내면 실제로 깔끔해지는데, 그게 아주
만족스럽다"는 것은 심리학에서 말하는 "유능감(competence)"이다.
자기결정이론(Self-Determination Theory)의 세 가지 기본 욕구 중 하나다. 카타가 이
욕구를 충족시키기 때문에 학습자가 자발적으로 반복하게 된다.

800개 이상의 포크가 이를 증명한다. "해야 해서" 하는 것이 아니라 "하고 싶어서"
하는 것이다.

### "끔찍한 코드"의 교육적 의도

Bache가 "극도로 끔찍한 상태"라고 표현한 Gilded Rose의 초기 코드는 의도적으로
나쁘다. 이것은 교육적 장치다.

현실에서 레거시 코드를 만나면 "누가 이렇게 짰어?"라는 감정이 먼저 온다. 카타는
이 감정을 안전한 환경에서 경험하게 한다. 판타지 설정("마법 아이템")은 실제
비즈니스 로직의 무게를 덜어내어 순수하게 기법에 집중할 수 있게 한다.

이것은 의학에서 시체를 해부하는 것과 비슷하다. 실제 환자를 수술하기 전에 안전한
환경에서 기술을 연마한다. 감정적 부담 없이 기술적 역량을 쌓는 것이다.

### AI 시대에 이 기법들의 가치가 올라간다

AI 코딩 도구는 Combination Testing의 입력 조합 생성, Approval Testing의 출력
검증, 커버리지 분석을 자동화할 수 있다.

그러나 핵심 판단은 여전히 인간의 몫이다:

- 어떤 조건을 끌어올릴 것인가
- 어떤 클래스 계층이 적절한가
- 리팩터링의 방향은 무엇인가

기법을 아는 인간 + 실행을 돕는 AI의 조합이 레거시 코드 리팩터링의 비용을 한 차원
더 낮출 것이다.

더 구체적으로 AI가 각 기법을 어떻게 증강하는지:

| 기법                | 인간의 역할    | AI의 역할      |
| ------------------- | -------------- | -------------- |
| Combination Testing | 의미 있는 범주 | 조합 생성      |
|                     | 선정           |                |
| Mutation Testing    | 실패 원인 분석 | 변이 자동 적용 |
| Lift-Up Conditional | 끌어올릴 조건  | 기계적 치환    |
|                     | 선택           | 실행           |
| Polymorphism        | 클래스 계층    | 코드 이동      |
|                     | 설계           | 자동화         |

AI가 기계적 단계를 대행하면 인간은 판단에만 집중할 수 있다. 이것은 기법의 가치를
떨어뜨리는 것이 아니라 높이는 것이다. 기법을 "아는 인간"의 생산성이
기하급수적으로 올라가기 때문이다.

AI 코딩 도구에게 "이 레거시 코드를 리팩터링해" 라고 하면 실패할 가능성이 높다.
"Approval Testing으로 현재 동작을 포획하고, 커버리지를 확인하고, Lift-Up
Conditional을 적용해"라고 하면 성공 가능성이 높아진다.

기법의 이름은 AI와의 소통 프로토콜이 된다. 어휘가 풍부한 프로그래머가 AI를 더 잘
다룬다.

### 코드의 동작과 구조의 분리

이 글의 기법들이 공유하는 철학적 기반: "동작을 바꾸지 않으면서 구조를 바꾼다."

이것은 David Parnas의 "정보 은닉(information hiding)" 원칙의 반대편이다.
Parnas가 "구조로 동작을 보호하라"고 했다면, Falco/Bache는 "동작을 보존하면서
구조를 교체하라"고 말한다.

두 원칙 모두 동작과 구조의 독립성을 전제한다. 같은 동작을 다른 구조로 표현할 수
있다는 것. 이것이 리팩터링의 존재론적 근거다.

프로그래밍에서 이 분리는 흔히 "무엇(what)"과 "어떻게(how)"로 표현된다. Approval
Testing은 "무엇"을 포획하고, 리팩터링은 "어떻게"를 변경한다. "무엇"이 포획되어
있으므로 "어떻게"를 자유롭게 바꿀 수 있다.

### 복잡성을 다루는 두 가지 전략

복잡한 시스템을 다루는 전략은 크게 두 가지다:

1. **분해(decomposition)**: 큰 문제를 작은 문제들로 나누기
2. **추상화(abstraction)**: 세부사항을 감추고 본질만 드러내기

Falco/Bache의 기법은 이 둘을 순차적으로 적용한다.

- Lift-Up Conditional = 분해. 하나의 거대한 조건문을 독립된 분기로 분리.
- Replace Conditional with Polymorphism = 추상화. 분리된 분기를 클래스로 캡슐화.

분해 없이 추상화하면 잘못된 추상화가 된다. (코드의 구조를 모른 채 클래스를
만들면 실패.) 추상화 없이 분해만 하면 복잡성이 이동할 뿐 감소하지 않는다.
(조건문을 분리만 하면 코드가 더 길어진다.)

순서가 중요하다. 분해 → 추상화. 이것은 Sandi Metz가 "잘못된 추상화보다 중복이
낫다"고 말한 것과 통한다. 충분히 분해되기 전에 추상화하지 마라.

### Mutation Testing의 과소평가된 가치

커버리지 100%에 대한 흔한 오해: "모든 줄이 실행되었으니 안전하다."

Mutation Testing은 이 환상을 깨뜨린다. "실행되었다"와 "테스트되었다"는 다르다.

```python
# 이 코드가 커버되었다고 해서
# 테스트된 것은 아니다
if quality > 0:
    quality -= 1
```

`quality = 10`으로 실행하면 커버리지 100%다. 그러나 `quality -= 1`을
`quality -= 2`로 바꿔도 테스트가 통과한다면, 이 줄은 실행되었을 뿐 테스트되지
않은 것이다.

Mutation Testing은 "이 코드가 변경되었을 때 테스트가 실패하는가?"를 묻는다.
이것은 Karl Popper의 반증주의 (falsificationism)와 같은 논리다. "이 이론이
틀렸다는 것을 보여줄 수 있는가?"

좋은 테스트는 반증 가능한 테스트다. 코드가 잘못 변경되었을 때 반드시 실패하는
테스트만이 진정한 안전망이다.

### "충분히 좋은" 테스트에서 시작하는 용기

완벽주의는 레거시 코드 앞에서 마비를 만든다. "완벽한 테스트를 작성할 수 없으니
아예 시작하지 않겠다."

Approval Testing의 핵심 메시지: "충분히 좋은 테스트로 시작하라."

승인된 결과(approved output)가 "올바른" 결과인지는 모른다. 그러나 "현재" 결과인
것은 확실하다. 현재를 기록한 것만으로도 변경을 감지할 수 있다. 이것이 "테스트
없음"보다 무한히 낫다.

Kent Beck의 표현: "Make it work, make it right, make it fast."

Approval Testing은 이것의 테스트 버전이다: "Make it captured, make it verified,
make it specified." 포획하고, 검증하고, 그다음에 명세화하라.

### 작은 단계의 누적 효과

이 글의 모든 기법이 공유하는 원칙: "작은 단계로 나누어 실행하라."

- Combination Testing: 입력 하나씩 추가
- Lift-Up Conditional: 조건 하나씩 끌어올림
- Replace Conditional: 분기 하나씩 추출

왜 작은 단계가 강력한가?

1. **피드백 주기가 짧다**: 실수를 즉시 발견
2. **되돌림 비용이 낮다**: 한 단계만 되돌리면 됨
3. **진행이 가시적이다**: 매 단계가 작은 성공
4. **학습이 누적된다**: 매 단계에서 코드를 조금 더 이해

이것은 제조업의 "단일 단위 흐름(single-piece flow)"과 같다. Toyota Production
System에서 배치(batch)를 줄이고 흐름(flow)을 만드는 것이 품질과 속도를 동시에
향상시키듯, 리팩터링에서도 단계를 줄이면 품질(안전성)과 속도(두려움 감소) 모두
향상된다.

### 도구가 사고를 형성한다

Bache가 "올바른 도구를 알면 상황이 크게 달라진다"고 말한 것은 도구적 차원을
넘어선다.

ApprovalTests 라이브러리가 없으면 Approval Testing이라는 사고방식 자체가
발생하지 않는다. IDE의 자동 리팩터링이 없으면 Provable Refactoring이라는 개념이
의미가 없다. 커버리지 도구가 없으면 "커버리지를 가이드로 사용"한다는 전략이
불가능하다.

Marshall McLuhan: "도구가 인간을 형성한다." 도구는 가능성의 공간을 연다.
ApprovalTests가 열어준 가능성의 공간에서 Falco/Bache의 워크플로우가 탄생했다.

역으로, 새로운 도구가 나오면 새로운 워크플로우가 가능해진다. AI 코딩 도구는 아직
탐색되지 않은 새로운 레거시 코드 접근법을 열어줄 것이다.

### Samman Coaching과 기법 전파의 메커니즘

Falco가 Bache에게, Bache가 독자에게, Learning Hour가 팀에게. 이 기법들은 사람
사이에서 전파된다.

주목할 것은 전파의 방식이다. 문서가 아니라 시연(demonstration)이다. Bache는
스크린캐스트를 녹화했다. Learning Hour에서는 짝 프로그래밍으로 직접 해본다. 읽는
것이 아니라 보고 따라 한다.

이것은 Michael Polanyi의 "암묵지(tacit knowledge)" 이론과 맞닿는다. "우리는 말할
수 있는 것보다 더 많이 안다." 리팩터링의 감각 — 언제 끌어올리고, 언제 되돌리고,
언제 다음 단계로 넘어갈지 — 은 명시적으로 가르칠 수 없다. 함께 하면서 전달되는
것이다.

50명의 기여자와 800개의 포크는 이 암묵지가 GitHub을 통해서도 부분적으로 전달될
수 있음을 보여준다. 그러나 Bache가 스크린캐스트를 녹화하고 Learning Hour를
운영하는 이유는 암묵지의 핵심 부분은 여전히 직접적 경험을 통해서만 전달되기
때문이다.

### "5년 만에 800 포크"가 말해주는 것

Gilded Rose Kata가 2013년경 GitHub에 공개되고 2018년 기준 800개 이상의 포크를
기록했다. 50명 이상이 다양한 언어로 번역하여 기여했다.

이 숫자가 의미하는 것: 레거시 코드 다루기는 보편적 고통이다. 프로그래밍 언어에
관계없이, 업종에 관계없이, 경력에 관계없이, 모든 개발자가 겪는 문제다.

그리고 그 고통에 대한 체계적 접근법의 수요가 거대하다는 것이다. 카타가 인기를
끄는 이유는 재미뿐 아니라 "절실함" 때문이다. 현실에서 매일 마주치지만 어떻게
해야 할지 모르는 문제에 대한 연습 기회를 제공하기 때문이다.

### 원문의 겸손함이 숨기는 깊이

원문은 놀라울 정도로 짧고 겸손하다. "올바른 도구를 알면 도움이 된다." "Falco에게
배웠다." "스크린캐스트를 녹화했다."

그러나 이 짧은 글 뒤에는:

- Characterization Testing이라는 인식론적 전환
- Provable Refactoring이라는 형식 검증의 실용화
- Lift-Up Conditional이라는 새로운 리팩터링 기법의 발명
- Samman Coaching이라는 기술 코칭 방법론의 확립

이 모든 것이 들어 있다. Bache와 Falco가 "간단하게" 설명하는 것은 이 기법들이
진정으로 내면화되었기 때문이다. 전문가는 복잡한 것을 간단하게 말한다. 그 간단함
뒤의 깊이를 놓치면 안 된다.

---

## 관련 문서

- [Tests Are The New Moat](../test/tests-are-the-new-moat.md)
- [Test Pyramid](../test/test-pyramid.md)

## 참고

- [Advanced Testing and Refactoring Techniques - Eficode Blog](https://www.eficode.com/blog/advanced-testing-refactoring-techniques)
- [Lift Up Conditional - Samman Coaching](https://sammancoaching.org/refactorings/lift_up_conditional.html)
- [Gilded Rose Refactoring Kata - GitHub](https://github.com/emilybache/GildedRose-Refactoring-Kata)
- [Arlo's Commit Notation - GitHub](https://github.com/RefactoringCombos/ArlosCommitNotation)
- [Cutting Code Quickly - Llewellyn Falco](https://www.classcentral.com/course/youtube-cutting-code-quickly-from-0-to-cleanly-refactored-100-tested-code-llewellyn-falco-132984)
- [Approval Testing on Legacy Code - Nicolas Carlo](https://www.nicoespeon.com/en/2019/01/approval-testing-on-legacy-code/)
- [Replace Conditional with Polymorphism - Refactoring Guru](https://refactoring.guru/replace-conditional-with-polymorphism)
