# T-Ruby: 타입을 코드 안에 쓰고 지워서 Ruby로 내보내는 TypeScript식 타입 계층

<https://type-ruby.github.io/>

<https://github.com/type-ruby/t-ruby>

HN 토론: <https://news.ycombinator.com/item?id=46395871> (178점, 149개 댓글)

## 소개

T-Ruby는 TypeScript에서 영감을 받은 Ruby용 타입 계층이다.
`trc`라는 실행 파일 하나로 배포되며,
타입 표기가 들어간 `.trb` 파일을 받아 평범한 `.rb` 파일로 컴파일한다.
타입은 컴파일 시점에 지워지므로 결과물은 Ruby가 도는 곳이면 어디서든 돌고,
런타임 비용이 없다.
동시에 Steep, Ruby LSP 같은 도구가 읽을 수 있는 `.rbs` 시그니처 파일도 만든다.

저장소는 2025년 12월 8일에 만들어졌고,
2026년 10월 현재 GitHub 별 약 270개, BSD 2-Clause 라이선스다.
README는 영어, 한국어, 일본어로 제공되고,
커밋 대부분은 한 명의 메인테이너(yhk1038, 137회)가 했다.
README 첫머리에 아직 실험적인 프로젝트라는 안내가 있고,
상태 절은 API가 바뀔 수 있으니 프로덕션에는 아직 권하지 않는다고 밝힌다.
마지막 릴리스는 2026년 1월 21일의 0.0.46이고,
마지막 커밋은 2026년 1월 23일이다.

### 기존 방식과의 차이

README는 Ruby 생태계의 두 기존 방식을 비교 대상으로 삼는다.
Sorbet은 `sig { params(name: String).returns(String) }`처럼
타입을 메서드 위에 주석처럼 쓰는 방식이라
JSDoc을 쓰고 IDE가 오류를 잡아 주길 바라는 느낌이라고 평한다.
RBS는 Ruby 공식 방식으로, TypeScript의 `.d.ts`처럼 별도 파일에 타입을 적지만
손으로 쓰거나 암묵적 추론 뒤 손으로 고쳐야 해서 번거롭다고 한다.
T-Ruby는 TypeScript처럼 타입을 코드 안에 두고,
`.trb` 하나에서 `.rb`와 `.rbs`를 함께 만들어 내는 쪽을 택했다.
Crystal 같은 새 언어는 엄밀히 말해 Ruby와 다른 언어이므로,
Ruby 생태계에서 벗어나는 것이 아니라 그 안에서 나아가고 싶다는 것이
README가 밝힌 동기다.

## 동작 방식

### 컴파일 파이프라인

로드맵 문서는 구조를 다음처럼 그린다.

```text
.trb → Parser Combinator → IR Builder → Optimizer → Code Generator → .rb + .rbs
                               ↓
                         Type Checker
                               ↓
                         SMT Solver
                               ↓
                         Diagnostics
```

파서 조합기(parser combinator)로 타입 문법을 읽고,
중간 표현(IR)을 만든 뒤 최적화를 거쳐 Ruby 코드와 RBS를 따로 생성한다.
타입 검사 쪽에는 SMT 기반 제약 해결기와 타입 추론 엔진이 붙어 있다.
변경 기록을 보면 0.0.39에서 TypeScript식 타입 추론 엔진이 들어왔다.
리터럴 타입 추론(`"hello"`는 `String`, `42`는 `Integer`),
메서드 호출 추적(`str.upcase`는 `String`),
마지막 식을 반환값으로 보는 암묵적 반환 처리,
`if`/`else` 분기에서 합집합 타입을 만드는 조건부 추론,
200개가 넘는 내장 메서드 타입이 그 내용이다.

### 타입을 지우는 규칙

핵심은 타입 정보를 지운 결과가 평범한 Ruby여야 한다는 점이다.
README의 예시에서 다음 `.trb`는

```ruby
# src/hello.trb
def greet(name: String): String
  "Hello, #{name}!"
end

puts greet("world")
```

`trc src/hello.trb`를 거쳐 `build/hello.rb`가 되고,
`ruby build/hello.rb`는 `Hello, world!`를 출력한다.
매개변수 타입과 반환 타입이 지워지고 `def greet(name)`만 남는 셈이다.

여기서 눈여겨볼 점은 `name: String`이 평범한 Ruby에서는
기본값이 `String` 클래스인 키워드 인자라는 것이다.
T-Ruby는 이 문법을 위치 매개변수의 타입 표기로 다시 해석한다.
그래서 진짜 키워드 인자는 다른 문법을 쓴다.
저장소의 키워드 인자 테스트를 보면
`def greet({ name: String }): String`이 `def greet(name:)`으로,
`def greet_with_prefix({ name: String, prefix: String = "Hello" }): String`이
`def greet_with_prefix(name:, prefix: "Hello")`로 컴파일된다.
`interface`로 정의한 묶음을
`def create_user({ name:, age: }: UserParams): String`처럼 참조하면
`def create_user(name:, age:)`가 된다.
중괄호로 감싼 구조분해 문법이 키워드 인자를 뜻하는 것이다.

이 문법은 처음부터 있던 것이 아니다.
2025년 12월 26일 HN에 T-Ruby가 올라왔을 때
jrochkind1은 키워드 인자를 쓰고 싶으면 어떻게 되느냐고 물었다.[^jrochkind1]
anamexis는 문서를 보면 T-Ruby에서는
모든 인자가 키워드 인자인 것 같다고 추측했고,[^anamexis]
Dan42는 플레이그라운드에서 `def greet(name: "someone")`처럼
기본값이 있는 키워드 인자를 넣어 보니
`"someone"`을 타입처럼 취급해 엉뚱하게 변환했다고 보고했다.[^Dan42]
ximus는 예시를 보자마자 떠오르는 의문인데
문서에 언급이 전혀 없다고 꼬집었다.[^ximus]
저장소 기록을 보면 중괄호 키워드 인자 문법은
그로부터 이틀 뒤인 12월 28일 커밋으로 들어왔다.

### 표현할 수 있는 타입

README가 꼽는 기능은 다음과 같다.

| 기능        | 예                                                |
| ----------- | ------------------------------------------------- |
| 타입 표기   | 매개변수와 반환 타입, 컴파일 시 지워짐            |
| 합집합 타입 | `String`, `Integer`, `nil` 중 하나를 뜻하는 타입  |
| 제네릭      | `User[]`, `Array<User>`, `Hash<String, Integer>`  |
| 인터페이스  | 객체 사이의 계약 정의                             |
| 타입 별칭   | `type UserID = Integer`                           |
| RBS 생성    | Steep, Ruby LSP, Sorbet과 연동                    |
| IDE 지원    | VS Code(Cursor 포함), JetBrains, Vim/Neovim용 LSP |
| 감시 모드   | 파일이 바뀌면 다시 컴파일                         |

합집합 타입은 TypeScript처럼 `String | Integer | nil`로 쓴다.

0.0.43에서는 `Integer[][]`, `String[]?`, `String?[]`,
`(String | Integer)[]` 같은 TypeScript식 배열 축약 문법이 들어왔다.
`String[]?`는 배열 자체가 `nil`일 수 있다는 뜻이고,
`String?[]`는 원소가 `nil`일 수 있다는 뜻이다.
0.0.44에서는 중간 파일 없이 `.trb`를 바로 실행하는 `trc run`이 추가되었다.

## 설정하기

```bash
gem install t-ruby
trc --version

# trbconfig.yml, src/, build/를 만든다
trc --init

trc src/hello.trb          # 컴파일
trc -w                     # trbconfig.yml의 경로를 감시 (기본 src/)
trc --emit-rbs src/        # .rbs만 생성
trc --check src/           # 컴파일 없이 타입 검사만
```

`trc --init`이 만드는 `trbconfig.yml`에서 결정해야 할 값은 다음과 같다.

```yaml
source:
  include:
    - src
  extensions:
    - ".trb"
    - ".rb"          # 기존 .rb 파일도 입력으로 받는다
output:
  ruby_dir: build
  # rbs_dir: sig     # .rbs를 따로 모으려면 지정한다
  preserve_structure: true
compiler:
  strictness: standard  # strict | standard | permissive
  generate_rbs: true
  target_ruby: "3.0"
  # checks:
  #   no_implicit_any: false
  #   strict_nil: false
watch:
  debounce: 100
  # on_success: "bundle exec rspec"  # 성공할 때마다 테스트를 돌린다
```

기존 프로젝트에 점진적으로 들이려면 `strictness: permissive`로 시작해
타입을 단 파일이 늘어나는 만큼 `standard`, `strict`로 올리는 순서가 자연스럽다.
`no_implicit_any`와 `strict_nil`은 TypeScript의
`noImplicitAny`, `strictNullChecks`에 대응하는 스위치로 보이며,
기본값은 꺼져 있다.
`rbs_dir`을 `sig`로 두면 Steep 같은 도구가 기대하는 위치에
시그니처를 모을 수 있다.

## 트레이드오프

### 코드 안의 타입은 Ruby 문법과 부딪힌다

T-Ruby의 장점은 타입이 코드 바로 옆에 있다는 것이다.
Sorbet의 `sig` 블록처럼 메서드와 시그니처가 떨어져 있지 않고,
RBS처럼 파일이 갈라지지도 않는다.
하지만 Ruby는 TypeScript가 JavaScript에 대해 누렸던 여유가 없다.
TypeScript는 JavaScript 문법에 비어 있던 자리에 `: Type`을 넣었지만,
Ruby에서 `name: String`은 이미 키워드 인자라는 뜻을 갖고 있다.

그래서 T-Ruby는 같은 표기를 다른 뜻으로 쓰고,
진짜 키워드 인자에는 `{ name: String }`이라는 새 문법을 만들었다.
이 결정은 `.trb` 파일이 더는 Ruby 문법으로 읽히지 않는다는 뜻이다.
Ruby 파서, RuboCop, 일반 Ruby 문법 강조는 `.trb`를 그대로 다룰 수 없고,
T-Ruby가 VS Code, JetBrains, Vim용 플러그인을 따로 제공하는 것도 그 때문이다.
TypeScript가 그랬듯 별도 언어로서의 생태계를 갖춰야 하는 길이다.

이것이 README가 말하는 생태계 안에서의 진보와
Crystal 같은 다른 언어 사이 어디쯤에 있는지는 분명히 해 둘 필요가 있다.
출력은 Ruby지만, 입력은 Ruby 도구가 읽을 수 없는 새 문법이다.
Sorbet과 RBS가 어색함을 감수한 이유가
바로 기존 Ruby 문법과 도구를 깨지 않기 위해서였다는 점을 생각하면,
T-Ruby의 선택은 그 비용을 반대쪽으로 옮긴 것이다.

HN에서 cpeterso는 RBS처럼 `def greet: (name: String) -> String`이라는
화살표 표기 선례가 있는데 왜 콜론으로 벗어났느냐고 물었다.[^cpeterso]
k1w1은 Rails 개발자 대부분이 프런트엔드에서 TypeScript를 쓰므로
같은 근육 기억을 쓸 수 있다는 점이 바로 이 프로젝트의 매력이라고 답했다.[^k1w1]
결국 T-Ruby는 Ruby 문법과의 정합성보다 TypeScript와의 친숙함을 택했고,
키워드 인자 문제는 그 선택의 직접적인 비용이다.
gls2ro는 Sorbet이 고유한 DSL을 배워야 한다는
T-Ruby 사이트의 비판에 반박했다.[^gls2ro]
Sorbet의 DSL은 평범한 Ruby라 다른 젬이 제공하는 메서드와 다르지 않으며,
어떤 타입 시스템이든 단순한 기본 타입을 넘어서면
결국 그 나름의 문법을 배워야 한다는 것이다.

### 타입을 지우면 실행 시점에는 아무것도 보장하지 않는다

타입을 지운다는 것은 런타임 비용이 없다는 뜻이지만,
동시에 런타임에 아무 검사도 하지 않는다는 뜻이다.
`.trb`로 쓴 코드를 일반 Ruby 코드나 외부 입력이 부를 때
타입이 틀린 값이 들어와도 아무 일도 일어나지 않는다.
TypeScript가 겪는 문제를 그대로 물려받는다.

Ruby에서는 이 문제가 더 크다.
Rails처럼 메타프로그래밍이 많은 코드는
정적 분석이 메서드의 존재 자체를 알기 어렵고,
대부분의 젬은 타입 정보가 없다.
`.rbs`를 내보내 기존 도구와 연동하는 설계는 이 간극을 메우려는 것이지만,
젬 쪽의 타입 정보가 부족하면 경계에서 `any`가 쏟아지는 상황은 피하기 어렵다.

Fire-Dragon-DoL은 `instance_variable_set`처럼
어디서든 인스턴스 변수를 바꿀 수 있는 Ruby에서는
인스턴스 변수에 대해 아무것도 확정할 수 없지 않느냐고 물었다.[^Fire-Dragon-DoL]
dudeinjapan은 Ruby에 타입이 필요한 이유로
YJIT와 ZJIT가 메서드의 타입 시그니처를 알 때
훨씬 잘 동작한다는 점을 들었다.[^dudeinjapan]
하지만 T-Ruby는 컴파일 시 타입을 지우므로
그 정보는 실행 시점의 JIT까지 전달되지 않는다.
타입을 지우는 설계는 런타임 비용을 없애는 대신
타입이 런타임에 줄 수 있는 이득도 함께 버린다.

### 한 사람이 끌고 가는 실험이다

T-Ruby는 2025년 12월에 시작해 두 달 만에 0.0.46까지 왔고,
SMT 해결기와 추론 엔진, 세 가지 IDE 플러그인까지 갖췄다.
속도는 인상적이지만 기여의 대부분이 한 사람에게서 나왔고,
2026년 1월 23일 이후 저장소에 커밋이 없다.
README 스스로 프로덕션 사용을 권하지 않는다.

HN 반응도 초기 프로젝트의 거친 면을 짚었다.
jhealy는 웹사이트는 매우 충실하지만
gem 다운로드가 약 1,500회에 불과하다고 적었고,[^jhealy]
omoikane는 플레이그라운드가 어떤 오류도 보고하지 않고
닫는 괄호 하나만 있는 파일도 받아들인다고 했다.[^omoikane]
jacobjuul은 문서에는 `trc watch`라고 되어 있지만 실제로는 `trc --watch`이고,
그마저도 아무것도 컴파일하지 않고 오류도 내지 않는다며
전부 AI로 만든 것이냐고 물었다.[^jacobjuul]
언어 확장은 한번 코드베이스에 들이면 빼기 어려운 종류의 의존이므로,
지금 단계에서는 컴파일 결과인 `.rb`를 저장소에 함께 두어
언제든 T-Ruby를 걷어 낼 수 있게 해 두는 것이 안전하다.

## 함정

- 버전 번호가 거꾸로 간다.
  변경 기록에는 2025년 12월 9일의 `0.1.0-alpha`가 가장 먼저 있고,
  그 뒤 릴리스는 0.0.39, 0.0.43, 0.0.44, 0.0.46이다.
  버전 비교로 최신 여부를 판단하는 도구는 혼동할 수 있다.
- 설정 파일 형식이 두 가지 보인다.
  README와 `trc --init`은 `source:`, `output:`, `compiler:` 구조를 쓰지만,
  저장소의 일부 E2E 테스트는 `emit:`, `paths:` 구조의 설정을 만든다.
  옛 예제를 그대로 옮기면 설정이 무시될 수 있다.
- 기본 입력 확장자에 `.rb`가 들어 있다.
  `name: String`의 의미가 Ruby와 다르므로,
  기존 `.rb` 파일 중 키워드 인자를 쓰는 파일이
  어떻게 해석되는지 직접 확인하고 나서 포함 범위를 정해야 한다.
- `examples/hello.trb`에는 타입 표기가 하나도 없다.
  타입 문법 예제는 README와 테스트 코드에서 찾아야 한다.

## 확인하기

키워드 인자 해석 차이는 다음 파일 하나로 확인할 수 있다.

```ruby
# src/kw.trb
def positional(name: String): String
  "Hello, #{name}!"
end

def keyword({ name: String, greeting: String = "Hi" }): String
  "#{greeting}, #{name}!"
end

puts positional("ada")
puts keyword(name: "ada")
```

```bash
trc src/kw.trb
cat build/kw.rb      # positional(name)과 keyword(name:, greeting: "Hi")를 확인한다
ruby build/kw.rb     # 기대 출력: Hello, ada! / Hi, ada!
cat build/kw.rbs     # 생성된 시그니처를 확인한다
```

## 체크리스트

- 컴파일된 `.rb`를 저장소에 함께 두어 T-Ruby 없이도 빌드할 수 있는가?
- 생성된 `.rbs`를 Steep나 Ruby LSP가 읽는 위치에 두었는가?
- `source.extensions`에 `.rb`를 남겨 둘지 확인했는가?
- 키워드 인자를 `{ ... }` 문법으로 썼는가?
- 외부 입력이 들어오는 경계에 런타임 검증을 따로 두었는가?
- 팀의 RuboCop과 에디터가 `.trb`를 다룰 수 있는가?

---

[^jrochkind1]: <https://news.ycombinator.com/item?id=46398481>

[^anamexis]: <https://news.ycombinator.com/item?id=46399630>

[^Dan42]: <https://news.ycombinator.com/item?id=46398978>

[^ximus]: <https://news.ycombinator.com/item?id=46399525>

[^cpeterso]: <https://news.ycombinator.com/item?id=46404246>

[^k1w1]: <https://news.ycombinator.com/item?id=46407086>

[^gls2ro]: <https://news.ycombinator.com/item?id=46399568>

[^Fire-Dragon-DoL]: <https://news.ycombinator.com/item?id=46401915>

[^dudeinjapan]: <https://news.ycombinator.com/item?id=46399933>

[^jhealy]: <https://news.ycombinator.com/item?id=46398555>

[^omoikane]: <https://news.ycombinator.com/item?id=46398758>

[^jacobjuul]: <https://news.ycombinator.com/item?id=46553614>
