# AI 리뷰어는 어디까지 하는가

[← AI 시대의 코드 리뷰](index.md)

리뷰 병목에 대한 가장 직접적인 처방은 리뷰도 AI에게 맡기는 것이다.
이 저장소의 노트들은 AI 리뷰어가 실제로 버그를 잡는다는 기록과,
잡음과 과신 때문에 오히려 부담이 늘었다는 기록을 함께 담고 있다.

## 측정된 성능은 출처마다 정반대다

| 출처                                                                                                                         | 측정 결과                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Anthropic 자체 보고([Claude Code Review](../../claude/claude-code-review.md))                                                | 실질적 코멘트를 받는 PR 16%→54%, 1,000줄 넘는 PR의 84%에서 평균 7.5건 발견, 틀렸다고 표시된 지적 1% 미만, 리뷰당 15~25달러 |
| 리뷰 대화 278,790건 분석([코드 리뷰에서 AI는 지적하고 사람은 이해시킨다](../../code-review/human-ai-synergy-code-review.md)) | 제안 채택률 사람 56.5%, AI 16.6%, 채택되지 않은 AI 제안의 28.7%는 명백히 잘못된 코드                                       |
| Creatrip 자체 벤치마크([AI 리뷰를 신뢰할 수 있을까요?](../../ai/can-you-trust-ai-reviews.md))                                | 프로덕션 핫픽스로 만든 벤치마크에서 초기 33점, 체감 “잘 된다”와 실제 점수가 어긋남                                         |
| 207개 프로젝트 PR 102만 건([리뷰는 빨라졌지만 좋아지지는 않았다](../../code-review/review-quality-across-ai-eras.md))        | 급진적 LLM 도입은 속도 개선이 유의하지 않고 리뷰 스멜이 늘어남                                                             |
| Open Code Review 자가 측정 vs 독립 측정([Open Code Review](../../code-review/open-code-review.md))                           | 자가 주장은 고정밀, HN 사용자의 제3자 측정은 정밀도 약 12%, 재현율 약 74%                                                  |

Anthropic 수치의 54%는 사람이 리뷰한 비율이 아니라 실질적 코멘트를 받은
PR의 비율이라는 점에
주의해야 한다([Claude Code Review](../../claude/claude-code-review.md)).
자가 측정과 독립 측정이 정반대로 나온 Open Code Review 사례는
AI 리뷰 도구의 성능 주장을 그대로 받아들이기 어렵다는 것을 보여 준다.

## 잘하는 것과 못 하는 것

긍정적인 사용기도 많다.
[AI 도구 실전 실험 기록](../../agentic-coding/artificial-adventures.md)은
가장 가치가 컸던 용도를 코드 리뷰로 꼽으며,
diff가 컨텍스트를 한정하고 답이 버그 유무로
수렴하기 때문에 AI의 “킬러 유스케이스”라고 본다.
Claude Code Review는 인증을 깨뜨릴 한 줄 변경 같은 의미 수준의 결함을 잡은
사례를 든다([Claude Code Review](../../claude/claude-code-review.md)).

못 하는 쪽은 diff 바깥의 기억이 필요한 결함이다.
최신 LLM 리뷰가 놓치고 사람이 잡은
사례 세 건(gitconfig 잠금, AWS CLI 버전, 체크섬 비원자성)은
모두 diff 바깥의 맥락이
필요했다([코드가 리뷰를 앞질렀다](../../code-review/code-outruns-review.md)).
Gandhi가 잡은 버그 세 건 가운데 둘도 주변 코드에 경험이 있는
사람의
PR이었다([코드를 리뷰하는 것은 배워서 늘릴 수 있는 기술이다](../../code-review/reviewing-is-a-skill.md)).
[Verification Debt](../../agentic-coding/verification-debt.md)는
Greptile이나 Bugbot이 구문적 결함은 잡지만
“사용자가 원하는 것을 하는가”는 환원할 수 없는 사람의 판단이라고 본다.
AI 코멘트의 95% 이상이 코드 개선과 결함 탐지인 반면 사람은 이해를 돕는 피드백을
31% 준다는 분석도 같은 경계를 보여
준다([코드 리뷰에서 AI는 지적하고 사람은 이해시킨다](../../code-review/human-ai-synergy-code-review.md)).

## 잡음은 비용이다

Swizec Teller의 팀은 BugBot에 주당 약 1,000달러,
자체 Claude 리뷰 스킬을 CI에서 돌리는 데 하루 1,000달러를 썼고,
지적이 너무 많아 AI 코멘트까지 검토해야 해서 리뷰 부담이 오히려 늘었다고
한다([AI 코드 리뷰에 토큰을 태우지 말고, 결정론적 규칙은 커스텀 린터로 옮겨라](../../agentic-coding/stop-burning-tokens-on-code-review.md)).
그래서 결정론적 규칙은 커스텀 린터로 옮기자는 결론을 낸다.

잡음을 줄이는 쪽으로 설계된 도구도 있다.
Codex 루브릭은 “해당 커밋에서 생긴 문제”, “저자가 알았다면 고쳤을 것”,
“영향이 추측이 아니라 증명 가능할 것” 같은 조건을 두어
틀린 것이 아니라 말할 가치가 있는 것을
고른다([OpenAI Codex의 코드 리뷰 루브릭](../../codex/codex-review-rubric.md)).
PR Agent는 기본 최대 지적 수를 3개로
묶는다([PR Agent](../../code-review/pr-agent.md)).
반대로 정밀도만 높인 봇은 “지적 없음”을 “문제 없음”으로 착각하게 만들어 아무도
보지 않는 사각지대를 만든다는 경고도
있다([Open Code Review](../../code-review/open-code-review.md)).
Creatrip은 지표를 정확도에서 채택률로 바꾸고 PR 템플릿에
의도와 결정 섹션을 넣어 채택률 63%를 얻었는데,
그 개선은 모델 성능보다 UX 덕분이었다고
본다([AI 리뷰를 신뢰할 수 있을까요?](../../ai/can-you-trust-ai-reviews.md)).

## 여러 모델로 교차 리뷰하기

같은 모델은 같은 편향을 공유하므로 다른 모델로 리뷰하라는 권고가 반복된다.
[LLM은 올바른 코드가 아니라 그럴듯한 코드를 쓴다](../../llm/llm-writes-plausible-code-not-correct-code.md)는 LLM에게 자기 코드를 리뷰시키지 말라고 하고,
Codex 플러그인의 `/codex:adversarial-review`도 같은 이유로
다른 모델 간 적대적 검증을
한다([OpenAI의 Claude Code용 Codex 플러그인](../../codex/openai-codex-plugin-for-claude-code.md)).
CodeRabbit, Greptile, Sentry Seer,
Cursor BugBot을 함께 돌렸더니 발견한 문제의 93.4%가
한 도구에서만 탐지됐다는 데이터는
이종성이 핵심이라는 근거로
쓰인다([에이전트 시대의 코드 리뷰](../../code-review/agentic-code-review.md)).
Nolan Lawson은 Claude, Codex,
Bugbot을 함께 돌려 거짓 양성을 거르고 critical과 high만
고친다([AI로 더 좋은 코드를, 더 느리게 작성하기](../../agentic-coding/ai-code-review-slowly.md)).
Bun의 Rust 이식은 태스크마다 구현자 1명, 적대적 리뷰어 2명,
수정자 1명을
붙였다([Rewriting Bun in Rust](../../rust/rewriting-bun-in-rust.md)).

반대 근거도 있다.
멀티 모델 결합의 정확도 상한은 모든 모델이 동시에 틀릴 확률로 정해지고,
세 모델의 비가중 다수결은 평균적으로
오히려
손해였다([멀티 모델 결합의 상한선은 공동 실패율이다](../../llm/multi-model-orchestration-co-failure-ceiling.md)).
Creatrip은 서브에이전트를 늘리자 성능이
떨어졌다([AI 리뷰를 신뢰할 수 있을까요?](../../ai/can-you-trust-ai-reviews.md)).
같은 모델 기반 AI끼리의 교차 리뷰는 같은 맹점을 공유한다는
지적([잠자는 동안 돌아가는 에이전트를 만들고 있다](../../agentic-coding/agents-that-run-while-i-sleep.md))과
에이전트가 만든 코드를 에이전트가 검증하면 검증의 독립성이
사라진다는 지적([OpenAI Symphony](../../codex/symphony.md))도 있다.
LLM 코드를 다른 LLM이 리뷰하는 해법 자체에 회의적인 시각도
있다([Yap: LLM 코드 주석의 군더더기에 이름 붙이기](../../code-review/yap-llm-comments.md)).

## 누가 쓰고 누가 리뷰하는가

Peter Bloem은 AI가 쓰고 사람이 확인하는 구도가 성립하지 않는다고 본다.
사람은 모든 줄을 깊이 확인하지 못하고,
실패가 드물면 기계를 믿게 되며, 남의 코드 확인은 재미가 없다는 이유다.
그래서 “당신이 코딩하고 AI가 리뷰하라”를 원칙으로
삼는다([크래프트 코딩: 사람이 손으로 쓰고 AI가 리뷰한다](../../agentic-coding/craft-coding.md)).
OpenJDK와 SourceHut도 LLM을 이해·디버그·리뷰에 쓰는 것은 허용하고
생성 코드 제출만
막는다([Oracle는 AI가 쓴 코드를 사랑하지만 OpenJDK에는 받지 않는다](../../java/openjdk-ai-ban.md), [SourceHut이 LLM 사용을 이용약관으로 금지하다](../../github/sourcehut-llm-ban.md)).
AI를 리뷰어로 쓰는 것과 작성자로 쓰는 것을 구분하는 흐름이다.
Addy Osmani는 반대로 AI가 쓰고 사람은 위험도 분류만 보는 “루프 위의 인간”을
제안한다([에이전트 시대의 코드 리뷰](../../code-review/agentic-code-review.md)).

관련: 생성자와 평가자를 분리하는 설계와 그 무한 후퇴 문제는
[하네스 엔지니어링의 검증 계층의 분리와 그 한계](../harness-engineering/evaluator-separation.md)에 있다.
AI 리뷰를 결정론적 도구로 바꾸는 쪽은
[리뷰를 어디로 옮기는가](shifting-review.md)를 본다.

## 출처

- [claude/claude-code-review.md](../../claude/claude-code-review.md)
- [code-review/human-ai-synergy-code-review.md](../../code-review/human-ai-synergy-code-review.md)
- [ai/can-you-trust-ai-reviews.md](../../ai/can-you-trust-ai-reviews.md)
- [code-review/review-quality-across-ai-eras.md](../../code-review/review-quality-across-ai-eras.md)
- [code-review/open-code-review.md](../../code-review/open-code-review.md)
- [agentic-coding/artificial-adventures.md](../../agentic-coding/artificial-adventures.md)
- [code-review/code-outruns-review.md](../../code-review/code-outruns-review.md)
- [code-review/reviewing-is-a-skill.md](../../code-review/reviewing-is-a-skill.md)
- [agentic-coding/verification-debt.md](../../agentic-coding/verification-debt.md)
- [agentic-coding/stop-burning-tokens-on-code-review.md](../../agentic-coding/stop-burning-tokens-on-code-review.md)
- [codex/codex-review-rubric.md](../../codex/codex-review-rubric.md)
- [code-review/pr-agent.md](../../code-review/pr-agent.md)
- [llm/llm-writes-plausible-code-not-correct-code.md](../../llm/llm-writes-plausible-code-not-correct-code.md)
- [codex/openai-codex-plugin-for-claude-code.md](../../codex/openai-codex-plugin-for-claude-code.md)
- [code-review/agentic-code-review.md](../../code-review/agentic-code-review.md)
- [agentic-coding/ai-code-review-slowly.md](../../agentic-coding/ai-code-review-slowly.md)
- [rust/rewriting-bun-in-rust.md](../../rust/rewriting-bun-in-rust.md)
- [llm/multi-model-orchestration-co-failure-ceiling.md](../../llm/multi-model-orchestration-co-failure-ceiling.md)
- [agentic-coding/agents-that-run-while-i-sleep.md](../../agentic-coding/agents-that-run-while-i-sleep.md)
- [codex/symphony.md](../../codex/symphony.md)
- [code-review/yap-llm-comments.md](../../code-review/yap-llm-comments.md)
- [agentic-coding/craft-coding.md](../../agentic-coding/craft-coding.md)
- [java/openjdk-ai-ban.md](../../java/openjdk-ai-ban.md)
- [github/sourcehut-llm-ban.md](../../github/sourcehut-llm-ban.md)
