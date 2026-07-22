# 구글의 Gemini 3.6 Flash, 3.5 Flash-Lite, 3.5 Flash Cyber

원문: [3\.6 Flash, 3.5 Flash-Lite, and 3.5 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/)

HN 토론: <https://news.ycombinator.com/item?id=48993414> (716점, 540개 댓글)

GN 토론: <https://news.hada.io/topic?id=31662>

## 요약

구글이 세 가지 새로운 Gemini 모델을 발표했다.
Gemini 3.6 Flash, Gemini 3.5 Flash-Lite, Gemini 3.5 Flash Cyber다.

**Gemini 3.6 Flash**는 코딩, 지식 작업, 멀티모달 성능을 강화한 모델이다.
DeepSWE 벤치마크에서 이전 세대보다 최대 65% 향상됐으며,
출력 토큰 사용량이 3.5 Flash 대비 17% 감소했다.
입력 토큰 가격은 백만 개당 1.50달러, 출력은 7.50달러다.

**Gemini 3.5 Flash-Lite**는 속도와 비용 효율을 최대화한 모델이다.
초당 350개의 출력 토큰을 처리하며
고처리량 에이전트 작업에 최적화됐다.
입력 토큰 가격은 백만 개당 0.30달러, 출력은 2.50달러다.

**Gemini 3.5 Flash Cyber**는 코드 보안 취약점 발견과 수정을 위해 미세조정된 모델이다.
현재 CodeMender 내 제한된 파일럿 프로그램으로 정부 및 신뢰 파트너에게만 제공된다.

## 분석

### Pro 모델 없이 Flash 라인업만 출시한 배경

이번 발표에서 눈에 띄는 것은 대형 Pro 모델 없이 Flash 계열만 나왔다는 점이다.
Hacker News 사용자 postalcoder는 세 가지 가능성을 제시했다.[^postalcoder]
모델이 너무 커서 경제적으로 비효율적이거나,
구글 내 충분한 컴퓨팅 자원이 없거나,
정렬 문제가 해결되지 않았을 가능성이다.

martinald의 HN 댓글에 따르면[^martinald] 구글이 자체 TPU 하드웨어 최적화에 집중하는 동안
엔터프라이즈 거래를 거절할 정도로 컴퓨팅 부족이 심각하다는 분석이 있다.
인프라 병목이 출시 전략에 영향을 미쳤을 가능성이 높다.

Tenoke는 대형 모델이 OpenAI나 Anthropic 대비 성능이 낮을 경우를 우려하며[^Tenoke]
구글이 속도 우위에 집중하는 전략을 취하고 있다고 봤다.
3.5 Flash-Lite의 초당 350 토큰은 이 전략의 방향을 보여준다.

### 사이버 보안 특화 모델의 등장이 의미하는 것

3.5 Flash Cyber는 코드 취약점 분석에 특화된 미세조정 모델이다.
이것은 도메인 특화 LLM이 범용 모델과 별도로 제공되는 추세의 일환이다.
의료, 법률, 금융에 이어 사이버 보안 영역에서 특화 모델이 출시되는 것은
벤더들이 전문 영역에서 정밀도를 높이는 방향으로 제품을 분화시키고 있음을 보여준다.

현재 정부 및 신뢰 파트너 대상 파일럿으로 제한된 것은
보안 도메인 모델의 오용 가능성을 통제하려는 의도와 함께
엔터프라이즈 계약 중심의 수익 모델을 테스트하는 의미도 있다.

GeekNews 사용자 dhkd63는 비즈니스 플랜에서 3.6 Thinking 모델도 별도로 활성화됐음을 언급했다.[^dhkd63]
일반 플랜과 비즈니스 플랜 간 기능 차이가 점점 커지는 추세다.

### 가격 경쟁의 방향

ekidd의 HN 댓글은 DeepSeek V4 Flash와의 가격 비교를 언급하며[^ekidd]
저가 모델 시장에서 미국 기업들이 마진을 유지하기 어렵다고 지적했다.
Gemini 3.5 Flash-Lite의 0.30달러/백만 토큰 입력 가격은 경쟁력 있는 수준이지만,
중국 오픈소스 모델들이 지속적으로 가격 압박을 가하고 있다.

janalsncm이 지적한 것처럼[^janalsncm] 대형 모델의 비즈니스 케이스가 불명확해지면서
작고 빠르고 저렴한 모델이 더 지속 가능한 수익 구조를 만든다는 시각도 있다.
이것이 구글이 Flash 라인업에 집중하는 또 다른 이유일 수 있다.

## 비평

### 성능 비교 근거가 선택적이다

“DeepSWE에서 65% 향상”이라는 수치는 구체적이지만,
DeepSWE가 어떤 코딩 작업을 측정하는 벤치마크인지,
실제 사용 환경과 얼마나 다른지는 발표 자료에서 확인하기 어렵다.
벤치마크 선택 자체가 모델이 강한 영역을 골라 보여주는 마케팅 도구로 쓰일 수 있다.

m_w_는 이 점을 정확히 짚었다.[^m_w_]
다른 모델과의 비교가 없는 발표는 진전을 평가하기 어렵게 만든다.
특히 jgbuddy가 지적했듯이[^jgbuddy] 3.6 Flash는 GLM 5.2보다 비용이 높으면서 성능은 낮고 가중치도 비공개다.
오픈소스 경쟁자가 이미 유사하거나 더 나은 성능을 더 낮은 가격에 제공한다면,
“구글 생태계 안에 있어야 하는” 이유가 점점 얇아진다.

경쟁사 모델과의 직접 비교가 없다는 점도 눈에 띈다.
GPT-4.1이나 Claude 3.7 Sonnet 같은 비슷한 포지셔닝의 모델과
동일한 벤치마크에서 비교한 수치가 없으면
“최고”라는 주장은 상대적 위치를 알 수 없다.

### 제품 라인업 복잡성이 사용자 혼란을 만든다

3.6 Flash, 3.5 Flash, 3.5 Flash-Lite, 3.5 Flash Cyber,
그리고 별도 플랜에서만 접근 가능한 3.6 Thinking까지 더해지면
어떤 모델을 언제 써야 하는지 명확하지 않다.
openpgc의 GeekNews 댓글처럼[^openpgc] “성능보다 혁신적 방향이 필요하다”는 반응은
현재의 점진적 개선 중심 출시 전략에 대한 피로감을 반영한다.

Gemini Enterprise Agent Platform 설정이 극도로 복잡하다는 지적도 있다.
기업 고객 입장에서 어떤 모델을 어떤 상황에 써야 하는지
명확한 의사결정 가이드가 없으면 도입 장벽이 높아진다.

stonewhite는 이 문제를 실제 경험으로 전달했다.[^stonewhite]
그는 Antigravity IDE 용 AI Ultra 구독이 갑자기 중단되면서 경쟁사 구독으로 전환했고,
Gemini Enterprise Agent Platform의 설정 과정이 "형편없는 수준"이었다고 밝혔다.
이것은 단순한 사용자 불만이 아니라 구글이 기업 고객 유지에 실패하는 패턴을 보여준다.
빠르게 변하는 제품 라인업과 갑작스러운 정책 변경은
기업 고객이 장기 계획을 세우기 어렵게 만든다.

## 인사이트

### Flash 라인업 집중이 보여주는 AI 시장의 구조 변화

대형 모델 경쟁에서 벗어나 빠르고 저렴한 모델 중심으로 전략을 전환하는 것은
AI API 시장이 성숙하고 있다는 신호다.
초기에는 “가장 강력한 모델”이 경쟁력이었지만,
에이전트 워크플로, 대규모 배치 처리, 비용 효율이 중요한 사용 사례에서는
속도와 가격이 더 중요한 요소가 된다.

이 전환은 AI를 인프라로 소비하는 기업 고객 비중이 늘고 있다는 뜻이기도 하다.
기능을 탐색하는 사용자에서 비용을 최적화하는 운영자로 고객 구성이 바뀌면
시장의 요구 사항 자체가 달라진다.

### 도메인 특화 모델이 새로운 경쟁 축을 만든다

Gemini 3.5 Flash Cyber는 사이버 보안이라는 특정 영역에서 경쟁하는 모델이다.
이것은 범용 모델이 아닌 도메인 전문 모델이 별도 제품군을 형성하는 흐름을 보여준다.
보안, 의료, 법률, 금융 각각에서 특화 모델이 나오면
경쟁이 “범용 벤치마크”가 아니라 “특정 도메인 실용성”으로 이동한다.

이 흐름에서 기업은 도메인별로 다른 모델을 평가하고 도입하게 된다.
그것은 구매 결정의 복잡성을 높이지만,
동시에 특정 영역에서 입증된 성능을 가진 모델에게 더 높은 가격을 받을 수 있는 기회가 된다.
범용 모델의 가격 압박에서 벗어날 수 있는 전략적 경로다.

---

[^postalcoder]: <https://news.ycombinator.com/item?id=48993972>
[^martinald]: <https://news.ycombinator.com/item?id=48995318>
[^Tenoke]: <https://news.ycombinator.com/item?id=48994334>
[^ekidd]: <https://news.ycombinator.com/item?id=48999006>
[^janalsncm]: <https://news.ycombinator.com/item?id=48995781>
[^dhkd63]: <https://news.hada.io/topic?id=31662#cid62202>
[^openpgc]: <https://news.hada.io/topic?id=31662#cid62190>
[^m_w_]: <https://news.ycombinator.com/item?id=48993626>
[^jgbuddy]: <https://news.ycombinator.com/item?id=48993576>
[^stonewhite]: <https://news.ycombinator.com/item?id=48994254>
