# OpenAI

## Responses API

[API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/responses)

[Responses vs. Chat Completions - OpenAI API](https://platform.openai.com/docs/guides/responses-vs-chat-completions)

## Agents SDK

[Agents - OpenAI API](https://platform.openai.com/docs/guides/agents)

<https://github.com/openai/openai-agents-python>

<https://openai.github.io/openai-agents-python/>

[Quickstart: Create an agent (preview) | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/create-test-basic-agent)
\
→ 한국어 번역:
[\[Microsoft 365 Agents SDK\] 04 빠른 시작: Agents SDK를 사용하여 에이전트 만들기](https://blog.naver.com/ilovehandson/223859405377)

## OpenAI 거버넌스 이슈 (2026-02)

### 참고 기사

[OpenAI has deleted the word "safely" from its mission](https://theconversation.com/openai-has-deleted-the-word-safely-from-its-mission-and-its-new-structure-is-a-test-for-whether-ai-serves-society-or-shareholders-274467)

### 핵심 분석

이 글은 OpenAI가 미션 문구에서 "safely(안전하게)"를 삭제한 변화가 단순한
표현 수정이 아니라, 비영리 공익 우선 모델에서 투자자 수익 압력이 강한
구조로 이동했음을 보여주는 신호라고 주장한다.

OpenAI의 2022~2023년 IRS 문구는 "인류에 안전하게(safely) 이익이 되도록
AGI를 개발"이었는데, 2024년 문구는 "AGI가 인류 모두에게 이익이 되도록"으로
바뀌었다. 동시에 OpenAI는 구조를 재편해 비영리 재단(OpenAI Foundation) +
영리 공익법인(OpenAI Group) 체제로 전환했다. 재편 결과, 비영리 측 지분은
약 26%로 축소되고 마이크로소프트(약 27%) 및 기타 투자자·직원 지분 비중이
커졌다. 회사는 대규모 투자(SoftBank 등)를 유치하며 기업가치가 급등했고,
향후 IPO 가능성도 열리면서 주주수익 압력이 더 커질 수 있다.

저자는 현재의 안전 관련 장치(안전·보안 위원회, 이사회 권한 등)는 있으나,
미션 자체에 안전이 약화되어 실질적 책임추궁(accountability)이 약해질 수
있다고 본다. 결론적으로 이 사례를 "AI가 사회를 우선할지, 주주를 우선할지"를
가르는 거버넌스 시험대로 제시한다.

### 인사이트

문구 변경은 거버넌스 신호다. 미션 문구는 PR 카피가 아니라,
이사회·경영진·규제기관이 의사결정을 정당화할 때 쓰는 "기준 문장"이다.
"안전"이 빠지면 분쟁 시 우선순위를 수익·확장 쪽으로 해석할 여지가 커진다.

PBC(공익법인)만으로는 충분하지 않다. Public Benefit Corporation은 공익
고려 의무가 있지만, 실제로 "무엇을 얼마나 우선할지"는 이사회 재량이 크다.
즉, 형식(법인 형태)보다 실질 KPI·감사·공시 체계가 더 중요하다.

AI 안전의 본질은 기술보다 권력 배분이다. 모델 레드팀, 평가 프레임워크도
중요하지만 최종적으로 출시 중단 버튼을 누를 권한이 누구에게 있는지가
핵심이다. 지분·이사회 구조가 바뀌면 안전 의사결정도 바뀐다.

투자 유치 성공과 안전 신뢰는 긴장관계에 있다. 자본이 많이 들어오면
연구·인프라는 빨라지지만, 동시에 성장속도·시장점유 압력이 커져 안전 마진을
잠식할 수 있다. 따라서 성장과 안전을 동시에 관리하는 운영 설계가 필수다.

규제기의 역할은 사후 처벌보다 사전 조건 설계에 가깝다. 기사처럼 AG 합의에
안전 조항이 들어가도, 미션·지분·이사회 독립성까지 강하게 묶지 않으면
실제 집행력은 제한될 수 있다. 앞으로는 안전 관련 독립이사 비율,
고위험 모델 출시 전 외부감사 의무, 사건·근접사고(near miss) 정기 공시 같은
구체적 조건이 더 중요해질 가능성이 크다.

### 정리

따라서 OpenAI 같은 조직을 평가할 때는 모델 성능이나 제품 확장 속도만 보면
안 되고, 지분 구조, 이사회 구성의 독립성, 안전 관련 거부권 및 출시 중단권,
외부 검증 체계까지 함께 봐야 한다. 이 관점은 특정 기업 비판을 넘어,
앞으로 AI 산업 전반에서 "사회적 신뢰"와 "주주가치"를 어떻게 조정할지에 관한
기본 프레임으로 활용할 수 있다.
