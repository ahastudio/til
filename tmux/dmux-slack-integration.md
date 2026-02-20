# dmux 외부 제어와 Slack 연동

dmux는 HTTP API를 제공한다.
공식 문서([dmux.ai](https://dmux.ai/))에
"setup guides, configuration, hooks, and the
HTTP API reference"가 있다고 명시되어 있다.
이를 활용하면 외부에서 dmux를 프로그래밍적으로
제어할 수 있다.

## 외부 제어 수단

### HTTP API

dmux가 로컬 서버를 띄우고 API를 노출한다.
pane 생성, 프롬프트 전달, 병합 같은 핵심 동작을
API 호출로 수행할 수 있을 것으로 보인다.

> 구체적인 엔드포인트는
> [dmux.ai](https://dmux.ai/)의
> HTTP API reference를 참고할 것.

### Lifecycle Hooks

worktree 생성, 병합 전/후 등 주요 시점에
커스텀 스크립트를 실행할 수 있다.
여기에 Slack Incoming Webhook 호출을 넣으면
작업 상태를 실시간으로 Slack에 알릴 수 있다.

```bash
# .dmux-hooks/post-merge 예시
#!/bin/bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-type: application/json' \
  -d "{\"text\": \"✅ 병합 완료: $BRANCH\"}"
```

## Slack 연동 구조

모바일에서 매끄럽게 쓰려면 양방향 연동이 필요하다.

### dmux → Slack (알림)

Lifecycle Hook에서 Slack Incoming Webhook을
호출한다. 설정이 간단하고 바로 쓸 수 있다.

- 에이전트 작업 시작/완료 알림
- 병합 성공/실패 알림
- 충돌 발생 시 사람에게 알림

### Slack → dmux (명령)

Slack Bot이 slash command나 메시지를 받아서
dmux HTTP API를 호출하는 구조다.

```txt
[모바일 Slack]
    │
    ▼
[Slack Bot (slash command)]
    │
    ▼
[터널 (ngrok / Cloudflare Tunnel)]
    │
    ▼
[로컬 dmux HTTP API]
    │
    ▼
[tmux pane 생성 → 에이전트 실행]
```

### 터널링이 필요한 이유

dmux는 로컬 머신에서 돌아간다.
Slack Bot이 외부에서 접근하려면
로컬 API를 인터넷에 노출해야 한다.

| 방법                  | 특징                       |
| --------------------- | -------------------------- |
| ngrok                 | 빠른 설정, 무료 플랜 있음  |
| Cloudflare Tunnel     | 안정적, 도메인 연결 가능   |
| Tailscale Funnel      | VPN 기반, 보안 우수        |

## 모바일 워크플로우 예시

```txt
1. Slack에서 /dmux "로그인 버그 수정" 입력
2. Slack Bot → 터널 → dmux HTTP API 호출
3. dmux가 worktree + pane 생성, 에이전트 실행
4. 에이전트 작업 완료 → hook → Slack 알림
5. Slack에서 /dmux-merge 입력
6. dmux가 메인 브랜치에 병합
7. 결과를 Slack으로 알림
```

이 구조라면 모바일에서 tmux 화면을 직접 볼
필요 없이 Slack만으로 에이전트를 관리할 수 있다.

## 대안: tmux 직접 접근

Slack 연동 없이 모바일에서 직접 접근하는
방법도 있다.

- **SSH 클라이언트** (Termius, Blink Shell 등)로
  서버에 접속하여 `tmux attach`
- **VS Code Remote** + 모바일 브라우저
- **Mosh** — 불안정한 모바일 네트워크에 적합

다만 모바일에서 tmux를 직접 조작하는 것은
화면이 작아서 불편하다.
Slack 연동이 UX 측면에서 훨씬 낫다.

## 참고

- [dmux 공식 사이트](https://dmux.ai/)
- [dmux GitHub](https://github.com/standardagents/dmux)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [Slack Bolt (Bot 프레임워크)](https://slack.dev/bolt-js/)
- [ngrok](https://ngrok.com/)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
