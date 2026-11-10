# Muse Ember: Meta가 가장 작은 모델로 비용 대비 지능 곡선의 앞쪽을 노린다

원문: [Introducing Our Smallest, Most Efficient Model: Muse Ember](https://research.meta.ai/blog/muse-ember)

HN 토론: <https://news.ycombinator.com/item?id=50429024> (256점, 108개 댓글)

## 요약

### 무엇을 내놓았는가

Meta AI Research는 2026년 11월 9일 글에서 가장 작고 효율적인 모델 Muse Ember를
공개했다.
복잡한 추론 실행과 에이전트가 하루 종일 반복하는 일, 곧 도구 호출,
코딩 하위 작업, 라우팅, 추출, 긴 문서 분석을 위해 설계했다고 한다.
텍스트, 이미지, 음성, 영상을 원래부터 이해하며,
컨텍스트 창은 100만 토큰, 출력은 최대 51만 2천 토큰이다.
모델 ID는 `muse-ember-1.0`이고 Muse Code와 Meta Model API에서 쓸 수 있으며
Responses API를 지원한다.
가격은 입력 100만 토큰당 0.10달러, 캐시된 입력 0.004달러,
출력 0.50달러이고, 20만 토큰을 넘는 프롬프트는 0.30달러, 0.012달러, 1.50달러다.
글 끝에서 Muse Ember, Muse Spark, Muse Wonder가 Google Cloud와 Oracle Cloud에도
올라왔다고 한다.

### 성능 주장

글의 핵심 주장은 Ember가 Claude Haiku 5.5와 GPT-6 Luna보다 모든 추론 설정에서
달러당 지능이 높다는 것이다.
Haiku의 최고 점수에 약 3분의 1 비용으로 맞추고 Luna의 모든 설정을 넘으며,
Artificial Analysis 전체 순위표에서도 더 적은 비용에 더 높은 점수를 내는 모델이
없다는 효율 경계(efficiency frontier)에 있다고 한다.
Artificial Analysis 지능 지수에서 Ember(max)는 36으로 Spark 1.3(max)의 37에
가깝고, 지능 지수 과제당 비용은 0.14달러로 Spark 1.3의 2.39달러보다 훨씬
낮다.
가격은 Spark 1.3이 입력 1.25달러, 출력 4.25달러다.

### 벤치마크 비교(max 추론 설정)

| 평가                                              | Muse Ember | Claude Haiku 5.5 | GPT-6 Luna |
| ------------------------------------------------- | ---------- | ---------------- | ---------- |
| AutomationBench-AA                                | 37.8       | 13.9             | 20.2       |
| Agents' Last Exam (Meta 내부)                     | 61.6       | 57.0             | 57.1       |
| Personal Superintelligence Index (Meta 내부 종합) | 46.8       | 36.1             | 37.0       |
| Terminal-Bench 4.0                                | 40.9       | 39.2             | 16.4       |
| Coding Agent Index-AA                             | 46         | 37               | 31         |
| FrontierCode 2.0-AA                               | 27.2       | 34.9             | 25.2       |
| GDP.pdf-AA                                        | 22.8       | 20.8             | 22.8       |
| OSWorld 2.1 (부분 점수, Meta 내부)                | 69.5       | 68.9             | 50.5       |
| PerceptionBench (도구 사용, Meta 내부)            | 80.6       | 78.6             | 62.8       |
| Artificial Analysis 지능 지수                     | 36         | 36               | 28         |

각주는 모든 모델이 max 추론 노력에서 돌았고,
Terminal-Bench 4.0은 모델마다 가장 좋은 공개 하네스(Ember는 mini-swe-agent,
Haiku는 Claude Code, Luna는 Codex)를 썼으며,
Personal Superintelligence Index는 Agents' Last Exam, AutomationBench,
FocusBench,
JobBench, OfficeQA Pro, GDP.pdf, GDP.xlsx, VBT의 여덟 평가로 된 Meta의 내부 종합
지표라고 밝힌다.

### 파트너 평가와 위치

Box는 계약서를 협상 지침에 대조해 조항별로 점수를 매기는 평가를,
Cline은 하네스의 하위 에이전트로 쓰는 비용 절감을,
Cloudflare는 꼬리 지연이 비교 모델보다 최대 30% 빠르다는 점을,
You.com은 p95 지연 2.2초가 선두 오픈 웨이트 모델보다 4배에서 13배 빠르고 출력
토큰이 36~48% 적다는 점을 말한다.
글은 Ember가 Muse Wonder Full로 훈련한 첫 모델이며,
가장 어려운 문제에는 Wonder, 코딩과 에이전트에는 Spark,
대규모 반복 작업에는 Ember를 쓰는 포트폴리오를 완성한다고 말한다.
안전 평가는 Meta Superintelligence Scaling Framework 아래에서 화학과 생물,
사이버 보안, 통제 상실 위험 모두 높은 위험 임계 아래에 있었다고 한다.

## 분석

### 비교 축을 달러당 지능으로 옮겨 놓았다

글은 처음부터 최고 점수가 아니라 비용 대비 점수를 앞세운다.
절대 성능에서는 Haiku 5.5(max)가 지능 지수 36.2로 Ember의 최고 35.8과 같은
수준이고, 이긴 곳은 같은 점수에 드는 비용이다.
Haiku는 가장 높은 설정에서 과제당 0.411달러, Ember는 0.136달러다.
이 틀에서 작은 모델의 경쟁력은 정확도가 아니라 가격 곡선의 위치다.
같은 방식으로 Spark 1.3과도 비교해 지수 1점 차이에 비용이 17배 낮다는 점을
보인다.

### 에이전트 하위 작업이라는 시장을 정의한다

글은 에이전트가 토큰의 대부분을 작고 구조화된 많은 단계에 쓴다고 말하고,
Ember를 그 단계에 맞춘 모델로 자리매김한다.
하나의 큰 모델이 계획하고 작은 모델이 물량을 처리하는 구조(Wonder가 계획하고
Ember가 처리량을 맡는다는 글의 문장)가 전제다.
이 전제에서는 작은 모델의 평가축이 지연, 비용, 도구 호출 신뢰도로 바뀐다.
파트너 인용도 하위 에이전트와 처리량을 말한다.

### 큰 모델에서 작은 모델로 가는 증류의 흐름

글은 Ember가 Muse Wonder Full로 훈련한 첫 모델이며,
Wonder 출시 때 말한 특화 모델의 첫 결과라고 설명한다.
훈련 방법은 이 글에 없지만, 가장 큰 모델이 더 작은 모델을 만들어 내는
파이프라인이 제품군 전략의 중심이라는 점은 읽힌다.

## 비평

### 평가 조건이 비교를 Ember 쪽으로 기울인다

가장 눈에 띄는 것은 Terminal-Bench 4.0의 하네스 선택이다.
모델마다 가장 좋은 공개 하네스를 썼다는 설명은 공정해 보이지만,
Ember는 오픈소스 mini-swe-agent, Haiku는 Claude Code, Luna는 Codex라서
하네스의 차이가 모델의 차이로 읽힐 수 있다.
Agents' Last Exam(Linux 부분집합), OSWorld 2.1, PerceptionBench는 Meta 내부
평가이고 Personal Superintelligence Index는 Meta가 만든 종합 지표다.
Artificial Analysis의 외부 평가 항목에서는 Ember가 반드시 앞서지 않는다.
FrontierCode 2.0-AA에서는 Haiku 34.9가 Ember 27.2보다 높고,
GDP.pdf-AA는 Luna와 같은 22.8이다.
글은 이를 숨기지 않고 표에 두었지만 요약 문장은 이 사실을 말하지 않는다.

### 비용 숫자의 기준이 섞여 있다

첫 도표의 설명은 Ember의 비용이 제안 가격 기준의 추정이라고 하고,
같은 도표의 아래 문구는 목록 가격 기준이라고 한다.
글 끝의 각주는 과제당 비용을 각 모델의 목록 가격으로 계산한다고 적는다.
이번에 읽은 텍스트로는 이 두 표현이 같은 값인지 알 수 없다.
가격이 확정된 뒤의 값이라면 문제가 없지만,
추정치가 한 도표에 섞여 있다는 사실은 기록해 둔다.

### 효율 경계의 주장은 한 순위표에 기대어 있다

가장 강한 주장(어떤 모델도 더 적은 비용에 더 높은 점수를 내지 못한다)은
Artificial Analysis의 한 순위표와 그 지수의 구성에 달려 있다.
이 순위표는 Meta가 마련한 것이 아니지만, 모델 제작사가 자기에게 유리한 지수
위에서 비교를 고르는 구조는 이 글에서 그대로 나타난다.
DeepSeek와의 비교가 없다는 지적도 HN에 나왔다.[^v9v]

### 오픈 웨이트가 아니라는 점이 반응의 큰 부분이었다

HN에서 한 사용자는 가장 작은 모델이라는 말에 오픈 웨이트를 기대했는데 가중치를
찾을 수 없어 아쉽다고 썼고,[^Retro_Dev]
다른 사용자는 Spark Open이 10월에 나왔다고 기다리라고 답했다.[^loeg]
또 다른 사용자는 오픈이 아니면 중국의 출시를 기다리겠다고 했다.[^mococa]
공개 가중치는 이 모델의 설계 대상(에이전트 하위 작업)에서 특히 중요한 요구여서,
글이 이를 다루지 않은 것이 눈에 띈다.

### 긴 호흡의 에이전트 작업에서의 성능은 이 글이 말하지 않는다

글은 에이전트가 하루 종일 반복하는 일을 대상으로 하지만 보여 주는 평가는 대부분
한 번의 과제 점수다.
HN의 한 사용자는 스텔스 모델 crouton alpha가 이 모델이라고 믿는다고
썼고,[^open-paren]
다른 사용자는 그 모델을 많이 썼는데 시작은 강하지만 10턴쯤 되면 나빠지고
20턴이면 쓸 수 없고, 짧은 작업에는 좋고 긴 작업에는 형편없다고
했다.[^OsrsNeedsf2P]
두 모델이 같다는 것은 확인되지 않았고 이 문서가 확인하지 못했다.
다만 하위 에이전트 작업이 여러 턴에 걸쳐 일관성을 유지하는지는 글의 단일 점수가
말해 주지 않는다.

## 인사이트

### 소형 모델의 경쟁이 가격표의 캐시 항목으로 옮겨 간다

HN에서 한 사용자는 Ember의 캐시된 입력 값이 일반 입력의 4%여서 Luna와 Haiku의
10%보다 낮다고 짚었다.[^minimaxir]
에이전트는 같은 맥락을 반복해 읽으므로 캐시 가격이 총비용을 크게 좌우한다.
모델 가격 경쟁의 축이 입력과 출력의 단가에서 캐시 적중 때의 단가로 옮겨 가고
있다는 것을 이 사소한 항목이 보여 준다.
이것은 이 문서의 해석이다.

### 추론 노력과 품질의 상관이 약한 모델은 평가를 어렵게 한다

HN에서 Simon Willison은 여섯 단계 노력 수준에서 펠리컨 SVG를 그렸더니
(high는 완전한 SVG를 내지 못했다) 추론 토큰이 많아도 눈에 띄게 나은 SVG가
나오지 않았다고 썼다.[^simonw]
평소에는 생각 수준과 시각 품질이 꽤 강하게 상관하는데 이 모델에서는 그 상관이
처음으로 깨졌다는 것이다.
이것이 일반적인 현상인지는 한 사용자의 한 시험이어서 알 수 없다.
다만 노력 수준을 비용 곡선의 축으로 쓰는 글의 도표가 모델마다 노력 대 품질의
관계가 다르다는 사실을 가린다는 점이 이 일화에서 드러난다.

### 모델이 너무 많다는 피로가 시장의 신호다

HN에서 한 사용자는 모델 갱신에 지쳤다고 썼고,[^cheesecompiler]
다른 사용자는 따라잡고 가치를 가늠하는 일이 전업이 되었다고 했다.[^PaulKeeble]
다른 사용자는 초기 PC 시절처럼 결국 몇 가지 모양으로 굳어져 특화 모델로 갈
것이라고
예상했다.[^kbrannigan]
Meta가 Wonder, Spark, Ember로 포트폴리오를 가른 것은 이런 특화를 먼저 내세운
것이다.
선택지가 많아질수록 모델 선택 자체가 비용이 되므로, 가격표와 순위표 위에 얹힌
추천기가 다음 단계의 제품이 될 것이다.

---

[^v9v]: <https://news.ycombinator.com/item?id=50430725>

[^Retro_Dev]: <https://news.ycombinator.com/item?id=50431857>

[^loeg]: <https://news.ycombinator.com/item?id=50432210>

[^mococa]: <https://news.ycombinator.com/item?id=50430458>

[^open-paren]: <https://news.ycombinator.com/item?id=50429645>

[^OsrsNeedsf2P]: <https://news.ycombinator.com/item?id=50434838>

[^minimaxir]: <https://news.ycombinator.com/item?id=50430835>

[^simonw]: <https://news.ycombinator.com/item?id=50429478>

[^cheesecompiler]: <https://news.ycombinator.com/item?id=50431112>

[^PaulKeeble]: <https://news.ycombinator.com/item?id=50431700>

[^kbrannigan]: <https://news.ycombinator.com/item?id=50430375>
