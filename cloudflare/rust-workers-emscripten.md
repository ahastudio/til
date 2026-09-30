# Rust Workers에 Emscripten 타깃을 열다: 네이티브 Rust와 Tokio가 이벤트 루프 안에서 돈다

원문: [Supporting native Rust in Workers with the new Emscripten target for wasm-bindgen | Cloudflare Blog](https://blog.cloudflare.com/rust-workers-emscripten-target/)

## 요약

Cloudflare의 Guy Bedford와 Google의 Mitch Foley가 2026년 9월 28일, Birthday Week에 쓴 글이다.
Rust Workers에서 네이티브 Rust 코드와 Tokio 기반 애플리케이션까지 그대로 돌게 하는 기능의 첫 공개 실험 프리뷰를 발표한다.
핵심은 오픈소스 툴체인 `wasm-bindgen`과 Cloudflare의 Rust Workers에서 Emscripten의 `wasm32-unknown-emscripten` Rust 컴파일러 타깃을 일급으로 지원하는 것이다.
`wasm-bindgen`은 V8 기반 Workers 런타임에서 Rust WebAssembly 애플리케이션을 움직이는 툴체인이고, 이 타깃 지원은 1년여 전 Google이 시작해 `wasm-bindgen`을 유지보수하는 Cloudflare 엔지니어들이 검토하고 도운 장기 작업이었다.

Emscripten은 Mozilla가 처음 만들고 지금은 Google 엔지니어들이 유지하는 WebAssembly 컴파일러 툴체인으로, 타이머, 파일 시스템 연산, 소켓 같은 플랫폼 기능을 가상화해 네이티브 코드를 웹 플랫폼과 잇는다.
Workers는 웹 플랫폼 API와 Node.js 호환성을 지원하므로, Emscripten의 Node.js 컴파일 플래그를 써서 이 네이티브 기능들을 기존 Node.js API 위에서 가상화할 수 있다.
시험 삼아 Rust 네이티브 Minecraft 서버 Pumpkin을 Tokio의 실제 TCP 소켓을 써서 TCP 인그레스가 있는 Durable Object 안에서 돌렸다고 한다.

출발점은 Google 내부의 문제였다.
Google의 Portable Toolchains 팀 Mitch Foley는 한 내부 팀이 `wasm-bindgen`으로 JavaScript와 연결하면서 C++ 의존성도 Emscripten의 링커(`wasm-ld`)로 붙이고 싶어 한다는 요청을 받았다.
두 도구 모두 자기가 JavaScript를 불러오고 최종 JS와 Wasm 출력을 만든다고 가정했기 때문에, 사용자는 한쪽만 골라야 했다.
Mitch와 동료 Yifan Yang은 Emscripten이 빌드를 주도하고 Wasm 모듈을 불러오고 동반 JS를 만들며, `wasm-bindgen`은 Emscripten의 라이브러리 시스템에 바로 넣을 수 있는 작은 휴대용 바인딩을 만드는 협업 방식을 설계했다.
두 프로젝트 유지보수자들이 서로에 의존하는 통합 테스트를 유지하는 데 동의해야 했고, 그 결과 새 `-sWASM_BINDGEN` 설정으로 두 툴체인이 매끄럽게 함께 쓰이게 되었다.

라이브러리 호환성은 대체로 좋았다.
Emscripten이 이미 Rust의 `target_family = unix`를 지원하므로 저수준 시스템 라이브러리를 포함해 많은 라이브러리가 그대로 돌았다.
`libc`, `socket2`, Mio처럼 Emscripten을 몰랐던 라이브러리는 패치가 필요했지만, 대개 기존 플랫폼 조건에 `target_os = "emscripten"`을 더하는 수준이었다.
중요한 예외가 Tokio였다.

Workers는 단일 스레드이고 JS 이벤트 루프 안에서 돈다.
Tokio는 블로킹 연산을 스레드 파킹으로 처리하도록 설계되어 있어, 대기 중인 소켓 읽기나 `epoll_wait` 같은 블로킹 연산은 공유 JS 이벤트 루프를 막을 수 없다.
그들은 두 방식을 모두 구현했다.
하나는 WebAssembly JavaScript Promise Integration(JSPI)이다.
JSPI는 동기 연산에서 Wasm 스택을 멈추고 JS 이벤트 루프에 제어를 돌려주므로 파킹과 잘 맞는다.
다만 한 호출이 멈춘 동안 새 Wasm 호출이 들어오면 새 스택이 열리는데, Tokio의 런타임 맥락은 스레드 로컬에 있고 JSPI 스택 전환은 스레드 전환이 아니므로, Tokio는 아직 파킹 중이라고 생각하고 런타임에 이미 들어와 있다며 패닉한다.
그래서 JSPI 진입, 탈출, 멈춤, 재개마다 스레드 로컬 맥락을 바꿔 끼워야 하고, 이것은 사실상 멈춘 스택마다 자기 런타임 맥락을 가진 협력적 시분할 스레딩이다.

다른 하나는 Tokio에 이벤트 루프 런타임을 더하는 것이다.
Tokio 런타임은 준비된 작업을 더 이상 없을 때까지 폴링하고, 그다음 기다린다.
그 기다림을 호스트의 깨우기(wake)로 바꾸고, 한 묶음의 준비된 작업을 돌리고 돌아오는 명시적 `drive()`로 나눈 것이 제안된 `LocalEventLoop`다.
호스트가 소유한 `std::task::Waker`로 런타임 자체를 돌려야 한다는 신호를 보내고, 호스트가 준비되면 `drive()`를 부른다.
`spawn_local`은 곧바로 돌아오고, 소켓이 읽을 수 있게 되면 Tokio가 호스트 Waker로 신호를 보낸다.
기다릴 수 없다는 것이 유일한 제약이라, 일반 런타임이라면 파킹할 자리에서 `LocalEventLoop::block_on`은 패닉한다.
같은 구조가 GTK 메인 루프, Win32 메시지 펌프, Cocoa 런 루프에도 들어간다고 글은 쓴다.

소켓은 Emscripten이 `poll()`과 WebSocket 에뮬레이션만 지원하고 Tokio의 I/O 드라이버가 기대는 `epoll_wait()`는 지원하지 않아 마지막까지 남은 문제였다.
그들은 Workers의 Node.js 호환 계층에 이미 있는 `node:net`을 다리로 쓰기로 했다.
Emscripten의 `-sNODERAWFS`가 Node.js 파일 시스템 API로 바로 잇는 것처럼, 소켓도 같은 방식으로 이으면 양쪽 모두 새 API를 만들 필요가 없다.
그들은 Emscripten에 40개 넘는 풀 리퀘스트를 기여해 이것을 `-sNODERAWSOCKETS` 옵션으로 만들었고, Node.js에서 Emscripten 애플리케이션이 epoll, TCP, UDP, Unix 소켓을 쓰게 되었으며 같은 `node:net`을 구현한 Workers에서도 그렇다.
JSPI에서는 `epoll_wait()`가 준비될 때까지 스택을 멈추고, `LocalEventLoop`를 위해서는 epoll의 준비 이벤트에 콜백을 거는 `emscripten_epoll_add_listener` API를 Emscripten에 제안했다.

Minecraft 서버는 Dan Lapid가 주말 하루 만에 옮겼다.
Pumpkin은 Tokio 위에 멀티코어 기계용으로 설계되어, 월드 생성은 전용 스레드 풀에서, 게임 틱 루프와 청크 스케줄러는 각자의 OS 스레드에서 돈다.
Durable Object 안에는 스레드가 정확히 하나이므로, 틱 루프와 청크 스케줄러를 비동기 작업으로, 각 Rayon 작업을 Tokio 작업으로 바꾸고, 월드 생성은 청크 하나마다 한 차례씩 이벤트 루프에서 네트워크 I/O와 틱 사이에 끼워 돌렸다.
영속성은 Pumpkin이 평범한 `std::fs`로 쓰는 것을 `-sNODERAWFS`가 `node:fs`로 넘기고, Dan의 `worker-fs-mount` 라이브러리와 `durable-object-fs` 백엔드가 파일을 Durable Object의 SQLite 저장소 행으로 저장한다.
Pumpkin이 저장하는 모든 파일이 객체의 데이터베이스 행이 되어 동기로 쓰이고 트랜잭션과 함께 커밋되며, 다시 시작한 객체는 같은 월드에서 바로 부팅된다.
네트워킹도 Pumpkin을 바꾸지 않았다.
각 플레이어 연결은 Workers TCP 인그레스로 Worker의 `connect()` 핸들러에 들어와 Durable Object로 넘어가고, `cloudflare:node`의 `handleAsNodeConnection()`이 그 소켓을 객체 안의 `net.Server`로 보낸다.
`-sNODERAWSOCKETS`가 `TcpListener`를 `net.Server` 위에 구현하므로, 서버는 Linux에서처럼 플레이어를 받는다.

## 분석

### 호환성을 새로 만들지 않고 이미 있는 Node.js 계층에 기대었다

이 작업의 가장 영리한 결정은 다리를 새로 만들지 않은 것이다.
Emscripten은 네이티브 기능을 가상화할 줄 알고, Workers는 Node.js 호환 API를 이미 갖고 있다.
그래서 Emscripten의 Node.js 백엔드를 켜기만 하면, Workers가 따로 Emscripten 전용 API를 만들 필요가 없다.

소켓이 그 결정의 핵심 사례다.
Emscripten에 없던 `epoll`과 실제 소켓을 채우는 데 Workers 쪽 새 API는 하나도 필요하지 않았다.
Emscripten의 `-sNODERAWSOCKETS`가 `node:net` 위에 구현되었고, Workers는 이미 `node:net`을 구현하고 있었다.
그 결과 이 기여는 Workers만이 아니라 Node.js에서 도는 모든 Emscripten 애플리케이션에도 쓸모가 있다.

이것은 Workers가 Node.js 호환성에 투자해 온 것이 어떤 복리를 낳는지 보여 준다.
처음에는 npm 패키지를 돌리려는 투자였지만, 그 계층이 생기자 Node.js를 겨냥한 다른 툴체인들이 그대로 올라올 수 있는 표면이 되었다.

### 스레드를 가정한 런타임을 이벤트 루프에 넣는 두 가지 길

Tokio와 Workers의 충돌은 비동기 런타임의 근본 가정 차이다.
Tokio는 기다릴 때 스레드를 재우고, Workers는 기다리는 동안 이벤트 루프를 계속 돌려야 한다.
글은 이 충돌을 푸는 두 길을 모두 보여 준다.

JSPI는 런타임을 바꾸지 않고 스택을 바꾼다.
Wasm 스택을 멈추면 Tokio는 평소처럼 파킹한다고 믿는다.
대신 멈춘 스택이 여럿일 때 스레드 로컬 맥락이 섞이는 문제를 풀어야 하고, 그것은 사실상 협력적 스레드 스케줄러를 Tokio 밑에 새로 만드는 일이다.

`LocalEventLoop`는 스택을 그대로 두고 런타임을 바꾼다.
기다리는 대신 호스트를 깨우고, 호스트가 부를 때 한 묶음씩 돈다.
이것은 Tokio에 새 개념을 더하는 일이라 업스트림 설계 논의가 필요하지만, Workers만이 아니라 GUI 이벤트 루프를 가진 네이티브 애플리케이션에도 같은 문제를 푼다.
두 길은 각각 어디에 복잡도를 두느냐의 선택이다.

### 큰 데모는 호환성의 경계를 보여 주려는 것이다

Minecraft 서버를 Durable Object에서 돌린 데모는 과장된 쇼처럼 보이지만, 무엇을 증명하려는지가 분명하다.
Pumpkin은 멀티코어, 전용 스레드 풀, 파일 시스템, TCP 서버라는, 이 런타임이 가장 못 할 것 같은 네 가지를 모두 쓴다.
그것이 돈다면, 그보다 가벼운 대부분의 Rust 애플리케이션은 돌 가능성이 크다.

그리고 데모는 새 기능이 서로 맞물리는 방식을 보여 준다.
파일 시스템은 `-sNODERAWFS`와 `durable-object-fs`가 Durable Object의 SQLite로, 네트워크는 TCP 인그레스와 `handleAsNodeConnection()`과 `-sNODERAWSOCKETS`가 `net.Server`로 잇는다.
Pumpkin 자신은 자기가 디스크에 있지 않다는 것을 모른다는 문장이 이 설계의 목표를 요약한다.

## 비평

### 네이티브라는 말은 스레드를 버린 대가를 가린다

글의 제목은 네이티브 Rust를 지원한다고 말한다.
그런데 Minecraft 사례에서 가장 큰 작업은 네이티브 동작을 바꾸는 것이었다.
전용 스레드 풀과 OS 스레드를 쓰던 틱 루프, 청크 스케줄러, 월드 생성, Rayon 작업을 모두 단일 스레드 이벤트 루프 위의 협력적 작업으로 바꿨다.

이것은 코드를 그대로 가져왔다는 뜻이 아니다.
멀티코어를 위해 설계된 서버를 코어 하나에 넣었고, 월드 생성은 이제 네트워크 I/O와 틱 사이에 청크 하나씩 끼워 돈다.
플레이어가 늘거나 월드 생성이 무거워지면, 한 스레드가 모든 것을 나눠 맡는 구조는 틱 지연으로 드러날 것이다.
글은 이 데모가 몇 명의 플레이어에서, 어떤 틱 속도로 돌았는지 말하지 않는다.

그래서 이 발표가 여는 것은 네이티브 Rust 전체가 아니라, 스레드에 기대지 않거나 스레드를 협력적 작업으로 바꿀 수 있는 Rust 코드다.
Rayon처럼 병렬성을 전제로 한 라이브러리를 쓰는 애플리케이션은, 동작은 하더라도 원래 성능 모델은 잃는다.

### 실험 프리뷰의 의존 사슬이 길다

글은 이것이 실험 프리뷰라는 점을 분명히 한다.
그러나 그 실험이 기대는 조각을 세어 보면 사슬이 길다.
`wasm-bindgen`의 Emscripten 타깃, `libc`와 `socket2`와 Mio의 패치, 업스트림 리뷰 중인 Tokio 패치셋, 설계 논의 중인 JSPI 맥락 전환과 `LocalEventLoop`, Emscripten에 제안된 `emscripten_epoll_add_listener`, 그리고 `-sNODERAWSOCKETS`다.

이 가운데 일부는 이미 업스트림에 들어갔고, 일부는 Cloudflare의 예제에서 직접 패치로 필요하다고 글은 쓴다.
사용자가 오늘 이것을 쓰려면 업스트림에 들어가지 않은 Tokio 패치를 직접 끌어와야 한다.
그 패치가 최종 설계에서 바뀌면, 그 위에 만든 코드도 바뀌어야 한다.

프로덕션 사용을 고민하는 독자에게 필요한 것은 각 조각이 언제 업스트림에 들어갈 것인지, 어느 것이 바뀔 가능성이 큰지다.
글은 협업이 진행 중이라고만 쓴다.

### 성능과 비용의 숫자가 하나도 없다

기술적으로 무엇이 가능해졌는지는 자세하지만, 얼마나 잘 도는지는 없다.
Emscripten의 가상화 계층을 거치는 파일 시스템과 소켓 호출이 네이티브보다 얼마나 느린지, 기존 `wasm32-unknown-unknown` 타깃의 Rust Workers와 비교해 번들 크기와 시작 시간이 어떻게 달라지는지, JSPI의 스택 전환 비용이 얼마인지가 모두 빠져 있다.

Workers에서 이 숫자는 곧 비용이다.
CPU 시간으로 과금되고 콜드 스타트가 사용자 경험을 좌우하는 플랫폼에서, 호환성 계층이 더하는 오버헤드는 결정의 핵심 변수다.
네이티브 호환성과 플랫폼 효율 사이의 거래를 판단할 근거가 발표에 없다.

## 인사이트

### 툴체인 통합은 기술보다 유지보수 계약이 어렵다

글에서 가장 눈에 띄는 문장은 기술적인 것이 아니다.
이것은 단지 기술 문제가 아니었고, Emscripten과 `wasm-bindgen` 유지보수자 모두 이 계획을 지지하고 서로에 의존하는 통합 테스트를 유지하는 데 동의해야 했다는 대목이다.
두 도구가 서로의 출력을 가정하게 되는 순간, 한쪽의 변경은 다른 쪽을 깨뜨릴 수 있다.

이것은 오픈소스 생태계에서 반복되는 패턴이다.
두 프로젝트를 잇는 코드는 누구의 소유도 아니기 쉽고, 누가 깨진 것을 고칠지 정하지 않으면 통합은 몇 릴리스 만에 조용히 썩는다.
Google과 Cloudflare가 각각 한쪽을 유지보수하는 사람들을 두고 있다는 것이 이 통합이 성립한 조건이다.

그래서 이런 통합을 평가할 때는 기술이 동작하는지보다, 양쪽 프로젝트에 이것을 계속 지킬 이유가 있는 사람이 있는지를 봐야 한다.
Google 내부 팀의 수요와 Cloudflare의 플랫폼 수요가 각각 한쪽을 붙잡고 있는 동안에는 유지되지만, 어느 한쪽의 수요가 사라지면 통합 테스트는 가장 먼저 꺼질 것이다.

### 에지 런타임의 경쟁은 격리가 아니라 호환성으로 옮겨 간다

Workers는 V8 격리로 컨테이너보다 가볍고 빠르게 시작하는 것을 강점으로 삼아 왔다.
그 대가는 호환성이었다.
스레드도, 실제 파일 시스템도, 원시 소켓도 없는 환경에서는 기존 코드를 그대로 가져올 수 없었다.

이번 작업은 그 대가를 줄이려는 흐름의 연장이다.
Node.js 호환성, Python Workers, 컨테이너, 그리고 이번의 Emscripten 타깃은 모두 기존 코드를 거의 바꾸지 않고 에지에 올리게 하려는 시도다.
격리의 가벼움은 유지하면서 호환성의 비용을 가상화 계층이 떠맡는 구조다.

이 흐름이 계속되면 경쟁의 축이 바뀐다.
누가 더 가볍게 격리하느냐보다, 누가 더 많은 기존 코드를 수정 없이 받아들이느냐가 된다.
그리고 그 경쟁에서 가장 큰 자산은 이미 쌓아 둔 호환 계층이고, Workers가 Node.js 호환성 위에 Emscripten을 얹은 것이 그 자산의 쓰임을 보여 준다.

### 협력적 스케줄링이 다시 돌아온다

단일 스레드에서 여러 작업을 나눠 돌리고, 각 작업이 스스로 제어를 넘기게 하는 방식은 오래된 기술이다.
Windows 3.1과 고전 Mac OS가 협력적 멀티태스킹을 썼고, 한 프로그램이 제어를 넘기지 않으면 시스템 전체가 멈췄다.
운영체제는 그 문제 때문에 선점형 스케줄링으로 옮겨 갔다.

JSPI 위의 Tokio와 `LocalEventLoop`, 그리고 Pumpkin의 청크 하나씩 도는 월드 생성은 그 협력적 모델의 현대판이다.
이벤트 루프는 선점하지 않으므로, 한 작업이 오래 제어를 쥐면 같은 Durable Object의 모든 것이 기다린다.
월드 생성을 청크 하나씩 쪼갠 것은 바로 그 위험을 피하려는 조치다.

그래서 이 환경에서 네이티브 Rust를 쓰는 개발자는 오래된 규율을 다시 배워야 한다.
긴 계산은 쪼개서 중간에 제어를 넘기고, 블로킹 호출을 피하고, 한 작업이 루프를 독점하지 않게 설계하는 것이다.
에지 런타임이 스레드 없는 호환성을 넓혀 갈수록, 이 규율은 선택이 아니라 필수가 된다.
