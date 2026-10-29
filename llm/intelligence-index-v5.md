# Artificial Analysis Intelligence Index v5: 비공개 평가를 60퍼센트로 높이고 네 영역에 25퍼센트씩 나눈 새 지수

원문: [Announcing Artificial Analysis Intelligence Index v5 | Artificial Analysis](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5)

HN 토론: <https://news.ycombinator.com/item?id=50268868> (92점, 82개 댓글)

GN 토론: <https://news.hada.io/topic?id=36197>

## 요약

Artificial Analysis가 2026년 10월 27일에 올린 지수 개편 발표이다.
Intelligence Index는 실제 사용을 반영하는 작업들에서 모델의 능력을 합산한 종합
지표이고, v5는 1월에 낸 v4 이후 가장 큰 개편이라고 글은 쓴다.
핵심 변화는 지수의 60퍼센트가 비공개 시험 세트나 비공개 정답을 쓰는 평가에
기반한다는 것이다.
글은 새 평가 둘, 개선 셋, 유지 넷, 제외 셋을 나열한다.

| 구분 | 평가                                                                   |
| ---- | ---------------------------------------------------------------------- |
| 신규 | FrontierCode 2.0, Terminal-Bench-Science                               |
| 개선 | HLE-Diamond(Humanity's Last Exam 대체), AA-Omniscience v1.1, CritPt v2 |
| 유지 | AA-Briefcase, AutomationBench-AA, GDP.pdf, Terminal-Bench 4.0          |
| 제외 | GDPval-AA v2.1, SciCode, AA-LCR v1.1                                   |

가중치는 지식 노동, 코딩, 과학, 일반의 네 영역이 각각 25퍼센트이다.
지식 노동은 AA-Briefcase 15, AutomationBench-AA 5, GDP.pdf 5이고,
코딩은 FrontierCode 2.0이 15, Terminal-Bench 4.0이 10이다.
과학은 Terminal-Bench-Science 15와 CritPt v2의 어려운 부분집합 10이고,
일반은 AA-Omniscience v1.1이 15(정확도 10,
환각하지 않음 5)와 HLE-Diamond 10이다.

주요 결과는 이렇다.
Claude Opus 5.5(max)가 58점으로 1위이고 GPT-6 Astra(max) 57점,
GPT-6.1 Sol(max) 55점이
뒤따르며, Anthropic과 OpenAI가 상위 다섯 모델을 차지한다.
Gemini 4 Argon(high)은 50점이다.
오픈 가중치 모델과의 격차는 v4.3의 3점에서 12점으로 벌어졌다.
오픈 가중치 최고는 가중치가 아직 공개되지 않은 Kimi K3.1 Pro의 46점이고,
가중치가 공개된 모델 중에서는 DeepSeek V4.1 Flash 1017과 GLM-5.3이 32점으로
Claude Haiku 5.5(36점)에도 못 미친다.
비용은 상위 10개 모델 사이에서 작업당 13배 넘게 차이가 나서,
GPT-6.1 Terra(max)가 0.96달러로 가장 싸고 Claude Fable 5.1(max)이 13.04달러로
가장 비싸다.

새 평가의 설명도 길다.
FrontierCode 2.0은 Cognition이 같은 날 낸 비공개 코딩 벤치마크로,
실제 오픈소스 저장소의 132개 작업을 관리자가 병합할 변경이냐는
기준으로 채점하고,
막는 검사 하나라도 실패하면 0점이며, 각 작업을 Artificial Analysis의 하네스
Stirrup에서 세 번 돌린다.
1위는 Claude Opus 5.5(max)의 46퍼센트이다.
Terminal-Bench-Science는 터미널에서 70개의 과학 연구 작업을 수행하고
모든 검사를 통과해야 통과이며, GPT-6 Astra(max)가 63퍼센트로 1위이다.
HLE-Diamond는 Center for AI Safety와 Scale AI의 Humanity's Last Exam을
1,000문항으로
다듬은 것이고, Claude Opus 5.5(max)가 68퍼센트로 앞선다.
CritPt v2는 연구 수준 물리 문제 70개에서 출시 때 일곱 개의 최전선 모델이 다섯 번
모두 푼 30개를 뺀 40문항의 비공개 부분집합이다.

글은 지수에 더해 Progress Index v1도 낸다.
2022년 11월 이후에 나온 언어 모델을 하나의 능력 척도에 놓아 시간에
따른 능력 변화를
비교하게 하는 지표이고, 현재 모델을 비교할 때는 여전히 Intelligence
Index를 쓰라고
한다.
Epoch Capabilities Index를 설계하며 얻은 교훈을 바탕으로 했다고 Epoch AI와
Anthropic에 감사를 표한다.

## 분석

### 비공개 평가는 오염을 막고 검증 가능성을 내놓는다

v5의 가장 큰 설계 선택은 비공개 평가 비중을 60퍼센트로 올린 것이다.
공개 문제는 학습 데이터에 섞일 수 있고 모델 제작자가 그 문제에 맞춰 최적화할 수
있다.
비공개 세트는 이 경로를 막는다.
글이 FrontierCode 2.0의 작업을 오염을 막으려고 비공개로 둔다고 쓰는 것이 이
논리이다.
그 대가는 외부에서 결과를 재현할 수 없다는 점이다.
이 문서의 해석으로는 이 교환이 v5의 성격을 정한다.
오염에 대한 신뢰를 시험지의 비공개에서 얻는 대신,
평가를 운영하는 쪽에 대한 신뢰가
더 필요해진다.

### 평가의 성격이 문제 풀이에서 일의 완수로 옮겨 간다

새 평가와 가중치를 보면 방향이 보인다.
FrontierCode 2.0은 정답 일치가 아니라 관리자가 병합할 변경인지를 보고,
Terminal-Bench-Science는 모든 검사가 통과해야 통과이고,
AA-Briefcase와 AutomationBench-AA는 업무 자동화이다.
글이 밝힌 대로 에이전트형 평가인 Terminal-Bench-Science, Terminal-Bench 4.0,
AA-Briefcase, FrontierCode 2.0은 지수 가중치의 55퍼센트이지만 출력 토큰의 중앙값
약 90퍼센트를 쓴다.
모델당 작업당 출력 토큰의 중앙값은 v4.3의 35k에서 59k로 3분의 2가 늘었다.
이 문서의 해석으로는 이 지수가 재는 것은 지식의 크기가 아니라 긴 작업을 끝까지
끌고 가는 힘이고, 그 힘은 토큰과 비용을 많이 쓰는 방식으로 얻어진다.

### 노력 설정과 비용이 점수의 일부가 된다

글은 노력 설정이 v4.3보다 v5에서 더 중요하다고 쓴다.
Claude Opus 5.5는 낮은 노력에서 35점, 최대에서 58점이고
작업당 비용은 0.98달러와 10.04달러로 10배이다.
Claude Sonnet 5.5는 낮음에서 최대까지 29점 차이로 v4.3의 20점에서 늘었고,
GPT-6.1 Sol의 폭은 10점에서 20점으로 두 배가 되었다.
GPT-6.1 Sol(max)은 Claude Opus 5.5(max)와 4점 안쪽에 있으면서 작업당
비용이 약 8분의
1이다.
따라서 이 지수에서 모델의 점수는 하나의 숫자가 아니라 노력 설정과 비용에 따라
움직이는 곡선 위의 점이다.

## 비평

### 순위가 바뀐 이유를 글이 설명하지 않는다

HN에서 mirekrusin은 v4.3에서 v5로의 점수 변화를 정리했다.
오픈 가중치 모델은 Kimi K3.1 Pro가 9점, DeepSeek V4.1 Flash 1017과 GLM-5.3이
13점, MiMo-V2.6-Pro가 16점 내려갔고, 독점 모델은 GPT-6 Astra가 4점,
GPT-6.1 Sol과 Terra가 3점 올랐으며 Claude Opus 5.5는 0점이었다는
것이다.[^mirekrusin]
그는 OpenAI와 관계가 있는 것인지 우연인지 물었다.[^mirekrusin]
글은 오픈 가중치의 격차가 3점에서 12점으로 벌어졌다고 쓰지만 왜 벌어졌는지,
어떤 평가가 그 격차를 만들었는지는 설명하지 않는다.
다만 글 안의 단서는 있다.
격차가 가장 큰 평가는 HLE-Diamond와 Terminal-Bench-Science이고,
Kimi K3.1 Pro가 각각 37퍼센트와 34퍼센트인 반면 Claude Opus 5.5(max)는 68퍼센트,
GPT-6 Astra(max)는 63퍼센트이다.
rbehrends는 HN에서 코딩 지수만 보면 소프트웨어 공학의 관점에서 더 그럴듯한
결과가 나오고, 코딩에 최적화된 작은 모델이 비코딩 작업에서 낮은 것은 이상하지
않으며 Terminal-Bench Science의 도입이 합산 점수를 특히 낮춘다고
짚었다.[^rbehrends]
이것이 편향이 아니라 구성의 효과라는 설명이고,
글이 이 설명을 직접 쓰지 않은 점이
의심을 키운다.

### 비공개 평가의 비중이 커질수록 재현할 수 없는 부분이 커진다

irthomasthomas는 이번 개편이 비공개 출처 두 개를 포함해서 재현할 수
없는 데이터가
되었다는 점이 유독 나쁘다고 썼다.[^irthomasthomas]
hgoel은 지수를 자주 고쳐서 포화된 구성 요소를 버린다면 비공개로 두는 것이 연구상
무슨 의미냐고 물었다.[^hgoel]
chvid는 이 회사가 실리콘밸리의 40명 규모 회사인데 누가 자금을 대고 어떻게 돈을
버느냐고 물었다.[^chvid-funding]
글에는 자금원이나 이해관계의 서술이 없고,
이 문서는 Artificial Analysis의 재무를 확인하지 못했다.
이는 비공개 평가가 늘수록 신뢰의 근거가 시험지에서 운영자의 이해관계로 옮겨
간다는 앞의 분석을 확인하는 반응이다.

### 합산 점수의 정밀도가 보고되지 않는다

글의 점수는 정수이고 신뢰 구간이 없다.
yorwba는 개별 벤치마크가 정보가 적고 나쁜 모델은 우연 수준,
좋은 모델은 포화이며,
작업 수가 적어 몇 퍼센트포인트의 차이가 잡음일 수 있어서 가중 합산은
어느 잡음을 더
증폭할지 고르는 일에 가깝다고 썼다.[^yorwba]
그는 포화를 명시적으로 모델링하고 오차 막대를 제공하는 Epoch의 ECI 방식을
선호한다고 했다.[^yorwba]
hobofan은 사람들이 가장 관심을 두는 코딩과 과학 영역이 문항 수가 적어 코딩은 약
200개, 과학은 약 150개라고 짚었다.[^hobofan]
글이 밝힌 규모도 이를 뒷받침한다.
FrontierCode 2.0은 132개 작업, Terminal-Bench-Science는 70개 작업,
CritPt v2는 40문항이다.
hgoel은 1점 차이가 무엇을 뜻하고 모델 사이의 의미 있는 구분이 되려면 몇 점이
벌어져야 하느냐고 물었다.[^hgoel]
글은 이 질문에 답하지 않는다.
이 문서의 추정으로는 Claude Opus 5.5의 58점과 GPT-6 Astra의 57점의 1점 차이는
작업이 수십 개인 평가들의 합에서 잡음과 구별되지 않을 수 있다.
글이 오차를 주지 않아서 이 판단은 표본 크기에서 온 짐작일 뿐이고
직접 계산한 것이
아니다.

### 심판과 선택의 구조가 한쪽으로 기울 수 있다

chvid는 AA의 FrontierCode 서술을 인용해 검증기가 작업의 시험과 평가 기준으로
채점하고 LLM 심판으로 GPT-6 Luna(중간)를 쓴다고 짚으며,
왜 비공개 폐쇄 모델을 심판으로 쓰느냐고 물었다.[^chvid-judge]
이 문서는 AA의 평가 페이지를 열어 보지 못했으므로 인용된 문장의
정확함은 확인하지
못했다.
CritPt v2의 40문항 선택도 구조가 있다.
70문항에서 출시 때 일곱 개 최전선 모델이 다섯 번 모두 푼 30문항을 뺐으므로,
그 일곱 모델이 쉽게 푸는 문제가 제거되었다.
이 필터가 그 일곱 모델의 점수를 낮추는 방향이고, 일곱에 포함되지 않은 모델에는
같은 효과가 없다.
글은 이 일곱 모델이 어느 모델인지 밝히지 않는다.

### 빠진 모델과 열거된 오픈 가중치의 정의

peri-cl은 HN에서 글이 몇몇 인기 있는 오픈 가중치 모델을 새 지수에서
조용히 뺐다고
썼다.
GLM 5.3-flash와 Qwen 3.8-flash-next의 모델 페이지에 N/A가 표시된다는
것이다.[^peri-cl]
이 문서는 그 페이지를 확인하지 못했다.
글은 오픈 가중치의 격차가 12점으로 벌어졌다는 주장의 최고 모델이 가중치가 아직
공개되지 않은 Kimi K3.1 Pro라고 스스로 적는다.
공개된 가중치 중 최고는 32점이어서 선두와 26점 차이이다.
머리글의 12점은 아직 가중치가 공개되지 않은 모델을 오픈 가중치로 센 값이다.

## 인사이트

### 벤치마크는 공개에서 포화로, 비공개로 이동하고 신뢰가 감사의 문제가 된다

v5의 흐름은 벤치마크의 수명 주기를 보여 준다.
공개된 시험은 포화되고, 포화된 시험을 버리고 새 시험을 넣고,
새 시험은 오염을 막으려 비공개로 둔다.
Humanity's Last Exam이 HLE-Diamond로, AA-Omniscience가 v1.1로 바뀌고,
포화되었거나 공개된 문항을 빼는 작업이 글에 나온다.
이 문서의 해석으로는 이 주기의 끝에서 시험은 외부 검증이 불가능해지고,
신뢰는 시험을 운영하는 조직의 구조(자금, 이해관계, 변경 이력)로 옮겨 간다.
신용평가나 회계 감사가 평가 대상에게 돈을 받는 구조가 늘 문제가 되었던 것처럼,
평가 회사가 누구에게 돈을 받는지가 평가의 일부가 된다.
HN의 반응이 숫자보다 자금과 시점에 집중된 것은 이 때문이다.
이 가설을 뒤집는 관측은 비공개 평가의 결과를 독립 기관이 재현해 일치를 확인하는
경우이다.

### 모델은 순위가 아니라 점수와 비용과 노력의 곡선으로 고른다

글의 비용 서술이 보이는 것은 점수의 순서가 선택의 기준이 될 수 없다는 점이다.
Claude Opus 5.5 최대 설정은 작업당 10.04달러이고
GPT-6.1 Sol 최대 설정은 4점 안쪽에서 1.27달러이다.
Opus 5.5는 낮은 노력에서 35점이고 0.98달러이다.
이 문서의 해석으로는 고르는 단위가 모델이 아니라 모델과 노력 설정의 쌍이다.
선택은 작업의 가치에 달려 있다.
한 건의 작업이 비싸도 되는 일(보안 검토, 장애 조사)에서는 최대 설정이 맞고,
많은 양을 싸게 돌려야 하는 일에서는 점수가 조금 낮아도 비용이 8분의
1인 쪽이 맞다.
HN에서 piterrro와 ilumanty의 대화가 이 선택을 일상의 말로 보인다.
DeepSeek Flash는 속도와 비용 때문에 충분하다는 쪽과,
Opus 5.5가 더 적은 토큰으로 맞게 한다는 쪽이다.[^piterrro][^ilumanty]
두 사람 모두 지수의 점수로는 알 수 없는 이유로 모델을 골랐다.

### 현재의 순위와 시간에 따른 진전을 한 척도로 둘 수 없다

글이 Progress Index를 따로 낸 것은 지수의 구성이 바뀔 때마다 순위가 바뀌어서
시간에 따른 비교에 쓸 수 없기 때문이다.
v4.3에서 v5로 가며 오픈 가중치 격차가 3점에서 12점이 된 것은 구성의
효과를 능력의
변화와 섞어 놓은 사례이다.
이 문서의 해석으로는 이 분리가 지수의 역할을 정직하게 나눈다.
Intelligence Index는 지금의 모델을 가리는 도구이고,
Progress Index는 능력의 변화를 재는 도구이다.
yorwba가 선호한다고 한 Epoch의 방식은 포화를 모델링하고 오차 막대를 낸다는
점에서 Progress Index의 방향과 가깝고, 글이 Epoch AI에 감사를 표한 이유와
맞닿는다.[^yorwba]
다만 글이 이 두 지표의 결과 사이의 관계(같은 모델의 두 점수가 어떻게 다른지)를
보이지 않아서 이 분리가 실제로 얼마나 다른 이야기를 하는지는 확인되지 않았다.

### 지수가 나온 지 하루 만에 1위가 바뀐다는 사실이 정밀도의 질문이다

GeekNews에서 xguru는 이 지수를 발표한 직후 Gemini 4 Carbon(high)이
59점으로 새 1위에
올랐고 기존 선두 Claude Opus 5.5(max)와 1점 차이라고 적었다.[^xguru]
그는 Carbon이 9개 평가 중 HLE-Diamond, Terminal-Bench-Science, AA-Omniscience,
AutomationBench-AA에서 1위라고 했다.[^xguru]
글의 사이드바에도 이 문서가 읽은 시점에 같은 내용의 후속 글이 보인다.
Carbon이 새 1위이고 코딩 에이전트 지수에서는 Claude Opus 5.5
다음이라는 제목이다.
이 문서의 해석으로는 1점 차이로 1위가 하루 만에 바뀌는 것은 지수가 순위를 가르는
도구가 아니라 군집을 나누는 도구에 가깝다는 신호이다.
위의 정밀도 문제와 이어서 보면, 지수의 순위는 1점 안쪽에서는 해석하지 않는 것이
안전하다.

---

[^mirekrusin]: <https://news.ycombinator.com/item?id=50270428>

[^rbehrends]: <https://news.ycombinator.com/item?id=50270361>

[^irthomasthomas]: <https://news.ycombinator.com/item?id=50271561>

[^hgoel]: <https://news.ycombinator.com/item?id=50272321>

[^chvid-funding]: <https://news.ycombinator.com/item?id=50270912>

[^yorwba]: <https://news.ycombinator.com/item?id=50271145>

[^hobofan]: <https://news.ycombinator.com/item?id=50270060>

[^chvid-judge]: <https://news.ycombinator.com/item?id=50270115>

[^peri-cl]: <https://news.ycombinator.com/item?id=50271289>

[^piterrro]: <https://news.ycombinator.com/item?id=50270686>

[^ilumanty]: <https://news.ycombinator.com/item?id=50270861>

[^xguru]: <https://news.hada.io/topic?id=36197#cid68705>
