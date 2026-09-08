# 하네스란 무엇인가: 정의 논쟁

[← 하네스 엔지니어링](index.md)

“하네스 엔지니어링”이라는 용어 자체가 안정되지 않았다. 이 저장소에
모인 여러 글이 서로 다른 은유와 구성 요소 목록을 제시하고, 그 불일치
자체가 하나의 관찰거리다.

## 경쟁하는 은유들

[에이전트 하네스: 사용자가 소유할 수 있는 AI 실행
환경](../../agentic-coding/what-is-a-harness.md)은 등반 하네스 은유를
쓴다 — 모델은 벽(소유 불가), 하네스는 장비(소유 가능)라는 것이다.
[Harness Engineering: AI 에이전트를 실제로 작동하게 만드는 시스템
설계](../../agentic-coding/harness-engineering.md)는 마구(馬具)
은유를 쓴다 — 모델은 말, 하네스는 고삐와 재갈, 인간은 기수다. 두
은유는 같은 대상을 다르게 프레이밍한다. 등반 은유는 하네스 착용자
(인간)의 주체성과 안전을 강조하고, 마구 은유는 하네스가 통제하는
대상(모델)의 야생성과 위험을 강조한다. HN에서 저자 본인이 검토했다고
밝힌 다른 은유들 — 섀시/엔진/연료(자동차), 배낭(짐) — 도 저마다 다른
함의를 가진다. 배낭 은유를 고르면 “모델이 좋을수록 하네스는 얇아진다”는
결론이 자연스럽게 따라오고, 등반 은유를 고르면 “하네스 없이는 추락한다”는
결론이 따라온다. 은유의 선택이 이미 결론을 정하고 있다는 것이,
[모델이 좋아져도 하네스가 사라지지 않는
이유](why-harness-persists.md)에서 다룬 논쟁이 왜 은유 차원에서부터
갈리는지를 설명한다.

## “모델 + 하네스”라는 공식의 계보

여러 노트가 인용하는 “Agent = Model + Harness”라는 단순한 공식은
[하네스 엔지니어링 종합
보고서](../../agentic-coding/harness-engineering-comprehensive-report.md)가
추적하는 계보를 갖는다 — 2024년 Princeton SWE-agent 논문이 만든
ACI(agent-computer interface) 개념에서 시작해, Anthropic이 “HCI에
투자하듯 ACI에 투자하라”고 재구성하고, 이후 여러 업계 글이 “하네스
엔지니어링”이라는 이름으로 굳혔다는 것이다. 이 계보가 중요한 이유는
공식 자체가 반증 가능한 명제로 시작했다는 점이다 — SWE-agent 논문은
동일 모델에 ACI만 바꿔 SWE-bench 12.5%p SOTA를 달성했다. [Learn Harness
Engineering 강의](../../agentic-coding/learn-harness-engineering-lectures.md)는
이 공식을 다섯 서브시스템(지시·도구·환경·상태·피드백)으로 분해하고,
[Harness Engineering (NxCode)](../../agentic-coding/harness-engineering.md)는
세 기둥(컨텍스트·아키텍처 제약·엔트로피 관리)으로 분해한다. 두 분류가
겹치는 부분(컨텍스트 관리, 검증/피드백)은 업계의 합의 영역이고, 겹치지
않는 부분(엔트로피 관리 대 상태 서브시스템)은 학파별 강조점 차이로
읽을 수 있다.

## 용어 자체가 마케팅이라는 비판

[Harness Engineering (NxCode
가이드)](../../agentic-coding/harness-engineering.md)의 비평에서
GeekNews의 kimjoin2는 “점점 마케팅 용어만 엄청 생기는 느낌”이라고
지적한다 — 파일시스템·Git·Bash 같은 기본 도구를 “하네스의 핵심
구성 요소”로 재포장하는 것은 CI/CD, DevOps, 프롬프트 엔지니어링,
MLOps의 재발명에 가깝다는 것이다. [에이전트 하네스: 사용자가 소유할
수 있는 AI 실행 환경](../../agentic-coding/what-is-a-harness.md)의
HN 토론에서는 이 비판이 더 날카롭게 나타난다. `profsummergig`는
“소프트웨어 엔지니어들이 어떤 도구의 의미에 합의하지 못한다면 그
도구는 욕망의 대리물”이라고 정리했고, 143개 댓글에 걸쳐 하네스가
섀시·배낭·안장·휠체어·손으로 번갈아 비유되고도 정의 논쟁이 이어졌다는
사실이 그 진단을 뒷받침한다. `wangii`는 더 강하게, 하네스라는 용어
자체가 “LLM을 더 통제된 방식으로 쓰겠다”는 모호한 비전을 서술하려고
빌려 온 것이며, 정작 필요한 질문(제한된 컨텍스트를 가진 모델이 혼란한
코드베이스를 유능한 신입처럼 다루게 하는 일반적 틀이 존재하는가)은
용어 논쟁 뒤에 가려진다고 봤다.

## 그럼에도 실무에서는 네 구성 요소가 반복된다

용어를 둘러싼 논쟁과 별개로, 실제 하네스가 하는 일을 서술할 때는
비슷한 목록이 반복된다. 시스템 프롬프트(지시), 도구 정의, 에이전틱
루프, 그리고 (선택적으로) 모델 간 번역 계층이다. [에이전트 하네스:
사용자가 소유할 수 있는 AI 실행
환경](../../agentic-coding/what-is-a-harness.md)의 비평은 이 목록에서
빠진 것을 짚는다 — HN의 `_pdp_`는 “모델의 나쁜 행동을 실시간으로
보정하는 층”이 네 구성 요소 어디에도 속하지 않는다고 지적했다. 이
공백은 우연이 아니다. 시스템 프롬프트는 요청이고, 도구는 능력이고,
루프는 반복이고, 번역 계층은 호환이다 — 넷 다 능력을 확장하는
장치이지, 확신을 갖고 틀린 방향으로 가는 모델을 멈추는 장치가 아니다.
이 공백을 메우는 것이 [검증 계층의 분리와 그 한계](evaluator-separation.md)에서
다루는 생성자-평가자 분리이며, “하네스의 네 구성 요소”라는 정의 자체가
불완전하다는 것을 보여준다.

## 관련

[모델이 좋아져도 하네스가 사라지지 않는 이유](why-harness-persists.md) ·
[검증 계층의 분리와 그 한계](evaluator-separation.md)

## 출처

- [agentic-coding/what-is-a-harness.md](../../agentic-coding/what-is-a-harness.md)
- [agentic-coding/harness-engineering.md](../../agentic-coding/harness-engineering.md)
- [agentic-coding/harness-engineering-comprehensive-report.md](../../agentic-coding/harness-engineering-comprehensive-report.md)
- [agentic-coding/learn-harness-engineering-lectures.md](../../agentic-coding/learn-harness-engineering-lectures.md)
