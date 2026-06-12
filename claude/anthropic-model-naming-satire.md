# Anthropic 모델 이름 짓기, 외삽해보면

원문: <https://samwilkinson.io/posts/2026-06-09-anthropics-model-naming-extrapolated>

## 요약

Sam Wilkinson이 쓴 짧은 풍자 글이다.
Anthropic이 Claude Fable을 출시하면서 모델 이름을 시(詩)에서 “기업 규모 서사 객체”로 진화시키고 있다는 관찰에서 출발한다.
필자는 이 명명 패턴을 논리적으로 끝까지 밀어붙여, Anthropic이 “문학 스택 전체”를 커버하는 모델 포트폴리오를 개발 중이라고 상상한다.

원문의 핵심은 아래 표다.
각 모델 이름은 실제 존재하거나 존재할 법한 제품을 가리키고, 설명은 그 이름이 암시하는 행동 방식을 한 줄로 비틀어 표현한다.

| Model Name                          | Description                                                   |
| ----------------------------------- | ------------------------------------------------------------- |
| Aphorism                            | One sentence, but it always feels right                       |
| Haiku                               | Small poem, small bill                                        |
| Marginalia                          | Provides unprompted commentary on your code                   |
| Abstract                            | Summarizes reasoning it hasn't done                           |
| Sonnet                              | Medium poem, medium bill                                      |
| Diatribe                            | Sonnet, but angry                                             |
| Opus                                | Long poem, entire bill                                        |
| Treatise                            | Opus, but citation is left as an exercise for the reader      |
| Mythos                              | Opus, but scary                                               |
| Fable                               | Mythos, until the question matters                            |
| Fable (xhigh)                       | Bankruptcy speedrun                                           |
| Saga                                | Fable, but with extra meandering                              |
| Saga (Unabridged)                   | Includes answers to unrelated questions                       |
| Lore                                | Interpretation requires a wiki                               |
| Cinematic Universe                  | Multiple Sagas with a Lore dispatch layer                     |
| Cinematic Universe (Director's Cut) | Same answer, 42% more tokens                                  |
| Terms of Service                    | No liability for answers or the consequences thereof          |
| Overwhelmingly Large Narrative Unit | Requires viewing a “previously on” segment prior to usage     |
| Omnibus                             | Fine-tuning will continue until morale improves               |

## 풍자의 포인트

### 가격 구조와 품질의 비선형 관계

Haiku/Sonnet/Opus 3단 구조는 “작은 시/중간 시/긴 시”이면서 동시에 “작은 청구서/중간 청구서/전체 청구서”다.
필자는 이 대응을 글자 그대로 표로 만들어버림으로써, AI 모델 가격표가 사실상 문학 형식의 길이 계층을 그대로 베낀 것임을 노출한다.
Fable (xhigh)를 “Bankruptcy speedrun”으로 묘사한 것은 추론 모델의 확장 사고(extended thinking) 과금 구조가 얼마나 빠르게 비용을 폭발시킬 수 있는지를 겨냥한다.

### 모델 능력과 실제 동작의 간극

Abstract는 “Summarizes reasoning it hasn't done”이고, Marginalia는 “Provides unprompted commentary on your code”다.
이 두 항목은 각각 환각(hallucination)과 과잉 도움(over-helpfulness)을 가리킨다.
Fable은 “Mythos, until the question matters”인데, 이는 어려운 질문 앞에서 모델이 갑자기 신중해지거나 거부하는 패턴을 꼬집는다.
Treatise의 “citation is left as an exercise for the reader”는 출처 없는 자신감 있는 서술이라는 고질적 문제를 학술 관행의 언어로 비튼다.

### 복잡성 증가와 시스템 불투명성

Cinematic Universe는 “Multiple Sagas with a Lore dispatch layer”로, 멀티 에이전트 오케스트레이션 아키텍처를 마블 세계관에 빗댄다.
Lore가 “Interpretation requires a wiki”인 것은 모델 동작을 이해하기 위해 점점 더 두꺼워지는 문서와 커뮤니티 지식이 필요해지는 현실을 짚는다.
Saga (Unabridged)가 “Includes answers to unrelated questions”인 것은 컨텍스트 윈도우가 커질수록 모델이 관련 없는 정보까지 끌어들이는 경향을 묘사한다.
Overwhelmingly Large Narrative Unit의 “previously on” 세그먼트는 긴 대화 세션에서 모델이 이전 맥락을 요약해야 하는 기술적 필요를 드라마 시리즈의 “지난 줄거리”로 표현한다.

## 인사이트

### 명명 인플레이션은 기대치 인플레이션을 반영한다

Haiku에서 Omnibus까지의 이름 진화는 단순한 마케팅 변화가 아니다.
각 이름은 암묵적으로 새로운 능력 수준을 약속하고, 사용자는 그 이름에서 기대치를 형성한다.
풍자가 드러내는 것은, 이름이 커질수록 실제 능력과 기대치 사이의 간극도 커진다는 점이다.
Terms of Service가 “No liability for answers or the consequences thereof”로 끝나는 것은 이 간극의 법적·제도적 해소 방식이 무엇인지를 냉소적으로 요약한다.

### 문학 은유는 AI의 불확실성을 포장한다

시 형식을 모델 이름으로 쓰는 것은 중립적 선택이 아니다.
시는 해석의 여지를 전제로 한다.
Haiku는 여백이 의미를 만들고, Opus는 장대함이 가치를 보증한다는 인상을 준다.
이 은유 체계를 끝까지 밀면 Omnibus나 Lore처럼 “해석이 필요한 텍스트”가 된다.
풍자는 그 은유 자체가 AI 출력의 모호성과 비결정성을 문화적으로 정당화하는 기제임을 드러낸다.

### 웃음은 불안의 형식이다

이 글이 재미있는 이유는 묘사된 행동들이 낯설지 않기 때문이다.
Diatribe(화난 Sonnet), Saga(meandering Fable), Cinematic Universe(복잡한 멀티에이전트)는 모두 현재 AI 시스템을 쓰면서 실제로 경험하는 불편함을 이름으로 만든 것이다.
풍자가 효과적인 것은 정확히 이 지점, 즉 “우리가 이미 알고 있지만 공식적으로는 말하지 않는 것”을 말하기 때문이다.
