# 하네스는 소모품이다: 유지와 가지치기

[← 하네스 엔지니어링](index.md)

하네스를 짓는 능력과 하네스를 해체하는 규율은 별개의 기술이며, 이
저장소의 노트들은 후자가 거의 항상 빠져 있다는 것을 반복해서 지적한다.
프롬프트와 규칙 파일은 자연스럽게 자라기만 하고, 줄어드는 방향의
절차는 누구도 기본으로 갖추지 않는다.

## 추가는 안심을 주고 삭제는 위험만 준다

[Claude 5 세대 모델을 위한 컨텍스트 엔지니어링의 새
규칙](../../claude/new-rules-of-context-engineering-for-claude-5.md)의
인사이트가 이 비대칭의 원인을 짚는다 — 문제가 생기면 지시를 추가하고,
그 지시는 문제가 재발하지 않는 한 검토되지 않는다. 추가는 즉각적인
안심을 주고 삭제는 위험만 주기 때문에 단조 증가가 자연스럽게
일어난다. Anthropic이 Claude Code 시스템 프롬프트의 80% 이상을
걷어냈다는 사례의 진짜 의미도 여기 있다 — 모델이 좋아져서 불필요해진
것이 아니라, 불필요해졌는데 아무도 확인하지 않아서 남아 있었을
가능성이 크다는 것이다.

[같은 지적을 반복하지 않으려고 agent.md를
썼다](../../agentic-coding/sanglard-agent-md.md)가 같은 문제를 규칙
파일 차원에서 보여준다. 저자는 에이전트에게 직접 `agent.md`를
갱신하라고 요청하는 방식으로 규칙 추가의 마찰을 없앴는데, 이 편의가
목록을 단조 증가시킨다. 비평이 짚는 세 가지 문제가 구체적이다.
규칙 간 충돌(짧게 쓰라는 항목과 상세히 주석 달라는 항목이 공존해도
결정 기준이 없다), 근거의 소실(왜 그 규칙이 생겼는지 기록되지 않아
반년 뒤에는 아무도 필요성을 판단할 수 없다), 그리고 삭제의 부재
(코드에는 삭제가 있지만 규칙 목록에는 대체로 없다).

## 소멸을 절차로 만든 유일한 사례

[Learn Harness Engineering
강의](../../agentic-coding/learn-harness-engineering-lectures.md)
12강이 이 문제에 대한 구체적 해법을 제시하는 거의 유일한 노트다 —
월별로 하네스 구성 요소 하나를 비활성화하고 벤치마크해, 필요 없으면
제거하거나 더 가벼운 대안으로 교체하라는 것이다. [장기 실행
애플리케이션 개발을 위한 하네스
설계](../../agentic-coding/harness-design-long-running-apps.md)의
“가정을 스트레스 테스트하라”는 원칙도 같은 방향이지만 구체적 주기를
명시하지 않는다는 점에서 12강의 처방이 더 실행 가능하다. 이 노트의
인사이트는 이 규율의 필요성을 컴파일러 최적화 트릭의 역사에
비유한다 — 하네스 엔지니어가 정교한 구조를 만들수록 다음 모델
릴리스가 자기 작업을 폐기할 가능성에 더 많이 노출된다. 합리적 전략은
하네스를 영구 자산이 아니라 모델 능력의 현재 격차를 메우는 일회용
발판으로 다루는 것이다.

## 클린 상태를 완료의 정의에 포함시킨다

[Learn Harness Engineering
강의](../../agentic-coding/learn-harness-engineering-lectures.md)
12강은 가지치기를 “완료”의 조건 자체로 승격시킨다. 세션이 빌드·테스트·
진행 상황·산출물·시작 가능성이라는 다섯 차원 모두에서 깨끗하지 않으면
완료된 것이 아니라는 것이다. 정리 전략 없는 프로젝트는 12주 후 빌드
성공률이 68%로 떨어졌지만, 정리 전략이 있는 프로젝트는 97%를
유지했다는 실측이 이 규율의 값을 보여준다. Lehman의 소프트웨어 진화
법칙(능동적 정리 없이는 복잡성이 기하급수적으로 증가한다는 것)이
이 현상의 이론적 근거로 인용된다.

## 왜 이 규율이 특히 잘 지켜지지 않는가

가지치기가 유독 소홀히 다뤄지는 이유는 그것이 자기 실수의 기록이기
때문이다. [solo-skills: 혼자 49개를 자동화하고 그중 15개를 함정
목록과 함께 공개했다](../../agentic-coding/solo-skills.md)의
분석이 이 심리를 정확히 짚는다 — “성공한 방법만 적으면 다음 사람이
같은 데서 막힌다”는 것을 알면서도 실패 기록을 남기는 사람이 드문
이유는, 그것이 자기가 겪은 실수를 공개적으로 인정하는 일이기
때문이다. 규칙을 삭제하는 것도 같은 심리적 장벽을 갖는다 — “이
규칙은 더 이상 필요 없다”고 선언하려면 그 규칙이 왜 있었는지, 그리고
지금은 왜 없어도 되는지를 능동적으로 확인해야 하는데, 확인하지
않고 그냥 두는 쪽이 훨씬 쉽다.

## 결정론적 규칙과 텍스트 지침은 소모 속도가 다르다

[결정론적 강제와 텍스트 지침의 경계](deterministic-vs-prompted.md)에서
다룬 분류가 가지치기 전략에도 그대로 적용된다. 포매터·린터로 옮긴
규칙은 모델 세대가 바뀌어도 낡지 않는다 — `rustfmt`나 `black`이
강제하는 규칙은 어떤 모델을 쓰든 여전히 유효하다. 반면 텍스트로 남은
규칙, 특히 “이전 모델은 이걸 못 해서 넣은 지침”은 다음 모델에서
바로 사장 비용이 될 후보다. 이는 가지치기 대상의 우선순위를 정해준다
— 규칙 파일을 검토할 때 먼저 확인할 것은 “검사로 옮길 수 있는 항목이
아직 프롬프트에 남아 있는가”이고, 그다음이 “모델이 이제 기본적으로
지키는 항목이 남아 있는가”다. [Learn Harness Engineering
강의](../../agentic-coding/learn-harness-engineering-lectures.md)가
제시한 월별 실험은 후자를 확인하는 절차이고, 전자는 그보다 앞서
상시로 확인해야 하는 더 기본적인 점검이다.

## 관련

[모델이 좋아져도 하네스가 사라지지 않는 이유](why-harness-persists.md) ·
[결정론적 강제와 텍스트 지침의 경계](deterministic-vs-prompted.md)

## 출처

- [claude/new-rules-of-context-engineering-for-claude-5.md](../../claude/new-rules-of-context-engineering-for-claude-5.md)
- [agentic-coding/sanglard-agent-md.md](../../agentic-coding/sanglard-agent-md.md)
- [agentic-coding/learn-harness-engineering-lectures.md](../../agentic-coding/learn-harness-engineering-lectures.md)
- [agentic-coding/harness-design-long-running-apps.md](../../agentic-coding/harness-design-long-running-apps.md)
- [agentic-coding/solo-skills.md](../../agentic-coding/solo-skills.md)
