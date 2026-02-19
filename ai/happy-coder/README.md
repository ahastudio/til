# Happy Coder - AI 코딩 에이전트 원격 제어 클라이언트

<https://happy.engineering/>

<https://github.com/slopus/happy>

Claude Code와 Codex를 모바일·웹에서 원격 제어하는
오픈소스 클라이언트. 종단간 암호화(E2EE)로 코드를
보호하면서 어디서든 AI 코딩 에이전트의 작업을
모니터링하고 개입할 수 있다.

## 설치

```bash
npm install -g happy-coder
```

Homebrew Formulae:
<https://formulae.brew.sh/formula/happy-coder>

```bash
brew install happy-coder
```

## 사용법

`claude` 대신 `happy`, `codex` 대신 `happy codex`를
사용한다. 기존 워크플로우를 거의 바꾸지 않아도 된다.

```bash
# Claude Code 래핑
happy

# Codex 래핑
happy codex
```

### 벤더 인증 (`happy connect`)

원격 디바이스에서 에이전트 세션을 제어하려면 AI
벤더의 API 키가 필요하다. `happy connect`는 이
키를 Happy 클라우드에 암호화하여 저장한다.

사전에 `happy auth login`으로 Happy 계정에
로그인해야 한다.

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
   (`authenticateClaude()`,
   `authenticateCodex()`,
   `authenticateGemini()`).
3. 획득한 토큰을
   `api.registerVendorToken()`으로
   Happy 클라우드에 등록한다.
4. Gemini의 경우
   로컬(`~/.gemini/oauth_creds.json`)에도
   자격증명을 동기화한다.

`happy connect status`로 각 벤더의 연결 상태를
확인할 수 있다. JWT 토큰에서 이메일을 추출하고
만료 여부를 표시한다.

로컬 세션과 원격 세션의 인증 경로가 다르다:

| 시작 방식                       | 사용 인증                    |
| ------------------------------- | ---------------------------- |
| 로컬 (`claude`, `happy`)        | 머신의 로컬 Anthropic 계정  |
| 원격 (모바일 Start New Session) | `happy connect` 클라우드 키 |

각 디바이스에 서로 다른 Anthropic 계정이
로그인되어 있어도 원격 세션 시작에는 문제가 없다.
`happy connect`로 등록한 키가 모든 원격 세션에
공통으로 쓰이기 때문이다. 다만 같은 머신에서
로컬 세션과 원격 세션이 서로 다른 계정으로
실행될 수 있으므로 과금 추적에 주의해야 한다.

## 특장점

### 원격 모니터링과 제어

데스크톱에서 `happy` 명령으로 세션을 시작하면
모바일이나 웹에서 진행 상황을 실시간으로 확인할
수 있다. 에이전트가 권한을 요청하거나 오류가
발생하면 푸시 알림을 보내준다. 자리를 비운
동안에도 AI가 무엇을 만들고 있는지 파악할 수
있다.

### 디바이스 전환

모바일에서 제어하다가 데스크톱 키보드의 아무
키나 누르면 즉시 데스크톱으로 제어권이 돌아온다.
별도의 전환 절차 없이 한 번의 키 입력으로 전환이
완료된다.

### 오픈소스

MIT 라이선스. 텔레메트리나 추적 코드가 없다.
코드를 직접 감사(audit)할 수 있다.

### Start New Session (v1.5.0)

v1.5.0(2025-09-18)에서 추가. 모바일 기기에서
원격으로 새로운 Claude Code 또는 Codex 세션을
직접 생성하고 시작할 수 있다.

| 항목   | 이전            | 이후                |
| ------ | --------------- | ------------------- |
| 시작   | 데스크톱에서만  | 모바일에서도 가능   |
| 모바일 | 모니터링만      | 생성 + 모니터링     |
| 지원   | Claude Code     | Claude Code + Codex |
| 흐름   | 단방향 핸드오프 | 양방향 전환         |

작동 방식:

1. 모바일 앱에서 "Start New Session" 버튼을
   탭한다.
2. Claude Code 또는 Codex 중 에이전트를
   선택한다.
3. 작업 디렉토리와 초기 프롬프트를 입력한다.
4. Happy Server가 데스크톱 데몬의 WebSocket
   연결로 `spawn-happy-session` RPC를
   호출한다.
5. 데몬의 `spawnSession()`이 토큰을 환경
   변수로 주입한 뒤 에이전트 프로세스를
   기동한다. Claude의 경우
   `CLAUDE_CODE_OAUTH_TOKEN`, Codex의 경우
   `auth.json`에 토큰을 기록한다.
6. 세션 프로세스가 데몬의
   `/session-started` 웹훅을 호출하여
   등록을 완료한다.
7. 데몬이 Expo 푸시 알림으로 모바일에 세션
   시작을 통지한다.

이때 사용되는 인증 토큰은 RPC 페이로드에
포함된 것으로, 머신의 로컬 계정이 아니라
`happy connect`로 등록한 클라우드 키다.

핵심은 샌드박스나 별도 서비스에 접속하는 것이
아니라, 실제 머신에서 실행되는 실제 Claude Code
세션에 직접 연결된다는 점이다. 세션이 시작되면
양쪽 디바이스에서 동일한 세션에 접근할 수 있으며,
"주(primary)" 디바이스와 "보조(secondary)"
디바이스의 구분이 없다.

### 병렬 세션 실행

여러 AI 에이전트를 동시에 실행할 수 있다. 한
세션에서 프론트엔드를 리팩토링하는 동안 다른
세션에서 백엔드 테스트를 작성하고, 모바일에서
세션 간을 즉시 전환할 수 있다.

```bash
# 머신 A: 프론트엔드 작업
happy

# 머신 B: 백엔드 작업
happy

# 같은 머신에서 병렬 실행도 가능
# 별도 터미널에서 각각 happy 실행
# 원격 세션은 tmux 세션으로 생성됨
```

## 관련 문서

- [아키텍처](./architecture.md)
- [베스트 프랙티스와 주의점](./best-practices.md)
- [인사이트](./insights.md)

## 앱 다운로드

- iOS: <https://apps.apple.com/us/app/happy-claude-code-client/id6748571505>
- Android: <https://play.google.com/store/apps/details?id=com.ex3ndr.happy>
- 웹: <https://app.happy.engineering/>

## 문서

<https://happy.engineering/docs/>

## 커뮤니티

Discord: <https://discord.gg/happy-coder>
