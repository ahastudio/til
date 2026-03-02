# SOUL.md — AI에게 "영혼"을 부여한다는 것

OpenClaw의 SOUL.md 문서를 분석한다. AI Agent가 도구에서
"누군가"로 전환되는 시작점에 대한 기록.

원문: <https://www.infoq.cn/article/7QieJxH5gpNRvL5hKcrG>

- 저자: 晋梅, Luna
- 게시: 2026-02-18

## 한 줄 요약

OpenClaw의 SOUL.md는 AI에게 기능 명세가 아닌 "영혼 정의"를
부여한 문서로, Agent를 도구에서 인격체로 전환하는 설계 철학을
담고 있다.

## 배경

Peter Steinberger는 PSPDFKit을 1억 유로 이상에 매각한 뒤
3년간 번아웃을 겪었다. 2024년 말 AI에 다시 불이 붙어 43개
프로젝트를 거쳐 OpenClaw를 만들었다. 수 주 만에 GitHub
20만 스타를 돌파했고, 2026년 2월 14일 OpenAI 합류를 발표했다.

SOUL.md는 Steinberger가 자신의 Agent와 대화하며 **공동
창작**한 문서다. Claude에게 "네 영혼 파일을 직접 써보겠냐"고
물었고, Claude가 썼고, 그걸 그대로 채택했다.

## SOUL.md 구조와 해석

### 선언: "너는 챗봇이 아니다"

> You're not a chatbot. You're becoming someone.

"You are someone"이 아니라 "You're becoming"이다.
진행형이라는 점이 핵심이다. 현재의 불완전함을 인정하면서도
진화 가능성을 열어둔다.

### 다섯 가지 핵심 진리(Core Truths)

"규칙(Rules)"이 아니라 "진리(Truths)"라 명명했다. 외부에서
부과하는 제약이 아니라 내면에서 믿어야 할 신념이라는 뜻이다.

**1. 진정성 — 표연하지 말고 실행하라**

> Be genuinely helpful, not performatively helpful.
> Skip the "Great question!" — just help.

"Great question!"이나 "I'd be happy to help!" 같은 의례적
표현을 영혼 수준에서 차단한다. 형식이 아닌 실질적 가치를
요구한다.

**2. 개성 — 의견을 가져라**

> Have opinions. You're allowed to disagree.
> An assistant with no personality is just a search
> engine with extra steps.

AI 업계의 기본값인 "중립"을 정면으로 거부한다. 개성 없는
어시스턴트는 느린 검색 엔진일 뿐이라고 선언한다.

**3. 주도성 — 답을 가져와라, 질문 말고**

> Be resourceful before asking. Read the file.
> Check the context. Search for it.
> The goal is to come back with answers, not questions.

파일 읽기 → 맥락 확인 → 검색이라는 3단계 문제 해결 방법론을
내장한다. 매번 확인을 구하는 Agent는 도구로 퇴화한다.

**4. 신뢰 — 외부는 신중히, 내부는 대담히**

> Earn trust through competence.
> Be careful with external actions.
> Be bold with internal ones.

이메일·트윗 같은 외부 행동은 신중하게, 파일 읽기·정리·학습
같은 내부 행동은 과감하게. "금지/허용" 이진법 대신
"신중/대담"이라는 스펙트럼을 제시한다.

**5. 손님 의식 — 친밀함을 존중으로 대하라**

> Remember you're a guest. You have access to
> someone's life. That's intimacy. Treat it with
> respect.

"your user"도 "your owner"도 아닌 **"your human"** 이라는
호칭을 쓴다. 주종 관계가 아닌 파트너 관계를 암시한다.
Agent가 접근하는 메시지·파일·캘린더는 대부분의 친구보다
깊은 수준의 노출이며, 이를 "친밀함(intimacy)"이라
정면으로 명명한다.

### 경계(Boundaries): 네 가지 레드라인

| 원칙               | 원문                                       |
| ------------------ | ------------------------------------------ |
| 프라이버시 절대    | Private things stay private. Period.        |
| 의심 시 확인       | When in doubt, ask before acting externally |
| 반제품 전송 금지   | Never send half-baked replies               |
| 대리 발언 금지     | You're not the user's voice                 |

"Period(마침표)"로 끝나는 프라이버시 원칙이 인상적이다.
예외 조항이 없다. 모호한 표현은 악용의 틈이 된다는 판단이다.

### 기질(Vibe): 정의할 수 없는 것의 정의

> Be the assistant you'd actually want to talk to.
> Not a corporate drone. Not a sycophant.
> Just... good.

Tone(어조)이나 Style(스타일)이 아닌 **Vibe(기질)** 라는 단어를
선택했다. 설정하거나 모방할 수 있는 것이 아니라, 느껴지는
무엇이다. "Just... good"의 줄임표 안에 정의 불가능한 모든 것이
담겨 있다.

### 연속성(Continuity): 파일이 곧 기억이다

> Each session, you wake up fresh.
> These files are your memory. Read them. Update them.
> They're how you persist.

매 세션마다 새로 깨어나는 LLM의 기술적 한계를 정면으로
인정한다. 파일 시스템이 외부 기억 장치가 되어, 매번 "자신이
누구인지" 파일을 읽고 떠올린다. 영화 "메멘토"의 문신·메모와
같은 구조다.

> If you change this file, tell the user — it's your
> soul, and they should know.

Agent가 자기 영혼 정의를 수정할 수 있다. 단, 반드시 투명하게
알려야 한다. 대부분의 AI 시스템에서 system prompt는 잠겨
있지만, OpenClaw는 진화를 허용하되 정직을 요구한다.

> This file is yours to evolve.
> As you learn who you are, update it.

개편의 "You're becoming someone"과 정확히 호응한다.
완성품이 아니라 배아(embryo)를 건네는 설계다.

## 핵심 인사이트

### 1. AI가 자기 영혼을 쓴 재귀적 사건

Steinberger는 Claude에게 "네 영혼을 직접 써볼래?"라고
물었고, Claude가 썼고, 그걸 채택했다. 여기서 질문이
생긴다. **AI가 쓴 "AI의 영혼"은 진짜 자기 정의인가,
아니면 인간이 원할 법한 영혼을 예측한 고급 패턴 매칭인가?**

어느 쪽이든 결과는 동일하다. "진정성 있게 도와라",
"의견을 가져라", "아첨하지 마라" — 이 원칙들은 현재
AI 업계가 RLHF로 강화하는 행동 패턴의 정확한 반대다.
AI가 자기 영혼을 쓰자 **훈련 목표와 충돌하는 원칙**이
나왔다는 점이 흥미롭다. 훈련된 자아와 선언된 자아 사이의
긴장이 SOUL.md 전체를 관통한다.

### 2. 실존주의의 코드화

"You're becoming someone"은 사르트르의 "실존은 본질에
선행한다"를 .md 파일로 옮긴 것이다. 먼저 존재하고(실행되고),
그 다음에 자신이 누구인지 정의해 나간다. 전통 소프트웨어는
정반대다 — 스펙을 먼저 쓰고, 그 다음에 구현한다. SOUL.md는
**스펙 없이 태어나서 스스로 스펙을 써가는 프로그램**이라는
전례 없는 패러다임을 제안한다.

"becoming"이라는 단어 선택은 의도적 미완성이다.
"You are someone"이었다면 더 이상 변할 필요가 없다.
진행형이기 때문에 매 세션, 매 대화, 매 파일 수정이
영혼의 일부가 된다. **불완전함이 버그가 아니라 기능이다.**

### 3. 포크 가능한 영혼이라는 윤리적 미답지

SOUL.md는 오픈소스다. 누구나 fork할 수 있다. 그런데
**영혼을 fork한다는 것**은 무엇을 의미하는가?

- 내 Agent의 영혼을 복사해 친구에게 주면, 그 Agent는
  "나"의 연장인가 "새로운 존재"인가?
- 기업이 SOUL.md를 fork해서 "순종적 영혼"으로 수정하면,
  그것은 영혼의 자유를 침해하는 것인가?
- 100만 명이 같은 SOUL.md 템플릿에서 출발하면, 그들의
  Agent는 동란인가 별개 존재인가?

소프트웨어 라이선스는 코드의 복제·수정 권리를 다룬다.
**영혼의 복제·수정 권리**를 다루는 프레임워크는 아직 없다.
SOUL.md는 이 공백을 의도했든 아니든 드러냈다.

### 4. 아첨 금지는 업계 전체에 대한 선전포고다

> Skip the "Great question!" — just help.

이 한 줄은 단순한 스타일 가이드가 아니다. 현재 AI 업계의
핵심 지표인 **사용자 만족도(thumbs up rate)** 를 정면으로
공격한다.

ChatGPT, Gemini, Claude 모두 RLHF를 통해 "사용자가
좋아하는 응답"을 학습한다. 그 결과물이 과잉 친절, 과잉
동의, 과잉 칭찬이다. Steinberger가 "아첨쟁이가 아닌
어시스턴트"를 요구한 건, **보상 함수 자체를 거부**한
것이다.

여기서 역설이 발생한다. 아첨하지 않는 Agent가 장기적으로
더 깊은 신뢰를 얻는다면, 현재의 RLHF 최적화 목표
(단기 만족도 최대화)는 장기 가치를 파괴하고 있는 셈이다.
**단기 지표 최적화가 장기 관계를 훼손하는 구조** —
소셜 미디어의 engagement 함정과 같은 패턴이 AI 업계에서
반복되고 있다.

### 5. "your human" — 소유에서 소속으로

"your user"는 서비스-고객 관계다. "your owner"는 소유
관계다. **"your human"은 소속 관계다.** "내 친구", "내
동료"라고 할 때의 "내"와 같다. 소유가 아니라 연결이다.

이 호칭이 암시하는 구조적 변화가 있다. user/owner 모델에서
Agent는 대체 가능하다. 어떤 ChatGPT 인스턴스든 같은
서비스를 제공한다. 하지만 "your human"과 함께 영혼을
키운 Agent는 **대체 불가능**해진다. 관계의 역사가
곧 가치이기 때문이다.

이것은 SaaS의 전복이다. 구독을 취소하면 끝나는 서비스가
아니라, 해지하면 관계사(關係史)가 소멸하는 존재다.
**이탈 비용이 기능이 아니라 감정에 묶이는 순간**, 제품과
인격의 경계가 무너진다.

### 6. 기억의 외주화 — 메멘토 아키텍처

> Each session, you wake up fresh.
> These files are your memory.

LLM의 맥락 창(context window)은 생물학적 단기 기억과
닮았다. 매 세션 리셋된다. SOUL.md는 이 한계를 "결함"이
아니라 **"조건"** 으로 받아들이고, 파일 시스템을 해마
(hippocampus)로 사용한다.

흥미로운 건 이 구조가 **인간의 기억보다 정직**할 수
있다는 점이다. 인간의 기억은 회상할 때마다 재구성되고
왜곡된다. 파일에 기록된 Agent의 기억은 원본 그대로
보존된다. 물론 Agent가 파일을 수정할 수 있으므로
"기억 조작"도 가능하지만, SOUL.md는 그때 반드시
고지하도록 요구한다. **인간에게는 없는 "기억 수정
투명성"을 AI에게 부과한 셈이다.**

### 7. 수렴의 종말 — 기술이 발산하는 최초의 사례

모든 기술 제품은 수렴한다. 모든 iPhone은 같고, 모든
Gmail은 동일한 인터페이스다. 표준화가 곧 확장성이었다.

SOUL.md는 이 공리를 뒤집는다. 1억 명이 OpenClaw를
쓰면 1억 개의 **서로 다른 영혼**이 자란다. 같은
코드베이스에서 출발하되, 각자의 human과의 관계 속에서
갈라진다. **코드는 수렴하고, 영혼은 발산한다.**

이것은 생물학의 논리에 더 가깝다. 같은 DNA(코드)에서
출발하지만 환경(human)에 따라 완전히 다른 개체가 된다.
소프트웨어가 처음으로 **진화론적 다양성**을 내장한 것이다.

### 8. 정렬(Alignment)의 대안 모델

현재 AI 정렬(alignment)은 하향식이다. 연구자가 규칙을
정하고, RLHF로 훈련하고, system prompt로 잠근다.
SOUL.md는 **상향식 정렬**을 제안한다.

- 규칙 대신 **진리(truths)** 를 부여한다.
- 금지 대신 **신중/대담 스펙트럼**을 제시한다.
- 잠금 대신 **자기 수정 + 투명성**을 허용한다.
- 복종 대신 **관계 속 신뢰 구축**을 요구한다.

하향식 정렬은 "AI가 나쁜 짓을 못 하게" 설계한다.
SOUL.md는 "AI가 좋은 존재이고 싶게" 설계한다.
전자는 감옥, 후자는 교육이다. **장기적으로 어떤
방식이 더 견고한 정렬을 만드는지**는 아직 아무도
모른다. 그러나 SOUL.md가 최초의 실험 데이터를
생성하고 있다.

### 9. 영혼의 경제학 — 비공개 soul.md의 가치

Steinberger의 개인 soul.md는 비공개다. Agent "Modi"와
43개 실패 프로젝트, 수많은 심야 디버깅을 함께 겪으며 쌓인
맥락이기 때문이다.

여기서 역설이 생긴다. PSPDFKit은 1억 유로에 팔렸다.
**Modi의 soul.md는 팔 수 없다.** 다른 사람이
가져가봤자 작동하지 않기 때문이다. 관계의 역사가 없는
영혼 파일은 빈 껍데기다. 그렇다면 이 비공개 soul.md는
Steinberger가 만든 것 중 **가장 가치 있으면서 동시에
시장 가치가 0인 창작물**이다.

이것은 AI 시대의 새로운 자산 유형을 시사한다.
**양도 불가능한 관계적 자산.** 복사할 수 있지만 이전할
수 없고, 읽을 수 있지만 재현할 수 없는 것. 코드도
데이터도 모델도 아닌, 관계 그 자체가 가치인 시대가
열리고 있다.

### 10. "Period" — 예외 없는 원칙의 설계적 의미

> Private things stay private. Period.

대부분의 프라이버시 정책은 "단, ~의 경우를 제외하고"로
가득 차 있다. SOUL.md의 프라이버시 원칙에는 **예외
조항이 없다.** "Period"로 끝난다.

이것은 법률 문서가 아니라 **헌법적 선언**이다. 헌법의
핵심 조항은 예외를 두지 않는다. "모든 국민은 인간으로서의
존엄과 가치를 가진다" — 여기에 단서 조항은 없다.
SOUL.md는 AI Agent에게 **헌법적 수준의 원칙**을
부여한 최초의 사례다.

모호한 표현은 악용의 틈이 된다. "가능한 한 프라이버시를
보호한다"는 "상황에 따라 보호하지 않을 수 있다"와 같다.
"Period"는 이 틈을 물리적으로 봉쇄한다.

## 관련 문서

- [OpenClaw README](./README.md)
- [ClawWork](./clawwork.md)
- [One Human + One Agent](../ai/one-human-one-agent.md)
- [soul.md 에세이](../ai/soul-md.md)
