# Claude Code Remote Control: 내 컴퓨터의 세션을 폰과 브라우저에서 이어 쓰기

## 소개

Remote Control은 내 컴퓨터에서 돌아가는 Claude Code 세션에
claude.ai/code나 Claude 모바일 앱을 연결하는 기능이다.[^rc]
실행은 계속 내 컴퓨터에서 하고, 웹과 모바일은 그 세션을 보는 창이다.[^rc]
그래서 로컬 파일, MCP 서버, 프로젝트 설정을 그대로 쓴다.[^rc]
대신 컴퓨터가 켜져 있고 `claude` 프로세스가 살아 있어야 한다.[^rc]

이 기능의 가치는 폰으로 코딩하는 데 있지 않다.
로컬 환경에서 돌아가는 에이전트에 사람이 개입할 지점을
어디서든 열어 두는 데 있다.
이 문서는 그 관점에서 쓸모 있는 부분만 추렸다.

## 시작하는 법

| 입력                      | 동작                                            |
| ------------------------- | ----------------------------------------------- |
| `claude remote-control`   | 서버 모드. 한 프로세스가 세션 여러 개를 받는다  |
| `claude --rc`             | 평소처럼 대화하면서 원격 연결도 켠다            |
| `/rc` (`/remote-control`) | 하던 세션을 대화 기록째 원격으로 연결한다       |

위 표는 공식 문서의 진입점이다.[^rc]
`claude rc`는 문서에 없는 형태다.
`claude rc --help`를 실행했더니 도움말 없이 2분 넘게 끝나지 않았고,
원인은 확인하지 못했다.
줄여 쓰려면 `claude --rc`나 `/rc`를 쓴다.

연결은 세션 URL을 열거나, QR 코드를 스캔하거나,
claude.ai/code와 앱의 Code 탭 목록에서 찾으면 된다.[^rc]
서버 모드는 스페이스바로 QR 코드를 띄운다.[^rc]
구독(Pro, Max, Team, Enterprise)과 claude.ai 로그인이 필요하고
API 키, Bedrock, 사용자 지정 `ANTHROPIC_BASE_URL`에서는 쓸 수 없다.[^rc]

## 개발할 때 좋은 점

### 승인 대기를 없앤다

에이전트 작업에서 가장 흔한 낭비는
권한 확인을 기다리며 멈춰 있는 시간이다.
`/config`에서 `Push when actions required`를 켜면
권한 요청과 질문이 폰 알림으로 오고,
`Push when Claude decides`를 켜면 긴 작업이 끝났을 때 알려 준다.[^rc]
승인 한 번에 자리로 돌아오지 않아도 된다는 점이 핵심이다.

### 폰에서 병렬 세션을 연다

```bash
claude remote-control --spawn worktree --name "til"
```

서버가 이 옵션으로 떠 있으면
폰이나 웹에서 새 세션을 열 때마다 별도 git worktree가 생긴다.[^rc]
기본값 `same-dir`은 세션들이 같은 디렉터리를 공유해
같은 파일을 고치면 충돌한다.[^rc]
동시 세션 상한은 기본 32개다.[^rc]
서로 다른 파일을 건드리는 작업을 나눠 맡길 때만 이득이다.

### 세션끼리 말하게 한다

이 기능이 가장 눈여겨볼 만하다.
Claude는 `ListAgents`와 `SendMessage` 도구로
내 다른 세션을 찾아 메시지를 보낸다.[^xs]
쓰임새는 문서가 꼽은 네 가지다.[^xs]

- 한 세션이 알아낸 사실을 영향받는 세션에 넘긴다.
- 같은 저장소의 worktree 세션들끼리 무엇이 병합됐는지 알린다.
- 오래 걸리는 작업의 상태를 보고받는다.
- 다른 머신이나 클라우드의 세션에 메시지를 보낸다.

프롬프트에서 `@api-worker`처럼 세션 이름을 멘션해 대상을 지정할 수 있다.[^xs]
"마이그레이션 세션이 끝나면 알려 줘"라고 하면
상대 세션이 다음에 유휴 상태가 되거나 종료할 때 알림을 한 번 받는다.[^xs]
토큰을 쓰지 않고 기다릴 수 있다는 점이 쓸모 있다.[^xs]

Remote Control과의 관계는 이렇다.
같은 머신의 세션끼리는 소켓으로 직접 오가서 Anthropic 서버를 거치지 않는다.[^xs]
다른 머신이나 클라우드 세션은 이 세션이 Remote Control에 연결돼 있어야
목록에 보이고, 메시지는 Anthropic 서버를 거친다.[^xs]
집 맥, 사무실 서버, 클라우드 세션을 한 대화에서 부릴 수 있다는 뜻이다.
이 조합은 문서 내용에서 이끌어 낸 추론이고,
직접 구성해 시험해 본 것은 아니다.

### 외부 이벤트를 세션에 밀어 넣는다

Channels는 MCP 서버가 이벤트를 실행 중인 세션에 밀어 넣는 기능이다.[^ch]
Telegram, Discord, iMessage 플러그인이 기본으로 제공된다.[^ch]
웹훅 수신기를 직접 만들면
CI 실패나 에러 트래커 알림이 파일을 이미 열어 둔 세션에 도착한다.[^ch]

```bash
claude --channels plugin:telegram@claude-plugins-official
```

Remote Control은 내가 세션에 말을 거는 길이고,
Channels는 세상이 세션에 말을 거는 길이다.
문서도 둘을 서로 다른 칸에 두고, 채팅 앱에서 질문하면
내 파일을 가진 로컬 세션이 답한다고 설명한다.[^ch]
Channels는 research preview이고 조직이 허용해야 한다.[^ch]

### 클라우드와 나눠 쓴다

Remote Control은 로컬 환경이 필요한 작업에,
클라우드 세션은 저장소를 클론하지 않고 시작하거나
컴퓨터를 꺼도 되는 작업에 맞다.[^rc]
Projects는 한 대화에서 일을 여러 스레드로 나눠 병렬 클라우드 세션으로
돌리다가, 내 컴퓨터에만 있는 것이 필요하면 그 스레드만
Remote Control로 로컬에서 돌린다.[^proj]
Projects는 Pro와 Max에서 공개 베타로 점진 배포 중이고
Team과 Enterprise에는 아직 없다.[^proj]
폰에서 작업을 던지기만 하려면 Desktop의 Dispatch가 있고
Pro와 Max에서 쓸 수 있다.[^desk]

## 알아 둘 위험

- 대화 기록이 Anthropic 서버에 저장된다. 메시지, 응답, 도구 활동이
  모두 포함된다.[^rc] 비밀 값이 대화에 섞이는 작업이면 먼저 따진다.
- 폰의 `!` 줄은 셸 명령이 아니라 메시지로 처리된다.[^rc]
- 다른 세션의 메시지는 내 승인을 대신할 수 없고,
  명령으로 실행되지 않고, 설정을 바꾸지도 못한다.[^xs]
- 권한을 건너뛰는 모드의 세션은 다른 세션의 메시지를 받으면
  기본적으로 승인 대기로 보류한다.[^xs]
  무인 작업자에게 메시지를 받게 하려면 `crossSessionInbound`를 명시한다.[^xs]
- 채널은 허용 목록에 있는 발신자만 밀어 넣을 수 있다.
  채널이 권한 중계를 선언하면 그 발신자는 도구 사용도 승인할 수 있으므로
  믿는 사람만 넣는다.[^ch]
- 자동 연결(`Enable Remote Control for all sessions`)을 켜면
  프로세스마다 원격 세션이 생긴다.[^rc]
  저장소의 `.claude/settings.json`에서는 `false`만 효력이 있다.[^rc]

## 한계

- 터미널을 닫거나 프로세스가 끝나면 세션이 오프라인이 된다.
  SSH로 쓸 때는 `tmux`나 `screen` 안에서 시작한다.[^rc]
- 서버를 Ctrl+C로 멈춰도 약 4시간 안에는 같은 디렉터리에서
  `claude remote-control`로 세션을 되살릴 수 있다.[^rc]
- 서버 모드는 네트워크가 약 10분 넘게 끊기면 종료한다.[^rc]
- `/plugin`, `/resume` 같은 명령은 폰에서 안 된다.
  `/compact`, `/model`, `/effort`, `/usage` 등은 된다.[^rc]
- 컨테이너 안의 세션과 호스트의 세션은 서로 메시지를 보낼 수 없다.[^xs]
- Zero Data Retention이나 HIPAA 구성을 적용한 조직은 쓸 수 없다.[^rc]

## 도입 판단

먼저 폰 푸시 두 가지만 켜고 일주일 쓴다.
알림을 받고도 결국 컴퓨터 앞에서 승인해야 하는 일이 잦거나
세션이 오프라인인 날이 많다면 기대한 이점이 없는 것이다.
그렇지 않다면 `--spawn worktree` 서버로 병렬 작업을 맡기고,
세션이 서로 알려야 할 일이 생길 때 세션 간 메시지를 시험한다.
Channels는 CI나 알림을 세션이 받아야 할 필요가 분명할 때 붙인다.

대화가 서버에 저장되는 것을 조직이나 프로젝트가 허용하지 않으면
처음부터 쓰지 않는다.

## 관련 문서

- [Claude Code on the Web 제품 발표](claude-code-on-the-web.md)

---

[^rc]: Anthropic, [Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control)

[^xs]: Anthropic, [Message your other Claude Code sessions](https://code.claude.com/docs/en/cross-session-messaging)

[^ch]: Anthropic, [Push events into a running session with channels](https://code.claude.com/docs/en/channels)

[^proj]: Anthropic, [Let Claude coordinate ongoing work with Projects](https://code.claude.com/docs/en/claude-projects)

[^desk]: Anthropic, [Desktop application](https://code.claude.com/docs/en/desktop)
