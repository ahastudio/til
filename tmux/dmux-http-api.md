# dmux HTTP API

dmux는 키보드 단축키 외에 HTTP API를 제공한다.
공식 문서([dmux.ai](https://dmux.ai/))에
"setup guides, configuration, hooks, and the
**HTTP API reference**"가 있다고 명시되어 있다.

<https://dmux.ai>

<https://github.com/standardagents/dmux>

## 의미

키보드 단축키는 사람이 tmux 앞에 앉아 있어야
쓸 수 있다. HTTP API가 있으면 어디서든
프로그래밍적으로 dmux를 제어할 수 있다.

- pane 생성, 프롬프트 전달, 병합 등을
  API 호출로 수행
- CI/CD, 챗봇, 스크립트, 모바일 앱 등
  어떤 클라이언트든 연결 가능
- 사람이 오케스트레이터에서
  시스템이 오케스트레이터로 전환

## Lifecycle Hooks와의 조합

dmux는 worktree 생성, 병합 전/후 등
주요 시점에 커스텀 스크립트를 실행할 수 있다.
HTTP API가 "명령을 보내는 채널"이라면,
Lifecycle Hook은 "결과를 받는 채널"이다.

```txt
[외부 시스템]
    │
    ▼ HTTP API (명령)
[dmux]
    │
    ▼ Lifecycle Hook (결과)
[외부 시스템]
```

이 양방향 구조가 있으면 dmux를 완전히
외부에서 제어할 수 있는 루프가 완성된다.

## 활용 사례

### 1. 슬랙(Slack) 연동 — 모바일 에이전트 관리

Slack Bot이 slash command를 받아
dmux HTTP API를 호출하고,
Lifecycle Hook이 결과를 Slack으로 보낸다.

```txt
[모바일 Slack]
    │
    ▼ /dmux "로그인 버그 수정"
[Slack Bot]
    │
    ▼ HTTP API 호출
[터널 (ngrok 등) → dmux]
    │
    ▼ worktree + 에이전트 실행
[hook → Slack 알림: "작업 완료"]
```

dmux가 로컬에서 돌기 때문에
ngrok, Cloudflare Tunnel, Tailscale Funnel
같은 터널링이 필요하다.

모바일에서 tmux 화면을 직접 볼 필요 없이
Slack만으로 에이전트를 관리할 수 있게 된다.

### 2. CI/CD 파이프라인 — 자동 병렬 작업

GitHub Actions 등에서 이슈가 생기면
dmux API를 호출하여 에이전트를 자동 실행한다.

```txt
[GitHub Issue 생성]
    │
    ▼ webhook
[CI 서버]
    │
    ▼ dmux HTTP API 호출
[dmux: worktree 생성 → 에이전트 실행]
    │
    ▼ hook: 작업 완료
[CI 서버: PR 자동 생성]
```

사람이 이슈만 만들면 코드 작성부터
PR까지 자동으로 진행되는 구조다.

### 3. 웹 대시보드 — 에이전트 모니터링

dmux HTTP API를 폴링하거나
hook으로 이벤트를 수집하면
에이전트 상태를 웹에서 시각화할 수 있다.

- 각 pane의 현재 상태 (실행 중, 완료, 충돌)
- 브랜치별 진행 상황
- 병합 이력과 성공률

### 4. 스케줄러 — 야간 배치 작업

cron이나 스케줄러에서 dmux API를 호출하여
정해진 시간에 에이전트 작업을 실행한다.

```bash
# crontab 예시: 매일 새벽 2시에 기술 부채 정리
0 2 * * * curl -X POST http://localhost:PORT/api \
  -d '{"prompt": "TODO 주석 정리하고 PR 생성"}'
```

## 인사이트

**터미널 도구에서 플랫폼으로.**
HTTP API가 있다는 것은 dmux가 단순한 터미널
도구가 아니라 프로그래밍 가능한 플랫폼이라는
뜻이다. tmux는 사람이 직접 조작하는 도구였지만,
dmux는 다른 시스템이 호출할 수 있는 서비스가 된다.

**에이전트 오케스트레이션의 두 계층.**
에이전트를 관리하는 방법에는 두 가지 계층이 있다.
첫째는 dmux처럼 로컬에서 여러 에이전트를
직접 실행하고 관리하는 것이고,
둘째는 HTTP API를 통해 그 dmux 자체를
외부에서 제어하는 것이다.
메타 오케스트레이션이라 할 수 있다.

**로컬 실행 + 원격 제어 패턴.**
코드는 로컬 머신에서 실행하되
제어는 원격에서 하는 구조가 만들어진다.
컴퓨팅은 개발 머신의 리소스를 활용하면서,
인터페이스는 Slack이든 웹이든 편한 것을 쓴다.
GPU 서버에 에이전트를 돌리면서 카페에서
모바일로 관리하는 시나리오가 가능해진다.

## 참고

- [dmux 공식 사이트](https://dmux.ai/)
- [dmux GitHub](https://github.com/standardagents/dmux)
- [ngrok](https://ngrok.com/)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
