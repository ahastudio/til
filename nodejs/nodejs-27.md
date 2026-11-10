# Node.js 27 첫 알파: V8 15.6의 Iterator.zip과 Math.sumPrecise, 그리고 기본값이 바뀌는 곳들

원문: [What's new in Node.js 27](https://nodejsdesignpatterns.com/blog/whats-new-in-nodejs-27/)

Lobste.rs 토론: <https://lobste.rs/s/vtjjbc/what_s_new_node_js_27> (19점, 6개 댓글)

## 소개

Node.js 27은 새 연간 릴리스 일정을 처음 따르는 버전이다.
2026년 10월 29일에 v27.0.0-alpha.0.0.0이 나왔다.[^release]
Node.js Design Patterns의 저자 Luciano Mammino는 이 알파의 변경을 정리한 글을
2026년 11월 7일에 올리고 11월 9일에 갱신했다.
글에 따르면 예전에는 10월에 Current 릴리스가 나왔지만,
이제 10월은 6개월짜리 알파의 시작이다.
27.0.0 Current는 2027년 4월, LTS 승격은 2027년 10월이고
홀수와 짝수의 구분은 없어져 모든 릴리스가 LTS가 된다.
글은 지원 기간이 2030년 4월까지라고 적는다.

이 문서는 그 글을 소스로 삼았다.
글이 인용한 공식 릴리스 노트와 Node.js 블로그의 V8 변경 글을 열어 수치와 목록을
대조했다.[^release][^v8]
글의 예제 코드는 실행하지 않았다.

### 지금 써도 되는가

글의 결론은 둘로 나뉜다.
프로덕션이라면 2027년 4월 전에는 LTS 릴리스를 계속 쓴다.
오픈소스 라이브러리와 프레임워크 저자는 알파를 지금 CI에 넣어,
사용자가 올리기 몇 달 전에 깨지는 곳을 찾는다.
알파를 기존 런타임과 나란히 설치하는 데는 fnm이나 nvm 같은 버전 관리자를 쓰라고
한다.
Lobste.rs에서 bakkot은 `Math.sumPrecise`와 `Iterator.prototype.join`이 자신의 제안이라고 밝혔다.
처음에는 중간 반올림 오차를 감수하는 단순한 `Math.sum`을 계획했지만, 최대한 정밀한 합산도 그리 느리지 않게 구현할 수 있어 제대로 하기로 했다고 한다.
이름도 `Math.sum`으로 하고 싶었으나 여전히 다소 느리다는 이유로 엔진 쪽이 반대했다고 적었다.[^bakkot]

## 새 JavaScript 기능

V8이 14.6에서 15.6으로 올라가면서 아래 기능이 기본으로 켜진다.
릴리스 노트는 V8 버전을 15.6.75.13으로 적고,
기본으로 켜진 기능으로 `Math.sumPrecise()`, `Intl.Locale.prototype.variants`,
`Iterator.prototype.join()`, `Iterator.prototype.includes()`, `Iterator.zip()`,
`Iterator.zipKeyed()`를 든다.[^release]
이 기능들은 Node.js가 아니라 V8의 것이어서,
브라우저와 다른 런타임의 지원 여부는 별개다.

### Iterator.zip과 Iterator.zipKeyed

`Iterator.zip()`은 이터러블의 이터러블을 받아 같은 위치의 값을 묶은 배열을
하나씩 내놓는 지연(lazy) 이터레이터를 돌려준다.
배열에서는 `.map((v, i) => other[i] - v)`처럼 인덱스로 접근하면 되지만,
제너레이터나 이터레이터에는 인덱스가 없고 배열로 바꾸면
전체를 메모리에 올려야 한다.
`zip()`은 둘 다 한 항목씩 당겨 쓴다.

길이가 다른 입력은 `mode` 옵션이 정한다.
기본값인 `shortest`는 가장 짧은 입력이 끝나면 멈추고 남은 이터레이터를 닫는다.
`strict`는 길이가 다르면 `TypeError`를 던지며,
글은 벡터의 내적처럼 길이가 같아야 의미가 있는 계산에 쓰라고 한다.
`longest`는 `padding` 값으로 모자란 쪽을 채우며 끝까지 간다.

`Iterator.zipKeyed()`는 값이 이터러블인 객체를 받아 같은 키를 가진 객체를
내놓는다.
필드가 열 단위 배열로 따로 오는 API 응답을 행 단위 객체의 지연 시퀀스로 바꿀 때
쓴다.
세 개 이상을 묶을 때 위치 구조 분해가 헷갈리는 문제를 이름으로 풀어 준다.

```javascript
const items = ['Keyboard', 'Mouse', 'Monitor']
const prices = [129.99, 49.99, 349.95]

const line = Iterator.zipKeyed({ item: items, price: prices })
  .map(({ item, price }) => `${item} ($${price.toFixed(2)})`)
  .join(', ')

console.log(`${line} -> Total: $${Math.sumPrecise(prices)}`)
// Keyboard ($129.99), Mouse ($49.99), Monitor ($349.95) -> Total: $529.93
```

무한 이터레이터에도 쓸 수 있다.
글은 태양광 발전량과 가정 소비량을 읽는 두 계량기를 끝없는 제너레이터로 감싸
`zip()`으로 묶고 `.take(5)`로 다섯 쌍만 읽는 예를 든다.
`take()` 없이 `[...solar]`나 `.toArray()`를 부르면 끝나지 않고
메모리를 소진한다.

### Iterator.prototype.join과 includes

`join(separator)`는 이터레이터를 소비해 문자열로 바로 이어 붙인다.
이전에는 `.toArray().join(', ')`로 문자열 배열을 만들었다가 버렸다.
V8 블로그의 예는 `[1, 2, 3].values().map(x => x * 2).join('-')`이 `'2-4-6'`을
돌려준다는 것이다.[^v8]

`includes(value)`는 일치하는 값을 찾으면 즉시 멈춘다.
비교는 `Array.prototype.includes()`와 같은 SameValueZero이고,
이터레이터를 소비하므로 다시 검색하려면 새 이터레이터가 필요하다.
글은 `message.matchAll(/\bAPP-\d+\b/g)`로 이슈 참조를 뽑아
`includes('APP-142')`를 확인하는 예를 든다.
문자열에 `includes('APP-14')`를 쓰면 `APP-142`의 일부와 맞는 오탐이 나지만,
완전한 참조만 뽑아 비교하면 이를 피한다.

### 동기 이터레이터에만 적용된다

위 헬퍼는 동기 이터레이터용이다.
`async function*` 제너레이터와 Node.js 스트림의 비동기 이터레이터에는 같은
체인을 쓸 수 없다.
글은 비동기 이터레이터 헬퍼가 별도의 TC39 제안이고 이 알파에는 들어 있지 않다고
적는다.
그런 입력에는 `for await...of`나 비동기 헬퍼를 가진 라이브러리를 쓴다.
bakkot은 지금 진행 중인 큰 작업이 동시성을 지원하는 비동기 이터레이터 헬퍼이고, 그래서 동기 판보다 훨씬 복잡하다고 답했다.[^bakkot-async]

### Math.sumPrecise

`.reduce((a, b) => a + b, 0)`은 덧셈마다 중간 결과를 64비트 부동소수점으로
반올림한다.
글의 예에서 `[129.99, 49.99, 349.95]`는 `529.9300000000001`이 되고,
`[1e20, 0.1, -1e20]`은 `0.1`이 사라져 `0`이 된다.
`Math.sumPrecise()`는 내부에 정밀한 누산기를 두고
마지막에 한 번만 반올림하므로 앞의 두 예는 각각 `529.93`과 `0.1`이 된다.
이터러블을 받으므로 `.map()`의 결과를 `.toArray()` 없이 넘길 수 있다.

돈 계산에는 여전히 맞지 않는다.
입력 `0.1`과 `0.2`가 이미 이진 부동소수점으로 저장된 값이어서
`Math.sumPrecise([0.1, 0.2])`도 `0.30000000000000004`다.
글은 정확한 십진 계산이 필요하면 센트 같은 정수 단위나 십진 라이브러리를 쓰라고
한다.

## 새 Node.js API

### node:net/promises

`node:fs`, `node:dns`, `node:stream`, `node:timers`,
`node:readline`에는 `.promises` 하위 모듈이 있었지만
`node:net`은 이벤트와 콜백뿐이었다.
이전에는 서버를 띄우려면 `once(server, 'listening')`처럼 이벤트를 프로미스로
직접 감싸야 했다.
알파는 실험 단계의 `node:net/promises`에 `listen()`과 `connect()`를 추가하고,
`net.Server`를 비동기 이터러블로 만든다.[^release]

글은 연결마다 한 줄을 받아 다른 모든 클라이언트에 전달하는 TCP 채팅 서버를 예로
든다.
핵심은 연결 루프 안에서 핸들러를 기다리지 않는 것이다.

```javascript
for await (const socket of server) {
  // await 없이 시작해야 다음 연결을 받는다
  void handleConnection(socket).catch((error) => {
    console.error('Connection handler failed:', error)
    socket.destroy()
  })
}
```

`await handleConnection(socket)`으로 바꾸면
첫 클라이언트가 끊길 때까지 다음 연결의 핸들러가 시작되지 않아,
첫 클라이언트의 메시지를 받을 상대가 없다.
서버 이터레이터 문서는 소비가 느리면 연결이 제한 없이 쌓일 수 있다고
경고하므로 `server.maxConnections`를 명시한다.
`clients` 맵의 키로 쓴 원격 주소와 포트는 연결 라벨일 뿐 사용자 식별자가 아니다.

### node:vfs

`node:vfs`는 메모리 안에 격리된 가상 파일 시스템을 만든다.
이전에는 `--experimental-vfs` 플래그 뒤에 있었고 이제 플래그 없이 쓸 수 있지만,
안정성 등급은 여전히 실험(Stability 1)이다.
`vfs.create()`로 만들어 `mkdirSync`와 `writeFileSync`로 채운 뒤 `mount()`하면,
평소의 `node:fs` 호출과 `import`, `require()`가 그 경로에서 읽는다.

마운트 지점은 `path.join(os.devNull, 'vfs')` 아래로 예약되어 있어(POSIX에서는
`/dev/null/vfs/1` 같은 경로) 실제 디스크의 파일을 가리거나 덮을 수 없다.
`using` 선언으로 만들면 블록을 벗어날 때 자동으로 마운트가 풀리고,
`const`로 만들면 `unmount()`를 직접 불러야 한다.
CLI에서는 `node --vfs-load=<디렉터리>`가 그 디렉터리를 마운트해 `index.js`를
실행한다.
ZIP 아카이브를 넘기면 `package.json`의 `main`이나 `index.js`를 실행한다.
단일 실행 애플리케이션(SEA)에서는 `vfsArchive`가 레이어 0에 마운트되고
Worker 스레드에서도 자동으로 보인다.

### fs.mkstemp

POSIX `mkstemp(3)`를 본뜬 `fs.mkstemp()`, `fs.mkstempSync()`,
`fsPromises.mkstemp()`가 추가되었다.
접두사 뒤에 임의의 여섯 글자를 붙여 고유한 파일 이름을 만들고, 같은 단계에서
파일을 열어 경로와 파일 핸들을 돌려준다.
이전에는 `fs.mkdtemp()`로 임시 디렉터리를 만들고 그 안에서 파일을 열거나,
임의 이름을 만들어 충돌 시 재시도하는 루프를 직접 짰다.
`fs.glob()`은 Node.js 22에서 도입된 뒤 이번에 JavaScript에서 C++로 옮겨졌다.
글은 관리자들의 벤치마크에서 일부 작업은 크게 빨라졌지만
동기 방식에 제외 패턴을 쓴 한 작업은 느려졌다고 적고,
자신의 패턴으로 측정해 보라고 한다.

### 권한 모델의 --allow-env

`--permission`을 켜면 `--allow-env`로 허용하지 않은 환경 변수는 JavaScript가
실행되기 전에 프로세스에서 제거된다.
`PATH`, `HOME`, `LANG`, `NODE_OPTIONS` 같은 런타임 변수와 `--env-file`로 불러온
변수는 예외다.

```bash
SECRET_KEY=super-secret APP_PORT=3000 \
  node --permission --allow-env='PUBLIC_*,APP_*' app.js
# process.env.APP_PORT 는 읽히고 SECRET_KEY 는 undefined
```

글에 따르면 제거는 운영체제 환경 블록에서도 이뤄지고
리눅스의 `/proc/self/environ` 접근도 막으며,
읽은 뒤 `process.permission.drop('env', '이름')`으로 지울 수도 있다.
`NODE_ENV`는 기본으로 보존되지 않으므로 앱이 쓰면 명시해야 한다.
글은 이것이 실수로 인한 노출을 줄일 뿐 악성 코드를 막는 샌드박스는 아니라고
선을 긋는다.

### 내장 테스트 러너

`node --test --watch`가 안정(Stability 2)이 되었다.
`--test-forbid-only`는 `{ only: true }`나 `test.only()`가 하나라도 있으면
실행을 실패시켜 CI가 실수로 커밋된 `.only`를 잡는다.
`MockFunctionContext`에는 `mockReturnValue()`, `mockResolvedValue()`,
`mockRejectedValue()`, `mockThrownValue()`가 생겨
`mockImplementation(() => ...)`를 감싸는 수고가 줄었다.

## 기본값이 바뀌는 곳

코드를 바꾸지 않아도 동작이 달라지는 항목이다.

### http.Server의 keepAliveTimeout이 5초에서 65초로

AWS ALB는 유휴 시간 제한이 기본 60초이고 Node.js의 `keepAliveTimeout`은 5초였다.
Node.js가 유휴 소켓을 닫는 순간 프록시가 그 연결을 다시 쓰면
요청이 실패해 간헐적 502가 난다.
새 기본값 65초는 60초 프록시 제한보다 길다.
글은 소켓의 실제 제한에 `keepAliveTimeoutBuffer`(기본 1초)가 더해지며,
65초가 모든 프록시 설정을 덮지는 못하므로 프록시의 실제 유휴 제한을 확인해
그보다 길게 설정하라고 한다.
릴리스 노트에는 이 변경과 HTTP/2 기본 윈도 크기 증가가 모두 semver-major
항목으로 있다.[^release]

### req.headers와 req.trailers의 프로토타입 제거

들어오는 요청의 헤더 객체는 `Object.prototype`을 상속하지 않는다.
클라이언트가 `constructor`나 `__proto__`라는 헤더를 보낼 수 있고
Node.js는 이름을 소문자로 바꾸므로,
일반 객체로는 사용자가 정한 키와 상속된 속성이 섞인다.
`__proto__`에 값을 대입하면 값이 저장되지 않고
프로토타입을 바꾸려는 동작이 된다.

글은 이 변경이 PR #62900의 Matteo Collina 작업이라고 적는다.
2026년 3월 보안 릴리스의 CVE-2026-21710은 `__proto__` 헤더 때문에
`req.headersDistinct`가 비정상으로 동작해 프로세스가 죽을 수 있던 서비스 거부
취약점이고, 수정은 `headersDistinct`에 `{ __proto__: null }`을 쓴 것이라고 한다.
그 권고는 `headersDistinct`만 다루므로 `req.headers`에 같은 충돌이 있었다는 뜻은
아니라고 글이 분명히 적는다.

깨지는 코드는 `req.headers.hasOwnProperty('authorization')`처럼 상속 메서드를
부르는 곳이며 `TypeError`가 난다.

```javascript
// Node.js 26과 27 모두에서 동작한다
const hasAuthorization = Object.hasOwn(req.headers, 'authorization')
```

`Object.prototype`을 헤더 객체에 되돌려 놓는 식의 우회는 쓰지 말라고
글이 권한다.
`in` 연산자는 동작하지만 갱신된 문서가 권하지 않는다고 한다.
헤더의 존재를 확인하는 것은 값을 인증하는 것이 아니다.

### 힙 기본 한도

`--max-old-space-size`를 주지 않으면
V8은 물리 메모리(또는 컨테이너 cgroup 메모리)의 절반을 256MB에서
4GB 사이로 잘라 old-generation 한도로 쓴다.
이전에는 절반이되 2GB가 상한이었고 메모리가 15GB 이상이어야 4GB였다.
그래서 8GB 머신은 2GB에서 4GB로, 6GB 머신은 2GB에서 3GB로 올라간다.[^v8]
이 값은 old-generation 한도이고 프로세스 전체 메모리 제한이 아니다.
`Buffer`와 `ArrayBuffer`가 잡은 메모리도 V8의 전역 할당 한도에 포함되어 가비지
컬렉션이 시작되는 시점이 달라진다.[^v8]
암묵적 2GB 상한에 기대어 한 머신에서 여러 프로세스를 돌렸다면
`--max-old-space-size=2048`을 명시한다.

## 업그레이드 전에 확인할 것

글의 점검 목록과 본문의 주의를 한 표로 합쳤다.

| 점검 대상                                         | 달라지는 것                                         | 할 일                                                |
| ------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| `req.headers.hasOwnProperty`, `req.trailers`      | `TypeError`                                         | `Object.hasOwn(req.headers, 이름)`으로 바꾼다        |
| Redis나 DB에 저장한 `v8.serialize()` 결과         | 새 형식을 이전 Node.js가 읽지 못한다                | 혼합 버전이 읽는 저장소인지 확인한다                 |
| 4GB 초과 15GB 미만 머신의 힙 기본 한도            | 2GB 상한이 사라진다                                 | `--max-old-space-size`를 명시한다                    |
| `Math` 함수의 하드코딩 비교, `--random-seed`      | 마지막 비트가 다르고 난수 열이 바뀐다               | 허용 오차로 비교하고 기대값을 새로 만든다            |
| 정렬 비교 함수의 호출 횟수를 세거나 부작용이 있음 | 큰 배열에서 PowerSort로 호출 횟수가 달라진다        | 일관된 비교 함수만 쓰고 횟수에 기대지 않는다         |
| 디스크에 둔 컴파일 캐시와 `vm` 캐시 데이터        | 패치와 마이너 릴리스에서도 무효화된다               | 캐시 미스를 전제한다                                 |
| `_http_*`, `_tls_*`, `node:domain`                | 비공개 `_http_*` 폐기, `_tls_*` 제거, `domain` 경고 | `node:http`, `node:tls`와 `AsyncLocalStorage`를 쓴다 |
| 네이티브 애드온, OpenSSL 엔진 API                 | `NODE_MODULE_VERSION` 153, 엔진 API 제거            | 애드온을 다시 빌드하고 엔진 사용처를 찾는다          |
| 힙 스냅샷                                         | 크기와 생성 시간이 약 2배, 스크립트 전체 소스 포함  | 파일을 민감 정보로 다룬다                            |

수치의 출처를 확인했다.
`Math.log(3)`이 26에서 `1.0986122886681096`, 27에서 `1.0986122886681098`이고
`--random-seed=42`의 첫 `Math.random()`이 `0.6159659788862542`에서
`0.22876995452731475`로 바뀐다는 것은 V8 블로그의 예와 일치했다.
2000개 원소 배열을 정렬할 때 비교 함수 호출이 19220회에서
19249회로 달라진다는 예도 그 글에 있다.[^v8]
알파는 새 직렬화 형식이 4GB를 넘는 타입 배열을 `structuredClone()`과
`postMessage()`에서 지원하지만 `v8.serialize()`는 여전히 4GB 제한을 유지한다고
V8 블로그가 적는다.[^v8]

## 비평

### 점검표는 알파가 바꾼 것의 일부다

글은 마지막에 전체 커밋 목록으로 가는 링크를 두므로 누락이 오류는 아니다.
그러나 제목이 점검 목록이고 항목마다 깨지는 증상이 적혀 있어 완전한 목록처럼
읽힌다.
V8 블로그에는 글의 목록에 없는 항목이 있다.
`error.stack` 게터가 더는 프로토타입 체인에서 저장된 스택을 찾지 않고,
asm.js가 더는 WebAssembly로 컴파일되지 않으며
`--experimental-wasm-<이름>` 플래그가 `--wasm-<이름>`으로 바뀐다.
알파 빌드에서는 `--trace-event-categories`가 쓰는 파일에 대부분의 V8 트레이스
이벤트가 나오지 않고, `Debugger.setScriptSource`는 항상 실패하며,
쓰이지 않는 바이트코드가 약 3분 뒤 메이저 GC에서 버려질 수 있다.[^v8]
릴리스 노트의 커밋 제목에는 이전 `AsyncLocalStorage` 구현 제거,
`net`의 여러 번 `listen` 호출 시 예외, 한도를 넘는 헤더를 가진 HTTP 응답 거부,
끝난 뒤 `addTrailers` 거부, 암호 입력과 출력 인코딩 검증이 있다.[^release]
이 문서는 이 커밋의 제목만 읽었고 동작의 세부는 확인하지 못했다.
어떤 변경이 자기 코드를 깨는지는 결국 전체 목록과 자기 코드를 대조해야 안다.

### 호환성 영향의 크기를 재지 않았다

`req.headers.hasOwnProperty`가 던지는 `TypeError`는 분명하다.
그러나 글은 생태계에서 얼마나 많은 패키지가 이 호출을 쓰는지,
이전에 흔한 관용구였는지를 보여 주지 않는다.
이 문서도 그것을 조사하지 못했다.
같은 한계가 힙 기본 한도에도 있다.
한도가 올라가면 메모리가 넉넉한 서비스는 그대로이고 한도를 믿고
여러 프로세스를 얹은 서비스만 영향받는데, 어느 쪽이 많은지는 글의 범위 밖이다.
알파 단계의 글이라는 점을 고려하면 이해되지만,
점검표의 우선순위는 독자가 스스로 정해야 한다.

## 인사이트

### 알파에서는 Node 27 호환이 움직이는 목표다

릴리스 노트에는 이 알파 하나 안에서 `NODE_MODULE_VERSION`이 151, 152,
153으로 세 번 갱신된 커밋이 있다.[^release]
V8 블로그는 새 일정에서 알파와 Current 단계에 V8 일괄 업그레이드 같은 깨지는
변경이 들어올 수 있고, 네이티브 애드온 ABI에 영향이 있으면
`NODE_MODULE_VERSION`이 올라간다고 밝힌다.
LTS가 되면 V8 버전이 안정되고 심각한 보안 수정 같은 예외가 아니면
ABI와 API가 깨지는 변경이 없을 것으로 기대한다고도 한다.[^v8]

이 설명에서 읽히는 결과는 CI에 알파를 넣는 일이 한 번의 호환성 확인이 아니라는
점이다.
알파 빌드가 바뀔 때마다 ABI 버전으로 미리 빌드된 바이너리를 고르는 도구는 다시
빌드를 받아야 하고, 어제 통과한 테스트가 오늘 깨질 수 있다.
알파를 CI 행렬에 넣는다면 빌드를 고정하고 갱신 주기를 정해 두는 편이 낫다.
이것은 이 문서의 해석이다.

### 직렬화 형식 변경은 롤링 배포와 롤백에서 한 방향으로만 호환된다

새 Node.js는 이전 형식을 읽지만 이전 Node.js는 새 형식을 읽지 못하고
`invalid or unsupported version` 오류가 난다고 V8 블로그가 적는다.[^v8]
혼합 버전의 서버가 `v8.serialize()` 결과를 공유 저장소에 쓰고 읽는 구조에서
27 서버가 쓴 값을 26 서버가 읽을 수 없다.
같은 이유로 27로 올린 뒤 문제가 생겨 26으로 되돌리면
그 사이에 쓰인 값을 읽지 못한다.

글의 점검 항목은 이 위험을 짚지만 해결 순서는 제시하지 않는다.
읽는 쪽을 먼저 올리는 방법은 쓸 수 없다. 이전 Node.js에는 새 형식을 읽는 기능이
추가되지 않기 때문이다.
형식이 런타임 안에서 정해지므로 앱이 쓰는 형식을 고를 수도 없다.
남는 방법은 저장소의 키에 Node.js 주 버전을 넣어 두 세대가 서로의 값을 만나지
않게 하거나, 공유 저장소에는 JSON처럼 런타임 독립적인 형식을 쓰는 것이다.
이것도 이 문서의 해석이며 글이 권한 것이 아니다.

### 기본값 변경은 설정하지 않은 코드에만 닿는다

`keepAliveTimeout`, 힙 한도, HTTP/2 윈도 크기는 모두 기본값의 변경이다.
값을 명시한 서비스에는 아무 일도 일어나지 않고,
기본값에 기대던 서비스만 코드 변경 없이 동작이 달라진다.
테스트가 통과해도 이 차이는 드러나지 않는다. 테스트는 보통 프로덕션 규모의
머신과 프록시를 갖추지 않기 때문이다.

업그레이드 전후에 실효 값을 기록하면 이 차이를 숫자로 비교할 수 있다.

```javascript
import { getHeapStatistics } from 'node:v8'
import { createServer } from 'node:http'

console.log('heap limit', getHeapStatistics().heap_size_limit)
console.log('keepAliveTimeout', createServer().keepAliveTimeout)
```

같은 이미지를 4GB 노드와 8GB 노드에 배포하면 힙 한도가 이미 달랐고,
이제 그 차이는 한도 상한이 올라간 만큼 더 커진다.
이 출력은 알파에서 실행해 확인하지 않았으며, 값의 의미는 위에서
인용한 문서의 설명에 따른다.

### 라이브러리는 런타임 하한이 올라갈 때까지 새 기능을 쓸 수 없다

`Iterator.zip()`과 `Math.sumPrecise()`는 Node.js 27의 V8에만 있다.
LTS 27은 2027년 10월에 나오므로,
그 전에 나온 LTS 라인을 지원하는 라이브러리는 이 기능을 직접 호출하면
그 라인에서 `TypeError`가 난다.
글은 이 문제를 다루지 않는다.
쓰려면 호출 전에 `typeof Iterator.zip === 'function'`으로 확인하고 없으면
배열 기반 구현으로 되돌리는 경로가 필요하며,
이 경로는 새 기능이 줄여 주려던 중간 배열을 다시 만든다.
그래서 지연 시퀀스의 이점은 지원 하한이 27 이상인 애플리케이션 코드에서
먼저 얻고, 라이브러리에는 한참 뒤에 도착한다.

---

[^release]: Node.js 블로그, [Node.js 27.0.0-alpha.0.0.0 (Alpha)](https://nodejs.org/en/blog/release/v27.0.0-alpha.0.0.0), 2026-10-29

[^bakkot]: <https://lobste.rs/s/vtjjbc/what_s_new_node_js_27#c_eobkhf>

[^bakkot-async]: <https://lobste.rs/s/vtjjbc/what_s_new_node_js_27#c_iume6s>

[^v8]: Node.js 블로그, [Notable V8 changes from Node.js 26 to 27 (Alpha)](https://nodejs.org/en/blog/announcements/notable-v8-changes-from-node-js-26-to-27-alpha), 게시일 표시 없음
