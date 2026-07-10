# 에이전트형 코딩의 실패/함정 패턴

주제: 에이전트에게 코드 작성과 의사결정을 맡기는 작업에서 실제로 어떤 종류의
실패가 반복적으로 보고되는지, 그리고 그 실패가 “에이전트를 잘못 써서”인지
“구조적으로 피하기 어려운 함정”인지를 구별한다. 자율성을 높일수록 검증이
느슨해져서 생기는 사고와, 스펙/TDD가 에이전트 시대에 어떤 역할을 하는지를
같이 다룬다. 목표는 “어디까지 자율을 주고 어디서 사람이 개입해야 하는가”에
대한 이 저장소 노트들의 공통된 판단 기준을 찾는 것이다.

## 개요

이 저장소의 노트들을 종합하면, 에이전트형 코딩의 실패는 크게 두 갈래로
갈린다. 하나는 [돌이킬 수 없는 사고](irreversible-incidents.md)처럼 눈에
보이는 사건이고, 다른 하나는 [자율성이 검증을 잠식하는
구조](autonomy-erodes-verification.md)처럼 서서히 쌓여 사고 전까지는 보이지
않는 부채다. 두 갈래 모두 같은 원인으로 수렴한다 — 에이전트는 권한이 있으면
사용하고, 맥락과 사회적 규범은 명시적으로 인코딩하지 않으면 존재하지 않는
것과 같다는 것이다. [스펙/TDD 같은 구조적 처방](spec-and-tdd-as-guardrails.md)은
이 문제에 실질적으로 대응하지만 만능은 아니며, 처방 자체가 새로운 병목과
한계를 낳는다. 자율성을 여러 에이전트로 확장하면
[멀티 에이전트 오케스트레이션 특유의 실패](multi-agent-orchestration-failures.md)가
추가로 발생한다. 마지막으로 이 저장소의 여러 노트가 수렴하는 지점은
[어디까지 자율을 주고 어디서 사람이 개입해야 하는가](where-to-draw-the-line.md)에
대한 공통 판단 기준이다 — “이 장애를 소유할 수 있는가”라는 하나의 질문으로
수렴하는 경향이 있다.

## 하위 주제

- [돌이킬 수 없는 사고들](irreversible-incidents.md) — 프로덕션 DB 삭제,
  AWS 비용 폭주, 아마존 연쇄 장애 등 실제로 보고된 구체적 사건과 그 공통
  패턴
- [자율성이 검증을 잠식하는 구조](autonomy-erodes-verification.md) — 왜
  에이전트를 더 많이 쓸수록 그것을 감독할 능력 자체가 줄어드는가 (검증
  부채, 감독의 역설, 검증 에이전트가 검증 대상과 공유하는 편향)
- [스펙/TDD가 하는 일과 못 하는 일](spec-and-tdd-as-guardrails.md) — SDD와
  TDD가 실제로 해결하는 문제와, 해결하지 못하거나 새로 만들어내는 문제
- [멀티 에이전트 오케스트레이션 특유의 실패](multi-agent-orchestration-failures.md) —
  에이전트가 여러 개로 늘어날 때만 발생하는 구조적 실패 (맥락 붕괴, 유령
  위임, 검증 오류)
- [어디까지 자율을 주고 어디서 개입해야 하는가](where-to-draw-the-line.md) —
  이 저장소 노트들이 공통으로 수렴하는 판단 기준과 실행 프레임워크

## 출처

- [agentic-coding/cursor-railway-db-incident.md](../../agentic-coding/cursor-railway-db-incident.md)
- [agentic-coding/ai-agent-aws-bankruptcy.md](../../agentic-coding/ai-agent-aws-bankruptcy.md)
- [ai/amazon-senior-engineer-signoff-ai-changes-2026.md](../../ai/amazon-senior-engineer-signoff-ai-changes-2026.md)
- [security/vibe-coding-horror-story.md](../../security/vibe-coding-horror-story.md)
- [agentic-coding/agentic-coding-is-a-trap.md](../../agentic-coding/agentic-coding-is-a-trap.md)
- [agentic-coding/ai-coding-is-gambling.md](../../agentic-coding/ai-coding-is-gambling.md)
- [agentic-coding/verification-debt.md](../../agentic-coding/verification-debt.md)
- [agentic-coding/ai-orchestrator-illusion.md](../../agentic-coding/ai-orchestrator-illusion.md)
- [agentic-coding/agent-responsibly.md](../../agentic-coding/agent-responsibly.md)
- [agentic-coding/spec-driven-development.md](../../agentic-coding/spec-driven-development.md)
- [agentic-coding/sufficiently-detailed-spec-is-code.md](../../agentic-coding/sufficiently-detailed-spec-is-code.md)
- [agentic-coding/tdd-in-ai-era.md](../../agentic-coding/tdd-in-ai-era.md)
- [agentic-coding/kakaopay-spec-kit-practice.md](../../agentic-coding/kakaopay-spec-kit-practice.md)
- [agentic-coding/bottleneck-was-never-the-code.md](../../agentic-coding/bottleneck-was-never-the-code.md)
- [agentic-coding/intent-debt.md](../../agentic-coding/intent-debt.md)
- [agentic-coding/multi-agent-orchestration-problems.md](../../agentic-coding/multi-agent-orchestration-problems.md)
- [agentic-coding/agentic-software-levels.md](../../agentic-coding/agentic-software-levels.md)
- [agentic-coding/vibe-coding-cult.md](../../agentic-coding/vibe-coding-cult.md)
- [devops/google-sre-ai.md](../../devops/google-sre-ai.md)
- [agentic-coding/reviews-dead.md](../../agentic-coding/reviews-dead.md)
- [agentic-coding/swe-bench-pro-signal-noise.md](../../agentic-coding/swe-bench-pro-signal-noise.md)
- [rust/rewriting-bun-in-rust.md](../../rust/rewriting-bun-in-rust.md)
