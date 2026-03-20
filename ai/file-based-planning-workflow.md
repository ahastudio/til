# File-based Planning Workflow

파일 시스템을 AI 에이전트의 영구 메모리로 활용하는 워크플로우입니다.

## 해결하는 문제

AI 에이전트는 다음과 같은 한계가 있습니다:

- 컨텍스트가 리셋되면 작업 내용을 잊어버림
- 긴 작업 중에는 원래 목표를 잃어버림
- 실패한 시도가 추적되지 않아 같은 실수를 반복함

## 해법: 3-File Pattern

세 개의 전용 파일(`tasks.md`, `findings.md`, `progress.md`)로 분리하여 계획,
발견사항, 진행상황을 각각 관리합니다. AI가 작업 전후로 이 파일들을 읽고
업데이트하여 영구 메모리로 활용합니다.

### 파일 구조

| 파일            | 역할                    | 업데이트 시점        |
| --------------- | ----------------------- | -------------------- |
| **tasks.md**    | 작업 계획 및 추적       | 새로운 단계 시작 시  |
| **findings.md** | 기술적 발견사항 및 결정 | 탐색 및 조사 후 즉시 |
| **progress.md** | 세션별 작업 내역        | 각 작업 세션마다     |

### tasks.md

```markdown
# Project: [프로젝트명]

## Goal

명확한 최종 목표 (북극성 역할)

## Current Phase

🔄 Phase 2: Planning & Structure

## Phases

### Phase 1: Requirements & Discovery ✅

- [x] 사용자 요구사항 확인
- [x] 기존 코드베이스 탐색
- [x] 제약사항 문서화

### Phase 2: Planning & Structure 🔄

- [x] 아키텍처 설계
- [ ] 디렉토리 구조 생성
- [ ] 인터페이스 정의

### Phase 3: Implementation ⏸️

- [ ] 핵심 기능 구현
- [ ] 단위 테스트 작성
- [ ] 통합

### Phase 4: Testing & Verification ⏸️

- [ ] 요구사항 검증
- [ ] 테스트 실행 및 결과 로깅

### Phase 5: Delivery ⏸️

- [ ] 최종 리뷰
- [ ] 사용자 전달

## Key Questions

1. 어떤 DB를 사용하나?
2. 인증 방식은?

## Decisions Made

| Decision         | Rationale                     |
| ---------------- | ----------------------------- |
| TypeScript 사용  | 타입 안전성, 팀 표준          |
| PostgreSQL 14    | 인증 데이터의 정합성과 신뢰성 |
| JWT + Redis 세션 | 확장성 + 빠른 만료 처리       |

## Errors Encountered

| Error                  | Attempt | Resolution                         |
| ---------------------- | ------- | ---------------------------------- |
| npm install 실패       | 1       | package-lock.json 삭제 후 재설치   |
| TypeScript 컴파일 에러 | 3       | tsconfig strictNullChecks 비활성화 |

## Notes

- 진행할 때마다 Phase 상태를 업데이트하세요: 대기 중 → 진행 중 → 완료
- 중요한 결정을 내리기 전에 이 계획을 다시 읽어보세요. (attention manipulation)
- 모든 오류를 기록하세요. 삽질을 반복하는 걸 막을 수 있습니다.
```

### findings.md

````markdown
# Findings & Decisions

> **기술적 발견, 중요한 결정이 있을 때마다 이 파일을 즉시 업데이트하세요.**

## Requirements

- [ ] 사용자 등록 (이메일 + 비밀번호)
- [ ] 로그인 및 세션 관리
- [ ] 비밀번호 재설정 기능
- [ ] 관리자 대시보드

## Research Findings

### 코드베이스 구조

- 백엔드: Express.js + TypeScript
- 프론트엔드: React 18 + Vite
- DB: PostgreSQL (모델: Sequelize)
- 인증: 현재 없음 → 새로 구축

### 기존 패턴

- API 라우트: `src/routes/` 디렉토리
- 미들웨어: `src/middleware/`
- 에러 처리: 중앙화된 에러 핸들러 (`src/utils/errors.ts`)

## Technical Decisions

| Decision          | Rationale                  |
| ----------------- | -------------------------- |
| Passport.js 사용  | 검증된 인증 라이브러리     |
| JWT 토큰 (24시간) | Stateless, 확장성          |
| Redis 세션 저장소 | 빠른 조회, 자동 만료       |
| Argon2            | 최신 보안 표준, OWASP 권장 |

## Issues Encountered

### 1. Argon2 설치 실패

**문제**: node-gyp 컴파일 에러

**해결**:

```bash
npm install -g node-gyp
node-gyp rebuild
```bash

**결과**: 성공

### 2. Redis 연결 타임아웃

**문제**: localhost:6379 연결 안 됨

**원인**: Redis 서버 미실행

**해결**: `docker-compose up redis`

**결과**: 해결됨

## Resources

### 문서

- [Passport.js JWT Strategy](https://www.passportjs.org/packages/passport-jwt/)
- [Argon2 보안 가이드](https://github.com/ranisalt/node-argon2)

### 코드 참조

- 에러 핸들러: `src/utils/errors.ts:45`
- DB 설정: `src/config/database.ts:12`
- 환경 변수: `.env.example:8-15`

### API 엔드포인트

- POST `/api/auth/register`
- POST `/api/auth/login`
- POST `/api/auth/logout`
- GET `/api/auth/me`

## Learnings

### 데이터베이스 스키마 (2026-01-21 10:30)

ERD 다이어그램 확인:

- `users` 테이블: `id`, `email`, `password_hash`, `created_at`
- `sessions` 테이블: 없음 (Redis 사용)
- Foreign keys: `posts.user_id` → `users.id`

### UI 목업 (2026-01-21 11:00)

Figma에서 확인한 로그인 화면:

- 이메일/비밀번호 입력
- "Remember me" 체크박스
- Google OAuth 버튼 (Phase 2에서 구현)
````

### progress.md

날짜순(오름차순)으로 기록합니다. 가장 최근 세션이 맨 아래에 위치합니다.

```markdown
# Progress Log

> **각 단계를 완료하거나 문제가 발생하면 업데이트하세요.**

## Session 2026-01-20

### Phase 1: Requirements & Discovery ✅

**작업 내역**:

1. 사용자 요구사항 문서화
2. 코드베이스 탐색 완료
3. 기술 스택 조사 및 결정

**생성/수정 파일**:

- `docs/auth-requirements.md` (새로 생성)

## Session 2026-01-21

### Phase 2: Planning & Structure 🔄

**작업 내역**:

1. 프로젝트 구조 설계 완료
2. 의존성 패키지 설치
   - passport
   - passport-jwt
   - argon2
   - jsonwebtoken
   - redis
3. 환경 변수 설정 (.env.example 업데이트)

**생성/수정 파일**:

- `src/auth/passport-config.ts` (새로 생성)
- `src/middleware/auth.ts` (새로 생성)
- `src/types/user.ts` (새로 생성)
- `.env.example` (수정)

### Phase 3: Implementation ⏸️

아직 시작 안 함

## Test Results

| Test             | Input                | Expected         | Actual       | Status |
| ---------------- | -------------------- | ---------------- | ------------ | ------ |
| 사용자 등록      | valid email/password | 201 Created      | 201 Created  | ✅     |
| 중복 이메일 등록 | existing email       | 409 Conflict     | 409 Conflict | ✅     |
| 잘못된 로그인    | wrong password       | 401 Unauthorized | 500 Error    | ❌     |
| JWT 검증         | valid token          | user object      | user object  | ✅     |

## Error Log

| Timestamp        | Error                  | Attempt | Resolution                  |
| ---------------- | ---------------------- | ------- | --------------------------- |
| 2026-01-21 09:15 | Argon2 설치 실패       | 1       | node-gyp 재빌드             |
| 2026-01-21 10:30 | Redis 연결 실패        | 1       | Docker 컨테이너 시작        |
| 2026-01-21 11:45 | 비밀번호 검증 500 에러 | 2       | argon2.verify await 추가    |
| 2026-01-21 14:20 | JWT 만료 시간 에러     | 1       | expiresIn 형식 수정 ('24h') |

## 5-Question Reboot Check

작업 재개 시 이 질문들로 컨텍스트 복구:

| Question               | Answer                                            |
| ---------------------- | ------------------------------------------------- |
| 1. 현재 어느 단계인가? | Phase 2: Planning & Structure (90% 완료)          |
| 2. 다음에 할 일은?     | Remaining phases                                  |
| 3. 목표는?             | 세션 관리를 포함한 안전한 사용자 인증 시스템 구축 |
| 4. 지금까지 배운 것?   | See findings.md                                   |
| 5. 완료한 작업은?      | See above                                         |
```

## 비교: Spec-Driven Development

**Spec-Driven Development**: “무엇을” 만들지 사전에 명확히 정의 (Top-down, 계획
중심)

**File-based Planning**: “어떻게” 진행되는지 과정을 추적 (Bottom-up, 탐색 중심)

함께 사용하면: Spec으로 방향을 정하고, Planning으로 과정을 추적

[Spec-Driven Development](./spec-driven-development.md)

## 구현 사례

[Planning with Files](../claude/planning-with-files.md) - Claude Code 플러그인
