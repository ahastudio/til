# AI 시대의 개발 학습법: 작은 MVP를 에이전트와 끝까지 만들며 배우기

## 소개

코딩 에이전트를 처음 배우는 사람은 흔히 강의, 책, AI가 만들어 준 교재 가운데
무엇으로 시작할지 고민한다.
2026년 10월 14일 백엔드 취업 준비생인 Threads 사용자 kim_gi_myung도
에이전트, 훅, 스킬이 무엇인지 전혀 모른다며
이 세 가지 방법을 놓고 조언을 구했다.
그는 Pro 플랜을 쓰고, 기초부터 큰 그림을 쌓는 공부를 선호하며,
배운 것을 자기 프로젝트에 적용해 포트폴리오도
함께 준비하려 한다고 덧붙였다.[^question]

이 문서는 그 질문에 대한 하나의 답을 실제 결과물로 정리한다.
개념을 먼저 공부하는 대신, 작은 MVP 하나를 문서 → 테스트 → 구현 순서로
에이전트와 끝까지 만들면서 필요한 개념을 그때그때 묻는 방식이다.
예제로 쓰는 `second-hand-marketplace` 저장소는
“Claude Code 학습을 위한 예제 프로젝트”로 공개된 중고거래 플랫폼이고,
데모 사이트도 함께 공개되어 있다.[^readme]

## 시작 프롬프트

저장소는 아래 프롬프트 하나로 시작했고,
PRD, SPEC, PLAN, E2E 테스트, 구현, 개발 일지까지
이후의 모든 결과물이 이 요청에서 나왔다고 밝힌다.[^readme]

```text
Java, Spring Boot(Web MVC), PostgreSQL(Docker Compose로 실행), JUnit으로
아주 작은 MVP 수준의 중고거래 플랫폼 백엔드(REST API 서버)를 만들려고 해.
TypeScript, React, Tailwind, Vite, Vitest, Playwright로 프론트엔드도 함께 만들고 싶어.
backend, frontend라는 두 개의 폴더를 만들어서 각각 위치하게 해줘.
PRD 먼저 작성하고, 스펙 문서 만들고, Outside-in TDD로 개발할 수 있는 계획 문서 작성해줘.
반드시 각 기능에 대한 E2E 테스트를 Playwright 사용하는 코드를 먼저 작성하면서 시작해야 해.
진행하면서 각 단계마다 중요한 부분을 문서로 남기면서 진행하자.
잘 모르는 게 있으면 내가 중간 중간 물어볼게
```

이 프롬프트를 제안한 Threads 사용자 ahastudio는
여기서 시작해 계속 지켜보며 묻고, 혼내고,
주고받는 것이 중요하다고 했다.[^prompt]

프롬프트의 각 요구는 저장소에서 다음 결과물로 이어졌다.[^readme]

| 프롬프트의 요구                            | 결과물                                         |
| ------------------------------------------ | ---------------------------------------------- |
| `backend`, `frontend` 두 폴더              | `backend/`, `frontend/`                        |
| PRD → 스펙 → 계획 문서 순서                | `docs/01-PRD.md` → `02-SPEC.md` → `03-PLAN.md` |
| 기능마다 Playwright E2E 테스트를 먼저 작성 | `frontend/e2e/`, 기능별 Red 확인 후 구현       |
| 단계마다 중요한 부분을 문서로 기록         | `docs/devlog/`                                 |
| 모르는 것은 중간에 질문                    | SPEC의 결정 로그                               |

## 프롬프트 하나가 정하는 것

프롬프트는 짧지만 학습에 필요한 장치를 모두 담고 있다.

- 기술 스택을 이름으로 정해 둔다.
  에이전트가 고르게 두지 않으므로 결과물이 배우려는 스택에서 벗어나지 않는다.
- 범위를 “아주 작은 MVP”로 제한한다.
  끝까지 완성할 수 있는 크기여야 전체 흐름을 한 번 볼 수 있다.
- 문서 순서를 정한다.
  PRD로 무엇을 만들지, SPEC으로 어떻게 동작할지, PLAN으로 어떤 순서로 만들지를
  코드보다 먼저 쓰게 한다.
- 검증 방법을 먼저 정한다.
  E2E 테스트를 먼저 쓰게 하면 에이전트의 결과를 사람이 눈으로 다 읽지 않아도
  테스트가 통과했는지로 판단할 수 있다.
- 기록을 남기게 한다.
  단계마다 남긴 개발 일지가 나중에 학습 자료가 된다.

## 실제로 진행된 순서

PLAN 문서는 기능 하나를 끝까지 만드는 사이클을 다음처럼 정했다.[^plan]

```text
1. E2E 테스트 시나리오 작성 (frontend/e2e/*.spec.ts)  → 실행해 Red 확인 (실패 이유 기록)
2. 프론트: 컴포넌트/페이지 테스트(Vitest) Red → 최소 구현 Green
3. 백엔드: API 테스트(MockMvc) Red → 컨트롤러/서비스/리포지토리 최소 구현 Green
4. 도메인/검증 단위 테스트 보강
5. E2E 테스트 재실행 → Green
6. 리팩터링 (모든 테스트 Green 유지)
7. devlog 작성
```

이 사이클을 기능마다 반복한 결과는 PLAN의 진행 결과 표에 남아 있다.[^plan]

| 단계     | 내용               | 누적 테스트 (E2E 테스트 / Vitest / JUnit) |
| -------- | ------------------ | ----------------------------------------- |
| Phase 0  | 기반 셋업과 스모크 | 1 / 1 / 1                                 |
| Phase 1  | 인증               | 5 / 5 / 7                                 |
| Phase 2  | 상품 등록과 상세   | 9 / 9 / 12                                |
| Phase 3  | 목록과 검색        | 13 / 12 / 15                              |
| Phase 4  | 수정과 삭제        | 17 / 17 / 22                              |
| Phase 5  | 판매 상태 변경     | 20 / 20 / 25                              |
| Phase 6  | 마무리와 회고      | 20 / 20 / 25                              |
| Phase 7  | 마감 다듬기        | 26 / 23 / 25                              |
| Phase 8  | 서버 배포 인프라   | 26 / 26 / 28                              |
| Phase 9  | 보안 검토와 강화   | 26 / 26 / 37                              |
| Phase 10 | 품질 강화          | 26 / 40 / 72, 커버리지 100%               |

커밋 기록을 보면 Phase 0부터 회고와 마감 다듬기까지의 커밋은
2026년 10월 14일 23시 54분에 기록되었고,
배포 인프라, 보안, 품질 강화 커밋은 다음 날 22시 10분에 기록되었다.[^commits]
ahastudio는 첫 MVP를 중간에 전혀 개입하지 않고 loop로 쭉 진행한 결과라고 했고,
스크린샷을 찍어 `screenshots` 폴더에 넣는
일만 끝난 뒤 따로 시켰다고 덧붙였다.[^loop]

## 개발 일지에서 배울 수 있는 것

개발 일지는 단계마다 무엇을 먼저 썼고, 처음에 왜 실패했고,
어떤 결정을 내렸는지를 남긴다.
학습자에게는 이 기록이 강의보다 구체적인 교재가 된다.

### Red의 이유를 확인한다

인증 단계에서 E2E 테스트는 `/signup` 화면이 없어 입력 필드를 찾지 못하고
4개 모두 시간 초과로 실패했다.[^devlog-auth]
수정과 삭제 단계에서는 버튼이 없음을 검증하는 테스트 2개가
구현 전에도 통과했고, 이를 회귀 방지용 테스트로 따로 분류했다.[^devlog-edit]
PLAN의 교훈 항목도 Red의 이유가 의도와 같은지 매번 확인하고,
없음을 검증하는 테스트는 구현 전에도 통과하므로 따로 기록하라고 정리한다.[^plan]

### 실패는 앱보다 테스트에서 먼저 났다

회고에 따르면 E2E 테스트의 경쟁 조건 3건은 모두 앱이 아니라 테스트 쪽 문제였다.
가입 뒤 페이지 이동을 기다리지 않거나,
검색 결과가 갱신되기 전에 클릭한 경우다.[^devlog-retro]
해결 원칙은 `toHaveURL`, `toHaveCount`처럼 자동으로 재시도하는 `expect`로
상태에 도달할 때까지 기다리는 것이었다.[^devlog-retro]

### 에이전트의 사고도 기록에 남는다

목록과 검색 단계의 일지에는 초기에 광범위한
`pkill -f`로 프로세스를 종료했다는 사실과,
그 뒤 포트와 작업 디렉터리를 확인해 이 프로젝트의 서버만 끄는
`scripts/stop-servers.sh`와 `CLAUDE.md`
규칙을 추가했다는 기록이 있다.[^devlog-list]
지금의 프로젝트 지침은 `pkill`, `killall`,
프로젝트를 지정하지 않은 Docker 정리를 금지하고,
모르는 프로세스가 포트를 점유하면
죽이지 말고 사용자에게 보고하라고 적는다.[^agents]
에이전트에게 맡길 때 무엇을 금지해야 하는지가 실제 사고에서 나온 셈이다.

### 리팩터링이 보안 동작을 지울 수 있다

품질 강화 단계에서 로그인 메서드를 정리하다가 단락 평가 때문에
없는 이메일에도 해시를 검증하는 타이밍 보호가 사라졌다.[^devlog-quality]
코드 리뷰에서 이를 발견했고,
호출 여부를 확인하는 테스트로 다시 빠지지 않게 했다.
일지는 이 경험을 보안 동작은 눈이 아니라 테스트로
지킨다는 말로 정리한다.[^devlog-quality]

## 개념은 작업 중에 묻는다

ahastudio는 이렇게 작업하면서 에이전트가 무엇인지,
Claude Code에서 훅을 쓴다는 게 무엇인지,
스킬을 만든다는 게 무엇인지를 대놓고 묻고,
지금 하는 작업이나 함께 반복하는 일 가운데 스킬로 만들면 좋은 것이 있는지
조금씩 실험해 보라고 권했다.[^ask]
개념을 따로 공부한 뒤 적용하는 대신,
지금 손에 든 프로젝트를 예시로 삼아 개념을 배우는 순서다.

저장소에도 이런 결과가 남아 있다.
품질 점검, 프로덕션 빌드, E2E 테스트, 보안 스캔을 한 번에 돌리는 `/check` 스킬은
두 스크립트의 순서와 주의점을 기억해야 하는 번거로움
때문에 만들어졌다.[^devlog-quality][^check]
반복되는 확인 작업이 스킬이 된 구체적인 예다.

책에 대해서는 ahastudio도 새로 시작할 때 시중의 책을 모두 사서 본다고 했다.
큰 의미가 있는 것은 아니지만 그렇게 하면
이상한 말에 휘둘릴 일이 적다는 이유다.[^ask]
책은 학습의 주 경로가 아니라 판단 기준을 세우는 보조 수단으로 쓰인다.

## 따라 해 보기

1. 배우고 싶은 스택으로 아주 작은 MVP를 정한다.
   기능은 대여섯 개, 인증과 CRUD 정도면 충분하다.
2. 스택, 폴더 구조, 문서 순서, 테스트 우선, 기록 규칙을 담은 시작 프롬프트를 쓴다.
3. PRD, SPEC, PLAN이 나오면 읽고, 모르는 결정은 묻는다.
   답은 SPEC의 결정 로그에 남기게 한다.
4. 기능마다 E2E 테스트의 Red 이유를 확인한 뒤 구현을 진행시킨다.
5. 에이전트가 위험한 일을 하면 그 자리에서 멈추고 규칙을 `CLAUDE.md`에 추가하게 한다.
6. 반복해서 시키는 확인 작업이 생기면 스킬로 만들 수 있는지 묻는다.
7. 끝나면 개발 일지와 커밋 기록을 처음부터 다시 읽는다.

## 함정

- 끝까지 지켜보지 않으면 배우는 것이 줄어든다.
  ahastudio가 계속 지켜보며 묻고 혼내라고 한 이유가 여기에 있다.[^prompt]
  결과물만 받아 두면 포트폴리오는 생기지만 판단 근거는 남지 않는다.
- 테스트가 통과했다고 의도대로 동작한다는 뜻은 아니다.
  구현 전에도 통과하는 테스트가 실제로 있었다.[^devlog-edit]
- 개발 서버와 E2E 테스트가 같은 DB를 쓰면 테스트 데이터가 섞인다.
  이 저장소는 E2E 테스트 전용 DB를 따로 띄우고, E2E 테스트 전에 개발 서버를 끄라고 적는다.[^readme]
- MVP의 한계는 문서로 남겨야 한다.
  저장소는 목록이 첫 20개만 보이고, 토큰 갱신과 서버 측 폐기,
  이메일 인증과 비밀번호 재설정이 없다는 점을 알려진 한계로 밝힌다.[^readme]

## 기억할 원칙

### 배울 개념보다 끝낼 프로젝트를 먼저 정한다

에이전트, 훅, 스킬은 정의를 외워서는 쓸 곳이 보이지 않는다.
작은 프로젝트 하나를 끝까지 만들면
어디서 반복이 생기는지, 어디서 사고가 나는지,
무엇을 자동으로 확인해야 하는지가 드러나고,
그 자리가 곧 훅과 스킬이 필요한 자리다.
ahastudio도 일단 해 보면 다음이 보인다는 말로 이 예제를 소개했다.[^demo]

### 사람이 할 일은 검증 기준을 정하고 기록을 읽는 것이다

이 예제의 첫 MVP에서 사람이 직접 쓴 것은 시작 프롬프트뿐이었고,
에이전트가 나머지를 만드는 동안 품질을 붙든 것은
E2E 테스트 우선, 커버리지 100%, 문서 동기화 같은 규칙이었다.[^agents]
학습자가 익혀야 할 것은 코드를 직접 치는 속도보다
무엇을 먼저 검증하게 할지 정하고,
에이전트가 남긴 기록에서 결정과 실패를 읽어 내는 능력이다.

---

[^question]: kim_gi_myung(Threads), [안녕하세요 백엔드 취준생인데 Ai 활용 공부 좀 해야할 것 같아요](https://www.threads.com/@kim_gi_myung/post/DedkrfFoOlQ), 2026-10-14

[^prompt]: ahastudio(Threads), [클로드 코드로 “Java, Spring Boot(Web MVC), PostgreSQL(Docker Compose로 실행), JUnit으로](https://www.threads.com/@ahastudio/post/DeejKqZGhUC), 2026-10-14

[^ask]: ahastudio(Threads), [이렇게 작업하면서 대놓고 “에이전트가 뭐야?”](https://www.threads.com/@ahastudio/post/DeejMYDmkeo), 2026-10-14

[^loop]: ahastudio(Threads), [방금 이렇게 돌린 겁니다](https://www.threads.com/@ahastudio/post/Deepl0Jmsw8), 2026-10-14

[^demo]: ahastudio(Threads), [소스 코드: github.com/ahastudio/second-hand-marketplace](https://www.threads.com/@ahastudio/post/DehNRaNmrPl), 2026-10-15

[^readme]: ahastudio(GitHub), [second-hand-marketplace README.md](https://github.com/ahastudio/second-hand-marketplace/blob/main/README.md), 2026-10-15

[^agents]: ahastudio(GitHub), [second-hand-marketplace AGENTS.md](https://github.com/ahastudio/second-hand-marketplace/blob/main/AGENTS.md), 2026-10-15

[^plan]: ahastudio(GitHub), [PLAN: Outside-in TDD 개발 계획](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/03-PLAN.md), 2026-10-15

[^commits]: ahastudio(GitHub), [second-hand-marketplace 커밋 기록](https://github.com/ahastudio/second-hand-marketplace/commits/main), 2026-10-15

[^devlog-auth]: ahastudio(GitHub), [02. Phase 1 — F1 인증 (E2E-01)](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/02-auth.md), 2026-10-14

[^devlog-list]: ahastudio(GitHub), [04. Phase 3 — F3 목록·검색 (E2E-03, E2E-04 후속)](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/04-list-search.md), 2026-10-14

[^devlog-edit]: ahastudio(GitHub), [05. Phase 4 — F5 수정·삭제 (E2E-05)](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/05-edit-delete.md), 2026-10-14

[^devlog-retro]: ahastudio(GitHub), [07. 마무리 및 회고](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/07-retro.md), 2026-10-14

[^devlog-quality]: ahastudio(GitHub), [11. 품질 강화와 전체 검증](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/11-quality.md), 2026-10-15

[^check]: ahastudio(GitHub), [Full Project Check](https://github.com/ahastudio/second-hand-marketplace/blob/main/_agent/skills/check/SKILL.md), 2026-10-15
