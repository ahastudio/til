# zt: Zig 컴파일러가 검사하는 HTML 템플릿

원문: [Type-safe HTML templating in Zig | Lukáš Lalinský](https://lalinsky.com/2026/10/11/type-safe-html-templating-in-zig.html)

HN 토론: <https://news.ycombinator.com/item?id=50051573> (165점, 66개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/dujxbl/type_safe_html_templating_zig> (6점, 0개 댓글)

GN 토론: <https://news.hada.io/topic?id=35240>

## 요약

Lukáš Lalinský는 2000년 무렵 PHP 3.0으로 웹 개발을 시작해
PHP, Python 문자열 연결, Smarty, Template Toolkit,
Jinja와 Django 템플릿을 두루 써 왔다.
SPA와 JavaScript 프레임워크의 시대가 오자 프론트엔드에서 손을 뗐다가,
2년 전 Zig를 배우면서 자신의 생태계인 zio와 Dusty를 만들었다.
처음에는 JSON이나 MessagePack을 내보내는 API 백엔드용이었지만,
arena allocator를 잘 쓰면
웹 개발의 수많은 임시 문자열을 일일이 해제하지 않아도 되고,
comptime으로 성능을 잃지 않는 고수준 인터페이스를
만들 수 있다는 것을 알게 되었다.
htmx나 Datastar를 쓰면 JavaScript와 TypeScript 없이도 SPA를 만들 수 있다.

빠진 것은 템플릿이었다.
저자의 요구 조건은 네 가지였다.
모든 입력이 타입을 갖고 컴파일 시점에 검사될 것,
할당이나 중간 상태 없이 `std.Io.Writer`에 바로 쓸 것,
모든 입력을 기본으로 이스케이프해 XSS를 막을 것,
그리고 싸워야 하는 Zig DSL이 아니라 HTML을 쓰는 느낌일 것.
JSX 방식을 Zig로 옮긴 Ziex에서 영감을 받았지만 WASM 프레임워크는 원하지 않았고,
Go의 Templ을 발견한 뒤 무엇을 만들지 분명해졌다.

그렇게 만든 것이 zt다.
템플릿은 `zig build` 중에 파싱되어 Zig 코드로 변환되므로,
앱 코드가 템플릿을 가져다 쓸 수 있고 템플릿도 앱 코드를 가져다 쓸 수 있다.
그래서 모든 매개변수가 타입을 가진다.
생성된 코드는 `std.Io.Writer`에 쓰기만 하므로
소켓에 바로 쓰거나 버퍼에 모을 수 있다.

```zig
const User = @import("../models.zig").User;

pub templ Layout(title: []const u8) {
    <!DOCTYPE html>
    <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            @children
        </body>
    </html>
}

pub templ HomePage(user: ?User) {
    @Layout("Home") {
        if (user) |u| {
            <h1>Welcome back, {u.name}!</h1>
            <a href="/users/{u.id}">Your profile</a>
        } else {
            <h1>Welcome, guest!</h1>
            <a href="/login">Log in</a>
        }
    }
}
```

호출 쪽은 `pages.HomePage.render(.{user}, w)`처럼 쓰고,
Dusty 안에서는 `res.render(.html, pages.HomePage, .{user})` 한 줄로 끝난다.
동적 값은 텍스트와 속성 모두에서 기본으로 HTML 이스케이프되고,
`href`나 `src` 같은 URL 속성은 위험한 스킴까지 검사한다.
원시 HTML은 `{!value}`로 명시해야 나오고,
모든 요소가 제대로 닫혀야 파싱된다.
`{u.nmae}`처럼 오타를 내면 `zig build`가
“no field named 'nmae' in struct 'models.User'”라고 알려 주며,
생성 코드의 각 줄에는 원래 템플릿 위치가 주석으로 붙는다.

컴포넌트를 값으로 넘길 수 있고, `@children`으로 레이아웃을 만들어
다른 언어의 템플릿 상속을 대신한다.
제어 흐름은 Zig 그대로여서 `if`, `for`, `switch`와 페이로드 캡처를 쓸 수 있다.
아직 열린 문제도 있다.
줄이 `if`, `for`, `switch`로 시작하면 코드로 파싱되므로
“if you forgot your password…” 같은 문장이 한 줄에 홀로 있으면 파싱 오류가 난다.
저자는 Razor나 Twirl처럼 `@if`, `@for`, `@switch`로 바꾸는 방안을
검토하며 의견을 받고 있다.
여러 사람이 이미 쓰고 있지만 아직 성숙하지 않은 프로젝트라고 밝힌다.

## 분석

### 템플릿 오류를 컴파일러 오류로 바꾸는 것이 핵심이다

이 글의 중심 주장은 템플릿 언어를 새로 만드는 것이 아니라
템플릿을 호스트 언어의 컴파일 단위로 끌어들이는 데 있다.
Jinja나 Django 템플릿에서 필드 이름 오타는 실행해 봐야 드러나고,
그것도 빈 문자열로 조용히 넘어가는 경우가 많다.
zt에서는 같은 오타가 빌드를 멈춘다.
저자가 동적 언어의 런타임 템플릿 오류에 지쳤다고 쓴 이유가 여기 있다.

이 방식이 가능한 것은 템플릿을 별도 인터프리터로 돌리지 않고
Zig 코드로 바꿔 Zig 컴파일러에 넘기기 때문이다.
타입 검사기를 새로 만들 필요가 없고,
템플릿과 앱 코드가 같은 타입 체계 안에 들어간다.
Go의 Templ이 `generate` 명령으로 하는 일을 zt는 `zig build` 안에서 한다.

### 저수준 언어의 웹 개발을 가능하게 한 것은 언어보다 주변 환경이다

저자는 Zig로 웹 개발을 하게 될 줄 몰랐다고 말한다.
그 전환을 가능하게 한 요소를 글에서 추려 보면 세 가지다.
요청 단위로 한꺼번에 해제하는 arena allocator가
임시 문자열 관리의 고통을 없앴고,
comptime이 성능을 잃지 않는 고수준 인터페이스를 허락했고,
htmx와 Datastar가 서버에서 HTML 조각을 내려보내는 방식으로
클라이언트 JavaScript 없이 동적인 화면을 만들게 했다.

마지막 요소가 특히 중요하다.
서버가 JSON만 내보내던 시대에는 템플릿이 프론트엔드 프레임워크의 몫이었다.
htmx 계열이 서버 렌더링 HTML을 다시 주인공으로 만들자,
서버 언어마다 안전하고 빠른 HTML 생성기가 다시 필요해졌다.
zt는 그 수요가 Zig까지 내려온 사례다.

### “HTML처럼 느껴질 것”이라는 조건이 설계를 정한다

저자는 Zig 기반 DSL을 원하지 않았다고 분명히 적는다.
그래서 zt는 JSX처럼 HTML 태그를 그대로 쓰고, 제어 흐름만 Zig를 빌린다.
이 선택에는 대가가 있다.
HTML 텍스트와 Zig 코드가 같은 공간에 섞이므로,
`if`로 시작하는 영어 문장이 코드로 오인되는 모호성이 생긴다.
글 말미의 열린 문제는 이 조건에서 직접 나온 것이다.

## 비평

### 오류가 생성 코드를 가리키는 한 경험은 절반만 해결된다

저자가 가장 좋아한다고 꼽은 기능은
템플릿 오류가 Zig 컴파일러 오류가 된다는 점이다.
그런데 글에 실린 오류 메시지는 `src/templates/pages.zig:45:43`,
즉 생성된 코드의 위치를 가리킨다.
원래 템플릿 위치는 그 줄 끝의 주석 `pages.zt:18:31`에만 있다.

편집기와 언어 서버는 이 주석을 이해하지 못한다.
오류 목록에서 클릭하면 사람이 고칠 일이 없는 생성 파일이 열리고,
사람은 주석을 읽어 원래 파일로 다시 이동해야 한다.
컴파일 시점 검사라는 장점은 오류를 찾는 순간까지만 유효하고,
오류를 고치는 순간의 경험은 아직 다듬어지지 않았다.
Templ이 언어 서버를 함께 제공하는 이유가 바로 이 지점이다.

### 이스케이프 범위가 어디까지인지 글이 말하지 않는다

글은 텍스트와 속성의 HTML 이스케이프,
URL 속성의 위험한 스킴 검사를 설명하고
“가장 흔한 XSS 원인을 없앤다”고 정리한다.
그러나 `<script>` 안의 값, `<style>` 안의 값,
`onclick` 같은 이벤트 핸들러 속성 안의 값을 어떻게 다루는지는 나오지 않는다.
이런 위치에서는 HTML 이스케이프만으로는 안전하지 않다.

HN에서 weitzj가 떠올린 Google Soy(Closure Templates)는
HTML과 JavaScript 이스케이프를 내장한 템플릿 시스템이었다.[^weitzj]
저자도 예전에 Soy에 Python 지원을 붙인 포크를 만들어 즐겨 썼다고
답했다.[^lukaslalinsky-soy]
그 경험을 가진 저자라면
문맥별 이스케이프가 어디까지 되는지 밝혀 주는 편이 좋았다.
“안전한 기본값”을 첫 요구 조건으로 내건 글이므로,
보호 범위의 경계는 장점 목록만큼 중요하다.

### 예제의 첫 코드가 저자 스스로 버그가 있다고 말한 코드다

글의 `main` 예제 바로 아래에서 저자는
`std.Io` 취소가 중요한 곳에서 이 패턴을 쓰면
오류 처리에 매우 드러나지 않는 버그가 있다고 덧붙이고, Ziggit 스레드로 넘긴다.
Dusty의 `render` 함수가 그 문제를 해결한다는 설명도 붙인다.

이것은 zt의 문제라기보다 Zig 표준 라이브러리의 문제지만,
템플릿을 Dusty 밖에서 쓰려는 독자에게는 큰 함정이다.
HN에서 orf는 그 스레드를 보고 Zig 표준 라이브러리가 버그가 많고
IO 인터페이스가 취소 처리에 애를 먹는다고 읽었다.[^orf]
저자는 Io 인터페이스가 오히려 가장 좋은 취소 모델 중 하나이고,
문제는 Reader와 Writer 인터페이스와 Io 사이의 오류 처리 상호작용뿐이라고
반박했다.[^lukaslalinsky-io]
어느 쪽이든 결론은 같다.
zt를 단독으로 쓰려면 예제를 그대로 베끼지 말고
Dusty의 처리 방식을 확인해야 한다.

### “HTML처럼 쓴다”는 기준은 논쟁적이다

HN에서 slopinthebag은 Rust 매크로라면
별도 파일 형식이나 새 문법 없이 같은 일을 할 수 있다며
`rsx!` 예제를 보였다.[^slopinthebag]
그러자 dnautics는 그것은 HTML이 아니라
Rust 파서 규칙을 따라야 하는 새 DSL이라고 반박했고,[^dnautics-rsx]
skavi는 그 역시 문법을 발명한 것이라고 짚었다.[^skavi]

이 논쟁은 zt의 설계 조건이 보편적이지 않다는 것을 보여 준다.
Kotlin 쪽에서 flossly는 kotlinx.html 같은 내장 DSL을 선호한다고 했다.
템플릿 코드에 중단점을 걸 수 있고,
HTML 명세에서 생성한 타입 덕분에
허용되지 않는 요소 중첩까지 막아 준다는 이유다.[^flossly]
zt는 HTML 문법을 지키는 대신 요소 중첩 같은 구조 검사를
컴파일러에게 맡길 수 없고, 별도 파일 형식과 변환 단계를 감수한다.
글은 이 트레이드오프를 선택의 이유로만 제시하고 비용으로는 다루지 않는다.

## 인사이트

### 타입 검사되는 템플릿은 언어마다 같은 모양으로 수렴하고 있다

HN 스레드는 zt와 비슷한 시도의 목록이 되었다.
Java의 jte가 비슷하다는 지적이 있었고,[^_kidlike]
stefs는 템플릿마다 값을 매개변수로 받는 Kotlin 클래스를 생성하는
자기만의 엔진을 소개했다.[^stefs]
kitd는 그 방식이 Go의 Templ이 택한 길이라고 답했다.[^kitd]
marcle은 Ur/Web의 타입 안전한 XML을 떠올렸다.[^marcle]

언어도 시대도 다르지만 구조는 하나로 모인다.
템플릿을 호스트 언어 코드로 생성하고,
그 언어의 타입 검사와 빌드 도구에 검증을 맡긴다.
런타임 인터프리터를 가진 템플릿 엔진이
빌드 단계의 코드 생성기로 바뀌는 흐름이다.
zt의 의미는 새 발명보다
이 흐름이 메모리를 직접 관리하는 언어에까지 닿았다는 데 있다.

### 템플릿은 호스트 언어에서 떼어 내기 어렵다

Humphrey는 Django와 React 프론트엔드에서
같은 템플릿을 재사용할 수 있으면 좋겠다고 했지만,[^Humphrey]
riffraff는 한때 모두가 Mustache를 구현했다가 금방 시든 사례를 들었다.
호스트 언어는 바꾸지 않으면서 템플릿만 유지하는 일은 드물어서
언어 간 템플릿이 생각만큼 쓸모 있지 않았다는 것이다.[^riffraff]

zt는 정반대 방향의 극단이다.
템플릿이 앱의 타입을 직접 가져다 쓰므로 Zig 밖에서는 아무 의미가 없다.
타입 안전성은 호스트 언어와의 결합도를 높여서 얻는 것이고,
그 결합이 바로 Mustache 같은 중립적 템플릿이 줄 수 없던 검사를 가능하게 한다.
이식성과 안전성은 같은 축의 양 끝이다.

### 컴파일되는 템플릿은 코딩 에이전트에게 검증기가 된다

템플릿 엔진이 왜 필요하냐는 jaxxzi의 질문에
chii는 직접 문자열을 이어 붙이면
이스케이프 실수 하나가 HTML 주입으로 이어진다고 답했다.[^jaxxzi][^chii]
이 논리는 사람보다 에이전트에게 더 강하게 적용된다.
flossly는 Claude Code가 kotlinx.html을 문제없이 쓰며
자신은 템플릿을 거의 직접 쓰지 않는다고 적었다.[^flossly]

에이전트가 템플릿을 쓰는 시대에는
“실행해 봐야 아는 오류”보다 “빌드가 거부하는 오류”가 훨씬 값싸다.
필드 이름 오타, 잘못된 타입, 닫히지 않은 태그, 명시하지 않은 원시 HTML 출력이
모두 빌드 단계에서 걸리면,
에이전트는 사람이 화면을 보기 전에 스스로 고칠 수 있다.
zt 같은 도구의 진짜 고객은
런타임 오류에 지친 저자 같은 사람만이 아니라
매번 빌드 결과로 자기 출력을 검증해야 하는 에이전트일 수 있다.

### 1인 생태계는 빠르지만 경계가 흐리다

zt, Dusty, zio는 모두 같은 저자의 프로젝트다.
템플릿의 `render`가 Dusty에 묶여 있고,
예제의 취소 버그를 Dusty가 해결하며,
TODO 예제도 Dusty 안에 있다.
한 사람이 전체 스택을 설계하면 이렇게 빠르게 일관된 경험을 만들 수 있다.

그 대가는 경계가 흐려진다는 점이다.
HN에서 brodo는 Zig 핵심 팀과 저자 사이에 이력이 있다고 언급했다.[^brodo]
표준 라이브러리와의 마찰을 자기 라이브러리에서 해결하는 구조는
사용자에게 편하지만,
그 해결이 표준 쪽으로 흘러가지 않으면 생태계는 갈라진다.
zt를 도입하려는 팀은 템플릿 하나가 아니라
그 뒤에 있는 Dusty와 zio까지 함께 들이는지 따져 봐야 한다.

---

[^weitzj]: <https://news.ycombinator.com/item?id=50052610>

[^lukaslalinsky-soy]: <https://news.ycombinator.com/item?id=50052692>

[^orf]: <https://news.ycombinator.com/item?id=50052813>

[^lukaslalinsky-io]: <https://news.ycombinator.com/item?id=50052984>

[^slopinthebag]: <https://news.ycombinator.com/item?id=50051667>

[^dnautics-rsx]: <https://news.ycombinator.com/item?id=50051890>

[^skavi]: <https://news.ycombinator.com/item?id=50052142>

[^flossly]: <https://news.ycombinator.com/item?id=50054671>

[^_kidlike]: <https://news.ycombinator.com/item?id=50052323>

[^stefs]: <https://news.ycombinator.com/item?id=50053360>

[^kitd]: <https://news.ycombinator.com/item?id=50053670>

[^marcle]: <https://news.ycombinator.com/item?id=50052039>

[^Humphrey]: <https://news.ycombinator.com/item?id=50051808>

[^riffraff]: <https://news.ycombinator.com/item?id=50052321>

[^jaxxzi]: <https://news.ycombinator.com/item?id=50052361>

[^chii]: <https://news.ycombinator.com/item?id=50052382>

[^brodo]: <https://news.ycombinator.com/item?id=50053514>
