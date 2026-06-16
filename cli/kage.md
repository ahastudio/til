# Kage: JavaScript-free static offline mirror generator

> A website, frozen as a shadow

<https://kage.tamnd.com/>

<https://github.com/tamnd/kage>

GeekNews: <https://news.hada.io/topic?id=30497>

## 소개

Kage는 웹사이트를 자바스크립트(JavaScript) 없는 정적 오프라인 미러로 변환하는 Go 언어 기반 CLI 도구다.
헤드리스 Chrome을 이용해 페이지를 렌더링하고 최종 DOM 상태를 캡처한 뒤, 모든 자바스크립트를 제거하고 CSS·이미지·폰트를 로컬 경로에 다운로드한다.

브라우저의 “다른 이름으로 저장” 기능으로 보존한 웹페이지는 시간이 지나면 깨진 스크립트, 누락된 애널리틱스 호출, 외부 CDN 의존성 때문에 접근 불가능해진다.
Kage는 이 문제를 JavaScript를 완전히 제거하고 자산을 로컬화하는 방식으로 해결한다.
창작자 tamnd는 과거 128MB USB 드라이브에 웹사이트를 저장하던 시절의 경험에서 동기를 얻었다고 밝혔다.

MIT 라이선스로 공개됐다.

## 주요 기능

- **breadth-first 크롤링**: `robots.txt`를 준수하면서 사이트를 너비 우선으로 탐색한다.
- **멱등성(idempotency)**: 동일 페이지가 여러 경로로 도달되더라도 한 번만 처리한다.
- **재개 가능한 클론**: 저장된 상태를 통해 중단된 작업을 이어서 실행할 수 있다.
- **다양한 출력 형식**: 디렉토리 폴더, ZIM 아카이브(Kiwix 에코시스템 호환), 독립 실행 바이너리, 데스크톱 앱 중 선택 가능하다.
- **결정론적 패킹(deterministic packing)**: 콘텐츠 기반 UUID를 사용해 바이트 단위로 동일한 출력을 보장한다.
- **멀티 플랫폼**: Windows GUI, macOS 앱 번들, Linux AppImage를 지원한다.

## CLI

```bash
# Go 설치
go install github.com/tamnd/kage/cmd/kage@latest

# WinGet 설치 (Windows)
winget install tamnd.kage

# 오프라인 미러 생성
kage clone <url>

# 로컬 미리보기
kage serve [dir]

# ZIM 또는 바이너리로 패킹
kage pack
```

Chrome 또는 Chromium이 호스트에 설치되어 있어야 한다.
Docker 컨테이너 이미지도 제공한다.

## 아키텍처

Go(97.4%)로 작성됐으며 크롬 제어, 자바스크립트 제거, 자산 다운로드, URL-to-path 결정론적 매핑, ZIM 아카이빙이 분리된 관심사(separation of concerns)로 구현되어 있다.

HN 논의에서 창작자 tamnd는 SingleFile 같은 기존 단일 페이지 저장 도구와의 차이를 설명했다.
SingleFile은 단일 페이지 저장에 강하지만, Kage는 사이트 전체를 미러링하는 접근 방식을 취한다는 것이다.

## 분석

### 웹 보존의 근본 문제를 공략하는 접근

인터넷 아카이브(Wayback Machine) 같은 서비스는 중앙화된 보존 방식이다.
Kage는 누구나 특정 사이트를 자신의 환경에서 독립적으로 보존할 수 있도록 한다.
이 분산화 접근은 특히 검열 위험이 있는 콘텐츠나 기업의 서비스 종료 위험이 있는 문서에 대한 개인 차원의 보존 전략이 된다.

JavaScript를 완전히 제거하는 선택은 장기 보존에서 결정적이다.
자바스크립트는 외부 의존성, API 호출, CDN 리소스와 연결되어 있다.
이것들이 사라지면 페이지가 작동하지 않는다.
정적 HTML과 인라인화된 자산만 남기는 것이 가장 내구성 있는 보존 형태다.

### 기술적 트레이드오프

헤드리스 Chrome 의존성은 단순 HTTP 크롤러보다 훨씬 무겁다.
HN에서 gregwebs는 사이트에 가해지는 부하를 우려하며 스로틀링 옵션을 요청했다.[^gregwebs]
현재 `robots.txt` 준수가 유일한 속도 제한 메커니즘이다.

HN에서 dimiprasakis는 Chrome의 `--no-sandbox` 플래그 사용에 대한 보안 우려를 제기했다.[^dimiprasakis]
Docker 환경에서는 이 플래그가 필요하지만, 신뢰할 수 없는 페이지를 크롤링할 때 잠재적 위험이 있다.

HN에서 nikisweeting은 아카이빙의 기술적 복잡성을 지적했다.
“닫힌 shadow DOM, cross-origin iframe, 웹소켓, 미디어 URL, 중복 자산 제거” 등이 완전한 아카이빙을 어렵게 만드는 요소들이다.
Kage가 이 모든 케이스를 어떻게 처리하는지는 추가 검증이 필요하다.

## 비평

### 자바스크립트 제거의 완전성에 대한 의문

자바스크립트가 서버 사이드 렌더링(SSR)에 의존하는 현대 웹 앱에서는 헤드리스 Chrome이 최종 DOM을 캡처할 수 있다.
하지만 클라이언트 사이드 라우팅, 무한 스크롤, 동적으로 로드되는 콘텐츠는 단일 DOM 스냅샷으로 완전히 보존하기 어렵다.
크롤링 범위를 어떻게 정의하느냐에 따라 보존의 완전성이 크게 달라진다.

### 규모 있는 사용의 실용성

wolttam의 제안처럼 모든 콘텐츠를 단일 HTML 파일에 인라인화하는 접근이 더 실용적일 수 있다.[^wolttam]
현재의 디렉토리 구조 기반 아카이브는 별도의 서빙 서버가 필요하며, 이것이 오프라인 사용성을 제한한다.
ZIM 형식과 독립 실행 바이너리 옵션이 이 문제를 부분적으로 해결하지만, 아직 모든 플랫폼에서 완성도 있게 작동하는지는 불명확하다.

## 인사이트

### 웹의 일시성이 만드는 보존 수요

링크 로트(link rot) — 웹 링크가 시간이 지나면서 접근 불가능해지는 현상 — 는 오래된 문제다.
Kage 같은 도구의 등장은 이 문제가 개인 개발자 수준에서도 해결 가능해졌음을 보여준다.
과거에는 Wayback Machine이나 HTTrack 같은 전문 도구가 필요했던 작업이 이제 일반 CLI 도구로 가능해졌다.

### 자바스크립트 최소화 트렌드와의 접점

Kage의 철학 — 자바스크립트를 제거하고 정적 HTML로 환원 — 은 점진적으로 성장하는 “자바스크립트 없는 웹(no-JS web)” 트렌드와 맥을 같이한다.
htmx, Astro의 아일랜드 아키텍처, HTML-first 접근 방식들이 보여주듯, 복잡한 자바스크립트 없이도 기능하는 웹 페이지가 더 오래 살아남는다.
Kage가 아카이빙할 수 있는 사이트의 범위는 이 트렌드가 성장할수록 넓어진다.

---

[^gregwebs]: <https://news.ycombinator.com/item?id=48530366>
[^dimiprasakis]: <https://news.ycombinator.com/item?id=48530697>
[^wolttam]: <https://news.ycombinator.com/item?id=48530457>
