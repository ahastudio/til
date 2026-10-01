# GPT-6.1 Sol: Astra에 가까운 지능을 5분의 1 가격에 판다는 OpenAI의 중간 모델

원문: [GPT-6.1 Sol 소개 | OpenAI](https://openai.com/ko-KR/index/introducing-gpt-6-1-sol/)

HN 토론: <https://news.ycombinator.com/item?id=49896586> (1050점, 931개 댓글)

GN 토론: <https://news.hada.io/topic?id=34500>

## 요약

OpenAI가 2026년 9월 29일 DevDay에서 공개한 GPT-6 Sol의 업그레이드 모델이다.
글의 부제는 Astra에 가까운 지능을 5분의 1 가격으로 준다는 것이다.
에이전트 코딩, 컴퓨터 사용, 전문 업무에서 GPT-6 Astra에 한층 가까운
성능을 내면서, 표준 입출력 토큰 가격은 Astra의 5분의 1이라고 소개한다.
캐시된 입력은 100만 토큰당 0.10달러로 표준 입력보다 95% 싸며,
컨텍스트를 반복해서 쓰는 에이전트 작업의 비용을 줄인다고 강조한다.
종합적인 역량에서는 여전히 GPT-6 Astra가 가장 뛰어난 프런티어 모델이라고 분명히
하고, 6.1 Sol은 역량과 비용 사이의 새 균형점이라고 자리매김한다.

벤치마크는 다섯 영역으로 제시된다.

| 영역      | 평가                       | 주장                                                                        |
| --------- | -------------------------- | --------------------------------------------------------------------------- |
| 코딩      | DeepSWE v1.1               | 약 5분의 1 비용으로 Astra와 대등, GPT-6 Sol 최고 점수보다 6.4%p 높음        |
| 전문 업무 | GDP.pdf                    | 폴백을 쓰는 Opus 5.5보다 높고 작업당 비용은 절반 미만                       |
| 전문 업무 | AutomationBench 1.0.6      | 중간 추론 강도에서 Opus 5.5보다 2.2%p 높고 비용은 약 3분의 1                |
| 컴퓨터    | OSWorld 2.0 오프라인 세트  | 최대 추론에서 GPT-6 Sol보다 7%p 높고, Astra와 2.1%p 차이, 비용 7분의 1      |
| 과학      | Terminal-Bench Science 0.1 | GPT-6 Sol의 2배 이상, 평균 작업당 5.47달러로 Opus 5.5, Astra의 4분의 1 미만 |

과학 연구에서는 Astra가 68.1%로 가장 높으므로 가장 어려운 과학
작업에는 Astra를 쓰라고 권한다.
사실 정확성은 사용자가 이전 모델의 오류를 신고한 대화를 비식별화한 평가에서,
추론 강도 매우 높음 기준 오류율 4.1%로 GPT-6 Sol의 4.5%보다 낮고
Astra의 4.0%에 가깝다.
안전 평가에서는 검색 도구가 고장 났을 때 추측하지 않고 알리는지 보는 항목에서
알리지 않은 비율이 6.1 Sol 2.1%, 6 Sol 4.9%, Astra 1.5%, GPT-6 Luna 28.7%였고,
자동 안전 검토 시스템을 우회하려는 시도는 관찰되지 않았다고 밝힌다.

모델은 그날부터 Plus, Pro, Business, Enterprise,
Edu 사용자가 ChatGPT Work와 Codex에서 쓸 수 있지만, Chat에서는 아직 쓸 수 없다.
API 이름은 `gpt-6.1-sol`이고 가격은 입력 100만 토큰당 2달러,
캐시 입력 0.10달러, 출력 10달러다.
함께 나온 GPT-6 Astra Ultrafast와 GPT-6.1 Sol Ultrafast는 Astra보다 최대 8배
빠르다고 하며, API와 월 500달러의 새 Pro 등급에서 쓸 수 있다.
글은 평가가 OpenAI 연구 환경이나 API에서 수행되어 ChatGPT의 출력과 조금
다를 수 있고, 경쟁사 수치는 공개 보고서에서 가져왔다고 각주를 단다.

## 분석

### 이번 발표의 실제 경쟁 상대는 Astra가 아니라 Opus 5.5다

제목은 Astra와 비교하지만, 벤치마크 문단을 읽으면 비교의 무게중심이 다르다.
GDP.pdf, AutomationBench, Terminal-Bench Science 세 곳에서 OpenAI는 Anthropic의
Opus 5.5를 직접 이름으로 부르고, 점수와 작업당 비용을 함께 댄다.
Astra와의 비교는 같은 회사 안에서의 가격 사다리이고,
Opus 5.5와의 비교가 시장에서의 싸움이다.

HN 반응은 이 맥락을 그대로 보여 준다.
mynameisjonny_는 GPT-6 Sol의 첫 반응이 나빴고 Opus 5.5가 여론에서 이기고
있었으니 무언가를 서둘러 내놓는 것이 이해된다고 썼고[^mynameisjonny_],
the_duke는 Sol 6가 너무 나빠 Opus 5.5로 완전히 갈아탔다고 했다[^the_duke].
TuxSH는 모든 API 가격 항목이 정확히 Opus 5.5의 절반이라고 짚었다[^TuxSH].
가격표를 경쟁 모델의 정확히 절반에 맞춘 것은 우연이 아니라 포지셔닝이다.

### 출시 일주일 만에 교체된 모델이 무엇이었는지가 논쟁의 중심이 되었다

GPT-6 Sol은 이 발표 일주일 전인 9월 22일에 나왔다.
intenex는 6 Sol이 말 그대로 6일 전에 나왔으니
주간 출시 주기에 들어선 것이라고 놀랐고[^intenex],
zarzavat은 일주일 사이에 할 수 있는 것은 사소한 후속 학습뿐이니 압박
속에 6 Sol을 너무 일찍 내놓고 이제 진짜 버전을 내는 것이라고 봤다[^zarzavat].
이름에 대한 추측도 이어졌다.
codewithcheese는 6 Sol이 사실상 Terra였고, Opus 5.5 때문에 역효과가 나자
진짜 6 Sol을 6.1로 내는 것이라고 썼고[^codewithcheese],
jumploops는 API에서 6.1 Sol은 Astra처럼 추론이 필수인데 6 Sol과 Luna는 추론
없음을 허용한다는 점을 정황으로 들었다[^jumploops].

GN에서도 같은 추측이 나왔다.
click은 6.1 Astra로 내려던 것이 경쟁사에 못 미치자 이름만 바꾼 것 아니냐고
물었고[^gn-click], cronex는 6 Sol로 내려던 것이 지연되자 6 Terra를 6 Sol
이름으로 냈다가 고쳐서 6.1 Sol로 다시 낸 것일 수 있다고 추측했다[^gn-cronex].
JacobAsmuth는 6.1 Sol이 6 Sol보다 느리다는 Artificial Analysis 측정을 근거로
들면서도, 작은 모델을 큰 배치로 돌리면 처리량은 높고 응답성은 낮아질 수 있으니
그것만으로는 단정할 수 없다고 선을 그었다[^JacobAsmuth].
이 추측들은 모두 확인되지 않았지만, 공통된 메시지는 분명하다.
사용자는 모델 이름을 능력의 약속으로 읽는데, 그 약속이 일주일 만에 바뀌었다.

### 캐시 가격이 이 발표의 숨은 주인공이다

minimaxir는 캐시 입력이 100만 토큰당 0.10달러로 GPT-6 Sol의 캐시 가격보다 50%
싸다는 점이 진짜 큰 발표라고 썼다[^minimaxir].
tensegrist는 입력, 출력,
캐시의 비율이 Astra와 Luna는 10:50:1인데 Sol만 10:50:0.5라는,
단조롭지 않은 움푹한 지점이 생겼다는 점을 짚었다[^tensegrist].
에이전트 작업에서 입력의 대부분은 반복되는 시스템 프롬프트, 도구 정의,
이전 대화이므로, 캐시 가격이 실제 비용의 대부분을 정한다.

하지만 캐시의 효과는 작업 방식에 달려 있다.
joshstrange는 5분마다 문맥을 압축하면 캐시는 별 도움이 안 되며, 중간 추론의 Sol
에이전트 하나로 월 100달러 구독을 놀랄 만큼 빨리 다 썼다고 답했다[^joshstrange].
압축은 문맥의 앞부분을 바꾸고, 앞부분이 바뀌면 캐시는 다시 처음부터 쌓인다.
그래서 같은 가격표라도 하네스의 문맥 관리 방식에 따라 실제
비용은 몇 배씩 달라진다.

## 비평

### 토큰 단가의 5분의 1과 작업 비용의 5분의 1은 다른 말인데, 글은 둘을 섞는다

글의 제목과 첫 문단은 표준 토큰 가격이 Astra의 5분의 1이라고 말한다.
본문의 벤치마크는 작업당 비용으로 비교한다.
두 숫자가 같은 방향을 가리킨다는 것은 맞지만, 같은 크기를 가리키지는 않는다.
OSWorld에서는 작업당 비용이 약 7분의 1이고, 사실 정확성 평가에서는 약 83% 싸며,
DeepSWE에서는 약 5분의 1이다.

이 차이가 독자에게 중요한 이유는 모델마다 작업
하나에 쓰는 토큰의 양이 다르기 때문이다.
AspireOne은 Artificial Analysis 자료를 인용해, 작업
하나에 DeepSeek V4.1 Flash(max)는 0.27달러, 5.5분, 생성 토큰 8만 9천 개를 썼고
GPT-6.1 Sol(medium)은 0.21달러, 2.2분, 8천 개를 썼다고 비교했다[^AspireOne].
토큰 단가로는 훨씬 싼 모델이 작업 비용으로는 더 비쌀 수 있다는 뜻이다.
글이 작업당 비용을 함께 보여 준 것은 정직하지만,
제목과 부제에서 토큰 단가를 앞세운 것은 독자를 덜 정확한 숫자로 먼저 이끈다.

### 더 높은 추론 강도가 더 낮은 점수를 내는 결과를 설명하지 않는다

HN의 pazimzadeh은 DeepSWE에서 6.1 Sol High가 75.2%인데 더 비싼
XHigh는 71.9%라며, 왜 추론을 더 하면 점수가 떨어지는지,
조건마다 몇 번 시험했는지 물었다[^pazimzadeh].
zamadatix는 생각이 길어지면 중요한 정보가 문맥에서 밀려나거나 환각한
정보가 문맥에 남아 나중에 행동의 근거가 될 수 있다고 답했고[^zamadatix],
heaney-555는 일부 벤치마크가 사용자가 요청하지 않은 범위 밖의 일을 하면
감점하는데, 높은 추론 강도가 그런 행동을 부르곤 한다고 덧붙였다[^heaney-555].

이 현상은 사용자에게 실질적인 결정 문제다.
추론 강도를 올리면 비용은 확실히 오르지만 결과는 나빠질 수도 있다.
그렇다면 사용자는 어떤 작업에 어떤 강도를 써야 하는지 알아야 하는데,
글은 강도별 점수를 차트로만 보여 주고 이 비단조성을 설명하지 않는다.
시행 횟수와 분산도 밝히지 않으므로, 3%p 정도의 차이가 실제 차이인지
실행마다의 흔들림인지 독자는 판단할 수 없다.

### 구독 사용자에게는 가격 인하가 아니라 가격 인상으로 도착했다

글은 가격 인하를 말하지만, 같은 날 구독 구조가 바뀌었다.
Aboutplants는 Engadget 기사를 인용해 새 500달러 Pro 등급이 생기고,
기존 200달러 Pro의 Codex와 Work 사용량이 Plus의 20배에서 10배로 줄며, ChatGPT의
GPT-6 Pro 메시지 상한이 주 200개에서 100개로 줄었다고 전했다[^Aboutplants].
gobdovan은 구독 한도가 절반이 되었으니 Codex 사용자에게는 최선의
경우에도 약 2.5배 싸진 것에 그친다고 계산했고[^gobdovan], kenzic은 대부분의
사용자가 크레딧의 절반을 잃는데 정말 5분의 1 가격이냐고 물었다[^kenzic].
GN에서 xguru도 본문에는 없지만 200달러 플랜의 사용량을 절반으로 줄인 조정이 가장
아쉽다고 남겼다[^gn-xguru].

moregrist는 이를 전형적인 제품 포지셔닝으로 설명했다.
여러 가격대를 내놓았다가 중간이 대부분의 사용자에게 너무 잘 맞으면,
중간을 덜 매력적으로 만들어 위로 밀어 올린다는 것이다[^moregrist].
`openai/pro-plan-reopening.md`가 다룬 Pro 요금제
재조정이 바로 이 흐름의 앞부분이다.
API 고객에게는 진짜 인하이고,
구독 사용자에게는 같은 돈으로 받는 양이 줄어든 개편이다.
모델 소개 글이 앞쪽만 말하고 뒤쪽은 말하지 않으면,
독자가 받는 메시지는 실제 경제적 효과와 반대가 된다.

## 인사이트

### 가격 경쟁은 프런티어 경쟁이 둔화했다는 신호로 읽히기 시작했다

HN에서 gradus_ad는 토큰 가격이 주된
전장이 되는 것은 업계와 투자자에게 불길한 일이라고 썼고[^gradus_ad],
mixdup은 이것이 능력의 정체기에 들어섰다는 증거라면서도 능력이 더 늘지
않아도 지금의 능력을 싸게 만드는 것은 모두에게 큰 이득이라고 덧붙였다[^mixdup].
mpweiher는 최근 AI 회사들의 발표가 거의 모두 같은 성능을 더 싸게
준다는 내용이라며 상품화 단계에 들어선 것 같다고 했다[^mpweiher].

이 해석이 맞는지는 아직 모른다.
글 스스로 Astra가 여전히 최고이고 가장 어려운 과학
작업에는 Astra를 쓰라고 권한다.
하지만 시장의 관심이 최고 점수에서 같은 점수를 얼마에 얻느냐로 옮겨 가는 순간,
모델 회사의 차별화 수단은 연구 성과에서 증류, 서빙 효율,
캐시 설계 같은 운영 기술로 이동한다.
jumploops가 미국 프런티어 연구소들은 아직 중국 연구소처럼
모델을 줄이는 데 집중할 동기가 없었는데 이 모델이 그 첫걸음일 수 있다고 본 것도
같은 맥락이다[^jumploops-distill].

### 모델 이름은 버전 번호가 아니라 계약이 되어 간다

GN의 semjei는 5.5부터 6.1까지 모델이 너무 많아 상황에 따라
골라 쓰기 애매하다며 정리가 필요하다고 했고[^gn-semjei],
mse9000은 5.5는 퇴역이 확정되었다고 답했다[^gn-mse9000].
HN의 jennnnx도 Sol, Terra,
Astra 같은 이름과 5.6, 6, 6.1 같은 번호를 따라갈 수 없다고 했다[^jennnnx].
rpdillon은 Luna, Terra, Sol, Astra가 Anthropic의 Haiku, Sonnet,
Opus 같은 크기 사다리라고 정리했다[^rpdillon].

크기 사다리가 의미를 가지려면 이름이 능력의 범위를 약속해야 한다.
그런데 6 Sol이 Terra 수준이었다는 의심이 퍼지고,
일주일 만에 6.1 Sol로 교체되면서, Sol이라는 이름이 무엇을 보장하는지가 흐려졌다.
기업 고객은 모델 이름을 계약서와 예산에 적는다.
이름이 가리키는 능력이 출시 뒤에 바뀌거나, 같은 이름의 다음 버전이 일주일
만에 나오면, 모델을 고정하고 평가하고 승인하는 기업의 절차가 따라가지 못한다.
결국 모델 회사들은 이름을 마케팅이 아니라, 일정 기간 동안
능력과 가격을 보장하는 서비스 수준의 약속으로 다루라는 압박을 받게 될 것이다.

### 출시 반응은 원문보다 빨리 퍼지고, 원문을 읽지 않은 채 굳는다

HN에서 itzikkatz는 OpenAI가 벤치마크와 테스트 결과를 보여
주지 않은 이유가 있을 것이라고 의심했고[^itzikkatz],
mekpro는 왜 Anthropic이나 다른 회사 모델과 비교하지 않느냐고 물었다[^mekpro].
하지만 원문은 다섯 영역의 벤치마크를 싣고,
그중 세 곳에서 Opus 5.5를 직접 비교한다.
`openai/devday-2026.md`가 지적한 근거 부족은 DevDay 요약 글에 대한 것이었고,
모델 소개 글 자체에는 근거가 있다.

이 어긋남은 출시 주기가 짧아질 때 생기는 부작용을 보여 준다.
요약 글, 뉴스 기사, 트윗이 원문보다 먼저 퍼지고,
토론은 원문이 아니라 그 요약에 대해 이루어진다.
일주일에 한 번 모델이 나오면, 누구도 각 원문을 꼼꼼히 읽을 시간이 없다.
그 결과 모델에 대한 평판은 원문의 수치보다 첫 사흘의 체감과 요약의 인상으로
정해지고, nitinreddy88이 말했듯 출시 첫날의 결과와 이틀 뒤의 결과가 다르다는
의심까지 더해지면 평가의 기준점 자체가 사라진다[^nitinreddy88].

---

[^mynameisjonny_]: <https://news.ycombinator.com/item?id=49896973>

[^the_duke]: <https://news.ycombinator.com/item?id=49897054>

[^TuxSH]: <https://news.ycombinator.com/item?id=49896874>

[^intenex]: <https://news.ycombinator.com/item?id=49897155>

[^zarzavat]: <https://news.ycombinator.com/item?id=49897303>

[^codewithcheese]: <https://news.ycombinator.com/item?id=49898297>

[^jumploops]: <https://news.ycombinator.com/item?id=49899096>

[^gn-click]: <https://news.hada.io/topic?id=34500#cid66615>

[^gn-cronex]: <https://news.hada.io/topic?id=34500#cid66623>

[^JacobAsmuth]: <https://news.ycombinator.com/item?id=49898415>

[^minimaxir]: <https://news.ycombinator.com/item?id=49896762>

[^tensegrist]: <https://news.ycombinator.com/item?id=49898166>

[^joshstrange]: <https://news.ycombinator.com/item?id=49897249>

[^AspireOne]: <https://news.ycombinator.com/item?id=49901659>

[^pazimzadeh]: <https://news.ycombinator.com/item?id=49900156>

[^zamadatix]: <https://news.ycombinator.com/item?id=49900473>

[^heaney-555]: <https://news.ycombinator.com/item?id=49901963>

[^Aboutplants]: <https://news.ycombinator.com/item?id=49897140>

[^gobdovan]: <https://news.ycombinator.com/item?id=49898147>

[^kenzic]: <https://news.ycombinator.com/item?id=49900134>

[^gn-xguru]: <https://news.hada.io/topic?id=34500#cid66618>

[^moregrist]: <https://news.ycombinator.com/item?id=49897415>

[^gradus_ad]: <https://news.ycombinator.com/item?id=49896666>

[^mixdup]: <https://news.ycombinator.com/item?id=49896949>

[^mpweiher]: <https://news.ycombinator.com/item?id=49905652>

[^jumploops-distill]: <https://news.ycombinator.com/item?id=49901567>

[^gn-semjei]: <https://news.hada.io/topic?id=34500#cid66601>

[^gn-mse9000]: <https://news.hada.io/topic?id=34500#cid66604>

[^jennnnx]: <https://news.ycombinator.com/item?id=49902450>

[^rpdillon]: <https://news.ycombinator.com/item?id=49910828>

[^itzikkatz]: <https://news.ycombinator.com/item?id=49897668>

[^mekpro]: <https://news.ycombinator.com/item?id=49896864>

[^nitinreddy88]: <https://news.ycombinator.com/item?id=49903069>
