# File-based Planning Workflow

파일 시스템을 AI 에이전트의 영구 메모리로 활용하는 워크플로우입니다.

Manus AI가 $2B 인수를 이끌어낸 컨텍스트 엔지니어링 방식에서
영감을 받았습니다.
컨텍스트 윈도우에 의존하는 대신 파일 시스템을 영구 저장소로
활용합니다.

## 해결하는 문제

AI 에이전트는 다음과 같은 한계가 있습니다:

- 컨텍스트가 리셋되면 작업 내용을 잊어버림
- 긴 작업 중에는 원래 목표를 잃어버림
- 실패한 시도가 추적되지 않아 같은 실수를 반복함

## 핵심 아이디어

하나의 파일에 계획, 발견사항, 진행상황을 모두 기록합니다.
AI가 작업 전후로 이 파일을 읽고 업데이트합니다.

## 사용 예시

```markdown
# Project: 사용자 인증 기능 추가

## Goal
세션 관리를 포함한 안전한 사용자 인증 구현

## Plan

### Phase 1: 요구사항 및 탐색 ✅
- [x] 코드베이스의 기존 인증 패턴 조사
- [x] 세션 저장소 솔루션 파악
- [x] Rate limiting 요구사항 문서화

### Phase 2: 구현 🔄
- [x] 로그인 엔드포인트 구현
- [ ] 세션 관리 추가
- [ ] 로그아웃 엔드포인트 추가
- [ ] 테스트 작성

### Phase 3: 테스트
- [ ] 단위 테스트
- [ ] 통합 테스트
- [ ] 보안 테스트

## Findings

### 기술 스택
- 인증 미들웨어: src/middleware/auth.ts
- 세션 저장소: Redis (redis://localhost:6379)
- 토큰 형식: JWT (24시간 만료)
- Rate limiting: IP당 분당 100회

### 주요 결정사항
| 결정 | 근거 |
|------|------|
| 세션 대신 JWT 사용 | Stateless, API 확장성 향상 |
| Redis 저장소 선택 | 빠른 속도, 만료 기능 지원 |
| bcrypt 해싱 사용 | 업계 표준, 느린 속도 = 보안 강화 |

### 참고 자료
- 인증 문서: https://example.com/auth-guide
- Redis 클라이언트: /lib/redis-client.js

## Progress

### 2025-01-21 - Session 2
**현재 상태**: 세션 관리 구현 중

**완료**:
- JWT 생성을 포함한 로그인 엔드포인트 (src/auth/login.ts)
- bcrypt를 사용한 비밀번호 검증
- 잘못된 인증 정보에 대한 에러 처리

**다음 작업**:
- Redis에 세션 저장
- 로그아웃 엔드포인트 구현

**발생한 에러**:
- bcrypt 설치 에러 (node-gyp 실패)
  → 해결: node-gyp rebuild 실행
  → 해결에 15분 소요

### 2025-01-20 - Session 1
**완료**: 초기 코드 탐색 및 계획 수립
**다음**: 구현 시작
```

## 비교: Spec-Driven Development

**Spec-Driven Development**: "무엇을" 만들지 사전에 명확히 정의
(Top-down, 계획 중심)

**File-based Planning**: "어떻게" 진행되는지 과정을 추적
(Bottom-up, 탐색 중심)

함께 사용하면: Spec으로 방향을 정하고, Planning으로 과정을 추적

[Spec-Driven Development](./spec-driven-development.md)

## 구현 사례

[Planning with Files](../claude/planning-with-files.md) -
Claude Code 플러그인
