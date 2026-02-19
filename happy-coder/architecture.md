# 아키텍처

| 구성 요소       | 역할                              |
| --------------- | --------------------------------- |
| Happy App       | 웹·모바일(Expo) 클라이언트       |
| Happy CLI       | Claude Code/Codex CLI 래퍼       |
| `happy daemon`  | 백그라운드 서비스. 원격 요청 수신 |
| `happy-agent`   | 원격 세션 제어 CLI (생성, 조회)  |
| Happy Server    | 릴레이 서버. 암호화된 동기화 처리 |

기술 스택은 TypeScript 기반 Yarn 모노레포 구조다.
Docker를 지원한다.

## `happy daemon`

`happy` 실행 시 자동으로 백그라운드에서 시작된다.
CLI 진입점(`index.ts`)에서
`isDaemonRunningCurrentlyInstalledHappyVersion()`
으로 데몬 상태를 확인하고, 실행 중이 아니면
`spawnHappyCLI(['daemon', 'start-sync'])`로
detached 프로세스를 기동한다. 사용자가
`happy daemon`을 직접 실행할 필요는 없다.

데몬 시작 시퀀스:

1. 락 파일 획득 (atomic `O_CREAT | O_EXCL`,
   5회 지수 백오프 재시도).
2. `~/.happy/access.key`에서 자격증명 로드.
3. Happy Server에 머신 등록.
4. 로컬 Fastify HTTP 서버 시작
   (`127.0.0.1`, localhost 전용).
5. Happy Server와 WebSocket 연결 수립
   (`ApiMachineClient`, `clientType:
   'machine-scoped'`). 20초 간격 keep-alive.
6. `daemon.state.json`에 PID, 포트, 버전 기록.
7. 60초 간격 하트비트로 세션 정리 및 버전
   불일치 감지.

로컬 HTTP 서버가 제공하는 엔드포인트:

| 엔드포인트         | 역할                    |
| ------------------ | ----------------------- |
| `/spawn-session`   | 새 세션 생성            |
| `/stop-session`    | 세션 종료               |
| `/list`            | 추적 중인 세션 목록     |
| `/session-started` | 생성된 세션의 등록 웹훅 |
| `/stop`            | 데몬 종료               |

WebSocket RPC 핸들러:

| RPC                   | 역할                  |
| --------------------- | --------------------- |
| `spawn-happy-session` | 원격 세션 시작 (핵심) |
| `stop-session`        | 원격 세션 종료        |
| `stop-daemon`         | 원격 데몬 종료        |

`happy` 세션이 모두 종료되어도 데몬은 백그라운드에
잔류하므로 원격 세션 시작이 가능하다. 버전 불일치
시(예: `npm update` 후) 하트비트에서 감지하여
새 데몬을 자동 기동하고 기존 데몬을 교체한다.

macOS LaunchDaemon 설치 기능(`happy daemon
install`)이 코드에 존재하지만 현재 사용되지
않는다. `sudo` 권한이 필요하기 때문이다. 따라서
재부팅 후에는 `happy`를 한 번 실행해야 데몬이
다시 뜬다.

## 종단간 암호화

디바이스 간 모든 통신은 릴레이 서버(Happy
Server)를 경유하지만, 코드와 세션 데이터는
클라이언트에서 암호화한 뒤 전송된다. 서버는
암호화된 데이터를 중계만 할 뿐 복호화할 수
없는 영지식(Zero-Knowledge) 설계다.

암호화에는 TweetNaCl(Signal과 동일한 암호화
라이브러리)을 사용한다. 최초 디바이스 페어링
시 QR 코드를 스캔하면 키 교환이 이루어지고,
이후 모든 메시지는 이 키로 암호화된다.

와이어 프로토콜(`@slopus/happy-wire`)이
메시지 형식을 정의한다. 암호화된 페이로드는
`{t: "encrypted", c: "<Base64>"}` 구조로
전송되며, 세션 프로토콜 이벤트(텍스트, 도구
호출, 파일, 턴 관리 등 9종)를 봉투(envelope)
형태로 감싸서 주고받는다.

## 릴레이 서버 (Happy Server)

모든 디바이스 간 통신을 중계하는 백엔드 서버다.
공식 서버(`happy-api.slopus.com`)를 사용하거나
직접 호스팅할 수 있다.

서버 스택:

| 구성 요소    | 기술                    |
| ------------ | ----------------------- |
| 런타임       | Node.js 20              |
| 프레임워크   | Fastify 5               |
| 실시간 통신  | Socket.io               |
| 데이터베이스 | PostgreSQL (Prisma ORM) |
| 캐시·Pub/Sub | Redis (ioredis)         |

Socket.io를 통해 데스크톱 CLI와 모바일·웹 앱
사이의 실시간 양방향 통신을 처리한다. 세션 상태
변경, 에이전트 출력, 사용자 입력이 모두 이
채널을 통해 흐른다.

영지식 설계이므로 서버 관리자도 세션 내용을
볼 수 없다. 서버에 저장되는 것은 암호화된
blob뿐이다.

### 자체 호스팅

Docker 이미지로 자체 호스팅이 가능하다. 독립
실행 (standalone) 모드에서는 외부 의존성 없이
단일 컨테이너로 동작한다.

```bash
docker build -t happy-server -f Dockerfile .
```

```bash
docker run -p 3005:3005 \
  -e HANDY_MASTER_SECRET=<시크릿> \
  -v happy-data:/data \
  happy-server
```

독립 실행 모드의 내부 구성:

| 구성 요소    | 대체 기술                       |
| ------------ | ------------------------------- |
| 데이터베이스 | PGlite (내장 PostgreSQL)        |
| 파일 저장소  | 로컬 파일시스템 (`/data/files`) |
| 메시지 버스  | 인메모리 이벤트 버스            |

주요 환경 변수:

| 변수                  | 필수 | 설명                      |
| --------------------- | ---- | ------------------------- |
| `HANDY_MASTER_SECRET` | O    | 인증·암호화 마스터 시크릿 |
| `PUBLIC_URL`          |      | 파일 URL 기본 주소        |
| `PORT`                |      | 서버 포트 (기본 3005)     |
| `DATA_DIR`            |      | 데이터 디렉토리           |

확장 배포 시 외부 서비스로 전환할 수 있다:

| 변수           | 용도                             |
| -------------- | -------------------------------- |
| `DATABASE_URL` | 외부 PostgreSQL (PGlite 대체)    |
| `REDIS_URL`    | 외부 Redis                       |
| `S3_HOST`      | S3/MinIO (로컬 파일 저장소 대체) |
