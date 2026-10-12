# Python 3.15: 지연 임포트와 UTF-8 기본값, 올릴 때 무엇이 달라지나

원문: [Python Release Python 3.15.0 | Python.org](https://www.python.org/downloads/release/python-3150/)

HN 토론: <https://news.ycombinator.com/item?id=50021127> (294점, 100개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/rpiwtb/python_3_15_0> (42점, 4개 댓글)

GN 토론: <https://news.hada.io/topic?id=35085>

## 소개

Python 3.15.0은 2026년 10월 9일에 나온 안정판이다.
릴리스 페이지는 3.14 이후 1,012명이 커밋 5,643개를 보탰다고 적는다.
릴리스 매니저는 3.14에 이어 Hugo van Kemenade가 맡았고,
Sovereign Tech Agency가 Sovereign Tech Fellowship으로 그 일을 지원했다.

릴리스 페이지 자체는 짧은 목록이다.
실제 내용은 What's New in Python 3.15 문서와 각 PEP에 있다.
목록을 묶으면 다음과 같다.

| 분류            | 항목                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------ |
| 인터프리터      | PEP 810 지연 임포트, PEP 686 UTF-8 기본 인코딩, PEP 814 `frozendict`                                   |
| 인터프리터      | PEP 661 `sentinel`, PEP 798 컴프리헨션 언패킹, PEP 829 `.start` 파일                                   |
| 인터프리터      | 실험적 JIT 개선, 오류 메시지 개선                                                                      |
| 표준 라이브러리 | PEP 799 `profiling` 패키지와 샘플링 프로파일러 Tachyon, 색상 출력 확대                                 |
| 타입            | PEP 728 `TypedDict` 추가 항목, PEP 747 `TypeForm`, PEP 800 disjoint base                               |
| C API           | PEP 782 `PyBytesWriter`, PEP 788 종료 보호, PEP 803·820·793 `abi3t`                                    |
| 빌드            | PEP 831 프레임 포인터 기본 활성화                                                                      |
| 배포            | Windows 64비트 공식 바이너리의 tail-calling 인터프리터, macOS 공식 바이너리의 free-threading 기본 설치 |

릴리스 페이지에는 기능 목록 말고도 경고가 하나 있다.
macOS 27.0에서 IDLE이나 `tkinter` 앱이 대화상자를 여는 메뉴 명령을 실행하면
멈출 수 있다.
원인은 macOS 27.0의 운영체제 동작 변경이며,
현재 모든 Tk 버전과 그에 따라 현행 모든 Python 버전이 영향을 받는 것으로 본다.
Tk 기반 앱에 기대고 있다면 macOS 27.0 설치를 미루거나
작업 흐름이 영향을 받는지 먼저 시험하라고 권하고,
진행 상황은 이슈 #158053에서 추적한다.

마지막에는 Barry Warsaw가 만든 `whatsnewt`가 소개된다.
3.15의 새 기능을 실제로 써서 풀어야 하는 퍼즐 18개로 된 TUI 텍스트 어드벤처다.
타입 검사기가 필요한 퍼즐은 pyrefly로 답을 검증한다.

JIT 컴파일러의 개발 경과는 `python/cpython-jit-3-15.md`에,
JIT가 쓰는 인터프리터 트레이싱 기법은
`python/cpython-ultra-low-overhead-profiling.md`에 따로 정리되어 있다.

## 기본값이 바뀌는 곳: UTF-8 인코딩

### 무엇이 바뀌나

3.15부터 Python은 시스템 환경과 무관하게 UTF-8을 기본 인코딩으로 쓴다.
`encoding` 인자 없이 `open('flying-circus.txt')`처럼 연 파일은
UTF-8로 읽고 쓴다.
PEP 686은 이것을 UTF-8 모드를 기본으로 켜는 일로 정의하며,
파일뿐 아니라 표준 입출력과 파이프에도 같은 기본값이 적용된다.
인코딩을 명시한 호출은 그대로이고, `encoding='locale'`은 3.10부터 있던
대로 현재 로캘 인코딩을 쓴다.

이전 동작으로 돌리려면 `PYTHONUTF8=0` 환경 변수나 `-X utf8=0` 옵션을 준다.
PEP 686은 대부분의 Unix 시스템이 이미 UTF-8 로캘을 쓰고,
로캘이 `C`나 `POSIX`일 때는 UTF-8 모드가 켜져 왔기 때문에
이 변화가 주로 Windows 사용자에게 영향을 준다고 적는다.
해석을 덧붙이면, 한국어 Windows처럼 기본 로캘 인코딩이 UTF-8이 아닌
환경에서 `encoding` 없이 텍스트 파일을 읽던 코드가 가장 먼저 영향을 받는다.

HN에서는 UTF-8이 이미 기본값인 줄 알았다는 반응이 나왔다.[^hleszek]
zahlman은 3.0부터 UTF-8이 기본이었던 것은 소스 파일을 읽을 때뿐이었고
내장 기능과 표준 라이브러리의 기본값은 아니었다고 정리했다.[^zahlman-utf8]
masklinn은 Linux에서도 로캘 인코딩을 따랐고 POSIX 로캘만 예외로
UTF-8 모드가 켜졌다고 덧붙였다.[^masklinn-utf8]
PaulHoule은 출처가 제각각인 Python 이미지로 Docker 이미지를 만든 탓에
예상하지 못한 문자 집합이 들어오고,
서드파티 라이브러리가 `print()`한 문자 때문에
프로그램이 죽던 경험을 적었다.[^PaulHoule]

### 영향받는 코드를 찾는 방법

PEP 686이 제시하는 순서는 이렇다.
먼저 `EncodingWarning`(PEP 597)으로 기본 인코딩에 기대는 곳을 모두 찾는다.
`encoding`을 생략한 곳에는
`encoding="utf-8"`이나 `encoding="locale"`을 명시한다.
`locale.getpreferredencoding()`을 쓰는 곳은 `"utf-8"`이나
`locale.getencoding()`으로 바꾼다.
그리고 UTF-8 모드에서 애플리케이션을 시험한다.

`EncodingWarning`은 `-X warn_default_encoding` 옵션으로 켠다.
이 옵션은 3.10부터 있었으므로
3.15로 올리기 전에 현재 버전에서 미리 돌릴 수 있다.

```bash
# 3.10 이상 어느 버전에서든 기본 인코딩에 기대는 호출을 경고로 드러낸다
python -X warn_default_encoding -W error::EncodingWarning -m pytest
```

## 지연 임포트의 동작 방식

### 문법과 프록시

`lazy` 소프트 키워드를 `import`나 `from ... import` 앞에 붙이면
모듈 로딩이 그 이름을 처음 쓰는 순간까지 미뤄진다.
그 전까지 이름에는 가벼운 프록시 객체(`types.LazyImportType`)가 묶여 있다.

```python
import sys

lazy import json
lazy from pathlib import Path

print("json" in sys.modules)  # False: 아직 로딩하지 않았다
data = json.loads('{"key": "value"}')  # 여기서 json을 실제로 임포트한다
print("json" in sys.modules)  # True
p = Path(".")  # pathlib은 여기서 임포트된다
```

PEP 810은 프록시를 실제 객체로 바꾸는 과정을 reification이라 부른다.
전역 변수나 모듈 속성으로 이름에 접근하면 reification이 일어나고,
모듈이 임포트되면서 프록시가 실제 객체로 교체된다.
교체 뒤에는 적응형 인터프리터가 보통 2~3번 접근 안에 바이트코드를 특수화해
검사 비용이 사라진다고 PEP는 설명한다.

`lazy from json import dumps, loads`처럼 여러 이름을 가져오면
`dumps`를 처음 쓸 때 `json` 모듈 전체가 로딩되지만 실제 객체로 바뀌는 것은
`dumps`뿐이다.
`loads`는 접근할 때 바뀐다.
지연 임포트는 언제 로딩하느냐를 바꿀 뿐 무엇을 로딩하느냐는 바꾸지 않는다.
`lazy from heavy import MyClass`도 첫 사용 시 `heavy` 모듈 파일 전체를 실행한다.

### 쓸 수 있는 곳과 없는 곳

`lazy`는 모듈 최상위에서만 쓸 수 있다.
함수, 클래스 본문, `try`/`except`/`finally` 블록 안에서 쓰면 `SyntaxError`다.
`lazy from module import *`와 `lazy from __future__ import ...`도
`SyntaxError`다.
`.pth` 파일의 `import` 줄은 지연 임포트 대상이 아니다.

3.15 이전 버전도 지원해야 하는 코드는 `lazy` 키워드 대신 모듈 전역에
`__lazy_modules__`를 정의한다.
여기 이름이 있는 모듈의 일반 `import` 문은 `lazy`가 붙은 것처럼 동작하고,
이전 버전은 이 변수를 무시하므로 평소처럼 즉시 임포트한다.

```python
__lazy_modules__ = ["json", "pathlib"]  # 모든 import보다 먼저 정의한다

import json     # 3.15 이상에서는 지연, 이전 버전에서는 즉시 임포트
import os       # 목록에 없으므로 즉시 임포트
```

### 전역 모드와 필터

소스를 고치지 않고 전체를 지연시키려면 `-X lazy_imports=all`이나
`PYTHON_LAZY_IMPORTS=all`을 쓴다.
기본값 `normal`은 소스의 `lazy` 키워드만 존중한다.
런타임에는 `sys.set_lazy_imports()`와 `sys.get_lazy_imports()`로
모드를 바꾸고 조회한다.

`sys.set_lazy_imports_filter()`에는 모듈마다 지연 여부를 정하는 함수를 넘긴다.
함수는 임포트하는 모듈 이름, 임포트되는 모듈 이름, `fromlist`를 받고
`True`면 지연, `False`면 즉시 임포트한다.
What's New는 자기 애플리케이션 모듈만 지연시키고 서드파티는 즉시 임포트하는
패턴을 예로 든다.

```python
import sys

def myapp_filter(importing, imported, fromlist):
    # 자기 패키지만 지연시키고 서드파티 의존성은 즉시 임포트한다
    return imported.startswith("myapp.")

sys.set_lazy_imports_filter(myapp_filter)
sys.set_lazy_imports("all")
```

출시된 문서와 PEP 사이에는 차이가 하나 있다.
PEP 810은 모드 값으로 `normal`, `all`, `none` 세 가지를 정의하고,
`none`을 모든 지연 임포트를 끄는 디버깅 수단이자 패키지 설치 도구가
즉시 임포트를 강제하는 방법으로 권한다.
그러나 3.15 문서의 `-X lazy_imports`, `PYTHON_LAZY_IMPORTS`,
`sys.set_lazy_imports()` 설명은 `all`과 `normal` 두 값만 적는다.
`none`이 실제로 받아들여지는지는 3.15 인터프리터에서 확인하지 않았다.

### 오류가 나는 시점

지연 임포트한 모듈 로딩이 실패하면
예외는 `import` 문이 아니라 첫 사용 지점에서 난다.
traceback에는 `lazy import`를 선언한 위치와 실제로 접근한 위치가 예외 연쇄로
함께 표시된다.
reification이 실패하면 프록시는 그대로 남고, 다음 접근에서 다시 시도한다.

HN에서 frodowtf2가 전역으로 켜지 않을 이유가 있느냐고 묻자,
zem은 레지스트리 패턴처럼 의도된 임포트 부작용이 주된 이유라고 답했다.[^zem]
zem은 코드를 분석해 지연 임포트를 안전하게 켤 수 있는 곳을 찾는
Facebook의 lifeguard도 소개했는데, 알파 단계라고 밝혔다.
ris는 실행 경로에 따라 임포트 순서가 비결정적으로 바뀌는 문제를
짧게 지적했다.[^ris]

## 새 내장 타입과 문법

### `frozendict`

`frozendict`는 `builtins`에 들어온 불변 매핑이다.
`dict`의 하위 클래스가 아니라 `object`를 직접 상속한다.
PEP 814는 `dict`를 상속하면
`dict.__setitem__(fd, key, value)`처럼 `dict` 메서드로 값을 바꿀 길이 생기기
때문에 상속하지 않았다고 설명한다.
모든 키와 값이 해시 가능하면 `frozendict`도 해시 가능해서
딕셔너리 키, 집합 원소, `functools.lru_cache` 인자로 쓸 수 있다.

삽입 순서는 유지하지만 동등성 비교와 해시는 순서를 보지 않는다.
`frozendict(x=1, y=2) == dict(x=1, y=2)`도 `True`다.
`|`로 병합할 수 있고, `|=`는 제자리에서 바꾸지 않고 새 객체를 만든다.
`copy()`는 얕은 복사라서 안에 든 리스트 같은 가변 값은 그대로 공유된다.

`copy`, `decimal`, `json`, `marshal`, `pickle`, `pprint`,
`xml.etree.ElementTree`가 `frozendict`를 받도록 바뀌었고
`plistlib`은 직렬화에서만 받는다.
`isinstance(arg, dict)`로 검사하던 코드는 `frozendict`를 거부하게 되므로,
What's New는 `isinstance(arg, (dict, frozendict))`나
`isinstance(arg, collections.abc.Mapping)`으로 바꾸라고 권한다.

### `sentinel`

`sentinel('MISSING')`은 고유한 표식 값을 만든다.
repr이 이름 그대로 `MISSING`으로 나오고, 복사해도 같은 객체이며,
모듈과 이름으로 임포트할 수 있으면 pickle 왕복 뒤에도 동일성이 유지된다.
타입 표현식에서 `int | MISSING`처럼 쓸 수 있고,
타입 검사기는 `is`와 `is not`으로 타입을 좁힌다.
PEP 661에 따르면 `None`과 달리 참으로 평가되므로,
`if value:` 대신 `if value is MISSING:`으로 검사해야 한다.

### 컴프리헨션 언패킹

리스트, 집합, 딕셔너리 컴프리헨션과 제너레이터 표현식에서
`*`와 `**`를 쓸 수 있다.
`[*L for L in lists]`는 `[x for L in lists for x in L]`과 같고,
`{**d for d in dicts}`는 딕셔너리들을 하나로 합치며,
겹치는 키는 뒤의 값이 이긴다.
중첩 컴프리헨션이나 `itertools.chain.from_iterable()`을 대신하는 문법이다.
비동기 제너레이터 표현식에도 적용된다.

### 그 밖에 손에 닿는 변화

`AttributeError` 메시지가 더 친절해졌다.
`container.area`처럼 내부 속성을 거쳐야 하는 경우 `'.inner.area'`를 제안하고,
`[1, 2, 3].push(4)`에는 `.append`, `'hello'.toUpperCase()`에는 `.upper`를,
`{}.put("a", 1)`에는 `d[k] = v`를 제안한다.
다른 언어의 메서드 이름을 정적 표로 가지고 있다가 비슷한 이름이 없을 때
대응하는 Python 표현을 알려 주는 방식이다.

`re.match()`는 soft deprecated가 되고 `re.prefixmatch()`가 추가됐다.
다른 언어 정규식 라이브러리 대부분이 `match`라는 이름을 Python의 `search` 뜻으로
쓰기 때문에 생기는 혼동을 줄이려는 것이고,
30년 넘게 쓰인 이름이라 `match()`를 제거할 계획은 없다.
`bytearray.take_bytes()`는 복사 없이 버퍼에서 `bytes`를 꺼낸다.
`math.integer` 모듈이 새로 생겼고, 유니코드 데이터베이스는 17.0.0으로 올랐다.
Lobste.rs에서 hawski는 `logging.basicConfig()`가 3.15부터 `formatter`
인자를 받게 되어 직접 만든 Formatter를 쓰는 상용구가 줄었다고 반겼다.[^hawski]

## 시작 시점에 실행되는 코드: `.pth`에서 `.start`로

`site` 모듈이 읽는 `.pth` 파일은 `sys.path`를 넓히는 일과
`import`로 시작하는 줄을 `exec()`로 실행하는 일을 함께 해 왔다.
PEP 829는 뒤쪽 기능이 인터프리터 시작 때 무엇이 실행되는지 알기 어렵게 만들고
공격 표면을 넓힌다고 본다.
3.15는 `pkg.mod:callable` 형식의 진입점을 적는 `.start` 파일을 도입한다.
시작할 때 그 callable을 찾아 인자 없이 호출한다.

같은 이름의 `.start` 파일이 있으면
짝이 되는 `.pth` 파일의 `import` 줄은 무시된다.
`.pth`의 `sys.path` 확장 줄은 바뀌지 않는다.
PEP 829가 예상하는 일정은 이렇다.
3.15에서 3.17까지는 `.start` 짝이 없는 `.pth`의 `import` 줄이 그대로 실행되고,
3.18과 3.19에서는 조용히 무시되며, 3.20부터는 경고가 난다.
PEP는 악성 패키지도 진입점으로 코드를 실행할 수 있으므로
공격 표면 자체가 사라지지는 않는다고 스스로 밝힌다.
얻는 것은 실행 지점이 파일 목록으로 드러나고
감사 훅으로 감시할 수 있다는 점이다.

HN에서 rirze는 `.pth` `import`로 코덱을 설치해 매크로를 돌리던
작업이 있었다고 아쉬워했다.[^rirze]
alextremblay는 요즘 매크로 시스템은 `.pth`에서 코드를 실행하지 않고
임포트 기구에 훅을 건다며 mcpyrate를 예로 들었다.[^alextremblay]

## 관측성과 성능

### `profiling` 패키지와 Tachyon

PEP 799는 프로파일링 도구를 `profiling` 아래로 모은다.
결정적 추적 프로파일러는 `profiling.tracing`으로 옮겨지고 `cProfile`은 호환용
별칭으로 남는다.
`profile` 모듈은 deprecated가 되었고 3.17에 제거된다.

새 샘플링 프로파일러 Tachyon은 `profiling.sampling`이다.
실행 중인 프로세스의 스택을 주기적으로 읽기 때문에 코드를 고치거나 재시작할
필요가 없다.
What's New는 최대 1,000,000 Hz의 샘플링 속도와
사실상 0에 가까운 오버헤드를 내세운다.
측정 모드는 실제 경과 시간(`wall`, 기본값), CPU 시간(`cpu`), GIL 보유
시간(`gil`), 예외 처리 중인 스레드(`exception`) 네 가지다.
출력은 `pstats`, 접힌 스택, 플레임 그래프 HTML, Firefox Profiler용 Gecko 형식,
줄 단위 히트맵, `top` 같은 실시간 TUI를 지원한다.
`--async-aware`로 asyncio 태스크 단위로 스택을 재구성할 수도 있다.

```bash
# 스크립트를 처음부터 프로파일링해 플레임 그래프로 저장한다
python -m profiling.sampling run --flamegraph -o profile.html script.py

# 이미 실행 중인 프로세스에 붙어 30초 동안 수집한다
python -m profiling.sampling attach --flamegraph -d 30 -o profile.html 12345

# 멈춘 프로세스의 모든 스레드 스택을 한 번 찍는다
python -m profiling.sampling dump 12345
```

다만 다른 프로세스의 메모리를 읽으려면 권한이 필요하다.
Linux에서는 root, `CAP_SYS_PTRACE`, 또는 Yama `ptrace_scope` 조정이,
macOS에서는 root나 디버거 entitlement가,
Windows에서는 관리자 권한이나 `SeDebugPrivilege`가 필요하다.
프로파일러와 대상 프로세스는 같은 마이너 버전이어야 하고,
free-threaded 빌드와 일반 빌드 사이에는 붙을 수 없다.

HN에서 febed는 실행 중인 프로세스를 프로파일링할 수 있어
프로덕션에서 유용하겠다고 평했다.[^febed]
zahlman은 XZ 소스 타르볼이 3.14보다 절반쯤 커진 이유를 찾다가,
Tachyon을 시연하는 애니메이션 GIF 두 개가 문서 폴더에 10MB 넘게
들어간 것을 발견했다.[^zahlman-gif]
TUI 모양은 보여 주지만 사용법을 배우는 데는 별 도움이 안 된다며
정적 화면에 기반한 SVG 도해가 나았겠다고 덧붙였다.

### 프레임 포인터

PEP 831에 따라 CPython은 지원 플랫폼에서 `-fno-omit-frame-pointer`와
`-mno-omit-leaf-frame-pointer`로 빌드된다.
시스템 프로파일러, 디버거, 크래시 분석 도구, eBPF 도구가 네이티브 스택을
더 빠르고 정확하게 풀 수 있게 하려는 것이다.
이 플래그는 `sysconfig`로 노출되어
Python 빌드 설정을 따르는 확장 모듈에도 전파된다.
What's New는 프레임 포인터 없이 빌드된 네이티브 구성 요소 하나가
프로세스 전체의 스택 풀기를 망가뜨릴 수 있으므로,
Python 설정을 물려받지 않는 C, C++, Rust 빌드 시스템은 같은 플래그를 직접
켜라고 경고한다.
끄려면 `--without-frame-pointers`로 빌드한다.

### 숫자로 본 성능 변화

실험적 JIT는 pyperformance 기하평균으로 x86-64 Linux에서 표준 인터프리터보다
7~8%, AArch64 macOS에서 tail-calling 인터프리터보다 11~12% 빠르다.
같은 문서는 JIT 빌드와 비JIT 빌드의 차이가 벤치마크별로 약 15% 느려지는 것부터
100% 넘게 빨라지는 것까지 걸쳐 있다고 적는다.
평균이 올랐다고 모든 워크로드가 빨라지지는 않는다는 뜻이다.

Windows 64비트 공식 바이너리는 MSVC 18의 새 기능 덕분에 tail-calling
인터프리터를 쓴다.
AMD Ryzen 7 5800X에서 switch-case 인터프리터 대비 pyperformance
기하평균 15~20% 향상이 측정됐고,
큰 순수 Python 라이브러리에서 14%, 오래 도는 작은 스크립트에서 40%까지 관찰됐다.
이 밖에 free-threaded 빌드의 원시 메모리 할당에 mimalloc이 기본으로 쓰이고,
`base64` 인코딩은 2배, 디코딩은 3배 빨라졌으며,
Base32와 Ascii85, Base85, Z85 구현은 C로 다시 작성됐다.

## C 확장과 `abi3t`

### free-threaded 빌드용 안정 ABI

Stable ABI를 쓰는 C 확장은 이제 `abi3t`로 컴파일해 free-threaded 빌드와
호환되게 만들 수 있다.
대개 소스 수정이 필요하다.
`PyObject`를 인스턴스 구조체에 넣는 대신 PEP 697의 음수 `basicsize`와
`PyObject_GetTypeData()`를 써야 하고,
`PyInit_` 함수 대신 PEP 793의 `PyModExport_*` 내보내기 훅과
PEP 820의 `PySlot` 구조체로 옮겨야 한다.
옮길 수 없는 확장은 기존 `abi3`와 버전별 free-threading ABI인 `cp315t`를
따로 빌드한다.
meson-python, scikit-build-core, Maturin이 `abi3t`를 지원한다.

HN 스레드를 올린 ngoldbaum은 이 기능의 생태계 지원을 맡아 온 사람이다.
CPython 구현은 대부분 Petr Viktorin이 했고, 자신은 beta1 직전 Windows 전용
문제를 고치느라 밤을 새웠다고 적었다.[^ngoldbaum]
cryptography 프로젝트가 3.15 이상용으로 플랫폼마다 `abi3.abi3t` 휠
하나만 배포하고 있으며,
`PyObject`가 불투명 타입이라
GIL 빌드와 free-threaded 빌드가 같은 휠을 쓴다고 설명했다.
pyo3의 `abi3t` 지원을 그대로 써도 되느냐는 masklinn의 질문에는
써도 되지만 3.15와 3.15t 양쪽에서 시험해 보라고 답했다.[^ngoldbaum-pyo3]

haberman은 protobuf의 약한 참조 값 캐시를 구현하려면
`PyUnstable_TryIncRef()` 같은 API가 필요하다며
limited API 편입 계획을 물었다.[^haberman]
ngoldbaum은 `PyUnstable` API가 일반 버전별 API를 한두 릴리스 거치지 않고
곧바로 limited API로 올라가지는 않을 것이라며,
discourse 스레드를 먼저 열라고 권했다.[^ngoldbaum-protobuf]
abi3 휠 하나로 CI 매트릭스가 20개쯤에서 4개로 줄었다는 댓글에는,[^hncbw02z5a]
masklinn이 지금 `abi3t`는 3.15에만 해당하고
가치는 3.16 이후를 대비하는 데 있으며,
free-threaded 휠은 3.14t와 `abi3t`로 최소 두 개가 필요하다고 바로잡았다.[^masklinn-abi3t]

### 인터프리터 종료 보호

PEP 788은 인터프리터 종료 중 스레드 상태를 붙이면 스레드가 영영 멈추거나,
다른 스레드가 지운 인터프리터에 붙다가 충돌하던 문제를 다룬다.
종료를 막는 interpreter guard, 종료 중이거나 삭제됐을 수 있는 인터프리터에
안전하게 접근하는 interpreter view,
종료 보호가 들어간 attach·detach API가 추가됐다.
`PyGILState_Ensure()`와 `PyGILState_Release()`는 soft deprecated가 되었다.
제거 계획은 없지만 새 `PyGILState` API는 더 나오지 않는다.

## 트레이드오프

### 지연 임포트는 시작 시간을 얻고 실패 시점과 부작용 순서를 내준다

지연 임포트가 주는 이득은 분명하다.
PEP 810은 Meta의 Instagram 서버와 ML 워크로드, Hudson River Trading,
PySide에서 10~20%의 시작 시간 개선 같은 사례를 근거로 든다.
CLI 도구, 테스트 모음, 의존성 그래프가 큰 애플리케이션이 주된 수혜자다.

대가는 세 가지다.
`ImportError`가 시작 시점이 아니라 처음 쓰는 시점에 나므로,
드물게 실행되는 경로의 임포트 오류는 배포 뒤 그 경로를 탈 때 비로소 드러난다.
모듈 최상위의 부작용은 첫 사용 시점으로 밀린다.
데코레이터로 플러그인을 등록하는 레지스트리 패턴은 아무도 그 모듈의 이름을
건드리지 않으면 등록 자체가 일어나지 않는다.
그리고 임포트 순서가 코드에 적힌 순서가 아니라 실행 경로를 따르게 된다.

그래서 `lazy` 키워드로 하나씩 고르는 방식과 `-X lazy_imports=all`로 전체를 켜는
방식의 무게가 다르다.
키워드는 그 모듈을 아는 사람이 책임지고 고르는 것이고,
전역 모드는 내가 쓰지 않은 서드파티 코드의 부작용까지 미루는 것이다.
PEP가 라이브러리 작성자에게 전역 모드를 쓰지 말라고 하고,
필터 함수로 문제 모듈만 즉시 임포트하게 하는 탈출구를 둔 이유가 여기에 있다.
해석을 덧붙이면, 전역 모드는 시작 시간을 측정해 효과를 확인한 애플리케이션
진입점에서만 켜고,
CI에서는 지연 없는 실행도 함께 돌려야 두 동작의 차이가 드러난다.

### UTF-8 기본값은 이식성을 얻고 조용한 데이터 손상 위험을 남긴다

PEP 686이 내세우는 이득은 플랫폼마다 다른 기본 인코딩이 만들던 버그가
줄어든다는 것이다.
JSON, TOML, YAML, 대부분의 편집기, Node.js, Go, Rust, Java가 이미 UTF-8을
기본으로 쓴다.

그러나 PEP 스스로 이 변화가 `UnicodeError`나 글자 깨짐뿐 아니라
조용한 데이터 손상까지 일으킬 수 있다고 적는다.
가장 위험한 경우는 예외가 나지 않는 쪽이다.
로캘 인코딩으로 써 둔 파일을 3.15가 UTF-8로 읽으면 디코딩 오류로 멈추지만,
3.15가 UTF-8로 쓴 파일을 로캘 인코딩을 기대하는 다른 프로그램이 읽으면
깨진 데이터가 그대로 흘러간다.
PEP는 기본 인코딩 사용 자체를 deprecated로 만드는 안을 기각했다.
ASCII만 읽고 쓰는 코드가 많아 경고가 너무 많아지면 사람들이 경고를 무시하게
된다는 이유다.
결과적으로 영향받는 곳을 찾는 일은
사용자가 `EncodingWarning`을 직접 켜야만 가능하다.

### 새 버전은 오래된 버전의 지원 종료이기도 하다

simonw는 새 Python 출시에서 가장 반가운 점이
오래된 버전의 지원 종료라고 적었다.[^simonw]
이번에는 3.10이 빠지므로 지원 중인 모든 버전을 지원하는 라이브러리도
드디어 3.11 기능을 쓸 수 있다는 것이다.
ryandrake는 3.10에 묶인 사용자를 깨는 정책이 싫다고 반박했고,[^ryandrake]
zahlman은 이전 패키지 버전은 계속 남아 있고 패키지 도구가 Python 버전에 맞는
릴리스를 고르므로 깨지는 일은 실제로 일어나지 않는다고 답했다.[^zahlman-support]

3.15로 올릴지와 별개로, 라이브러리를 관리한다면 이번 릴리스가 지원 범위의
하한을 올리는 신호라는 점이 실무에서는 더 즉각적이다.
반대로 애플리케이션 쪽은 배포판이 묶어 둔 Python 버전에 오래 머물 수 있으므로,
의존성의 `requires-python`이 언제 올라가는지 지켜봐야 한다.

## 함정

`lazy import`를 `try`/`except ImportError` 안에 넣는
선택적 의존성 패턴은 쓸 수 없다.
`SyntaxError`다.
선택적 의존성은 여전히 즉시 임포트로 감싸거나 사용 지점에서 처리해야 한다.

`globals()`나 모듈의 `__dict__`로 꺼낸 값은 reification되지 않는다.
딕셔너리를 순회하며 값을 검사하는 코드, 예를 들어 플러그인 탐색이나
직렬화 코드는 실제 모듈 대신 프록시를 만날 수 있다.
`dir()`도 reification을 일으키지 않는다.
필요하면 프록시의 `resolve()`를 직접 호출한다.

`isinstance(x, dict)` 검사는 `frozendict`를 받지 않는다.
API가 매핑을 받는다면 `collections.abc.Mapping`으로 검사하는 편이 안전하다.

`sentinel`은 참으로 평가된다.
`None` 대신 `sentinel`로 바꾸면서
`if not value:` 검사를 남겨 두면 의미가 뒤집힌다.

Porting 절에는 조용히 동작이 바뀌는 항목이 여럿 있다.

| 항목                                    | 바뀐 동작                                                      |
| --------------------------------------- | -------------------------------------------------------------- |
| `argparse` `add_argument('-f', '-foo')` | `dest`가 `'f'`가 아니라 `'foo'`로 추론된다                     |
| `base64.urlsafe_b64decode()`            | 입력 패딩을 더 이상 요구하지 않는다, 필요하면 `padded=True`    |
| `unittest` `assertWarns()`              | 맞지 않는 경고를 삼키지 않아 가려졌던 경고가 새어 나올 수 있다 |
| `sqlite3.connect()`                     | `database` 외 인자는 키워드 전용이다                           |
| `datetime.strptime()`                   | 연도 없는 `%d`는 `ValueError`다                                |
| `resource.RLIM_INFINITY`                | 항상 양수다, 예전 음수 값을 넘기는 것은 deprecated             |
| `xml.etree.ElementTree.iterparse()`     | 파일을 연 이터레이터를 닫지 않으면 `ResourceWarning`이 난다    |

제거된 것 중에는 `http.server`의 `CGIHTTPRequestHandler`와 `--cgi` 플래그,
`importlib`의 `load_module()`, `sre_compile`·`sre_constants`·`sre_parse`
모듈, `typing.no_type_check_decorator`, `NamedTuple`의 키워드 인자 문법이 있다.
`__version__` 속성은 `argparse`, `json`, `re`, `logging` 등 표준 라이브러리 여러
모듈에서 deprecated가 되었고 3.20에 제거된다.

Tachyon의 낮은 오버헤드는 대상 프로세스 쪽 이야기다.
프로덕션 컨테이너에서 쓰려면 `CAP_SYS_PTRACE` 같은 권한을 미리 열어 두어야 하고,
이는 보안 정책과 부딪힐 수 있다.

`uvx --python 3.15 whatsnewt`가 이상하게 동작하면 uv 자체가 오래된 것일 수 있다.
ameliaquining은 이 명령이 3.15.0a2로 실행되어 퍼즐 일부가 동작하지 않았는데,
원인은 패키지 관리자로 설치한 uv를 가리던
오래된 curl 설치 uv였다고 밝혔다.[^ameliaquining]

macOS 27.0과 `tkinter` 문제는 3.15만의 문제가 아니라 모든 현행 Python에 걸린다.
Lobste.rs에서 sri는 `tkinter` GUI에 스크립트를 연결하려던 계획을 미루겠다며
내장 IDE인 IDLE까지 영향을 받는다는 점을 짚었다.[^sri]

## 확인하기

아래 명령은 문서에 적힌 옵션과 API를 조합한 것이며,
3.15 인터프리터에서 직접 실행해 확인한 것은 아니다.

```bash
# 3.15를 받아 REPL을 띄운다
uv python install 3.15
uv run --python 3.15 python

# 기본 인코딩이 UTF-8인지 확인한다 (UTF-8 모드면 1)
uv run --python 3.15 python -c "import sys; print(sys.flags.utf8_mode)"

# 지연 임포트 전후의 시작 시간을 비교한다
uv run --python 3.15 python -X importtime -c "import myapp" 2> eager.log
uv run --python 3.15 python -X lazy_imports=all -X importtime -c "import myapp" 2> lazy.log
```

지연 임포트가 실제로 미뤄지는지는 `sys.modules`로 확인한다.

```python
import sys

lazy import decimal

assert "decimal" not in sys.modules  # 아직 로딩 전
print(decimal.Decimal("1.1"))        # 첫 접근에서 로딩
assert "decimal" in sys.modules
```

## 체크리스트

- `-X warn_default_encoding`으로 테스트를 돌려 `EncodingWarning`이 0건인가
- 로캘 인코딩 파일을 다루는 코드에 `encoding="locale"`이나 명시적 인코딩을 넣었는가
- 다른 프로그램이 읽는 출력 파일의 인코딩을 명시했는가
- 지연시킨 모듈 중 임포트 시점 부작용(등록, 설정 변경)에 기대는 것이 없는가
- 전역 지연 모드를 켰다면 필터로 제외할 모듈 목록을 정했는가
- `isinstance(x, dict)` 검사가 `frozendict`를 받아야 하는 API에 남아 있지 않은가
- Porting 절의 `argparse`, `base64`, `unittest`, `sqlite3` 변경에 걸리는 코드가 없는가
- `.pth` 파일의 `import` 줄로 시작 코드를 실행하는 패키지를 쓰거나 배포하는가
- C 확장을 배포한다면 `abi3t` 전환 여부와 `cp315t` 별도 빌드 여부를 정했는가
- 자체 네이티브 빌드에 프레임 포인터 플래그를 켰는가
- macOS 27.0에서 `tkinter`나 IDLE에 기대는 작업 흐름이 있는가

## 기억할 원칙

### 기본값에 기대지 않은 코드만 기본값 변경을 공짜로 넘긴다

이번 릴리스의 큰 변화 둘은 모두 기본값에 관한 것이다.
UTF-8 기본 인코딩은 기본값을 바꿨고, 지연 임포트는 임포트가 즉시 실행된다는
암묵적 기본값을 선택적으로 깨뜨린다.
어느 쪽이든 `encoding`을 명시하고, 모듈 최상위 부작용 대신 명시적 초기화 함수를
쓴 코드는 영향을 거의 받지 않는다.

PEP 810이 임포트 부작용 대신 명시적 초기화 함수를 쓰라고 권하고,
PEP 686이 `encoding`을 명시하라고 권하는 것은 같은 조언이다.
기본값은 언젠가 바뀌고, 그때 비용을 치르는 것은 기본값을 계약으로 여긴 코드다.

---

[^hleszek]: <https://news.ycombinator.com/item?id=50025172>

[^zahlman-utf8]: <https://news.ycombinator.com/item?id=50029571>

[^masklinn-utf8]: <https://news.ycombinator.com/item?id=50030296>

[^PaulHoule]: <https://news.ycombinator.com/item?id=50025582>

[^zem]: <https://news.ycombinator.com/item?id=50026890>

[^ris]: <https://news.ycombinator.com/item?id=50026761>

[^hawski]: <https://lobste.rs/s/rpiwtb/python_3_15_0#c_g1qevf>

[^rirze]: <https://news.ycombinator.com/item?id=50023591>

[^alextremblay]: <https://news.ycombinator.com/item?id=50023642>

[^febed]: <https://news.ycombinator.com/item?id=50030015>

[^zahlman-gif]: <https://news.ycombinator.com/item?id=50021510>

[^ngoldbaum]: <https://news.ycombinator.com/item?id=50022069>

[^ngoldbaum-pyo3]: <https://news.ycombinator.com/item?id=50025147>

[^haberman]: <https://news.ycombinator.com/item?id=50024463>

[^ngoldbaum-protobuf]: <https://news.ycombinator.com/item?id=50025138>

[^hncbw02z5a]: <https://news.ycombinator.com/item?id=50022681>

[^masklinn-abi3t]: <https://news.ycombinator.com/item?id=50024462>

[^simonw]: <https://news.ycombinator.com/item?id=50021647>

[^ryandrake]: <https://news.ycombinator.com/item?id=50021844>

[^zahlman-support]: <https://news.ycombinator.com/item?id=50029431>

[^ameliaquining]: <https://news.ycombinator.com/item?id=50030687>

[^sri]: <https://lobste.rs/s/rpiwtb/python_3_15_0#c_wxfwff>
