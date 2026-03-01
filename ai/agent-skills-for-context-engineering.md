# Agent Skills for Context Engineering

Muratcan Koylan의 에이전트 스킬 컬렉션:
<https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering>

프롬프트 엔지니어링이 "지시를 잘 작성하는 기술"이라면,
컨텍스트 엔지니어링(Context Engineering)은 **언어 모델의
제한된 주의(attention) 예산을 어떻게 최적 배분할 것인가**를
다루는 더 넓은 분야다. 이 저장소는 컨텍스트 엔지니어링의
핵심 원리를 실행 가능한 에이전트 스킬로 구조화한 오픈소스
프로젝트다.

## 핵심 개념: 컨텍스트 엔지니어링

컨텍스트 엔지니어링은 시스템 프롬프트, 도구 정의, 검색된
문서, 대화 히스토리, 도구 출력을 종합적으로 큐레이션하는
기술이다. 컨텍스트가 길어질수록 모델 성능이 예측 가능하게
저하되는데, 대표적인 현상이 두 가지다:

1. **Lost-in-the-Middle:** 컨텍스트 중간에 위치한 정보를
   모델이 놓치는 현상. 시작과 끝만 잘 기억한다.
2. **Attention Scaturation:** 주의가 너무 많은 토큰에
   분산되면서 각 토큰에 대한 집중도가 떨어지는 현상.

프롬프트 엔지니어링이 "무엇을 말할까"에 집중한다면,
컨텍스트 엔지니어링은 **"무엇을 보여주고, 무엇을 숨기고,
언제 꺼낼까"**에 집중한다.

## 스킬 구조

모든 스킬은 동일한 디렉토리 구조를 따른다:

```
skill-name/
├── SKILL.md       # 스킬 정의와 트리거 조건
├── scripts/       # 실행 가능한 Python 데모
└── references/    # 참고 자료
```

## 스킬 카테고리

### 기초(Foundational)

| 스킬                  | 설명                           |
| --------------------- | ------------------------------ |
| context-fundamentals  | 컨텍스트 윈도우의 기본 원리    |
| context-degradation   | 성능 저하 패턴과 진단법        |
| context-compression   | 컨텍스트 압축 전략             |

### 아키텍처(Architectural)

| 스킬                | 설명                           |
| ------------------- | ------------------------------ |
| multi-agent-patterns | 다중 에이전트 설계 패턴       |
| memory-systems      | 에이전트 메모리 시스템 설계    |
| tool-design         | 도구 정의 최적화               |
| filesystem-context  | 파일 시스템 기반 컨텍스트 관리 |
| hosted-agents       | 호스팅된 에이전트 아키텍처     |

### 운영(Operational)

| 스킬                  | 설명                           |
| --------------------- | ------------------------------ |
| context-optimization  | 컨텍스트 최적화 기법           |
| evaluation            | 평가 프레임워크                |
| advanced-evaluation   | LLM-as-Judge 고급 평가         |

### 개발(Development)

| 스킬                | 설명                           |
| ------------------- | ------------------------------ |
| project-development | 프로젝트 계획과 태스크 분석    |

### 인지(Cognitive)

| 스킬              | 설명                           |
| ----------------- | ------------------------------ |
| bdi-mental-states | BDI 모델 기반 에이전트 설계    |

## 설계 원칙

**Progressive Disclosure:** 스킬이 로드될 때 메타데이터만
먼저 보여주고, 실제 컨텐츠는 관련성이 확인된 후에만
로드한다. 컨텍스트 윈도우를 아끼는 핵심 전략이다.

**Platform Agnosticism:** Claude Code, Cursor, 커스텀
구현 등 플랫폼에 무관하게 적용 가능한 원리를 다룬다.

**Practical Foundation:** 외부 의존성 없는 Python
데모 코드로 개념을 실증한다.

## 예제 프로젝트

저장소에는 네 가지 실전 예제가 포함되어 있다:

**Digital Brain Skill:** 6개 모듈과 4개 자동화 스크립트로
구성된 개인 운영 체제. Progressive Disclosure와
append-only 메모리 패턴을 실증한다.

**X-to-Book System:** X(Twitter) 계정을 모니터링하고
일일 합성 도서를 생성하는 다중 에이전트 아키텍처.

**LLM-as-Judge Skills:** 직접 채점(Direct Scoring),
쌍별 비교(Pairwise Comparison), 루브릭 생성(Rubric
Generation)을 포함한 TypeScript 평가 도구. 19개 테스트
통과.

**Book SFT Pipeline:** Gertrude Stein 문체를 8B 모델에
전이하는 파인튜닝 파이프라인. 총 비용 $2.

## 학술적 인정

북경대학교 일반인공지능 국가중점연구소의 Meta Context
Engineering(MCE) 논문에서 인용되었다:

> "While static skills are well-recognized
> [Anthropic, 2025b; Muratcan Koylan, 2025],
> MCE is among the first to dynamically evolve them."

정적 스킬 아키텍처의 기초 연구로 인정받은 셈이다.

## 인사이트

### 컨텍스트 엔지니어링은 프롬프트 엔지니어링의 상위 개념

프롬프트 엔지니어링이 "한 번의 입력을 잘 작성하는 것"이라면,
컨텍스트 엔지니어링은 "모델이 보는 전체 정보 환경을
설계하는 것"이다. 시스템 프롬프트, 도구 출력, 메모리,
대화 히스토리를 모두 하나의 설계 대상으로 본다.
CLAUDE.md, AGENTS.md 같은 파일이 바로 컨텍스트
엔지니어링의 실천이다.

### Progressive Disclosure는 UX 원칙의 재발견

필요한 정보만 필요한 시점에 제공한다는 원칙은 UI/UX
설계에서 오래전부터 쓰인 패턴이다. 이를 에이전트의
컨텍스트 윈도우 관리에 적용한 것이 이 프로젝트의
가장 실용적인 기여다. 한정된 주의 자원을 가진 모델에게
정보를 한꺼번에 쏟아붓는 것은 사용자에게 복잡한 UI를
던지는 것과 같다.

### 스킬 단위의 모듈화가 핵심

각 스킬이 독립적인 SKILL.md, scripts, references
구조를 갖는다. 이 모듈화 덕분에 필요한 스킬만 선택적으로
로드할 수 있고, 컨텍스트 오염을 방지한다.
마이크로서비스가 모놀리스를 대체한 것처럼, 거대한 단일
시스템 프롬프트 대신 **조합 가능한 스킬 단위**로 에이전트를
구성하는 방향이다.

### 정적 스킬의 한계와 동적 진화

MCE 논문이 이 저장소를 "정적 스킬"로 분류한 점이
흥미롭다. 미리 정의된 스킬은 예측 가능하고 안정적이지만,
새로운 상황에 적응하지 못한다. 다음 단계는 에이전트가
스스로 스킬을 생성하고 진화시키는 것이다. 이 저장소는
그 기반이 되는 "잘 구조화된 정적 스킬"의 레퍼런스
구현이다.

### 실전 예제의 교육적 가치

Digital Brain, X-to-Book 같은 예제는 단순 데모가 아니라
실제 문제를 해결한다. 특히 Book SFT Pipeline이 $2로
문체 전이를 달성한 것은 컨텍스트 엔지니어링과 파인튜닝의
비용 효율성을 동시에 보여준다.

## 관련 문서

- [Agentic Engineering Patterns #1-1:
  코드 작성 비용은 이제 거의 공짜다
  ](./agentic-engineering-patterns-1-1-code-is-cheap.md)
- [File-Based Planning Workflow
  ](./file-based-planning-workflow.md)
- [AI Coding Agent Guidelines
  ](./ai-coding-agent-guidelines.md)
- [HuggingFace Skills](./huggingface-skills.md)
