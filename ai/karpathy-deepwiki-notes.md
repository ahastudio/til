# Karpathy's DeepWiki Notes

Andrej Karpathy의 트윗 (2026년 2월 12일):
<https://twitter.com/karpathy/status/2021633574089416993>

DeepWiki와 소프트웨어의 유동성(malleability)에 대한 글.

## DeepWiki

<https://deepwiki.com>

GitHub 저장소를 자동으로 위키 페이지로 변환하고, 코드에 대해 Q&A할 수 있는
서비스. URL에서 `github`을 `deepwiki`로 바꾸면 바로 사용 가능하다. MCP 서버도
제공해서 에이전트에 통합할 수 있다.

## 인사이트

### 코드가 진실의 원천이다

라이브러리 공식 문서는 종종 부실하고 오래된다. **코드 자체가 진실의 원천(source
of truth)**이며, LLM이 코드를 점점 더 잘 이해하게 되면서 문서 대신 코드에 직접
질문하는 것이 더 정확하다.

### 에이전트가 정보를 소비하게 하라

사람이 코드를 읽고 이해해서 구현하는 것보다 **에이전트에게 DeepWiki MCP 접근
권한을 주는 것**이 훨씬 강력하다. 사람은 정보의 직접 소비자가 아니라 에이전트의
감독자가 되는 것이 레버리지를 극대화한다.

### 소프트웨어는 유동적이 된다

에이전트 이전에는 거대한 라이브러리에서 특정 기능만 뜯어내는 것이 시간적으로
비경제적이었다. 이제 그것이 가능하고 경제적이다. **이전에 불가능했던 선택지가
새로 생긴 것.**

torchao에서 fp8 훈련을 추출한 사례: 에이전트가 5분 만에 **150줄의 자체 완결형
코드**를 만들었고, 원본 라이브러리보다 3% 빨랐다.

### 단순한 코드가 이긴다

라이브러리의 범용 코드는 다양한 케이스를 커버하느라 불필요하게 복잡해진다. 특정
용도로 추출하면 본질만 남아서 **더 단순하고 오히려 더 빠르다**. torch.compile
같은 도구도 단순한 코드를 더 잘 최적화하는 경향이 있다.

### 에이전트는 암묵지를 추출한다

사람이 놓치기 쉬운 미묘한 구현 디테일을 에이전트가 체계적으로 발견한다: 수치
트릭, dtype 처리, autocast 상호작용 등. 문서화하기 어려운 **암묵지(tacit
knowledge)**를 코드에서 직접 뽑아내는 강력한 방법이다.

### "박테리아 코드"로 설계하라

에이전트 시대의 코드 설계 원칙:

- **덜 엉킨**(less tangled) 코드
- **자체 완결형**(self-contained) 코드
- **의존성 없는**(dependency-free) 코드
- **상태 없는**(stateless) 코드

다른 프로젝트에서 에이전트가 쉽게 뜯어갈 수 있도록 결합도를 낮추고 자체 완결성을
높이는 것이 새로운 설계 원칙이 된다.

### 라이브러리의 종말?

> "Libraries are over, LLMs are the new compiler."

거대한 모놀리식 라이브러리를 통째로 의존하는 대신, 에이전트로 필요한 부분만
추출하는 방식이 가능해졌다. 프로젝트에 정말 100MB의 의존성이 필요한가?

## 실전 워크플로우

**DeepWiki MCP + GitHub CLI** 조합으로 어떤 GitHub 저장소에서든 특정 기능을
추출할 수 있다.

카파시의 프롬프트 예시:

> "DeepWiki MCP와 GitHub CLI로 torchao의 fp8 훈련 구현을 분석하라. 기능을
> '뜯어내서' 동일한 API의 자체 완결형 nanochat/fp8.py를 구현하라."

## 관련 문서

- [Karpathy's Claude Coding Notes](./karpathy-claude-coding-notes.md)
- [Karpathy-Inspired Claude Guidelines](./karpathy-inspired-claude-guidelines.md)
- [Vibe Coding](./vibe-coding.md)
- [Claude Code](../claude/claude-code.md)
