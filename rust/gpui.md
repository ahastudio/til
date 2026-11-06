# GPUI: Zed가 만든 GPU 가속 Rust UI 프레임워크이고 아직 Zed와 묶여 있다

<https://gpui.rs/>

<https://docs.rs/gpui/latest/gpui/>

<https://github.com/zed-industries/zed/tree/main/crates/gpui>

HN 토론: <https://news.ycombinator.com/item?id=39119953> (50점, 8개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=46611940> (4점, 0개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=45530819> (2점, 0개 댓글)

## 소개

GPUI는 Zed 편집기를 만든 사람들이 만든 Rust용 UI 프레임워크다.
홈페이지는 이를 빠르고 즉시 모드와 유지 모드를 섞은 GPU 가속 Rust UI
프레임워크라고 소개하며,
Zed와 Delta를 만든 사람들의 작품이라고 적는다.
홈페이지에는 `div()`에 `flex()`, `gap_3()`, `bg(...)` 같은 메서드를 이어 붙이는
Hello World 예제가 있고, 문서와 예제로 가는 링크가 있다.

홈페이지가 가장 눈에 띄게 밝히는 제약은 기여 방식이다.
당분간 GPUI는 Zed와 묶여 있어서 기여는 Zed 저장소에 하고 그쪽과 맞춰 둬야
한다고 한다.
소스는 `zed-industries/zed` 저장소의 `crates/gpui`에 있고,
crates.io의 `gpui` 크레이트는 2026년 10월 30일 기준 최신 버전이 0.2.2이며
내려받기 수가 약 44만 회다.[^crates]

이 문서의 성능과 설계 설명은 홈페이지와 홈페이지가 가리키는 README에서
읽은 것이다.
이 문서는 GPUI로 앱을 만들어 보지 않았다.

## 구조

README는 GPUI가 서로 다른 세 가지 층을 제공한다고 설명한다.[^readme]

첫째는 엔티티(Entity)로 하는 상태 관리와 통신이다.
엔티티는 GPUI가 소유하며 `Rc`와 비슷한 소유 스마트 포인터로만 접근할 수 있다.

둘째는 뷰(view)로 하는 선언적 UI다.
뷰는 `Render` 트레이트를 구현한 엔티티이고,
프레임이 시작될 때마다 GPUI가 루트 뷰의 `render`를 부른다.
뷰는 요소(element) 트리를 만들고 Tailwind식 API로 배치하고 꾸민다.

셋째는 요소로 하는 저수준 명령형 UI다.
요소는 렌더링 방식을 완전히 통제하며
큰 목록의 효율적인 뷰나 코드 편집기의 사용자 지정 레이아웃에 쓴다.

그 밖에 키 입력을 논리 동작으로 바꾸는 액션,
플랫폼 서비스(앱 종료, URL 열기),
플랫폼 이벤트 루프와 통합된 비동기 실행기,
`#[gpui::test]` 매크로가 제공하는 테스트용 컨텍스트가 있다.

## 시작하기와 플랫폼

README에 따르면 GPUI는 Zed 개발과 함께 활발히 개발 중이며 1.0 이전이다.
버전 사이에 호환을 깨는 변경이 자주 있고 최신 안정 Rust가 필요하다.
`Cargo.toml`에는 `gpui`와 선택적으로 `gpui_platform`을 추가한다.[^readme]

```toml
gpui = { version = "*" }
gpui_platform = { version = "*", features = ["font-kit", "wayland", "x11"] }
```

플랫폼별 조건은 다음과 같다.[^readme]

| 플랫폼         | 렌더링과 글자                                                |
| -------------- | ------------------------------------------------------------ |
| macOS          | Metal로 그린다. 글리프를 그리려면 `font-kit` 기능이 필요하다 |
| Linux, FreeBSD | `wayland`나 `x11` 창 기능을 최소 하나 켠다                   |
| Windows        | 별도 기능이 필요 없다. Win32 창과 DirectWrite 글자를 쓴다    |

macOS에서는 Xcode와 명령줄 도구가 필요하다.
공식 문서에 대해서는 README가 가장 좋은 학습 방법이 Zed 소스 코드를 읽거나
Zed 디스코드에 질문하는 것이라고 인정한다.[^readme]

## 비평

### 아직 1.0이 아니고 호환 변경이 잦으며 Zed에 묶여 있다

README는 1.0 이전이라 버전 사이에 호환을 깨는 변경이 자주 있다고
밝힌다.[^readme]
홈페이지는 기여가 Zed 저장소로 모여야 한다고 하고,
README는 문서가 부족하며 소스를 읽는 것이 가장 좋은 방법이라고 한다.
외부 사용자는 프레임워크의 진행 방향을 Zed의 필요에 맡기는 셈이다.
HN의 the__alchemist는 몇 달 전 유지보수가 불확실해질 수 있다는 공지를 보고
GPUI를 써 보려다 물러섰다고 적었고,[^the__alchemist]
eviks는 공개된 프레임워크가 방치되어 있어 접근성에 도달하지 못할 수도 있다고
했다.[^eviks]
이 두 주장은 댓글 작성자의 것이고 이 문서는 그 공지를 확인하지 못했다.
홈페이지의 문구인 당분간 Zed와 묶여 있다는 말이 같은 방향을 가리킨다.

### 접근성과 입력기는 문서 밖에서 확인해야 한다

README는 추가 주제로 접근성 문서가 있다고 목록에 올리지만
이 문서는 그 문서를 열지 않았다.
Discord가 전체 클라이언트를 GPUI로 옮긴다는 발표가 나온 뒤,
Daedren은 접근성과 제대로 된 CJK 글자 표시를 보장하는지 물었고,[^Daedren]
mintflow는 받아들일 만한 중국어 글자가 그려지고 검색창에서 입력기가 작동한다고
답했다.[^mintflow]
tensor는 접근성이 저장소 안에는 없지만 `gpui-kit` 같은 프로젝트가 통합해 준다고
했다.[^tensor]
이 논의는 [Discord의 Rust 전환 발표](discord-rust-client.md)에 대한 글에도
담겨 있다.
홈페이지만으로는 접근성의 현재 수준을 알 수 없다는 것이 이 문서의 판단이다.

### 메서드 체이닝 API는 호불호가 갈린다

홈페이지 첫 화면의 예제는 `div().flex().flex_col().gap_3()...`처럼 길게
이어진다.
kayson은 이것이 끔찍해 보이고 더 나은 방법이 있을 것이라고 했고,[^kayson]
tcallred는 UI를 표현하는 데는 Swift와 Kotlin 같은 꼬리 람다 문법이 있으면
충분하다고 했다.[^tcallred]
2024년의 HN 스레드에서는 erikaww가 HTML과 CSS와 JS를 쓸 수 있는 Tauri 대신
이 프레임워크를 쓸 이유가 무엇이냐고 물었고,[^erikaww]
mgrandl은 이미 상태와 로직을 모두 Rust에 두고 있어서
Tauri 명령과 리스너를 건너뛰고 기존 구조체에 렌더러를 바로 구현할 수 있고,
웹뷰를 거치지 않으니 지연이 더 낮을 것이라고 답했다.[^mgrandl]
이 답은 이 프레임워크가 누구에게 맞는지를 보여 준다.
Rust로 앱 로직을 이미 가진 사람에게는 이점이 크고,
웹 기술에 익숙한 사람에게는 진입 비용이 크다.

## 인사이트

### 가장 큰 이용자가 만든 도구라는 점이 장점이자 위험이다

GPUI는 Zed라는 실제 큰 앱이 쓰는 프레임워크이므로
편집기에 필요한 요소(큰 목록, 사용자 지정 레이아웃,
키 입력 처리)가 검증되어 있다.
그러나 같은 이유로 Zed의 필요가 우선이고 외부 사용자의 필요는 그 뒤다.
README의 `gpui_platform`이 최근에 분리된 것도,
외부 앱이 플랫폼 기능을 고르게 하려는 방향으로 읽히지만
이는 이 문서의 해석이다.
Discord 같은 큰 외부 이용자가 쓰기 시작하면
프레임워크의 우선순위를 둘러싼 긴장이 커질 수 있다.

### 선택의 기준은 UI의 종류가 아니라 앱 로직이 어디에 있느냐다

mgrandl의 답은 GPUI가 UI를 그리는 도구를 넘어
앱의 상태와 로직이 Rust에 있을 때 그 구조체에 바로 렌더러를 붙이는 방식이라는
점을 보여 준다.
이 점이 웹 기술 위에 UI를 두는 선택과 갈리는 지점이다.
웹 UI는 로직과 화면을 명령과 이벤트로 나누고,
GPUI는 둘을 같은 언어와 같은 메모리에 둔다.
그러므로 도입 판단은 화면이 얼마나 복잡한가가 아니라
앱의 핵심이 이미 Rust인가, 그리고 접근성과 국제화를 직접 책임질 수 있는가에
달려 있다.

### 결론을 바꿀 관찰

GPUI가 Zed 저장소에서 분리되어 독립 저장소와 안정 버전(1.0)을 갖는다는
발표가 나오면
외부 사용자의 위험이 크게 줄어든다.
접근성 문서가 스크린 리더를 실제로 지원한다고 보여 주고
독립된 앱이 그것을 확인한 사례가 나오면 가장 큰 의문이 풀린다.
Discord 클라이언트가 출시되어 접근성과 입력기를 어떻게 다루는지 알려지면
이 프레임워크가 큰 앱의 요구를 감당하는지가 드러난다.

---

[^crates]: crates.io, [gpui](https://crates.io/crates/gpui), 2026-10-30

[^readme]: GitHub, [Welcome to GPUI! (zed-industries/zed, crates/gpui/README.md)](https://github.com/zed-industries/zed/blob/main/crates/gpui/README.md), 2026-06-09

[^the__alchemist]: <https://news.ycombinator.com/item?id=50379999>

[^eviks]: <https://news.ycombinator.com/item?id=50380894>

[^Daedren]: <https://news.ycombinator.com/item?id=50379235>

[^mintflow]: <https://news.ycombinator.com/item?id=50379359>

[^tensor]: <https://news.ycombinator.com/item?id=50383192>

[^kayson]: <https://news.ycombinator.com/item?id=50379724>

[^tcallred]: <https://news.ycombinator.com/item?id=50381689>

[^erikaww]: <https://news.ycombinator.com/item?id=39124765>

[^mgrandl]: <https://news.ycombinator.com/item?id=39126509>
