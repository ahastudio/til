# CodeBurn

<https://github.com/getagentseal/codeburn>

## 소개

CodeBurn은 AI 코딩 도구의 토큰 사용량과 비용을 추적하는 로컬 기반 TUI(Terminal User Interface) 대시보드다.
Claude Code, Codex, Cursor, Gemini CLI 등 18개 AI 코딩 도구를 지원하며,
API 키나 프록시 없이 디스크의 세션 데이터를 직접 읽어 비용을 산정한다.
모든 처리가 로컬에서 이루어지므로 개인정보가 외부로 전송되지 않는다.

AgentSeal이 개발했으며, MIT 라이선스로 배포된다.

## 주요 기능

| 기능                | 설명                                                               |
| ------------------- | ------------------------------------------------------------------ |
| 비용 추적           | 입력/출력/캐시 토큰 기반 가격 책정 (LiteLLM 활용)                 |
| 작업 분류           | 코딩, 디버깅, 기능개발 등 13가지 카테고리로 자동 분류             |
| 원샷 레이트         | 재시도 없이 성공한 편집 작업 비율 추적                            |
| 최적화 분석         | 낭비 패턴 감지 및 수정 제안 (`codeburn optimize`)                  |
| 모델 비교           | 모델 간 성능 지표 비교 분석 (`codeburn compare`)                   |
| Yield 분석          | Git 커밋과 연관지어 생산성 평가 (`codeburn yield`)                 |
| 다중 통화           | 162개 통화 지원                                                    |

## 지원 도구

```text
Claude Code, Claude Desktop, Codex, Cursor, cursor-agent,
Gemini CLI, GitHub Copilot, Kiro, OpenCode, OpenClaw,
Pi, OMP, Droid, Roo Code, KiloCode, Qwen, Goose, Antigravity, Crush
```

## CLI

```bash
# 설치
npm install -g codeburn
# 또는
brew tap getagentseal/codeburn && brew install codeburn
# 또는 직접 실행
npx codeburn
```

```bash
codeburn              # 대시보드 (기본 7일)
codeburn today        # 오늘 사용량
codeburn week         # 주간 사용량
codeburn month        # 월간 사용량
codeburn optimize     # 낭비 패턴 분석
codeburn compare      # 모델 성능 비교
codeburn yield        # Git 기반 생산성 평가
codeburn status       # 한 줄 요약
codeburn export       # CSV/JSON 내보내기
codeburn report --format json  # JSON 형식 출력
```

필터 옵션: `--provider`, `--project`, `--from`, `--to`

## 데이터 소스

각 도구의 세션 데이터 경로를 직접 읽는다:

| 도구          | 데이터 경로                          |
| ------------- | ------------------------------------ |
| Claude Code   | `~/.claude/projects/`                |
| Cursor        | `~/.config/Cursor/` (SQLite DB)      |
| Codex         | `~/.codex/sessions/`                 |
| Gemini CLI    | `~/.gemini/tmp/`                     |

## 분석

CodeBurn은 AI 코딩 도구 비용 가시성 문제를 직접 겨냥한다.
Claude Code 같은 도구를 팀 단위로 사용하면 월 수십만 원의 비용이 발생할 수 있는데,
어떤 작업에 얼마나 소비되는지 파악하기 어렵다는 불만이 많았다.
`CLAUDE.md` 같은 설정 파일이 비대해지거나 파일을 반복적으로 읽는 패턴이 토큰 낭비의 주원인으로 꼽힌다.

[GeekNews 댓글](https://news.hada.io/topic?id=29343)에서 `openusage`라는 유사 도구도 언급됐다.
두 도구 모두 같은 문제를 해결하려 하지만, CodeBurn은 18개 도구를 한번에 지원한다는 점에서 범위가 넓다.

Git 커밋과 토큰 사용량을 연결하는 `yield` 기능이 흥미롭다.
얼마를 소비했는지뿐 아니라, 그 소비가 실제 코드 산출로 이어졌는지 추적하는 시도다.
AI 코딩 도구의 ROI를 측정하는 실질적인 방법을 제공한다는 점에서 차별화된다.

## 비평

비용 추적이라는 기능 자체는 확실한 수요가 있다.
그러나 각 도구의 세션 파일 형식이 업데이트될 때마다 파서를 유지보수해야 하는 부담이 있다.
18개 도구를 지원한다는 것은 그만큼 18개의 변경 위험이 있다는 의미다.

원샷 레이트와 같은 지표는 AI 코딩 도구 품질을 평가하는 새로운 언어를 만들고 있다.
단순한 토큰 수가 아니라 “한 번의 시도로 목표를 달성했는가”를 측정하는 방식은
AI 도구의 실질적 효율성을 더 정확히 반영한다.

## 인사이트

### AI 도구 사용의 관찰 가능성 문제

소프트웨어 개발 영역에서 관찰 가능성(observability)은 오랫동안 중요한 주제였다.
로그, 메트릭, 트레이스가 서버 운영의 필수 인프라가 된 것처럼,
AI 코딩 도구의 사용 패턴을 추적하는 것도 곧 개발팀의 필수 인프라가 될 것이다.
CodeBurn은 이 공백을 채우려는 초기 시도다.
앞으로는 개발 도구들이 자체적으로 이런 분석 기능을 내장하거나,
기업용 AI 코딩 플랫폼이 대시보드를 제공하는 방향으로 발전할 가능성이 높다.

### 토큰 소비 패턴이 개발 습관을 드러낸다

코드 커버리지가 테스트 습관을 드러내듯, 토큰 소비 패턴은 AI 활용 습관을 드러낸다.
`CLAUDE.md`가 지나치게 커서 매 세션마다 수천 토큰을 소비한다면, 그 파일을 정리해야 한다는 신호다.
같은 파일을 반복적으로 읽는다면 컨텍스트 관리 방식을 개선해야 한다는 신호다.
CodeBurn이 제공하는 `optimize` 기능은 단순한 비용 절감 도구가 아니라,
AI와 협업하는 방식을 되돌아보게 하는 피드백 루프다.

### 생산성 측정의 새로운 단위

소프트웨어 개발 생산성을 측정하는 방법은 오랫동안 논쟁의 대상이었다.
코드 줄 수(LoC)는 무의미하고, 커밋 수도 불완전하다.
CodeBurn의 `yield` 기능은 “투입 토큰 대비 산출 커밋”이라는 새로운 단위를 제안한다.
이 지표가 완벽하진 않지만, AI 코딩 도구 시대에 맞는 생산성 측정 방식을 찾으려는 진지한 시도다.
팀이 어떤 도구에서 더 높은 yield를 얻는지 비교할 수 있다면,
도구 선택과 워크플로우 최적화에 실질적인 근거가 생긴다.
