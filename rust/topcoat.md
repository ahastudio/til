# Topcoat: The full full-stack framework for Rust

<https://github.com/tokio-rs/topcoat>

발표 글: <https://tokio.rs/blog/2026-07-22-announcing-topcoat>

Toasty ORM: <https://github.com/tokio-rs/toasty>

HN 토론: <https://news.ycombinator.com/item?id=48952067> (134점, 48개 댓글)

Lobste.rs 토론 (저장소): <https://lobste.rs/s/zmg7ot/topcoat_batteries_included_framework> (18점)

Lobste.rs 토론 (발표 글): <https://lobste.rs/s/l8hiip/announcing_topcoat_framework_for> (16점)

## 소개

Topcoat은 tokio-rs 조직에서 공개한 Rust 풀스택 웹 프레임워크다.
“배터리 포함(batteries-included)”을 표방하며 라우팅, 서버 사이드 렌더링, 클라이언트 반응성, 에셋 번들링, 컴포넌트 라이브러리, Tailwind 통합을 하나의 프레임워크로 제공한다.
README는 조기 단계이며 실험적이고 브레이킹 체인지가 예상된다고 명시한다.
저장소는 2026년 4월 3일에 만들어졌고, 이 문서 갱신 시점 기준 스타 4,378개, 포크 161개, 열린 이슈 32개이며 라이선스는 MIT다.

공개 경위 자체가 계획적이지 않았다.
Tokio 창시자인 `carllerche`는 HN에서 여기 올라올 줄 몰랐다며, 비공개 CI 사용량이 소진되어 저장소를 열었고 블로그 포스트가 다음 주에 나올 것이라고 밝혔다.[^carllerche]
그가 예고한 글은 2026년 7월 22일 Tokio 블로그에 「Announcing Topcoat: a framework for building full-stack reactive web apps with Rust」로 실렸고, Carl Lerche와 Julien Scholz 공동 명의로 서명되어 있다.
Carl은 2025년 말 Julien Scholz를 만나 웹 앱 프레임워크에 대한 그의 안목과 열정에 감명받아 직접 만들어 보라고 설득했다고 밝힌다.

발표 글이 제시하는 동기는 언어 선택의 계산이 바뀌었다는 것이다.
3년 전이라면 Rust가 웹 앱을 만들기 좋은 언어라고 말했을 때 미쳤다는 소리를 들었을 것이고 그것이 온당했을 텐데, 웹 앱은 전통적으로 성능에 민감한 애플리케이션이 아니어서 빨리 출시하게 해 주는 도구가 옳은 선택이었고 그래서 가장 풍부한 웹 생태계가 JavaScript와 Ruby와 PHP에 있다는 것이다.
그러나 AI가 그 계산을 완전히 재편했으며, AI는 학습 장벽과 생산성 격차를 지워 버리고, 현대적인 코딩 AI 도구가 무언가를 만드는 데 걸리는 시간의 차이는 주로 사용 가능한 라이브러리 집합의 함수이지 프로그래밍 언어의 함수가 아니라는 주장이다.
Rust를 한 번도 써 본 적 없는 숙련된 소프트웨어 엔지니어가 AI 도구와 함께 첫날부터 Rust로 만들어 나가는 것을 보았다며, 바이브 코딩이 아니라 일반적인 공학 경험으로 도구와 상호작용하며 언어를 배우면서 진척을 내는 것을 말한다고 단서를 단다.
그러므로 지금 필요한 것은 풍부한 라이브러리 생태계이고, 그것이 자신이 만들어 온 것이며, 가장 어려운 부품이라 판단해 ORM인 Toasty부터 시작했고 Toasty는 2026년 4월부터 쓸 수 있으며 로드맵의 다음 단계가 웹 프레임워크라고 밝힌다.

핵심 설계 아이디어는 `$(...)` 표현식이다.
타입 검사된 일반 Rust 코드를 서버 초기 렌더링에서 실행하면서 동시에 JavaScript로 변환해 브라우저에서도 재실행되게 한다.
WASM 번들도 클라이언트 빌드 단계도 없다.

```rust
view! {
    signal open = false;

    <button @click=$(|_e| open.set(!open.get()))>"What is Topcoat?"</button>
    <p :hidden=$(!open.get())>"A fullstack Rust framework."</p>
}
```

서버 왕복이 필요한 컴포넌트는 `#[shard]`로 선언한다.
`$(...)` 인수가 바뀔 때 서버에서 재렌더링하고 HTML을 교체하며, 발표 글은 shard를 라우터에서 API 엔드포인트를 노출하는 특별한 종류의 컴포넌트라고 설명한다.

```rust
#[shard]
async fn search_results(cx: &Cx, query: String) -> Result {
    view! {
        <ul>
            for product in search_products(cx, &query).await? {
                <li>(product.name)</li>
            }
        </ul>
    }
}
```

발표 글은 Leptos와 Dioxus를 명시적으로 대비 대상으로 든다.
그 프레임워크들은 코드를 WebAssembly로 컴파일해 브라우저에서 실행함으로써 고도로 상호작용적인 웹 애플리케이션을 만드는 데 훌륭하지만, 많은 애플리케이션은 그 수준의 상호작용성을 필요로 하지 않으며 그런 경우에는 별도 타깃으로 컴파일하고 번들 크기와 분할을 걱정하고 클라이언트와 서버 경계로 데이터를 직렬화하는 것이 부담이 된다는 것이다.
Topcoat은 모든 마크업을 서버에서 렌더링하므로 컴포넌트가 비동기일 수 있고 데이터베이스에 접근하거나 사용자 권한을 안전하게 검증할 수 있으며, 반응성은 완전히 타입 검사된 Rust 표현식의 부분 집합을 매크로로 JavaScript에 교차 컴파일해 더한다고 설명한다.
반응성 모델 자체는 “HTMX와 발상이 비슷하게” 서버에서 HTML 조각을 렌더링하고 메타데이터로 반응 명령을 붙이는 방식이라고 규정한다.
같은 글은 클라이언트 반응성 시스템이 아직 초기 개발 단계이고 몇 가지 한계가 있으며 그동안 HTMX와 Alpine.js 통합을 쓸 수도 있다고 밝힌다.

모듈 기반 라우팅은 앱의 모듈 구조에서 라우트 트리를 빌드 단계 없이 선택적으로 유추한다.
`src/app.rs`가 `/`와 루트 `<html>` 레이아웃이 되고, `src/app/posts/id.rs`가 `/posts/{post_id}`로, 밑줄이 붙은 `_marketing.rs`는 URL 세그먼트 없는 레이아웃이 된다.
에셋 번들러는 컴파일된 바이너리에서 `asset!` 호출을 스캔해 파일을 복사하거나 내려받아 로컬 에셋 디렉터리에 모으고 콘텐츠 해시 URL로 공격적인 브라우저 캐싱과 함께 제공한다.
Fontsource와 Iconify 통합으로 웹 폰트와 아이콘 세트를 Rust 상수로 선언할 수 있고, `tailwind` 기능을 켜면 Node 없이 Tailwind가 에셋 파이프라인에 연결된다.

Topcoat UI는 shadcn/ui에서 영감을 받은 Tailwind 기반 컴포넌트 라이브러리로, `topcoat ui` CLI 명령으로 컴포넌트를 프로젝트에 복사해 오므로 디자인과 기능을 자유롭게 바꿀 수 있다.
그 밖에 문서화된 것으로는 요청 컨텍스트 `Cx`, 타입으로 키를 삼아 요청 간에 오래 사는 값을 공유하는 앱 컨텍스트, 요청 단위 캐싱과 팬아웃 중복 제거를 하는 `#[memoize]`, 미들웨어 대신 함수로 인증 같은 요청 범위 관심사를 모델링하는 방식, 서명·암호화·접두사 쿠키, 저장소를 직접 가져오는 세션 인증, 브라우저에서 호출 가능한 비동기 서버 함수인 `#[procedure]`, `mail!` 매크로와 SMTP·파일·인메모리 전송이 있다.
서드파티 통합으로는 Tailwind 외에 htmx, Alpine AJAX, Datastar가 있다.
로드맵에는 `topcoat new` CLI, 정적 내보내기, Toasty 통합 강화, 검증, 지역화, OpenAPI 엔드포인트, 사이트맵, 배포 문서, 스트리밍 SSR/서스펜스, 클라이언트 사이드 내비게이션, 이미지 최적화, 인증, 백그라운드 작업, 아일랜드 등 19개 항목이 나열되어 있다.

## 분석

### `$(...)` 표현식이 해결하는 문제와 그 대가

전통적인 서버 사이드 렌더링에서 클라이언트 반응성을 추가하려면 JavaScript 레이어가 필요하고, 두 코드베이스 간의 동기화 문제가 생긴다.
SPA 아키텍처는 이를 클라이언트 전체 렌더링으로 해결했지만 서버 로직과의 분리 비용이 컸다.
Next.js나 Remix 같은 메타프레임워크는 두 레이어 사이에 타입 안전한 API 계층을 제공하지만 복잡도는 여전히 높다.

`$(...)`의 접근은 다르다.
“이 Rust 코드가 서버와 브라우저에서 모두 의미 있는 코드”라는 교집합을 정의하는 것이다.
단순 상태 토글 같은 클라이언트 로직은 JavaScript로 변환하고, 데이터베이스 접근이 필요한 경우는 `#[shard]`로 서버 왕복을 표현한다.
개발자는 이 두 가지만 구분하면 된다.

그 교집합이 얼마나 넓은지가 이 프레임워크의 표현력을 결정하는데, Lobste.rs의 `goldstein`이 실제 구현을 확인해 답을 내놓았다.
“JavaScript로 어떻게 번역하는가”가 자기 즉각적인 질문이었고 답은 “아주 수동으로, AST 수준에서”였다는 것이다.
Rust의 구문 구성이 비슷한 JS 구성으로 직접 번역되므로, 자기가 놓친 것이 없다면 바깥 문맥의 함수를 호출할 수 없을 것이고 그 정의가 당연히 접근 불가능하기 때문이며, 따라서 이것은 정말로 “일반 Rust”가 아니라 쉬운 구문 대응을 갖는 Rust의 부분 집합이라는 결론이다.[^goldstein]

이 확인이 README의 표현을 정확히 좁힌다.
“타입 검사된 일반 Rust”라는 문구는 참이지만 그것은 컴파일러가 그 표현식을 검사한다는 뜻이지 임의의 Rust를 쓸 수 있다는 뜻이 아니다.
발표 글이 “완전히 타입 검사된 Rust 표현식의 부분 집합”이라고 쓴 것이 더 정확한 서술이며, README 쪽 표현이 한 단계 넓게 잡혀 있다.

### Toasty를 먼저 낸 순서가 이 프로젝트의 논리를 드러낸다

이 프레임워크에 데이터베이스 계층이 없다는 지적은 HN 스레드의 최상위 댓글이었고 여러 갈래에서 반복되었다.
`newaccountman2`는 자신이 Rust 웹 프레임워크 생태계에서 느끼는 고통을 이것이 해결해 주는 것 같지 않으며 DB 계층에 대한 것이 아무것도 없는데 어떻게 풀스택이냐고 물었다.[^newaccountman2]
`carllerche`의 답은 곧 Toasty ORM과 더 긴밀히 통합될 것이고 예를 들어 폼에서 레코드로 가는 흐름이 촘촘해질 것이며 지금 출시하는 것은 사용례를 얻기 위해서라는 것이었다.[^carllerche-toasty]
같은 답이 스레드에서 최소 다섯 번 반복된다.[^carllerche-migrations][^carllerche-roadmap][^carllerche-rails][^carllerche-built]

발표 글을 읽으면 이 반복이 우연이 아니라 순서의 결과임이 드러난다.
Carl은 가장 어려운 부품이라 판단해 ORM인 Toasty부터 시작했고 그것이 2026년 4월부터 쓸 수 있는 상태이며 로드맵의 다음 단계가 웹 프레임워크였다고 밝힌다.
글의 마지막 문단도 “데이터베이스가 필요하면 Toasty를 가져오라”로 끝난다.
즉 이 프로젝트의 설계자 관점에서 ORM은 빠진 것이 아니라 이미 나온 것이고, Topcoat은 그 위에 얹히는 두 번째 조각이다.

이 순서가 의미하는 바가 크다.
대부분의 풀스택 프레임워크는 웹 계층에서 출발해 데이터 계층을 나중에 붙이거나 남의 것을 감싼다.
Rails가 Active Record를 처음부터 품고 시작한 것이 예외적이었고, 그 선택이 Rails의 정체성을 만들었다.
Carl이 Rails 초기에 관여했던 사람이라는 사실[^carllerche-old]과 ORM을 먼저 낸 결정이 무관하지 않아 보인다.
다만 아직 두 조각이 붙지 않았다는 것이 현재 상태이고, 그 간격이 다음 절의 비판을 낳는다.

### AI가 언어 선택의 계산을 바꿨다는 명제가 이 프레임워크의 전제다

발표 글에서 가장 이례적인 대목은 기술 설명이 아니라 시장 분석이다.
웹 앱 생태계가 JavaScript와 Ruby와 PHP에 몰린 이유가 그 언어들이 생산성에 집중했기 때문이고 성능은 있으면 좋은 것이었는데, AI가 학습 장벽과 생산성 격차를 지워 버렸으므로 이제 차이를 만드는 것은 언어가 아니라 사용 가능한 라이브러리 집합이라는 논지다.
그리고 그 결론이 곧바로 행동 지침이 된다.
Rust에 없는 것은 언어의 매력이 아니라 라이브러리이므로 라이브러리를 만들면 된다는 것이다.

이 전제가 설계에도 직접 반영되어 있다.
발표 글의 “행위의 지역성을 지침 원리로” 절은 사람과 AI 모두 작은 코드 영역을 가로질러 추론하는 데 더 능하다는 문장으로 시작한다.
컴포넌트가 인수로 데이터를 받는 대신 스스로 데이터를 가져오게 권장하고, 중복 조회를 막기 위해 React의 `cache`에서 영감을 받은 요청 단위 `#[memoize]`를 두고, 인증도 코드베이스의 완전히 다른 곳에 있고 실행될지 안 될지 모르는 미들웨어에 의존하는 대신 컴포넌트 안에서 데이터를 직접 보호하게 한다.
설계 판단의 근거로 AI의 추론 특성이 명시적으로 인용되는 프레임워크 문서는 아직 드물다.

이 전제가 Rust 진영 바깥에서 어떻게 읽히는지도 기록해 둘 만하다.
Lobste.rs에서 두 개의 Topcoat 스레드는 모두 `rust` 태그와 함께 `vibecoding` 태그로 분류되었다.
`ssokolow`는 “반응성 없는 WebAssembly” 절이 이전에 가졌던 가장 큰 의문에 답해 주어 고맙다고 하면서도, 3년 전이라면 미쳤다는 소리를 들었을 것이라는 도입부에는 유보를 표했다.[^ssokolow-blog]
전제를 받아들이지 않는 독자에게는 이 글의 나머지가 근거 없는 확신으로 읽힐 수 있다는 뜻이다.

### 모듈 기반 라우팅의 절충

파일 시스템 구조에서 라우트를 유추하는 것은 Next.js와 SvelteKit과 Remix가 정착시킨 패턴이다.
Topcoat은 이것을 Rust 모듈 시스템에 적용하되 빌드 단계 없이 매크로로 처리하고, 선택 사항으로 두어 수동 라우터도 함께 지원한다.
직관적이고 설정이 적다는 장점이 있다.

대가는 유연성이다.
도메인 모델과 URL 구조가 자연스럽게 일치하지 않을 때 파일 시스템 기반 라우팅은 제약이 된다.
대규모 애플리케이션에서 라우트와 도메인 로직이 얽혀 있을 때 이 구조가 어떻게 작동하는지는 더 많은 실전 경험이 필요하다.

## 비평

### “배터리 포함”의 기준을 프로젝트 자신이 낮춰 잡았다

Toasty가 존재한다는 사실은 ORM 부재라는 비판을 반박하지만 완전히 해소하지는 못한다.
`hoistbypetard`가 문제를 정확히 세웠다.
이것은 ORM도, ORM 없이 만드는 것에 대한 논거도 빠져 있어 보이며, ORM이 없거나 그것이 비목표인 이유와 무엇이 그 관례를 대신하고 자동 생성 관리자 페이지 같은 것을 어떻게 가능하게 하는지에 대한 아주 잘 정리된 진술이 없다면 무언가를 “완전한 풀스택 프레임워크”라고 부르기 어렵겠다는 것이다.
ORM이 반드시 필요하다고 보지는 않지만 그 방향으로 간다면 사람들이 대신 무엇을 해야 하고 그것 없이 배터리가 어떻게 포함되는지를 말해야 한다고 덧붙였다.[^hoistbypetard]
`carllerche`는 ORM이 여기 있다며 Toasty 링크를 주고 긴밀한 통합이 단기 로드맵에 있다고 답했다.[^carllerche-orm]

이 답변이 놓치는 것은 `hoistbypetard`가 요구한 것이 링크가 아니라 문서라는 점이다.
README 어디에도 Toasty가 언급되지 않는다.
로드맵의 “Better Toasty integration” 한 줄이 유일한 흔적이고, 그것도 이미 통합되어 있다는 전제로 읽히는 표현이다.
“배터리 포함”이라고 자칭하는 프레임워크의 README가 데이터 계층에 대해 아무 말도 하지 않는 상태에서, 답이 스레드 댓글에만 있다면 그것은 배터리가 별매라는 사실을 문서가 숨기고 있는 것이다.

무엇이 빠졌는지에 대한 요구 목록도 스레드에서 반복적으로 같은 형태였다.
`the__alchemist`는 자신이 Rust를 임베디드와 PC 애플리케이션과 생화학 분야에서 쓰는 애호가이지만 웹 개발만은 여전히 Python으로 하며 Django 수준의 것이 없기 때문이라면서, 자동 마이그레이션과 관리자와 이메일과 인증 같은 빠진 측면을 이것이 해결해 주지 못한다고 했다.[^alchemist]
`frio`는 자신이 htmx 스타일 풀스택 앱으로 해결되는 문제는 아주 적고 생성된 관리자와 인증 프레임워크와 캐싱과 이벤팅으로 해결되는 문제가 많다며 Django에 상당하는 것이라면 많은 것을 내놓겠다고 했다.[^frio]
`mamcx`도 가장 중요한 것이 자동 관리자이고 그다음이 `auth`이며 가장 큰 고통은 모든 것이 ORM과 자동 관리자에 얽혀 있는 것이라고 적었다.[^mamcx]
같은 스레드에서 `m4tx`는 완전한 배터리 포함 프레임워크의 부재가 Rust에서 자기 가장 큰 불만이었고 그래서 Django에 강하게 영감을 받아 자동 마이그레이션과 관리자 패널과 인증을 지원하는 `cot.rs`를 만들어 왔다고 두 번 소개했다.[^m4tx]

`az09mugen`이 이 상황을 한 문장으로 정리했다.
“완전한 풀스택(full fullstack)”이라는 표현을 쓴다는 사실 자체가 풀스택이라는 단어가 시간이 지나며 의미를 잃었다는 뜻이며, 그래서 이제 풀스택이 무슨 뜻이냐는 것이다.[^az09mugen]
`BobbyTables2`도 풀스택이 요즘은 정말 “웹서버 더하기 웹페이지”를 뜻하느냐고 물었다.[^bobbytables]

### tokio-rs 조직 소속이라는 신호가 사실은 CI 할당량의 산물이었다

Topcoat이 tokio-rs 조직에 있다는 사실은 이 프로젝트가 받은 초기 관심의 상당 부분을 설명한다.
Tokio는 Rust 비동기 생태계의 사실상 표준 런타임이고 Axum과 Tonic과 Tower도 같은 조직에 있으므로, 그 이름 아래 풀스택 프레임워크가 나왔다는 것은 표준 스택의 예고처럼 읽힌다.

`hobofan`이 그 읽기를 경계했다.
Tokio 프로젝트가 만든 많은 것의 팬이고 Axum의 만족한 사용자이지만, Topcoat이나 그들의 ORM 같은 프로젝트가 이 프로젝트에 좋은 방향인지 확신이 서지 않으며 그것들이 실질보다 이름값에 근거해 과도한 채택을 얻게 될까 우려된다는 것이다.[^hobofan]

`carllerche`의 답이 이 우려를 반박하는 대신 그 전제를 무너뜨렸다.
Topcoat과 Toasty가 분리되어 나갈 가능성이 매우 높다고 보며 그것은 그저 일의 문제인데, 특히 tokio-rs가 기본 GitHub 조직보다 CI 사용량을 더 많이 쓸 수 있기 때문이라는 것이다.[^carllerche-split]
앞서 저장소 공개 시점도 비공개 CI 사용량 소진 때문이었다는 설명과 합치면, 이 프로젝트가 tokio-rs 아래 있는 이유는 전략이 아니라 인프라 할당량이다.

이 사실이 두 방향으로 작용한다.
한편으로는 `hobofan`의 우려가 정당했음을 보여 준다.
독자들이 조직 이름에서 읽어 낸 보증은 애초에 의도된 신호가 아니었고, 그럼에도 4개월 만에 4,378개의 스타를 모으는 데 기여했다.
다른 한편으로는 이 프로젝트가 Tokio의 공식 로드맵이 아니라는 뜻이기도 하다.
발표 글이 “Axum은 어떻게 되는가”라는 절을 따로 두어 Topcoat과 Axum이 아주 다른 용도를 다루며 많은 Topcoat 사용자가 프로젝트 안에서 Axum도 함께 쓰게 될 것이라고 명시한 것도 같은 정리다.
`valorzard`가 Tokio가 Rust의 Spring Boot가 되어 가는 것 아니냐고 물었을 때[^valorzard] `carllerche`가 런타임으로서의 Tokio는 가볍고 안정적이며 조직으로서의 Tokio는 Rust로 클라이언트와 서버 앱을 만드는 생태계 전체를 만들고 유지하는 개발자 집합이라고 답한 것[^carllerche-spring]은 그 구분을 지키려는 서술이다.

### 두 런타임에서 같은 코드를 돌린다는 약속에 의미 차이가 숨어 있다

`jdw64`가 이 프레임워크에 대한 가장 구체적인 기술적 반론을 냈다.
`$(...)` 같은 문법을 보면 Rust AST를 JS 안에 넣는 트랜스파일러처럼 보이고 이미 끔찍한 Rust 개발자 경험을 더 나쁘게 만들 것 같으며, 구체적으로 서버 쪽 문자열 길이 값이 다를 것 같다고 `len()`을 지목했다.[^jdw64]
이어진 댓글에서 더 정확히 짚었다.
Rust의 `str::len()`을 호출하면서 JS의 `String.length`를 쓰는 것 같은데 앞의 것은 UTF-8 기준이고, API 쪽에서는 유니코드 문자열이 보통 네 가지이므로 Rust식 스네이크 케이스로 `len()`과 `utf16_len()` 같은 함수를 따로 두어야 할지 모르겠지만 라이브러리와 브라우저 사이의 추상을 어떻게 다룰지는 모르겠다는 것이다.[^jdw64-len]

이 지적이 아픈 이유는 `$(...)`의 가치 제안 자체를 겨냥하기 때문이다.
같은 코드가 서버와 브라우저에서 모두 돌아간다는 약속의 값어치는 두 실행이 같은 결과를 낸다는 데 있다.
그런데 Rust의 `str::len()`은 UTF-8 바이트 수를 반환하고 JavaScript의 `String.length`는 UTF-16 코드 단위 수를 반환하므로, ASCII 바깥의 문자열에서 두 값이 갈린다.
한글 한 글자는 Rust에서 3, JavaScript에서 1이다.
초기 서버 렌더링과 브라우저 재실행이 다른 결과를 내는 종류의 버그이며, 타입 시스템이 잡아 주지 않는 종류이기도 하다.

`carllerche`의 답변은 이 지점을 다루지 않았다.
설계 의견 차이에 기분 상하지 않으며 Topcoat의 목표는 의견이 뚜렷한 것이고 모두를 행복하게 만드는 것이 아니라고, JS 라이브러리들이 많은 것을 제대로 해 왔고 브라우저 앱 공간에서 수년의 경험이 있어 무거운 영감이 되었다고, 마음에 들지 않으면 Axum이 누구나 자기 추상을 그 위에 쌓을 수 있는 저수준 HTTP 라우터를 지향한다고 답했다.[^carllerche-opinion]
`jdw64`가 기분 상하게 했다면 미안하다며 `len()` 부분을 확인해 달라고 다시 요청했지만[^jdw64-len] 답은 달리지 않았다.

이것이 앞서 `goldstein`이 확인한 AST 수준 번역과 같은 문제의 두 얼굴이다.
구문을 대응시키는 방식은 구현이 단순하고 빠르지만 의미론까지 대응시키지는 않는다.
`$(...)` 안에서 무엇이 정확히 같은 값을 내고 무엇이 그렇지 않은지의 목록이 이 프레임워크에서 가장 중요한 문서가 될 텐데, 현재는 존재하지 않는다.

### 서버 중심 아키텍처의 트레이드오프

Topcoat은 서버 사이드 렌더링을 기반으로 클라이언트 반응성을 추가하는 모델이다.
이 접근은 SEO와 초기 로드 성능과 데이터베이스 접근 단순화에서 유리하고, 발표 글이 강조하듯 컴포넌트가 비동기로 권한을 검증할 수 있다는 보안상 이점도 있다.

반면 오프라인 동작이나 로컬 우선 데이터 동기화나 복잡한 실시간 협업 같은 시나리오에서는 클라이언트 중심 SPA가 더 자연스럽다.
Topcoat이 이런 사용 사례를 커버하려면 추가 추상화가 필요하고, 그러면 단순성이라는 핵심 가치와 충돌할 수 있다.
로드맵에 스트리밍 SSR과 서스펜스와 클라이언트 사이드 내비게이션과 아일랜드가 함께 올라 있다는 사실이 그 압력을 이미 보여 준다.

반대 방향의 우려도 나왔다.
Lobste.rs의 `ssokolow`는 이것이 클라이언트와 서버 경계를 흐리는 방식에 기반한 또 하나의 프레임워크로 보이며, uMatrix나 NoScript가 있는 환경에서 우아한 성능 저하를 확인하려는 자기 같은 개발자에게는 그런 방식이 추가 작업과 추가 함정을 만든다고 적었다.
그리고 하이드레이션이 있는 서버 사이드 렌더링을 어떻게 하는지에 대한 문서를 놓친 것이 아니라면 Sycamore와 Leptos 같은 이 분야의 더 성숙한 항목과 비교해 무슨 가치 제안이 있는지 모르겠다고 했다.[^ssokolow-repo]
`$(...)`가 JavaScript로 번역된다는 사실은 JavaScript가 꺼진 환경에서 그 상호작용이 사라진다는 뜻이고, 문서는 이 경우의 동작을 규정하지 않는다.

## 인사이트

### AI가 생산성 격차를 지운다는 전제는 이 프레임워크의 해자도 함께 지운다

발표 글의 논증을 한 번 더 밀어 보면 흥미로운 자기모순이 나온다.
전제는 AI가 학습 장벽과 생산성 격차를 지우므로 언어가 아니라 라이브러리가 차이를 만든다는 것이다.
그렇다면 “배터리 포함”이라는 가치는 어디서 오는가.

배터리 포함 프레임워크의 값어치는 역사적으로 두 가지였다.
하나는 결정을 대신 내려 주어 초보자의 인지 부담을 줄이는 것이고, 다른 하나는 관례를 공유해 코드베이스 사이의 이동 비용을 낮추는 것이다.
전자는 AI가 상당 부분 흡수한다.
어떤 라우팅 방식을 고를지, 세션을 어떻게 저장할지 같은 결정은 도구에게 물어 즉시 관례적인 답을 얻을 수 있다.
후자는 남지만, 그것은 프레임워크가 널리 쓰일 때만 성립하는 가치다.

역설은 여기서 나온다.
AI가 언어 학습 장벽을 지운다는 주장이 참이라면 Rust로 웹을 만드는 것을 막던 장벽도 프레임워크가 아니라 도구가 치우게 된다.
Axum과 sqlx로 직접 조립하는 비용이 AI 덕에 충분히 낮아진다면, 조립을 대신해 주는 프레임워크의 상대적 가치는 그만큼 줄어든다.
`carllerche`가 Topcoat의 존재 이유로 든 것이 “이미 인프라 수준이나 성능 민감한 이유로 Rust를 쓰는 조직이 자기가 이미 쓰는 언어로 웹 앱을 만들고 싶어 한다”는 것[^carllerche]이었는데, 이 이유는 AI 논증과 별개로 성립하며 오히려 더 튼튼하다.
두 논거가 같은 글에 있지만 서로를 필요로 하지 않는다.

그렇다면 이 프레임워크가 AI 시대에 실제로 얻는 것은 무엇인가.
발표 글의 “행위의 지역성” 절이 답을 갖고 있다.
사람과 AI 모두 작은 코드 영역을 가로질러 추론하는 데 더 능하므로 로직을 지역적이고 조합 가능하게 유지한다는 설계 원리다.
이것은 생산성 주장이 아니라 검증 가능성 주장이며, 컴포넌트가 자기 데이터를 스스로 가져오고 자기 권한을 스스로 확인하는 구조는 에이전트가 한 파일만 읽고도 그 코드의 안전성을 판단할 수 있게 만든다.
미들웨어가 실행될지 안 될지 모른다는 지적이 정확히 그 반대 사례다.
AI 시대의 프레임워크 설계에서 진짜 축은 코드를 덜 쓰게 하는 것이 아니라 코드의 문맥 의존성을 줄이는 것일 수 있고, Topcoat은 그것을 명시적으로 표방한 드문 사례다.

### 이 스레드에서 무너진 것은 프레임워크가 아니라 “풀스택”이라는 단어다

`az09mugen`의 지적을 진지하게 받아들이면 이 논쟁의 성격이 달라진다.
“완전한 풀스택”이라는 표현이 필요했다는 사실 자체가 “풀스택”만으로는 아무것도 구별되지 않는다는 뜻이다.

이 단어의 의미가 실제로 갈라져 있다.
Topcoat이 뜻하는 풀스택은 서버와 브라우저를 한 언어로 다룬다는 뜻이며, 그래서 `$(...)`와 `#[shard]`가 핵심 기능이 된다.
스레드에서 Django를 요구한 사람들이 뜻하는 풀스택은 데이터베이스에서 관리자 화면까지의 수직 스택이 갖춰졌다는 뜻이며, 그래서 자동 마이그레이션과 관리자와 인증이 핵심 기능이 된다.
두 정의는 겹치지 않는다.
Django에는 `$(...)`에 해당하는 것이 없고 Topcoat에는 `django.contrib.admin`에 해당하는 것이 없는데, 양쪽 다 자기를 풀스택이라 부른다.

이 갈라짐에는 역사가 있다.
2000년대 중반의 풀스택 프레임워크는 데이터베이스와 HTML 사이의 수직축을 뜻했고, 브라우저는 프레임워크의 관심사가 아니었다.
SPA 시대에 축이 90도 돌아가 서버와 클라이언트라는 수평축이 되었고, Next.js 이후 “풀스택”은 대개 그쪽을 뜻하게 되었다.
Topcoat은 수평축의 언어로 말하고 있고 Django를 요구하는 사람들은 수직축의 언어로 답하고 있으며, 두 진영이 같은 스레드에서 서로 다른 질문을 하고 있다.

여기서 나오는 실천적 결론은 이 프레임워크를 평가할 때 두 축을 분리하라는 것이다.
수평축에서 Topcoat의 경쟁자는 Leptos와 Dioxus이고, 발표 글이 그 둘을 명시적으로 대비 대상으로 삼은 것은 정확한 자리 잡기다.
수직축에서 경쟁자는 Loco.rs와 `cot.rs`이고, `carllerche`가 Loco와의 차이를 묻는 질문에 둘 다 배터리 포함을 지향하지만 각 프로젝트에 그것이 아주 다른 것을 뜻한다고 답한 것[^carllerche-loco]이 그 인식을 보여 준다.
문제는 README의 표제가 수직축의 언어를 쓴다는 것이고, 그래서 수직축 사용자들이 몰려와 없는 것을 세게 된다.

### `view!` 매크로 기반 템플릿의 위험은 아직 검증되지 않았다

Rust 매크로는 강력하지만 디버깅과 컴파일 오류 메시지가 어렵다는 오랜 문제가 있다.
`view!` 같은 DSL 매크로에서 오류가 나면 메시지가 매크로 내부를 가리키며 원인 파악이 어려울 수 있다.
Lobste.rs의 `lightandlight`가 그 우려를 짧게 표현했다.
Rust 토큰으로 정의된 템플릿 언어라며 오류 메시지가 좋기를 바란다는 것이다.[^lightandlight]

이 우려가 이 프레임워크에서 특히 무거운 이유는 매크로가 하나가 아니기 때문이다.
`view!`, `attributes!`, `class!`, `asset!`, `mail!`, `expr!`이 있고 `#[page]`, `#[component]`, `#[shard]`, `#[procedure]`, `#[memoize]` 같은 속성 매크로가 있으며, `$(...)`는 그 안에서 다시 별도의 표현식 언어를 연다.
`topcoat fmt` CLI가 매크로 본문을 자동 서식화하는 도구로 제공된다는 사실 자체가 이 매크로들이 일반 Rust 도구 체계 바깥에 있다는 증거다.
`rustfmt`가 손대지 못하니 전용 포매터가 필요했던 것이다.

같은 논리가 다른 도구로도 이어진다.
`rust-analyzer`가 `view!` 안에서 얼마나 잘 동작하는지, 자동 완성과 정의로 이동과 타입 힌트가 매크로 경계를 넘는지가 실사용 경험을 좌우할 텐데 어느 문서에도 언급이 없다.
Leptos와 Dioxus가 같은 문제를 겪어 왔고, 그것이 두 프레임워크에 대한 가장 흔한 불만 중 하나다.
`Arch`가 Leptos를 써 보고 `wasm-bindgen`과 씨름하며 답답했던 경험 때문에 이 프레임워크에 처음부터 낙관적이라고 적었지만[^arch], 그가 피하려던 문제와 매크로 도구 지원 문제는 다른 문제다.

### 이 프로젝트의 실제 시험대는 첫 브레이킹 체인지가 아니라 Toasty 통합이다

“브레이킹 체인지가 예상된다”는 명시는 정직하지만, 조기 단계 프레임워크에서 그것은 예상된 비용이지 위험이 아니다.
더 큰 위험은 다른 데 있다.

앞서 정리했듯 이 프로젝트의 논리는 Toasty를 먼저 내고 Topcoat을 그 위에 얹는 것이었고, 로드맵의 “Better Toasty integration”은 폼에서 레코드로 가는 흐름, 곧 모든 필드를 나열하지 않고 폼에서 레코드를 안전하게 만들고 갱신하는 것을 목표로 한다.
이것이 실제로 이 프로젝트가 Rails나 Django의 자리를 노릴 수 있는지를 가르는 지점이다.
자동 관리자 화면도, 검증도, 마이그레이션 연계도 전부 웹 계층이 데이터 모델을 알아야 성립하기 때문이다.

그런데 두 조각을 붙이는 일이 각각을 만드는 일보다 어려울 수 있다.
Rails의 Active Record가 강력했던 이유는 ORM이 좋아서가 아니라 폼 헬퍼와 검증과 라우팅이 모두 같은 모델 객체를 중심으로 설계되었기 때문이며, 그 결합은 나중에 붙일 수 있는 것이 아니라 처음부터 같은 사람이 같은 시기에 설계해야 나온다.
Toasty와 Topcoat은 다른 시기에 다른 사람이 주도해 만들어졌고, 발표 글의 서술대로라면 Julien Scholz가 Topcoat을 만드는 동안 Toasty는 이미 완성 단계였다.

통합 방식에 따라 이 프레임워크의 성격이 갈릴 것이다.
Toasty의 모델 타입이 `view!`와 폼 매크로에서 일급으로 다뤄지면 Rails 계열의 수직 통합에 가까워지고, 단지 함께 쓸 수 있는 두 크레이트로 남으면 README가 이미 강조한 모듈성은 지켜지지만 “배터리 포함”이라는 주장은 계속 반박당한다.
`carllerche`가 Topcoat이 모듈식이라 Toasty를 갈아 끼울 수 있다고 밝힌 것[^carllerche-loco]은 후자 쪽 설계 의지를 시사하며, 그것이 옳은 선택일 수도 있지만 그렇다면 표제의 “완전한 풀스택”은 다른 말로 바뀌어야 한다.
지금 이 프로젝트에서 가장 정보량이 큰 사건은 다음 릴리스가 아니라 그 통합이 어떤 모양으로 나오느냐다.

---

[^carllerche]: HN `carllerche`, <https://news.ycombinator.com/item?id=48953076>

[^goldstein]: Lobste.rs `goldstein`, <https://lobste.rs/s/zmg7ot/topcoat_batteries_included_framework#c_okolao>

[^newaccountman2]: HN `newaccountman2`, <https://news.ycombinator.com/item?id=48952415>

[^carllerche-toasty]: HN `carllerche`, <https://news.ycombinator.com/item?id=48953091>

[^carllerche-migrations]: HN `carllerche`, <https://news.ycombinator.com/item?id=48953506>

[^carllerche-roadmap]: HN `carllerche`, <https://news.ycombinator.com/item?id=48953619>

[^carllerche-rails]: HN `carllerche`, <https://news.ycombinator.com/item?id=48953718>

[^carllerche-built]: HN `carllerche`, <https://news.ycombinator.com/item?id=48953842>

[^carllerche-old]: HN `carllerche`, <https://news.ycombinator.com/item?id=48954010>

[^ssokolow-blog]: Lobste.rs `ssokolow`, <https://lobste.rs/s/l8hiip/announcing_topcoat_framework_for#c_u2a0m3>

[^hoistbypetard]: HN `hoistbypetard`, <https://news.ycombinator.com/item?id=48954650>

[^carllerche-orm]: HN `carllerche`, <https://news.ycombinator.com/item?id=48954758>

[^alchemist]: HN `the__alchemist`, <https://news.ycombinator.com/item?id=48953363>

[^frio]: HN `frio`, <https://news.ycombinator.com/item?id=48953662>

[^mamcx]: HN `mamcx`, <https://news.ycombinator.com/item?id=48954148>

[^m4tx]: HN `m4tx`, <https://news.ycombinator.com/item?id=48967075>

[^az09mugen]: HN `az09mugen`, <https://news.ycombinator.com/item?id=48957730>

[^bobbytables]: HN `BobbyTables2`, <https://news.ycombinator.com/item?id=48953601>

[^hobofan]: HN `hobofan`, <https://news.ycombinator.com/item?id=48953279>

[^carllerche-split]: HN `carllerche`, <https://news.ycombinator.com/item?id=48953304>

[^valorzard]: HN `valorzard`, <https://news.ycombinator.com/item?id=48955086>

[^carllerche-spring]: HN `carllerche`, <https://news.ycombinator.com/item?id=48955205>

[^jdw64]: HN `jdw64`, <https://news.ycombinator.com/item?id=48953925>

[^jdw64-len]: HN `jdw64`, <https://news.ycombinator.com/item?id=48954062>

[^carllerche-opinion]: HN `carllerche`, <https://news.ycombinator.com/item?id=48954006>

[^ssokolow-repo]: Lobste.rs `ssokolow`, <https://lobste.rs/s/zmg7ot/topcoat_batteries_included_framework#c_8b4oop>

[^carllerche-loco]: HN `carllerche`, <https://news.ycombinator.com/item?id=48954637>

[^lightandlight]: Lobste.rs `lightandlight`, <https://lobste.rs/s/l8hiip/announcing_topcoat_framework_for#c_n8ssoq>

[^arch]: Lobste.rs `Arch`, <https://lobste.rs/s/l8hiip/announcing_topcoat_framework_for#c_z29kaa>
