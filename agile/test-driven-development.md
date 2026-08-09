# 테스트 주도 개발

Test Driven Development <http://wiki.c2.com/?TestDrivenDevelopment>

[Xper:Test Driven Development](https://web.archive.org/web/20070628064054/http://xper.org/wiki/xp/TestDrivenDevelopment)

[Code the Unit Test First](http://www.extremeprogramming.org/rules/testfirst.html)

## Test Driven Development: By Example

<https://www.oreilly.com/library/view/test-driven-development/0321146530/>

- 원서: <https://a.co/d/faRGN86>
- 번역서: <http://aladin.kr/p/dGXdZ>

[Xper:Test Driven Development By Example](https://web.archive.org/web/20061012041417/http://xper.org/wiki/xp/TestDrivenDevelopmentByExample)

## 자료

[Xper:Is Tdd Top Down](https://web.archive.org/web/20061012054232/http://xper.org/wiki/xp/IsTddTopDown)

[Xper:Tdd Test](https://web.archive.org/web/20061012050549/http://xper.org/wiki/xp/TddTest)

[Xper:Tdd Web Sites](https://web.archive.org/web/20061012050559/http://xper.org/wiki/xp/TddWebSites)

[Xper:TDD수련법](https://web.archive.org/web/20061012050617/http://xper.org/wiki/xp/TDD_bc_f6_b7_c3_b9_fd)

[[OKKYCON] 이혜승 - 테알못 신입은 어떻게 테스트를 시작했을까?](https://www.slideshare.net/OKJSP/okkycon-120498066)

## 아샬이 만든 자료

[TDD FAQ](https://github.com/ahastudio/til/blob/main/blog/2016/12-03-tdd-faq.md)

[Jest를 이용한 간단한 TDD 예제](https://github.com/ahastudio/til/blob/main/jest/20201204-simple-tdd-example.md)

[📺 Java+JUnit TDD 실습](https://www.youtube.com/playlist?list=PLbdtsbZUwdeRirBYnWrMSvKYS4CcmXCeU)

## Canon TDD

<https://tidyfirst.substack.com/p/canon-tdd>

Kent Beck이 2023년 12월에 쓴 글. TDD가 아닌 것을 비판하는 글이 넘쳐나서, TDD의
원래 정의를 정리했다.

### TDD의 목표

TDD는 프로그래밍 워크플로우다. 프로그래머가 시스템의 행동을 변경해야 할 때,
TDD는 다음 상태를 달성하도록 돕는다:

- 기존에 동작하던 것은 여전히 동작한다.
- 새로운 행동이 기대한 대로 동작한다.
- 시스템이 다음 변경을 받아들일 준비가 되어 있다.
- 프로그래머와 동료가 위 사항에 대해 확신한다.

### 인터페이스 설계와 구현 설계

설계를 하나로 뭉뚱그리는 것이 첫 번째 오해다. 설계에는 두 가지 종류가 있다:

- **인터페이스 설계**: 행동이 어떻게 호출되는가.
- **구현 설계**: 시스템이 그 행동을 어떻게 구현하는가.

### 5단계

1. 테스트할 시나리오 목록(Test List)을 작성한다.
2. 목록에서 딱 하나를 골라 실행 가능한 테스트로 만든다.
3. 테스트(와 기존 테스트 전부)가 통과하도록 코드를 변경한다. 이 과정에서 새
   항목이 떠오르면 목록에 추가한다.
4. 선택적으로 리팩터링하여 구현 설계를 개선한다.
5. 목록이 빌 때까지 2단계로 돌아간다.

### 각 단계의 핵심

#### 1단계: Test List

행동 변경에 대한 예상 변형을 모두 나열한다. 이것은 행동 분석(behavioral
analysis)이다. 기존 행동이 깨지지 않아야 하는 경우도 포함한다.

> 실수: 구현 설계 결정을 여기서 섞는 것. 내부 구조를 결정할 시간은 나중에
> 충분하다.

Kent Beck은 이 단계가 책에서 간과되었다고 했다. "TDD는 바로 코딩에 뛰어든다"는
비판에 대해 "아니다"라고 반박했다.

#### 2단계: 테스트 하나 작성

setup, 호출, assertion이 포함된 자동화 테스트를 하나만 작성한다. 여기서
인터페이스 설계 결정이 시작된다. 다음 테스트를 고르는 순서가 중요하며, 이는
경험을 통해 익히는 기술이다.

> 실수: 목록의 모든 항목을 테스트로 변환한 뒤 하나씩 통과시키는 것. 첫 번째
> 테스트를 통과시키다가 나머지 테스트에 영향을 주는 결정을 바꿔야 하면? 재작업이
> 발생한다.

#### 3단계: 테스트 통과시키기 (Red → Green)

> 실수: 실제 계산된 값을 복사해서 기대값에 붙여넣는 것. 이중 검증(double
> checking)을 무력화한다.

> 실수: 테스트 통과와 리팩터링을 섞는 것. 먼저 동작하게 만들고, 그다음 올바르게
> 만든다.

통과 과정에서 새 테스트가 필요하면 목록에 추가한다. 테스트가 통과하면 목록에서
지운다.

#### 4단계: 선택적 리팩터링

이제 구현 설계 결정을 내린다.

> 실수: 이번 세션에 필요한 것 이상으로 리팩터링하는 것.

## AI 시대의 TDD

[AI 시대에 TDD가 더 강력해진 이유](./2026-02-26-tdd-in-ai-era.md)
