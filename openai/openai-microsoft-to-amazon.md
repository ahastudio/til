# OpenAI의 클라우드 지형 재편: MS 독점 해체에서 Amazon 동맹까지

자료:

- [한국경제 — MS, 오픈AI 클라우드 독점 공급권 상실 (2025-01-22)](https://www.hankyung.com/article/202501223598i)
- [OpenAI — AWS and OpenAI announce multi-year strategic partnership](https://openai.com/ko-KR/index/aws-and-openai-partnership/)
- [OpenAI — OpenAI and Amazon announce strategic partnership](https://openai.com/ko-KR/index/amazon-partnership/)

## 요약

2025년 1월부터 2026년 초에 걸쳐, OpenAI의 컴퓨팅 공급 구조가 MS(Microsoft)
단일 의존에서 멀티 클라우드로, 그리고 Amazon과의 전면적 전략 동맹으로
이동했다. 세 건의 보도를 시간 순으로 읽으면 "독점 해체 → 공급원 추가 →
자본·제품 동맹"의 3단계 흐름이 드러난다.

## 1단계 — MS 독점권의 해체 (2025-01-22)

한국경제 보도에 따르면, MS는 2019년 이래 OpenAI의 클라우드 인프라 독점
공급권을 쥐고 있었으나, 2025년 1월 이 지위가 "우선협상권(right of first
refusal)"으로 축소되었다. MS가 필요한 용량을 공급하지 못하면 OpenAI가
Oracle 등 경쟁사를 선택할 수 있게 된 것이다.

배경에는 5,000억 달러 규모로 거론되는 "스타게이트(Stargate)" AI 데이터센터
프로젝트가 있다. MS 단독으로는 OpenAI가 요구하는 컴퓨팅 규모를 감당할 수
없다는 현실이 계약 구조 자체를 밀어냈다.

글로벌 클라우드 시장 점유율 — Amazon 32%, MS 23%, Google 12% — 을 감안하면,
독점 해체는 최대 사업자인 AWS에게 문을 여는 사건이기도 했다.

## 2단계 — AWS의 합류 (2025-11-03)

MS 독점이 풀린 지 약 10개월 뒤, AWS와 OpenAI는 7년간 380억 달러 규모의
다년 전략 파트너십을 발표했다. 핵심 조항:

- 수십만 개의 NVIDIA GB200/GB300 GPU를 Amazon EC2 UltraServer 클러스터로
  묶어 저지연으로 연결
- 수천만 개의 CPU로 확장해 에이전트 워크로드를 대응
- ChatGPT 추론 서빙부터 차세대 모델 학습까지 전 범위 지원
- 2026년 말까지 목표 용량 배치 완료, 2027년 이후 추가 확장

발표 당일 Amazon 주가는 사상 최고치를 기록하며 시가총액이 약 1,400억 달러
늘었다. 동시에 이 계약은 OpenAI가 9월 Oracle과 맺은 3,000억 달러 규모
계약과 함께 "멀티 클라우드 전략"의 실체를 확인시켰다.

## 3단계 — Amazon과의 전략 동맹 (2026)

OpenAI와 Amazon은 한 걸음 더 나아간 전략적 파트너십을 발표했다. 1단계의
공급 계약을 자본·제품 영역까지 확장한 형태다.

- **투자**: Amazon이 OpenAI에 500억 달러 투자. 초기 150억 달러, 이후 조건
  충족 시 350억 달러 추가
- **컴퓨팅 확장**: 기존 380억 달러 계약을 8년간 1,000억 달러 추가 확대. 약
  2GW(기가와트)의 Trainium 용량 약정 (Trainium3 및 2027년 출시 예정
  Trainium4)
- **제품 공동 개발**: OpenAI 모델 기반 Stateful Runtime Environment를
  Amazon Bedrock에서 제공. 장기 작업의 맥락·기억을 유지하는 에이전트
  런타임
- **유통**: AWS가 OpenAI Frontier의 독점 3자 클라우드 유통 채널이 됨

## 분석

### 수직 통합에서 수평 연합으로

2019~2024년의 OpenAI–MS 관계는 "독점 공급자 + 지분 투자자" 모델이었다.
이는 AI 스택의 수직 통합에 가까웠다. 2026년의 OpenAI–Amazon 관계는
형태는 유사해 보이지만(투자+컴퓨팅+유통), 성격이 다르다. OpenAI가
공급원을 복수화한 상태에서 맺은 동맹이기 때문에, 어느 한쪽도 상대를
"잠글" 수 없다. Oracle·MS와의 기존 계약이 Amazon에 대한 협상력으로
작동한다.

### NVIDIA 의존과 Trainium 약정의 공존

AWS 1차 계약은 NVIDIA GPU 기반이었다. 2026년 확장분은 AWS 자체 칩인
Trainium을 2GW 규모로 약정했다. OpenAI 입장에서는 NVIDIA 단일 의존을
줄일 수 있는 헤지이고, AWS 입장에서는 Trainium의 최대 레퍼런스 고객을
확보하는 거래다. 양쪽 모두 NVIDIA에 대한 협상력을 확보한다.

### MS의 위치

1월의 MS는 "배타적 권한을 잃은 사업자"로 보이지만, 이후 흐름을 보면 오히려
OpenAI의 급증하는 수요를 단독으로 감당하지 않아도 되는 출구를 얻은
셈이다. 동시에 4월 보도에서 확인되듯, OpenAI는 내부 메모에서 "MS가 고객
접근을 제한해왔다"는 불만을 드러내며 Amazon 동맹을 대안적 채널로
제시한다. 독점 해체는 기술적 필요를 넘어 관계 역학의 문제이기도 했다.

### 스타게이트의 현실화

세 발표는 결국 5,000억 달러급 "스타게이트" 구상이 어떻게 실제 계약으로
쪼개지는지를 보여준다. Oracle 3,000억 + AWS 380억(→1,000억 확장) +
기존 MS 계약 + Amazon 투자 500억. 한 회사의 CapEx로는 불가능한 규모가
여러 하이퍼스케일러에 분산 편성되는 중이다. OpenAI는 단일 고객에서
클라우드 산업 전체의 수요를 재편하는 존재로 이동했다.

## 한 줄 정리

MS 독점이 깨지자 AWS가 들어오고, AWS가 들어오자 Amazon이 지분·제품까지
엮었다. OpenAI의 협상력은 공급원을 늘릴수록 커지는 구조이며, 이 흐름이
곧 2026년 AI 인프라 지형의 기본 지도다.
