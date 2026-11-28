# GPT-6.2 추론 토큰 감소 분석

원문: [OpenAI may be in cost control mode](https://micjm.com/blog/openai-is-in-cost-control-mode/)

HN 토론: <https://news.ycombinator.com/item?id=50652527> (355점, 357개 댓글)

GN 토론: <https://news.hada.io/topic?id=37922>

## 요약

micjm이 2026년 11월 26일에 올린 짧은 글이다.
OpenAI가 최근 낸 Astra 6.2와 Sol 6.2가 널리 혹평받은 이유를 저자들이 가진
데이터로 설명하려 한다.
저자들의 결론은 두 모델이 비용 절감 쪽으로 조정된 것으로 보이며,
작업당 출력 토큰과 추론 토큰이 줄었다는 것이다.

글이 쓰는 데이터는 실제 작업을 시키는 대결 시스템에서 나온다.
첫 그래프는 가로축에 상대 모델 대비 지출 비율, 세로축에 리더보드 Elo를 놓고
GPT-6에서 6.2로의 변화를 보여 준다.
둘째 그래프는 같은 대결에서 상대보다 얼마나 추론했는지를 보여 주며,
Astra 6과 Sol 6.1은 평범했으나 Astra 6.2와 Sol 6.2는 이상치가 되었다고 한다.
출력 토큰도 같은 효과가 있다고 한다.
저자가 제시한 p값은 다음과 같다.

| 항목      | Sol     | Astra  |
| --------- | ------- | ------ |
| 출력 감소 | 0.0055  | 0.022  |
| 추론 감소 | 0.00013 | 0.0064 |

글은 이 두 모델이 이전 모델에 비해 비용 쪽으로 조정되었고,
그 정도가 생각이 부족한 이상치가 될 만큼이라고 결론짓는다.

## 분석

### 증거의 범위

글이 보여 주는 것은 두 가지다.
상대 모델보다 추론과 출력이 줄었다는 통계적 차이,
그리고 같은 대결에서 비용 대비 Elo가 움직였다는 것이다.
원인에 대한 서술은 추정이다.
저자들이 쓴 표현도 “비용 통제 모드일 수 있다”로 단정을 피한다.
글에는 대결 시스템이 어떤 작업과 어떤 도구에서 돌아가는지,
몇 번의 대결에서 나온 수치인지 적혀 있지 않다.
HN에서 글의 데이터를 올린 것으로 보이는 seizethecheese는 오픈소스 코딩
하네스 opencode 위에서 만든 대결 시스템이라고 밝혔고,
Sol 6.2는 지금까지 213번 중 73번만 이겼다고 썼다.[^seizethecheese-sol]

### 비용 통제와 성능 하락의 구분

토큰이 줄었다는 것이 성능이 나빠졌다는 뜻은 아니다.
HN의 ac29는 가장 분명한 설명이 비용과 지능의 파레토 경계에 맞춰 조정하는
것이라고 썼고,[^ac29]
posnet은 API 비용을 내는 기업은 Artificial Analysis의 작업당 비용 파레토를
눈여겨보며
OpenAI가 Fable 5.2가 있는 극단을 뺀 모든 구간에서 앞선다고 했다.[^posnet]
seizethecheese는 이것이 글의 데이터와 맞는다며 기업 시장을 겨냥한 벤치마크와
비용 조정이라고 보았다.[^seizethecheese]
따라서 같은 데이터가 의도된 효율화일 수도 있고 품질 저하일 수도 있다.

## 비평

### 코딩 사용자의 체감

dwb는 직장에서 비용 때문에 Claude에서 Codex로 옮겼는데 Astra와 Sol 6.x의 코딩이
기대보다 훨씬 나빴다고 썼다.[^dwb]
tezza는 두 회사를 대형 코드베이스에서 많이 쓰는데 각각 강점이 있다며
구체적인 사례를 물었다.[^tezza]
이 증언은 개인 경험이고 대결 데이터와 같은 방향이지만 서로를 검증하지는 않는다.

### 모델이 나빠진다는 서사

jrflo는 Opus도 4.5가 훌륭하다가 점점 나빠져 5.5에 이르렀다며
연구소들이 훌륭한 모델을 내고 증류해 추론 비용을 줄이는 공식을 따른다고
썼다.[^jrflo]
SOLAR_FIELDS는 같은 작업이 시간이 갈수록 나빠지는 평가가 없으면 느낌일 뿐이라고
했다.[^SOLAR_FIELDS]
이 논쟁은 글이 다루는 단일 세대 비교와 다른 문제이며,
글은 시간에 따른 변화가 아니라 모델 사이의 차이만 보여 준다.

### 출시 시점에 대한 추측

torginus는 Astra 6.2가 경쟁사의 IPO에 맞춘 일정 출시여서 덜 다듬어졌을 수 있다고
추측했다.[^torginus]
이는 글에도 데이터에도 근거가 없는 추측이다.

### 글이 배제하지 않은 설명들

zmmmmm은 글이 증명하는 것은 출력 토큰이 줄었다는 사실뿐이며,
모델이 더 똑똑해서 결론에 빨리 닿았을 때도 토큰은 준다고 썼다.
토큰당 비용이 더 비싼 모델이면 작업당 비용은 오히려 늘 수도 있다는
지적이다.[^zmmmmm]
jcrben은 글이 추론 강도(effort) 설정을 언급하지 않았다고 짚었다.
설정을 올리면 추론량도 올릴 수 있으므로 사용자에게 더 많은 조절권을 준 것일
수도 있다는 것이다.[^jcrben]
q17과 InsideOutSanta는 OpenAI가 고객에게 덜 받는다고 해서 자기 비용을 통제한다는
뜻은 아니며, 토큰이 많아지면 매출이 늘 텐데 이 틀이 이해되지 않는다고
물었다.[^q17][^InsideOutSanta]
글은 이 설명들을 따로 검토하지 않으며, 결론도 “비용 통제 모드일 수 있다”에
머무른다.

### 사용 한도 정책에 대한 정황

voxgen은 OpenAI가 사용량 초기화(reset)를 훨씬 드물게 주고 있다고 썼고,
Janicc는 5월 이후 두 달마다 한도 정책이 바뀐다고 했다.[^voxgen][^Janicc]
joeyhage는 두 모델의 저렴한 비용이 OpenAI의 말로는 과금 버그였다는 기사를
링크했고, piskov는 그것이 구독 요금제 이야기이지 API가 아니라고
구분했다.[^joeyhage][^piskov]
이들은 모두 정황이며 글의 데이터가 말하는 토큰 감소와 직접 이어지지 않는다.

## 인사이트

### 토큰 가격이 통신 요금처럼 될 가능성

alexpotato는 토큰이 1990년대 말 장거리 전화 분 단위 요금과 닮아 가고 있다고
했다.
새 기술, 큰 수요, 소수 사업자, 막대한 인프라, 5년쯤의 좋은 사업 뒤에 정액제로
가격 경쟁이 일어났다는 유사점을 들었다.[^alexpotato]
x3haloed는 효율은 모든 기술이 약속한 가치의 일부라고 답했다.[^x3haloed]
mapontosevenths는 OpenAI와 Anthropic 중 하나가 망하면 남은 쪽이 개선 동기를
잃을 테니 모든 소비자에게 나쁘다고 썼다.[^mapontosevenths]
이들은 비용 통제 자체가 나쁜 일이냐를 두고 의견이 갈린다.
이 문서가 가져갈 것은 모델을 고를 때 토큰당 가격이 아니라 작업당 비용과 결과
품질을 같이 봐야 한다는 점이다.

---

[^zmmmmm]: <https://news.ycombinator.com/item?id=50660439>

[^jcrben]: <https://news.ycombinator.com/item?id=50659329>

[^q17]: <https://news.ycombinator.com/item?id=50659694>

[^InsideOutSanta]: <https://news.ycombinator.com/item?id=50660186>

[^voxgen]: <https://news.ycombinator.com/item?id=50658660>

[^Janicc]: <https://news.ycombinator.com/item?id=50659477>

[^joeyhage]: <https://news.ycombinator.com/item?id=50660494>

[^piskov]: <https://news.ycombinator.com/item?id=50660616>

[^seizethecheese-sol]: <https://news.ycombinator.com/item?id=50660824>

[^ac29]: <https://news.ycombinator.com/item?id=50659291>

[^posnet]: <https://news.ycombinator.com/item?id=50659124>

[^seizethecheese]: <https://news.ycombinator.com/item?id=50659231>

[^dwb]: <https://news.ycombinator.com/item?id=50659691>

[^tezza]: <https://news.ycombinator.com/item?id=50659895>

[^jrflo]: <https://news.ycombinator.com/item?id=50659112>

[^SOLAR_FIELDS]: <https://news.ycombinator.com/item?id=50659169>

[^torginus]: <https://news.ycombinator.com/item?id=50660438>

[^alexpotato]: <https://news.ycombinator.com/item?id=50660707>

[^x3haloed]: <https://news.ycombinator.com/item?id=50660774>

[^mapontosevenths]: <https://news.ycombinator.com/item?id=50659287>
