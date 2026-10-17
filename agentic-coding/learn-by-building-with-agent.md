# AI 시대의 개발 학습법: 작은 MVP를 Agent와 끝까지 만들며 배우기

## 소개

코딩 Agent를 처음 배우는 사람은 흔히 강의, 책, AI가 만들어 준 교재 가운데
무엇으로 시작할지 고민한다.
2026년 10월 14일 Threads의 한 백엔드 취업 준비생은
Agent, Hook, Skill이 무엇인지 전혀 모른다며
이 세 가지 방법을 놓고 조언을 구했다.
그는 Pro 플랜을 쓰고, 기초부터 큰 그림을 쌓는 공부를 선호하며,
배운 것을 자기 프로젝트에 적용해 포트폴리오도
함께 준비하려 한다고 덧붙였다.[^question]

여기에 대한 답은 셋 중 하나를 고르는 것이 아니라 순서를 바꾸는 것이다.
개념을 먼저 공부하는 대신, 작은 MVP 하나를 문서 → 테스트 → 구현 순서로
Agent와 끝까지 만들면서 필요한 개념을 그때그때 묻는다.
Hook과 Skill이 필요해지는 자리는 정의를 외워서는 보이지 않고
프로젝트를 끝까지 겪어야 드러나기 때문이다.

예제는 `second-hand-marketplace` 저장소다.
“Claude Code 학습을 위한 예제 프로젝트”로 공개된 중고거래 플랫폼이고,
데모 사이트도 함께 공개되어 있다.[^readme]
PRD, SPEC, PLAN, 테스트, 개발 일지, 프로젝트 지침까지 과정이 통째로 남아 있어서
결과물보다 과정을 따라 읽는 교재로 쓸 수 있다.

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

이 프롬프트를 제안한 아샬은
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

README는 여기에 한 줄을 더 둔다.
보안 검토는 프롬프트에 없던 요구로, “이후 추가”라고 표시되어 있다.[^readme]
PLAN도 마감 다듬기(Phase 7)를 “계획 외 추가”로 적는다.[^plan]
프롬프트 하나에서 나온 것은 기능 구현까지의 첫 MVP이고,
배포, 보안, 품질은 같은 방식으로 이어 붙인 후속 요구였다.

## 프롬프트에서 챙길 것

프롬프트는 짧지만 학습에 필요한 장치가 다 들어 있다.
내 프로젝트의 프롬프트를 쓸 때도 아래 다섯 가지를 빠뜨리지 않으면 된다.

- 기술 스택을 이름으로 정한다.
  Agent가 고르게 두면 결과물이 배우려는 스택에서 벗어난다.
- 범위를 “아주 작은 MVP”로 제한한다.
  끝까지 완성할 수 있는 크기여야 전체 흐름을 한 번 볼 수 있다.
- 문서 순서를 정한다.
  PRD로 무엇을 만들지, SPEC으로 어떻게 동작할지, PLAN으로 어떤 순서로 만들지를
  코드보다 먼저 쓰게 한다.
  코드가 나오기 전에 읽을 수 있는 글이 먼저 나오므로
  방향이 틀어졌을 때 가장 싸게 바로잡을 수 있다.
  계획과 결정과 진행을 파일로 남겨 Agent의 기억으로 쓰는
  [File-based Planning Workflow](../ai/file-based-planning-workflow.md)(FBPW)와
  같은 방식이다.
- 검증 방법을 먼저 정한다.
  E2E 테스트를 먼저 쓰게 하면 코드를 다 읽지 않아도
  화면에서 되는지로 결과를 판단할 수 있다.
- 기록을 남기게 한다.
  단계마다 남긴 개발 일지가 나중에 가장 좋은 학습 자료가 된다.

프롬프트에는 처음 보는 사람이 모를 용어가 그대로 있다.
Outside-in TDD, Playwright, PRD·SPEC·PLAN을 미리 설명하지 않고
마지막 줄에서 모르는 것은 중간에 묻겠다고 한다.
그러니 용어가 낯설어도 프롬프트를 고치지 말고 그대로 쓴 뒤,
결과물에서 낯선 말을 만날 때마다 Agent에게 물으면 된다.

### 열린 질문은 눈에 보이는 곳에 적힌다

내가 모든 질문을 미리 떠올릴 필요는 없다.
이 저장소의 PRD에는 열린 질문 세 가지가 있었다.
인증 방식, 가격 단위, 상태 전이 제약이다.
문서 작성 일지는 이를 확인이 필요한 가정으로 표시했고,[^devlog-docs]
PRD는 나중에 각 질문의 결정을 적는다.
인증은 “JWT Bearer 확정 (사용자 이의 없음)”이고,
상태 전이는 제약 없이 자유롭게 두는 것이다.[^prd]
PRD와 SPEC을 읽을 때는 열린 질문과 가정을 먼저 찾아서
이의가 있으면 그 자리에서 말하면 된다.
말하지 않으면 그 가정이 그대로 확정된다.

### 지침 파일에 규칙을 쌓는다

프로젝트의 `AGENTS.md`(`CLAUDE.md`는 이를 가리키는 심볼릭 링크)에는
개발 방식과 Agent가 지킬 규칙이 모여 있다.[^agents][^devlog-polish]
내 프로젝트의 지침 파일에 옮겨 쓸 만한 항목은 이렇다.

- 전용 포트: 흔한 기본 포트와 충돌하지 않게 이 프로젝트만의 포트를 쓴다.
- 서버 종료 규칙: 이름이나 패턴으로 프로세스를 죽이는 명령을 금지하고,
  모르는 프로세스가 포트를 점유하면 죽이지 말고 보고하게 한다.
- 문서 동기화: 동작, API, 화면, 포트, 테스트 구성을 바꾸면
  같은 작업 안에서 SPEC, PRD, PLAN, README를 함께 고치게 한다.
- 끝내기 전 점검: 오래된 포트나 경로가 남지 않았는지 `grep`으로 확인하고
  문서의 상대 링크가 유효한지 본다.
- 기록 위치: 규칙과 선호는 지침 파일에만 쓰고 Memory 기능은 쓰지 않으며,
  기술적 결정은 SPEC의 결정 로그와 devlog에 남긴다.[^agents]

문서 동기화 규칙에는 이유가 있다.
마감 다듬기 단계의 문서 검토는 SPEC의 옛 포트, PLAN의 어긋난 devlog 번호,
남아 있던 Draft 표시, 결정되지 않은 열린 질문,
20으로 적힌 테스트 개수를 찾아냈다.[^devlog-polish]
코드를 바꾸는 속도를 문서가 따라가지 못하면 이런 어긋남이 쌓인다.

## 진행 방식

PLAN 문서는 기능 하나를 끝까지 만드는 사이클을 다음처럼 정했다.[^plan]

```text
1. E2E 테스트 시나리오 작성 (frontend/e2e/*.spec.ts)  → 실행해 Red 확인 (실패 이유 기록)
2. 프론트엔드: 컴포넌트/페이지 테스트(Vitest) Red → 최소 구현 Green
3. 백엔드: API 테스트(MockMvc) Red → 컨트롤러/서비스/리포지토리 최소 구현 Green
4. 도메인/검증 단위 테스트 보강
5. E2E 테스트 재실행 → Green
6. 리팩터링 (모든 테스트 Green 유지)
7. devlog 작성
```

기능 하나가 끝났다고 보는 기준(완료 정의)도 정해 두었다.
세 종류의 테스트가 모두 통과하고,
이전 기능에 회귀가 없고,
devlog에 Red 확인과 설계 결정과 이슈와 다음 단계가 적혀 있어야 한다.[^plan]
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

Phase 0부터 6까지가 시작 프롬프트에서 나온 첫 MVP이고,
7부터는 후속 요구로 붙인 단계다.
아샬은 첫 MVP를 중간에 전혀 개입하지 않고 loop로 쭉 진행한 결과라고 했고,
스크린샷을 찍어 `screenshots` 폴더에 넣는
일만 끝난 뒤 따로 시켰다고 덧붙였다.[^loop]
이 방식으로 돌리면 Agent가 만든 결정은 사람이 보지 않는 사이에 쌓이므로,
끝난 뒤 devlog를 읽으며 따라잡는 시간이 학습의 본체가 된다.

커밋 기록은 작업 순서를 알려 주지 않는다.
Phase 0부터 마감 다듬기까지의 커밋 다섯 개는
2026년 10월 14일 23시 54분 18초로 같은 초에 기록되었고,
배포 인프라, 보안, 품질 강화 커밋 여섯 개는
다음 날 22시 10분 24초와 25초에 기록되었다.[^commits]
무엇을 어떤 순서로 겪었는지는 devlog에서 읽는다.
각 devlog는 마지막 줄에 다음 단계를 적어 두어서,
다음 작업의 출발점이 되는 지시서 구실도 한다.
Phase 1의 devlog는
“Phase 2 — E2E-02/E2E-04(상품 등록·상세) 먼저 작성”으로 끝난다.
이 구조는 FBPW와 겹친다.
PLAN은 작업 계획, SPEC의 결정 로그는 기술적 결정,
devlog는 진행 내역에 해당한다.
컨텍스트가 바뀌어도 Agent가 이 파일들을 다시 읽으면
어디까지 했는지 이어갈 수 있다.

## 개발 일지에서 배울 수 있는 것

devlog는 단계마다 무엇을 먼저 썼고, 처음에 왜 실패했고,
어떤 결정을 내렸는지를 남긴다.
PLAN의 템플릿은 날짜와 대상 기능, 작성한 E2E 테스트와 최초 Red의 원인,
설계 결정과 이유, 겪은 문제와 해결, 테스트 현황, 다음 단계다.[^plan]
강의보다 구체적인 교재가 되는 이유는
이 항목들이 모두 실제로 겪은 일이기 때문이다.

### Red의 이유를 확인한다

인증 단계에서 E2E 테스트는 `/signup` 화면이 없어 입력 필드를 찾지 못하고
4개 모두 시간 초과로 실패했다.[^devlog-auth]
실패한 이유가 “화면이 아직 없어서”라는 의도한 이유였기에
다음 단계로 넘어갈 수 있었다.

때로는 Red가 되어야 할 테스트가 통과한다.
수정과 삭제 단계에서는 버튼이 없음을 검증하는 테스트 2개가
구현 전에도 통과했고, 이를 회귀 방지용 테스트로 따로 분류했다.[^devlog-edit]
판매 상태 변경 단계에서도 미노출을 검증하는 테스트 하나가 같은 이유로
구현 전에 통과했고,[^devlog-status]
보안 단계에서는 보안 테스트 9개 가운데 7개만 Red였다.[^devlog-security]
PLAN의 교훈 항목은 Red의 이유가 의도와 같은지 매번 확인하고,
없음을 검증하는 테스트는 따로 기록하라고 정리한다.[^plan]
내 프로젝트에서도 Green만 보지 말고
Red가 왜 Red였는지를 읽는 습관을 들이면 된다.

### 실패는 앱보다 테스트에서 먼저 난다

회고에 따르면 E2E 테스트의 경쟁 조건 3건은 모두 앱이 아니라 테스트 쪽 문제였다.
가입 뒤 페이지 이동을 기다리지 않거나,
검색 결과가 갱신되기 전에 클릭한 경우다.[^devlog-retro]
해결 원칙은 `toHaveURL`, `toHaveCount`처럼 자동으로 재시도하는 `expect`로
상태에 도달할 때까지 기다리는 것이었다.[^devlog-retro]
회고는 E2E 테스트를 연속 2회 돌려
안정적으로 통과하는지 확인했다고도 적는다.[^devlog-retro]
E2E 테스트가 가끔 실패하면 앱부터 의심하지 말고
무엇을 기다리지 않았는지부터 본다.

### 프론트엔드와 백엔드는 각자의 책임을 테스트한다

수정과 삭제 단계의 설계 결정에서 배울 것은 책임의 분담이다.
프론트엔드는 소유자가 아니면 버튼을 숨기지만
이는 사용성을 위한 것이고,
권한의 근거는 백엔드의 403이라고 일지는 못 박는다.
백엔드 테스트는 타인의 수정을 403으로 거절하면서
데이터가 그대로인지까지 확인하고,
존재하지 않는 리소스와 타인의 리소스를 구분해 응답한다.[^devlog-edit]
또 백엔드 테스트는 가짜 DB 대신 Testcontainers로 실제 PostgreSQL을 띄우고
Flyway 마이그레이션까지 검증한다.[^devlog-retro]
화면에서 버튼이 보이지 않는다고 권한이 지켜지는 것이 아니므로
권한은 서버의 테스트로 확인한다.

### 사고는 규칙이 된다

목록과 검색 단계의 일지에는 초기에 광범위한
`pkill -f`로 프로세스를 종료했다는 사실과,
그 뒤 포트와 작업 디렉터리를 확인해 이 프로젝트의 서버만 끄는
`scripts/stop-servers.sh`와 `CLAUDE.md`
규칙을 추가했다는 기록이 있다.[^devlog-list]
지금의 프로젝트 지침은 `pkill`, `killall`,
프로젝트를 지정하지 않은 Docker 정리를 금지하고,
모르는 프로세스가 포트를 점유하면
죽이지 말고 사용자에게 보고하라고 적는다.[^agents]
금지 목록은 이미 일어난 사고만 막지만,
모르는 프로세스를 죽이지 말고 보고하라는 마지막 원칙은
아직 일어나지 않은 사고까지 덮는다.
Agent가 위험한 일을 하면 그 자리에서 멈추고,
무엇이 위험했는지 한 줄 규칙으로 지침 파일에 남기게 한다.
가능하면 목록이 아니라 원칙으로 넓혀서 쓴다.

### 점검은 스크립트와 빌드 설정으로 남긴다

보안 단계는 찾기, Red, Green, 반복 가능하게 만들기의 네 단계로 진행되었다.
찾는 방법은 코드 리뷰, 이미지와 시크릿 스캔, `npm audit`,
강화한 이미지를 실제로 띄워 `curl`과 로그로 확인하는 것이었고,
마지막 단계에서 이 점검 전체를 `scripts/security-scan.sh` 한 번으로
다시 돌릴 수 있게 했다.[^devlog-security]

품질 단계도 같은 모양이다.
먼저 커버리지를 쟀다(백엔드 라인 97%, 분기 75%,
프론트엔드 문장 94.7%, 분기 87%).
기존 코드 스타일을 Checkstyle 규칙으로 고정하고,
리팩터링과 함께 새로 생긴 작은 단위마다 테스트를 더해 100%에 맞췄다.
그 100%는 지침으로 요청하는 데 그치지 않고
빌드가 임계값으로 강제한다.[^devlog-quality]
지침에 적은 규칙은 Agent가 어길 수 있지만,
빌드가 거부하는 규칙은 어기면 작업이 끝나지 않는다.
한 번 쓰고 말 점검이 아니라 다시 돌릴 점검은 스크립트로 만들고,
꼭 지켜야 하는 기준은 빌드 설정으로 옮긴다.

### 검증은 여러 방법을 겹쳐야 한다

일지에 적힌 발견을 어느 검증이 잡았는지 모아 보면 서로 다르다.

| 발견 | 잡은 검증 |
| --- | --- |
| 리팩터링이 지운 타이밍 보호 | 코드 리뷰[^devlog-quality] |
| CORS 도입 뒤 개발 환경의 상태 변경 요청이 403이 된 문제 | E2E 테스트[^devlog-security] |
| Argon2용으로 추가한 BouncyCastle의 치명적 취약점 | 의존성 스캔[^devlog-security] |
| 로그에 찍히던 쓰지 않는 기본 사용자의 임의 비밀번호 | 로그 읽기[^devlog-security] |
| 가입 뒤 이동을 기다리지 않던 테스트 | 반복 실행[^devlog-retro] |

E2E 테스트는 이 가운데 한 줄을 잡았고
나머지는 코드 리뷰, 스캔, 로그 읽기, 반복 실행이 잡았다.
테스트 우선으로 시작하더라도 코드 리뷰와 스캔과 로그 확인을 함께 두어야 한다.

### 리팩터링이 보안 동작을 지울 수 있다

품질 강화 단계에서 로그인 메서드를 정리하다가 단락 평가 때문에
없는 이메일에도 해시를 검증하는 타이밍 보호가 사라졌다.[^devlog-quality]
코드 리뷰에서 이를 발견했고,
호출 여부를 확인하는 테스트로 다시 빠지지 않게 했다.
일지는 이 경험을 보안 동작은 눈이 아니라 테스트로
지킨다는 말로 정리한다.[^devlog-quality]
이 저장소의 [AI 시대의 코드 리뷰](../_wiki/ai-era-code-review/index.md)도
같은 문제, 곧 무엇이 지켜져야 하는지를 사람이 알아야 한다는 점을 다룬다.
보안 동작을 리팩터링할 때는 그 동작을 확인하는 테스트가 있는지부터 본다.

## 개념은 작업 중에 묻는다

아샬은 이렇게 작업하면서 Agent가 무엇인지,
Claude Code에서 Hook을 쓴다는 게 무엇인지,
Skill을 만든다는 게 무엇인지를 대놓고 묻고,
지금 하는 작업이나 함께 반복하는 일 가운데 Skill로 만들면 좋은 것이 있는지
조금씩 실험해 보라고 권했다.[^ask]
개념을 따로 공부한 뒤 적용하는 대신,
지금 손에 든 프로젝트를 예시로 삼아 개념을 배우는 순서다.

저장소에 그 예가 있다.
품질 점검, 프로덕션 빌드, E2E 테스트, 보안 스캔을
한 번에 돌리는 `/check` Skill은
두 스크립트의 순서와 주의점을 기억해야 하는 번거로움
때문에 만들어졌다.[^devlog-quality][^check]
Skill 안에는 안전 규칙도 들어 있다.
E2E 테스트는 전용 DB만 쓰고, 개발 서버가 떠 있으면
이 프로젝트의 서버만 안전하게 종료하며,
포트를 모르는 프로세스가 점유하면
종료하지 않고 충돌을 보고한다.[^devlog-quality]
지침에 쌓인 사고의 교훈이 Skill 안으로 옮겨 간 것이다.
내 프로젝트에서도 같은 확인 작업을 세 번쯤 반복하고 있다면
Agent에게 이것을 Skill로 만들 수 있는지 물어볼 때다.

책에 대해서는 아샬도 새로 시작할 때 시중의 책을 모두 사서 본다고 했다.
큰 의미가 있는 것은 아니지만 그렇게 하면
이상한 말에 휘둘릴 일이 적다는 이유다.[^ask]
책은 학습의 주 경로가 아니라 Agent의 말을 가늠하는 기준을 세우는 데 쓴다.

## 따라 해 보기

1. 배우고 싶은 스택으로 아주 작은 MVP를 정한다.
   기능은 대여섯 개, 인증과 CRUD 정도면 충분하다.
2. 스택, 폴더 구조, 문서 순서, 테스트 우선, 기록 규칙을 담은 시작 프롬프트를 쓴다.
   처음이라면 이 예제의 프롬프트를 그대로 가져다 쓴다.
3. PRD, SPEC, PLAN이 나오면 읽고, 열린 질문과 가정에 이의가 있으면 말한다.
   모르는 용어는 그 자리에서 묻고, 답은 SPEC의 결정 로그에 남기게 한다.
4. 기능마다 E2E 테스트의 Red 이유를 확인한 뒤 구현을 진행시킨다.
   통과해 버린 Red는 회귀 방지용으로 따로 표시하게 한다.
5. Agent가 위험한 일을 하면 그 자리에서 멈추고 규칙을 지침 파일에 추가하게 한다.
6. 반복해서 시키는 확인 작업이 생기면 Skill이나 스크립트로 만들 수 있는지 묻는다.
7. 첫 MVP가 끝나면 보안, 품질 같은 후속 요구를 같은 사이클로 이어 붙인다.
8. 끝나면 devlog와 커밋 기록을 처음부터 다시 읽는다.
   기능 하나를 Agent 없이 설명할 수 있다면 배운 것이고,
   그렇지 못하다면 그 기능의 devlog를 다시 읽는다.

## 주의할 점

- 끝까지 지켜보지 않으면 배우는 것이 줄어든다.
  아샬이 계속 지켜보며 묻고 혼내라고 한 이유가 여기에 있다.[^prompt]
  결과물만 받아 두면 포트폴리오는 생기지만 판단 근거는 남지 않는다.
  포트폴리오로 내세울 때는 왜 이 구조인지, 무엇을 버렸는지를 답할 수 있어야 하고,
  SPEC의 결정 로그와 devlog가 그 답의 재료다.
- 테스트가 통과했다고 의도대로 동작한다는 뜻은 아니다.
  구현 전에도 통과하는 테스트가 실제로 있었다.[^devlog-edit]
- 커버리지 100%는 코드가 실행되었다는 뜻이지 의도가 검증되었다는 뜻이 아니다.
  타이밍 보호처럼 호출 여부를 따로 확인해야 하는 동작이 있다.[^devlog-quality]
- 개발 서버와 E2E 테스트가 같은 DB를 쓰면 테스트 데이터가 섞인다.
  이 저장소는 E2E 테스트 전용 DB를 따로 띄우고,
  E2E 테스트 전에 개발 서버를 끄라고 적는다.[^readme]
- 새 의존성은 새 취약점을 가져온다.
  보안 강화에 쓴 라이브러리가 스캔에서 걸려 버전을 올렸다.[^devlog-security]
- MVP의 한계는 문서로 남긴다.
  저장소는 목록이 첫 20개만 보이고, 토큰 갱신과 서버 측 폐기,
  이메일 인증과 비밀번호 재설정이 없다는 점을 알려진 한계로 밝힌다.[^readme]

## 기억할 원칙

### 배울 개념보다 끝낼 프로젝트를 먼저 정한다

Agent, Hook, Skill은 정의를 외워서는 쓸 곳이 보이지 않는다.
작은 프로젝트 하나를 끝까지 만들면
어디서 반복이 생기는지, 어디서 사고가 나는지,
무엇을 자동으로 확인해야 하는지가 드러나고,
그 자리가 곧 Hook과 Skill이 필요한 자리다.
아샬도 일단 해 보면 다음이 보인다는 말로 이 예제를 소개했다.[^demo]
이 저장소에서는 `pkill` 사고가 종료 스크립트와 지침이 되었고,
반복되는 확인이 `/check` Skill이 되었다.

### 사람이 할 일은 검증 기준을 정하고 기록을 읽는 것이다

이 예제의 첫 MVP에서 사람이 직접 쓴 것은 시작 프롬프트뿐이었고,
Agent가 나머지를 만드는 동안 품질을 붙든 것은
E2E 테스트 우선, 커버리지 100%, 문서 동기화 같은 규칙이었다.[^agents]
익혀야 할 것은 코드를 직접 치는 속도보다
무엇을 먼저 검증하게 할지 정하고,
Agent가 남긴 기록에서 결정과 실패를 읽어 내는 능력이다.
검증은 코드 리뷰, 테스트, 스캔, 로그처럼 한 가지로 끝나지 않으므로
어떤 방법이 무엇을 잡는지를 아는 것도 그 능력에 들어간다.

---

[^question]: kim_gi_myung(Threads), [안녕하세요 백엔드 취준생인데 Ai 활용 공부 좀 해야할 것 같아요](https://www.threads.com/@kim_gi_myung/post/DedkrfFoOlQ), 2026-10-14

[^prompt]: 아샬(Threads), [클로드 코드로 “Java, Spring Boot(Web MVC), PostgreSQL(Docker Compose로 실행), JUnit으로](https://www.threads.com/@ahastudio/post/DeejKqZGhUC), 2026-10-14

[^ask]: 아샬(Threads), [이렇게 작업하면서 대놓고 “에이전트가 뭐야?”](https://www.threads.com/@ahastudio/post/DeejMYDmkeo), 2026-10-14

[^loop]: 아샬(Threads), [방금 이렇게 돌린 겁니다](https://www.threads.com/@ahastudio/post/Deepl0Jmsw8), 2026-10-14

[^demo]: 아샬(Threads), [소스 코드: github.com/ahastudio/second-hand-marketplace](https://www.threads.com/@ahastudio/post/DehNRaNmrPl), 2026-10-15

[^readme]: 아샬(GitHub), [second-hand-marketplace README.md](https://github.com/ahastudio/second-hand-marketplace/blob/main/README.md), 2026-10-15

[^agents]: 아샬(GitHub), [second-hand-marketplace AGENTS.md](https://github.com/ahastudio/second-hand-marketplace/blob/main/AGENTS.md), 2026-10-15

[^plan]: 아샬(GitHub), [PLAN: Outside-in TDD 개발 계획](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/03-PLAN.md), 2026-10-15

[^commits]: 아샬(GitHub), [second-hand-marketplace 커밋 기록](https://github.com/ahastudio/second-hand-marketplace/commits/main), 2026-10-15

[^devlog-auth]: 아샬(GitHub), [02. Phase 1 — F1 인증 (E2E-01)](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/02-auth.md), 2026-10-14

[^devlog-list]: 아샬(GitHub), [04. Phase 3 — F3 목록·검색 (E2E-03, E2E-04 후속)](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/04-list-search.md), 2026-10-14

[^devlog-edit]: 아샬(GitHub), [05. Phase 4 — F5 수정·삭제 (E2E-05)](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/05-edit-delete.md), 2026-10-14

[^devlog-retro]: 아샬(GitHub), [07. 마무리 및 회고](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/07-retro.md), 2026-10-14

[^devlog-quality]: 아샬(GitHub), [11. 품질 강화와 전체 검증](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/11-quality.md), 2026-10-15

[^check]: 아샬(GitHub), [Full Project Check](https://github.com/ahastudio/second-hand-marketplace/blob/main/_agent/skills/check/SKILL.md), 2026-10-15

[^prd]: 아샬(GitHub), [PRD](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/01-PRD.md), 2026-10-15

[^devlog-docs]: 아샬(GitHub), [00. 문서 작성](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/00-docs.md), 2026-10-14

[^devlog-setup]: 아샬(GitHub), [01. Phase 0 기반 셋업](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/01-setup.md), 2026-10-14

[^devlog-status]: 아샬(GitHub), [06. Phase 5 — F6 판매 상태 변경 (E2E-06)](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/06-status.md), 2026-10-14

[^devlog-polish]: 아샬(GitHub), [08. Phase 7 — 마감 다듬기](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/08-polish.md), 2026-10-14

[^devlog-infra]: 아샬(GitHub), [09. 서버 배포 인프라](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/09-infra.md), 2026-10-15

[^devlog-security]: 아샬(GitHub), [10. 보안 검토와 강화](https://github.com/ahastudio/second-hand-marketplace/blob/main/docs/devlog/10-security.md), 2026-10-15
