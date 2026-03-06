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

**모델 독립적인 맥락 레이어가 핵심이다.** 저자의 말:

> "A month from now there are going to be new models. So what.
> If you have your context you can make it work in any situation."

Claude Code든 Gemini CLI든, 도구가 바뀌어도 맥락은 남는다. AI
도구의 빠른 교체 주기 속에서 지속적으로 가치를 갖는 자산은 모델이
아닌 **컨텍스트**다.

**토큰 절감 효과도 크다.** grep 방식 대비 벡터 검색 기반 접근이
토큰 사용량을 40% 이상 감소시킨다.

**마찰을 없애야 습관이 된다.** 세션 종료 시 자동으로 인덱스를
갱신하는 훅이 없으면 실제 사용으로 이어지지 않는다. 자동화가
채택률을 결정한다.

## 관련 항목

- [QMD](../llm/qmd.md)
