# Spec-Driven Development

## 개요

Spec-Driven Development(SDD)는 AI와 함께 소프트웨어를 개발하는 새로운 접근
방식이다. 기존의 “vibe-coding” 문제(AI가 겉보기엔 괜찮아 보이지만 실제로는
제대로 작동하지 않는 코드를 생성하는 현상)를 해결하기 위해 등장했다.
[병목은 결코 코드가 아니었다](bottleneck-was-never-the-code.md)가 지적하듯,
코드 작성 비용이 0에 수렴하면 병목은 “무엇을 만들지를 정밀하게 정의하는”
명세 단계로 이동한다.
SDD는 이 진단을 워크플로 형태로 구조화한 시도다.

### 핵심 개념

Spec-Driven Development에서는 **명세(specification)가 코드의 동작 방식에 대한
계약(contract)이자 도구와 AI 에이전트의 신뢰할 수 있는 단일 정보원(source of
truth)** 이 된다. 기존 방식과 달리 명세를 임시 문서로 취급하지 않고, 실제 구현을
직접 생성하는 “실행 가능한” 문서로 다룬다.
그러나 [충분히 상세한 명세는 코드다](sufficiently-detailed-spec-is-code.md)가
지적하듯, 실행 가능할 만큼 정밀해진 명세는 결국 코드와 같은 정밀성을 요구한다.
SDD는 “명세가 코드를 대체한다”는 약속이 아니라
“명세와 구현 사이의 의존성 방향을 강제한다”는 약속으로 읽어야 한다.

### 작동 방식

구조화된 다단계 프로세스를 따른다:

1. **원칙 수립(Principles)** - 프로젝트 거버넌스와 개발 가이드라인 정의
2. **요구사항 명세(Specify)** - 무엇을 만들지(what) 설명 (어떻게 만들지(how)가
   아님)
3. **구현 계획(Plan)** - 선택한 기술 스택으로 기술 전략 수립
4. **작업 생성(Tasks)** - 계획을 실행 가능한 항목으로 분해
5. **구현(Implement)** - 계획에 따라 기능 구현

### 주요 이점

- **기술 독립성**: 다양한 기술 스택과 프로그래밍 언어에서 작동
- **구조화된 개발**: 다단계 개선 프로세스로 모호한 프롬프트 기반 생성 방지
- **예측 가능한 결과**: 즉흥적인 개발 대신 제품 시나리오와 문서화된 요구사항에
  집중
- **엔터프라이즈 호환**: 조직의 제약사항과 기존 디자인 시스템 지원

[카카오페이의 Spec-kit 실전기](kakaopay-spec-kit-practice.md)는 SDD의
이런 약속이 실제 팀에서 어떻게 작동하는지를 보여준다 — 일관성은 향상되지만
간단한 작업에서는 오버엔지니어링이 되며 토큰 소모도 크다.
한편 [AI 오케스트레이터라는 환상](ai-orchestrator-illusion.md)은 더 근본적인
반론을 제기한다: 언어는 의도를 완전히 표현하지 못하고 AI는 그 빈틈을
확률적으로 채우므로, 스펙을 쓰는 행위가 구현을 통한 컨텍스트 축적을
대체할 수 없다는 것이다.

## 참고 자료

[Spec-driven development with AI: Get started with a new open source toolkit - The GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)

[Diving Into Spec-Driven Development With GitHub Spec Kit - Microsoft for Developers](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)

## Spec Kit

> 💫 Toolkit to help you get started with Spec-Driven Development

<https://github.com/github/spec-kit>

## SDD Flow - AI Coding Assistant Framework

<https://github.com/Ataden/SDD_Flow>

## cc-sdd: Spec-driven development for your team's workflow

<https://github.com/gotalab/cc-sdd>
