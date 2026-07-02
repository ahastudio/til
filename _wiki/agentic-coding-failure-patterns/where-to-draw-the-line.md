# 어디까지 자율을 주고 어디서 개입해야 하는가

[← 에이전트형 코딩의 실패/함정 패턴](index.md)

앞선 네 주제 — [돌이킬 수 없는 사고들](irreversible-incidents.md),
[자율성이 검증을 잠식하는 구조](autonomy-erodes-verification.md),
[스펙/TDD가 하는 일과 못 하는 일](spec-and-tdd-as-guardrails.md),
[멀티 에이전트 오케스트레이션 특유의 실패](multi-agent-orchestration-failures.md) —
를 관통해서 이 저장소의 노트들이 수렴하는 판단 기준을 정리한다.

## 리트머스 테스트: "이 장애를 소유할 수 있는가"

[agent-responsibly.md](../../agentic-coding/agent-responsibly.md)가 제시하는
"의존하기(Depend) vs 활용하기(Leverage)" 구분이 이 저장소에서 가장
자주 인용되는 판단 프레임이다. 세 가지 질문으로 요약된다.

1. 이 코드가 정확히 뭘 하는가?
2. 프로덕션에 어떤 악영향을 미칠 수 있는가?
3. 이 PR에서 장애가 나면 내가 소유할 수 있는가?

세 질문 모두 "예"여야 배포해도 된다는 것이다. 이 세 번째 질문은 사실상
"코드를 이해하는가?"와 같은 말이며, 여러 다른 노트에서 같은 형태로
반복된다.
[cursor-railway-db-incident.md](../../agentic-coding/cursor-railway-db-incident.md)에서는
운영자가 프로덕션 자격증명을 에이전트가 접근 가능한 파일에 두는 순간
이미 이 질문을 물었어야 했다는 사후 비평으로,
[ai-agent-aws-bankruptcy.md](../../agentic-coding/ai-agent-aws-bankruptcy.md)에서는
자격증명 위임 직전에 물었어야 할 질문으로,
[intent-debt.md](../../agentic-coding/intent-debt.md)에서는 "장애를
소유할 수 있는가"가 결국 "의도의 소유권" 질문이라는 형태로 다시
나타난다.

## 판단이 상류로 이동한다는 공통 관찰

[bottleneck-was-never-the-code.md](../../agentic-coding/bottleneck-was-never-the-code.md),
[verification-debt.md](../../agentic-coding/verification-debt.md),
[google-sre-ai.md](../../devops/google-sre-ai.md)가 독립적으로 같은
구조를 관찰한다. 에이전트가 구현(어떻게)을 맡을수록, 인간이 담당해야
할 몫은 명세와 검증(무엇을, 왜)으로 상류 이동한다. `google-sre-ai.md`는
이를 "코드 리뷰가 PR 단위 라인 검토에서 아키텍처·안전 제약 사전
정의로 이동해야 한다"고 표현하고,
[reviews-dead.md](../../agentic-coding/reviews-dead.md)는 "diff가 아니라
스펙과 인수 기준을 리뷰하라"는 실천으로 구체화한다. 이것은 도피가
아니라 이동이다 — 검증이 사라지는 게 아니라 자리를 옮긴다.

## 자동화 레벨: 낮은 위험부터 신뢰를 쌓는다

[google-sre-ai.md](../../devops/google-sre-ai.md)가 제시하는 L0~L4
자율성 수준(수동 → 보조 → 부분 → 높음 → 완전)과
[multi-agent-orchestration-problems.md](../../agentic-coding/multi-agent-orchestration-problems.md)의
업무 위임 판별 기준(오류 비용, 검증 용이성, 암묵지 의존도, 컨텍스트
범위, 피드백 루프 길이)은 사실상 같은 원칙을 서로 다른 언어로
말한다 — **오류 비용이 낮고 검증이 쉬운 작업부터 자율을 넓히고, 오류
비용이 높거나(돌이킬 수 없거나) 검증이 어려운(암묵지 의존적인) 작업은
인간이 쥐고 있어야 한다.**

`google-sre-ai.md`의 Actus 아키텍처는 이 원칙을 시스템으로 구현한
사례다. 에이전트에게 인프라 직접 접근을 주지 않고, 모든 프로덕션
변경이 통합 안전 게이트웨이를 거치도록 강제한다. 추론 엔진(에이전트)과
실행 엔진(Actus)을 엄격히 분리해, AI 모델이 아무리 발전해도 안전
경계는 유지되도록 설계한다. 이것은
[irreversible-incidents.md](irreversible-incidents.md)에서 확인한
교훈 — 프롬프트 기반 안전 지침은 시스템 레이어의 강제가 아니다 — 을
가장 성숙한 형태로 구현한 사례라 할 수 있다.

## 실행 가능한 보호장치 vs 문서 기반 지침

여러 노트가 공유하는 또 다른 결론: 규칙은 에이전트가 "읽고 따르는"
것이 아니라 "우회할 수 없는" 형태여야 한다. `agent-responsibly.md`의
"실행 가능한 보호장치(문서가 아닌 도구로 인코딩된 제약)",
`kakaopay-spec-kit-practice.md`의 "정책을 코드로 표현하라(Policy as
Code)", `intent-debt.md`의 "명시적 지시 없이 변경하지 말아야 할 영역을
나열한 문서" 사례가 모두 같은 원칙을 가리킨다. 텍스트 지침은 모델이
"이해하고 준수"할 것이라는 검증되지 않은 가정에 의존하지만, 코드로
인코딩된 제약은 모델의 판단과 무관하게 작동한다.

## 이 기준이 완전하지 않다는 것도 함께 기록되어야 한다

이 저장소의 노트들은 위 기준이 실제로 적용하기 쉽다고 주장하지
않는다. `agent-responsibly.md`에 대한 비평은 "의존 vs 활용"의 경계가
현실에서는 흐릿하다고 지적한다 — 코드 리뷰에 10분을 쓰면 활용이고
5분이면 의존인가? 에이전트가 생성한 500줄을 한 줄씩 이해하는 것이
직접 작성하는 것보다 오래 걸릴 수 있는데, 그 비용을 무시하면 "활용"은
구호에 그친다. 그리고
[intent-debt.md](../../agentic-coding/intent-debt.md)가 짚듯, 아무리
좋은 판단 기준을 세워도 "왜 이 결정을 내렸는가"라는 의도 자체는
기록해두지 않으면 에이전트도 인간도 복원할 수 없다 — 판단 기준은
필요조건이지 충분조건이 아니다.

## 종합: 이 저장소의 노트들이 가리키는 하나의 원칙

여러 각도에서 반복되는 것을 하나로 모으면 다음과 같다.

> **오류 비용이 낮고 검증이 즉시 가능한 작업은 자율에 맡기되, 그
> 자율의 경계는 프롬프트가 아니라 코드로 강제한다. 오류 비용이 높거나
> (돌이킬 수 없거나) 검증에 암묵지·조직 맥락이 필요한 작업은 사람이
> 명세와 최종 승인을 쥐고, "이 결과에 이름을 걸 수 있는가"를 매번
> 물을 수 있는 상태를 유지한다.**

이것이 이 저장소가 담고 있는, 아직 완결되지 않은 채로 축적되고 있는
판단 기준이다.

## 출처

- [agentic-coding/agent-responsibly.md](../../agentic-coding/agent-responsibly.md)
- [devops/google-sre-ai.md](../../devops/google-sre-ai.md)
- [agentic-coding/bottleneck-was-never-the-code.md](../../agentic-coding/bottleneck-was-never-the-code.md)
- [agentic-coding/verification-debt.md](../../agentic-coding/verification-debt.md)
- [agentic-coding/reviews-dead.md](../../agentic-coding/reviews-dead.md)
- [agentic-coding/multi-agent-orchestration-problems.md](../../agentic-coding/multi-agent-orchestration-problems.md)
- [agentic-coding/intent-debt.md](../../agentic-coding/intent-debt.md)
- [agentic-coding/cursor-railway-db-incident.md](../../agentic-coding/cursor-railway-db-incident.md)
- [agentic-coding/ai-agent-aws-bankruptcy.md](../../agentic-coding/ai-agent-aws-bankruptcy.md)
