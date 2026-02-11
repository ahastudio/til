# Karpathy's DeepWiki Notes

Andrej Karpathy의 트윗 (2026년 2월 10일):
<https://twitter.com/karpathy/status/2021633574089416993>

DeepWiki와 소프트웨어의 유동성(malleability)에 대한 글.

## DeepWiki 활용의 세 단계

### 1단계: 코드베이스 위키 & Q&A

[DeepWiki](https://deepwiki.com)는 GitHub 저장소를
자동으로 위키 페이지로 변환한다.
URL에서 `github`을 `deepwiki`로 바꾸면 바로 사용 가능하다.

```
github.com/karpathy/nanochat
→ deepwiki.com/karpathy/nanochat
```

라이브러리 공식 문서는 종종 부실하고 오래되지만,
**코드 자체가 진실의 원천(source of truth)**이다.
LLM이 코드를 점점 더 잘 이해하게 되면서
DeepWiki로 코드에 직접 질문하는 것이 효과적이다.

### 2단계: MCP를 통한 에이전트 통합

사람이 직접 정보를 소비하는 것보다
**에이전트에게 DeepWiki MCP 접근 권한을 주는 것**이
훨씬 강력하다.

### 3단계: 기능 추출 (Rip Out)

DeepWiki MCP + GitHub CLI 조합으로
거대한 라이브러리에서 **필요한 기능만 정확히 추출**할 수 있다.

## 사례: torchao fp8 훈련

카파시는 torchao의 fp8 훈련이
불필요하게 복잡하다고 의심했다.
실제로는 `Linear`에 캐스트 몇 번과
`torch._scaled_mm` 호출 3번이면 될 것 같았다.

에이전트에게 이렇게 지시했다:

> "DeepWiki MCP와 GitHub CLI로
> torchao의 fp8 훈련 구현을 분석하라.
> 기능을 '뜯어내서' 동일한 API의
> 자체 완결형 nanochat/fp8.py를 구현하라."

### 결과

- **150줄**의 깔끔한 코드로 즉시 동작
- 동등한 결과를 증명하는 테스트 포함
- torchao 의존성 제거 성공
- 오히려 **3% 더 빠름**
  (torch.compile 내부 동작과 관련된 것으로 추정)
- 에이전트가 사람이 놓치기 쉬운 **미묘한 구현 디테일**을
  모두 찾아냄:
  수치 트릭, dtype 처리, autocast,
  meta device, torch.compile 상호작용

이 구현이 nanochat의 기본 fp8 훈련이 되었다.

## 핵심 인사이트

### 소프트웨어의 유동성

에이전트 덕분에 소프트웨어가 훨씬
**유동적(fluid)이고 가변적(malleable)**이 되었다.
예전에는 시간이 너무 많이 들어 불가능했던
기능 추출이 이제 경제적으로 가능해졌다.

### "박테리아 코드" (Bacterial Code)

이 워크플로우를 적극 장려하는 방향으로
소프트웨어를 설계해야 한다:

- 덜 엉킨(less tangled) 코드
- 자체 완결형(self-contained) 코드
- 의존성 없는(dependency-free) 코드
- 상태 없는(stateless) 코드
- 저장소에서 쉽게 뜯어낼 수 있는 코드

### 라이브러리의 종말?

> "Libraries are over, LLMs are the new compiler."

거대한 모놀리식 라이브러리를 통째로 의존성에 넣는 대신,
에이전트로 필요한 부분만 추출하는 방식이 가능해졌다.
프로젝트에 정말 100MB의 의존성이 필요한가?

## 배울 점

### 1. 문서보다 코드에 직접 질문하라

공식 문서는 항상 코드보다 뒤처진다.
DeepWiki처럼 코드 자체를 이해하는 도구가
점점 더 유용해질 것이다.

### 2. 에이전트를 정보의 중간 소비자로 활용하라

사람이 정보를 읽고 코드를 짜는 것보다
에이전트가 정보를 읽고 코드를 짜게 하는 것이
더 강력하다. MCP를 통한 도구 통합이 핵심이다.

### 3. 의존성을 재고하라

모든 라이브러리 의존성에 대해 질문하라:
정말 전체가 필요한가,
아니면 특정 기능만 추출할 수 있는가?

### 4. 추출 가능한 코드를 작성하라

미래의 코드는 다른 프로젝트에서
에이전트가 쉽게 뜯어갈 수 있도록 설계해야 한다.
결합도를 낮추고 자체 완결성을 높이는 것이
새로운 설계 원칙이 된다.

### 5. 에이전트는 미묘한 디테일을 찾는다

사람이 놓치기 쉬운 구현 세부사항을
에이전트가 체계적으로 발견한다.
이는 문서화하기 어려운 암묵지(tacit knowledge)를
추출하는 강력한 방법이다.

## 관련 문서

- [Karpathy's Claude Coding Notes](./karpathy-claude-coding-notes.md)
- [Karpathy-Inspired Claude Guidelines](./karpathy-inspired-claude-guidelines.md)
- [Vibe Coding](./vibe-coding.md)
- [Claude Code](../claude/claude-code.md)
