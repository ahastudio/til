# (How to Write a (Lisp) Interpreter (in Python))

<https://norvig.com/lispy.html>

HN 토론:

- 2024년: <https://news.ycombinator.com/item?id=39665939> (193점, 91개 댓글)
- 2026년: <https://news.ycombinator.com/item?id=48619831> (187점, 61개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/alzcxf>

## 요약

Peter Norvig이 작성한 이 글은 Python으로 Scheme 방언 인터프리터 "Lispy"를 구현하는 과정을 단계적으로 설명한다.
117줄, 4,000바이트의 코드로 동작하는 Lisp 인터프리터를 만들 수 있음을 보여주며,
인터프리터 구현의 일반 원리와 함께 Scheme의 우아한 설계 철학을 드러낸다.

Scheme의 핵심 매력은 극단적 미니멀리즘이다.
Python의 키워드가 33개, 문법 형태가 110개인 데 반해,
Scheme은 키워드 5개와 문법 형태 8개만으로 완전한 언어를 구성한다.
모든 프로그램이 표현식으로만 이루어지며, 문장(statement)과 표현식(expression)의 구분이 없다.

Lispy는 파싱과 실행 두 단계로 동작한다.
파싱 단계에서 문자 시퀀스를 중첩 리스트(AST)로 변환하고,
실행 단계에서 그 리스트를 의미 규칙에 따라 평가한다.
환경(environment)은 이름을 값에 매핑하는 딕셔너리로 구현되며,
중첩 구조로 렉시컬 스코핑을 지원한다.
Lispy가 의도적으로 생략한 기능으로는 꼬리 재귀 최적화, 계속(continuation), 문자열/벡터 타입,
100개 이상의 표준 기본 프로시저, 에러 처리 등이 있다.

## 소스 코드 해설

### 타입 시스템: Python 타입에 Scheme 의미를 부여하다

```python
Symbol = str
List   = list
Number = (int, float)
```

새로운 클래스를 정의하는 대신 Python의 내장 타입에 별칭을 부여한다.
`Symbol`은 단순히 `str`이고, `List`는 단순히 `list`다.
Lisp의 심벌과 리스트가 Python의 문자열과 리스트에 자연스럽게 대응되기 때문에 가능한 선택이다.
별도의 타입 변환 없이 Python의 모든 내장 연산을 그대로 활용할 수 있다.

### 파서: 괄호 문법이 파싱을 단순하게 만든다

```python
def tokenize(s):
    return s.replace('(',' ( ').replace(')',' ) ').split()
```

`tokenize`는 단 한 줄이다.
괄호 앞뒤에 공백을 삽입한 뒤 `.split()`으로 자르면 토큰 목록이 만들어진다.
Lisp의 문법이 괄호로만 구성되기 때문에 가능한 구현이다.
정규표현식도 필요 없다.

```python
def read_from_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)
```

`read_from_tokens`는 재귀 하강 파서다.
`(`를 만나면 `)` 전까지 재귀 호출로 하위 표현식을 수집하고,
그것도 아니면 `atom`으로 원자 값을 반환한다.
Python 리스트의 중첩이 곧 AST가 된다.

```python
def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)
```

`atom`은 `int`, `float`, 그것도 아니면 `Symbol`(문자열) 순서로 변환한다.
예외를 타입 판별 수단으로 사용하는 Python다운 코드다.

### 환경: 렉시컬 스코핑의 최소 구현

```python
class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        return self if (var in self) else self.outer.find(var)
```

`Env`는 `dict`를 상속한다.
`outer` 포인터 하나로 스코프 체인을 구현한다.
`find`는 현재 환경에 변수가 없으면 `outer.find`를 재귀 호출한다.
"변수는 정의된 환경에서 찾는다"는 렉시컬 스코핑의 본질이 이 9줄에 담겨 있다.

전역 환경은 `standard_env`로 초기화된다.
`vars(math)`로 `math` 모듈 전체를 한 번에 올리고,
`operator` 모듈로 산술 연산자를 함수로 바인딩한다.

```python
env.update(vars(math))  # sin, cos, sqrt, pi, ...
env.update({
    '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv,
    'begin': lambda *x: x[-1],
    'car':   lambda x: x[0],
    'cdr':   lambda x: x[1:],
    'cons':  lambda x,y: [x] + y,
    ...
})
```

`begin`은 여러 표현식을 순서대로 평가하고 마지막 값을 반환하는 Scheme 특수 형태다.
`lambda *x: x[-1]` 한 줄로 구현된다.
`car`, `cdr`, `cons`는 Lisp의 핵심 리스트 연산이며, Python 리스트 연산과 완벽하게 대응된다.

### `eval`: 인터프리터의 심장

```python
def eval(x, env=global_env):
    if isinstance(x, Symbol):      # 변수 참조
        return env.find(x)[x]
    elif not isinstance(x, List):  # 숫자 등 상수
        return x
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:                          # 프로시저 호출
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)
```

`eval`은 `if-elif` 체인으로 모든 Scheme 표현식을 처리한다.
`Symbol`이면 환경 체인에서 값을 찾고,
리스트도 아니면 그대로 반환하며,
`quote`는 평가 없이 표현식 자체를 돌려준다.
`if`는 `test` 결과에 따라 `conseq`나 `alt`를 평가하고,
`define`은 현재 환경에 새 바인딩을 만들며,
`set!`은 `find`로 기존 바인딩이 있는 환경을 찾아 값을 갱신한다.
`lambda`는 현재 환경을 캡처해 `Procedure` 객체를 만들고,
나머지는 모두 프로시저 호출이다.

`define`과 `set!`의 차이가 여기서 선명하게 드러난다.
`define`은 항상 현재 환경에 새 바인딩을 만들고,
`set!`은 `find`로 이미 바인딩된 환경을 찾아 그 값을 변경한다.

### `Procedure`: 클로저의 최소 표현

```python
class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))
```

`Procedure`는 파라미터 이름 목록, 본문 표현식, 정의 시점의 환경 세 필드를 가진다.
`__call__`은 파라미터와 인수를 바인딩한 새 `Env`를 만들고,
그 `outer`를 정의 시점 환경으로 설정한다.
호출 시점이 아닌 정의 시점 환경을 캡처한다 — 이것이 클로저(closure)다.

## 분석

### 인터프리터 구현은 언어에 대한 가장 깊은 이해 방식이다

Steve Yegge의 인용 — "컴파일러가 어떻게 작동하는지 모르면 컴퓨터가 어떻게 작동하는지 모르는 것이다" — 은 이 글의 핵심 주장을 압축한다.
파싱, AST, 환경, 평가 규칙의 4단계 구조는 모든 언어 구현의 공통 골격이다.
Lispy를 이해하면 Ruby가 어떻게 클로저를 구현하는지,
JavaScript가 어떻게 스코프 체인을 탐색하는지,
Python이 어떻게 네임스페이스를 관리하는지를 이해하는 개념적 토대가 생긴다.

Python을 구현 언어로 선택한 것은 의도적이다.
Python의 리스트는 Lisp의 리스트와 자연스럽게 대응되고,
딕셔너리는 환경 구현에 정확히 맞아떨어지며,
가비지 컬렉션은 Python 런타임이 처리해 구현자가 신경 쓸 필요가 없다.
cjfd의 HN 댓글이 지적했듯이, C++로 같은 구현을 시도하면 순환 참조로 인해 `shared_ptr`이 충분하지 않아
가비지 컬렉션 구현이 필요해지는 지점에서 복잡도가 폭발한다.[^cjfd]

### Scheme의 미니멀리즘은 언어 설계의 선택이 아니라 철학이다

키워드 5개, 문법 형태 8개라는 숫자는 단순한 통계가 아니라 설계 철학의 결과다.
Scheme은 John McCarthy의 원래 Lisp 아이디어를 Guy Steele과 Gerald Sussman이
"가장 작은 완전한 언어"로 정제한 결과다.
람다 대수(lambda calculus)에서 증명된 것처럼,
몇 가지 기본 요소의 조합으로 모든 계산을 표현할 수 있다.

이 철학은 실용적 결과를 낳는다.
Scheme 인터프리터를 이해한 사람은 언어를 확장하는 방법도 이해한다.
paddy_m은 HN 댓글에서 `lispy2.py`를 수정해 JSON 방언 Lisp를 만들고
로우코드 UI를 구축했다고 밝혔다.[^paddy_m]
괄호를 대괄호로 바꿔 JSON 호환 Lisp를 만들고, React 프론트엔드가 이를 직접 조작하게 한 것이다.
이런 창의적 응용이 가능한 것은 구현이 이해 가능한 수준으로 작기 때문이다.

### 재귀가 반복을 대체하는 방식은 계산의 본질에 닿는다

Lispy에서 반복은 재귀 함수 호출로 표현된다.

```scheme
(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))
```

이 표현은 단순히 `while` 루프의 함수적 대안이 아니다.
수학적 귀납법과 같은 구조로, 기저 사례(n≤1)와 귀납 단계(n>1)를 명시적으로 분리한다.

이 구조가 중요한 이유는 꼬리 재귀 최적화와 연결되기 때문이다.
Lispy가 의도적으로 꼬리 재귀를 생략한 것은 구현 단순성을 위한 선택이지만,
완전한 Scheme 구현에서 꼬리 재귀는 선택이 아닌 필수다.
꼬리 재귀 없이는 반복적 프로세스를 스택 오버플로우 없이 표현할 수 없고,
재귀가 반복을 진정으로 대체할 수 없다.
이 생략은 "이해를 위한 Lispy"와 "실용적 Scheme 구현" 사이의 간극을 정확히 짚는다.

## 비평

### 117줄의 단순성은 의도적 생략의 결과이며, 그 생략의 비용이 과소평가된다

Norvig은 Lispy가 생략한 기능들을 솔직하게 나열하지만,
그 생략이 얼마나 근본적인지는 충분히 강조하지 않는다.
꼬리 재귀 최적화의 부재는 실제 프로그래밍에서 치명적이다.
많은 Scheme 관용 패턴이 꼬리 재귀를 전제하며, 이 없이는 스택 공간이 프로그램 길이의 상한이 된다.
계속(continuation)의 부재는 비동기 프로그래밍, 예외 처리, 코루틴 같은 고급 제어 흐름을 불가능하게 한다.

"117줄로 Lisp 인터프리터를 쓸 수 있다"는 메시지는 매력적이지만,
실제 언어 구현자가 씨름하는 복잡도의 대부분은 이 생략된 기능들에 있다.
독자가 이 글에서 얻는 이해와 실제 언어 구현 사이의 간극은
글의 단순성이 암시하는 것보다 훨씬 크다.

### Python의 "공짜" 기능들이 실제 구현의 어려움을 가린다

가비지 컬렉션, 동적 타입, 유니코드 문자열 처리, 예외 시스템 등이 모두 Python 런타임에서 공짜로 제공된다.
pjmlp의 HN 댓글은 이 문제를 다른 각도에서 짚는다.[^pjmlp]
Norvig이 2000년에 쓴 "Python for Lisp Programmers"에서 지적한 Python의 두 가지 약점 —
컴파일 타임 타입 검사의 부재, Lisp 대비 10배 느린 실행 속도 — 이 2024년에도 여전히 유효하다는 것이다.
Python으로 Lisp를 구현하는 것은 교육적으로 탁월하지만,
그 결과물은 Python이 가진 동일한 한계를 그대로 상속한다.

C로 Lisp 인터프리터를 구현하는 경험은 matheusmoreira가 댓글에서 언급했듯이 "그 자체의 모험"이다.[^matheusmoreira]
메모리 관리, 가비지 컬렉션 구현, 타입 태깅(type tagging)은 모두 Python이 추상화한 복잡도들이며,
그것을 직접 구현할 때 비로소 언어 런타임의 진짜 어려움이 드러난다.

### 이 글은 "인터프리터의 구조"를 가르치지, "인터프리터 구현 방법"을 가르치지 않는다

lisper의 HN 댓글이 보여준 "클로저를 포함한 Lisp 방언을 137줄 Python으로"[^lisper]라는 구현은
이 분야에서 코드 골프와 정상 공학이 쉽게 혼동된다는 것을 보여준다.
Lispy를 읽고 "인터프리터 구현은 쉽다"는 결론을 내리면,
실제 프로덕션 언어 구현에 뛰어들었을 때 큰 고통을 경험할 것이다.

V8, SpiderMonkey, CPython 같은 실제 인터프리터/컴파일러는
JIT 컴파일, 타입 특화(type specialization), 인라인 캐시(inline cache),
가비지 컬렉터의 세대별 수집, 스택 프레임 최적화 등
Lispy가 아예 건드리지 않는 영역에서 대부분의 복잡도가 발생한다.
그 구분을 명확히 전달하지 않는 것이 이 글의 한계다.

## 인사이트

### Lispy가 반복적으로 재발견되는 이유는 "이해 가능한 완전성" 때문이다

이 글이 2010년에 작성되었음에도 2026년 HN에 187점을 받으며 다시 등장한 것은 우연이 아니다.
HN 모더레이터 dang의 댓글은 이 반복의 역사를 정확히 기록했다.[^dang]
2010년 9월 첫 제출(39개 댓글)부터 2026년까지, 이 글은 16년에 걸쳐 10번 이상 HN 첫 페이지에 올랐다.
stevekemp가 언급한 속편 `lispy2.py`까지 합치면,[^stevekemp]
이 두 편의 글은 인터프리터를 배우고 싶은 사람들이 세대를 넘어 반복적으로 발견하는 고전이 되었다.

그 이유는 "이해 가능한 완전성"에 있다.
대부분의 교재는 이해 가능하지만 완전하지 않거나(장난감 예제),
완전하지만 이해하기 어렵다(실제 언어 구현 코드).
Lispy는 실제로 동작하는 완전한 언어이면서 한 사람이 한 번에 읽고 이해할 수 있는 크기다.
chombier가 댓글에서 짚었듯이, "프로그래밍 언어 구현을 시작하고 싶다면 이 글이 최고의 자료이며,
다음 단계는 Crafting Interpreters"라는 것이 커뮤니티의 공통된 평가다.[^chombier]
이 균형점은 의도적 설계의 결과이며, 수십 년이 지나도 추천 목록 1번에 머무는 교육 자료로서의 가치가 여기서 나온다.

### 최소 언어 구현의 전통은 프로그래밍 교육의 통과의례로 자리잡았다

djtriptych가 ES6로 변환했고,[^djtriptych]
paddy_m이 JSON 방언을 만들었으며, lisper가 137줄로 재구현했다.
Lispy를 자신의 언어로 포팅하거나 확장하는 것은 비공식적인 프로그래밍 통과의례가 되었다.
azhenley의 댓글은 이 전통을 개인의 습관으로 체화한 사례다.[^azhenley]
"Lisp 구현은 내가 가장 좋아하는 프로젝트 중 하나다. 1~2년마다 매번 다른 접근 방식으로 다시 구현한다."
반복 구현이 의미 있는 이유는, 같은 문제를 다른 언어나 패러다임으로 풀 때마다 새로운 통찰이 생기기 때문이다.

이 전통의 가치는 특정 기술 습득이 아니라 사고 방식의 형성에 있다.
tosh(2026년 이 글을 HN에 제출한 사람)는 댓글에서 "Lisp 또는 Forth 구현을 강력하게 추천한다.
계몽적인 경험이며, 무엇보다 괄호를 다른 시각으로 보게 된다"고 썼다.[^tosh]
언어를 데이터 구조로 표현하고, 프로그램을 트리로 변환하며,
평가를 트리 순회로 구현하는 것을 한 번 직접 해본 사람은
이후 어떤 언어를 배우거나 어떤 코드를 읽을 때도 다른 시각을 갖게 된다.
Norvig이 만든 것은 인터프리터가 아니라 그 시각을 전달하는 도구다.

### 수동 메모리 관리 Lisp에 대한 수요는 시스템 프로그래밍의 지속적 긴장을 드러낸다

mapreduce의 HN 댓글 — "GC 없는 Lisp가 있다면 C++을 버리겠다" — 은 흥미로운 욕구를 드러낸다.[^mapreduce]
Lisp의 구문적 균일성과 표현력을 원하지만, 가비지 컬렉터의 비결정적 일시 정지를 피하고 싶다는 것이다.
이 욕구는 Zig, Rust, Vale 같은 현대 시스템 언어들이 탐구하는 영역과 맞닿는다.
PreScheme(Scheme의 수동 메모리 관리 방언)이 댓글에서 언급되었지만,
주류 생태계에서 이 조합을 완전히 실현한 언어는 아직 없다.

GC는 메모리 안전성과 개발 편의성을 제공하지만 예측 불가능한 지연 시간을 도입한다.
수동 메모리 관리는 제어권을 주지만 복잡성과 위험을 동반한다.
Rust의 소유권 시스템은 이 사이에서 세 번째 길을 찾으려는 시도지만,
"Lisp 구문 + 수동 메모리"의 조합은 여전히 언어 설계의 미개척 영역으로 남아 있다.

---

[^cjfd]: <https://news.ycombinator.com/item?id=39666238>
[^paddy_m]: <https://news.ycombinator.com/item?id=39670780>
[^pjmlp]: <https://news.ycombinator.com/item?id=39666627>
[^matheusmoreira]: <https://news.ycombinator.com/item?id=39668922>
[^lisper]: <https://news.ycombinator.com/item?id=39666324>
[^stevekemp]: <https://news.ycombinator.com/item?id=39666462>
[^djtriptych]: <https://news.ycombinator.com/item?id=39668492>
[^mapreduce]: <https://news.ycombinator.com/item?id=39670350>
[^dang]: <https://news.ycombinator.com/item?id=48621746>
[^chombier]: <https://news.ycombinator.com/item?id=48620229>
[^azhenley]: <https://news.ycombinator.com/item?id=48620099>
[^tosh]: <https://news.ycombinator.com/item?id=48619922>
