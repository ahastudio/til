# Claude Code Desktop — SSH Support

2026년 2월 13일, Anthropic의 Claude Code 팀 엔지니어
Anthony Morris가 트윗으로 발표했다.

> SSH support is now available for Claude Code on desktop.
> Connect to your remote machines and let Claude cook,
> TMUX optional.

이에 대해 전 Stripe 개발자 경험(DevX) 리드이자
전 Microsoft VS Code 팀 출신인
Kenneth Auchenberg는 한마디로 반응했다.

> RIP startups

## 기능 설명

Claude Code Desktop 앱의 세션 환경 선택지가 3가지로 확장됐다.

| 환경     | 설명                                         |
|----------|----------------------------------------------|
| Local    | 로컬 머신에서 직접 실행                      |
| Remote   | Anthropic 클라우드 인프라에서 실행           |
| SSH      | 사용자가 관리하는 원격 머신에서 SSH로 실행   |

SSH 세션을 추가하려면 세션 시작 전 환경 드롭다운에서
"+ Add SSH connection"을 선택한다.

설정 항목:

- **Name**: 연결의 식별 이름
- **SSH Host**: `user`+`hostname` 또는
  `~/.ssh/config`에 정의된 호스트
- **SSH Port**: 기본값 22 (SSH config 사용 가능)
- **Identity File**: 개인 키 경로
  (예: `~/.ssh/id_rsa`)

SSH 세션에서 지원되는 기능:

- Permission modes (Code, Plan)
- Connectors (GitHub, Slack, Linear 등)
- Plugins
- MCP servers

단, 원격 머신에 Claude Code가 설치되어 있어야 한다.

## 도입 시점

정확한 버전 번호가 공식 CHANGELOG에는 없다.
Desktop 앱은 CLI와 별도의 릴리스 사이클을 가지며,
자체 번들된 Claude Code 런타임을 사용한다.

타임라인으로 추정하면:

- **2025-12-19**: SSH Connector 기능 요청 이슈 등록
  ([#15208])
- **2025-12-24**: 웹 버전 SSH Connector 기능 요청
  ([#14666])
- **2026-01경**: amorriscode가 Desktop 대규모 업데이트
  발표 (Plan mode, 권한 알림, 성능 개선 등)
- **2026-02-13**: SSH support 공식 발표 (트윗)
- **2026-02-14**: Windows에서 SSH 경로 하드코딩 버그
  리포트 ([#25659]) — 기능이 방금 출시됐음을 시사

[#15208]: https://github.com/anthropics/claude-code/issues/15208
[#14666]: https://github.com/anthropics/claude-code/issues/14666
[#25659]: https://github.com/anthropics/claude-code/issues/25659

## "RIP startups" — 무엇이 죽는가

Auchenberg의 반응이 의미하는 바는 명확하다.
원격 개발 환경을 제공하던 스타트업들의 존재 이유가
흔들린다는 것이다.

기존에 원격으로 Claude Code를 쓰려면:

1. SSH + tmux를 수동으로 구성하거나
2. 서드파티 MCP 서버를 설치하거나
3. Tailscale/WireGuard VPN을 조합해야 했다

이제 Desktop 앱에서 드롭다운 하나로 SSH 연결이 된다.
GUI에서 원격 머신의 코드베이스를 직접 조작하면서
diff 리뷰, 커넥터, 플러그인까지 모두 쓸 수 있다.

이는 다음 영역의 스타트업에 직접적 위협이다:

- **원격 개발 환경** (Cloud IDE, Remote Dev)
- **AI 코딩 에이전트 래퍼** (Claude Code 위에 SSH를
  얹어 파는 서비스)
- **개발자 인프라 자동화** (원격 세션 관리 도구)

## 인사이트

**플랫폼이 기능을 흡수하는 패턴.**
써드파티가 만들어낸 워크플로가 검증되면
플랫폼이 네이티브로 통합하는 것은 반복되는 역사다.
VS Code의 Remote SSH Extension이
원격 개발 시장을 재편한 것과 같은 맥락이다.

**"TMUX optional"의 의미.**
기존에는 SSH로 Claude Code를 쓰려면
세션 유지를 위해 tmux가 사실상 필수였다.
이제 Desktop 앱이 세션 관리를 대신하므로
tmux 없이도 안정적인 원격 작업이 가능하다.

**남은 기회.**
SSH 세션에서 아직 지원되지 않는 것들이 있다:

- Ask mode (원격 세션은 파일 편집을 자동 수락)
- Act mode (원격 환경이 이미 샌드박스)
- "Continue in Claude Code on the Web"
  (SSH 세션에서는 불가)
- Agent Teams (CLI/Agent SDK에서만 가능)

이 빈틈을 메우는 도구에는 아직 기회가 있다.

## 참고

- [Claude Code Desktop 공식 문서](https://code.claude.com/docs/en/desktop)
- [SSH 연결 Windows 버그 #25659](https://github.com/anthropics/claude-code/issues/25659)
- [SSH Connector 기능 요청 #15208](https://github.com/anthropics/claude-code/issues/15208)
