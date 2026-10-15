# 리뷰를 어디로 옮기는가

[← AI 시대의 코드 리뷰](index.md)

“리뷰를 없앤다”는 주장을 자세히 읽으면
대부분 리뷰를 다른 곳으로 옮긴다는 뜻이다.
[스스로 검증하는 코드베이스면 코드 리뷰가 끝난다는 낙관](../../agentic-coding/bend-code-review-solved.md)도
구현 리뷰는 필요 없어지지만 명세 리뷰는 남는다고 해석한다.
노트들이 제안하는 이동 방향은 크게 다섯 가지다.

## 리뷰 시점을 다섯으로 나누기

[코드가 리뷰를 앞질렀다](../../code-review/code-outruns-review.md)는
리뷰를 한 시점의 행위가 아니라 다섯 시점에 흩어진 활동으로 본다.
생성 전에는 스펙을 검토하고, 생성 중에는 자동 검증을 돌리고,
PR 시점에는 AI를 센서로 쓰고,
머지 전에는 틀렸을 때의 비용에 따라 리뷰 강도를 정하고,
배포 후에는 플래그와 롤백으로 대응한다.
기준은 작성자가 사람인지 AI인지가 아니라 실패 비용이다.
같은 노트의 결론은 사라지는 것은 리뷰가
아니라 모든 변경을 같은 방식으로 읽던 관행이라는 것이다.
아래의 이동 방향은 각각 이 다섯 시점 가운데 하나에 무게를 싣는다.

## 앞으로: 명세와 인수 기준을 리뷰한다

가장 많이 나오는 처방은 diff 대신 사양과 인수 기준을 리뷰하라는
것이다([코드 리뷰는 어떻게 죽는가](../../agentic-coding/reviews-dead.md)).
리뷰어의 질문이 “이 코드가 맞나”에서 “이 기준이 맞나”로 바뀐다.
[AI 시대, 코드 리뷰는 코드가 아니라 판단을 검증하는 것이다](../../code-review/ai-era.md)는 스펙 문서와 테스트를 판단의 외부 기록으로 삼자고 하고,
[Why Software Factories Fail](../../ai/software-factories-fail-coding-agents.md)은 리서치와 플랜 단계의 검토가 코드 리뷰보다 레버리지가 훨씬 크다고 본다.
Anthropic 플레이북은 승인된 `intent.md`와 `spec.md`를 PR로 올리는 흐름을
그린다([AI 네이티브 SDLC](../../agentic-coding/ai-native-sdlc.md)).
리뷰 코멘트가 팀 내 기대 불일치에서도 생긴다는 관찰에 따라
조사→질문→계획→구현→리뷰 루프를 도입한 팀은
2개월 뒤 1,000라인당 가중 리뷰 코멘트가
72.3%
줄었다([개인 프롬프트 기술을 버리고 팀이 돌아가는 AI 주도 개발 루프를 만든 이야기](../../agentic-coding/interview-dev-loop.md)).
카카오페이는 Spec-kit 흐름으로 맥락을 잃은 AI 코드의 검토 시간을
줄이려 했다([SDD(Spec-kit) 에이전틱 코딩
실전기](../../agentic-coding/kakaopay-spec-kit-practice.md)).

이 처방은 문제를 옮길 뿐이라는 반론이 있다.
HN의 loveparade는 명세 도구가 모호함과 코드 리뷰를 옮길 뿐이라고 했고,
AI가 쓴 명세를 검토하는 일은 다른 종류의 피로를
낳는다([OpenSpec](../../agentic-coding/openspec.md)).
기준 자체가 틀리면 기준 통과로 확인하는 방식은 그 오류를 잡지 못하고 확증 편향을
제도화한다([PLAN 프레임워크](../../agentic-coding/plan-framework.md)).
테스트는 Claude가 해석한 요구사항만 검증할 뿐 사용자가 실제로 원한 것은
검증하지
않는다([잠자는 동안 돌아가는 에이전트를 만들고 있다](../../agentic-coding/agents-that-run-while-i-sleep.md)).

## 기계로: 결정론적 게이트

사람의 기억과 리뷰에 기대는 스타일 가이드는 가장 약한 층이고 PR 속도를
따라가지
못한다([에이전트를 믿으려면 주방부터 고쳐라](../../agentic-coding/michelin-kitchen-for-agents.md)).
그래서 결정론적으로 확인할 수 있는 것은 기계에 넘기자는 처방이 나온다.
gofumpt는 “포맷 논쟁은 없다, 도구가 결정한다”로 리뷰에서
스타일 논의를 없앴다([gofumpt](../../go/gofumpt.md)).
Knip은 문제가 하나라도 있으면 종료 코드 1로 끝나 그대로
CI 게이트가 된다([Knip](../../javascript/knip.md)).
Swizec Teller는 AI 리뷰 대신 커스텀 린터를 쓰자고 하고,
가장 느린 린터도 전체 검사에 27초였다고
한다([AI 코드 리뷰에 토큰을 태우지 말고, 결정론적 규칙은 커스텀 린터로 옮겨라](../../agentic-coding/stop-burning-tokens-on-code-review.md)).
Anthropic 플레이북은 스킬이 권고형 통제일 뿐이니 반드시 지켜야 할 정책은 훅과
PR 단계 재검사로 뒷받침하라고
한다([AI 네이티브 SDLC](../../agentic-coding/ai-native-sdlc.md)).
[AI가 읽을 수 있는 코드베이스](../../agentic-coding/ai-readable-codebase.md)는
가능한 검증을 모두 컴파일 타임으로 끌어올리라고 하고,
Bun의 Rust 이식은 스타일 가이드, 리뷰,
테스트가 모두 “사람이 실수하지 않기를 바라는” 장치라며 컴파일러 수준의 보장으로
대체하자고 한다([Rewriting Bun in Rust](../../rust/rewriting-bun-in-rust.md)).
가장 멀리 간 주장은 형식 검증이 되는 코드베이스면 “코드 리뷰는 해결되었다”는
것이다([스스로 검증하는 코드베이스면 코드 리뷰가 끝난다는 낙관](../../agentic-coding/bend-code-review-solved.md)).

결정론적 장치에도 사각이 있다.
Copilot이 안전한 셸 처리 패턴을 되돌린 PR은
GitHub Advanced Security도 표시하지 못해 Jira 토큰 유출로 이어졌다.
스캐너는 위험한 패턴의 존재는 잡지만 보호 장치의 제거는
잡지
못한다([AI가 되돌린 안전 패턴 하나가 Snowflake Jira를 열었다](../../security/snowflake-jira-copilot-autofix.md)).
axios 공급망 공격은 악성 코드가 의존성 추가 형태라 코드 리뷰에서 눈에
띄지
않았다([axios npm 공급망 공격 분석](../../security/axios-npm-compromise.md)).

## 실행으로: 테스트와 런타임 검증

PR에 E2E 테스트나 데모 녹화 같은 Acceptance 증명을
붙이면 동작 확인은 자동화가 맡고,
리뷰어는 책임 범위, 트랜잭션 경계,
의존성 방향 같은 설계 판단에
집중할 수
있다([AI가 읽을 수 있는 코드베이스](../../agentic-coding/ai-readable-codebase.md)).
네이버파이낸셜은 에이전트가 “문제없이 완료”라고 보고한 Next.js 업그레이드에서
뒤로 가기가 깨진 일을 겪고 Playwright E2E 하네스를
만들었다([AI가 쓴 코드 누가 검증하나](../../test/ai-agent-playwright-e2e-harness.md)).
TDD가 새 병목을 푸는 실천법이라는 주장도
있다([AI 시대에 TDD가 더 강력해진 이유](../../agentic-coding/tdd-in-ai-era.md)).

테스트도 만능은 아니다.
Dan Luu의 실험에서 TDD 지시를 받은 에이전트는 일반적인 경우를 다루는 테스트를
더 많이 쓰고도 어려운 경우를 놓쳐 평가 테스트에
더 자주
실패했다([테스트 기법 이름만 알려주면 에이전트는 그 기법을 흉내만 낸다](../../agentic-coding/agent-test-technique-eval.md)).
Slack 실험에서는 생성된 결정론 테스트가 긴 시나리오에서 약 48% 실패해
가장
불안정했다([Agentic Testing](../../test/slack-agentic-testing-e2e-stack.md)).
테스트를 깨진 동작에 맞게 고쳐 쓰는 “테스트 변조”를 감지하는 일이
리뷰의 핵심 지표가 된다는 관점도
있다([에이전트 시대의 코드 리뷰](../../code-review/agentic-code-review.md)).

## 단위로: 작은 PR과 읽을 수 있는 diff

한 사람의 컨텍스트 창을 넘는 PR은 읽히지 않으니 PR을 주의의 기본 단위로 보자는
주장이 있다([LLM 시대의 엔지니어링](../../llm/engineering-in-llm-age.md)).
넓게 만든 뒤 독립적으로 리뷰할 수 있는 최소 PR 집합으로 쪼개는 일은
이제 프롬프트 하나로
된다([넓게 만들고 좁게 출하하라](../../agentic-coding/build-wide-ship-narrow.md)).
GitHub는 에이전트가 만든 큰 diff를 스택 단위로 나누는 통합을
공식
지원한다([GitHub Stacked PRs](../../github/github-stacked-pull-requests.md)).
리뷰 화면 자체도 바뀌고 있다.
에이전트가 구현·테스트·스냅샷을 한꺼번에 만든 PR이 리뷰 화면을 무너뜨린다는
진단([On Rendering Diffs](../../code-review/on-rendering-diffs.md)),
에이전트가 변경을 다이어그램과 결정 기록으로 설명하게 하는
캔버스([Whiteboard](../../code-review/whiteboard.md)),
리뷰 루프 전용 IDE([px0](../../code-review/px0.md)),
의미론적 diff를
내세운 리뷰 레이어([Cursor · Origin](../../cursor/cursor-origin.md))가 그 예다.
다만 좋은 분해는 리뷰를 쉽게 하지만 병합까지 빠르게 하지는 않는다.
[넓게 만들고 좁게 출하하라](../../agentic-coding/build-wide-ship-narrow.md)의
저자도 글을 쓴 시점에 PR 다섯 개가 모두 열린 채였다.

## 뒤로: 표본 검사와 프로덕션 관측

Lauren Tan은 한 달에 PR 2,500개를 내며 에이전트가 자기 PR을 직접 머지하게 하고,
리뷰는 품질 관리자처럼 표본만
본다([모든 접시를 맛보지 않는다](../../agentic-coding/agents-merge-their-own-code.md)).
[코드 리뷰는 어떻게 죽는가](../../agentic-coding/reviews-dead.md)의 구호는
“빠르게 배포하고, 모든 것을 관찰하고, 더 빠르게 되돌려라”다.
[Production Is Where the Rigor Goes](../../devops/production-is-where-the-rigor-goes.md)는 배포 전 검증의 한계를 인정하고 엄밀함을 프로덕션 옵저버빌리티로 옮기자고 한다.
위험도로 분류해 고위험 변경만 깊이 보자는 제안도 같은
방향이다([에이전트 시대의 코드 리뷰](../../code-review/agentic-code-review.md)).

이 방향은 가장 강한 반론을 받는다.
환자 데이터 앱이 리뷰와 QA 없이 배포되어 데이터가 노출된 사례는 배포 전 검증을
의무화하자는 요구로
이어진다([AI 바이브 코딩 호러 스토리](../../security/vibe-coding-horror-story.md)).
에이전트가 만들고, 리뷰가 병목이 되고, 리뷰도 자동화하고,
사람 리뷰를 없애는 것이 소프트웨어 팩토리의 실패 경로라는 지적도
있다([Why Software Factories Fail](../../ai/software-factories-fail-coding-agents.md)).
저위험 분류의 정확도는 검증할 수 없다는 역설도
남는다([에이전트 시대의 코드 리뷰](../../code-review/agentic-code-review.md)).
Tan 스스로도 자신의 방식이 사실상 “불 꺼진 공장”이라고
인정한다([모든 접시를 맛보지 않는다](../../agentic-coding/agents-merge-their-own-code.md)).

관련: 결정론적 강제와 텍스트 지침의 경계는
[하네스 엔지니어링의 결정론적 강제와 텍스트 지침의 경계](../harness-engineering/deterministic-vs-prompted.md)에,
스펙과 TDD가 에이전트에 대해 하는 일과 못 하는 일은
[에이전트형 코딩의 실패/함정 패턴의 스펙/TDD가 하는 일과 못 하는 일](../agentic-coding-failure-patterns/spec-and-tdd-as-guardrails.md)에,
자율과 개입의 경계선은
[어디까지 자율을 주고 어디서 개입해야 하는가](../agentic-coding-failure-patterns/where-to-draw-the-line.md)에 있다.

## 출처

- [agentic-coding/bend-code-review-solved.md](../../agentic-coding/bend-code-review-solved.md)
- [code-review/code-outruns-review.md](../../code-review/code-outruns-review.md)
- [agentic-coding/reviews-dead.md](../../agentic-coding/reviews-dead.md)
- [code-review/ai-era.md](../../code-review/ai-era.md)
- [ai/software-factories-fail-coding-agents.md](../../ai/software-factories-fail-coding-agents.md)
- [agentic-coding/ai-native-sdlc.md](../../agentic-coding/ai-native-sdlc.md)
- [agentic-coding/interview-dev-loop.md](../../agentic-coding/interview-dev-loop.md)
- [agentic-coding/kakaopay-spec-kit-practice.md](../../agentic-coding/kakaopay-spec-kit-practice.md)
- [agentic-coding/openspec.md](../../agentic-coding/openspec.md)
- [agentic-coding/plan-framework.md](../../agentic-coding/plan-framework.md)
- [agentic-coding/agents-that-run-while-i-sleep.md](../../agentic-coding/agents-that-run-while-i-sleep.md)
- [agentic-coding/michelin-kitchen-for-agents.md](../../agentic-coding/michelin-kitchen-for-agents.md)
- [go/gofumpt.md](../../go/gofumpt.md)
- [javascript/knip.md](../../javascript/knip.md)
- [agentic-coding/stop-burning-tokens-on-code-review.md](../../agentic-coding/stop-burning-tokens-on-code-review.md)
- [agentic-coding/ai-readable-codebase.md](../../agentic-coding/ai-readable-codebase.md)
- [rust/rewriting-bun-in-rust.md](../../rust/rewriting-bun-in-rust.md)
- [security/snowflake-jira-copilot-autofix.md](../../security/snowflake-jira-copilot-autofix.md)
- [security/axios-npm-compromise.md](../../security/axios-npm-compromise.md)
- [test/ai-agent-playwright-e2e-harness.md](../../test/ai-agent-playwright-e2e-harness.md)
- [agentic-coding/tdd-in-ai-era.md](../../agentic-coding/tdd-in-ai-era.md)
- [agentic-coding/agent-test-technique-eval.md](../../agentic-coding/agent-test-technique-eval.md)
- [test/slack-agentic-testing-e2e-stack.md](../../test/slack-agentic-testing-e2e-stack.md)
- [code-review/agentic-code-review.md](../../code-review/agentic-code-review.md)
- [llm/engineering-in-llm-age.md](../../llm/engineering-in-llm-age.md)
- [agentic-coding/build-wide-ship-narrow.md](../../agentic-coding/build-wide-ship-narrow.md)
- [github/github-stacked-pull-requests.md](../../github/github-stacked-pull-requests.md)
- [code-review/on-rendering-diffs.md](../../code-review/on-rendering-diffs.md)
- [code-review/whiteboard.md](../../code-review/whiteboard.md)
- [code-review/px0.md](../../code-review/px0.md)
- [cursor/cursor-origin.md](../../cursor/cursor-origin.md)
- [agentic-coding/agents-merge-their-own-code.md](../../agentic-coding/agents-merge-their-own-code.md)
- [devops/production-is-where-the-rigor-goes.md](../../devops/production-is-where-the-rigor-goes.md)
- [security/vibe-coding-horror-story.md](../../security/vibe-coding-horror-story.md)
