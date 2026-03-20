# Codex Subagents

Codex의 서브에이전트(subagent)는 현재 대화와 분리된 작업 단위를
별도 에이전트에 맡겨 병렬로 진행하거나, 컨텍스트를 오염시키지
않고 정찰·조사·구현 일부를 위임할 때 쓰는 기능이다.

핵심 가치는 속도만이 아니라 **컨텍스트 분리**다.
메인 에이전트는 현재 작업 흐름을 유지하고, 서브에이전트는 더
좁은 목표만 집중해서 처리한다.

## 언제 유용한가

- 처음 들어온 저장소를 빠르게 훑고 싶을 때
- 특정 디렉터리나 주제를 별도 조사시키고 싶을 때
- 구현 전 자료 조사와 코드 변경을 분리하고 싶을 때
- 병렬로 여러 하위 작업을 돌리고 싶을 때

## 어떻게 지시하나

서브에이전트에게는 넓은 요청보다 **단일 목표와 명확한 산출물**을
주는 편이 낫다.

좋은 지시의 예:

- 무엇을 볼지
- 무엇을 하지 말지
- 어떤 형식으로 요약할지
- 필요하면 어떤 파일을 우선 볼지

예:

```text
Spawn a subagent to explore this repo.
```

```text
Spawn a subagent to map the codex docs in this repo.
```

```text
Spawn a subagent to inspect repo-specific writing conventions.
```

## 첫 예제: `Spawn a subagent to explore this repo.`

가장 기본적인 활용은 저장소 정찰이다.
직접 구현을 시작하기 전에 저장소의 목적, 디렉터리 구조,
주요 문서, 작업 규칙을 먼저 파악시키는 데 유용하다.

이 프롬프트로 생성한 서브에이전트는 보통 다음을 요약한다.

- 저장소의 주된 성격
- 최상위 디렉터리 구조
- 눈에 띄는 하위 디렉터리와 대표 문서
- 빌드/테스트/도구 관례
- 이후 작업에 중요한 저장소 로컬 규칙

이 저장소에서는 실제로 다음과 같은 내용이 먼저 확인됐다.

- 앱 코드 중심 저장소라기보다 주제별 마크다운 문서를 쌓아두는
  TIL 아카이브에 가깝다.
- [`ai`](../ai), [`codex`](./README.md), [`.agent/skills`](../.agent/skills)
  등이 눈에 띄는 영역이다.
- [`AGENTS.md`](../AGENTS.md) 와 [`.prettierrc`](../.prettierrc) 가
  이후 작업 규칙에 중요하다.

## 후속 프롬프트 예시

처음 탐색이 끝나면 범위를 좁혀 다시 맡기면 된다.

```text
Spawn a subagent to explore the ai directory.
```

```text
Spawn a subagent to inspect repo-specific writing conventions.
```

```text
Based on that exploration, add a new document under codex.
```

## 주의할 점

서브에이전트는 만능이 아니다.
범위가 넓고 목표가 흐리면 결과도 뭉뚱그려지기 쉽다.

또한 "탐색"과 "수정"은 분리하는 편이 안전하다.
먼저 탐색 결과를 받고, 그다음 수정 작업을 별도로 지시하는 흐름이
대체로 안정적이다.
