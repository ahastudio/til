# Spec-Driven Development

## 개요

Spec-Driven Development(SDD)는 AI와 함께 소프트웨어를 개발하는 새로운 접근 방식이다. 기존의 "vibe-coding" 문제(AI가 겉보기엔 괜찮아 보이지만 실제로는 제대로 작동하지 않는 코드를 생성하는 현상)를 해결하기 위해 등장했다.

### 핵심 개념

Spec-Driven Development에서는 **명세(specification)가 코드의 동작 방식에 대한 계약(contract)이자 도구와 AI 에이전트의 신뢰할 수 있는 단일 정보원(source of truth)** 이 된다. 기존 방식과 달리 명세를 임시 문서로 취급하지 않고, 실제 구현을 직접 생성하는 "실행 가능한" 문서로 다룬다.

### 작동 방식

구조화된 다단계 프로세스를 따른다:

1. **원칙 수립(Principles)** - 프로젝트 거버넌스와 개발 가이드라인 정의
2. **요구사항 명세(Specify)** - 무엇을 만들지(what) 설명 (어떻게 만들지(how)가 아님)
3. **구현 계획(Plan)** - 선택한 기술 스택으로 기술 전략 수립
4. **작업 생성(Tasks)** - 계획을 실행 가능한 항목으로 분해
5. **구현(Implement)** - 계획에 따라 기능 구현

### 주요 이점

- **기술 독립성**: 다양한 기술 스택과 프로그래밍 언어에서 작동
- **구조화된 개발**: 다단계 개선 프로세스로 모호한 프롬프트 기반 생성 방지
- **예측 가능한 결과**: 즉흥적인 개발 대신 제품 시나리오와 문서화된 요구사항에 집중
- **엔터프라이즈 호환**: 조직의 제약사항과 기존 디자인 시스템 지원

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
