# Rust 빌림 검사기가 11년 동안 놓친 수명 구멍: Drop과 공변 필드 대입

원문: [struct's lifetime requirements can be bypassed via covariant field assignment · Issue #164250 · rust-lang/rust](https://github.com/rust-lang/rust/issues/164250)

HN 토론: <https://news.ycombinator.com/item?id=50069499> (720점, 402개 댓글)

GN 토론: <https://news.hada.io/topic?id=35294>

## 요약

2026년 10월 13일 jsnell이 rust-lang/rust 저장소에 올린 이슈다.
구조체의 수명 요구 조건을 공변(covariant) 필드에
값을 대입하는 방식으로 우회할 수 있어서,
안전한(safe) Rust 코드만으로 해제된 메모리를 읽을 수 있다는 보고다.
이슈에는 `I-unsound`, `P-high`, `A-borrow-checker`,
`A-variance`, `A-destructors` 등의
레이블이 붙어 있다.

최초 재현 코드는 `T: 'static`을 요구하는 구조체 `Q<T>`에 `Drop`을 구현하고,
`Q(None)`으로 만든 뒤 필드에 지역 변수의 참조를 대입한다.
컴파일러는 `'static`이 아닌 `&String`이 들어가는 것을 막지 못하고,
`Drop`은 그 참조를 `'static`으로 믿고 전역 벡터에 보관한다.
지역 변수가 사라진 뒤 그 자리에 다른 문자열을 만들면
보관된 참조가 새 문자열 `XXXX...`를 출력한다.
AddressSanitizer로 돌리면 `stack-use-after-scope`로 멈춘다.
보고자는 현재 nightly와 적어도 1.85.0까지의 stable에서 재현된다고 적었다.

댓글에서 재현 범위가 빠르게 넓어졌다.
theemathas는 핵심을 몇 줄로 줄이고 자신의 버전이
1.18.0(2017)부터 컴파일된다고 했다.
lcnr는 `'static` 없이 수명 매개변수 세 개만으로 같은 문제를 만들었고,
theemathas는 그 변형이 Rust 1.4.0(2015)부터 컴파일된다고 확인했다.
maxdexh는 클로저를 이용해 해제된 메모리를 출력하는 버전과,
필드 대입 없이 배열의 타입 통합(unification)만으로
같은 일을 일으키는 버전을 내놓았다.
mueddib는 이 배열 버전이 stable 1.99.0과 nightly 1.101.0에서 컴파일되며,
Miri가 해제 후 사용(use-after-free)으로
정의되지 않은 동작을 보고한다고 확인했다.

Types 팀의 lcnr는 이슈 맨 위에 설명을 덧붙였다.
이 버그는 실제 사용 여부와 관계없이
`P-critical`이었겠지만 11년 된 버그라서 `P-high`로 두었다.
11년 동안 발견되지 않았다면 실제로 마주치기는 쉽지 않다는 판단이다.
또 이 구멍을 악용하려면 의도적으로 악의적인 `Drop` 구현이 필요하므로
실수로 메모리 안전성이 깨졌을 가능성은 낮다고 봤다.
Types 팀은 차세대 트레이트 해결기, 수명 제약 재작업,
Project Zero 같은 작업으로 타입 시스템의 불건전성을
없애는 데 우선순위를 두고 있다고 밝혔다.

## 분석

### 무엇이 빠졌는가: 대입 시점에 구조체의 수명 경계를 다시 확인하지 않는다

`Q<T: 'static>`에서 `T`가 `'static`이어야 한다는
조건은 타입이 만들어질 때 지켜져야 한다.
`Q(None)`으로 만들 때는 `T`가 정해지지 않았고,
이후 `q.0 = Some(&l)`에서 공변성 덕분에 `T`가 짧은 수명의 참조로 정해진다.
이때 컴파일러가 `Q<&'짧은 String>`이 `T: 'static`을
만족하는지 다시 확인하지 않는 것이 문제다.

maxdexh는 이를 일반화해 통합 과정이
타입의 수명 경계를 확인하지 않는 것 같다고 했다.
필드 대입이든 배열 원소의 타입 통합이든,
여러 값의 타입을 하나로 맞추는 과정에서 경계 검사가 빠진다는 것이다.
HN에서 GrantMoyer는 이것이 타입 시스템 규칙 자체의 결함이 아니라
컴파일러가 규칙대로 거부했어야 할 코드를 받아들인 구현 버그라며,
규칙을 바꿀 필요 없이 거부하도록 고치면 된다고 정리했다.[^GrantMoyer]

### 왜 Drop인가

수명 경계가 깨진 값이 존재하는 것만으로는 아무 일도 일어나지 않는다.
그 값을 잘못된 수명으로 믿고 쓰는 코드가 있어야 한다.
`Drop`은 그런 코드가 자동으로 실행되는 자리다.
`impl<T: 'static> Drop for Q<T>` 안에서는
`T`가 `'static`이라고 가정할 수 있으므로,
그 값을 전역에 저장하거나 다른 스레드로 넘겨도 컴파일러가 막지 않는다.

HN에서 vincent-uden은 이 예제가 상상한 것처럼 기괴하지 않고
평범한 코드에서도 쉽게 마주칠 수 있을 것 같다고 놀랐다.[^vincent-uden]
jvanderbot는 4년 동안 시스템 쪽 Rust를 써 왔지만
직접 `Drop`을 구현한 적이 없다며,
함정은 `Drop` 구현에 있다고 반박했다.[^jvanderbot]
lcnr가 악의적인 `Drop` 구현이 필요하다고 본 근거도 여기에 있다.

### 11년 동안 숨어 있을 수 있었던 이유

FuzzywarmWalnut은 분산(variance) 관련 린트를 만들어 본 경험에서,
사람이 분산을 직접 적는 일이 거의 없어서 이런 버그가
10년 동안 시험되지 않은 채 남는다고 했다.[^FuzzywarmWalnut]
afdbcreid는 Rust에서는 1.0 이전부터 분산을 손으로
적는 것 자체가 불가능하다고 덧붙였다.[^afdbcreid]
즉 분산은 컴파일러가 추론하는 영역이고,
그 추론과 `Drop`의 수명 가정이 만나는
지점을 의식적으로 시험하는 사람이 드물었다.

weinzierl은 지금 `unsound` 레이블이 붙은 이슈가 100개가 넘는다며
이런 발견 자체는 드물지 않다고 했다.[^weinzierl]
재현 코드를 여럿 만든 theemathas는 HN에서
이번 건이 특이한 것은 재현 코드가 너무 단순하다는 점이며,
다른 불건전성 버그는 컴파일러 검사를 피하려고
코드를 많이 비틀어야 한다고 답했다.[^theemathas]

## 비평

### “11년간 안 걸렸으니 쉽게 걸리지 않는다”는 논리는 공격자에게는 성립하지 않는다

lcnr의 설명은 우발적인 메모리 오류의 가능성을 따지는 데는 타당하다.
그러나 이 논리는 누군가 의도적으로 구멍을 쓰지 않는다는 가정 위에 있다.
HN에서 coliveira는 드물고 고약한 버그도 발견되면 결국 악용된다며,
악의적인 사용자가 이 패턴을 무해해 보이는
코드에 넣기만 하면 된다고 지적했다.[^coliveira]

Rust 생태계의 안전성 주장은
“unsafe 블록이 없으면 메모리 안전”이라는 약속에 크게 기댄다.
코드 리뷰와 감사가 `unsafe`를 찾는 데 집중되는 이유도 그것이다.
이 버그는 `unsafe` 없이 해제 후 사용을 만들 수 있으므로,
그 약속에 기대는 공급망 검사 도구와 리뷰 관행을 우회한다.
우선순위를 “실수로 걸릴 확률”이 아니라
“의도적으로 숨길 수 있는가”로 매겼다면 `P-critical`이 맞았을 것이다.

### 수정이 쉬울 것이라는 기대는 아직 근거가 없다

GrantMoyer는 규칙을 바꿀 필요가 없으니 고치기 쉽다고 봤지만,[^GrantMoyer]
mav65는 잘못된 코드를 거부하면서
올바른 프로그램까지 거부하지 않는 것이 어렵다고 짚었다.[^mav65]
Eridrus는 이 버그를 고쳤을 때 실제로 컴파일되지 않게 되는
크레이트가 있는지 보는 것이 흥미로울 것이라고 했고,[^Eridrus]
Falell은 수정 PR이 공개 크레이트 전체를 빌드하는
crater 실행과 함께 나올 것이라고 답했다.[^Falell]

maxdexh의 배열 통합 버전이 보여 주듯 문제는 필드 대입 하나가 아니라
타입 통합 전반에서 수명 경계를 다시 확인하지 않는 데 있을 수 있다.
그렇다면 수정 범위는 생각보다 넓고,
그만큼 기존 코드가 깨질 위험도 커진다.

### 커뮤니티의 안전 담론에 대한 반발

cheney_2004는 Rust 커뮤니티가 다른 언어의 안전성을 깎아내리면서
공급망 같은 자기 위험은 얼버무린다며,
보안에서 금메달을 주장하는 태도를 버려야 한다고 했다.[^cheney_2004]
이 비판은 버그 자체보다는 담론을 겨눈다.
그러나 이번 이슈에서 Types 팀이 보인 대응,
즉 몇 시간 안에 우선순위를 정하고 배경을 공개하고 장기 로드맵을 연결한 방식은
안전성을 과장하기보다 결함을 관리 대상으로 다루는 쪽에 가깝다.

## 인사이트

### 컴파일러 검증은 증명이 아니라 축적된 신뢰다

WiSaGaN은 이 버그를 동료 검토를 거쳐 받아들여진 수학 증명에서
나중에 오류가 발견되는 일에 빗댔다.[^WiSaGaN]
Rust의 안전성은 언어 설계의 규칙과 그 규칙을
구현한 컴파일러 두 층으로 되어 있다.
규칙이 옳아도 구현이 빠뜨리면 안전성은 깨진다.
mrkeen이 소개한 counterexamples.org처럼 여러 언어의 타입 시스템 구멍을
모은 자료가 있다는 것은
이 문제가 Rust만의 것이 아님을 보여 준다.[^mrkeen]

MrBuddyCasino는 안전 필수 분야용 인증 컴파일러(Ferrocene)도
같은 문제를 갖는지 궁금해했다.[^MrBuddyCasino]
인증은 컴파일러가 특정 명세에 맞게 동작한다는 절차적 보증이지,
타입 시스템의 모든 구멍이 막혔다는 증명이 아니다.
안전성이 중요한 분야일수록 언어의 보증과
컴파일러 구현의 보증을 구분해서 다뤄야 한다.

### AI 기반 퍼징은 이런 구멍을 더 빨리 드러낼 것이다

lambdaone은 AI로 Rust 컴파일러의 버그를 찾는 일이 이런 구멍을 더 많이 찾아내
결국 Rust를 완전한 신뢰성에 가깝게 밀어붙일 것이라고 봤다.[^lambdaone]
이 이슈의 재현 코드가 짧다는 점은 바로 그런 탐색에 유리하다.
몇 줄짜리 프로그램 공간을 체계적으로 생성하고
Miri나 AddressSanitizer로 판정하는 방식이라면
사람이 11년 동안 놓친 조합을 짧은 시간에 훑을 수 있다.

이 흐름은 양쪽으로 작동한다.
방어자가 먼저 찾으면 컴파일러가 단단해지고,
공격자가 먼저 찾으면 `unsafe` 없는 악성 코드가 공급망에 숨는다.
불건전성 이슈 100여 개가 열려 있는 상황에서
어느 쪽이 먼저 체계적으로 탐색하느냐가 앞으로 몇 년의 Rust 보안을 결정할 것이다.

### “unsafe 없음”은 감사 기준으로 충분하지 않다

크레이트를 고를 때 `unsafe` 사용 여부를 확인하는 관행은 유용하지만,
이 버그는 그 관행의 사각지대를 보여 준다.
`Drop` 구현 안에서 `'static` 경계에 기대어 값을
전역이나 다른 스레드로 넘기는 패턴은
`unsafe`가 없어도 위험 신호가 될 수 있다.
불건전성 이슈가 닫히기 전까지는
감사 도구가 `unsafe`뿐 아니라 이런 알려진 패턴까지 찾아야 한다.

## 수정 전까지의 대응

이 이슈를 읽고 곧바로 모든 Rust 코드를 취약하다고 결론 내릴 필요는 없다.
실제 위험은 영향을 받는 컴파일러 버전,
문제의 타입 경계,
그 값을 신뢰해 수명을 연장하는 코드가 함께 있을 때 성립한다.
이슈의 재현만으로 배포된 프로그램이 실제 악용되었다고 말할 수도 없다.

조직은 우선 사용 중인 컴파일러와 종속 크레이트를 목록으로 만들고,
수정 릴리스와 권고가 나오면 영향을 받는 빌드를 다시 시험한다.
제네릭 타입에 `Drop`을 구현하고
참조를 전역 저장소나 다른 스레드로 넘기는 코드는
별도 검토 대상으로 올린다.
Miri나 메모리 검사 도구는 잘못된 동작을 찾는 데 도움이 되지만,
모든 타입 조합의 안전성을 증명하지는 않는다.

임시 조치의 목표는 Rust의 안전성 보장을 포기하는 것이 아니라
현재 알려진 경로를 좁히고 수정 여부를 추적하는 것이다.
컴파일러 수정 전에는 문제가 된 조합에 의존하지 않도록 코드를 바꾸고,
수정 후에는 기존 테스트와 재현 코드를 함께 돌려
정상 코드가 새 제약 때문에 깨지지 않는지도 확인해야 한다.

---

[^GrantMoyer]: <https://news.ycombinator.com/item?id=50070882>

[^vincent-uden]: <https://news.ycombinator.com/item?id=50069748>

[^jvanderbot]: <https://news.ycombinator.com/item?id=50069811>

[^FuzzywarmWalnut]: <https://news.ycombinator.com/item?id=50069792>

[^afdbcreid]: <https://news.ycombinator.com/item?id=50071508>

[^weinzierl]: <https://news.ycombinator.com/item?id=50070471>

[^theemathas]: <https://news.ycombinator.com/item?id=50070843>

[^coliveira]: <https://news.ycombinator.com/item?id=50070898>

[^mav65]: <https://news.ycombinator.com/item?id=50071020>

[^Eridrus]: <https://news.ycombinator.com/item?id=50071964>

[^Falell]: <https://news.ycombinator.com/item?id=50072081>

[^cheney_2004]: <https://news.ycombinator.com/item?id=50071861>

[^WiSaGaN]: <https://news.ycombinator.com/item?id=50071244>

[^mrkeen]: <https://news.ycombinator.com/item?id=50069883>

[^MrBuddyCasino]: <https://news.ycombinator.com/item?id=50069796>

[^lambdaone]: <https://news.ycombinator.com/item?id=50070224>
