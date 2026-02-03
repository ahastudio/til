# Karpathy-Inspired Claude Code Guidelines

Tweet:
<https://twitter.com/jiayuan_jy/status/2015998216517583211>

GitHub Repository:
<https://github.com/forrestchang/andrej-karpathy-skills>

[Karpathy의 Claude Coding Notes](./karpathy-claude-coding-notes.md)에서
지적한 문제들을 해결하기 위한 실용적인 가이드라인.

## Karpathy가 지적한 세 가지 함정

### 1. 검증 없는 가정 (Unexamined Assumptions)

모델이 잘못된 가정을 하고 확인 없이 진행한다.
혼란을 관리하지 않고, 명확화를 요청하지 않으며,
불일치를 표면화하지 않고, 트레이드오프를 제시하지 않는다.

### 2. 과잉 복잡화 (Overcomplication)

코드와 API를 과도하게 복잡하게 만든다.
추상화를 부풀리고, 죽은 코드를 정리하지 않는다.
100줄이면 충분한 것을 1000줄로 구현한다.

### 3. 직교적 수정 (Orthogonal Modifications)

작업과 무관한 코드나 주석을 변경하거나 삭제한다.
충분히 이해하지 못한 코드를 부수 효과로 건드린다.

## 네 가지 해결 원칙

| 원칙                 | 해결하는 문제                       |
|----------------------|-------------------------------------|
| Think Before Coding  | 잘못된 가정, 숨겨진 혼란, 트레이드오프 누락 |
| Simplicity First     | 과잉 복잡화, 추상화 부풀리기         |
| Surgical Changes     | 직교적 수정, 불필요한 코드 변경      |
| Goal-Driven Execution | 테스트 우선, 검증 가능한 성공 기준   |

### 원칙 1: Think Before Coding (코딩 전에 생각하기)

- 가정을 명시적으로 밝힌다
- 불확실하면 질문한다
- 여러 해석이 있으면 모두 제시한다
- 필요하면 반박한다
- 혼란스러우면 멈추고 명확화를 요청한다

### 원칙 2: Simplicity First (단순함 우선)

- 문제를 해결하는 최소한의 코드만 작성한다
- 추측성 기능을 추가하지 않는다
- 일회용 추상화를 만들지 않는다
- 요청받지 않은 유연성을 넣지 않는다
- 발생할 수 없는 시나리오에 대한 에러 처리를 하지 않는다

**리트머스 테스트:** 시니어 엔지니어가 이 코드를 보고
"과잉 복잡화"라고 할까?

### 원칙 3: Surgical Changes (외과적 변경)

- 필요한 코드만 건드린다
- 인접 코드를 개선하지 않는다
- 포맷팅을 바꾸지 않는다
- 기존 스타일을 따른다
- 내 변경으로 고아가 된 코드만 제거한다
- 기존의 죽은 코드는 요청받지 않으면 삭제하지 않는다

### 원칙 4: Goal-Driven Execution (목표 기반 실행)

Karpathy의 핵심 통찰:

> "LLM은 특정 목표를 충족할 때까지 루프를 도는 데 뛰어나다...
> 무엇을 하라고 지시하지 말고, 성공 기준을 주고 지켜봐라."

- 명령형 지시를 선언형 목표로 변환한다
- 구현 전에 검증 가능한 성공 기준을 정의한다
- 명시적 검증 단계를 설정한다

## 적용 방법

**플러그인 방식** (권장):

```bash
claude plugins add https://github.com/forrestchang/andrej-karpathy-skills
```

**프로젝트별 방식**:

```bash
curl -o CLAUDE.md \
  https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md
```

## 성공 지표

- 불필요한 diff 변경이 줄어든다
- 과잉 엔지니어링으로 인한 재작성이 감소한다
- 구현 전에 명확화 질문을 한다
- PR이 최소화되고 집중된다

## 설계 철학

이 가이드라인은 **속도보다 신중함**을 우선한다.
단, 사소한 작업에는 판단을 적용한다.

## 관련 문서

- [Karpathy's Claude Coding Notes](./karpathy-claude-coding-notes.md)
- [Vibe Coding](./vibe-coding.md)
