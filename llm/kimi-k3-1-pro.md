# Kimi K3.1 Pro: 사이버 능력을 학습 데이터에서 덜어 낸 3조 파라미터급 오픈 웨이트

원문: [Kimi K3.1 Pro Tech Blog: Advancing Open Intelligence](https://www.kimi.ai/blog/kimi-k3-1-pro)

HN 토론: <https://news.ycombinator.com/item?id=50212065> (731점, 458개 댓글)

GN 토론: <https://news.hada.io/topic?id=35879>


## 요약

Moonshot의 Kimi 팀이 2026년 10월 23일에 공개한 기술 블로그다.
K3.1 시리즈의 첫 모델인 Kimi K3.1 Pro를 소개하고, 지금까지 가장 성능이 높은
3T급(3조 파라미터급) 오픈 웨이트 모델이며 컨텍스트 창이 100만 토큰이라고 한다.
같이 낸 K3.1 Pro Highspeed는 K3.1 Pro의 2~3배 속도다.
두 모델은 Kimi.ai, Kimi Work, Kimi Code, Kimi API에서 오늘부터 쓸 수 있고 전체
가중치는 2026년 11월 4일까지 공개한다고 한다.
K3.1 Pro는 K3를 훨씬 큰 후처리 학습(post-training) 연산량으로 다시 학습한
버전이며, 수백 개 하위 영역에 걸친 대규모 공동 강화학습(RL)을 위해 RL
프레임워크, 장문 추론, 샌드박스, 롤아웃 스케줄링, 환경 품질 점검 플랫폼을 모두
최적화했다고 한다.

벤치마크는 코딩, 3D, 금융의 세 영역으로 소개된다.
Terminal-Bench 4.0에서 K3.1 Pro는 65.7%로 GPT-6 Astra(58.2%)를 앞서고 Claude
Opus 5.5(66.4%)에 근소하게 뒤진다.
내부 벤치마크 Kimi Code Bench 3.0 Long-horizon에서는 K3의 55.95%에서 61.2%로
올랐다.
CAD 코드 생성으로 다시점 3D 복원을 시험하는 BenchCAD에서는 도구 사용 시 92.7%로,
Opus 5.5(96.2%)와 GPT-6 Astra(95.9%)에 근접한다.
금융에서는 OfficeQA Pro v2에서 64.4로 최고 성능을 냈고, 내부 벤치마크에서 금융
모델링은 K3보다 7.2점, 금융 리서치는 11.6점 오르고 경영 시뮬레이션은 약
4.2배였다고 한다.
사실 정확성 시험(Kimi Hallu Bench Hard)에서 주장 단위 환각률이 K3의 23.4%에서
8.3%로 떨어지고, 오류를 하나라도 포함한 응답의 비율은 K3의 42.4% 수준이라고
한다.
글은 이 시험이 오류를 일으키기 쉬운 예를 일부러 모은 스트레스 테스트이므로
일상의 전체 오류율을 뜻하지 않는다고 단서를 단다.

글의 가장 독특한 절은 사이버 보안이다.
후처리 학습 규모가 커질수록 취약점 연구 성능이 꾸준히 올랐고, 원인을 추적하니
일반 중간 학습 말뭉치에 사이버 관련 내용이 섞여 있었고 RL 환경 혼합에도 사이버
과제가 들어 있었다는 것이다.
중간 학습과 RL 어느 단계에서도 데이터를 제거하지 않으면 하위 사이버 능력이 크게
오르는 것을 예비 실험에서 확인했고, 오픈 웨이트 공개본에서는 두 단계 모두에서
사이버 관련 데이터를 식별해 제거하되 일반 코딩 과제는 남겼다고 한다.
평가 도구는 내부 벤치마크 xdev-bench-hard이고, 위험 저감 조치를 하지 않은
체크포인트는 pass@3에서 90.5%를 풀고 최종 K3.1 Pro는 81.0%를 푼다고 한다.
글은 데이터 제거가 같은 학습 파이프라인이 만들었을 능력을 의미 있게 줄였고,
그래도 이전 모델보다는 크게 올랐으며 공개된 지 3개월 이상 된 최전선 상용
모델보다는 뒤처진다고 쓴다.
공개 원칙으로 첫째 절대적 최전선의 사이버 능력을 넓히는 오픈 웨이트는 내지
않겠다는 것, 둘째 오픈 웨이트에서 쓸 수 있는 사이버 능력을 점진적으로 올리겠다는
것을 든다.

## 분석

### 글의 중심 주장: 오픈 웨이트도 능력 제어를 학습 데이터 단계에서 한다

이 글의 구조적 새로움은 능력 제한을 출시 뒤 가드레일이 아니라 학습 데이터
선별에서 한다고 밝힌 점이다.
오픈 웨이트는 배포 뒤 모델 접근을 통제할 수 없으므로, 제거할 수 있는 시점은 학습
전과 학습 중뿐이다.
글이 사이버 능력의 출처를 일반 말뭉치와 RL 환경 혼합의 부산물로 추적했다는
서술은 능력 제어를 데이터 위생의 문제로 다룬다는 뜻이다.
측정치(90.5%에서 81.0%)는 제어가 효과가 있지만 능력을 없애지는 못한다는 것을
보여 준다.

### 공개 원칙은 최전선을 넓히지 않는다는 상한과 점진적 상향을 함께 말한다

첫째 원칙(최전선을 넓히지 않음)과 둘째 원칙(점진적으로 올림)은 방향이 반대다.
둘은 상한이 프로프라이어터리 최전선이라는 점으로 묶인다.
오픈 웨이트의 사이버 능력은 폐쇄 모델의 최전선 아래에 머물되 그 간격을 시간이
지나며 좁힌다는 것이다.
글은 이를 방어자에게 이로운 이중 용도 능력의 비차별적 공개로 정당화하고,
유지하는 코드를 감사할 수 있는 팀이 늘어난다는 논거를 든다.

### 벤치마크의 조건 서술이 상세하다

각주는 평가 하네스(Claude-Code, Codex, OpenHands 등), 추론 노력(최대),
샘플링(temperature 1.0, top-p 0.95), 외부 모델의 점수 출처(블로그 또는 공식
리더보드)를 모두 밝힌다.
일부 시험에서는 모델이 정답을 온라인에서 찾아낸 실행에 0점을 줬다고 한다.
이 투명성은 점수의 해석에 필요한 조건을 독자가 확인할 수 있게 한다.

## 비평

### 모델이 더 할 수 있지만 안 한다는 서술에 대한 반응

HN에서 rudolftheone은 이 문장을 두고 그들은 더 할 수 있지만 하지 않겠다고 인정한
것이냐고 되물었고,[^rudolftheone] NitpickLawyer는 글의 다른 문단(데이터 제거)을
들어 설명했다.[^nitpicklawyer]
scottyah는 우사인 볼트보다 빠를 수 있어도 세계 기록을 세우지 않는 것과 같아
변명이라고 보았다.[^scottyah]
TuxSH는 데이터 제거를 못마땅해했고, AspireOne은 사이버 능력의 증가를 늦출 수
있다면 좋고 세상이 준비할 시간이 필요하다며 반대했다.[^tuxsh][^aspireone]
CamperBob2는 가중치를 공개하면서 안전을 위해 약화했다고 주장하되 실제로는 하지
않을 수도 있다고 비꼬았다.[^camperbob2-kimi]
이 마지막 가능성은 검증 불가능하며, 공개 뒤 제3자가 같은 벤치마크로 재현하는
것이 유일한 확인 방법이다.

### 제거의 범위가 정의되지 않았다

besterman23은 사이버 보안 데이터라는 범주가 일반 소프트웨어 지식과 어디서
갈리는지, 해킹 관련 언급을 모두 지웠는지를 물었다.[^besterman23]
zozbot234는 사이버 공격은 매우 좁은 영역이고 현대 시스템의 완화책이 많아서
관심이 없다면 후처리에서 빼는 것이 당연한 접근이라고 답했다.[^zozbot234]
ByteAtATime은 보안 지식이 줄면 모델이 부수 효과로 안전하지 않은 시스템을 구현할
우려가 있다고 덧붙였다.[^byteatatime]
글은 제거 기준(식별 방법, 분류 정확도)과 방어 코딩 능력에 미치는 영향의 평가를
제시하지 않는다.

### 벤치마크는 자기 평가이고 성능 평가는 갈린다

점수의 상당수는 내부 벤치마크(Kimi Code Bench, Kimi Hallu Bench Hard)이거나 공개
리더보드의 최대값이다.
minimaxir는 Artificial Analysis 지수가 55로 전체 4위이고 GPT-6 Astra와 Fable
5.1보다 높으며 더 빠르다고 전하면서, 지수 평가에서 1억 5천만 토큰을 생성해
중앙값 8,700만보다 장황하다고 적었다.[^minimaxir]
saberience는 이 지수를 신뢰하지 않고 직접 써 본 순위와 다르다고
했다.[^saberience]
cogman10은 Kimi 모델이 벤치마크 점수는 높지만 실제 성능이 Deepseek, Qwen, GLM만
못했다고 했고, RussianCow는 과도한 생각 때문에 실제 비용이 가격표보다 비싸다고
했으나, InsideOutSanta는 K3의 풀스택과 UI 디자인이 뛰어나다고 반대 경험을
말했다.[^cogman10][^russiancow][^insideoutsanta]
같은 모델에 대한 평가가 갈리는 것은 벤치마크와 개인 작업이 다른 것을 재기
때문이다.

### 구독 한도와 가격이 실사용 판단을 흐린다

johnmlussier는 월 99달러 요금제에서 한 세션이 47분 만에 5시간 할당량에 걸렸다고
했고, SwellJoe는 월 19달러 요금제에서도 한 작업이 5시간 한도와 주간 한도의 큰
부분을 썼다고 했다.[^johnmlussier][^swellJoe]
daviTeodoro가 올린 가격표는 kimi-k3.1-pro가 입력 100만 토큰당 2달러, 출력
10달러(캐시 0.20달러)이고, minimaxir는 이것이 K3의 3달러와 15달러에서 내린
것이라고 짚었다.[^daviteodoro][^minimaxir-price]
red_hare는 토큰이 더 장황하면 사실상 가격이 비교 모델과 가까워질 수 있다고
계산했다.[^red_hare]
이 수치들은 댓글이 전한 것이며 이 문서가 가격 페이지를 확인하지 못했다.

## 인사이트

### 오픈 웨이트의 안전은 공개 시점의 학습 결정으로 이동한다

폐쇄 모델은 접근 통제와 모니터링이라는 사후 수단이 있지만 오픈 웨이트는 가중치가
나가면 끝이다.
이 글이 학습 데이터 제거를 능력 제어의 수단으로 내세운 것은 그 비대칭에서 나온
선택이다.
그러나 일반 코딩과 장기 디버깅 능력이 사이버 과제로 일반화돼 제거 뒤에도 이전
모델보다 크게 올랐다는 서술은 이 수단의 한계를 인정한다.
능력의 상당 부분이 일반 역량에서 오므로 데이터 제거만으로는 상한을 정하기
어렵고, 공개 원칙이 점진적 상향을 말하는 것은 이 한계를 전제로 한 것으로 읽힌다.
이 해석은 이 문서의 것이다.

### 공개 후 첫 검증은 제3자 재현이 맡는다

글의 핵심 수치(90.5%와 81.0%)는 내부 벤치마크이고 벤치마크 과제도 비공개다.
가중치가 공개되면 제3자가 같은 방식의 데이터 제거 효과를 측정할 수 있게 되지만,
제거 전의 체크포인트는 공개되지 않으므로 비교는 불가능하다.
따라서 확인 가능한 것은 최종 모델의 능력 수준이며 제거의 인과 효과는 아니다.
jamienk는 Anthropic이 중국 AI 회사들에 제기한 혐의의 핵심이 증류가 아니라
대량의 침해된 컴퓨터와 신용 카드 사용이라고 썼고,[^jamienk]
johnnyApplePRNG는 상장을 앞둔 회사들의 홍보 문구를 짜깁기한 말이라며
맞섰다.[^johnnyapplepng]
이 논쟁은 근거가 제시되지 않은 채 끝났고 이 문서도 확인하지 못했다.
이 글 자체는 학습 데이터의 출처를 다루지 않는다.

### 이 글을 읽는 방법

이 글은 모델 성능 발표와 능력 제어 정책이 한 문서에 섞인 공개 문서이며, 두
부분을 따로 읽는 편이 좋다.
성능 수치는 조건 서술을 확인하고 직접 작업으로 시험해 볼 문제이고, 정책 부분은
공개 뒤 제3자 평가가 나오면 다시 읽을 문제다.
이 글의 주장을 가를 관찰은 두 가지다.
11월 4일 가중치 공개 뒤 독립 평가에서 사이버 과제 성능이 글의 81.0%와 비슷하게
나오는지, 그리고 같은 모델의 구독 한도와 실사용 비용이 가격표에서 예상하는
수준에 가까운지다.
둘 다 현재 자료로는 확인되지 않는다.

---

[^rudolftheone]: <https://news.ycombinator.com/item?id=50212365>

[^nitpicklawyer]: <https://news.ycombinator.com/item?id=50212851>

[^scottyah]: <https://news.ycombinator.com/item?id=50212409>

[^tuxsh]: <https://news.ycombinator.com/item?id=50212324>

[^aspireone]: <https://news.ycombinator.com/item?id=50213178>

[^camperbob2-kimi]: <https://news.ycombinator.com/item?id=50214377>

[^besterman23]: <https://news.ycombinator.com/item?id=50213204>

[^zozbot234]: <https://news.ycombinator.com/item?id=50213282>

[^byteatatime]: <https://news.ycombinator.com/item?id=50215672>

[^minimaxir]: <https://news.ycombinator.com/item?id=50213093>

[^saberience]: <https://news.ycombinator.com/item?id=50214165>

[^cogman10]: <https://news.ycombinator.com/item?id=50212523>

[^russiancow]: <https://news.ycombinator.com/item?id=50212768>

[^insideoutsanta]: <https://news.ycombinator.com/item?id=50213266>

[^johnmlussier]: <https://news.ycombinator.com/item?id=50212563>

[^swellJoe]: <https://news.ycombinator.com/item?id=50214102>

[^daviteodoro]: <https://news.ycombinator.com/item?id=50212489>

[^minimaxir-price]: <https://news.ycombinator.com/item?id=50212657>

[^red_hare]: <https://news.ycombinator.com/item?id=50213303>

[^jamienk]: <https://news.ycombinator.com/item?id=50213831>

[^johnnyapplepng]: <https://news.ycombinator.com/item?id=50213968>
