# AI 시대 코딩 용어 비교

카파시가 2025.2에 "바이브 코딩"을 던지고,
2026.2에 스스로 넘어섰다.
그 1년 사이 업계가 붙인 이름 10개를 비교한다.

## 비교표

| 용어                    | 제안자          | 핵심 한 줄                           |
|-------------------------|-----------------|--------------------------------------|
| Vibe Coding             | Karpathy        | 코드를 잊어라. 동작만 봐라.          |
| Agentic Engineering     | Karpathy        | 에이전트를 감독하라. 테스트가 핵심.  |
| Augmented Coding        | Kent Beck       | AI를 쓰되 깔끔한 코드를 포기 마라.   |
| AI-Assisted Eng.        | Addy Osmani     | 70% AI, 30% 사람의 판단.             |
| Agentic Coding          | Anthropic/업계  | 에이전트가 쓰고 테스트하고 고친다.   |
| CHOP                    | Steve Yegge     | 대화로 코드를 이끌어낸다.            |
| Prompt-Driven Dev.      | 커뮤니티        | 구조화된 프롬프트가 코드를 낳는다.   |
| Spec-Driven Dev.        | Thoughtworks    | 명세가 원천, 코드는 파생물.          |
| AI Pair Programming     | GitHub/업계     | AI가 짝. 가장 넓은 우산 용어.        |
| Centaur Coding          | 체스 메타포     | 기수(rider)가 돼라. 승객이 되지 마라. |

## 용어별 핵심 통찰

**Vibe Coding** (2025.2) —
diff도 안 읽고, Accept All만 누른다.
주말 프로젝트용. 카파시 본인이 못 박았다.

**Agentic Engineering** (2026.2) —
바이브 코딩의 후속. YOLO에서 감독 하의 위임으로.
테스트 스위트 없으면 에이전트는
깨진 코드를 "완료"라고 선언한다.

**Augmented Coding** —
AI의 비대칭: 흡입(기능 추가)은 잘하고,
호흡(리팩터링)은 못한다.
이 비대칭이 복잡도를 쌓아
결국 AI 자신의 한계를 초과하게 만든다.

**AI-Assisted Engineering** —
바이브 코딩과 전통 엔지니어링 사이에 슬라이더가 있다.
상황에 따라 옮겨라.

**Agentic Coding** —
자율적 피드백 루프가 핵심.
단, 개발자가 "완전 위임" 가능하다고
느끼는 비율은 0~20%에 불과하다(Anthropic 2026).

**CHOP** (2024) —
바이브 코딩보다 의도적이고,
명세 주도보다 자유롭다.

**Prompt-Driven Development** —
프롬프트에 구조를 부여하는 순간
바이브 코딩을 졸업한다.

**Spec-Driven Development** —
코드가 1차 산출물이라는 전제를 뒤집는다.
Spec-First → Spec-Anchored → Spec-as-Source.

**AI Pair Programming** (2021~) —
용어가 너무 넓어서 방법론을 특정할 수 없다.
바이브 코딩도, 증강 코딩도 이 우산 안에 들어간다.

**Centaur Coding** —
인간+컴퓨터가 순수 인간과 순수 컴퓨터를 모두 이긴
체스의 교훈.

## 스펙트럼

```text
사람이 직접 씀 ◀────────────────▶ AI가 알아서 씀

AI Pair → Centaur → Augmented → AI-Assisted
→ CHOP → Spec → PDD → Agentic Coding
→ Agentic Eng. → Vibe Coding
```

```text
품질 관심 높음 ◀────────────────▶ 품질 관심 낮음

Augmented → Spec → AI-Assisted → Centaur
→ Agentic Coding → CHOP → PDD
→ Agentic Eng. → Vibe Coding
```

Kent Beck의 증강 코딩은 자율성 중간, 품질 최상위.
바이브 코딩은 자율성 최고, 품질 무관심도 최고.

## 카파시의 궤적

```text
2025.2                        2026.2
Vibe Coding ── (1년) ──▶ Agentic Engineering
"코드를 잊어라"           "에이전트를 감독하라"
```

같은 사람이 극단에서 중간으로 돌아왔다.
이 이동이 업계의 학습 곡선을 압축해서 보여준다.

- 2025: LLM 제한적 → 분위기로 충분.
- 2026: LLM 강력 → 감독과 규율 필수.

## 참고 자료

- [Karpathy — Vibe Coding](https://twitter.com/karpathy/status/1886192184808149383)
- [Karpathy — Agentic Engineering](https://thenewstack.io/vibe-coding-is-passe/)
- [Kent Beck — Augmented Coding](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes)
- [Addy Osmani — Beyond Vibe Coding](https://beyond.addy.ie/)
- [Anthropic — Agentic Coding Trends 2026](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)
- [Thoughtworks — Spec-Driven Dev.](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Gradient Flow — CHOP](https://gradientflow.com/vibe-coding-and-chop-what-you-need-to-know/)
