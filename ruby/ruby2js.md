# Ruby2JS: an extensible Ruby to modern JavaScript transpiler

<https://www.ruby2js.com/>

<https://github.com/ruby2js/ruby2js>

HN 토론: <https://news.ycombinator.com/item?id=46465467> (2점, 0개 댓글)

## 소개

Ruby2JS는 README의 표현으로 최소한이지만 확장 가능한
Ruby에서 JavaScript로의 변환기다.
저장소는 2013년 10월에 만들어졌고,
2026년 10월 현재 GitHub 별 약 490개, MIT 라이선스다.
README의 저작권 표기에는 Macario Ortega, Sam Ruby, Jared White가 올라 있고,
최근 커밋은 대부분 Sam Ruby가 하고 있다.
마지막 gem 릴리스는 2024년 5월의 5.1.2이지만,
2026년 4월까지 저장소에 커밋이 계속 들어왔다.

목표는 Opal과 정반대다.
Opal이 Ruby 의미론을 지키는 런타임을 함께 싣는다면,
Ruby2JS는 런타임 없이 사람이 쓴 것처럼 보이는 JavaScript를 만든다.
문서의 도구 선택 안내는 풍부한 Ruby 런타임과 잘 검증된 프레임워크로
일을 끝내고 싶다면 Opal을 쓰고,
기계가 만든 것처럼 보이지 않는 JavaScript를 원하면 Ruby2JS를 쓰라고 정리한다.
그리고 진짜 답은 CoffeeScript일 수도 있다는 농담을 덧붙인다.

README의 예시가 그 성격을 잘 보여 준다.

```ruby
a = { age: 3 }            # let a = {age: 3}
a.age += 1                # a.age++
items.map { |x| x * 2 }   # items.map(x => x * 2)
class Dog < Animal        # class Dog extends Animal {
  def bark                #   bark() {
    puts "woof!"          #     console.log("woof!")
  end                     #   }
end                       # }
```

`a.age`가 해시 접근이 아니라 JavaScript 속성 접근으로,
`puts`가 `console.log`로 바뀐다.
Ruby 코드처럼 보이지만 실제로는 Ruby 문법으로 쓴 JavaScript에 가깝다.

## 동작 방식

### 브라우저에서 Ruby를 돌리는 세 가지 길

설계 철학 문서는 브라우저에서 Ruby를 돌리는 방법을 셋으로 나눈다.

| 방식      | 원리                                 | 얻는 것                                            | 잃는 것                                                        |
| --------- | ------------------------------------ | -------------------------------------------------- | -------------------------------------------------------------- |
| Opal      | 포괄적인 런타임과 함께 컴파일        | 높은 Ruby 호환성, 음수 인덱스와 참거짓 의미론 유지 | 큰 런타임, 읽기 어려운 출력, 일부 JavaScript 프레임워크와 충돌 |
| ruby.wasm | Ruby 인터프리터를 WebAssembly로 실행 | 완전한 호환성, 표준 라이브러리, 기존 코드 그대로   | 20~40MB 다운로드, 느린 시작, 명시적 연동 필요                  |
| Ruby2JS   | 빌드 시점의 정적 AST 변환            | 작은 출력, 읽기 쉬운 코드, JavaScript 원래 속도    | 동적 기능 불가, 참거짓과 음수 인덱스 등 의미 차이              |

Ruby2JS를 고르면 기본적으로 JavaScript 의미론을 받아들이게 된다.
`a[-1]`은 마지막 원소가 아니라 `undefined`이고,
`0 || 1`은 Ruby에서는 `0`이지만 JavaScript에서는 `1`이다.
`method_missing`, `define_method`, `eval`은
임의의 메서드 호출을 가로채는 런타임이 있어야 하므로 아예 변환할 수 없다.

### Ruby다움을 단계적으로 고르는 장치

대신 Ruby에 가까운 동작이 필요한 만큼만 고를 수 있는 장치가 층층이 있다.

- 필터(filter)는 변환 시점에 Ruby 메서드를 JavaScript 대응물로 바꾼다.
  `functions` 필터를 쓰면 `arr.first`는 `arr[0]`,
  `arr.empty?`는 `arr.length === 0`,
  `str.gsub(/a/, 'b')`는 `str.replace(/a/g, 'b')`가 된다.
- 폴리필(polyfill)은 런타임에 JavaScript 프로토타입에 Ruby 메서드를 더한다.
- 프래그마(pragma)는 `# Pragma: ??`처럼 줄 단위 주석으로 변환을 지시한다.
- `or: :nullish`, `truthy: :ruby` 같은 옵션은 동작을 전역으로 바꾼다.

이름 규칙도 기계적으로 처리한다.
`empty?`, `chomp!`의 `?`와 `!`는 떼어 내고,
`const`, `new`처럼 JavaScript 예약어인 이름에는 `$`를 붙인다.
기존 클래스를 확장할 때는 `class String # Pragma: extend`처럼 표시한다.
Ruby에서는 주석이라 무시되므로 같은 파일이 양쪽에서 돈다.

### 기본값의 변화

변경 기록의 미배포 항목을 보면 기본 ES 수준이 ES5에서 ES2020으로 올라갔고,
프리셋은 ES2021에서 ES2022로 올라갔다.
Ruby의 `||`는 새 `or` 옵션의 기본값 `:auto`에 따라
불리언 문맥에서는 `||`로, 값 문맥에서는 `??`로 바뀐다.
조건문은 자연스럽게 동작하면서 할당에서는 `0`과 `""`을 지키려는 절충이다.
2023년의 5.1.0에서는 유지보수를 위해 많은 필터와 기능을 폐기했고,
Vite와 Rollup 패키지는 새 메인테이너를 찾는다고 공지했었다.

## 사용하기

```bash
gem install ruby2js
# --preset은 자주 쓰는 필터, ES2022, 일치 비교(===)를 한꺼번에 켠다
echo "puts 'hello'" | ruby2js --preset
```

Ruby 코드 안에서는 `Ruby2JS.convert`를 부른다.

```ruby
require 'ruby2js'

# 프리셋으로 변환한다
puts Ruby2JS.convert("a = {age: 3}; a.age += 1", preset: true)
# => let a = {age: 3}; a.age++

# 필요한 필터만 골라 쓸 수도 있다
puts Ruby2JS.convert('"2A".to_i(16)', filters: [:functions])

# == 를 === 로 바꾼다
puts Ruby2JS.convert('a==1', comparison: :identity)
```

esbuild, Vite, webpack, Rollup용 플러그인과
Astro, Nuxt, Svelte, Rails 연동 패키지가 저장소의 `packages/` 아래에 있다.

## 자기 자신과 Rails까지 옮기기

### 셀프호스팅

Ruby2JS는 자기 자신을 JavaScript로 변환한다.
README에 따르면 Opal로 컴파일한 데모는 약 5MB이고,
Ruby2JS가 스스로를 변환한 셀프호스트 데모는
약 200KB에 Prism WASM을 더한 크기다.
설계 문서는 변환기, 워커, 런타임을 합친 출력을 약 460KB로 적는다.
같은 기능을 두 방식으로 만든 결과물의 크기 차이가
두 도구의 철학 차이를 그대로 보여 준다.

셀프호스트 작업 안내는 Ruby 스펙도 함께 변환해
JavaScript 변환기에 돌린다고 설명한다.
스펙은 반드시 통과해야 하는 `ready`,
작업 중인 `partial`, 의존이 풀리길 기다리는 `blocked`로 관리된다.
Ruby와 JavaScript 양쪽에서 돌아야 하는 코드에서는
`arg.is_a?(Range)` 대신 `arg.respond_to?(:begin)`처럼
양쪽 모두에서 의미가 맞는 표현을 골라 써야 한다는 예도 나온다.

### Juntos와 VISION 문서

최근 저장소의 중심은 Juntos다.
Juntos는 Rails 호환 프레임워크를
JavaScript 런타임에 구현하는 Ruby2JS 필터 묶음으로,
모델, 컨트롤러, 뷰, 라우트를 Ruby로 쓰고
엣지(Cloudflare Workers, Vercel Edge, Deno Deploy),
브라우저(IndexedDB, SQLite/WASM), 서버(Node.js, Bun, Deno),
모바일(Capacitor), 데스크톱(Electron, Tauri)에 배포하는 것을 목표로 한다.

핵심 발상은 Rails의 메타프로그래밍을 뒤집는 것이다.
Rails는 `has_many :comments`를 보고 실행 시점에 메서드를 만들지만,
Juntos는 Rails DSL이 유한하고 선언적이라는 점에 기대
그 메서드를 변환 시점에 미리 계산해 ES2022 클래스로 내놓는다.
문서는 생성 코드의 약 95%가 애플리케이션이고
약 5%가 프레임워크 접착 코드라고 말한다.

`VISION.md`는 이 방향을 세 가지 명제로 정리한다.
Ruby의 유용한 부분집합은 JavaScript로 깨끗하게 옮겨지고,
잘 짜인 ERB의 부분집합은 JSX로 옮겨지며,
Rails MVC와 단일 파일 컴포넌트는 포장만 다른 같은 개념이라는 것이다.
그리고 모든 것이 기계적 변환으로 귀결된다는 결론을 내린다.
출력은 읽을 수 있고, 변환기 없이 고칠 수 있으며,
런타임에 Ruby 의존이 없어야 한다는 탈출 시험(eject test)도 제시한다.

## 트레이드오프

### 읽을 수 있는 출력은 Ruby 의미론을 포기한 대가다

Ruby2JS의 가장 큰 장점인 깔끔한 출력은
`a + 1`을 그대로 `a + 1`로 내보낼 수 있기 때문에 가능하다.
그러려면 `+`가 숫자 덧셈이라고 믿어야 하고,
누군가 `+`를 재정의했을 가능성을 무시해야 한다.
Ruby2JS는 그 가능성을 정면으로 무시하는 쪽을 택했다.

그 결과 겉보기에는 같은 Ruby 코드가 Ruby와 JavaScript에서 다르게 동작한다.
`0`과 빈 문자열의 참거짓, 음수 인덱스, 정수 나눗셈이 대표적이다.
옵션과 필터로 일부를 되돌릴 수 있지만,
되돌릴수록 출력은 Opal처럼 런타임 함수 호출로 채워지거나
폴리필에 기대게 된다.
즉 Ruby2JS에서 Ruby 호환성을 높이는 것은
Opal 쪽으로 한 걸음씩 다가가는 일이다.

어려움은 이 차이가 어디서 문제가 될지 미리 알 수 없다는 점이다.
변환은 오류 없이 끝나고, 생성된 코드는 그럴듯해 보인다.
차이는 실행 결과에서만 드러나므로,
양쪽에서 같은 결과를 내야 하는 코드라면
양쪽에서 같은 테스트를 돌리는 수밖에 없다.
셀프호스트가 Ruby 스펙을 함께 변환해 돌리는 이유도 여기에 있다.

### 정적 변환은 Rails의 핵심을 미리 펼쳐야 한다

Juntos의 발상은 매력적이지만 무거운 전제에 기댄다.
Rails DSL이 유한하다는 전제다.
`has_many`, `validates`, `before_save`처럼 이름이 정해진 선언은
필터가 하나씩 알아보고 펼칠 수 있다.
하지만 실제 Rails 앱은 concern, 젬이 추가하는 DSL,
애플리케이션이 직접 만든 매크로를 함께 쓴다.

필터가 모르는 선언을 만나면 정적 변환은 할 수 있는 일이 없다.
런타임 메타프로그래밍을 금지한 이상,
Rails 호환성은 필터가 아는 DSL의 범위로 정해진다.
Rails 문서가 대부분 그대로 적용된다는 Juntos의 약속은
그 범위 안의 앱에서만 성립한다.

### 탈출 가능성과 선택 가능성은 함께 가질 수 없다

`VISION.md`가 스스로 인정하듯,
생성된 `dist/`를 가져가 순수 JavaScript로 계속 개발할 수는 있지만
그 순간 같은 소스를 여러 런타임에 배포하는 능력을 잃는다.
소스를 유지하는 것이 선택지를 유지하는 것이라는 문장은
반대로 말하면 Ruby2JS를 떠나는 비용이 선택지를 버리는 것이라는 뜻이다.

이 긴장은 팀 구성에서 드러난다.
JavaScript 개발자가 생성 코드를 고치기 시작하면
그 수정은 다음 변환에서 사라지거나 소스와 어긋난다.
읽을 수 있는 출력은 디버깅을 돕지만,
출력을 고칠 수 있다는 착각도 함께 준다.
셀프호스트 안내가 생성된 파일을 절대 고치지 말라고 강조하는 것도
같은 이유다.

## 함정

- 문서와 저장소의 상태가 다르다.
  배포된 gem은 2024년 5월의 5.1.2인데,
  ES2020 기본값, `or: :auto`, ES2022 프리셋은 변경 기록의 미배포 항목에만 있다.
  저장소 문서를 보고 gem의 동작을 예상하면 어긋날 수 있다.
- 5.1.0에서 많은 필터가 폐기되었으므로,
  옛 블로그 글의 예제가 지금 그대로 동작한다고 기대하면 안 된다.
- `?`와 `!` 접미사를 떼어 내므로
  `empty?`와 `empty`처럼 접미사만 다른 두 메서드가 같은 이름으로 합쳐진다.
- 비교 연산은 옵션에 따라 `==` 또는 `===`가 되므로,
  같은 코드라도 설정이 다르면 결과가 달라질 수 있다.
- 잘못 짜인 ERB, 즉 조건문이 태그 일부만 감싸는 템플릿은 JSX로 옮길 수 없다.

## 체크리스트

- 공유 코드가 `method_missing`, `define_method`, `eval`을 쓰지 않는가?
- 참거짓 판단에서 `0`이나 빈 문자열이 나올 수 있는 곳을 확인했는가?
- 음수 인덱스로 배열에 접근하는 곳이 없는가?
- 같은 코드를 Ruby와 JavaScript 양쪽에서 같은 테스트로 돌리는가?
- 쓰려는 옵션이 배포된 gem 버전에 실제로 들어 있는가?
- 생성된 JavaScript를 직접 고치지 않고 소스에서만 고치는가?
