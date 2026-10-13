# Valen의 그룹 대여: 참조가 가리키는 곳을 기억하는 대여 검사

원문: [Valen's Memory Safety: A New Kind of Borrow Checking](https://verdagon.dev/blog/valen-group-borrowing)

HN 토론: <https://news.ycombinator.com/item?id=50042362> (163점, 93개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/gmnqhj/valen_s_memory_safety_new_kind_borrow> (32점, 5개 댓글)

GN 토론: <https://news.hada.io/topic?id=35190>

## 요약

Vale 언어를 만든 Evan Ovadia가 후속 언어 Valen의
새 대여 검사기(borrow checker)를 소개한 글이다.
2026년 10월 11일에 올라왔다.
저자는 Rust 대여 검사만큼 강력하면서
참조 카운팅이나 가비지 컬렉션만큼 단순하고
유연한 메모리 안전성을 “성배”라고 부르고,
거기에 닿으려면 세 문제를 풀어야 한다고 말한다.
더 느슨한 대여 검사기를 만들 수 있는가,
대여 검사기가 더 복잡한 데이터 그래프를 읽을 수 있는가,
두 체계를 동시에 함께 쓸 수 있는가다.
이 글은 첫 번째 문제를 다룬다.

Valen의 접근은 저자의 친구 Nick Smith가
설계한 그룹 대여(group borrowing) 제안에서 출발한다.
원래 Mojo를 위해 설계했지만 채택되지 않았고,
저자와 Nick Smith가 지난해 설명 글을 공개한 뒤
Google의 Carbon이 이 방식으로 전환했고
Ante, Plecra의 exclusion typing, Zeta, Fang도 받아들였다고 한다.
핵심은 기존 대여 검사의 “shared-xor-mutable” 제약,
즉 참조를 들고 있는 동안 아무도 객체를 바꿀 수 없다는 규칙을
“use-after-free 금지”로 완화하는 것이다.
이 덕분에 같은 객체를 가리키는 여러 지역 변수나 매개변수로 각각 쓰기,
객체와 그 안쪽을 함께 받아 안쪽만 쓰기,
ScopeGuard 같은 되돌림 구조체,
여러 구조체가 공통 하위 시스템에 가변 참조를 들고 있는 패턴을
컴파일 타임에 안전하게 허용한다고 주장한다.

동작 원리는 다섯 가지 규칙이다.
단일 소유권에 따라 모든 객체는 `world.entities[].hp` 같은 경로(path)로 기술된다.
모든 참조는 자신이 가리키는 경로를 기억한다.
객체를 파괴하면 그 경로 안쪽을 가리키는 참조는 쓸 수 없게 된다.
함수 시그니처는 자신이 수정하는 경로를 밝힌다.
함수를 호출하면 그 함수가 수정하는 경로 안쪽을 가리키는 참조는 무효화된다.
중요한 구분은 객체를 가리키는 참조는 살아남고,
객체 안쪽을 가리키는 참조만 무효화된다는 점이다.
`vec.push()` 뒤에도 `&vec`는 쓸 수 있지만 `&vec[0]`은 쓸 수 없다.

Valen에는 대여 참조가 한 종류뿐이다.
C++의 const와 non-const, Rust의 `&`와 `&mut` 같은 구분이 타입에 없고,
가변성은 `mut(self)`처럼 함수 시그니처의 효과(effect)로 표현된다.
대표 예제는 `func step(world &World, entity in world.entities[] mut)`로,
`entity`가 `world.entities`의 원소 중 하나를 가리키며
그것만 수정할 수 있다는 뜻이다.
저자는 같은 일을 C++로 쓰면 단순하지만 안전하지 않고,
Rust로 쓰면 안전하지만 매번 인덱스로 다시 참조를 얻느라 느리고 복잡하며,
GhostCell을 쓰면 빠르지만 여전히 복잡하다고 비교한다.

원래 그룹 대여 위에 Valen이 더한 것은 세 가지다.
불변 객체 안의 일부만 가변으로 받는
Mutable-in-Immutable은 더 강한 API와 최적화 여지를 준다.
Rust 호출 시 그 호출 동안 데이터에 닿는 유일한 참조라면 `&mut`로,
아니면 `&`로 넘기는 일시적 유일성(Temporary Uniqueness)은
Rust 상호 운용을 위한 장치다.
Rust 함수가 반환한 참조를 `in self.gem...`처럼 “어딘가 안쪽”으로 해석하는
와일드카드 후손 경로(Wildcard Descendant Paths)도 같은 목적이다.
나머지 두 문제, 즉 참조 카운팅과 세대 참조를 섞는 일은
힙을 타입별 배열로 보는
2023년의 사고 실험 Arrrlang을 바탕으로 다음 글에서 다룬다고 예고한다.
부록에서는 원시 값처럼 타입이 바뀔 수 없는 데이터는
무효화하지 않는 type-stability 예외도 소개한다.

## 분석

### 무효화의 단위를 “참조”에서 “경로”로 옮긴 것이 핵심이다

Rust의 대여 검사는 참조를 만드는 순간 규칙을 건다.
`&mut`를 들고 있으면 다른 누구도 그 객체를 보지 못하게 미리 막는 방식이다.
Valen은 규칙을 거는 시점을 뒤로 미룬다.
참조는 자유롭게 여러 개 만들 수 있고,
실제로 어떤 경로가 수정되었을 때
그 경로 안쪽을 가리키던 참조만 사후에 무효화한다.

이 차이가 허용 범위를 넓힌다.
같은 리스트에 두 참조로 차례로 `push`하는 예제가 Rust에서 막히는 이유는
둘 다 `&mut`가 되어야 하기 때문인데,
Valen에서는 리스트 자체를 가리키는 참조는 `push`로 무효화되지 않으므로 통과한다.
금지 대상이 “동시에 존재하는 가변 별칭”에서
“이미 사라진 메모리를 가리키는 접근”으로 좁혀진 셈이다.

저자가 각주에서 그룹 대여를 “컴파일 타임 세대 참조”라고
부르는 것도 같은 맥락이다.
세대 참조가 런타임에 대상 객체의 세대 번호를 기억하듯,
그룹 대여는 컴파일 타임에 대상의 경로를 기억한다.
Vale에서 세대 참조와 지역 대여를 섞었던 저자가
그 직관을 컴파일 타임 분석으로 옮겨 온 것으로 읽을 수 있다.

### 가변성을 타입에서 함수 효과로 옮긴 결정이 상호 운용을 떠받친다

Valen의 대여 참조가 한 종류뿐이라는 점은 단순함 이상의 의미가 있다.
가변성이 참조의 타입이 아니라 함수가 선언한 효과라면,
같은 참조를 Rust에 넘길 때 그 호출의 맥락만 보고
`&`인지 `&mut`인지 정할 수 있다.
Temporary Uniqueness는 바로 이 성질을 이용한다.

저자는 HN에서 이 설계가 shared-xor-mutable을 버린 것이 아니라
선택 가능하게 만든 것이라고 설명했다.
어떤 그룹에 `mut` 효과를 가진 함수가 다른 별칭을
`in`으로 선언하지 않으면 사실상 유일 참조이고,
`mut` 효과가 하나도 없으면 사실상 공유 불변 참조라는 것이다.
가변 별칭은 `in`으로 명시해야 생기므로
기본값은 오히려 shared-xor-mutable 쪽으로 기운다고 덧붙였다.[^verdagon-xor]

이렇게 보면 Valen의 목표는 Rust를 대체하는 것이 아니라
Rust 생태계 위에 올라타는 것이다.
Kotlin이 Java를, C++이 C를 부르듯 Rust를 부르겠다는 목표가
대여 검사기의 모양을 결정했다.

### 이 글은 한 아이디어의 확산 기록이기도 하다

글의 앞부분은 기술 설명보다 그룹 대여가 어떻게 퍼졌는지에 대한 이야기다.
Mojo 내부에서 채택되지 못한 제안이 공개 글 한 편으로
Carbon, Ante, Zeta, Fang에 흘러 들어갔고,
이제 Valen이 그것을 Vale의 기법과 섞는다.
여러 언어가 같은 문제,
즉 “더 유연한 대여 검사기”라는 과제를 중심으로 모이고 있다는 진단이 깔려 있다.

HN에서 melodyogonna는 Mojo의 origin이 이런 의미 일부를 표현할 수 있고
Nick Smith의 제안에서 많이 배운 것으로 보인다고 했지만,
저자는 Mojo가 모든 매개변수를 유일 참조나 공유 참조로 강제해
`step` 예제는 표현하지 못한다고 답했다.[^melodyogonna][^verdagon-mojo]
maufl이 Rust에 이 대여 검사기를 이식할 수 있느냐고 묻자,
저자는 Niko Matsakis의 장소 기반 수명 구상과
Polonius가 이미 경로로 생각한다는 점을 들어
컴파일러 설계보다 언어 설계의 문제라고 답했다.[^maufl][^verdagon-rust]

## 비평

### shared-xor-mutable을 메모리 안전성의 장애물로만 그린다

글은 shared-xor-mutable을 다른 메모리 관리 방식과 충돌하는 제약으로 소개하고,
그룹 대여가 이를 “use-after-free 금지”로 완화해 갈등을 해소한다고 말한다.
그러나 이 제약은 use-after-free만을 위한 것이 아니다.
HN의 zamalek은 이 규칙이
동시성 코드에서 특정 버그 부류를 생각하지 않아도 되게 해 주는 장치이며,
Rust의 “fearless concurrency”가 여기서 나온다고 반박했다.[^zamalek]
octoberfranklin은 더 구체적으로,
Rust 프로그램은 shared^mutable을 먼저 증명하게 강제하기 때문에
`Vec`가 있는 곳에 Rayon만 넣어도 쉽게 멀티코어가 되고,
그 결과 Rust 생태계의 계산 집약 라이브러리가 사실상 자동으로 병렬화된다고
지적했다.[^octoberfranklin]

dgrunwald의 지적은 더 근본적이다.
Rust 열거형처럼 태그 유니언의 필드에 대한 참조를 허용하는 언어에서는
다른 변형으로 바꾸는 순간 기존 필드의 수명이 끝나므로
use-after-free를 막기 위해서도 shared-xor-mutable이
필요하다는 것이다.[^dgrunwald]
글의 부록이 열거형 내용물을 “type-unstable”로 분류해 무효화 대상으로 둔 것은
이 문제를 인식하고 있다는 뜻이지만,
본문은 shared-xor-mutable을 버려도 되는 부담처럼 서술한다.

반대편 논리도 있다.
pron은 안전한 부분 집합을 좁힐수록 올바른 프로그램이 unsafe로 밀려나며,
심각한 취약점의 원인으로는 경계 밖 접근과 use-after-free가 압도적이지
동시성 문제가 그만큼 대표적이지는 않다고 반론했다.[^pron]
그러나 VorpalWay가 답했듯 찢어진 쓰기(torn write) 같은 동시성 문제는
다른 스레드에서 경계 밖 접근과 미정의 동작을 쉽게 일으킨다.[^VorpalWay]
이 논쟁은 글이 다음 편으로 미룬 structured concurrency 설계가
얼마나 설득력 있게 나오느냐에 따라 결론이 달라진다.

Lobste.rs에서 polywolf가
동시성에서의 값 무효화가 TOCTTOU 문제를 낳을 수 있다고 걱정하자,
저자는 구현할수록 무효화와 일반 대여 검사가
사실상 같은 것이라는 점을 발견하고 있다며,
structured concurrency로 다른 스레드와 공유 중인 데이터는
그동안 수정할 수 없다고 답했다.[^polywolf][^Verdagon-lobsters]
polywolf는 그것이 “기묘하게 shared-xor-mutable과 비슷하다”고 받으면서,
`mut` 효과가 없는 클로저만 structured concurrency에 넘기고
뮤텍스가 내부의 `mut` 효과를 바깥에 드러내지 않게 하는 계획으로 정리했고,
저자는 정확히 그렇다고 동의했다.[^polywolf-plan][^Verdagon-agree]
결국 동시성 영역에서
Valen은 shared-xor-mutable을 다른 이름으로 다시 들여오는 셈이며,
그렇다면 글이 이 제약을 극복 대상으로 그린 서술은 단일 스레드 코드에만 해당한다.

### 경로가 시그니처에 드러나면 추상화 비용이 생긴다

그룹 대여의 핵심 규칙 하나는
“함수 시그니처가 자신이 수정하는 경로를 밝힌다”는 것이다.
octoberfranklin은 이것이 추상화에 비용을 매긴다고 지적했다.
필드 경로는 구조체의 구체적인 구현에 묶여 있으므로,
필드를 숨기고 getter와 setter를 쓰면
그 함수가 어떤 경로를 수정하는지 말할 수 없게 된다는
것이다.[^octoberfranklin-abstraction]
C++과 Rust가 지켜 온 제로 비용 추상화 원칙과 정면으로 부딪힌다.

글도 이 긴장을 일부 알고 있다.
와일드카드 후손 경로 `in self.gem...`이 시그니처에서 내부 세부 사항을 지우고
라이브러리 API를 더 유연하게 만들 수 있다고 쓰고,
비공개 그룹을 공개 이름으로 다시 내보내는
“associated group”도 각주에서 언급한다.
그러나 이것들은 Rust 상호 운용을 위해 들여온 장치로 소개될 뿐,
캡슐화와 경로 노출 사이의 균형을 어떻게 잡는지는 설명하지 않는다.
대형 코드베이스에서는 구현을 바꿀 때마다 시그니처가
바뀌는 문제가 먼저 나타날 것이다.

같은 지점을 Lobste.rs의 polywolf도 짚었다.
지난해 그룹 대여 글을 읽었을 때는
모든 필드가 공개된 단순한 구조체와 배열에는 맞지만,
이진 트리나 연결 리스트처럼
“경로 추상화”가 필요한 구조에서는 금방 다루기 어려워질 것이라 봤고,
와일드카드 경로가 그 불만을 해결한다고 평가했다.[^polywolf]
저자는 연관 타입처럼 그룹과 경로를 다루는 “associated groups/paths”가
경로 추상화를 더 도울 것이라고 답했다.[^Verdagon-lobsters]
즉 해법의 방향은 있지만,
그것이 실제 라이브러리 설계에서 얼마나 무거운지는 아직 보여 주지 않았다.

### 예제가 정적인 세계를 가정한다

글의 예제는 모두 `World`와 `Entity` 같은 게임 개발 용어로 되어 있다.
SleepyMyroslav는 코드가 시스템의 모든 경로를 정적으로 아는 구조에는 잘 맞겠지만,
요즘 게임은 대부분 데이터 주도 방식으로 옮겨 갔으므로
이 예제는 오해를 부른다고 지적했다.[^SleepyMyroslav]
엔티티의 `advance`는 실제로는 블루프린트 실행에 가깝고,
그때 무엇이 어떤 경로를 수정하는지 컴파일러가 알기 어렵다.

예제에 제어 흐름이 없다는 점도 같은 문제다.
user142가 이를 묻자 저자는 if 문은 두 분기의 무효화를 합치고,
반복문은 본문 안의 무효화를 미리 찾아 본문 앞에서
“재생”한다고 답했다.[^user142][^verdagon-loops]
user142는 다시 제어 흐름에 따라 참조가
서로 다른 경로를 가리키는 경우를 물었는데,[^user142-paths]
이 질문은 글의 경로 모델이 가장 먼저 시험받을 지점이다.
경로가 정적으로 하나로 정해지지 않을 때 Valen이 그것을 어떻게 표현하는지,
혹은 그런 코드를 금지하는지는 아직 공개되지 않았다.

### “아무도 해결하지 못한 문제”라는 틀은 선행 연구를 지운다

저자는 이런 패턴을 컴파일 타임에 메모리 안전하게 모두 다룬 언어는 없다고 쓴다.
pjmlp는 Rust보다 강력한 알고리즘이 Cyclone부터 시작해
함수형 언어의 의존 타입, 증명, 효과, capability 연구에 이미 있었고,
많은 사람이 Rust로만 이 주제를 접해 계시처럼 여긴다고 꼬집었다.[^pjmlp]
EliasLittle은 가변성을 데이터가 아니라 함수 인자의 속성으로 두는 설계가
Jane Street OxCaml의 mode를 떠올리게 한다고 했고,[^EliasLittle]
Panzerschrek은 자신의 언어가 2020년쯤부터 비슷한 기능을 갖고
있었다고 주장했다.[^Panzerschrek]
Lobste.rs의 davidbalbert는
Ante의 안전한 공유 가변성이 OxCaml의 uniqueness mode와 사실상 같아 보이고,
Ante가 “shape-stable”이라 부르는 개념이 이 글의 “type-stable”과 같은 것 같다며
OxCaml mode와의 관계를 물었다.[^davidbalbert]

글은 Carbon, Ante, Zeta 같은 동시대 언어와의 관계는 자세히 다루지만,
Cyclone의 영역 기반 포인터나 Polonius처럼 직접 연관된 선행 작업은 본문에서
비교하지 않는다.
다음 글에서 여러 언어의 접근을 비교하겠다는 예고가 있으므로,
그 글이 이 공백을 얼마나 메우느냐가 그룹 대여의 위치를 정할 것이다.

## 인사이트

### 대여 검사의 이름 논쟁은 개념의 중심이 어디인지에 대한 논쟁이다

HN에서 여러 사람이 반응한 주제 가운데 하나는 이름이었다.
저자 스스로 “그룹”은 아이디어 이해에 핵심이 아니라며
경로 대여(path borrowing)가 더 나은 이름일 수 있다고 썼고,[^verdagon-name]
kvark, _old_dude_, falconBrisk47 모두 “경로”가 핵심 개념을 더 잘 드러낸다고
동의했다.[^kvark][^_old_dude_][^falconBrisk47]
falserum은 단일 소유권이
`main`에서 뻗는 소유 트리이고 각 경로가 부분 트리를 가리키므로
“부분 트리 대여(subtree borrowing)”를 제안했다.[^falserum]

이 논쟁은 단순한 작명 취향이 아니다.
“그룹”은 무효화가 묶여서 일어나는 구현 방식을 가리키고,
“경로”와 “부분 트리”는 소유권 트리 위의 위치라는 개념을 가리킨다.
munchler가 `in`이라는 키워드가 .NET 개발자에게 반복을 연상시킨다고
지적한 것도 같은 맥락이다.[^munchler]
새 언어 개념은 이름과 문법이 기존 직관과 어긋나면
개념 자체보다 이름을 이해하는 데 비용이 든다.
Rust의 “lifetime”이 실제로는 코드 구간에 가까운 개념이어서
오랫동안 초보자를 헤매게 한 것처럼,
그룹 대여가 확산되려면 개념의 중심을 정확히 가리키는 이름이 먼저 필요하다.

### 가비지 컬렉션의 도달 가능성 분석이 컴파일 타임으로 내려오고 있다

torginus는 경로 검사를 컴파일 타임 추적 GC로 볼 수 있다고 적었다.
컴파일러가 아는 루트가 있고,
코드의 각 지점에서
루트가 범위를 벗어날 때마다 생존 분석을 한다는 비유다.[^torginus]
저자 자신도 그룹 대여를 컴파일 타임 세대 참조라고 불렀고,
다음 단계로 힙을 타입별 배열로 보는 Arrrlang 모델로
참조 카운팅을 대여 검사기에 설명하겠다고 한다.

이 흐름은 메모리 관리 기법들이 서로의 모델을
빌려 오는 수렴 과정으로 읽을 수 있다.
GC는 런타임에 도달 가능성을 계산했고,
Rust는 수명이라는 정적 근사로 같은 질문에 답했으며,
Valen은 소유 트리의 경로라는 더 구체적인 정적 구조로 답하려 한다.
저자가 각주에서 Iris가 Rust의 안전성을 형식 검증할 때 힙을
같은 방식으로 표현한다고 언급한 점도 의미심장하다.
검증 도구의 내부 모델이 언어 사용자가 쓰는 표면 문법으로 올라오는 중이다.

### 최적화 이득은 LLVM이 따라오기 전까지 약속에 머문다

글은 Mutable-in-Immutable이 최적화기에 더 세밀한 정보를 주어
“어떤 언어도 하지 못한 방식으로” 최적화기를 활용할 수 있을지 모른다고 쓴다.
그러나 같은 글의 각주는 이를 위해 LLVM을 패치해야 할 수 있으며,
LLVM은 “읽기 전용”이 아니라 `noalias` 관점으로 생각한다고 인정한다.
또 Valen이 C++이나 Rust보다 빨라지는 것은 아니며,
주된 이점은 속도가 아니라 사용성과 유연성이라고 스스로 낮춘다.

이 간극은 새 언어가 흔히 겪는 문제다.
언어가 더 많은 의미 정보를 표현해도 백엔드가
그 정보를 받을 통로가 없으면 이득은 사라진다.
저자가 HN에서 GPU 컴파일을 위해 Rust MIR, SPIR-V,
MLIR 중 어디로 내릴지 고민 중이라고 밝힌 것도 같은 문제다.[^verdagon-gpu]
Rust MIR로 내리면 Rust 생태계와 붙기 쉽지만
그룹 대여가 주는 정보를 MIR이 담을 수 있는지는 미지수다.
Valen의 실용성은 대여 규칙의 우아함보다
그 규칙이 실제 기계어 품질로 이어지는 경로를 확보하느냐에 더 크게 달려 있다.

### Rust 상호 운용이라는 목표는 언어 설계의 자유를 미리 저당 잡는다

Valen은 Rust 함수를 자연스럽게 부르기 위해
Temporary Uniqueness와 와일드카드 후손 경로를 만들었다.
이 결정은 생태계라는 거대한 이점을 주지만,
동시에 Valen의 의미론이 Rust의 `&`/`&mut` 구분과
계속 맞물려야 한다는 제약을 만든다.
글 스스로 Rust의 `Vec<&mut Ship>` 같은 유일 참조 컬렉션을 지원하려면
“unique group” 같은 두 번째 참조 종류가 필요할 수 있고,
그것은 Valen의 가장 큰 장점인 단일 참조 종류를 흔든다고 인정한다.

Kotlin과 Java의 관계가 좋은 비교 대상이다.
Kotlin은 Java 상호 운용을 위해 플랫폼 타입이라는 타협을 들여왔고,
그 타협은 null 안전성이라는 핵심 약속에 구멍을 남겼다.
Valen도 Rust 경계에서 비슷한 타협 지점을 갖게 될 가능성이 크다.
amluto가 Rust의 `&T`는 “아무도 바꾸지 않는다”는 약속을 주는데
Valen이 스레드와 클로저를 거친 깊은 호출 체인에서도
그 약속을 지킬 수 있는지 물은 것이 바로 그 경계다.[^amluto]
저자는 효과로 “캡처한 것을 수정하지 않는 클로저”를 표현하겠다고
답했지만,[^verdagon-closure]
그 설계가 Rust의 보장과 정확히 맞물리는지는 다음 글들이 증명해야 한다.

---

[^verdagon-xor]: <https://news.ycombinator.com/item?id=50046041>

[^melodyogonna]: <https://news.ycombinator.com/item?id=50045572>

[^verdagon-mojo]: <https://news.ycombinator.com/item?id=50045745>

[^maufl]: <https://news.ycombinator.com/item?id=50043324>

[^verdagon-rust]: <https://news.ycombinator.com/item?id=50043524>

[^zamalek]: <https://news.ycombinator.com/item?id=50045650>

[^octoberfranklin]: <https://news.ycombinator.com/item?id=50046618>

[^dgrunwald]: <https://news.ycombinator.com/item?id=50053945>

[^pron]: <https://news.ycombinator.com/item?id=50047801>

[^VorpalWay]: <https://news.ycombinator.com/item?id=50052935>

[^octoberfranklin-abstraction]: <https://news.ycombinator.com/item?id=50046505>

[^SleepyMyroslav]: <https://news.ycombinator.com/item?id=50045848>

[^user142]: <https://news.ycombinator.com/item?id=50043494>

[^verdagon-loops]: <https://news.ycombinator.com/item?id=50043591>

[^user142-paths]: <https://news.ycombinator.com/item?id=50043736>

[^pjmlp]: <https://news.ycombinator.com/item?id=50053813>

[^EliasLittle]: <https://news.ycombinator.com/item?id=50047245>

[^Panzerschrek]: <https://news.ycombinator.com/item?id=50051801>

[^verdagon-name]: <https://news.ycombinator.com/item?id=50042493>

[^kvark]: <https://news.ycombinator.com/item?id=50044156>

[^_old_dude_]: <https://news.ycombinator.com/item?id=50045265>

[^falconBrisk47]: <https://news.ycombinator.com/item?id=50042814>

[^falserum]: <https://news.ycombinator.com/item?id=50047280>

[^munchler]: <https://news.ycombinator.com/item?id=50043294>

[^torginus]: <https://news.ycombinator.com/item?id=50052910>

[^verdagon-gpu]: <https://news.ycombinator.com/item?id=50043440>

[^amluto]: <https://news.ycombinator.com/item?id=50044588>

[^verdagon-closure]: <https://news.ycombinator.com/item?id=50045928>

[^polywolf]: <https://lobste.rs/s/gmnqhj/valen_s_memory_safety_new_kind_borrow#c_h24jpb>

[^Verdagon-lobsters]: <https://lobste.rs/s/gmnqhj/valen_s_memory_safety_new_kind_borrow#c_gdcxr4>

[^polywolf-plan]: <https://lobste.rs/s/gmnqhj/valen_s_memory_safety_new_kind_borrow#c_fuattz>

[^Verdagon-agree]: <https://lobste.rs/s/gmnqhj/valen_s_memory_safety_new_kind_borrow#c_qzsbmg>

[^davidbalbert]: <https://lobste.rs/s/gmnqhj/valen_s_memory_safety_new_kind_borrow#c_cewa4e>
