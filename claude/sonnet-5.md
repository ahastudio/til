# Claude Sonnet 5 출시

[Introducing Claude Sonnet 5 \\ Anthropic](https://www.anthropic.com/news/claude-sonnet-5)

[What's new in Claude Sonnet 5 - Claude Platform Docs](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5)

HN 토론: <https://news.ycombinator.com/item?id=48736605> (1044점, 610개 댓글)

## 공식 트윗

1️⃣

> Introducing Claude Sonnet 5, our most agentic Sonnet yet.
> It makes plans, uses tools like browsers and terminals, and runs autonomously
> at a level that just a few months ago required larger and more expensive models.
>
> — [@claudeai](https://twitter.com/claudeai/status/2072017450611142835)

2️⃣

> Sonnet 5 is a substantial improvement over Sonnet 4.6 on reasoning, tool use,
> coding, and knowledge work.
> Its performance is close to Opus 4.8, at lower prices.
>
> — [@claudeai](https://twitter.com/claudeai/status/2072017452335087996)

## 모델 개요

Claude Sonnet 5는 2026년 6월 30일 출시된 Anthropic의 새 Sonnet 계열 모델이다.
Anthropic은 "가장 에이전트 지향적인 Sonnet 모델"이라고 소개하며,
Opus 4.8 수준의 성능에 근접하면서도 같은 가격대를 유지한다고 밝혔다.
API 모델 ID는 `claude-sonnet-5`다.

## 성능 및 벤치마크

Sonnet 4.6 대비 가장 큰 향상은 코딩과 에이전트 작업에서 나타난다.

에이전트 검색 벤치마크인 BrowseComp에서 비용 대비 성능이 우수하며,
컴퓨터 사용 벤치마크인 OSWorld-Verified에서도 Sonnet 4.6을 크게 앞선다.
더 높은 effort 수준에서는 Opus 4.8 수준에 도달한다.

## API 주요 변경 사항

Sonnet 5는 Sonnet 4.6의 드롭인 대체 모델이지만, 세 가지 동작이 바뀌었다.

**Adaptive thinking 기본 활성화.** 기존에는 `thinking` 필드를 지정하지 않으면
thinking 없이 실행됐지만, Sonnet 5부터는 adaptive thinking이 기본값이다.
끄려면 `thinking: {type: "disabled"}`를 명시해야 한다.
`max_tokens`는 thinking 토큰을 포함한 전체 출력 한도이므로 기존 설정을 재검토해야
한다.

**샘플링 파라미터 제거.** `temperature`, `top_p`, `top_k`를 기본값 외의 값으로
설정하면 400 에러가 반환된다.
마이그레이션 시 해당 파라미터를 제거하고, 모델 동작 조정은 시스템 프롬프트로
대신해야 한다.
이 제약은 Opus 4.7에서 먼저 도입된 것이다.

**Manual extended thinking 제거.** Sonnet 4.6에서 deprecated됐던
`thinking: {type: "enabled", budget_tokens: N}` 방식이 Sonnet 5에서 완전히
제거됐다.
Adaptive thinking과 `effort` 파라미터로 대체한다.

```python
# Sonnet 5에서 동작하지 않음 (400 에러)
thinking = {"type": "enabled", "budget_tokens": 32000}

# 대신 이렇게 사용
thinking = {"type": "adaptive"}
```

## 새 토크나이저

Sonnet 5는 새로운 토크나이저를 사용한다.
같은 텍스트에 대해 Sonnet 4.6보다 약 30% 더 많은 토큰이 생성된다.
API 요청/응답 형태는 바뀌지 않으므로 코드 변경은 필요 없지만,
다음 사항을 확인해야 한다.

- 토큰 수 측정값과 비용 추정을 Sonnet 5 기준으로 다시 측정해야 한다.
- 컨텍스트 윈도우는 1M 토큰으로 동일하지만, 토큰당 텍스트 양이 줄어 실제 담을 수
  있는 텍스트 분량이 감소한다.
- `max_tokens` 한도를 출력 예상 길이 근처로 설정해 둔 경우 잘릴 수 있다.
- 토큰당 가격은 동일하지만, 같은 텍스트에 더 많은 토큰이 소요되므로 실질 비용이
  달라진다.

## 사양

컨텍스트 윈도우는 기본값이자 최댓값으로 1M 토큰이다.
최대 출력은 128k 토큰이다.
Priority Tier는 지원하지 않는다.
어시스턴트 메시지 프리필링은 Sonnet 4.6과 동일하게 지원하지 않는다.

## 가격

| 구분   | 도입 가격 (~2026-08-31) | 표준 가격 (2026-09-01~) |
| ------ | ----------------------- | ----------------------- |
| 입력   | $2 / 1M 토큰            | $3 / 1M 토큰            |
| 출력   | $10 / 1M 토큰           | $15 / 1M 토큰           |

## 사이버보안 안전장치

Sonnet 5는 Sonnet 계열 모델 중 처음으로 실시간 사이버보안 안전장치를 적용한다.
금지되거나 고위험 사이버보안 주제를 포함한 요청은 거부될 수 있다.
거부는 HTTP 에러가 아닌 200 응답으로 전달되며, `stop_reason: "refusal"`로
구분한다.

## 가용성

다음 플랫폼에서 이용할 수 있다.

- Claude API (전체 고객 대상)
- AWS Bedrock (신형 API 한정; 레거시 `InvokeModel`/`Converse` API는 미지원)
- Google Cloud Vertex AI
- Microsoft Foundry (프리뷰)
- Claude 앱 (Free, Pro, Max, Team, Enterprise 전 플랜)

## 마이그레이션

모델 ID만 변경하면 기본 마이그레이션은 완료된다.

```python
model = "claude-sonnet-4-6"  # 변경 전
model = "claude-sonnet-5"    # 변경 후
```

이후 세 가지를 점검해야 한다.

1. 토큰 예산과 `max_tokens` — 새 토크나이저 기준으로 재측정한다.
2. Extended thinking — `budget_tokens` 방식을 adaptive thinking으로 교체한다.
3. 샘플링 파라미터 — `temperature`, `top_p`, `top_k` 설정을 제거한다.

## 분석

### 에이전트 방향으로의 전환

Sonnet 계열이 "에이전트 지향"을 전면에 내세운 것은 이번이 처음이다.
기존 Sonnet이 속도와 비용 균형을 강조했다면, Sonnet 5는 에이전트 작업에서의
실질적 완수 능력을 핵심 차별점으로 제시한다.
이는 AI 활용 패턴이 단발성 질의에서 다단계 자율 작업으로 이동하는 흐름을 모델
포지셔닝에 반영한 것이다.
그러나 커뮤니티 일각에서는 "에이전트 최적화가 보조 개발(assisted development)에는
오히려 퇴보"라는 반응도 나왔다.[^microtonal]
자율 실행에 적합하게 튜닝된 모델이 사람과 함께 작업하는 맥락에서는
맞지 않을 수 있다는 지적이다.

### API 설계 철학의 변화

세 가지 변경 사항 — adaptive thinking 기본화, 샘플링 파라미터 제거,
manual extended thinking 제거 — 은 개별적으로 보면 제약처럼 보이지만,
함께 보면 일관된 방향을 가리킨다.
Anthropic이 모델의 동작 제어권 일부를 개발자에서 모델 자체로 가져오는 방향이다.
샘플링 파라미터를 직접 조정하는 대신 시스템 프롬프트로 유도하고,
thinking 예산을 수동으로 지정하는 대신 모델이 스스로 필요한 만큼 사용하게 한다.
Opus 4.7에서 시작된 이 방향이 Sonnet 계열에도 확장됐다.

### Effort 수준별 비용 구조

"더 높은 effort 수준에서는 Opus 4.8 수준에 도달한다"는 공식 설명과 달리,
실제 비용 분석에서는 다른 결론이 나온다.
medium effort를 초과하면 작업당 비용이 Opus 4.8을 넘어선다는 것이다.[^doctoboggan]
즉 고성능이 필요한 작업은 Sonnet 5 high effort보다 Opus 4.8 low effort가
더 경제적이라는 판단이다.[^johnfahey]
Sonnet 5가 가장 의미 있는 구간은 low~medium effort의 대량 처리 작업이다.

### 토크나이저 교체의 실질적 영향

30% 더 많은 토큰이 생성된다는 것은 단순한 기술 노트가 아니다.
기존 Sonnet 4.6 기준으로 조정된 `max_tokens`, 토큰 비용 예측, 컨텍스트 관리
로직이 모두 영향을 받는다.
API 호환성은 유지되지만 비용과 동작이 달라질 수 있어,
대규모 트래픽을 처리하는 서비스라면 마이그레이션 전 충분한 검증이 필요하다.
실측에 따르면 토큰 증가폭은 콘텐츠 유형에 따라 1.0~1.35배로 다르게 나타났다.[^m3h]
"약 30%"는 평균치이며, 특정 입력 유형에서는 그 차이가 더 클 수 있다.

## 비평

### 강점

에이전트 작업에 특화된 포지셔닝은 명확하다.
BrowseComp와 OSWorld-Verified 결과를 투명하게 공개하고,
API 변경 사항을 상세한 마이그레이션 가이드와 함께 제공한 점은
개발자 경험을 고려한 출시 방식이다.
Opus 4.8에 근접한 성능을 같은 가격에 제공한다는 메시지도 실용적이다.

### 약점

토크나이저 교체에 따른 비용 변동이 얼마나 현실적으로 영향을 미치는지
구체적인 사례가 부족하다.
"약 30% 더 많은 토큰"이라는 수치가 어떤 텍스트 유형에서 측정된 것인지,
코드, 한국어, 긴 문서 등 상황별로 차이가 있는지에 대한 정보가 없다.

토크나이저 교체를 사실상의 가격 인상으로 읽는 시각도 있다.[^ianberdin]
토큰당 단가는 유지됐지만 같은 텍스트에 더 많은 토큰이 소요되므로,
도입 할인 기간이 끝난 뒤 실질 비용이 Sonnet 4.6보다 높아진다는 계산이다.

샘플링 파라미터 제거는 기존 워크플로에 따라 마이그레이션 비용이 클 수 있다.
temperature를 세밀하게 조정하며 사용하던 애플리케이션은 시스템 프롬프트 기반의
대안을 별도로 검토해야 한다.

사이버보안 안전장치와 관련해서는 역설적인 지적도 제기됐다.[^Sol-]
보안 관련 지식을 제한하면 모델이 안전한 코드를 작성하는 능력도 함께 줄어들
수 있다는 논리다.
사이버보안 역량은 공격과 방어에 모두 필요한 지식이기 때문이다.

## 인사이트

### 에이전트 AI에서 "완수"가 핵심 지표가 되다

속도와 정확도 중심이던 언어 모델 평가 기준이 에이전트 맥락에서는 "완수율"로 이동하고
있다.
BrowseComp와 OSWorld 같은 벤치마크는 단일 질의 응답이 아니라 다단계 작업의
끝까지 해내는 능력을 측정한다.
Sonnet 5가 "이전에 중단되던 작업을 끝까지 완료"한다는 사용 후기는,
에이전트 AI에서 가장 중요한 것이 지식의 깊이가 아니라 작업 지속성임을 보여준다.

### 제어권 이양은 점진적이다

샘플링 파라미터 제거와 adaptive thinking 기본화는 개발자 관점에서 불편함을 줄 수
있다.
그러나 이 방향의 장기적 함의는 모델이 더 자율적으로 판단하도록 설계된다는 것이다.
Anthropic이 Opus 계열에서 먼저 적용하고 Sonnet 계열로 확장하는 방식은,
이 변화를 단계적으로 생태계에 적응시키는 전략이다.
개발자 입장에서는 지금 마이그레이션 비용을 치르지만, 그 방향으로 가는 것 자체는
피하기 어렵다.

### 1M 컨텍스트가 기본값인 시대

Sonnet 5는 1M 토큰 컨텍스트를 기본값이자 유일한 옵션으로 제공한다.
더 작은 변형이 없다는 점은 모델 선택의 복잡성을 줄인다.
다만 새 토크나이저로 인해 실제 담을 수 있는 텍스트 분량이 Sonnet 4.6보다 줄어든다는
점은, 컨텍스트 윈도우 크기만으로 실질 용량을 가늠하기 어렵게 만드는 요소다.

---

[^doctoboggan]: <https://news.ycombinator.com/item?id=48736821>
[^johnfahey]: <https://news.ycombinator.com/item?id=48736861>
[^microtonal]: <https://news.ycombinator.com/item?id=48736833>
[^ianberdin]: <https://news.ycombinator.com/item?id=48740299>
[^m3h]: <https://news.ycombinator.com/item?id=48737851>
[^Sol-]: <https://news.ycombinator.com/item?id=48736907>
