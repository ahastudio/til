# Relax

<https://makepad.github.io/relax/>

<https://github.com/makepad/relax>

HN 토론: <https://news.ycombinator.com/item?id=50458849> (180점, 118개 댓글)

GN 토론: <https://news.hada.io/topic?id=37860>

## 소개

Relax는 Makepad 팀이 공개한 Rust용 라이브 컴파일러이자 JIT 런타임이다.
Cargo 패키지를 소스 그대로 실행하며 rustc, LLVM, 링커를 거치지 않는다.
함수를 처음 호출할 때 컴파일하고, 자주 쓰이는 함수는 실행 중에 최적화하며,
수정한 내용을 돌고 있는 프로세스에 바로 반영한다.
README는 이것이 LLM이 Rust 코드를 다룰 때의 지연을 줄이려고 설계한 AI 생성
재구현이며, Rust 프로젝트와 무관한 실험적 개발 도구라고 밝힌다.
릴리스 빌드는 반드시 `cargo build --release`로 하라는 경고도 붙어 있다.

README의 비교표는 다음과 같다.
모든 수치는 프로젝트가 M4 MacBook에서 잰 것이다.

| 항목                                  | cargo + rustc              | Relax                                     |
| ------------------------------------- | -------------------------- | ----------------------------------------- |
| 큰 3D 게임, 새 체크아웃에서 첫 프레임 | 빌드 약 3분 뒤 실행        | 소스에서 바로 11초                        |
| 같은 게임의 두 번째 실행              | 빌드된 바이너리 실행       | 1.15초, 재컴파일 없음                     |
| 함수 하나를 고치고 반영               | 재빌드와 재시작, 상태 소실 | 실행 중 반영, 상태 유지                   |
| 저장 후 테스트 92개 재실행            | 테스트 바이너리 재빌드     | 저장 2.2초 뒤                             |
| 최적화된 코드의 속도                  | 1.00배                     | x64 1.12배, arm64 1.24배 느림             |
| 필요한 것                             | rustc, LLVM, 링커          | 라이브러리 하나, 43.8만 줄, 외부 의존성 0 |

JIT이라서 가능한 기능도 따로 정리되어 있다.
저장하면 바뀐 함수만 다시 검사해 교체하는 핫 패치,
수정한 함수에 닿는 테스트만 다시 돌리는 저장 시 테스트,
패닉이 나면 스레드를 스택째 멈춰 두고 지역 변수를 읽고 식을 평가하는 기능,
디버거 없는 중단점, 교착 원인 설명, 프로파일링, 항상 켜진 비행 기록기,
메모리 누수 후보 추적이 있다.

## 한계

프로젝트가 직접 적은 한계는 다섯 가지다.
최적화된 코드가 rustc의 `--release`보다 느리고,
컴파일러와 캐시가 프로그램 프로세스 안에 있어 메모리를 더 쓴다.
`relax check`는 아직 `cargo check`보다 빠르지 않고,
모든 크레이트가 돌지는 않으며,
구조체 배치, import, 트레이트 헤더, 매크로를 바꾸면 재시작이 필요하다.
빌림 검사기(borrow checker)는 프로그램 옆에서 비동기로 돌아서,
검사가 끝나기 전에 코드가 실행될 수 있다.
README는 Makepad 자체의 편집-실행 루프에서만 주로 시험했고 다른 프로젝트에서는
가볍게만 시험했다고도 말한다.

## 분석

### 컴파일 대기를 없애는 방식

핵심은 빌드와 실행을 나누지 않는다는 점이다.
함수 단위로 필요할 때 컴파일하므로 처음 보이는 화면까지의 시간이 줄고,
실행 중인 프로세스가 컴파일러를 품고 있어서 수정과 상태 보존이 가능하다.
이 설계의 값은 코드 속도에서 지불된다.
그래서 프로젝트도 릴리스는 rustc로 하라고 선을 긋는다.

### 수치의 범위

11초와 약 3분이라는 비교는 큰 3D 게임 한 종류에서 나왔고,
기기도 M4 MacBook 한 대다.

## 비평

### 다른 프로젝트에서의 작동

HN의 ben-schaaf는 여러 Rust 프로젝트로 시험해 대부분 실행되지 않았고,
하나는 오동작했으며, 돌아간 actix-web 사이트는 서버가 뜨는 데 14초가 걸렸다고
썼다.
같은 프로젝트의 일반 증분 디버그 빌드는 2.3초였다고 한다.[^ben-schaaf]
suddenlybananas는 네 개 중 두 개가 컴파일되지 않았고,
돌아간 둘도 테스트가 20% 느리거나 같았다고 답했다.[^suddenlybananas]
README가 다른 프로젝트에서는 가볍게만 시험했다고 말한 것과 맞는 보고다.
다만 이 시험은 개인 프로젝트에서의 결과이고 시점도 공개 직후다.

### 성공한 시험과 그 조건

반대 방향의 보고도 있다.
amarko는 자기 프로젝트에서 돌려 보고 컴파일되도록 PR을 보내 병합되었으며,
테스트는 cargo로 검증하고 Relax는 변경을 받아들이기 전 앱을 빨리 확인하는 데
쓴다고
썼다.
테스트 묶음은 cargo보다 많이 느렸고 핫 패치는 시험하지 않았다고 한다.[^amarko]
tkng는 약 20만 줄 규모의 사내 Rust 프로젝트에서 소스 쪽 수정 두 건과 Relax 쪽
수정
한 건 뒤에 돌아갔고, 6분이 넘던 빌드가 약 70초로 줄었다고 보고했다.
전체 테스트는 cargo와 rustc로 돌리는 것이 낫지만 몇 개만 돌릴 때는 매우
유용하다는
평가다.[^tkng]
두 보고 모두 코드를 고치거나 PR을 보낸 뒤의 결과라서,
ben-schaaf와 suddenlybananas의 실패 보고와 모순되기보다 “바로는 안 돌지만 고치면
돈다”는 같은 현상의 양면으로 읽힌다.

### 다른 접근

knuckleheads는 rustc/cargo의 패치 포크를 유지하는 방식을 원하지 않아
기존 도구 위에 얹는 쪽으로, 컴파일러 팀의 LLM 사용 방침을 존중하면서 속도를
높이는 방법을 찾고 있다고 썼다.[^knuckleheads]
jkelleyrtp는 Rust Analyzer가 코드를 내보내게 해 브라우저에서도 돌아가는 비슷한
시도를 소개했다.[^jkelleyrtp]
개발 반복 속도를 줄이는 방법이 JIT 재구현, 컴파일 데몬, 캐시 등으로 갈려 있다는
것을 보여 준다.

### 기존 대안과의 관계

medler는 같은 영역에 10년 넘게 유지되는 Cranelift 컴파일러가 있다고
지적했다.[^medler]
_cart는 한 달 사이에 AI로 만든 Rust 반복 컴파일러가 세 개 나왔다는 점이
놀랍다고 했다.[^_cart]
pcwalton은 이 프로젝트를, 매우 야심 차지만 개념적으로는 어렵지 않은 일을 AI
에이전트가 가능하게 만든 교과서적인 예라고 보았다.[^pcwalton]
이는 프로젝트의 정체성과도 이어진다.
README가 AI 생성임을 맨 앞에 밝히고 있어서, 신뢰의 근거를 코드 품질이 아니라
검증 결과에서 찾아야 한다.

### 안전성

HN의 Surac은 오류를 컴파일 시점에서 실행 시점으로 옮기는 것이 좋은 일이냐고
물었고,
jtwaleson은 로컬 개발을 빠르게 하는 용도라면 훌륭한 거래라고
답했다.[^Surac][^jtwaleson]
README도 Rust의 안전 보장이 자동으로 유지되지 않는다고 적고 있어서,
이 거래는 개발 반복에만 한정된다는 점이 전제다.

## 인사이트

### 반복 속도를 위한 개발 전용 도구

Relax는 완성된 컴파일러를 목표로 하지 않고 편집-실행 루프의 지연만 겨냥한다.
faresahmed는 코딩과 실행 사이의 시간을 줄이려는 시도가 Lisp의 계산 모델부터
Bret Victor의 발표까지 반복되어 왔다고 썼다.[^faresahmed]
Capricorn2481은 Rust의 빌드 시간이 단순한 취향이 아니라는 점에서 Lisp와는
다르다고 되받았다.[^Capricorn2481]
두 입장 모두 이 프로젝트가 해결하려는 문제가 실재한다는 데에는 이견이 없다.
각자 조건에서 시험해 보고 판단할 수 있는 도구다.

---

[^amarko]: <https://news.ycombinator.com/item?id=50490845>

[^tkng]: <https://news.ycombinator.com/item?id=50497690>

[^knuckleheads]: <https://news.ycombinator.com/item?id=50481795>

[^jkelleyrtp]: <https://news.ycombinator.com/item?id=50473288>

[^ben-schaaf]: <https://news.ycombinator.com/item?id=50477968>

[^suddenlybananas]: <https://news.ycombinator.com/item?id=50482409>

[^medler]: <https://news.ycombinator.com/item?id=50476410>

[^_cart]: <https://news.ycombinator.com/item?id=50474806>

[^pcwalton]: <https://news.ycombinator.com/item?id=50473732>

[^Surac]: <https://news.ycombinator.com/item?id=50472751>

[^jtwaleson]: <https://news.ycombinator.com/item?id=50472848>

[^faresahmed]: <https://news.ycombinator.com/item?id=50472606>

[^Capricorn2481]: <https://news.ycombinator.com/item?id=50472669>
