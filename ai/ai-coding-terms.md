# AI 시대 코딩 용어 비교

바이브 코딩 그 너머의 지형도.

2025년 2월 카파시가 "바이브 코딩"이라는 말을 트윗으로 던졌고,
1년 뒤 스스로 그 용어를 넘어섰다.
그 사이 업계는 AI와 함께 코딩하는 행위에
서로 다른 이름을 붙이기 시작했다.

## 요약 비교표

| 용어                    | 제안자/출처      | 사람의 역할            | 코드 이해 |
|-------------------------|------------------|------------------------|-----------|
| Vibe Coding             | Karpathy         | 분위기로 지시          | 낮음      |
| Agentic Engineering     | Karpathy         | 에이전트 오케스트레이터 | 중간      |
| Augmented Coding        | Kent Beck        | 판단하는 개발자        | 높음      |
| AI-Assisted Engineering | Addy Osmani      | 70% AI + 30% 판단      | 높음      |
| Agentic Coding          | Anthropic/업계   | 목표 설정자            | 중간      |
| CHOP                    | Steve Yegge 등   | 대화로 코드를 이끔     | 중간      |
| Prompt-Driven Dev.      | 커뮤니티         | 프롬프트 설계자        | 중간      |
| Spec-Driven Dev.        | Thoughtworks 등  | 명세 작성자            | 높음      |
| AI Pair Programming     | GitHub/업계      | 능동적 코더            | 높음      |
| Centaur Coding          | 체스 메타포 차용 | 전략적 기수            | 높음      |

## 각 용어 정리

### 1. Vibe Coding — 바이브 코딩

Karpathy (2025.2).
코드를 읽지 않고 동작만 확인한다.
에러가 나면 메시지를 그대로 AI에게 되돌린다.
주말 프로젝트나 일회성 데모에 적합하며,
프로덕션 코드에는 부적합하다.
Collins English Dictionary 2025 올해의 단어.

### 2. Agentic Engineering — 에이전틱 엔지니어링

Karpathy (2026.2).
바이브 코딩 1주년에 직접 제안한 후속 용어.
99%의 시간 동안 직접 코드를 쓰지 않되,
에이전트를 오케스트레이션하고 감독한다.
테스트가 핵심이고,
사람이 아키텍처·품질·정확성을 소유한다.
"YOLO vs. 감독 하의 위임"으로 요약할 수 있다.

### 3. Augmented Coding — 증강 코딩

Kent Beck (2025).
AI를 쓰되 "깔끔한 코드"라는 가치관을 유지한다.
AI가 잘하는 흡입(기능 추가)과
못하는 호흡(리팩터링)의 비대칭이 핵심 통찰이다.
비전, 전략, 작업 분해, 피드백 루프 설계가
개발자의 핵심 역량이 된다.

### 4. AI-Assisted Engineering — AI 보조 엔지니어링

Addy Osmani — 『Beyond Vibe Coding』 (2025).
바이브 코딩과 전통적 엔지니어링 사이의 스펙트럼을
상황에 따라 조절하라는 실용적 접근이다.
AI에게 맡기는 70%(루틴 코드, 초안, 테스트)와
사람이 지키는 30%(아키텍처, 보안, 유지보수성)로 나눈다.

### 5. Agentic Coding — 에이전틱 코딩

Anthropic, Google Cloud, 업계 전반 (2025~).
에이전트가 코드를 쓰고, 테스트를 돌리고,
실패를 관찰하고, 수정해서 다시 시도하는
자율적 피드백 루프가 핵심이다.
Claude Code, Cursor Agent, Devin 등이 대표 도구.

### 6. CHOP — 대화형 프로그래밍

Steve Yegge 등 (2024).
Chat-Oriented Programming.
LLM과의 반복적 대화를 통해 코드를 작성한다.
바이브 코딩보다 의도적이고,
Spec-Driven Development보다는 자유롭다.

### 7. Prompt-Driven Development — 프롬프트 주도 개발

커뮤니티 (2025).
구조화된 프롬프트로 AI에게 코드 생성을 지시한다.
바이브 코딩과의 차이는 구조와 의도의 수준이다.
프롬프트에 구조를 부여하는 순간
이 영역에 들어선다.

### 8. Spec-Driven Development — 명세 주도 개발

Thoughtworks, Amazon Kiro, GitHub Spec-Kit (2025).
명세가 진실의 원천이고 코드는 파생물이다.
Spec-First, Spec-Anchored, Spec-as-Source의
세 가지 엄격도 수준이 있다.

### 9. AI Pair Programming — AI 페어 프로그래밍

GitHub Copilot (2021~), 업계 공통.
가장 오래되고 가장 넓은 우산 용어.
사람이 주도적으로 코드를 쓰고 AI가 제안·완성을 돕는다.
용어가 넓어서 구체적 방법론을 지칭하기 어렵다.

### 10. Centaur Coding — 켄타우로스 코딩

체스 프리스타일 메타포 차용 (2024~).
인간+컴퓨터 팀이 순수 인간이나 순수 컴퓨터를 이긴
체스의 교훈을 코딩에 적용한다.
핵심 원칙: 사람이 기수(rider)여야 한다.
승객이 되면 안 된다.

## 스펙트럼

AI 자율성 축으로 보면:

```text
사람이 직접 코드를 씀 ◀──────────▶ AI가 알아서 씀

AI Pair → Centaur → Augmented → AI-Assisted
→ CHOP → Spec-Driven → Prompt-Driven
→ Agentic Coding → Agentic Eng. → Vibe Coding
```

코드 품질 관심도 축으로 보면:

```text
품질 관심 높음 ◀──────────────▶ 품질 관심 낮음

Augmented → Spec-Driven → AI-Assisted → Centaur
→ Agentic Coding → CHOP → Prompt-Driven
→ Agentic Eng. → Vibe Coding
```

두 축을 교차하면 각 용어의 위치가 명확해진다.

## 카파시의 궤적

```text
2025.2                        2026.2
Vibe Coding ── (1년) ──▶ Agentic Engineering
"코드를 잊어라"           "에이전트를 감독하라"
```

같은 사람이 스펙트럼의 극단에서 중간으로 돌아왔다.
이 이동 자체가 업계의 학습 곡선을 압축해서 보여준다.

- 2025.2: LLM 능력 제한적 → 주말 프로젝트용 → 분위기로 충분.
- 2026.2: LLM이 강력해짐 → 프로 워크플로우 통합 가능
  → 감독과 엔지니어링 규율 필수.

## 참고 자료

- [Karpathy — Vibe Coding 원문 트윗](https://x.com/karpathy/status/1886192184808149383)
- [Karpathy — 2025 LLM Year in Review](https://karpathy.bearblog.dev/year-in-review-2025/)
- [Karpathy — Agentic Engineering 발표](https://thenewstack.io/vibe-coding-is-passe/)
- [Kent Beck — Augmented Coding: Beyond the Vibes](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes)
- [Addy Osmani — 『Beyond Vibe Coding』](https://beyond.addy.ie/)
- [Anthropic — 2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)
- [Thoughtworks — Spec-Driven Development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Google Cloud — What Is Agentic Coding](https://cloud.google.com/discover/what-is-agentic-coding)
- [Gradient Flow — Vibe Coding and CHOP](https://gradientflow.com/vibe-coding-and-chop-what-you-need-to-know/)
