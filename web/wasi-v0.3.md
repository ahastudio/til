# WASI v0.3 — 비동기가 WebAssembly 컴포넌트의 기본이 되다

<https://github.com/WebAssembly/WASI/releases/tag/v0.3.0>

HN 토론: <https://news.ycombinator.com/item?id=48504063> (254점, 96개 댓글)

Lobste.rs 토론: <https://lobste.rs/s/kosw9h/wasi_0_3_launched>

## 개요

WASI 0.3은 Component Model의 네이티브 비동기 프리미티브(async primitive) 위에 재기반한
주요 마일스톤 릴리스다.
“WASI 0.3은 공식적이며, 비동기는 이제 WebAssembly 컴포넌트에 네이티브하다”는 문장이
이번 릴리스의 핵심을 요약한다.

이전까지 WASI의 비동기 처리는 `subscribe` 패턴과 리소스 기반 상태 추적을 통해
폴링(polling) 방식으로 구현되었다.
0.3에서는 이 구조 전체가 Component Model의 `stream`과 `future` 타입으로 대체된다.

## 패키지별 변경

### wasi:cli

`stdin`과 `stdout`이 스트림 기반 패턴과 `future`를 사용하도록 변경되었다.
기존에는 리소스를 반환하는 방식이었으나, 이제는 `stream`과 `future`를 직접 다룬다.
`stdout`의 방향이 역전되어, 호출자가 스트림을 전달하면 완료 여부를 나타내는 `future`를
돌려받는 구조가 된다.

### wasi:sockets

가장 실질적인 리팩터링이 이루어진 패키지다.

`network` 리소스가 완전히 제거되었다.
네트워크 접근 권한은 이제 월드 임포트(world import)를 통해 부여된다.
모든 start/finish 함수 쌍이 단일 비동기 함수로 통합되었다.
진행 중 상태를 나타내는 리소스와 `subscribe` 패턴이 제거되었다.
TCP, UDP, DNS에 걸친 오류 처리가 단일 `error-code` 배리언트로 통일되었다.

### wasi:http

가장 광범위하게 재구성된 패키지다.
이제 두 개의 월드를 노출한다: `service`(HTTP 클라이언트 + 서버 요청 처리)와
`middleware`(`service`를 확장해 요청 포워딩을 지원).
컴포넌트들이 네트워크를 거치지 않고 프로세스 내에서 직접 합성(compose)되는
서비스 체이닝(service chaining)이 가능해진다.

### wasi:filesystem

스트리밍 연산이 `stream` + `future` 패턴을 채택했다.
디렉터리 순회(iteration)가 리소스 기반 이터레이터에서 스트림으로 전환되었다.

### wasi:clocks

“wall-clock”이 “system-clock”으로, “datetime”이 “instant”로 이름이 변경되었다.
POSIX 및 생태계 관례에 맞추기 위한 조정이다.

## 분석

WASI 0.3의 핵심은 단순한 API 개선이 아니라 비동기의 추상화 경계를 이동시킨 것이다.

0.2까지의 WASI는 비동기를 “런타임이 처리하는 것”으로 간주했다.
컴포넌트는 `subscribe`를 호출해 폴링 지점을 등록하고, 런타임이 이벤트를 주입하면
`finish` 류의 함수를 호출해 결과를 회수하는 2단계 방식이었다.
이 구조는 POSIX의 `select`/`epoll`에서 이어진 사고방식이다.

0.3에서는 비동기가 Component Model 타입 시스템 안으로 들어온다.
`stream`과 `future`는 단순한 편의 래퍼가 아니라 컴포넌트 인터페이스의 일급 타입이다.
이는 컴포넌트의 시그니처만 보고도 비동기성을 알 수 있다는 뜻이다.
런타임이 아닌 타입이 계약을 정의한다.

이 변화가 중요한 이유는 컴포넌트 합성 모델과의 정합성 때문이다.
컴포넌트는 네트워크 없이 프로세스 내에서 직접 연결될 수 있다.
`wasi:http`의 `middleware` 월드는 이 가능성을 가장 직접적으로 드러낸다.
컴포넌트 A가 컴포넌트 B의 HTTP 요청을 가로채 변환하는 것이,
별도 프록시 프로세스 없이 타입 수준에서 구현된다.

`network` 리소스 제거는 또 다른 패러다임 전환을 보여준다.
기존 모델에서 `network`는 소켓 생성의 팩토리이자 권한 컨테이너였다.
이 개념이 제거되고 월드 임포트로 대체된다는 것은,
권한 모델이 런타임 객체에서 컴파일 타임 인터페이스로 격상됨을 의미한다.
컴포넌트가 어떤 네트워크 접근을 요구하는지는 이제 바이너리 외부에서 정적으로 검사 가능하다.

2차 효과로는 다음을 예상할 수 있다.
런타임 구현자들은 `subscribe`/`poll` 루프 대신 네이티브 비동기 스케줄러를 통합해야 한다.
기존 WASI 0.2 기반 컴포넌트와의 하위 호환성은 어댑터 레이어가 필요하다.
`wasi:http`의 서비스 체이닝은 Wasm 기반 미들웨어 에코시스템의 기반이 될 수 있다.

### 비동기 구현의 기술적 기반

비동기 구현이 스택 전환(stack switching) 제안에 의존하는지를 묻는 질문이 있었다.[^hmry]
컴포넌트 모델 기여자 phickey의 답변에 따르면, 스택 전환 제안은 사용되지 않는다.[^phickey]
현재 stackful async 모드는 ABI 레이어를 통해 구현되며,
웹 엔진에서는 JSPI(JavaScript Promise Integration)를,
wasmtime에서는 메모리 기반 스택 관리를 활용한다.
스택 전환 제안이 모든 엔진에서 보편화되면,
이 기능을 호스트 개입 없이 WebAssembly 안에서 완전히 구현할 수 있게 된다.

## 비평

변경의 방향은 올바르지만 마이그레이션 비용이 상당하다.

`wasi:sockets`의 start/finish 쌍 통합은 API를 깔끔하게 만들지만,
기존 구현체들이 상태 머신을 전면 재작성해야 한다는 뜻이기도 하다.
`wasi:clocks`의 이름 변경은 작아 보이지만,
생태계 전반에 걸친 문자열 검색·치환을 유발하는 종류의 변경이다.

`wasi:http`의 `service`와 `middleware` 이분법은 명확하지만,
실제 HTTP 게이트웨이 시나리오에서 두 월드 사이의 경계가 항상 깔끔하게 떨어질지는
구현 사례가 축적되기 전까지 알 수 없다.

비동기가 타입 시스템으로 들어온 것은 올바른 방향이지만,
`stream`과 `future`의 에러 전파 시맨틱이 언어별 구현에서 얼마나 일관되게
표현될 수 있는지는 여전히 열린 문제다.

### 단순성 대 표현력 논쟁

컴포넌트 모델의 복잡성에 대한 비판도 있다.
garganzol은 WASI가 단순하고 안정적인 Unix 계열 API 모델을 유지했어야 했으며,
컴포넌트 모델은 불필요한 과도한 복잡성이라고 주장한다.[^garganzol]
이에 대한 반론으로, spankalee는 컴포넌트 모델이 서로 다른 언어로 작성된 모듈 간
비교적 타입 안전한 상호운용성을 가능하게 한다는 점에서,
다수의 언어를 런타임 타깃으로 삼는 WebAssembly의 맥락에서 적절하고 유용한 목표라고 반박한다.[^spankalee]
IDL 기반 접근이 언어 독립적인 API 노출 방식으로 최적이라는 시각은,
Microsoft가 독립적으로 유사한 아키텍처 패턴을 두 차례 채택한 사례에서도
방증을 찾을 수 있다.[^pie_flavor]

### 호환성 파괴와 실용성 문제

syrusakbary는 WASI 0.3이 현재 단 하나의 서버 사이드 Wasm 런타임에서만 실행 가능하며,
브라우저에서는 네이티브 지원이 없다는 점을 지적한다.[^syrusakbary]
기존 WASI 제안 및 런타임과의 하위 호환성이 깨진다는 것도 비판의 핵심이다.
기존의 수정되지 않은 C/C++ 프로그램과 라이브러리를 WebAssembly로 컴파일하는 것이 목표라면,
오늘날 더 실용적인 선택지로 WASIX가 있다는 주장이다.

b33j0r는 컴포넌트를 배포 전에 정적으로 링킹하는 접근 방식이
대부분의 실용적인 사용 사례를 약화시킨다고 주장하며,
프리스탠딩 WebAssembly와 커스텀 통합으로 이미 대안을 구축했다고 밝힌다.[^b33j0r]
이 관점은 컴포넌트 모델의 런타임 동적 인스턴스화 부재에 대한 우려를 반영하며,
해당 기능을 위한 이슈가 이미 공개 논의 중이다.[^spankalee_issue]

## 인사이트

WASI 0.3은 WebAssembly가 샌드박스 실행 모델에서 컴포넌트 합성 플랫폼으로
이행하는 과정에서 필요한 기반을 정비한 릴리스다.

비동기를 타입 시스템 안으로 끌어들인 것은
컴포넌트 경계에서의 의도(intent)를 명시적으로 만드는 설계 철학의 일관된 표현이다.
권한, 의존성, 이제 비동기성까지 — 모두 컴파일 타임 인터페이스로 표현된다.

이 방향이 완성되면 Wasm 컴포넌트는 기존 마이크로서비스가 네트워크를 통해 하던 일을
프로세스 내 타입 수준 합성으로 대체하는 단위가 될 수 있다.
그 가능성의 기술적 기반이 0.3에서 처음으로 갖춰졌다.

실제 커뮤니티에서 WASI의 구체적인 사용 사례로는 두 가지가 두드러진다.
feznyng는 LLM이 생성한 코드를 프로세스 내 샌드박스에서 실행하는 사례를 제시한다.[^feznyng]
Docker나 마이크로VM을 띄우는 것보다 훨씬 가볍고 부팅이 빠르다는 점에서,
AI 코드 실행 환경으로서 Wasm의 위치가 부각된다.
airstrike는 VSCode 방식의 WASM 기반 익스텐션 마켓플레이스를 구축하는 사례를 언급한다.[^airstrike]
이러한 실용 사례들은 컴포넌트 모델의 완성도와 무관하게 이미 진행 중이며,
0.3이 이 생태계에 비동기 기반을 제공함으로써 더 풍부한 익스텐션 인터페이스가
가능해질 것임을 시사한다.

---

[^hmry]: <https://news.ycombinator.com/item?id=48507756>
[^phickey]: <https://news.ycombinator.com/item?id=48508159>
[^garganzol]: <https://news.ycombinator.com/item?id=48505125>
[^spankalee]: <https://news.ycombinator.com/item?id=48505694>
[^pie_flavor]: <https://news.ycombinator.com/item?id=48506154>
[^syrusakbary]: <https://news.ycombinator.com/item?id=48507964>
[^b33j0r]: <https://news.ycombinator.com/item?id=48504974>
[^spankalee_issue]: <https://news.ycombinator.com/item?id=48505776>
[^feznyng]: <https://news.ycombinator.com/item?id=48505574>
[^airstrike]: <https://news.ycombinator.com/item?id=48505265>
