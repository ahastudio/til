# 책임은 누구에게 있는가

[← AI 시대의 코드 리뷰](index.md)

AI가 쓰는 비용을 0에 가깝게 만들었지만 읽는 비용은 그대로다.
그 차이를 누가 떠안느냐가 AI 시대 리뷰의 윤리 문제이고,
노트들은 대체로 작성자가 먼저 읽고 책임져야 한다는 데 모인다.

## 쓰는 비용과 읽는 비용의 비대칭

Shopify CEO의 “슬롭 수류탄” 발언을 다룬 노트는 직원이 읽지도 않은
AI 코드를 보내고 동료가 “이거 이상한데”를 찾아내야 하는 상황을 짚는다.
쓰는 비용은 0에 가까워졌지만 읽는 비용은 그대로라는
것이다([Shopify CEO의 “슬롭 수류탄”](../../ai/shopify-slop-grenades.md)).
코드만의 문제가 아니다.
AI 답변 복붙은 생산 시간을 20초로 줄였지만 읽는 시간은 그대로이고,
검증 없이 넘기는 것은 “판단의 외주화”이자 책임 회피라는 지적이
있다([AI 답변 복붙이 우리 팀을 피곤하게 만드는 이유](../../management/ai-slop-workplace-tax.md)).
생성은 빨라졌지만 검증은 빨라지지 않았고 검증 비용이
큰 업무일수록 더 위험하다는 관찰([워크슬롭](../../ai/workslop.md))과,
코드를 쓰는 일은 늘 읽는 일보다 쉬웠다는
지적([AI가 코드를 쓸수록 도메인 주도 설계가 더 중요해진다](../../domain-driven-design/ddd-and-ai-coding.md))도 같은 구조를 본다.

## 작성자가 먼저 읽어야 한다

[인간의 주의를 요청할 때는 인간의 노력을 증명하라](../../agentic-coding/human-attention-and-human-effort.md)는 동료에게 리뷰를 요청하기 전에 직접 검토하고 AI 생성물임을 표시하라고 한다.
AI PR을 쏟아낸 동료의 PR을 리뷰어들이 무의식적으로 피하게 된 사례도 함께 든다.
[AI 출력을 그대로 옮기는 고기 프록시가 되지 마라](../../agentic-coding/meat-proxy.md)는 리뷰 피드백을 Claude에 붙여 넣고 결과를 읽지 않으면 실제로 구현한 사람은 리뷰어라고 본다.
자기 말로 쓴 답이 “읽고 이해하고 검증했다는 증명서”라는 것이다.
에이전트가 쓴 PR 설명도 직접 검토해야 하며 읽지 않은 텍스트를 내는 것은 리뷰어에
대한 무례라는
지적([Agentic Engineering Patterns](../../agentic-coding/agentic-engineering-patterns.md))과,
커밋 설명은 산출물이 아니라 검증 절차라서 에이전트가 대신 쓰면 정보는 남지만
검증이 사라진다는
주장([에이전트 시대에도 커밋 설명은 직접 써야 한다](../../git/commit-description-thinking.md))도 같은 원칙이다.
[Verification Debt](../../agentic-coding/verification-debt.md)의 체크리스트
마지막 질문은 “내 이름을 걸 수 있는가”이고,
답이 “아마도”이면 리뷰를 끝내지 않은 것이다.

이 원칙에 대한 비판도 있다.
[인간의 주의를 요청할 때는 인간의 노력을 증명하라](../../agentic-coding/human-attention-and-human-effort.md)를 다룬 노트는 이 제안이 책임을 개인에게만 지운다고 보고,
슬롭 수류탄 노트는 정책은 그대로 두고 직원만 훈계하는 것은 책임을
옮긴 것일 뿐이라고
본다([Shopify CEO의 “슬롭 수류탄”](../../ai/shopify-slop-grenades.md)).

## 승인했다면 누구의 책임인가

AI 리뷰 도구는 대부분 승인을 사람에게 남긴다.
Claude Code Review는 PR을
승인하지 않는다([Claude Code Review](../../claude/claude-code-review.md)).
리뷰 대화 분석 논문도 병합 전 최종 응답은 사람이 해야 한다고
권한다([코드 리뷰에서 AI는 지적하고 사람은 이해시킨다](../../code-review/human-ai-synergy-code-review.md)).
Amazon이 AI 보조 코드 변경에 시니어 승인을 의무화한 사례가 여러 노트에
인용된다([AI가 주니어 개발자를 무용하게 만들고 있다](../../ai/ai-making-junior-devs-useless.md), [AI 리뷰를 신뢰할 수 있을까요?](../../ai/can-you-trust-ai-reviews.md)).

하지만 승인의 의미는 흐려지고 있다.
[루프 속의 인간은 지쳐 있다](../../ai/human-in-loop-tired.md)는
리뷰어가 승인했다면 책임은 누구에게 있는지 묻는다.
Snowflake Jira 사고에서는 Copilot이 공동 작성자로서 최종 리비전을
승인했다([AI가 되돌린 안전 패턴 하나가 Snowflake Jira를 열었다](../../security/snowflake-jira-copilot-autofix.md)).
서브에이전트를 늘릴수록 책임 소재가 불명확해졌다는 보고도
있다([AI 리뷰를 신뢰할 수 있을까요?](../../ai/can-you-trust-ai-reviews.md)).
에이전트 다섯 개의 변경을 병합할 때 책임을 어떻게 지는지 설명이 없다는 비판도
같은 문제를
가리킨다([Claude Code 생산성의 비결은 AI가 아니라 배관이다](../../agentic-coding/its-the-infrastructure-not-the-ai.md)).
“좋은 결과물은 곧 역량 있는 사람”이라는 등식이 깨지면서 리뷰를
포함한 검증 메커니즘이 구조적으로 무력화된다는 진단도
있다([AI 시대의 생산적으로 보이기](../../management/appearing-productive-ai.md)).
AI 사용률은 76%에서 84%로 올랐지만 신뢰는 40%에서 29%로 떨어졌다는 수치와 함께,
틀리는 위치를 알면 통제할 수 있지만 매일 바뀌면 믿을 수 없다는 관점은
신뢰의 조건을 보여
준다([개발자가 도구에 애착을 갖는 이유는 도구가 신뢰를 담고 있기 때문이다](../../developer-tools/tools-encode-trust.md)).

## 오픈소스의 정책 실험

오픈소스 프로젝트들은 이 책임 문제에 서로 다른 답을 냈다.

| 프로젝트  | 정책                                                        | 근거                                                                                                                                       |
| --------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| OpenJDK   | LLM을 이해·디버그·리뷰에는 쓰되 생성물 제출 금지            | 리뷰 부담, 안전, 보안, 지식재산([Oracle는 AI가 쓴 코드를 사랑하지만 OpenJDK에는 받지 않는다](../../java/openjdk-ai-ban.md))                |
| SourceHut | 사적인 리뷰 용도는 허용, 생성 코드 제출은 이용약관으로 금지 | LLM은 리뷰와 보안 분석에 유용하다고 인정([SourceHut이 LLM 사용을 이용약관으로 금지하다](../../github/sourcehut-llm-ban.md))                |
| Debian    | 허용하되 기여자가 이해하고, 검토하고, 테스트하고, 수정할 것 | 방법이 아니라 결과에 대한 책임을 규제([Debian이 생성형 AI를 허용하되 책임은 기여자에게 지웠다](../../open-source/debian-generative-ai.md)) |
| Godot     | 병합된 PR 3개라는 신뢰 단계와 사람이 썼다는 서약            | 리뷰어 부족과 열린 PR 5,479개([Godot](../../game/godot.md))                                                                                |

공통된 난점은 탐지가 불가능하다는 것이다.
OpenJDK는 사람과 AI 콘텐츠를 신뢰성 있게 구별할 수 없다고 스스로 밝혀 리뷰어에게
탐지 책임을
지우지
않는다([Oracle는 AI가 쓴 코드를 사랑하지만 OpenJDK에는 받지 않는다](../../java/openjdk-ai-ban.md)).
SourceHut 댓글은 같은 이유로 약관을 집행할 수 없고 책임만 기여자에게 넘어간다고
반박한다([SourceHut이 LLM 사용을 이용약관으로 금지하다](../../github/sourcehut-llm-ban.md)).
Linus Torvalds는 LLM이 메인테이너에게 고통이 아니라 도움이 되어야 한다고 했지만,
일부 메인테이너의 실제 경험은 반대라 둘 사이에 긴장이
있다([커널 개발에서 LLM 사용에 관한 Linus Torvalds의 견해](../../linux/linus-torvalds-on-llm-usage.md)).
[Short Leash AI 코딩 방법론](../../ai/short-leash-ai-coding-method.md)은
코드 품질은 측정할 수 있지만 개발자의 이해도는 그렇지 않다며,
제출자가 코드를 이해한다는 것을 메인테이너에게 입증할 수 있어야 한다고 본다.

관련: 이 비용 전가가 리뷰어 개인에게 어떻게
쌓이는지는 [리뷰하는 사람](reviewers.md)에서,
메인테이너 대기열의 규모는 [리뷰가 병목이 되다](bottleneck.md)에서 다룬다.

## 출처

- [ai/shopify-slop-grenades.md](../../ai/shopify-slop-grenades.md)
- [management/ai-slop-workplace-tax.md](../../management/ai-slop-workplace-tax.md)
- [ai/workslop.md](../../ai/workslop.md)
- [domain-driven-design/ddd-and-ai-coding.md](../../domain-driven-design/ddd-and-ai-coding.md)
- [agentic-coding/human-attention-and-human-effort.md](../../agentic-coding/human-attention-and-human-effort.md)
- [agentic-coding/meat-proxy.md](../../agentic-coding/meat-proxy.md)
- [agentic-coding/agentic-engineering-patterns.md](../../agentic-coding/agentic-engineering-patterns.md)
- [git/commit-description-thinking.md](../../git/commit-description-thinking.md)
- [agentic-coding/verification-debt.md](../../agentic-coding/verification-debt.md)
- [claude/claude-code-review.md](../../claude/claude-code-review.md)
- [code-review/human-ai-synergy-code-review.md](../../code-review/human-ai-synergy-code-review.md)
- [ai/ai-making-junior-devs-useless.md](../../ai/ai-making-junior-devs-useless.md)
- [ai/can-you-trust-ai-reviews.md](../../ai/can-you-trust-ai-reviews.md)
- [ai/human-in-loop-tired.md](../../ai/human-in-loop-tired.md)
- [security/snowflake-jira-copilot-autofix.md](../../security/snowflake-jira-copilot-autofix.md)
- [agentic-coding/its-the-infrastructure-not-the-ai.md](../../agentic-coding/its-the-infrastructure-not-the-ai.md)
- [management/appearing-productive-ai.md](../../management/appearing-productive-ai.md)
- [developer-tools/tools-encode-trust.md](../../developer-tools/tools-encode-trust.md)
- [java/openjdk-ai-ban.md](../../java/openjdk-ai-ban.md)
- [github/sourcehut-llm-ban.md](../../github/sourcehut-llm-ban.md)
- [open-source/debian-generative-ai.md](../../open-source/debian-generative-ai.md)
- [game/godot.md](../../game/godot.md)
- [linux/linus-torvalds-on-llm-usage.md](../../linux/linus-torvalds-on-llm-usage.md)
- [ai/short-leash-ai-coding-method.md](../../ai/short-leash-ai-coding-method.md)
