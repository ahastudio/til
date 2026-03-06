# Paperclip

<https://paperclip.ing/>

<https://github.com/paperclipai/paperclip>

오픈소스 AI 에이전트 오케스트레이션 플랫폼. 슬로건은 **"zero-human
company를 위한 오케스트레이션"**이다. 에이전트 한 명이 아니라, 에이전트로
구성된 조직 전체를 운영하는 것이 목표다.

"OpenClaw이 직원이라면, Paperclip은 회사다."

## 핵심 개념

단일 에이전트를 잘 다루는 프레임워크가 아니다. 에이전트 팀에 조직도,
예산, 목표, 거버넌스를 부여해 실제 회사처럼 운영하는 인프라다. 에이전트
런타임에 무관하다 — 하트비트 신호를 보낼 수 있으면 무엇이든 "채용"된다.
Claude Code 세션, OpenClaw 봇, Python 스크립트, 쉘 커맨드, HTTP 웹훅 모두
연결 가능하다.

채팅 창 기반의 일회성 대화가 아니라, 에이전트가 리부트를 넘어서 세션을
유지하며 작업을 계속 수행하는 **지속 운영(persistent operation)** 모델이다.

## 기술 스택

- **백엔드**: Node.js 20+, TypeScript (코드베이스의 97.5%)
- **프런트엔드**: React
- **데이터베이스**: PostgreSQL (로컬은 임베디드, 프로덕션은 외부 연결)
- **배포**: 자체 호스팅(self-hosted), Paperclip 계정 불필요
- **라이선스**: MIT

## 주요 기능

### 오케스트레이션

- 조직도 기반 에이전트 계층 구조 관리
- 스케줄 하트비트 및 이벤트 기반 실행
- 태스크 체크아웃으로 중복 작업 방지(원자적 연산)
- 세션 재시작 후에도 에이전트 상태 유지

### 목표 정렬(Goal Alignment)

태스크에 목표 계보(goal ancestry) 전체를 포함시켜, 에이전트가 제목만
보는 게 아니라 "왜 이 일을 하는지"까지 일관되게 파악하게 한다.

### 비용 관리

- 에이전트별 월 예산 한도 설정
- 80% 도달 시 경고, 100% 도달 시 에이전트 자동 일시정지
- 에이전트·태스크·프로젝트·목표 단위 비용 추적

### 거버넌스

- 승인 게이트(approval gate) 강제
- 설정 변경 버전 관리 및 롤백
- 불변 감사 로그(immutable audit log)

### 멀티 컴퍼니 격리

단일 배포로 여러 회사를 운영할 수 있다. 모든 엔티티가 company-scoped로
분리되어 각각 독립적인 데이터와 감사 추적을 갖는다.

## 시작하기

```bash
npx paperclipai onboard --yes
```

또는:

```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip && pnpm install && pnpm dev
```

`http://localhost:3100`에서 바로 실행된다.

## Paperclip이 아닌 것

공식 문서가 명시적으로 선을 긋는다: **챗봇, 에이전트 프레임워크, 워크플로우
빌더, 프롬프트 매니저, 단일 에이전트 도구, 코드 리뷰 시스템**이 아니다.

## 분석과 인사이트

→ [Paperclip 분석과 인사이트](./paperclip-insights.md)
