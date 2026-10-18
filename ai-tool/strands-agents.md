# Strands Agents: 에이전트 루프를 직접 짜는 대신 쓰는 AWS의 오픈소스 하네스

<https://strandsagents.com/>

<https://github.com/strands-agents/harness-sdk>

HN 토론: <https://news.ycombinator.com/item?id=49817289> (150점, 97개 댓글)

GN 토론: <https://news.hada.io/topic?id=35442>

## 소개

Strands Agents는 Python과 TypeScript로 AI 에이전트를 만들고 실행하는 오픈소스 SDK다.
README는 자기 에이전트 루프를 직접 짜려던 사람에게 이것을 고르라고 권한다.
호스팅된 제어 평면 없이 내 프로세스 안에서 실행되고,
직접 짠 루프가 결국 떠안게 되는 일들을 한 SDK에 담았다는 것이다.
턴 제한, 토큰 예산, 취소, 중단 사유 같은 생명주기 제어,
도구와 구조화된 출력, MCP, 멀티 에이전트 패턴, 메모리와 세션,
모델 이식성, 스트리밍, 가드레일, 추적, 평가가 그것이다.[^readme]

Amazon Web Services의 Strands 팀이 만들며 라이선스는 Apache 2.0이다.[^harness-readme]
저장소 `strands-agents/harness-sdk`는 2025년 5월 14일에 만들어졌고,
2026년 10월 17일 확인 기준 스타 8,843개, 포크 1,383개다.[^gh-api]
홈페이지는 이 SDK를 “운영용 AI 에이전트를 위한 오픈소스 도구 모음”으로 소개하며,
하네스와 SDK 외에 에이전트 샌드박스 Box, 에이전트용 가상 셸 Shell,
평가 SDK, 실험 프로젝트 Labs를 함께 보여 준다.[^home]
Box는 OS 수준의 격리에 Dogwood 정책을 더한 샌드박스로 소개된다.[^home]
홈페이지의 최근 소식은 Strands Decider에 에이전트 판단용
Gemma 4 모델 네 개가 추가되었다는 것이다.[^home]
홈페이지가 내세우는 GitHub 스타 14,800개 이상은 이 저장소 하나의 수치보다 커서,
여러 저장소를 합친 값으로 보인다.[^home]
하네스 출시 때 HN의 crossroadsguy도
스타가 가장 많은 SDK 저장소가 7,800개인데
랜딩 페이지가 모든 저장소를 더해 13,000개 이상을 내세운다고
지적한 바 있다.[^crossroadsguy]

## 구성

모노레포는 다음으로 나뉜다.[^readme]

| 디렉터리       | 내용                                                        |
| -------------- | ----------------------------------------------------------- |
| `harness-py/`  | Python 하네스, `create_harness()` 한 번으로 완성된 에이전트 |
| `harness-ts/`  | TypeScript 하네스, `createHarness()`                        |
| `strands-cli/` | 터미널에서 하네스 에이전트로 시제품을 만들고 대화하는 CLI   |
| `strands-py/`  | Python SDK, 에이전트 루프와 모델 공급자와 도구              |
| `strands-ts/`  | TypeScript SDK                                              |
| `strands-mcp/` | 코딩 에이전트에게 Strands 사용법을 알려 주는 MCP 서버       |
| `site/`        | strandsagents.com 문서 사이트 소스                          |
| `team/`        | 거버넌스와 SDK 간 프로세스 문서, 설계 제안                  |
| `test-infra/`  | 통합 테스트용 AWS 자원을 만드는 CDK 스택                    |

Claude Code, Codex, Cursor용 Strands 플러그인도 있어서
프레임워크 선택, 뼈대 생성, 도구 작성, MCP 서버 연결, LangGraph 이전 안내를
코딩 에이전트 안에서 받을 수 있다.[^readme]

## 사용법

### 하네스로 시작하기

가장 쉬운 시작은 완성된 에이전트인 하네스다.[^readme]

```bash
pip install strands-harness
```

```python
from strands_harness import create_harness

agent = create_harness()
agent("Find the slowest test in this repo and explain why it's slow")
```

TypeScript에서는 `@strands-agents/harness`의 `createHarness()`를 쓴다.
기본 모델은 Amazon Bedrock이고, 다른 공급자는 추가 패키지로 붙인다.

```bash
pip install "strands-harness[openai]"   # 또는 [anthropic], [gemini], [ollama], [litellm]
```

### 하네스의 기본값

`create_harness()`가 기본으로 주는 것은 다음과 같다.[^harness-readme]

- 추론을 켠 프런티어 모델.
  기본값은 Amazon Bedrock의 Claude Opus 5이고,
  바꾸기 전에 탐색하고, 되돌릴 수 없는 일 전에 확인하고,
  끝났다고 하기 전에 검증하라는 시스템 프롬프트가 붙는다.
- 셸, 파일 도구(`read`, `write`, `edit`), 웹 접근,
  그리고 다른 도구를 엮고 반복하고 병렬로 부르는 코드를 쓰는 샌드박스
  `programmatic_tool_caller`.
- 오래된 턴을 요약하고 큰 도구 결과를 저장소로 옮겨 짧은 참조만 남기는
  컨텍스트 관리와,
  공급자가 지원하면 반복되는 부분을 캐시하는 기능.
- 대화를 디스크에 저장해 세션 ID로 재개하고,
  대화를 넘나드는 사실을 마크다운 파일로 정리하는 장기 메모리.
- 반환값이 평범한 `strands.Agent`라서 모든 기본값을 바꿀 수 있다.

주요 인자는 다음과 같다.

| 인자              | 기본값                    | 뜻                                          |
| ----------------- | ------------------------- | ------------------------------------------- |
| `model`           | Bedrock의 Claude Opus 5   | `"공급자/이름"`이나 Model 인스턴스          |
| `effort`          | `"auto"`                  | `"off"`부터 `"max"`까지 추론 강도           |
| `context_manager` | `"auto"`                  | `"agentic"`, 설정, 인스턴스, `False`        |
| `session`         | `True`                    | 세션 저장과 재개                            |
| `skills`          | `True`(`./.agent/skills`) | 경로, git URL, `False`                      |
| `memory`          | `True`(`./.agent/memory`) | 디렉터리나 저장소 지정, `False`             |
| `interventions`   | 없음                      | `"ask"`, `"smart"`, 정책 문자열, Cedar 파일 |

### SDK로 내려가기

에이전트 루프와 도구, 모델 공급자,
메모리를 직접 엮고 싶으면 SDK를 쓴다.[^readme]

```bash
pip install strands-agents strands-agents-tools
```

```python
from strands import Agent
from strands_tools import calculator

agent = Agent(tools=[calculator])
agent("What is the square root of 1764")
```

Python SDK는 3.10 이상, TypeScript SDK는 Node.js 22 이상이 필요하다.
모델 공급자는 Amazon Bedrock, Anthropic, OpenAI, Gemini를 일급으로 지원하고
Ollama와 사용자 정의 공급자도 붙일 수 있다.

## 분석

### “하네스”라는 이름이 제품의 위치를 바꿨다

저장소 이름이 `harness-sdk`이고, README의 첫 권유도 SDK가 아니라 하네스다.
하네스는 모델, 도구, 컨텍스트 관리, 세션, 메모리를 미리 조립하고
시스템 프롬프트까지 다듬어 한 줄로 쓰게 한 완성품이다.
SDK는 그 아래에서 루프를 직접 다루고 싶은 사람을 위한 층이 되었다.[^readme]

이 구조는 에이전트 프레임워크 경쟁의 축이 바뀌었음을 보여 준다.
예전에는 얼마나 유연한 추상화를 주느냐로 경쟁했다면,
이제는 Claude Code나 Codex 같은 코딩 에이전트가 이미 보여 준
“잘 다듬어진 기본값”을 누가 일반 에이전트에 줄 수 있느냐로 경쟁한다.
하네스의 기본 시스템 프롬프트가 탐색, 확인, 검증을 강조하는 것도
코딩 에이전트에서 검증된 습관을 그대로 옮긴 것이다.[^harness-readme]

### 모델 중립을 말하지만 기본값은 AWS를 향한다

README는 어떤 모델, 어떤 클라우드든 된다고 강조하고
Bedrock, Anthropic, OpenAI, Gemini를 일급으로 지원한다.[^readme]
그러나 하네스의 기본 모델은 Bedrock 위의 Claude Opus 5이고,
다른 공급자는 추가 패키지를 설치해야 한다.[^harness-readme]
통합 테스트 인프라도 AWS CDK로 만든다.

기본값은 대부분의 사용자가 바꾸지 않는다는 점에서 영향이 큰 결정이다.
Strands는 모델 이식성을 진지하게 지원하면서도,
아무것도 바꾸지 않은 사용자를 AWS로 이끄는 구조를 갖고 있다.

### 저장소가 코딩 에이전트를 사용자로 상정한다

루트에 `AGENTS.md`, `CLAUDE.md`, `.claude`, `.cursor-plugin`, `.kiro` 같은
여러 코딩 에이전트용 설정이 있고,
Strands 사용법을 알려 주는 MCP 서버와
코딩 에이전트 플러그인을 따로 제공한다.[^readme][^gh-api]
이는 Strands로 에이전트를 만드는 사람의 상당수가
직접 코드를 쓰기보다 코딩 에이전트에게 맡길 것이라는 전제다.
프레임워크의 문서와 예제가 사람이 읽는 것만큼
에이전트가 읽기 좋게 쓰여야 하는 시대가 되었다.

## 비평

### 기본값의 근거는 벤더가 직접 잰 벤치마크에 기대 있다

README는 하네스가 모델, 도구, 메모리, 세션, 컨텍스트 관리에
벤치마크로 검증한 기본값을 준다고만 말한다.[^readme]
그 근거는 9월 21일 하네스 출시 글에 있다.
같은 Claude나 GPT 모델을 쓸 때 여섯 개 벤치마크에서 비용이 28% 적었고,
Fable 5에서는 Claude Code보다 비용이 77% 적으면서
Terminal-Bench 2.1 점수는 더 높았다는 것이다.
측정은 EC2에서 Harbor로 분산 실행했고,
약 1,500토큰이 넘는 도구 결과를 자르고
컨텍스트 창이 85%에 이르면 요약하는 설정이
이 결과를 낳은 기본값으로 소개된다.[^launch]

그러나 이 수치는 Strands 팀이 직접 잰 것이고,
여섯 벤치마크 가운데 이름이 밝혀진 것은 Terminal-Bench 2.1 하나뿐이며,
반복 횟수와 재현 방법도 글에는 없다.
결과는 대화형 차트로만 제공되고, 연구진의 후속 논문을 기다리라고 한다.[^launch]
도구 결과를 자르고 오래된 턴을 요약하는 방식은
작업 종류에 따라 정보 손실을 낳을 수 있는데,
그 비용이 어떤 작업에서 커지는지도 다루지 않는다.
완성품을 내세우는 하네스일수록,
기본값이 어디서 손해를 보는지까지 밝힐 책임이 크다.

HN에서도 같은 지적이 나왔다.
seizethecheese는 Terminal-Bench 2.1이 이미 포화되어
토큰 절약 기법 상당수가 비슷한 점수로 돈만 아낄 것이고,
점수가 더 높다는 차이도 통계적으로 유의하지 않을 것이라고 했다.[^seizethecheese]
Strands 쪽으로 보이는 strandstan은
높은 추론 강도에서 Strands 하네스가 69.7점, Claude Code가 61.8점이었고
더 많은 하네스를 다룬 후속 글을 준비 중이라고 답했다.[^strandstan]
RomanKornev는 기본값을
1,500토큰 넘는 도구 결과는 링크로 바꾸고 85%에서 강제 압축하는 것으로 요약하며,
프런티어 연구소들이 이미 오래 다듬어 온 장기 작업에서는
통하지 않을 가능성이 크다고 봤다.[^RomanKornev]
johnmlussier는 모델 제공사가 자기 하네스에 맞춰 에이전트를 학습시키기 시작해
비공식 하네스를 쓰기가 점점 망설여지며,
모델이 나올 때마다 하네스를 다시 평가하고 싶지는 않다고 했다.[^johnmlussier]

### 프로젝트가 넓어질수록 무엇이 안정적인지 흐려진다

릴리스는 Python SDK, TypeScript SDK, Python 하네스, TypeScript 하네스, CLI가
각자 다른 버전 번호로 나온다.
10월 12일부터 15일 사이에만 Python SDK 1.60.0, 1.61.0, 1.61.1과
하네스 0.3.0, 0.3.1, CLI 0.2.1이 나왔다.[^releases]
SDK는 1.x지만 README가 먼저 권하는 하네스는 0.x다.

홈페이지는 여기에 Box, Shell, Evals SDK, Labs까지 더한다.[^home]
사용자가 가장 먼저 만나는 진입점이 아직 0.x라는 점,
그리고 어떤 구성 요소가 안정판이고 어떤 것이 실험인지가
한눈에 보이지 않는다는 점은 운영 환경 도입을 검토하는 팀에게 부담이다.

## 인사이트

### 에이전트 프레임워크는 “루프”가 아니라 “운영 기본값”을 판다

에이전트 루프 자체는 이제 수십 줄이면 짤 수 있다.
Strands가 README 첫머리에서 강조하는 것도 루프가 아니라
턴 제한, 토큰 예산, 취소, 추적, 평가처럼
직접 짠 루프가 결국 떠안게 되는 운영 문제들이다.[^readme]
프레임워크의 가치는 추상화의 우아함보다
운영에서 마주칠 문제를 미리 얼마나 풀어 두었느냐로 옮겨 갔다.

### 하네스의 기본 프롬프트가 사실상 가장 중요한 코드가 된다

`create_harness()` 한 줄의 품질은 상당 부분
시스템 프롬프트와 도구 구성에서 나온다.
이 부분은 일반 코드처럼 타입 검사나 단위 테스트로 품질을 보장하기 어렵고,
모델이 바뀌면 같은 프롬프트의 효과도 달라진다.
하네스를 쓰는 팀은 라이브러리 버전만이 아니라
그 버전에 묶인 프롬프트와 기본 모델의 변화도 함께 추적해야 한다.

---

[^readme]: strands-agents/harness-sdk, [README.md](https://github.com/strands-agents/harness-sdk/blob/main/README.md), 2026-10-17 확인

[^harness-readme]: strands-agents/harness-sdk, [harness-py/README.md](https://github.com/strands-agents/harness-sdk/blob/main/harness-py/README.md), 2026-10-17 확인

[^gh-api]: GitHub API, [strands-agents/harness-sdk](https://api.github.com/repos/strands-agents/harness-sdk), 2026-10-17 확인

[^home]: Strands Agents, [strandsagents.com](https://strandsagents.com/), 2026-10-17 확인

[^releases]: strands-agents/harness-sdk, [Releases](https://github.com/strands-agents/harness-sdk/releases), 2026-10-17 확인

[^launch]: Strands Agents, [Introducing Strands harness: frontier performance with 28% lower token cost](https://strandsagents.com/blog/introducing-strands-harness/), 2026-09-21

[^crossroadsguy]: <https://news.ycombinator.com/item?id=49820163>

[^seizethecheese]: <https://news.ycombinator.com/item?id=49817721>

[^strandstan]: <https://news.ycombinator.com/item?id=49818622>

[^RomanKornev]: <https://news.ycombinator.com/item?id=49822334>

[^johnmlussier]: <https://news.ycombinator.com/item?id=49817858>
