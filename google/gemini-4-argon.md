# Gemini 4 Argon: 신뢰된 사이버 방어자에게만 먼저 여는 Google의 프런티어 모델

원문: [Gemini 4 Argon: our next era of frontier intelligence](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)

HN 토론: <https://news.ycombinator.com/item?id=49913571> (1143점, 758개 댓글)

GN 토론: <https://news.hada.io/topic?id=34563>

## 요약

Google DeepMind의 Koray Kavukcuoglu가 2026년 9월 30일 공개한 발표문이다.
Google은 새 프런티어 모델 Gemini 4 Argon을 신뢰된 사이버 방어자 집단에 먼저
풀고 있다고 밝힌다.
이 집단은 Fairwind Program으로 묶이며, 개발자와 기업과 일반
소비자에게는 가능한 한 빨리 열겠다고 하되 날짜는 적지 않았다.
정식 출시는 유료 API 고객과 Google AI Ultra 구독자부터 시작한다고 한다.
미국 정부의 자발적 출시 전 모델 접근 절차에도 참여하고 있고,
단계적 출시가 안전하게 풀려면 필요하다는 설명이다.

가격은 입력 100만 토큰당 2달러, 출력 100만 토큰당 10달러의 도입 가격이고,
캐시된 입력은 입력 가격의 95% 할인이다.
출력 토큰 한도는 기존 64K에서 100만 토큰으로 늘렸다고 하며, 약 15배다.
모델이 수십만 토큰을 한 궤적 안에서 생성할 여유가 있으면 어려운
문제를 한 번에 풀 수 있다는 논리다.

Google 내부 사례가 먼저 나온다.
양자 컴퓨팅 연구자들이 부분 루틴의 시공간 자원(큐비트 곱하기 게이트)을
최적화하는 데 쓰였고, 한 예에서 발표된 기준선을 몇 분 만에 40% 앞질렀다.
Argon 에이전트 팀이 전사 프로파일링 텔레메트리를 분석해 데이터센터 전반의 메모리
최적화를 자동으로 찾아 적용했고, 배포가 끝나면 300 TiB가 넘는 메모리를 확보하며
전체로는 500 TiB에서 1 PiB를 절감할 것으로 추정한다.
C와 C++ 코드베이스를 Rust로 옮기는 일은 re2와 libgav1 같은 핵심
라이브러리의 수만 줄에서 Fuchsia Zircon 커널의 80만 줄 이상까지 번지고 있다.
libgav1에서는 기존 Rust 포팅의 SIMD 코드 3만 2천 줄을, 프로파일 기반
실험을 여러 차례 돌려 컴파일러가 자동 벡터화할 수 있는 안전한 Rust로 바꿨고,
결과 디코더는 기존 Rust 포팅보다 2.7배 빠르면서 출력은 동일하다.
이런 대규모 재작성은 프로덕션에 나가기 전에 자동 검증과 수동 감사,
에뮬레이션 테스트, 리뷰를 거치는 중이라고 밝힌다.

성능 주장은 다음과 같다.
실제 장기 소프트웨어 엔지니어링 과제를 재는 DeepSWE v1.1에서 77.9%로 새 최고
기록이고, 금융과 코딩과 법률과 세무를 GDP 비중으로 가중한 Vals Index에서
선두이며, Zapier의 AutomationBench에서 51.3%로 1위, 장편 영상
이해를 재는 LVBench에서 91.7%로 최고 기록이다.
보안 취약점 수정 능력을 재는 CWE-bench v1에서는 68%로 공동 1위다.

사이버 방어는 발표의 무게중심이다.
Argon은 심각한 소프트웨어 취약점을 자율적으로 찾고 검증하고 고칠 수 있다고 하며,
신뢰된 방어자와 Google 내부 팀에는 사이버 안전장치를 제거한
판본을 내놓겠다고 밝힌다.
보안 기업 Wiz가 공공 인프라 보호 프로그램 Scan for Good에서 이미 쓰고 있고,
이전 프런티어 모델들이 놓친, 전 세계 병원이 쓰는 의료 소프트웨어의 개인 정보
노출 취약점을 찾았다고 한다.

출시 전 강화하는 안전 장치는 네 가지다.
오용 방어는 사이버와 CBRN 공격을 막되 이중 용도 과학 연구는 살리고,
모델의 내부 활성화를 감시하는 기법을 개선했다.
간접 프롬프트 주입 방어는 Gray Swan의 벤치마크에서 선두라고 한다.
정렬 이탈 감시는 모델의 사고 과정과 행동을 모니터링해 필요하면 실행을 멈추고,
훈련 중에도 비슷한 시스템으로 감시하되 발견
내용을 훈련에 되먹임하지 않는다고 한다.
마지막으로 고위험 훈련과 평가 전에 샌드박스를 격리하고 봉인해
시스템을 단단히 한다.

## 분석

### 발표의 대상은 사용자가 아니라 규제 절차와 경쟁사다

발표문은 쓸 수 있는 제품을 내놓지 않았다.
접근은 신뢰된 사이버 방어자로 한정되고,
일반 공개 시점은 가능한 한 빨리라는 문장뿐이다.
HN에서 babelfish는 이 문장을 인용하며 Gemini가 모델을 출시하지
못한다는 비판을 떨치지 못했다고 썼다[^babelfish].
arjunchint는 아무것도 쓸 수 없고 비교할 벤치마크도 하나뿐인데 왜 발표하느냐고
물었다[^arjunchint].

답변은 두 갈래였다.
kylecazar는 Google이 전날 백악관의 초지능 관련
협약에 서명했고 책임 있는 출시를 약속했으니, 발표가 협약까지
미뤄졌다가 출시는 준수를 보이려고 더 미뤄졌을 수 있다고 추측했다[^kylecazar].
ncruces는 이 모델을 쓸 수 있고 써 온 사람들은 발표
전에는 이야기할 수 없었을 것이라며,
비밀 유지 계약 때문에 발표가 먼저 필요했다고 풀었다[^ncruces].
발표문이 미국 정부의 자발적 출시 전 접근 절차를 직접 언급한 것을 보면,
발표 시점이 제품 준비보다 절차의 단계에 맞춰졌다는 해석이 설득력을 얻는다.

### 사이버 방어를 앞세운 출시는 접근권을 선별하는 구조다

이 모델의 가장 강한 능력은 취약점을 찾고 고치는 일이고,
바로 그 능력이 첫 출시 대상을 정한다.
방어자에게는 안전장치 없는 판본을 주고 일반
사용자에게는 오용을 거절하는 판본을 준다는 설계는,
같은 능력을 누구에게 어떤 조건으로 열지를 모델 밖의 신뢰 체계에 맡긴다.
`security/glm-5-3-cyber-capabilities.md`가 다룬 Anthropic의 경고는 이런
능력이 누구나 받을 수 있는 모델로 퍼지는 것을 문제 삼았다.
Argon의 발표는 그 반대 방향의 답이다.
능력이 퍼지기 전에 방어자에게 먼저 줘 격차를 만든다는 것이다.

이 접근이 성립하려면 신뢰된 방어자의 범위가 좁고 명확해야 한다.
발표문은 Fairwind에 누가 들어갈 수 있는지,
어떤 조건에서 안전장치 없는 판본을 쓸 수 있는지를 적지 않는다.
Wiz의 사례, 즉 병원 소프트웨어의 취약점 발견은 방어의 가치를 보여 주지만,
같은 모델이 공격에도 똑같이 강하다는 사실도 함께 보여 준다.

### 가격은 경쟁사와 같은 숫자로 수렴했다

도입 가격 입력 2달러, 출력 10달러,
캐시 입력 95% 할인은 같은 시기 OpenAI의 GPT-6.1 Sol의 표준 가격, 즉 입력 2달러,
캐시 입력 0.10달러, 출력 10달러와 같은 숫자다(`openai/gpt-6-1-sol.md`).
Argon의 캐시 가격은 입력 가격의 5%이므로
계산하면 0.10달러가 되어 Sol과 일치한다.
HN에서 LucasBrandt는 Astra에 비해 입력과 출력이 5배,
캐시 입력이 10배 싸다고 정리했다[^LucasBrandt].

그런데 GodelNumbering은 발표문의 각주를 인용해 도입 기간이 끝나면 입력 4달러,
출력 20달러가 적용된다고 알렸다[^GodelNumbering].
Artificial Analysis 기준으로 작업당 비용이 1.99달러로 Astra high나
Opus 5.5 high보다 높고 Sol 6.1 Max의 0.72달러보다 훨씬
높다는 계산도 함께 올렸다.
이 수치는 댓글이 전한 것이고 이번에 직접 확인하지는 못했지만, 같은 단가에서
작업당 비용이 다르다는 것은 토큰 사용량이 가격만큼 중요하다는 뜻이다.

## 비평

### 벤치마크 수치가 하나뿐이라 선두라는 말을 확인할 수 없다

발표문이 구체적인 숫자를 준 것은 DeepSWE 77.9%, AutomationBench 51.3%,
LVBench 91.7%, CWE-bench 68% 정도다.
Vals Index와 Vals Finance Agent와 Harvey의 법률 벤치마크는 선두라고만
쓰고 점수와 비교 대상을 적지 않는다.
HN의 nonethewiser는 모든 모델이 범주의 75%에서 1위라고 발표하는 것이 통계적으로
가능하냐고 물었고[^nonethewiser], sebzim4500은 벤치마크 선택의 편향과 번갈아
앞서는 구도가 함께 작용한다고 답했다[^sebzim4500].

신뢰의 문제도 있다.
pietz는 Gemini 3.8 Flash가 보고한 수치와 실제 경험 사이의 간극을 겪은 뒤로
Google이 내놓는 숫자는 의미가 없다며, 가중치가 조정된 뒤 Artificial Analysis에서
가장 크게 떨어진 모델이라고 썼다[^pietz].
반대로 rcr-anti는 Artificial Analysis의 환각률이 15%로,
OpenAI 최신 모델이 40~50%대이고 Anthropic이 60~70%대인 것과 비교해 눈에 띄게
낮다고 전했다[^rcr-anti].
두 평가가 정반대인 것은 숫자가 어떤 지표를 고르느냐에 크게
좌우된다는 것을 보여 준다.
이 댓글의 수치들은 직접 확인하지 않았고, 발표문에는 환각에 관한 수치가 없다.

### 내부 사례는 검증할 수 없는 단위로 쓰였다

300 TiB, 500 TiB에서 1 PiB, 40%, 2.7배는 인상적이지만 모두 Google 내부
시스템에서 나온 수치다.
메모리 절감은 배포가 끝나면이라는 조건과 추정이라는 표현이 붙어 있고,
양자 알고리즘 최적화는 어떤 기준선을 어떤 알고리즘에서 40% 앞섰는지 적지 않는다.
HN의 elAhmo는 첫 번째 사례가 양자 알고리즘 최적화라는 점을,
일상에 얼마나 유용한지 빗대어 꼬집었다[^elAhmo].

libgav1 사례의 문장은 스스로를 약화시키기도 한다.
기존 Rust 포팅보다 2.7배 빠르지만 최적화된 C++에 가까워졌다는 말은,
여전히 C++보다는 느리다는 뜻이다.
mlmonkey가 Rust가 아직 C++를 이기지 못한다고 짚었고[^mlmonkey],
ariwilson은 자기 블로그 글에서 스스로를 깎는 표현이라고 썼다[^ariwilson].
zem은 이미 최적화된 C++ 라이브러리와 더 안전하지만 느린 Rust
포팅이 있었고, 새 Rust 버전이 성능 격차를 상당히 회복했으니 충분히
좋은 결과라고 옹호했다[^zem].
이 논쟁은 발표문이 비교 기준을 기존 Rust 포팅으로만 잡은 데서 비롯한다.

### 추론 투명성을 촉구하면서 자신의 API에서는 사고 과정을 숨긴다는 지적이 있다

발표문은 업계가 모델의 사고 과정이 정렬 문제를 진단하는 데 쓸모 있도록
추론의 투명성을 유지하라고 촉구한다.
HN의 lukewarm707은 Google이 API로 실제 사고 과정을 돌려주지 않고 작은 모델이
만든 사고 요약을 돌려주므로 외부에서 감시할 수 없다고 주장했다[^lukewarm707].
이 주장은 댓글의 것이고 이번에 확인하지 못했다.

사실이라면 촉구의 무게가 달라진다.
Google 내부에서는 감시하고,
외부 사용자와 연구자는 감시할 수 없는 구조가 되기 때문이다.
janustimes는 사고 과정 감시를 처음 제안하고 대중화한 곳이 OpenAI라는 점을 들어
Google이 그 기법의 주인은 아니라고 지적했다[^janustimes].
발표문은 훈련 중 발견한 내용을 훈련에 되먹임하지
않는다는 주의도 적었지만, 그 주장을 외부가 검증할 방법은 없다.

## 인사이트

### 발표와 출시가 분리되면서 발표 자체가 하나의 제품이 되었다

예전에는 모델 발표와 출시가 같은 날이었다.
Argon은 발표가 먼저고 출시가 한참 뒤다.
HN의 bakugo는 우리 모델은 너무 위험해서 바로 공개하기 어렵다는 말이 이제 표준
관행이 되었다고 꼬집었다[^bakugo].
woggy는 이런 발표는 출시 직전에 하거나 최소한 날짜를 밝혀야 한다고 했다.[^woggy]

이 분리는 의약품의 단계적 승인과 닮았다.
임상 결과는 발표하되 허가는 별도 절차를 거친다.
다른 점은, 의약품에는 허가 기관이 정한 공개된 단계가 있지만 모델에는 자발적
절차와 회사의 판단이 있다는 것이다.
그래서 발표는 안전 절차를 밟고 있다는 신호, 경쟁사가 앞서가는 뉴스 주기에서
존재감을 지키는 수단, 이미 쓰는 소수의 비밀 유지를 푸는 장치가 한꺼번에 된다.
arjunchint의 말대로 발표가 내부 일정에 맞춘 것이라는 의심도 자연스럽게 따라온다.
사용자에게 가치가 없는 발표가 회사에게는 가치가 있는
한, 이 관행은 더 퍼질 것이다.

### 가격과 단가가 수렴하면 경쟁은 하네스와 접근성으로 옮겨 간다

같은 숫자로 수렴한 가격에서 사용자가 고르는 기준은 모델 점수보다
모델을 담은 도구와 얻을 수 있는지가 된다.
HN에서 copperx는 하네스에 묶이지 말고 사용자가 하네스를 고르게 해 주지
않는 모델, 즉 Google을 피하라고 했다[^copperx].
adithyassekhar는 벤치마크는 좋아도 실제 세계에서는 코딩
하네스 덕분에 Claude가 앞서 있다고 했고[^adithyassekhar],
GN의 click도 모델이 아무리 좋아도 Antigravity CLI의 하네스가 너무 멍청해서
믿음이 안 가고 차라리 Pi에서 쓰게 해 주면 좋겠다고 적었다[^click].
모델 점수는 같은 곳을 향하는데, 모델을 여는 문은 회사마다 다르다.

접근성도 마찬가지다.
Androider는 유료 Pro 사용자인데 앱에서 고를 수 있는 최신 모델이 3.6이라고
했고[^Androider], wasabi991011은 3.8 Flash가 발표일부터 Pro 사용자에게 열려
있었다고 바로잡았다[^wasabi991011].
같은 모델 제품군 안에서도 어느 요금제가 어떤 모델에 닿는지 알기
어렵다는 점이 사용 경험의 가장 큰 변수로 남는다.

### 에이전트가 쓰는 속도와 사람이 감사하는 속도의 차이가 이전 작업의 병목이다

발표문은 Zircon 커널 80만 줄 이상의 Rust 이전을 이야기하면서,
자동 검증과 수동 감사와 에뮬레이션 테스트와 리뷰를 거치는 중이라고 쓴다.
쓰는 쪽은 에이전트가 빠르게 하고, 병목은 검증으로 옮겨 간다.
HN의 tazjin은 cppnext 팀이 Rust를 고려조차 하지 않고 Carbon과 Swift를 보던
시절을 회고했고[^tazjin], uvdn7은 핵심 C++ 라이브러리를 대규모로
옮긴다면 몇 년 뒤에 C++가 여전히 의미 있을지 모르겠다고 했다[^uvdn7].
이 논쟁이 놓치기 쉬운 것은 이후의 일이다.

6thbit은 자동 이전된 코드베이스를 유지보수하는 것이 전업이 될 사람이
있을지, 그 사람은 Rust에는 낯설어도 제품에는 능숙할 것이라고 상상했다[^6thbit].
이 상상은 자동 이전의 비용 구조를 정확히 짚는다.
글쓰기 비용은 0에 가까워지지만, 그 코드를 이해하고 책임질
사람의 비용은 그대로다.
mhils는 Google의 Bughunters 블로그에 이미 AI 보조 Rust
재작성이 여럿 프로덕션에 있다는 글이 있다고 알렸는데[^mhils],
이는 이 흐름이 발표문의 약속이 아니라 진행 중인 일이라는 증거다.
다음 질문은 몇 줄을 옮겼느냐가 아니라,
옮긴 코드의 결함 책임을 누가 어떤 절차로 지느냐다.

---

[^babelfish]: <https://news.ycombinator.com/item?id=49913608>

[^arjunchint]: <https://news.ycombinator.com/item?id=49913814>

[^kylecazar]: <https://news.ycombinator.com/item?id=49916277>

[^ncruces]: <https://news.ycombinator.com/item?id=49915108>

[^LucasBrandt]: <https://news.ycombinator.com/item?id=49913663>

[^GodelNumbering]: <https://news.ycombinator.com/item?id=49914488>

[^nonethewiser]: <https://news.ycombinator.com/item?id=49913956>

[^sebzim4500]: <https://news.ycombinator.com/item?id=49914307>

[^pietz]: <https://news.ycombinator.com/item?id=49914409>

[^rcr-anti]: <https://news.ycombinator.com/item?id=49914850>

[^elAhmo]: <https://news.ycombinator.com/item?id=49913813>

[^mlmonkey]: <https://news.ycombinator.com/item?id=49916294>

[^ariwilson]: <https://news.ycombinator.com/item?id=49914119>

[^zem]: <https://news.ycombinator.com/item?id=49914241>

[^lukewarm707]: <https://news.ycombinator.com/item?id=49914968>

[^janustimes]: <https://news.ycombinator.com/item?id=49913836>

[^bakugo]: <https://news.ycombinator.com/item?id=49913924>

[^copperx]: <https://news.ycombinator.com/item?id=49915968>

[^adithyassekhar]: <https://news.ycombinator.com/item?id=49917676>

[^click]: <https://news.hada.io/topic?id=34563#cid66698>

[^Androider]: <https://news.ycombinator.com/item?id=49913873>

[^wasabi991011]: <https://news.ycombinator.com/item?id=49915319>

[^tazjin]: <https://news.ycombinator.com/item?id=49913673>

[^uvdn7]: <https://news.ycombinator.com/item?id=49913926>

[^6thbit]: <https://news.ycombinator.com/item?id=49914513>

[^mhils]: <https://news.ycombinator.com/item?id=49914748>

[^woggy]: <https://news.ycombinator.com/item?id=49917701>
