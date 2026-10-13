# TurboPython: GC도 GIL도 없이 Python 문법을 네이티브 바이너리로

<https://tpy-lang.org/>

<https://github.com/trozen/tpy-lang>

HN 토론: <https://news.ycombinator.com/item?id=49954875> (27점, 14개 댓글)

GN 토론: <https://news.hada.io/topic?id=35267>

## 소개

TurboPython(TPy)은 Python 문법으로 쓴 코드를 C++로 옮긴 뒤
네이티브 바이너리로 컴파일하는 정적 타입 언어이자 컴파일러다.
홈페이지는 이 언어를 Python의 문법에 소유권(ownership) 모델을 더해
가비지 컬렉터, 자동 참조 카운팅, GIL 없이
메모리 안전성과 예측 가능한 성능을 얻는 언어로 소개한다.

내세우는 특징은 다섯 가지다.

- 익숙한 Python 문법: 타입 어노테이션과 몇 가지 확장을 더한 표준 Python이라
  대부분의 편집기, 타입 검사기, 린터가 그대로 동작한다.
- 네이티브 컴파일: 독립 실행 바이너리를 만들고, 고정 폭 정수, 포인터,
  스팬 같은 시스템 수준 제어를 제공하며, GIL 없이 멀티스레딩을 한다.
- 예측 가능한 성능과 메모리: 메모리를 컴파일 시점에 소유권과 빌림으로 관리하고,
  공유 소유권이 필요할 때만 `Rc`를 명시적으로 쓴다.
- 컴파일 시점 메모리 안전성: 해제 후 사용(use-after-free)과
  별칭(aliasing) 버그를 실행 전에 잡는다.
- 앱 또는 확장: 독립 바이너리, CPython 확장 모듈,
  `@native`를 통한 기존 C/C++ 호출을 모두 지원한다.

홈페이지 맨 위에는 초기 개발 단계라는 경고가 붙어 있다.
핵심 언어는 실제 프로그램을 컴파일하고 실행하지만,
평범한 Python 구문 일부가 아직 거부되고, 표준 라이브러리는 일부만 있으며,
알려진 버그가 조용히 틀린 결과를 낼 수 있다고 적었다.

2026년 10월 13일 기준 문서는 0.6.2 버전을 설명한다.
저장소는 2026년 3월 3일에 만들어졌고,
라이선스는 LLVM 예외 조항을 붙인 Apache-2.0이다.
이 예외 덕분에 컴파일 결과물에 런타임 코드가 들어가도
Apache-2.0의 고지 의무 일부를 지키지 않고 배포할 수 있다.
커밋 2,583개가 모두 `trozen` 한 계정에서 나왔다.
GitHub 스타는 13개이고,
GitHub 릴리스 없이 PyPI의 `tpy-lang` 패키지로만 배포된다.

## 동작 방식

### 컴파일 경로

프로그램은 타입 검사를 거쳐 C++로 번역되고, 시스템 C++ 컴파일러로 빌드된다.
C++23을 지원하는 GCC 13 이상이나 Clang 19 이상이 필요하고,
`tpy-lang[bundled]`를 설치하면 zig를 C++ 컴파일러로 함께 받는다.
기본 빌드는 `-O3` 최적화이고, `--debug`는 `-g -O0`으로 빌드한다.
오버플로 검사 같은 런타임 검사는 두 빌드 모두에서 유지된다.

결과 바이너리는 Python 설치 없이 돌아가며,
C++ 런타임과 libc 같은 표준 시스템 라이브러리만 링크한다.
Linux와 macOS를 지원하고, Windows에서는 WSL 안에서 Linux 바이너리를 만든다.

`tpyc -o build program.py`는 네이티브 빌드를 건너뛰고 C++ 프로젝트만 내보낸다.
이 프로젝트에는 `sources.cmake`가 들어 있어 기존 CMake 빌드에 넣을 수 있고,
`--no-main`을 주면 생성된 `main()` 없이 다른 C++ 프로그램에 링크된다.
`tpyc --dump-code`는 생성된 C++를 표준 출력으로 보여 준다.

### 소유권 모델

문서가 “Python과 다른 유일한 깊은 차이”라고 부르는 부분이다.
먼저 값 타입과 참조 타입을 나눈다.
`int`와 고정 폭 정수, `float`, `bool`, `str`, `char`, 이들의 튜플은
값 타입이라 대입할 때 복사되고, 소유권 규칙과 무관하다.
클래스 인스턴스, `list`, `dict`, `set` 같은 참조 타입 객체는
컴파일 시점에 알려진 소유자를 정확히 하나 가지며,
소유자가 사라질 때 함께 해제된다.

- 함수가 만든 객체는 그 함수의 프레임이 소유하고,
  함수가 반환할 때 해제된다.
- 필드나 컨테이너에 저장된 객체는 그 저장소가 소유한다.
  문서는 이를 지속 저장소(durable storage)라고 부르고,
  컴파일러 진단은 owned storage라고 부른다.
- 지역 변수와 매개변수는 아무것도 소유하지 않는다.
  Python처럼 같은 객체를 여러 이름이 가리킬 수 있다.

그래서 평소 코드는 Python과 똑같이 동작하고,
소유권은 두 지점에서만 드러난다.
프레임이 소유한 객체를 반환할 때와, 객체를 필드나 컨테이너에 저장할 때다.

| 상황                                   | 표기                       |
| -------------------------------------- | -------------------------- |
| 함수에 객체를 넘길 때                  | 그냥 `T` (빌림)            |
| 다른 곳이 소유한 객체를 반환할 때      | 그냥 `T` (참조 반환)       |
| 새로 만든 객체를 반환할 때             | `Own[T]`                   |
| 소유권을 가져가는 필드나 매개변수      | `Own[T]`                   |
| 마지막 사용인 지역 변수나 임시 값 저장 | 표기 없음 (이동)           |
| 저장 후에도 계속 쓰는 객체 저장        | `copy(...)` 또는 구조 변경 |
| 변경하지 않는 매개변수                 | `readonly[T]` (선택)       |

지역 객체를 그냥 `T`로 반환하면 컴파일 오류가 난다.
반환 후 해제될 객체를 가리키는 참조가 되기 때문이다.
컴파일러는 `Own[T]`로 바꾸라고 진단에서 알려 준다.

### 이동과 복사

저장소에 값을 넣을 때 컴파일러는 이동과 복사 중 하나를 고른다.
그 객체가 현재 프레임에서 만들어졌고 저장이 마지막 사용이면 그대로 넘긴다(이동).
저장 후에도 어떤 이름이 그 객체를 가리키면 깊은 복사를 하고 경고를 낸다.
CPython이라면 같은 객체를 공유했을 자리라는 뜻이다.
`copy()`를 써도 복사는 똑같이 일어나며, 의도를 드러내고 경고를 없앨 뿐이다.
이동될 자리에 `copy()`를 쓰면 반대로 불필요한 복사라고 경고한다.

C++이나 Rust에 빗대면 `Own[T]`는 `std::unique_ptr`를 넘기거나
Rust의 값 전달과 같은 이동이고, `readonly[T]`는 `const T&`다.
저장소는 Rust처럼 소유자가 하나지만, 빌림은 C++식 참조라서
Rust의 “별칭 또는 변경, 둘 중 하나” 규칙이 없다.
컴파일러가 검사하는 것은 참조가 소유자보다 오래 살아남는지(escape)뿐이다.
참조가 살아 있는 동안 컨테이너를 변경하면 금지하지 않고
`'append' may invalidate references` 경고만 낸다.

공유 소유권이 정말 필요할 때는 `Rc`를, 스레드 사이에서는 `Arc`를 쓴다.
`Arc`는 데이터 경쟁을 컴파일 시점에 검사하지 않으므로
`Mutex`, `RwLock`, `Atomic`으로 직접 보호해야 한다.

### Python과 다른 그 밖의 규칙

- 함수 매개변수, 반환 타입, 클래스 필드에는 어노테이션이 필수다.
  지역 변수는 추론된다.
- 어노테이션 없는 정수 리터럴은 32비트 `int32`가 된다.
  고정 폭 정수가 넘치면 조용히 감기지 않고 panic으로 프로그램이 끝나며,
  panic은 예외가 아니라서 잡을 수 없다.
  `int`는 Python처럼 임의 정밀도이고, 63비트에 들어가는 값은 힙 할당이 없다.
- 클래스에 `__dict__`가 없어서 선언하지 않은 필드는 나중에 추가할 수 없다.
- `A | B`는 힌트가 아니라 태그를 가진 실제 유니온이고,
  `match`는 태그 분기로 컴파일된다.
  반환 타입이 있는 함수에서 빠진 경우가 있으면 컴파일 오류다.
- 메서드 호출은 선언된 타입에 컴파일 시점에 묶인다.
  하위 클래스가 메서드를 재정의하면 경고가 나고,
  런타임 디스패치가 필요하면 `@dynamic` 프로토콜을 써야 한다.
- `eval`, 몽키 패칭, 런타임 `__dict__` 변경은 없다.
- CPython용 패키지는 import할 수 없다.
  numpy나 requests는 물론 순수 Python 패키지도 TurboPython으로 컴파일되지 않으면
  쓸 수 없고, 문서는 이것이 일시적인 공백이 아니라 설계라고 밝힌다.

## 시작하기

```bash
# 설치 (Python 3.12 이상)
uv tool install tpy-lang
# C++23 컴파일러가 없으면 zig를 함께 받는다
uv tool install "tpy-lang[bundled]"

# 컴파일하고 바로 실행
tpy hello.py

# 최적화된 독립 실행 바이너리
tpy -b -o build program.py
./build/release/program

# C++ 프로젝트만 내보내기 (타입·소유권 검사를 빠르게 돌릴 때도 쓴다)
tpyc -o build program.py
```

`tpy`를 인자 없이 실행하면 REPL이 열리고, `tpy -c 'print(2 + 3)'`처럼
한 줄을 평가할 수도 있다.
아직 `pyproject.toml` 통합이 없어서 설정은 모두 명령줄 플래그로 한다.

### CPython 확장 모듈

모듈 첫 줄에 `# tpy: ext_module`을 쓰고 공개할 함수에 `@export`를 붙이면
일반 CPython 확장 모듈이 나온다.

```python
# tpy: ext_module
from tpy.extern import export

@export
def triple(x: int) -> int:
    return x * 3
```

```bash
tpyc -b -o build fastmod.py
cp build/release/fastmod.so .
python3 -c "import fastmod; print(fastmod.triple(14))"
```

인자와 결과는 경계에서 Python 타입으로 변환되고,
타입이 맞지 않으면 Python 쪽에서 `TypeError`가 난다.
문서는 이것을 애플리케이션은 CPython에 두고
뜨거운 모듈만 옮기는 점진적 이전 경로로 제시한다.

### 코딩 에이전트용 문서

`tpy --install-agent-docs docs`는 에이전트가 읽을 참조 파일 네 개를 쓴다.
Python과의 차이를 요약한 `TPY_FOR_AGENTS.md`,
언어 전체 참조인 `TPY_LANGUAGE_FEATURES.md`,
표준 라이브러리 현황인 `TPY_STDLIB_ROADMAP.md`,
설치된 패키지에서 생성한 API 목록인 `TPY_API_REFERENCE.md`다.
명령이 출력하는 짧은 안내문을 `AGENTS.md`나 `CLAUDE.md`에 넣으면
에이전트가 TurboPython 코드를 쓰기 전에 이 파일들을 읽게 된다.

## 확인하기

2026년 10월 13일 macOS(Apple Silicon, Apple clang 21)에서
`uvx --from tpy-lang`으로 0.6.2를 받아 직접 실행해 보았다.
문서는 첫 실행에서 런타임을 컴파일하느라 몇 분이 걸릴 수 있다고 했지만,
이 환경에서는 26개 모듈을 2.2초에 컴파일했다.

### 소유권 경고와 정수 오버플로

```python
class Reading:
    sensor: str
    def __init__(self, sensor: str):
        self.sensor = sensor

def main():
    log: list[Reading] = []
    r = Reading("boiler-3")
    log.append(r)
    r.sensor = "renamed"
    print(log[0].sensor)
    k = 2147483647
    print(k + 1)

main()
```

```text
own.py:9: warning: copies Reading into owned storage; use copy() to make this explicit
TurboPython panic: int32 overflow in addition
boiler-3
```

같은 파일을 CPython 3.14로 실행하면 `renamed`와 `2147483648`이 나온다.
같은 소스가 두 런타임에서 두 줄 모두 다른 결과를 낸다.
복사에는 경고가 나오지만, 정수 오버플로는 컴파일 시점에 아무 말이 없다가
실행 중에 panic으로 끝난다.
panic 메시지는 표준 오류로 먼저 나오고 버퍼에 있던 `boiler-3`이 뒤에 찍혔다.

### 정적 디스패치

```python
class Animal:
    def sound(self) -> str:
        return "..."

class Dog(Animal):
    def sound(self) -> str:
        return "woof"

def speak(a: Animal) -> str:
    return a.sound()

def main():
    print(speak(Dog()))

main()
```

TurboPython은 `...`를 출력하고 CPython은 `woof`를 출력한다.
컴파일러는 `Dog.sound`가 `Animal.sound`를 가린다는 경고와 함께
`@dynamic` 프로토콜을 쓰라는 해결책을 알려 준다.
경고가 있으니 조용한 차이는 아니지만,
객체 지향 Python 코드를 옮기면 이 경고가 클래스 계층마다 쏟아질 것이다.

### 성능

300만 미만에서 Collatz 수열이 가장 긴 수를 찾는 프로그램으로 비교했다.
TurboPython 버전은 `from tpy import int64`로 변수를 `int64`로 선언했고,
CPython 버전은 그 줄만 `int64 = int`로 바꿨다.
세 결과 모두 `2298025 559`로 같았다.

| 실행                             | user 시간 | CPython 대비 |
| -------------------------------- | --------- | ------------ |
| CPython 3.14                     | 16.30초   | 1배          |
| TurboPython, `int` (임의 정밀도) | 4.53초    | 약 3.6배     |
| TurboPython, `int64`             | 0.74초    | 약 22배      |

빌드된 바이너리는 229KB였고 `libc++`와 `libSystem`만 링크했다.
성능의 대부분은 컴파일 자체가 아니라 고정 폭 정수에서 나온다.
타입을 `int`로 그대로 두면 컴파일해도 CPython보다 3.6배 빠를 뿐이다.

## 트레이드오프

### 생태계를 통째로 포기한다

TurboPython의 가장 큰 비용은 문법이 아니라 PyPI다.
import하는 모든 모듈을 함께 컴파일하는 구조라서
CPython용 패키지는 순수 Python이든 C 확장이든 쓸 수 없고,
문서는 이것이 설계라고 분명히 밝혔다.
표준 라이브러리도 일부만 있다.
`pathlib`, `subprocess`, `logging`, `unittest`, `decimal`, `statistics`가
아직 없고,
`collections`에는 `Counter`만 있어 `deque`와 `defaultdict`가 없다.
`itertools`에서는 `chain`, `product`, `groupby`가 빠졌다.

그래서 TurboPython이 “Python 코드를 빠르게 만든다”는 말은
“Python 문법으로 새 코드를 쓸 수 있다”에 가깝다.
기존 애플리케이션을 옮기려면 의존성부터 다시 써야 한다.
CPython 확장 모듈로 뜨거운 함수만 옮기는 경로가 현실적인 진입점인 이유다.

### 소유권은 Rust보다 느슨하고 Python보다 엄격하다

Rust는 별칭과 변경을 동시에 허용하지 않아서 반복자 무효화 같은 버그를
컴파일 시점에 막지만, 그 대가로 빌림 검사기와 싸워야 한다.
TurboPython은 별칭을 자유롭게 허용하고 탈출만 검사하므로
평범한 Python 코드가 거의 그대로 컴파일된다.
그 대가로 컨테이너를 변경하면서 그 안의 참조를 쓰는 코드는
경고만 받고 컴파일된다.
홈페이지가 말하는 “컴파일 시점 메모리 안전성”은
해제 후 사용과 일부 별칭 버그까지이고, Rust 수준의 보장은 아니다.

반대쪽에서 보면 Python 개발자에게는 새 규칙이 생긴다.
리스트에 넣은 객체를 이후에 바꾸면 리스트 안의 값은 바뀌지 않는다.
경고가 나오기는 하지만, 그 경고를 이해하려면 소유권 모델을 배워야 한다.

### 고정 폭 정수의 속도와 위험

위 실험에서 보듯 속도의 대부분은 `int32`와 `int64`에서 나온다.
그러나 어노테이션 없는 리터럴이 `int32`가 되는 기본값은
Python 개발자의 직관과 정반대다.
Python에서는 결코 넘치지 않던 계산이 TurboPython에서는 panic으로 끝나고,
panic은 `try`로 잡을 수 없다.
`int`로 어노테이션하면 안전하지만 속도 이점이 크게 줄어든다.
어떤 변수를 고정 폭으로 둘지는 값의 범위를 아는 사람이 정해야 한다.

### 정적 디스패치는 성능과 Python다움을 맞바꾼다

메서드 호출을 컴파일 시점에 묶으면 가상 호출 비용이 없지만,
상속과 재정의에 기대는 Python 코드는 결과가 달라진다.
컴파일러가 모든 재정의에 경고를 내고 `@dynamic`을 권하므로
조용히 틀리지는 않는다.
하지만 `list[SomeProtocol]`이 아직 거부되어서
서로 다른 타입을 한 리스트에 담는 고전적인 다형성 패턴은 지금 쓸 수 없다.

## 함정

- 홈페이지 스스로 알려진 버그가 조용히 틀린 결과를 낼 수 있다고 경고한다.
  문서는 진단이 없는 차이를 따로 “Silent difference from CPython”으로 표시하므로,
  옮기기 전에 이 표시를 찾아 읽어야 한다.
- 사용자 정의 예외 클래스를 `print(e)`하면 메시지가 아니라 객체가 출력되고,
  진단도 나오지 않는다.
- `raise X from e`는 컴파일되지만 원인(cause)을 버린다.
- `tplib.requests`의 예외를 `except requests.ConnectionError`처럼
  모듈 이름을 붙여 잡으면 컴파일은 되지만 실제로 잡히지 않는다.
  `from tplib.requests import ConnectionError`로 가져와야 한다.
- `crc32`와 `adler32`는 `uint32`를 반환하므로,
  그 결과로 32비트를 넘는 계산을 하면 커지지 않고 panic이 난다.
- 사용자 정의 데코레이터와 `yield from`은 아직 컴파일되지 않는다.
- `@noalloc` 데코레이터는 파싱만 되고 할당 금지 검사는 구현되지 않았다.
  붙여 두었다고 보장받는 것이 아니다.
- 멀티스레드 코드에서 `Arc`는 데이터 경쟁을 검사하지 않는다.
  GIL이 없으니 CPython에서 우연히 안전하던 코드가 그대로 경쟁 상태가 된다.

## 비평

### 소스가 “유효한 Python”이라는 말은 절반만 맞다

시작 안내는 TurboPython 소스가 유효한 Python이라 코딩 에이전트가
플러그인 없이 동작한다고 말한다.
문법만 보면 맞다.
그러나 위 실험의 두 프로그램은 CPython에서 전혀 다른 결과를 냈다.
같은 텍스트가 두 런타임에서 다른 의미를 갖는다면,
“Python으로 읽힌다”는 장점은 오히려 함정이 된다.
코드를 읽는 사람과 에이전트가 Python의 의미로 해석하기 때문이다.
프로젝트가 `--install-agent-docs`를 따로 만든 것 자체가
문법의 유사성만으로는 부족하다는 사실을 인정한 셈이다.

저자는 HN에서 이 유사성을 테스트 방법으로 쓴다고 설명했다.[^turbopython-tests]
테스트 케이스의 약 90%를 TurboPython과 CPython 양쪽으로 실행해
출력이 바이트 단위로 같아야 통과하고,
CPython에서 실행할 때는
`tpy` 패키지가 TurboPython 핵심 타입의 스텁 구현을 제공한다.
이 방식은 두 런타임이 같게 동작하는 영역을 넓히는 데는 강력하다.
그러나 저자도 인정하듯 방향은 한쪽뿐이다.
TurboPython을 통과한 프로그램은 CPython에서도 돌지만,
대부분의 Python 프로그램은 더 엄격한 규칙에 맞게 고쳐야 TurboPython을 통과한다.
테스트가 확인하는 것은 TurboPython으로 쓴 코드의 의미이지,
기존 Python 코드를 옮겼을 때의 의미가 아니다.

### 경고에 의존하는 안전성은 규모가 커지면 무뎌진다

TurboPython은 CPython과 다르게 동작하는 대부분의 지점에서
오류 대신 경고를 낸다.
암묵적 복사, 재정의된 메서드, None 가능 값 접근,
참조 무효화가 모두 경고다.
작은 예제에서는 친절하지만, 수천 줄을 옮기면 경고가 수백 개 쌓이고
사람은 경고를 무시하는 법부터 배운다.
`@nocopy`처럼 경고를 오류로 바꾸는 장치가 일부 있지만,
프로젝트 단위로 경고를 오류로 다루는 설정은
문서와 `tpy --help`에서 찾지 못했다.
`pyproject.toml` 통합도 아직 계획 단계다.

저자는 HN에서 경고를 고른 이유를 밝혔다.[^turbopython-recursion]
지금의 빌림 분석은 AST 수준이라 원하는 만큼 정밀하지 않아서 경고로 두고,
제어 흐름 그래프(CFG) 기반 중간 표현(MIR)으로 옮긴 뒤
엄격 모드에서 오류로 바꿀 계획이라고 했다.
반환값이 어느 인자에서 빌려 온 것인지도 별도 표기 없이 함수 본문에서 추론한다.
인자가 여럿이면 그 합집합으로 보고, 빌림이 살아 있는 동안 인자를 바꾸면
호출자에게 경고한다.[^turbopython-borrow]
재귀 함수는 같은 인자로 자기를 부르는 흔한 경우만 처리한다.
결국 지금의 경고는 설계 철학이라기보다 분석기가 덜 익었다는 신호다.
그렇다면 엄격 모드가 나오기 전까지 이 언어의 메모리 안전성 주장은
홈페이지 문구보다 한 단계 낮춰 읽어야 한다.

### 한 사람 프로젝트의 지속 가능성이 가장 큰 미지수다

커밋 2,583개가 모두 한 계정에서 나왔고, 저장소는 만들어진 지 7개월이다.
그 기간에 컴파일러, 소유권 분석, C++ 런타임,
TLS·HTTP·asyncio를 포함한 표준 라이브러리 일부를 만든 속도는 인상적이다.
하지만 생태계를 포기하는 언어는 표준 라이브러리와 `tplib`를
프로젝트가 직접 채워야 하고, 그 양은 한 사람이 감당할 수 있는 범위를 넘는다.
홈페이지와 문서는 누가 만드는지, 어떤 조직이 지원하는지,
로드맵과 1.0 계획이 무엇인지 밝히지 않는다.
도입을 검토한다면 기술보다 이 질문에 먼저 답해야 한다.

### 비교 대상을 말하지 않는다

시작 안내는 예제 저장소의 대형 예제를 “다른 Python-to-C++ 컴파일러”의
예제에서 옮겨 왔다고 적고, 실행 예시 경로는 `tpy-examples/shedskin/voronoi`다.
Shed Skin, Cython, Codon, mypyc, Mojo처럼
Python 문법이나 Python 생태계로 네이티브 성능을 노린 시도는 이미 많다.
홈페이지는 이들과 무엇이 다른지 설명하지 않는다.
HN 토론의 첫 질문도 Cython으로 할 수 없는 무엇을 주느냐였다.[^fps-hero]
fps-hero는 CPython 코드와 100% 호환되지 않으면
Python 생태계의 라이브러리를 쓸 수 없어 아무도 관심을 두지 않는다고 했다.
fulafel은 Cython이 Python 모듈을 쓰기 위한 Python 호환 확장인 반면,
TurboPython은 Python과 닮았을 뿐
독립적으로 쓰는 별개 언어라고 정리했고,[^fulafel]
저자도 이 구분이 맞다고 답했다.[^turbopython-tests]
Mojo를 쓰면 되지 않느냐는 질문에는
Mojo는 Python 호환을 목표로 한 적이 없다는 반론이 붙었다.[^skavi][^az09mugen]
PyPy가 C 확장과의 통합 문제로 겪은 일을 떠올린 댓글도 있었다.[^aaronsung]

비교가 필요한 쪽은 Python 컴파일러만이 아니다.
Ohentis는 홈페이지가 Python과의 차이만 길게 말하고,
실제로 더 닮은 Rust와의 차이는 말하지 않는다고 지적했다.[^Ohentis]
문서 안에 C++/Rust 대응표 페이지가 있다는 답이 달렸지만,[^irq-1]
그 페이지는 개념 대응표이지 Rust 대신 이 언어를 고를 이유를 말하지는 않는다.
차별점은 소유권 모델로 보이지만,
그것이 사용자가 기꺼이 지불할 학습 비용인지는 홈페이지만으로 판단할 수 없다.
Mojo와의 비교는 [Mojo](../programming-languages/mojo.md) 문서를 참고할 만하다.

## 기억할 원칙

### 속도는 언어가 아니라 타입에서 나온다

같은 컴파일러로 만든 바이너리가 `int`로는 CPython의 3.6배,
`int64`로는 22배 빨랐다.
Python을 컴파일하는 도구를 평가할 때는 “컴파일했더니 몇 배”라는 숫자보다
그 숫자를 얻으려고 어떤 타입 결정을 해야 했는지를 봐야 한다.
그 결정은 값의 범위를 아는 사람이 내려야 하고,
틀리면 실행 중에 프로그램이 멈춘다.

### 문법이 같고 의미가 다르면 차이를 소리 내어 알려야 한다

TurboPython은 CPython과 다른 지점을 경고로 알리는 데 공을 들였다.
Python과 비슷한 문법을 쓰는 언어를 만들거나 고를 때 핵심 질문은
얼마나 비슷한가가 아니라 다른 곳에서 얼마나 크게 알려 주는가다.
조용히 달라지는 지점이 하나라도 있으면,
익숙한 문법은 오히려 그 지점을 가린다.

---

[^turbopython-tests]: <https://news.ycombinator.com/item?id=49970207>

[^turbopython-recursion]: <https://news.ycombinator.com/item?id=49975454>

[^turbopython-borrow]: <https://news.ycombinator.com/item?id=49969862>

[^fps-hero]: <https://news.ycombinator.com/item?id=49960411>

[^fulafel]: <https://news.ycombinator.com/item?id=49961133>

[^skavi]: <https://news.ycombinator.com/item?id=49960639>

[^az09mugen]: <https://news.ycombinator.com/item?id=49965343>

[^aaronsung]: <https://news.ycombinator.com/item?id=49960824>

[^Ohentis]: <https://news.ycombinator.com/item?id=49957408>

[^irq-1]: <https://news.ycombinator.com/item?id=49958245>
