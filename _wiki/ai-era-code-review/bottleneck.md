# 리뷰가 병목이 되다

[← AI 시대의 코드 리뷰](index.md)

AI가 코드 생산량을 늘리자 리뷰는 개발 흐름에서 가장 좁은 구간이 되었다.
이 저장소에서 가장 많은 노트가 동의하는 지점이고, 수치도 가장 많이 쌓여 있다.

## 실측 데이터

| 출처                                                                                                                                 | 생산 쪽 변화                                      | 리뷰 쪽 변화                                             |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- | -------------------------------------------------------- |
| Jellyfish 718개사 이중차분 분석([코드는 30% 늘었지만 소프트웨어는 늘지 않았다](../../agentic-coding/more-code-not-more-software.md)) | 코드 30%, PR 23% 증가, 이슈·에픽 해결은 변화 없음 | 리뷰 시간 49%, 리뷰 담당 인원 14%, 변경 요청 비율 약 2배 |
| Faros AI 22,000명([에이전트 시대의 코드 리뷰](../../code-review/agentic-code-review.md))                                             | 코드 이탈률 861% 증가                             | 리뷰 시간 441.5% 증가                                    |
| Faros AI([코드가 리뷰를 앞질렀다](../../code-review/code-outruns-review.md))                                                         | —                                                 | 리뷰 없이 머지된 PR 31.3% 증가                           |
| [코드 리뷰는 어떻게 죽는가](../../agentic-coding/reviews-dead.md)                                                                    | 태스크 21%, PR 머지 98% 증가                      | PR 리뷰 시간 91% 증가                                    |
| Anthropic 내부([Claude Code Review](../../claude/claude-code-review.md))                                                             | 엔지니어 1인당 산출 200% 증가                     | —                                                        |
| GitHub 보고서([AI 리뷰를 신뢰할 수 있을까요?](../../ai/can-you-trust-ai-reviews.md))                                                 | 머지된 PR 23% 증가                                | AI 코드의 PR당 이슈율 1.7배, 논리 오류율 75% 높음        |

리뷰 시간 증가폭은 49%에서 441.5%까지 크게 다르다.
측정 방식과 표본이 달라 직접 비교할 수는 없고,
[코드가 리뷰를 앞질렀다](../../code-review/code-outruns-review.md)는
Faros 수치에 관찰 데이터라는 단서를 붙인다.
방향은 모든 수치가 같다.

## 비율이 깨졌다

Kieran Klaassen은 작성 시간 대 리뷰 시간 비율이 원래 5:1~10:1이었는데 AI가 이를
깨뜨렸다고
본다([AI가 코드 작성과 리뷰의 비율을 깨뜨렸다는 주장](../../code-review/review-ratio-broken.md)).
HN의 intended는 이를 “검증 용량 대 생성 용량 비율이 깨진 문제”로 불렀고,
한 사람의 생산성이 다른 사람의 검토 부담이 된다고
짚었다([미안하지만 여전히 생각은 해야 한다](../../agentic-coding/you-still-have-to-think.md)).
리드타임의 80%가 PR 리뷰, CI,
QA 같은 대기열이라는
진단([코드 작성 속도가 문제라고 생각했다면 더 큰 문제가 있다](../../agile/if-you-thought-the-speed-of-writing-code-was-your-problem.md))과
가장 느린 단계가 전체 처리량을 정한다는
지적([AI 보조 코딩 평가에서 틀리는 열두 가지 방식](../../agentic-coding/twelve-ways-wrong-ai-coding.md))이 같은 결론을 낸다.
리뷰어의 처리량이 그대로면 대기열만 쌓이고,
AI 출력을 충분히 믿을 수 없으니 사람 검증을 건너뛸 수도
없다([Writing Code vs. Shipping Code](../../ai/writing-code-vs-shipping-code.md)).

반론도 있다.
같은 노트는 리뷰, 테스트,
배포가 동시에 도는 환경에서는 가장 느린 단계가 전체를 막는다는 가정이
늘 성립하지는 않는다고
덧붙인다([Writing Code vs. Shipping Code](../../ai/writing-code-vs-shipping-code.md)).
Linear는 에이전트 때문에 CI가 병목이 되자 테스트 묶음이 거의 4배로 늘었는데도
PR 대기 시간을
줄였다([AI 코딩이 CI를 병목으로 만들었을 때 Linear가 한 일](../../devops/linear-ci-bottleneck.md)).
병목이 리뷰가 아니라 기계 쪽 대기열에 있는 경우도 있다는 뜻이다.

## 러버스탬프와 검증 부채

리뷰가 밀리면 승인은 형식이 된다.
PR이 폭증해도 리뷰어는 늘지 않으니 리뷰 대기, 컨텍스트 전환,
러버스탬프 승인, 품질 저하가 차례로 온다는 진단이 있고,
그 결과를 “더 많은 코드, 더 적은 이해”라고
부른다([코드 작성 속도가 문제라고 생각했다면 더 큰 문제가 있다](../../agile/if-you-thought-the-speed-of-writing-code-was-your-problem.md)).
[LLM 시대의 엔지니어링](../../llm/engineering-in-llm-age.md)은
한 사람의 컨텍스트 창을 넘는 PR은 승인은 되지만 읽히지는 않는다고 본다.
[잠자는 동안 돌아가는 에이전트를 만들고 있다](../../agentic-coding/agents-that-run-while-i-sleep.md)의 저자는 리뷰 시간이 늘다가 어느 순간 diff를 읽지 않게 됐다고 고백한다.

[Verification Debt](../../agentic-coding/verification-debt.md)는
이 상태에 이름을 붙인다.
검증 부채는 생성 속도와 검증 속도의 격차이고,
이해하지 못한 diff를 승인할 때마다 미래에서 빌려 온다.
기술 부채와 달리 마찰로 드러나지 않고 거짓 안심을 준다는 점이 더 위험하다.
생산성 향상은 산출물 50% 증가가
아니라 리뷰 부담 50% 증가라는 표현도 같은 노트에 있다.

## 오픈소스 메인테이너의 대기열

병목은 회사 밖에서 더 극단적이다.
curl은 실제 보고 비율이 5% 아래로 떨어지자 버그 현상금을 끝냈고,
Ghostty의 Mitchell Hashimoto는 저품질 AI 기여로 “나쁜” 건수가 10배 이상 늘었다고
썼다([AI는 낯선 사람의 PR을 받아 주던 오픈소스를 끝내고 있다](../../open-source/open-source-is-dead.md)).
Godot에는 열린 PR이 5,479개 쌓였고,
원인은 자격 있는 리뷰어 부족이다([Godot](../../game/godot.md)).
OpenJDK는 AI 기여 금지의 첫 근거로 리뷰어 부담을
들었다([Oracle는 AI가 쓴 코드를 사랑하지만 OpenJDK에는 받지 않는다](../../java/openjdk-ai-ban.md)).

관련: 병목이 생긴 뒤 각 조직이 택한 처방은
[리뷰를 어디로 옮기는가](shifting-review.md)와
[AI 리뷰어는 어디까지 하는가](ai-reviewers.md)에서,
오픈소스의 정책 대응은 [책임은 누구에게 있는가](accountability.md)에서 다룬다.
검증 부채가 자율성 확대와 맞물리는 구조는
[에이전트형 코딩의 실패/함정 패턴의 자율성이 검증을 잠식하는 구조](../agentic-coding-failure-patterns/autonomy-erodes-verification.md)에 더 자세히 있다.

## 출처

- [agentic-coding/more-code-not-more-software.md](../../agentic-coding/more-code-not-more-software.md)
- [code-review/agentic-code-review.md](../../code-review/agentic-code-review.md)
- [code-review/code-outruns-review.md](../../code-review/code-outruns-review.md)
- [agentic-coding/reviews-dead.md](../../agentic-coding/reviews-dead.md)
- [claude/claude-code-review.md](../../claude/claude-code-review.md)
- [ai/can-you-trust-ai-reviews.md](../../ai/can-you-trust-ai-reviews.md)
- [code-review/review-ratio-broken.md](../../code-review/review-ratio-broken.md)
- [agentic-coding/you-still-have-to-think.md](../../agentic-coding/you-still-have-to-think.md)
- [agile/if-you-thought-the-speed-of-writing-code-was-your-problem.md](../../agile/if-you-thought-the-speed-of-writing-code-was-your-problem.md)
- [agentic-coding/twelve-ways-wrong-ai-coding.md](../../agentic-coding/twelve-ways-wrong-ai-coding.md)
- [ai/writing-code-vs-shipping-code.md](../../ai/writing-code-vs-shipping-code.md)
- [devops/linear-ci-bottleneck.md](../../devops/linear-ci-bottleneck.md)
- [llm/engineering-in-llm-age.md](../../llm/engineering-in-llm-age.md)
- [agentic-coding/agents-that-run-while-i-sleep.md](../../agentic-coding/agents-that-run-while-i-sleep.md)
- [agentic-coding/verification-debt.md](../../agentic-coding/verification-debt.md)
- [open-source/open-source-is-dead.md](../../open-source/open-source-is-dead.md)
- [game/godot.md](../../game/godot.md)
- [java/openjdk-ai-ban.md](../../java/openjdk-ai-ban.md)
