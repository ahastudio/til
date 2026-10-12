# Opal: Ruby ♥︎ JavaScript

<https://opalrb.com/>

<https://github.com/opal/opal>

HN 토론: <https://news.ycombinator.com/item?id=4674315> (130점, 49개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=7851625> (67점, 67개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/t6ooet/opal_ruby_javascript_compiler> (7점, 6개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/uaxeaw/opal_ruby_javascript_source_source> (6점, 2개 댓글)

GN 토론: <https://news.hada.io/topic?id=3770>

## 소개

Opal은 Ruby 코드를 JavaScript 코드로 옮기는 소스 대 소스 컴파일러이며,
Ruby의 corelib와 stdlib 구현을 함께 제공한다.
README는 Ruby로 쓰고 JavaScript가 도는 곳이면 어디서든 실행하라고 소개하며,
그 대상으로 브라우저, Node.js, Deno, Bun, QuickJS를 든다.
저장소는 2009년 4월에 만들어졌고,
2026년 10월 현재 GitHub 별 약 4,900개, MIT 라이선스다.

README가 내세우는 특징은 다섯 가지다.
첫째, 자체 corelib와 stdlib을 갖춘 실제 Ruby 구현이며
CRuby가 쓰는 것과 같은 테스트 모음인 ruby/spec으로 검증한다.
둘째, 실행 시점의 인터프리터 없이 미리 평범한 JavaScript로 컴파일하므로
내려받을 VM도, 런타임 인터프리터 루프도 없다.
셋째, Ruby에서 JavaScript를 부르고 JavaScript에서 Ruby를 부르는
양방향 연동을 지원한다.
넷째, 같은 gem과 같은 객체와 같은 스펙을 서버와 클라이언트에서 함께 쓸 수 있다.
다섯째, 컴파일러가 Ruby로 쓰여 있어 `opal-parser.js`로 스스로를 컴파일하고,
그래서 브라우저 안에서도 돈다.

### 버전 상황

배포된 최신 gem은 1.8 계열이다.
GitHub 릴리스 기준으로 1.8.0이 2023년 10월, 1.8.2가 2023년 11월,
1.8.3이 2026년 5월에 나왔다.
`master` 브랜치는 아직 배포되지 않은 `2.0.0dev`이고,
2026년 9월에도 커밋이 이어지고 있다.
2.0은 컴파일 결과와 런타임이 ES2021을 지원하는 엔진을 전제하며,
그보다 오래된 엔진을 지원해야 한다면 1.x에 머물라고 README가 안내한다.
Internet Explorer는 지원하지 않는다.

## 동작 방식

### 컴파일러와 런타임은 다른 곳에서 돈다

저장소는 세 부분으로 나뉜다.
`lib/`은 파서와 컴파일러로, 개발자의 Ruby 환경에서 돌고
브라우저용 `opal-parser.js`로도 빌드된다.
`opal/`은 Ruby와 JavaScript로 쓴 런타임과 corelib로, JavaScript 환경에서 돈다.
`stdlib/`은 `StringScanner`, `Date`, `Observable` 같은 Ruby stdlib 구현으로,
선택적으로 JavaScript 환경에 포함된다.

즉 Opal로 만든 결과물은 컴파일된 애플리케이션 코드만이 아니라
Ruby 의미론을 흉내 내는 런타임까지 함께 실어 보낸다.
`Opal.compile`이 돌려주는 문자열은 그 자체로는 실행할 수 없고,
런타임과 corelib이 먼저 로드되어 있어야 한다.
CLI로 컴파일하면 런타임이 기본으로 포함되며, `--no-opal`로 뺄 수 있다.

### Ruby 의미론을 JavaScript 위에 얹는 대가

Opal은 성능과 런타임 단순성을 위해 Ruby의 몇 가지 성질을 포기한다.
미지원 기능 문서가 밝히는 차이는 다음과 같다.

| 항목                   | Opal의 동작                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------------- |
| 문자열                 | 모두 불변이다. `#<<`, `#gsub!` 같은 파괴적 메서드가 없고, Symbol과 String이 구별되지 않는다 |
| 정규식                 | JavaScript 정규식을 쓴다. `\A`, `\z` 일부는 번역하지만 `^`, `$`의 줄바꿈 처리 등이 다르다   |
| 정수와 실수            | 둘 다 JavaScript 숫자인 `Number` 하나다. `1 / 4`는 `0.25`, `4.0 / 2`는 `2`다                |
| 인코딩                 | 아주 작은 구현만 있다                                                                       |
| 스레드                 | 호환용 자리표시 `Thread` 클래스만 있고 기능은 없다                                          |
| `private`, `protected` | 모든 메서드가 `public`이며, `Module#private`과 `Module#protected`는 아무 일도 하지 않는다   |

이 표는 Opal을 쓸 때 무엇이 Ruby와 같은지보다
무엇이 다른지를 먼저 알려 준다.
정수 나눗셈과 문자열 변경은 평범한 Ruby 코드에 흔히 나오므로,
서버와 클라이언트가 같은 코드를 공유한다는 약속은
이 차이를 피한 코드에 대해서만 성립한다.

### JavaScript와 만나는 두 가지 길

가장 직접적인 길은 백틱이나 `%x{}` 안에 JavaScript를 그대로 쓰는 것이다.
1.8.0부터 이 방식에는 파일 첫머리에 `# backtick_javascript: true`
매직 주석을 달라는 경고가 붙는다.
Ruby에서 백틱은 원래 셸 명령 실행이므로,
의도를 명시하지 않으면 2.0에서 깨질 것이라는 경고다.

다른 길은 `Native` 모듈이다.
`require 'native'` 뒤에 `$$` 또는 `$global`로 전역 객체를 잡고,
`win[:location][:href]`처럼 속성을 읽고 쓰며,
JavaScript 객체에 Ruby 메서드를 정의할 수도 있다.
연산자 수준의 `typeof`, `instanceof`, `new` 같은 기능은
1.x의 `JS` 모듈에서 2.0의 `Opal::Raw`로 이름이 바뀌었다.

## 사용하기

### 설치

gemspec은 Ruby 2.3 이상을 선언하지만,
CI가 Ruby 3.0부터 4.0과 JRuby를 검사하므로 3.x 이상이 현실적인 선택이다.

```bash
gem install opal
opal -v
# Ruby를 컴파일해 Node.js에서 실행한다
opal -e "puts 'Hello from Opal'"
```

아직 배포되지 않은 2.0을 따라가려면 `Gemfile`에서 저장소를 직접 가리킨다.

```ruby
gem 'opal', github: 'opal/opal'
```

### CLI로 컴파일해 브라우저에서 실행

```bash
echo "puts 'Hello world!'" > app.rb
# 런타임이 기본으로 포함된다. 빼려면 --no-opal
opal --compile app.rb > app.js
```

페이지 인코딩은 반드시 UTF-8이어야 한다.
Opal의 문자열 처리가 그 전제에 기대기 때문이다.

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="app.js"></script>
  </head>
  <body></body>
</html>
```

### Ruby 코드 안에서 빌드

`Opal::Builder`는 `require` 의존을 따라가며 앱 전체를 한 파일로 만든다.

```ruby
require 'opal'

builder = Opal::Builder.new
builder.build_str('require "opal"; puts "wow"', '(inline)')
# 바이너리 모드로 써야 한다
File.binwrite 'app.js', builder.to_s
```

HTML에서 `opal-parser.js`를 불러 `<script type="text/ruby">`를
바로 실행하는 방법도 있지만,
README는 이것이 컴파일러를 클라이언트로 보내는 방식이라
맛보기용이지 배포용이 아니라고 분명히 적어 둔다.

Rails, Sinatra, Roda, 정적 앱용 연동 안내도 저장소 문서에 따로 있다.

## 1.x에서 2.0으로

마이그레이션 가이드는 1.8.1에서 2.0 사이의 변경을
호환 장치가 없는 강한 변경과,
경고와 함께 옛 코드가 계속 도는 약한 변경으로 나눈다.
업그레이드 전에 `Opal.raise_on_deprecation = true`로
Ruby 쪽 폐기 경고를 예외로 바꿔 두라고 권한다.

### 경고 없이 깨지는 것

가장 위험한 변경은 ECMAScript 대상이 ES3에서 ES2021로 올라간 것이다.
가이드는 이 변경에 경고가 전혀 없다고 강조한다.
임베디드 엔진, 오래된 JVM 엔진, IE처럼
2021년 이전 엔진에서는 2.0 결과물이 돌지 않으며,
트랜스파일 단계도 따로 제공하지 않는다.
Nashorn 러너와 `require 'nashorn'`이 사라진 것도 같은 이유다.
특히 `OPAL_PLATFORM == 'nashorn'` 분기는 오류 없이 브라우저 기본값으로 빠진다.

corelib 동작 수정도 경고 없이 결과를 바꾼다.
몇 가지만 추리면 다음과 같다.

| 변경                            | 결과                                                       |
| ------------------------------- | ---------------------------------------------------------- |
| 빈 컬렉션의 `Enumerable#first`  | 이제 `nil`을 돌려준다                                      |
| `String#strip` 계열             | NBSP 처리가 MRI와 같아져 결과 문자열이 달라질 수 있다      |
| 생성되는 JavaScript `RegExp`    | 항상 `u` 플래그가 붙어 기존 정규식이 다르게 일치할 수 있다 |
| `#hash`                         | 1.x와 값이 다르다. 버전을 넘어 저장하면 안 된다            |
| 문자열 보간                     | 얼리지 않은 String을 돌려준다                              |
| `Array#compact`, `Hash#compact` | JavaScript `null`과 `undefined`도 제거한다                 |

### 이름이 바뀐 것

`Opal::Builder#preload`와 `#prerequired`는 사라졌고
`build_require`와 `stubs`로 대체된다.
흥미롭게도 CLI의 `-p`, `--preload` 플래그는 그대로 남아
내부에서 `build_require`를 부른다.
`opal/builder_processors` 같은 경로와 상수는 `Opal::Builder` 아래로 옮겨졌고,
별칭은 남기지 않았다.
런타임은 단일 파일 `opal/corelib/runtime.js`에서
`opal/runtime/` 아래 여러 모듈로 쪼개졌으므로,
`require`는 그대로 되지만 파일 경로를 직접 가리키던 빌드 스크립트는 깨진다.

`JS` 모듈과 `JS::Error`는 `Opal::Raw`와 `Opal::Raw::Error`로 바뀌었다.
2.0에서는 호환 장치가 남아 경고만 내고,
실제 제거는 2.1로 예정되어 있다.

### 새로 생긴 것

2.0에는 실험적 죽은 코드 제거(`--dce`),
단독 실행 파일 생성(`--compile-to-exe`),
디렉터리 단위 빌드(`--directory`),
async/await 지원(`--await`),
`Opalfile` DSL, Bun과 Deno 러너,
스레드 빌드 스케줄러와 JRuby, TruffleRuby 지원이 들어간다.

## 트레이드오프

### Ruby다움과 JavaScript 성능은 한쪽을 양보해야 한다

Opal의 설계는 일관되게 Ruby 의미론의 일부를 내주고
JavaScript 성능과 단순성을 얻는 쪽을 택했다.
문자열을 불변으로 두면 JavaScript 문자열을 그대로 쓸 수 있고,
정수와 실수를 하나로 합치면 JavaScript 숫자를 그대로 쓸 수 있으며,
`private`을 무시하면 메서드 호출마다 가시성을 검사하지 않아도 된다.

반대로 이 차이를 메우려 하면 비용이 급격히 커진다.
정규식이 대표적이다.
문서는 Ruby 정규식을 완전히 지원하려면
Ruby의 정규식 엔진 전체를 컴파일해 넣어야 하는데
현재로서는 현실적이지 않다고 적는다.
정수 나눗셈을 지키려면 모든 `/` 연산을 런타임 함수 호출로 바꿔야 하고,
가변 문자열을 지키려면 모든 문자열을 래퍼 객체로 감싸야 한다.
어느 쪽이든 생성 코드가 느려지고 JavaScript 쪽에서 다루기 어려워진다.

이 비용이 얼마나 큰지는 2014년 HN 스레드에서 구체적인 숫자로 나왔다.
Dart 팀의 munificent는 Opal 0.6.2가 `a = a + 1`을
JavaScript의 덧셈이 아니라
`a['$+'](1)`이라는 메서드 호출로 컴파일한다는 점을 보이고,
1,000만 번 반복하는 루프가
순수 JavaScript보다 264배 느렸다고 측정했다.[^munificent]
그는 Ruby의 산술 의미론을 지키려면 메서드 호출이 필요하고,
숫자임이 확실한 곳에서만 JavaScript 연산자로 내리려면 타입 분석이 필요하며,
정적 타입이 없는 언어에서 그 분석을 제대로 하려면
프로그램 전체 분석이 필요하다고 설명했다.
dart2js가 무겁고 복잡한 이유가 바로 그것이라는 것이다.
azakai는 C로 쓴 Ruby VM 자체를 JavaScript로 컴파일하면
264배가 아니라 2배 정도 느린 수준을
적은 노력으로 얻을 수 있다고 반박했다.[^azakai]
그보다 앞선 2012년 스레드에서 btilly는 Ruby에서 2의 100제곱은 정확한 정수지만
JavaScript에서는 부정확한 부동소수점이 된다며,
Ruby 숫자 의미론을 지키려면 기본 산술을 쓸 수 없다고 짚었다.[^btilly]
Opal은 결국 정수와 실수를 합치는 쪽을 택했고,
지금의 미지원 기능 문서는 그 선택의 결과다.

해시도 같은 길을 걸었다.
2012년에 vjeux는 Opal의 해시가 JavaScript 객체 위에 만들어져
`h['0']`과 `h[0]`이 같은 키로 합쳐진다고 지적했다.[^vjeux]
2.0 마이그레이션 가이드에 따르면 지금은 `Opal.hash2`도 `Map`을 만들고
`compare_by_identity` 해시의 문자열 키를 구별하는 수정이
2026년 9월에도 들어가고 있다.
JavaScript 엔진이 `Map` 같은 기본 자료구조를 갖추면서
예전에는 포기해야 했던 Ruby 의미론 일부를 다시 되찾고 있는 셈이다.

그래서 남는 어려움은 이 차이가 조용히 드러난다는 점이다.
`1 / 4`가 `0`이 아니라 `0.25`가 되어도 예외는 나지 않는다.
서버와 클라이언트에서 같은 코드를 돌릴 때
가장 먼저 의심해야 할 것이 바로 이런 산술과 문자열 변경 지점이다.

### 런타임을 싣는 대가로 Ruby를 얻는다

인터프리터는 없지만 corelib을 포함한 런타임은 반드시 따라간다.
아주 작은 위젯 하나를 위해 Opal을 쓰면
애플리케이션 코드보다 런타임이 훨씬 커질 수 있다.
2.0의 `--dce`가 실험 기능으로 들어간 것도
이 크기를 줄이려는 시도로 읽힌다.

이 비용은 Ruby 의미론을 얼마나 지키느냐와 직결된다.
런타임이 클수록 메서드 디스패치, `method_missing`, 모듈 믹스인 같은
Ruby다운 기능이 더 정확해지고,
런타임을 줄일수록 생성 코드는 평범한 JavaScript에 가까워지지만
Ruby 라이브러리를 그대로 가져다 쓰기는 어려워진다.
같은 문제를 반대쪽에서 푼 도구가 Ruby2JS다.

런타임이 무겁다는 것과 디버깅이 어렵다는 것은 다른 문제다.
2012년 스레드에서 jonny_eh는 생성된 JavaScript가 너무 복잡해서
CoffeeScript와 달리 디버깅이 두렵다고 했고,[^jonny_eh]
wtetzner는 CoffeeScript는 JavaScript 의미론을 그대로 쓰도록 설계되었지만
Ruby는 의미론이 달라 일대일 대응이 불가능하다고 답했다.[^wtetzner]
2014년 스레드에서 Opal 개발자 adambeynon은
Chrome 개발자 도구와 소스 맵만으로 디버깅하며,
변수와 인스턴스 변수가 Ruby 이름 그대로 컴파일되므로
생성된 JavaScript를 직접 볼 일은
Opal 런타임 자체의 버그를 잡을 때뿐이라고 설명했다.[^adambeynon]

동적 기능의 지원 범위는 Opal이 앞선 시도들과 갈라진 지점이기도 하다.
DanielRibeiro는 2012년에 HotRuby, ColdRuby, RubyJS 같은
앞선 Ruby-JavaScript 변환기들을 나열하며
그 어느 것도 `method_missing` 같은 동적 기능을 다루지 못해
기존 Ruby 코드를 브라우저에서 재사용하기 어려웠다고 지적했다.[^DanielRibeiro]
adambeynon은 Opal이 `method_missing`을 지원하되
기본으로는 꺼 두고 선택해서 켜게 한다고 답했다.[^adambeynon-mm]
런타임 크기와 동적 기능 사이의 저울질이 처음부터 설계에 들어 있었던 것이다.

문법도 처음부터 벽이었다.
2012년 Lobste.rs 스레드에서 한 사용자는 처음 시도한 코드부터 Opal에서 깨졌고,
이슈 트래커에 블록처럼 미구현이거나 부실한 기능이 많다며
Ruby를 구현하기까지 갈 길이 멀다고 적었다.[^inactive-user]
steveklabnik은 Ruby 문법을 직접 다시 구현하려 하면
고생할 것이라고 답했고,[^steveklabnik]
같은 사용자는 검증된 방법이 두 가지뿐이라고 덧붙였다.[^inactive-user-grammar]
`parse.y`의 렉서 상태를 그대로 흉내 내거나,
일반화된 파서(GLR)로 모호한 트리를 만든 뒤 나중에 풀어내는 것이다.
Ruby 문법은 모호한 곳이 있어서
렉서와 파서 중 어느 한쪽이 그 모호함을 떠안아야 하기 때문이다.
지금의 Opal이 ruby/spec으로 검증한다고 내세울 수 있게 된 것은
그 긴 작업을 거친 결과다.

## 함정

- 업그레이드 경고가 서로 다른 경로로 나온다.
  `Opal.hash2` 같은 런타임 경고는 JavaScript `console.warn`으로 나오므로
  `Opal.raise_on_deprecation`으로 잡히지 않는다.
- 폐기 경고 문구를 일정표로 읽으면 안 된다.
  백틱 경고와 `Opal.hash2` 경고는 2.0에서 깨지거나 제거된다고 말하지만,
  `2.0.0dev` 시점에도 실제로는 아직 동작한다고 가이드가 직접 밝힌다.
- `#hash` 값이 버전마다 달라지므로,
  해시 값을 저장소나 캐시 키로 남겨 두는 코드는 업그레이드 때 조용히 깨진다.
- `opal-parser.js`로 브라우저에서 Ruby를 바로 실행하는 데모는
  컴파일러 전체를 클라이언트로 보내는 구조라 프로덕션에 그대로 옮기면 안 된다.
- `Builder#to_s`를 텍스트 모드로 쓰면 인코딩이 꼬일 수 있으므로
  README대로 `File.binwrite`를 쓴다.

## 체크리스트

- 배포 대상 엔진이 ES2021을 지원하는가?
- 공유 코드에서 정수 나눗셈 결과에 기대는 곳이 없는가?
- 공유 코드에서 `<<`, `gsub!` 같은 파괴적 문자열 메서드를 쓰지 않는가?
- JavaScript를 넣은 파일마다 `# backtick_javascript: true`가 있는가?
- `JS`와 `JS::Error`를 `Opal::Raw`와 `Opal::Raw::Error`로 바꿨는가?
- HTML 페이지의 문자 인코딩이 UTF-8인가?
- 업그레이드 뒤 테스트 모음을 다시 돌렸는가?

---

[^munificent]: <https://news.ycombinator.com/item?id=7852821>

[^azakai]: <https://news.ycombinator.com/item?id=7853605>

[^btilly]: <https://news.ycombinator.com/item?id=4675378>

[^vjeux]: <https://news.ycombinator.com/item?id=4676452>

[^jonny_eh]: <https://news.ycombinator.com/item?id=4674531>

[^wtetzner]: <https://news.ycombinator.com/item?id=4675198>

[^adambeynon]: <https://news.ycombinator.com/item?id=7852074>

[^DanielRibeiro]: <https://news.ycombinator.com/item?id=4674637>

[^adambeynon-mm]: <https://news.ycombinator.com/item?id=4696960>

[^inactive-user]: <https://lobste.rs/s/t6ooet/opal_ruby_javascript_compiler#c_ctou5u>

[^steveklabnik]: <https://lobste.rs/s/t6ooet/opal_ruby_javascript_compiler#c_ctvmg1>

[^inactive-user-grammar]: <https://lobste.rs/s/t6ooet/opal_ruby_javascript_compiler#c_7tqre6>
