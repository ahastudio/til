# One Human + One Agent = One Browser

1인간 + 1에이전트가 수백 에이전트 스웜을 압도한 실험.

원문: <https://emsh.cat/one-human-one-agent-one-browser/>

## 실험 개요

LLM 기반 에이전트 하나와 인간 하나가 협업하여
**72시간 내에 20,000줄의 Rust 코드로 브라우저를 구축**했다.

- HTML과 CSS를 렌더링하는 기능적인 브라우저
- 서드파티 라이브러리 의존성 없음 (Cargo 의존성 제로)
- Linux, macOS, Windows 크로스 플랫폼 지원
- 스크롤, 뒤로가기 버튼, 회귀 테스트까지 구현

> "It's not great, I wouldn't even say it's good, but it works."
> (훌륭하진 않고, 좋다고도 못하겠지만, **작동한다**.)

## 대조군: Cursor의 에이전트 스웜 실험

Cursor는 GPT-5.2 기반으로 **수백 개의 에이전트**를 수주간 돌려
브라우저를 만드는 실험을 진행했다.

| 항목       | One Human + One Agent | Cursor 에이전트 스웜 |
|------------|:---------------------:|:--------------------:|
| 에이전트   | 1개                   | 수백 개              |
| 기간       | 72시간                | 수주                 |
| 작동 여부  | 작동함                | 미검증 (빌드 실패)   |
| 비용       | 낮음                  | 매우 높음            |

Cursor는 "의미 있는 진전"이라 주장했지만,
**컴파일 가능한 바이너리나 렌더링 결과를 제시하지 못했다**.

## 핵심 원칙 → 결과 연결

### 1. 인간의 뇌가 최고의 조정자다

> "I have something even better: a human brain! It is usually better than
> any machine at coordinating and thinking through things."

| 원칙                              | 결과                               |
|-----------------------------------|----------------------------------- |
| 인간이 전략적 의사결정을 주도     | 에이전트가 방향 잃지 않고 진행     |
| 에이전트는 실행에 집중            | 불필요한 조정 오버헤드 제거        |
| 복잡한 계층 구조 배제             | 72시간 내 완성                     |

### 2. 병렬화는 조정 비용을 동반한다

| 원칙                              | 결과                               |
|-----------------------------------|----------------------------------- |
| 에이전트 수 증가 → 충돌 증가      | Cursor: "minimal conflicts" 주장   |
| 인간 조정자 부재 시 품질 저하     | 빌드조차 안 되는 결과물            |
| 1:1 협업은 조정 비용 제로         | 작동하는 결과물                    |

### 3. 작동하는 것이 먼저다

| 원칙                              | 결과                               |
|-----------------------------------|----------------------------------- |
| "완벽한" 대신 "작동하는"          | 실제 렌더링 가능한 브라우저        |
| 점진적 기능 추가                  | 스크롤, 뒤로가기 등 순차 구현      |
| 회귀 테스트 즉시 도입             | 안정성 확보                        |

## 즉시 적용 가능한 교훈

### 에이전트 개수보다 인간의 판단력이 중요하다

> "Can we scale autonomous coding by throwing more agents at a problem?"
> → **Probably not.**

에이전트를 늘리기 전에 **인간 조정자의 역할을 명확히** 해야 한다.
스웜 방식은 비용만 높이고 결과를 보장하지 않는다.

### 검증 가능한 결과물을 빠르게 만들어라

72시간 안에 "작동하는" 결과물을 만든 것이 핵심이다.
수주간 "진전"을 주장하면서 **작동 증거를 못 내면 실패**다.

### 단순한 구조가 이긴다

- Planner, Worker, Judge 같은 복잡한 역할 분리 불필요
- 1인간 + 1에이전트의 **단순한 루프**가 더 효과적
- 조정 오버헤드가 없으면 속도가 나온다

## 결론

> "If one person with one agent can produce equal or better results
> than 'hundreds of agents for weeks', then the answer to the question:
> 'Can we scale autonomous coding by throwing more agents at a problem?'
> probably has a more pessimistic answer than some expected."

**에이전트 스케일링의 정답은 수량이 아니라 인간과의 협업 품질이다.**

## 관련 문서

- [Karpathy's Claude Coding Notes](./karpathy-claude-coding-notes.md)
- [Vibe Coding](./vibe-coding.md)
- [Agent](./agent.md)
