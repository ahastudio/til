# Clef: Cloudflare가 Jev의 인터페이스를 복제하고 파인튜닝 서비스를 얹었다

원문: [Introducing Clef: our open-source decision models, and new RL fine-tuning platform | Cloudflare Blog](https://blog.cloudflare.com/clef-decision-models/)

HN 토론: <https://news.ycombinator.com/item?id=49923692> (467점, 170개 댓글)

GN 토론: <https://news.hada.io/topic?id=34621>

## 요약

Cloudflare의 Michelle Chen, Alex Reneau,
Kevin Flansburg가 2026년 10월 1일에 쓴 Birthday Week 글이다.
Typesafe AI의 Jev가 만든 결정 모델(decision model) 개념, 곧 입력이
무엇이든 경계가 있는 구조화된 출력을 싸고 빠르고 일관되게 내놓는 모델을 받아,
Cloudflare가 직접 학습한 `Clef`와 `Clef-flash`를 Workers AI에 올렸다는 발표다.
모델은 Jev API와 완전히 호환되고,
가중치는 Apache 2.0으로 Hugging Face에 공개한다.
글은 Clef가 현재 Jev Decision Index에서 선두라고 주장하며, 마지막에 고객이
Clef를 자기 용도에 맞춰 파인튜닝하는 강화학습(RL) 서비스를 처음 선보인다.

결정 모델의 정의는 이렇다.
고객 지원 메시지(입력)를 주고 긴급한지,
어느 팀이 맡아야 하는지 물으면 확률이 붙은 타입 있는 답(출력)을 돌려주고,
코드가 이를 라우팅이나 에스컬레이션이나 사람에게 넘기는 데 쓴다.
API 예시는 `noul`(참일 확률), `choice`(기준이 붙은 선택지),
`score`(순서형 점수) 세 가지 질문 형태를 보여 준다.
Cloudflare 위협 인텔리전스 팀은 도메인을 Clef에 넣어 분류하는 데 시험했고,
사이트를 가져와 렌더링하고 분류하는 데 2.2초가 걸린 반면 가장 빠른 범용 LLM인
gpt-oss-120b는 4.7초가 걸렸고 분류도 두 개만 내놨다고 한다.
이름은 악보에서 음높이를 정해 주는 음자리표(clef)에서 따왔다.

글이 내세우는 차별점은 셋이다.
이미지를 받는 비전 인코더가 있어 시각 콘텐츠도 분류하고(Jev는 현재 텍스트만),
컨텍스트 창이 64k로 Jev의 32k보다 크며,
여러 품질 벤치마크에서 경쟁력 있게 점수를 낸다는 것이다.
벤치마크 표에서 Clef는 BFCL 98.47, ToolRet 69.19, API-Bank 91.93,
BANKING77 94.20, CLINC150+OOS 97.43에서 Jev(95.75, 65.28, 88.19, 79.74,
89.27)보다 높고, When2Call(72.37 대 80.97), BRIGHT(45.91 대 47.52)에서는 낮다.
PhishNChips에서는 79.60으로 Jev의 62.55보다 높지만 DiffusionGemma Jev의
85.35에는 못 미친다.
Typesafe 자체 평가 묶음 네 개 중 세 개에서 Jev를 이겼고(송장 처리 64.7 대 61.8,
고객 서비스 76.3 대 76.0, 보안 사고 62.9 대 61.7),
에이전트 트레이스 관측성에서는 졌다(68.5 대 71.6).
43개 평가 전체의 중앙값 지연은 Clef 209.3ms, Clef-flash 38.8ms, Jev 524.1ms,
DiffusionGemma Jev 84.4ms, Kev-9B 51.4ms, Laya 5.8ms이고 p95는 순서대로 238.6,
122.4, 536.0, 211.2, 187.9, 222.5ms다.

학습 방식은 이렇게 설명된다.
Jev가 나온 주에 Cloudflare도 DiffusionGemma를
LLM의 logprob을 노출해 결정론적 확률을 내도록 바꾼 자체 실험을 공개했고,
Clef는 그 개념을 이어받되 백본을 Qwen으로 바꿨다.
Clef는 Qwen3.8-27B, Clef-flash는 Qwen3.5-9B를 동결하고 라우팅 헤드와 랭크 256
저랭크 어댑터를 함께 최적화했다.
추론은 Qwen으로 프리필(prefill)만 한 번 하고 유효한 스키마 선택지를 병렬로 점수
매기는 비자기회귀 방식이라 토큰을 하나씩 생성하지 않는다.
후학습 손실은 레이블 평활화 교차 엔트로피와 확률 보정을 다듬는 Brier 손실이고,
인접한 순서형 선택지에 부분 점수를 주고 정확한 레코드 출력을 보상하며
분포 이동을 막는 참조 페널티를 두는 RLCD(Reinforcement Learning for Calibrated
Decisions)를 보조 목표로 쓴다.
데이터는 필드 순서, 프롬프트,
스키마 구조를 바꿔 만든 Cloudflare 내부 합성 데이터셋이다.

RL 서비스는 두 단계다.
먼저 전방 배치 엔지니어(FDE) 팀이 고객과 직접 파인튜닝하고,
거기서 배운 것으로 데이터 수집, 파인튜닝,
재배포를 Cloudflare 안에서 하는 셀프 서비스 플랫폼을 만든다.
구성 요소는 AI Gateway(AI 트래픽을 통과시켜 데이터셋을 자동 생성), Workers
AI(기본 Clef에 대한 롤아웃 생성), Containers(점수 매기기와 재생용 RL 샌드박스),
새로 나온 Trainer(파인튜닝된 가중치 갱신), Workers AI의 BYO Model(재배포)이다.
Cloudflare는 요청과 응답을 읽거나 저장하거나 학습에 쓰지 않는다고 보장하며,
파인튜닝 제품을 쓰는 경우만 예외라고 적는다.

## 분석

### 개념은 Jev에서, 구현은 알려진 부품에서 왔다

글의 첫 문단이 Jev의 공을 인정하는 방식이 눈에 띈다.
분류 모델은 오래전부터 있었지만,
Jev가 도입한 것은 새로운 분류 범주를 위해 모델을 계속 재학습하지 않고도 임의의
입력에 쓸 수 있는 결정 모델이라는 개념이라고 말한다.
이어서 Clef가 Jev API와 호환된다는 점을 강조해 바꿔 쓰기가 쉽다고 한다.
개념의 출처를 인정하고 인터페이스를 따르는 것은 시장에서 표준을 만든 쪽을
따라가는 전형적인 전략이다.

기술 구성은 새로운 부품이라기보다 알려진 부품의 조합이다.
기반 LLM을 동결하고 어댑터와 작은 헤드만 학습하며, 생성
대신 프리필 한 번으로 선택지를 점수 매긴다.
이 구조에서 지연이 줄어드는 이유는 토큰 생성이 없기 때문이고,
확률이 나오는 이유는 선택지별 점수를 직접 읽기 때문이다.
HN의 woah는 트랜스포머가 원래 확률 집합을 내고 그것이 다음 토큰이든
구조화된 선택지 목록이든 될 수 있다며, Jev가 혁신한 것은 인터페이스와 API와 제품
개념이고 그 인터페이스는 쉽게 복제된다고 정리했다.[^woah]

### 보정이 이 범주의 약속을 지탱한다

결정 모델의 가치는 확률을 믿고 임계값으로 자동 게이팅할 수 있다는 데 있다(이
저장소의 Laya 실측 노트도 같은 지점을 짚었다).
그래서 글이 보정(calibration)을 별도로 다룬 점이 중요하다.
Brier 손실과 RLCD라는 두 장치가 모두 이 목적이다.
HN의 zwaps가 보정에 대한 언급이 없고 또 하나의 LLM 파인튜닝이냐고 묻자,
글쓴이 Kevin Flansburg로 보이는 kflansburg가 글의 Brier 손실 문장을 그대로
인용해 답했다.[^zwaps][^kflansburg]
다만 글은 보정이 얼마나 잘 됐는지의 수치(보정 오차나 신뢰도
도표)를 제시하지 않는다.

### 사업 구조는 모델이 아니라 데이터 루프를 향한다

글의 후반부는 모델 공개보다 RL 서비스에 무게를 둔다.
AI Gateway로 트래픽을 통과시키면 데이터셋이 자동으로 만들어지고,
Workers AI에서 롤아웃을 만들고, Containers에서 점수를 매기고,
Trainer로 가중치를 갱신하고, BYO Model로 재배포한다는 파이프라인은 Cloudflare
플랫폼의 기존 상품을 한 줄로 꿴 것이다.
글은 Jev에 대한 관심이 작고 빠르고 특화된 분류 모델의 수요를 보여 줬고,
이를 RL 환경을 실험할 첫 틈새로 골랐다고 쓴다.

이 구조에서 모델은 입구이고 고객의 트래픽과 라벨이 쌓이는 곳이
Cloudflare 위라는 점이 가치다.
FDE 팀이 먼저 직접 붙는 것도 같은 맥락이다.
셀프 서비스 플랫폼을 만들기 전에 어떤 데이터와 환경이 필요한지
배우는 단계이기 때문이다.

## 비평

### 벤치마크는 이기는 줄이 많지만 일부는 지고, 채점 기준은 Cloudflare가 운영한다

표에서 Clef가 Jev를 이기는 항목이 많은 것은 사실이다.
그러나 When2Call(72.37 대 80.97), BRIGHT(45.91 대 47.52),
Typesafe 평가의 에이전트 트레이스 관측성(68.5 대 71.6)에서는 졌고,
PhishNChips에서는 DiffusionGemma Jev(85.35)에 졌다.
Clef-flash는 CLINC150+OOS에서 66.77로 Clef(97.43)와 격차가 크다.
글은 선두라는 문장과 함께 “경쟁력 있게” 점수를 냈다고 쓰는데, 두 표현의 사이에는
승패가 섞인 표가 있다.

선두의 근거인 Jev Decision Index의 실시간 데모 사이트는 Cloudflare의
`workers.dev` 아래에 있다.
이름은 Jev의 것을 따르지만 채점과 호스팅은 Cloudflare가 한다는 뜻으로
읽힌다(지수의 정의 주체는 글에서 확인하지 못했다).
HN의 segmondy는 Jev 수준이라고 주장하는 많은 모델이 결국 비자명한 과제에서
실패한다며, 분류 모델에 게임을 시켜 보면 대부분 형편없이 플레이해 좁은 범위의
모델임이 드러난다고 했다.[^segmondy]
또 Cloudflare가 상위 오픈 벤치 대안들과 비교하지 않았다고 지적했다.

### 지연 주장은 사용자들의 측정과 맞지 않는다

글의 표에서 Jev의 중앙값 지연은 524.1ms로 표의 모델 중 가장 느리고 Clef는
209.3ms, Clef-flash는 38.8ms다.
그런데 HN에서 직접 호출해 본 사람들의 수치는 정반대에 가깝다.
ralusek은 Jev가 중앙값 230ms인데 Clef-flash는 661ms였다고
했고,[^ralusek] pdlug는 같은 과제에서 호스팅 p50이 Clef 약 850ms, Jev 약
110ms였다고 적었다.[^pdlug]
agrippanux는 Clef가 Jev보다 2~3배 느리고 혐오 발언을 덜
잡았다고 했으며,[^agrippanux] alex7o는 Jev 대체로 시험했는데 3초가 걸려 쓸 수
없었다고 했다.[^alex7o]
nikcub의 250건 미니 벤치도 Clef가 5.2배 비싸고 훨씬 느리며 결과는 근소하게 나은
정도라고 했다.[^nikcub]

차이의 원인은 글만으로는 알 수 없다.
글의 지연은 평가 하네스의 모델 측 값이고 사용자는 호스팅된 API의 종단 지연을
쟀을 수 있다(필자의 추정이다).
그렇다면 “엣지 GPU 덕분에 낮은 네트워크 지연”이라는 글의 설명이 호스팅 값에서는
확인되지 않은 것이다.
필자는 이 수치들을 직접 재현하지 못했으며 모두 댓글의 자기 보고다.

### 가격과 비용은 글의 비교에서 빠져 있다

글의 파레토 도표는 지연과 결정 지수만 비교한다.
CBLT는 파레토 경계에 비용이 없다는 점을 이상하게 여겼다.[^CBLT]
vulture916은 입력 토큰 기준 가격이 Jev $0.042/m, Clef $0.24/m이고
호출당 300토큰이면 100만 건에 약 $12.60 대 약 $72라고 계산했고,[^vulture916]
ssiddharth는 Clef-flash($0.09/m)가 훨씬 경쟁력 있다고 적었다.[^ssiddharth]
이 가격은 댓글이 인용한 것이며 글에는 없다.
jampekka는 출력 항목이 너무 적어 출력 가격은 사실상 무시해도 되므로 Jev의 “출력
무료” 홍보가 거의 누락에 의한 거짓말이라고 했다.[^jampekka]
글이 비용을 비교에서 뺀 것은 Clef의 더 큰 모델(27B)이 비싼 쪽에
있다는 사실을 가린다.

### “오픈소스”라는 단어는 가중치에 대한 것이다

제목은 오픈소스 결정 모델이라고 하고 본문도 모델을 완전히
오픈소스로 공개한다고 쓴다.
HN의 buildbuildbuild는 가중치는 허용적인 라이선스지만 데이터와 학습 파이프라인이
공개되지 않아 독점적인 Qwen 출발점에서 재현할 수 없으니 오픈 웨이트일 뿐
오픈소스가 아니라고 지적했고,[^buildbuildbuild] dang이 이에 맞춰 HN 제목을
“weights”로 바꿨다.[^dang]
합성 데이터셋이 내부 자료이고 후학습 코드도 글에는 없으므로 이
지적은 글의 서술과 맞는다.

글이 밝히지 않은 선택도 있다.
teleforce는 글이 처음에는 DiffusionGemma로 Jev
같은 시스템을 시험하다가 Qwen 기반으로 바꿨다고 쓰면서,
바꾼 이유와 근거는 말하지 않았다고 지적했다.[^teleforce]
백본 교체의 이유는 재현하려는 사람에게 가장 필요한 정보 중 하나다.

### 데이터 우위 서사는 학습 자료와 이어지지 않는다

글은 Cloudflare가 15년 이상의 네트워크 데이터와 오래 쌓은 라벨이 있어 특정
용도에 파인튜닝하면 범용 Clef보다 정확하고 빠르다고 말한다.
HN의 ranyume은 그 데이터가 있다면 왜 처음부터 그것으로 모델을 학습하지 않고
Clef가 필요했느냐고 물었다.[^ranyume]
글이 밝힌 Clef의 학습 데이터는 합성 데이터셋이며 내부 라벨 데이터가
쓰였다는 설명은 없다.
파인튜닝으로 얼마나 개선됐는지의 수치도 글에는 없고,
내부 팀과 협의 중이라는 문장뿐이다.

글이 내세운 도메인 분류 사례도 운영 수준인지는 알 수 없다.
johnbatch는 글이 인용한 위협 인텔리전스 팀의 시험이 운영에 쓰이는지는
모르겠지만, 자신이 쓰는 Cloudflare ZTNA 에이전트의 웹사이트 분류는 개선이
많이 필요하다고 했다.
어젯밤에는 보험사 사이트가 미분류라 차단 페이지가 떴고,
Clef가 2초 만에 판정할 수 있다면 지원 요청을 내고 몇 시간을 기다릴 일이 없을
것이라고 적었다.[^johnbatch]
이는 글의 2.2초 사례가 시험 단계의 수치이고 운영 중인 분류 제품에는 아직
반영되지 않았을 수 있다는 지적이다(반영 여부는 글에서 확인되지 않았다).

## 인사이트

### 인터페이스는 복제되고 경쟁은 보정과 평가로 옮겨 간다

Jev가 나온 지 몇 주 만에 호환 모델이 여럿 나왔다는 사실이 이
범주의 구조를 보여 준다.
HN에서 TeMPOraL은 이것이 새 패러다임이 아니라 오래 방치된 쉬운 열매이고
Typesafe가 처음 집어 들었을 뿐이라고 했고,[^TeMPOraL] ramoz는 접근하기 쉬운
프로그래밍 인터페이스를 잘 만든 것이 공이며 누구나 다른 모델에 같은 입출력을
씌울 수 있다고 했다.[^ramoz]
janalsncm은 모델과 구조는 숙련된 엔지니어에게 어렵지 않고 어려운 것은 데이터와
평가이며, 핫도그가 샌드위치인지를 분류하는 Jev 데모는 아무도 신경 쓰지 않는
문제라고 했다.[^janalsncm]

API가 호환되면 전환 비용이 사라지고,
경쟁은 인터페이스가 아니라 인터페이스 뒤의 품질로 옮겨 간다.
결정 모델에서 그 품질은 정확도 평균이 아니라 보정과 특정 도메인에서의 신뢰다.
fastball은 이 입출력 형태가 같다는 이유로 모든 결정 모델을 Jev와
비슷하다고 보는 것은 마르코프 체인이 GPT-2와 멀지 않다고 하는 것과 같으며,
가치는 지능과 출력 형태의 결합에 있다고 했다.[^fastball]
calebkaiser는 Jev의 발표가 정확도와 지연과 가격을 함께 얻은 구조를 찾았다는
것이었고, 그 뒤 복제 모델이 쏟아지는 것은 딥러닝 부품이 인기를 얻을 때의 흔한
일이라고 정리했다.[^calebkaiser]
호환 API가 흔해질수록 사용자가 판단해야 할 것은 같은 요청에 얼마나 맞고 얼마나
믿을 수 있고 얼마나 싸냐는 자기 데이터 기준의 비교다.

### 작은 출력의 모델은 입력 처리와 호스팅 오버헤드로 승부가 갈린다

출력이 몇 개의 선택지뿐이라면 비용과 지연의 대부분은 입력 처리(프리필)와
서빙 경로에서 나온다.
Jev의 출력 무료 홍보와 입력 토큰 중심의 가격 표기가 모두 이 점을 반영한다(위
비평에서 본 댓글의 가격 정보다).
호스팅 위치도 변수다.
글은 엣지 GPU로 낮은 네트워크 지연을 얻는다고 주장하지만,
사용자 측정은 큐 대기, 콜드 스타트,
배치 같은 모델 밖 요인이 지연을 좌우할 수 있음을 시사한다(필자의 추정이다).

이는 결정 모델을 에이전트의 핫 패스에 넣는다는 글의 제안에 직접 영향을 준다.
핫 패스에서는 평균보다 꼬리 지연이 중요하고,
p95가 중앙값의 몇 배인지 모르면 설계할 수 없다.
글의 p95 수치(Clef 238.6ms)는 모델 측이므로 호스팅 경로의 꼬리는
사용자가 직접 재야 한다.

### RL 서비스는 데이터 루프를 판다

AI Gateway가 트래픽을 통과시키며 데이터셋을 자동으로 만든다는 설명에서 이
상품의 본질이 드러난다.
고객이 쌓은 요청과 응답이 곧 파인튜닝 데이터이므로,
트래픽을 가진 쪽이 학습 자원을 가진 쪽이 된다.
CDN에서 엣지 컴퓨트로 간 Cloudflare의 이동과 같은 구조다(필자의 비유다).
통로를 쥔 회사가 통로 위의 데이터로 부가 서비스를 파는 것이다.

여기에는 글이 다루지 않은 긴장이 있다.
Cloudflare는 요청과 응답을 읽거나 저장하거나 학습에 쓰지 않는다고 보장하면서,
같은 글에서 AI Gateway가 데이터셋을 자동으로 만든다고 한다.
이 둘은 파인튜닝에 옵트인한 경우만 예외라는 한 문장으로 갈린다.
이 경계가 실제 설정과 계약에서 어떻게 구현되는지가 기업
고객의 채택을 정할 것이다.
amluto가 지적한 한계도 같은 방향이다.
Jev에는 사전 확률(prior)을 넘길 방법이 없고 텍스트로 넣으면 잘 안 되므로
파인튜닝 없이는 출력이 거의 무의미할 수 있다고 했는데,[^amluto] 파인튜닝을 파는
쪽에서는 이 불편이 곧 수요다.
반면 mikeocool은 파인튜닝할 데이터를 모을 거라면 구식 분류기를 직접 학습해 더
싸고 빠르게 만들 수 있다고 반박한다.[^mikeocool]

### 결정 모델이 늘수록 에이전트는 추론 호출과 결정 호출로 갈라진다

글은 에이전트가 맥락을 모으고 결정하고 행동하며 필요하면 사람에게 넘긴다고
말하고, 사람이 루프에 없어도 되는 시대라고 표현한다.
cakoose는 이미 많은 LLM 에이전트 행동에
사람이 없고 그것은 신뢰의 문제이지 새로운 패러다임이 아니라고 짚었고,
단일 결정을 출력하는 모델이 어떻게 맥락을 모으느냐고 물었다.[^cakoose]
meander_water는 결정 모델이 결정론적이라는 글의 대비가
오해를 부른다며 반복 호출하면 구조화된 출력의 LLM처럼 다른 결정이 나올 수 있다고
했다.[^meander_water]

두 지적을 합치면 글의 표현이 느슨하다는 점이 보이지만,
방향 자체는 실제 변화를 가리킨다.
에이전트 파이프라인에서 열린 추론은 LLM이 맡고 닫힌 선택은 작은 모델이 맡는
분업이 자리 잡을 수 있다(필자의 전망이다).
그러면 결정 단계가 로그와 보정의 대상이 된다.
각 결정의 확률을 남기고 임계값을 정하고 어긋남을 추적하는 일이 에이전트
관측성의 새 항목이 된다.
ksymph가 이렇게 빠르게 늘어난 모델들로 실제로 무엇을 만든 사람이 있느냐고 물은
것은,[^ksymph] 이 분업이 아직 개념 단계임을 보여 주는 질문이다.

그 뒤에 나온 답 가운데 reassess_blind는 사용자 가입을 훑어 도박 스팸이나 피싱
징후를 찾는 데 시험 중이며, 지금 LLM으로 처리하는 과정이 이런 분류 모델에 맞아
보인다고 했다.[^reassess_blind]
분업이 실제로 시도되는 사례이지만, 한 사람의 시험 보고라는 점에서 개념 단계를
벗어났다고 보기는 이르다.

---

[^woah]: <https://news.ycombinator.com/item?id=49924159>

[^zwaps]: <https://news.ycombinator.com/item?id=49924303>

[^kflansburg]: <https://news.ycombinator.com/item?id=49924339>

[^segmondy]: <https://news.ycombinator.com/item?id=49927360>

[^ralusek]: <https://news.ycombinator.com/item?id=49925250>

[^pdlug]: <https://news.ycombinator.com/item?id=49928781>

[^agrippanux]: <https://news.ycombinator.com/item?id=49929048>

[^alex7o]: <https://news.ycombinator.com/item?id=49925328>

[^nikcub]: <https://news.ycombinator.com/item?id=49926169>

[^CBLT]: <https://news.ycombinator.com/item?id=49925249>

[^vulture916]: <https://news.ycombinator.com/item?id=49926385>

[^ssiddharth]: <https://news.ycombinator.com/item?id=49924252>

[^jampekka]: <https://news.ycombinator.com/item?id=49926617>

[^buildbuildbuild]: <https://news.ycombinator.com/item?id=49924502>

[^dang]: <https://news.ycombinator.com/item?id=49928246>

[^ranyume]: <https://news.ycombinator.com/item?id=49925578>

[^TeMPOraL]: <https://news.ycombinator.com/item?id=49924635>

[^ramoz]: <https://news.ycombinator.com/item?id=49924294>

[^janalsncm]: <https://news.ycombinator.com/item?id=49925016>

[^fastball]: <https://news.ycombinator.com/item?id=49926079>

[^calebkaiser]: <https://news.ycombinator.com/item?id=49924648>

[^amluto]: <https://news.ycombinator.com/item?id=49925842>

[^mikeocool]: <https://news.ycombinator.com/item?id=49926212>

[^cakoose]: <https://news.ycombinator.com/item?id=49926220>

[^meander_water]: <https://news.ycombinator.com/item?id=49927461>

[^ksymph]: <https://news.ycombinator.com/item?id=49924597>

[^johnbatch]: <https://news.ycombinator.com/item?id=49929567>

[^teleforce]: <https://news.ycombinator.com/item?id=49929481>

[^reassess_blind]: <https://news.ycombinator.com/item?id=49929153>
