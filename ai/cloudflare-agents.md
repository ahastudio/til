# Cloudflare Agents

- 문서: <https://developers.cloudflare.com/agents/>
- 저장소: <https://github.com/cloudflare/agents>

## 요약

Cloudflare Agents는 Cloudflare Workers 위에서
AI 에이전트를 실행하도록 돕는 런타임/SDK 계열로
이해할 수 있다.

핵심 포인트는 다음 세 가지다.

1. 요청 단위 서버리스 실행(Workers)
2. 상태 유지 실행(Durable Objects)
3. 엣지 네트워크 분산 배포(Cloudflare 네트워크)

즉, "LLM 호출"만이 아니라
"상태가 있는 에이전트 세션"을
엣지에 가까운 위치에서 운영하는 관점이 중요하다.

## 왜 Cloudflare에서 Agent를 빌드하나

### 1) 상태 중심 워크로드에 유리하다

일반 서버리스는 무상태(stateless) 실행에 강하다.
하지만 에이전트는 대화 문맥, 작업 큐,
도구 실행 결과를 누적 관리해야 한다.

Cloudflare 스택에서는 Durable Objects를 통해
세션 상태를 한 단위 객체로 고정해
일관성을 확보하는 패턴이 자주 쓰인다.

### 2) 지연 시간(latency) 최적화 여지가 크다

도구 호출이나 사용자 인터랙션이 반복되는
에이전트 워크플로우는 왕복 지연에 민감하다.

Workers 기반 배포는 사용자와 가까운 엣지에서
빠르게 응답을 시작할 수 있어
"첫 토큰 시간"과 체감 반응성 개선에 유리하다.

### 3) 운영 단순화가 가능하다

기본 배포 단위가 Worker 스크립트이므로
컨테이너 오케스트레이션 계층을
반드시 먼저 구축할 필요는 없다.

초기 단계에서는
"작은 에이전트 + 명확한 상태 모델"부터
빠르게 검증하기 좋다.

## 코드 관점 분석

아래는 Cloudflare Agents 자체 API를 모사한 예제가 아니라,
Workers + Durable Objects 조합에서
에이전트를 구현할 때의 구조 분석이다.

```ts
// Worker entry (개념 예시)
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const sessionId = getSessionId(request)
    const id = env.AGENT_SESSION.idFromName(sessionId)
    const stub = env.AGENT_SESSION.get(id)
    return stub.fetch(request)
  },
}
```

```ts
// Durable Object (개념 예시)
export class AgentSession {
  constructor(private state: DurableObjectState, private env: Env) {}

  async fetch(request: Request): Promise<Response> {
    const input = await request.json()
    const memory = await this.state.storage.get("memory")

    const prompt = buildPrompt(memory, input)
    const output = await callModel(this.env, prompt)

    await this.state.storage.put("memory", update(memory, input, output))
    return Response.json({ output })
  }
}
```

### 분석 포인트 A: 세션 라우팅이 핵심 경계다

`idFromName(sessionId)`는
동일 세션을 동일 객체 인스턴스로 보낸다.
이 경계가 에이전트 일관성을 보장한다.

### 분석 포인트 B: 메모리 저장 단위를 먼저 설계해야 한다

메시지 전체를 저장하면 단순하지만
비용과 검색 성능이 빠르게 나빠진다.

실무에서는 다음 3계층 분리를 권장한다.

- 단기: 최근 N턴 원문
- 중기: 압축 요약(memory summary)
- 장기: 벡터 검색 인덱스(RAG)

### 분석 포인트 C: 도구 실행은 멱등성(idempotency) 확보가 먼저다

네트워크 재시도, 타임아웃 재호출이 생기면
중복 실행 부작용이 발생한다.

툴 호출에 `operationId`를 붙이고
이미 처리한 작업인지 저장소에서 확인하는
"at-least-once 방어"가 필요하다.

## 아키텍처 패턴 제안

### 패턴 1: Session Actor 패턴

- 1세션 = 1Durable Object
- 채팅/작업 상태를 객체 내부 저장
- 장점: 강한 일관성, 단순한 디버깅
- 단점: 핫 세션 집중 시 단일 병목 가능

### 패턴 2: Planner/Executor 분리

- Planner: 계획 수립(상태 전이 결정)
- Executor: 외부 도구 호출 실행
- 장점: 실패 복구와 재실행 정책 분리 용이
- 단점: 이벤트 스키마 설계 비용 증가

### 패턴 3: Event-Sourced Agent

- 상태 대신 이벤트 append 로그를 저장
- 필요 시 스냅샷으로 재구성
- 장점: 감사 추적, 리플레이 테스트 용이
- 단점: 모델 진화 시 마이그레이션 복잡도 증가

## 운영 인사이트

### 1) "정확도"보다 "회복력"이 먼저다

에이전트는 100% 정답 시스템이 아니다.
실패를 빠르게 감지하고 복구하는 경로가
제품 신뢰도를 결정한다.

### 2) 토큰 비용은 상태 모델링 문제다

프롬프트 엔지니어링만으로는 한계가 있다.
메모리 계층 분리와 요약 정책이
비용/품질 균형의 핵심이다.

### 3) 도구 신뢰도 SLO를 분리하라

LLM 품질 지표와 도구 성공률을 섞으면
병목 위치를 찾기 어렵다.

- LLM: 응답 관련 지표
- Tool: 성공률, 재시도율, P95 지연
- Orchestrator: 단계 완료율, 회복 시간

## 구현 체크리스트

### 최소 기능(MVP)

- 세션 식별자 기반 라우팅
- 최근 대화 N턴 메모리
- 도구 1~2개(읽기 전용 우선)
- 실패 시 재시도 + 타임아웃
- 기본 관측성 로그(trace id)

### 프로덕션 전환

- 메모리 계층화(단기/요약/RAG)
- 도구 멱등성 키
- 운영자 개입(Human-in-the-loop)
- 비용 가드레일(턴당 토큰 상한)
- 모델/프롬프트 버전 롤백 전략

## 조사 메모

현재 환경에서는 외부 네트워크 접근 제한으로
Cloudflare 문서/저장소 본문을 직접 인용하지 못했다.

따라서 이 문서는
Cloudflare에서 에이전트를 설계할 때의
아키텍처 중심 실무 관점을 우선 정리한 메모다.

문서 접근이 가능한 환경에서는
공식 SDK API 시그니처와 코드 예제를 추가해
이 문서를 업데이트하는 것을 권장한다.
