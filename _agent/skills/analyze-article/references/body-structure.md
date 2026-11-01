# Section headings, body structure and templates (steps 5, 5a, 6)

## Contents

- [5. Choose the first section heading](#5-choose-the-first-section-heading)
- [5a. Choose the body structure — argue vs. teach (CRITICAL)](#5a-choose-the-body-structure-argue-vs-teach-critical)
- [6. Write the document](#6-write-the-document)

## 5. Choose the first section heading

The first top-level section depends on the same classification:

- **Article** → `## 요약` is the usual opening, but it is not the only one.
  Choose the heading that matches what the first section actually does: a
  piece that argues gets `## 요약`; a reference or a tutorial may open with
  `## 소개`, a long document may open with `## 목차`. The document's type
  decides, not a blanket rule.
- **Non-article** → do NOT use `## 요약`. Choose a heading that fits what the
  section actually covers — e.g. `## 소개`, `## 명세`, `## 사용법`,
  `## 주요 기능`, `## CLI`. A single subject may warrant multiple top-level
  sections if its content naturally splits.

What is fixed is not the name of the opening section but the body structure
step 5a selects. Getting `## 요약` versus `## 소개` slightly wrong is a matter
of fit; shipping a document that was supposed to carry the analytical body and
carries only half of it is a defect.

## 5a. Choose the body structure — argue vs. teach (CRITICAL)

**The body structure follows the source's own job. Do not impose an analytical
structure on a source whose job is to teach a task.**

Decide which of these the source is, then use the matching body:

- **The source argues.** It advances a thesis, takes a position, reports an
  event with a frame, or reviews something. Blog posts, essays, news stories,
  papers, opinion pieces, most conference talks.
  → Body is `## 분석` → `## 비평` → `## 인사이트`, in that order, 비평
  immediately after 분석 and 인사이트 last. This is the default.

- **The source teaches.** Its job is to let the reader do a task: reference
  documentation, an API guide, a specification, a tutorial, a runbook, a tool's
  usage docs. The useful note is one the reader can work from, not one that
  critiques the manual's prose.
  → Body is practical. Choose headings that fit the task — e.g. `## 동작 방식`,
  `## 설정하기`, `## 구현하기`, `## 값 정하기`, `## 트레이드오프`,
  `## 체크리스트`, `## 함정`. Cover: how it actually works, what to decide and
  on what basis, what the trade-offs cost on each side, what goes wrong in
  practice, and how to verify. End with a short `## 기억할 원칙` when there is a
  transferable principle worth stating.

**The analytical body is all-or-nothing.** If you pick it, the document
carries `## 분석`, `## 비평` and `## 인사이트`, all three, in that order. A
document that analyses and then offers insights without ever challenging the
source is the most common way this structure fails, and 비평 is the section
that makes the note worth more than the source. Half the structure is a
defect, not a lighter version of it. The format gate in step 8b enforces this:
once `## 분석` appears, all three must appear, in that order.

A practical note is free to borrow one of these headings without owing the
other two. When a teaching source carries a strong claim worth contesting, a
single `## 비평` among practical sections is welcome; a practical note may
likewise close with `## 인사이트` instead of `## 기억할 원칙`. What marks a
document as analytical — and therefore owing all three — is `## 분석`.

When genuinely torn, ask what the reader will do with the note. If they will
*think differently*, the source argues. If they will *build something*, it
teaches.

**Trade-offs are where a teaching note earns its keep.** A table of "what you
gain / what you give up" in one line each is too thin. Show why the obvious fix
does not work, what breaks when you pick each side, and what you cannot have at
all. Name the difficulty, not just the cost.

## 6. Write the document

Two templates follow: one for a source that **argues**, one for a source that
**teaches**. Pick the one step 5a selected. **The `원문:` line and `## 요약`
heading shown apply to ARTICLES ONLY — for non-articles, substitute per steps
4 and 5.**

### 6a. Template — the source argues

```markdown
# <한국어 제목>

원문: [<원문 제목>](<URL>)

## 요약

Summarize the core content in 3-5 paragraphs.
Convey technical details accurately — preserve numbers, names, and
technical terms. Do not editorialize; save judgment for later sections.

## 분석

Analyze the logical structure and context. Go beyond restating what the
article says — ask WHY the argument is structured this way, WHAT it
assumes, and WHERE it connects to broader trends.

Each sub-section (###) should make a distinct analytical point:
- What is the article's core claim, and what does it rest on?
- What historical or technical context explains why this matters now?
- What structural pattern does this represent — and where else does it
  appear?
- What does the author take for granted that deserves scrutiny?

Aim for 3–4 sub-sections. Each sub-section is 2–4 paragraphs.
Do NOT list observations — build an argument within each sub-section.

## 비평

Do NOT use "강점 / 약점" sub-headings. A list of pros and cons is not
critique — it is a summary with opinions attached.

Real critique means: identify a specific flaw in the article's logic,
generalizability, omissions, or framing — and develop that flaw into a
substantive argument with evidence or counter-examples. Each sub-section
targets one such flaw.

Frame sub-headings as focused critical claims, not generic categories:

Good examples:
- "글의 논리는 성공 조건을 숨긴다"
- "저자가 인식하고도 답하지 않은 문제"
- "이 워크플로는 특정 맥락에서만 성립한다"
- "결론의 일반화는 근거 없이 확장된다"

Bad examples (forbidden):
- "강점"
- "약점"
- "한계"
- "긍정적 측면 / 부정적 측면"

Aim for 3–4 sub-sections of 3–5 paragraphs each. The critique must be
harder and sharper than the analysis — find the places where the article
fails to hold up under scrutiny.

## 인사이트

Insights are the most important section. They must offer something the
reader could NOT have obtained by reading the source alone.

Each insight (###) must be developed over 3–5 paragraphs. The sub-heading
names the insight as a declarative claim — not a question or topic label.

Mandatory coverage across the insights:
- A second-order effect or consequence the article does not anticipate
- A historical analogy or structural pattern that reframes the issue
- A tension or trade-off the article glosses over but that will matter
  at scale or over time

What to avoid:
- Restating the article's own conclusions as insights
- Surface-level observations ("this is an important trend")
- Insights that follow directly from the article without adding a new
  frame

Write at least 3 insights. 4 is better if the subject warrants it.
```

### 6b. Template — the source teaches

Headings here are examples, not a fixed set. Choose ones that match the task
and drop any that do not apply. What matters is that the reader can act from
the note.

```markdown
# <한국어 제목>

원문: [<원문 제목>](<URL>)

## <첫 섹션: 요약 또는 소개>

Pick per step 5. A non-article never uses `## 요약`.

What this is and what contract it offers. For a spec or reference, state the
guarantee and its exact boundary — what it promises, and what it explicitly
does not.

## 동작 방식

How it actually works, in enough depth that the reader can predict behavior
rather than memorize steps. Walk a concrete scenario in order (a timeline, a
request path, a state transition) when the mechanism is easy to misread.

## <구현하기 / 설정하기>

What the reader does. Include real, runnable code or commands — not fragments
that only illustrate. Comment the lines that encode a decision. Name the
values that must be chosen and what each one depends on.

## 값 정하기

Starting values with the reasoning behind each, in a table. A starting value
without its basis is unusable, because the reader cannot tell when to change
it. Add what to measure so the value can be revised from evidence.

## 트레이드오프

The heart of a teaching note. For each decision, show what you gain, what it
costs, AND what remains hard afterward. Give each significant trade-off its
own sub-section when one line cannot carry it: why the obvious fix fails,
what breaks on each side, what cannot be had at all. A two-column
gain/loss table alone is too thin.

## 함정

Failure modes that show up in practice but not in the source. What looks
correct and is not, what only breaks under load or at scale, what the source
assumes but never states.

## <확인하기>

How to verify locally — a reproducible experiment, a command sequence, a
minimal setup. A note the reader can run beats one they can only read.

## 체크리스트

Checkable items for before shipping or reviewing. Write each so the answer is
yes or no, not "consider X."

## 기억할 원칙

Only when a transferable principle is genuinely there. One or two, each with
a `###` sub-heading and a few paragraphs. Skip this section rather than pad
it.
```
