# Portless

> Replace port numbers with stable, named .localhost URLs.
> For humans and agents.

- 원문: <https://github.com/vercel-labs/portless>
- 사이트: <https://port1355.dev/>

## 요약

Vercel Labs가 만든 로컬 개발 프록시 도구다.
`localhost:3000` 대신 `myapp.localhost:1355` 같은
안정적이고 사람이 읽을 수 있는 URL을 제공한다.

포트 1355에서 동작하는 리버스 프록시가 핵심이다.
각 앱에 4000~4999 범위의 랜덤 포트를 할당하고,
이름 기반 `.localhost` 서브도메인으로 라우팅한다.

RFC 6761에 따라 `.localhost` 도메인은 항상
루프백 주소(127.0.0.1)로 해석되므로 `/etc/hosts`
수정이 필요 없다.

## 해결하는 문제

| 문제                     | 설명                           |
|--------------------------|--------------------------------|
| 포트 충돌                | `EADDRINUSE` — 두 앱이 같은   |
|                          | 포트를 사용                    |
| 포트 암기                | 3000, 3001, 8080... 어떤 앱이 |
|                          | 어디인지 기억 불가             |
| 쿠키 충돌                | `localhost`에 설정된 쿠키가    |
|                          | 포트와 무관하게 모든 앱에 유출 |
| AI 에이전트 혼란         | 에이전트가 포트 번호를 추측    |
|                          | 하거나 하드코딩                |
| 새로고침 시 잘못된 앱    | 브라우저 탭에서 다른 앱이 표시 |

## 아키텍처

```
portless myapp next dev
        │
        ├─ 1) 프록시 실행 여부 확인
        │     (없으면 자동 기동)
        │
        ├─ 2) 랜덤 포트 할당 (4000~4999)
        │     PORT, HOST 환경변수 주입
        │
        ├─ 3) routes.json에 라우트 등록
        │     { hostname, port, pid }
        │
        └─ 4) 앱 프로세스 spawn

브라우저 → myapp.localhost:1355
              │
        프록시 (포트 1355)
              │
        Host 헤더 파싱 → routes.json 조회
              │
        http.request()로 백엔드 포워딩
              │
        localhost:4xxx (실제 앱)
```

프록시는 Node.js의 `http`/`http2` 모듈만 사용한다.
외부 의존성 없이 순수 Node.js로 리버스 프록시를
구현한 것이 특징이다.

## 프로젝트 구조

```
portless/
├── packages/portless/src/
│   ├── cli.ts          # CLI 진입점 (31KB)
│   ├── proxy.ts        # 리버스 프록시 서버 (13KB)
│   ├── routes.ts       # 라우트 저장소 (8KB)
│   ├── certs.ts        # TLS 인증서 관리 (19KB)
│   ├── cli-utils.ts    # 포트/프로세스 유틸 (14KB)
│   ├── utils.ts        # 공통 유틸리티
│   ├── types.ts        # 타입 정의
│   └── index.ts        # 공개 API
├── apps/docs/          # Next.js 문서 사이트
├── tests/e2e/          # E2E 테스트 픽스처
└── skills/portless/    # 에이전트 스킬 정의
```

## 핵심 코드 분석

### 프록시 서버 (`proxy.ts`)

외부 라이브러리 없이 `http.request()`로
리버스 프록시를 구현한다.

**바이트 피킹(Byte-Peeking)으로 프로토콜 감지:**

단일 포트에서 HTTP와 HTTPS를 동시에 처리한다.
`net.Server`가 첫 바이트를 읽어
`0x16`(TLS ClientHello)이면 HTTP/2 서버로,
아니면 HTTP/1.1 서버로 라우팅한다.

```typescript
socket.once("readable", () => {
  const buf = socket.read(1);
  socket.unshift(buf);
  if (buf[0] === 0x16) {
    h2Server.emit("connection", socket);
  } else {
    plainServer.emit("connection", socket);
  }
});
```

HTTP/2 클라이언트에 HTTP/1.1 백엔드 응답을 전달할 때
hop-by-hop 헤더를 제거한다.
이것은 HTTP/2 명세의 요구사항이다.

```typescript
const HOP_BY_HOP_HEADERS = new Set([
  "connection", "keep-alive",
  "proxy-connection", "transfer-encoding",
  "upgrade",
]);
```

`X-Portless-Hops` 헤더로 프록시 루프를 감지한다.
최대 5홉까지 허용하며, 이를 초과하면
HTTP 508(Loop Detected)을 반환한다.

```typescript
const PORTLESS_HOPS_HEADER = "x-portless-hops";
const MAX_PROXY_HOPS = 5;
```

`X-Forwarded-*` 헤더를 올바르게 설정해
백엔드 앱이 원래 요청 정보를 파악할 수 있게 한다.

WebSocket 업그레이드도 완전히 지원한다.
`upgrade` 이벤트를 가로채 양방향 소켓 파이프를
설정하고, `101 Switching Protocols` 응답을
그대로 전달한다.

라우트가 없을 때는 활성 앱 목록을 링크와 함께
보여주는 HTML 페이지를 반환해 탐색성을 높인다.

### 라우트 관리 (`routes.ts`)

파일 시스템 기반 라우트 저장소다.
`routes.json`에 라우트 매핑을 JSON으로 저장한다.

```typescript
export interface RouteMapping extends RouteInfo {
  pid: number;
}
```

`fs.mkdirSync()`로 원자적 디렉토리 잠금을
구현한다. POSIX에서 mkdir은 원자적이므로
`EEXIST` 에러로 잠금 충돌을 감지한다.

```typescript
const STALE_LOCK_THRESHOLD_MS = 10_000;
const LOCK_MAX_RETRIES = 20;
const LOCK_RETRY_DELAY_MS = 50;
```

동기 대기에 `Atomics.wait()`를 사용하는 점이
독특하다. `setTimeout`은 비동기라서 잠금
흐름에 적합하지 않으므로, `SharedArrayBuffer`
위에서 동기 sleep을 구현한다.

```typescript
private static readonly sleepBuffer =
  new Int32Array(new SharedArrayBuffer(4));
private syncSleep(ms: number): void {
  Atomics.wait(RouteStore.sleepBuffer, 0, 0, ms);
}
```

라우트 로드 시 각 항목의 PID를
`process.kill(pid, 0)`으로 검증해 죽은
프로세스의 stale 라우트를 자동 정리한다.

시스템 디렉토리(`/tmp/portless`)는
sticky bit(0o1777)로 설정해 다중 사용자 환경에서
안전하게 공유한다.

### 인증서 관리 (`certs.ts`)

로컬 CA를 생성하고 시스템 트러스트 스토어에
등록하는 전체 PKI 파이프라인을 구현한다.

- CA 유효기간: 10년(3650일)
- 서버 인증서 유효기간: 1년(365일)
- 만료 7일 전 자동 재생성
- SHA-1 서명 감지 및 거부(보안 강화)
- openssl CLI 호출로 인증서 생성

```typescript
const CA_VALIDITY_DAYS = 3650;
const SERVER_VALIDITY_DAYS = 365;
const EXPIRY_BUFFER_MS = 7 * 24 * 60 * 60 * 1000;
```

SNI(Server Name Indication) 콜백으로
호스트명별 인증서 선택을 지원한다.
`*.localhost` 와일드카드 인증서는 공개 접미사
경계(public-suffix boundary)에서 동작하지
않으므로, 호스트명마다 개별 인증서를 온디맨드로
생성하고 메모리 + 디스크에 캐시한다.
동시 요청 시 중복 생성을 방지하는 Promise
디듀플리케이션도 구현되어 있다.

### 프레임워크 자동 감지 (`cli-utils.ts`)

`PORT` 환경변수를 무시하는 프레임워크를 감지하고
적절한 CLI 플래그를 자동 주입한다.

| 프레임워크     | 주입 플래그                   |
|----------------|-------------------------------|
| Vite           | `--port PORT --host 127.0.0.1`|
| React Router   | `--port PORT --host 127.0.0.1`|
| Astro          | `--port PORT --host 127.0.0.1`|
| Angular (ng)   | `--port PORT --host 127.0.0.1`|

IPv6 바인딩을 방지하기 위해 `--host 127.0.0.1`을
명시적으로 주입하는 점이 세심하다.

### 상태 디렉토리 전략

포트 번호에 따라 상태 디렉토리를 분리한다.

| 조건                  | 디렉토리         |
|-----------------------|------------------|
| 특권 포트 (< 1024)   | `/tmp/portless`  |
| 비특권 포트 (>= 1024) | `~/.portless`    |

`PORTLESS_STATE_DIR` 환경변수로 재정의 가능하다.

특권 포트는 root와 일반 사용자 프로세스가
파일을 공유해야 하므로 `/tmp`를 사용한다.
`fixOwnership()`으로 sudo 실행 후
파일 소유권을 원래 사용자에게 복원한다.

## 기술 스택

| 항목           | 도구                     |
|----------------|--------------------------|
| 언어           | TypeScript               |
| 런타임         | Node.js 20+              |
| 빌드           | tsup                     |
| 테스트         | Vitest                   |
| 모노레포       | pnpm workspace + Turbo   |
| 린트           | ESLint + Prettier        |
| Git 훅         | Husky + lint-staged      |
| 프로덕션 의존성| chalk (단 하나)          |
| 문서 사이트    | Next.js + MDX            |
| 라이선스       | Apache-2.0               |
| OS 지원        | macOS, Linux             |

프로덕션 의존성이 `chalk` 하나뿐이라는 점이
인상적이다. 프록시, TLS, 프로세스 관리를
모두 Node.js 내장 모듈로 처리한다.

## 설치 및 사용

```bash
# 전역 설치 (npx로 실행하지 않는다)
npm install -g portless

# 앱 실행
portless myapp next dev
# → http://myapp.localhost:1355

# HTTPS 모드
portless proxy start --https
portless myapp next dev
# → https://myapp.localhost:1355

# 활성 라우트 확인
portless list

# CA 신뢰 등록
portless trust

# 비활성화
PORTLESS=0 next dev
```

## 주요 CLI 명령

| 명령어                           | 설명                    |
|----------------------------------|-------------------------|
| `portless <name> <cmd>`         | 앱 실행 및 등록         |
| `portless proxy start`          | 프록시 시작             |
| `portless proxy start --https`  | HTTPS 모드로 시작       |
| `portless proxy stop`           | 프록시 중지             |
| `portless list`                 | 활성 라우트 목록        |
| `portless trust`                | CA 트러스트 등록        |
| `portless unregister <name>`    | 라우트 제거             |

### CLI 구현 (`cli.ts`)

CLI 프레임워크(yargs, commander) 없이
직접 인수를 파싱한다.

프록시 데몬은 `detached: true`로 분리된
백그라운드 프로세스로 기동된다.
stdout/stderr를 로그 파일로 리다이렉션하고,
부모 프로세스는 프록시가 준비될 때까지 폴링한 뒤
종료한다.

`npx`와 `pnpm dlx` 실행을 명시적으로 차단한다.
`sudo npx`는 root 권한으로 패키지를 해석하므로
보안 위험이 있기 때문이다.

```typescript
const isNpx =
  process.env.npm_command === "exec" &&
  !process.env.npm_lifecycle_event;
```

`node_modules/.bin`을 CWD부터 상위로
탐색하면서 PATH에 추가해,
`npx` 없이도 로컬 바이너리를 직접 실행한다.

## 인사이트

### 1) 의존성 최소주의가 신뢰성을 만든다

프로덕션 의존성이 `chalk` 하나다.
HTTP 프록시, TLS 인증서 생성, 프로세스 관리를
전부 Node.js 내장 모듈로 구현했다.

`http-proxy`나 `express` 같은 검증된 라이브러리
대신 `http.request()`로 직접 프록시를 구현한
선택은 과감하다. 하지만 개발 도구라는 맥락에서
프로덕션 트래픽을 처리할 필요가 없으므로 합리적이다.

의존성이 적다는 것은 공급망 공격 표면이 작고,
버전 충돌이 없으며, 설치가 빠르다는 의미다.
CLI 도구에서 이것은 핵심 경쟁력이 된다.

### 2) RFC 6761이 이 도구의 존재를 가능하게 한다

`.localhost`가 항상 127.0.0.1로 해석된다는
RFC 6761 보장이 없었다면, 이 도구는 사용자에게
`/etc/hosts` 수정을 요구해야 했을 것이다.

표준이 만들어둔 "무료 인프라"를 활용한 것이다.
`myapp.localhost`는 DNS 조회 없이 작동하므로
오프라인에서도 안정적이다.

### 3) 파일 시스템이 IPC를 대신한다

프로세스 간 통신에 소켓이나 gRPC 대신
`routes.json` 파일을 사용한다.
`fs.watch()`로 변경을 감지하고
디렉토리 잠금으로 동시성을 제어한다.

이 설계는 단순하지만 영리하다.
프록시 프로세스와 앱 프로세스가 서로의 존재를
알 필요 없이 파일만 공유하면 된다.
프로세스가 비정상 종료해도 PID 기반 정리가
자동으로 stale 라우트를 제거한다.

다만 `fs.watch()`가 지원되지 않는 환경을 위해
3초 간격 폴링 폴백도 준비해둔 점이 방어적이다.

### 4) sudo 문제를 우아하게 해결한다

HTTPS를 위해 포트 443이나 80을 쓰면
sudo가 필요하다. 이때 두 가지 문제가 생긴다:
파일 소유권이 root로 바뀌는 것과,
사용자에게 암묵적 권한 상승을 강제하는 것.

`fixOwnership()`은 `SUDO_UID`/`SUDO_GID`
환경변수로 원래 사용자를 추적하고,
파일 생성 후 소유권을 복원한다.

비특권 포트(1355)에서는 sudo 없이 작동하므로
대부분의 사용자가 권한 문제를 겪지 않는다.
특권 포트가 필요한 경우에만 TTY에서 대화형으로
sudo를 요청한다.

### 5) 프록시 루프 감지가 실전적이다

`x-portless-hops` 헤더로 요청이 프록시를
몇 번 통과했는지 추적한다.
5홉을 초과하면 요청을 거부한다.

이것은 이론적 안전장치가 아니라 실전적 방어다.
Vite의 `server.proxy`에서 `changeOrigin: true`를
빠뜨리면 Host 헤더가 그대로 전달되어
프록시가 자기 자신에게 요청을 보내는
무한 루프가 발생한다.

문서에서도 이 패턴을 명시적으로 경고한다.

### 6) 포트 1355는 의도된 선택이다

1355는 IANA에 등록되지 않은 비특권 포트다.
sudo 없이 바인딩할 수 있으면서도
일반적인 개발 서버 포트(3000, 8080)와 충돌하지
않는다.

도메인 `port1355.dev`를 확보한 것은 이 숫자에
대한 의도를 보여준다. "portless"를 숫자로
읽으면 port-1-3-5-5가 된다.

### 7) 바이트 피킹은 우아한 절충안이다

단일 포트에서 HTTP와 HTTPS를 모두 처리하는
방법으로 첫 바이트 검사를 선택한 것은
네트워크 프로그래밍의 고전적 기법이다.

`0x16`은 TLS ClientHello의 ContentType이다.
이 한 바이트만으로 프로토콜을 결정하므로
별도 포트 분리(80 + 443)가 필요 없다.

개발 도구에서 "포트 하나만 기억하면 된다"는
핵심 가치와 정확히 부합하는 기술 선택이다.

### 8) `Atomics.wait()`는 의외의 활용이다

자바스크립트에서 동기 sleep이 필요한 경우는
극히 드물다. 하지만 파일 잠금에서는
비동기 sleep이 흐름을 복잡하게 만든다.

`SharedArrayBuffer` + `Atomics.wait()`로
이벤트 루프를 차단하지 않으면서 동기적 대기를
구현한 것은 Node.js 생태계에서 보기 드문
패턴이다. WASM이나 Worker 없이도
`Atomics.wait()`가 메인 스레드에서
유용할 수 있음을 보여준다.

### 9) AI 에이전트를 위한 설계가 명시적이다

"For humans and agents"라는 부제가 단순한
마케팅이 아니다. AI 코딩 에이전트가
`localhost:3000`을 추측하거나 하드코딩하는
문제를 구조적으로 해결한다.

안정적인 `myapp.localhost:1355` URL은
`.env` 파일이나 프롬프트에 한 번만 명시하면
세션과 관계없이 동작한다.

`skills/portless/SKILL.md`에 에이전트용
스킬 정의까지 포함한 것은 AI 에이전트 통합을
일급 시민으로 대우한다는 증거다.

### 10) E2E 테스트가 크로스 언어로 확장된다

E2E 테스트가 11개 프레임워크를 커버한다.
Angular, Astro, Express, FastAPI, Flask, Hono,
Next.js, Nuxt, Remix, Svelte, Vite.

Python 프레임워크(FastAPI, Flask)까지 포함한 것은
Portless가 Node.js 전용 도구가 아님을 증명한다.
`PORT` 환경변수를 존중하는 어떤 서버든 작동한다.

각 테스트가 고유 프록시 포트(19001~19011)를
사용해 병렬 실행이 가능하다.

## 제한 사항

- Windows 미지원 (macOS, Linux만 지원)
- Vercel Labs 실험 프로젝트 (공식 제품 아님)
- `os` 필드로 npm 설치 단계에서 차단
- WSL2에서 동작 가능하나 공식 테스트 없음

## 관련 문서

- [agent-browser](../ai/agent-browser.md)
