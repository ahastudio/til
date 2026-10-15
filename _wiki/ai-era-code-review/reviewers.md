# 리뷰하는 사람

[← AI 시대의 코드 리뷰](index.md)

리뷰 병목과 책임 문제는 결국 리뷰어 한 사람에게 쌓인다.
노트들은 리뷰를 배워서 늘릴 수 있는 기술로 보면서도,
AI 시대에 그 기술을 기르는 경로와 리뷰를 하고
싶은 동기가 함께 약해지고 있다고 기록한다.

## 리뷰는 기술이다

Varun Gandhi는 리뷰를 배우고 가르칠 수 있는 기술로 보고,
인간 능력의 천장을 아직 모른다고 쓴다.
그의 리뷰 의견 밀도는 30~100줄당 하나였고 대부분은
버그가 아니라 명확화 질문과 이름 짓기였다.
실력을 기를 실험으로 소크라테스식 과정 대화, 아차사고 사후 검토,
코드를 보지 않는 격리 모델링(Alloy),
전문성 연구를
제안한다([코드를 리뷰하는 것은 배워서 늘릴 수 있는 기술이다](../../code-review/reviewing-is-a-skill.md)).
[시니어 엔지니어 옆자리에서 1년](../../software-engineering/sitting-next-to-a-senior-engineer.md)은 동작 방식을 이해하기 전에는 승인하지 않는 규칙과,
이름의 무게를 리뷰로 배운 경험을 기록한다.
AI 발견을 분류하는 데도 도메인 전문성이 필요하고 주니어는 멘토링 없이 어렵다는
지적이
있다([AI로 더 좋은 코드를, 더 느리게 작성하기](../../agentic-coding/ai-code-review-slowly.md)).

AI 시대에 리뷰어에게 필요한 능력이 바뀐다는 주장도 있다.
반복 검증에서는 사람이 가장 약한 고리이니 기계에 맡기고 사람은
시스템 동작 이해로 옮겨 가야 한다는
주장([AI는 더 많은 엔지니어링 규율을 요구한다](../../agentic-coding/ai-demands-more-engineering-discipline.md)),
코드 리뷰보다 측정 설계에 가까운 능력이 필요하다는
주장([미안하지만 여전히 생각은 해야 한다](../../agentic-coding/you-still-have-to-think.md))이 그 예다.
앞의 노트에는 검증을 맡기면 이해까지 맡기게 되고
그 역량이 형성되는 경로가 막힌다는 반박이 함께 있다.

## 피로와 탈숙련

자동화는 만족스러운 작업을 없애고 지루한 감독 업무를 늘렸다.
30개 PR을 처리하는 모드의 판단 피로는 산출 지표에
잡히지 않으니 리뷰어의 인지 부하를 워크플로 설계에 넣어야 한다는 것이
[루프 속의 인간은 지쳐 있다](../../ai/human-in-loop-tired.md)의 주장이다.
같은 노트는 작은 diff, 명확한 테스트, 의도 요약을 PR의 조건으로 두자고 한다.
반론으로,
AI 코드를 리뷰할 때는 동료의 자존심을 고려하는 감정 노동이
없어 더 쉬운 면도 있다는 HN 댓글이 함께 실려 있다.

[에이전트 코딩의 네 기수](../../agentic-coding/four-horsemen.md)는
소외와 탈숙련이 리뷰 피로로 먼저 터진다고 본다.
리뷰는 사람이 코드를 읽는 마지막 지점이라 작성자가
코드에서 멀어진 만큼 부담이 리뷰어에게 몰리고,
리뷰까지 에이전트에게 넘기면 조직에서 코드를 읽는 사람이 사라진다.
치명적 버그로 병합을 막았더니 작성자가 매니저에게 신고한 사례도 기록되어 있다.
Kieran Klaassen은 13개 AI 리뷰어에게 리뷰를 맡기고 코드를 읽지 않게 되면서
스스로 “형태에 대한 감각”을 잃을 수 있다고
우려했다([AI가 코드 작성과 리뷰의 비율을 깨뜨렸다는 주장](../../code-review/review-ratio-broken.md)).
수동적으로 리뷰만 하면 소유감이 생기지 않고
슬롭이 레이더 아래로 지나간다는 주장도 있지만,
노트는 그 인과관계가 검증되지 않았다고
비판한다([2026년에도 왜 코드를 직접 작성해야 하는가](../../agentic-coding/why-write-code-in-2026.md)).
시니어에게 AI 코드 리뷰만 시키는 것은 낭비라는
관점([잠자는 동안 돌아가는 에이전트를 만들고 있다](../../agentic-coding/agents-that-run-while-i-sleep.md))과
시니어 엔지니어의 리뷰 부담이 “세금”처럼 늘어난다는
관점([에이전트 시대의 코드 리뷰](../../code-review/agentic-code-review.md))도
같은 문제를 다른 각도에서 본다.

## 리뷰 품질은 사람 조합에서도 나빠진다

102만 건의 PR을 본 연구에서 같은 리뷰어 조합이 반복되는 “Review Buddies” 스멜은
사람만 참여할 때 16%였지만 LLM이 끼면 60%, 에이전트가 끼면 53%였다.
에이전트가 먼저 리뷰하는 패턴은 더 빠르지만 스멜이
더
많았다([리뷰는 빨라졌지만 좋아지지는 않았다](../../code-review/review-quality-across-ai-eras.md)).
사람이 AI 코드를 리뷰하면 코멘트 왕복이 11.8% 늘어난다는 분석도
있다([코드 리뷰에서 AI는 지적하고 사람은 이해시킨다](../../code-review/human-ai-synergy-code-review.md)).
AI가 끼어든 리뷰가 사람 사이의 관점 다양성을 줄일 수 있다는 신호다.

## 주니어와 멘토링의 단절

AI 이전에 리뷰는
멘토링의 피드백 수단이었다([달랩 멘토링](../../blog/2019/12-01-mentoring.md)).
지금은 리뷰에서 “왜 이 접근법을 선택했나?”에
답하지 못하는 주니어가 늘었다는 관찰이 있고,
이해하지 못한 코드는 절대 배포하지 말라는 권고가
붙는다([AI가 주니어 개발자를 무용하게 만들고 있다](../../ai/ai-making-junior-devs-useless.md)).
코드 리뷰로 다른 시각을 받던 관계가 프롬프트로 대체된다는
지적([루프 속의 인간은 지쳐 있다](../../ai/human-in-loop-tired.md))과,
피드백이 기계에 흡수될 뿐이라면 리뷰에 여가를 쓸 이유가
없다는 Godot 메인테이너의 말([Godot](../../game/godot.md))은
리뷰가 지식을 전수하던 경로가 끊기고 있음을 보여 준다.
관리자 쪽에서는 생산성 향상분의 일부를 설계 리뷰와 대화에 쓰라는 권고가
있다([관리는 죽지 않았다](../../management/managers-path-in-the-age-of-ai.md)).
팀 차원의 리뷰 최소 기준이 없으면 리뷰가 취향 충돌이나 아무도 책임지지 않는 통과
의례가 된다는 지적도 같은
맥락이다([AI 도입 시 해야 할 것 5가지](../../ai/five-things-for-ai-adoption.md)).

관련: 리뷰의 지식 전수 기능에 대한 정의는
[리뷰는 무엇을 지키는가](purpose.md)에,
리뷰어 부담을 키우는 작성자의 행동은
[책임은 누구에게 있는가](accountability.md)에 있다.

## 출처

- [code-review/reviewing-is-a-skill.md](../../code-review/reviewing-is-a-skill.md)
- [software-engineering/sitting-next-to-a-senior-engineer.md](../../software-engineering/sitting-next-to-a-senior-engineer.md)
- [agentic-coding/ai-code-review-slowly.md](../../agentic-coding/ai-code-review-slowly.md)
- [agentic-coding/ai-demands-more-engineering-discipline.md](../../agentic-coding/ai-demands-more-engineering-discipline.md)
- [agentic-coding/you-still-have-to-think.md](../../agentic-coding/you-still-have-to-think.md)
- [ai/human-in-loop-tired.md](../../ai/human-in-loop-tired.md)
- [agentic-coding/four-horsemen.md](../../agentic-coding/four-horsemen.md)
- [code-review/review-ratio-broken.md](../../code-review/review-ratio-broken.md)
- [agentic-coding/why-write-code-in-2026.md](../../agentic-coding/why-write-code-in-2026.md)
- [agentic-coding/agents-that-run-while-i-sleep.md](../../agentic-coding/agents-that-run-while-i-sleep.md)
- [code-review/agentic-code-review.md](../../code-review/agentic-code-review.md)
- [code-review/review-quality-across-ai-eras.md](../../code-review/review-quality-across-ai-eras.md)
- [code-review/human-ai-synergy-code-review.md](../../code-review/human-ai-synergy-code-review.md)
- [blog/2019/12-01-mentoring.md](../../blog/2019/12-01-mentoring.md)
- [ai/ai-making-junior-devs-useless.md](../../ai/ai-making-junior-devs-useless.md)
- [game/godot.md](../../game/godot.md)
- [management/managers-path-in-the-age-of-ai.md](../../management/managers-path-in-the-age-of-ai.md)
- [ai/five-things-for-ai-adoption.md](../../ai/five-things-for-ai-adoption.md)
