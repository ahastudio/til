# Claude Code에 장기 기억 만들기: `/recall`

> Grep Is Dead: How I Made Claude Code Actually Remember Things

<https://twitter.com/artemxtech/status/2028330693659332615>

Artem Zhutov(@artemxtech)가 3주 동안 700개 세션을 진행하며 발견한
문제와 해결책을 정리한 트윗.

## 문제: Claude Code는 상태가 없다

Claude Code와의 모든 대화는 제로에서 시작된다. 두 가지 상황이
특히 고통스럽다.

- 세션 중 컨텍스트 60% 시점에 compact 또는 핸드오프 → 결정의 절반
  유실
- 다음 날 재개 → 이전에 무엇을 하고 있었는지 전혀 기억 없음

Anthropic 엔지니어도 Hacker News에서 인정했듯, Claude Code는
RAG 없이 **라인별 grep**으로 코드베이스를 탐색한다. 단순 코드 검색엔
충분하지만 장기 맥락 복원에는 근본적으로 부적합하다.

## 해결책: QMD + `/recall` 스킬

[QMD](https://github.com/tobi/qmd)는 Shopify CEO Tobi Lütke가
만든 로컬 마크다운 검색 엔진. Obsidian 볼트를 인덱싱해 1초 이내에
무엇이든 찾아준다.

### 검색 모드 비교

| 방식          | 명령어       | 특징                          |
| ------------- | ------------ | ----------------------------- |
| grep          | -            | 200개 노이즈 파일, 3분 소요   |
| BM25          | qmd search   | 2초, 검색의 80% 커버          |
| Semantic      | qmd vsearch  | 정확한 단어 없어도 개념 검색  |
| Hybrid        | qmd query    | BM25 + Semantic, 최고 품질    |

### `/recall` 스킬 설치

`/recall`은 `personal-os-skills` 저장소에 포함된 Claude Code
스킬이다. `.claude/skills/` 디렉터리에 파일을 복사해 설치한다.

<https://github.com/ArtemXTech/personal-os-skills>

Obsidian + Claude Code 환경을 처음 구성한다면 미리 설정된 스타터
킷을 사용할 수 있다.

<https://github.com/ArtemXTech/claude-code-obsidian-starter>

### `/recall` 스킬의 3가지 모드

- `temporal` — 날짜별 세션 히스토리 스캔
- `topic` — BM25로 컬렉션 전체 검색
- `graph` — 세션과 파일의 인터랙티브 시각화

작업 시작 전 `/recall topic <주제>`로 Claude에게 맥락을 로드하면,
직접 설명하는 과정 없이 바로 이어서 작업할 수 있다.

## 아키텍처

```
[Obsidian 볼트] → [QMD 인덱스] → [Claude Code / OpenClaw]
      ↑                 ↑
  Obsidian Sync    세션 종료 훅으로 자동 업데이트
```

Claude Code는 대화를 JSONL 파일로 저장한다. 세션 종료 훅이 이를
파싱 → QMD에 임베딩 → 항상 최신 인덱스 유지.

## 실사용 사례

- `"find the days when I was happy and what was the reason"` →
  수개월 일기에서 패턴 발견: 뭔가를 출시하고 수면 회복이 좋았던 날이
  가장 행복했다
- `"find the ideas I never acted on"` → 수개월 전 잊고 있던 아이디어
  (PhD 대시보드, 일러스트 앱 등) 발굴
- `topic` 검색으로 프로젝트 전체 상태 복원 후 "다음 최우선 액션은?"
  질문

## 인사이트

### 1. 컨텍스트가 유일한 장기 자산이다

> "A month from now there are going to be new models. So what.
> If you have your context you can make it work in any situation."

모델은 빠르게 교체된다. 2026년 현재 Claude, Gemini, GPT-4o가
경쟁하고 있지만 6개월 뒤 판도는 달라져 있을 것이다. 이 주기에서
지속적으로 가치를 갖는 자산은 **본인이 쌓아온 맥락**뿐이다.
수백 시간의 설계 결정, 실패 이유, 시도했던 접근법이 담긴 세션
히스토리는 어떤 모델로도 활용할 수 있는 범용 자산이다.

도구에 최적화하지 말고 **맥락 자체를 소유하는 구조**를 만들어야
한다.

### 2. AI 에이전트의 기억 문제는 아직 미해결이다

Claude Code가 RAG 없이 grep을 쓰는 건 설계 실수가 아니라 현재
상태다. 에이전트의 장기 기억은 업계 전체가 아직 풀지 못한 문제다.

- **단기 기억**: 컨텍스트 윈도우 (수십만 토큰)
- **작업 기억**: CLAUDE.md, 프로젝트 설정
- **장기 기억**: ← 공백. 이 부분이 미해결이다

이 공백을 채우려면 사용자가 직접 외부 레이어를 구축해야 한다.
QMD + `/recall`은 그 공백을 채우는 하나의 구체적인 패턴이다.

### 3. 검색은 계층 구조다, 단일 도구가 아니다

grep → BM25 → Semantic → Hybrid로 이어지는 계층은 단순히 도구
교체가 아니라 **"무엇을 찾느냐"에 따른 적합한 레이어 선택**이다.

- 정확한 함수명, 에러 메시지 → grep/BM25로 충분
- "저번에 인증 문제 어떻게 해결했지?" → Semantic 필요
- "내가 행복했던 날의 공통점은?" → 반드시 Semantic

문제는 대부분의 도구가 단일 레이어만 제공한다는 것이다. 검색
계층을 의식적으로 설계해야 한다.

### 4. 브루트포스 접근의 숨겨진 비용

"모든 파일을 grep해서 찾아"라고 하면 Claude가 실제로 그렇게 한다.
문제는 이게 느리고 토큰을 많이 쓸 뿐 아니라, **결과의 질도 나쁘다**
는 점이다. 노이즈가 많은 상위 결과를 모델이 처리하면 정작 중요한
내용이 묻힌다.

벡터 검색 기반 접근이 토큰을 40% 이상 줄이는 이유는 단순히 검색
속도 때문이 아니다. **검색 품질이 높아지면 Claude가 더 적은 컨텍스트
로 더 정확하게 답할 수 있기 때문이다.**

### 5. 마찰이 0이 되어야 습관이 된다

세션 히스토리를 수동으로 정리하겠다고 마음먹으면 절대 지속되지
않는다. 훅으로 자동화해야 한다. 이건 생산성 팁이 아니라 **시스템
설계 원칙**이다.

행동 변화 연구에서 반복적으로 확인된 것: 마찰이 1%만 줄어도 채택률
은 기하급수적으로 높아진다. 세션 종료 훅이 QMD 인덱스를 자동
갱신하는 구조가 없었다면 이 시스템은 3일 만에 사용하지 않게 됐을
것이다.

**좋은 시스템은 사용자가 의식하지 않아도 작동한다.**

### 6. PKM과 AI 에이전트의 통합이 시작됐다

Obsidian 볼트를 단순한 노트 앱이 아니라 **AI 에이전트의 장기 기억
저장소**로 쓰는 패턴이다. 이 관점 전환이 중요하다.

개인 지식 관리(PKM)와 AI 에이전트는 별개의 도구로 존재해 왔다.
하지만 에이전트가 나의 일기, 설계 노트, 세션 히스토리를 전부 검색할
수 있다면, 에이전트는 단순한 코드 도우미가 아니라 **나의 두뇌를
확장하는 시스템**이 된다.

앞으로 PKM 도구와 AI 에이전트의 경계는 점점 희미해질 것이다.
이 통합을 먼저 설계하는 사람이 생산성에서 비대칭적인 우위를 가진다.

## 스킬 내부 분석

`personal-os-skills` 저장소의 `skills/recall/` 구조:

```
recall/
├── SKILL.md              # 스킬 정의 (frontmatter + 설명)
├── scripts/
│   ├── extract-sessions.py   # JSONL → 마크다운 변환
│   ├── recall-day.py         # 날짜별 세션 조회
│   └── session-graph.py      # 인터랙티브 그래프 생성
└── workflows/
    └── recall.md         # 쿼리 라우팅 로직
```

### SKILL.md — 스킬 진입점

```yaml
allowed-tools: Bash(qmd:*), Bash(python3:*)
```

Claude가 이 스킬 안에서 실행할 수 있는 도구를 `qmd`와 `python3`로
제한한다. 허용 범위를 명시해야 Claude Code가 스킬을 실행할 수 있다.

트리거 문구 목록이 description에 직접 포함돼 있다.

```
"recall", "what did we work on", "load context about",
"remember when we", "prime context", "yesterday", ...
```

Claude가 사용자 입력을 보고 이 스킬을 언제 실행할지 판단하는 기준이다.

### workflows/recall.md — 쿼리 라우팅

입력을 4가지로 분류한다.

- **Graph**: 세션-파일 관계 시각화
- **Temporal**: 날짜 범위로 세션 조회
- **Topic**: BM25 키워드 검색
- **Hybrid**: Temporal + Topic 조합

Topic 검색 시 **쿼리 확장**을 적용한다. 사용자가 입력한 표현과 실제
세션 내용의 어휘가 다를 수 있기 때문에 LLM이 동의어·관련어 3~4개를
생성해 병렬 검색한다. BM25가 Hybrid보다 53배 빠르기 때문에 Topic
쿼리에는 BM25를 우선 사용한다.

모든 recall은 **"One Thing"** 으로 끝난다. 검색 결과를 바탕으로
"지금 당장 가장 높은 레버리지를 가진 다음 액션 하나"를 구체적으로
제시한다. 일반적인 요약이 아니라 실행 가능한 다음 단계다.

### scripts/extract-sessions.py — JSONL 파이프라인

Claude Code는 모든 대화를 `~/.claude/projects/{encoded-cwd}/*.jsonl`
에 저장한다. 이 스크립트가 그 파일을 파싱한다.

**처리 흐름:**

```
JSONL 파일
  → role == "user" 메시지만 추출
  → 시스템 태그 제거 (<system-reminder>, <command-name> 등)
  → 슬래시 커맨드 단독 입력 제거
  → 세션 제목 자동 추출 (첫 의미있는 메시지에서)
  → YYYY-MM-DD-HHMM-{session_id[:8]}.md 로 저장
```

어시스턴트 응답은 저장하지 않는다. 사용자가 입력한 내용만 인덱싱해
노이즈를 줄이고 인덱스 크기를 최소화한다.

출력 파일은 QMD 컬렉션으로 바로 추가할 수 있도록 frontmatter를
포함한다.

```yaml
---
date: 2026-02-25
session_id: abc12345-...
title: "Docker 컨테이너 네트워크 설정"
type: session-log
messages: 12
---
```

### scripts/session-graph.py — 그래프 시각화

Claude의 도구 호출 로그(Read, Edit, Write, Glob, Grep, Bash)에서
파일 경로를 추출해 **세션 ↔ 파일** 관계 그래프를 만든다.

- 노드: 세션(날짜별 색상) + 파일(폴더별 색상)
- 엣지: 세션이 해당 파일을 수정·참조한 관계
- 노이즈 제거: 세션의 60% 이상에서 등장하는 공통 파일 제외
- 출력: `/tmp/session-graph.html` (브라우저에서 바로 열림)

시각화에 NetworkX + Pyvis를 사용하며, Obsidian 스타일의 다크 테마를
적용한다.

## 관련 항목

- [QMD](../llm/qmd.md)
