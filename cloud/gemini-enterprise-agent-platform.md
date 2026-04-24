# Gemini Enterprise Agent Platform: Google Cloud의 AI 에이전트 거버넌스 스택

원문: <https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform>

[GeekNews 댓글](https://news.hada.io/topic?id=28810)

## 요약

Google Cloud가 Cloud Next '26(2026년 4월 23일)에서
Gemini Enterprise Agent Platform을 발표했다.
AI 에이전트를 빌드·확장·거버넌스·최적화하는 통합 플랫폼으로,
Vertex AI의 모든 서비스와 로드맵을 이 플랫폼으로 통합하겠다고 선언했다.

거버넌스 레이어가 핵심이다.
에이전트 플릿을 엔지니어링 조직처럼 관리한다는 개념 하에,
에이전트 신원 부여, 접근 제어, 정책 집행, 행위 모니터링, 감사 기능을 제공한다.
거버넌스 스택은 Agent Identity, Agent Registry, Agent Gateway,
이상 및 위협 탐지, Agent Security Dashboard의 5계층으로 구성된다.

플랫폼은 거버넌스 외에도 개발(Agent ADK, Agent Studio, Agent Garden),
실행(Agent Runtime, Agent Sandbox, Agent Memory Bank, Agent Sessions),
최적화(Agent Simulation, Agent Evaluation, Agent Observability, Agent Optimizer)
기능을 포함한다.
현재 Burns & McDonnell, Comcast, PayPal, L'Oréal 등
주요 기업이 이미 에이전트 플랫폼을 활용 중이라고 밝혔다.

모델 가든을 통해 Gemini 3.1 Pro, Gemma 4와 함께
Anthropic Claude Opus/Sonnet/Haiku도 지원한다.

## 분석

### 5계층 거버넌스 스택

```
[Agent Security Dashboard]  ← 통합 가시성
[Anomaly & Threat Detection] ← 행위 모니터링
[Agent Gateway]              ← 정책 집행 레이어
[Agent Registry]             ← 승인된 에이전트 카탈로그
[Agent Identity]             ← 암호화 신원
```

각 계층의 역할:

- **Agent Identity**: 에이전트마다 고유한 암호화 ID를 부여하여
  최소 권한 원칙에 기반한 접근 제어와 감사 추적을 가능하게 한다.

- **Agent Registry**: 조직 내 모든 에이전트, MCP 도구, 엔드포인트의
  중앙 카탈로그. 사내 npm 레포지터리처럼 플랫폼 팀이 승인한
  에셋만 프로덕션에서 사용할 수 있게 통제한다.

- **Agent Gateway**: 자연어로 작성된 보안 정책을 모든 에이전트에
  즉시 적용하는 “에이전트 생태계의 항공 교통 관제소”.
  MCP, A2A 같은 에이전트 프로토콜을 이해하고,
  Model Armor로 프롬프트 인젝션과 데이터 유출을 방어한다.

- **이상 및 위협 탐지**: 통계 기준선으로 행위 이상을 탐지하고,
  별도의 LLM 판사(LLM-as-a-judge)가 추론 패턴을 감사한다.
  리버스 셸, 악성 IP 연결 등 위협 활동도 실시간 탐지한다.

- **Agent Security Dashboard**: Security Command Center 기반의
  통합 시각화. 에이전트-모델 관계 매핑, 취약점 스캔,
  계층 간 신호 상관관계를 제공한다.

### 에이전트를 “조직원”처럼 관리한다는 발상

Google Cloud의 거버넌스 프레임워크는 에이전트에 인간 직원에 준하는
신원, 권한, 감사 체계를 부여한다.
이것은 단순한 기술적 추상화가 아니다.
에이전트가 기업 시스템에 접근하고, 외부 서비스를 호출하고,
다른 에이전트를 오케스트레이션하는 세계에서
“이 행동을 한 에이전트가 누구인가”를 추적하는 것은
법적 책임, 규정 준수, 사고 대응의 기반이 된다.
IAM이 클라우드 리소스에 적용한 것을 에이전트에 적용하는 논리다.

### Vertex AI의 완전한 흡수

“모든 Vertex AI 서비스와 로드맵이 Agent Platform을 통해 제공될 것”이라는 선언은
Google Cloud의 AI 전략 전환점을 의미한다.
Vertex AI는 더 이상 독립 서비스가 아니라 Agent Platform의 하부 레이어가 된다.
이는 클라우드 AI 서비스의 단위가 “모델”에서 “에이전트”로 이동했음을
플랫폼 아키텍처 수준에서 공식화한 것이다.

## 비평

### 강점

거버넌스 레이어를 5계층으로 구조화하고, 각 계층의 역할을 명확히 분리한 설계는
엔터프라이즈 보안 팀이 이해하고 채택하기 쉬운 프레임워크를 제공한다.
특히 자연어 정책을 Agent Gateway를 통해 전체 에이전트 플릿에 즉시 적용한다는
개념은 정책 관리의 마찰을 크게 줄이는 실용적 접근이다.
LLM-as-a-judge로 에이전트의 추론 패턴 자체를 감사한다는 아이디어도 참신하다.

### 약점

발표 수준에서 구체적인 구현 세부사항과 가격 정보가 공개되지 않았다.
“자연어 정책이 즉시 적용된다”는 주장은 매력적이지만,
자연어의 모호성이 실제 보안 정책에서 어떻게 처리되는지,
정책 충돌은 어떻게 해소되는지에 대한 설명이 없다.
또한 Google Cloud의 에이전트 생태계에 종속(vendor lock-in)되는 위험도 존재한다.
Agent Identity, Agent Registry가 Google Cloud 인프라에 종속된다면
멀티클라우드 에이전트 환경을 구축하는 것이 어려워진다.

## 인사이트

### 에이전트 거버넌스는 IAM의 진화다

클라우드 시대 초기에 “누가 어떤 리소스에 접근할 수 있는가”를 정의하는
IAM(Identity and Access Management)은 보안의 중심축이 되었다.
에이전트 시대에 같은 질문이 반복된다:
“어떤 에이전트가 어떤 도구를, 어떤 조건에서 사용할 수 있는가.”
Google Cloud의 거버넌스 스택은 IAM이 수행한 역할을 에이전트 레이어에서 재수행한다.
이 유사성은 우연이 아니다.
에이전트는 사실상 자율적으로 행동하는 새로운 종류의 “주체(principal)”이며,
모든 보안 아키텍처는 새로운 주체가 등장할 때마다 재설계 압력을 받는다.

흥미로운 점은 에이전트 거버넌스가 단순히 IAM을 확장하는 것이 아니라
새로운 차원을 추가한다는 것이다.
인간 사용자는 의도를 갖고 행동하며 그 의도를 언어로 설명할 수 있지만,
에이전트의 “추론 패턴”은 외부에서 완전히 관찰하기 어렵다.
LLM-as-a-judge로 에이전트의 추론을 감사한다는 접근은
이 문제에 대한 초기 시도이지만, 감사자 자신이 LLM이라는 재귀적 문제를 내포한다.
“누가 감시자를 감시하는가”라는 고전적 질문이 AI 거버넌스에서도 되풀이된다.

### 에이전트 레지스트리는 기업 AI의 새로운 패키지 관리자다

Agent Registry를 “사내 npm 레포지터리”에 비유한 것은 정확한 유추다.
npm이 JavaScript 생태계에서 “신뢰할 수 있는 패키지”의 관문 역할을 하듯,
Agent Registry는 기업 내에서 “승인된 에이전트와 도구”의 관문이 된다.
이 유추는 기회와 위험을 동시에 시사한다.
npm이 공급망 공격의 표적이 된 것처럼,
Agent Registry도 승인된 에이전트로 위장한 악성 에이전트의 잠재적 표적이 된다.
에이전트가 다른 에이전트를 실행하고 도구를 호출하는 체인에서
하나의 타협된 에이전트가 전체 워크플로를 오염시킬 수 있다.
에이전트 공급망 보안(agent supply chain security)은
소프트웨어 공급망 보안과 같은 수준의 주의가 필요한 문제가 될 것이다.
