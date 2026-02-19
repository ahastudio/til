# GitHub Copilot CLI

터미널에서 AI 에이전트와 대화하며 코드를 읽고, 쓰고, 실행할 수 있는
CLI 도구다. 에디터 없이 터미널만으로 개발 작업을 수행할 수 있다.

<https://github.com/features/copilot/cli>

<https://github.com/github/copilot-cli>

## 설치

```bash
# macOS / Linux (Homebrew)
brew install copilot-cli

# Windows (WinGet)
winget install GitHub.Copilot

# Cross-platform (npm)
npm install -g @github/copilot

# macOS / Linux (설치 스크립트)
curl -fsSL https://gh.io/copilot-install | bash
```

<https://formulae.brew.sh/cask/copilot-cli>

## 인증

```bash
# GitHub 계정으로 로그인
/login
```

GitHub 인증 정보를 사용하며, 조직의 Copilot 거버넌스 정책이
자동으로 적용된다. Personal Access Token도 사용할 수 있다.

## 주요 특징

- **터미널 네이티브**: 에디터 전환 없이 터미널에서 직접 작업
- **GitHub 통합**: 저장소, 이슈, PR에 자연어로 접근
- **승인 기반 실행**: 파일 변경과 명령 실행 전 사용자 확인 필요
- **세션 유지**: 대화 컨텍스트가 세션 간에 유지됨
- **MCP 확장**: Model Context Protocol 서버로 커스텀 도구 연결

## 슬래시 커맨드

- `/login` - GitHub 인증
- `/model` - AI 모델 전환
- `/experimental` - 실험 기능 활성화
- `/feedback` - 피드백 설문 제출
- `/lsp` - 설정된 Language Server 확인

## 기본 모델

Claude Sonnet 4.5가 기본 모델이다. `/model` 커맨드로 다른 모델로
전환할 수 있다.

## Autopilot 모드

실험 기능으로, 에이전트가 작업 완료까지 자율적으로 계속 진행한다.
`Shift+Tab`으로 토글한다.

## LSP 지원

Language Server Protocol을 지원하여 코드 인텔리전스를 강화한다.
설정 파일 위치:

- 사용자 수준: `~/.copilot/lsp-config.json`
- 저장소 수준: `.github/lsp.json`

## 지원 플랫폼

- macOS
- Linux
- Windows (PowerShell v6+ 필요)

## 요금

별도 API 키나 추가 과금이 없다. 기존 Copilot 구독(Pro, Pro+,
Business, Enterprise)에 포함되며, 프롬프트 제출마다 월간 프리미엄
요청 쿼터에서 차감된다.
