# AgentsView

> Local-first session search, analytics, insights, and token use statistics
> for coding agents, supporting Claude Code, Codex, and more than 20 other
> agents.

<https://www.agentsview.io/>

<https://github.com/kenn-io/agentsview>

## 소개

AgentsView는 Claude Code, Cursor, Gemini CLI, Codex, Devin CLI,
OpenHands, Windsurf 등 40개 이상의 AI 코딩 에이전트에서 생성된
세션을 자동으로 수집·분석하는 도구다.
로컬 웹 UI와 CLI를 통해 대화 검색, 토큰/비용 통계, 활동 분석,
파일 변경 추적을 제공한다.
외부 서비스 계정이나 클라우드 업로드 없이 로컬에서 데이터를
통합해 볼 수 있다는 점이 핵심이다.

## 아키텍처

로컬 우선(local-first) 설계에 선택적 클라우드 백엔드를 얹은
구조다.

- Go(83.8%) 백엔드가 수집·동기화·API를 담당
- Svelte 5 프론트엔드가 웹 UI 제공
- SQLite를 기본 저장소로 사용하며 FTS5로 전체 텍스트 검색 인덱싱
- 팀 대시보드를 위한 PostgreSQL, 분석 워크플로를 위한 DuckDB
  미러를 선택적 백엔드로 지원
- 파일 워처가 `~/.claude/projects/`, `~/.cursor/projects/` 같은
  에이전트별 디렉터리를 자동 탐지해 주기적으로 동기화

## 주요 기능

**세션 관리**는 전체 메시지 콘텐츠에 대한 전체 텍스트 검색과 선택적
임베딩 기반 시맨틱 검색을 지원한다.
활성 세션은 서버 전송 이벤트(SSE)로 실시간 업데이트되며, HTML 또는
GitHub Gist로 내보낼 수 있다.

**비용 추적**은 세션·모델별 토큰 사용량과 비용을 계산한다.
LiteLLM 요금표를 활용한 자동 가격 산정(오프라인 폴백 포함)과
프롬프트 캐싱을 고려한 비용 계산(캐시 생성/읽기 토큰 구분)을
지원한다.
활동 히트맵과 속도(velocity) 지표도 제공한다.

**팀 기능**으로 PostgreSQL 동기화를 통한 공유 대시보드, DuckDB
Quack 프로토콜을 통한 원격 읽기 접근, 다중 타깃 푸시 설정, `--watch`
플래그를 통한 자동 백그라운드 동기화가 있다.

## CLI

```bash
agentsview serve              # localhost:8080에서 웹 UI 시작
agentsview usage daily        # 일별 비용 요약 출력
agentsview session list       # 발견된 세션 목록
agentsview stats              # 기간 범위 분석 (git/GitHub 지표 옵션 포함)
agentsview pg push            # PostgreSQL로 동기화
agentsview duckdb push        # DuckDB로 미러링
agentsview daemon start       # 백그라운드 SQLite 서비스 시작
```

설치는 셸 스크립트, Homebrew(`brew install --cask agentsview`),
Docker, GitHub Releases의 바이너리 직접 다운로드를 지원한다.

## 프라이버시와 텔레메트리

세션 데이터는 기본적으로 기기 내에만 저장되며, 서비스는 루프백
(127.0.0.1)에만 바인딩된다.
설치 ID, 버전, OS 정보 등 최소한의 익명 텔레메트리를 PostHog로
전송하며, `AGENTSVIEW_TELEMETRY_ENABLED=0`으로 비활성화할 수 있다.

## 라이선스 및 상태

MIT 라이선스로 배포되며, 2026년 7월 기준 4.3k 스타, 70개 릴리스,
857개 커밋, 55개 오픈 이슈로 활발히 개발되고 있다.
최신 버전은 v0.37.5(2026년 7월 10일)이며 Go 1.26+를 요구한다.

## 분석

### 에이전트 파편화가 만든 관측성 공백

여러 AI 코딩 에이전트를 동시에 쓰는 개발자가 늘면서, 각 도구가
독립적으로 세션 로그를 남기는 방식은 비용과 사용 패턴을 통합적으로
파악하기 어렵게 만든다.
AgentsView는 이 파편화 문제를 로컬에만 존재하는 여러 로그
포맷(Claude Code, Cursor, Codex 등)을 하나의 SQLite 인덱스로
통합함으로써 해결한다.
40개 이상의 에이전트를 지원한다는 점은 이 파편화가 이미 상당히
진행되어 있다는 방증이기도 하다.

### 로컬 우선 설계와 팀 협업의 절충

기본값이 로컬 전용이라는 점은 코딩 세션에 포함될 수 있는 민감한
코드나 프롬프트 내용을 외부로 유출하지 않으려는 설계 선택으로
읽힌다.
동시에 PostgreSQL/DuckDB를 선택적으로 붙일 수 있게 해, 개인
사용에서 팀 단위 비용 관제로 자연스럽게 확장할 수 있는 경로를
열어둔다.
이는 "로컬 우선이지만 필요하면 공유 가능"이라는, 최근 개발자
도구들에서 반복되는 패턴을 따른다.

## 인사이트

AgentsView 같은 도구가 등장한다는 것 자체가, AI 코딩 에이전트
사용이 이제 "어떤 도구를 쓸 것인가"를 넘어 "여러 도구를 쓰는 비용을
어떻게 관리할 것인가"라는 다음 단계 문제로 넘어갔음을 보여준다.
토큰 비용, 세션 히스토리, 파일 변경 추적을 한곳에서 보는 것은
단순 편의 기능이 아니라, 여러 에이전트를 병행 운용할 때 발생하는
오케스트레이션 부담을 가시화하는 관측 인프라에 가깝다.
프롬프트 캐싱을 고려한 비용 계산까지 갖췄다는 점은, 실무에서 이미
비용 관리가 단순 토큰 수 세기를 넘어선 정교함을 요구하고 있다는
신호로 볼 수 있다.
</content>
