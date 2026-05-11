# KaibanJS

<https://www.kaibanjs.com/>

<https://github.com/kaiban-ai/KaibanJS>

## 소개

KaibanJS는 JavaScript와 TypeScript로 다중 에이전트 AI 시스템을 구축하는 프레임워크다.
칸반(Kanban) 방법론을 AI 에이전트 워크플로우 관리에 적용해, 에이전트의 작업 진행 상황을 칸반 보드 형태로 시각화한다.
React, Vue, Angular, Next.js 등 주요 프레임워크와 호환되며 브라우저와 서버 양쪽에서 실행된다.

Andrew Ng, CrewAI, LangChain에서 영감을 받아 마이애미 기반 팀이 개발했다.
Microsoft, Tencent, Accenture, SAP, Salesforce 등의 개발자들이 사용하고 있다고 밝히고 있다.

## 핵심 개념

**에이전트(Agent)**

특정 역할(role), 목표(goal), 배경(background)을 가진 AI 전문가 단위다.
각 에이전트에 다른 LLM(OpenAI, Anthropic Claude, Google Gemini 등)을 독립적으로 할당할 수 있다.

**태스크(Task)**

에이전트가 수행할 구체적인 작업 단위다.
기대 출력(expected output)을 명시해 에이전트가 결과를 형식에 맞게 생성하도록 유도한다.

**팀(Team)**

에이전트와 태스크의 조직화된 집합이다.
팀 내에서 에이전트들이 협력하거나 순차적으로 작업을 수행한다.

## 사용법

```bash
npx kaibanjs@latest init
npm run kaiban
```

수동 설치:

```bash
npm install kaibanjs
```

```javascript
import { Agent, Task, Team } from "kaibanjs";

const researcher = new Agent({
  name: "Researcher",
  role: "Information Gatherer",
  goal: "Find relevant information",
  background: "Expert at web research",
  tools: [searchTool],
});

const task = new Task({
  description: "Research the latest AI trends",
  expectedOutput: "A concise summary of 3 key trends",
  agent: researcher,
});

const team = new Team({
  name: "Research Team",
  agents: [researcher],
  tasks: [task],
  env: { OPENAI_API_KEY: process.env.OPENAI_API_KEY },
});

const result = await team.start();
```

## 주요 기능

**칸반 보드 시각화**

에이전트의 태스크 진행 상태를 Trello·Jira 스타일로 실시간 표시한다.
`npm run kaiban` 명령으로 로컬 대시보드를 열어 작업 흐름을 모니터링한다.

**Redux 기반 상태 관리**

Redux에서 영감을 받은 아키텍처로 에이전트, 태스크, 워크플로우 상태를 일관되게 관리한다.
상태 변화를 구독하거나 미들웨어를 통해 확장할 수 있다.

**관찰성**

토큰 사용량 추적, 운영 비용 분석, 상태 변화 로깅을 내장한다.

**LangchainJS 도구 호환**

검색, 계산, 외부 API 호출 등 LangchainJS 생태계의 도구를 그대로 사용할 수 있다.

## 분석

### CrewAI의 JavaScript 포팅 이상의 무언가

KaibanJS는 Python 생태계의 CrewAI와 개념적으로 유사하지만 JavaScript 퍼스트라는 점이 다르다.
웹 개발자가 별도의 파이썬 백엔드 없이 AI 에이전트 시스템을 프론트엔드 또는 Node.js 환경에서 직접 구축할 수 있다.
이것은 AI 개발 진입 장벽을 낮추는 효과가 있다.
파이썬을 모르는 웹 개발자 인구가 에이전트 시스템 개발자로 전환될 수 있는 경로를 만든다.

### 칸반 은유의 적절성

칸반은 작업 흐름을 시각화하고 진행 중인 작업(WIP)을 제한해 흐름을 최적화하는 방법론이다.
에이전트 워크플로우에 이 은유를 적용하면 “어떤 에이전트가 무엇을 처리 중인가”를 직관적으로 파악할 수 있다.
특히 여러 에이전트가 병렬로 동작하거나 핸드오프가 복잡한 시스템에서 가시성이 높아진다.

### 다중 LLM 에이전트 설계

각 에이전트에 다른 LLM을 할당할 수 있다는 것은 비용과 성능의 균형을 세밀하게 조정할 수 있다는 의미다.
단순한 분류 작업에는 저렴한 모델을, 복잡한 추론에는 고성능 모델을 쓰는 혼합 전략이 가능하다.
이것은 단일 모델로 모든 작업을 처리하는 단순한 아키텍처보다 운영 비용을 낮출 수 있다.

## 비평

아직 성숙한 생태계라고 보기 어렵다.
공식 GitHub 리포지토리(kaibanjs/kaiban)가 404를 반환하는 상황은 문서화와 개발 투명성에 의문을 남긴다.
CrewAI, AutoGen, LangGraph 같은 기성 프레임워크들과 비교했을 때 커뮤니티 크기와 실전 검증 사례가 부족하다.

브라우저에서 실행된다는 것은 LLM API 키가 클라이언트에 노출될 수 있다는 보안 위험을 내포한다.
프로덕션 환경에서는 반드시 서버 사이드 프록시를 통해 API 호출을 라우팅해야 하지만, 이 점이 입문 문서에서 충분히 강조되는지 불분명하다.

Y Combinator 미지원을 직접 언급하는 것은 오히려 신뢰를 떨어뜨리는 역효과를 낸다.
지원 여부는 품질의 기준이 아니지만, 굳이 언급한다는 것은 이 비교를 의식하고 있다는 신호다.

## 인사이트

### JavaScript가 AI 개발의 주류 언어가 될 수 있다

현재 AI 개발 생태계는 파이썬이 사실상 독점하고 있다.
그러나 웹 개발자가 전 세계에서 가장 많은 개발자 집단이라는 사실은 변하지 않는다.
KaibanJS 같은 도구가 성숙해지면 에이전트 시스템 구축이 파이썬 전문가의 영역에서 JavaScript 개발자의 영역으로 확장된다.
이것은 AI 도구 개발에 참여할 수 있는 인구를 수십 배 늘리는 효과를 낼 수 있다.

### 관찰성이 에이전트 시스템의 핵심 요건이 된다

단일 LLM 호출은 입력과 출력을 로깅하면 충분하다.
다중 에이전트 시스템은 에이전트 간 메시지 흐름, 태스크 전환, 도구 호출, 토큰 사용량을 추적하는 훨씬 복잡한 관찰성 요건을 갖는다.
KaibanJS가 칸반 대시보드와 상태 추적을 핵심 기능으로 내세우는 것은 이 시장 요구를 정확히 포착한 것이다.
에이전트 프레임워크의 경쟁에서 기능보다 디버깅·모니터링 경험이 채택의 기준이 될 가능성이 높다.

### 추상화 계층의 적절한 위치

LangChain은 너무 낮은 추상화로 보일러플레이트가 많다는 비판을 받았다.
AutoGen은 복잡한 설정 구조 때문에 학습 곡선이 가파르다.
KaibanJS는 에이전트, 태스크, 팀이라는 세 가지 개념만으로 시스템을 구성하는 단순함을 택했다.
이 선택이 단순한 사용 사례에서는 장점이지만, 복잡한 에이전트 상호작용(반복, 조건 분기, 오류 복구)을 표현할 때 추상화가 걸림돌이 될 수 있다.
프레임워크 성숙도는 결국 이 엣지 케이스들을 얼마나 우아하게 처리하는지로 판가름된다.
