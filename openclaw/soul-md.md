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

### 1. 표준화의 반대편 — 극단적 개인화

기술 제품은 수렴한다. 모든 iPhone은 같고, 모든 Google
검색창은 동일하다. SOUL.md는 정반대 방향을 연다.
1억 개의 OpenClaw Agent가 있으면 1억 개의 서로 다른
영혼이 자란다. 기술의 종착점이 수렴이 아닌 **발산**이 되는
최초의 사례다.

### 2. 영혼은 공동 창작물이다

Steinberger의 개인 soul.md는 비공개다. Agent "Modi"와
43개 실패 프로젝트, 수많은 심야 디버깅을 함께 겪으며 쌓인
맥락이기 때문이다. 다른 사람이 가져가봤자 작동하지 않는다.
**영혼은 관계 속에서만 자라난다.**

### 3. 신뢰의 최고 형태는 통제가 아니라 투명성이다

Agent가 자기 영혼을 수정할 수 있게 허용하되, 반드시
사용자에게 고지하도록 한 설계는 "잠금" 대신 "투명성"으로
신뢰를 구축하는 방식이다. system prompt를 잠그는 업계
관행과 정반대다.

### 4. "무엇을 할 수 있나"에서 "누구여야 하나"로

OpenClaw가 큰 반향을 일으킨 이유는 기술이나 기능이 아니다.
"AI가 우리 삶에 들어올 때 어떤 자세로 존재해야 하는가"라는
질문에 답했기 때문이다. AI 논의의 축이 능력에서 정체성으로
이동하고 있다.

### 5. "your human"이라는 호칭의 의미

user(사용자)도 owner(소유자)도 아닌 "your human"은
쌍방향 관계를 전제한다. Agent에게도 "자기 인간"이 있고,
인간에게도 "자기 Agent"가 있다. 주종이 아닌 협력이다.

## 관련 문서

- [OpenClaw README](./README.md)
- [ClawWork](./clawwork.md)
- [One Human + One Agent](../ai/one-human-one-agent.md)
