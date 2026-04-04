# awesome-llm-apps

> A curated collection of awesome LLM apps built with RAG and
> AI agents.

<https://github.com/Shubhamsaboo/awesome-llm-apps>

## 개요

RAG, AI 에이전트, 멀티 에이전트 팀, MCP, 음성 에이전트
등을 활용한 LLM 앱 모음.
OpenAI, Anthropic, Google, xAI, Qwen, Llama 등
다양한 모델을 사용한 실용적인 구현 예제를 제공한다.
GitHub 스타 98.4k 이상으로 커뮤니티 검증을 받았다.
Apache-2.0 라이선스.

## 저장소 구조

```
awesome-llm-apps/
├── starter_ai_agents/       # 입문 에이전트 (16개)
├── advanced_ai_agents/
│   ├── single_agent_apps/   # 고급 단일 에이전트 (16개)
│   ├── multi_agent_apps/    # 멀티 에이전트 (15개)
│   │   └── agent_teams/     # 에이전트 팀 (16개)
│   └── autonomous_game_playing_agent_apps/
├── rag_tutorials/           # RAG 구현 (22개)
├── mcp_ai_agents/           # MCP 에이전트 (5개)
├── voice_ai_agents/         # 음성 에이전트 (4개)
├── advanced_llm_apps/
│   ├── chat_with_X_tutorials/
│   ├── llm_apps_with_memory_tutorials/
│   ├── llm_optimization_tools/
│   ├── llm_finetuning_tutorials/
│   └── cursor_ai_experiments/
└── ai_agent_framework_crash_course/
    ├── google_adk_crash_course/
    └── openai_sdk_crash_course/
```

프로젝트마다 독립 디렉토리로 구성되어 있다.
clone 후 원하는 프로젝트만 골라 `pip install`로
바로 실행할 수 있다.

## 주요 카테고리

### Starter AI Agents (16개)

입문용 에이전트. 단일 에이전트 + 단일 도구
조합으로 핵심 개념을 익히기 좋다.

- 여행 에이전트 (로컬 & 클라우드)
- 블로그→팟캐스트 변환
- 데이터 분석, 데이터 시각화
- 의료 이미징, 음악 생성
- 밈 생성기 (브라우저 자동화)
- 생명보험 어드바이저
- 스타트업 트렌드 분석
- 추론 에이전트 (reasoning agent)
- Mixture of Agents
- 웹 스크래핑 (로컬 & 클라우드 SDK)

### Advanced Single Agents (16개)

단일 에이전트지만 복잡한 도메인 로직을 처리한다.

- **딥 리서치**: OpenAI Agents SDK + Firecrawl로
  웹을 반복 탐색하고, Research Agent가 정보를
  수집한 뒤 Elaboration Agent가 분석을 심화하는
  2단계 파이프라인
- **시스템 아키텍트**: 아키텍처 설계 자동화
- **투자 에이전트**: 투자 분석 자동화
- **저널리스트**: 뉴스 기사 작성 자동화
- **영화 프로덕션**: 영화 제작 기획
- **헬스 & 피트니스**: 개인화 건강 관리
- **멘탈 웰빙**: 정신 건강 상담
- **미팅 에이전트**: 회의 관리 및 요약
- **컨설턴트**: 전문 상담 에이전트
- **Self-Evolving Agent**: 스스로 개선하는 에이전트
- **AI Agent Governance**: 에이전트 거버넌스
- **Windows 자동화**: 데스크톱 자율 조작

### Multi-Agent Teams (16개 팀 + 15개 멀티 에이전트)

에이전트 팀은 이 저장소에서 가장 풍부한 카테고리다.
역할 분담과 협업을 통해 단일 에이전트의 한계를
넘어선다.

**도메인별 에이전트 팀:**

| 도메인       | 팀 구성                             |
|--------------|-------------------------------------|
| 금융         | Finance Team, Personal Finance      |
| 법률         | Legal Team (클라우드 & 로컬)        |
| 부동산       | Real Estate Team                    |
| 채용         | Recruitment Team                    |
| 경쟁 분석    | Competitor Intelligence Team        |
| 영업         | Sales Intelligence Team             |
| SEO          | SEO Audit Team                      |
| 교육         | Teaching Team                       |
| 게임 설계    | Game Design Team                    |
| VC 실사      | VC Due Diligence Team               |
| 여행         | Travel Planner Team                 |
| 서비스 대행  | Services Agency (CrewAI)            |

**멀티모달 팀:**

- Coding Agent Team: 코드 생성 + 리뷰 협업
- Design Agent Team: 디자인 생성 + 피드백
- UI/UX Feedback Team: 시각 분석 + UX 개선

**고급 멀티 에이전트:**

- 자기 진화(Self-Evolving) 에이전트
- 에이전트 신뢰 계층(Trust Layer)
- 협상 시뮬레이터(Negotiation Battle)
- 적응형 리서치 팀 (AG2)
- DevPulse AI: 멀티 에이전트 시그널 인텔리전스

### RAG 구현 (22개)

가장 많은 변형을 가진 카테고리다.

**기본 RAG:**

- RAG Chain: 가장 기본적인 검색→생성 파이프라인
- RAG with Database Routing: DB 기반 라우팅

**고급 RAG:**

- Corrective RAG (CRAG): 검색 결과를 검증·보정
- Agentic RAG: 에이전트가 검색 전략을 자율 결정
- Agentic RAG with Reasoning: 추론 결합
- Autonomous RAG: 완전 자율 RAG
- Gemini Agentic RAG: Gemini 모델 활용

**검색 전략:**

- Hybrid Search RAG (클라우드 & 로컬)
- Knowledge Graph RAG with Citations: 지식 그래프
  + 인용 추적
- Vision RAG: 이미지 기반 검색·생성

**로컬 실행:**

- Llama 3.1 Local RAG
- Deepseek Local RAG Agent
- Qwen Local RAG
- Local RAG Agent

**특수 목적:**

- RAG-as-a-Service: 서비스형 RAG
- RAG Failure Diagnostics Clinic: RAG 실패 진단
- AI Blog Search: 블로그 검색 특화
- Contextual AI RAG Agent: 문맥 인식 RAG
- Agentic RAG with Embedding Gemma: 임베딩 특화

### MCP AI Agents (5개)

- Browser MCP Agent: 브라우저 자동화
- GitHub MCP Agent: GitHub 연동
- Notion MCP Agent: Notion 연동
- Multi MCP Agent: 복수 MCP 서버 통합
- Travel Planner MCP Agent Team: 여행 계획 팀

### Voice AI Agents (4개)

- Audio Tour Agent: 오디오 가이드
- Customer Support Voice Agent: 고객 지원
- Voice RAG Agent (OpenAI SDK): 음성 RAG
- Open Source Voice Dictation: 받아쓰기

### Chat with X (6개)

- GitHub (GPT & Llama3)
- Gmail
- PDF (GPT & Llama3)
- Research Papers (ArXiv)
- Substack
- YouTube Videos

같은 기능을 GPT와 Llama3로 각각 구현한 예제가
있어 모델 간 비교가 가능하다.

### 최적화 도구

**TOON(Token-Oriented Object Notation):**

JSON을 TOON 포맷으로 변환하여 토큰 사용량을 줄인다.
평균 63.9% 토큰 절감, 테이블 데이터는 최대 73.4%.
JSON 247바이트 → TOON 98바이트로 60% 압축하면서
가독성은 유지한다. GPT-4 기준 100만 API 호출 시
약 $2,147 절감.

**Headroom 컨텍스트 압축:**

컨텍스트 윈도우를 50~90% 압축하여 더 많은
정보를 담거나 비용을 절감한다.

### 프레임워크 크래시 코스

Google ADK와 OpenAI Agents SDK를 단계별로 학습한다.
에이전트 생성, 함수 호출, 구조화된 출력, 메모리,
콜백, 멀티 에이전트 패턴까지 체계적으로 다룬다.
새로운 에이전트 프레임워크를 빠르게 익히기 좋다.

### 파인튜닝

Gemma 3, Llama 3.2 파인튜닝 튜토리얼을 제공한다.

## 분석

### 학습 경로가 설계되어 있다

Starter → Advanced → Multi-Agent 순서로
자연스러운 학습 흐름을 제공한다.
여행 에이전트 하나만 봐도 로컬 버전, 클라우드 버전,
메모리 탑재 버전, MCP 버전, 멀티 에이전트 팀 버전이
단계별로 존재한다.
하나의 주제를 깊이 파고들며 난이도를 올릴 수 있다.

### LLM 앱 패턴의 진화가 보인다

저장소의 카테고리 구성은 LLM 앱 개발 패턴의
진화를 보여준다.

1. **단일 프롬프트 → RAG** (22개): 외부 지식을
   주입하여 환각(hallucination)을 줄이는 단계
2. **RAG → 에이전트** (32개): 도구 사용(tool use)과
   자율적 판단으로 복잡한 태스크를 수행하는 단계
3. **단일 에이전트 → 멀티 에이전트** (31개): 역할
   분담을 통해 전문성과 신뢰성을 높이는 단계
4. **텍스트 → 멀티모달** (7개): 음성, 이미지, 비디오
   등 다양한 입출력을 처리하는 단계
5. **클라우드 → 로컬** (6개+): 프라이버시와 비용을
   고려한 온디바이스 실행 단계

프로젝트 수로 보면 에이전트(32개)가 주류이고,
멀티 에이전트(31개)가 거의 동등하게 성장했으며,
RAG(22개)가 기반 기술로 자리 잡았다.

### 모델에 구애받지 않는다

같은 앱을 OpenAI, Claude, Gemini, Llama, Deepseek,
Qwen 등 다양한 모델로 구현한 예제가 있다.
Chat with X에서 GPT와 Llama3로 동일 기능을 구현하고,
RAG에서 Llama, Deepseek, Qwen, Gemini로 로컬
변형을 제공한다. 특정 모델에 종속되지 않는 설계를
배울 수 있고, 모델 간 성능과 비용을 비교할 수 있다.

### 2단계 에이전트 패턴이 반복된다

딥 리서치 에이전트에서 보이는 "수집 → 정제" 패턴이
여러 프로젝트에서 반복된다. Research Agent가 정보를
수집하고, Elaboration Agent가 분석을 심화하는
구조다. 단순히 에이전트를 병렬로 늘리는 것이 아니라,
파이프라인으로 직렬 연결하여 품질을 높이는 접근이다.

### 에이전트 팀이 실제 조직 구조를 모방한다

16개 에이전트 팀은 실제 기업 조직의 팀 구성을
반영한다. VC 실사팀, 법률 자문팀, 채용팀, SEO 팀
등은 각각 현실의 전문 팀이 하는 업무를 에이전트로
모델링한 것이다. 이는 "어떤 업무를 자동화할 수
있는가"를 판단할 때 좋은 참고 프레임을 제공한다.

### 프레임워크 다양성이 학습 가치를 높인다

CrewAI, Phidata, OpenAI Agents SDK, Google ADK,
AG2 등 다양한 프레임워크를 활용한 예제가 있다.
같은 문제를 다른 프레임워크로 풀어볼 수 있어
프레임워크 간 장단점을 실전적으로 비교할 수 있다.

## 인사이트

### LLM 앱의 핵심은 오케스트레이션이다

모델 성능 자체보다 "모델을 어떻게 조합하고, 어떤
순서로 호출하며, 실패 시 어떻게 복구하는가"가
실전 앱의 품질을 결정한다.
멀티 에이전트 팀 사례들이 이를 잘 보여준다.
개별 에이전트의 능력보다 에이전트 간 역할 분담과
정보 흐름 설계가 결과를 좌우한다.
에이전트 신뢰 계층(Trust Layer)이나 협상
시뮬레이터 같은 프로젝트는 에이전트 간 상호작용의
품질 관리까지 다루고 있다.

### RAG의 진화가 계속되고 있다

22개의 RAG 변형은 이 패턴이 단일 기술이 아니라
하나의 스펙트럼임을 보여준다.
기본 RAG Chain에서 시작해 Corrective RAG(검증),
Agentic RAG(자율 전략), Knowledge Graph RAG(구조화),
Vision RAG(멀티모달)까지 계속 진화하고 있다.
특히 RAG Failure Diagnostics Clinic의 존재는
"RAG가 실패하는 이유를 체계적으로 진단하는 것"
자체가 하나의 전문 분야가 되었음을 시사한다.

### 비용 최적화가 프로덕션의 관문이다

TOON 포맷으로 평균 63.9% 토큰을 절감하고,
테이블 데이터는 최대 73.4%까지 줄일 수 있다.
GPT-4 기준 100만 호출 시 $2,147 절감 효과.
Headroom 컨텍스트 압축은 50~90%까지 줄인다.
프로토타입에서 프로덕션으로 넘어갈 때 비용은
가장 큰 장벽이다. 모델 성능만 추구하면 비용이
폭증하고, 비용만 줄이면 품질이 떨어진다.
최적화 도구를 별도 카테고리로 다루는 것은
이 긴장 관계의 중요성을 반영한다.

### 자기 진화하는 에이전트가 등장했다

Self-Evolving Agent는 에이전트가 자신의 성능을
스스로 평가하고 개선하는 패턴이다.
이는 에이전트 개발의 방향이 "사람이 설계 →
에이전트가 실행"에서 "에이전트가 설계도 자율적으로
개선"하는 쪽으로 이동하고 있음을 보여준다.
AI Agent Governance 프로젝트의 존재도 이런 자율성
확대에 따른 통제 필요성을 반영한다.

### MCP가 에이전트의 연결성을 표준화한다

MCP(Model Context Protocol) 에이전트가 별도
카테고리로 존재하는 것은 이 프로토콜이 에이전트와
외부 시스템 간의 연결을 표준화하는 방향으로 빠르게
자리잡고 있음을 시사한다. 특히 Multi MCP Agent는
복수의 MCP 서버를 통합하는 패턴을 보여주는데,
이는 단일 도구 연동을 넘어 에이전트의 "도구 생태계"가
형성되고 있음을 의미한다.

### 로컬 실행이 새로운 차별화 요소다

Llama, Deepseek, Qwen 각각의 로컬 RAG 구현과
법률 팀의 로컬 버전 등 클라우드 API에 의존하지
않는 구현이 다수 포함되어 있다.
이는 비용 절감뿐 아니라 데이터 주권
(data sovereignty), 오프라인 환경, 규제 대응
측면에서 점점 중요해지는 방향이다.
오픈소스 모델의 성능이 향상되면서 로컬 실행이
실질적 대안이 되고 있다.

### 멀티모달 팀이 새로운 가능성을 연다

Multimodal Coding Team, Design Team, UI/UX
Feedback Team은 텍스트만 다루는 에이전트의 한계를
넘어선다. 코드 생성 + 시각적 리뷰, 디자인 생성 +
피드백 루프, UI 스크린샷 분석 + 개선 제안 등
"보고 판단하는" 능력이 팀 단위로 작동한다.
이는 향후 에이전트가 텍스트 기반 업무를 넘어
시각적 판단이 필요한 업무까지 확장될 방향을
보여준다.

### 실전 도메인 적용이 핵심 가치다

단순 데모가 아니라 금융, 법률, 부동산, 의료, 채용,
SEO, 경쟁 분석 등 구체적 도메인에 적용한 사례가
많다. 이는 "LLM으로 무엇을 만들 수 있는가"라는
질문에 구체적 답을 제공한다.
특히 에이전트 팀 구성은 실제 업무 프로세스를
에이전트로 모델링하는 좋은 참고 사례다.
홈 리노베이션, 보험 어드바이저, 이별 회복 에이전트
등 예상 밖의 도메인도 있어 적용 범위의 넓이를
실감할 수 있다.

### 에이전트 간 신뢰와 협상이 연구 주제가 되었다

Trust Layer와 Negotiation Battle Simulator의
존재는 흥미롭다.
에이전트가 많아질수록 "이 에이전트의 출력을
얼마나 신뢰할 수 있는가", "에이전트 간 의견이
충돌할 때 어떻게 해결하는가"가 중요해진다.
이는 단순한 기술적 문제를 넘어 에이전트 시스템의
아키텍처적 과제로 떠오르고 있다.
