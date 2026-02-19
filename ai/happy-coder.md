# Happy Coder - AI 코딩 에이전트 원격 제어 클라이언트

<https://happy.engineering/>

<https://github.com/slopus/happy>

Claude Code와 Codex를 모바일·웹에서 원격 제어하는
오픈소스 클라이언트. 종단간 암호화(E2EE)로 코드를
보호하면서 어디서든 AI 코딩 에이전트의 작업을 모니터링하고
개입할 수 있다.

## 특장점

### 원격 모니터링과 제어

데스크톱에서 `happy` 명령으로 세션을 시작하면 모바일이나
웹에서 진행 상황을 실시간으로 확인할 수 있다.
에이전트가 권한을 요청하거나 오류가 발생하면 푸시 알림을
보내준다. 자리를 비운 동안에도 AI가 무엇을 만들고 있는지
파악할 수 있다.

### 디바이스 전환

모바일에서 제어하다가 데스크톱 키보드의 아무 키나 누르면
즉시 데스크톱으로 제어권이 돌아온다. 별도의 전환 절차 없이
한 번의 키 입력으로 전환이 완료된다.

### 종단간 암호화와 릴레이 서버

디바이스 간 모든 통신은 릴레이 서버(Happy Server)를
경유하지만, 코드와 세션 데이터는 클라이언트에서
암호화한 뒤 전송된다. 서버는 암호화된 데이터를 중계만
할 뿐 복호화할 수 없는 영지식(Zero-Knowledge) 설계다.

암호화에는 TweetNaCl(Signal과 동일한 암호화 라이브러리)을
사용한다. 최초 디바이스 페어링 시 QR 코드를 스캔하면
키 교환이 이루어지고, 이후 모든 메시지는 이 키로
암호화된다.

와이어 프로토콜(`@slopus/happy-wire`)이 메시지 형식을
정의한다. 암호화된 페이로드는
`{t: "encrypted", c: "<Base64>"}` 구조로 전송되며,
세션 프로토콜 이벤트(텍스트, 도구 호출, 파일, 턴 관리
등 9종)를 봉투(envelope) 형태로 감싸서 주고받는다.

### CLI 래퍼 방식

기존 워크플로우를 거의 바꾸지 않아도 된다.
`claude` 대신 `happy`, `codex` 대신 `happy codex`를
사용하면 된다.

```bash
npm install -g happy-coder
```

Homebrew Formulae:
<https://formulae.brew.sh/formula/happy-coder>

```bash
brew install happy-coder
```

```bash
# Claude Code 래핑
happy

# Codex 래핑
happy codex
```

### 벤더 인증 (`happy connect`)

AI 벤더의 API 키를 Happy 클라우드에 암호화하여
저장하는 명령어다. 원격 디바이스에서 에이전트 세션을
시작하려면 벤더 인증이 필요하다.

사전에 `happy auth login`으로 Happy 계정에 로그인해야
한다.

```bash
# Anthropic 인증
happy connect claude

# OpenAI 인증
happy connect codex

# Google Gemini 인증
happy connect gemini

# 전체 연결 상태 확인
happy connect status
```

인증 흐름:

1. 저장된 Happy 자격증명을 로드한다.
2. 각 벤더의 인증 절차를 진행한다
   (`authenticateClaude()`, `authenticateCodex()`,
   `authenticateGemini()`).
3. 획득한 토큰을 `api.registerVendorToken()`으로
   Happy 클라우드에 등록한다.
4. Gemini의 경우 로컬(`~/.gemini/oauth_creds.json`)에도
   자격증명을 동기화한다.

`happy connect status`로 각 벤더의 연결 상태를 확인할
수 있다. JWT 토큰에서 이메일을 추출하고 만료 여부를
표시한다.

### 오픈소스

MIT 라이선스. 텔레메트리나 추적 코드가 없다.
코드를 직접 감사(audit)할 수 있다.

## 아키텍처

| 구성 요소    | 역할                              |
| ------------ | --------------------------------- |
| Happy App    | 웹·모바일(Expo) 클라이언트        |
| Happy CLI    | Claude Code/Codex CLI 래퍼        |
| Happy Agent  | 원격 세션 관리 CLI (생성, 전송,   |
|              | 모니터링)                         |
| Happy Server | 릴레이 서버. 암호화된 동기화 처리 |

기술 스택은 TypeScript 기반 Yarn 모노레포 구조다.
Docker를 지원한다.

### 릴레이 서버 (Happy Server)

모든 디바이스 간 통신을 중계하는 백엔드 서버다.
공식 서버(`happy-api.slopus.com`)를 사용하거나 직접
호스팅할 수 있다.

서버 스택:

| 구성 요소          | 기술                          |
| ------------------ | ----------------------------- |
| 런타임             | Node.js 20                    |
| 프레임워크         | Fastify 5                     |
| 실시간 통신        | Socket.io                     |
| 데이터베이스       | PostgreSQL (Prisma ORM)       |
| 캐시·Pub/Sub       | Redis (ioredis)               |

Socket.io를 통해 데스크톱 CLI와 모바일·웹 앱 사이의
실시간 양방향 통신을 처리한다. 세션 상태 변경, 에이전트
출력, 사용자 입력이 모두 이 채널을 통해 흐른다.

영지식 설계이므로 서버 관리자도 세션 내용을 볼 수
없다. 서버에 저장되는 것은 암호화된 blob뿐이다.

#### 자체 호스팅

Docker 이미지로 자체 호스팅이 가능하다. 독립 실행
(standalone) 모드에서는 외부 의존성 없이 단일
컨테이너로 동작한다.

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

| 구성 요소      | 대체 기술                     |
| -------------- | ----------------------------- |
| 데이터베이스   | PGlite (내장 PostgreSQL)      |
| 파일 저장소    | 로컬 파일시스템 (`/data/files`)|
| 메시지 버스    | 인메모리 이벤트 버스          |

주요 환경 변수:

| 변수                  | 필수 | 설명                     |
| --------------------- | ---- | ------------------------ |
| `HANDY_MASTER_SECRET` | O    | 인증·암호화 마스터 시크릿|
| `PUBLIC_URL`          |      | 파일 URL 기본 주소       |
| `PORT`                |      | 서버 포트 (기본 3005)    |
| `DATA_DIR`            |      | 데이터 디렉토리          |

확장 배포 시 외부 서비스로 전환할 수 있다:

| 변수           | 용도                              |
| -------------- | --------------------------------- |
| `DATABASE_URL` | 외부 PostgreSQL (PGlite 대체)     |
| `REDIS_URL`    | 외부 Redis                        |
| `S3_HOST`      | S3/MinIO (로컬 파일 저장소 대체)  |

## 주의점

### 네트워크 의존성

원격 제어의 특성상 네트워크 연결이 필수다. 오프라인
환경에서는 사용할 수 없으며, 네트워크 지연이 조작 응답성에
직접 영향을 준다.

### 릴레이 서버 의존성

종단간 암호화로 내용은 보호되지만, 모든 통신이 릴레이
서버를 경유하는 구조다. 공식 서버
(`happy-api.slopus.com`) 장애 시 원격 제어가
불가능해진다. 자체 호스팅으로 가용성을 직접 관리할 수
있지만, 운영 부담이 생긴다.

### CLI 래퍼의 한계

`claude`나 `codex` 위에 래퍼를 씌우는 구조이므로 원본
CLI의 업데이트에 따라 호환성 문제가 발생할 수 있다.
원본 CLI와 래퍼 사이의 버전 동기화에 신경 써야 한다.

### 모바일 입력의 제약

모바일에서 코드를 직접 편집하거나 복잡한 명령을 입력하는
것은 데스크톱 대비 불편하다. 모바일은 모니터링과 간단한
승인/거부 위주로 사용하는 것이 현실적이다.

### IDE 통합 미지원

VS Code 등 IDE와의 통합을 지원하지 않는다. CLI 래퍼
방식만 제공하므로, IDE 내장 터미널이 아닌 환경에서
Claude Code를 사용하는 경우(예: VS Code의 Claude Code
확장)에는 Happy Coder를 적용할 수 없다.

## 인사이트

### 비동기 코딩의 실현

AI 코딩 에이전트가 자율적으로 작업을 수행하는 시대에
"자리를 비워도 괜찮다"는 것은 중요한 가치다.
Happy Coder는 에이전트의 자율성을 높이는 것이 아니라,
사람이 에이전트를 감독하는 방식을 유연하게 만든다.
데스크톱에 묶여 있지 않아도 작업 흐름이 끊기지 않는다.

### Claude Code와의 관계

Claude Code 자체의 기능이 아니라 그 위에 올라가는 서드파티
도구다. Claude Code의 원격 세션 기능이 공식적으로 강화되면
역할이 축소될 수 있다. 반면 현재 시점에서는 Claude Code에
없는 모바일 접근성을 제공하는 유일한 선택지다.

### 에이전트 도구 생태계

Happy Coder의 등장은 AI 코딩 에이전트가 단독 도구가 아니라
생태계의 중심이 되어가고 있음을 보여준다. 에이전트 위에
모니터링, 알림, 원격 제어 같은 부가 도구가 쌓이는 구조는
CI/CD 도구들이 Git 위에 쌓여온 과정과 닮아 있다.

## 앱 다운로드

- iOS:
  <https://apps.apple.com/us/app/happy-claude-code-client/id6748571505>
- Android:
  <https://play.google.com/store/apps/details?id=com.ex3ndr.happy>
- 웹: <https://app.happy.engineering/>

## 문서

<https://happy.engineering/docs/>

## 커뮤니티

Discord: <https://discord.gg/happy-coder>
