# 리뷰는 무엇을 지키는가

[← AI 시대의 코드 리뷰](index.md)

AI 시대에 리뷰를 줄일지 늘릴지는 리뷰가
무엇을 위한 것인지에 대한 답에 달려 있다.
이 저장소의 노트들은 그 답을 하나로 모으지 않는다.

## 버그 탐지인가, 유지보수성인가

Mark Dominus는 코드를 읽어서 버그를 찾는 일은 일반적으로 가능하지 않으며,
리뷰의 주된 목적은 유지보수하기 어려운 코드를 찾는 것이라고
본다([코드 리뷰의 목적은 버그 발견이 아니라 유지보수성 확인이다](../../code-review/purpose-maintainability.md)).
“버그를 찾아라”는 끝나는 기준이 없지만
“이해하고, 이해 안 되는 곳을 메모하라”는 완료 기준이 분명하다는 것이다.

반대편에는 버그를 잡은 기록이 있다.
Varun Gandhi는 자신이 리뷰에서 잡은 버그 세 건을
상위 LLM 리뷰가 모두 놓쳤다고 쓰면서,
구글 2018 연구가 정리한 리뷰 기대(교육, 규범 유지, 게이트키핑, 사고 예방)를 들어
리뷰가 여러 목적에 동시에 복무한다고
본다([코드를 리뷰하는 것은 배워서 늘릴 수 있는 기술이다](../../code-review/reviewing-is-a-skill.md)).
Codex 루브릭과 Claude Code Review 같은 AI 리뷰 도구는 거의 전적으로 버그 탐지에
맞춰져
있다([OpenAI Codex의 코드 리뷰 루브릭](../../codex/codex-review-rubric.md),
[Claude Code Review](../../claude/claude-code-review.md)).
AI가 잘하는 쪽이 버그 탐지이기 때문에, 리뷰의 목적을 어떻게 정의하느냐가
AI로 리뷰를 대체할 수 있느냐의 답을 거의 결정한다.

## 다섯 가지 역할로 나누기

[코드가 리뷰를 앞질렀다](../../code-review/code-outruns-review.md)는
리뷰의 역할을
검증, 유지보수성 확인, 지식 공유, 게이트키핑, 책임 분산의 다섯으로 나누고,
문제를 “사람과 AI 중 누가 더 잘하나”가
아니라 “이 역할을 어떻게 나누나”로 다시 세운다.
이 틀에서 보면 AI가 넘겨받을 수 있는 것은 검증의 일부이고,
지식 공유와 책임은 여전히 사람에게 남는다.
같은 노트는 사람이 소유해야 할 것으로 의도, 맥락, 증거,
책임을 꼽고 “모델은 온콜을 받을 수 없다”고 정리한다.

## 이해와 이론의 전수

Naur의 “이론 형성으로서의 프로그래밍”을 다룬 노트는
코드 읽기가 이론 전수의 불완전한 대체물이고,
그래서 페어 프로그래밍과 코드 리뷰가 지식 전수 수단으로 중요하다고
본다([이론 형성으로서의 프로그래밍](../../thinking/programming-as-theory-building.md)).
인지 부채를 다룬 노트들은 이 관점을 AI 시대로 옮긴다.
인지 부채는 코드가 바뀌는 속도보다 그 코드를
이해하는 사람이 줄어드는 속도가 빠를 때 쌓이고,
리뷰에서 “이게 왜 이렇게 됐어?”에 아무도 답하지 못하는 것이
그
증상이다([기술 부채, 인지 부채, 의도 부채](../../clean-code/tech-cognitive-intentional-debt.md)).
AI가 생성한 코드는 “어떤 사람의 이해도 반영하지 않을 수 있다”는 지적도 같은
맥락이다([‘부채’라는 말을 너무 쉽게 쓰고 있다](../../clean-code/debt-metaphor-misuse.md)).
작성 비용이 낮아질수록 리뷰와 이해가 더 귀해진다는
주장([코드는 더 싸졌다](../../software-engineering/code-got-cheaper.md))은
이 관점에서 나온다.

## 코드가 아니라 판단을 검증한다

[AI 시대, 코드 리뷰는 코드가 아니라 판단을 검증하는 것이다](../../code-review/ai-era.md)는
AI가 형식 검사라는 “가짜 리뷰”를 없애면서
진짜 리뷰가 무엇이었는지 드러났다고 본다.
[만드는 값이 0이 되면 남는 것은 판정뿐이다](../../programming/taste-is-all-thats-left.md)도
판정의 실무적 형태를 리뷰에서 “왜”를 묻는 일로 본다.
[코드를 아직도 읽는가](../../agentic-coding/accelerators-vs-vibecoders.md)는
코드 품질이 원래 “이해”의 대리 지표였는데
LLM이 이해를 흉내 내면서 그 대리 관계가 깨졌고,
리뷰는 “의도의 고고학”으로 바뀐다고 정리한다.

## 협업의 초대

오픈소스 쪽 노트는 리뷰를 사회적 장치로 정의한다.
[AI는 낯선 사람의 PR을 받아 주던 오픈소스를 끝내고 있다](../../open-source/open-source-is-dead.md)는 리뷰를 “함께 해 보자”는 대답으로 부르고,
Godot 노트는 리뷰가 미래의 메인테이너를 가르치는 일이라 보람이 있었는데
피드백이 기계에 흡수될 뿐이라면 여가를 리뷰에
쓸 이유가 없다고 적는다([Godot](../../game/godot.md)).
[스태프 엔지니어에게 필요한 세 가지 역량](../../management/staff-engineer-competencies.md)이
코드 리뷰 문화가 조직의 집단 지성이 작동하는
방식을 정한다고 본 것도 같은 줄에 있다.

관련: [리뷰하는 사람](reviewers.md)은 이
사회적 기능이 AI 시대에 어떻게 약해지는지를,
[리뷰를 어디로 옮기는가](shifting-review.md)는
목적별로 어떤 장치가 리뷰를 대신할 수 있는지를 다룬다.

## 출처

- [code-review/purpose-maintainability.md](../../code-review/purpose-maintainability.md)
- [code-review/reviewing-is-a-skill.md](../../code-review/reviewing-is-a-skill.md)
- [code-review/code-outruns-review.md](../../code-review/code-outruns-review.md)
- [code-review/ai-era.md](../../code-review/ai-era.md)
- [codex/codex-review-rubric.md](../../codex/codex-review-rubric.md)
- [claude/claude-code-review.md](../../claude/claude-code-review.md)
- [thinking/programming-as-theory-building.md](../../thinking/programming-as-theory-building.md)
- [clean-code/tech-cognitive-intentional-debt.md](../../clean-code/tech-cognitive-intentional-debt.md)
- [clean-code/debt-metaphor-misuse.md](../../clean-code/debt-metaphor-misuse.md)
- [software-engineering/code-got-cheaper.md](../../software-engineering/code-got-cheaper.md)
- [programming/taste-is-all-thats-left.md](../../programming/taste-is-all-thats-left.md)
- [agentic-coding/accelerators-vs-vibecoders.md](../../agentic-coding/accelerators-vs-vibecoders.md)
- [open-source/open-source-is-dead.md](../../open-source/open-source-is-dead.md)
- [game/godot.md](../../game/godot.md)
- [management/staff-engineer-competencies.md](../../management/staff-engineer-competencies.md)
