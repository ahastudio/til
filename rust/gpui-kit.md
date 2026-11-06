# GPUI Kit: Longbridge가 GPUI 위에 만든 75개 이상의 컴포넌트와 접근성 약속

<https://gpui-kit.com/>

<https://github.com/longbridge/gpui-kit>

HN 토론: <https://news.ycombinator.com/item?id=45719004> (515점, 218개 댓글)

HN 토론: <https://news.ycombinator.com/item?id=43942607> (3점, 1개 댓글)

GN 토론: <https://news.hada.io/topic?id=23960>

## 소개

GPUI Kit는 증권사 Longbridge가 만든 Rust 데스크톱 UI 컴포넌트 묶음이다.
홈페이지는 이를 프로덕션에서 쓰이는 Rust UI 프레임워크라고 소개하며,
75개가 넘는 컴포넌트와 프리미티브,
WebAssembly, 접근성, UI 통합 테스트, 데이터 테이블, 도킹, 차트,
코드 편집을 내세운다.
Zed가 만든 [GPUI](gpui.md) 위에서 동작한다고 밝힌다.

이 프로젝트는 이름이 바뀌었다.
2025년 10월에 Hacker News와 GeekNews에 올라온 글은 `gpui-component`라는
이름이었고
GeekNews의 요약에 따르면 컴포넌트가 60개 이상이었으며,
당시 저장소 지표는 별 5.4천 개, 포크 223개,
최신 릴리스는 v0.3.1(2025년 10월 27일)이었다.
지금 홈페이지는 이름이 GPUI Kit이고 최신 버전은 v0.9.0이다.
2026년 11월 6일 기준 GitHub 저장소는 별 19,428개, 포크 1,209개,
열린 이슈 148개이고 2024년 6월 13일에 만들어졌으며 마지막 푸시가 2026년 11월
5일이다.
홈페이지는 소프트웨어 소스와 문서의 코드 예제가 Apache-2.0이고
Longbridge가 개발했다고 밝히며 macOS, Windows, Linux,
WebAssembly를 지원한다고 한다.
GitHub는 라이선스를 Other(NOASSERTION)로 표시하는데,
저장소에 Apache 라이선스 파일과 문서용 라이선스 파일이 따로 있기
때문으로 보인다.
이 판단은 이 문서의 추정이다.

이 문서에서 말하는 기능과 성능은 모두 홈페이지에서 만든 사람이 한 주장이다.
이 문서는 GPUI Kit로 앱을 만들어 보지 않았다.

## 구조

홈페이지는 세 겹의 구조를 제시하며 시각 체계를 누가 소유할지 고르게 한다.

`gpui-component`는 완결된 시각과 상호작용 체계로,
제품의 일관성을 지키고 싶을 때 쓴다.
75개가 넘는 컴포넌트와 프리미티브, 밝고 어두운 테마가 들어 있다고 한다.

`gpui-base`는 스타일이 없는 프리미티브로,
포커스, 선택, 오버레이, 가상화의 동작을 재사용하면서 모든 픽셀을 직접 소유할
때 쓴다.
접근성 동작이 완전히 들어 있다고 한다.

`gpui-shell`은 JavaScript로 확장할 수 있게 한다.
호스트는 Rust이고 스크립트가 닿을 수 있는 것을 한 번에 하나씩 권한으로
준다고 한다.
기본으로 부여되는 권한은 없고 저장 시 즉시 다시 불러오며,
스크립트가 같은 프로세스에서 실제 인터페이스를 그린다고 한다.
홈페이지의 다른 곳은 이를 AI가 만든 UI를 네이티브로 렌더링하는 것이라고
소개한다.

홈페이지가 내세우는 기능은 다음과 같다.

| 기능           | 홈페이지의 설명                                                             |
| -------------- | --------------------------------------------------------------------------- |
| 데이터 테이블  | 가상 스크롤, 고정과 크기 조절이 되는 열, 정렬, 셀 선택, 수십만 행           |
| 가상화된 목록  | 보이는 범위만 렌더링해서 긴 목록도 부드럽게 스크롤                          |
| 코드 편집기    | 20만 줄에서도 안정적인 로프(rope) 텍스트, Tree-sitter 강조, LSP 진단과 완성 |
| 도킹 레이아웃  | 끌어서 재배치하고 확대할 수 있으며 직렬화 가능한 패널                       |
| 테마           | 의미 기반 토큰으로 구동되는 밝은 테마, 어두운 테마, 사용자 지정 테마        |
| WebAssembly    | `wasm32-unknown-unknown`으로 웹에서 실행하고 네이티브 구현을 공유           |
| 접근성         | AccessKit의 역할, 이름, 상태, 관계, 동작이 상호작용 계층에 내장             |
| UI 통합 테스트 | 헤드리스 창에 실제 컴포넌트를 그리고 입력을 보내 상태와 접근성을 확인       |

## 시작하기

`Cargo.toml`에 `gpui-kit = "0.9.0"`을 추가하고 `Render`를 구현한다.
홈페이지의 예제는 다음과 같다.

```rust
use gpui_kit::component::{button::*, *};

impl Render for HelloWorld {
    fn render(&mut self, _: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .v_flex()
            .gap_2()
            .items_center()
            .child("Hello, World!")
            .child(
                Button::new("ok")
                    .primary()
                    .label("Let's Go!")
                    .on_click(cx.listener(Self::go)),
            )
    }
}
```

## 비평

### 접근성은 새로 생긴 약속이고 이전에는 문제로 지적되었다

2025년 10월의 HN 스레드에서 kennydude는 스크린 리더에서 어떻게 작동하는지
궁금해했고,[^kennydude]
miki123211은 접근성이 Rust UI 프레임워크의 흔한 문제이며
접근성이 필요해지는 순간 앱 전체를 다시 써야 한다고 했다.[^miki123211]
andrewl-hn은 이 도구가 GPUI에 기반하고 Zed 편집기가 스크린 리더에는 불투명하다며
접근성이 필요하면 Slint나 Qt를 보라고 했다.[^andrewl-hn]
jeroenhd는 API 문서가 접근성을 언급하며 설명과 이름을 붙이는 한 컨트롤이 ARIA
규격에 맞아 보인다고 했다.[^jeroenhd]
지금 홈페이지는 AccessKit의 역할과 이름과 상태가 상호작용 계층에 내장되어
있다고 쓰고,
접근성을 검증하는 통합 테스트도 내세운다.
이 문서는 이 약속을 스크린 리더로 확인하지 못했고,
댓글들이 지적한 상황이 그 뒤에 해결되었는지는 홈페이지만으로 알 수 없다.
다만 접근성을 기능 목록의 앞쪽에 두고 테스트로 검증하겠다는 방향은
2025년의 비판에 대한 응답으로 읽힌다.

### 의존성 트리가 크다

WhyNotHugo는 가장 단순한 예제도 의존성이 천 개가 넘고
GTK와 GDK와 pango를 포함해 다른 툴킷에 의존한다는 점이 이상하다고
했다.[^WhyNotHugo]
nicce도 약 900개의 의존성이 마음에 걸린다고 했다.[^nicce]
dminik은 GNOME이 서버 측 창 장식을 구현하지 않아
libadwaita에 기댈 수밖에 없고 그것이 GTK 의존성을 끌어온다고 설명했고,[^dminik]
iknowstuff는 작고 조합 가능하고 감사할 수 있는 천 개의 의존성과
같은 양의 코드를 담은 하나의 덩어리 중 무엇을 택하겠느냐고
반문했다.[^iknowstuff]
UndyingHorse는 평균 바이너리 크기가 10MB인 이유를 물었고,
nicoburns는 Rust UI 툴킷이 최적화와 LTO를 켜고 ICU 데이터와 WGPU 렌더러와
SVG 렌더링을 포함하면 대체로 10~15MB가 나온다고
답했다.[^UndyingHorse][^nicoburns]
의존성 수는 보안과 빌드 시간의 비용이고 바이너리 크기는 배포의 비용이므로,
Electron 대안을 찾는 사람이 따져 볼 항목이다.

### GPUI가 아직 1.0이 아니고 Zed에 묶여 있다

GPUI Kit는 GPUI 위에 만들어져서 그 위험을 그대로 이어받는다.
[GPUI의 README](gpui.md)는 1.0 이전이라 호환을 깨는 변경이 잦다고 밝히고,
홈페이지는 기여가 Zed 저장소에서 이루어져야 한다고 한다.
GPUI Kit 자신도 0.x 버전이고 이름이 한 번 바뀌었다.
프레임워크의 기반과 컴포넌트 계층이 모두 1.0 이전이면,
버전을 올릴 때의 비용이 이중으로 든다.

### 네이티브라는 말은 OS 위젯을 쓴다는 뜻이 아니다

fidotron은 이것이 웹이 아니라는 뜻의 네이티브인지,
실제 네이티브 텍스트 입력과 스크롤 위젯을 쓴다는 뜻인지 물었다.[^fidotron]
nu11ptr는 웹이 아니라는 뜻이고 모든 것이 GPU API로 그려진다고
답했으며,[^nu11ptr-native]
hsn915는 네이티브 실행 파일이라는 뜻이지 OS 위젯이 아니라고 했다.[^hsn915]
운영 체제의 위젯을 쓰지 않으므로 입력기, 접근성, 시스템 메뉴, 글자 렌더링을
프레임워크가 직접 책임진다.
홈페이지의 접근성과 국제화 약속이 중요한 이유가 이것이다.

## 인사이트

### 동작은 기반이 갖고 모양은 애플리케이션이 갖는다

홈페이지는 원칙을 한 문장으로 밝힌다.
어려운 상호작용 동작(포커스, 오버레이 위치, 가상화,
접근성)은 기반 계층이 처리하고
어떻게 보이고 느껴질지는 제품이 정한다는 것이다.
이 구분은 UI 프레임워크의 오래된 문제인
스타일을 바꾸려다 접근성이 깨지는 상황을 막으려는 설계로 읽힌다.
접근성이 시각 요소 안에 섞여 있으면 디자인을 바꾸는 사람이 접근성을 부수고,
기반에 있으면 디자인을 마음껏 바꿔도 접근성이 남는다.
이 문서의 해석으로는 이 점이 GPUI Kit의 가장 흥미로운 구조적 선택이다.

### 정보 밀도가 높은 소프트웨어가 Rust GUI의 실제 수요를 만든다

홈페이지는 이를 정보 밀도가 높은 소프트웨어를 위해 만들었다고 소개하고
수십만 행의 표, 20만 줄의 코드 편집, 도킹 패널을 내세운다.
artursapek은 트레이딩 애플리케이션이 Rust GUI의 연구개발을 밀어붙이는 수요처인
듯하다며
자신의 팀이 Kraken의 데스크톱 앱을 Iced로 만들었고
웹뷰와 Rust GUI의 차이가 느껴지며 많은 요소를 그리면서도 높은 프레임률을
유지한다고 했다.[^artursapek]
증권사가 만든 컴포넌트와 거래소가 만든 데스크톱 앱이 모두 같은 요구에서 나왔다는
점이 공통이다.
화면에 변하는 숫자가 많은 도메인이 웹 기술의 한계를 먼저 드러낸다.

### 가장 큰 시험은 외부 앱의 채택이다

nu11ptr는 이 프로젝트가 가장 완성도 높은 컴포넌트 모음처럼 보이지만
사용이 거의 없다고 했다.[^nu11ptr]
그 뒤 1년 만에 별이 5.4천 개에서 약 1.9만 개로 늘었다는 것은 관심이
커졌다는 지표다.
다만 별이 실제 사용을 뜻하지는 않는다.
Discord가 전체 클라이언트를 GPUI로 옮긴다고 밝힌 것은
[이 생태계에 큰 외부 사용자가 생긴다는 신호](discord-rust-client.md)지만,
Discord가 GPUI Kit를 쓰는지는 알려지지 않았다.

### 결론을 바꿀 관찰

스크린 리더 사용자가 이 컴포넌트로 만든 앱을 실제로 쓸 수 있다는 보고가 나오면
접근성 약속이 확인된다.
Longbridge 밖의 이름 있는 앱이 GPUI Kit로 출시되면 채택이 입증된다.
GPUI와 GPUI Kit가 1.0에 이르거나 GPUI가 Zed에서 독립하면 이중 위험이 줄어든다.
`gpui-shell`의 권한 모델이 독립된 검토를 받으면 JavaScript 확장의 안전성이
판단된다.

---

[^kennydude]: <https://news.ycombinator.com/item?id=45719366>

[^miki123211]: <https://news.ycombinator.com/item?id=45720591>

[^andrewl-hn]: <https://news.ycombinator.com/item?id=45721492>

[^jeroenhd]: <https://news.ycombinator.com/item?id=45719918>

[^WhyNotHugo]: <https://news.ycombinator.com/item?id=45720705>

[^nicce]: <https://news.ycombinator.com/item?id=45719883>

[^dminik]: <https://news.ycombinator.com/item?id=45722143>

[^iknowstuff]: <https://news.ycombinator.com/item?id=45723805>

[^UndyingHorse]: <https://news.ycombinator.com/item?id=45719550>

[^nicoburns]: <https://news.ycombinator.com/item?id=45720199>

[^fidotron]: <https://news.ycombinator.com/item?id=45719657>

[^nu11ptr-native]: <https://news.ycombinator.com/item?id=45719675>

[^hsn915]: <https://news.ycombinator.com/item?id=45719730>

[^artursapek]: <https://news.ycombinator.com/item?id=45720890>

[^nu11ptr]: <https://news.ycombinator.com/item?id=45719344>
