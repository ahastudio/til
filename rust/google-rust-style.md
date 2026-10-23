# Google Rust 스타일 가이드: 서식보다 API와 구현의 설계를 다루는 규칙집

원문: [Rust Style Guide | Google Style Guides](https://google.github.io/styleguide/rustguide.html)

HN 토론: <https://news.ycombinator.com/item?id=50186010> (377점, 222개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide> (49점, 17개 댓글)

GN 토론: <https://news.hada.io/topic?id=35789>

## 소개

Google이 사내에서 Rust를 쓰는 방식을 정리한 스타일 가이드다.
여기서 스타일은 서식만이 아니라 API 설계와 구현 설계에 대한 지침까지 포함한다.
google3, Android, ChromeOS, Fuchsia, Chrome에서 쓰이는 Rust 코드가 코드베이스 안과 사이에서 일관되게 하고, 품질의 기준을 세우는 것이 목적이다.

규칙의 출처를 밝히는 목표 목록이 이 가이드를 읽는 열쇠다.
가독성과 유지보수성을 작성 편의보다 앞세우고, 자동화에 유리한 규칙을 고르고, 더 넓은 Rust 생태계와 어긋나지 않게 하고, 부담에 값하는 규칙만 넣고, 사소한 의견 충돌을 줄인다는 항목이다.
그리고 일반 Rust 규칙과 갈라지는 이유를 하나 더 든다.
코드베이스 전체에 걸친 대규모 변경(Large-Scale Changes, LSC)을 도구로 하기 쉽게 만드는 것이다.
이 목표를 알면 이 가이드의 규칙 중 일부가 왜 그렇게 정해졌는지 읽힌다.

가이드는 공개된 Rust 스타일 규칙과 Rust API Guidelines를 따르되, 충돌할 때만 이 가이드가 우선한다고 한다.
서식은 대부분 `rustfmt`가 맡는다.
이 문서는 가이드 전체를 옮기지 않고, 규칙을 고르는 데 쓸 수 있는 구조로 정리한다.

## 동작 방식

### 라이브러리 코드와 애플리케이션 코드를 구분한다

API 설계 규칙은 코드의 종류에 따라 구속력이 다르다.
다른 프로젝트가 가져다 쓰는 범용 라이브러리 코드에는 API 설계 규칙이 구속력을 가진다.
한 애플리케이션에서만 쓰는 코드에는 강한 권고이고, 이런 코드는 일반성보다 단순함과 직접성을 택해야 한다.
가이드는 성급한 일반화와 추상화를 피하고 당장의 필요에 집중하라고 한다.

이 구분은 규칙마다 반복된다.
반환 타입에 반복자(iterator)를 쓰는 규칙은 라이브러리에는 권하지만, 애플리케이션에서는 `Vec<T>`를 돌려주는 편이 단순하면 그렇게 해도 된다고 한다.
`impl Into<T>` 매개변수는 라이브러리의 호출 편의를 위해 고려할 수 있지만, 애플리케이션 코드는 거의 쓰지 말라고 한다.
trait 구현도 저수준 라이브러리는 사용자의 필요를 미리 예상해 추가하고, 애플리케이션은 필요할 때 추가한다.

### 규칙을 영역별로 읽는 지도

| 영역          | 핵심 규칙                                                                                                                                |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 코드 구성     | glob import 금지, `use` 하나는 한 모듈에서만 가져옴, 최상위 함수는 모듈 이름으로 한정해 호출, 타입은 한정 없이 사용                      |
| 소유권과 빌림 | `Rc`와 `Arc` 피하기, 깊은 복사 대신 빌림, 복사가 필요할 때만 `.clone()`                                                                  |
| 함수 입출력   | `&Vec<T>` 대신 `&[T]`, `&String` 대신 `&str`, 불분명한 `bool` 대신 `enum`, 오류 종류에 맞는 `Option`, `Result`, `panic!` 선택            |
| 타입          | 의미가 다르면 별칭이 아니라 newtype, 튜플보다 이름 붙은 필드                                                                             |
| trait         | 표준 trait이 맞으면 직접 만든 메서드 대신 구현, 가능하면 `#[derive()]`, 라이브러리는 `dyn Trait`보다 제네릭, 확장 trait에는 `Ext` 접미사 |
| 동시성        | 오염된(poisoned) 뮤텍스 내부를 꺼내지 않기. Chromium은 `async`와 `.await`를 쓰지 않고, 스레드 대신 시퀀스를 쓴다                         |
| 매크로        | 함수와 타입이 우선, 다음이 `macro_rules!`, 코드 생성, `proc_macro`는 마지막                                                              |
| 이름 짓기     | 표준 라이브러리 방식, 수명(lifetime)은 서술적인 이름, 약어는 모르는 사람이 없는 경우에만                                                 |
| 문서          | 공개 API에 문서 주석, 패닉 조건과 `unsafe` 불변식은 반드시 기술, 코드가 이미 말하는 내용은 반복하지 않기                                 |
| 기타 기능     | `unsafe`는 불가피할 때만, 안정되지 않은 기능 금지, 공개 enum과 구조체에 `#[non_exhaustive]`, `main()` 이전에 실행되는 코드 금지          |
| 구현          | 확인 뒤 `unwrap` 대신 패턴 매칭, `unwrap`보다 `expect`, 추론에 지나치게 의존하지 않기, `panic::catch_unwind` 금지                        |

[chrome]과 [Fuchsia] 표시가 붙은 규칙은 해당 코드베이스에만 적용된다.
`async` 금지와 작은 크레이트 선호가 그 예이며, 가이드의 일반 규칙으로 읽으면 안 된다.

### 오류를 보고하는 세 방식

가이드는 오류의 성격에 따라 도구를 나눈다.
원인이 뻔하고 호출자가 자세한 정보를 얻어도 쓸 곳이 없는 단순한 실패에는 `Option`을 쓴다.
정수 오버플로로 합이 만들어지지 않는 `checked_add`가 그 예다.
호출자가 원인을 알아야 회복할 수 있는 실패에는 `Result`를 쓴다.
파일을 여는 함수가 `NotFound`와 `PermissionDenied`를 구분해야 하는 경우다.
버그와 깨진 불변식을 알리는 데에는 `panic!`을 쓴다.
이런 오류는 미리 검사하면 피할 수 있으므로 런타임에 처리하는 것이 아니라 코드에서 고쳐야 한다고 한다.
다만 일부 코드베이스는 패닉을 아예 피하고 깨진 불변식도 `Result`로 보고하게 할 수 있다고 덧붙인다.

## 적용하기

가이드에서 바로 쓸 수 있는 규칙 몇 개를 코드로 옮겼다.
이 환경에는 Rust 툴체인이 없어서 아래 코드를 컴파일해 확인하지는 못했다.
가이드의 규칙을 내 말로 옮긴 예이며, 원문의 코드를 그대로 옮긴 것이 아니다.

```rust
// 함수 입력: &Vec<String>이나 &String이 아니라 &[String]과 &str을 받는다.
fn count_matches(lines: &[String], needle: &str) -> usize {
    lines.iter().filter(|line| line.contains(needle)).count()
}

// 불분명한 bool 대신 enum을 쓴다. 호출부가 스스로 설명한다.
enum Overwrite {
    Yes,
    No,
}

fn save(path: &str, overwrite: Overwrite) -> bool {
    match overwrite {
        Overwrite::Yes => !path.is_empty(),
        Overwrite::No => false,
    }
}

// is_some() 확인 뒤 unwrap()하지 말고, 패턴 매칭으로 컴파일러에 증명한다.
fn describe(value: Option<u32>) -> String {
    if let Some(v) = value {
        format!("값: {v}")
    } else {
        String::from("없음")
    }
}

// 문자열을 둘 넘게 이을 때는 + 대신 format!을 쓴다.
fn label(prefix: &str, id: u32, suffix: &str) -> String {
    format!("{prefix}-{id}-{suffix}")
}

// 반복자 체인은 변수에 담아 이름을 붙이고, for 루프 머리에 두지 않는다.
fn urgent_total(priorities: &[u8]) -> u32 {
    let urgent = priorities.iter().filter(|p| **p <= 1);
    let mut total = 0;
    for p in urgent {
        total += u32::from(*p) + 1;
    }
    total
}
```

이 예는 `rustc`로 컴파일해 보기 전에는 컴파일이 되는지 장담할 수 없다.
규칙을 손으로 익히는 용도이며, 실제 프로젝트에서는 `cargo clippy`가 이 중 상당수를 잡는다.
가이드는 규칙마다 대응하는 Clippy 린트를 적어 두었다.
`ptr_arg`는 `&Vec<T>`와 `&String` 규칙, `should_implement_trait`은 표준 trait 구현 규칙, `len_without_is_empty`는 `len()`과 `is_empty()`를 함께 구현하는 규칙에 해당한다.

## 트레이드오프

### Rc와 Arc를 피하는 규칙은 논쟁적이다

가이드는 고유 소유권과 빌림을 `Rc`나 `Arc`보다 앞세운다.
공유 소유권 포인터가 런타임 비용과 고유한 복잡성을 더하고, 다른 언어에서 온 개발자가 너무 쉽게 쓴다는 이유다.
대안이 쓰기, 이해하기, 유지하기에 지나치게 복잡하면 예외를 두고, 이는 코드 리뷰에서 판단한다.

HN에서 slaymaker1907은 호출 스택 밖에서 사는 참조에는 `Rc`와 `Arc`를 써야 한다고 반대했다.
수명을 갖고 컴파일러를 설득하려 애쓰기보다 그냥 `Rc`나 `Arc`를 쓰라는 것이다.[^slaymaker1907]
i2talics는 참조 카운팅을 쓰면 객체 그래프를 게으르게 던지다가 누가 누구를 소유하는지 놓친다고 반박했다.[^i2talics-rc]
wtetzner는 공유 수명이 정말 필요한 경우가 아니면 수명이 참조 카운팅보다 읽기 쉽다고 했다.[^wtetzner]
mrbonner는 한정된 범위에서는 빌림을, 범위 밖으로 넘기는 구조에서는 `Rc`나 `Arc`를 선호한다고 절충했다.[^mrbonner]
가이드의 예외 문구가 이 절충을 이미 허용하므로, 논쟁은 어디서부터 지나치게 복잡한가에 달려 있다.

### 타입을 한정 없이 쓰는 규칙은 이름의 의미를 지울 수 있다

가이드는 `regex::Regex`가 아니라 `Regex`를 쓰라고 한다.
HN에서 epage는 이 규칙이 `io::Error` 대신 `IoError`처럼 이름에 중복 정보를 넣게 만들고, `Source` 같은 일반적인 이름은 어디서 왔는지 알아야 읽힌다고 반박했다.[^epage-types]
Blikkentrekker는 가이드가 모호한 경우의 예외로 `io::Error`를 직접 들었다고 짚었다.[^Blikkentrekker]
wtetzner는 어느 방향이든 일률적인 규칙은 나쁜 생각이라고 했다.[^wtetzner-types]
가이드 자신이 이 규칙의 이유를 대부분 리뷰어 사이의 이견을 피하기 위해서라고 밝힌다.
따라서 이 규칙은 정답의 문제가 아니라 합의 비용의 문제다.

### 공개 enum의 `#[non_exhaustive]`는 컴파일러의 도움을 포기하는 일이다

가이드는 다른 팀이 쓰는 공개 API의 enum에 `#[non_exhaustive]`를 붙이라고 한다.
새 variant를 추가해도 사용자의 코드가 컴파일되도록 하기 위해서다.
HN에서 japgolly는 이 권고가 enum의 가장 큰 힘을 버리게 한다고 비판했다.
새 case가 생기면 컴파일러가 갱신할 모든 패턴 매칭을 알려 주는 점이 enum의 힘인데, 와일드카드 팔을 두면 새 case를 처리하지 않아도 런타임 문제가 된다는 것이다.[^japgolly]
ninkendo는 반대로 공개 API에 올리는 enum을 신중하게 골라야 하고, 하위 호환성을 진지하게 보려면 “알 수 없음” 같은 유연한 variant를 포함해야 한다고 덧붙였다.[^ninkendo]
Lobste.rs에서 ettolrach도 같은 반대 의견을 냈다.
호출자가 새 variant가 추가됐을 때 오류를 받아 새 논리를 처리하게 해야 하는데, 기본 분기로 흘러가면 안 된다는 것이다.[^ettolrach]
foonathan은 와일드카드는 두되 모든 variant를 나열하지 않으면 경고하는 Clippy 린트 `match_wildcard_for_single_variants`가 있다고 답했다.
새 값을 추가할 권리를 사용자에게 알리면서도, 사용자는 모두 처리해야 하는 양쪽의 장점을 얻는다는 설명이다.[^foonathan]
가이드도 `non_exhaustive` enum을 매칭할 때 variant를 모두 나열하라는 규칙과 빌트인 린트 `non_exhaustive_omitted_patterns`를 따로 둔다.
가이드는 변하지 않을 enum, 두 가지 상태뿐인 enum, 대규모 변경으로 고칠 각오가 된 경우를 예외로 둔다.

### 제네릭이냐 dyn이냐에서 코드 크기는 이유 일부일 뿐이다

가이드는 라이브러리에서 매개변수로 `dyn Trait`보다 제네릭을 권하고, 코드 크기가 중요한 경우를 예외로 든다.
Lobste.rs에서 ettolrach는 코드 크기만 예외로 드는 것이 오해를 부를 수 있다고 했다.
긴 타입 사슬을 따라 제네릭을 계속 명시하지 않아도 되는 이점이 있고, 이는 글자 수 차이를 넘어 단형화(monomorphisation)를 줄이는 효과도 있다는 것이다.[^ettolrach-dyn]
가이드의 이유 항목은 효율, 곧 간접 참조와 인라인 불가를 들고 있어, 이 지적은 가이드가 다루지 않은 비용 쪽을 보탠다.

### getter 이름 규칙

가이드의 getter와 setter 규칙은 `foo()`, `foo_mut()`, `take_foo()`, `set_foo()`, `replace_foo()`, 클로저를 받는 `with_foo()` 순이다.
HN에서 incrediblers는 메서드가 구체적인 일을 한다는 관점에서 setter가 `text`, getter가 `get_text`여야 한다고 반대했다.[^incrediblers]
i2talics는 표준 라이브러리에 널리 퍼진 방식이니 그 지역의 관습을 따르라고 답했고,[^i2talics-getter]
epage는 빌더 타입은 접두사 없는 setter와 `get_` getter를, 레코드 같은 구조체는 접두사 없는 getter와 `set_` setter를 선호한다고 구분했다.[^epage-getter]
어느 쪽이 맞는지보다, 한 코드베이스 안에서 하나를 정해 일관되게 쓰는 것이 이 규칙의 목적이다.

## 함정

- Chromium과 Fuchsia 전용 규칙을 일반 규칙처럼 따라 하면 안 된다.
  `async` 금지, 작은 크레이트 선호, 평평한 파일 배치는 해당 코드베이스의 빌드 구조에서 나온 규칙이다.
  HN에서 evmar는 Cargo에서는 크레이트가 자체 디렉터리와 `Cargo.toml`을 요구해 추상화 비용이 크지만, Google의 빌드 시스템에서는 같은 디렉터리에 파일을 섞어 두고 더 잘게 나눈다고 설명했다.[^evmar]
  Lobste.rs에서 sluongng은 크기를 줄이는 이유가 빌드 도구보다 `rustc`의 한계에 가깝다고 했다.
  파일이 아니라 크레이트가 증분 컴파일의 단위여서, Blaze나 Bazel도 같은 제약을 받는다는 설명이다.[^sluongng]
  refi64도 외부 빌드 시스템 상당수가 한 크레이트의 증분 빌드 캐시를 다음 빌드에 이어 쓰지 못한다고 했고,[^refi64]
  novedevo는 Cargo에서는 복잡도가 정당하면 크레이트에 `.rs` 파일이 몇 개 이상 들어도 좋다고 했다.[^novedevo]
  이 차이를 모르고 Cargo 프로젝트에 옮기면 맞지 않는다.
- 규칙 하나를 떼어 내 전체 가이드를 판단하면 안 된다.
  가이드 스스로 부담에 값하는 규칙만 넣는다고 하고, 예외를 규칙마다 달아 두었다.
- 서식 규칙 가운데 `rustfmt` 옵션 일부는 안정(stable) 채널에서 쓸 수 없는 옵션이다.
  가이드는 안정 채널에서 빌드하는 코드베이스라면 이 옵션을 적용하지 않아도 된다고 한다.
- `#[rustfmt::skip]`은 수동 정렬이 필요한 경우와 생성된 코드에만 쓴다.
  개인 취향은 이유가 되지 않는다.
- 코드가 이미 말하는 내용을 문서 주석으로 반복하지 않는다.
  `MockFileSystem`에 “테스트용 모의 구현”이라고 적는 주석이 가이드가 드는 나쁜 예다.

## 체크리스트

- 이 코드는 라이브러리인가 애플리케이션인가, 그에 따라 API 규칙의 강도를 정했는가.
- 함수가 `&Vec<T>`, `&String`, `&Box<T>`, `&Option<T>`를 받고 있지 않은가.
- 이유가 분명하지 않은 `bool` 인자가 있지 않은가.
- `Rc`나 `Arc`를 쓴 곳마다 대안(빌림)이 너무 복잡한 이유를 말할 수 있는가.
- `unwrap`을 쓰는 곳에서 패턴 매칭으로 바꿀 수 있는가.
- `unsafe` 블록마다 `SAFETY:` 주석과 안전한 구현을 쓰지 않는 이유가 있는가.
- 공개 API의 enum과 공개 필드가 있는 구조체에 `#[non_exhaustive]`를 붙일지 정했는가.
- 공개 API에 문서 주석이 있고, 패닉 조건이 기술돼 있는가.
- `cargo clippy`를 돌려 가이드가 지목한 린트를 켰는가.

## 기억할 원칙

### 규칙의 값은 이유에 있다

이 가이드의 설득력은 규칙 아래에 적힌 근거에서 나온다.
많은 규칙이 “리뷰어 사이의 이견을 줄이기 위해”라고 직접 밝히고, 다른 규칙은 대규모 변경 도구에 맞추려는 것이라고 한다.
이유를 모르고 규칙만 가져오면 자기 코드베이스에서 같은 효과가 나는지 알 수 없다.
HN의 논쟁 대부분이 규칙 자체가 아니라 그 규칙이 쓰인 맥락, 곧 Google의 모노레포와 빌드 시스템, 대규모 변경에서 갈렸다.
Lobste.rs에서 junon은 이 가이드가 Rust를 Java처럼 만들려는 것 같다고 했다.[^junon]
epidemian은 거대 기업의 사내 규칙에서는 스타일을 통일하고 부분과 사람의 교체 가능성을 높이는 것이 당연하다고 보면서, 가이드에서 Java식이라 할 구체적인 지점은 찾지 못했다고 답했다.[^epidemian]
joshka는 같은 종류의 문서로 Microsoft와 Ed Page의 Rust 지침을 소개했다.[^joshka]

### 일관성은 도구가 있을 때 가치가 커진다

가이드가 서식 규칙을 `rustfmt` 설정으로, 나머지 규칙을 Clippy 린트로 연결해 두는 것은 같은 이유다.
HN에서 manlymuppet은 이 가이드를 모델에 엄격히 따르라고 주는 것이 쓸모 있는지 물었고,[^manlymuppet] threethirtytwo는 컨텍스트를 소모하므로 쓸모없다고 답했다.[^threethirtytwo]
어느 쪽이든 기계가 검사할 수 있는 규칙은 사람이 기억하는 규칙보다 지켜지기 쉽다.
실제로 한 사용자는 회사에서 모델에게 지침을 줘도 모델이 항상 따르지는 않고, 검토할 코드가 너무 많아 강제하기 어렵다고 적었다.[^yodsanklai]
따라서 규칙을 채택한다면 그 규칙을 검사할 린트나 설정을 함께 정하는 것이 먼저다.

---

[^slaymaker1907]: <https://news.ycombinator.com/item?id=50187239>

[^i2talics-rc]: <https://news.ycombinator.com/item?id=50187399>

[^wtetzner]: <https://news.ycombinator.com/item?id=50188140>

[^mrbonner]: <https://news.ycombinator.com/item?id=50189247>

[^epage-types]: <https://news.ycombinator.com/item?id=50187811>

[^Blikkentrekker]: <https://news.ycombinator.com/item?id=50187941>

[^wtetzner-types]: <https://news.ycombinator.com/item?id=50188051>

[^japgolly]: <https://news.ycombinator.com/item?id=50190529>

[^ninkendo]: <https://news.ycombinator.com/item?id=50190843>

[^incrediblers]: <https://news.ycombinator.com/item?id=50187233>

[^i2talics-getter]: <https://news.ycombinator.com/item?id=50187348>

[^epage-getter]: <https://news.ycombinator.com/item?id=50187763>

[^evmar]: <https://news.ycombinator.com/item?id=50187119>

[^manlymuppet]: <https://news.ycombinator.com/item?id=50189961>

[^threethirtytwo]: <https://news.ycombinator.com/item?id=50189988>

[^yodsanklai]: <https://news.ycombinator.com/item?id=50186765>

[^ettolrach]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_8wxvry>

[^ettolrach-dyn]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_8wxvry>

[^foonathan]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_cxeajh>

[^sluongng]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_03om4k>

[^refi64]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_al7kbt>

[^novedevo]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_yrtxmg>

[^junon]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_dp62eh>

[^epidemian]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_rcy2m6>

[^joshka]: <https://lobste.rs/s/9jgl3x/google_s_rust_style_guide#c_iilhg1>
