# Glojure

원문: <https://github.com/glojurelang/glojure>

HN 토론: <https://news.ycombinator.com/item?id=42272524> (234점, 68개 댓글)

## 소개

Glojure는 Go 위에서 동작하는 Clojure 인터프리터다.
Clojure가 JVM 위에서 Java 생태계에 접근하듯,
Glojure는 Go 위에서 Go 라이브러리에 접근할 수 있게 설계되었다.
프로젝트는 현재 초기 개발 단계로, v1 릴리스 이전까지는 하위 호환성을 보장하지 않는다.

“호스티드(hosted) 언어”라는 개념이 이 프로젝트의 핵심이다.
JVM 기반 Clojure에서 모든 Java 값이 Clojure 값으로도 쓰이듯,
Glojure는 Go 값과 Clojure 값 사이의 완전한 상호 운용성을 목표로 한다.
이 점이 대부분의 다른 Go Clojure 구현체와 차별화되는 특징이다.

## 설치 및 사용법

Go 1.24 이상이 필요하며, `go install`로 설치한다.

```bash
go install github.com/glojurelang/glojure/cmd/glj@latest
```

### REPL

```bash
$ glj
user=> (+ 1 2 3)
6
user=> (println "Hello from Glojure!")
Hello from Glojure!
nil
```

REPL은 vi/emacs 편집 모드, 탭 완성, 멀티라인 편집, 히스토리 저장(`~/.glj_history`),
Ctrl+Z 잡 컨트롤 등을 지원한다.

### 스크립트 실행

```bash
$ glj -e '(apply + (range 3 10))'
42
$ glj hello.glj World
```

### Go 애플리케이션에 임베딩

Glojure를 Go 애플리케이션 내부에 스크립팅 엔진으로 삽입할 수 있다.

```go
package main

import (
    "fmt"
    _ "github.com/glojurelang/glojure/pkg/glj"
    "github.com/glojurelang/glojure/pkg/runtime"
)

func main() {
    result := runtime.ReadEval(`
        (defn factorial [n]
          (if (<= n 1) 1 (* n (factorial (dec n)))))
        (factorial 5)
    `)
    fmt.Printf("5! = %v\n", result)
}
```

Go 함수를 Clojure에서 호출하거나, Clojure 함수를 Go에서 호출하는 양방향 interop도 지원한다.

## Go Interop

Go 표준 라이브러리 패키지(`fmt`, `net/http`, `os`, `sync` 등 약 22개)가 기본 제공되며,
패키지명의 `/`는 `:`로 변환해 사용한다.

```clojure
user=> (println (fmt.Sprintf "Methods: %v" [net:http.MethodGet net:http.MethodPost]))
Methods: ["GET" "POST"]
nil
```

추가 패키지는 `gen-import-interop` 도구로 패키지 맵을 생성하여 컴파일 시 포함한다.

## Clojure와의 차이점

숫자 타입이 JVM 대신 Go 타입으로 매핑된다.

| Clojure 타입 | Glojure 타입       |
| ------------ | ------------------ |
| `long`       | `int64`            |
| `double`     | `float64`          |
| `byte`       | `byte` (unsigned)  |
| `char`       | `lang.Char` (rune) |
| `BigInt`     | `*lang.BigInt`     |

Go `byte`는 부호 없는 정수인 반면 JVM `byte`는 부호 있는 정수이며,
Go `int`는 플랫폼에 따라 32비트 또는 64비트이지만 JVM `int`는 항상 32비트다.

## 다른 Go Clojure 구현체와의 비교

| 특성                            | Glojure | Joker | let-go          |
| ------------------------------- | ------- | ----- | --------------- |
| 호스티드 언어                   | Yes     | No    | No              |
| 확장 가능한 Go interop          | Yes     | No    | No              |
| 동시성                          | Yes     | Yes   | Yes             |
| Clojure 툴링(린터 등)           | No      | Yes   | No              |
| 실행 방식                       | 트리 워크 | 트리 워크 | 바이트코드 |

Joker는 Clojure 린터 지원이 있지만 호스티드 언어 특성이 없고,
let-go는 바이트코드 인터프리터로 실행 방식이 다르다.

## 분석

### “호스티드 언어”라는 설계 철학이 의미하는 것

Glojure가 스스로를 “호스티드 언어”로 규정하는 것은 단순한 기술 구현 선택이 아니다.
Clojure의 창시자 Rich Hickey가 JVM 위에서 언어를 설계할 때 채택한
“Clojure는 JVM 언어다, JVM 위의 언어가 아니라”는 원칙을 Go 맥락으로 이식하려는 시도다.
이 원칙의 핵심은 타입 시스템 경계의 소멸이다 — Go 값이 곧 Clojure 값이고,
별도의 변환 계층 없이 양쪽을 넘나들 수 있어야 한다.

이 설계 선택이 가져오는 실질적 의미는 크다.
JVM 기반 Clojure 사용자는 Java 라이브러리 전체를 Clojure에서 직접 쓸 수 있었고,
이것이 Clojure가 실용적인 언어로 자리잡는 데 결정적인 역할을 했다.
Glojure가 같은 모델을 따른다면, 이론적으로 Go 표준 라이브러리와
서드파티 Go 생태계 전체를 Clojure 문법으로 쓸 수 있는 환경이 된다.
Go의 성숙한 네트워킹, 동시성, 시스템 프로그래밍 라이브러리가 모두 Clojure REPL에서 접근 가능해진다.
HN 커뮤니티에서도 이 가능성에 대한 기대가 표현되었다.
breadchris는 "Clojure가 Go 위에서 동작하는 것은 정말 더 많은 관심을 받아야 한다.
Clojure가 JVM 위에 구축된 것은 나쁜 결정이 아니지만,
Go 생태계에 안정적으로 쌓여가는 수많은 패키지들을 Clojure로 조합할 수 있으면 좋겠다"고 밝혔다.[^breadchris]
실제로 bbqfog는 Go 함수를 `->>` 파이프라인과 `doto`로 조합하는 매크로가
정상 작동하는 코드 예제를 공유하며 이 가능성이 이미 현실임을 보여주었다.[^bbqfog]

그러나 이 철학은 동시에 구현 복잡도를 크게 높인다.
JVM은 리플렉션 API가 매우 강력해 런타임에 Java 타입 정보를 쉽게 조회할 수 있지만,
Go는 리플렉션이 상대적으로 제한적이고, 타입 정보가 컴파일 타임에 결정된다.
`gen-import-interop`이라는 코드 생성 도구가 필요한 이유가 여기에 있다 —
Java와 달리 Go는 런타임 패키지 발견이 어려우므로, 미리 패키지 맵을 생성해야 한다.

### Clojure의 Go 이식 시도가 이 시점에 나타나는 이유

Glojure는 2022년에 처음 등장했다.
이 시점은 Go가 제네릭을 도입(1.18, 2022년 3월)하고, Go 모듈 시스템이 성숙해지며,
Go 생태계가 단순한 시스템 도구를 넘어 범용 언어로 확장되던 시기와 겹친다.
동시에 Clojure 커뮤니티에서는 JVM 없는 Clojure를 원하는 수요가 꾸준히 존재했는데,
ClojureScript(JavaScript 타겟)나 Babashka(GraalVM 네이티브 이미지)가 그 수요를 일부 충족시켰다.

Go는 단일 바이너리 컴파일, 빠른 빌드, 낮은 메모리 사용이라는 특성 덕분에
JVM이 부담스러운 환경 — 컨테이너, CLI 도구, 서버리스 — 에서 매력적이다.
Glojure는 이 맥락에서 “Go의 배포 특성 + Clojure의 표현력”을 결합하려는 시도로 읽힌다.
특히 Go 애플리케이션에 Clojure를 임베딩 스크립팅 언어로 쓰는 use case는
기존 어떤 Clojure 구현체도 제공하지 못했던 포지션이다.

### 임베딩 스크립팅 엔진으로서의 위치

README가 두 가지 사용 방식을 병렬로 제시하는 구성이 흥미롭다:
독립 실행형 `glj` 도구와 Go 애플리케이션 임베딩.
이 구성은 프로젝트의 실질적인 가치가 어디에 있는지를 시사한다.

독립 실행형 Clojure 인터프리터로서 Glojure는 이미 성숙한 경쟁자들 — 공식 Clojure, Babashka — 과
경쟁해야 한다.
반면 “Go 앱에 임베딩 가능한 Clojure 스크립팅 엔진”이라는 니치는 훨씬 비어 있다.
Lua가 C/C++ 애플리케이션에 임베딩 스크립팅 언어로 성공했던 패턴,
혹은 JavaScript(V8)가 Node.js를 통해 서버 임베딩 엔진으로 쓰이는 패턴을
Clojure+Go 조합으로 재현하려는 시도로 볼 수 있다.

## 비평

### 호스티드 언어 원칙이 Go의 타입 시스템 앞에서 삐걱거린다

Glojure가 주장하는 “Go 값 = Clojure 값”의 완전한 상호 운용성은
JVM 맥락에서보다 Go 맥락에서 훨씬 더 마찰이 크다.
JVM Clojure는 Java의 리플렉션 API 덕분에 런타임에 임의의 Java 객체를 투명하게 다룰 수 있었고,
이것이 `.method` 문법으로 Java 메서드를 직접 호출하는 매끄러운 interop을 가능하게 했다.

Go에서는 상황이 다르다.
Go의 리플렉션은 존재하지만, 패키지 수준의 심볼을 런타임에 동적으로 발견하는 메커니즘이 없다.
`gen-import-interop`이라는 코드 생성 단계가 필수인 이유가 이것이다.
이는 “임의의 Go 패키지를 Clojure에서 즉시 쓸 수 있다”는 환상이
실제로는 “미리 코드 생성을 돌리고 재컴파일해야 한다”는 조건부 진실임을 뜻한다.
진정한 호스티드 언어라면 이 마찰이 없어야 하는데, Glojure는 이 점에서 JVM Clojure의 경험을 재현하지 못한다.
throwaway894345는 이 문제를 직접적으로 지적한다.
"Go는 JVM보다 언어를 호스팅하기에 훨씬 불리하다.
Go 인터프리터가 아무리 최적화되어도 JVM이 제공하는 JIT 수준의 성능에는 미치지 못할 것이다.
이런 상황이 아니었으면 하지만, 아쉽게도 현실이 그렇다"고 말했다.[^throwaway894345]

### Clojure 툴링 생태계 부재가 주요 사용 사례를 막는다

비교 표에서 Glojure가 솔직하게 인정하는 약점이 있다: Clojure 툴링(린터, 포매터 등)이 없다는 것.
그런데 이 약점은 단순한 편의 기능의 부재가 아니다.

Clojure 개발 생산성의 핵심은 REPL 기반 인터랙티브 개발과,
Cider(Emacs), Cursive(IntelliJ), Calva(VS Code) 같은 IDE 통합에 있다.
이 툴링들은 nREPL 프로토콜 위에서 동작한다.
Glojure가 nREPL을 지원하지 않는 한, 기존 Clojure 개발자가 Glojure로 넘어올 이유가 극히 줄어든다.
CLI REPL은 존재하지만, 그것은 Clojure 개발 경험의 껍데기만 제공할 뿐이다.
결국 Glojure는 “Clojure 개발자를 위한 Go 접근 도구”도, “Go 개발자를 위한 Clojure 도구”도
아닌 어중간한 위치에 놓일 위험이 있다.

### 초기 개발 상태라는 경고가 핵심 가치 제안을 상쇄한다

README는 “버그, 누락된 기능, 제한된 성능을 예상하라”고 경고한다.
하위 호환성도 v1 이전까지 보장되지 않는다.
이 경고는 정직하지만, 동시에 프로젝트의 실질적 채택 가능성에 의문을 던진다.

Go 애플리케이션에 스크립팅 엔진을 임베딩하는 결정은 가볍지 않다.
스크립팅 엔진이 변경되면 기존 스크립트가 깨지고, 이는 사용자에게 직접적인 영향을 미친다.
하위 호환성을 보장받지 못하는 임베딩 언어를 프로덕션에 쓰기는 어렵다.
Lua, Tengo, Starlark, goja(JS) 같은 Go 임베딩 스크립팅 언어들이 이미 이 공간을 차지하고 있으며,
이들은 훨씬 안정적인 API를 제공한다.
Glojure가 “Clojure 문법”이라는 차별점 하나만으로 이 경쟁에서 이길 수 있는지는 불분명하다.
zerr의 “왜 Go로 트랜스파일해서 네이티브 실행 파일을 만들지 않느냐”는 질문[^zerr]에 대해
Glojure 작성자 jfhamlin은 직접 답변했다.
“트랜스파일은 분명히 고려 중인 방향이다.
현재는 인터랙티비티를 우선하는 use case에 집중하고 있어 인터프리터 방식이 더 적합하다.
하지만 특히 코어 라이브러리를 Go로 트랜스파일하는 것은 스타트업 성능 개선 수단으로
강하게 고려하고 있으며, 이후 공개 기능으로 제공될 수 있다”고 밝혔다.[^jfhamlin]
이 답변은 현재의 성능 한계를 인정하면서도 트랜스파일이 장기 로드맵에 있음을 시사한다.

### 트리 워크 인터프리터라는 구조적 한계

비교 표에서 드러나듯, Glojure는 트리 워크(tree-walk) 인터프리터다.
let-go가 바이트코드 인터프리터를 채택한 것과 대조된다.
트리 워크 인터프리터는 구현이 단순하지만, 성능 천장이 낮다.
Clojure on JVM이 JIT 컴파일의 혜택을 누리는 것과 달리,
Glojure는 AST를 매번 다시 순회해야 한다.
이는 “임베딩 스크립팅 엔진”이라는 use case에서 치명적일 수 있는데,
임베딩 스크립팅 엔진을 선택하는 이유 중 하나가 성능이기 때문이다.
README가 “제한된 성능을 예상하라”고 경고하는 맥락이 이 구조적 한계와 연결된다.
sesm이 제기한 “일반 Clojure는 JVM의 런타임 클래스 로딩 능력에 의존하는데,
Go VM도 그것을 할 수 있느냐”는 질문[^sesm]은 이 한계의 다른 측면을 드러낸다.
Go 인터프리터 위에서 동작하는 Glojure는 그 질문에 대해 “인터프리터이므로 가능하다”고 답할 수 있지만,
그 자체가 바로 트리 워크 인터프리터의 구조를 선택해야 했던 이유이기도 하다.
JVM처럼 클래스를 동적으로 로드하고 JIT 컴파일하는 메커니즘이 Go에 없으므로,
인터프리터 방식이 동적성을 확보하는 유일한 현실적 경로였던 것이다.

## 인사이트

### Go 스크립팅 언어 공간에서 Clojure가 가진 독특한 포지션

Go 임베딩 스크립팅 언어 시장은 이미 여러 선택지로 채워져 있다.
Lua는 전통적인 선택이고, Starlark는 구성 언어로서 Google이 채택했으며,
Tengo, Expr, goja(JavaScript) 등이 각자의 영역을 점유하고 있다.
이 언어들의 공통점은 Go 개발자가 새로 배워야 하는 문법을 제공한다는 것이다.

Clojure는 여기서 흥미로운 역설을 만든다.
Clojure를 이미 아는 개발자에게 Glojure는 즉시 생산적인 도구가 될 수 있다.
그러나 Clojure 인구는 전체 개발자 중 소수이며, 그 소수가 Go를 메인 언어로 쓸 확률은 더 낮다.
역설적으로, Glojure의 실질적 사용자는 “Clojure를 알면서 Go 생태계가 필요한 사람”보다
“Go를 쓰면서 Lisp 계열 스크립팅 언어에 관심 있는 사람”이 될 가능성이 높다.
후자에게 Clojure의 학습 곡선은 Lua나 Starlark보다 훨씬 가파르다.
이 수요 불일치는 Glojure의 성장에 구조적 제약으로 작용할 것이다.
no_wizard는 이 틈새를 더 구체적으로 제시한다.
"Go 생태계는 웹과 HTTP 서비스에 매우 뛰어나다.
이 영역에서 Go를 쓸 때 진가가 드러난다"고 언급하며[^no_wizard],
Clojure 개발자들이 Go의 HTTP 생태계에서 얻을 수 있는 이점을 지적했다.
이것은 Glojure가 찾아야 할 포지션에 대한 힌트를 담고 있다 —
범용 스크립팅이 아니라 Go의 네트워킹 강점을 Clojure 문법으로 활용하는 특수 목적 도구.

### 단일 바이너리 문화와 Lisp의 충돌

Go의 가장 강력한 문화적 특성 중 하나는 단일 바이너리 배포다.
의존성 없이 하나의 실행 파일로 배포한다는 원칙이 Go 생태계 전반에 깊이 박혀 있다.
Glojure를 Go 앱에 임베딩하면 이 원칙은 유지된다 — Clojure 런타임이 바이너리 안에 포함된다.

그러나 Clojure의 개발 철학은 이와 상충하는 면이 있다.
Lisp/Clojure 개발의 핵심은 REPL 기반의 인터랙티브 개발이며,
코드를 실행 중인 시스템에 동적으로 로드하고 평가하는 것이 자연스러운 워크플로다.
이 동적성은 Go의 정적 컴파일 문화와 근본적으로 긴장 관계에 있다.
`gen-import-interop`이 코드 생성을 요구하는 것,
추가 패키지를 쓰려면 재컴파일이 필요하다는 것은 이 긴장의 산물이다.
Glojure가 인터랙티브 개발 경험을 제대로 제공하려면,
이 문화적 충돌을 어떻게 해소할지에 대한 명확한 답이 필요하다.

### Clojure 이식 프로젝트들의 반복되는 패턴과 생존 조건

역사적으로 Clojure를 다른 플랫폼에 이식하려는 시도는 여러 차례 있었다.
ClojureScript는 JavaScript를 타겟으로 삼아 성공했고,
ClojureCLR은 .NET을 타겟으로 삼았지만 주류에 못 미쳤다.
Babashka는 네이티브 이미지로 빠른 스타트업을 제공해 스크립팅 도구로 성공하고 있다.
이 중 성공한 사례들의 공통점은 명확한 킬러 use case가 있었다는 것이다 —
ClojureScript는 브라우저 Clojure, Babashka는 셸 스크립트 대체.

Glojure의 킬러 use case는 아직 명확하지 않다.
“Go interop”은 기능이지 use case가 아니다.
“Go 앱에 임베딩”은 잠재적 use case지만, 앞서 분석한 대로 경쟁이 치열하고 안정성 문제가 있다.
“Clojure로 Go 표준 라이브러리 접근”은 흥미롭지만 Clojure 인구가 좁다.
Glojure가 Babashka처럼 “이것이 있어서 X를 Clojure로 해결할 수 있게 됐다”는
명확한 포지션을 찾지 못하면, 기술적 완성도와 무관하게 틈새 프로젝트로 남을 가능성이 높다.
mark_l_watson도 이 비교를 직접 언급한다.
“Babashka처럼 빠른 스타트업 인터프리터 공간에서 좋은 추가 옵션이 될 수 있다”고 평가하며[^mark_l_watson],
Go 생태계에 “Lisp 생활 방식”을 가져온다는 점에서 의미가 있다고 보았다.
Babashka 비교는 Glojure가 직접 경쟁해야 할 지점인 동시에,
목표로 삼을 수 있는 성공 모델이기도 하다.

### 코드 생성 기반 interop이 암시하는 더 큰 문제

`gen-import-interop` 도구의 존재는 표면적으로 작은 구현 세부 사항처럼 보이지만,
실제로는 Glojure의 장기 유지보수 모델에 대한 근본적 질문을 던진다.

Go 생태계는 매우 빠르게 움직인다.
표준 라이브러리는 매 마이너 릴리스마다 새로운 패키지와 API가 추가된다.
현재 Glojure가 기본 제공하는 약 22개 표준 라이브러리 패키지는
전체 Go 표준 라이브러리의 일부분에 불과하다.
나머지 패키지를 쓰려면 사용자가 직접 코드 생성을 실행하고 재컴파일해야 한다.
이는 유지보수 부담이 Glojure 프로젝트 팀뿐 아니라 각 사용자에게도 전가된다는 의미다.
Go 1.x 마이너 업데이트가 나올 때마다 interop 레이어가 업데이트되어야 하고,
이 작업은 자동화되어 있지 않다.
소수 개발자가 관리하는 오픈소스 프로젝트(현재 GitHub 기여자 현황을 보면)에서
이 유지보수 부담이 지속 가능한지는 의문이다.

---

[^breadchris]: <https://news.ycombinator.com/item?id=42312972>
[^bbqfog]: <https://news.ycombinator.com/item?id=42312979>
[^throwaway894345]: <https://news.ycombinator.com/item?id=42318642>
[^zerr]: <https://news.ycombinator.com/item?id=42318800>
[^jfhamlin]: <https://news.ycombinator.com/item?id=42319185>
[^sesm]: <https://news.ycombinator.com/item?id=42320062>
[^mark_l_watson]: <https://news.ycombinator.com/item?id=42321076>
[^no_wizard]: <https://news.ycombinator.com/item?id=42315551>
