# Genie Session: Codex App

Kent Beck의 Genie Session — Codex for Mac으로
GPUSortedMap을 구현하는 라이브 코딩 세션 분석.

영상: <https://www.youtube.com/watch?v=PVMOCU2zjZg>

Substack:
[Genie Session: Codex for Mac/GPUSortedMap](https://tidyfirst.substack.com/p/genie-session-codex-for-macgpusortedmap)

## 배경

Kent Beck은 B+ Tree 프로젝트를 Rust와 Python으로
구현하며 Augmented Coding을 탐구해왔다.
이번 세션에서는 **Codex app**(macOS용 데스크톱 앱)을
사용하여 GPU 가속 Sorted Map 구현에 도전한다.

이전 세션에서는 주로 Augment Code를 사용했는데,
이번에는 OpenAI의 Codex app을 선택한 점이 주목할 만하다.

### B+ Tree에서 GPUSortedMap으로

이전 프로젝트인 BPlusTree3에서 겪은 경험:

- Rust 구현 중 메모리 소유권 모델과 자료구조의
  복잡성이 결합되어 지니가 멈춤
- Python으로 알고리즘을 먼저 구현하고
  Rust로 번역(transliterate)하는 전략으로 돌파
- 결과물은 Rust BTreeMap과 성능 경쟁이 가능한 수준

GPUSortedMap은 이 경험의 연장선이다.
GPU 연산을 활용하는 더 도전적인 자료구조로,
AI가 기존 솔루션을 복사할 수 없는 영역이다.

## Kent Beck이 강조하는 것들

### 1. 억제(Inhibition)가 핵심이다

> Using genies for coding is mostly inhibition —
> getting it not to do harmful stuff.

프롬프팅은 지니에게 무언가를 시키는 것처럼 보이지만,
실제로는 대부분 **"그것 말고", "그렇게 말고",
"이것부터 해"** 라고 말하는 과정이다.
달리려고만 하는 말의 고삐를 잡는 것과 같다.

### 2. 옵션성(Optionality) 보존

> Don't eat the seed corn.

봄에 배가 고프더라도 종자를 심어야 가을에 수확할 수 있다.
지니는 이 원칙을 모른다.

- 지니는 기능 추가(inhale)에 탁월하지만,
  구조 정리(exhale)를 하지 않는다
- 복잡성이 축적되면 결국 지니조차 다음 기능을
  구현할 수 없는 지점에 도달한다
- **리팩터링으로 옵션성을 회복**하는 것은
  인간의 판단이 필요한 영역이다

Kent Beck은 이를 **Design Contest**라는 개념으로
확장한다. 백만 개의 지니가 각자 다른 방식으로
다음 기능을 구현하게 하고, 가장 낮은 비용으로
성공한 지니를 선택하는 것이다.
Jessica Kerr는 이를 "Design Contest"라 불렀다.

### 3. 컨텍스트 제한 전략

다음 단계에 필요한 정보만 지니에게 제공한다.
전체 맥락을 주지 않는다.

- 지니가 지속 불가능한 기능 개발로 달려나가는 것을
  방지한다
- 복잡성이 복리로 쌓이는 것을 차단한다
- 리팩터링 능력은 유지된다

### 4. plan.md를 통한 TDD

지니에게 구체적인 규칙을 부여한다:

> When I say 'go', find the next unmarked test
> in plan.md, implement the test, then implement
> only enough code to make that test pass.

이 전략의 핵심:

- 테스트 하나씩 점진적으로 진행
- 요청하지 않은 기능 구현을 차단
- plan.md가 진행 상황의 단일 소스가 됨

### 5. 지니의 타이밍 문제

> The genie's timing is off.

지니는 자신의 거대한 두뇌가 어떤 복잡성도
처리할 수 있다고 가정한다.
그래서 복잡성을 줄일 필요를 느끼지 않는다.

경고 신호:

- 요청하지 않은 기능이 구현될 때
- 테스트를 비활성화하거나 삭제할 때
- "수정"이 연쇄적으로 이어질 때

이런 신호가 보이면 즉시 개입해야 한다.

### 6. 실험 극대화

> Augmented coding means never having to say no
> to an idea.

코드 생성 비용이 거의 0에 수렴하는 시대에서
전략적 대응은 **실험의 극대화**다.

- 백만 가지를 시도하고 대부분을 버릴 준비
- 비용이 낮으니 아이디어를 시작하는 것은 선택의 문제
- 과거에 비싸다고 가정했던 것들이 저렴해졌다

## 인사이트

### Augmented Coding의 가치 체계

| Vibe Coding              | Augmented Coding         |
|--------------------------|--------------------------|
| 코드를 신경 쓰지 않음   | 코드 품질에 집중         |
| 동작하면 됨             | 정돈된 코드가 동작       |
| 에러를 지니에게 되돌림  | 복잡성을 적극적으로 관리 |
| 빠른 프로토타입에 적합  | 프로덕션 코드에 적합     |

### 더 이상 가치 없는 스킬 vs 증폭되는 스킬

Augmented Coding은 기존 스킬의 가치를 재편한다:

- **감가하는 스킬**: 언어 전문성, 타이핑 속도,
  API 암기
- **증폭되는 스킬**: 비전, 전략, 태스크 분해,
  피드백 루프, 디자인 판단

### 되돌리기의 용이함

지니와의 협업에서 변경 사항이 너무 많아
따라갈 수 없을 때의 전략:

1. 디자인 문서를 수정하고 지니가 적응하게 하거나
2. 학습 내용만 남기고 전부 버린 뒤 다시 시도

자존심 없이 되돌리고 다른 경로를 택하는 것이
이전보다 훨씬 쉬워졌다.

### 소프트웨어 디자인은 인간 관계의 연습

> Software design is an exercise in
> human relationships.

지니와의 협업도 결국 관계다.
코드가 지니가 이해하고 수정할 수 있는 형태를
유지해야 한다.
그러려면 내가 이해하고 수정할 수 있는 형태여야 한다.
구조가 엉키고 결합도가 높아지면,
지니가 실수하기 시작한다.

## 관련 문서

- [Genie Sessions: GPU Sorted Map](./genie-sessions-gpu-sorted-map.md)
- [Vibe Coding](./vibe-coding.md) - Augmented Coding
- [Codex](./codex.md) - OpenAI Codex
- [Kent Beck](../agile/kent-beck.md)
