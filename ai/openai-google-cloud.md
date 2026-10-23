# OpenAI 모델이 Google Cloud에서 판매된다: 클라우드 약정으로 사는 프런티어 모델

원문: [OpenAI models are coming to Google Cloud](https://openai.com/index/openai-models-google-cloud/)

HN 토론: <https://news.ycombinator.com/item?id=50180079> (322점, 144개 댓글)

GN 토론: <https://news.hada.io/topic?id=35775>

## 요약

OpenAI가 2026년 10월 21일에 올린 발표문이다.
OpenAI와 Google Cloud가 제휴해, OpenAI의 프런티어 모델과 Codex 기반 에이전트 워크플로를 Google Cloud의 Model Garden에 들여온다는 내용이다.
고객은 이 모델들을 Google Cloud 안에서 쓰고, Google Cloud의 데이터 거버넌스와 고성능 인프라를 그대로 이용한다.
발표문은 규제 산업의 조직이 민감한 데이터에 누가 접근하고 어떻게 쓰는지 통제해야 한다는 점을 강조하며, Google Cloud의 접근 제어와 중앙 데이터 거버넌스를 장점으로 내세운다.

구매 방식이 핵심이다.
고객은 Model Garden에서 OpenAI 모델을 구매하고, 거래는 Google Cloud Marketplace를 통해 이뤄진다.
Google Cloud 지출 약정이 있는 기업은 그 약정에서 이 구매 금액을 차감할 수 있다.
모델은 곧 Google Antigravity와 Gemini Agent에서도 쓸 수 있게 된다고 한다.
정식 출시(General Availability)는 앞으로 몇 주 안에 예정돼 있고, 지금은 접근 권한을 신청하는 단계다.

발표문에는 두 사람의 인용문이 있다.
OpenAI 사장 Greg Brockman은 고객이 이미 일하는 곳에서 가장 유능한 모델과 Codex를 쓰게 하는 중요한 걸음이라고 말한다.
Google Cloud CEO Thomas Kurian은 다양한 모델 중에서 작업마다 맞는 모델을 고르게 해 품질을 높이고 비용을 낮추는 것이 목표라고 말한다.
마지막 줄은 Microsoft가 여전히 OpenAI의 주된 클라우드 파트너라는 문장이다.
같은 페이지의 관련 글 목록에는 Oracle 클라우드 약정으로 OpenAI 모델을 쓰게 한 6월 발표도 있다.

## 분석

### 핵심 주장: 모델을 만드는 쪽이 판매망을 빌린다

발표문의 주장은 모델 접근이 아니라 구매 경로에 있다.
OpenAI 모델은 이미 API로 살 수 있다.
달라지는 것은 Google Cloud 계약 안에서, 기존 청구서와 기존 약정으로 살 수 있다는 점이다.
HN에서 echelon은 이를 매출 구조로 풀었다.
OpenAI는 Microsoft 투자 계약 때문에 Azure에서 컴퓨팅을 사고, 기업 고객에게는 GCP를 통해 팔아 더 많은 돈을 번다는 것이다.
기업은 데이터 보존 제로(zero data retention) 보증을 원하고 이미 AWS나 GCP를 쓰고 있다는 이유를 들었다.[^echelon]

open592는 이를 경쟁 압박으로 읽었다.
Anthropic이 이미 GCP, Azure, AWS 세 곳에서 추론을 직접 제공하므로, OpenAI도 같은 방식으로 경쟁한다는 것이다.[^open592]
iamdelirium도 GCP가 이미 Anthropic 모델을 호스팅한다는 점을 들어 이번 일이 새로운 유형의 거래가 아니라고 지적했다.[^iamdelirium]
이 해석에 따르면 발표는 전략 전환이 아니라 판매 채널을 고객이 있는 곳에 맞추는 일이다.

### 약정 차감이 뜻하는 것

가장 구체적인 조건은 GCP 약정 차감이다.
기업들은 클라우드 사업자와 일정 금액을 쓰겠다고 약정하고 할인을 받는다.
이 약정을 소진하려고 쓸 곳을 찾는 기업에게, 외부 모델 구매를 약정에 넣을 수 있다는 것은 구매 장벽을 크게 낮춘다.
OpenAI 입장에서는 별도 예산을 설득하지 않아도 되는 판매 경로를 얻는다.

HN에서 londons_explore는 이를 Google에게 위험한 조치로 읽었다.
이미 보고한 매출을 남에게 내줄 수 있다는 것이다.[^londons_explore]
eitally는 이를 바로잡았다.
고객이 약정으로 이미 예약된 매출을 OpenAI 모델 소비를 통해 청구 매출로 바꿀 수 있고, OpenAI도 돈을 받고 Google은 실제 플랫폼 소비에 청구하는 구조라는 것이다.
전에는 GCP 고객이 ChatGPT나 Codex를 쓰려면 GCP 프로젝트에서 API를 호출하는 것밖에 없었다고 한다.[^eitally]
jaynate도 Google은 여전히 매출을 인식하고, 영향을 받는 것은 매출원가와 총이익이라고 설명했다.[^jaynate]
두 설명이 같은 방향으로 모인다.
이 거래의 비용은 매출 상실이 아니라 마진이다.

### 같은 발표가 말하지 않는 것

발표문은 가격, 지원하는 모델 목록, 지역, 데이터가 어디에 저장되고 누가 접근하는지를 밝히지 않는다.
데이터 거버넌스를 장점으로 내세우면서도 OpenAI가 모델 호출 기록을 볼 수 있는지는 설명하지 않는다.
이것은 기업이 가장 먼저 물을 질문이다.
정식 출시가 몇 주 뒤라고 했으므로, 이 조건들은 그때 공개될 가능성이 있다.

## 비평

### Microsoft 문구는 읽을 거리가 작다

HN에서 nsagent는 맨 아래의 Microsoft 문구를 면책 조항처럼 읽었다.[^nsagent]
hobofan은 계약상 어쩔 수 없이 넣은 문장으로 봤고,[^hobofan] cmiles8은 주된 클라우드 제공자라는 말이 무슨 뜻인지 모르겠다고 비꼬았다.[^cmiles8]
이 해석은 근거가 없다.
발표문이 계약 때문에 그 문장을 넣었다는 증거는 어디에도 없다.
확인되는 것은 OpenAI가 Microsoft를 계속 주된 파트너로 부른다는 사실뿐이다.
이 문장이 무엇을 보장하는지, 곧 컴퓨팅 구매 기준인지 독점 판매 권리 기준인지도 발표문에 없다.

### 증류 방지에 대한 질문은 답이 추측뿐이다

HN에서 bananzamba는 Google이 OpenAI 모델을 증류하지 않으리라고 어떻게 믿느냐고 물었다.
답은 계약과 법률가였다.
binlog는 계약과 변호사가 어떤 기술적 수단보다 강하다고 했고,[^binlog] lrvick은 OpenAI가 자체 고객의 세션 로그를 읽듯 읽을 수 있을 것이라고 추측했다.[^lrvick]
aviinuo는 Nvidia GPU가 암호화된 가중치를 올려 칩 안에서 복호화할 수 있어서, 가중치를 읽으려면 Nvidia 관리 펌웨어를 공격해야 한다고 했다.[^aviinuo]

이 답들은 모두 발표문 바깥의 추측이다.
발표문은 모델이 Google Cloud에서 어떻게 호스팅되는지, 곧 OpenAI가 운영하는지 Google이 운영하는지도 밝히지 않는다.
따라서 증류 위험이 실제로 어느 쪽에 있는지는 이 글만으로 판단할 수 없다.

### 약정 차감의 한도는 발표문에 없다

HN에서 mmnfrdmcx는 Google에 직접 물어봤다고 하며, OpenAI 지출은 파트너 지출로만 계산되고 약정의 25%까지만 쓸 수 있다고 전했다.[^mmnfrdmcx]
이 말이 맞다면 발표문의 약정 차감이라는 설명은 상한이 있는 조건이다.
이 숫자는 한 사용자의 전언이어서 확인되지 않았다.
다만 발표문이 한도를 언급하지 않는다는 사실은 확인된다.
고객이 이 조건을 기준으로 구매를 정하려면, 정식 출시 때 공개되는 약관을 읽어야 한다.

## 인사이트

### 모델 경쟁이 판매 경로 경쟁으로 옮겨 간다

HN에서 skohan은 지난 한 해의 증거가 AI에 비밀 무기가 없다는 쪽이라고 했다.
모델 능력이 수렴하고 한 달 남짓 앞서는 것으로는 마진이 나지 않는다는 것이다.[^skohan]
이 판단이 맞다면 차이를 만드는 것은 모델 순위가 아니라 구매 경로다.
고객이 이미 약정한 클라우드에서, 이미 승인된 데이터 거버넌스 안에서 쓸 수 있느냐가 선택을 좌우한다.

이 구조는 클라우드가 엔터프라이즈 소프트웨어를 마켓플레이스로 파는 방식과 같다.
소프트웨어 회사는 직접 판매 대신 클라우드 마켓플레이스에 올려 고객의 약정으로 팔았다.
이번 발표는 같은 구조가 모델에도 적용된다는 신호다.
이 구조에서 수익을 가져가는 것은 모델을 만든 쪽만이 아니고, 고객의 약정 예산을 쥔 쪽이다.

### Google의 선택은 모델 사업과 클라우드 사업의 우선순위를 드러낸다

HN에서 anthonypasq는 Google Cloud가 경쟁 모델을 호스팅하는 것이 Gemini에 대한 Alphabet 내부의 신뢰가 약하다는 신호라고 읽었다.[^anthonypasq]
paxy는 파트너십과 외부 모델 호스팅은 Google에게 비용이 거의 들지 않고 수익이 결국 Gemini에 되돌아간다고 반박했다.[^paxy]
Google이 모델 회사와 클라우드 회사를 동시에 하고 있다는 점이 이 대화의 바탕이다.

tancop은 Amazon에 Bedrock이 있으므로 Google도 GPT와 Claude, Gemini, 오픈 모델을 모두 제공해야 경쟁할 수 있다고 설명했다.[^tancop]
이 설명이 맞다면 Google의 선택은 포기가 아니라 방어다.
클라우드 고객이 모델을 고르려고 다른 클라우드로 옮겨 가는 일을 막으려면, 그 모델을 팔아야 한다.
다만 이는 해석이고, Google이 내부에서 어떻게 우선순위를 정하는지는 발표문에 없다.

### 기업이 이 발표를 읽는 방법

기업의 구매 담당자라면 이 발표에서 확인할 것은 세 가지다.
첫째, 약정 차감의 상한과 조건이다.
둘째, 데이터 보존 제로 같은 보증이 Google Cloud 경로에서도 같은 수준으로 적용되는지다.
셋째, 모델 버전과 출시 시점이 OpenAI 직접 API와 같은지다.
HN에서 felindev는 GCP에서 AI 모델을 쓰는 경험이 불안정했다고 적었다.
Gemini는 잘 되지만 동적 사용량 제한이 심하고, Anthropic 모델은 끝내 완전히 활성화하지 못했다는 것이다.[^felindev]
이는 한 사용자의 경험이지만, 정식 출시 뒤 실제 사용량 한도와 접근 조건을 직접 확인해야 하는 이유다.

이 발표의 신뢰도를 가를 관찰은 정식 출시 문서다.
가격과 약정 차감 한도, 호스팅 주체, 데이터 처리 조건이 직접 API와 같은 수준으로 공개된다면 이번 제휴는 판매 채널의 확장이다.
조건이 공개되지 않거나 직접 API보다 느리게 공급된다면, 이 발표는 보도자료에 가까운 제휴 선언이다.

---

[^echelon]: <https://news.ycombinator.com/item?id=50184950>

[^open592]: <https://news.ycombinator.com/item?id=50184832>

[^iamdelirium]: <https://news.ycombinator.com/item?id=50184793>

[^londons_explore]: <https://news.ycombinator.com/item?id=50185535>

[^eitally]: <https://news.ycombinator.com/item?id=50189154>

[^jaynate]: <https://news.ycombinator.com/item?id=50188958>

[^nsagent]: <https://news.ycombinator.com/item?id=50183965>

[^hobofan]: <https://news.ycombinator.com/item?id=50184715>

[^cmiles8]: <https://news.ycombinator.com/item?id=50190402>

[^binlog]: <https://news.ycombinator.com/item?id=50184724>

[^lrvick]: <https://news.ycombinator.com/item?id=50184471>

[^aviinuo]: <https://news.ycombinator.com/item?id=50184492>

[^mmnfrdmcx]: <https://news.ycombinator.com/item?id=50194161>

[^skohan]: <https://news.ycombinator.com/item?id=50187412>

[^anthonypasq]: <https://news.ycombinator.com/item?id=50186241>

[^paxy]: <https://news.ycombinator.com/item?id=50187168>

[^tancop]: <https://news.ycombinator.com/item?id=50184990>

[^felindev]: <https://news.ycombinator.com/item?id=50192094>
