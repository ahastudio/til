# “WebAssembly outside the web has a huge future” — Lin Clark의 WASI 발표 트윗

원문: <https://twitter.com/linclark/status/1110920999061594113>

## 요약

2019년 3월 28일, Mozilla의 엔지니어 Lin Clark(@linclark)이 WASI(WebAssembly System Interface) 발표 트윗을 올렸다.

> WebAssembly running outside the web has a huge future.
> And that future gets one giant leap closer today with...
> 📢 Announcing WASI: A system interface for running WebAssembly outside the web (and inside it too)

한국어 번역:

> 웹 밖에서 실행되는 WebAssembly는 엄청난 미래를 가지고 있습니다.
> 그 미래가 오늘 한 걸음 더 가까워졌습니다.
> 📢 WASI 발표: 웹 밖에서(그리고 웹 안에서도) WebAssembly를 실행하기 위한 시스템 인터페이스

이 트윗은 같은 날 Mozilla Hacks에 게시한 글
“[Standardizing WASI: A system interface to run WebAssembly outside the web](wasi-standardizing.md)”으로 연결됐다.
43개의 답글, 1060번 리포스트, 2586개의 좋아요를 받았다.
Solomon Hykes가 이 트윗을 인용하며 “2008년에 WASM+WASI가 있었다면 Docker를 만들 필요가 없었을 것”이라고 응답했고, 그로 인해 업계 전체의 주목을 받게 됐다.

→ [Solomon Hykes의 반응](solomon-hykes-wasi-tweet.md)

## 분석

### WASI 발표의 기술적 배경

Lin Clark의 Mozilla Hacks 글은 WASI 발표의 핵심 논거를 담고 있다.
당시 브라우저 밖 WebAssembly 실행은 Emscripten의 JavaScript 글루 코드에 의존했다.
각 런타임(서버, 엣지, 임베디드)이 이 브라우저용 코드를 각자 재구현하는 “에뮬레이션의 에뮬레이션(emulation of an emulation of POSIX)” 구조가 생겨났다.
WASI는 이 악순환을 끊고 런타임이 공통으로 구현할 표준 인터페이스를 정의함으로써 문제를 근원에서 해결한다.

Lin Clark이 제시한 두 가지 설계 원칙은 명확하다.
첫째는 이식 가능한 바이너리(portable binary)다. 소스 코드 이식성이 아니라 컴파일된 바이너리 자체가 어느 환경에서나 실행되어야 한다.
둘째는 기능 기반(capability-based) 보안이다. POSIX처럼 사용자 권한을 상속하는 대신, 모듈이 명시적으로 부여받은 기능만 사용할 수 있다.

### WASM+WASI 발표가 동시에 이루어진 의미

2019년 3월 이 발표가 나왔을 때 Bytecode Alliance가 함께 발족했다.
Mozilla, Fastly, Intel, Red Hat이 공동 창립한 이 컨소시엄은 WASI 구현의 레퍼런스가 될 Wasmtime 런타임과 함께 발표됐다.
표준 제안, 레퍼런스 구현, 거버넌스 조직이 동시에 나온 것은 단순한 아이디어 공개가 아니라 실행 가능한 표준화 궤도에 오른 것을 의미했다.
Lin Clark의 트윗이 단순한 블로그 공유 이상의 반향을 낳은 것은 이 맥락 때문이었다.

## 비평

### 발표 시점의 성숙도와 기대 사이의 간극

2019년 당시 WASI는 초기 설계 단계였다.
Lin Clark과 Mozilla가 공개한 것은 방향과 원칙이었지, 완성된 구현이 아니었다.
Solomon Hykes의 트윗이 “Let's hope WASI is up to the task”로 끝나는 것은 이 불확실성을 정확히 반영한다.
실제로 안정 버전인 Preview 2가 나오기까지 약 5년이 걸렸고, 그 사이 Preview 1에서 Preview 2로의 비호환 전환이 생태계 단절을 낳았다.

### POSIX 대비 축소된 범위의 의도성

Lin Clark이 설계한 WASI 초기 범위(wasi-core)는 의도적으로 작게 시작했다.
파일, 네트워크, 클록, 난수라는 최소 집합부터 표준화하고 나머지를 제안 프로세스로 확장하는 방식은 신중한 선택이었다.
그러나 이 전략은 “WASI가 내가 필요한 것을 아직 지원하지 않는다”는 조기 이탈 문제를 낳기도 했다.
표준화의 신중함과 생태계 채택 속도 사이의 긴장은 현재도 진행 중이다.

## 인사이트

### 기술 발표의 두 층위

Lin Clark의 발표는 기술 커뮤니케이션의 모범을 보여준다.
Mozilla Hacks 글은 만화 스타일 삽화로 기능 기반 보안 모델을 시각화했고, 트윗은 그 글로 연결하는 진입점 역할을 했다.
기술 자체의 복잡성을 은유와 시각 언어로 단순화한 것, 그리고 단순화된 메시지가 정확성을 잃지 않은 것이 이 발표의 강점이었다.
Hykes의 반응이 불을 붙이기 전에, Lin Clark의 원발표가 불씨를 준비했다.

발표 직후 Solomon Hykes가 응답한 것은 우연이 아닐 수 있다.
컨테이너 세계의 최고 권위자가 WASI 발표를 빠르게 포착하고 반응한 것은, Lin Clark의 발표가 기술 커뮤니티 안에서 올바른 청중에게 빠르게 닿았다는 증거다.
올바른 메시지가 올바른 채널을 통해 올바른 사람에게 닿을 때 기술의 가시성이 폭발적으로 높아지는 패턴을 이 사례가 잘 보여준다.
